# iContact professional email explainer: delivery notes

Why a business needs a professional email address, plus how to forward an old Gmail address to it, in Nyasha's voice.

## Files (in `delivery/`)

| Version | 16:9 (1920 × 1080) | 9:16 (1080 × 1920) | 4:5 (1080 × 1350) |
|---|---|---|---|
| V1, 60 s | `iContact_ProEmail_V1_60s_16x9_v1.mp4` | `…_V1_60s_9x16_v1.mp4` | `…_V1_60s_4x5_v1.mp4` |
| V2, full (2:55) | `iContact_ProEmail_V2_3min_16x9_v1.mp4` | `…_V2_3min_9x16_v1.mp4` | `…_V2_3min_4x5_v1.mp4` |

Every video has a matching `.srt` caption file, and the captions are also burned in.

**Specification:**
- H.264, 30 fps, stereo, about −13 LUFS. The music sits well below the voice.
- Each size is laid out for its own frame, not cropped. Copy and screens stay clear of the burned-in captions.
- **Timing:** V2 plays at Nyasha's natural pace. V1 is sped up by 1.04× to fit 60 s, using Rubber Band so there's no stutter.
- End card: "Every email should look like it comes from a real business.", "WhatsApp EMAIL to +263 71 857 4277" and "iContact Africa Solutions | Harare, Zimbabwe".

## What the full version covers

1. **Hook:** the same invoice from a random Gmail address and from `accounts@examplebusiness.co.zw`. Which would you pay?
2. **What it is:** `info@examplebusiness.co.zw`, built up part by part.
3. **Five reasons:** trust, brand, control (the mailbox stays when staff leave), structure (sales@, accounts@, support@) and security (SPF, DKIM and DMARC records help emails reach the inbox and make them harder to fake).
4. **Works everywhere:** phone, Outlook, webmail and shared calendars.
5. **Forwarding Gmail to the new address, in three steps:**
   - On a computer: Settings › See all settings › **Forwarding and POP/IMAP**. On screen: forwarding can't be set up in the Gmail app.
   - **Add a forwarding address**, then open the confirmation link Gmail sends and confirm.
   - Choose **Forward a copy of incoming mail to** the new address, **keep Gmail's copy in the Inbox**, then **Save Changes**.
6. **A "we've moved" auto-reply** using Gmail's vacation responder.
7. **Update the address everywhere:** website, Google Business Profile, WhatsApp Business, Facebook page, invoices and email signature.
8. **What iContact does:** registers the .co.zw domain, sets up mailboxes and security records, moves old emails (Mail Business and Mail Pro) and sets up the forwarding.
9. **Plans:** Mail Basic $10, Mail Business $18 and Mail Pro $25, each per mailbox a month, with features as listed on the hosting page.

V1 covers the same ground in short.

## Rules check

- [x] **English only.**
- [x] **No invented claims:** no statistics, client names or results. Prices and plan features are copied from the website's hosting page.
- [x] **Invented, labelled screens:** Example Business, examplebusiness.co.zw and plumber.example2019@gmail.com. Every screen carries an **Example** label.
- [x] **No real company branding:** Gmail is named, because the steps use its menu names, but its settings are drawn as a plain window with no Google logo.
- [x] **AI use:** the voice is AI-generated (ElevenLabs, Nyasha's voice "Sim"), so switch on the platform's AI-content label when posting. The visuals are motion graphics drawn in code, not AI footage.

**Please check before posting:** the site's calculator shows the prices as a monthly total, so the video says "per mailbox a month". Confirm that's right. Migration is listed on Mail Business ("Migration from Gmail/old host") and Mail Pro ("Priority migration & support").

## Licence record

| Asset | Source | Licence |
|---|---|---|
| Music and sound effects | Composed and synthesised in code (`tools/psound.py`) | Original work, owned by you |
| Voiceover | ElevenLabs text-to-speech on your account ("iContact professional email explainer: voiceover (Nyasha)") | Commercial use under your ElevenLabs plan |
| Fonts (Poppins, Inter) | Google Fonts | SIL Open Font License |

## Rebuild

`python3 tools/build_email.py v1 --vo <folder> --speed 1.04` and `python3 tools/build_email.py v2 --vo <folder>`. The scenes are in `tools/email_pages.py`.
