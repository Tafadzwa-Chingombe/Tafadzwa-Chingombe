"""Write an ad's shot pages from ad.json, timing each on-screen item to the word that introduces it.

A shot in ad.json may carry "kind" and its content; build.py ignores these keys, pages.py reads them:

  {"page": "hook", "kind": "photo", "img": "c4", "kicker": "Website inoita marii?", "say": "much",
   "headline": "How much does a <span class=\"hl\">website</span> cost?", "badge": "5", "line": "…", "min": 3}
  {"page": "price", "kind": "list", "title": "What changes the price", "marker": "num|tick|cross|dot|q|step",
   "start": 1, "note": "small print", "items": [["Number of pages", "pages"], …], "headline": "…", …}
  {"page": "vs", "kind": "compare", "cols": ["Facebook page", "Your website"],
   "rows": [["You own it", "own", "no", "yes"], …], "headline": "…", …}
  {"page": "who", "kind": "cards", "cards": [["DIY", "Cheapest, but it costs your time.", "DIY"], …], "us": 2, …}
  {"page": "pay", "kind": "phone", "screen": "<div …data-say=\"declines\" data-anim=\"pop\">…</div>", "css": "…", …}
  {"page": "endcard", "kind": "endcard", "note": "General information, not legal advice."}   (new_ad.sh made the page)

Each item's last field is its cue word: it appears 0.1 s before Nyasha says that word (read from assets/vo/line-N.vtt;
before a voice exists, from the stand-in captions). Also rewrites ad.json "sfx": a whoosh before each cut, a pop per item
(spaced so they never overlap), a ding on the last tick of a tick list.

usage: python3 pages.py <film-folder>     then build.py; after a new voice: build.py --vo …, pages.py, build.py
"""
import html, json, os, re, sys

LEAD = 0.15
IMGS = {'c2': ('c2-portrait.jpg', 0.5, 0.32), 'c3': ('c3-wave-square.jpg', 0.52, 0.4), 'c3-square': ('c3-wave-square.jpg', 0.52, 0.4),
        'c3-wide': ('c3-wave-wide.jpg', 0.6, 0.38), 'c4': ('c4-closeup.jpg', 0.5, 0.42)}
SVG = {
    'tick': '<svg viewBox="0 0 24 24" fill="none"><path d="M5 12.5l4.5 4.5L19 7.5" stroke="#0B1F3A" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    'cross': '<svg viewBox="0 0 24 24" fill="none"><path d="M6 6l12 12M18 6L6 18" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/></svg>',
    'step': '<svg viewBox="0 0 24 24" fill="none"><path d="M5 12h13M13 6l6 6-6 6" stroke="#0B1F3A" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>',
}


def words_at(vtt_path):
    """[(word, start seconds)] from a word-timed WebVTT"""
    if not os.path.exists(vtt_path): return []
    out = []
    for line in open(vtt_path).read().splitlines():
        if not line.startswith('<v '): continue
        cue = re.sub(r'^<v [^>]*>', '', line)
        parts = re.split(r'<(\d\d:\d\d:\d\d\.\d+)>', cue)
        # parts: first word(s) with no tag (their time is the cue start, set below), then time, text, time, text…
        out.append(('__CUE__', None))
        out.append((parts[0], None))
        for i in range(1, len(parts), 2):
            h, m, s = parts[i].split(':')
            out.append((parts[i + 1], int(h) * 3600 + int(m) * 60 + float(s)))
    # cue starts come from the timing lines
    starts = [sum(float(x) * f for x, f in zip(l.split(' --> ')[0].split(':'), (3600, 60, 1)))
              for l in open(vtt_path).read().splitlines() if ' --> ' in l]
    res, ci = [], -1
    for w, t in out:
        if w == '__CUE__': ci += 1; continue
        if t is None: t = starts[ci]
        for word in w.split():
            res.append((word, t))
    return res


def cue_times(words, cues, default_from=0.4, step=0.6):
    """the time each cue word is said (+LEAD into the shot, 0.1 s early), in order; evenly spaced if not found"""
    norm = lambda w: re.sub(r'[^a-z0-9]', '', w.lower())
    times, i, last = [], 0, 0.0
    for n, cue in enumerate(cues):
        t = None
        if cue:
            key = norm(cue)
            for j in range(i, len(words)):
                if norm(words[j][0]).startswith(key):
                    t, i = words[j][1], j + 1
                    break
        if t is None: t = max(last + step, default_from + n * step) - LEAD + 0.1
        t = round(max(0.1, t + LEAD - 0.1), 2)
        times.append(t); last = t
    return times


def page(body, css='', script='shot(3);', extra_css_files=('lib/pages.css',)):
    links = ''.join(f'<link rel="stylesheet" href="{f}">\n' for f in extra_css_files)
    return f'''<!doctype html>
<html>
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="lib/brand.css">
{links}{'<style>' + css + '</style>' if css else ''}
</head>
<body>
<div class="stage"></div>
{body}
<script type="module">
import {{ shot }} from './lib/shot.js';
{script}
</script>
</body>
</html>
'''


def build_pages(film):
    spec_path = os.path.join(film, 'ad.json')
    spec = json.load(open(spec_path))
    sfx = []
    for idx, s in enumerate(spec['shots']):
        kind = s.get('kind')
        if not kind: continue
        words = words_at(os.path.join(film, 'assets', 'vo', f'line-{idx + 1}.vtt'))
        if idx > 0: sfx.append([idx, 'whoosh', -0.15])
        pops = []
        prev = os.path.join(film, f"{s['page']}.html")
        dur = re.search(r'\bshot\((\d+(?:\.\d+)?)', open(prev).read()).group(1) if os.path.exists(prev) else str(s.get('min', 3))
        script = f'shot({dur});'
        head = s.get('headline', '')
        if kind == 'endcard':
            if s.get('note'):
                p = open(prev).read()
                if 'class="endnote"' not in p:
                    p = p.replace('<div class="url"', f'<div class="endnote" style="position:absolute;left:70px;right:70px;top:1180px;text-align:center;font-weight:500;font-size:26px;color:var(--muted)" data-rise="0.9">{html.escape(s["note"])}</div>\n<div class="url"', 1)
                    open(prev, 'w').write(p)
            sfx.append([idx, 'pop', 0.4])
            continue
        if kind == 'photo':
            img, fx, fy = IMGS[s.get('img', 'c3')]
            cues = [s.get('say_kicker') if s.get('kicker') else None, s.get('say')]
            tk, th = cue_times(words, cues, default_from=0.15)
            if not s.get('kicker'): th = s.get('at', 0.2) if not s.get('say') else th
            body = f'<div class="photo"><img src="assets/nyasha/{img}" alt="Nyasha" data-from="{s.get("from", 1.0)}" data-to="{s.get("to", 1.1)}" data-fx="{fx}" data-fy="{fy}" data-tilt="{s.get("tilt", 0.8)}"></div>\n'
            if s.get('badge'):
                body += f'<div class="badge-num" data-pop="0.3"><span>{html.escape(s["badge"])}</span></div>\n'; pops.append(0.3)
            if s.get('kicker'):
                body += f'<div class="kicker-big" data-pop="{tk}">{html.escape(s["kicker"])}</div>\n'; pops.append(tk)
            body += f'<div class="headline" data-rise="{th}" data-fit="70"><span>{head}</span></div>'
            open(prev, 'w').write(page(body, script=script, extra_css_files=('lib/pages.css',)))
        elif kind == 'list':
            items = s['items']; marker = s.get('marker', 'num'); start = s.get('start', 1)
            times = cue_times(words, [it[1] if len(it) > 1 else None for it in items])
            body = f'<div class="title" data-rise="0.1">{html.escape(s.get("title", ""))}</div>\n'
            if s.get('note'): body += f'<div class="footnote" data-rise="0.3">{html.escape(s["note"])}</div>\n'
            body += f'<div class="items{" with-note" if s.get("note") else ""}">\n'
            for n, (it, t) in enumerate(zip(items, times)):
                mk = {'num': str(start + n), 'q': '?', 'dot': '•'}.get(marker, SVG.get(marker, ''))
                cls = {'cross': ' cross', 'dot': ' dot', 'q': ' q'}.get(marker, '')
                body += f'  <div class="item" data-rise="{t}"><div class="mk{cls}">{mk}</div><div>{html.escape(it[0])}</div></div>\n'
                pops.append(t)
            body += '</div>\n'
            hk = cue_times(words, [s.get('say')], default_from=0.3)[0] if s.get('say') else 0.3
            body += f'<div class="headline" data-rise="{hk}" data-fit="70"><span>{head}</span></div>'
            if marker == 'tick' and times: sfx.append([idx, 'ding', times[-1]]); pops = pops[:-1]
            open(prev, 'w').write(page(body, script=script))
        elif kind == 'compare':
            cols = s['cols']; rows = s['rows']
            times = cue_times(words, [r[1] for r in rows])
            body = '<div class="compare">\n  <div class="row head" data-rise="0.1"><div class="feat"></div>' + ''.join(
                f'<div class="col{" us" if i == len(cols) - 1 else ""}">{html.escape(c)}</div>' for i, c in enumerate(cols)) + '</div>\n'
            for r, t in zip(rows, times):
                marks = ''.join(f'<div class="col"><div class="mark {m}" data-pop="{round(t + 0.15 * k, 2)}">{SVG["tick" if m == "yes" else "cross"]}</div></div>'
                                for k, m in enumerate(r[2:]))
                body += f'  <div class="row" data-rise="{t}"><div class="feat">{html.escape(r[0])}</div>{marks}</div>\n'
                pops.append(t)
            body += '</div>\n'
            hk = cue_times(words, [s.get('say')], default_from=0.3)[0] if s.get('say') else 0.3
            body += f'<div class="headline" data-rise="{hk}" data-fit="70"><span>{head}</span></div>'
            open(prev, 'w').write(page(body, script=script))
        elif kind == 'cards':
            cards = s['cards']
            times = cue_times(words, [c[2] for c in cards])
            body = '<div class="cards">\n'
            for n, (c, t) in enumerate(zip(cards, times)):
                body += f'  <div class="card2{" us" if n == s.get("us", -1) else ""}" data-rise="{t}"><div class="t">{html.escape(c[0])}</div><div class="b">{html.escape(c[1])}</div></div>\n'
                pops.append(t)
            body += '</div>\n'
            hk = cue_times(words, [s.get('say')], default_from=0.3)[0] if s.get('say') else 0.3
            body += f'<div class="headline" data-rise="{hk}" data-fit="70"><span>{head}</span></div>'
            open(prev, 'w').write(page(body, script=script))
        elif kind == 'phone':
            screen = s['screen']
            cues = re.findall(r'data-say="([^"]*)"', screen)
            times = cue_times(words, cues)
            it = iter(times)
            def timed(m):
                t = next(it); pops.append(t)
                return f'data-{m.group(2)}="{t}"'
            screen = re.sub(r'data-say="([^"]*)" data-anim="(pop|rise)"', timed, screen)
            hk = cue_times(words, [s.get('say')], default_from=0.3)[0] if s.get('say') else 0.3
            body = f'<div class="phone"><div class="notch"></div><div class="screen">\n{screen}\n</div></div>\n<div class="headline" data-rise="{hk}" data-fit="70"><span>{head}</span></div>'
            open(prev, 'w').write(page(body, css=s.get('css', ''), script=script))
        else:
            raise SystemExit(f'{s["page"]}: unknown kind {kind}')
        # pops: never closer than 0.25 s to each other, never under the whoosh that opens the shot
        last = 0.35 if idx > 0 else -1
        for t in sorted(pops):
            if t >= last + 0.25 or (idx == 0 and last < 0):
                t = max(t, 0.35 if idx > 0 else t)
                sfx.append([idx, 'pop', round(t, 2)]); last = t
    # a ding must not collide with a pop either
    by_shot = {}
    for e in sfx: by_shot.setdefault(e[0], []).append(e)
    clean = []
    for i in sorted(by_shot):
        ev = sorted(by_shot[i], key=lambda e: e[2]); last = -9
        for e in ev:
            gap = 0.5 if clean and clean[-1][1] == 'whoosh' and clean[-1][0] == i else 0.25
            if e[2] - last >= gap or e[1] == 'whoosh': clean.append(e); last = e[2]
    spec['sfx'] = clean
    txt = json.dumps(spec, indent=1, ensure_ascii=False)
    open(spec_path, 'w').write(txt + '\n')
    print(f'{film}: {len([s for s in spec["shots"] if s.get("kind")])} pages, {len(clean)} sound effects')


if __name__ == '__main__':
    if len(sys.argv) != 2: raise SystemExit(__doc__)
    build_pages(sys.argv[1])
