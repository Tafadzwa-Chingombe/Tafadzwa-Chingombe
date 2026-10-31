"""Put Nyasha's ElevenLabs voice into a film and fit the cut to it.

Each shot becomes as long as its voice line needs (never shorter than it was), the line starts 0.15 s into the
shot, sound effects move with their shot, the music is made again at the new length (and sits lower, under the
voice), and each line gets a word-timed caption file from its audio: words are spread over the stretches where
she is speaking (the pauses come from silence detection), in proportion to their length.

usage: python3 nyasha-ads/tools/retime_vo.py <film-key> <folder-with-a1.mp3…>      e.g. a ~/vo
then:  python3 nyasha-ads/tools/mksquare.py <film> square/<film>-1x1  and render both.
"""
import os, re, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_audio

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEAD, TAIL, END_TAIL, MUSIC = 0.15, 0.45, 1.3, 0.3

# film: folder, shots [(page, original length)], voice lines (one per shot), sound effects at their original film times
FILMS = {
    'a': ('a-show-up-online', [('hook', 3), ('search', 5), ('intro', 7), ('enquiry', 6), ('endcard', 4)]),
    'b': ('b-three-mistakes', [('count', 3), ('mobile', 7), ('contact', 7), ('slow', 6), ('endcard', 5)]),
    'c': ('c-same-day-quote', [('hook', 3), ('quote', 7), ('smile', 4), ('endcard', 4)]),
    'd': ('d-meet-nyasha', [('hello', 3), ('guide', 6), ('montage', 3), ('endcard', 3)]),
}
# sound effects as (shot index, kind, seconds into that shot; negative = just before its cut), matched to the
# moments in each page (which are timed to the voice)
W = 'whoosh'
SFX = {
    'a': [(1, W, -0.15), (1, 'pop', 1.6), (1, 'pop', 2.05), (1, 'pop', 2.5), (2, W, -0.15), (2, 'pop', 5.1), (2, 'pop', 6.2),
          (2, 'pop', 6.7), (3, W, -0.15), (3, 'pop', 0.5), (3, 'pop', 1.4), (3, 'ding', 2.8), (4, W, -0.15), (4, 'pop', 0.4)],
    'b': [(0, 'pop', 0.3), (1, W, -0.15), (1, 'pop', 1.6), (1, 'pop', 7.6), (2, W, -0.15), (2, 'pop', 2.5), (2, 'ding', 4.0),
          (3, W, -0.15), (3, 'pop', 4.8), (4, W, -0.15), (4, 'pop', 0.5)],
    'c': [(1, W, -0.15), (1, 'pop', 2.5), (1, 'pop', 2.8), (1, 'ding', 3.8), (2, W, -0.15), (3, W, -0.15), (3, 'pop', 0.4)],
    'd': [(0, 'pop', 0.15), (1, W, -0.15), (1, 'pop', 5.1), (1, 'pop', 5.7), (1, 'pop', 6.4), (2, W, -0.15), (2, 'pop', 0.35),
          (2, 'pop', 1.4), (2, 'pop', 3.3), (3, W, -0.15), (3, 'pop', 0.4)],
}
LINES = {k: [t for _, _, t in v[1]] for k, v in gen_audio.SCRIPTS.items()}


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
            if t - start > 0.05: spans.append((start, t))
            start = None
        else:
            start = t
    if start is not None and dur - start > 0.05: spans.append((start, dur))
    return spans, dur


def caption(text, spans, maxlen=34):
    """WebVTT: words laid along the speaking time by length, cut into cues of ~maxlen characters"""
    words = text.split()
    weights = [len(w) + 1 for w in words]
    total_talk = sum(b - a for a, b in spans)
    def at(frac):  # a fraction of the speaking time → seconds in the file
        left = frac * total_talk
        for a, b in spans:
            if left <= b - a: return a + left
            left -= b - a
        return spans[-1][1]
    acc, timed, W = 0, [], sum(weights)
    for w, n in zip(words, weights):
        timed.append((w, at(acc / W), at((acc + n) / W)))
        acc += n
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


def run(key, src):
    folder, shots = FILMS[key]
    film_dir = os.path.join(ROOT, folder)
    vo_dir = os.path.join(film_dir, 'assets', 'vo')
    os.makedirs(vo_dir, exist_ok=True)
    for name in os.listdir(vo_dir): os.remove(os.path.join(vo_dir, name))   # the silent stand-in, or an older take

    new_lens = []
    for i, (page, n) in enumerate(shots, 1):
        mp3 = os.path.join(film_dir, 'assets', 'vo', f'line-{i}.mp3')
        shutil.copy(os.path.join(src, f'{key}{i}.mp3'), mp3)
        spans, _ = speech(mp3)
        open(mp3[:-4] + '.vtt', 'w').write(caption(LINES[key][i - 1], spans))
        need = LEAD + spans[-1][1] + (END_TAIL if page == 'endcard' else TAIL)
        new_lens.append(round(max(n, need) + 0.049, 1))
    new_starts, t = [], 0.0
    for n in new_lens: new_starts.append(round(t, 2)); t += n
    length = round(t, 2)

    # each page lasts as long as its shot now (its own push-in spans the whole shot)
    for (page, _), n in zip(shots, new_lens):
        p = os.path.join(film_dir, f'{page}.html')
        s = open(p).read()
        s = re.sub(r'\bshot\(\d+(?:\.\d+)?', f'shot({n:g}', s, count=1)
        open(p, 'w').write(s)

    # sound effects keep their place within their shot
    sfx = [(kind, round(new_starts[i] + off, 2)) for i, kind, off in SFX[key]]

    gen_audio.write_mp3(os.path.join(film_dir, 'assets', 'music', 'bed.mp3'), gen_audio.music(length))

    L = f'{length:g}'
    out = ['<!doctype html>', '<html>', '<head>', '<meta charset="utf-8">', '<meta name="viewport" content="width=1080, height=1920">',
           '</head>', '<body>', '<section>', f'  <iframe id="chrome" src="chrome.html#t=0,{L}"></iframe>', '</section>', '<section>']
    for (page, _), at in zip(shots, new_starts):
        out.append(f'  <iframe id="{page}" src="{page}.html"' + (f' at="{at:g}"' if at else '') + '></iframe>')
    out += ['</section>', '<section>']
    for i, at in enumerate(new_starts, 1):
        out.append(f'  <audio id="vo-{i}" src="assets/vo/line-{i}.mp3" at="{at + LEAD:g}"></audio>')
    out += ['</section>', '<section>']
    count = {}
    for kind, at in sfx:
        count[kind] = count.get(kind, 0) + 1
        out.append(f'  <audio id="sfx-{kind}-{count[kind]}" src="assets/sfx/{kind}.mp3" at="{at:g}" volume="{ {"pop": 0.45, "ding": 0.5, "whoosh": 0.5}[kind] }"></audio>')
    out += ['</section>', '<section>', f'  <audio id="music" src="assets/music/bed.mp3#t=0,{L}" volume="{MUSIC}"></audio>', '</section>',
            '</body>', '</html>', '']
    open(os.path.join(film_dir, 'film.html'), 'w').write('\n'.join(out))
    print(f'{folder}: {length}s  shots {new_lens}')


if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2])
