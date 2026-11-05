// A small business on a city street at dusk, drawn in code (no AI footage, no readable signs, no real places).
// drawStreet(ctx, t, opts) paints the whole frame from t alone; textures are built once by makeStreet().
import { rng, hash, clamp, lerp, ease, prog } from './kit.js';
import { plaster, offscreen } from './fx.js';

const GROUND = 1360;          // pavement line in the 1080×1920 frame
const OFFICE = { x: 230, w: 620, top: 560 };   // the business's two-storey building
const WIN = { x: 280, y: 1010, w: 420, h: 330 };   // ground-floor shop window
const DOOR = { x: 722, y: 1040, w: 104, h: 300 };
const SIGN = { x: 300, y: 930, w: 380, h: 56 };

export function makeStreet(W, H) {
  const r = rng(12);
  const tex = {
    office: plaster(OFFICE.w, GROUND - OFFICE.top, { color: '#cfc4b3', mottle: 0.25, grain: 10, seed: 3 }),
    left: plaster(300, 760, { color: '#9aa3ab', mottle: 0.3, grain: 10, seed: 5 }),
    right: plaster(300, 820, { color: '#b9a48e', mottle: 0.3, grain: 10, seed: 7 }),
  };
  // the far city: a row of rooftops with a few lit windows
  const far = offscreen(W, 700), f = far.getContext('2d');
  let x = -40;
  while (x < W + 40) {
    const w = 90 + r() * 170, h = 220 + r() * 380;
    f.fillStyle = `rgb(${22 + r() * 10},${30 + r() * 12},${50 + r() * 14})`;
    f.fillRect(x, 700 - h, w, h);
    for (let wy = 700 - h + 20; wy < 690; wy += 34) for (let wx = x + 12; wx < x + w - 16; wx += 26)
      if (r() < 0.16) { f.fillStyle = `rgba(255,${190 + r() * 40},${110 + r() * 60},${0.5 + r() * 0.4})`; f.fillRect(wx, wy, 10, 14); }
    x += w + 6 + r() * 20;
  }
  // the interior seen through the window: warm light, a desk, a chair, shelves, a plant (silhouettes only)
  const inner = offscreen(WIN.w, WIN.h), n = inner.getContext('2d');
  let g = n.createRadialGradient(WIN.w * 0.42, WIN.h * 0.3, 10, WIN.w * 0.5, WIN.h * 0.5, WIN.w * 0.8);
  g.addColorStop(0, '#ffe2ad'); g.addColorStop(0.45, '#f0a85e'); g.addColorStop(1, '#7a3f1c');
  n.fillStyle = g; n.fillRect(0, 0, WIN.w, WIN.h);
  n.fillStyle = 'rgba(80,40,18,0.55)'; for (let i = 0; i < 4; i++) n.fillRect(250 + i * 8, 40 + i * 52, 150, 8);   // shelves
  n.fillStyle = 'rgba(60,30,14,0.8)'; n.fillRect(60, 210, 220, 18); n.fillRect(80, 228, 14, 100); n.fillRect(246, 228, 14, 100);   // desk
  n.fillStyle = 'rgba(40,22,10,0.85)'; n.beginPath(); n.roundRect(150, 150, 60, 70, 10); n.fill();   // monitor
  n.fillStyle = 'rgba(255,240,210,0.9)'; n.fillRect(156, 156, 48, 52);
  n.fillStyle = 'rgba(46,26,12,0.85)'; n.beginPath(); n.roundRect(300, 200, 60, 80, 12); n.fill(); n.fillRect(322, 280, 12, 50);   // chair
  n.fillStyle = 'rgba(30,50,20,0.85)'; for (let i = 0; i < 7; i++) { n.beginPath(); n.ellipse(30 + Math.cos(i) * 20, 170 - i * 14, 26, 12, i, 0, 7); n.fill(); }   // plant
  const lamp = n.createRadialGradient(120, 60, 2, 120, 60, 140); lamp.addColorStop(0, 'rgba(255,250,225,0.9)'); lamp.addColorStop(1, 'rgba(255,220,160,0)');
  n.fillStyle = lamp; n.fillRect(0, 0, WIN.w, WIN.h);
  return { tex, far, inner };
}

function figure(ctx, x, ground, s, phase, { phone = false, dir = 1, rim = 'rgba(255,190,120,0.35)' } = {}) {
  // a silhouetted person walking; phase drives the stride
  ctx.save(); ctx.translate(x, ground); ctx.scale(s * dir, s);
  const sw = Math.sin(phase) * 0.5, col = '#0a0e15';
  ctx.strokeStyle = col; ctx.lineCap = 'round';
  ctx.lineWidth = 32;   // legs
  ctx.beginPath(); ctx.moveTo(0, -190); ctx.lineTo(Math.sin(sw) * 90, 0); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(0, -190); ctx.lineTo(-Math.sin(sw) * 90, 0); ctx.stroke();
  ctx.fillStyle = col; ctx.beginPath();   // a coat: narrow at the shoulders, wider at the hem
  ctx.moveTo(-30, -385); ctx.quadraticCurveTo(0, -398, 30, -385); ctx.lineTo(46, -160); ctx.quadraticCurveTo(0, -150, -46, -160); ctx.closePath(); ctx.fill();
  ctx.lineWidth = 18;   // arms
  if (phone) { ctx.beginPath(); ctx.moveTo(18, -350); ctx.lineTo(42, -280); ctx.lineTo(20, -320); ctx.stroke(); }
  else { ctx.beginPath(); ctx.moveTo(0, -350); ctx.lineTo(-Math.sin(sw) * 60, -230); ctx.stroke(); }
  ctx.beginPath(); ctx.moveTo(0, -350); ctx.lineTo(Math.sin(sw) * 60, -230); ctx.stroke();
  ctx.beginPath(); ctx.arc(phone ? 8 : 0, -415, 34, 0, 7); ctx.fill();   // head
  ctx.strokeStyle = rim; ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(phone ? 8 : 0, -415, 34, -1.9, -0.2); ctx.stroke();
  if (phone) {
    ctx.fillStyle = 'rgba(200,225,255,0.95)'; ctx.fillRect(16, -330, 26, 40);
    const g = ctx.createRadialGradient(28, -340, 2, 28, -360, 90); g.addColorStop(0, 'rgba(170,205,255,0.45)'); g.addColorStop(1, 'rgba(170,205,255,0)');
    ctx.fillStyle = g; ctx.fillRect(-80, -460, 200, 200);
  }
  ctx.restore();
}

/**
 * light: 0–1, the business's lights (and how present it looks); sign: 0–1; door: 0–1 open;
 * passer: x position (or null) of a passer-by on their phone; client: x of someone walking to the door (or null)
 */
export function drawStreet(ctx, t, S, { light = 1, sign = 1, door = 0, passer = null, client = null, clientScale = 1 } = {}) {
  const W = ctx.canvas.width, H = ctx.canvas.height;
  // sky: deep blue above, the last orange at the horizon
  let g = ctx.createLinearGradient(0, 0, 0, 900);
  g.addColorStop(0, '#0b1830'); g.addColorStop(0.55, '#24365a'); g.addColorStop(0.85, '#7b5a5c'); g.addColorStop(1, '#d88a52');
  ctx.fillStyle = g; ctx.fillRect(0, 0, W, 900);
  ctx.save(); ctx.filter = 'blur(2px)'; ctx.drawImage(S.far, 0, 200); ctx.restore();
  // neighbours: shuttered, dark
  ctx.drawImage(S.tex.left, -70, GROUND - 760); ctx.drawImage(S.tex.right, OFFICE.x + OFFICE.w, GROUND - 820);
  ctx.fillStyle = 'rgba(12,20,36,0.72)'; ctx.fillRect(-70, GROUND - 760, 300, 760); ctx.fillRect(OFFICE.x + OFFICE.w, GROUND - 820, 300, 820);
  ctx.fillStyle = 'rgba(40,46,56,0.9)';   // roller shutters
  ctx.fillRect(-40, GROUND - 330, 250, 330); ctx.fillRect(OFFICE.x + OFFICE.w + 30, GROUND - 330, 240, 330);
  ctx.fillStyle = 'rgba(255,255,255,0.05)'; for (let y = GROUND - 330; y < GROUND; y += 12) { ctx.fillRect(-40, y, 250, 2); ctx.fillRect(OFFICE.x + OFFICE.w + 30, y, 240, 2); }
  // the business's building
  ctx.drawImage(S.tex.office, OFFICE.x, OFFICE.top);
  g = ctx.createLinearGradient(0, OFFICE.top, 0, GROUND);
  g.addColorStop(0, 'rgba(14,22,40,0.65)'); g.addColorStop(1, 'rgba(14,22,40,0.25)');
  ctx.fillStyle = g; ctx.fillRect(OFFICE.x, OFFICE.top, OFFICE.w, GROUND - OFFICE.top);
  for (let i = 0; i < 3; i++) {   // upper windows: dark glass, one softly lit
    const wx = OFFICE.x + 50 + i * 190, wy = OFFICE.top + 90;
    ctx.fillStyle = i === 1 ? `rgba(255,200,130,${0.15 + 0.35 * light})` : 'rgba(10,16,28,0.85)'; ctx.fillRect(wx, wy, 130, 170);
    ctx.strokeStyle = 'rgba(0,0,0,0.5)'; ctx.lineWidth = 6; ctx.strokeRect(wx, wy, 130, 170);
  }
  // the blank sign panel (no lettering), lit from above
  ctx.fillStyle = `rgba(25,40,70,${0.95})`; ctx.fillRect(SIGN.x, SIGN.y, SIGN.w, SIGN.h);
  ctx.fillStyle = `rgba(171,207,71,${0.9 * sign})`; ctx.fillRect(SIGN.x + 20, SIGN.y + 22, 40, 12); ctx.fillRect(SIGN.x + 70, SIGN.y + 22, 180, 12);
  g = ctx.createLinearGradient(0, SIGN.y - 30, 0, SIGN.y + SIGN.h); g.addColorStop(0, `rgba(255,230,190,${0.35 * sign})`); g.addColorStop(1, 'rgba(255,230,190,0)');
  ctx.fillStyle = g; ctx.fillRect(SIGN.x - 20, SIGN.y - 30, SIGN.w + 40, SIGN.h + 30);
  // the shop window: the interior, dimmed with `light`
  ctx.drawImage(S.inner, WIN.x, WIN.y);
  ctx.fillStyle = `rgba(8,14,26,${0.92 * (1 - light)})`; ctx.fillRect(WIN.x, WIN.y, WIN.w, WIN.h);
  g = ctx.createLinearGradient(WIN.x, WIN.y, WIN.x + WIN.w, WIN.y + WIN.h); g.addColorStop(0, 'rgba(255,255,255,0.12)'); g.addColorStop(0.4, 'rgba(255,255,255,0)'); g.addColorStop(0.55, 'rgba(255,255,255,0.08)'); g.addColorStop(0.6, 'rgba(255,255,255,0)');
  ctx.fillStyle = g; ctx.fillRect(WIN.x, WIN.y, WIN.w, WIN.h);
  ctx.strokeStyle = '#1b222c'; ctx.lineWidth = 12; ctx.strokeRect(WIN.x, WIN.y, WIN.w, WIN.h); ctx.lineWidth = 7; ctx.beginPath(); ctx.moveTo(WIN.x + WIN.w / 2, WIN.y); ctx.lineTo(WIN.x + WIN.w / 2, WIN.y + WIN.h); ctx.stroke();
  // the door: opens into the light
  ctx.fillStyle = '#1b222c'; ctx.fillRect(DOOR.x - 8, DOOR.y - 8, DOOR.w + 16, DOOR.h + 8);
  ctx.fillStyle = `rgba(255,${200 + 30 * light},${140 + 40 * light},${(0.25 + 0.75 * light) * Math.max(door, 0.12)})`; ctx.fillRect(DOOR.x, DOOR.y, DOOR.w, DOOR.h);
  ctx.fillStyle = '#2a333f'; ctx.fillRect(DOOR.x + DOOR.w * door * 0.85, DOOR.y, DOOR.w * (1 - door * 0.85), DOOR.h);
  // the whole building sinks into the dusk when the lights go
  ctx.fillStyle = `rgba(14,22,40,${0.62 * (1 - light)})`; ctx.fillRect(OFFICE.x, OFFICE.top, OFFICE.w, GROUND - OFFICE.top);
  // pavement and road
  g = ctx.createLinearGradient(0, GROUND, 0, H); g.addColorStop(0, '#2a2f38'); g.addColorStop(0.25, '#1a1e25'); g.addColorStop(1, '#0c0e12');
  ctx.fillStyle = g; ctx.fillRect(0, GROUND, W, H - GROUND);
  ctx.fillStyle = 'rgba(255,255,255,0.06)'; ctx.fillRect(0, GROUND + 120, W, 6);   // kerb
  ctx.save(); ctx.filter = 'blur(18px)';   // warm spill and reflection from the window
  ctx.fillStyle = `rgba(255,190,110,${0.38 * light})`; ctx.beginPath(); ctx.ellipse(WIN.x + WIN.w / 2, GROUND + 60, WIN.w * 0.7, 70, 0, 0, 7); ctx.fill();
  ctx.fillStyle = `rgba(255,190,110,${0.22 * light})`; ctx.fillRect(WIN.x + 40, GROUND + 140, WIN.w - 80, 300);
  ctx.restore();
  // street lamps
  for (const lx of [110, 985]) {
    ctx.fillStyle = '#0d1118'; ctx.fillRect(lx - 7, 720, 14, GROUND - 700);
    ctx.fillRect(lx - 40, 712, 80, 14);
    const lg = ctx.createRadialGradient(lx, 740, 4, lx, 760, 260); lg.addColorStop(0, 'rgba(255,224,170,0.85)'); lg.addColorStop(0.15, 'rgba(255,200,140,0.35)'); lg.addColorStop(1, 'rgba(255,200,140,0)');
    ctx.fillStyle = lg; ctx.fillRect(lx - 260, 500, 520, 520);
  }
  // people
  if (passer != null) figure(ctx, passer, GROUND + 230, 0.95, t * 7, { phone: true, dir: 1 });
  if (client != null) figure(ctx, client, GROUND + 40 + 190 * (1 - clientScale), clientScale, t * 6.5, { dir: -1 });
  // haze and a few out-of-focus lights in front
  ctx.save(); ctx.filter = 'blur(10px)';
  for (let i = 0; i < 9; i++) { const bx = hash(i, 4) * W, by = 1500 + hash(i, 5) * 380, br = 20 + hash(i, 6) * 40; ctx.fillStyle = `rgba(255,${170 + hash(i, 7) * 60},120,${0.12 + 0.1 * hash(i, 8)})`; ctx.beginPath(); ctx.arc(bx + Math.sin(t * 0.3 + i) * 10, by, br, 0, 7); ctx.fill(); }
  ctx.restore();
}

export const SCENE = { GROUND, OFFICE, WIN, DOOR, SIGN };
