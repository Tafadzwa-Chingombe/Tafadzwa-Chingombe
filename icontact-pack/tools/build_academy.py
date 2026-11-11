"""Build the iContact Academy ads, each in 16:9, 9:16 and 4:5, in Nyasha's voice:
  full     the explainer (about 2.5 min)     ad60   the 60 s ad      teaser  the 20 s teaser
  story    Tendai's story (invented student, about 2.5 min)          story60 its 60 s cut
usage: python3 tools/build_academy.py <film> --vo <dir> [--speed <x>]
Output: icontact-pack/academy/<film>-16x9, -9x16, -4x5
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_aiv as B
import academy_pages as P

OUT = os.path.join(B.PACK, 'academy')
W = [('whoosh', -0.2, 0.22)]


def shot(page, line, html, sfx=None, **kw):
    return dict(page=page, line=line, html=html, sfx=W + (sfx or []), **kw)


def END(line, tag=None):
    return shot('endcard', line, (lambda T: P.end(tag)) if tag else (lambda T: P.end()), [('shimmer', 0.8, 0.25)])


def full():
    return dict(speed=1.0, tail=0.3, end_tail=2.2, music=0.16, shots=[
        dict(page='hook', line='What if you could learn the exact skills a web agency uses to bring in customers, on your phone, at your own pace?', html=lambda T: P.hook(T), sfx=[('pop', 'p', 0.25)], cues={'p': 0.1}),
        shot('intro', 'Meet iContact Academy: self-paced online courses in digital marketing and website development, from the team that builds websites and runs campaigns for Zimbabwean businesses.', lambda T: P.intro(T)),
        shot('realwork', "These aren't theory courses. They're built from real client work: the same skills we use every day on websites, search, social media and ads.", lambda T: P.realwork(T)),
        shot('tracks', 'Choose your track. Digital marketing teaches you how to get a business found and chosen online. Website development teaches you how to build sites that bring in enquiries.', lambda T: P.tracks(T)),
        shot('selfpaced', 'Every course is self-paced. Start any time, learn when it suits you, and pause, rewatch or pick up exactly where you left off.', lambda T: P.selfpaced(T)),
        shot('devices', 'The short video lessons and notes work on your phone, tablet or laptop, and your progress is saved as you go.', lambda T: P.devices(T)),
        shot('projects', "And you don't just watch. Each track ends with a realistic project.", lambda T: P.project_intro(T)),
        shot('sitebuild', 'In website development, you build and publish a working website for a small business, step by step.', lambda T: P.site_build(T), [('ding', 'live', 0.3)], cues={'live': 0.8}),
        shot('marketing', 'In digital marketing, you plan a real campaign and set up a Google Business Profile for a business.', lambda T: P.marketing(T)),
        shot('zimbabwe', 'The examples, tools and payment options are made for Zimbabwe, from EcoCash to local search.', lambda T: P.zimbabwe(T)),
        shot('value', "Value for money is simple. You make one payment per course. There's no subscription and no deadline, and you keep access to your course, including every update to its lessons.", lambda T: P.value(T)),
        shot('payment', 'Paying is easy, too. Pay by EcoCash, Paynow or bank transfer.', lambda T: P.payment(T), [('pop', 't0', 0.25), ('pop', 't1', 0.25), ('pop', 't2', 0.25)], cues={'t0': 0.2, 't1': 0.38, 't2': 0.56}),
        shot('steps', 'Choose a course, request your place and pay. Once we confirm your payment, usually the same day, we send your login by WhatsApp or email.', lambda T: P.steps(T)),
        shot('beginner', 'New to all of this? Beginner courses assume no experience beyond using a phone or a computer.', lambda T: P.beginner(T)),
        shot('portal', 'Already an iContact client? Your courses appear in the same Client Portal login you already use.', lambda T: P.portal(T)),
        END('Learn the skills that bring in customers. WhatsApp the word ACADEMY to iContact Africa Solutions, and start today.'),
    ])


def ad60():
    return dict(speed=1.0, tail=0.2, end_tail=1.8, music=0.17, shots=[
        dict(page='hook', line='Want to learn the skills that bring in customers, at your own pace?', html=lambda T: P.hook(T), sfx=[('pop', 'p', 0.25)], cues={'p': 0.1}),
        shot('intro', 'iContact Academy has new self-paced courses in digital marketing and website development.', lambda T: P.intro(T)),
        shot('selfpaced', "They're built from real client work, with short lessons that work on your phone.", lambda T: P.selfpaced(T, 'Real skills', 'Built from <span class="ac">real client work</span>', 'Short lessons on your phone.')),
        shot('sitebuild', 'Each track ends with a realistic project: publish a working business website, or plan a real campaign.', lambda T: P.site_build(T, 'Realistic projects', 'Publish a real website, <span class="ac">or plan a campaign</span>', ''), [('ding', 'live', 0.3)], cues={'live': 0.8}),
        shot('value', 'Pay once per course and keep access, including updates. No subscription, no deadlines.', lambda T: P.value(T)),
        shot('payment', 'Pay by EcoCash, Paynow or bank transfer, and get your login, usually the same day.', lambda T: P.payment(T, 'Easy to pay', 'EcoCash, Paynow <span class="ac">or bank transfer</span>', 'Login usually the same day.'),
             [('pop', 't0', 0.25), ('pop', 't1', 0.25), ('pop', 't2', 0.25)], cues={'t0': 0.2, 't1': 0.38, 't2': 0.56}),
        END('WhatsApp the word ACADEMY to iContact, and start learning.'),
    ])


def teaser():
    return dict(speed=1.0, tail=0.15, end_tail=1.6, music=0.18, shots=[
        dict(page='hook', line='Learn digital marketing or website development, at your own pace.', html=lambda T: P.hook(T, 'Learn it <span class="ac">at your own pace</span>'), sfx=[('pop', 'p', 0.25)], cues={'p': 0.1}),
        shot('recap', 'Real projects. One payment. EcoCash, Paynow or bank transfer.', lambda T: P.recap(T, ('Real projects', 'One payment per course', 'EcoCash, Paynow or bank transfer'), 'iContact Academy', 'New <span class="ac">online courses</span>')),
        END('WhatsApp the word ACADEMY to iContact.'),
    ])


def story():
    return dict(speed=1.0, tail=0.35, end_tail=2.4, music=0.16, shots=[
        shot('who', 'This is Tendai. She bakes the best cakes in her neighbourhood, and every order happens on WhatsApp.', lambda T: P.who(T)),
        shot('problem', "She wants new customers to find her online. But hiring a web designer isn't in the budget yet, and she has no idea where to start.", lambda T: P.problem(T)),
        shot('finds', 'One evening, she finds iContact Academy: self-paced courses in website development and digital marketing.', lambda T: P.finds(T)),
        shot('coursepage', 'She picks the website development course. The page shows every lesson and the price: one payment for the whole course.', lambda T: P.coursepage(T)),
        shot('paid', 'She pays with EcoCash, and that same day, her login arrives on WhatsApp.', lambda T: P.paid(T), [('pop', 'msg', 0.3)], cues={'msg': 0.45}),
        shot('bus', 'Her first lesson happens on her phone, on the way home. Short videos, clear notes, and her progress saved as she goes.', lambda T: P.bus(T)),
        shot('pace', 'Some nights she does three lessons. Some weeks, none. There are no deadlines, so the course simply waits for her.', lambda T: P.pace(T)),
        shot('rewatch', "When something doesn't click, she rewatches it, as many times as she needs.", lambda T: P.rewatch(T)),
        shot('brief', 'Then comes the project: build a real website for a small business. She chooses her own.', lambda T: P.brief(T)),
        shot('shaping', "Step by step, her bakery's website takes shape: her cakes, her prices, her photos, and a button to order on WhatsApp.", lambda T: P.shaping(T)),
        shot('live', "And then, it's live. A real website, that she built herself.", lambda T: P.live(T), [('ding', 'live', 0.35), ('shimmer', 'live', 0.2)], cues={'live': 0.15}),
        shot('nextcourse', 'Next, she takes the digital marketing course. She plans her first campaign, and sets up her Google Business Profile, so people nearby can find her.', lambda T: P.nextcourse(T)),
        shot('account', 'Her courses stay in her account, with every update, so she can come back whenever she needs.', lambda T: P.account(T)),
        shot('honest', "Tendai is invented for this story. But the courses are real, and so is the project you'll build.", lambda T: P.honest(T)),
        shot('recap', 'Self-paced lessons. A realistic project. One payment per course, by EcoCash, Paynow or bank transfer.', lambda T: P.recap(T)),
        END('WhatsApp the word ACADEMY to iContact Africa Solutions, and start your own story.', 'Your skills. Your pace. <span>Your own story.</span>'),
    ])


def story60():
    return dict(speed=1.0, tail=0.25, end_tail=2.0, music=0.17, shots=[
        shot('who', 'Tendai bakes the best cakes in her neighbourhood. She wanted new customers to find her online, so she found iContact Academy.', lambda T: P.who(T)),
        shot('paid', 'She chose website development, paid once with EcoCash, and got her login on WhatsApp the same day.', lambda T: P.paid(T), [('pop', 'msg', 0.3)], cues={'msg': 0.45}),
        shot('bus', 'She learned on her phone, at her own pace: pause, rewatch, and pick up where she left off.', lambda T: P.bus(T)),
        shot('live', 'Then came the project: a real website for a small business. She built her own, and published it.', lambda T: P.site_build(T, 'Example story', 'She built it. <span class="ac">And published it.</span>', '', live_at=0.85, name="Tendai's Bakery"), [('ding', 'live', 0.35)], cues={'live': 0.85}),
        shot('honest', 'Tendai is invented. The courses, and the project, are real.', lambda T: P.honest(T)),
        END('Pay once per course, by EcoCash, Paynow or bank transfer. WhatsApp the word ACADEMY to iContact, and start your own story.', 'Your skills. Your pace. <span>Your own story.</span>'),
    ])


FILMS = {'full': full, 'ad60': ad60, 'teaser': teaser, 'story': story, 'story60': story60}

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0] not in FILMS or '--vo' not in a: raise SystemExit(__doc__)
    B.build(a[0], a[a.index('--vo') + 1], out=OUT, spec=FILMS[a[0]](),
            speed_override=float(a[a.index('--speed') + 1]) if '--speed' in a else None)
