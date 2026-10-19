"""Turn deploy/*.html into a production site in dist/ with clean URLs, tracking, redirects and SEO files.
Run after build.py:  python3 build.py && python3 prod.py
"""
import os, re, shutil, glob, json, datetime

SITE = "https://animalparadisegyms.com"
GTM = "GTM-MRFZPWTB"
PIXEL = "446714868529209"
WEBHOOK = os.environ.get("APG_WEBHOOK", "https://services.leadconnectorhq.com/hooks/31VwWnIDdjlwKYy4I7QI/webhook-trigger/b23536f8-c971-4baa-9478-b0058a9c36c4")          # GHL inbound webhook URL for the tour forms
SRC, OUT = "deploy", "dist"

shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT)

TRACK_HEAD = f"""<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{GTM}');</script>
<!-- Meta Pixel -->
<script>!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');fbq('init','{PIXEL}');fbq('track','PageView');</script>
<script>window.APG_WEBHOOK={json.dumps(WEBHOOK)};</script>
"""
TRACK_BODY = f"""<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<noscript><img height="1" width="1" style="display:none" alt="" src="https://www.facebook.com/tr?id={PIXEL}&ev=PageView&noscript=1"></noscript>
"""

pages = {}
for f in glob.glob(os.path.join(SRC, "*.html")):
    html = open(f).read()
    m = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    url = m.group(1).replace(SITE, "") if m else "/"
    pages[os.path.basename(f)] = (url, html)

fn2url = {fn: u for fn, (u, _) in pages.items()}
fn2url["404.html"] = "/"  # never link to the 404 page

def rewrite(html):
    html = re.sub(r'href="([a-z0-9-]+\.html)"', lambda m: f'href="{fn2url.get(m.group(1), "/")}"', html)
    html = re.sub(r'(src|href|poster)="(img|css|js|video)/', r'\1="/\2/', html)
    html = html.replace("</title>", "</title>\n" + TRACK_HEAD, 1) if "<title>" in html else html
    html = html.replace("<body>", "<body>\n" + TRACK_BODY, 1)
    return html

sitemap = []
for fn, (url, html) in pages.items():
    out = rewrite(html)
    if fn in ("404.html", "thank-you.html", "parent-consent-form.html"):
        out = out.replace("<title>", '<meta name="robots" content="noindex">\n<title>', 1)
    if fn == "404.html":
        path = os.path.join(OUT, "404.html")
    else:
        path = os.path.join(OUT, url.strip("/"), "index.html") if url != "/" else os.path.join(OUT, "index.html")
        if fn not in ("thank-you.html", "parent-consent-form.html"):
            sitemap.append(url)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(out)

for d in ("css", "js", "img", "video"):
    shutil.copytree(os.path.join("site", d), os.path.join(OUT, d))

# ---- image performance: mobile-size variants, srcset, intrinsic sizes ----
from PIL import Image
VARIANTS = (760, 1200)
dims = {}
for f in glob.glob(os.path.join("site", "img", "**", "*.*"), recursive=True):
    if f.endswith((".webp", ".png", ".jpg")):
        rel = "/" + os.path.relpath(f, "site").replace(os.sep, "/")
        with Image.open(f) as im:
            dims[rel] = im.size
            if rel.startswith(("/img/photos/", "/img/events/")):
                for vw in VARIANTS:
                    if im.size[0] > vw + 200:
                        out = os.path.join(OUT, rel[1:]).replace(".webp", f"-{vw}.webp")
                        im.resize((vw, round(im.size[1] * vw / im.size[0])), Image.LANCZOS).save(out, "WEBP", quality=78, method=6)

def img_tag(m):
    tag = m.group(0)
    src = re.search(r'src="([^"]+)"', tag)
    if not src or src.group(1) not in dims: return tag
    u = src.group(1); w, h = dims[u]
    if "width=" not in tag:
        tag = tag.replace("<img ", f'<img width="{w}" height="{h}" ', 1)
    vs = [(vw, u.replace(".webp", f"-{vw}.webp")) for vw in VARIANTS]
    vs = [(vw, v) for vw, v in vs if v != u and os.path.exists(os.path.join(OUT, v[1:]))]
    if "srcset=" not in tag and vs:
        if 'class="gimg"' in tag: sizes = "(max-width: 700px) 50vw, (max-width: 1100px) 33vw, 25vw"
        elif "data-hero" in tag: sizes = "100vw"
        else: sizes = "(max-width: 900px) 100vw, 50vw"
        srcset = ", ".join(f"{v} {vw}w" for vw, v in vs) + f", {u} {w}w"
        tag = tag.replace("<img ", f'<img srcset="{srcset}" sizes="{sizes}" ', 1)
    return tag

def tune_images(html):
    # the first photo in a hero is the LCP: mark it, load it eagerly and with priority
    html = html.replace('<div class="ph hero-bg"><img ', '<div class="ph hero-bg"><img data-hero ', 1)
    return re.sub(r"<img [^>]+>", img_tag, html)

for path in glob.glob(os.path.join(OUT, "**", "*.html"), recursive=True):
    t = open(path).read(); t2 = tune_images(t)
    if t2 != t: open(path, "w").write(t2)

# cache-bust css/js so they can be cached for a year
import hashlib as _h
for asset in ("css/site.css", "js/site.js"):
    v = _h.md5(open(os.path.join(OUT, asset), "rb").read()).hexdigest()[:8]
    for path in glob.glob(os.path.join(OUT, "**", "*.html"), recursive=True):
        t = open(path).read()
        if f"/{asset}\"" in t: open(path, "w").write(t.replace(f"/{asset}\"", f"/{asset}?v={v}\""))
shutil.copy(os.path.join("site", "favicon.ico"), os.path.join(OUT, "favicon.ico"))

# 301s from the old WordPress addresses
REDIRECTS = [
    ("/services/", "/memberships/"), ("/membership/", "/memberships/"),
    ("/visit-us/", "/visit/"), ("/contact/", "/visit/"),
    ("/testimonials/", "/about/"), ("/shop/", "/animal-supps/"),
    ("/3124-2/", "/gallery/"), ("/about/events/", "/events/"),
    ("/discover-animal-paradise-the-ultimate-gym-experience-designed-by-athletes/", "/the-gym/"),
    ("/animal-paradise-the-ultimate-luxurious-gym-experience/", "/the-gym/"),
    ("/trainer/", "/personal-training/"),
    ("/category/*", "/blog/"), ("/tag/*", "/blog/"), ("/author/*", "/blog/"), ("/feed/", "/blog/"),
    ("/home/", "/"),
    ("/cart/", "/animal-supps/"), ("/checkout/", "/animal-supps/"), ("/my-account/", "/animal-supps/"),
]
with open(os.path.join(OUT, "_redirects"), "w") as f:
    for a, b in sorted(REDIRECTS, key=lambda r: "*" in r[0]):  # exact rules first, splats last
        f.write(f"{a} {b} 301\n")
        if not a.endswith("*") and a.endswith("/") and a != "/":
            f.write(f"{a.rstrip('/')} {b} 301\n")

import hashlib
_agr = open("waiver_text.html").read()
os.makedirs("worker", exist_ok=True)
with open(os.path.join("worker", "agreement.js"), "w") as f:
    f.write("// generated by prod.py from waiver_text.html\nexport const AGREEMENT_HTML = " + json.dumps(_agr) + ";\nexport const AGREEMENT_SHA256 = " + json.dumps(hashlib.sha256(_agr.encode()).hexdigest()) + ";\n")

today = datetime.date.today().isoformat()
with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u in sorted(sitemap, key=lambda x: (x != "/", x)):
        f.write(f"  <url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>\n")
    f.write("</urlset>\n")

with open(os.path.join(OUT, "robots.txt"), "w") as f:
    f.write("User-agent: *\nAllow: /\nDisallow: /thank-you/\nDisallow: /api/\n\n"
            "User-agent: GPTBot\nAllow: /\nUser-agent: OAI-SearchBot\nAllow: /\nUser-agent: ChatGPT-User\nAllow: /\n"
            "User-agent: ClaudeBot\nAllow: /\nUser-agent: Claude-SearchBot\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\n"
            "User-agent: Google-Extended\nAllow: /\nUser-agent: Applebot-Extended\nAllow: /\n\n"
            f"Sitemap: {SITE}/sitemap.xml\n")

with open(os.path.join(OUT, "llms.txt"), "w") as f:
    f.write("""# Animal Paradise Gyms

> Full-service gym inside Cumberland Mall, 3849 S Delsea Dr, Suite E000, Vineland, NJ 08360. Open every day 4AM to 12AM. Phone (856) 839-4536.

- Memberships from $60/month (12-month Gold). No-contract Silver is $70/month. Day pass $20, one-week pass $40.
- Equipment: Arsenal, Atlantis, Rogue, Booty Builder, StarTrac. 80-foot functional turf. Posing room.
- Recovery: Hibernation Station (massage chairs, compression therapy) on Premium and Diamond. Sauna rooms included with every plan. Red light therapy and tanning beds on site.
- Lioness Den: code-locked women's-only training area, included with Platinum ($70) and Diamond ($80).
- Personal training and NPC contest prep with coaches Chuck, Hakim and Lauren. Booked separately from membership; first consultation free.
- On site: Animal Cafe (shakes, acai bowls, juice, coffee) and Animal Supps (supplements), same hours as the gym. Daycare available.

## Key pages
""")
    for u, label in [("/", "Home"), ("/memberships/", "Memberships and prices"), ("/the-gym/", "Equipment and amenities"),
                     ("/personal-training/", "Personal training and contest prep"), ("/lioness-den/", "Lioness Den women's-only area"),
                     ("/animal-cafe/", "Animal Cafe"), ("/animal-supps/", "Animal Supps"), ("/visit/", "Hours, directions, free tour"),
                     ("/faq/", "FAQ"), ("/events/", "Events, including Animal Fest"), ("/gallery/", "Photo gallery"), ("/blog/", "Blog")]:
        f.write(f"- [{label}]({SITE}{u})\n")
    f.write("\n## Coaches\n- [Chuck: NPC contest prep]({0}/trainer/chuck/)\n- [Hakim: NASM certified personal trainer]({0}/trainer/hakim/)\n- [Lauren: female personal trainer]({0}/trainer/lauren/)\n".format(SITE))
    f.write("\n## Quick answers\n"
            "- Hours: every day 4AM to 12AM, including weekends.\n"
            "- Cheapest membership: Gold, $60 a month on a 12-month plan. Month to month: Silver, $70.\n"
            "- Personal training is booked separately from membership. The first consultation is free.\n"
            "- Women's-only area: the Lioness Den, included with Platinum ($70) and Diamond ($80).\n"
            "- Recovery: sauna with every plan; Hibernation Station (massage chairs, compression) with Premium and Diamond; red light therapy and tanning on site.\n"
            "- Parking: free, right at the door.\n")
    import re as _re
    posts = []
    for fn, (url, html) in pages.items():
        if '"BlogPosting"' in html:
            t = _re.search(r"<h1[^>]*>(.*?)</h1>", html, _re.S)
            posts.append((url, _re.sub(r"<[^>]+>", "", t.group(1)).strip() if t else url))
    f.write("\n## Articles\n" + "".join(f"- [{t}]({SITE}{u})\n" for u, t in sorted(posts, key=lambda x: x[1])))

with open(os.path.join(OUT, "_headers"), "w") as f:
    f.write("/img/*\n  Cache-Control: public, max-age=31536000, immutable\n/video/*\n  Cache-Control: public, max-age=31536000, immutable\n"
            "/css/*\n  Cache-Control: public, max-age=31536000, immutable\n/js/*\n  Cache-Control: public, max-age=31536000, immutable\n")

print(f"dist: {len(pages)} pages, {len(sitemap)} in sitemap, {len(REDIRECTS)} redirect rules, webhook {'SET' if WEBHOOK else 'NOT SET'}")
