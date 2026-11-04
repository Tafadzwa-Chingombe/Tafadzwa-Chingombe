// Procedural "footage" for the Parker films: plaster walls, cracks, peeling paint, sun and leaf shadows,
// rain, drops, a paint pour and a roller. Textures are built once (seeded); frames are drawn from t alone.
import { rng, hash, clamp, lerp, ease, prog } from './kit.js';

export function canvasFor(el, scale = 1) {
  const c = el; c.width = Math.round(window.innerWidth * scale); c.height = Math.round(window.innerHeight * scale);
  return c.getContext('2d');
}
export function offscreen(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; }

const hex = (h) => { const n = parseInt(h.slice(1), 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; };

/** multi-octave value noise as a grey canvas (upscaled random tiles) */
function noiseLayer(w, h, r, octaves = [[6, 0.5], [24, 0.3], [96, 0.2]]) {
  const out = offscreen(w, h), o = out.getContext('2d');
  o.fillStyle = '#808080'; o.fillRect(0, 0, w, h);
  for (const [cells, amt] of octaves) {
    const tw = Math.max(2, Math.round(cells)), th = Math.max(2, Math.round(cells * h / w));
    const tile = offscreen(tw, th), tc = tile.getContext('2d'), id = tc.createImageData(tw, th);
    for (let i = 0; i < tw * th; i++) { const v = Math.round(r() * 255); id.data.set([v, v, v, 255], i * 4); }
    tc.putImageData(id, 0, 0);
    o.globalAlpha = amt; o.imageSmoothingEnabled = true; o.imageSmoothingQuality = 'high';
    o.drawImage(tile, 0, 0, w, h);
  }
  o.globalAlpha = 1;
  return out;
}

/**
 * A plaster wall: base colour, mottled noise, fine grain. Options:
 *   color '#d8cbb4', mottle 0.35 (how blotchy), grain 18 (per-pixel speckle), seed
 *   aged: faded patches, cracks, peeling flakes showing grey cement, water stains
 */
export function plaster(w, h, { color = '#d9ccb6', mottle = 0.35, grain = 18, seed = 1, aged = false, smooth = false } = {}) {
  const r = rng(seed);
  const c = offscreen(w, h), x = c.getContext('2d');
  x.fillStyle = color; x.fillRect(0, 0, w, h);
  const n = noiseLayer(w, h, r, smooth ? [[5, 0.6], [20, 0.4]] : [[6, 0.45], [28, 0.3], [140, 0.25]]);
  x.globalCompositeOperation = 'overlay'; x.globalAlpha = mottle; x.drawImage(n, 0, 0);
  x.globalCompositeOperation = 'source-over'; x.globalAlpha = 1;
  // per-pixel grain (sand in the plaster)
  const id = x.getImageData(0, 0, w, h), d = id.data;
  for (let i = 0; i < d.length; i += 4) {
    const g = (r() - 0.5) * grain * (r() < 0.02 ? 3 : 1);
    d[i] += g; d[i + 1] += g; d[i + 2] += g;
  }
  x.putImageData(id, 0, 0);
  if (aged) age(x, w, h, r);
  return c;
}

function age(x, w, h, r) {
  // water stains running down from the top and sun-bleached patches
  for (let i = 0; i < 7; i++) {
    const sx = r() * w, sw = 60 + r() * 180, len = h * (0.25 + r() * 0.5);
    const g = x.createLinearGradient(0, 0, 0, len);
    g.addColorStop(0, 'rgba(70,58,40,0.28)'); g.addColorStop(1, 'rgba(70,58,40,0)');
    x.fillStyle = g; x.filter = 'blur(14px)';
    x.beginPath(); x.moveTo(sx, 0);
    for (let y = 0; y <= len; y += 40) x.lineTo(sx + Math.sin(y / 90 + i) * 18 + (y / len) * sw * 0.2, y);
    x.lineTo(sx + sw, len); x.lineTo(sx + sw, 0); x.fill();
  }
  x.filter = 'blur(40px)';
  for (let i = 0; i < 9; i++) { x.fillStyle = `rgba(255,250,240,${0.12 + r() * 0.12})`; x.beginPath(); x.ellipse(r() * w, r() * h, 80 + r() * 220, 60 + r() * 160, r() * 3, 0, 7); x.fill(); }
  x.filter = 'none';
  // peeling flakes: cement shows through, the curled edge catches the light
  for (let i = 0; i < 16; i++) {
    const cx = r() * w, cy = r() * h, rad = 10 + r() * (i < 3 ? 80 : 34);
    const pts = []; const k = 9 + Math.floor(r() * 6);
    for (let j = 0; j < k; j++) { const a = (j / k) * Math.PI * 2, rr = rad * (0.55 + r() * 0.6); pts.push([cx + Math.cos(a) * rr, cy + Math.sin(a) * rr * 0.8]); }
    const path = () => { x.beginPath(); pts.forEach(([px, py], j) => (j ? x.lineTo(px, py) : x.moveTo(px, py))); x.closePath(); };
    x.save(); path(); x.clip();
    const cg = x.createLinearGradient(cx - rad, cy - rad, cx + rad, cy + rad); cg.addColorStop(0, '#a39b8c'); cg.addColorStop(1, '#7f786c');
    x.fillStyle = cg; x.fillRect(cx - rad * 2, cy - rad * 2, rad * 4, rad * 4);
    for (let s = 0; s < rad * 14; s++) { const v = 95 + r() * 80; x.fillStyle = `rgb(${v},${v - 4},${v - 10})`; x.fillRect(cx - rad + r() * rad * 2, cy - rad + r() * rad * 2, 2, 2); }
    x.restore();
    x.save(); path(); x.strokeStyle = 'rgba(255,255,255,0.55)'; x.lineWidth = 3; x.shadowColor = 'rgba(0,0,0,0.55)'; x.shadowBlur = 6; x.shadowOffsetY = 4; x.stroke(); x.restore();
  }
  // cracks: branching random walks, dark core with a lit lower lip
  for (let i = 0; i < 6; i++) crack(x, r() * w, r() * h * 0.9, Math.PI * (0.35 + r() * 0.3), 220 + r() * 420, 3.6, r, 0);
}

function crack(x, sx, sy, a, len, width, r, depth) {
  let px = sx, py = sy;
  const seg = [];
  for (let s = 0; s < len; s += 7) { a += (r() - 0.5) * 0.7; px += Math.cos(a) * 7; py += Math.sin(a) * 7; seg.push([px, py]); }
  const stroke = (col, lw, oy) => { x.beginPath(); x.moveTo(sx, sy + oy); seg.forEach(([qx, qy]) => x.lineTo(qx, qy + oy)); x.strokeStyle = col; x.lineWidth = lw; x.lineCap = 'round'; x.stroke(); };
  stroke('rgba(255,255,255,0.35)', width + 1.5, 2);
  stroke('rgba(45,34,24,0.7)', width, 0);
  if (depth < 1) for (let b = 0; b < 2; b++) { const [bx, by] = seg[Math.floor(r() * seg.length)] || [sx, sy]; crack(x, bx, by, a + (r() - 0.5) * 2.4, len * 0.4, width * 0.55, r, depth + 1); }
}

/** a wall drawn with a camera: scale about (fx, fy) */
export function drawWall(ctx, tex, s = 1, fx = 0.5, fy = 0.5, ox = 0, oy = 0) {
  const w = ctx.canvas.width, h = ctx.canvas.height;
  const dw = tex.width * s, dh = tex.height * s;
  ctx.drawImage(tex, (w - dw) * fx + ox, (h - dh) * fy + oy, dw, dh);
}

/** raking sunlight: warm wash from one corner, plus moving leaf shadows (a tree outside frame) */
export function sunlight(ctx, t, { strength = 1, leaves = 1, seed = 3 } = {}) {
  const w = ctx.canvas.width, h = ctx.canvas.height;
  const g = ctx.createLinearGradient(w * 1.1, -h * 0.1, 0, h);
  g.addColorStop(0, `rgba(255,214,150,${0.55 * strength})`); g.addColorStop(0.55, `rgba(255,190,120,${0.12 * strength})`); g.addColorStop(1, `rgba(40,20,10,${0.35 * strength})`);
  ctx.globalCompositeOperation = 'soft-light'; ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
  ctx.globalCompositeOperation = 'source-over';
  if (leaves > 0) {
    ctx.save(); ctx.filter = 'blur(22px)'; ctx.fillStyle = `rgba(60,36,18,${0.2 * leaves})`;
    for (let i = 0; i < 90; i++) {
      const cl = Math.floor(i / 15), bx = (hash(cl, seed + 9) * 1.1 - 0.05) * w + (hash(i, seed) - 0.5) * w * 0.35, by = hash(cl, seed + 8) * h * 0.55 + (hash(i, seed + 1) - 0.5) * h * 0.18;
      const sway = Math.sin(t * 1.3 + hash(i, seed + 2) * 6) * 14 + Math.sin(t * 0.4) * 22;
      ctx.beginPath(); ctx.ellipse(bx + sway, by + sway * 0.4, 18 + hash(i, seed + 3) * 46, 9 + hash(i, seed + 4) * 20, hash(i, seed + 5) * 3, 0, 7); ctx.fill();
    }
    ctx.restore();
  }
}

/** dust motes drifting in the sun */
export function dust(ctx, t, n = 70, seed = 9, alpha = 0.6) {
  const w = ctx.canvas.width, h = ctx.canvas.height;
  for (let i = 0; i < n; i++) {
    const x = (hash(i, seed) * w + t * (8 + hash(i, seed + 1) * 20) + Math.sin(t * 0.7 + i) * 20) % w;
    const y = (hash(i, seed + 2) * h - t * (4 + hash(i, seed + 3) * 12) + h * 4) % h;
    const r = 1 + hash(i, seed + 4) * 3.2, a = alpha * (0.3 + 0.7 * hash(i, seed + 5)) * (0.6 + 0.4 * Math.sin(t * 2 + i));
    const g = ctx.createRadialGradient(x, y, 0, x, y, r * 2.5);
    g.addColorStop(0, `rgba(255,240,210,${a})`); g.addColorStop(1, 'rgba(255,240,210,0)');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r * 2.5, 0, 7); ctx.fill();
  }
}

/** falling rain streaks; `near` adds a few big out-of-focus drops in front */
export function rain(ctx, t, { n = 380, speed = 2600, angle = 0.12, alpha = 0.5, seed = 5, near = true } = {}) {
  const w = ctx.canvas.width, h = ctx.canvas.height;
  ctx.save(); ctx.lineCap = 'round';
  for (let i = 0; i < n; i++) {
    const z = 0.35 + hash(i, seed) * 0.65;
    const len = 40 + z * 90, v = speed * z;
    const y = ((hash(i, seed + 1) * (h + 400) + t * v) % (h + 400)) - 200;
    const x = hash(i, seed + 2) * (w + 300) - 150 + y * angle;
    ctx.strokeStyle = `rgba(210,225,240,${alpha * z})`; ctx.lineWidth = 0.8 + z * 1.6;
    ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + len * angle, y + len); ctx.stroke();
  }
  if (near) {
    ctx.filter = 'blur(5px)';
    for (let i = 0; i < 14; i++) {
      const v = speed * 1.6, y = ((hash(i, seed + 7) * (h + 600) + t * v) % (h + 600)) - 300, x = hash(i, seed + 8) * w + y * angle;
      ctx.strokeStyle = 'rgba(230,240,255,0.35)'; ctx.lineWidth = 7; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + 200 * angle, y + 200); ctx.stroke();
    }
  }
  ctx.restore();
}

/** water running down a wall: darkened wet trails that grow with t, each with a bead at its head */
export function wetTrails(ctx, t, { n = 26, seed = 11, start = 0, grow = 260, beads = true, sheen = 'rgba(255,255,255,0.5)', trail = 'rgba(40,32,22,0.28)' } = {}) {
  const w = ctx.canvas.width, h = ctx.canvas.height;
  for (let i = 0; i < n; i++) {
    const t0 = start + hash(i, seed) * 2.2; if (t < t0) continue;
    const x0 = hash(i, seed + 1) * w, y0 = hash(i, seed + 2) * h * 0.5;
    const len = (t - t0) * (grow * (0.6 + hash(i, seed + 3) * 0.8));
    const pts = [];
    for (let y = 0; y <= len; y += 12) pts.push([x0 + Math.sin((y0 + y) / 70 + i) * 6 + Math.sin((y0 + y) / 23 + i * 3) * 2, y0 + y]);
    if (pts.length < 2) continue;
    ctx.save(); ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    ctx.strokeStyle = trail; ctx.lineWidth = 9 + hash(i, seed + 4) * 8;
    ctx.beginPath(); pts.forEach(([x, y], j) => (j ? ctx.lineTo(x, y) : ctx.moveTo(x, y))); ctx.stroke();
    ctx.strokeStyle = sheen; ctx.lineWidth = 1.6; ctx.globalAlpha = 0.5;
    ctx.beginPath(); pts.forEach(([x, y], j) => (j ? ctx.lineTo(x - 2, y) : ctx.moveTo(x - 2, y))); ctx.stroke();
    ctx.restore();
    if (beads) { const [bx, by] = pts[pts.length - 1]; bead(ctx, bx, by, 7 + hash(i, seed + 5) * 6); }
  }
}

/** a glossy water bead */
export function bead(ctx, x, y, r) {
  ctx.save();
  ctx.fillStyle = 'rgba(0,0,0,0.22)'; ctx.beginPath(); ctx.ellipse(x + r * 0.25, y + r * 0.45, r, r * 1.1, 0, 0, 7); ctx.fill();
  const g = ctx.createRadialGradient(x - r * 0.35, y - r * 0.45, r * 0.1, x, y, r * 1.15);
  g.addColorStop(0, 'rgba(255,255,255,0.95)'); g.addColorStop(0.25, 'rgba(255,255,255,0.35)'); g.addColorStop(0.7, 'rgba(160,180,200,0.18)'); g.addColorStop(1, 'rgba(255,255,255,0.55)');
  ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(x, y, r, r * 1.12, 0, 0, 7); ctx.fill();
  ctx.restore();
}

/** a lightning flash: brightness 0–1 at t */
export const flash = (t, at) => { const d = t - at; if (d < 0 || d > 0.6) return 0; return (d < 0.06 ? 1 : d < 0.12 ? 0.25 : d < 0.18 ? 0.8 : 0) + Math.max(0, 0.35 - d) * 0.6; };

/**
 * Thick paint poured from above into a pool (macro, slow motion).
 * cx: stream x; top: where the stream enters; poolY: the pool's surface; color: the paint.
 */
export function pour(ctx, t, { cx, top = 0, poolY, color = '#1c55e0', width = 64, start = 0, maxPool = 1e9 } = {}) {
  const w = ctx.canvas.width, h = ctx.canvas.height;
  const [R, G, B] = hex(color);
  const shade = (k, a = 1) => `rgba(${Math.round(R * k)},${Math.round(G * k)},${Math.round(B * k)},${a})`;
  const lt = (k, a = 1) => `rgba(${Math.round(R + (255 - R) * k)},${Math.round(G + (255 - G) * k)},${Math.round(B + (255 - B) * k)},${a})`;
  const head = top + (poolY - top) * ease.in(clamp((t - start) / 0.9)) ; // the stream's leading end falls in first
  const landed = t - start - 0.9;
  // pool
  const poolR = landed > 0 ? Math.min(maxPool, 40 + Math.sqrt(landed) * 330) : 0;
  if (poolR > 0) {
    const pg = ctx.createRadialGradient(cx - poolR * 0.2, poolY - poolR * 0.08, poolR * 0.05, cx, poolY, poolR);
    pg.addColorStop(0, lt(0.35)); pg.addColorStop(0.5, shade(1)); pg.addColorStop(1, shade(0.6));
    ctx.fillStyle = pg; ctx.beginPath(); ctx.ellipse(cx, poolY, poolR, poolR * 0.2, 0, 0, 7); ctx.fill();
    // ripples rolling out from the impact
    for (let k = 0; k < 5; k++) {
      const rr = ((landed * 160 + k * 70) % (poolR + 1));
      ctx.strokeStyle = lt(0.6, 0.35 * (1 - rr / poolR)); ctx.lineWidth = 3;
      ctx.beginPath(); ctx.ellipse(cx, poolY, rr, rr * 0.2, 0, Math.PI * 1.05, Math.PI * 1.95); ctx.stroke();
    }
    // the mound where the stream lands
    const mg = ctx.createRadialGradient(cx - 18, poolY - 26, 4, cx, poolY - 6, width * 1.3);
    mg.addColorStop(0, lt(0.55)); mg.addColorStop(1, shade(0.9, 0));
    ctx.fillStyle = mg; ctx.beginPath(); ctx.ellipse(cx, poolY - 8, width * 1.4, width * 0.5, 0, 0, 7); ctx.fill();
  }
  // the stream: a ribbon that wobbles and narrows as it falls
  const pts = [];
  for (let y = top; y <= head; y += 10) {
    const f = (y - top) / Math.max(1, poolY - top);
    const half = width * (1 - f * 0.45) * (0.92 + 0.08 * Math.sin(y / 37 - t * 9));
    const x = cx + Math.sin(y / 120 - t * 3) * 10 * f;
    pts.push([x, y, half]);
  }
  if (pts.length > 1) {
    const sg = ctx.createLinearGradient(cx - width, 0, cx + width, 0);
    sg.addColorStop(0, shade(0.55)); sg.addColorStop(0.28, lt(0.25)); sg.addColorStop(0.38, lt(0.75)); sg.addColorStop(0.5, shade(1)); sg.addColorStop(1, shade(0.5));
    ctx.fillStyle = sg; ctx.beginPath();
    pts.forEach(([x, y, hw], j) => (j ? ctx.lineTo(x - hw, y) : ctx.moveTo(x - hw, y)));
    for (let j = pts.length - 1; j >= 0; j--) ctx.lineTo(pts[j][0] + pts[j][2], pts[j][1]);
    ctx.closePath(); ctx.fill();
    // a rounded leading end while falling
    const [hx, hy, hw] = pts[pts.length - 1];
    if (landed <= 0) { ctx.beginPath(); ctx.ellipse(hx, hy, hw, hw * 1.2, 0, 0, Math.PI); ctx.fill(); }
    // specular streak sliding down the stream
    ctx.strokeStyle = 'rgba(255,255,255,0.7)'; ctx.lineWidth = 4; ctx.lineCap = 'round'; ctx.setLineDash([60, 110]); ctx.lineDashOffset = -t * 420;
    ctx.beginPath(); pts.forEach(([x, y, hw], j) => (j ? ctx.lineTo(x - hw * 0.35, y) : ctx.moveTo(x - hw * 0.35, y))); ctx.stroke(); ctx.setLineDash([]);
  }
  // a few droplets thrown out on impact
  if (landed > 0 && landed < 1.6) {
    for (let i = 0; i < 9; i++) {
      const a = Math.PI * (1.1 + hash(i, 4) * 0.8), v = 260 + hash(i, 5) * 260, tt = landed;
      const x = cx + Math.cos(a) * v * tt, y = poolY - 10 + Math.sin(a) * v * tt + 900 * tt * tt;
      if (y > poolY + 6) continue;
      const rr = 5 + hash(i, 6) * 9;
      const dg = ctx.createRadialGradient(x - rr * 0.3, y - rr * 0.3, 1, x, y, rr);
      dg.addColorStop(0, lt(0.7)); dg.addColorStop(1, shade(0.8));
      ctx.fillStyle = dg; ctx.beginPath(); ctx.arc(x, y, rr, 0, 7); ctx.fill();
    }
  }
}

/** a paint roller seen from the front, at (x, y) with head width `len` */
export function roller(ctx, x, y, len, color, t) {
  const [R, G, B] = hex(color);
  const r = len * 0.16;
  ctx.save();
  // handle: frame up to the grip, then down out of frame
  ctx.strokeStyle = '#c9ccd0'; ctx.lineWidth = len * 0.035; ctx.lineCap = 'round';
  ctx.beginPath(); ctx.moveTo(x + len / 2 + 6, y); ctx.lineTo(x + len / 2 + len * 0.1, y); ctx.lineTo(x + len * 0.12, y + len * 0.55); ctx.lineTo(x + len * 0.12, y + len * 0.9); ctx.stroke();
  ctx.strokeStyle = '#1b1d24'; ctx.lineWidth = len * 0.09; ctx.beginPath(); ctx.moveTo(x + len * 0.12, y + len * 0.9); ctx.lineTo(x + len * 0.12, y + len * 2.2); ctx.stroke();
  // the sleeve, wet with paint, rotating texture
  ctx.shadowColor = 'rgba(0,0,0,0.45)'; ctx.shadowBlur = 30; ctx.shadowOffsetY = 18;
  const g = ctx.createLinearGradient(0, y - r, 0, y + r);
  g.addColorStop(0, `rgb(${R * 0.55},${G * 0.55},${B * 0.55})`); g.addColorStop(0.3, `rgb(${Math.min(255, R * 1.15 + 30)},${Math.min(255, G * 1.15 + 30)},${Math.min(255, B * 1.15 + 30)})`);
  g.addColorStop(0.45, `rgb(${R},${G},${B})`); g.addColorStop(1, `rgb(${R * 0.4},${G * 0.4},${B * 0.4})`);
  ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x - len / 2, y - r, len, r * 2, r * 0.5); ctx.fill();
  ctx.shadowColor = 'transparent';
  ctx.globalAlpha = 0.25;
  for (let i = 0; i < 26; i++) { const yy = y - r + ((i * 9 + t * 600) % (r * 2)); ctx.fillStyle = i % 2 ? 'rgba(0,0,0,0.5)' : 'rgba(255,255,255,0.5)'; ctx.fillRect(x - len / 2 + 6, yy, len - 12, 2); }
  ctx.restore();
}

/** a freshly painted wall surface (fine orange-peel texture, soft sheen) */
export function freshPaint(w, h, color, seed = 21) {
  return plaster(w, h, { color, mottle: 0.05, grain: 5, seed, smooth: true });
}

/** film grain tiles: drawn once, picked by frame number */
export function grainTiles(n = 4, size = 512, seed = 77) {
  const r = rng(seed), tiles = [];
  for (let k = 0; k < n; k++) {
    const c = offscreen(size, size), x = c.getContext('2d'), id = x.createImageData(size, size);
    for (let i = 0; i < size * size; i++) { const v = Math.round(128 + (r() - 0.5) * 120); id.data.set([v, v, v, 255], i * 4); }
    x.putImageData(id, 0, 0); tiles.push(c);
  }
  return tiles;
}

/** a paint splat growing from (cx, cy) to radius R (organic edge, flung droplets) */
export function splat(ctx, cx, cy, R, color, seed = 1, p = 1) {
  if (R <= 0) return;
  ctx.save(); ctx.fillStyle = color; ctx.beginPath();
  const n = 72;
  for (let i = 0; i <= n; i++) {
    const a = (i / n) * Math.PI * 2;
    const k = 1 + 0.12 * Math.sin(a * 5 + seed) + 0.08 * Math.sin(a * 11 + seed * 2) + (hash(i % n, seed) > 0.86 ? 0.22 * hash(i % n, seed + 1) : 0);
    const x = cx + Math.cos(a) * R * k, y = cy + Math.sin(a) * R * k;
    i ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
  }
  ctx.fill();
  for (let i = 0; i < 26; i++) {
    const a = hash(i, seed + 3) * Math.PI * 2, d = R * (1.15 + hash(i, seed + 4) * 0.5) * Math.min(1, p * 1.2), r = R * 0.02 + hash(i, seed + 5) * R * 0.05;
    ctx.beginPath(); ctx.arc(cx + Math.cos(a) * d, cy + Math.sin(a) * d, r, 0, 7); ctx.fill();
  }
  ctx.restore();
}
