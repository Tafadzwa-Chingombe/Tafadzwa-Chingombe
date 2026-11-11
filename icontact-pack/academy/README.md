# iContact Academy course ads: delivery notes

Ads for the new self-paced online courses (Digital marketing and Website development), in Nyasha's voice. There are two sets: an explainer set and a story-led set about an invented student, Tendai.

## Files (in `delivery/`)

| Film | Length | 16:9 (1920 × 1080) | 9:16 (1080 × 1920) | 4:5 (1080 × 1350) |
|---|---|---|---|---|
| Full explainer | 2:08 | `iContact_Academy_Explainer_2min_16x9_v1.mp4` | `…_Explainer_2min_9x16_v1.mp4` | `…_Explainer_2min_4x5_v1.mp4` |
| Short ad | 0:39 | `iContact_Academy_Ad_40s_16x9_v1.mp4` | `…_Ad_40s_9x16_v1.mp4` | `…_Ad_40s_4x5_v1.mp4` |
| Teaser | 0:14 | `iContact_Academy_Teaser_15s_16x9_v1.mp4` | `…_Teaser_15s_9x16_v1.mp4` | `…_Teaser_15s_4x5_v1.mp4` |
| Tendai's story | 1:56 | `iContact_Academy_Story_2min_16x9_v1.mp4` | `…_Story_2min_9x16_v1.mp4` | `…_Story_2min_4x5_v1.mp4` |
| Tendai's story, short | 0:45 | `iContact_Academy_Story_45s_16x9_v1.mp4` | `…_Story_45s_9x16_v1.mp4` | `…_Story_45s_4x5_v1.mp4` |

Every video has a matching `.srt` caption file, and the captions are also burned in.

**Specification:**
- H.264, 30 fps, stereo, about −13 LUFS.
- Each size is laid out for its own frame, not cropped.
- Every film plays at Nyasha's natural pace, with no speed-up.
- End card: "WhatsApp ACADEMY to +263 71 857 4277".

## What the films cover

| Point | How it is shown |
|---|---|
| **Self-paced** | Start any time, pause, rewatch, pick up where you left off, and no deadlines. Short video lessons and notes on phone, tablet or laptop, with progress saved. |
| **Realistic project** | Website development: build and publish a working small-business website (an "Example Bakery" site going from Draft to Live). Digital marketing: plan a real campaign and set up a Google Business Profile. |
| **Value for money** | One payment per course, with no subscription and no deadline. You keep access to the course, including updates to its lessons. No price is shown. |
| **Easy payment** | EcoCash, Paynow or bank transfer. The login is sent by WhatsApp or email once payment is confirmed, usually the same day. |
| **Also covered** | Built from real client work, examples made for Zimbabwe, beginner courses, and courses showing in the existing Client Portal login. |

**The story:** Tendai bakes cakes and takes orders on WhatsApp. She finds the Academy, pays with EcoCash and learns on her phone at her own pace. She publishes her bakery's website, then takes the marketing course. The film then says plainly: "Tendai is invented for this story. But the courses are real."

## Rules check

- [x] **English only.**
- [x] **Phone number, not the website,** on the end cards and in the voiceovers ("WhatsApp the word ACADEMY").
- [x] **No invented claims:** no prices, statistics, student numbers or testimonials. Facts come from the Academy page: self-paced, one payment per course, updates included, EcoCash / Paynow / bank, login usually the same day, beginner levels and the Client Portal.
- [x] **Invented people and screens are labelled.** Tendai appears only as an initial "T", never as a realistic AI face, and the voiceover says she's invented. Every screen carries an **Example** label.
- [x] **AI use:** the voice is AI-generated (ElevenLabs, Nyasha's voice), so switch on the platform's AI-content label when posting. The visuals are motion graphics drawn in code.

**Please check before posting:**
- The Academy page currently says the first courses "open soon". Post these once the courses can be bought.
- Check that the lesson names in the films are close enough to the real ones, or ask for them to be changed. They are: "Get found on Google", "Your first landing page" and "Add a WhatsApp button".

## Licence record

| Asset | Source | Licence |
|---|---|---|
| Music and sound effects | Composed and synthesised in code (`tools/psound.py`) | Original work, owned by you |
| Voiceover | ElevenLabs text-to-speech on your account (Nyasha's voice) | Commercial use under your ElevenLabs plan |
| Fonts (Poppins, Inter) | Google Fonts | SIL Open Font License |

## Rebuild

Run `python3 tools/build_academy.py <full|ad60|teaser|story|story60> --vo <folder of numbered mp3s>`. The scenes are in `tools/academy_pages.py`.

## Course trailers (`trailers/delivery/`)

There is one trailer of about 60 s for each published course, in 16:9, 9:16 and 4:5, with `.srt` captions. Each trailer covers the hook, the course and its curriculum, what you learn, a showcase screen and who it's for, then "learn at your own pace, pay once by EcoCash, Paynow or bank transfer, keep access including updates", and ends on the WhatsApp ACADEMY end card. Every claim comes from the course's own page in the Academy catalogue (11 Nov 2026). Prices are left out on purpose, so a price change never dates a video.

| Course | Short name | Status |
|---|---|---|
| Website Basics for Business Owners | `web-basics` | ✅ Done (60 s) |
| HTML & CSS for Beginners | `html-css` | ✅ Done (59 s) |
| SEO & Google Business Profile | `seo-gbp` | ⏳ 3 voice lines still to make (lines 5, 6 and 8; 1–4 and 7 are done) |
| Social Media Marketing for Small Business | `social` | ⏳ Waiting for voiceover |
| Facebook & Instagram Ads from Zimbabwe | `meta-ads` | ⏳ Waiting for voiceover |
| WhatsApp Business for Sales | `whatsapp` | ⏳ Waiting for voiceover |

The ElevenLabs monthly quota ran out partway through. The layouts for all six trailers are built and checked. To finish one, generate its lines, then run `python3 tools/build_trailers.py --lines` to print the script, and `python3 tools/build_trailers.py <short-name> --vo <folder of 1.mp3…8.mp3>` to build it. Line 7 is the same in every trailer, so its file is reused.

**On the website:** each course page shows its trailer once `courses.trailer_url` is set. Run `supabase/academy_trailers.sql` in the website repo once. The web copies (720p, about 3.4 MB) live in `assets/video/academy/trailer-<short-name>.mp4`, next to `-vertical.mp4` (used on phones) and the `-poster.jpg` stills.
