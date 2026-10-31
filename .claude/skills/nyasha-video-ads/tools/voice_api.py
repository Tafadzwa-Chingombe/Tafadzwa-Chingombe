"""Nyasha's voice lines straight from the ElevenLabs API (the alternative to the ElevenLabs connector).

Writes <out-dir>/1.mp3, 2.mp3 … — one per shot in <film>/ad.json — ready for `build.py <film> --vo <out-dir>`.
needs:  ELEVENLABS_API_KEY in the environment (never in code or chat) and network access to api.elevenlabs.io
        ELEVENLABS_VOICE_ID optional (default: Sim – Warm South African English)
usage:  python3 voice_api.py <film-folder> <out-dir>
"""
import json, os, sys, urllib.request

VOICE = 'Sy7d8PNbkbjIJxf1li2K'   # Sim – Warm South African English
MODEL = 'eleven_v3'
SETTINGS = {'stability': 0.45, 'similarity_boost': 0.75, 'style': 0.25, 'use_speaker_boost': True}
SPOKEN = {'SEO': 'S.E.O.'}       # how a word should be said, where the written form misleads the voice


def speak(text, key, voice):
    for a, b in SPOKEN.items():
        text = text.replace(a, b)
    req = urllib.request.Request(
        f'https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_128',
        data=json.dumps({'text': text, 'model_id': MODEL, 'voice_settings': SETTINGS}).encode(),
        headers={'xi-api-key': key, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


if __name__ == '__main__':
    if len(sys.argv) != 3: raise SystemExit(__doc__)
    film, out = sys.argv[1], sys.argv[2]
    key = os.environ.get('ELEVENLABS_API_KEY') or sys.exit('ELEVENLABS_API_KEY is not set')
    voice = os.environ.get('ELEVENLABS_VOICE_ID', VOICE)
    os.makedirs(out, exist_ok=True)
    for i, shot in enumerate(json.load(open(os.path.join(film, 'ad.json')))['shots'], 1):
        open(os.path.join(out, f'{i}.mp3'), 'wb').write(speak(shot['line'], key, voice))
        print(f'{i}.mp3  {shot["line"][:60]}')
