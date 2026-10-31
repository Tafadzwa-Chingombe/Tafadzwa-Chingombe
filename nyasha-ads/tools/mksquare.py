"""A 1:1 (1080×1080) cut of a vertical Nyasha film, as its own OpenFilm project beside it.
Each shot plays twice: sharp and scaled into a centre panel (the whole vertical layout, headline included),
and blurred to cover the frame behind it. The wordmark sits in the square's top-left; captions at the bottom.
usage: python3 mksquare.py <vertical-project> <square-project>"""
import os, re, shutil, sys

src, dst = sys.argv[1], sys.argv[2]
if os.path.exists(dst):
    for name in os.listdir(dst):
        if name in ('.film', 'film.html'): continue
        p = os.path.join(dst, name)
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
os.makedirs(dst, exist_ok=True)
for name in os.listdir(src):
    if name in ('.film', 'film.html') or name.endswith('.mp4'): continue
    p = os.path.join(src, name)
    (shutil.copytree if os.path.isdir(p) else shutil.copy2)(p, os.path.join(dst, name))

film = open(os.path.join(src, 'film.html')).read()
shots = re.findall(r'<iframe id="(?!chrome)([^"]+)" src="([^"]+)"(?: at="([^"]+)")?></iframe>', film)
chrome = re.search(r'<iframe id="chrome" src="([^"]+)"></iframe>', film).group(1)
sounds = re.findall(r'<section>\n((?:  <audio[^\n]*\n)+)</section>', film)

S = 0.65                                   # the panel's scale
W, H = round(1080 * S), round(1920 * S)    # 702 × 1248
LEFT = (1080 - W) // 2                     # 189
TOP = 900 - round(1580 * S)                # the headline band ends at y ≈ 900; captions go below it
at = lambda a: f' at="{a}"' if a else ''

out = ['<!doctype html>', '<html>', '<head>', '<meta charset="utf-8">', '<meta name="viewport" content="width=1080, height=1080">',
       '<style>',
       f'  .panel {{ -webkit-mask-image: linear-gradient(to right, transparent, #000 7%, #000 93%, transparent); mask-image: linear-gradient(to right, transparent, #000 7%, #000 93%, transparent); }}',
       '  .backdrop { filter: blur(36px) brightness(0.5) saturate(1.15); }',
       '</style>', '</head>', '<body>',
       '<section>', f'  <iframe id="chrome" src="{chrome}" size="1080x1920" style="left: 0px; top: -232px; width: 1080px; height: 1920px"></iframe>', '</section>',
       '<section>']
for id_, s, a in shots:
    out.append(f'  <iframe id="{id_}" src="{s}"{at(a)} size="1080x1920" class="panel" style="left: {LEFT}px; top: {TOP}px; width: {W}px; height: {H}px"></iframe>')
out += ['</section>', '<section>']
for id_, s, a in shots:
    out.append(f'  <iframe id="{id_}-backdrop" src="{s}"{at(a)} size="1080x1920" class="backdrop" style="left: -60px; top: -500px; width: 1200px; height: 2133px"></iframe>')
out.append('</section>')
for block in sounds:
    out += ['<section>', block.rstrip('\n'), '</section>']
out += ['</body>', '</html>', '']
open(os.path.join(dst, 'film.html'), 'w').write('\n'.join(out))
print(f'{dst}: {len(shots)} shots, panel {W}x{H} at ({LEFT},{TOP})')
