"""Scenes for the iContact Academy ads (explainer, 60 s, teaser) and the story film (Tendai, an invented student).
Built on aiv_pages / email_pages: one page per shot, laid out for 16:9, 9:16 and 4:5. Every screen is invented and labelled
Example; Tendai is shown only as an initial (no realistic person), and the film says she is invented.
Facts come from the Academy page: self-paced, short video lessons + notes on any device, built from real client work,
one payment per course, keep access incl. updates, EcoCash / Paynow / bank transfer, login by WhatsApp or email usually
the same day, beginner courses, same Client Portal login for clients."""
from aiv_pages import page, card, st, f, TICK, endcard  # noqa: F401
import email_pages as E

E.ICON.update({
    'cap': '<path d="M6 24L32 12l26 12-26 12z"/><path d="M16 29v11c0 4 7 8 16 8s16-4 16-8V29"/><path d="M58 24v14"/>',
    'clock': '<circle cx="32" cy="32" r="22"/><path d="M32 20v13l9 6"/>',
    'play': '<rect x="8" y="12" width="48" height="34" rx="5"/><path d="M27 22l12 7-12 7z"/><path d="M18 54h28"/>',
    'build': '<rect x="8" y="10" width="48" height="40" rx="4"/><path d="M8 20h48M18 30h18M18 38h26"/>',
    'chart': '<path d="M10 52h44"/><rect x="14" y="34" width="8" height="18"/><rect x="28" y="24" width="8" height="28"/><rect x="42" y="14" width="8" height="38"/>',
    'pin': '<path d="M32 56s-16-15-16-28a16 16 0 0 1 32 0c0 13-16 28-16 28z"/><circle cx="32" cy="28" r="6"/>',
    'coin': '<circle cx="32" cy="32" r="22"/><path d="M38 24c-2-3-11-4-12 1-1 6 13 4 12 10-1 5-10 4-13 1M32 18v4M32 42v4"/>',
    'phone': '<rect x="20" y="6" width="24" height="52" rx="5"/><path d="M29 50h6"/>',
    'heart': '<path d="M32 52s-18-10.5-18-24a10 10 0 0 1 18-6 10 10 0 0 1 18 6c0 13.5-18 24-18 24z"/>',
    'star': '<path d="M32 8l7 15 16 2-12 11 3 16-14-8-14 8 3-16-12-11 16-2z"/>',
})
split = E.split

CSS2 = '''.player { position: relative; height: 230px; margin: 20px 22px 0; border-radius: 16px; background: linear-gradient(135deg, #1c3a61, #2E5795); display: grid; place-items: center; color: #fff; overflow: hidden; }
  .player .pl { width: 74px; height: 74px; border-radius: 50%; background: rgba(255,255,255,0.18); display: grid; place-items: center; }
  .player .pl svg { width: 34px; height: 34px; fill: #fff; }
  .player .ttl { position: absolute; left: 18px; top: 16px; font: 700 20px var(--f); }
  .bar { height: 10px; border-radius: 5px; background: #e6eaf0; margin: 16px 22px 0; overflow: hidden; }
  .bar i { display: block; height: 100%; background: #abcf47; border-radius: 5px; }
  .ctrls { display: flex; gap: 10px; flex-wrap: wrap; padding: 16px 22px; }
  .ctrl { font: 700 18px/1 var(--f-ui); padding: 12px 14px; border-radius: 10px; background: #eef1f5; color: var(--paper-muted); }
  .ctrl.on { background: #2E5795; color: #fff; }
  .site { position: relative; padding: 18px 22px; }
  .site .blk { border-radius: 12px; margin-bottom: 12px; }
  .site .hero { height: 120px; background: linear-gradient(135deg, #fbe7d3, #f6c9a2); display: flex; flex-direction: column; justify-content: center; padding: 0 20px; }
  .site .hero b { font: 800 30px var(--f); color: #6b3410; } .site .hero span { font: 500 17px var(--f-ui); color: #8a5a35; }
  .site .menu { display: flex; gap: 10px; } .site .menu i { flex: 1; height: 88px; border-radius: 12px; background: #f3e5d8; }
  .site .wab { display: inline-flex; gap: 10px; align-items: center; background: #25a244; color: #fff; font: 700 19px var(--f-ui); padding: 13px 16px; border-radius: 12px; }
  .url { display: flex; align-items: center; gap: 10px; margin: 14px 22px 0; padding: 10px 14px; border-radius: 10px; background: #f1f3f6; font: 500 17px var(--f-ui); color: var(--paper-muted); }
  .tiles { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; padding: 22px; }
  .tile { border-radius: 18px; border: 2px solid var(--paper-line); padding: 24px 14px; text-align: center; font: 800 26px var(--f); color: var(--paper-ink); }
  .tile small { display: block; margin-top: 8px; font: 500 15px var(--f-ui); color: var(--paper-muted); }
  .tile.on { border-color: #abcf47; background: #f4f9e7; }
  .avatar { width: 150px; height: 150px; border-radius: 50%; background: linear-gradient(135deg, #f6c9a2, #e79a5f); display: grid; place-items: center; font: 800 70px var(--f); color: #6b3410; box-shadow: 0 0 0 8px rgba(171,207,71,0.25); }
  .wk { display: grid; grid-template-columns: repeat(7, 1fr); gap: 10px; padding: 20px 22px; }
  .wk div { text-align: center; font: 600 15px var(--f-ui); color: var(--paper-muted); }
  .wk i { display: block; margin: 10px auto 0; width: 34px; height: 34px; border-radius: 10px; background: #eef1f5; }
  .wk i.on { background: #abcf47; }
  .gbp .stars { color: #f5b301; font-size: 20px; letter-spacing: 2px; }
  .chips { display: flex; gap: 10px; flex-wrap: wrap; padding: 4px 22px 18px; }
  .chip { font: 700 17px/1 var(--f-ui); padding: 12px 14px; border-radius: 999px; background: #e3ecf8; color: #2E5795; }'''

PLAY = '<svg viewBox="0 0 24 24"><path d="M8 5l11 7-11 7z"/></svg>'
WA_ICON = '<svg viewBox="0 0 32 32" style="width:22px;height:22px"><path d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3z" fill="#fff"/></svg>'


def s(icon, kick, title, sub, art, w, h, extra=''):
    html = split(icon, kick, title, sub, art, w, h, extra)
    return html.replace('</style>', CSS2 + '</style>', 1)


def A(T): return lambda p: 0.35 + T * p


# ---------------------------------------------------------------- explainer / ads

def hook(T, title='Learn the skills that <span class="ac">bring in customers</span>'):
    a = A(T)
    inner = f'''<div class="player"><span class="ttl">Lesson 3 · Get found on Google</span><span class="pl" data-pop="{f(a(0.1))}">{PLAY}</span></div>
      <div class="bar"><i style="width:0%" data-w="{f(a(0.25))}"></i></div>
      <div class="ctrls"><span class="ctrl on">On your phone</span><span class="ctrl" data-on="{f(a(0.5))}">At your own pace</span></div>'''
    grow = ", (t) => { document.querySelectorAll('.bar i').forEach((b) => { const s = +b.dataset.w; b.style.width = Math.max(0, Math.min(62, (t - s) * 30)) + '%'; }); }"
    return s('cap', 'iContact Academy', title, '', card('Example lesson', inner, 640, 420), 640, 420, grow)


def intro(T):
    a = A(T)
    rows = ''.join(f'<div class="row" data-rise="{f(a(0.25 + i * 0.15))}"><span class="av">{ic}</span><span class="m"><b>{t}</b><small>{d}</small></span><span class="st on">Self-paced</span></div>'
                   for i, (ic, t, d) in enumerate([('DM', 'Digital marketing', 'Get a business found and chosen online'), ('WD', 'Website development', 'Build sites that bring in enquiries')]))
    body = f'''    <div class="txt"><div class="plate" data-pop="0.1"><img src="img/icontact-logo.png" alt="iContact Africa Solutions"></div>
      <div class="h" data-rise="0.4">iContact <span class="ac">Academy</span></div><div class="s" data-rise="0.6">Self-paced online courses</div></div>
    <div class="vis"><div class="art" data-w="680" data-h="300">{card('Courses', rows, 680, 300, 0, 0, 0.3)}</div></div>'''
    return page(body, css=E.CSS + CSS2)


def realwork(T):
    a = A(T)
    items = [('Websites', 'Built for real clients'), ('Search', 'Local SEO and Google'), ('Social media', 'Content that gets enquiries'), ('Ads', 'Campaigns that are measured')]
    inner = ''.join(f'<div class="row" data-rise="{f(a(0.1 + i * 0.15))}"><span class="m"><b>{t}</b><small>{d}</small></span><span class="st on">Real work</span></div>' for i, (t, d) in enumerate(items))
    return s('star', 'Not theory', 'Built from <span class="ac">real client work</span>', 'The skills we use every day.', card('What you learn', inner, 660, 420), 660, 420)


def tracks(T):
    a = A(T)
    def pane(x, head, sub, items, at):
        lis = ''.join(f'<div class="li" data-rise="{f(at + 0.3 + j * 0.3)}">{TICK}<span>{it}</span></div>' for j, it in enumerate(items))
        return f'<div class="pane" data-rise="{f(at)}" style="left:{x}px;top:0;width:700px;height:520px"><h3>{head}</h3><div class="note">{sub}</div><div style="margin-top:14px">{lis}</div></div>'
    land = pane(0, '<span class="ac">Digital</span> marketing', 'Get a business found and chosen online', ['Google Business Profile', 'Local search', 'Social media', 'Ad campaigns'], a(0.2)) + \
        pane(760, '<span class="ac">Website</span> development', 'Build sites that bring in enquiries', ['Pages that convert', 'Mobile-first design', 'WhatsApp buttons', 'Publishing your site'], a(0.55))
    def vpane(y, head, sub, items, at):
        lis = ''.join(f'<div class="li" data-rise="{f(at + 0.3 + j * 0.25)}" style="font-size:24px;margin:8px 18px 8px 0">{TICK}<span>{it}</span></div>' for j, it in enumerate(items))
        return f'<div class="pane" data-rise="{f(at)}" style="left:0;top:{y}px;width:900px;height:340px;padding:26px 30px"><h3 style="font-size:36px;margin-bottom:6px">{head}</h3><div class="note">{sub}</div><div style="display:flex;flex-wrap:wrap">{lis}</div></div>'
    vert = vpane(0, '<span class="ac">Digital</span> marketing', 'Get a business found and chosen online', ['Google Business Profile', 'Local search', 'Social media', 'Ad campaigns'], a(0.2)) + \
        vpane(380, '<span class="ac">Website</span> development', 'Build sites that bring in enquiries', ['Pages that convert', 'Mobile-first design', 'WhatsApp buttons', 'Publishing your site'], a(0.55))
    body = f'''    <div class="txt"><div class="kick" data-rise="0.1">Choose your track</div></div>
    <div class="vis"><div class="art only-L" data-w="1460" data-h="520">{land}</div><div class="art only-V" data-w="900" data-h="720">{vert}</div></div>'''
    return page(body, wide=True, noh=True, css=E.CSS + CSS2)


def selfpaced(T, kick='Self-paced', title='Learn <span class="ac">when it suits you</span>', sub='Start any time. No deadlines.'):
    a = A(T)
    inner = f'''<div class="player"><span class="ttl">Lesson 5 · Your first landing page</span><span class="pl">{PLAY}</span></div>
      <div class="ctrls"><span class="ctrl" data-on="{f(a(0.35))}">❚❚ Pause</span><span class="ctrl" data-on="{f(a(0.5))}">↺ Rewatch</span><span class="ctrl" data-on="{f(a(0.7))}">▶ Pick up where you left off</span></div>
      <div class="ok" data-rise="{f(a(0.8))}" style="margin-top:0">{TICK} Progress saved</div>'''
    return s('clock', kick, title, sub, card('Example lesson', inner, 660, 460), 660, 460)


def devices(T):
    a = A(T)
    art = ''.join(f'<div class="dev" data-rise="{f(a(0.05 + i * 0.15))}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><h4>{n}</h4><div class="line b"></div><div class="line"></div>'
                  f'<div class="bar" style="margin:16px 0 0"><i style="width:{p}%"></i></div><div style="font:600 15px var(--f-ui);color:var(--paper-muted);margin-top:10px">Lesson {l} · saved</div></div>'
                  for i, (n, x, y, w, h, p, l) in enumerate([('Phone', 0, 60, 220, 360, 40, 4), ('Tablet', 240, 0, 320, 230, 40, 4), ('Laptop', 240, 250, 320, 230, 40, 4)]))
    return s('phone', 'Any device', 'Phone, tablet <span class="ac">or laptop</span>', 'Short video lessons and notes. Progress saved as you go.', art, 560, 480)


def project_intro(T):
    a = A(T)
    inner = ''.join(f'<div class="row" data-rise="{f(a(0.1 + i * 0.2))}"><span class="m"><b>{t}</b><small>{d}</small></span>{st("Lessons", "Project", a(0.25 + i * 0.2), "blue")}</div>'
                    for i, (t, d) in enumerate([('Website development', 'Build and publish a working website'), ('Digital marketing', 'Plan a campaign and set up a Google Business Profile')]))
    return s('build', 'Not just watching', 'Every track ends in a <span class="ac">realistic project</span>', '', card('Your projects', inner, 680, 300), 680, 300)


def site_build(T, kick='Website development project', title='Build and <span class="ac">publish a real site</span>', sub='For a small business, step by step.', live_at=0.8, name='Example Bakery'):
    a = A(T)
    inner = f'''<div class="url" data-rise="0.2">🔒 examplebakery.co.zw <span class="st" style="margin-left:auto" data-on="{f(a(live_at))}"><span class="a">Draft</span><span class="b">Live</span></span></div>
      <div class="site"><div class="blk hero" data-rise="{f(a(0.1))}"><b>{name}</b><span>Cakes for every celebration · Harare</span></div>
        <div class="blk menu" data-rise="{f(a(0.3))}"><i></i><i></i><i></i></div>
        <div data-rise="{f(a(0.5))}" style="display:flex;justify-content:space-between;align-items:center;font:600 18px var(--f-ui);color:var(--paper-ink)"><span>Birthday cakes from Example prices</span><span class="wab">{WA_ICON} Order on WhatsApp</span></div></div>'''
    return s('build', kick, title, sub, card(f'{name} · Example', inner, 700, 470), 700, 470)


def marketing(T, kick='Digital marketing project', title='Plan a campaign. <span class="ac">Get found.</span>', sub='Then set up a Google Business Profile.'):
    a = A(T)
    plan = ''.join(f'<div class="field" data-rise="{f(a(0.05 + i * 0.1))}"><span>{k}</span><b>{v}</b></div>'
                   for i, (k, v) in enumerate([('Goal', 'More cake orders'), ('Audience', 'Nearby, planning parties'), ('Channel', 'Facebook and Instagram'), ('Message', 'Order on WhatsApp')]))
    gbp = f'''<div class="row gbp" style="border-bottom:0"><span class="av">EB</span><span class="m"><b>Example Bakery</b><small>Bakery · Harare · Open today</small></span></div>
      <div class="chips"><span class="chip">Call</span><span class="chip">Directions</span><span class="chip">Website</span></div>'''
    art = card('Campaign plan', plan + '<div style="height:20px"></div>', 520, 380, 0, 0, a(0.02)) + card('Google Business Profile', gbp, 520, 220, 120, 330, a(0.55))
    return s('chart', kick, title, sub, art, 640, 560)


def zimbabwe(T):
    a = A(T)
    items = [('EcoCash', 'Payments people already use'), ('Local search', 'Being found in Harare and beyond'), ('WhatsApp', 'Where customers actually message'), ('.co.zw', 'Local domains and hosting')]
    inner = ''.join(f'<div class="row" data-rise="{f(a(0.05 + i * 0.15))}"><span class="m"><b>{t}</b><small>{d}</small></span><span class="st on">Covered</span></div>' for i, (t, d) in enumerate(items))
    return s('pin', 'Made for Zimbabwe', 'Examples and tools <span class="ac">that work here</span>', '', card('In the lessons', inner, 660, 420), 660, 420)


def value(T, kick='Value for money', title='One payment. <span class="ac">Yours to keep.</span>', sub='No subscription. No deadline.'):
    a = A(T)
    rows = [('Video lessons and notes', 'Included'), ('Realistic project', 'Included'), ('Updates to the lessons', 'Included'), ('Subscription', 'None'), ('Deadline', 'None')]
    inner = (f'<div class="big" data-rise="{f(a(0.02))}"><div class="l">Payment</div><div class="v">One payment per course</div></div>'
             + ''.join(f'<div class="row" data-rise="{f(a(0.15 + i * 0.12))}"><span class="m"><b>{t}</b></span><span class="st on">{v}</span></div>' for i, (t, v) in enumerate(rows)))
    return s('coin', kick, title, sub, card('Example course', inner, 640, 560), 640, 560)


def payment(T, kick='Easy to pay', title='EcoCash, Paynow <span class="ac">or bank transfer</span>', sub='Whichever suits you.'):
    a = A(T)
    tiles = ''.join(f'<div class="tile" data-pop="{f(a(0.2 + i * 0.18))}">{t}<small>{d}</small></div>' for i, (t, d) in enumerate([('EcoCash', 'Mobile money'), ('Paynow', 'Online'), ('Bank', 'Transfer')]))
    inner = f'<div class="tiles">{tiles}</div><div class="ok" data-rise="{f(a(0.8))}" style="margin-top:0">{TICK} Payment confirmed</div>'
    return s('coin', kick, title, sub, card('Pay for your course', inner, 680, 330), 680, 330)


def steps(T):
    a = A(T)
    items = [('1', 'Choose a course', 'Every lesson and the price on the page'), ('2', 'Request your place and pay', 'EcoCash, Paynow or bank transfer'), ('3', 'Get your login', 'By WhatsApp or email, usually the same day'), ('4', 'Learn at your pace', 'Tick off each lesson as you go')]
    inner = ''.join(f'<div class="row" data-rise="{f(a(0.04 + i * 0.18))}"><span class="av">{n}</span><span class="m"><b>{t}</b><small>{d}</small></span>{st("Next", "Done", a(0.14 + i * 0.18))}</div>' for i, (n, t, d) in enumerate(items))
    inner += f'<div class="bub ai" data-rise="{f(a(0.62))}" style="margin-bottom:18px"><small>WhatsApp · Example</small>Your iContact Academy login is ready. Happy learning!</div>'
    return s(None, 'How it works', 'From enrolment <span class="ac">to your first lesson</span>', '', card('Enrolment', inner, 680, 560), 680, 560)


def beginner(T):
    a = A(T)
    inner = (f'<div class="big" data-rise="{f(a(0.05))}"><div class="l">Level</div><div class="v">Beginner</div></div>'
             + ''.join(f'<div class="row" data-rise="{f(a(0.25 + i * 0.15))}"><span class="m"><b>{t}</b></span><span class="st on">✓</span></div>' for i, t in enumerate(['No experience needed', 'Just a phone or a computer', 'Step-by-step lessons'])))
    return s('heart', 'New to this?', 'Start <span class="ac">from zero</span>', 'Each course page shows its level.', card('Example course level', inner, 600, 390), 600, 390)


def portal(T):
    a = A(T)
    inner = ''.join(f'<div class="row" data-rise="{f(a(0.05 + i * 0.12))}"><span class="m"><b>{t}</b><small>{d}</small></span>{tag}</div>'
                    for i, (t, d, tag) in enumerate([('Projects', 'Track your website project', '<span class="st">Open</span>'), ('Invoices', 'Pay and download', '<span class="st">Open</span>'),
                                                    ('My courses', 'Your Academy lessons', st('…', 'New', a(0.5)))]))
    return s('key', 'Already a client?', 'Same <span class="ac">Client Portal</span> login', 'Your courses appear alongside your projects.', card('Client Portal · Example', inner, 640, 360), 640, 360)


def recap(T, items=('Self-paced lessons', 'A realistic project', 'One payment per course', 'EcoCash, Paynow or bank transfer'), kick='iContact Academy', title=None):
    a = A(T)
    lis = ''.join(f'<div class="li" data-rise="{f(a(0.05 + i * 0.2))}">{TICK}<span>{x}</span></div>' for i, x in enumerate(items))
    art = f'<div class="pane" data-rise="0.1" style="left:0;top:0;width:640px;height:360px">{lis}</div>'
    return s('cap', kick, title or 'Everything you need <span class="ac">to start</span>', '', art, 640, 360)


def end(tag='Learn the skills that <span>bring in customers.</span>'):
    return endcard(tag, 'ACADEMY')


# ---------------------------------------------------------------- the story (Tendai is invented)

def who(T, name='Tendai'):
    a = A(T)
    chat = ''.join(f'<div class="bub {cls}" data-rise="{f(a(0.25 + i * 0.18))}"><small>{who}</small>{msg}</div>'
                   for i, (cls, who, msg) in enumerate([('you', 'Example customer', 'Hi! Do you have a chocolate cake for Saturday?'), ('ai', name, 'Yes! I can bake one for you 🎂'), ('you', 'Example customer', 'Perfect. Where can I see your cakes?')]))
    art = f'<div data-pop="0.2" style="position:absolute;left:0;top:120px"><div class="avatar">{name[0]}</div></div>' + card('WhatsApp orders', chat + '<div style="height:16px"></div>', 520, 420, 180, 0, 0.4)
    return s(None, 'Example story', f'Meet <span class="ac">{name}</span>', 'She bakes the best cakes in her neighbourhood.', art, 700, 430)


def problem(T):
    a = A(T)
    rows = [('Hire a web designer?', 'Not in the budget yet', 'red'), ('Do it herself?', 'No idea where to start', 'red'), ('Find customers online?', 'She really wants to', '')]
    inner = ''.join(f'<div class="row" data-rise="{f(a(0.05 + i * 0.22))}"><span class="m"><b>{t}</b><small>{d}</small></span><span class="st {c}">{"?" if c else "Yes"}</span></div>' for i, (t, d, c) in enumerate(rows))
    return s(None, 'Example story', 'Where do you <span class="ac">even start?</span>', '', card("Tendai's thoughts", inner, 640, 330), 640, 330)


def finds(T):
    return intro(T).replace('Self-paced online courses', 'One evening, she finds it')


def coursepage(T):
    a = A(T)
    lessons = ''.join(f'<div class="row" data-rise="{f(a(0.05 + i * 0.08))}"><span class="av">{i + 1}</span><span class="m"><b>{t}</b></span><span class="st">Video + notes</span></div>'
                      for i, t in enumerate(['Plan your pages', 'Write words that sell', 'Design for phones', 'Add a WhatsApp button', 'Publish your site']))
    inner = lessons + f'<div class="ok blue" data-rise="{f(a(0.6))}">{TICK} One payment for the whole course</div>'
    return s('build', 'Website development', 'Every lesson. <span class="ac">One price.</span>', 'All on the course page.', card('Course page · Example', inner, 660, 540), 660, 540)


def paid(T):
    a = A(T)
    inner = (f'<div class="tiles"><div class="tile on" data-pop="{f(a(0.05))}">EcoCash<small>Mobile money</small></div><div class="tile">Paynow<small>Online</small></div><div class="tile">Bank<small>Transfer</small></div></div>'
             f'<div class="bub ai" data-rise="{f(a(0.45))}" style="margin-bottom:20px"><small>WhatsApp · same day</small>Hi Tendai! Your iContact Academy login is ready. Happy learning!</div>')
    return s(None, 'Example story', 'Paid with EcoCash. <span class="ac">Login the same day.</span>', '', card('Payment', inner, 680, 380), 680, 380)


def bus(T):
    return selfpaced(T, 'Example story', 'Lesson one, <span class="ac">on the way home</span>', 'Short videos, clear notes, progress saved.')


def pace(T):
    a = A(T)
    days = 'Mon Tue Wed Thu Fri Sat Sun'.split()
    pattern = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
    wk = lambda off, start: ''.join(f'<div>{d}<i class="{"on" if pattern[off + i] else ""}" data-rise="{f(a(start + i * 0.03))}"></i></div>' for i, d in enumerate(days))
    inner = (f'<div style="padding:16px 22px 0;font:700 18px var(--f-ui)">Week 1</div><div class="wk">{wk(0, 0.05)}</div>'
             f'<div style="padding:0 22px;font:700 18px var(--f-ui)">Week 2</div><div class="wk">{wk(7, 0.35)}</div>'
             f'<div class="ok" data-rise="{f(a(0.7))}">{TICK} No deadlines. The course waits.</div>')
    return s('clock', 'Example story', 'Her pace. <span class="ac">Her schedule.</span>', '', card('Lessons done', inner, 640, 440), 640, 440)


def rewatch(T):
    a = A(T)
    inner = f'''<div class="player"><span class="ttl">Lesson 4 · Add a WhatsApp button</span><span class="pl">{PLAY}</span></div>
      <div class="ctrls">{''.join(f'<span class="ctrl" data-on="{f(a(0.2 + i * 0.2))}">↺ Rewatch</span>' for i in range(3))}</div>
      <div class="ok" data-rise="{f(a(0.8))}" style="margin-top:0">{TICK} Got it</div>'''
    return s(None, 'Example story', 'Rewatch it <span class="ac">as often as you need</span>', '', card('Example lesson', inner, 660, 460), 660, 460)


def brief(T):
    a = A(T)
    inner = ''.join(f'<div class="field" data-rise="{f(a(0.05 + i * 0.12))}"><span>{k}</span><b>{v}</b></div>'
                    for i, (k, v) in enumerate([('Project', 'A real website'), ('For', 'A small business'), ('Tendai chose', 'Her own bakery'), ('Must include', 'Pages, prices, photos, WhatsApp')])) + '<div style="height:22px"></div>'
    return s('build', 'The project', 'Build a real website <span class="ac">for a small business</span>', '', card('Project brief · Example', inner, 640, 360), 640, 360)


def shaping(T):
    return site_build(T, 'Example story', 'Step by step, <span class="ac">it takes shape</span>', 'Cakes, prices, photos and an order button.', live_at=2.0, name="Tendai's Bakery")


def live(T):
    return site_build(T, 'Example story', "It's live. <span class=\"ac\">She built it.</span>", '', live_at=0.15, name="Tendai's Bakery")


def nextcourse(T):
    return marketing(T, 'Example story', 'Next: digital marketing', 'A campaign plan and a Google Business Profile.').replace('Example Bakery', "Tendai's Bakery")


def account(T):
    a = A(T)
    inner = ''.join(f'<div class="row" data-rise="{f(a(0.05 + i * 0.15))}"><span class="m"><b>{t}</b><small>{d}</small></span>{tag}</div>'
                    for i, (t, d, tag) in enumerate([('Website development', 'Completed · project published', '<span class="st on">Done</span>'),
                                                    ('Digital marketing', 'In progress', '<span class="st blue on">Lesson 6</span>'),
                                                    ('Lesson updates', 'Added to your courses', st('…', 'Updated', a(0.55)))]))
    return s('key', 'Example story', 'Hers <span class="ac">to come back to</span>', 'Every update included.', card('My courses · Example', inner, 640, 340), 640, 340)


def honest(T):
    a = A(T)
    body = f'''    <div class="txt"><div class="kick" data-rise="0.1">A quick note</div>
      <div class="h" data-rise="0.3">Tendai is invented. <span class="ac">The courses are real.</span></div>
      <div class="s" data-rise="{f(a(0.5))}">So is the project you'll build.</div></div>'''
    return page(body, wide=True, css=E.CSS + CSS2 + ' html.L .wide .txt, html.P .wide .txt, html.S .wide .txt { top: 0; height: 100%; justify-content: center; } html.P .wide .txt { top: 260px; height: 1040px; } html.S .wide .txt { height: 900px; }')
