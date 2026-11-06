"""Build the AI Voice Agent explainer: V1 (60 s) and V2 (120 s), each as three OpenFilm projects drawn from the same
pages: 16:9 1920×1080 (master), 9:16 1080×1920 and 4:5 1080×1350. Each shot is cut to fit its voice line.

usage: python3 tools/build_aiv.py v1|v2 --vo <dir>
  <dir>/N.mp3 is the voice for shot N. For V2, shot 4 (the Example call) is made from demo-a1.mp3, demo-c.mp3 and
  demo-a2.mp3 (agent, customer, agent): trimmed, given a phone-line sound and joined with short pauses.
Output: aivoice/<version>-16x9, -9x16, -4x5 (each a project with film.html and an .srt).
The voice is sped up once to `speed` with Rubber Band (see timed()); film.html plays it at normal speed.
"""
import importlib.util, json, os, re, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import psound
import aiv_pages as P
_spec = importlib.util.spec_from_file_location('nyasha_build', os.path.join(HERE, '..', '..', '.claude', 'skills', 'nyasha-video-ads', 'tools', 'build.py'))
_nb = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_nb)
speech, caption = _nb.speech, _nb.caption

PACK = os.path.abspath(os.path.join(HERE, '..'))
KIT = os.path.join(PACK, 'kit')
OUT = os.path.join(PACK, 'aivoice')
SIZES = {'16x9': (1920, 1080), '9x16': (1080, 1920), '4x5': (1080, 1350)}
LEAD = 0.06


def V1():
    I = lambda kind, label, task, line: dict(page=f'ind-{kind}', line=line, html=lambda T, k=kind, l=label, s=task: P.industry(k, l, s, T),
                                            sfx=[('whoosh', -0.2, 0.22)])
    return dict(speed=1.15, tail=0.12, end_tail=1.7, music=0.18, shots=[
        dict(page='hook', line='What if every enquiry got a call, without stretching your team?',
             html=lambda T: P.hook('Every enquiry needs a <span class="ac">follow-up</span>', T), sfx=[('ring', 0.25, 0.35), ('ring', 1.65, 0.25)]),
        dict(page='intro', line='iContact Africa Solutions sets up AI voice agents that call, qualify, remind and book appointments.',
             html=lambda T: P.intro('AI voice agents', '<span style="color:var(--text)">Call · qualify · remind · book</span>', [0.12 + T * x for x in (0.55, 0.66, 0.77, 0.88)], T),
             sfx=[('whoosh', -0.2, 0.25), ('ding', 'booked', 0.35)]),
        I('telecom', 'Telecommunications', 'Leads and renewals', 'Telecoms: follow up sales leads and renewals.'),
        I('finance', 'Financial services', 'Confirmations and enquiries', 'Financial services: confirm appointments and qualify enquiries.'),
        I('health', 'Healthcare', 'Appointment reminders', 'Healthcare: reduce missed visits with reminders.'),
        I('tech', 'Technology', 'Demo requests', 'Technology: qualify demo requests faster.'),
        I('retail', 'Retail &amp; e-commerce', 'Customer follow-ups', 'Retail: follow up orders and returning customers.'),
        I('travel', 'Travel &amp; hospitality', 'Booking confirmations', 'Hospitality: confirm bookings and answer routine questions.'),
        I('support', 'Customer support', 'Routine questions, full records', 'Support: handle routine questions and log every call.'),
        dict(page='split', line='AI handles repetitive calls at scale. People bring judgment and empathy.',
             html=lambda T: P.compare('<span class="ac">AI</span>: repetitive calls', ['At scale', 'Every call logged'],
                                      '<span class="ac">People</span>: judgment and empathy', ['Judgment', 'Empathy'], 'AI and your team', T),
             sfx=[('whoosh', -0.2, 0.25)]),
        dict(page='when', line='Use AI alone for simple tasks. Use both for sales and complex support.',
             html=lambda T: P.columns([('<span class="ac">AI</span> alone', ['Simple tasks', 'Ends with a booking'], 'Simple tasks'),
                                       ('<span class="ac">AI</span> + people', ['Sales and complex support', 'Passed to a person'], 'Both')], 'When to use what', T),
             sfx=[('whoosh', -0.2, 0.25)]),
        dict(page='pricing', min=6.6, line='Setup from $150, monthly management from $150, plus $40 per attended sales appointment.',
             html=lambda T: P.pricing([('Setup', 'from $150', '', ''), ('Management', 'from $150', 'a month', ''),
                                       ('Sales campaigns', '$40', 'per attended appointment', '')], [0.3, 0.12 + T * 0.36, 0.12 + T * 0.66], ''),
             sfx=[('whoosh', -0.2, 0.25), ('pop', 'card0', 0.3), ('pop', 'card1', 0.3), ('pop', 'card2', 0.3)]),
        dict(page='endcard', line='WhatsApp the word AGENT to iContact to plan your pilot.', html=lambda T: P.endcard(),
             sfx=[('whoosh', -0.2, 0.25), ('shimmer', 0.8, 0.25)]),
    ])


def V2():
    I = lambda kind, label, task, line: dict(page=f'ind-{kind}', line=line, html=lambda T, k=kind, l=label, s=task: P.industry(k, l, s, T),
                                            sfx=[('whoosh', -0.2, 0.22)])
    return dict(speed=1.1, tail=0.2, end_tail=2.0, music=0.17, shots=[
        dict(page='hook', line="Enquiries come in. Reminders need sending. Your team is already busy. So some calls just don't happen.",
             html=lambda T: P.hook('Leads go cold when follow-up is <span class="ac">slow</span>', T), sfx=[('ring', 0.25, 0.35), ('ring', 1.65, 0.25), ('ring', 3.05, 0.2)]),
        dict(page='intro', line='iContact Africa Solutions sets up and manages AI voice agents for your business. They make routine calls, qualify leads, send reminders and book appointments.',
             html=lambda T: P.intro('iContact AI voice agents', 'Set up and managed for your business', [0.12 + T * x for x in (0.58, 0.69, 0.8, 0.9)], T),
             sfx=[('whoosh', -0.2, 0.25), ('ding', 'booked', 0.35)]),
        dict(page='flow', line="We build the script around your business. The agent says it's an AI, follows your rules, then books a time, passes the call to your team or records the follow-up.",
             html=lambda T: P.flow(T), sfx=[('whoosh', -0.2, 0.25)]),
        dict(page='demo', demo=True, line="Hi, this is the AI assistant for Example Motors. I'm calling to confirm your car service tomorrow at ten. Does that still suit you? Yes, that works for me. Great, you're confirmed. Thank you!",
             html=None, sfx=[('whoosh', -0.2, 0.25), ('ring', 'ring', 0.3), ('ding', 'done', 0.3)]),
        I('telecom', 'Telecommunications', 'Renewals, upgrades and enquiries', 'For telecoms, follow up sales leads, renewals and upgrades without tying up your whole team.'),
        I('finance', 'Financial services', 'Qualify enquiries, confirm meetings', 'In financial services, qualify enquiries and confirm meetings, while advice and sensitive questions stay with staff.'),
        I('health', 'Healthcare', 'Reminders and confirmations', 'In healthcare, confirm visits and send reminders, while clinical questions stay with your medical team.'),
        I('tech', 'Technology', 'Demo qualification', 'Technology companies can qualify demo requests quickly, so sales teams focus on serious buyers.'),
        I('retail', 'Retail &amp; e-commerce', 'Orders and returning customers', 'Retail and e-commerce teams can follow up orders, reach returning customers and share routine updates.'),
        I('travel', 'Travel &amp; hospitality', 'Bookings and guest questions', 'Travel and hospitality businesses can confirm bookings, answer routine questions and follow up on enquiries.'),
        I('support', 'Customer support', 'First response and call records', 'For customer support, handle common questions first, then give your team a clear call record.'),
        dict(page='compare', line='So how does this compare with a human employee? AI is built for repetition, consistency and records. People are better at judgment, empathy and negotiation.',
             html=lambda T: P.compare('<span class="ac">AI</span>: consistent, scalable, records calls', ['Consistent', 'Scalable', 'Records every call'],
                                      '<span class="ac">People</span>: judgment, empathy, negotiation', ['Judgment', 'Empathy', 'Negotiation'], 'AI and a human employee', T),
             sfx=[('whoosh', -0.2, 0.25)]),
        dict(page='when', line='Use AI alone for simple reminders and confirmations. Combine AI and people for sales and support. Keep sensitive or high-value conversations with your team.',
             html=lambda T: P.columns([('<span class="ac">AI</span> only', ['Reminders', 'Confirmations'], 'Simple and routine'),
                                       ('<span class="ac">AI</span> + people', ['Sales', 'Support'], 'Work together'),
                                       ('People first', ['Sensitive issues', 'High-value conversations'], 'Stay with your team')], 'When to use what', T),
             sfx=[('whoosh', -0.2, 0.25)]),
        dict(page='pricing', min=11.6, line='Pricing is simple. Setup starts at $150, and management starts at $150 a month. Sales campaigns add $40 per attended appointment. Support plans are quoted by volume.',
             html=lambda T: P.pricing([('Setup', 'from $150', '', ''), ('Management', 'from $150', 'a month', ''),
                                       ('Sales campaigns', '$40', 'per attended appointment', ''),
                                       ('Support and reminders', 'Monthly plan', '', 'Quoted by volume')],
                                      [0.12 + T * x for x in (0.12, 0.33, 0.56, 0.82)], 'Pricing is <span class="ac">simple</span>'),
             sfx=[('whoosh', -0.2, 0.25), ('pop', 'card0', 0.3), ('pop', 'card1', 0.3), ('pop', 'card2', 0.3), ('pop', 'card3', 0.3)]),
        dict(page='endcard', line="Start with a small pilot. WhatsApp the word AGENT to iContact Africa Solutions, and let's plan yours.", html=lambda T: P.endcard(),
             sfx=[('whoosh', -0.2, 0.25), ('shimmer', 0.8, 0.25)]),
    ])


def make_demo(src, out):
    """agent, customer, agent → one file with a phone-line sound; returns when each turn starts and the last ends (file seconds)"""
    parts, t, times = [], 0.0, []
    for name, gap in (('demo-a1', 0.5), ('demo-c', 0.4), ('demo-a2', 0)):
        p = os.path.join(src, f'{name}.mp3'); sp, _ = speech(p)
        a, b = sp[0][0], sp[-1][1]; parts.append((p, a, b)); times.append(t); t += (b - a) + gap
    times.append(t)
    inputs, chains = [], []
    for i, (p, a, b) in enumerate(parts):
        inputs += ['-i', p]
        pad = 0.5 if i == 0 else 0.4 if i == 1 else 0
        chains.append(f'[{i}:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,highpass=f=320,lowpass=f=3400,aformat=sample_rates=44100:channel_layouts=mono,apad=pad_dur={pad}[p{i}]')
    graph = ';'.join(chains) + ';' + ''.join(f'[p{i}]' for i in range(3)) + 'concat=n=3:v=0:a=1,volume=1.15[o]'
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', *inputs, '-filter_complex', graph, '-map', '[o]', '-codec:a', 'libmp3lame', '-b:a', '160k', out], check=True)
    return times


def timed(src, out, a, b, speed):
    """the line, trimmed with a little air around the words, sped up once with Rubber Band (speech settings, formants kept,
    so no warble or stutter) and faded in and out by a few milliseconds so it never starts or stops on a click"""
    n = b - a; fo = n / speed - 0.04
    af = (f'atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,'
          + (f'rubberband=tempo={speed}:transients=mixed:detector=soft:formant=preserved:pitchq=quality:channels=together,' if speed != 1 else '')
          + f'afade=t=in:d=0.015,afade=t=out:st={fo:.3f}:d=0.04')
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', src, '-af', af, '-ar', '44100', '-codec:a', 'libmp3lame', '-b:a', '192k', out], check=True)


def build(version, vo_src):
    spec = {'v1': V1, 'v2': V2}[version](); shots, speed = spec['shots'], spec['speed']
    work = os.path.join(OUT, f'.vo-{version}'); os.makedirs(work, exist_ok=True)
    trims, lens, Ts, demo_times, demo_off = [], [], [], None, 0.0
    for i, shot in enumerate(shots, 1):
        src = os.path.join(work, f'src-{i}.mp3'); mp3 = os.path.join(work, f'line-{i}.mp3')
        if shot.get('demo'):
            demo_times = make_demo(vo_src, src)
        else:
            shutil.copy(os.path.join(vo_src, f'{i}.mp3'), src)
        sp, dur = speech(src)
        pa, pb = max(0.0, sp[0][0] - 0.06), min(dur, sp[-1][1] + 0.1)
        timed(src, mp3, pa, pb, speed)
        if shot.get('demo'): demo_off = pa
        spans, dur = speech(mp3)
        b = spans[-1][1]
        trims.append((0.0, round(dur - 0.09, 2)))
        open(mp3[:-4] + '.vtt', 'w').write(caption(shot['line'], spans).replace('<v Nyasha>', '<v iContact>'))
        need = LEAD + b + (spec['end_tail'] if i == len(shots) else spec['tail'])
        need = max(need, LEAD + dur)          # the next line never starts before this file ends
        lens.append(round(max(shot.get('min', 0), need) + 0.049, 1))
        Ts.append(b)
    starts, t = [], 0.0
    for n in lens: starts.append(round(t, 2)); t += n
    length = round(t, 2)
    if demo_times:
        k = [s['page'] for s in shots].index('demo')
        page_t = [LEAD + (x - demo_off) / speed for x in demo_times]
        shots[k]['html'] = lambda T, pt=page_t: P.demo(pt, T)

    # sound effects, at film seconds; named offsets point at the events in a shot
    named = {}
    for i, shot in enumerate(shots):
        T = Ts[i]
        if shot['page'] == 'intro': named[(i, 'booked')] = LEAD + T * (0.9 if version == 'v2' else 0.88) + 0.3
        if shot['page'] == 'pricing':
            xs = (0.12, 0.33, 0.56, 0.82) if version == 'v2' else (None, 0.36, 0.66)
            for j, x in enumerate(xs): named[(i, f'card{j}')] = 0.3 if x is None else LEAD + T * x
        if shot['page'] == 'demo':
            named[(i, 'ring')] = 0.0; named[(i, 'done')] = LEAD + (demo_times[-1] - demo_off) / speed
    cues = []
    for i, shot in enumerate(shots):
        for kind, off, vol in shot.get('sfx', []):
            if i == 0 and kind == 'whoosh': continue
            at = named[(i, off)] if isinstance(off, str) else off
            cues.append((kind, round(starts[i] + at, 2), vol))

    for size, (w, h) in SIZES.items():
        d = os.path.join(OUT, f'{version}-{size}'); os.makedirs(d, exist_ok=True)
        for name in os.listdir(d):
            if name == '.film' or name.endswith('.mp4'): continue
            p = os.path.join(d, name); shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
        shutil.copytree(os.path.join(KIT, 'lib'), os.path.join(d, 'lib'), ignore=shutil.ignore_patterns('street.js', 'fx.js', 'ui.js'))
        shutil.copytree(os.path.join(KIT, 'img'), os.path.join(d, 'img'))
        for i, (shot, n) in enumerate(zip(shots, lens)):
            html = shot['html'](Ts[i])
            html, k = re.subn(r'\bshot\(5', f'shot({n:g}', html, count=1)
            assert k == 1, shot['page']
            open(os.path.join(d, f"{shot['page']}.html"), 'w').write(html)
        vo = os.path.join(d, 'assets', 'vo'); os.makedirs(vo)
        for i in range(1, len(shots) + 1):
            for ext in ('mp3', 'vtt'): shutil.copy(os.path.join(work, f'line-{i}.{ext}'), vo)
        sfx_dir = os.path.join(d, 'assets', 'sfx'); os.makedirs(sfx_dir)
        for kind in {c[0] for c in cues}: psound.write_mp3(os.path.join(sfx_dir, f'{kind}.mp3'), psound.fx(kind))
        psound.write_mp3(os.path.join(d, 'assets', 'music', 'score.mp3'), psound.score_calm(length + 0.1, {'end': starts[-1]}))

        out = ['<!doctype html>', '<html>', '<head>', '<meta charset="utf-8">', f'<meta name="viewport" content="width={w}, height={h}">',
               '</head>', '<body>', '<section>']
        for shot, at in zip(shots, starts):
            out.append(f'  <iframe id="{shot["page"]}" src="{shot["page"]}.html"' + (f' at="{at:g}"' if at else '') + '></iframe>')
        out += ['</section>', '<section>']
        for i, (at, (a, b)) in enumerate(zip(starts, trims), 1):
            out.append(f'  <audio id="vo-{i}" src="assets/vo/line-{i}.mp3#t={a:.2f},{b:.2f}" at="{at + LEAD:g}"></audio>')
        out.append('</section>')
        tracks = []
        for kind, at, vol in sorted(cues, key=lambda c: c[1]):
            ln = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', os.path.join(sfx_dir, f'{kind}.mp3')], capture_output=True, text=True).stdout)
            for tr in tracks:
                if tr[-1][3] <= at: tr.append((kind, at, vol, at + ln)); break
            else: tracks.append([(kind, at, vol, at + ln)])
        n = 0
        for tr in tracks:
            out.append('<section>')
            for kind, at, vol, _ in tr:
                n += 1; out.append(f'  <audio id="sfx-{n}-{kind}" src="assets/sfx/{kind}.mp3" at="{at:g}" volume="{vol}"></audio>')
            out.append('</section>')
        out += ['<section>', f'  <audio id="music" src="assets/music/score.mp3#t=0,{length:g}" volume="{spec["music"]}"></audio>', '</section>', '</body>', '</html>', '']
        open(os.path.join(d, 'film.html'), 'w').write('\n'.join(out))
        write_srt(os.path.join(d, f'{version}-{size}.srt'), vo, starts, trims, 1.0)
    json.dump({'version': version, 'length': length, 'speed': speed, 'shots': [{'page': s['page'], 'line': s['line'], 'start': st, 'length': n} for s, st, n in zip(shots, starts, lens)]},
              open(os.path.join(OUT, f'{version}.json'), 'w'), indent=1)
    print(f'{version}: {length}s  shots {lens}')


def write_srt(path, vo, starts, trims, speed):
    def ts(x):
        ms = int(round(x * 1000)); return f'{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}'
    def sec(s):
        h, m, r = s.split(':'); return int(h) * 3600 + int(m) * 60 + float(r)
    out, n = [], 0
    for i, (at, (a, _)) in enumerate(zip(starts, trims), 1):
        vtt = open(os.path.join(vo, f'line-{i}.vtt')).read()
        for x, y, text in re.findall(r'([\d:.]+) --> ([\d:.]+)\n(.+)', vtt):
            n += 1
            out += [str(n), f'{ts(at + LEAD + (sec(x) - a) / speed)} --> {ts(at + LEAD + (sec(y) - a) / speed)}', re.sub(r'<[^>]+>', '', text).strip(), '']
    open(path, 'w').write('\n'.join(out))


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0] not in ('v1', 'v2') or '--vo' not in a: raise SystemExit(__doc__)
    build(a[0], a[a.index('--vo') + 1])
