"""Pages for the AI Voice Agent explainer (V1 60 s, V2 120 s). Every page lays itself out for 16:9, 9:16 and 4:5
(lib/orient.js sets html.L / html.P / html.S). Everything on screen is invented and labelled Example, per the brief.

Each template returns a page's HTML. `T` is about how long the shot's voice lasts, so the events inside a shot
can be spread to match it. Times are page seconds; the voice starts at 0.2 s.
"""

TICK = '<svg viewBox="0 0 24 24"><path d="M5 12.5l4.2 4.2L19 7"/></svg>'
ICONS = {
    'telecom': '<path d="M32 22v34M24 56h16M27 34l5-12 5 12M25 42h14"/><path d="M20 16a16 16 0 0 0 0 22M44 16a16 16 0 0 1 0 22M13 10a25 25 0 0 0 0 34M51 10a25 25 0 0 1 0 34"/>',
    'finance': '<path d="M10 26L32 12l22 14H10zM16 30v18M26 30v18M38 30v18M48 30v18M10 52h44"/>',
    'health': '<path d="M32 52s-18-10.5-18-24a10 10 0 0 1 18-6 10 10 0 0 1 18 6c0 13.5-18 24-18 24z"/><path d="M32 27v12M26 33h12"/>',
    'tech': '<rect x="14" y="14" width="36" height="26" rx="3"/><path d="M8 48h48l-4-8H12z"/><path d="M28 22l-5 5 5 5M36 22l5 5-5 5"/>',
    'retail': '<path d="M16 22h32l-3 32H19z"/><path d="M24 26v-6a8 8 0 0 1 16 0v6"/>',
    'travel': '<rect x="12" y="22" width="40" height="28" rx="4"/><path d="M24 22v-6h16v6M24 22v28M40 22v28"/>',
    'support': '<path d="M14 36v-4a18 18 0 0 1 36 0v4"/><rect x="10" y="34" width="10" height="14" rx="3"/><rect x="44" y="34" width="10" height="14" rx="3"/><path d="M50 48c0 6-6 8-14 8"/>',
}
PHONE = '<svg viewBox="0 0 24 24" style="width:64px;height:64px;fill:#fff"><path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>'
PERSON = '<svg viewBox="0 0 64 64"><circle cx="32" cy="22" r="10"/><path d="M14 54c2-11 9-16 18-16s16 5 18 16"/></svg>'
WA = ('<svg viewBox="0 0 32 32" fill="none" aria-hidden="true"><path d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3z" fill="#fff"/>'
      '<path d="M11.6 9.6c-.3-.7-.6-.7-.9-.7h-.8c-.3 0-.7.1-1 .5-.4.4-1.3 1.3-1.3 3.1s1.3 3.6 1.5 3.9c.2.2 2.6 4.1 6.4 5.6 3.1 1.2 3.8 1 4.5.9.7-.1 2.2-.9 2.5-1.8.3-.9.3-1.6.2-1.8-.1-.2-.3-.3-.7-.5l-2.5-1.2c-.3-.1-.6-.2-.8.2-.2.4-.9 1.2-1.1 1.4-.2.2-.4.3-.8.1-.4-.2-1.6-.6-3-1.9-1.1-1-1.9-2.2-2.1-2.6-.2-.4 0-.6.2-.8l.6-.7c.2-.2.3-.4.4-.7.1-.3 0-.5 0-.7l-1.3-2.9z" fill="#25a244"/></svg>')


def page(body, css='', wide=False, extra='', noh=False):
    return f'''<!doctype html>
<html>
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="lib/aiv.css">
<script src="lib/orient.js"></script>
<style>{css}</style>
</head>
<body>
<div class="stage{' wide' if wide else ''}{' noh' if noh else ''}">
  <div class="bg-navy"></div>
  <div class="cam" data-from="1" data-to="1.035">
{body}
  </div>
</div>
<script type="module">
import {{ shot }} from './lib/aiv.js';
shot(5{extra});
</script>
</body>
</html>
'''


def f(x): return f'{x:.2f}'


def st(a, b, at, cls=''):
    return f'<span class="st {cls}" data-on="{f(at)}"><span class="a">{a}</span><span class="b">{b}</span></span>'


def card(title, inner, w, h, x=0, y=0, rise=0.25):
    return (f'<div class="card" data-rise="{f(rise)}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
            f'<div class="ch"><span class="dots"><i></i><i></i><i></i></span><span class="grow">{title}</span><span class="ex">Example</span></div>{inner}</div>')


# ---------------------------------------------------------------- scenes

def hook(title, T):
    rows = ''
    for i in range(5):
        rows += (f'<div class="row" data-rise="{f(0.3 + i * T * 0.13)}"><span class="av">E{i + 1}</span><span class="m"><b>Example customer {i + 1}</b>'
                 f'<small>Website enquiry · {i + 1} h ago</small></span><span class="st red">Not called</span></div>')
    body = f'''    <div class="txt"><div class="h" data-rise="0.15">{title}</div></div>
    <div class="vis"><div class="art" data-w="800" data-h="620">
      {card('Enquiries', rows, 600, 600, 200, 10)}
      <div data-pop="0.2" style="position:absolute;left:0;top:330px;width:210px;height:210px">
        <div class="orb" style="width:210px;height:210px"><span class="ringwave"></span><span class="ringwave" data-off="0.7"></span>{PHONE}</div>
      </div>
    </div></div>'''
    return page(body)


def intro(title, sub, steps_at, T):
    chips = ''.join(f'<span class="step" data-on="{f(a)}">{s}</span>' for s, a in zip(('Call', 'Qualify', 'Remind', 'Book'), steps_at))
    inner = f'''<div style="display:flex;gap:30px;align-items:center;padding:34px 30px 10px">
        <div class="orb"><div class="wave">{'<i></i>' * 7}</div></div>
        <div><div style="font:600 17px var(--f-ui);letter-spacing:.14em;text-transform:uppercase;color:var(--paper-muted)">On a call</div>
          <div style="font:700 34px var(--f);margin:6px 0">Example Customer</div>
          <div style="font:500 20px var(--f-ui);color:var(--paper-muted)">New enquiry · follow-up call</div></div></div>
      <div class="steps" style="padding:24px 30px">{chips}</div>
      <div class="ok blue" data-rise="{f(steps_at[-1] + 0.3)}">{TICK} Appointment booked · Thu 10:00</div>'''
    body = f'''    <div class="txt"><div class="plate" data-pop="0.1"><img src="img/icontact-logo.png" alt="iContact Africa Solutions"></div>
      <div class="h" data-rise="0.55">{title}</div>{f'<div class="s" data-rise="0.8">{sub}</div>' if sub else ''}</div>
    <div class="vis"><div class="art" data-w="720" data-h="520">{card('AI voice agent', inner, 720, 520, 0, 0, 0.45)}</div></div>'''
    return page(body)


def industry_card(kind, T):
    a = lambda p: 0.35 + T * p   # an event at a share of the line
    if kind == 'telecom':
        inner = ''.join(f'<div class="row" data-rise="{f(a(0.05 + i * 0.1))}"><span class="av">{n}</span><span class="m"><b>{who}</b><small>{what}</small></span>{st("Queued", done, a(0.35 + i * 0.17), cls)}</div>'
                        for i, (n, who, what, done, cls) in enumerate([
                            ('A', 'Example Customer A', 'Contract ends 30 Nov', 'Renewal booked', ''),
                            ('B', 'Example Customer B', 'Upgrade enquiry', 'Callback set', 'blue'),
                            ('C', 'Example Customer C', 'New sales lead', 'Qualified', '')]))
        return card('Renewals and leads', inner, 680, 400)
    if kind == 'finance':
        inner = (f'<div class="big" data-rise="{f(a(0.05))}"><div class="l">Meeting</div><div class="v">Thursday · 14:00</div>'
                 f'<div style="font:500 20px var(--f-ui);color:var(--paper-muted);margin-top:6px">Example Advisory · with an adviser</div></div>'
                 f'<div class="row" data-rise="{f(a(0.25))}"><span class="m"><b>Appointment</b><small>Confirmation call</small></span>{st("Calling", "Confirmed", a(0.4))}</div>'
                 f'<div class="row" data-rise="{f(a(0.45))}"><span class="m"><b>New enquiry</b><small>Example Customer</small></span>{st("Checking", "Qualified", a(0.7), "blue")}</div>')
        return card('Appointments', inner, 680, 430)
    if kind == 'health':
        inner = (f'<div class="big" data-rise="{f(a(0.05))}"><div class="l">Reminder</div><div class="v">Tuesday · 09:30</div>'
                 f'<div style="font:500 20px var(--f-ui);color:var(--paper-muted);margin-top:6px">Example Clinic · Example Patient</div></div>'
                 f'<div class="row" data-rise="{f(a(0.25))}"><span class="m"><b>Reminder call</b><small>Day before the visit</small></span>{st("Scheduled", "Called", a(0.4))}</div>'
                 f'<div class="ok" data-rise="{f(a(0.65))}">{TICK} Visit confirmed</div>')
        return card('Appointment reminders', inner, 680, 440)
    if kind == 'tech':
        inner = (''.join(f'<div class="field" data-rise="{f(a(0.05 + i * 0.1))}"><span>{k}</span><b>{v}</b></div>' for i, (k, v) in enumerate([
                    ('Company', 'Example Tech Ltd'), ('Team size', '25 people'), ('Looking for', 'A product demo')]))
                 + f'<div class="ok blue" data-rise="{f(a(0.55))}" style="margin-top:22px">{TICK} Qualified · Demo booked Wed 11:00</div>')
        return card('Demo request', inner, 680, 410)
    if kind == 'retail':
        inner = ''.join(f'<div class="row" data-rise="{f(a(0.05 + i * 0.12))}"><span class="av">{n}</span><span class="m"><b>{who}</b><small>{what}</small></span>{st("Queued", done, a(0.35 + i * 0.2), cls)}</div>'
                        for i, (n, who, what, done, cls) in enumerate([
                            ('EX', 'Order EX-1042', 'Delivered yesterday', 'Followed up', ''),
                            ('EX', 'Order EX-1043', 'Out for delivery', 'Update shared', 'blue'),
                            ('R', 'Example returning customer', 'Last order in June', 'Called', '')]))
        return card('Orders and customers', inner, 680, 400)
    if kind == 'travel':
        inner = (f'<div class="big" data-rise="{f(a(0.05))}"><div class="l">Booking</div><div class="v">Example Lodge · 2 nights</div>'
                 f'<div style="font:500 20px var(--f-ui);color:var(--paper-muted);margin-top:6px">12–14 December · Example Guest</div></div>'
                 f'<div class="row" data-rise="{f(a(0.25))}"><span class="m"><b>Booking</b><small>Confirmation call</small></span>{st("Calling", "Confirmed", a(0.4))}</div>'
                 f'<div class="row" data-rise="{f(a(0.45))}"><span class="m"><b>Question: check-in time</b><small>Routine question</small></span>{st("Open", "Answered", a(0.65), "blue")}</div>')
        return card('Bookings', inner, 680, 430)
    if kind == 'support':
        inner = (''.join(f'<div class="row" data-rise="{f(a(0.05 + i * 0.12))}"><span class="m"><b>{tm} · {what}</b><small>{note}</small></span>{st("Live", done, a(0.3 + i * 0.18), cls)}</div>'
                         for i, (tm, what, note, done, cls) in enumerate([
                             ('09:12', 'Opening hours', 'Routine question', 'Answered', ''),
                             ('09:20', 'Order status', 'Routine question', 'Answered', ''),
                             ('09:31', 'Billing query', 'Needs a person', 'Passed to team', 'blue')]))
                 + f'<div class="bub ai" data-rise="{f(a(0.75))}" style="margin-bottom:18px"><small>Call record</small>Every call logged with a summary for your team.</div>')
        return card('Call log', inner, 680, 470)
    raise ValueError(kind)


def industry(kind, label, task, T):
    body = f'''    <div class="txt"><div class="icon" data-pop="0.1"><svg viewBox="0 0 64 64">{ICONS[kind]}</svg></div>
      <div class="h ind" data-rise="0.2">{label}</div><div class="s" data-rise="0.4">{task}</div></div>
    <div class="vis"><div class="art" data-w="680" data-h="480">{industry_card(kind, T)}</div></div>'''
    return page(body)


def flow(T):
    steps = ''.join(f'<span class="num" data-on="{f(a)}"><b>{i + 1}.</b>{s}</span>' for i, (s, a) in enumerate(
        [('Script', 0.3), ('Call', T * 0.33), ('Book or transfer', T * 0.55), ('Report', T * 0.85)]))
    A = lambda p: f(0.3 + T * p)
    land = f'''<div class="art only-L" data-w="1500" data-h="520">
        <div class="node" data-pop="{A(0.0)}" style="left:0;top:180px;width:270px;height:160px">Your list<small>Leads, bookings, reminders</small></div>
        <div class="arrow" data-grow="{A(0.18)}" style="left:290px;top:258px;width:170px"></div>
        <div class="node ac" data-pop="{A(0.25)}" style="left:480px;top:170px;width:300px;height:180px">AI call<small>Says it's an AI · follows your rules</small></div>
        <div class="arrow" data-grow="{A(0.5)}" data-rot="-24" style="left:800px;top:240px;width:250px"></div>
        <div class="arrow" data-grow="{A(0.58)}" style="left:800px;top:258px;width:220px"></div>
        <div class="arrow" data-grow="{A(0.66)}" data-rot="24" style="left:800px;top:276px;width:250px"></div>
        <div class="node" data-pop="{A(0.52)}" style="left:1060px;top:0;width:440px;height:130px">Booked<small>A time in your calendar</small></div>
        <div class="node" data-pop="{A(0.6)}" style="left:1060px;top:195px;width:440px;height:130px">Transferred<small>Passed to your team</small></div>
        <div class="node" data-pop="{A(0.7)}" style="left:1060px;top:390px;width:440px;height:130px">Follow-up recorded<small>Logged for your report</small></div>
      </div>'''
    vert = f'''<div class="art only-V" data-w="900" data-h="700">
        <div class="node" data-pop="{A(0.0)}" style="left:250px;top:0;width:400px;height:130px">Your list<small>Leads, bookings, reminders</small></div>
        <div class="arrow" data-grow="{A(0.18)}" data-rot="90" style="left:450px;top:140px;width:70px"></div>
        <div class="node ac" data-pop="{A(0.25)}" style="left:200px;top:230px;width:500px;height:150px">AI call<small>Says it's an AI · follows your rules</small></div>
        <div class="arrow" data-grow="{A(0.5)}" data-rot="125" style="left:400px;top:395px;width:150px"></div>
        <div class="arrow" data-grow="{A(0.58)}" data-rot="90" style="left:450px;top:395px;width:90px"></div>
        <div class="arrow" data-grow="{A(0.66)}" data-rot="55" style="left:500px;top:395px;width:150px"></div>
        <div class="node" data-pop="{A(0.52)}" style="left:0;top:530px;width:280px;height:170px">Booked<small>In your calendar</small></div>
        <div class="node" data-pop="{A(0.6)}" style="left:310px;top:530px;width:280px;height:170px">Transferred<small>To your team</small></div>
        <div class="node" data-pop="{A(0.7)}" style="left:620px;top:530px;width:280px;height:170px">Follow-up<small>Recorded</small></div>
      </div>'''
    body = f'''    <div class="txt"><div class="kick" data-rise="0.1">How it works</div><div class="nums">{steps}</div></div>
    <div class="vis">{land}{vert}</div>'''
    return page(body, wide=True)


def demo(times, T):
    a1, c, a2, end = times
    inner = f'''<div style="display:flex;gap:20px;align-items:center;padding:22px 26px 8px">
        <div class="orb" style="width:84px;height:84px"><div class="wave" style="height:34px;gap:4px" data-from="{f(a1)}" data-to="{f(end)}">{'<i style="width:5px"></i>' * 5}</div></div>
        <div><div style="font:700 26px var(--f)">Example Customer</div><div style="font:500 18px var(--f-ui);color:var(--paper-muted)">On a call · <span id="clock">00:00</span></div></div></div>
      <div class="bub ai" data-rise="{f(a1)}"><small>AI assistant</small>Hi, this is the AI assistant for Example Motors. I'm calling to confirm your car service tomorrow at ten. Does that still suit you?</div>
      <div class="bub you" data-rise="{f(c)}"><small>Customer</small>Yes, that works for me.</div>
      <div class="bub ai" data-rise="{f(a2)}"><small>AI assistant</small>Great, you're confirmed. Thank you!</div>
      <div class="ok" data-rise="{f(end)}">{TICK} Service confirmed · call logged</div>'''
    body = f'''    <div class="txt"><div class="kick" data-rise="0.1">Example call</div>
      <div class="h" data-rise="0.2">The agent says it's an AI, <span class="ac">then gets it done.</span></div>
      <div class="s" data-rise="0.4">An invented call, in the agent's voice.</div></div>
    <div class="vis"><div class="art" data-w="700" data-h="660">{card('Example Motors · AI assistant', inner, 700, 660, 0, 0, 0.1)}</div></div>'''
    clock = (", (t) => { const s = Math.max(0, Math.floor(t - %s)); document.getElementById('clock').textContent = '00:' + String(s).padStart(2, '0'); }" % f(a1))
    return page(body, extra=clock)


def li(text, at): return f'<div class="li" data-rise="{f(at)}">{TICK}<span>{text}</span></div>'


def compare(ai_head, ai_items, ppl_head, ppl_items, kick, T):
    queue = ''.join(f'<div class="qrow" data-rise="{f(0.3 + i * 0.35)}">Example call {i + 1}<span class="tk" data-rise="{f(0.6 + i * 0.35)}">✓</span></div>' for i in range(4))
    ai_li = ''.join(li(x, 0.5 + i * 0.35) for i, x in enumerate(ai_items))
    pp_li = ''.join(li(x, T * 0.55 + i * 0.4) for i, x in enumerate(ppl_items))
    def panes(w, h, vertical):
        if vertical:
            return (f'<div class="pane" data-rise="0.2" style="left:0;top:0;width:{w}px;height:{h // 2 - 15}px;display:flex;gap:30px">'
                    f'<div style="flex:1"><h3>{ai_head}</h3>{ai_li}</div><div style="width:300px">{queue}</div></div>'
                    f'<div class="pane" data-rise="{f(T * 0.5)}" style="left:0;top:{h // 2 + 15}px;width:{w}px;height:{h // 2 - 15}px;display:flex;gap:30px;align-items:flex-start">'
                    f'<div class="person" data-pop="{f(T * 0.52)}">{PERSON}</div><div style="flex:1"><h3>{ppl_head}</h3>{pp_li}</div></div>')
        return (f'<div class="pane" data-rise="0.2" style="left:0;top:0;width:{w // 2 - 20}px;height:{h}px"><h3>{ai_head}</h3>{ai_li}<div style="margin-top:20px">{queue}</div></div>'
                f'<div class="pane" data-rise="{f(T * 0.5)}" style="left:{w // 2 + 20}px;top:0;width:{w // 2 - 20}px;height:{h}px">'
                f'<div class="person" data-pop="{f(T * 0.52)}" style="margin-bottom:20px">{PERSON}</div><h3>{ppl_head}</h3>{pp_li}</div>')
    body = f'''    <div class="txt"><div class="kick" data-rise="0.1">{kick}</div></div>
    <div class="vis"><div class="art only-L" data-w="1500" data-h="600">{panes(1500, 600, False)}</div>
      <div class="art only-V" data-w="900" data-h="760">{panes(900, 760, True)}</div></div>'''
    return page(body, wide=True, noh=True)


def columns(cols, kick, T, h_text=None):
    """cols: [(heading, [items], accent?)]: two or three panes, side by side (L) or stacked (P, S)"""
    n = len(cols)
    def art(W, H, vertical):
        out = ''
        for i, (head, items, sub) in enumerate(cols):
            at = 0.3 + i * T * (0.9 / n)
            lis = ''.join(li(x, at + 0.3 + j * 0.3) for j, x in enumerate(items))
            if vertical:
                hh = (H - 20 * (n - 1)) // n
                out += f'<div class="pane" data-rise="{f(at)}" style="left:0;top:{i * (hh + 20)}px;width:{W}px;height:{hh}px;padding:26px 32px"><h3 style="font-size:36px;margin-bottom:6px">{head}</h3><div class="note">{sub}</div><div style="display:flex;gap:28px;flex-wrap:wrap">{lis}</div></div>'
            else:
                ww = (W - 30 * (n - 1)) // n
                out += f'<div class="pane" data-rise="{f(at)}" style="left:{i * (ww + 30)}px;top:0;width:{ww}px;height:{H}px"><h3>{head}</h3><div class="note">{sub}</div><div style="margin-top:16px">{lis}</div></div>'
        return out
    body = f'''    <div class="txt"><div class="kick" data-rise="0.1">{kick}</div>{f'<div class="h" data-rise="0.2">{h_text}</div>' if h_text else ''}</div>
    <div class="vis"><div class="art only-L" data-w="1500" data-h="560">{art(1500, 560, False)}</div>
      <div class="art only-V" data-w="900" data-h="720">{art(900, 720, True)}</div></div>'''
    return page(body, wide=True, noh=not h_text)


def pricing(cards, times, h_text):
    """cards: [(label, value, small, detail)], each popping in at its time and staying up"""
    n = len(cards)
    def one(i, x, y, w, h):
        l, v, sm, d = cards[i]
        return (f'<div class="price" data-pop="{f(times[i])}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><span class="bar"></span>'
                f'<div class="l">{l}</div><div class="v">{v}{f" <small>{sm}</small>" if sm else ""}</div>{f"<div class=d>{d}</div>" if d else ""}</div>')
    gap = 30
    lw = (1500 - gap * (n - 1)) // n
    land = ''.join(one(i, i * (lw + gap), 40, lw, 420) for i in range(n))
    if n == 4:
        vw, vh = 900, 720; cw, chh = (vw - gap) // 2, (vh - gap) // 2
        vert = ''.join(one(i, (i % 2) * (cw + gap), (i // 2) * (chh + gap), cw, chh) for i in range(n))
    else:
        vw, vh = 900, 720; chh = (vh - gap * (n - 1)) // n
        vert = ''.join(one(i, 0, i * (chh + gap), vw, chh) for i in range(n))
    body = f'''    <div class="txt"><div class="kick" data-rise="0.1">Pricing</div>{f'<div class="h" data-rise="0.2">{h_text}</div>' if h_text else ''}</div>
    <div class="vis"><div class="art only-L" data-w="1500" data-h="500">{land}</div>
      <div class="art only-V" data-w="{vw}" data-h="{vh}">{vert}</div></div>'''
    css = 'html.S .price .v { font-size: 54px; } html.P .price .v { font-size: 58px; }' + (' html.L .price .v { font-size: 50px; } html.L .price { padding: 30px 26px; }' if n == 4 else '')
    return page(body, wide=True, noh=not h_text, css=css)


def endcard():
    css = '''.ecw { position: absolute; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; gap: 40px; }
  html.L .ecw { left: 160px; right: 160px; top: 70px; height: 810px; gap: 34px; }
  html.P .ecw { left: 80px; right: 80px; top: 290px; height: 1010px; }
  html.S .ecw { left: 70px; right: 70px; top: 40px; height: 860px; gap: 30px; }
  .ecw .plate img { width: 460px; } html.S .ecw .plate img { width: 400px; }
  .ecw .tag { font: 700 64px/1.1 var(--f); text-wrap: balance; max-width: 1300px; } .ecw .tag span { color: var(--accent); }
  html.P .ecw .tag { font-size: 68px; } html.S .ecw .tag { font-size: 54px; }
  .ecw .wa { display: inline-flex; align-items: center; gap: 18px; padding: 22px 32px; border-radius: 22px; background: #25a244; font: 700 40px/1.15 var(--f); color: #fff; box-shadow: 0 18px 40px rgba(0,0,0,0.35); text-align: left; }
  html.S .ecw .wa { font-size: 36px; }
  .ecw .wa svg { width: 54px; height: 54px; flex: none; } .ecw .wa b { font-weight: 800; letter-spacing: .04em; }
  .ecw .foot { font: 500 28px/1.2 var(--f-ui); color: var(--muted); }
  .glow { position: absolute; left: 50%; top: 46%; width: 1400px; height: 1400px; margin: -700px 0 0 -700px; border-radius: 50%; background: radial-gradient(circle, rgba(171,207,71,0.10), transparent 60%); }'''
    body = f'''    <div class="glow" id="glow"></div>
    <div class="ecw">
      <div class="plate" data-rise="0.1"><img src="img/icontact-logo.png" alt="iContact Africa Solutions"></div>
      <div class="tag" data-rise="0.35">AI handles the repetitive calls. <span>Your people handle the moments that matter.</span></div>
      <div class="wa" data-pop="0.8">{WA}<span>WhatsApp <b>AGENT</b><br>to +263 71 857 4277</span></div>
      <div class="foot" data-rise="1.2">iContact Africa Solutions | Harare, Zimbabwe</div>
    </div>'''
    return page(body, css=css, extra=", (t) => { document.getElementById('glow').style.transform = `scale(${1 + 0.06 * (0.5 - 0.5 * Math.cos(2 * Math.PI * t / 4))})`; }")
