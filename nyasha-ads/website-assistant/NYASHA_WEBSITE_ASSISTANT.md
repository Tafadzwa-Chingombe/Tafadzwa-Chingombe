# Add Nyasha to the iContact website as the on-screen AI assistant

This file is a set of instructions for adding Nyasha, iContact Africa Solutions' AI assistant, to every page of the website. Hand it to a coding assistant (such as Claude Code) inside the website's repository, or follow the steps yourself.

When it's done, every page shows a small Nyasha button in the bottom-right corner. Visitors click it to talk to her by voice or by typing. She answers from iContact's website and price list, and books a free 30-minute call with Tafadzwa or passes the visitor to him.

---

## What's already set up (in ElevenLabs)

Nothing here needs changing. It's listed so whoever adds the code knows what to expect.

| Setting | Value |
|---|---|
| Agent | "iContact AI Assistant (Inbound + Outbound)" |
| Agent ID | `agent_0101m6ntdac3e89s6m1wz7a49hgr` |
| Voice | Nyasha ("Sim – Warm South African English") |
| Greeting | "Hi! I'm Nyasha, iContact Africa Solutions' AI assistant. How can I help you today?" |
| Avatar | Nyasha's photo (`nyasha-avatar.jpg`, beside this file) |
| Button text | "Talk to Nyasha" / "Hi, I'm Nyasha, iContact's AI assistant. Ask me anything." |
| Colours | Brand blue `#2E5795` buttons, green `#ABCF47` focus |
| Allowed websites | `tafadzwa-chingombe.github.io`, `icontactafricasolutions.org` |
| Voice and text | Both. Visitors can call her or type. |
| Privacy notice | Shown before the first chat: AI assistant, recorded, kept 90 days, don't share card numbers or passwords |

**The widget only starts on the allowed websites above.** The agent's security settings block every other address, including `localhost` (see "Testing before you publish" below).

---

## Steps

### 1. Add Nyasha's picture to the website

Copy `nyasha-avatar.jpg` (512 × 512, in the same folder as this file) into the website repository as:

```
assets/img/nyasha-avatar.jpg
```

If you only have this Markdown file, download the picture from:

```
https://raw.githubusercontent.com/tafadzwa-chingombe/Tafadzwa-Chingombe/df9b7cb6df2d358c1776ef1c06953fba891b37e4/nyasha-ads/website-assistant/nyasha-avatar.jpg
```

The widget already loads Nyasha's picture from ElevenLabs' settings. A copy in the website lets the site use its own picture (step 3) and keeps it working if the link above ever changes.

### 2. Add the widget to every page

Paste this just before the closing `</body>` tag on **every** HTML page: home, services, pricing, domains, hosting, about, contact, work and any blog pages.

```html
<!-- Nyasha, iContact's AI assistant (ElevenLabs) -->
<elevenlabs-convai agent-id="agent_0101m6ntdac3e89s6m1wz7a49hgr"></elevenlabs-convai>
<script src="https://unpkg.com/@elevenlabs/convai-widget-embed" async type="text/javascript"></script>
```

- If the site has a shared footer or layout file (an include, partial or template), add it there once instead.
- Add the `<script>` line **once per page** only. Two copies on the same page break the widget.
- The widget floats in the bottom-right corner by itself. It needs no CSS and doesn't move anything on the page.

### 3. Optional: use the website's own copy of the picture

To load Nyasha's picture from the website instead of from ElevenLabs, add the `avatar-image-url` attribute:

```html
<elevenlabs-convai
  agent-id="agent_0101m6ntdac3e89s6m1wz7a49hgr"
  avatar-image-url="https://tafadzwa-chingombe.github.io/iContact-Africa-Solutions/assets/img/nyasha-avatar.jpg">
</elevenlabs-convai>
```

Use the full `https://` address of the picture on the live site, not a relative path.

### 4. Keep the WhatsApp button clear of Nyasha

If the site already has a floating WhatsApp button in the bottom-right corner, the two will overlap. Fix it one of these ways:

- **Move the WhatsApp button to the bottom-left** (simplest). For example:
  ```css
  .whatsapp-float { right: auto; left: 20px; }
  ```
  Replace `.whatsapp-float` with whatever class the site's WhatsApp button uses.
- **Or move Nyasha** by changing the widget placement to bottom-left in ElevenLabs: Agent → Widget → Placement.

### 5. Say she's AI on the page (recommended)

The widget already tells visitors she's an AI assistant before the first chat. For extra clarity, add a short line to the footer of every page:

```html
<p class="ai-note">Nyasha is iContact's AI assistant. Prefer a person? Call or WhatsApp +263 71 857 4277 · +263 77 419 2027.</p>
```

---

## Testing before you publish

1. **Locally:** the widget won't start on `localhost`, because the agent only allows the two live domains. To test locally, temporarily add `localhost` in ElevenLabs (Agent → Security → Allowlist), then remove it when you're done.
2. **On the live site** (after pushing to GitHub Pages):
   - The round Nyasha button appears bottom-right on every page.
   - Clicking it shows the privacy notice, then her greeting.
   - Typing "How much is a website?" gets a starting price (from $300, plus a maintenance plan from $100 a month).
   - Asking for a person offers a call with Tafadzwa or gives the phone numbers.
   - On a phone, it opens full screen and closes cleanly.
3. **In ElevenLabs:** under Agent → Conversations you can see each website chat, its summary and the lead details collected (name, number, service needed).

---

## If something doesn't work

| What you see | Likely cause and fix |
|---|---|
| No button appears | The `<script>` line is missing or blocked. Check the browser console for errors and confirm the script loads from `unpkg.com`. |
| The button appears but won't connect | The page's address isn't in the allowlist. Add the exact domain in ElevenLabs (Agent → Security). |
| Two buttons, or it opens twice | The `<script>` line is on the page twice. Keep one. |
| No microphone | The browser blocked it. Visitors can allow it in the address bar, or just type. |
| The old picture or orb shows | Hard-refresh the page (Ctrl + Shift + R). The widget caches its settings for a short time. |

---

## Brief for a coding assistant

Paste this into Claude Code (or similar) inside the website repository:

> Add the ElevenLabs Conversational AI widget for our assistant Nyasha to every page of this site, following `NYASHA_WEBSITE_ASSISTANT.md`.
> 1. Save `nyasha-avatar.jpg` to `assets/img/nyasha-avatar.jpg`.
> 2. Add `<elevenlabs-convai agent-id="agent_0101m6ntdac3e89s6m1wz7a49hgr" avatar-image-url="https://tafadzwa-chingombe.github.io/iContact-Africa-Solutions/assets/img/nyasha-avatar.jpg"></elevenlabs-convai>` and the script `https://unpkg.com/@elevenlabs/convai-widget-embed` (async) just before `</body>` on every HTML page, once per page. Use the shared footer or layout if there is one.
> 3. If there is a floating WhatsApp button in the bottom-right, move it to the bottom-left so the two don't overlap.
> 4. Add the footer line: "Nyasha is iContact's AI assistant. Prefer a person? Call or WhatsApp +263 71 857 4277 · +263 77 419 2027."
> 5. Don't change any other content or styling. List every file you changed.
