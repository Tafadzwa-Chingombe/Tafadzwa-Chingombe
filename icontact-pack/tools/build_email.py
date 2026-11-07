"""Build the professional email explainer: V1 (about 60 s) and V2 (full, about 3 min), each in 16:9, 9:16 and 4:5.
Uses build_aiv's engine (voice fitting, Rubber Band timing, captions, sound, three frame sizes).

usage: python3 tools/build_email.py v1|v2 --vo <dir> [--speed <x>]
Output: icontact-pack/email/<version>-16x9, -9x16, -4x5
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_aiv as B
import email_pages as E

OUT = os.path.join(B.PACK, 'email')
W = [('whoosh', -0.2, 0.22)]


def V1():
    return dict(speed=1.0, tail=0.15, end_tail=1.8, music=0.18, shots=[
        dict(page='hook', line='Would you pay an invoice from a random Gmail address? Many clients wouldn\'t.',
             html=lambda T: E.hook('Would you pay <span class="ac">this</span> invoice?', T), sfx=[('pop', 'b', 0.25)], cues={'b': 0.45}),
        dict(page='address', line='A professional email puts your business name on every message, like info@yourbusiness.co.zw.',
             html=lambda T: E.address(T), sfx=W),
        dict(page='trust', line='It builds trust, so clients act on your quotes and invoices.',
             html=lambda T: E.trust(T, 'Trust', 'Clients <span class="ac">trust it</span>', ''), sfx=W),
        dict(page='own', line="It's yours. When staff leave, the mailbox stays with the business.",
             html=lambda T: E.own(T, 'Control'), sfx=W),
        dict(page='aliases', line='Use sales, accounts and support addresses, so every enquiry reaches the right person.',
             html=lambda T: E.aliases(T, 'Structure'), sfx=W),
        dict(page='secure', line='Set up properly, your emails reach the inbox, and are harder for scammers to fake.',
             html=lambda T: E.secure(T, 'Security'), sfx=W),
        dict(page='forward', line='Clients still using your old Gmail? In Gmail settings, forward a copy of every email to your new address.',
             html=lambda T: E.step3(T, 'Keep your Gmail clients', 'Forward Gmail to <span class="ac">your new address</span>', 'Settings › Forwarding and POP/IMAP.'),
             sfx=W + [('ding', 'ok', 0.3)], cues={'ok': 0.55}),
        dict(page='autoreply', line='Then add an auto-reply with your new address, so nobody slips through.',
             html=lambda T: E.autoreply(T), sfx=W),
        dict(page='pricing', min=6.2, line='Professional email starts at $10 per mailbox a month.',
             html=lambda T: E.plans([0.3, 0.12 + T * 0.55, 0.12 + T * 0.8], 'Professional email from <span class="ac">$10</span>'),
             sfx=W + [('pop', 'card0', 0.3), ('pop', 'card1', 0.3), ('pop', 'card2', 0.3)], cues={'card1': 0.55, 'card2': 0.8}),
        dict(page='service', line='iContact Africa Solutions sets up your domain, your mailboxes and the forwarding for you.',
             html=lambda T: E.service(T, 'Done for you'), sfx=W),
        dict(page='endcard', line="WhatsApp the word EMAIL to iContact, and let's set yours up.", html=lambda T: E.end(),
             sfx=W + [('shimmer', 0.8, 0.25)]),
    ])


def V2():
    return dict(speed=1.0, tail=0.3, end_tail=2.2, music=0.16, shots=[
        dict(page='hook', line='Quick question. Would you pay an invoice that came from a random Gmail address? Most clients would stop and think twice. And that moment of doubt can cost you the job.',
             html=lambda T: E.hook('Would you pay <span class="ac">this</span> invoice?', T), sfx=[('pop', 'b', 0.25)], cues={'b': 0.45}),
        dict(page='address', line="A professional email address uses your own business name. Instead of a free address, it's info@yourbusiness.co.zw.",
             html=lambda T: E.address(T), sfx=W),
        dict(page='trust', line="Reason one is trust. A business address tells clients you're established, so your quotes, invoices and payment details feel safe to act on.",
             html=lambda T: E.trust(T), sfx=W),
        dict(page='brand', line='Reason two is your brand. Every email you send repeats your name, and points people back to your website.',
             html=lambda T: E.brand(T), sfx=W),
        dict(page='own', line='Reason three is control. The addresses belong to your business. When someone leaves, their mailbox and client history stay with you, not in a personal Gmail account.',
             html=lambda T: E.own(T), sfx=W),
        dict(page='aliases', line='Reason four is structure. Use sales, accounts and support addresses, so every enquiry reaches the right person and nothing gets lost.',
             html=lambda T: E.aliases(T), sfx=W),
        dict(page='secure', line='Reason five is security. With the right records set up on your domain, your emails are more likely to reach the inbox, and harder for scammers to fake.',
             html=lambda T: E.secure(T), sfx=W),
        dict(page='devices', line='And it works the way you do, on your phone, in Outlook and in any browser.',
             html=lambda T: E.devices(T), sfx=W),
        dict(page='bridge', line="But what about clients who still have your old Gmail address? You don't have to lose a single one. Here's how to forward it.",
             html=lambda T: E.bridge(T), sfx=W),
        dict(page='step1', line='On a computer, open Gmail and go to Settings, then See all settings. Open the tab called Forwarding and POP/IMAP.',
             html=lambda T: E.step1(T), sfx=W),
        dict(page='step2', line='Click Add a forwarding address, and type your new business email. Gmail sends a confirmation link to that address. Open it, and confirm.',
             html=lambda T: E.step2(T), sfx=W + [('pop', 'ok', 0.3)], cues={'ok': 0.78}),
        dict(page='step3', line="Back in Gmail, choose Forward a copy of incoming mail to your new address, keep Gmail's copy in the inbox, and save. Now every email sent to your Gmail reaches your business inbox too.",
             html=lambda T: E.step3(T), sfx=W + [('ding', 'ok', 0.3)], cues={'ok': 0.55}),
        dict(page='autoreply', line="Then switch on Gmail's vacation responder with a short note: we've moved, please use our new address. Clients update their contacts, and nobody slips through the cracks.",
             html=lambda T: E.autoreply(T), sfx=W),
        dict(page='everywhere', line='Finally, put your new address everywhere: your website, Google Business Profile, WhatsApp Business, your Facebook page, invoices and email signature.',
             html=lambda T: E.everywhere(T), sfx=W),
        dict(page='service', line='Or let us do it for you. iContact Africa Solutions registers your .co.zw domain, sets up your mailboxes and security records, can move your old emails across, and sets up the forwarding with you.',
             html=lambda T: E.service(T), sfx=W),
        dict(page='pricing', min=13.5, line='Professional email starts at $10 per mailbox a month. Mail Business, at $18, adds shared calendars, Gmail migration and daily backups. Mail Pro, at $25, adds archiving and two-factor login.',
             html=lambda T: E.plans([0.12 + T * 0.04, 0.12 + T * 0.33, 0.12 + T * 0.66], 'Pick the plan <span class="ac">that fits</span>'),
             sfx=W + [('pop', 'card0', 0.3), ('pop', 'card1', 0.3), ('pop', 'card2', 0.3)], cues={'card0': 0.04, 'card1': 0.33, 'card2': 0.66}),
        dict(page='endcard', line="Make every email look like it comes from a real business. WhatsApp the word EMAIL to iContact Africa Solutions, and let's set yours up.",
             html=lambda T: E.end(), sfx=W + [('shimmer', 0.8, 0.25)]),
    ])


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0] not in ('v1', 'v2') or '--vo' not in a: raise SystemExit(__doc__)
    v = a[0]
    B.build(v, a[a.index('--vo') + 1], out=OUT, spec={'v1': V1, 'v2': V2}[v](),
            speed_override=float(a[a.index('--speed') + 1]) if '--speed' in a else None)
