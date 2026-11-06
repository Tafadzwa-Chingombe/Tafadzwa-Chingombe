// AI Voice Agent explainer: the kit's shot() plus the pieces these scenes share. Every picture comes from t alone.
import { shot as kshot, prog, ease } from './kit.js';

/** size each screen (.art, drawn at data-w × data-h) to fit its .vis box, centred */
export function fitAll() {
  const w = innerWidth, h = innerHeight;
  document.documentElement.className = w > h ? 'L' : (h / w > 1.5 ? 'P' : 'S');
  for (const vis of document.querySelectorAll('.vis')) {
    for (const a of vis.querySelectorAll(':scope > .art')) {
      if (getComputedStyle(a).display === 'none') continue;
      const W = Number(a.dataset.w), H = Number(a.dataset.h);
      a.style.width = `${W}px`; a.style.height = `${H}px`;
      const s = Math.min(vis.clientWidth / W, vis.clientHeight / H, Number(a.dataset.max || 1.5));
      a.style.left = `${(vis.clientWidth - W * s) / 2}px`; a.style.top = `${(vis.clientHeight - H * s) / 2}px`;
      a.style.transform = `scale(${s})`;
    }
  }
}

export function shot(duration, extra = () => {}) {
  kshot(duration, (t) => {
    for (const el of document.querySelectorAll('[data-grow]')) {   // arrows draw themselves
      const p = ease.out(prog(t, Number(el.dataset.grow), 0.5));
      el.style.transform = `rotate(${el.dataset.rot || 0}deg) scaleX(${p})`; el.style.opacity = p > 0 ? '1' : '0';
    }
    for (const w of document.querySelectorAll('.wave')) {          // the voice bars move while someone talks
      const on = t >= Number(w.dataset.from || 0) && t < Number(w.dataset.to || 1e9);
      [...w.children].forEach((b, i) => {
        const k = on ? Math.abs(Math.sin(t * 7.3 + i * 1.7) * Math.sin(t * 3.1 + i * 0.9)) : 0;
        b.style.height = `${10 + k * (Number(w.dataset.amp || 44))}px`;
      });
    }
    for (const r of document.querySelectorAll('.ringwave')) {      // a ringing phone
      const ph = ((t + Number(r.dataset.off || 0)) % 1.4) / 1.4;
      r.style.transform = `scale(${1 + ph * 0.9})`; r.style.opacity = String((1 - ph) * 0.9);
    }
    return extra(t);
  }, fitAll);
}
