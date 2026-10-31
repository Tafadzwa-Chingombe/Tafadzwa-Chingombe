"""Original sound for the ads, synthesised in code (so there is no licence to clear).
  music(length)  an upbeat Afro-pop-flavoured bed (112 bpm, vi-IV-I-V in A), fade baked in
  sfx(kind)      'pop' | 'ding' | 'whoosh'
  write_mp3(path, samples)
CLI:  python3 sound.py sfx <film-folder>     writes assets/sfx/{pop,ding,whoosh}.mp3
      python3 sound.py music <film-folder> <seconds>
"""
import os, subprocess, sys, wave
import numpy as np

SR = 44100
rng = np.random.default_rng(7)


# ---------- synthesis ----------
def env(n, a, d):
    """attack a s, exponential decay with time constant d s"""
    t = np.arange(n) / SR
    e = np.exp(-t / d)
    na = max(1, int(a * SR))
    e[:na] *= np.linspace(0, 1, na)
    return e

def tone(freq, dur, partials=((1, 1.0),), a=0.005, d=0.3):
    n = int(dur * SR); t = np.arange(n) / SR
    s = sum(amp * np.sin(2 * np.pi * freq * k * t) for k, amp in partials)
    return s * env(n, a, d)

def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x):
        acc = (1 - a) * v + a * acc; y[i] = acc
    return y

def add(buf, x, at):
    i = int(at * SR)
    if i >= len(buf): return
    j = min(len(buf), i + len(x)); buf[i:j] += x[:j - i]

def midi(m): return 440.0 * 2 ** ((m - 69) / 12)

def kick():
    n = int(0.35 * SR); t = np.arange(n) / SR
    f = 45 + 80 * np.exp(-t / 0.04)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.11)

def noise_hit(dur, d, hp=True):
    n = int(dur * SR); x = rng.standard_normal(n)
    if hp: x = np.diff(x, prepend=0)
    return x * env(n, 0.001, d)

def clap():
    x = noise_hit(0.25, 0.06, hp=False)
    return x - lowpass(x, 900)

def music(length):
    bpm = 112; beat = 60 / bpm; bar = 4 * beat
    L = np.zeros(int((length + 1) * SR)); R = np.zeros_like(L)
    # vi – IV – I – V in A major: F#m, D, A, E
    chords = [(54, [66, 69, 73]), (50, [62, 66, 69]), (57, [64, 69, 73]), (52, [64, 68, 71])]
    nbars = int(np.ceil(length / bar)) + 1
    k = kick(); c = clap()
    for b in range(nbars):
        root, notes = chords[b % 4]; t0 = b * bar
        # pad: soft additive chord, long attack
        for m in notes:
            p = tone(midi(m - 12), bar, ((1, 1), (2, .35), (3, .15)), a=0.25, d=3.0) * 0.045
            add(L, p, t0); add(R, p * 0.9, t0)
        # bass: root on 1, the "and" of 2, and 4
        for off, m in ((0, root), (1.5, root), (3, root + 7)):
            bs = np.tanh(2 * tone(midi(m - 24), beat * 0.9, ((1, 1), (2, .3)), a=0.005, d=0.25)) * 0.16
            add(L, bs, t0 + off * beat); add(R, bs, t0 + off * beat)
        # marimba-like plucks, syncopated arpeggio
        pattern = [0, 1, 2, 1, 2, 0, 1, 2]
        for i, step in enumerate([0, 0.75, 1.5, 2, 2.5, 3, 3.25, 3.75]):
            m = notes[pattern[i]] + (12 if i in (3, 6) else 0)
            pl = tone(midi(m), 0.5, ((1, 1), (4, .25), (10, .05)), a=0.002, d=0.12) * 0.06
            pan = 0.35 + 0.3 * (i % 2)
            add(L, pl * (1 - pan), t0 + step * beat); add(R, pl * pan, t0 + step * beat)
        # drums
        for q in (0, 2, 2.75):
            add(L, k * 0.42, t0 + q * beat); add(R, k * 0.42, t0 + q * beat)
        for q in (1, 3):
            add(L, c * 0.12, t0 + q * beat); add(R, c * 0.12, t0 + q * beat)
        for s in range(16):
            h = noise_hit(0.06, 0.012) * (0.035 if s % 2 == 0 else 0.02)
            add(L, h * 0.8, t0 + s * beat / 4); add(R, h, t0 + s * beat / 4 + 0.004)
    n = int(length * SR); L, R = L[:n], R[:n]
    st = np.stack([L, R], 1)
    st = np.tanh(st * 1.3)
    fade_in = int(0.25 * SR); fade_out = int(1.4 * SR)
    st[:fade_in] *= np.linspace(0, 1, fade_in)[:, None]
    st[-fade_out:] *= np.linspace(1, 0, fade_out)[:, None] ** 1.5
    return st / np.max(np.abs(st)) * 0.7

def sfx(kind):
    if kind == 'pop':
        n = int(0.16 * SR); t = np.arange(n) / SR
        f = 700 + 900 * (t / 0.16)
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.04)
        return x * 0.5
    if kind == 'ding':
        return (tone(1318.5, 0.6, ((1, 1), (2.01, .2)), d=0.18) * 0.35
                + np.pad(tone(1760, 0.6, ((1, 1), (2.01, .2)), d=0.25), (int(0.09 * SR), 0))[:int(0.6 * SR)] * 0.35)
    if kind == 'whoosh':
        n = int(0.45 * SR); t = np.arange(n) / SR
        x = rng.standard_normal(n)
        shape = np.sin(np.pi * t / 0.45) ** 2
        y = lowpass(x * shape, 2500) - lowpass(x * shape, 300)
        return y / np.max(np.abs(y)) * 0.22
    raise ValueError(kind)


def write_mp3(path, data, stereo=True):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + '.tmp.wav'
    data = np.clip(data, -1, 1)
    if data.ndim == 1: data = data[:, None]
    with wave.open(tmp, 'wb') as w:
        w.setnchannels(data.shape[1]); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((data * 32767).astype('<i2').tobytes())
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-codec:a', 'libmp3lame', '-b:a', '160k', path], check=True)
    os.remove(tmp)

if __name__ == '__main__':
    cmd, folder = sys.argv[1], sys.argv[2]
    if cmd == 'sfx':
        for kind in ('pop', 'ding', 'whoosh'):
            write_mp3(os.path.join(folder, 'assets', 'sfx', f'{kind}.mp3'), sfx(kind))
    elif cmd == 'music':
        write_mp3(os.path.join(folder, 'assets', 'music', 'bed.mp3'), music(float(sys.argv[3])))
    else:
        raise SystemExit(__doc__)
