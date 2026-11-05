# iContact production pack: Batch 1 delivery notes

Batch 1 from the *iContact Video Ad Production Pack*: **S1 The 10-Second Test**, **S2 The Portal Tour** and **C1 Invisible**.
The S1 Shona slot is ready but is waiting for your Shona recording (see `s1-shona/README.md`).

## Files (in `delivery/`)

| Video | 9:16 | 4:5 | Captions | Thumbnail |
|---|---|---|---|---|
| S1 The 10-Second Test | `iContact_S1_10SecondTest_9x16_v1.mp4` | `…_4x5_v1.mp4` | `.srt` for each | `iContact_S1_10SecondTest_thumbnail_9x16_v1.png` + 4:5 |
| S2 The Portal Tour | `iContact_S2_PortalTour_9x16_v1.mp4` | `…_4x5_v1.mp4` | `.srt` for each | `…_thumbnail_9x16_v1.png` + 4:5 |
| C1 Invisible | `iContact_C1_Invisible_9x16_v1.mp4` | `…_4x5_v1.mp4` | `.srt` for each | `…_thumbnail_9x16_v1.png` + 4:5 |

**Specification met:**
- 1080 × 1920 and 1080 × 1350, H.264, 30 fps, stereo.
- Under 30 MB each.
- −14 LUFS, with the voice clear and the music well below it.
- Captions burned in, plus an SRT file for every version.
- Text and logos kept inside the safe zones: nothing in the top 14% or bottom 20% of the 9:16 frame.
- The 4:5 version is a centred crop of the same frame.
- British spelling throughout ("enquiries").
- Every video ends on the standard end card, with **your supplied logo file** (unaltered, on an off-white panel so the blue reads on navy) and the logo's green `#abcf47` as the accent: the tagline, "WhatsApp [KEYWORD] to +263 71 857 4277" and "iContact Africa Solutions | Harare, Zimbabwe".

## Rules check

- [x] **No invented proof:** no client numbers, ratings, testimonials or results.
- [x] **Mock websites only:** "Example Plumbing", "Example Bakery", "Example Services Ltd" and other invented names. Every phone screen is labelled **Example**.
- [x] **No client data:** the portal demo uses invented details only ("client@example.com", "Invoice EX-002", "Example amount").
- [x] **No identifiable real people or businesses:** C1 is drawn in code. The street, building and people are generic silhouettes, and the sign panel has no lettering.
- [x] **AI use, for platform labels:**
  - **Footage:** none of the shots is AI-generated, so no AI label is needed for imagery.
  - **Voice:** the voiceover is an **AI stand-in voice** (ElevenLabs, "Peter – South African Commercial"). If you post these before swapping in your own recordings, switch on the platform's AI-generated content label. TikTok in particular asks for it for synthetic voices.
- [x] **Licences:** see the record below.

## Licence record (music and sound effects)

| Asset | Source | Licence |
|---|---|---|
| Music beds (S1 and S2 calm score, C1 cinematic score) | Composed and synthesised in code for this project (`icontact-pack/tools/psound.py`) | Original work, owned by you; no third-party licence |
| Sound effects (ticks, whooshes, street ambience) | Synthesised in code (`psound.py`) | Original work, owned by you; no third-party licence |
| Stand-in voiceover | ElevenLabs text-to-speech, generated on your ElevenLabs account (flow "iContact production pack: Batch 1 voiceover (stand-in)") | Commercial use under your ElevenLabs plan's terms |
| Fonts (Poppins, Inter) | Google Fonts | SIL Open Font License |

## Still needed from you

1. **Your voiceover recordings** (one take per script). The cut re-times itself to your takes, and the captions are rebuilt from your actual words.
2. **S1 Shona voiceover and approved Shona captions.** See `s1-shona/README.md`.
3. **Approval of the mock sites and portal screens.** The pack asks for placeholders to be sent for approval when your own screen recordings aren't ready. These are those placeholders. If you'd rather use your real portal demo recording, send it and I'll put it in the phone frame.
4. **Optional: real Harare street footage for C1.** The code-drawn street can be replaced shot by shot.

## Posting (from the pack)

| When | What |
|---|---|
| Week of 23 Nov | S1 and C1 |
| Week of 30 Nov | S2 and S1 Shona |

Use the Meta post descriptions, CTA button ("Send WhatsApp message") and the `wa.me` links in the pack exactly as written.
