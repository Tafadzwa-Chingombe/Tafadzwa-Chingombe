# Nyasha video ads: iContact Africa Solutions

Four 9:16 (1080×1920, 30 fps) Reels/TikTok/Shorts ads, built from *Nyasha_Video_Ad_Scripts.md* with [OpenFilm](https://github.com/openfilm/openfilm).
Each folder is an OpenFilm project: `film.html` is the edit, each `*.html` page is one shot, and the rendered MP4 sits beside it.

| Folder | Script | Length | Shots |
|---|---|---|---|
| `a-show-up-online/` | A: "Do you show up online?" (hero) | 25 s | C4 hook → search B-roll → C3 intro + services → enquiry notifications → C3 end card |
| `b-three-mistakes/` | B: "3 website mistakes" (educational) | 28 s | C3 "3" hook → not mobile-friendly → no contact button (and the fix) → slow loading → end card |
| `c-same-day-quote/` | C: "Same-day quote" (offer) | 18 s | C2 lean-in → form → fixed-price quote → sent → C2 smile → "Tatenda!" end card |
| `d-meet-nyasha/` | D: "Meet Nyasha" (brand intro) | 15 s | C4 "Mhoro!" → C3 digital guide → services montage → "Follow" end card |

**1:1 cuts for Facebook/LinkedIn** (1080×1080) are in `square/<name>-1x1/`. Each uses the same shot pages: the full vertical layout is scaled into a centre panel over a blurred copy of the shot, with the wordmark top-left and captions along the bottom. If you edit a vertical shot, copy the page into the square project too (or rebuild it), then render both.

Render map: C4 = `c4-closeup.jpg`, C3 = `c3-wave-square.jpg` / `c3-wave-wide.jpg`, C2 = `c2-portrait.jpg`.

## What is in every ad
- The iCONTACT wordmark top-left on every frame (`chrome.html`). The on-screen "AI-generated character" badge was removed at the client's request, so disclosure relies on the platform AI labels below (and Nyasha's own line in Script D).
- **Safe zones**: no key text in the top 250 px or the bottom 340 px.
- **Burned-in captions** of the full voice-over script, from `assets/vo/nyasha-vo.vtt` (word-timed).
- Brand colours `#2E5795` / `#ABCF47` / `#0B1F3A`, Poppins type, a green **Book a free call** button and **icontactafricasolutions.org** on the end card.
- **Music and sound effects were synthesised in code** for these ads (original, so there is no licence to clear).

## Before publishing: checklist
- [ ] **[verify] claims approved by iContact**: "Fixed-price quotes", "Same-day reply" (A, 15–21 s) and "fixed-price quote — same day" (C, 3–10 s; the "Sent · same day" tick). Each is one DOM element in `enquiry.html` / `quote.html`, so it is easy to soften in Studio if needed.
- [ ] **Record the real voice-over** (ElevenLabs or a Zimbabwean voice actor) and have a native speaker check *Mhoro*, *Zvakanaka* and *Tatenda*.
- [ ] **Required:** switch on each platform's **AI-content label** when uploading (Meta, TikTok, YouTube). With no on-screen badge, this is the only AI disclosure on A, B and C.
- [ ] Script B wants a **pointing render** for the "3" hook; `count.html` uses C3 (hand raised) until one exists.

## Adding the voice-over (ElevenLabs)
`tools/voiceover.py` generates Nyasha's voice line by line (`eleven_multilingual_v2`, stability 0.45, similarity 0.75, style 0.25),
writes word-timed captions from the real audio, places every line at its shot in **all eight** films (vertical and 1:1),
replaces the silent stand-in and lowers the music to 0.3 under the voice. A line longer than its shot is sped up to at most 1.15×;
anything still too long is listed so that shot can be lengthened.

1. In the cloud environment settings: allow `api.elevenlabs.io` under Network access, and add `ELEVENLABS_API_KEY`
   (and optionally `ELEVENLABS_VOICE_ID`) as environment variables. Start a new session so they apply.
2. `python3 nyasha-ads/tools/voiceover.py` (or `… voiceover.py a c` for some films only)
3. Render each project: `npx -y openfilm@latest render --subtitles`
4. Have a native speaker check *Mhoro*, *Zvakanaka* and *Tatenda*; adjust the `SPOKEN` table in the script if a word needs respelling.

## Editing and rendering
```bash
cd nyasha-ads/a-show-up-online
npx -y openfilm@latest open .                    # opens Studio: drag, retime, edit text, restyle captions
npx -y openfilm@latest render --subtitles        # → a-show-up-online.mp4 with captions burned in
```
To change caption size or colour (e.g. the brand-green word highlight), open the project in Studio and use its Subtitles panel.
