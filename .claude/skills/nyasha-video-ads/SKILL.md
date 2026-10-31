---
name: nyasha-video-ads
description: Turn an iContact Africa Solutions ad script into finished Nyasha video ads — 9:16 Reels/TikTok/Shorts and 1:1 Facebook/LinkedIn cuts, with Nyasha's ElevenLabs voice, word-timed burned-in captions, brand motion graphics, original music and sound effects. Use when the user shares a Nyasha script (or asks for a new Nyasha / iContact video ad), wants a line re-voiced, an ad re-cut, or the square versions made.
---

# Nyasha video ads

A script doc → finished MP4s, built with OpenFilm (`.claude/skills/openfilm`; run `npx -y openfilm@latest` for its manual
the first time in a session). The four ads in `nyasha-ads/` were made this way: read them as worked examples before
writing new pages (`a-show-up-online/` is the fullest).

```
.claude/skills/nyasha-video-ads/
  kit/lib/           brand.css, kit.js (motion helpers), shot.js (declarative shots), fonts/ (Poppins)
  kit/chrome.html    the iCONTACT wordmark overlay, over the whole film
  kit/endcard.html   end card template (IMG, FX, SIGNOFF, CTA, DURATION placeholders)
  kit/renders/       Nyasha: c4-closeup (C4), c3-wave-square / c3-wave-wide (C3), c2-portrait (C2)
  tools/new_ad.sh    start an ad folder        tools/build.py     fit the cut to the voice, write film.html
  tools/mksquare.py  1:1 cut of a vertical ad  tools/loudness.sh  -14 LUFS for social, video untouched
  tools/sound.py     original music + sfx      tools/voice_api.py voice via the ElevenLabs API (if no connector)
```

## Before starting

Ask (with the question tool) only what the script does not settle: which scripts to make, whether claims marked
**[verify]** are approved (keep them and list them if not), and whether to use the default voice. Defaults: all scripts,
both formats, voice "Sim – Warm South African English", no on-screen AI badge (the client asked for it removed — see
Compliance).

## 1. Plan each ad

From each script table, one **shot per row**: a page name, the script's seconds for it as `min`, and its voice-over line.
Choose a page type per shot:

| Script asks for | Page | Example |
|---|---|---|
| Nyasha talking / reacting | `.photo` render with push-in + headline | `a-show-up-online/hook.html`, `intro.html` |
| Phone / website / form B-roll | CSS `.phone` mock | `search.html`, `enquiry.html`, `c-same-day-quote/quote.html` |
| Montage of cards | absolutely placed cards popping in | `d-meet-nyasha/montage.html` |
| Final CTA | `endcard.html` from the kit | every ad |

Render choice follows the brief: C4 close-up for hooks, C3 (waving, copy space) as default presenter, C2 for portrait/offer.

## 2. Start the folder

```bash
.claude/skills/nyasha-video-ads/tools/new_ad.sh nyasha-ads/<letter>-<slug> '<sign-off, may use <span class="hl">…</span>>' 'Book a free call' c3-wide
export PLAYWRIGHT_BROWSERS_PATH=…   # the line new_ad.sh prints, in a cloud container
```
It opens the OpenFilm project, copies the kit and renders, makes `endcard.html`, and a starter `ad.json`.

## 3. Write the shot pages

One page per shot, 1080×1920, built on `lib/shot.js` — mostly declarative:

```html
<link rel="stylesheet" href="lib/brand.css">
<div class="stage"></div>
<div class="photo"><img src="assets/nyasha/c4-closeup.jpg" data-from="1.0" data-to="1.12" data-fx="0.5" data-fy="0.42" data-tilt="1.2"></div>
<div class="headline" data-rise="0.2" data-fit="70">Would customers find you <span class="hl">online?</span></div>
<script type="module">
import { shot } from './lib/shot.js';
shot(3);                       // build.py rewrites this number to the shot's real length
</script>
```
`data-rise` / `data-pop` = enters at s; `data-out` = fades at s (only on an element that also has rise/pop);
`data-on` = gets class `on` from s (chips); `data-fit` = font shrinks from px to fit. Anything else goes in
`shot(len, (t) => {…})`, computed from `t` only (`typed`, `prog`, `ease`, `pulse` in `kit.js`).

Layout rules (1080×1920):
- Key text between **y 250 and y 1580** (platform UI covers the top 250 and bottom 340 px).
- Captions sit just above **y ≈ 1380**; the headline band is **y 1428–1580**, two lines at 70 px max.
- Photos fill y 0–1330 and fade into navy; phones go at `.phone` (y 360–1280).
- Brand: blue `#2E5795`, green `#ABCF47` (highlights, CTA), navy `#0B1F3A`. Never draw subtitles in a page.
- Mock businesses (Moyo Interiors, Tendai's Plumbing…) are invented; avoid real brands' logos.

## 4. Fill ad.json and build without voice

```json
{"title": "…", "shots": [{"page": "hook", "min": 3, "line": "Mhoro! …"}, …],
 "sfx": [[1, "whoosh", -0.15], [1, "pop", 1.6], …], "music_volume": 0.3}
```
`sfx`: shot index, `pop|ding|whoosh`, seconds into that shot (a whoosh at −0.15 before each cut; a pop when something
pops in; a ding on a success tick). Effects share one track: keep them ≥ 0.5 s apart after a whoosh, ≥ 0.2 s otherwise.

```bash
python3 .claude/skills/nyasha-video-ads/tools/build.py nyasha-ads/<ad>
cd nyasha-ads/<ad> && npx -y openfilm@latest look      # contact sheet + same-t-same-picture check; read the PNG
```
Without voice files it uses silent stand-ins sized to each line, so the captions and timing are already close.

## 5. Voice (ElevenLabs connector)

1. `creative_list_voices` once to confirm the voice (default `Sy7d8PNbkbjIJxf1li2K`, Sim – Warm South African English).
2. `creative_create_flow` named "<ad> voice-over", then `creative_generate_speech` per line with that `flow_id`,
   `model_id: eleven_v4`, default takes. Write *SEO* as "S.E.O." in the prompt (captions keep "SEO").
3. Poll `creative_get_flow_run_status` (large results land in a file: read it with python/jq), pick the shorter take
   of each line, and `curl` its `content_url` to `<dir>/<n>.mp3` (1-based, shot order). The URLs expire after 2 h.
4. Tell the user the credits spent (shown per generation).

No connector? `tools/voice_api.py <ad> <dir>` with `ELEVENLABS_API_KEY` set and `api.elevenlabs.io` allowed.

```bash
python3 .claude/skills/nyasha-video-ads/tools/build.py nyasha-ads/<ad> --vo <dir>
```
Shots stretch to fit natural delivery (never rush the voice; if the ad gets too long, shorten the script). Then **re-sync
on-screen moments**: read `assets/vo/line-N.vtt` for when keywords are said (`<00:00:05.005>websites`), set the page's
`data-pop`/`data-on`/`data-rise` to that time + 0.15, move matching `sfx` entries in `ad.json`, and build again.

## 6. Check, square, render, loudness

```bash
npx -y openfilm@latest look                                         # in each ad folder; fix anything it flags
python3 .claude/skills/nyasha-video-ads/tools/mksquare.py nyasha-ads/<ad> nyasha-ads/square/<ad>-1x1   # after `openfilm open` of that folder
npx -y openfilm@latest render --subtitles --workers 4               # in each folder (vertical and square), ~1 min each
.claude/skills/nyasha-video-ads/tools/loudness.sh nyasha-ads/<ad>/<ad>.mp4 nyasha-ads/square/<ad>-1x1/<ad>-1x1.mp4
```
Run renders in the background. Then pull a few frames with ffmpeg at the moments that matter (hook, a synced chip, the
end card) and look at them before sending. Commit and push, then send the MP4s.

## Compliance and sign-off (always tell the user)

- Nyasha is a photoreal AI character: switch on each platform's **AI-content label** at upload (Meta, TikTok, YouTube).
  The on-screen badge was removed at the client's request; offer to add a smaller one if wanted.
- **[verify]** claims (fixed-price quotes, same-day reply, …) need iContact's approval before publishing.
- Have a Zimbabwean listener check *Mhoro*, *Zvakanaka*, *Tatenda* in the AI voice.

## Things that bite

- **Chromium mismatch** in cloud containers: OpenFilm wants its own build; `new_ad.sh` symlinks the installed one and
  prints the `PLAYWRIGHT_BROWSERS_PATH` to export. Without it `open`/`look`/`render` fail with "could not download the browser".
- `data-rise` sets `transform`: put it on a wrapper when the element needs its own transform (scaled mock sites).
- Page layout is relative to `body` (`position: relative` in brand.css) — keep it, or text fitting changes in the square cut.
- Every picture must depend only on `t`; `look` fails "same t drew two different pictures" otherwise.
- `mksquare.py` replaces the square folder's files (keeps its `.film/`): re-run it after any vertical change, then render both.
- Never commit a half-written MP4: commit renders after `loudness.sh` finishes.
