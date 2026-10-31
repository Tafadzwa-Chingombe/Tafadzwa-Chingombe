"""The nine keyword-campaign ads (from the "Zimbabwe Digital Marketing & Web Dev Keyword Research" content calendar).
Running it writes each ad's ad.json (scripts, shots, on-screen content). [verify] = claim iContact must approve.
usage: python3 nyasha-ads/keyword-campaign/ads.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
H = lambda s: s  # headline html

ADS = {
 'e-website-price': dict(title='Website inoita marii? (how much is a website)', week=1,
   end=('c3-wide', 'Get your <span class="hl">fixed quote.</span>', 'Book a free call'),
   shots=[
    dict(page='hook', kind='photo', img='c4', min=3, kicker='Website inoita marii?', say='How',
         headline='How much does a <span class="hl">website</span> cost?',
         line="Website inoita marii? How much does a website cost in Zimbabwe? Here's the honest answer."),
    dict(page='drivers', kind='list', min=6, title='What changes the price', marker='num', say='four',
         items=[['Number of pages', 'pages'], ['EcoCash & Paynow payments', 'EcoCash'], ['An online shop', 'shop'], ['Who writes the content', 'content']],
         headline='It depends on <span class="hl">four things</span>',
         line="It depends on four things: how many pages you need, whether you take EcoCash or Paynow payments, if you want an online shop, and who writes the content."),
    dict(page='yearly', kind='list', min=4, title='Plan for yearly costs', marker='dot', say='yearly',
         items=[['.co.zw domain', 'domain'], ['Hosting', 'hosting'], ['Business email', 'email']],
         headline='Ask about these <span class="hl">up front</span>',
         line="Then plan for yearly costs: your .co.zw domain, hosting, and a business email."),
    dict(page='quote', kind='photo', img='c2', min=4, say='Tell',
         headline='No "inbox for price". <span class="hl">A fixed quote, in writing.</span>',   # [verify] fixed quotes
         line="At iContact, there's no inbox for price. Tell us what you need, and we'll send you a fixed quote."),
    dict(page='endcard', kind='endcard', min=4, line="Book your free call. Tatenda!"),
   ]),
 'f-overpaying': dict(title='5 signs you are overpaying for your website', week=1,
   end=('c3-wide', 'Get a free <span class="hl">second opinion.</span>', 'Book a free call'),
   shots=[
    dict(page='hook', kind='photo', img='c3', min=3, badge='5', at=0.2,
         headline='<span class="hl">5 signs</span> you\'re overpaying for your website',
         line="Mhoro! Five signs you're paying too much for your website."),
    dict(page='signs1', kind='list', min=6, title='Signs 1 to 3', marker='num',
         items=[["The domain isn't in your name", 'domain'], ['Surprise renewal fees', 'surprise'], ['No written quote', 'written']],
         headline='Overpaying? <span class="hl">Check these.</span>',
         line="One: the domain isn't in your name. Two: surprise renewal fees. Three: no written quote."),
    dict(page='signs2', kind='list', min=5, title='Signs 4 and 5', marker='num', start=4,
         items=[['You pay for every small update', 'pay'], ["It's slow on mobile data", 'slow']],
         headline='Overpaying? <span class="hl">Check these.</span>',
         line="Four: you pay for every small update. Five: it's slow on mobile data."),
    dict(page='promise', kind='photo', img='c2', min=4, say='domain',
         headline='Your domain. Your site. <span class="hl">Your price, in writing.</span>',   # [verify] fixed price
         line="With us, the domain is yours, the price is fixed, and it's all in writing."),
    dict(page='endcard', kind='endcard', min=4, line="Book a free call for a second opinion. Zvakanaka!"),
   ]),
 'g-facebook-not-website': dict(title='A Facebook page is not a website', week=1,
   end=('c3-wide', 'Let\'s get you <span class="hl">found.</span>', 'Book a free call'),
   shots=[
    dict(page='hook', kind='photo', img='c4', min=3, kicker='"Ndine page yeFacebook…"', say='Sound',
         headline='"I have a Facebook page. <span class="hl">I don\'t need a website."</span>',
         line="Ndine page yeFacebook, handidi website. Sound familiar?"),
    dict(page='versus', kind='compare', min=7, cols=['Facebook page', 'Your website'], say='rented',
         rows=[['You own it', 'yours', 'no', 'yes'], ['Ranks on Google for your services', 'Google', 'no', 'yes'],
               ['EcoCash & Visa checkout', 'EcoCash', 'no', 'yes'], ['No algorithm deciding who sees you', 'algorithm', 'no', 'yes']],
         headline='A page is <span class="hl">rented space</span>',
         line="A Facebook page is rented space. A website is yours: it shows up on Google, takes EcoCash and Visa payments, and no algorithm decides who sees it."),
    dict(page='both', kind='photo', img='c3-wide', min=4, say='Keep',
         headline='Keep the page. <span class="hl">Add the website.</span>',
         line="Keep your page for conversations, and send people to a website that closes the sale."),
    dict(page='endcard', kind='endcard', min=4, line="Book a free call. Zvakanaka!"),
   ]),
 'h-website-whatsapp': dict(title='Website + WhatsApp, working together', week=2,
   end=('c3-wide', 'Make them <span class="hl">work together.</span>', 'Book a free call'),
   shots=[
    dict(page='hook', kind='photo', img='c3', min=3, say='Should',
         headline='WhatsApp <span class="hl">or</span> a website?',
         line="Mhoro! Should you sell on WhatsApp, or on a website? The answer is both."),
    dict(page='path', kind='list', min=6, title='How they work together', marker='step',
         items=[['Customer finds you on Google', 'Google'], ['Sees your prices on your site', 'prices'],
                ['Taps "Order on WhatsApp"', 'WhatsApp'], ['Pays with EcoCash', 'EcoCash']],
         headline='One smooth path <span class="hl">to paid</span>',
         line="Customers find you on Google, see your prices on your website, tap to order on WhatsApp, and pay with EcoCash."),
    dict(page='shop', kind='phone', min=4, say='WhatsApp',
         css=('.shopimg{height:300px;margin:6px 22px 0;border-radius:22px;background:linear-gradient(135deg,#8a5a3b,#c99a6b)}'
              '.pname{margin:22px 26px 4px;font-weight:700;font-size:32px}.pmeta{margin:0 26px;font-size:22px;color:#5a6578}'
              '.wa{margin:26px 26px 0;height:86px;border-radius:22px;background:#2fbf5b;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:28px}'
              '.bubble{margin:26px 26px 0 90px;padding:18px 22px;border-radius:22px 22px 4px 22px;background:#dcf8c6;font-size:23px;line-height:1.3}'),
         screen=('<div class="status"><span>9:41</span><span>●●● 5G</span></div>'
                 '<div class="shopimg"></div><div class="pname">Teak coffee table</div><div class="pmeta">Moyo Interiors · In stock · Delivery in Harare</div>'
                 '<div class="wa" data-say="WhatsApp" data-anim="pop">Order on WhatsApp</div>'
                 '<div class="bubble" data-say="closes" data-anim="rise">Hi! I\'d like the teak table. Can I pay with EcoCash?</div>'),
         headline='Your site sells. <span class="hl">WhatsApp closes.</span>',
         line="Your website answers the questions. WhatsApp closes the deal."),
    dict(page='endcard', kind='endcard', min=4, line="Let's set it up. Book a free call. Tatenda!"),
   ]),
 'i-pay-facebook-ads': dict(title='How to pay for Facebook ads from Zimbabwe', week=3,
   end=('c2', 'Or let us <span class="hl">run your ads.</span>', 'Book a free call'),
   shots=[
    dict(page='hook', kind='photo', img='c4', min=3, kicker='Boost ndoibhadhara sei?', say='Card',
         headline='Card declined when you <span class="hl">boost a post?</span>',
         line="Boost ndoibhadhara sei? Card declined when you try to boost a post?"),
    dict(page='declined', kind='phone', min=4, say='often',
         css=('.ah{margin:10px 26px 0;font-weight:800;font-size:32px}.ar{margin:18px 26px 0;padding:22px;border-radius:20px;background:#fff;box-shadow:0 2px 10px rgba(0,0,0,.08);font-size:24px}'
              '.ar b{display:block;font-size:20px;color:#7a8598;font-weight:600;margin-bottom:6px}'
              '.fail{margin:26px 22px 0;padding:24px;border-radius:22px;background:#ffe3e0;border:3px solid var(--red);color:#8a1f15;font-weight:700;font-size:26px;line-height:1.3}'
              '.zig{margin:18px 22px 0;padding:20px 24px;border-radius:22px;background:#1b2433;color:#fff;font-weight:600;font-size:24px}'),
         screen=('<div class="status"><span>9:41</span><span>●●● 5G</span></div><div class="ah">Boost post</div>'
                 '<div class="ar"><b>Daily budget</b>US$5.00 · 7 days</div><div class="ar"><b>Payment method</b>Local card •••• 4021</div>'
                 '<div class="fail" data-say="declines" data-anim="pop">Payment failed. Your card was declined.</div>'
                 '<div class="zig" data-say="ZiG" data-anim="rise">ZiG is not a supported currency</div>'),
         headline='Meta often <span class="hl">declines local cards</span>',
         line="Meta often declines local cards, and it doesn't accept ZiG."),
    dict(page='fix', kind='list', min=6, title='The fix', marker='num',
         items=[['Get a USD prepaid Visa card', 'prepaid'], ['Add it in Billing & payments', 'Billing'],
                ['Load it before you boost', 'load'], ['Set a daily budget', 'daily']],
         headline='Pay in <span class="hl">USD</span>',
         line="The fix: get a USD prepaid Visa card from your bank, add it under Billing and payments, load it before you boost, and set a daily budget."),
    dict(page='endcard', kind='endcard', min=4, line="Or let us run your ads for you. Book a free call. Zvakanaka!"),   # [verify] ads management offered
   ]),
 'j-google-maps': dict(title='Get your business on Google Maps', week=3,
   end=('c3-wide', 'Let\'s get you <span class="hl">found.</span>', 'Book a free call'),
   shots=[
    dict(page='hook', kind='photo', img='c4', min=3, say='Can',
         headline='Is your business on <span class="hl">Google Maps?</span>',
         line="Mhoro! Can customers find your business on Google Maps? Here's how, in four steps."),
    dict(page='steps', kind='list', min=6, title='Four steps, free to set up', marker='num',
         items=[['Open Google Business Profile', 'Profile'], ['Add name, category & location', 'category'],
                ['Verify your business', 'verify'], ['Add photos, hours & phone', 'photos']],
         headline='It\'s <span class="hl">free</span>',
         line="Go to Google Business Profile, add your name, category and location, verify your business, then add photos, opening hours and your phone number."),
    dict(page='map', kind='phone', min=4, say='nearby',
         css=('.map{position:absolute;inset:0;background:#e9eef2;'
              'background-image:linear-gradient(90deg,transparent 46%,#fff 46%,#fff 54%,transparent 54%),linear-gradient(0deg,transparent 46%,#fff 46%,#fff 54%,transparent 54%),'
              'linear-gradient(35deg,transparent 48%,#f7d98a 48%,#f7d98a 52%,transparent 52%);background-size:180px 180px,220px 220px,100% 100%}'
              '.pin{position:absolute;left:50%;top:300px;width:84px;height:84px;margin-left:-42px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);background:#e5483b;box-shadow:0 8px 20px rgba(0,0,0,.3)}'
              '.pinwrap{position:absolute;left:0;right:0;top:0;height:420px}'
              '.place{position:absolute;left:18px;right:18px;bottom:22px;padding:24px;border-radius:26px;background:#fff;box-shadow:0 10px 30px rgba(0,0,0,.18)}'
              '.place b{display:block;font-size:30px}.place span{display:block;margin-top:6px;font-size:22px;color:#5a6578}'
              '.btns{display:flex;gap:12px;margin-top:16px}.btns div{flex:1;height:66px;border-radius:999px;display:grid;place-items:center;font-weight:700;font-size:22px}'
              '.btns .d{background:#1a73e8;color:#fff}.btns .c{background:#e8f0fe;color:#1a73e8}'),
         screen=('<div class="map"></div><div class="status" style="position:relative"><span>9:41</span><span>●●● 5G</span></div>'
                 '<div class="pinwrap" data-say="show" data-anim="pop"><div class="pin"></div></div>'
                 '<div class="place" data-say="directions" data-anim="rise"><b>Moyo Interiors</b><span>★★★★★ 4.9 · Furniture store · Open now</span>'
                 '<div class="btns"><div class="d">Directions</div><div class="c">Call</div></div></div>'),
         headline='Now they can <span class="hl">find you</span>',
         line="Now, when someone nearby searches, you show up, with directions and a call button."),
    dict(page='endcard', kind='endcard', min=4, line="Want it done for you? Book a free call."),
   ]),
 'k-potraz-ready': dict(title='Is your website POTRAZ-ready?', week=4,
   end=('c2', 'Get your website <span class="hl">checked.</span>', 'Book a free call'),
   shots=[
    dict(page='hook', kind='photo', img='c2', min=3, say='Is',
         headline='Is your website <span class="hl">POTRAZ-ready?</span>',
         line="Mhoro! Is your website ready for Zimbabwe's data protection rules?"),
    dict(page='collect', kind='list', min=6, title='Does your site collect…', marker='dot', say='licence',
         note='General information, not legal advice.',
         items=[['Names', 'names'], ['Phone numbers', 'phone'], ['Email addresses', 'emails']],
         headline='You may need a <span class="hl">data controller licence</span>',   # [verify] legal framing
         line="If your contact form or customer list collects names, phone numbers or emails, you may need a data controller licence from POTRAZ."),
    dict(page='start', kind='list', min=7, title='Start here', marker='tick', say='inspections',
         note='POTRAZ compliance inspections began 1 September 2026.',   # [verify]
         items=[['A privacy policy', 'privacy'], ['Consent on your forms', 'consent'], ['A secure, HTTPS site', 'secure'], ['Know where data is stored', 'stored']],
         headline='Inspections have <span class="hl">started</span>',
         line="POTRAZ began compliance inspections in September 2026. Start with a privacy policy, consent on your forms, a secure site, and knowing where your data is stored."),
    dict(page='endcard', kind='endcard', min=4, note='General information, not legal advice.',
         line="Book a free call, and check the legal details with a lawyer."),
   ]),
 'l-agency-freelancer-diy': dict(title='Agency vs freelancer vs DIY', week=4,
   end=('c3-wide', 'Ask us <span class="hl">anything.</span>', 'Book a free call'),
   shots=[
    dict(page='hook', kind='photo', img='c3', min=3, say='Agency',
         headline='Agency, freelancer <span class="hl">or DIY?</span>',
         line="Mhoro! Agency, freelancer, or build it yourself?"),
    dict(page='options', kind='cards', min=7, us=2, say='DIY',
         cards=[['DIY', 'Cheapest, but it costs your time.', 'DIY'], ['Freelancer', 'Can be great. Get a contract.', 'freelancer'],
                ['Agency', 'A team, plus aftercare.', 'agency']],
         headline='Each has <span class="hl">its place</span>',
         line="DIY is cheapest, but it costs your time. A freelancer can be great, just get a contract. An agency gives you a team and aftercare."),
    dict(page='ask', kind='list', min=6, title='Whoever you choose, ask:', marker='q',
         items=[['Who owns the domain?', 'owns'], ['Is the price in writing?', 'writing'], ['Who fixes it after launch?', 'fixes']],
         headline='Three questions <span class="hl">to ask</span>',
         line="Whoever you choose, ask three things: who owns the domain, is the price in writing, and who fixes it after launch?"),
    dict(page='endcard', kind='endcard', min=4, line="Ask us anything. Book a free call. Tatenda!"),
   ]),
 'm-free-audit': dict(title='Free website audit', week=4,
   end=('c3-wide', '<span class="hl">Free</span> website audit.', 'Get my free audit'),   # [verify] free audit offer
   shots=[
    dict(page='hook', kind='photo', img='c4', min=3, say='Is',
         headline='Is your website <span class="hl">losing you customers?</span>',
         line="Mhoro! Is your website quietly losing you customers?"),
    dict(page='check', kind='list', min=6, title="We'll check", marker='tick', say='check',
         items=[['Speed on mobile data', 'speed'], ['Your Google visibility', 'Google'], ['Contact & WhatsApp buttons', 'contact'], ['Security', 'security']],
         headline='A <span class="hl">free</span> website audit',
         line="We'll check your speed on mobile data, your Google visibility, your contact buttons, and your security."),
    dict(page='offer', kind='photo', img='c2', min=4, say='free',
         headline='No obligation. <span class="hl">Plain English.</span>',
         line="It's free, there's no obligation, and you get the results in plain English."),
    dict(page='endcard', kind='endcard', min=4, line="Tap to get your free audit. Zvakanaka!"),
   ]),
}

if __name__ == '__main__':
    for slug, ad in ADS.items():
        folder = os.path.join(HERE, slug)
        os.makedirs(folder, exist_ok=True)
        spec = {'title': ad['title'], 'week': ad['week'], 'endcard': ad['end'], 'shots': ad['shots'], 'sfx': [], 'music_volume': 0.3}
        json.dump(spec, open(os.path.join(folder, 'ad.json'), 'w'), indent=1, ensure_ascii=False)
        print(slug)
