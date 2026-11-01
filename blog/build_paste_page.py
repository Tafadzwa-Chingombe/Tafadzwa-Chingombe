"""Builds blog-articles.html: every article with copy buttons for each CMS field and the formatted body.
usage: python3 blog/build_paste_page.py   (needs: pip install markdown)"""
import glob, html, json, os, re
import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
FIELDS = [('title', 'Title'), ('slug', 'URL slug'), ('category', 'Category'), ('excerpt', 'Excerpt / meta description'),
          ('focus_keyword', 'Focus keyword'), ('cover_image', 'Cover image idea'), ('cover_alt', 'Cover image alt text'),
          ('related_video', 'Matching video to embed')]

cards, toc = [], []
for i, path in enumerate(sorted(glob.glob(os.path.join(HERE, '0*.md'))), 1):
    raw = open(path).read()
    fm, body = re.match(r'---\n(.*?)\n---\n(.*)', raw, re.S).groups()
    meta = {k: (v[1:-1] if v.startswith('"') and v.endswith('"') else v).strip() for k, v in re.findall(r'^(\w+): (.*)$', fm, re.M)}
    body = re.sub(r'^# .*\n', '', body, count=1).strip()          # the title goes in its own CMS field
    words = len(re.sub(r'[#*>|`\-\[\]()]', ' ', body).split())
    body_html = markdown.markdown(body, extensions=['tables', 'sane_lists'])
    rows = ''.join(
        f'<div class="field"><div class="lbl">{lab}</div><div class="val" id="a{i}-{k}">{html.escape(meta.get(k, ""))}</div>'
        f'<button onclick="copyText(\'a{i}-{k}\', this)">Copy</button></div>' for k, lab in FIELDS)
    toc.append(f'<li><a href="#art{i}">{html.escape(meta["title"])}</a> <span>{words:,} words</span></li>')
    cards.append(f'''<section class="card" id="art{i}">
  <div class="num">Article {i} of 9 · {words:,} words</div>
  <h2>{html.escape(meta["title"])}</h2>
  <div class="fields">{rows}</div>
  <div class="bodyhead"><span>Article body (paste into the content editor)</span><button class="primary" onclick="copyBody('a{i}-body', this)">Copy article</button></div>
  <article id="a{i}-body">{body_html}</article>
</section>''')

page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Blog Articles: Ready to Paste</title>
<style>
  :root {{ --bg:#f4f6fa; --card:#fff; --ink:#14213a; --muted:#5a6578; --line:#dde3ec; --blue:#2E5795; --green:#ABCF47; --navy:#0B1F3A; }}
  @media (prefers-color-scheme: dark) {{ :root {{ --bg:#0b1220; --card:#121b2d; --ink:#e7ecf5; --muted:#9aa7bd; --line:#24324a; --blue:#8fb0e8; }} }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--ink); font:16px/1.6 Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif; }}
  header {{ background:var(--navy); color:#fff; padding:28px 16px; }}
  header .in, main {{ max-width:900px; margin:0 auto; }}
  header h1 {{ margin:0 0 6px; font-size:26px; }} header h1 b {{ color:var(--green); }}
  header p {{ margin:0; color:#c9d4e6; }}
  main {{ padding:20px 16px 60px; }}
  .how {{ background:var(--card); border:1px solid var(--line); border-radius:14px; padding:16px 20px; }}
  .how ol {{ margin:8px 0 0; padding-left:20px; }} .how li {{ margin:4px 0; }}
  .toc {{ list-style:none; padding:0; margin:16px 0 0; }} .toc li {{ padding:6px 0; border-bottom:1px solid var(--line); display:flex; justify-content:space-between; gap:12px; }}
  .toc a {{ color:var(--blue); text-decoration:none; font-weight:600; }} .toc span {{ color:var(--muted); font-size:14px; white-space:nowrap; }}
  .card {{ background:var(--card); border:1px solid var(--line); border-radius:16px; padding:22px; margin-top:24px; }}
  .num {{ font-size:13px; font-weight:700; letter-spacing:.06em; text-transform:uppercase; color:var(--muted); }}
  .card h2 {{ margin:4px 0 14px; font-size:22px; line-height:1.3; }}
  .field {{ display:grid; grid-template-columns:170px 1fr auto; gap:10px; align-items:start; padding:8px 0; border-top:1px solid var(--line); }}
  .lbl {{ font-size:13px; font-weight:700; color:var(--muted); padding-top:2px; }}
  .val {{ font-size:15px; word-break:break-word; }}
  button {{ font:600 13px Inter, system-ui, sans-serif; padding:6px 12px; border-radius:8px; border:1px solid var(--line); background:var(--bg); color:var(--ink); cursor:pointer; }}
  button.primary {{ background:var(--blue); color:#fff; border-color:var(--blue); }}
  button.done {{ background:#1f7a4a; color:#fff; border-color:#1f7a4a; }}
  .bodyhead {{ display:flex; justify-content:space-between; align-items:center; gap:12px; margin:16px 0 8px; padding-top:14px; border-top:2px solid var(--line); font-weight:700; }}
  article {{ border:1px dashed var(--line); border-radius:12px; padding:4px 18px; max-height:520px; overflow:auto; }}
  article h2 {{ font-size:20px; }} article h3 {{ font-size:17px; }} article table {{ border-collapse:collapse; width:100%; font-size:14px; }}
  article th, article td {{ border:1px solid var(--line); padding:6px 8px; text-align:left; }} article a {{ color:var(--blue); }}
  article blockquote {{ margin:12px 0; padding:8px 14px; border-left:4px solid var(--green); background:var(--bg); }}
  @media (max-width:640px) {{ .field {{ grid-template-columns:1fr auto; }} .lbl {{ grid-column:1 / -1; }} }}
</style></head>
<body>
<header><div class="in"><h1>Blog articles: <b>ready to paste</b></h1>
<p>Nine SEO articles from the Zimbabwe keyword research · English only · phone-number CTAs</p></div></header>
<main>
  <div class="how"><b>How to post an article in your CMS</b>
    <ol>
      <li>In your admin, click <b>New article</b>.</li>
      <li>Copy each field below (title, slug, excerpt, category) into the matching box.</li>
      <li>Click <b>Copy article</b> and paste into the content editor. Headings, lists, tables and links keep their formatting.</li>
      <li>Upload a cover image and paste the <b>alt text</b>. Embed the matching video if you've posted it.</li>
      <li>Check the internal links (<code>/blog/…</code>) match your blog's URL pattern, then <b>Publish</b>.</li>
    </ol>
    <ul class="toc">{''.join(toc)}</ul>
  </div>
  {''.join(cards)}
</main>
<script>
function flash(btn, txt) {{ const o = btn.textContent; btn.textContent = txt; btn.classList.add('done'); setTimeout(() => {{ btn.textContent = o; btn.classList.remove('done'); }}, 1600); }}
async function copyText(id, btn) {{
  const t = document.getElementById(id).textContent;
  try {{ await navigator.clipboard.writeText(t); flash(btn, 'Copied'); }} catch (e) {{ selectEl(id); flash(btn, 'Press Ctrl+C'); }}
}}
async function copyBody(id, btn) {{
  const el = document.getElementById(id);
  try {{
    await navigator.clipboard.write([new ClipboardItem({{ 'text/html': new Blob([el.innerHTML], {{ type: 'text/html' }}),
                                                           'text/plain': new Blob([el.innerText], {{ type: 'text/plain' }}) }})]);
    flash(btn, 'Copied');
  }} catch (e) {{ selectEl(id); flash(btn, 'Press Ctrl+C'); }}
}}
function selectEl(id) {{ const r = document.createRange(); r.selectNodeContents(document.getElementById(id)); const s = getSelection(); s.removeAllRanges(); s.addRange(r); }}
</script>
</body></html>'''
open(os.path.join(HERE, 'blog-articles.html'), 'w').write(page)
print('wrote blog-articles.html')
