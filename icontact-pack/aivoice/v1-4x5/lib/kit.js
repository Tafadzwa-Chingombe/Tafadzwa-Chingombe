// iContact production-pack film kit: motion helpers and the shot wrapper. Every picture is set from t alone (no state).

export const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
/** 0 → 1 over [start, start + dur] */
export const prog = (t, start, dur) => (dur <= 0 ? (t >= start ? 1 : 0) : clamp((t - start) / dur));
export const lerp = (a, b, p) => a + (b - a) * p;
export const ease = {
  out: (x) => 1 - Math.pow(1 - x, 3),
  out5: (x) => 1 - Math.pow(1 - x, 5),
  in: (x) => x * x * x,
  inOut: (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2),
  sine: (x) => -(Math.cos(Math.PI * x) - 1) / 2,
  back: (x) => { const c1 = 1.7, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); },
};
export const $ = (s) => document.querySelector(s);
export const $$ = (s) => [...document.querySelectorAll(s)];

/** seeded random numbers (mulberry32) */
export function rng(seed) {
  let a = seed >>> 0;
  return () => {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let r = Math.imul(a ^ (a >>> 15), 1 | a);
    r = (r + Math.imul(r ^ (r >>> 7), 61 | r)) ^ r;
    return ((r ^ (r >>> 14)) >>> 0) / 4294967296;
  };
}
/** a stable pseudo-random number for (i, salt) */
export const hash = (i, salt = 0) => { const x = Math.sin(i * 127.1 + salt * 311.7) * 43758.5453; return x - Math.floor(x); };

/** fade + slide up, with a little motion blur */
export function rise(el, t, start, dur = 0.6, dy = 60) {
  const p = ease.out(prog(t, start, dur));
  el.style.opacity = p;
  el.style.transform = `translateY(${(1 - p) * dy}px)`;
  el.style.filter = p < 1 ? `blur(${(1 - p) * 10}px)` : 'none';
}
/** springy scale in */
export function pop(el, t, start, dur = 0.55, from = 0.6) {
  const x = prog(t, start, dur);
  el.style.opacity = clamp(x * 4);
  el.style.transform = `scale(${x === 0 ? from : lerp(from, 1, ease.back(x))})`;
}
/** letters of a word slam in one after another (el's text split into spans once, in setup) */
export function splitLetters(el) {
  // whole words stay together (each an unbreakable box of letter spans); <br> and spaces are kept
  const walk = (node) => {
    for (const child of [...node.childNodes]) {
      if (child.nodeType === 3) {
        const frag = document.createDocumentFragment();
        child.textContent.split(/(\s+)/).forEach((part) => {
          if (!part) return;
          if (/^\s+$/.test(part)) { frag.append(document.createTextNode(' ')); return; }
          const w = document.createElement('span'); w.style.display = 'inline-block'; w.style.whiteSpace = 'nowrap';
          for (const ch of part) { const s = document.createElement('span'); s.className = 'ltr'; s.textContent = ch; s.style.display = 'inline-block'; w.append(s); }
          frag.append(w);
        });
        child.replaceWith(frag);
      } else if (child.nodeType === 1 && child.tagName !== 'BR') walk(child);
    }
  };
  walk(el);
}
export function letters(el, t, start, gap = 0.035, dur = 0.45) {
  [...el.querySelectorAll('.ltr')].forEach((s, i) => {
    const p = ease.out5(prog(t, start + i * gap, dur));
    s.style.opacity = clamp(p * 2);
    s.style.transform = `translateY(${(1 - p) * 0.6}em) rotate(${(1 - p) * 8}deg)`;
    s.style.filter = p < 1 ? `blur(${(1 - p) * 8}px)` : 'none';
  });
}
/** camera: a slow push-in (and drift) on a wrapper, plus a whip-in over the first 0.4 s of the shot */
export function camera(el, t, dur, { from = 1.0, to = 1.08, dx = 0, dy = 0, whip = 'up', rot = 0 } = {}) {
  const p = ease.sine(clamp(t / dur));
  const s = lerp(from, to, p);
  const w = whip ? 1 - ease.out5(prog(t, 0, 0.42)) : 0;
  const wx = whip === 'left' ? -w * 220 : whip === 'right' ? w * 220 : 0;
  const wy = whip === 'up' ? w * 260 : whip === 'down' ? -w * 260 : 0;
  el.style.transform = `translate(${dx * p + wx}px, ${dy * p + wy}px) scale(${s + w * 0.08}) rotate(${rot * p}deg)`;
  el.style.filter = w > 0.01 ? `blur(${w * 26}px)` : 'none';
}
/** a short shake (impact) */
export const shake = (t, at, amt = 14, dur = 0.35) => {
  const p = prog(t, at, dur); if (p <= 0 || p >= 1) return [0, 0];
  const k = (1 - p) * amt; return [Math.sin(t * 90) * k, Math.cos(t * 77) * k];
};

/** shrink a block's font until it fits its box (once, while loading) */
export function fit(el, { max = 96, min = 40 } = {}) {
  let size = max;
  el.style.fontSize = `${size}px`;
  while (size > min && (el.scrollHeight > el.clientHeight + 4 || el.scrollWidth > el.clientWidth + 4)) { size -= 2; el.style.fontSize = `${size}px`; }
}

/** fonts and every <img> decoded; then `then` */
export function loaded(then = () => {}) {
  return Promise.all([
    ...['400', '500', '600', '700', '800'].map((w) => document.fonts.load(`${w} 40px Poppins`)),
    ...['400', '500', '600', '700'].map((w) => document.fonts.load(`${w} 40px Inter`)),
    ...[...document.images].map((i) => (i.complete && i.naturalWidth ? Promise.resolve() : i.decode())),
  ]).then(() => document.fonts.ready).then(then);
}

export const W = () => window.innerWidth;
export const H = () => window.innerHeight;
export const vertical = () => window.innerHeight > window.innerWidth * 1.3;

/**
 * One shot. Declared in HTML:
 *   .cam                 the camera wrapper (push-in + whip-in)  data-from data-to data-dx data-dy data-whip
 *   [data-rise] [data-pop] [data-letters]   enters at s seconds
 *   [data-out]           fades out at s seconds    [data-on] gets class "on" from s
 *   [data-fit]           font shrunk from px until it fits
 * `extra(t)` draws the rest; `setup()` runs once, after loading.
 */
export function shot(duration, extra = () => {}, setup = () => {}) {
  window.film = {
    duration,
    ready: loaded(() => {
      for (const el of $$('[data-fit]')) fit(el, { max: Number(el.dataset.fit) || 96 });
      for (const el of $$('[data-letters]')) splitLetters(el);
      return setup();
    }),
    frame(t) {
      for (const el of $$('.cam')) {
        const d = el.dataset;
        camera(el, t, duration, { from: Number(d.from ?? 1), to: Number(d.to ?? 1.08), dx: Number(d.dx ?? 0), dy: Number(d.dy ?? 0), whip: d.whip ? (d.whip === 'none' ? null : d.whip) : null, rot: Number(d.rot ?? 0) });
      }
      for (const el of $$('[data-rise]')) rise(el, t, Number(el.dataset.rise));
      for (const el of $$('[data-pop]')) pop(el, t, Number(el.dataset.pop));
      for (const el of $$('[data-letters]')) letters(el, t, Number(el.dataset.letters));
      for (const el of $$('[data-out]')) { const p = prog(t, Number(el.dataset.out), 0.35); if (p > 0) el.style.opacity = String(Number(el.style.opacity || 1) * (1 - p)); }
      for (const el of $$('[data-on]')) el.classList.toggle('on', t >= Number(el.dataset.on));
      return extra(t);
    },
  };
}

/** a gentle pulse, period in seconds */
export const pulse = (t, period = 1.1, amt = 0.05) => 1 + amt * (0.5 - 0.5 * Math.cos((2 * Math.PI * t) / period));

/** typing: the first n characters of text, as of t */
export function typed(el, text, t, start, cps = 18, caret = true) {
  const n = Math.floor(Math.max(0, t - start) * cps);
  const typing = t >= start && n < text.length;
  el.textContent = text.slice(0, n) + (caret && typing && Math.floor(t * 3) % 2 === 0 ? '|' : '');
}
