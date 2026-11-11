"""Course trailers for the six published iContact Academy courses (about 60-75 s each, 16:9, 9:16 and 4:5, Nyasha's voice).
Every fact comes from the course's own page (title, subtitle, outcomes, who it's for, description, lesson list) as published
in the Academy catalogue on 11 Nov 2026. Prices are left out of the voice and screens so a price change never dates a video.
Screens are invented and labelled Example.

usage: python3 tools/build_trailers.py <short-name> --vo <dir of 1.mp3..N.mp3> [--speed x]
       python3 tools/build_trailers.py --lines        print every voice line (for generating the voiceover)
Output: icontact-pack/academy/trailers/<short-name>-16x9, -9x16, -4x5
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_aiv as B
import academy_pages as P
import email_pages as E
from aiv_pages import page, card, st, f, TICK, endcard

OUT = os.path.join(B.PACK, 'academy', 'trailers')
W = [('whoosh', -0.2, 0.22)]
A = P.A

CSS3 = '''.cover { height: 150px; margin: 20px 22px 0; border-radius: 16px; padding: 22px; display: flex; flex-direction: column; justify-content: flex-end; color: #fff; }
  .cover.web { background: linear-gradient(135deg, #1c3a61, #2E5795); } .cover.marketing { background: linear-gradient(135deg, #2E5795, #5e8f2a); }
  .cover small { font: 700 14px/1 var(--f-ui); letter-spacing: .14em; text-transform: uppercase; opacity: .8; margin-bottom: 10px; }
  .cover b { font: 800 30px/1.15 var(--f); }
  .code { margin: 16px 22px 0; padding: 18px 20px; border-radius: 12px; background: #0f1b2b; font: 500 19px/1.65 ui-monospace, Menlo, Consolas, monospace; color: #d6e4f5; white-space: pre; }
  .code .tg { color: #8fd3ff; } .code .at { color: #abcf47; } .code .vl { color: #f6c9a2; } .code .cm { color: #7c8da3; }
  html.L .h.ct { font-size: 60px; } html.P .h.ct { font-size: 62px; } html.S .h.ct { font-size: 44px; }
  .who { margin: 4px 26px 0; font: 600 23px/1.4 var(--f); color: var(--paper-ink); }'''


def s(icon, kick, title, sub, art, w, h):
    return P.s(icon, kick, title, sub, art, w, h).replace('</style>', CSS3 + '</style>', 1)


CAT = {'web': ('Website development', 'build'), 'marketing': ('Digital marketing', 'chart')}


# ---------------------------------------------------------------- scenes shared by every trailer

def cover(T, c, hook):
    a = A(T)
    cat, icon = CAT[c['cat']]
    inner = (f'<div class="cover {c["cat"]}" data-rise="{f(a(0.05))}"><small>{cat}</small><b>{c["title"]}</b></div>'
             f'<div class="chips" style="padding-top:18px">' + ''.join(
                 f'<span class="chip" data-pop="{f(a(0.3 + i * 0.12))}">{x}</span>' for i, x in enumerate([c['level'], f'{c["lessons"]} lessons', 'Self-paced'])) + '</div>')
    return s(icon, 'iContact Academy', hook, '', card('Online course', inner, 640, 330), 640, 330)


def titlecard(T, c):
    a = A(T)
    mods = c['modules']
    rows = ''.join(f'<div class="row" data-rise="{f(a(0.2 + i * 0.12))}"><span class="av">{i + 1}</span><span class="m"><b>{m}</b></span><span class="st">{n} lessons</span></div>'
                   for i, (m, n) in enumerate(mods))
    h = 84 + 78 * len(mods)
    body = f'''    <div class="txt"><div class="plate" data-pop="0.1"><img src="img/icontact-logo.png" alt="iContact Africa Solutions"></div>
      <div class="h ct" data-rise="0.4">{c["title_html"]}</div><div class="s" data-rise="0.6">{c["subtitle"]}</div></div>
    <div class="vis"><div class="art" data-w="680" data-h="{h}">{card(f'Curriculum · {c["lessons"]} lessons', rows, 680, h, 0, 0, 0.3)}</div></div>'''
    return page(body, css=E.CSS + P.CSS2 + CSS3)


def checklist(T, icon, kick, title, sub, head, items, tag=('…', '✓')):
    a = A(T)
    inner = ''.join(f'<div class="row" data-rise="{f(a(0.05 + i * 0.14))}"><span class="m"><b>{t}</b>{f"<small>{d}</small>" if d else ""}</span>{st(tag[0], tag[1], a(0.15 + i * 0.14))}</div>'
                    for i, (t, d) in enumerate(items))
    h = 84 + (90 if any(d for _, d in items) else 76) * len(items)
    return s(icon, kick, title, sub, card(head, inner + '<div style="height:10px"></div>', 660, h), 660, h)


def who(T, c, title):
    a = A(T)
    inner = (f'<div class="big" data-rise="{f(a(0.05))}"><div class="l">Level</div><div class="v">{c["level"]}</div></div>'
             f'<div class="who" data-rise="{f(a(0.2))}">{c["who"]}</div>'
             f'<div class="chips" style="padding-top:20px">' + ''.join(f'<span class="chip" data-pop="{f(a(0.45 + i * 0.12))}">{x}</span>' for i, x in enumerate(['Self-paced', 'Any device', 'Lessons + notes'])) + '</div>')
    return s('heart', "Who it's for", title, '', card("Who it's for", inner, 640, 400), 640, 400)


def pay(T):
    return P.payment(T, 'One payment per course', 'Pay once. <span class="ac">Keep access.</span>', 'Updates included. EcoCash, Paynow or bank.')


def end(tag):
    return endcard(tag, 'ACADEMY')


# ---------------------------------------------------------------- one showcase per course

def domain_email(T):
    return checklist(T, 'brand', 'Domains, hosting and email', 'Know what <span class="ac">you\'re paying for</span>', 'Explained in plain language.',
                     'Your business online · Example', [('examplebusiness.co.zw', 'Domain name'), ('Hosting', 'Where your site lives'),
                                                         ('SSL', 'The padlock in the address bar'), ('info@examplebusiness.co.zw', 'Professional email')], ('…', 'Done'))


def code_editor(T):
    a = A(T)
    lines = ['<span class="tg">&lt;section</span> <span class="at">class</span>=<span class="vl">"hero"</span><span class="tg">&gt;</span>',
             '  <span class="tg">&lt;h1&gt;</span>Example Bakery<span class="tg">&lt;/h1&gt;</span>',
             '  <span class="tg">&lt;a</span> <span class="at">class</span>=<span class="vl">"btn"</span><span class="tg">&gt;</span>Order on WhatsApp<span class="tg">&lt;/a&gt;</span>',
             '<span class="tg">&lt;/section&gt;</span>', '',
             '<span class="at">.hero</span> { <span class="tg">display</span>: <span class="vl">flex</span>; <span class="tg">gap</span>: <span class="vl">16px</span>; }',
             '<span class="cm">/* phones */</span>',
             '<span class="at">@media</span> (<span class="tg">max-width</span>: <span class="vl">600px</span>) { … }']
    code = ''.join(f'<div data-rise="{f(a(0.04 + i * 0.07))}">{ln or "&nbsp;"}</div>' for i, ln in enumerate(lines))
    inner = f'<div class="code">{code}</div><div class="ok" data-rise="{f(a(0.75))}">{TICK} Works on phones</div>'
    return s('build', 'HTML and CSS', 'Write it. <span class="ac">Style it.</span>', 'Flexbox, Grid and phone layouts.', card('index.html · Example', inner, 700, 470), 700, 470)


def project_site(T):
    html = P.site_build(T, 'Course project', 'A one-page <span class="ac">business site</span>', 'Then publish it free on GitHub Pages.', live_at=0.75)
    return html.replace('examplebakery.co.zw', 'yourname.github.io')


def gbp_check(T):
    a = A(T)
    head = '<div class="row gbp"><span class="av">EB</span><span class="m"><b>Example Bakery</b><small>Bakery · Harare · Open today</small></span></div>'
    rows = ''.join(f'<div class="row" data-rise="{f(a(0.1 + i * 0.15))}"><span class="m"><b>{t}</b></span>{st("…", "Done", a(0.2 + i * 0.15))}</div>'
                   for i, t in enumerate(['Profile verified', 'Photos, posts and products', 'Reviews answered']))
    inner = head + rows + '<div class="chips" style="padding-top:18px"><span class="chip">Call</span><span class="chip">Directions</span><span class="chip">Website</span></div>'
    return s('pin', 'Google Business Profile', 'Show up on <span class="ac">Search and Maps</span>', '', card('Google Business Profile · Example', inner, 640, 470), 640, 470)


def content_plan(T):
    a = A(T)
    rows = [('M', 'Tip of the week', 'Designed in Canva'), ('W', 'Short video', 'Filmed on your phone'), ('F', 'Product post', 'Caption that sells'), ('S', 'Customer question', 'Answered in comments')]
    inner = ''.join(f'<div class="row" data-rise="{f(a(0.05 + i * 0.14))}"><span class="av">{d}</span><span class="m"><b>{t}</b><small>{n}</small></span>{st("Planned", "Posted", a(0.3 + i * 0.14))}</div>'
                    for i, (d, t, n) in enumerate(rows))
    return s('list', 'Content', 'A <span class="ac">30-day content plan</span>', 'What to post, and when.', card('Content plan · Example', inner + '<div style="height:10px"></div>', 660, 400), 660, 400)


def ad_campaign(T):
    a = A(T)
    fields = [('Objective', 'Messages on WhatsApp'), ('Audience', 'Nearby, local customers'), ('Budget', 'A small daily budget'), ('Ad', 'Photo + Send message button')]
    inner = ''.join(f'<div class="field" data-rise="{f(a(0.05 + i * 0.13))}"><span>{k}</span><b>{v}</b></div>' for i, (k, v) in enumerate(fields))
    inner += f'<div class="ok" data-rise="{f(a(0.7))}">{TICK} Ready to publish</div>'
    return s('chart', 'Your first campaign', 'Ads that bring <span class="ac">WhatsApp messages</span>', '', card('New campaign · Example', inner, 660, 440), 660, 440)


def wa_chat(T):
    a = A(T)
    head = '<div class="row"><span class="av">EB</span><span class="m"><b>Example Bakery</b><small>Business account · Catalogue</small></span><span class="st on">Business</span></div>'
    chat = ''.join(f'<div class="bub {cls}" data-rise="{f(a(0.15 + i * 0.18))}"><small>{who}</small>{msg}</div>'
                   for i, (cls, who, msg) in enumerate([('you', 'Example customer', 'Hi! How much is the chocolate cake?'), ('ai', 'Quick reply', "Thanks for your message! Here's our catalogue 🎂")]))
    inner = head + chat + f'<div class="chips" style="padding-top:16px"><span class="chip" data-pop="{f(a(0.6))}">Label: New order</span><span class="chip" data-pop="{f(a(0.72))}">Away message on</span></div>'
    return s('reply', 'WhatsApp Business', 'Answer faster. <span class="ac">Sell more.</span>', '', card('WhatsApp Business · Example', inner, 660, 440), 660, 440)


# ---------------------------------------------------------------- the six courses (from the published catalogue)

COURSES = {
    'web-basics': dict(slug='website-basics-for-business', cat='web', level='Beginner', lessons=10, title='Website Basics for Business Owners',
                       title_html='Website Basics <span class="ac">for Business Owners</span>', subtitle='Plan, buy and launch a simple business website.',
                       modules=[('Getting started', 2), ('Domains, hosting and email', 3), ('Content that sells', 3), ('Launch and look after it', 2)],
                       who='Business owners and managers in Zimbabwe who want a website, or want to understand the one they have.'),
    'html-css': dict(slug='html-css-for-beginners', cat='web', level='Beginner', lessons=12, title='HTML & CSS for Beginners',
                     title_html='HTML &amp; CSS <span class="ac">for Beginners</span>', subtitle='Build and publish your first responsive web page.',
                     modules=[('Setting up', 2), ('HTML', 3), ('CSS', 4), ('Responsive and live', 3)],
                     who='Complete beginners who want to start building websites. You only need a laptop and internet.'),
    'seo-gbp': dict(slug='seo-and-google-business-profile', cat='marketing', level='Beginner', lessons=10, title='SEO & Google Business Profile',
                    title_html='SEO &amp; <span class="ac">Google Business Profile</span>', subtitle='Get your business found on Google Search and Maps.',
                    modules=[('How Google works', 2), ('Google Business Profile', 3), ('On-page SEO', 3), ('Measure and improve', 2)],
                    who='Business owners and marketers who want more customers to find them on Google.'),
    'social': dict(slug='social-media-marketing', cat='marketing', level='Beginner', lessons=9, title='Social Media Marketing for Small Business',
                   title_html='Social Media Marketing <span class="ac">for Small Business</span>', subtitle='Plan, create and post content that brings in customers.',
                   modules=[('Strategy', 3), ('Content', 4), ('Growth and results', 2)],
                   who='Business owners and social media managers who post but are not getting results.'),
    'meta-ads': dict(slug='facebook-instagram-ads-zimbabwe', cat='marketing', level='Intermediate', lessons=10, title='Facebook & Instagram Ads from Zimbabwe',
                     title_html='Facebook &amp; Instagram Ads <span class="ac">from Zimbabwe</span>', subtitle='Run paid ads that bring leads, on a small budget.',
                     modules=[('Set up', 3), ('Your first campaign', 4), ('Optimise', 3)],
                     who='Business owners and marketers ready to spend a small budget on ads. Basic social media experience helps.'),
    'whatsapp': dict(slug='whatsapp-business-for-sales', cat='marketing', level='Beginner', lessons=7, title='WhatsApp Business for Sales',
                     title_html='WhatsApp Business <span class="ac">for Sales</span>', subtitle='Turn WhatsApp into your best sales channel.',
                     modules=[('Set up', 2), ('Daily tools', 2), ('Selling', 3)],
                     who='Anyone who sells on WhatsApp and wants to look more professional and close more sales.'),
}

VALUE = 'Learn at your own pace, on any device. Pay once, by EcoCash, Paynow or bank transfer, and keep access to the course, including updates.'


def shot(page_name, line, html, sfx=None, **kw):
    return dict(page=page_name, line=line, html=html, sfx=W + (sfx or []), **kw)


def film(c, shots, end_line, tag):
    first = dict(shots[0]); first['sfx'] = [('pop', 'p', 0.25)]; first['cues'] = {'p': 0.15}
    return dict(speed=1.0, tail=0.25, end_tail=2.0, music=0.17, shots=[first] + shots[1:] + [
        shot('valuepay', VALUE, lambda T: pay(T), [('pop', 't0', 0.25), ('pop', 't1', 0.25), ('pop', 't2', 0.25)], cues={'t0': 0.2, 't1': 0.38, 't2': 0.56}),
        shot('endcard', end_line, lambda T: end(tag), [('shimmer', 0.8, 0.25)])])


def spec(name):
    c = COURSES[name]
    if name == 'web-basics':
        return film(c, [
            shot('hook', "Thinking about a website for your business, but not sure what you're paying for?", lambda T: cover(T, c, 'A website, <span class="ac">without wasting money</span>')),
            shot('title', 'Website Basics for Business Owners is a beginner course from iContact Academy. Plan, buy and launch a simple business website, without wasting money.', lambda T: titlecard(T, c)),
            shot('online', 'You will learn what a business website needs before you pay anyone, how to choose the right domain name, and how hosting, email and SSL work, in plain language.', lambda T: domain_email(T)),
            shot('content', 'Then you will write page content that turns visitors into enquiries, with clear calls to action and WhatsApp buttons.', lambda T: P.site_build(T, 'Content that sells', 'Pages that <span class="ac">bring in enquiries</span>', 'Clear calls to action and WhatsApp buttons.', live_at=0.7)),
            shot('launch', 'And you will finish with a launch checklist, and know how to keep your site fresh and secure.', lambda T: checklist(T, 'list', 'Launch and look after it', 'Launch it. <span class="ac">Keep it working.</span>', '', 'Launch checklist · Example',
                 [('Pages and content', ''), ('Domain, email and SSL', ''), ('WhatsApp buttons tested', ''), ('Updates and backups', '')])),
            shot('who', 'It is for business owners and managers in Zimbabwe who want a website, or want to understand the one they have.', lambda T: who(T, c, 'Built for <span class="ac">business owners</span>')),
        ], 'WhatsApp the word ACADEMY to iContact, and start today.', 'Know exactly what <span>your website needs.</span>')
    if name == 'html-css':
        return film(c, [
            shot('hook', 'Every website you visit is built with two languages. Want to learn them?', lambda T: cover(T, c, 'Learn the languages <span class="ac">behind every website</span>')),
            shot('title', 'HTML and CSS for Beginners, from iContact Academy. Build and publish your first responsive web page, from scratch.', lambda T: titlecard(T, c)),
            shot('learn', 'You will write clean HTML for headings, text, images and links, then style your pages with CSS colours, fonts and spacing.', lambda T: checklist(T, 'list', "What you'll learn", 'Clean HTML. <span class="ac">Styled with CSS.</span>', '', 'Lessons · Example',
                 [('Headings, paragraphs and lists', 'HTML'), ('Links and images', 'HTML'), ('Selectors, colours and fonts', 'CSS'), ('The box model and spacing', 'CSS')])),
            shot('code', 'You will build layouts with Flexbox and Grid, and make your pages work on phones. Each lesson ends with a small task, so you practise as you go.', lambda T: code_editor(T)),
            shot('project', 'And you will build a real one-page business site, then publish it, free, on GitHub Pages.', lambda T: project_site(T), [('ding', 'live', 0.3)], cues={'live': 0.75}),
            shot('who', 'It is for complete beginners. You only need a laptop and internet.', lambda T: who(T, c, 'Start <span class="ac">from zero</span>')),
        ], 'WhatsApp the word ACADEMY to iContact, and build your first website.', 'Build your first <span>website from scratch.</span>')
    if name == 'seo-gbp':
        return film(c, [
            shot('hook', 'When someone nearby searches for what you sell, do they find you?', lambda T: cover(T, c, 'Can customers <span class="ac">find you on Google?</span>')),
            shot('title', 'SEO and Google Business Profile, from iContact Academy. Get your business found on Google Search and Maps.', lambda T: titlecard(T, c)),
            shot('gbp', 'You will set up and verify a Google Business Profile, add photos, posts and products, and learn how to get and answer reviews.', lambda T: gbp_check(T)),
            shot('onpage', 'Then you will find the words your customers search for, using free tools, and improve your page titles, descriptions and content.', lambda T: checklist(T, 'list', 'On-page SEO', 'The words your <span class="ac">customers search for</span>', '', 'Your website · Example',
                 [('Keyword research', 'With free tools'), ('Page titles', ''), ('Meta descriptions', ''), ('Content that ranks', '')])),
            shot('measure', 'You will track results with Google Search Console, and build a simple monthly routine, the habits that move you up the results over time.', lambda T: checklist(T, 'chart', 'Measure and improve', 'A simple <span class="ac">monthly routine</span>', '', 'Monthly SEO routine · Example',
                 [('Check Search Console', ''), ('Post on your profile', ''), ('Answer new reviews', ''), ('Improve one page', '')])),
            shot('who', 'It is a hands-on guide to local SEO for Zimbabwean businesses, for owners and marketers who want more customers to find them on Google.', lambda T: who(T, c, 'Local SEO, <span class="ac">for Zimbabwe</span>')),
        ], 'WhatsApp the word ACADEMY to iContact, and get your business found.', 'Get found on <span>Google Search and Maps.</span>')
    if name == 'social':
        return film(c, [
            shot('hook', 'Posting on social media, but not getting customers?', lambda T: cover(T, c, 'Posts that <span class="ac">bring in customers</span>')),
            shot('title', 'Social Media Marketing for Small Business, from iContact Academy. Plan, create and post content that brings in customers.', lambda T: titlecard(T, c)),
            shot('strategy', 'You will choose the right platforms for your business, get to know your audience, and set goals you can measure.', lambda T: checklist(T, 'list', 'Strategy', 'Start with <span class="ac">a plan</span>', '', 'Strategy · Example',
                 [('Pick your platforms', ''), ('Know your audience', ''), ('Set goals you can measure', '')])),
            shot('plan', 'Then you will build a simple thirty-day content plan, design posts in Canva, film short videos on your phone, and write captions that sell.', lambda T: content_plan(T)),
            shot('growth', 'You will grow engagement without paying for it, read your insights, and keep improving.', lambda T: checklist(T, 'chart', 'Growth and results', 'Grow it. <span class="ac">Measure it.</span>', '', 'Insights · Example',
                 [('Engagement and community', 'Without paying for it'), ('Reading your insights', ''), ('What to improve next', '')])),
            shot('who', "It is a simple, repeatable system that fits around running a business, for owners and social media managers who post but aren't getting results.", lambda T: who(T, c, 'A system that <span class="ac">fits your week</span>')),
        ], 'WhatsApp the word ACADEMY to iContact, and start posting with a plan.', 'Turn followers into <span>paying customers.</span>')
    if name == 'meta-ads':
        return film(c, [
            shot('hook', 'Ready to run Facebook and Instagram ads, but worried about wasting money?', lambda T: cover(T, c, 'Ads that bring leads, <span class="ac">on a small budget</span>')),
            shot('title', 'Facebook and Instagram Ads from Zimbabwe, from iContact Academy. Run paid ads that bring leads, on a small budget.', lambda T: titlecard(T, c)),
            shot('setup', 'You will set up Meta Business Suite and an ad account, learn how to pay for ads from Zimbabwe, and install the Meta Pixel.', lambda T: checklist(T, 'tools', 'Set up', 'Ready to advertise <span class="ac">from Zimbabwe</span>', '', 'Set up · Example',
                 [('Meta Business Suite', ''), ('Ad account', ''), ('Paying for ads from Zimbabwe', ''), ('Meta Pixel', 'On your website')], ('…', 'Done'))),
            shot('campaign', 'Then you will build your first campaign: the right objective, a local audience, your budget, and ads that get clicks and WhatsApp messages.', lambda T: ad_campaign(T)),
            shot('optimise', 'You will read your results in Ads Manager, test and scale what works, retarget website visitors, and stop wasting budget.', lambda T: checklist(T, 'chart', 'Optimise', 'Keep what works. <span class="ac">Stop the waste.</span>', '', 'Ads Manager · Example',
                 [('Read your results', ''), ('Test and scale', ''), ('Retarget website visitors', '')])),
            shot('who', 'It is an intermediate course for owners and marketers ready to spend a small budget on ads. Basic social media experience helps.', lambda T: who(T, c, 'For when <span class="ac">you\'re ready to spend</span>')),
        ], 'WhatsApp the word ACADEMY to iContact, and make every dollar count.', 'Run ads that <span>bring in leads.</span>')
    if name == 'whatsapp':
        return film(c, [
            shot('hook', 'Your customers already message you on WhatsApp. Is it set up to sell?', lambda T: cover(T, c, 'Is your WhatsApp <span class="ac">set up to sell?</span>')),
            shot('title', 'WhatsApp Business for Sales, from iContact Academy. Turn WhatsApp into your best sales channel.', lambda T: titlecard(T, c)),
            shot('tools', 'You will set up a professional business profile and catalogue, and use labels, quick replies and away messages to answer faster.', lambda T: wa_chat(T)),
            shot('selling', 'Then you will write broadcast messages people actually read, post status updates that sell, and take an enquiry all the way to payment.', lambda T: checklist(T, 'list', 'Selling', 'From enquiry <span class="ac">to payment</span>', '', 'Selling · Example',
                 [('Broadcast lists that get read', ''), ('Status updates that sell', ''), ('From enquiry to payment', '')])),
            shot('links', 'You will also connect WhatsApp to your website and ads, with click-to-WhatsApp links.', lambda T: checklist(T, 'forward', 'Connect it', 'WhatsApp, <span class="ac">everywhere you sell</span>', '', 'Click-to-WhatsApp · Example',
                 [('Website button', ''), ('Facebook and Instagram ads', ''), ('Link in your bio', '')], ('…', 'Linked'))),
            shot('who', 'It is for anyone who sells on WhatsApp and wants to look more professional and close more sales.', lambda T: who(T, c, 'For anyone who <span class="ac">sells on WhatsApp</span>')),
        ], 'WhatsApp the word ACADEMY to iContact, and start selling smarter.', 'Turn WhatsApp into your <span>best sales channel.</span>')
    raise KeyError(name)


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['--lines']:
        for n in COURSES:
            print(f'## {n}')
            for i, sh in enumerate(spec(n)['shots'], 1): print(f'{i}. {sh["line"]}')
        raise SystemExit
    if not a or a[0] not in COURSES or '--vo' not in a: raise SystemExit(__doc__)
    B.build(a[0], a[a.index('--vo') + 1], out=OUT, spec=spec(a[0]),
            speed_override=float(a[a.index('--speed') + 1]) if '--speed' in a else None)
