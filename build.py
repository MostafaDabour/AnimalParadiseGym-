import re
import json, os
OUT = "site"
SITE = "https://animalparadisegyms.com"
LIVE = "https://animalparadisegyms.com/wp-content"
ABC = "https://onlinejoin.abcfitness.com/signup/plan?club=31857&amp;planId="
PLAN_IDS = dict(silver="13656dbde8fd436bb689e32c16b63056", gold="9ebe7a5348c7495fae488912433d9c65",
                premium="81293d61d2af47cebc834aec823432e4", platinum="563c3fc6a6954a9ca216624c35a4378a",
                diamond="8c6f6ea07fe0440cb83468ca56c58cdb")
ARROW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'
MAPS = "https://www.google.com/maps/search/?api=1&amp;query=Animal%20Paradise%20Gyms%2C%20Cumberland%20Mall%2C%203849%20S%20Delsea%20Dr%2C%20Vineland%2C%20NJ%2008360"

NAV = [("the-gym.html", "The Gym"), ("memberships.html", "Memberships"),
       ("personal-training.html", "Training"), ("lioness-den.html", "Lioness Den"),
       ("animal-cafe.html", "Cafe"), ("animal-supps.html", "Supps"), ("events.html", "Events"), ("blog.html", "Blog"), ("about.html", "About"), ("visit.html", "Visit")]

GYM_ID = {"@id": SITE + "/#gym"}

def ph(src, alt, cls="ph", extra=""):
    s = src if src.startswith("http") or src.startswith("img/") else LIVE + src
    return f'<div class="{cls}"{extra}><img loading="lazy" src="{s}" alt="{alt}" onerror="this.remove()"></div>'

def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, indent=1, ensure_ascii=False) + "</script>"

def crumbs_ld(name, slug):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": f"{SITE}/{slug}/"}]}

def head(title, desc, slug, schemas, full):
    canon = SITE + ("/" if slug == "" else f"/{slug}/")
    meta = f'''<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Animal Paradise Gyms">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/img/photos/vineland-gym-hero-floor.webp">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Unbounded:wght@500;700;800;900&family=Michroma&family=Figtree:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="css/site.css">
''' + "\n".join(ld(s) for s in schemas)
    if full:
        return f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{meta}\n</head>\n<body>\n'
    return meta + "\n"

def nav(active):
    items = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a></li>' for h, t in NAV)
    return f'''<div class="announce"><span class="ann-long">Open every day 4AM to 12AM · Book a free tour</span><span class="ann-short">Open daily 4AM to 12AM · Vineland, NJ</span></div>
<header class="nav" id="nav">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="Animal Paradise Gyms home"><img src="img/logo.png" alt="Animal Paradise Gyms" width="157" height="46"></a>
    <ul class="links" id="links">{items}</ul>
    <button class="menu-btn" id="menu-btn" aria-expanded="false" aria-controls="links">Menu</button>
    <a class="btn btn-gold" href="visit.html#tour">Free Tour</a>
  </div>
</header>
<main>
'''

def closer(h1="Come see", h2="it for yourself."):
    return f'''<section class="band closer" aria-label="Book a tour">
  <div class="wrap" style="display:grid;gap:28px;justify-items:center">
    <span class="eyebrow" id="closer-eyebrow">Open tonight until midnight</span>
    <h2>{h1}<br><span class="gold">{h2}</span></h2>
    <div class="hero-cta" style="margin:0">
      <a class="btn btn-gold" href="visit.html#tour">Book a free tour {ARROW}</a>
      <a class="btn btn-glass" href="memberships.html">See memberships</a>
    </div>
  </div>
</section>
'''

def footer(full):
    links = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV + [("gallery.html", "Gallery"), ("faq.html", "FAQ"), ("parent-consent-form.html", "Parent consent waiver")])
    end = "</body>\n</html>\n" if full else ""
    return f'''</main>
<footer>
  <div class="wrap">
    <div class="foot">
      <div style="display:grid;gap:16px;align-content:start">
        <img src="img/logo.png" alt="Animal Paradise Gyms" width="177" height="52">
        <p style="max-width:36ch">The full-service gym inside Cumberland Mall in Vineland, NJ. Open every day, 4AM to 12AM.</p>
      </div>
      <div><h4>Explore</h4><ul>{links}</ul></div>
      <div><h4>Visit</h4><ul><li>3849 S Delsea Dr, Suite E000</li><li>Cumberland Mall, Vineland, NJ 08360</li><li>(856) 839-4536</li><li>Info@AnimalParadiseGyms.com</li><li><a href="visit.html">Hours and directions</a></li></ul></div>
      <div><h4>Follow</h4><ul>
        <li><a target="_blank" rel="noopener" href="https://animalcafe.net/">Animal Cafe site</a></li>
        <li><a target="_blank" rel="noopener" href="https://animalsupps.co/">Shop Animal Supps</a></li>
        <li><a target="_blank" rel="noopener" href="https://www.instagram.com/animalparadisegyms">Instagram</a></li>
        <li><a target="_blank" rel="noopener" href="https://www.facebook.com/profile.php?id=61560036899811">Facebook</a></li>
        <li><a target="_blank" rel="noopener" href="https://apps.apple.com/us/app/animal-paradise-gym/id6745569852">App Store</a></li>
        <li><a target="_blank" rel="noopener" href="https://play.google.com/store/apps/details?id=com.trainerize.animalparadisegyms">Google Play</a></li>
        </ul></div>
    </div>
    <div class="legal"><span>© 2026 Animal Paradise Gyms · Vineland, NJ</span><span>Website and marketing by Leads Magnets</span></div>
  </div>
</footer>
<div class="mbar"><a class="btn btn-glass" href="visit.html">Call or visit</a><a class="btn btn-gold" href="visit.html#tour">Free tour</a></div>
<script src="js/site.js"></script>
{end}'''

def page_hero(eyebrow, h1, lede, crumb, ctas=True, bg=None):
    c = f'<ol class="crumbs"><li><a href="index.html">Home</a></li><li aria-current="page">{crumb}</li></ol>'
    cta = f'<div class="hero-cta"><a class="btn btn-gold" href="visit.html#tour">Book a free tour {ARROW}</a><a class="btn btn-glass" href="memberships.html">See memberships</a></div>' if ctas else ""
    bgh = f'<div class="ph hero-bg"><img src="img/photos/vineland-gym-{bg}.webp" alt="" fetchpriority="high"></div>' if bg else ""
    return f'''<section class="page-hero{' has-bg' if bg else ''}">{bgh}
  <div class="wrap">
    <nav aria-label="Breadcrumb">{c}</nav>
    <p class="eyebrow" style="margin-top:28px">{eyebrow}</p>
    <h1>{h1}</h1>
    <p class="lede" style="color:rgba(242,236,223,.82)">{lede}</p>
    {cta}
  </div>
</section>
'''

def head_block(eyebrow, h2, lede="", center=False, hid=None):
    i = f' id="{hid}"' if hid else ""
    l = f'<p class="lede">{lede}</p>' if lede else ""
    return f'<div class="head{" center" if center else ""} rv"><span class="eyebrow">{eyebrow}</span><h2{i}>{h2}</h2>{l}</div>'

def faq_html(qs, open_first=True):
    out = []
    for i, (q, a) in enumerate(qs):
        out.append(f'<details{" open" if (i == 0 and open_first) else ""}><summary>{q}</summary><p>{a}</p></details>')
    return "".join(out)

def faq_ld(qs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qs]}

# ---------- shared data ----------
COACHES = [
    dict(slug="chuck", name="Chuck", role="Contest prep coach", img="img/coach-chuck.webp",
         bio="Two decades of certification and a shelf of NPC overall titles. Chuck has been on both sides of a prep, so he knows what the last eight weeks actually feel like.",
         alt="Chuck, contest prep coach at Animal Paradise Gyms in Vineland NJ"),
    dict(slug="hakim", name="Hakim", role="NASM certified trainer", img="img/coach-hakim.webp",
         bio="An exercise science degree, three years on the floor and a clinical background from Inspira. A great fit for first-timers.",
         alt="Hakim, NASM certified personal trainer at Animal Paradise Gyms"),
    dict(slug="lauren", name="Lauren", role="NPC Bikini competitor", img="img/coach-lauren.webp",
         bio="An NPC Bikini competitor who trains clients the way she trains herself: consistently, with a plan, and with patience.",
         alt="Lauren, NPC Bikini competitor and coach at Animal Paradise Gyms"),
]

def team_cards(link=True):
    out = []
    for c in COACHES:
        tag = "a" if link else "div"
        href = f' href="coach-{c["slug"]}.html"' if link else ""
        more = '<span class="more">View profile →</span>' if link else ""
        out.append(f'<{tag} class="tcard rv"{href}><div class="tshot"><img loading="lazy" src="{c["img"]}" alt="{c["alt"]}"></div><div class="tbody"><span class="role">{c["role"]}</span><h3>{c["name"]}</h3><p>{c["bio"]}</p>{more}</div></{tag}>')
    return '<div class="team">' + "".join(out) + "</div>"

def founders_card():
    return f'''<div class="founders-card rv">
  <div class="tshot"><img loading="lazy" src="img/founders-pete-andrew.webp" alt="Pete and Andrew, founders of Animal Paradise Gyms in Vineland NJ"></div>
  <div class="tbody">
    <span class="role">Founders</span>
    <h3>Pete &amp; Andrew</h3>
    <p>Two lifters who wanted a gym South Jersey didn't have, so they built it inside Cumberland Mall. You will still find them on the floor most days, and they still answer the questions nobody else can.</p>
    <a class="textlink" href="about.html">Read our story →</a>
  </div>
</div>'''

PLANS = [
    ("silver", "No contract", False, "Silver", "Month to month", "$70", ["Full gym access", "4 studio classes", "Posing room", "Sauna"]),
    ("gold", "Best value", True, "Gold", "12 months", "$60", ["Everything in Silver", "1hr daycare add-on", "5% off cafe and supps"]),
    ("premium", "Recovery", False, "Premium", "12 months", "$70", ["Everything in Gold", "Hibernation Station", "Towel service", "2hr daycare add-on", "10% off cafe and supps"]),
    ("platinum", "Women", False, "Platinum", "12 months · Women only", "$70", ["Everything in Gold", "Lioness Den", "Towel service", "2hr daycare add-on", "10% off cafe and supps"]),
    ("diamond", "Women · All access", False, "Diamond", "12 months · Women only", "$80", ["Everything in Gold", "Lioness Den + Hibernation", "Towel service", "2hr daycare", "10% off cafe and supps"]),
]

def plan_card(p):
    k, badge, solid, name, term, price, feats = p
    btn = "btn-gold" if solid else "btn-glass"
    lis = "".join(f"<li>{x}</li>" for x in feats)
    return f'<article class="plan rv" data-tier="{k}"><span class="badge{" solid" if solid else ""}">{badge}</span><h3>{name}</h3><p class="term">{term}</p><p class="amt">{price}<small> /mo</small></p><ul>{lis}</ul><a class="btn {btn}" target="_blank" rel="noopener" href="{ABC}{PLAN_IDS[k]}">Join {name}</a></article>'

PASSES = '<div class="passes"><span>Day pass <b>$20</b></span><span>One-week pass <b>$40</b></span><span>Fit3D scan <b>$20</b></span><span>Classes <b>$15</b></span><span>Towel service <b>$10/mo</b></span><span>Daycare <b>$10/mo</b></span></div>'

def tour_form(fid="tour", title="Book your free tour"):
    return f'''<!-- On GHL: replace with the GHL tour-booking form embed (same fields) so leads land in the pipeline. -->
<form class="tour rv" id="{fid}" data-lead novalidate>
  <span class="eyebrow">No pressure</span>
  <h3>{title}</h3>
  <p class="fine" style="font-size:15px">Fifteen minutes, no sales pitch, and a straight answer on price.</p>
  <div class="field"><label for="{fid}-name">Your name</label><input id="{fid}-name" data-name autocomplete="name"></div>
  <div class="row2">
    <div class="field"><label for="{fid}-phone">Phone</label><input id="{fid}-phone" type="tel" autocomplete="tel"></div>
    <div class="field"><label for="{fid}-email">Email</label><input id="{fid}-email" type="email" autocomplete="email"></div>
  </div>
  <div class="row2">
    <div class="field"><label for="{fid}-time">Best time</label><select id="{fid}-time"><option>Any time</option><option>Early morning</option><option>Lunchtime</option><option>Afternoon</option><option>Evening</option><option>Late night</option></select></div>
    <div class="field"><label for="{fid}-goal">Your goal</label><select id="{fid}-goal"><option>Not sure yet</option><option>Build muscle</option><option>Lose weight</option><option>Get stronger</option><option>Compete</option><option>General fitness</option></select></div>
  </div>
  <button class="btn btn-gold" type="submit">Book my tour</button>
  <p class="fine">We never share your details. No card needed.</p>
  <div class="msg" hidden></div>
</form>'''

STRIPS = '<section aria-label="Photos from the gym floor" class="strips"><div class="strip"><div class="ph"><img loading="lazy" src="img/photos/vineland-gym-squat-rack-training.webp" alt="Training at Animal Paradise Gyms, Vineland NJ: squat rack training"></div><div class="ph tall"><img loading="lazy" src="img/photos/vineland-gym-cable-pulldown.webp" alt="Training at Animal Paradise Gyms, Vineland NJ: cable pulldown"></div><div class="ph tall"><img loading="lazy" src="img/photos/vineland-gym-biggest-dumbbells.webp" alt="Training at Animal Paradise Gyms, Vineland NJ: biggest dumbbells"></div><div class="ph tall"><img loading="lazy" src="img/photos/vineland-gym-incline-dumbbell-press.webp" alt="Training at Animal Paradise Gyms, Vineland NJ: incline dumbbell press"></div><div class="ph"><img loading="lazy" src="img/photos/vineland-gym-overhead-press.webp" alt="Training at Animal Paradise Gyms, Vineland NJ: overhead press"></div><div class="ph tall"><img loading="lazy" src="img/photos/vineland-gym-dumbbell-lunge.webp" alt="Training at Animal Paradise Gyms, Vineland NJ: dumbbell lunge"></div><div class="ph tall"><img loading="lazy" src="img/photos/vineland-gym-plate-loaded-row.webp" alt="Training at Animal Paradise Gyms, Vineland NJ: plate loaded row"></div><div class="ph tall"><img loading="lazy" src="img/photos/vineland-gym-deadlift.webp" alt="Training at Animal Paradise Gyms, Vineland NJ: deadlift"></div><div class="ph"><img loading="lazy" src="img/photos/vineland-gym-squat-rack-training.webp" alt=""></div><div class="ph tall"><img loading="lazy" src="img/photos/vineland-gym-cable-pulldown.webp" alt=""></div><div class="ph tall"><img loading="lazy" src="img/photos/vineland-gym-biggest-dumbbells.webp" alt=""></div><div class="ph tall"><img loading="lazy" src="img/photos/vineland-gym-incline-dumbbell-press.webp" alt=""></div><div class="ph"><img loading="lazy" src="img/photos/vineland-gym-overhead-press.webp" alt=""></div><div class="ph tall"><img loading="lazy" src="img/photos/vineland-gym-dumbbell-lunge.webp" alt=""></div><div class="ph tall"><img loading="lazy" src="img/photos/vineland-gym-plate-loaded-row.webp" alt=""></div><div class="ph tall"><img loading="lazy" src="img/photos/vineland-gym-deadlift.webp" alt=""></div></div><div class="strip rev"><div class="ph tall"><img loading="lazy" src="img/photos/vineland-gym-cable-crunch.webp" alt="Training at Animal Paradise Gyms, Vineland NJ: cable crunch"></div><div class="ph tall"><img loading="lazy" src="img/photos/vineland-gym-lift-heavy.webp" alt="Training at Animal Paradise Gyms, Vineland NJ: lift heavy"></div><div class="ph"><img loading="lazy" src="img/photos/vineland-gym-cable-training.webp" alt="Training at Animal Paradise Gyms, Vineland NJ: cable training"></div><div class="ph tall"><img loading="lazy" src="img/photos/vineland-gym-dumbbell-flyes.webp" alt="Training at Animal Paradise Gyms, Vineland NJ: dumbbell flyes"></div><div class="ph tall"><img loading="lazy" src="img/photos/vineland-gym-cable-extension.webp" alt="Training at Animal Paradise Gyms, Vineland NJ: cable extension"></div><div class="ph"><img loading="lazy" src="img/photos/vineland-gym-surf-machine.webp" alt="Training at Animal Paradise Gyms, Vineland NJ: surf machine"></div><div class="ph tall"><img loading="lazy" src="img/photos/vineland-gym-cable-pushdown.webp" alt="Training at Animal Paradise Gyms, Vineland NJ: cable pushdown"></div><div class="ph tall"><img loading="lazy" src="img/photos/vineland-gym-red-light-recovery.webp" alt="Training at Animal Paradise Gyms, Vineland NJ: red light recovery"></div><div class="ph tall"><img loading="lazy" src="img/photos/vineland-gym-cable-crunch.webp" alt=""></div><div class="ph tall"><img loading="lazy" src="img/photos/vineland-gym-lift-heavy.webp" alt=""></div><div class="ph"><img loading="lazy" src="img/photos/vineland-gym-cable-training.webp" alt=""></div><div class="ph tall"><img loading="lazy" src="img/photos/vineland-gym-dumbbell-flyes.webp" alt=""></div><div class="ph tall"><img loading="lazy" src="img/photos/vineland-gym-cable-extension.webp" alt=""></div><div class="ph"><img loading="lazy" src="img/photos/vineland-gym-surf-machine.webp" alt=""></div><div class="ph tall"><img loading="lazy" src="img/photos/vineland-gym-cable-pushdown.webp" alt=""></div><div class="ph tall"><img loading="lazy" src="img/photos/vineland-gym-red-light-recovery.webp" alt=""></div></div></section>'

# ---------- FAQ bank ----------
FAQ_HOURS = [
    ("What are Animal Paradise Gyms' hours?", "Animal Paradise is open every day of the week from 4AM to 12AM (midnight), including weekends."),
    ("Where is Animal Paradise Gyms?", "Inside Cumberland Mall at 3849 S Delsea Dr, Suite E000, Vineland, NJ 08360. Members from Millville, Bridgeton and the rest of Cumberland County train here."),
    ("Is there parking?", "Yes. Parking at Cumberland Mall is free, and it is right outside the gym door."),
]
FAQ_MEM = [
    ('Is personal training included in my membership?', 'No. Memberships cover gym access and the amenities listed in your plan. Personal training is a separate service you book with a coach. Your first consultation is free, so you can learn the options and pricing before you decide.'),
    ("How much is a gym membership at Animal Paradise in Vineland?", "Memberships start at $60 a month on the 12-month Gold plan. The no-contract Silver plan is $70 a month. A day pass is $20 and a one-week pass is $40."),
    ("Do I have to sign a contract?", "No. Silver is month to month with no contract. Gold, Premium, Platinum and Diamond are 12-month agreements, which is why they cost the same or less per month with more included."),
    ("Can I try the gym before I join?", "Yes. Book a free tour to see every area first, or buy a $20 day pass or a $40 one-week pass to train before you commit."),
    ("Can I join online?", "Yes. Every plan has a Join button that takes you to secure online sign-up. You can also join at the front desk."),
    ("Is there childcare at the gym?", "Yes. Daycare is a $9.99 a month add-on, with one hour on Gold and two hours on Premium, Platinum and Diamond."),
]
FAQ_TRAIN = [
    ('Is personal training included in my membership?', 'No. Memberships cover gym access and the amenities listed in your plan. Personal training is a separate service you book with a coach. Your first consultation is free, so you can learn the options and pricing before you decide.'),
    ("Is Animal Paradise good for beginners?", "Yes. Book a free tour and staff will walk you through every area and show you how the equipment works. If you want more guidance, personal training is available as a separate service."),
    ("Do you offer personal training in Vineland?", "Yes. Our coaches offer one-on-one sessions, small groups, meal plans and athlete development. Personal training is a separate service from your membership, and your first consultation is free."),
    ("Do you offer NPC contest prep?", "Yes. Chuck and Lauren coach competitors through prep, posing and peak week, and members get access to a dedicated posing room."),
]
FAQ_AMEN = [
    ("Does Animal Paradise have a women's-only area?", "Yes. The Lioness Den is a women's-only training space with its own free weights, machines and cables, included with Platinum and Diamond memberships."),
    ("What is the Hibernation Station?", "Our recovery room, with massage chairs and compression sleeves to help you recover between sessions. It is included with Premium and Diamond."),
    ("Does the gym have a sauna?", "Yes. Animal Paradise has sauna rooms, and access is included with every membership."),
    ("What equipment brands do you have?", "Arsenal, Atlantis, Rogue, Booty Builder and StarTrac, plus an 80-foot functional training turf and full free-weight floors."),
]

GYM_LD = {
    "@context": "https://schema.org", "@type": ["ExerciseGym", "HealthClub"], "@id": SITE + "/#gym",
    "name": "Animal Paradise Gyms", "url": SITE + "/",
    "logo": SITE + "/img/logo.png",
    "image": SITE + "/img/photos/vineland-gym-hero-floor.webp",
    "description": "Full-service gym inside Cumberland Mall in Vineland, NJ. Open every day 4AM to 12AM with Arsenal, Atlantis and Rogue equipment, an 80-foot turf, sauna, recovery room, a women's-only training area, personal training, an on-site cafe and supplement store.",
    "telephone": "+1-856-839-4536", "email": "Info@AnimalParadiseGyms.com", "priceRange": "$20 to $80",
    "address": {"@type": "PostalAddress", "streetAddress": "3849 S Delsea Dr, Suite E000, Cumberland Mall", "addressLocality": "Vineland", "addressRegion": "NJ", "postalCode": "08360", "addressCountry": "US"},
    "areaServed": ["Vineland NJ", "Millville NJ", "Bridgeton NJ", "Cumberland County NJ", "Glassboro NJ"],
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "04:00", "closes": "24:00"}],
    "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": n, "value": True} for n in ["Sauna", "Free parking", "Childcare", "Women's-only training area", "80-foot functional training turf", "Fit3D body composition scanner", "Posing room", "Recovery room"]],
    "founder": [{"@type": "Person", "name": "Pete"}, {"@type": "Person", "name": "Andrew"}],
    "sameAs": ["https://www.instagram.com/animalparadisegyms", "https://www.facebook.com/profile.php?id=61560036899811", "https://apps.apple.com/us/app/animal-paradise-gym/id6745569852"],
}

ICONS = dict(
    leaf='<path d="M12 21V11"/><path d="M12 11C12 7 9 4 4 4c0 4 3 7 8 7z"/><path d="M12 13c0-3 2.5-5.5 7-5.5 0 3-2.5 5.5-7 5.5z"/>',
    back='<path d="M3 12a9 9 0 1 0 3-6.7"/><path d="M3 4v5h5"/>',
    trophy='<path d="M8 21h8M12 17v4M7 4h10v5a5 5 0 0 1-10 0V4z"/><path d="M17 5h3v2a3 3 0 0 1-3 3M7 5H4v2a3 3 0 0 0 3 3"/>',
    shield='<path d="M12 3l7 3v5c0 4.5-3 8.5-7 10-4-1.5-7-5.5-7-10V6l7-3z"/><path d="M9 12l2 2 4-4"/>',
    user='<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/>',
    users='<circle cx="9" cy="8" r="3.5"/><path d="M2 20c0-3.5 3-5.5 7-5.5s7 2 7 5.5"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M22 20c0-3-2-5-5-5.4"/>',
    plate='<path d="M4 3v18M8 3v6a4 4 0 0 1-8 0"/><path d="M14 3c-1.5 2-2 4.5-2 7h4V3h-2zM16 10v11"/>',
    bolt='<path d="M13 2L4 14h7l-1 8 9-12h-7l1-8z"/>',
    flame='<path d="M12 22c4 0 7-3 7-7 0-5-5-7-5-12-3 2-4 5-4 7-1-1-2-2-2-4-2 2-3 5-3 9 0 4 3 7 7 7z"/>',
    scan='<path d="M4 8V4h4M16 4h4v4M20 16v4h-4M8 20H4v-4"/><path d="M8 12h8"/>',
    cup='<path d="M5 8h12v5a6 6 0 0 1-12 0V8z"/><path d="M17 9h2a2 2 0 0 1 0 4h-2"/><path d="M8 3v2M11 3v2M14 3v2"/>',
    pin='<path d="M12 21s-7-6-7-11a7 7 0 0 1 14 0c0 5-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
)
def icon(n):
    return f'<div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICONS[n]}</svg></div>'

def card(ic, title, text, href=None, go=None):
    tag = "a" if href else "article"
    h = f' href="{href}"' if href else ""
    g = f'<span class="go">{go} →</span>' if go else ""
    return f'<{tag} class="who-card rv"{h}>{icon(ic)}<h3>{title}</h3><p>{text}</p>{g}</{tag}>'

def vid(name, label, cap):
    return f'''<figure class="vframe rv" style="margin:0"><video muted playsinline loop preload="none" poster="video/{name}.webp" aria-label="{label}" data-autoplay><source src="video/{name}.mp4" type="video/mp4"></video><figcaption>{cap}</figcaption></figure>'''

PAGES = {}

# ================= HOME =================
PAGES["index.html"] = dict(
    title="Gym in Vineland, NJ | Open 4AM to 12AM | Animal Paradise Gyms",
    desc="Full-service gym inside Cumberland Mall, Vineland NJ. Open daily 4AM to midnight. Memberships from $60/mo, no-contract option, women's-only Lioness Den, sauna, personal training. Book a free tour.",
    slug="", schemas=[GYM_LD, faq_ld(FAQ_HOURS[:1] + FAQ_MEM[:2] + FAQ_TRAIN[:1])],
    body=f'''
<section class="hero" aria-labelledby="hero-h">
  <div class="ph hero-bg"><img src="img/photos/vineland-gym-hero-floor.webp" alt="Main training floor at Animal Paradise Gyms, Vineland NJ" fetchpriority="high" onerror="this.remove()"></div>
  <div class="wrap">
    <div>
      <span class="pill" id="status"><i class="dot"></i><span id="status-text">Gym in Vineland, NJ · Cumberland Mall</span></span>
      <h1 id="hero-h"><span class="line">Built for strength.</span><span class="line gold">Made for everyone.</span></h1>
      <p class="hero-sub">Serious equipment. Supportive people. All fitness levels.</p>
      <p class="lede" style="color:rgba(242,236,223,.82)">South Jersey's best-equipped gym, inside Cumberland Mall in Vineland. Whether you are just starting out, getting back in shape, training for a sport or simply want to feel better, you will find the space, the equipment and a crew that makes you feel welcome.</p>
      <div class="hero-cta">
        <a class="btn btn-gold" href="visit.html#tour">Book a free tour {ARROW}</a>
        <a class="btn btn-glass" href="memberships.html">See memberships</a>
      </div>
      <div class="hero-stats">
        <div class="hs"><b>4AM to 12AM</b><span>Open every day</span></div>
        <div class="hs"><b>$60/mo</b><span>Memberships from</span></div>
        <div class="hs"><b>80 ft</b><span>Training turf</span></div>
      </div>
    </div>
    <form class="quick" id="quick" data-lead novalidate>
      <span class="eyebrow">No pressure</span>
      <h3>Book a free tour</h3>
      <p>Fifteen minutes, no sales pitch, and a straight answer on price.</p>
      <div class="field"><label for="q-name">Name</label><input id="q-name" data-name autocomplete="name"></div>
      <div class="field"><label for="q-phone">Phone</label><input id="q-phone" type="tel" autocomplete="tel"></div>
      <button class="btn btn-gold" type="submit">Book my free tour</button>
      <div class="msg" hidden></div>
    </form>
  </div>
</section>

<div class="brands" aria-label="Equipment brands on the floor">
  <div class="track">
    <span>ARSENAL</span><span>ATLANTIS</span><span>ROGUE</span><span>BOOTY BUILDER</span><span>STARTRAC</span><span>FIT3D</span>
    <span aria-hidden="true">ARSENAL</span><span aria-hidden="true">ATLANTIS</span><span aria-hidden="true">ROGUE</span><span aria-hidden="true">BOOTY BUILDER</span><span aria-hidden="true">STARTRAC</span><span aria-hidden="true">FIT3D</span>
  </div>
</div>

<section class="band">
  <div class="wrap">
    {head_block("Who it's for", 'Serious equipment. <span class="gold">Zero attitude.</span>', "Built by Pete and Andrew, two lifters who wanted the gym they couldn't find in South Jersey. The iron is competition grade. The people are why members stay.")}
    <div class="who">
      {card("leaf", "Brand new", "Take a free tour, learn where everything is and ask staff about any machine. Nobody expects you to know the equipment yet.", "first-week-at-the-gym-beginners.html", "Beginner guide")}
      {card("back", "Getting back in", "Recovery room, sauna and Fit3D body scans so you see progress beyond the scale.", "the-gym.html#recovery", "See recovery")}
      {card("trophy", "Competing", "Posing room, NPC contest-prep coaching and the machines lifters ask for by name.", "personal-training.html#contest-prep", "Contest prep")}
      {card("shield", "Women", "The Lioness Den: a women's-only training space with its own weights, machines and cables.", "lioness-den.html", "Tour the Den")}
    </div>
  </div>
</section>

<section class="band" style="padding-top:0">
  <div class="wrap">
    {head_block("Inside the gym", 'Everything under <span class="gold">one roof.</span>', "Train, recover, refuel and restock without leaving the building.")}
    <div class="bento">
      <a class="tile big rv" href="the-gym.html#equipment" style="text-decoration:none">
        {ph("img/photos/vineland-gym-squat-racks.webp", "Squat racks and Atlantis plates on the Animal Paradise floor in Vineland NJ")}
        <div class="tile-body"><span class="tag">The floor</span><h3 style="font-size:clamp(24px,2.6vw,34px)">Competition-grade iron</h3><p>Full free-weight and machine floors from the brands lifters travel for.</p><div class="chips"><span>Arsenal</span><span>Atlantis</span><span>Rogue</span><span>Booty Builder</span><span>StarTrac</span></div></div>
      </a>
      <div class="tile stat rv"><div class="tile-body"><b>80<span style="font-size:.4em">FT</span></b><p>Functional turf for sleds, carries and sprints.</p></div></div>
      <a class="tile rv" href="the-gym.html#recovery" style="text-decoration:none">{ph("img/photos/vineland-gym-hibernation-station-2.webp", "Massage chairs in the Hibernation Station recovery room")}<div class="tile-body"><span class="tag">Recovery</span><h3>Hibernation Station</h3><p>Massage chairs, compression and sauna.</p></div></a>
      <a class="tile wide rv" href="lioness-den.html" style="text-decoration:none">{ph("img/photos/vineland-gym-lioness-den.webp", "Lioness Den women's-only training area with pink neon wall")}<div class="tile-body"><span class="tag">Women only</span><h3>The Lioness Den</h3><p>Its own free weights, machines and cables. Train without an audience.</p></div></a>
      <a class="tile rv" href="animal-cafe.html" style="text-decoration:none">{ph("img/photos/vineland-gym-animal-cafe.webp", "Animal Cafe counter inside Animal Paradise Gyms")}<div class="tile-body"><span class="tag">Fuel</span><h3>Animal Cafe</h3><p>Shakes, açaí bowls, juice.</p></div></a>
      <a class="tile rv" href="animal-supps.html" style="text-decoration:none">{ph("img/photos/vineland-gym-animal-supps.webp", "Animal Supps supplement shelves")}<div class="tile-body"><span class="tag">Restock</span><h3>Animal Supps</h3><p>Members save up to 10%.</p></div></a>
      <div class="tile dark wide rv"><div class="tile-body"><span class="tag">Also included</span><h3>The small things that matter</h3><div class="chips"><span>Posing room</span><span>Fit3D scanning</span><span>Daycare</span><span>Towel service</span><span>Pool table lounge</span><span>Free parking</span><span>Member app</span></div></div></div>
    </div>
    <div class="center-row"><a class="btn btn-glass" href="the-gym.html">Explore the full gym {ARROW}</a></div>
  </div>
</section>

{STRIPS}
<div class="wrap center-row" style="margin-top:28px"><a class="btn btn-glass" href="gallery.html">See all photos {ARROW}</a></div>

<section class="band" style="padding-block:clamp(56px,7vw,90px)" aria-label="Animal Paradise by the numbers">
  <div class="wrap"><div class="nums">
    <div class="num"><b class="gold" data-count="7">7</b><span>Days a week</span></div>
    <div class="num"><b class="gold" data-count="20">20</b><span>Hours a day, 4AM to 12AM</span></div>
    <div class="num"><b class="gold" data-count="80">80</b><span>Feet of training turf</span></div>
    <div class="num"><b class="gold" data-count="5">5</b><span>Membership plans</span></div>
  </div></div>
</section>

<section class="band mem">
  <div class="wrap">
    {head_block("Memberships", 'Gym memberships in Vineland from <span class="gold">$60</span>', "Five plans, one standard of gym. No-contract option available.", center=True)}
    <div class="mini-plans">{plan_card(PLANS[1])}{plan_card(PLANS[0])}{plan_card(PLANS[2])}</div>
    <div class="center-row"><a class="btn btn-glass" href="memberships.html">Compare all 5 plans {ARROW}</a></div>
  </div>
</section>

<section class="band" style="padding-top:0">
  <div class="wrap">
    {head_block("Under the same roof", 'Fuel up. <span class="gold">Stock up.</span>', "Animal Cafe and Animal Supps are inside the gym, open 4AM to midnight every day. Members save up to 10% at both.")}
    <div class="cards two">
      <a class="tile rv" style="min-height:420px;text-decoration:none" href="animal-cafe.html">{ph("img/photos/vineland-gym-animal-cafe-2.webp", "Animal Cafe in Vineland NJ, inside Animal Paradise Gyms")}<div class="tile-body"><span class="tag">Animal Cafe</span><h3 style="font-size:clamp(22px,2.4vw,30px)">Shakes, açaí bowls, juice and coffee</h3><p>Order on the way in, grab it on the way out.</p><span class="textlink">See the cafe →</span></div></a>
      <a class="tile rv" style="min-height:420px;text-decoration:none" href="animal-supps.html">{ph("img/photos/vineland-gym-animal-supps-2.webp", "Animal Supps supplement store in Vineland NJ")}<div class="tile-body"><span class="tag">Animal Supps</span><h3 style="font-size:clamp(22px,2.4vw,30px)">Pre-workout, protein, creatine</h3><p>Top-tier brands, staff who actually train.</p><span class="textlink">Shop supps →</span></div></a>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    {head_block("New to the gym?", 'Your first week, <span class="gold">planned for you.</span>', "Most people put off joining because the first walk-in feels like a lot. Here is exactly what happens.")}
    <div class="timeline">
      <div class="tstep rv"><div class="n">1</div><span class="when">Day one</span><h3>Take a free tour</h3><p>Fifteen minutes with a staff member. See every area, ask anything, get a straight answer on price.</p></div>
      <div class="tstep rv"><div class="n">2</div><span class="when">Same visit</span><h3>Pick your plan</h3><p>Use the membership finder or ask at the desk. There is a no-contract option if you are not ready to commit.</p></div>
      <div class="tstep rv"><div class="n">3</div><span class="when">First week</span><h3>Start training</h3><p>Train on your own with the full floor, or add personal training if you want a coach. Training is booked separately from your membership.</p></div>
    </div>
  </div>
</section>

<section class="band" style="padding-top:0">
  <div class="wrap">
    {head_block("Personal training in Vineland", 'Coaches who <span class="gold">still train.</span>', "One-on-one, small groups, meal plans and NPC contest prep. Available as a separate service from your membership.")}
    {team_cards()}
    <div class="center-row"><a class="btn btn-glass" href="personal-training.html">Personal training {ARROW}</a></div>
  </div>
</section>

<section class="band" style="padding-top:0">
  <div class="wrap">
    {head_block("Members", "What the floor says")}
    <div class="reviews">
      <figure class="rv-card feature rv" style="margin:0"><p>Easily hands down the best gym in the tri-state. From the equipment to the staff, you aren't going to find anything like this.</p><figcaption class="who-said"><span class="av">H</span><span><b>Harry M</b><span>Member</span></span></figcaption></figure>
      <figure class="rv-card rv" style="margin:0"><p>The equipment is top of the line. The atmosphere and energy is a whole vibe.</p><figcaption class="who-said"><span class="av">J</span><span><b>JoAnna W</b><span>Member</span></span></figcaption></figure>
      <figure class="rv-card rv" style="margin:0"><p>Whenever I visit Vineland I go here now. I can't find equipment close to this even in Boston.</p><figcaption class="who-said"><span class="av">J</span><span><b>Jared G</b><span>Visiting member</span></span></figcaption></figure>
    </div>
  </div>
</section>

<section class="band faq" style="padding-top:0">
  <div class="wrap faq-grid">
    <div class="head rv" style="margin:0;align-content:start"><span class="eyebrow">Questions</span><h2>Straight answers.</h2><p class="lede">More on the <a class="textlink" href="faq.html">full FAQ page</a>, or call <b style="color:var(--ink)">(856) 839-4536</b>.</p></div>
    <div class="faq-list">{faq_html(FAQ_HOURS[:1] + FAQ_MEM[:2] + FAQ_TRAIN[:1])}</div>
  </div>
</section>
<section class="band" style="padding-top:0">
  <div class="wrap">
    <a class="tile rv" style="min-height:420px;text-decoration:none" href="animal-fest-3.html">{ph("img/photos/vineland-gym-animal-fest-belt.webp", "Animal Fest III champion belt at Animal Paradise Gyms")}<div class="tile-body"><span class="tag">Events · October 10, 2026</span><h3 style="font-size:clamp(26px,3.4vw,44px)">Animal Fest 3 recap</h3><p>Guest posing, competitions, vendors and the whole crew under one roof.</p><span class="textlink">See the event →</span></div></a>
  </div>
</section>
{closer()}''')

# ================= THE GYM =================
PAGES["the-gym.html"] = dict(
    title="Gym Equipment and Amenities in Vineland NJ | Animal Paradise Gyms",
    desc="Arsenal, Atlantis, Rogue, Booty Builder and StarTrac equipment, an 80-ft turf, sauna, recovery room, Fit3D scanning, cafe and supplement store. Inside Cumberland Mall, Vineland NJ.",
    slug="the-gym", schemas=[crumbs_ld("The Gym", "the-gym")],
    body=page_hero("The gym · Vineland, NJ", 'Inside South Jersey\'s <span class="gold">best-equipped</span> gym', "Specialty equipment, real recovery, a women's-only training space and a cafe and supplement store under one roof at Cumberland Mall.", "The Gym", bg="cardio-floor") + f'''
<section class="band" id="equipment">
  <div class="wrap split">
    {ph("img/photos/vineland-gym-cable-stations.webp", "Cable stations and machines under the Animal Paradise sign")}
    <div class="prose rv">
      <span class="eyebrow">The equipment</span>
      <h2>Machines lifters <span class="gold">ask for by name</span></h2>
      <p>Most gyms in South Jersey run one brand of selectorized machines. Animal Paradise runs <strong>Arsenal, Atlantis, Rogue, Booty Builder and StarTrac</strong> side by side, so every muscle group has more than one way to train it.</p>
      <ul class="ticks"><li>Plate-loaded and selectorized machine floors</li><li>Full free-weight area with dumbbells and racks</li><li>Booty Builder glute stations</li><li>StarTrac cardio line</li><li>Posing room for competitors</li></ul>
    </div>
  </div>
</section>

<section class="band" style="padding-top:0" id="dumbbells">
  <div class="wrap cards two">
    <div class="tile rv" style="min-height:460px"><div class="ph"><img loading="lazy" src="img/photos/vineland-gym-biggest-dumbbells.webp" alt="Wall reading Home of the biggest dumbbells in the world at Animal Paradise Gyms"></div><div class="tile-body"><span class="tag">On the wall</span><h3>Home of the biggest dumbbells in the world</h3><p>It's painted on our wall for a reason. Come see them in person.</p></div></div>
    <div class="tile rv" style="min-height:460px"><div class="ph"><img loading="lazy" src="img/photos/vineland-gym-cardio-floor-2.webp" alt="Rows of StarTrac cardio machines under LED lights at Animal Paradise"></div><div class="tile-body"><span class="tag">Cardio</span><h3>A full cardio floor</h3><p>Treadmills, bikes and more, lined up under the lights and open 4AM to midnight.</p></div></div>
  </div>
</section>

<section class="band" style="padding-top:0" id="turf">
  <div class="wrap split flip">
    <div class="tile stat rv" style="min-height:360px"><div class="tile-body"><b style="font-size:clamp(90px,12vw,170px)">80<span style="font-size:.35em">FT</span></b><p style="font-size:17px">Of functional training turf</p></div></div>
    <div class="prose rv">
      <span class="eyebrow">The turf</span>
      <h2>Room to push, pull <span class="gold">and sprint</span></h2>
      <p>An 80-foot lane of turf for sled pushes, farmer carries, lunges, sprints and conditioning. It is the part of training a treadmill can't do, and it is open every hour the gym is.</p>
    </div>
  </div>
</section>

<section class="band" style="padding-top:0" id="recovery">
  <div class="wrap">
    {head_block("Recovery and wellness", 'Recovery is where <span class="gold">results happen.</span>', "The training breaks you down. These put you back together.")}
    <div class="split" style="margin-bottom:40px">
      {vid("vineland-gym-recovery-room","Video tour of the Hibernation Station recovery room and sauna rooms","Inside the Hibernation Station")}
      <div class="prose rv">
        <span class="eyebrow">Take a look</span>
        <h2>Massage chairs, compression <span class="gold">and sauna rooms</span></h2>
        <p>The Hibernation Station is our recovery room: a row of full-body massage chairs and Sharper Image compression therapy boots. Next door, the sauna rooms are open to every member.</p>
        <ul class="ticks"><li>Full-body massage chairs</li><li>Compression therapy</li><li>Sauna rooms, included with every plan</li><li>Fit3D body scanning</li></ul>
        <p><a class="btn btn-glass" href="memberships.html">Plans with the Hibernation Station {ARROW}</a></p>
      </div>
    </div>
    <div class="cards">
      {card("bolt", "Hibernation Station", "Massage chairs and compression therapy. Included with Premium and Diamond.", "memberships.html", "Plans with recovery")}
      {card("flame", "Sauna rooms", "Included with every membership, from Silver up. Use them after training or on rest days.")}
      {card("scan", "Fit3D body scanning", "A full 3D body composition scan that shows what is changing beyond the scale. $20 per scan.")}
    </div>
  </div>
</section>

<section class="band" style="padding-top:0" id="lioness">
  <div class="wrap split">
    {ph("img/photos/vineland-gym-lioness-den-2.webp", "Lioness Den women's-only training area at Animal Paradise")}
    <div class="prose rv">
      <span class="eyebrow">Women only</span>
      <h2>The <span class="gold">Lioness Den</span></h2>
      <p>A women's-only training space with its own free weights, machines and cables, open the same hours as the main floor. Included with Platinum and Diamond memberships.</p>
      <p><a class="btn btn-glass" href="lioness-den.html">Tour the Lioness Den {ARROW}</a></p>
    </div>
  </div>
</section>

<section class="band" style="padding-top:0" id="fuel">
  <div class="wrap">
    {head_block("Fuel and restock", 'You never have to <span class="gold">leave the building.</span>', "Both open the same hours as the gym, 4AM to midnight. Members save up to 10%.")}
    <div class="cards two">
      <a class="tile rv" style="min-height:380px;text-decoration:none" href="animal-cafe.html">{ph("img/photos/vineland-gym-animal-cafe-counter.webp", "Animal Cafe counter at Animal Paradise Gyms")}<div class="tile-body"><span class="tag">Animal Cafe</span><h3>Shakes, açaí bowls and cold-pressed juice</h3><p>Order before you train and pick it up on the way out.</p></div></a>
      <a class="tile rv" style="min-height:380px;text-decoration:none" href="animal-supps.html">{ph("img/photos/vineland-gym-animal-supps-storefront.webp", "Animal Supps storefront inside the gym")}<div class="tile-body"><span class="tag">Animal Supps</span><h3>The supplement store on the gym floor</h3><p>Pre-workout, protein, creatine and aminos from staff who actually train.</p></div></a>
    </div>
  </div>
</section>

<section class="band" style="padding-top:0">
  <div class="wrap">
    {head_block("Also included", "The small things that matter")}
    <div class="cards four">
      {card("users", "Daycare", "Add-on for $9.99 a month. One hour on Gold, two hours on Premium, Platinum and Diamond.")}
      {card("cup", "Pool table lounge", "A social area to hang out before or after your session.")}
      {card("trophy", "Posing room", "A private room with mirrors for competitors practicing their routine.")}
      {card("pin", "Free parking", "Cumberland Mall parking right outside the door.")}
    </div>
    <div class="cards" style="margin-top:14px">
      <div class="tile rv" style="min-height:300px"><div class="ph"><img loading="lazy" src="img/photos/vineland-gym-posing-room.webp" alt="Posing room lounge with gold decor at Animal Paradise"></div><div class="tile-body"><span class="tag">Competitors</span><h3>Posing room</h3><p>Practice your routine before show day.</p></div></div>
      <div class="tile rv" style="min-height:300px"><div class="ph"><img loading="lazy" src="img/photos/vineland-gym-daycare.webp" alt="Daycare entrance at Animal Paradise Gyms Vineland"></div><div class="tile-body"><span class="tag">Parents</span><h3>Daycare</h3><p>Train while the kids are looked after.</p></div></div>
      <div class="tile rv" style="min-height:300px"><div class="ph"><img loading="lazy" src="img/photos/vineland-gym-pool-table-lounge.webp" alt="Pool table lounge with mall views next to Animal Cafe"></div><div class="tile-body"><span class="tag">Hang out</span><h3>Pool table lounge</h3><p>Stay a while after your session.</p></div></div>
    </div>
  </div>
</section>
{STRIPS}
<div class="wrap center-row" style="margin-top:28px"><a class="btn btn-glass" href="gallery.html">See all photos {ARROW}</a></div>
{closer("See it in", "person.")}''')

# ================= MEMBERSHIPS =================
cmp_rows = [("Full gym access", "yyyyy"), ("Sauna", "yyyyy"), ("4 studio classes", "yyyyy"), ("Posing room", "yyyyy"),
            ("No contract", "ynnnn"), ("Daycare add-on", "nyyyy"), ("Cafe and supps discount", "n5↑↑↑"),
            ("Towel service", "nnyyy"), ("Hibernation Station", "nnyny"), ("Lioness Den", "nnnyy")]
def cmp_cell(c):
    return {"y": '<td class="y">✓</td>', "n": '<td class="n">·</td>', "5": "<td>5%</td>", "↑": "<td>10%</td>"}[c]
cmp_html = "".join(f"<tr><td>{r}</td>{''.join(cmp_cell(c) for c in cs)}</tr>" for r, cs in cmp_rows)
PAGES["memberships.html"] = dict(
    title="Gym Memberships in Vineland NJ from $60/mo | Animal Paradise",
    desc="Compare 5 gym membership plans at Animal Paradise in Vineland NJ. From $60/month, no-contract option at $70, women's-only plans, $20 day pass. Join online.",
    slug="memberships", schemas=[crumbs_ld("Memberships", "memberships"), faq_ld(FAQ_MEM),
        {"@context": "https://schema.org", "@type": "OfferCatalog", "name": "Animal Paradise Gyms memberships", "itemListElement": [
            {"@type": "Offer", "name": f"{p[3]} membership", "description": p[4], "price": p[5].strip("$"), "priceCurrency": "USD", "seller": GYM_ID} for p in PLANS] +
            [{"@type": "Offer", "name": "Day pass", "price": "20", "priceCurrency": "USD"}, {"@type": "Offer", "name": "One-week pass", "price": "40", "priceCurrency": "USD"}]}],
    body=page_hero("Memberships · Vineland, NJ", 'Gym memberships <span class="gold">from $60</span> a month', "Five plans, one standard of gym. Month to month or 12 months for the better rate. Every plan includes the full floor, sauna and posing room.", "Memberships", ctas=False, bg="cardio-floor-2") + f'''
<section class="band mem">
  <div class="wrap">
    {head_block("Membership finder", "Not sure which plan? Answer three questions.", center=True)}
    <form class="finder rv" id="finder" aria-label="Membership finder">
      <div class="finder-q">
        <fieldset><legend>Want access to the women's-only Lioness Den?</legend><div class="seg"><input type="radio" name="den" id="den-n" value="n" checked><label for="den-n">Main floor is fine</label><input type="radio" name="den" id="den-y" value="y"><label for="den-y">Yes please</label></div></fieldset>
        <fieldset><legend>How do you want to pay?</legend><div class="seg"><input type="radio" name="term" id="term-12" value="12" checked><label for="term-12">12 months, lower rate</label><input type="radio" name="term" id="term-m" value="m"><label for="term-m">Month to month</label></div></fieldset>
        <fieldset><legend>Want the recovery room?</legend><div class="seg"><input type="radio" name="rec" id="rec-n" value="n" checked><label for="rec-n">Not needed</label><input type="radio" name="rec" id="rec-y" value="y"><label for="rec-y">Yes, massage chairs and all</label></div></fieldset>
      </div>
      <div class="finder-a" aria-live="polite">
        <span class="eyebrow">Your best fit</span>
        <div class="tier gold" id="f-tier">Gold</div>
        <div class="price" id="f-price">$60 <small>a month, 12 months</small></div>
        <p id="f-why">Our best value. Full gym, sauna, studio classes and 5% off at the cafe and supps store.</p>
        <a class="btn btn-gold" id="f-join" href="{ABC}{PLAN_IDS['gold']}" target="_blank" rel="noopener">Join Gold online</a>
      </div>
    </form>
    <div class="plans">{"".join(plan_card(p) for p in PLANS)}</div>
    {PASSES}
    <p class="pt-note">Personal training is not included in any membership. It is a separate service you book with a coach, and the first consultation is free. <a class="textlink" href="personal-training.html">See personal training</a></p>
    <div class="tbl-wrap rv">
      <table class="tbl">
        <thead><tr><th>Compare plans</th><th>Silver<br><small>$70</small></th><th>Gold<br><small>$60</small></th><th>Premium<br><small>$70</small></th><th>Platinum<br><small>$70</small></th><th>Diamond<br><small>$80</small></th></tr></thead>
        <tbody>{cmp_html}</tbody>
      </table>
    </div>
  </div>
</section>

<section class="band faq">
  <div class="wrap faq-grid">
    <div class="head rv" style="margin:0;align-content:start"><span class="eyebrow">Membership questions</span><h2>Before you join</h2><p class="lede">Rather talk it through? Book a tour and get a straight answer on price at the desk.</p></div>
    <div class="faq-list">{faq_html(FAQ_MEM)}</div>
  </div>
</section>
{closer("See it", "before you join.")}''')

# ================= PERSONAL TRAINING =================
PAGES["personal-training.html"] = dict(
    title="Personal Trainers in Vineland NJ | Contest Prep | Animal Paradise",
    desc="Personal training, small groups, meal plans and NPC contest prep in Vineland NJ. Meet Chuck, Hakim and Lauren. Booked separately from membership. First consultation free.",
    slug="personal-training",
    schemas=[crumbs_ld("Personal Training", "personal-training"), faq_ld(FAQ_TRAIN),
             {"@context": "https://schema.org", "@type": "Service", "serviceType": "Personal training", "name": "Personal training and contest prep in Vineland, NJ", "provider": GYM_ID, "areaServed": "Vineland NJ",
              "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Coaching", "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": n}} for n in ["One-on-one personal training", "Small group training", "Meal plans", "Athlete development", "NPC contest prep"]]}}] +
            [{"@context": "https://schema.org", "@type": "Person", "name": c["name"], "jobTitle": c["role"], "worksFor": GYM_ID, "image": f'{SITE}/{c["img"]}'} for c in COACHES],
    body=page_hero("Personal training · Vineland, NJ", 'Coaching you can <span class="gold">see and feel</span>', "Stop guessing in the gym. One-on-one sessions, small groups, meal plans, athlete development and NPC contest prep. Personal training is a separate service from your gym membership, and your first consultation is free.", "Personal Training", ctas=False, bg="squat-rack-training") + f'''
<section class="band">
  <div class="wrap">
    {head_block("What we offer", 'Pick how you <span class="gold">want to train.</span>')}
    <p class="pt-note" style="margin:-12px 0 28px">Personal training is a separate service and is not included in any gym membership. Your first consultation is free, with no obligation.</p>
    <div class="cards">
      {card("user", "One-on-one training", "A coach, a plan and accountability every session. Best if you are starting out or chasing a specific goal.")}
      {card("users", "Small groups", "Train alongside a small group with the same coaching and accountability.")}
      {card("plate", "Meal plans", "Nutrition built around your schedule and goal, so the work in the gym actually shows.")}
      {card("bolt", "Athlete development", "Speed, strength and conditioning for athletes, using the 80-foot turf.")}
      {card("trophy", "NPC contest prep", "Full prep from offseason to stage: training, nutrition, posing and peak week.", "#contest-prep", "Contest prep")}
      {card("scan", "Fit3D progress scans", "Body composition scans so you and your coach track real changes, not just weight.")}
    </div>
  </div>
</section>

<section class="band" style="padding-top:0" id="coaches">
  <div class="wrap">
    {head_block("The coaches", 'Coaches who <span class="gold">still train.</span>', "Tell us your goal and we will match you with the coach who fits it.")}
    {team_cards()}
  </div>
</section>

<section class="band" style="padding-top:0" id="contest-prep">
  <div class="wrap split">
    <div class="tcard rv" style="pointer-events:none"><div class="tshot" style="aspect-ratio:4/3"><img loading="lazy" src="img/coach-chuck.webp" alt="Chuck, NPC contest prep coach in Vineland NJ"></div></div>
    <div class="prose rv">
      <span class="eyebrow">NPC contest prep · South Jersey</span>
      <h2>Prep with coaches who <span class="gold">have stepped on stage</span></h2>
      <p>Chuck has two decades of certification and multiple NPC overall titles. Lauren competes in NPC Bikini.</p>
      <ul class="ticks"><li>Offseason building and prep phases</li><li>Nutrition plans and regular check-ins</li><li>Posing coaching in our private posing room</li><li>Peak week and show-day plan</li><li>Home of Animal Fest, our annual bodybuilding show</li></ul>
      <p><a class="btn btn-gold" href="#consult">Book a prep consultation {ARROW}</a></p>
    </div>
  </div>
</section>

<section class="band" style="padding-top:0">
  <div class="wrap">
    {head_block("How it works", 'From first call to <span class="gold">first result.</span>')}
    <div class="timeline">
      <div class="tstep rv"><div class="n">1</div><span class="when">Free</span><h3>Consultation</h3><p>Sit down with a coach. Talk goals, history and schedule, and get clear pricing for training. No obligation.</p></div>
      <div class="tstep rv"><div class="n">2</div><span class="when">Once you sign up</span><h3>Your plan</h3><p>Training and nutrition built for you, plus a Fit3D scan so we have a real starting point.</p></div>
      <div class="tstep rv"><div class="n">3</div><span class="when">Every week</span><h3>Train and adjust</h3><p>Sessions, check-ins and changes to the plan as your body responds.</p></div>
    </div>
  </div>
</section>

<section class="band faq" style="padding-top:0" id="consult">
  <div class="wrap faq-grid">
    <div class="faq-list" style="align-content:start">{faq_html(FAQ_TRAIN)}</div>
    {tour_form("consult-form", "Book a free consultation")}
  </div>
</section>
{closer("Your coach", "is waiting.")}''')

# ================= LIONESS DEN =================
den_faq = [FAQ_AMEN[0], ("How do I get into the Lioness Den?", "Entry is code-locked. Platinum and Diamond members scan their QR code at the door to get in, so the space stays women only."), ("Which memberships include the Lioness Den?", "Platinum ($70 a month) and Diamond ($80 a month), both on 12-month agreements. Diamond also includes the Hibernation Station recovery room."),
           ("When is the Lioness Den open?", "The same hours as the main gym: every day from 4AM to 12AM."),
           ("Can women use the main floor too?", "Yes. Platinum and Diamond members have full access to the main floor and every amenity, plus the Lioness Den.")]
PAGES["lioness-den.html"] = dict(
    title="Women's-Only Gym Area in Vineland NJ | The Lioness Den",
    desc="The Lioness Den is a women's-only training space inside Animal Paradise Gyms, Vineland NJ, with its own free weights, machines and cables. Open 4AM to 12AM. From $70/mo.",
    slug="lioness-den", schemas=[crumbs_ld("Lioness Den", "lioness-den"), faq_ld(den_faq)],
    body=page_hero("Women only · Vineland, NJ", 'The <span class="gold">Lioness Den</span>', "A women's-only, code-locked training space with its own Booty Builder equipment, free weights, machines and cables. Same hours as the main floor. Train without an audience.", "Lioness Den", ctas=False, bg="lioness-den") + f'''
<section class="band">
  <div class="wrap split">
    {vid("vineland-gym-lioness-den","Video tour of the Lioness Den women's-only gym area with code-locked entry","Inside the Lioness Den")}
    <div class="prose rv">
      <span class="eyebrow">What's inside</span>
      <h2>Your own space. <span class="gold">The full gym too.</span></h2>
      <p>The Lioness Den gives women a dedicated area to train with no one watching. Entry is code-locked, so only women members get in. When you want the main floor, the turf or the sauna rooms, they are all included.</p>
      <ul class="ticks"><li>Code-locked entry, women only</li><li>Booty Builder equipment, free weights, machines and cables</li><li>Open every day 4AM to 12AM</li><li>Full main-floor access included</li><li>Towel service and cafe discount</li><li>Personal training with Lauren, booked separately</li></ul>
    </div>
  </div>
</section>

<section class="band mem">
  <div class="wrap">
    {head_block("Plans with the Lioness Den", 'Two ways in, <span class="gold">from $70.</span>', center=True)}
    <div class="cards two">{plan_card(PLANS[3])}{plan_card(PLANS[4])}</div>
  </div>
</section>

<section class="band">
  <div class="wrap split flip">
    <div class="tcard rv"><div class="tshot"><img loading="lazy" src="img/coach-lauren.webp" alt="Lauren, female personal trainer at Animal Paradise Gyms Vineland"></div></div>
    <div class="prose rv">
      <span class="eyebrow">Train with Lauren</span>
      <h2>A coach who <span class="gold">gets it.</span></h2>
      <p>Lauren is an NPC Bikini competitor who trains clients the way she trains herself: consistently, with a plan, and with patience. Whether it is your first program or your first show, she will build it with you.</p>
      <p><a class="btn btn-gold" href="personal-training.html#consult">Book a free consultation {ARROW}</a></p>
    </div>
  </div>
</section>

<section class="band faq" style="padding-top:0">
  <div class="wrap faq-grid">
    <div class="head rv" style="margin:0;align-content:start"><span class="eyebrow">Questions</span><h2>About the Den</h2></div>
    <div class="faq-list">{faq_html(den_faq)}</div>
  </div>
</section>
{closer("Come see", "the Den.")}''')

# ================= ABOUT =================
PAGES["about.html"] = dict(
    title="About Animal Paradise Gyms | Founded by Pete and Andrew | Vineland NJ",
    desc="Animal Paradise Gyms was built by Pete and Andrew inside Cumberland Mall in Vineland NJ. Our story, our values and the people behind South Jersey's best-equipped gym.",
    slug="about", schemas=[crumbs_ld("About", "about"), {"@context": "https://schema.org", "@type": "AboutPage", "about": GYM_ID, "url": SITE + "/about/"}],
    body=page_hero("About us", 'Built by lifters, <span class="gold">for everyone.</span>', "Animal Paradise started with two people who couldn't find the gym they wanted in South Jersey, so they built it.", "About", ctas=False, bg="animal-team-mural") + f'''
<section class="band">
  <div class="wrap">
    {founders_card()}
  </div>
</section>

<section class="band" style="padding-top:0">
  <div class="wrap split">
    <div class="prose rv">
      <span class="eyebrow">Our story</span>
      <h2>A gym in a mall. <span class="gold">Nobody expected this.</span></h2>
      <p>Pete and Andrew set out to bring competition-grade equipment to Vineland. They put it inside Cumberland Mall so it would be easy to get to, with free parking at the door and hours that fit real schedules: <strong>4AM to midnight, every day.</strong></p>
      <p>Then they added the things members kept asking for: a recovery room, a women's-only training space, a cafe, a supplement store, daycare and coaches who still compete.</p>
      <p>One visiting member put it simply: he can't find equipment like this even in Boston.</p>
    </div>
    {ph("img/photos/vineland-gym-animal-team-mural.webp", "Animal Team bodybuilder mural inside Animal Paradise Gyms")}
  </div>
</section>

<section class="band" style="padding-top:0">
  <div class="wrap">
    {head_block("What we stand for", 'Four words on <span class="gold">the wall.</span>')}
    <div class="cards four">
      {card("bolt", "Strength", "Mental, emotional and earned. Discipline is the part nobody posts about.")}
      {card("users", "Community", "We're a crew, not a crowd. You get known here, not processed.")}
      {card("back", "Evolution", "Constant improvement, for you and for the gym. We keep adding what members need.")}
      {card("shield", "Integrity", "No gimmicks. Straight answers on price. Real effort and real progress.")}
    </div>
  </div>
</section>

<section class="band" style="padding-top:0">
  <div class="wrap split flip">
    {ph("img/photos/vineland-gym-animal-fest-belt.webp", "Animal Fest III champion belt from Animal Paradise Gyms")}
    <div class="prose rv">
      <span class="eyebrow">Animal Fest</span>
      <h2>Our biggest day <span class="gold">of the year.</span></h2>
      <p>Every year we host Animal Fest: guest posing, competitions, vendors and the whole crew under one roof. The third Animal Fest took place in October 2026. Follow us on Instagram to hear first about the next one.</p>
      <p><a class="btn btn-gold" href="animal-fest-3.html">Animal Fest 3 recap {ARROW}</a></p>
      <p><a class="btn btn-glass" target="_blank" rel="noopener" href="https://www.instagram.com/animalparadisegyms">Follow on Instagram {ARROW}</a></p>
    </div>
  </div>
  <div class="wrap cards" style="margin-top:14px">
    <div class="ph rv" style="aspect-ratio:3/4"><img loading="lazy" src="img/photos/vineland-gym-animal-fest-medal.webp" alt="Animal Fest 3 finisher medal"></div>
    <div class="ph rv" style="aspect-ratio:3/4"><img loading="lazy" src="img/photos/vineland-gym-animal-fest-medal-2.webp" alt="Animal Fest 3 medal on the champion belt"></div>
    <div class="ph rv" style="aspect-ratio:3/4"><img loading="lazy" src="img/photos/vineland-gym-animal-fest-medals.webp" alt="Animal Fest 3 medals and ribbons"></div>
  </div>
</section>

<section class="band" style="padding-top:0">
  <div class="wrap">
    {head_block("The coaching team", 'Meet the <span class="gold">coaches.</span>')}
    {team_cards()}
  </div>
</section>
{closer("Come meet", "the crew.")}''')

# ================= FAQ =================
ALL_FAQ = [("Hours and location", FAQ_HOURS), ("Memberships and pricing", FAQ_MEM), ("Training and coaching", [q for q in FAQ_TRAIN if q not in FAQ_MEM]), ("Amenities", FAQ_AMEN)]
faq_groups = "".join(f'<div class="faq-group rv"><h2>{t}</h2>{faq_html(q, open_first=(i == 0))}</div>' for i, (t, q) in enumerate(ALL_FAQ))
PAGES["faq.html"] = dict(
    title="Animal Paradise Gyms FAQ | Hours, Prices, Contracts | Vineland NJ",
    desc="Answers about Animal Paradise Gyms in Vineland NJ: hours (4AM to 12AM daily), membership prices, contracts, day passes, personal training, the Lioness Den, sauna and parking.",
    slug="faq", schemas=[crumbs_ld("FAQ", "faq"), faq_ld([x for _, g in ALL_FAQ for x in g])],
    body=page_hero("FAQ", 'Straight <span class="gold">answers.</span>', "Everything people ask before they join. Still not sure? Call (856) 839-4536 and a real person picks up.", "FAQ", ctas=False, bg="surf-machine") + f'''
<section class="band faq">
  <div class="wrap faq-grid">
    <div class="head" style="margin:0;align-content:start;position:sticky;top:110px">
      <span class="eyebrow">Jump to</span>
      <ul class="ticks">{"".join(f"<li>{t}</li>" for t, _ in ALL_FAQ)}</ul>
      <p style="margin-top:12px"><a class="btn btn-gold" href="visit.html#tour">Book a free tour {ARROW}</a></p>
    </div>
    <div>{faq_groups}</div>
  </div>
</section>
{closer("Still curious?", "Come see it.")}''')

# ================= VISIT =================
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
hours_rows = "".join(f'<tr data-day="{d}"><td>{d}</td><td>4:00 AM to 12:00 AM</td></tr>' for d in days)
PAGES["visit.html"] = dict(
    title="Visit Animal Paradise Gyms | Cumberland Mall, Vineland NJ | Hours",
    desc="Find Animal Paradise Gyms inside Cumberland Mall, 3849 S Delsea Dr, Vineland NJ 08360. Open every day 4AM to 12AM. Free parking. Book a free tour.",
    slug="visit", schemas=[crumbs_ld("Visit", "visit"), GYM_LD],
    body=page_hero("Visit us · Vineland, NJ", 'Find us at <span class="gold">Cumberland Mall.</span>', "Free parking at the door, open every day from 4AM to midnight. Book a free tour and see every area before you join.", "Visit", ctas=False, bg="lounge") + f'''
<section class="band">
  <div class="wrap visit-grid">
    <div class="map-card rv">
      <i class="pin"></i>
      <div style="display:grid;gap:14px"><span class="eyebrow">Address</span><h2 style="font-size:clamp(26px,3.4vw,40px)">3849 S Delsea Dr, Suite E000</h2><p class="lede" style="color:var(--ink)">Cumberland Mall, Vineland, NJ 08360</p></div>
      <dl class="nap">
        <div><dt>Phone</dt><dd>(856) 839-4536</dd></div>
        <div><dt>Email</dt><dd>Info@AnimalParadiseGyms.com</dd></div>
        <div><dt>Parking</dt><dd>Free, right outside</dd></div>
        <div><dt>Suite</dt><dd>E000, inside the mall</dd></div>
      </dl>
      <a class="btn btn-glass" style="justify-self:start" target="_blank" rel="noopener" href="{MAPS}">Get directions {ARROW}</a>
    </div>
    {tour_form()}
  </div>
</section>

<section class="band" style="padding-top:0">
  <div class="wrap split">
    <div class="prose rv">
      <span class="eyebrow">Hours</span>
      <h2>Open <span class="gold">20 hours</span> a day</h2>
      <table class="hours">{hours_rows}</table>
      <p class="fine">The Lioness Den, Animal Cafe and Animal Supps keep the same hours as the gym.</p>
    </div>
    <div class="prose rv">
      <span class="eyebrow">Nearby</span>
      <h2>Close to <span class="gold">home.</span></h2>
      <p>Members drive in from across Cumberland, Gloucester and Salem counties.</p>
      <ul class="ticks"><li><strong>Millville:</strong> about 15 minutes</li><li><strong>Bridgeton:</strong> about 20 minutes</li><li><strong>Glassboro:</strong> about 30 minutes</li><li><strong>Buena and Newfield:</strong> about 15 minutes</li></ul>
    </div>
  </div>
</section>
{closer("See you", "on the floor.")}''')


# ================= CAFE + SUPPS + COACH PAGES =================
CAFE_EXT = "https://animalcafe.net/"
SUPPS_EXT = "https://animalsupps.co/"
SAVE_TABLE = '''<div class="tbl-wrap rv" style="margin-top:0"><table class="tbl" style="min-width:520px">
<thead><tr><th>Your plan</th><th>Silver</th><th>Gold</th><th>Premium</th><th>Platinum</th><th>Diamond</th></tr></thead>
<tbody><tr><td>{label}</td><td class="n">·</td><td>5% off</td><td class="y">10% off</td><td class="y">10% off</td><td class="y">10% off</td></tr></tbody></table></div>'''

HOURS_SPEC = [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "04:00", "closes": "24:00"}]
ADDR = GYM_LD["address"]

def biz_ld(t, name, desc, slug, extra):
    d = {"@context": "https://schema.org", "@type": t, "name": name, "description": desc, "url": f"{SITE}/{slug}/",
         "telephone": "+1-856-839-4536", "address": ADDR, "openingHoursSpecification": HOURS_SPEC,
         "containedInPlace": GYM_ID, "parentOrganization": GYM_ID}
    d.update(extra)
    return {k: v for k, v in d.items() if v is not None}

CAFE_FAQ = [
    ("Where is Animal Cafe?", "Animal Cafe is inside Animal Paradise Gyms at Cumberland Mall, 3849 S Delsea Dr, Suite E000, Vineland, NJ 08360."),
    ("What are Animal Cafe's hours?", "The cafe keeps the same hours as the gym: every day from 4AM to 12AM."),
    ("What does Animal Cafe serve?", "Protein shakes, smoothies, açaí bowls built to order, cold-pressed juices, wellness shots and coffee."),
    ("Do members get a discount at the cafe?", "Yes. Gold members save 5%. Premium, Platinum and Diamond members save 10%."),
]
SUPPS_FAQ = [
    ("Where can I buy supplements in Vineland?", "Animal Supps is the supplement store inside Animal Paradise Gyms at Cumberland Mall, Vineland NJ, open every day from 4AM to 12AM, and online at animalsupps.co."),
    ("What does Animal Supps carry?", "Over 100 brands and hundreds of products: pre-workout, protein, creatine, aminos, recovery, weight loss support, vitamins and snacks. Brands include NutraBio, Axe & Sledge, Bucked Up, Raw Nutrition, Mutant, Redcon1, Dymatize, Cellucor, Quest and Momentous."),
    ("Are the supplements authentic?", "Yes. Animal Supps buys direct from the brands, so everything on the shelf is 100% authentic with no grey-market stock."),
    ("Can I order Animal Supps online?", "Yes. Order at animalsupps.co for delivery, or order online and pick it up free in store at the gym."),
    ("Do members get a supplement discount?", "Yes. Gold members save 5%. Premium, Platinum and Diamond members save 10%."),
]

PAGES["animal-cafe.html"] = dict(
    title="Animal Cafe | Protein Shakes and Açaí Bowls in Vineland NJ",
    desc="Animal Cafe inside Animal Paradise Gyms, Cumberland Mall, Vineland NJ. Protein shakes, smoothies, açaí bowls, cold-pressed juice and coffee. Open 4AM to 12AM daily.",
    slug="animal-cafe",
    schemas=[crumbs_ld("Animal Cafe", "animal-cafe"), faq_ld(CAFE_FAQ),
             biz_ld("CafeOrCoffeeShop", "Animal Cafe", "Protein shakes, smoothies, açaí bowls, cold-pressed juice, wellness shots and coffee inside Animal Paradise Gyms.", "animal-cafe",
                    {"sameAs": [CAFE_EXT], "servesCuisine": ["Smoothies", "Açaí bowls", "Juice", "Coffee"], "image": SITE + "/img/photos/vineland-gym-animal-cafe.webp"})],
    body=page_hero("Animal Cafe · Inside the gym", 'Fuel <span class="gold">before and after</span> the work.', "Protein shakes, açaí bowls, cold-pressed juice and coffee, made inside Animal Paradise. Open 4AM to midnight, the same hours you train.", "Animal Cafe", ctas=False, bg="animal-cafe-2").replace('</h1>', '</h1>', 1).replace('<p class="lede" style="color:rgba(242,236,223,.82)">Protein', '<p class="lede" style="color:rgba(242,236,223,.82)">Protein', 1) + f'''
<section class="band">
  <div class="wrap split">
    <div class="ph rv" style="aspect-ratio:4/5"><img loading="lazy" src="img/photos/vineland-gym-animal-cafe-counter.webp" alt="Animal Cafe counter in Vineland NJ" onerror="this.remove()"></div>
    <div class="prose rv">
      <span class="eyebrow">On the menu</span>
      <h2>Built for <span class="gold">people who train.</span></h2>
      <p>Most gym cafes are a fridge of drinks. Animal Cafe makes shakes, bowls and juice to order, so your post-workout meal is ready before you've wiped down the bench.</p>
      <div class="cards two" style="margin-top:10px">
        {card("cup", "Protein shakes and smoothies", "Blended to order, before or after your session.")}
        {card("leaf", "Açaí bowls", "Built to order with your toppings.")}
        {card("bolt", "Cold-pressed juice", "Plus wellness shots for a quick hit.")}
        {card("flame", "Coffee", "For the 4AM crew and the late-night lifters.")}
      </div>
      <p style="margin-top:8px"><a class="btn btn-gold" target="_blank" rel="noopener" href="{CAFE_EXT}">See the full cafe menu {ARROW}</a></p>
    </div>
  </div>
</section>

<section class="band" style="padding-top:0">
  <div class="wrap">
    {head_block("How members use it", 'Order now, <span class="gold">grab it on the way out.</span>')}
    <div class="timeline">
      <div class="tstep rv"><div class="n">1</div><span class="when">Walking in</span><h3>Order at the counter</h3><p>Tell the cafe what you want and when you'll be done training.</p></div>
      <div class="tstep rv"><div class="n">2</div><span class="when">Training</span><h3>Do the work</h3><p>Your shake or bowl gets made while you lift.</p></div>
      <div class="tstep rv"><div class="n">3</div><span class="when">Walking out</span><h3>Refuel</h3><p>Pick it up on the way out. Members save up to 10%.</p></div>
    </div>
  </div>
</section>

<section class="band mem">
  <div class="wrap">
    {head_block("Member savings", 'Your membership <span class="gold">pays you back.</span>', "Every 12-month plan includes a discount at Animal Cafe and Animal Supps.", center=True)}
    {SAVE_TABLE.format(label="Animal Cafe discount")}
    <div class="center-row"><a class="btn btn-glass" href="memberships.html">Compare memberships {ARROW}</a></div>
  </div>
</section>

<section class="band" style="padding-top:0">
  <div class="wrap split flip">
    {ph("img/photos/vineland-gym-animal-supps.webp", "Animal Supps supplement store next to Animal Cafe")}
    <div class="prose rv">
      <span class="eyebrow">Right next door</span>
      <h2>Restock at <span class="gold">Animal Supps.</span></h2>
      <p>Out of pre-workout or protein? The supplement store is a few steps from the cafe, with staff who actually train.</p>
      <p><a class="btn btn-glass" href="animal-supps.html">Visit Animal Supps {ARROW}</a></p>
    </div>
  </div>
</section>

<section class="band faq" style="padding-top:0">
  <div class="wrap faq-grid">
    <div class="head rv" style="margin:0;align-content:start"><span class="eyebrow">Cafe questions</span><h2>Good to know</h2></div>
    <div class="faq-list">{faq_html(CAFE_FAQ)}</div>
  </div>
</section>
{closer("Train hard.", "Eat well.")}''')

PAGES["animal-supps.html"] = dict(
    title="Animal Supps | Supplement Store in Vineland NJ | Protein, Pre-Workout",
    desc="Animal Supps supplement store inside Animal Paradise Gyms, Cumberland Mall, Vineland NJ. Pre-workout, protein, creatine and aminos. Open 4AM to 12AM. Shop in store or online at animalsupps.co.",
    slug="animal-supps",
    schemas=[crumbs_ld("Animal Supps", "animal-supps"), faq_ld(SUPPS_FAQ),
             biz_ld("Store", "Animal Supps", "Supplement store inside Animal Paradise Gyms carrying pre-workout, protein, creatine and aminos.", "animal-supps",
                    {"image": SITE + "/img/photos/vineland-gym-animal-supps.webp", "sameAs": [SUPPS_EXT]})],
    body=page_hero("Animal Supps · Vineland, NJ", 'The supplement store <span class="gold">on the gym floor.</span>', "Over 100 brands of pre-workout, protein, creatine and recovery, bought direct and picked by people who train. Open 4AM to midnight, or order online for delivery or free pickup.", "Animal Supps", ctas=False, bg="animal-supps") + f'''
<section class="band">
  <div class="wrap">
    {head_block("What we stock", 'Everything to <span class="gold">train and recover.</span>', "Over 100 brands, all bought direct from the brand. If our staff wouldn't take it, it's not on the shelf.")}
    <div class="cards four">
      {card("bolt", "Pre-workout", "Energy and focus for 4AM sessions and late-night lifts.")}
      {card("plate", "Protein", "Whey, isolates and blends for every goal and budget.")}
      {card("trophy", "Creatine", "The most researched supplement for strength and size.")}
      {card("back", "Aminos and recovery", "Intra-workout and recovery support between sessions.")}
    </div>
    <div class="chips" style="margin-top:28px;justify-content:center" aria-label="Supplement brands at Animal Supps"><span>NutraBio</span><span>Axe &amp; Sledge</span><span>Bucked Up</span><span>Raw Nutrition</span><span>Mutant</span><span>Redcon1</span><span>Dymatize</span><span>Cellucor</span><span>Quest</span><span>Momentous</span><span>and 100+ more</span></div>
  </div>
</section>

<section class="band" style="padding-top:0">
  <div class="wrap split">
    <div class="ph rv" style="aspect-ratio:4/5"><img loading="lazy" src="img/photos/vineland-gym-animal-supps-2.webp" alt="Animal Supps supplement shelves inside Animal Paradise Gyms" onerror="this.remove()"></div>
    <div class="prose rv">
      <span class="eyebrow">Why buy here</span>
      <h2>Advice from people <span class="gold">who actually lift.</span></h2>
      <p>Online stores sell you what's on sale. Animal Supps staff train on the same floor you do, so they can tell you what fits your goal, your budget and your training.</p>
      <ul class="ticks"><li>Over 100 brands, 100% authentic, bought direct</li><li>Staff who train and can advise</li><li>Open every day 4AM to 12AM</li><li>Members save up to 10%</li><li>Order online for delivery or free in-store pickup</li></ul>
      <p style="margin-top:8px"><a class="btn btn-gold" target="_blank" rel="noopener" href="{SUPPS_EXT}">Shop Animal Supps online {ARROW}</a></p>
    </div>
  </div>
</section>

<section class="band mem">
  <div class="wrap">
    {head_block("Member savings", 'Members save <span class="gold">up to 10%.</span>', "Every 12-month plan includes a discount at Animal Supps and Animal Cafe.", center=True)}
    {SAVE_TABLE.format(label="Animal Supps discount")}
    <div class="center-row"><a class="btn btn-glass" href="memberships.html">Compare memberships {ARROW}</a></div>
  </div>
</section>

<section class="band" style="padding-top:0">
  <div class="wrap split flip">
    {ph("img/photos/vineland-gym-animal-cafe.webp", "Animal Cafe next to Animal Supps")}
    <div class="prose rv">
      <span class="eyebrow">Right next door</span>
      <h2>Mix it at <span class="gold">Animal Cafe.</span></h2>
      <p>Grab your protein here and have it blended into a shake at the cafe, a few steps away.</p>
      <p><a class="btn btn-glass" href="animal-cafe.html">Visit Animal Cafe {ARROW}</a></p>
    </div>
  </div>
</section>

<section class="band faq" style="padding-top:0">
  <div class="wrap faq-grid">
    <div class="head rv" style="margin:0;align-content:start"><span class="eyebrow">Supplement questions</span><h2>Good to know</h2></div>
    <div class="faq-list">{faq_html(SUPPS_FAQ)}</div>
  </div>
</section>
{closer("Stock up", "on the way out.")}''')

# ---------- coach profile pages ----------
COACH_PAGES = {
    "chuck": dict(
        h1='Chuck, <span class="gold">contest prep coach</span>',
        lede="Two decades of certification and a shelf of NPC overall titles. Chuck has been on both sides of a prep.",
        title="Chuck | NPC Contest Prep Coach in Vineland NJ | Animal Paradise",
        desc="Train with Chuck, NPC contest prep coach at Animal Paradise Gyms in Vineland NJ. Two decades certified with multiple NPC overall titles. Book a free consultation.",
        about=["Chuck has spent two decades as a certified coach and has won multiple NPC overall titles on stage. That means he has lived every part of a prep: the offseason, the diet, the posing practice and the last few weeks when everything gets hard.",
               "He coaches competitors preparing for the stage, and lifters who just want to build serious size and strength without stepping on stage."],
        best=["First-time competitors", "Experienced NPC athletes", "Building size and strength", "Posing and peak week"],
        offers=["Full contest prep coaching", "Offseason building plans", "Posing sessions in our posing room", "Nutrition and check-ins"],),
    "hakim": dict(
        h1='Hakim, <span class="gold">NASM certified trainer</span>',
        lede="An exercise science degree, three years on the floor and a clinical background from Inspira.",
        title="Hakim | NASM Certified Personal Trainer in Vineland NJ | Animal Paradise",
        desc="Train with Hakim, NASM certified personal trainer at Animal Paradise Gyms in Vineland NJ. Exercise science degree and clinical background. Book a free consultation.",
        about=["Hakim holds an exercise science degree and is NASM certified. Before coaching full time he worked in a clinical setting at Inspira, which shapes how he coaches: technique first, then load.",
               "He has spent three years on the gym floor helping members learn the basics, return from time off and build a routine that sticks."],
        best=["First-time gym members", "Getting back into training", "General strength and fitness", "Weight loss"],
        offers=["One-on-one training", "Beginner programs", "Technique coaching", "Fit3D progress tracking"],),
    "lauren": dict(
        h1='Lauren, <span class="gold">NPC Bikini competitor</span>',
        lede="Trains clients the way she trains herself: consistently, with a plan, and with patience.",
        title="Lauren | Female Personal Trainer in Vineland NJ | Animal Paradise",
        desc="Train with Lauren, NPC Bikini competitor and personal trainer at Animal Paradise Gyms in Vineland NJ. Bikini prep, glute and strength training. Book a free consultation.",
        about=["Lauren competes in the NPC Bikini division, so she knows what it takes to build a stage-ready physique and how much consistency matters along the way.",
               "She coaches women who are new to lifting, women who want to build strength and shape, and competitors preparing for their first bikini show."],
        best=["Women new to lifting", "Glute and lower-body focus", "First bikini show", "Building consistency"],
        offers=["One-on-one training", "Bikini contest prep", "Posing practice", "Training in the Lioness Den"],),
}

def coach_page(c):
    d = COACH_PAGES[c["slug"]]
    others = "".join(
        f'<a class="tcard rv" href="coach-{o["slug"]}.html"><div class="tshot"><img loading="lazy" src="{o["img"]}" alt="{o["alt"]}"></div><div class="tbody"><span class="role">{o["role"]}</span><h3>{o["name"]}</h3><span class="more">View profile →</span></div></a>'
        for o in COACHES if o["slug"] != c["slug"])
    crumb = f'<ol class="crumbs"><li><a href="index.html">Home</a></li><li><a href="personal-training.html">Personal Training</a></li><li aria-current="page">{c["name"]}</li></ol>'
    body = f'''
<section class="page-hero">
  <div class="wrap split" style="align-items:end">
    <div>
      <nav aria-label="Breadcrumb">{crumb}</nav>
      <p class="eyebrow" style="margin-top:28px">Coach · Animal Paradise Gyms</p>
      <h1 style="max-width:12ch">{d["h1"]}</h1>
      <p class="lede" style="color:rgba(242,236,223,.82)">{d["lede"]}</p>
      <div class="hero-cta"><a class="btn btn-gold" href="#book">Train with {c["name"]} {ARROW}</a><a class="btn btn-glass" href="personal-training.html">All coaching</a></div>
    </div>
    <div class="tcard" style="max-width:460px;justify-self:end;width:100%"><div class="tshot"><img src="{c["img"]}" alt="{c["alt"]}" fetchpriority="high"></div></div>
  </div>
</section>

<section class="band">
  <div class="wrap split" style="align-items:start">
    <div class="prose rv">
      <span class="eyebrow">About {c["name"]}</span>
      <h2>Meet <span class="gold">{c["name"]}.</span></h2>
      {"".join(f"<p>{p}</p>" for p in d["about"])}
    </div>
    <div style="display:grid;gap:14px">
      <div class="who-card rv"><span class="eyebrow">Best for</span><ul class="ticks">{"".join(f"<li>{x}</li>" for x in d["best"])}</ul></div>
      <div class="who-card rv"><span class="eyebrow">Coaching with {c["name"]}</span><ul class="ticks">{"".join(f"<li>{x}</li>" for x in d["offers"])}</ul></div>
    </div>
  </div>
</section>


<section class="band" style="padding-top:0" id="book">
  <div class="wrap visit-grid">
    <div class="map-card rv">
      <div style="display:grid;gap:14px"><span class="eyebrow">First session</span><h2 style="font-size:clamp(28px,3.6vw,44px)">Your first consultation <span class="gold">is free.</span></h2>
      <p class="lede">Sit down with {c["name"]}, talk through your goal and find out how training works and what it costs. Personal training is separate from your gym membership.</p></div>
      <ul class="ticks"><li>Goal and history review</li><li>Training options and pricing</li><li>No obligation to sign up</li></ul>
    </div>
    {tour_form(f"book-{c['slug']}", f"Book with {c['name']}")}
  </div>
</section>

<section class="band" style="padding-top:0">
  <div class="wrap">
    {head_block("More coaches", 'Meet the <span class="gold">rest of the team.</span>')}
    <div class="cards two">{others}</div>
  </div>
</section>
{closer("Train with", c["name"] + ".")}'''
    person = {"@context": "https://schema.org", "@type": "Person", "name": c["name"], "jobTitle": c["role"],
              "description": d["about"][0], "image": f'{SITE}/{c["img"]}', "worksFor": GYM_ID,
              "url": f'{SITE}/trainer/{c["slug"]}/', "knowsAbout": d["best"]}
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Personal Training", "item": SITE + "/personal-training/"},
        {"@type": "ListItem", "position": 3, "name": c["name"], "item": f'{SITE}/trainer/{c["slug"]}/'}]}
    return dict(title=d["title"], desc=d["desc"], slug=f'trainer/{c["slug"]}', schemas=[person, bc], body=body, nav_active="personal-training.html")

for c in COACHES:
    PAGES[f'coach-{c["slug"]}.html'] = coach_page(c)


# ================= EVENTS + ANIMAL FEST 3 =================
FEST_LD = {"@context": "https://schema.org", "@type": "Event", "name": "Animal Fest 3",
    "description": "The third annual Animal Fest at Animal Paradise Gyms: guest posing, competitions, vendors and the whole crew under one roof.",
    "startDate": "2026-10-10", "eventStatus": "https://schema.org/EventScheduled",
    "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
    "location": {"@type": "Place", "name": "Animal Paradise Gyms, Cumberland Mall", "address": GYM_LD["address"]},
    "organizer": GYM_ID, "image": [SITE + "/img/photos/vineland-gym-animal-fest-belt.webp", SITE + "/img/photos/vineland-gym-animal-fest-medal.webp"],
    "url": SITE + "/animal-fest-3/"}

FEST_GALLERY = [("animal-fest-belt", "Animal Fest III champion belt"), ("animal-fest-medal", "Animal Fest 3 medal"),
                ("animal-fest-medal-2", "Animal Fest 3 medal on the champion belt"), ("animal-fest-medals", "Animal Fest 3 medals and ribbons"),
                ("posing-room", "Posing room at Animal Paradise used by Animal Fest competitors"), ("animal-team-mural", "Animal Team mural at Animal Paradise Gyms")]

def fest_gallery():
    return '<div class="gallery-grid">' + "".join(
        f'<div class="ph rv"><img loading="lazy" src="img/photos/vineland-gym-{k}.webp" alt="{a}"></div>' for k, a in FEST_GALLERY) + "</div>"

PAGES["events.html"] = dict(
    title="Events at Animal Paradise Gyms | Animal Fest | Vineland NJ",
    desc="Bodybuilding shows, guest posing and community events at Animal Paradise Gyms in Vineland NJ, home of Animal Fest. See past events and what's coming next.",
    slug="events", schemas=[crumbs_ld("Events", "events"), {"@context": "https://schema.org", "@type": "ItemList", "name": "Animal Paradise Gyms events",
        "itemListElement": [{"@type": "ListItem", "position": 1, "url": SITE + "/animal-fest-3/", "name": "Animal Fest 3"}, {"@type": "ListItem", "position": 2, "url": SITE + "/animal-fest-2/", "name": "Animal Fest 2"}]}],
    body=page_hero("Events · Vineland, NJ", 'More than <span class="gold">a gym.</span>', "Bodybuilding shows, guest posing, vendors and nights the whole crew shows up for. This is where South Jersey's training community gets together.", "Events", ctas=False, bg="animal-fest-belt") + f'''
<section class="band">
  <div class="wrap">
    {head_block("Next up", 'The next event <span class="gold">is in the works.</span>', "Follow us on Instagram or ask at the front desk to hear first when dates are announced.")}
    <div class="founders-card rv" style="grid-template-columns:1fr 1fr">
      <div class="ph" style="border-radius:0;min-height:320px"><img loading="lazy" src="img/photos/vineland-gym-posing-room.webp" alt="Posing room at Animal Paradise Gyms"></div>
      <div class="tbody">
        <span class="role">Coming soon</span>
        <h3>Stay in the loop</h3>
        <p>Competitions, guest posing, seminars and member nights. Announcements go out on Instagram first.</p>
        <div class="hero-cta" style="margin-top:6px"><a class="btn btn-gold" target="_blank" rel="noopener" href="https://www.instagram.com/animalparadisegyms">Follow on Instagram {ARROW}</a></div>
      </div>
    </div>
  </div>
</section>

<section class="band" style="padding-top:0">
  <div class="wrap">
    {head_block("Past events", 'From the <span class="gold">archive.</span>')}
    <div class="cards two">
      <a class="tile rv" style="min-height:440px;text-decoration:none" href="animal-fest-3.html">
        <div class="ph"><img loading="lazy" src="img/photos/vineland-gym-animal-fest-belt.webp" alt="Animal Fest III champion belt"></div>
        <div class="tile-body"><span class="tag">October 10, 2026</span><h3 style="font-size:clamp(24px,2.6vw,32px)">Animal Fest 3</h3><p>Our biggest day of the year. Guest posing, competitions, vendors and the whole crew under one roof.</p><span class="textlink">See the recap →</span></div>
      </a>
      <div class="tile dark rv" style="min-height:440px"><div class="tile-body"><span class="tag">Annual</span><h3 style="font-size:clamp(24px,2.6vw,32px)">Animal Fest is back every year</h3><p>Competing next time? Our coaches run full contest prep, and members train for show day in our private posing room.</p><a class="textlink" href="personal-training.html">Contest prep coaching →</a></div></div>
    </div>
    <a class="tile rv" style="min-height:440px;margin-top:14px;text-decoration:none" href="animal-fest-2.html">
      <div class="ph"><img loading="lazy" src="img/events/animal-fest-2-crowd-gym-floor.webp" alt="Crowd on the gym floor at Animal Fest 2, Animal Paradise Gyms"></div>
      <div class="tile-body"><span class="tag">October 25, 2025</span><h3 style="font-size:clamp(24px,2.6vw,32px)">Animal Fest 2</h3><p>Vendors, guest athletes, medals on stage and a packed gym floor. Where the Animal Fest tradition grew up.</p><span class="textlink">See the recap →</span></div>
    </a>
  </div>
</section>
{closer("Be part of", "the next one.")}''')

PAGES["animal-fest-3.html"] = dict(
    title="Animal Fest 3 | Bodybuilding Event at Animal Paradise Gyms, Vineland NJ",
    desc="Animal Fest 3 took place October 10, 2026 at Animal Paradise Gyms, Cumberland Mall, Vineland NJ. Guest posing, competitions, vendors, medals and the Animal Fest III champion belt.",
    slug="animal-fest-3",
    schemas=[FEST_LD, {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Events", "item": SITE + "/events/"},
        {"@type": "ListItem", "position": 3, "name": "Animal Fest 3", "item": SITE + "/animal-fest-3/"}]}],
    nav_active="events.html",
    body=page_hero("October 10, 2026 · Cumberland Mall", 'Animal Fest <span class="gold">3</span>', "Our third annual Animal Fest brought guest posing, competitions, vendors and the whole crew together under one roof at Animal Paradise.", "Animal Fest 3", ctas=False, bg="animal-fest-belt").replace('<li><a href="index.html">Home</a></li>', '<li><a href="index.html">Home</a></li><li><a href="events.html">Events</a></li>') + f'''
<section class="band">
  <div class="wrap split">
    <div class="prose rv">
      <span class="eyebrow">The recap</span>
      <h2>Our biggest day <span class="gold">of the year.</span></h2>
      <p>On October 10, 2026, Animal Paradise hosted the third edition of Animal Fest. Competitors, guest posers, vendors and members came together for the biggest day on our calendar.</p>
      <ul class="ticks"><li>Guest posing</li><li>Competitions</li><li>Vendors on site</li><li>Medals for competitors and the Animal Fest III champion belt</li></ul>
    </div>
    <div class="ph rv" style="aspect-ratio:4/5"><img loading="lazy" src="img/photos/vineland-gym-animal-fest-medal.webp" alt="Animal Fest 3 medal reading Unleash your inner animal"></div>
  </div>
</section>

<section class="band" style="padding-top:0" id="gallery">
  <div class="wrap">
    {head_block("Gallery", 'Animal Fest 3 <span class="gold">in photos.</span>')}
    <!-- EVENT PHOTOS: add Animal Fest 3 photos here -->
    {fest_gallery()}
  </div>
</section>

<section class="band" style="padding-top:0">
  <div class="wrap split flip">
    <div class="tcard rv" style="pointer-events:none"><div class="tshot" style="aspect-ratio:4/3"><img loading="lazy" src="img/coach-chuck.webp" alt="Chuck, contest prep coach at Animal Paradise"></div></div>
    <div class="prose rv">
      <span class="eyebrow">Next year</span>
      <h2>Want to compete at <span class="gold">Animal Fest 4?</span></h2>
      <p>Start prep with coaches who have stood on stage. Chuck and Lauren coach competitors through training, nutrition, posing and peak week.</p>
      <div class="hero-cta" style="margin-top:6px"><a class="btn btn-gold" href="personal-training.html">Contest prep coaching {ARROW}</a><a class="btn btn-glass" href="animal-fest-2.html">Animal Fest 2 recap</a></div>
    </div>
  </div>
</section>
{closer("See you at", "Animal Fest 4.")}''')


# ================= BLOG =================
import datetime as _dt
exec(open("posts.py").read())
POSTS.sort(key=lambda p: p["date"], reverse=True)

def _fmt(d):
    x = _dt.date.fromisoformat(d)
    return x.strftime("%B ") + str(x.day) + x.strftime(", %Y")

def _mins(p):
    return max(3, round(len(re.sub(r"<[^>]+>", " ", p["body"] + (p["lead"] or "")).split()) / 200))

def post_card(p, big=False):
    h = "clamp(22px,2.4vw,30px)" if big else "20px"
    return (f'<a class="pcard rv{" big" if big else ""}" href="{p["slug"]}.html">'
            f'<div class="ph"><img loading="lazy" src="img/photos/vineland-gym-{p["img"]}.webp" alt="{p["title"]}"></div>'
            f'<div class="pbody"><span class="pmeta"><span class="pcat">{p["cat"]}</span> · {_fmt(p["date"])} · {_mins(p)} min read</span>'
            f'<h3 style="font-size:{h}">{p["title"]}</h3><p>{p["desc"]}</p><span class="textlink">Read article →</span></div></a>')

def latest_posts_band(n=3, title='From the <span class="gold">floor.</span>', eyebrow="Blog"):
    cards = "".join(post_card(p) for p in POSTS[:n])
    return f'''<section class="band" style="padding-top:0">
  <div class="wrap">
    {head_block(eyebrow, title, "Training, nutrition and gym advice from the Animal Paradise team.")}
    <div class="pgrid">{cards}</div>
    <div class="center-row"><a class="btn btn-glass" href="blog.html">All articles {ARROW}</a></div>
  </div>
</section>'''

def related_band(slugs, title="Keep reading"):
    ps = [p for s in slugs for p in POSTS if p["slug"] == s]
    if not ps: return ""
    return f'''<section class="band" style="padding-top:0">
  <div class="wrap">
    {head_block("From the blog", title)}
    <div class="pgrid">{"".join(post_card(p) for p in ps)}</div>
  </div>
</section>'''

cats = []
for p in POSTS:
    if p["cat"] not in cats: cats.append(p["cat"])
chips = '<button class="chip" aria-pressed="true" data-cat="all">All</button>' + "".join(f'<button class="chip" aria-pressed="false" data-cat="{c}">{c}</button>' for c in cats)
grid = "".join(post_card(p).replace('<a class="pcard', f'<a data-cat="{p["cat"]}" class="pcard', 1) for p in POSTS[1:])
PAGES["blog.html"] = dict(
    title="Animal Paradise Blog | Training, Nutrition and Gym Advice | Vineland NJ",
    desc="Training, nutrition, contest prep and recovery advice from Animal Paradise Gyms in Vineland NJ. Beginner guides, membership costs and local gym tips.",
    slug="blog",
    schemas=[crumbs_ld("Blog", "blog"), {"@context": "https://schema.org", "@type": "Blog", "name": "Animal Paradise Blog", "url": SITE + "/blog/", "publisher": GYM_ID,
             "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": f'{SITE}/{p["slug"]}/', "datePublished": p["date"]} for p in POSTS]}],
    body=page_hero("Blog · Animal Paradise", 'From the <span class="gold">floor.</span>', "Training, nutrition, recovery and contest prep advice from the people who run South Jersey's best-equipped gym.", "Blog", ctas=False, bg="squat-rack-training") + f'''
<section class="band">
  <div class="wrap">
    {post_card(POSTS[0], big=True)}
    <div class="chips-row" role="group" aria-label="Filter articles by topic">{chips}</div>
    <div class="pgrid" id="post-grid">{grid}</div>
  </div>
</section>
{closer("Stop reading.", "Start training.")}''')

for p in POSTS:
    others = [o for o in POSTS if o["slug"] != p["slug"] and o["cat"] == p["cat"]][:2]
    others += [o for o in POSTS if o["slug"] != p["slug"] and o not in others][:3 - len(others)]
    crumb = f'<ol class="crumbs"><li><a href="index.html">Home</a></li><li><a href="blog.html">Blog</a></li><li aria-current="page">{p["cat"]}</li></ol>'
    answer = f'<p class="answer"><strong>Short answer:</strong> {p["lead"]}</p>' if p["lead"] else ""
    faqblock = (f'<div class="article-faq faq"><h2>Quick answers</h2><div class="faq-list">{faq_html(p["faq"], open_first=False)}</div></div>') if p["faq"] else ""
    keep = "".join(f'<li><a class="textlink" href="{h}">{l} →</a></li>' for h, l in p["links"])
    body = f'''
<section class="page-hero has-bg"><div class="ph hero-bg"><img src="img/photos/vineland-gym-{p["img"]}.webp" alt="" fetchpriority="high"></div>
  <div class="wrap">
    <nav aria-label="Breadcrumb">{crumb}</nav>
    <p class="eyebrow" style="margin-top:28px">{p["cat"]} · {_fmt(p["date"])} · {_mins(p)} min read</p>
    <h1 class="post-h1">{p["title"]}</h1>
    <p class="lede" style="color:rgba(242,236,223,.82)">By the Animal Paradise coaching team · Vineland, NJ</p>
  </div>
</section>
<section class="band" style="padding-top:clamp(48px,6vw,80px)">
  <div class="wrap article-grid">
    <article class="article">
      {answer}
      {p["body"]}
      {faqblock}
    </article>
    <aside class="aside">
      <div class="tour" style="gap:12px">
        <span class="eyebrow">Animal Paradise · Vineland</span>
        <h3 style="font-size:22px">Come see the gym</h3>
        <p class="fine" style="font-size:14.5px">Open 4AM to 12AM every day inside Cumberland Mall. Memberships from $60.</p>
        <a class="btn btn-gold" href="visit.html">Book a free tour {ARROW}</a>
      </div>
      <div class="who-card"><span class="eyebrow">Next steps</span><ul class="aside-links">{keep}</ul></div>
    </aside>
  </div>
</section>
{related_band([o["slug"] for o in others])}
{closer()}'''
    def _lbl(m):
        t = m.group(0); hs = re.findall(r"<th>(.*?)</th>", t)
        def row(r):
            i = [0]
            def td(x):
                k = hs[i[0]] if i[0] < len(hs) else ""; i[0] += 1
                return f'<td data-label="{k}">'
            return re.sub(r"<td>", td, r.group(0))
        return re.sub(r"<tr>(?:(?!</tr>).)*</tr>", row, t, flags=re.S)
    body = re.sub(r'<table class="post-tbl">.*?</table>', _lbl, body, flags=re.S)
    PAGES[p["slug"] + ".html"] = dict(
        title=f'{p["title"]} | Animal Paradise Gyms', desc=p["desc"], slug=p["slug"], nav_active="blog.html",
        schemas=[{"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "description": p["desc"],
                  "datePublished": p["date"], "dateModified": p["date"], "image": f'{SITE}/img/photos/vineland-gym-{p["img"]}.webp',
                  "author": {"@type": "Organization", "name": "Animal Paradise Gyms", "url": SITE + "/"}, "publisher": GYM_ID,
                  "mainEntityOfPage": f'{SITE}/{p["slug"]}/', "keywords": p["kw"], "articleSection": p["cat"]},
                 {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                     {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                     {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog/"},
                     {"@type": "ListItem", "position": 3, "name": p["title"], "item": f'{SITE}/{p["slug"]}/'}]}] + ([faq_ld(p["faq"])] if p["faq"] else []),
        body=body)

# internal links from service pages into the blog
_REL = {"index.html": None, "memberships.html": ["gym-membership-cost-vineland-nj", "best-gym-vineland-nj", "first-week-at-the-gym-beginners"],
        "personal-training.html": ["first-npc-show-prep-guide", "the-strategies-experienced-lifters-use-to-lose-fat-without-sacrificing-muscle", "how-long-does-it-actually-take-to-see-results-from-working-out"],
        "lioness-den.html": ["womens-only-gym-south-jersey", "first-week-at-the-gym-beginners", "gym-membership-cost-vineland-nj"],
        "the-gym.html": ["sauna-massage-compression-recovery", "best-gym-vineland-nj", "gym-open-late-vineland-nj"],
        "animal-cafe.html": ["protein-shake-before-or-after-workout", "the-strategies-experienced-lifters-use-to-build-muscle-without-gaining-excess-fat", "creatine-for-beginners"],
        "animal-supps.html": ["creatine-for-beginners", "protein-shake-before-or-after-workout", "the-strategies-experienced-lifters-use-to-build-muscle-without-gaining-excess-fat"],
        "visit.html": ["gym-open-late-vineland-nj", "best-gym-vineland-nj", "gym-membership-cost-vineland-nj"],
        "animal-fest-3.html": ["first-npc-show-prep-guide", "sauna-massage-compression-recovery", "the-strategies-experienced-lifters-use-to-lose-fat-without-sacrificing-muscle"]}
for _fn, _slugs in _REL.items():
    if _fn not in PAGES: continue
    _band = latest_posts_band() if _slugs is None else related_band(_slugs, "Read before you visit" if _fn == "visit.html" else "Keep reading")
    _b = PAGES[_fn]["body"]
    _i = _b.rfind('<section class="band closer"')
    PAGES[_fn]["body"] = _b[:_i] + _band + "\n" + _b[_i:]


# ================= ANIMAL FEST 2 =================
AF2_GALLERY = [("crowd-gym-floor", "Crowd on the gym floor at Animal Fest 2"), ("medal-presentation", "Competitor with his medals at Animal Fest 2"),
    ("bikini-lineup", "Bikini competitors with their medals on stage"), ("vendor-booth", "Supplement vendor booth on the Animal Paradise floor"),
    ("stage-medals", "Medals awarded on stage"), ("guest-athlete", "Guest athlete meeting fans at Animal Fest 2"),
    ("bikini-medal", "Bikini competitor receiving her medal on stage"), ("crowd-screen", "Crowd watching the big screen at Animal Fest 2")]
PAGES["animal-fest-2.html"] = dict(
    title="Animal Fest 2 | October 25, 2025 at Animal Paradise Gyms, Vineland NJ",
    desc="Animal Fest 2 took place October 25, 2025 at Animal Paradise Gyms in Vineland NJ: vendors, guest athletes, medals on stage and a packed gym floor. See the photos.",
    slug="animal-fest-2", nav_active="events.html",
    schemas=[{"@context": "https://schema.org", "@type": "Event", "name": "Animal Fest 2",
              "description": "The second Animal Fest at Animal Paradise Gyms: vendors, guest athletes, medals on stage and a packed gym floor.",
              "startDate": "2025-10-25", "eventStatus": "https://schema.org/EventScheduled",
              "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
              "location": {"@type": "Place", "name": "Animal Paradise Gyms, Cumberland Mall", "address": GYM_LD["address"]},
              "organizer": GYM_ID, "image": [SITE + "/img/events/animal-fest-2-" + k + ".webp" for k, _ in AF2_GALLERY[:3]],
              "url": SITE + "/animal-fest-2/"},
             {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                 {"@type": "ListItem", "position": 2, "name": "Events", "item": SITE + "/events/"},
                 {"@type": "ListItem", "position": 3, "name": "Animal Fest 2", "item": SITE + "/animal-fest-2/"}]}],
    body=f'''
<section class="page-hero has-bg"><div class="ph hero-bg"><img src="img/events/animal-fest-2-crowd-gym-floor.webp" alt="" fetchpriority="high"></div>
  <div class="wrap">
    <nav aria-label="Breadcrumb"><ol class="crumbs"><li><a href="index.html">Home</a></li><li><a href="events.html">Events</a></li><li aria-current="page">Animal Fest 2</li></ol></nav>
    <p class="eyebrow" style="margin-top:28px">October 25, 2025 · Animal Paradise, Vineland</p>
    <h1>Animal Fest <span class="gold">2</span></h1>
    <p class="lede" style="color:rgba(242,236,223,.82)">Vendors, guest athletes, medals on stage and a gym floor packed with the South Jersey training community.</p>
  </div>
</section>

<section class="band">
  <div class="wrap split">
    <div class="prose rv">
      <span class="eyebrow">The recap</span>
      <h2>The year Animal Fest <span class="gold">got bigger.</span></h2>
      <p>On October 25, 2025, Animal Paradise opened its doors for the second Animal Fest. Members, competitors, vendors and guest athletes filled the floor, and the day ended with medals handed out on stage.</p>
      <ul class="ticks"><li>Supplement and brand vendors on the gym floor</li><li>Guest athletes meeting the crowd</li><li>Medals presented on stage, including bikini and physique competitors</li><li>Big-screen presentations for the whole room</li></ul>
    </div>
    <div class="ph rv" style="aspect-ratio:4/3"><img loading="lazy" src="img/events/animal-fest-2-medal-presentation.webp" alt="Competitor with his medals at Animal Fest 2"></div>
  </div>
</section>

<section class="band" style="padding-top:0">
  <div class="wrap">
    {head_block("Gallery", 'Animal Fest 2 <span class="gold">in photos.</span>')}
    <div class="gallery-grid g4">{"".join(f'<div class="ph rv"><img loading="lazy" src="img/events/animal-fest-2-{k}.webp" alt="{a}"></div>' for k, a in AF2_GALLERY)}</div>
  </div>
</section>

<section class="band" style="padding-top:0">
  <div class="wrap">
    <a class="tile rv" style="min-height:400px;text-decoration:none" href="animal-fest-3.html">
      <div class="ph"><img loading="lazy" src="img/photos/vineland-gym-animal-fest-belt.webp" alt="Animal Fest III champion belt"></div>
      <div class="tile-body"><span class="tag">Next chapter · October 10, 2026</span><h3 style="font-size:clamp(24px,2.6vw,32px)">See Animal Fest 3</h3><p>Guest posing, competitions, vendors and the Animal Fest III champion belt.</p><span class="textlink">See the recap →</span></div>
    </a>
  </div>
</section>
{closer("See you at", "Animal Fest 4.")}''')


# ================= GALLERY =================
GAL = [
 # (src, category, caption)
 ("photos/vineland-gym-hero-floor", "floor", "The main training floor"),
 ("photos/vineland-gym-squat-racks", "floor", "Squat racks and Atlantis plates"),
 ("photos/vineland-gym-cable-stations", "floor", "Cable stations under the Animal Paradise sign"),
 ("photos/vineland-gym-biggest-dumbbells", "floor", "Home of the biggest dumbbells in the world"),
 ("photos/vineland-gym-cardio-floor", "floor", "The cardio floor"),
 ("photos/vineland-gym-cardio-floor-2", "floor", "Cardio rows under the LED ceiling"),
 ("photos/vineland-gym-surf-machine", "floor", "Surf machine and functional area"),
 ("photos/vineland-gym-animal-team-mural", "floor", "The Animal Team mural"),
 ("photos/vineland-gym-squat-rack-training", "training", "Squats in the rack"),
 ("photos/vineland-gym-overhead-press", "training", "Overhead press"),
 ("photos/vineland-gym-deadlift", "training", "Deadlift"),
 ("photos/vineland-gym-incline-dumbbell-press", "training", "Incline dumbbell press"),
 ("photos/vineland-gym-dumbbell-flyes", "training", "Dumbbell flyes"),
 ("photos/vineland-gym-plate-loaded-row", "training", "Plate-loaded row"),
 ("photos/vineland-gym-lift-heavy", "training", "Lift heavy"),
 ("photos/vineland-gym-cable-pulldown", "training", "Cable pulldown"),
 ("photos/vineland-gym-cable-crunch", "training", "Cable work"),
 ("photos/vineland-gym-cable-pushdown", "training", "Cable pushdown"),
 ("photos/vineland-gym-cable-extension", "training", "Cable extension"),
 ("photos/vineland-gym-cable-training", "training", "Cable training"),
 ("photos/vineland-gym-dumbbell-lunge", "training", "Dumbbell lunge"),
 ("photos/vineland-gym-hibernation-station", "recovery", "The Hibernation Station"),
 ("photos/vineland-gym-hibernation-station-2", "recovery", "Massage chairs"),
 ("photos/vineland-gym-red-light-recovery", "recovery", "Recovering between sessions"),
 ("photos/vineland-gym-lioness-den", "lioness", "The Lioness Den"),
 ("photos/vineland-gym-lioness-den-2", "lioness", "Lioness Den equipment"),
 ("photos/vineland-gym-lioness-den-3", "lioness", "Inside the Lioness Den"),
 ("photos/vineland-gym-animal-cafe", "fuel", "Animal Cafe"),
 ("photos/vineland-gym-animal-cafe-2", "fuel", "Animal Cafe by the windows"),
 ("photos/vineland-gym-animal-cafe-counter", "fuel", "The cafe counter"),
 ("photos/vineland-gym-animal-supps", "fuel", "Animal Supps shelves"),
 ("photos/vineland-gym-animal-supps-2", "fuel", "Animal Supps"),
 ("photos/vineland-gym-animal-supps-storefront", "fuel", "Animal Supps storefront"),
 ("photos/vineland-gym-pool-table-lounge", "lounge", "Pool table lounge"),
 ("photos/vineland-gym-pool-table", "lounge", "The Animal Paradise pool table"),
 ("photos/vineland-gym-lounge", "lounge", "The lounge"),
 ("photos/vineland-gym-posing-room", "lounge", "Posing room"),
 ("photos/vineland-gym-daycare", "lounge", "Daycare entrance"),
 ("events/animal-fest-2-crowd-gym-floor", "events", "Animal Fest 2 crowd"),
 ("events/animal-fest-2-medal-presentation", "events", "Animal Fest 2 medalist"),
 ("events/animal-fest-2-vendor-booth", "events", "Animal Fest 2 vendor booth"),
 ("events/animal-fest-2-guest-athlete", "events", "Animal Fest 2 guest athlete"),
 ("events/animal-fest-2-crowd-screen", "events", "Animal Fest 2 presentations"),
 ("events/animal-fest-2-bikini-lineup", "events", "Bikini competitors with medals"),
 ("events/animal-fest-2-stage-medals", "events", "Medals on stage"),
 ("events/animal-fest-2-bikini-medal", "events", "Medal presentation"),
 ("photos/vineland-gym-animal-fest-belt", "events", "Animal Fest III champion belt"),
 ("photos/vineland-gym-animal-fest-medal", "events", "Animal Fest 3 medal"),
 ("photos/vineland-gym-animal-fest-medal-2", "events", "Animal Fest 3 medal on the belt"),
 ("photos/vineland-gym-animal-fest-medals", "events", "Animal Fest 3 medals"),
]
GAL_CATS = [("all", "All"), ("floor", "The floor"), ("training", "Training"), ("recovery", "Recovery"),
            ("lioness", "Lioness Den"), ("fuel", "Cafe and Supps"), ("lounge", "Lounge and extras"), ("events", "Events")]
_GL = dict(GAL_CATS)

def _gal_items():
    out = []
    for i, (src, cat, cap) in enumerate(GAL):
        out.append(f'<button class="gitem" type="button" data-cat="{cat}" data-i="{i}" aria-label="Open photo: {cap}">'
                   f'<img loading="lazy" src="img/{src}.webp" alt="{cap} at Animal Paradise Gyms, Vineland NJ">'
                   f'<span class="gcap"><b>{cap}</b><small>{_GL[cat]}</small></span></button>')
    return "".join(out)

_gchips = "".join(f'<button class="chip" type="button" aria-pressed="{"true" if k == "all" else "false"}" data-gcat="{k}">{l} <span class="ccount">{len(GAL) if k == "all" else sum(1 for g in GAL if g[1] == k)}</span></button>' for k, l in GAL_CATS)

PAGES["gallery.html"] = dict(
    title="Gym Photos | Animal Paradise Gyms Gallery | Vineland NJ",
    desc="Photos of Animal Paradise Gyms in Vineland NJ: the training floor, equipment, Lioness Den, Hibernation Station recovery room, Animal Cafe, Animal Supps and Animal Fest events.",
    slug="gallery",
    schemas=[crumbs_ld("Gallery", "gallery"),
             {"@context": "https://schema.org", "@type": "ImageGallery", "name": "Animal Paradise Gyms photo gallery", "url": SITE + "/gallery/", "about": GYM_ID,
              "image": [{"@type": "ImageObject", "contentUrl": f"{SITE}/img/{s}.webp", "caption": c} for s, _, c in GAL]}],
    body=page_hero("Gallery · Vineland, NJ", 'See it <span class="gold">before you walk in.</span>', f"{len(GAL)} photos of the floor, the equipment, the Lioness Den, recovery, the cafe and supps store, and our events. Tap any photo to view it full screen.", "Gallery", ctas=False, bg="biggest-dumbbells") + f'''
<section class="band" style="padding-top:clamp(40px,5vw,64px)">
  <div class="wrap">
    <div class="chips-row gchips" role="group" aria-label="Filter photos">{_gchips}</div>
    <div class="ggrid" id="ggrid">{_gal_items()}</div>
  </div>
</section>

<div class="lb" id="lb" hidden role="dialog" aria-modal="true" aria-label="Photo viewer">
  <button class="lb-x" type="button" aria-label="Close">×</button>
  <button class="lb-nav lb-prev" type="button" aria-label="Previous photo">‹</button>
  <figure class="lb-fig"><img id="lb-img" alt=""><figcaption id="lb-cap"></figcaption></figure>
  <button class="lb-nav lb-next" type="button" aria-label="Next photo">›</button>
</div>
{closer("Like what", "you see?")}''')


# ================= THANK YOU + 404 =================
PAGES["thank-you.html"] = dict(
    title="Thank You | Animal Paradise Gyms", desc="Thanks for reaching out to Animal Paradise Gyms. We will text you shortly to confirm.",
    slug="thank-you", schemas=[],
    body=page_hero("You're booked in", 'Thank you. <span class="gold">We got it.</span>', "Someone from the front desk will text or call you shortly to confirm your time. If you need us sooner, call (856) 839-4536.", "Thank you", ctas=False, bg="hero-floor") + f'''
<section class="band"><div class="wrap cards">
  {card("pin", "Find us", "3849 S Delsea Dr, Suite E000, Cumberland Mall, Vineland, NJ 08360. Free parking at the door.", "visit.html", "Hours and directions")}
  {card("users", "Meet the coaches", "Chuck, Hakim and Lauren. Personal training is booked separately from membership.", "personal-training.html", "See coaching")}
  {card("cup", "While you are here", "Animal Cafe and Animal Supps are inside the gym, open 4AM to 12AM.", "animal-cafe.html", "See the cafe")}
</div></section>''')
WAIVER = open("waiver_text.html").read()
PAGES["parent-consent-form.html"] = dict(
    title="Parent Consent Waiver | Animal Paradise Gyms, Vineland NJ",
    desc="Parent or legal guardian consent waiver for minors training at Animal Paradise Gyms in Vineland, NJ. Read the full agreement and sign online.",
    slug="parent-consent-form", schemas=[crumbs_ld("Parent Consent Waiver", "parent-consent-form")],
    body=page_hero("For parents and guardians", 'Parent consent <span class="gold">waiver.</span>', "Every member under 18 needs a signed waiver from a parent or legal guardian before training. Read the agreement below, then sign it online.", "Parent Consent Waiver", ctas=False, bg="hero-floor") + f'''
<section class="band"><div class="wrap wv-wrap">
  <div><a class="textlink wv-skip" href="#sign">Skip to signing ↓</a>
  <article class="wv" id="waiver" aria-label="Minor participation waiver">
{WAIVER}
  </article></div>
  <div class="wv-sign" id="sign">
    <span class="eyebrow">Sign the waiver</span>
    <h2>Sign it <span class="gold">online.</span></h2>
    <!--CONSENT_FORM-->
  </div>
</div></section>''')
PAGES["404.html"] = dict(
    title="Page Not Found | Animal Paradise Gyms", desc="This page moved. Find memberships, coaching, the Lioness Den and more at Animal Paradise Gyms in Vineland NJ.",
    slug="404", schemas=[],
    body=page_hero("Page not found", 'This page <span class="gold">moved.</span>', "The page you were looking for is not here anymore. Try one of these instead.", "Not found", ctas=False, bg="biggest-dumbbells") + f'''
<section class="band"><div class="wrap cards">
  {card("bolt", "Memberships", "Plans from $60 a month, with a no-contract option.", "memberships.html", "See plans")}
  {card("user", "Personal training", "Coaches for beginners, competitors and everyone in between.", "personal-training.html", "Meet the coaches")}
  {card("pin", "Visit us", "Open every day 4AM to 12AM inside Cumberland Mall.", "visit.html", "Hours and directions")}
</div></section>''')

# ---------- write ----------
for fn, p in PAGES.items():
    full = fn != "index.html"
    html = head(p["title"], p["desc"], p["slug"], p["schemas"], full) + nav(p.get("nav_active", fn)) + p["body"] + footer(full)
    html = re.sub(r'href="([a-z0-9-]+\.html)#[^"]*"', r'href="\1"', html)
    open(os.path.join(OUT, fn), "w").write(html)
    # deploy copy: every page as a full document
    os.makedirs("deploy", exist_ok=True)
    open(os.path.join("deploy", fn), "w").write(html if full else re.sub(r'href="([a-z0-9-]+\.html)#[^"]*"', r'href="\1"', head(p["title"], p["desc"], p["slug"], p["schemas"], True) + nav(p.get("nav_active", fn)) + p["body"] + footer(True)))
print("built", list(PAGES))
