// Shared motion helpers for the Nyasha shots. Every function sets the picture from t alone (no state).

export const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
/** 0 → 1 over [start, start + dur] */
export const prog = (t, start, dur) => (dur <= 0 ? (t >= start ? 1 : 0) : clamp((t - start) / dur));
export const lerp = (a, b, p) => a + (b - a) * p;
export const ease = {
  out: (x) => 1 - Math.pow(1 - x, 3),
  inOut: (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2),
  sine: (x) => -(Math.cos(Math.PI * x) - 1) / 2,
  back: (x) => { const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); },
};

/** fade + slide up in */
export function rise(el, t, start, dur = 0.5, dy = 46) {
  const p = ease.out(prog(t, start, dur));
  el.style.opacity = p;
  el.style.transform = `translateY(${(1 - p) * dy}px)`;
}
/** springy scale in */
export function pop(el, t, start, dur = 0.5, from = 0.5) {
  const x = prog(t, start, dur);
  el.style.opacity = clamp(x * 4);
  el.style.transform = `scale(${x === 0 ? from : lerp(from, 1, ease.back(x))})`;
}
/** fade out */
export function leave(el, t, start, dur = 0.3) {
  const p = prog(t, start, dur);
  if (p > 0) el.style.opacity = String(Number(el.style.opacity || 1) * (1 - p));
}
/** a gentle pulse, period in seconds */
export const pulse = (t, period = 1.1, amt = 0.05) => 1 + amt * (0.5 - 0.5 * Math.cos((2 * Math.PI * t) / period));

/** typing: the first n characters of text, as of t */
export function typed(el, text, t, start, cps = 18, caret = true) {
  const n = Math.floor(Math.max(0, t - start) * cps);
  const shown = text.slice(0, n);
  const typing = t >= start && n < text.length;
  el.textContent = shown + (caret && typing && Math.floor(t * 3) % 2 === 0 ? '|' : '');
}

/**
 * A render placed to cover its .photo box (with a margin so the renders' rounded white corners never show),
 * pushed in from `from` to `to` over the shot, centred on (fx, fy) of the picture (0–1).
 */
export function cover(img, box) {
  const { naturalWidth: w, naturalHeight: h } = img;
  const bw = box.clientWidth, bh = box.clientHeight;
  const s = Math.max(bw / w, bh / h) * 1.04;
  img.style.width = `${w * s}px`;
  img.style.height = `${h * s}px`;
  return { w: w * s, h: h * s, bw, bh };
}
export function push(img, geo, t, dur, { from = 1.0, to = 1.1, fx = 0.5, fy = 0.4, tilt = 0 } = {}) {
  const p = ease.sine(clamp(t / dur));
  const s = lerp(from, to, p);
  // keep the focal point at the same place on the box, clamped so the edges never show
  const left = clamp(geo.bw / 2 - fx * geo.w, geo.bw - geo.w, 0);
  const top = clamp(geo.bh * 0.42 - fy * geo.h, geo.bh - geo.h, 0);
  img.style.left = `${left}px`;
  img.style.top = `${top}px`;
  img.style.transformOrigin = `${fx * 100}% ${fy * 100}%`;
  img.style.transform = `scale(${s}) rotate(${tilt * Math.sin(Math.PI * p)}deg)`;
}

/** shrink a block's font until it fits its box (once, while loading) */
export function fit(el, { max = 76, min = 48 } = {}) {
  let size = max;
  el.style.fontSize = `${size}px`;
  while (size > min && (el.scrollHeight > el.clientHeight + 1 || el.scrollWidth > el.clientWidth + 1)) {
    size -= 2;
    el.style.fontSize = `${size}px`;
  }
}

/** fonts and every <img> decoded; then `then` (layout that needs sizes) */
export function loaded(then = () => {}) {
  const weights = ['500', '600', '700', '800'];
  return Promise.all([
    ...weights.map((w) => document.fonts.load(`${w} 40px Poppins`)),
    document.fonts.load('italic 600 40px Poppins'),
    ...[...document.images].map((i) => (i.complete && i.naturalWidth ? Promise.resolve() : i.decode())),
  ]).then(() => document.fonts.ready).then(then);
}

export const $ = (s) => document.querySelector(s);
export const $$ = (s) => [...document.querySelectorAll(s)];
