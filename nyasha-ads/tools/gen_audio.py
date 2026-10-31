"""Sound for the Nyasha films, made in code (royalty-free because it is original):
- assets/music/bed.mp3   an upbeat Afro-pop-flavoured bed, the film's length, fade baked in
- assets/sfx/*.mp3       pop, success ding, whoosh
- assets/vo/nyasha-vo.mp3 + .vtt  a silent stand-in for the voice-over, carrying the script as timed words,
                          so Studio shows (and render --subtitles burns in) the captions. Swap in the real VO later.
usage: python3 gen_audio.py <film-folder> <film-key>
"""
import os, re, subprocess, sys, wave
import numpy as np

SR = 44100
rng = np.random.default_rng(7)

SCRIPTS = {
    'a': (25.0, [
        (0.15, 3.0, "Mhoro! Quick question — if a customer searched for your business right now… would they find you?"),
        (3.1, 8.0, "Most businesses in Harare don't show up. So those customers? They call someone else."),
        (8.1, 15.0, "I'm Nyasha from iContact Africa Solutions. We build fast, mobile-friendly websites, plus SEO and marketing, that bring in real enquiries."),
        (15.2, 20.8, "Fixed-price quotes. Same-day reply."),
        (21.0, 24.8, "Tap the link, book your free call — and let's get you found. Zvakanaka!"),
    ]),
    'b': (28.0, [
        (0.15, 3.0, "Mhoro! Three website mistakes that quietly cost you customers."),
        (3.1, 10.0, "One: your site doesn't work on a phone. Most people in Zimbabwe browse on mobile — if it's hard to read, they leave."),
        (10.1, 17.0, "Two: no clear way to contact you. Put your phone number and a WhatsApp or enquiry button on every page."),
        (17.1, 23.0, "Three: it's slow. If it takes more than a few seconds, people won't wait."),
        (23.1, 27.8, "We fix all three. Book a free call and we'll tell you what's holding your site back."),
    ]),
    'c': (18.0, [
        (0.15, 3.0, "Need a website but don't know what it'll cost?"),
        (3.1, 10.0, "Tell us what you need. We'll send you a fixed-price quote — same day."),
        (10.1, 14.0, "No surprises. No jargon. Just a clear plan."),
        (14.1, 17.8, "Tap to book your free call. Tatenda!"),
    ]),
    'd': (15.0, [
        (0.15, 3.0, "Mhoro! I'm Nyasha."),
        (3.1, 9.0, "I'm iContact Africa Solutions' digital guide — I'll show you how to get your business found, trusted and booked."),
        (9.1, 12.0, "Websites. SEO. Marketing. All in plain English."),
        (12.1, 14.8, "Follow me for tips every week — and yes, I'm AI-generated!"),
    ]),
}

# where each film's sound effects go (film seconds)
SFX = {
    'a': [('whoosh', 2.85), ('pop', 4.6), ('pop', 5.05), ('pop', 5.5), ('whoosh', 7.85), ('pop', 11.4), ('pop', 12.6), ('pop', 13.2),
          ('whoosh', 14.85), ('pop', 15.5), ('pop', 16.4), ('ding', 17.6), ('whoosh', 20.85), ('pop', 21.4)],
    'b': [('pop', 0.3), ('whoosh', 2.85), ('pop', 4.6), ('pop', 5.6), ('whoosh', 9.85), ('pop', 12.5), ('ding', 14.0),
          ('whoosh', 16.85), ('pop', 20.5), ('whoosh', 22.85), ('pop', 23.5)],
    'c': [('whoosh', 2.85), ('pop', 6.0), ('pop', 6.6), ('ding', 8.2), ('whoosh', 9.85), ('whoosh', 13.85), ('pop', 14.4)],
    'd': [('whoosh', 2.85), ('pop', 7.2), ('pop', 7.8), ('pop', 8.3), ('whoosh', 8.85), ('pop', 9.5), ('pop', 10.1), ('pop', 10.7),
          ('whoosh', 11.85), ('pop', 12.4)],
}


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


# ---------- captions ----------
def cues_for(start, end, text, maxlen=34):
    """split a VO line into subtitle cues at punctuation / word boundaries, timed by length"""
    words = text.split()
    groups, cur = [], []
    for w in words:
        if cur and (len(' '.join(cur + [w])) > maxlen):
            groups.append(cur); cur = []
        cur.append(w)
        if re.search(r'[.?!—…]$', w) and len(' '.join(cur)) > 12:
            groups.append(cur); cur = []
    if cur: groups.append(cur)
    total = sum(len(' '.join(g)) for g in groups)
    t = start; span = end - start; out = []
    for g in groups:
        d = span * len(' '.join(g)) / total
        # words timed by their length inside the cue
        wl = [len(w) + 1 for w in g]; acc = t; tagged = []
        for i, w in enumerate(g):
            tagged.append((acc, w)); acc += d * wl[i] / sum(wl)
        out.append((t, t + d - 0.04, tagged)); t += d
    return out

def ts(s):
    h = int(s // 3600); m = int(s % 3600 // 60); sec = s % 60
    return f"{h:02d}:{m:02d}:{sec:06.3f}"

def vtt(lines):
    out = ['WEBVTT', '']
    for (s, e, text) in lines:
        for (cs, ce, tagged) in cues_for(s, e, text):
            body = ' '.join((w if i == 0 else f"<{ts(wt)}>{w}") for i, (wt, w) in enumerate(tagged))
            out += [f"{ts(cs)} --> {ts(ce)}", f"<v Nyasha>{body}", '']
    return '\n'.join(out)


if __name__ == '__main__':
    folder, key = sys.argv[1], sys.argv[2]
    length, lines = SCRIPTS[key]
    write_mp3(f'{folder}/assets/music/bed.mp3', music(length))
    for kind in sorted({k for k, _ in SFX[key]}):
        write_mp3(f'{folder}/assets/sfx/{kind}.mp3', sfx(kind), stereo=False)
    os.makedirs(f'{folder}/assets/vo', exist_ok=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'anullsrc=r=22050:cl=mono', '-t', str(length),
                    '-codec:a', 'libmp3lame', '-b:a', '32k', f'{folder}/assets/vo/nyasha-vo.mp3'], check=True)
    open(f'{folder}/assets/vo/nyasha-vo.vtt', 'w').write(vtt(lines))
    # the sfx clips for film.html
    for kind, at in SFX[key]:
        print(f'  <audio id="{kind}-{str(at).replace(".", "-")}" src="assets/sfx/{kind}.mp3" at="{at}" volume="0.5"></audio>')
