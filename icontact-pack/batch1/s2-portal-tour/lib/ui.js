// Shared pieces for the screen videos: a phone, invented "Example" websites, a timer ring, ticks.
// All business names and details are invented, per the pack's rules.
import { clamp, prog, ease, lerp } from './kit.js';

export const TICK = '<svg viewBox="0 0 24 24" fill="none" stroke="#abcf47" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.2 4.2L19 7"/></svg>';
export const WA = '<svg width="22" height="22" viewBox="0 0 32 32"><path d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3z" fill="#fff"/></svg>';

export function phone(inner, { label = true } = {}) {
  return `<div class="phone"><div class="screen"><div class="notch"></div><div class="status"><span>9:41</span><span>●●● 5G</span></div>
    <div class="scroller">${inner}</div></div>${label ? '<div class="label-example" style="left:28px;top:-20px">Example</div>' : ''}</div>`;
}

/** a clean, well-built small-business site (invented) */
export function goodSite() {
  return `
  <div class="mk-nav"><div class="mk-logo">Example <i>Plumbing</i></div><div class="mk-burger"></div></div>
  <div class="mk-hero" data-hl="what">
    <h1 class="mk-h1">Plumbers in Harare. Same-day call-outs.</h1>
    <p class="mk-p">Burst pipes, geysers, blocked drains and bathroom fittings.</p>
    <div class="mk-row" data-hl="contact"><span class="mk-btn">${WA} WhatsApp us</span><span class="mk-btn alt">Call now</span></div>
  </div>
  <div class="mk-sec" data-hl="where">
    <h2 class="mk-h2">Where we work</h2>
    <div class="mk-li"><b>●</b> Avondale, Borrowdale and Mount Pleasant</div>
    <div class="mk-li"><b>●</b> Harare CBD and surrounding suburbs</div>
  </div>
  <div class="mk-sec"><h2 class="mk-h2">Services</h2>
    <div class="mk-li"><b>1</b> Geyser repairs and installs</div><div class="mk-li"><b>2</b> Burst and leaking pipes</div><div class="mk-li"><b>3</b> Blocked drains</div></div>
  <div class="mk-sec"><div class="mk-img"></div></div>`;
}

/** the same business, badly built: tiny text, a huge image, the contact button buried */
export function badSite() {
  return `
  <div style="padding:10px 14px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #eee">
    <div style="font:700 11px var(--f-ui);color:#999">EXAMPLE PLUMBING (PVT) LTD — WELCOME TO OUR OFFICIAL WEBSITE</div><div class="mk-burger" style="transform:scale(.6)"></div></div>
  <div style="height:420px;background:linear-gradient(135deg,#7a8a99,#b8c2cc 50%,#8f9aa6);display:grid;place-items:center;color:#fff;font:300 13px var(--f-ui);letter-spacing:.3em">WELCOME</div>
  <div style="padding:12px 14px;font:400 9.5px/1.5 var(--f-ui);color:#aaa">We are a leading provider of quality solutions committed to excellence and customer satisfaction since our establishment. Our mission is to deliver value through innovation and integrity across all of our diverse service offerings and products for clients.</div>
  <div style="padding:6px 14px;font:400 9.5px/1.5 var(--f-ui);color:#bbb">Our vision is to be the preferred partner for all of your needs. Please browse our website to learn more about our company history, values and team.</div>
  <div style="padding:14px;text-align:right"><span style="font:400 9px var(--f-ui);color:#ccc;border:1px solid #eee;padding:4px 6px">contact</span></div>`;
}

/** timer ring: 0–10 s, turns green at 10 */
export function timerHTML() {
  return `<div class="timer" id="timer"><svg viewBox="0 0 120 120"><circle cx="60" cy="60" r="52" fill="rgba(14,20,27,0.85)" stroke="rgba(255,255,255,0.15)" stroke-width="8"/>
    <circle id="tarc" cx="60" cy="60" r="52" fill="none" stroke="#f2f5f9" stroke-width="8" stroke-linecap="round" transform="rotate(-90 60 60)" stroke-dasharray="326.7" stroke-dashoffset="326.7"/></svg>
    <div class="tnum"><span id="tnum">0</span><small>sec</small></div></div>`;
}
export const timerCSS = `.timer{position:absolute;width:210px;height:210px;z-index:6}.timer svg{width:100%;height:100%}
  .tnum{position:absolute;inset:0;display:grid;place-content:center;text-align:center;font:800 78px/0.9 var(--f);font-variant-numeric:tabular-nums}
  .tnum small{font:600 20px var(--f-ui);letter-spacing:.2em;text-transform:uppercase;color:var(--muted)}`;
export function setTimer(s) {
  const v = clamp(s, 0, 10);
  document.getElementById('tnum').textContent = Math.floor(v + 1e-6);
  const arc = document.getElementById('tarc');
  arc.style.strokeDashoffset = String(326.7 * (1 - v / 10));
  arc.style.stroke = v >= 10 ? '#abcf47' : '#f2f5f9';
}

/** smooth scroll of a phone's page to y (px) between t0 and t0+d */
export function scrollTo(scroller, t, keys) {
  // keys: [[time, y], ...] with eased moves between them
  let y = keys[0][1];
  for (let i = 1; i < keys.length; i++) {
    const [t0, y0] = keys[i - 1], [t1, y1] = keys[i];
    if (t >= t0) y = lerp(y0, y1, ease.inOut(prog(t, t0, t1 - t0)));
  }
  scroller.style.transform = `translateY(${-y}px)`;
}

/** an outline that draws around an element in the phone at time `at` */
export function highlight(el, t, at, color = '#abcf47') {
  const p = ease.out(prog(t, at, 0.4));
  el.style.boxShadow = p > 0 ? `inset 0 0 0 ${4 * p}px ${color}` : 'none';
  el.style.borderRadius = '10px';
}
