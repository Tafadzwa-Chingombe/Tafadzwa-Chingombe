# Nyasha video ads: iContact Africa Solutions

Four 9:16 (1080×1920, 30 fps) Reels/TikTok/Shorts ads, built from *Nyasha_Video_Ad_Scripts.md* with [OpenFilm](https://github.com/openfilm/openfilm).
Each folder is an OpenFilm project: `film.html` is the edit, each `*.html` page is one shot, and the rendered MP4 sits beside it.

| Folder | Script | Length | Shots |
|---|---|---|---|
| `a-show-up-online/` | A: "Do you show up online?" (hero) | 25 s | C4 hook → search B-roll → C3 intro + services → enquiry notifications → C3 end card |
| `b-three-mistakes/` | B: "3 website mistakes" (educational) | 28 s | C3 "3" hook → not mobile-friendly → no contact button (and the fix) → slow loading → end card |
| `c-same-day-quote/` | C: "Same-day quote" (offer) | 18 s | C2 lean-in → form → fixed-price quote → sent → C2 smile → "Tatenda!" end card |
| `d-meet-nyasha/` | D: "Meet Nyasha" (brand intro) | 15 s | C4 "Mhoro!" → C3 digital guide → services montage → "Follow" end card |

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
- [ ] Optional: export a 1:1 (1080×1080) cut for Facebook/LinkedIn (Studio → Export → frame).
- [ ] Script B wants a **pointing render** for the "3" hook; `count.html` uses C3 (hand raised) until one exists.

## Adding the voice-over
`assets/vo/nyasha-vo.mp3` is a **silent stand-in** that carries the captions. To add the real voice:
1. Record or generate one take per film, following the script timings (they match the shot cuts).
2. Replace `assets/vo/nyasha-vo.mp3` with it, and either update `nyasha-vo.vtt` or let Studio transcribe it (Settings → Providers → connect ElevenLabs, OpenAI, Google…).
3. Render again (below). Lower `music` volume to about 0.3 in `film.html` so the voice sits on top.

## Editing and rendering
```bash
cd nyasha-ads/a-show-up-online
npx -y openfilm@latest open .                    # opens Studio: drag, retime, edit text, restyle captions
npx -y openfilm@latest render --subtitles        # → a-show-up-online.mp4 with captions burned in
```
To change caption size or colour (e.g. the brand-green word highlight), open the project in Studio and use its Subtitles panel.
