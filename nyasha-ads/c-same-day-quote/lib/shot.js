// One shot, mostly declared in its HTML:
//   .photo img[data-from][data-to][data-fx][data-fy][data-tilt]  the render, pushed in over the shot
//   [data-rise="s"] [data-pop="s"]                                 comes in at s seconds
//   [data-out="s"]                                                 fades out at s seconds
//   [data-on="s"]                                                  gets class "on" from s seconds
//   [data-fit="px"]                                                font shrunk from px until it fits its box
// `extra(t)` draws whatever else the shot does.
import { $, $$, cover, push, rise, pop, leave, fit, loaded } from './kit.js';

export function shot(duration, extra = () => {}, setup = () => {}) {
  const img = $('.photo img');
  let geo = null;
  window.film = {
    duration,
    ready: loaded(() => {
      if (img) geo = cover(img, img.parentElement);
      for (const el of $$('[data-fit]')) fit(el, { max: Number(el.dataset.fit) || 76, min: 44 });
      setup();
    }),
    frame(t) {
      if (img && geo) {
        const d = img.dataset;
        push(img, geo, t, duration, {
          from: Number(d.from ?? 1), to: Number(d.to ?? 1.08),
          fx: Number(d.fx ?? 0.5), fy: Number(d.fy ?? 0.4), tilt: Number(d.tilt ?? 0),
        });
      }
      for (const el of $$('[data-rise]')) rise(el, t, Number(el.dataset.rise));
      for (const el of $$('[data-pop]')) pop(el, t, Number(el.dataset.pop));
      for (const el of $$('[data-out]')) leave(el, t, Number(el.dataset.out));
      for (const el of $$('[data-on]')) el.classList.toggle('on', t >= Number(el.dataset.on));
      extra(t);
    },
  };
}
