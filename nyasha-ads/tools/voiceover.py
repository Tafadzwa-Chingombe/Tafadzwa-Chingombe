"""Nyasha's voice-over from ElevenLabs, dropped into all eight films (vertical + 1:1).

For each script line it asks ElevenLabs for speech *with timestamps*, saves
  assets/vo/line-N.mp3  and  assets/vo/line-N.vtt   (word-timed captions from the real audio)
and places each line in film.html at the second its shot starts, replacing the silent stand-in.
A line longer than its slot is sped up (pitch kept) up to MAX_SPEED; anything still too long is reported
so the shot can be lengthened rather than the voice rushed.

needs:  ELEVENLABS_API_KEY   (environment variable; never commit it)
        ELEVENLABS_VOICE_ID  (optional; else DEFAULT_VOICE)
usage:  python3 nyasha-ads/tools/voiceover.py [a b c d]          generate + place
        python3 nyasha-ads/tools/voiceover.py --selftest          check the caption/placement logic offline
then render each project:  npx -y openfilm@latest render --subtitles
"""
import base64, json, os, re, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL = 'eleven_multilingual_v2'
DEFAULT_VOICE = 'EXAVITQu4vr4xnSDxMaL'          # a warm female stock voice; swap for your chosen Nyasha voice
SETTINGS = {'stability': 0.45, 'similarity_boost': 0.75, 'style': 0.25, 'use_speaker_boost': True}  # per the brief
MAX_SPEED = 1.15
MUSIC_UNDER_VOICE = 0.3

# (film key, folders, [(slot start, slot end, line)]) — slots are the shot cuts in film.html
FILMS = {
    'a': (['a-show-up-online', 'square/a-show-up-online-1x1'], 25, [
        (0.15, 3.0, "Mhoro! Quick question — if a customer searched for your business right now… would they find you?"),
        (3.1, 8.0, "Most businesses in Harare don't show up. So those customers? They call someone else."),
        (8.1, 15.0, "I'm Nyasha from iContact Africa Solutions. We build fast, mobile-friendly websites, plus SEO and marketing, that bring in real enquiries."),
        (15.2, 20.8, "Fixed-price quotes. Same-day reply."),
        (21.0, 24.8, "Tap the link, book your free call — and let's get you found. Zvakanaka!"),
    ]),
    'b': (['b-three-mistakes', 'square/b-three-mistakes-1x1'], 28, [
        (0.15, 3.0, "Mhoro! Three website mistakes that quietly cost you customers."),
        (3.1, 10.0, "One: your site doesn't work on a phone. Most people in Zimbabwe browse on mobile — if it's hard to read, they leave."),
        (10.1, 17.0, "Two: no clear way to contact you. Put your phone number and a WhatsApp or enquiry button on every page."),
        (17.1, 23.0, "Three: it's slow. If it takes more than a few seconds, people won't wait."),
        (23.1, 27.8, "We fix all three. Book a free call and we'll tell you what's holding your site back."),
    ]),
    'c': (['c-same-day-quote', 'square/c-same-day-quote-1x1'], 18, [
        (0.15, 3.0, "Need a website but don't know what it'll cost?"),
        (3.1, 10.0, "Tell us what you need. We'll send you a fixed-price quote — same day."),
        (10.1, 14.0, "No surprises. No jargon. Just a clear plan."),
        (14.1, 17.8, "Tap to book your free call. Tatenda!"),
    ]),
    'd': (['d-meet-nyasha', 'square/d-meet-nyasha-1x1'], 15, [
        (0.15, 3.0, "Mhoro! I'm Nyasha."),
        (3.1, 9.0, "I'm iContact Africa Solutions' digital guide — I'll show you how to get your business found, trusted and booked."),
        (9.1, 12.0, "Websites. SEO. Marketing. All in plain English."),
        (12.1, 14.8, "Follow me for tips every week — and yes, I'm AI-generated!"),
    ]),
}

# Spoken forms: how the words should sound (captions keep the written form)
SPOKEN = {
    'iContact Africa Solutions': 'eye-Contact Africa Solutions',
    'SEO': 'S.E.O.',
}


def tts(text, key, voice):
    spoken = text
    for a, b in SPOKEN.items():
        spoken = spoken.replace(a, b)
    req = urllib.request.Request(
        f'https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128',
        data=json.dumps({'text': spoken, 'model_id': MODEL, 'voice_settings': SETTINGS}).encode(),
        headers={'xi-api-key': key, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=120) as r:
        body = json.load(r)
    return base64.b64decode(body['audio_base64']), body['alignment'], spoken


def word_times(alignment, spoken, written):
    """the start and end of each spoken word, mapped back onto the written words (same count, same order)"""
    chars, starts, ends = alignment['characters'], alignment['character_start_times_seconds'], alignment['character_end_times_seconds']
    words, cur = [], None
    for ch, s, e in zip(chars, starts, ends):
        if ch.isspace():
            if cur: words.append(cur); cur = None
            continue
        cur = [s, e] if cur is None else [cur[0], e]
    if cur: words.append(cur)
    w = written.split()
    if len(words) != len(w):   # the spoken form split differently: spread evenly as a fallback
        total = ends[-1] if ends else 1.0
        words = [[total * i / len(w), total * (i + 1) / len(w)] for i in range(len(w))]
    return list(zip(w, words))


def ts(s):
    s = max(0.0, s)
    return f"{int(s // 3600):02d}:{int(s % 3600 // 60):02d}:{s % 60:06.3f}"


def vtt(timed, maxlen=34):
    """cues of up to ~maxlen characters, cut after sentence ends; a timestamp tag at each word"""
    cues, cur = [], []
    for word, t in timed:
        if cur and len(' '.join(x for x, _ in cur + [(word, t)])) > maxlen:
            cues.append(cur); cur = []
        cur.append((word, t))
        if re.search(r'[.?!—…]$', word) and len(' '.join(x for x, _ in cur)) > 12:
            cues.append(cur); cur = []
    if cur: cues.append(cur)
    out = ['WEBVTT', '']
    for c in cues:
        body = ' '.join(w if i == 0 else f'<{ts(t[0])}>{w}' for i, (w, t) in enumerate(c))
        out += [f'{ts(c[0][1][0])} --> {ts(c[-1][1][1])}', f'<v Nyasha>{body}', '']
    return '\n'.join(out)


def place(folder, length, clips):
    """film.html: the silent stand-in replaced by the voice lines; music ducked under the voice"""
    path = os.path.join(ROOT, folder, 'film.html')
    film = open(path).read()
    lines = '\n'.join(
        f'  <audio id="vo-{i + 1}" src="assets/vo/line-{i + 1}.mp3" at="{at:g}"' + (f' speed="{sp:g}"' if sp != 1 else '') + '></audio>'
        for i, (at, sp) in enumerate(clips))
    film, n = re.subn(r'<section>\n  <audio id="vo"[^\n]*\n</section>', f'<section>\n{lines}\n</section>', film)
    if n == 0:
        film, n = re.subn(r'<section>\n(  <audio id="vo-\d+"[^\n]*\n)+</section>', f'<section>\n{lines}\n</section>', film)
    if n != 1: raise SystemExit(f'{folder}/film.html: could not find the voice track')
    film = re.sub(r'(<audio id="music" [^>]*volume=")[\d.]+', rf'\g<1>{MUSIC_UNDER_VOICE}', film)
    open(path, 'w').write(film)


def run(keys):
    key = os.environ.get('ELEVENLABS_API_KEY')
    if not key: raise SystemExit('ELEVENLABS_API_KEY is not set (add it in the environment settings, then start a new session)')
    voice = os.environ.get('ELEVENLABS_VOICE_ID', DEFAULT_VOICE)
    report = []
    for k in keys:
        folders, length, lines = FILMS[k]
        clips, files = [], []
        for i, (start, end, text) in enumerate(lines, 1):
            audio, alignment, spoken = tts(text, key, voice)
            timed = word_times(alignment, spoken, text)
            dur = alignment['character_end_times_seconds'][-1]
            slot = end - start
            speed = 1.0 if dur <= slot else min(MAX_SPEED, round(dur / slot + 0.005, 2))
            if dur / speed > slot + 0.05:
                report.append(f'{k} line {i}: {dur:.1f}s of speech in a {slot:.1f}s shot (even at {speed}×) — lengthen that shot')
            clips.append((start, speed))
            files.append((i, audio, vtt(timed)))
            print(f'{k}{i}: {dur:.2f}s  slot {slot:.2f}s  speed {speed}')
        for folder in folders:
            vo = os.path.join(ROOT, folder, 'assets', 'vo')
            os.makedirs(vo, exist_ok=True)
            for name in os.listdir(vo):
                if name.startswith('nyasha-vo.'): os.remove(os.path.join(vo, name))   # the silent stand-in
            for i, audio, cues in files:
                open(os.path.join(vo, f'line-{i}.mp3'), 'wb').write(audio)
                open(os.path.join(vo, f'line-{i}.vtt'), 'w').write(cues)
            place(folder, length, clips)
    print('\n'.join(['', 'Overruns:'] + report) if report else '\nEvery line fits its shot.')


def selftest():
    text = "Mhoro! I'm Nyasha."
    chars = list(text)
    al = {'characters': chars, 'character_start_times_seconds': [i * 0.05 for i in range(len(chars))],
          'character_end_times_seconds': [i * 0.05 + 0.05 for i in range(len(chars))]}
    timed = word_times(al, text, text)
    assert [w for w, _ in timed] == ['Mhoro!', "I'm", 'Nyasha.'], timed
    out = vtt(timed)
    assert out.startswith('WEBVTT') and '<v Nyasha>Mhoro!' in out, out
    print(out)
    print('selftest ok')


if __name__ == '__main__':
    args = sys.argv[1:]
    if args == ['--selftest']: selftest()
    else: run(args or list(FILMS))
