"""Scenes for the professional email explainer (built on aiv_pages' layout: one page per shot, laid out for 16:9, 9:16, 4:5).
Every address, business and screen is invented and labelled Example. The forwarding screens follow Gmail's real menu
names but are drawn as a plain settings window, with no Google logo or branding."""
from aiv_pages import page, card, st, li, f, TICK, pricing, endcard  # noqa: F401  (re-exported for the build)

BIZ = 'examplebusiness.co.zw'
OLD = 'plumber.example2019@gmail.com'

ICON = {
    'trust': '<path d="M32 8l20 8v14c0 13-9 22-20 26-11-4-20-13-20-26V16z"/><path d="M23 32l6 6 12-13"/>',
    'brand': '<rect x="10" y="16" width="44" height="32" rx="4"/><path d="M10 20l22 15 22-15"/>',
    'key': '<circle cx="22" cy="32" r="10"/><path d="M32 32h22M46 32v8M52 32v6"/>',
    'split': '<rect x="10" y="12" width="44" height="12" rx="3"/><rect x="10" y="28" width="44" height="12" rx="3"/><rect x="10" y="44" width="44" height="12" rx="3"/>',
    'lock': '<rect x="14" y="28" width="36" height="26" rx="4"/><path d="M22 28v-8a10 10 0 0 1 20 0v8"/><path d="M32 38v6"/>',
    'devices': '<rect x="8" y="14" width="34" height="24" rx="3"/><path d="M4 44h42"/><rect x="44" y="20" width="14" height="30" rx="3"/>',
    'forward': '<path d="M10 22h30l-8-8M40 22l-8 8"/><rect x="10" y="34" width="44" height="20" rx="3"/><path d="M10 37l22 10 22-10"/>',
    'reply': '<path d="M26 18L12 30l14 12"/><path d="M12 30h22c10 0 18 6 18 16"/>',
    'list': '<path d="M22 18h30M22 32h30M22 46h30"/><path d="M10 18l3 3 5-6M10 32l3 3 5-6M10 46l3 3 5-6"/>',
    'tools': '<path d="M40 10a10 10 0 0 0-12 13L12 39a5 5 0 0 0 7 7l16-16a10 10 0 0 0 13-12l-6 6-6-2-2-6z"/>',
}


def split(icon, kick, title, sub, art, w, h, extra=''):
    body = f'''    <div class="txt">{f'<div class="icon" data-pop="0.1"><svg viewBox="0 0 64 64">{ICON[icon]}</svg></div>' if icon else ''}
      {f'<div class="kick" data-rise="0.15">{kick}</div>' if kick else ''}<div class="h" data-rise="0.2">{title}</div>{f'<div class="s" data-rise="0.4">{sub}</div>' if sub else ''}</div>
    <div class="vis"><div class="art" data-w="{w}" data-h="{h}">{art}</div></div>'''
    return page(body, css=CSS, extra=extra)


CSS = '''.addr { font: 700 56px/1.1 var(--f); letter-spacing: -0.01em; color: var(--paper-ink); display: flex; flex-wrap: wrap; gap: 0 2px; }
  .addr span { display: inline-block; } .addr .biz { color: #2E5795; } .addr .dom { color: #3d6b10; }
  .parts { display: flex; gap: 16px; margin-top: 22px; flex-wrap: wrap; }
  .part { font: 600 18px/1.2 var(--f-ui); padding: 10px 14px; border-radius: 12px; background: #f1f3f6; color: var(--paper-muted); }
  .part b { color: var(--paper-ink); }
  .tabs { display: flex; gap: 6px; flex-wrap: wrap; padding: 14px 22px 0; border-bottom: 1px solid var(--paper-line); }
  .tab { font: 600 15px/1 var(--f-ui); padding: 12px 12px; color: var(--paper-muted); border-bottom: 3px solid transparent; }
  .tab.on { color: #2E5795; border-bottom-color: #2E5795; }
  .crumb { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; padding: 26px; }
  .crumb .c { font: 700 21px/1 var(--f-ui); padding: 14px 16px; border-radius: 12px; background: #f1f3f6; color: var(--paper-muted); }
  .crumb .c.on { background: #2E5795; color: #fff; } .crumb .arr { color: var(--paper-muted); font: 700 22px var(--f-ui); }
  .btn2 { display: inline-block; margin: 20px 26px 0; font: 700 19px/1 var(--f-ui); padding: 14px 18px; border-radius: 10px; border: 2px solid #2E5795; color: #2E5795; }
  .btn2.on { background: #2E5795; color: #fff; }
  .inp { margin: 14px 26px 0; padding: 14px 16px; border-radius: 10px; border: 2px solid #cfd8e3; font: 500 20px var(--f-ui); color: var(--paper-ink); }
  .radio { display: flex; gap: 12px; align-items: flex-start; margin: 14px 26px 0; font: 500 19px/1.45 var(--f-ui); color: var(--paper-muted); }
  .radio i { width: 22px; height: 22px; flex: none; border-radius: 50%; border: 2px solid #9aa7b6; margin-top: 3px; position: relative; }
  .radio.on { color: var(--paper-ink); } .radio.on i { border-color: #2E5795; } .radio.on i::after { content: ""; position: absolute; inset: 4px; border-radius: 50%; background: #2E5795; }
  .pill { display: inline-block; padding: 3px 8px; border-radius: 6px; background: #eef3fb; color: #2E5795; font-weight: 700; }
  .flow2 { position: absolute; inset: 0; }
  .fold { display: flex; gap: 14px; padding: 18px 26px; }
  .fold .x { flex: 1; padding: 16px; border-radius: 14px; background: #f1f3f6; font: 700 20px var(--f-ui); color: var(--paper-muted); text-align: center; }
  .fold .x.on { background: #e8f3d6; color: #3d6b10; }
  .dev { position: absolute; border-radius: 22px; background: var(--paper); color: var(--paper-ink); box-shadow: 0 24px 56px rgba(0,0,0,0.4); padding: 22px; font-family: var(--f-ui); }
  .dev h4 { margin: 0 0 12px; font: 700 22px var(--f); } .dev .line { height: 10px; border-radius: 5px; background: #e6eaf0; margin: 10px 0; }
  .dev .line.b { background: #cfdcf0; width: 70%; }'''


# ---------------------------------------------------------------- scenes

def hook(title, T):
    a = lambda p: 0.35 + T * p
    inner = (f'<div class="row" data-rise="{f(0.35)}"><span class="av" style="background:#fbe9e7;color:#b23b2e">?</span><span class="m"><b>{OLD}</b><small>Invoice: please pay into this account</small></span><span class="st red">Looks unsafe?</span></div>'
             f'<div class="row" data-rise="{f(a(0.45))}"><span class="av">EB</span><span class="m"><b>accounts@{BIZ}</b><small>Invoice EX-201 · Example Business</small></span>{st("Checking", "Looks right", a(0.62))}</div>'
             f'<div class="bub ai" data-rise="{f(a(0.8))}" style="margin-bottom:20px"><small>Same invoice</small>Which one would you pay?</div>')
    return split(None, 'Professional email', title, '', card('Inbox', inner, 760, 440), 760, 440)


def address(T, title='Your business name on <span class="ac">every email</span>'):
    a = lambda p: 0.35 + T * p
    inner = f'''<div style="padding:34px 30px 26px">
        <div class="addr"><span data-rise="{f(a(0.25))}">info</span><span data-rise="{f(a(0.35))}">@</span><span class="biz" data-rise="{f(a(0.45))}">examplebusiness</span><span class="dom" data-rise="{f(a(0.6))}">.co.zw</span></div>
        <div class="parts"><span class="part" data-rise="{f(a(0.3))}"><b>info</b> · the inbox</span><span class="part" data-rise="{f(a(0.5))}"><b>examplebusiness</b> · your name</span><span class="part" data-rise="{f(a(0.65))}"><b>.co.zw</b> · your domain</span></div></div>'''
    return split('brand', 'Professional email', title, 'Not a free address. Your own.', card('New address', inner, 780, 330), 780, 330)


def trust(T, kick='Reason 1', title='Clients trust it', sub='Quotes, invoices and payment details feel safe to act on.'):
    a = lambda p: 0.35 + T * p
    inner = f'''<div class="field" data-rise="{f(a(0.05))}"><span>From</span><b>accounts@{BIZ}</b></div>
      <div class="field" data-rise="{f(a(0.12))}"><span>Subject</span><b>Quote EX-114</b></div>
      <div style="padding:16px 26px 0"><div class="dev" style="position:static;box-shadow:none;padding:0"><div class="line"></div><div class="line b"></div></div></div>
      <div class="row" data-rise="{f(a(0.3))}" style="border-bottom:0"><span class="av">EB</span><span class="m"><b>Example Business</b><small>Harare · {BIZ}</small></span><span class="st">📎 Quote-EX-114.pdf</span></div>
      <div class="ok" data-rise="{f(a(0.65))}">{TICK} Client replied: approved</div>'''
    return split('trust', kick, title, sub, card('Example quote', inner, 700, 470), 700, 470)


def brand(T):
    a = lambda p: 0.35 + T * p
    rows = ''.join(f'<div class="row" data-rise="{f(a(0.05 + i * 0.12))}"><span class="m"><b>{who}<span class="pill">@{BIZ}</span></b><small>{what}</small></span><span class="st on">Sent</span></div>'
                   for i, (who, what) in enumerate([('sales', 'Quote for Example Customer'), ('accounts', 'Invoice EX-202'), ('info', 'Thank you for your enquiry')]))
    inner = rows + f'<div class="ok blue" data-rise="{f(a(0.6))}">{TICK} Every email points back to {BIZ}</div>'
    return split('brand', 'Reason 2', 'Every email promotes <span class="ac">your brand</span>', 'Your name, repeated in every inbox you reach.', card('Sent', inner, 720, 440), 720, 440)


def own(T, kick='Reason 3', title='The mailbox <span class="ac">stays with you</span>', sub='When someone leaves, their client history doesn\'t.'):
    a = lambda p: 0.35 + T * p
    inner = (f'<div class="row" data-rise="{f(a(0.05))}"><span class="av">ES</span><span class="m"><b>Example Staff</b><small>Sales · sales@{BIZ}</small></span>{st("Active", "Left the company", a(0.25), "blue")}</div>'
             + ''.join(f'<div class="row" data-rise="{f(a(0.35 + i * 0.12))}"><span class="m"><b>{x}</b></span><span class="st on">Kept</span></div>'
                       for i, x in enumerate(['Client emails and history', 'Quotes and invoices', 'Handed to the next person'])))
    return split('key', kick, title, sub, card(f'sales@{BIZ}', inner, 720, 470), 720, 470)


def aliases(T, kick='Reason 4', title='The right inbox <span class="ac">for every enquiry</span>', sub='Sales, accounts and support, all on one domain.'):
    a = lambda p: 0.35 + T * p
    inner = ''.join(f'<div class="row" data-rise="{f(a(0.05 + i * 0.14))}"><span class="m"><b><span class="pill">{addr}@</span> → {who}</b><small>{what}</small></span>{st("Routing", "Delivered", a(0.25 + i * 0.16))}</div>'
                    for i, (addr, who, what) in enumerate([('sales', 'Sales team', 'New quote request'), ('accounts', 'Accounts', 'Proof of payment'), ('support', 'Support', 'Question about an order')]))
    return split('split', kick, title, sub, card('Example Business mail', inner, 720, 380), 720, 380)


def secure(T, kick='Reason 5', title='Delivered, and <span class="ac">hard to fake</span>', sub='Security records on your domain help your emails land in the inbox.'):
    a = lambda p: 0.35 + T * p
    inner = (''.join(f'<div class="row" data-rise="{f(a(0.05 + i * 0.1))}"><span class="m"><b>{k}</b><small>{d}</small></span>{st("Checking", "Set up", a(0.2 + i * 0.12))}</div>'
                     for i, (k, d) in enumerate([('SPF', 'Lists who may send as your business'), ('DKIM', 'Signs every email you send'), ('DMARC', 'Tells inboxes what to do with fakes')]))
             + f'<div class="fold" data-rise="{f(a(0.6))}"><span class="x on">✓ Inbox</span><span class="x">Spam</span></div>')
    return split('lock', kick, title, sub, card(f'{BIZ} · security', inner, 720, 470), 720, 470)


def devices(T):
    a = lambda p: 0.35 + T * p
    art = ''.join(f'<div class="dev" data-rise="{f(a(0.05 + i * 0.18))}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><h4>{n}</h4><div class="line b"></div><div class="line"></div><div class="line"></div>'
                  f'<div style="font:600 16px var(--f-ui);color:var(--paper-muted);margin-top:14px">info@{BIZ}</div></div>'
                  for i, (n, x, y, w, h) in enumerate([('Phone', 0, 60, 230, 360), ('Outlook', 250, 0, 300, 230), ('Browser', 250, 250, 300, 230)]))
    art += f'<div class="ok blue" data-rise="{f(a(0.65))}" style="position:absolute;left:0;top:440px;width:550px;margin:0">{TICK} Shared calendars for your team</div>'
    return split('devices', 'And more', 'Works <span class="ac">wherever you work</span>', 'Android, iPhone, Outlook and webmail.', art, 560, 510)


def bridge(T, kick='Keep every client', title='Still getting emails <span class="ac">on Gmail?</span>', sub='Forward them, so nothing is missed.'):
    a = lambda p: 0.35 + T * p
    art = (card('Old Gmail', f'<div class="row" style="border-bottom:0"><span class="m"><b>Example Customer</b><small>to {OLD}</small></span><span class="st">New</span></div>', 340, 190, 0, 60, 0.3)
           + f'<div class="arrow" data-grow="{f(a(0.35))}" style="left:355px;top:150px;width:90px"></div>'
           + card('Business inbox', f'<div class="row" style="border-bottom:0"><span class="m"><b>Example Customer</b><small>to info@{BIZ}</small></span>{st("Waiting", "Received", a(0.5))}</div>', 340, 190, 460, 60, a(0.4)))
    return split('forward', kick, title, sub, art, 800, 310)


TABS = ['General', 'Labels', 'Inbox', 'Accounts and Import', 'Filters and Blocked Addresses', 'Forwarding and POP/IMAP']


def settings(body, tab_on):
    tabs = ''.join(f'<span class="tab"{f" data-on={f(tab_on)}" if t.startswith("Forwarding") else ""}>{t}</span>' for t in TABS)
    return card('⚙ Settings · Gmail on a computer', f'<div class="tabs">{tabs}</div>{body}', 780, 470)


def step1(T):
    a = lambda p: 0.35 + T * p
    body = f'''<div class="crumb"><span class="c" data-on="{f(a(0.12))}">⚙ Settings</span><span class="arr">›</span><span class="c" data-on="{f(a(0.32))}">See all settings</span><span class="arr">›</span><span class="c" data-on="{f(a(0.6))}">Forwarding and POP/IMAP</span></div>
      <div class="bub ai" data-rise="{f(a(0.7))}" style="max-width:86%"><small>Tip</small>Forwarding is only set up on a computer, not in the Gmail app.</div>'''
    return split(None, 'Step 1 of 3', 'Open <span class="ac">Forwarding</span> settings', 'In Gmail, on a computer.', settings(body, a(0.6)), 780, 470)


def step2(T):
    a = lambda p: 0.35 + T * p
    body = f'''<span class="btn2" data-on="{f(a(0.08))}">Add a forwarding address</span>
      <div class="inp" data-rise="{f(a(0.2))}">info@{BIZ}</div>
      <div class="row" data-rise="{f(a(0.45))}" style="border-bottom:0"><span class="m"><b>Confirmation link sent</b><small>to info@{BIZ}</small></span>{st("Waiting", "Confirmed", a(0.78))}</div>'''
    return split(None, 'Step 2 of 3', 'Add and confirm <span class="ac">your new address</span>', 'Open the link Gmail sends, and confirm.', settings(body, 0), 780, 470)


def step3(T, kick='Step 3 of 3', title='Forward a copy, <span class="ac">then save</span>', sub="Keep Gmail's copy in the inbox, too."):
    a = lambda p: 0.35 + T * p
    body = f'''<div class="radio" data-rise="0.3"><i></i><span>Disable forwarding</span></div>
      <div class="radio" data-on="{f(a(0.15))}"><i></i><span>Forward a copy of incoming mail to <span class="pill">info@{BIZ}</span> and <span class="pill">keep Gmail's copy in the Inbox</span></span></div>
      <span class="btn2" data-on="{f(a(0.45))}">Save Changes</span>
      <div class="ok" data-rise="{f(a(0.55))}">{TICK} Gmail emails now reach your business inbox</div>'''
    return split(None, kick, title, sub, settings(body, 0.3), 780, 470)


def autoreply(T, kick='Then', title='Add a <span class="ac">"we\'ve moved"</span> reply', sub="Gmail's vacation responder tells people your new address."):
    a = lambda p: 0.35 + T * p
    inner = f'''<div class="row" data-rise="{f(a(0.05))}"><span class="m"><b>Vacation responder</b><small>Settings · General</small></span>{st("Off", "On", a(0.2))}</div>
      <div class="field" data-rise="{f(a(0.3))}"><span>Subject</span><b>We've moved</b></div>
      <div class="inp" data-rise="{f(a(0.45))}" style="line-height:1.45">Thanks for your email. We have a new address: <b>info@{BIZ}</b>. Please update your contacts.</div>'''
    return split('reply', kick, title, sub, card('Gmail · auto-reply', inner, 720, 400), 720, 400)


def everywhere(T):
    a = lambda p: 0.35 + T * p
    items = ['Website', 'Google Business Profile', 'WhatsApp Business', 'Facebook page', 'Invoices and quotes', 'Email signature']
    inner = ''.join(f'<div class="row" data-rise="{f(a(0.02 + i * 0.1))}"><span class="m"><b>{x}</b></span>{st("Old Gmail", "Updated", a(0.12 + i * 0.12))}</div>' for i, x in enumerate(items))
    return split('list', 'Finally', 'Update it <span class="ac">everywhere</span>', 'Everywhere clients find your contact details.', card('Checklist', inner, 680, 540), 680, 540)


def service(T, kick='Or let us do it', title='iContact sets it <span class="ac">all up</span>'):
    a = lambda p: 0.35 + T * p
    items = [('Register your .co.zw domain', 'In your business name'), ('Set up your mailboxes', 'Phone, Outlook and webmail'), ('Add the security records', 'SPF, DKIM and DMARC'),
             ('Move your old emails', 'On Mail Business and Mail Pro'), ('Set up Gmail forwarding', 'With you, step by step')]
    inner = ''.join(f'<div class="row" data-rise="{f(a(0.02 + i * 0.12))}"><span class="m"><b>{x}</b><small>{d}</small></span>{st("To do", "Done", a(0.14 + i * 0.14))}</div>' for i, (x, d) in enumerate(items))
    return split('tools', kick, title, 'One team, one invoice.', card('Your switch', inner, 700, 560), 700, 560)


PLANS = [('Mail Basic', '$10', 'per mailbox a month', '10 GB · webmail, phone and Outlook · unlimited aliases'),
         ('Mail Business', '$18', 'per mailbox a month', '30 GB · shared calendars · Gmail migration · daily backups'),
         ('Mail Pro', '$25', 'per mailbox a month', '50 GB · email archiving · two-factor login')]


def plans(times, h_text):
    return pricing(PLANS, times, h_text)


def end():
    return endcard('Every email should look like it comes from a <span>real business.</span>', 'EMAIL')
