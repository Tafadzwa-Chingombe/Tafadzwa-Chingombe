"""Build (or rebuild) one ad's film.html from its ad.json, fitting the cut to the voice.

ad.json, beside film.html:
  {
    "title": "Do you show up online?",
    "shots": [ {"page": "hook", "min": 3, "line": "Mhoro! Quick question — …"}, … ],   one voice line per shot
    "sfx":   [ [1, "whoosh", -0.15], [1, "pop", 1.6], … ],     shot index, kind (pop|ding|whoosh), seconds into that shot
    "music_volume": 0.3                                         optional
  }

What it does:
- voice: assets/vo/line-N.mp3 per shot. With --vo <dir>, copies <dir>/N.mp3 in first (e.g. ElevenLabs downloads).
  A shot with no voice file gets a silent stand-in sized for its words, so captions show before the voice exists.
- captions: assets/vo/line-N.vtt, word-timed to the audio (pauses matched to punctuation).
- shot lengths: each shot lasts as long as its line needs (never shorter than "min"); each page's
  shot(…) duration is rewritten to match, so its push-in spans the whole shot.
- sound effects placed relative to their shot; music made again at the film's length.
- film.html written: wordmark overlay, shots, voice, sfx, music.

usage:  python3 build.py <film-folder> [--vo <dir-with-1.mp3,2.mp3…>]
"""
import json, os, re, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sound

LEAD, TAIL, END_TAIL, MUSIC = 0.15, 0.45, 1.3, 0.3
SFX_VOLUME = {'pop': 0.45, 'ding': 0.5, 'whoosh': 0.5}


def speech(path):
    """the stretches of the file where she is speaking, and its length"""
    log = subprocess.run(['ffmpeg', '-hide_banner', '-i', path, '-af', 'silencedetect=noise=-38dB:d=0.15', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path],
                               capture_output=True, text=True).stdout)
    marks = re.findall(r'silence_(start|end): ([\d.]+)', log)
    spans, start = [], 0.0
    for kind, t in marks:
        t = float(t)
        if kind == 'start':
            if t - start > 0.12: spans.append((start, t))
            start = None
        else:
            start = t
    if start is not None and dur - start > 0.12: spans.append((start, dur))
    return spans, dur


def spoken_weight(word):
    """roughly how long a word takes to say: its syllables, a spelled-out acronym 2.5 per letter, plus a beat after punctuation"""
    core = re.sub(r'[^A-Za-z]', '', word)
    if re.fullmatch(r'[A-Z]{2,}', core): n = 2.5 * len(core)
    else: n = max(1, len(re.findall(r'[aeiouy]+', core.lower())) - (1 if core.lower().endswith('e') and len(core) > 3 else 0))
    return n + 0.3 + (0.6 if re.search(r'[.,?!—…:;]$', word) else 0)


def split_by_pauses(words, weights, spans):
    """which words each stretch of speech holds: the pauses are put at word breaks, preferring breaks after
    punctuation, so that each stretch's share of the text matches its share of the speaking time"""
    n, k = len(words), len(spans)
    if k <= 1 or n < k: return [(0, n)] + [(n, n)] * (k - 1)
    talk = [b - a for a, b in spans]
    T, W = sum(talk), sum(weights)
    cum_w = [0]
    for w in weights: cum_w.append(cum_w[-1] + w)
    punct = [bool(re.search(r'[.,?!—…:;]$', w)) for w in words]
    INF = float('inf')
    # best[g][j]: cost of putting the first g stretches over words[0:j]
    best = [[INF] * (n + 1) for _ in range(k + 1)]
    back = [[0] * (n + 1) for _ in range(k + 1)]
    best[0][0] = 0
    for g in range(1, k + 1):
        for j in range(g, n - (k - g) + 1):
            for i in range(g - 1, j):
                if best[g - 1][i] == INF: continue
                share = (cum_w[j] - cum_w[i]) / W - talk[g - 1] / T
                brk = 0 if j == n or punct[j - 1] else 0.02   # a pause that falls mid-phrase costs a little
                c = best[g - 1][i] + share * share + brk
                if c < best[g][j]: best[g][j], back[g][j] = c, i
    out, j = [], n
    for g in range(k, 0, -1):
        i = back[g][j]; out.append((i, j)); j = i
    return out[::-1]


def caption(text, spans, maxlen=34):
    """WebVTT: words laid along the speaking time by length, cut into cues of ~maxlen characters"""
    words = text.split()
    weights = [spoken_weight(w) for w in words]
    groups = split_by_pauses(words, weights, spans)
    timed = []
    for (a, b), (i, j) in zip(spans, groups):   # each stretch of speech carries its own words, spread by length
        W, acc = sum(weights[i:j]) or 1, 0
        for k in range(i, j):
            timed.append((words[k], a + (b - a) * acc / W, a + (b - a) * (acc + weights[k]) / W))
            acc += weights[k]
    cues, cur = [], []
    for item in timed:
        if cur and len(' '.join(x[0] for x in cur + [item])) > maxlen:
            cues.append(cur); cur = []
        cur.append(item)
        if re.search(r'[.?!—…]$', item[0]) and len(' '.join(x[0] for x in cur)) > 12:
            cues.append(cur); cur = []
    if cur: cues.append(cur)
    ts = lambda s: f"{int(s // 3600):02d}:{int(s % 3600 // 60):02d}:{s % 60:06.3f}"
    out = ['WEBVTT', '']
    for c in cues:
        body = ' '.join(w if i == 0 else f'<{ts(s)}>{w}' for i, (w, s, _) in enumerate(c))
        out += [f'{ts(c[0][1])} --> {ts(c[-1][2])}', f'<v Nyasha>{body}', '']
    return '\n'.join(out)


def stand_in(path, text):
    """a silent mp3 about as long as the line would take to say"""
    seconds = max(1.0, sum(spoken_weight(w) for w in text.split()) / 4.2)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'anullsrc=r=22050:cl=mono', '-t', f'{seconds:.2f}',
                    '-codec:a', 'libmp3lame', '-b:a', '32k', path], check=True)


def build(film_dir, vo_src=None):
    spec = json.load(open(os.path.join(film_dir, 'ad.json')))
    shots = spec['shots']
    vo_dir = os.path.join(film_dir, 'assets', 'vo')
    os.makedirs(vo_dir, exist_ok=True)
    if not os.path.exists(os.path.join(film_dir, 'assets', 'sfx', 'pop.mp3')):
        for kind in ('pop', 'ding', 'whoosh'):
            sound.write_mp3(os.path.join(film_dir, 'assets', 'sfx', f'{kind}.mp3'), sound.sfx(kind))

    lens = []
    for i, shot in enumerate(shots, 1):
        mp3 = os.path.join(vo_dir, f'line-{i}.mp3')
        if vo_src and os.path.exists(os.path.join(vo_src, f'{i}.mp3')):
            shutil.copy(os.path.join(vo_src, f'{i}.mp3'), mp3)
        if not os.path.exists(mp3):
            stand_in(mp3, shot['line'])
        spans, dur = speech(mp3)
        if not spans: spans = [(0.0, dur)]          # silent stand-in: spread the words over it
        open(mp3[:-4] + '.vtt', 'w').write(caption(shot['line'], spans))
        need = LEAD + spans[-1][1] + (END_TAIL if i == len(shots) else TAIL)
        lens.append(round(max(shot.get('min', 0), need) + 0.049, 1))
    starts, t = [], 0.0
    for n in lens: starts.append(round(t, 2)); t += n
    length = round(t, 2)

    for shot, n in zip(shots, lens):
        p = os.path.join(film_dir, f"{shot['page']}.html")
        s = open(p).read()
        s, k = re.subn(r'\bshot\(\d+(?:\.\d+)?', f'shot({n:g}', s, count=1)
        if k != 1: raise SystemExit(f"{p}: no shot(<seconds>, …) call to set")
        open(p, 'w').write(s)

    sfx = [(kind, round(starts[i] + off, 2)) for i, kind, off in spec.get('sfx', [])]
    # a touch longer than the film, so encoder rounding never leaves it short of the #t= trim
    sound.write_mp3(os.path.join(film_dir, 'assets', 'music', 'bed.mp3'), sound.music(length + 0.1))

    L = f'{length:g}'
    out = ['<!doctype html>', '<html>', '<head>', '<meta charset="utf-8">', '<meta name="viewport" content="width=1080, height=1920">',
           '</head>', '<body>', '<section>', f'  <iframe id="chrome" src="chrome.html#t=0,{L}"></iframe>', '</section>', '<section>']
    for shot, at in zip(shots, starts):
        out.append(f'  <iframe id="{shot["page"]}" src="{shot["page"]}.html"' + (f' at="{at:g}"' if at else '') + '></iframe>')
    out += ['</section>', '<section>']
    for i, at in enumerate(starts, 1):
        out.append(f'  <audio id="vo-{i}" src="assets/vo/line-{i}.mp3" at="{at + LEAD:g}"></audio>')
    out += ['</section>']
    if sfx:
        out.append('<section>')
        count = {}
        for kind, at in sorted(sfx, key=lambda x: x[1]):
            count[kind] = count.get(kind, 0) + 1
            out.append(f'  <audio id="sfx-{kind}-{count[kind]}" src="assets/sfx/{kind}.mp3" at="{at:g}" volume="{SFX_VOLUME[kind]}"></audio>')
        out.append('</section>')
    out += ['<section>', f'  <audio id="music" src="assets/music/bed.mp3#t=0,{L}" volume="{spec.get("music_volume", MUSIC)}"></audio>',
            '</section>', '</body>', '</html>', '']
    open(os.path.join(film_dir, 'film.html'), 'w').write('\n'.join(out))
    print(f'{os.path.basename(os.path.abspath(film_dir))}: {length}s  shots {lens}  (starts {starts})')


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args or args[0].startswith('-'): raise SystemExit(__doc__)
    vo = args[args.index('--vo') + 1] if '--vo' in args else None
    build(args[0], vo)
