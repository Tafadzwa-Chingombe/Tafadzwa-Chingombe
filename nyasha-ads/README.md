# Nyasha video ads: iContact Africa Solutions

Four 9:16 (1080×1920, 30 fps) Reels/TikTok/Shorts ads, built from *Nyasha_Video_Ad_Scripts.md* with [OpenFilm](https://github.com/openfilm/openfilm).
Each folder is an OpenFilm project: `film.html` is the edit, each `*.html` page is one shot, and the rendered MP4 sits beside it.

| Folder | Script | Length | Shots |
|---|---|---|---|
| `a-show-up-online/` | A: "Do you show up online?" (hero) | 34.9 s | C4 hook → search B-roll → C3 intro + services → enquiry notifications → C3 end card |
| `b-three-mistakes/` | B: "3 website mistakes" (educational) | 35.1 s | C3 "3" hook → not mobile-friendly → no contact button (and the fix) → slow loading → end card |
| `c-same-day-quote/` | C: "Same-day quote" (offer) | 19.1 s | C2 lean-in → form → fixed-price quote → sent → C2 smile → "Tatenda!" end card |
| `d-meet-nyasha/` | D: "Meet Nyasha" (brand intro) | 21.7 s | C4 "Mhoro!" → C3 digital guide → services montage → "Follow" end card |

**1:1 cuts for Facebook/LinkedIn** (1080×1080) are in `square/<name>-1x1/`. Each uses the same shot pages: the full vertical layout is scaled into a centre panel over a blurred copy of the shot, with the wordmark top-left and captions along the bottom. If you edit a vertical shot, copy the page into the square project too (or rebuild it), then render both.

Render map: C4 = `c4-closeup.jpg`, C3 = `c3-wave-square.jpg` / `c3-wave-wide.jpg`, C2 = `c2-portrait.jpg`.

## What is in every ad
- The iCONTACT wordmark top-left on every frame (`chrome.html`). The on-screen "AI-generated character" badge was removed at the client's request, so disclosure relies on the platform AI labels below (and Nyasha's own line in Script D).
- **Safe zones**: no key text in the top 250 px or the bottom 340 px.
- **Nyasha's ElevenLabs voice-over**, with **burned-in captions** timed to her words (`assets/vo/line-N.vtt`).
- Brand colours `#2E5795` / `#ABCF47` / `#0B1F3A`, Poppins type, a green **Book a free call** button and **icontactafricasolutions.org** on the end card.
- **Music and sound effects were synthesised in code** for these ads (original, so there is no licence to clear).

## Before publishing: checklist
- [ ] **[verify] claims approved by iContact**: "Fixed-price quotes", "Same-day reply" (A, 15–21 s) and "fixed-price quote — same day" (C, 3–10 s; the "Sent · same day" tick). Each is one DOM element in `enquiry.html` / `quote.html`, so it is easy to soften in Studio if needed.
- [ ] Have a **native speaker check** *Mhoro*, *Zvakanaka* and *Tatenda* in the ElevenLabs voice-over (re-take any line that sounds off).
- [ ] **Required:** switch on each platform's **AI-content label** when uploading (Meta, TikTok, YouTube). With no on-screen badge, this is the only AI disclosure on A, B and C.
- [ ] Script B wants a **pointing render** for the "3" hook; `count.html` uses C3 (hand raised) until one exists.

## Voice-over (ElevenLabs)
Nyasha's voice was generated with the ElevenLabs connector: voice **"Sim – Warm South African English"**
(`Sy7d8PNbkbjIJxf1li2K`), model `eleven_v4`, one take per line chosen from two (the ElevenLabs flow
"Nyasha ad voice-overs" holds every take). Each film's lines are in `assets/vo/line-N.mp3`, with word-timed captions in `line-N.vtt`.

The cut follows the voice: each ad's `ad.json` lists its shots, voice lines and sound effects, and the
**`nyasha-video-ads` skill** (`.claude/skills/nyasha-video-ads/`) builds `film.html` from it: each shot as long as its line
needs (never shorter than the script's timing), captions timed to her words, effects moved with their shots, music made
again at the new length and set to 0.3 under the voice. On-screen moments (the service chips, "Same-day reply", the quote
steps, "Found · Trusted · Booked") are timed in each page to when she says them.

To replace a line (a re-take, a voice actor, a Shona correction), save the new takes as `1.mp3`, `2.mp3`… (shot order)
in one folder, then:
```bash
T=.claude/skills/nyasha-video-ads/tools
python3 $T/build.py nyasha-ads/a-show-up-online --vo <folder>
python3 $T/mksquare.py nyasha-ads/a-show-up-online nyasha-ads/square/a-show-up-online-1x1
```
and render both (then `$T/loudness.sh` on the MP4s). **New ads:** ask Claude to use the `nyasha-video-ads` skill with the
new script — see `.claude/skills/nyasha-video-ads/SKILL.md` for the full workflow.

## Editing and rendering
```bash
cd nyasha-ads/a-show-up-online
npx -y openfilm@latest open .                    # opens Studio: drag, retime, edit text, restyle captions
npx -y openfilm@latest render --subtitles        # → a-show-up-online.mp4 with captions burned in
../../.claude/skills/nyasha-video-ads/tools/loudness.sh a-show-up-online.mp4   # -14 LUFS for social
```
To change caption size or colour (e.g. the brand-green word highlight), open the project in Studio and use its Subtitles panel.
