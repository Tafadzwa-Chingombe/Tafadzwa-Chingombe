# iContact AI Voice Agent explainer: delivery notes

Built from *iContact AI Voice Agent Explainer Video* (the brief). Both versions are done in all three sizes.

## Files (in `delivery/`)

| Version | 16:9 master (1920 × 1080) | 9:16 (1080 × 1920) | 4:5 (1080 × 1350) |
|---|---|---|---|
| V1, 60 s | `iContact_AIVoice_V1_60s_16x9_v1.mp4` | `iContact_AIVoice_V1_60s_9x16_v1.mp4` | `iContact_AIVoice_V1_60s_4x5_v1.mp4` |
| V2, 120 s | `iContact_AIVoice_V2_120s_16x9_v1.mp4` | `iContact_AIVoice_V2_120s_9x16_v1.mp4` | `iContact_AIVoice_V2_120s_4x5_v1.mp4` |

Every video has a matching `.srt` with the same name.

**Specification:**
- H.264, 30 fps, stereo, −14 LUFS, with the music well below the voice.
- Captions are burned in on every export, and each export also has an SRT file.
- V1 runs 60.0 s and V2 runs 120.0 s.
- Each size is laid out for its own frame: the 9:16 and 4:5 versions are not crops of the 16:9 master. Copy and screens stay clear of the captions, and in 9:16 of the top 14% and bottom 20%.
- Colours: navy `#142a47` and near-black `#0e141b`, with the green `#abcf47` from your logo as the accent.
- Your logo file is used as supplied, on an off-white panel. It isn't recreated.
- End card: "AI handles the repetitive calls. Your people handle the moments that matter.", then "WhatsApp AGENT to +263 71 857 4277" and "iContact Africa Solutions | Harare, Zimbabwe". This is the single-number line from the brief, as you chose.

## Voice

- **The voiceover uses your ElevenLabs agent's voice, "Eric – Smooth, Trustworthy".** It was generated on your account in the flow "iContact AI Voice Agent explainer: voiceover (agent voice)".
- **The voice plays about 10–15% faster** (V1 ×1.15, V2 ×1.1) so the scripts fit 60 s and 120 s. At normal speed the V1 script alone runs 61 s. The pitch is unchanged.
- **Your approved recordings drop straight in.** Save them as `1.mp3`, `2.mp3` and so on, then run `python3 tools/build_aiv.py v1 --vo <folder>`. The cut and captions re-time themselves.
- **V2 Example call (0:26–0:37):** "Hi, this is the AI assistant for Example Motors. I'm calling to confirm your car service tomorrow at ten…" The agent is in your agent's voice. The customer is a different stand-in voice ("Sim"). Both have a phone-line sound and are labelled Example on screen.
  - This is the optional demo scene the brief allows. All of its words are new script, so please approve them.

## Rules check

- [x] **No added claims:** no client names, percentages, ratings, savings or results. The figures shown are only the prices in the brief.
- [x] **Fictional screens, labelled Example:** "Example Customer", "Example Advisory", "Example Clinic", "Example Patient", "Example Tech Ltd", "Example Lodge", "Order EX-1042", "Example Motors". Every screen carries an **Example** label.
- [x] **No sensitive data:** no real patient, banking, card or customer details.
- [x] **People shown honestly:** no AI-generated people. People appear only as a simple line icon.
- [x] **No real company logos:** simple line icons for each industry.
- [x] **Pricing cards:** the figures are unchanged. Each card stays on screen through the end of the scene, and the last card stays up for at least 2.5 s.
- [x] **All seven industries in both versions:** telecoms, financial services, healthcare, technology, retail & e-commerce, travel & hospitality, customer support.
- [x] **AI use, for platform labels:**
  - **Footage:** none is AI-generated. Every scene is motion graphics drawn in code.
  - **Voice:** AI-generated (ElevenLabs). Switch on the platform's AI-content label when you post, unless you replace it with your own recordings.

## On-screen copy beyond the script table

A few short labels were needed to make the screens readable. Please check them:
- "How it works" (V2 flow); "AI and your team" / "AI and a human employee" (comparison); "When to use what" (AI alone vs AI + people).
- "Pricing" (V1) and "Pricing is simple" (V2, from the voiceover).
- V2 Example call: "The agent says it's an AI, then gets it done." and "An invented call, in the agent's voice."
- Status chips on the mock screens: "Renewal booked", "Confirmed", "Qualified", "Passed to team" and similar.

## Licence record

| Asset | Source | Licence |
|---|---|---|
| Music bed (calm score) | Composed and synthesised in code for this project (`tools/psound.py`) | Original work, owned by you |
| Sound effects (whoosh, ring, pop, ding, shimmer) | Synthesised in code (`tools/psound.py`) | Original work, owned by you |
| Voiceover (agent voice "Eric", customer voice "Sim") | ElevenLabs text-to-speech on your account | Commercial use under your ElevenLabs plan |
| Fonts (Poppins, Inter) | Google Fonts | SIL Open Font License |

## How it's built

- `tools/aiv_pages.py`: the scenes. One page per shot, laid out for each frame.
- `tools/build_aiv.py`: fits each shot to its voice line and writes the three projects per version: `v1-16x9`, `v1-9x16`, `v1-4x5`, `v2-…`.
- `kit/lib/aiv.css`, `aiv.js`, `orient.js`: the shared layout and motion.
- Each project folder opens in OpenFilm Studio for edits.

## Scheduled posts (Metricool, auto-publish)

V2 (120 s), Nyasha voice, on **Sunday 16 November 2026** (Africa/Harare):

| Time | Network | Video | Notes |
|---|---|---|---|
| 10:00 | Facebook (post, title "AI Voice Agents for Your Business") | 4:5 | Caption includes `https://wa.me/263718574277?text=AGENT` |
| 12:00 | Instagram Reel | 9:16 | AI-content label on |
| 18:00 | TikTok (title "What if every enquiry got a call?") | 9:16 | AI-content label on |

Caption (Facebook; Instagram is the same without the link; TikTok is shorter):

> How can a business follow up every enquiry without stretching the team? An AI voice agent can make the routine calls for you: following up leads, qualifying enquiries, sending reminders and booking appointments.
>
> iContact Africa Solutions sets up and manages AI voice agents for businesses in Harare and across Zimbabwe. The agent says it's an AI, follows your script and rules, then books a time, passes the call to your team or records the follow-up.
>
> Built for telecoms, financial services, healthcare, technology, retail and e-commerce, travel and hospitality, and customer support.
>
> AI handles the repetitive calls. Your people handle the moments that matter.
>
> Pricing: setup from $150, management from $150 a month, plus $40 per attended appointment on sales campaigns. Support and reminder plans are quoted by volume.
>
> Start with a small pilot. WhatsApp the word AGENT to +263 71 857 4277 and let's plan yours.
>
> #AIVoiceAgent #AIForBusiness #BusinessAutomation #LeadGeneration #CustomerService #HarareBusiness #ZimbabweBusiness #SmallBusinessZimbabwe

TikTok hashtags: #AIVoiceAgent #AIForBusiness #BusinessAutomation #SmallBusiness #HarareBusiness #ZimbabweBusiness #TechTok
