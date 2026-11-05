"""Original music and sound design for the Parker Paints films, synthesised in code (nothing to license).
  score_cinematic(length, marks)  slow, warm brand-film score: tension (sun, rain) → lift at the pour → groove → resolve
  score_punchy(length, marks)     120 bpm Afro-house groove for the fast motion-graphics cut, drop after the hook
  fx(kind, length=None)           whoosh, impact, boom, riser, rain, thunder, cicadas, roller, pour, shimmer, pop, ding, tick
marks: {'lift': s, 'drop': s, 'end': s} — film times the music turns on.
"""
import os, subprocess, wave
import numpy as np

SR = 44100


def R(seed): return np.random.default_rng(seed)

def env(n, a, d):
    t = np.arange(n) / SR; e = np.exp(-t / d); na = max(1, int(a * SR)); e[:na] *= np.linspace(0, 1, na); return e

def band(x, lo=None, hi=None):
    """FFT band filter with soft edges"""
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); g = np.ones_like(f)
    if lo: g *= 1 / (1 + (lo / np.maximum(f, 1)) ** 4)
    if hi: g *= 1 / (1 + (f / hi) ** 4)
    return np.fft.irfft(X * g, len(x))

def tone(freq, dur, partials=((1, 1.0),), a=0.005, d=0.3, detune=0.0):
    n = int(dur * SR); t = np.arange(n) / SR
    s = sum(amp * (np.sin(2 * np.pi * freq * k * t) + (np.sin(2 * np.pi * freq * k * (1 + detune) * t) if detune else 0)) for k, amp in partials)
    return s * env(n, a, d)

def pad(freq, dur, a=1.2, rel=1.5, bright=0.3):
    n = int(dur * SR); t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * freq * k * (1 + dt) * t + k) / k ** (1.6 - bright) for k in (1, 2, 3, 4) for dt in (-0.003, 0.0, 0.004))
    e = np.minimum(1, t / a) * np.minimum(1, np.maximum(0, (dur - t) / rel))
    return s * e / 6

def add(buf, x, at, gain=1.0):
    i = int(at * SR)
    if i >= len(buf) or i + len(x) <= 0: return
    if i < 0: x = x[-i:]; i = 0
    j = min(len(buf), i + len(x)); buf[i:j] += x[:j - i] * gain

def midi(m): return 440.0 * 2 ** ((m - 69) / 12)

def kick(tight=False):
    n = int(0.4 * SR); t = np.arange(n) / SR
    f = 42 + 90 * np.exp(-t / (0.03 if tight else 0.05))
    return np.tanh(1.6 * np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.14 if tight else 0.22))

def noise(n, seed): return R(seed).standard_normal(n)

def hat(seed=1, d=0.02):
    n = int(0.08 * SR); return band(noise(n, seed), lo=7000) * env(n, 0.001, d)

def clap(seed=2):
    n = int(0.3 * SR); x = band(noise(n, seed), lo=900, hi=6000); e = env(n, 0.001, 0.07)
    for k in (0.011, 0.022): e += np.roll(env(n, 0.001, 0.01), int(k * SR)) * 0.6
    return x * e

def shaker(seed=3):
    n = int(0.09 * SR); return band(noise(n, seed), lo=5000, hi=12000) * env(n, 0.015, 0.03)


def finish(L, Rr, length, fade_in=0.3, fade_out=1.8, drive=1.2, peak=0.7):
    n = int(length * SR); st = np.stack([L[:n], Rr[:n]], 1)
    st = np.tanh(st * drive)
    fi, fo = int(fade_in * SR), int(fade_out * SR)
    st[:fi] *= np.linspace(0, 1, fi)[:, None]; st[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
    return st / (np.max(np.abs(st)) + 1e-9) * peak


def score_cinematic(length, marks):
    """D major-ish brand score. 0 → lift: low drone, heartbeat, tension. lift → drop: warm pads open up.
    drop → end: soft four-on-the-floor groove, piano arpeggios. end: final chord and a long tail."""
    lift, drop, end = marks['lift'], marks['drop'], marks['end']
    L = np.zeros(int((length + 4) * SR)); Rr = np.zeros_like(L)
    bpm = 96; beat = 60 / bpm; bar = beat * 4
    # tension: a low drone with a slow filter swell, a heartbeat thud
    dr = pad(midi(38), lift + 1.5, a=2.5, rel=1.2, bright=0.1) * 0.22
    add(L, dr, 0); add(Rr, dr, 0)
    t = 0.6
    while t < lift - 0.3:
        k = kick() * 0.22; add(L, k, t); add(Rr, k, t); add(L, k * 0.6, t + 0.28); add(Rr, k * 0.6, t + 0.28); t += beat * 2
    # a reversed-swell riser into the lift
    rs = fx('riser', 2.2); add(L, rs[:, 0], lift - 2.2, 0.8); add(Rr, rs[:, 1], lift - 2.2, 0.8)
    # chords from the lift: Bm – G – D – A, then G – D – A – D
    chords = [(47, [62, 66, 71]), (43, [62, 67, 71]), (50, [62, 66, 69]), (45, [61, 64, 69]),
              (43, [59, 62, 67]), (50, [62, 66, 69]), (45, [61, 64, 69]), (50, [62, 66, 69, 74])]
    t, i = lift, 0
    while t < end:
        root, notes = chords[i % len(chords)]
        dur = min(bar, end - t) + 1.2
        for m in notes:
            p = pad(midi(m), dur, a=0.6 if t > lift else 0.2, rel=1.0, bright=0.35) * 0.06
            add(L, p, t); add(Rr, p * 0.92, t + 0.01)
        b = pad(midi(root - 12), dur, a=0.15, rel=0.6, bright=0.05) * 0.16
        add(L, b, t); add(Rr, b, t)
        if t >= drop - 0.01:
            # groove: kick on 1 and 3 (and 4 "and"), clap 2 and 4, shaker 8ths, piano arpeggio
            for q in (0, 2, 3.5): add(L, kick() * 0.5, t + q * beat); add(Rr, kick() * 0.5, t + q * beat)
            for q in (1, 3): c = clap(i * 7 + q) * 0.12; add(L, c, t + q * beat); add(Rr, c, t + q * beat + 0.006)
            for s in range(8): sh = shaker(i * 13 + s) * (0.05 if s % 2 else 0.03); add(L, sh * 0.7, t + s * beat / 2); add(Rr, sh, t + s * beat / 2)
            arp = [0, 1, 2, 1, 2, 0, 1, 2]
            for s, q in enumerate([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]):
                m = notes[arp[s] % len(notes)] + (12 if s in (3, 6) else 0)
                pl = tone(midi(m), 0.9, ((1, 1), (2, .3), (3, .12), (5, .04)), a=0.003, d=0.35) * 0.05
                pan = 0.3 + 0.4 * (s % 2); add(L, pl * (1 - pan), t + q * beat); add(Rr, pl * pan, t + q * beat)
        t += bar; i += 1
    # resolve: a big D chord on the end card, with a cymbal-ish swell and a low boom
    for m in (38, 50, 57, 62, 66, 69, 74):
        p = pad(midi(m), 5.0, a=0.05, rel=3.5, bright=0.4) * (0.08 if m > 45 else 0.2); add(L, p, end); add(Rr, p, end + 0.008)
    bm = fx('boom')[:, 0]; add(L, bm, end, 0.9); add(Rr, bm, end, 0.9)
    return finish(L, Rr, length, fade_out=2.2, drive=1.1)


def score_punchy(length, marks):
    """120 bpm: stuttered hits over the hook, a drop into the groove, a stop-down for the end card."""
    drop, end = marks['drop'], marks['end']
    L = np.zeros(int((length + 3) * SR)); Rr = np.zeros_like(L)
    bpm = 120; beat = 60 / bpm; bar = beat * 4
    # hook: filtered pulse + riser into the drop
    t = 0.0
    while t < drop - 0.05:
        b = tone(midi(33), beat * 0.45, ((1, 1), (2, .5)), a=0.004, d=0.12) * 0.25; add(L, b, t); add(Rr, b, t); t += beat / 2
    rs = fx('riser', min(2.5, drop)); add(L, rs[:, 0], drop - len(rs) / SR, 0.9); add(Rr, rs[:, 1], drop - len(rs) / SR, 0.9)
    chords = [(45, [64, 69, 72]), (41, [65, 69, 72]), (48, [64, 67, 72]), (43, [62, 67, 71])]   # Am F C G
    t, i = drop, 0
    while t < end:
        root, notes = chords[i % 4]
        for q in range(4): add(L, kick(True) * 0.6, t + q * beat); add(Rr, kick(True) * 0.6, t + q * beat)
        for q in (1, 3): c = clap(i * 5 + q) * 0.16; add(L, c, t + q * beat); add(Rr, c, t + q * beat)
        for s in range(16):
            h = hat(i * 31 + s, 0.015 if s % 2 == 0 else 0.03) * (0.06 if s % 4 == 2 else 0.035); add(L, h * 0.8, t + s * beat / 4); add(Rr, h, t + s * beat / 4)
        for off in (0, 0.75, 1.5, 2.5, 3, 3.5):   # syncopated bass
            bs = np.tanh(2.2 * tone(midi(root - 12), beat * 0.4, ((1, 1), (2, .4)), a=0.003, d=0.12)) * 0.2; add(L, bs, t + off * beat); add(Rr, bs, t + off * beat)
        for off in (0.5, 1.25, 2.0, 2.75, 3.5):   # plucky stabs
            for m in notes:
                st = tone(midi(m), 0.3, ((1, 1), (2, .5), (3, .25), (4, .12)), a=0.002, d=0.08) * 0.035; add(L, st, t + off * beat); add(Rr, st * 0.9, t + off * beat + 0.007)
        t += bar; i += 1
    for m in (45, 57, 64, 69, 72, 76):
        p = pad(midi(m), 3.5, a=0.02, rel=2.5, bright=0.5) * (0.08 if m > 50 else 0.18); add(L, p, end); add(Rr, p, end)
    bm = fx('impact')[:, 0]; add(L, bm, end, 0.8); add(Rr, bm, end, 0.8)
    return finish(L, Rr, length, fade_in=0.05, fade_out=1.6, drive=1.3)


def fx(kind, length=None):
    """a stereo (n, 2) array"""
    st = lambda x, y=None: np.stack([x, x if y is None else y], 1)
    if kind == 'whoosh':
        n = int((length or 0.55) * SR); t = np.arange(n) / SR; T = n / SR
        sh = np.sin(np.pi * np.minimum(1, t / T) ) ** 3
        x = band(noise(n, 11) * sh, lo=250, hi=3500); y = band(noise(n, 12) * sh, lo=250, hi=3500)
        pan = t / T
        m = max(np.max(np.abs(x)), 1e-9); return st(x * (1 - pan * 0.6) / m * 0.3, y * (0.4 + pan * 0.6) / m * 0.3)
    if kind == 'impact':
        n = int(1.4 * SR); t = np.arange(n) / SR
        f = 38 + 120 * np.exp(-t / 0.05); low = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.4)
        hit = band(noise(n, 21), lo=600, hi=9000) * env(n, 0.001, 0.05)
        x = np.tanh(1.4 * low) * 0.7 + hit * 0.35; return st(x)
    if kind == 'boom':
        n = int(3.0 * SR); t = np.arange(n) / SR
        f = 30 + 60 * np.exp(-t / 0.12); low = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.003, 1.0)
        return st(np.tanh(1.3 * low) * 0.6 + band(noise(n, 22), hi=400) * env(n, 0.01, 0.6) * 0.3)
    if kind == 'riser':
        n = int((length or 2.0) * SR); t = np.arange(n) / SR; T = n / SR
        e = (t / T) ** 2.2
        f = 200 + 1800 * (t / T) ** 2; tn = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.15
        x = band(noise(n, 31), lo=1500, hi=9000) * 0.6 + tn
        y = band(noise(n, 32), lo=1500, hi=9000) * 0.6 + tn
        return st(x * e * 0.35, y * e * 0.35)
    if kind == 'rain':
        n = int((length or 6) * SR)
        x = band(noise(n, 41), lo=400, hi=9000) * 0.18 + band(noise(n, 42), hi=300) * 0.12
        y = band(noise(n, 43), lo=400, hi=9000) * 0.18 + band(noise(n, 44), hi=300) * 0.12
        r = R(45)
        for _ in range(int(n / SR * 90)):   # close drops
            d = band(noise(int(0.02 * SR), r.integers(1e6)), lo=1500) * env(int(0.02 * SR), 0.0005, 0.004) * r.uniform(0.1, 0.5)
            i = r.integers(0, n - len(d)); (x if r.random() < 0.5 else y)[i:i + len(d)] += d
        fi = int(0.6 * SR); e = np.ones(n); e[:fi] = np.linspace(0, 1, fi); e[-fi:] = np.linspace(1, 0, fi)
        return st(x * e, y * e)
    if kind == 'thunder':
        n = int(4.5 * SR); t = np.arange(n) / SR
        crack = band(noise(n, 51), lo=300, hi=5000) * env(n, 0.002, 0.15) * 0.6
        roll = band(noise(n, 52), hi=180) * (np.minimum(1, t / 0.4) * np.exp(-t / 1.6)) * 3.0
        x = np.tanh(crack + roll); return st(x, np.roll(x, int(0.012 * SR)))
    if kind == 'cicadas':
        n = int((length or 6) * SR); t = np.arange(n) / SR
        car = np.sin(2 * np.pi * 4600 * t) + 0.5 * np.sin(2 * np.pi * 5200 * t)
        am = (0.5 + 0.5 * np.sin(2 * np.pi * 48 * t)) ** 3 * (0.6 + 0.4 * np.sin(2 * np.pi * 0.35 * t))
        air = band(noise(n, 61), lo=200, hi=2000) * 0.05
        fi = int(0.8 * SR); e = np.ones(n); e[:fi] = np.linspace(0, 1, fi); e[-fi:] = np.linspace(1, 0, fi)
        return st((car * am * 0.03 + air) * e, (np.roll(car * am, 900) * 0.03 + air) * e)
    if kind == 'roller':
        n = int((length or 2.4) * SR); t = np.arange(n) / SR
        wet = band(noise(n, 71), lo=200, hi=2500) * (0.55 + 0.45 * np.sin(2 * np.pi * 9 * t) ** 2)
        tack = band(noise(n, 72), lo=2500, hi=8000) * (np.sin(2 * np.pi * 18 * t) > 0.6) * 0.3
        fi = int(0.15 * SR); e = np.ones(n); e[:fi] = np.linspace(0, 1, fi); e[-fi:] = np.linspace(1, 0, fi)
        x = (wet * 0.35 + tack * 0.15) * e; return st(x)
    if kind == 'pour':
        n = int((length or 3.5) * SR); t = np.arange(n) / SR
        glug = band(noise(n, 81), lo=80, hi=700) * (0.6 + 0.4 * np.sin(2 * np.pi * 3.2 * t + np.sin(2 * np.pi * 0.7 * t) * 2))
        fi = int(0.4 * SR); e = np.ones(n); e[:fi] = np.linspace(0, 1, fi); e[-fi:] = np.linspace(1, 0, fi)
        x = glug * 0.5 * e; return st(x, np.roll(x, 300))
    if kind == 'shimmer':
        n = int(1.6 * SR); out = np.zeros(n)
        for k, m in enumerate((86, 90, 93, 98)):
            tt = tone(midi(m), 1.6 - k * 0.06, ((1, 1), (2.76, .2)), a=0.002, d=0.5) * 0.12; out[int(k * 0.06 * SR):][:len(tt)] += tt[:n - int(k * 0.06 * SR)]
        return st(out, np.roll(out, 600))
    if kind == 'pop':
        n = int(0.16 * SR); t = np.arange(n) / SR; f = 700 + 900 * (t / 0.16)
        return st(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.04) * 0.45)
    if kind == 'tick':
        n = int(0.05 * SR); return st(band(noise(n, 91), lo=2000) * env(n, 0.0005, 0.006) * 0.5)
    if kind == 'ding':
        a = tone(1318.5, 0.7, ((1, 1), (2.01, .2)), d=0.2) * 0.3; b = np.pad(tone(1760, 0.6, ((1, 1), (2.01, .2)), d=0.25), (int(0.09 * SR), 0))[:len(a)] * 0.3
        return st(a + b)
    if kind == 'stamp':
        n = int(0.9 * SR); t = np.arange(n) / SR
        thud = np.sin(2 * np.pi * np.cumsum(60 + 160 * np.exp(-t / 0.03)) / SR) * env(n, 0.001, 0.18)
        return st(np.tanh(2 * thud) * 0.6 + band(noise(n, 95), lo=500, hi=4000) * env(n, 0.001, 0.03) * 0.4)
    raise ValueError(kind)


def write_mp3(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + '.tmp.wav'; data = np.clip(data, -1, 1)
    if data.ndim == 1: data = np.stack([data, data], 1)
    with wave.open(tmp, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((data * 32767).astype('<i2').tobytes())
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-codec:a', 'libmp3lame', '-b:a', '192k', path], check=True)
    os.remove(tmp)


def score_calm(length, marks):
    """Calm, trustworthy bed for the screen videos: soft pads, a sparse piano-like pattern and a light pulse.
    Sits well below a voice. Resolves on the end card."""
    end = marks.get('end', length - 4)
    L = np.zeros(int((length + 4) * SR)); Rr = np.zeros_like(L)
    bpm = 92; beat = 60 / bpm; bar = beat * 4
    chords = [(48, [60, 64, 67, 71]), (45, [57, 60, 64, 67]), (41, [57, 60, 65, 69]), (43, [55, 59, 62, 67])]  # Cmaj7 Am7 Fmaj7 G
    t, i = 0.0, 0
    while t < length:
        root, notes = chords[i % 4]
        dur = min(bar, length - t) + 1.0
        for m in notes:
            p = pad(midi(m), dur, a=0.8, rel=1.2, bright=0.25) * 0.05; add(L, p, t); add(Rr, p * 0.94, t + 0.012)
        b = pad(midi(root - 12), dur, a=0.3, rel=0.8, bright=0.05) * 0.12; add(L, b, t); add(Rr, b, t)
        for s, q in enumerate([0, 1.5, 2, 3]):   # sparse "piano"
            m = notes[[0, 2, 1, 3][s]] + 12
            pl = tone(midi(m), 1.4, ((1, 1), (2, .35), (3, .1), (4, .05)), a=0.004, d=0.55) * 0.045
            pan = 0.35 + 0.3 * (s % 2); add(L, pl * (1 - pan), t + q * beat); add(Rr, pl * pan, t + q * beat)
        if t >= 2 * bar:   # a light pulse once the story is under way
            for q in range(8):
                sh = shaker(i * 17 + q) * (0.03 if q % 2 else 0.018); add(L, sh * 0.7, t + q * beat / 2); add(Rr, sh, t + q * beat / 2)
            for q in (0, 2): k = kick(True) * 0.16; add(L, k, t + q * beat); add(Rr, k, t + q * beat)
        t += bar; i += 1
    for m in (48, 60, 64, 67, 71, 76):
        p = pad(midi(m), 4.0, a=0.05, rel=3.0, bright=0.3) * (0.06 if m > 50 else 0.14); add(L, p, end); add(Rr, p, end + 0.01)
    return finish(L, Rr, length, fade_in=0.4, fade_out=2.0, drive=1.0, peak=0.6)
