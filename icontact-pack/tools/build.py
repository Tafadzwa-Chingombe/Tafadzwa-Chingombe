"""Build an iContact production-pack film (9:16 master + 4:5 crop + SRT) from ad.json, fitting the cut to the voice.

ad.json:
  {"title": "...", "score": "cinematic" | "punchy", "music_volume": 0.32,
   "marks": {"lift": 2, "drop": 3, "end": 9},      shot indices where the music turns (lift/drop optional)
   "bug": [2, 9],                                   the logo bug shows from shot 2 until shot 9 starts
   "shots": [{"page": "sun", "min": 4, "line": "caption text", "say": "spoken form (optional)"}, ...],
   "sfx": [[shot, kind, offset, volume, length], ...]   length for rain/roller/pour/cicadas/riser/whoosh; "shot" = the shot's length
  }
Voice: assets/vo/line-N.mp3 (--vo <dir> copies <dir>/N.mp3 in). Missing → silent stand-ins sized for the words.

usage: python3 build.py <film-folder> [--vo <dir>] [--alt <4x5-folder>]
ad.json extras: keyword (end card), score: calm|cinematic, look: {grain, vignette}
"""
import json, os, re, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import importlib.util
import psound
_spec = importlib.util.spec_from_file_location('nyasha_build', os.path.join(HERE, '..', '..', '.claude', 'skills', 'nyasha-video-ads', 'tools', 'build.py'))
_nb = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_nb)
speech, caption, stand_in = _nb.speech, _nb.caption, _nb.stand_in   # the Nyasha kit's voice timing and caption alignment

KIT = os.path.join(HERE, '..', 'kit')
LEAD, TAIL, END_TAIL = 0.2, 0.5, 2.2


def build(film, vo_src=None, square=None):
    spec = json.load(open(os.path.join(film, 'ad.json')))
    shots = spec['shots']
    for sub in ('lib', 'img'):
        dst = os.path.join(film, sub)
        if os.path.exists(dst): shutil.rmtree(dst)
        shutil.copytree(os.path.join(KIT, sub), dst)
    shutil.copy(os.path.join(KIT, 'chrome.html'), os.path.join(film, 'chrome.html'))
    if spec.get('keyword'):
        open(os.path.join(film, 'endcard.html'), 'w').write(open(os.path.join(KIT, 'endcard.html')).read().replace('{{KEYWORD}}', spec['keyword']))
    vo = os.path.join(film, 'assets', 'vo'); os.makedirs(vo, exist_ok=True)

    lens = []
    for i, shot in enumerate(shots, 1):
        mp3 = os.path.join(vo, f'line-{i}.mp3')
        if vo_src and os.path.exists(os.path.join(vo_src, f'{i}.mp3')): shutil.copy(os.path.join(vo_src, f'{i}.mp3'), mp3)
        if not os.path.exists(mp3): stand_in(mp3, shot['line'])
        spans, dur = speech(mp3)
        if not spans: spans = [(0.0, dur)]
        open(mp3[:-4] + '.vtt', 'w').write(caption(shot['line'], spans).replace('<v Nyasha>', '<v iContact>'))
        need = LEAD + spans[-1][1] + (spec.get('end_tail', END_TAIL) if i == len(shots) else spec.get('tail', TAIL))
        lens.append(round(max(shot.get('min', 0), need) + 0.049, 1))
    starts, t = [], 0.0
    for n in lens: starts.append(round(t, 2)); t += n
    length = round(t, 2)

    for shot, n in zip(shots, lens):
        p = os.path.join(film, f"{shot['page']}.html"); s = open(p).read()
        s, k = re.subn(r'\bshot\(\d+(?:\.\d+)?', f'shot({n:g}', s, count=1)
        if k != 1: raise SystemExit(f'{p}: no shot(<seconds>, …) call')
        open(p, 'w').write(s)

    bug = spec.get('bug', [0, len(shots) - 1])
    open(os.path.join(film, 'lib', 'cuts.js'), 'w').write(
        f'export const cuts = {json.dumps(starts[1:])};\nexport const length = {length};\n'
        f'export const bug = [{starts[bug[0]]}, {starts[bug[1]]}];\n'
        f'export const starts = {json.dumps(starts)};\nexport const look = {json.dumps(spec.get("look", {}))};\n')

    # sound design
    sfx_dir = os.path.join(film, 'assets', 'sfx')
    if os.path.exists(sfx_dir): shutil.rmtree(sfx_dir)
    cues = []
    for entry in spec.get('sfx', []):
        i, kind, off = entry[0], entry[1], entry[2]
        vol = entry[3] if len(entry) > 3 else 0.6
        ln = entry[4] if len(entry) > 4 else None
        if ln == 'shot': ln = round(lens[i] - off + 0.3, 1)
        name = f'{kind}-{ln:g}' if ln else kind
        path = os.path.join(sfx_dir, f'{name}.mp3')
        if not os.path.exists(path): psound.write_mp3(path, psound.fx(kind, ln))
        cues.append((name, round(starts[i] + off, 2), vol))
    marks = {k: starts[v] for k, v in spec.get('marks', {}).items()}
    marks.setdefault('end', starts[-1]); marks.setdefault('drop', marks['end']); marks.setdefault('lift', marks['drop'])
    score = {'cinematic': psound.score_cinematic, 'calm': psound.score_calm}.get(spec.get('score'), psound.score_punchy)
    psound.write_mp3(os.path.join(film, 'assets', 'music', 'score.mp3'), score(length + 0.1, marks))

    def film_html(w, h, crop=0):
        L = f'{length:g}'
        out = ['<!doctype html>', '<html>', '<head>', '<meta charset="utf-8">', f'<meta name="viewport" content="width={w}, height={h}">']
        if crop: out += ['<style>', '  .backdrop { filter: blur(40px) brightness(0.55) saturate(1.1); }', '  .panel { -webkit-mask-image: linear-gradient(to right, transparent, #000 6%, #000 94%, transparent); mask-image: linear-gradient(to right, transparent, #000 6%, #000 94%, transparent); }', '</style>']
        out += ['</head>', '<body>', '<section>', f'  <iframe id="chrome" src="chrome.html#t=0,{L}"></iframe>', '</section>', '<section>']
        for shot, at in zip(shots, starts):
            out.append(f'  <iframe id="{shot["page"]}" src="{shot["page"]}.html"' + (f' at="{at:g}"' if at else '') + pos(crop) + '></iframe>')
        if crop:   # behind the 4:5 panel: the same shot, blurred, filling the frame
            out += ['</section>', '<section>']
            for shot, at in zip(shots, starts):
                out.append(f'  <iframe id="{shot["page"]}-backdrop" src="{shot["page"]}.html"' + (f' at="{at:g}"' if at else '') + ' size="1080x1920" class="backdrop" style="left: -60px; top: -400px; width: 1200px; height: 2133px"></iframe>')
        out += ['</section>', '<section>']
        for i, at in enumerate(starts, 1):
            out.append(f'  <audio id="vo-{i}" src="assets/vo/line-{i}.mp3" at="{at + LEAD:g}"></audio>')
        out.append('</section>')
        # effects on as few tracks as they need without overlapping
        tracks = []
        for name, at, vol in sorted(cues, key=lambda c: c[1]):
            ln = psound_len(os.path.join(sfx_dir, f'{name}.mp3'))
            for tr in tracks:
                if tr[-1][3] <= at: tr.append((name, at, vol, at + ln)); break
            else: tracks.append([(name, at, vol, at + ln)])
        n = 0
        for tr in tracks:
            out.append('<section>')
            for name, at, vol, _ in tr:
                n += 1; out.append(f'  <audio id="sfx-{n}-{name}" src="assets/sfx/{name}.mp3" at="{at:g}" volume="{vol}"></audio>')
            out.append('</section>')
        out += ['<section>', f'  <audio id="music" src="assets/music/score.mp3#t=0,{L}" volume="{spec.get("music_volume", 0.32)}"></audio>',
                '</section>', '</body>', '</html>', '']
        return '\n'.join(out)

    open(os.path.join(film, 'film.html'), 'w').write(film_html(1080, 1920))
    write_srt(os.path.join(film, os.path.basename(os.path.abspath(film)) + '.srt'), vo, starts)
    print(f'{os.path.basename(os.path.abspath(film))}: {length}s  shots {lens}  starts {starts}')
    if square:
        os.makedirs(square, exist_ok=True)
        for name in os.listdir(square):
            if name in ('.film',): continue
            p = os.path.join(square, name); shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
        for name in os.listdir(film):
            if name in ('.film', 'film.html') or name.endswith('.mp4'): continue
            p = os.path.join(film, name); (shutil.copytree if os.path.isdir(p) else shutil.copy2)(p, os.path.join(square, name))
        open(os.path.join(square, 'film.html'), 'w').write(film_html(1080, 1350, crop=200))
        write_srt(os.path.join(square, os.path.basename(os.path.abspath(square)) + '.srt'), vo, starts)
        print(f'  4:5 → {square}')


def pos(crop):
    # the 4:5 cut: the whole 9:16 page at 86%, its content band (y 330–1300) placed from y 74 so it clears the captions
    return ' size="1080x1920" class="panel" style="left: 76px; top: -210px; width: 929px; height: 1651px"' if crop else ''


def write_srt(path, vo, starts):
    def ts(x):
        ms = int(round(x * 1000)); return f'{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}'
    def sec(s):
        h, m, r = s.split(':'); return int(h) * 3600 + int(m) * 60 + float(r)
    out, n = [], 0
    for i, at in enumerate(starts, 1):
        vtt = open(os.path.join(vo, f'line-{i}.vtt')).read()
        for a, b, text in re.findall(r'([\d:.]+) --> ([\d:.]+)\n(.+)', vtt):
            words = re.sub(r'<[^>]+>', '', text).strip()
            n += 1; out += [str(n), f'{ts(at + LEAD + sec(a))} --> {ts(at + LEAD + sec(b))}', words, '']
    open(path, 'w').write('\n'.join(out))


_lens = {}
def psound_len(path):
    import subprocess
    if path not in _lens:
        _lens[path] = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout)
    return _lens[path]


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0].startswith('-'): raise SystemExit(__doc__)
    build(a[0], a[a.index('--vo') + 1] if '--vo' in a else None, a[a.index('--alt') + 1] if '--alt' in a else None)
