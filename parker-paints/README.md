# Parker Paints: brand video ads

Two English-only brand ads for **Parker Paints (Pvt) Ltd**, Harare. They were made in November 2026 from the
Parker Paints website (`tafadzwa-chingombe.github.io/Parker-Paints/`): brand colours, tagline, product tins, catalogue
colours and contact details.

| Video | Length | Style | Files |
|---|---|---|---|
| **"Every wall tells a story"** | 57.8 s | Cinematic story: sun-baked wall → rain → paint pour → roller reveal → rain beading off → real room → product range → 10-year seal → colour samples → end card | `cinematic-60/cinematic-60.mp4` (9:16) · `square/cinematic-60-1x1/cinematic-60-1x1.mp4` (1:1) |
| **"The perfect finish"** | 31.8 s | Fast motion graphics: Sun. Rain. Cracks. → paint-splash logo reveal → 4 benefit tiles → 29-product fan → guarantee stamp → CTA | `motion-30/motion-30.mp4` (9:16) · `square/motion-30-1x1/motion-30-1x1.mp4` (1:1) |

**How they were made (no paid footage):**
- The "footage" is generated in code. The plaster walls, cracks, peeling paint, sunlight and leaf shadows, rain, water beads, the paint pour and the roller are all procedural.
- The room photo and the product tins come from Parker's own website.
- Modern edit techniques: whip-pans with motion blur, slow push-ins, light leaks on the cuts, film grain, speed-ramped
  text, beat-synced stamps, and word-timed burned-in captions.
- Voice: ElevenLabs "Peter – South African Commercial" (`eleven_v4`), English only. About 2,190 credits for both scripts.
- Music and sound design are original and synthesised in `tools/psound.py`, so there is no licence to clear. That covers the cinematic score, the 120 bpm groove, and the rain, thunder, cicadas, roller, pour, stamp and whooshes.

## Check with Parker Paints before publishing
- **10-year guarantee:** the website's About page ties it to the flagship / premium range. The ads say "premium range".
- **"29 products" and "made in Zimbabwe":** from the products page and the About page ("fully-fledged Zimbabwean paint manufacturer").
- **Free colour samples:** the colour catalogue says "free sample delivery". "Find a dealer" is a button on the site.
- **Contact details on the end cards:** +263 77 472 6179 · (0242) 663270 · 6 Portland Road, Workington, Harare.
  Confirm these are current, and whether the mobile number takes WhatsApp. If it does, the end card can say "Call or WhatsApp".
- **The room photo:** this is the website's hero image. Confirm Parker holds the rights to use it in ads.
- The "perfect finish" tagline and logo are drawn as text in brand colours, because the site's logo file is only 80 px wide.
  For pixel-perfect branding, send a high-resolution logo and it can be dropped in.

## Rebuild
```bash
python3 parker-paints/tools/build.py parker-paints/cinematic-60 --vo <dir with 1.mp3…> --square parker-paints/square/cinematic-60-1x1
python3 parker-paints/tools/build.py parker-paints/motion-30   --vo <dir>            --square parker-paints/square/motion-30-1x1
# then in each folder: npx -y openfilm@latest render --subtitles --workers 4
# and: .claude/skills/nyasha-video-ads/tools/loudness.sh <mp4>
```
- Shared code lives in `kit/`: `lib/kit.js` (motion and shot wrapper), `lib/fx.js` (procedural footage), `lib/parker.css`, `chrome.html` (grain, vignette, light leaks, logo bug) and `img/` (2× upscaled tins and room).
- Voice lines and timings are in each `ad.json`. Shot lengths fit the voice automatically.
