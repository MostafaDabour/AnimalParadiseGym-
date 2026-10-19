"""Turn deploy/*.html into a production site in dist/ with clean URLs, tracking, redirects and SEO files.
Run after build.py:  python3 build.py && python3 prod.py
"""
import os, re, shutil, glob, json, datetime

SITE = "https://animalparadisegyms.com"
GTM = "GTM-MRFZPWTB"
PIXEL = "446714868529209"
WEBHOOK = os.environ.get("APG_WEBHOOK", "")
CONSENT_FORM = os.environ.get("APG_CONSENT_FORM", "")  # GHL form embed URL for the parent consent waiver          # GHL inbound webhook URL for the tour forms
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
    if CONSENT_FORM:
        html = html.replace("<!--CONSENT_FORM-->", f'<iframe class="wv-frame" src="{CONSENT_FORM}" title="Parent consent waiver form" loading="lazy"></iframe><script src="https://link.msgsndr.com/js/form_embed.js" async></script>')
    else:
        html = html.replace("<!--CONSENT_FORM-->", '<p>Online signing is being set up. For now, a parent or guardian can sign the waiver at the front desk, any day 4AM to 12AM.</p><p><a class="btn btn-gold" href="tel:+18568394536">Call (856) 839-4536</a></p>')
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
    for a, b in REDIRECTS:
        f.write(f"{a} {b} 301\n")
        if not a.endswith("*") and a.endswith("/") and a != "/":
            f.write(f"{a.rstrip('/')} {b} 301\n")

today = datetime.date.today().isoformat()
with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u in sorted(sitemap, key=lambda x: (x != "/", x)):
        f.write(f"  <url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>\n")
    f.write("</urlset>\n")

with open(os.path.join(OUT, "robots.txt"), "w") as f:
    f.write("User-agent: *\nAllow: /\nDisallow: /thank-you/\n\n"
            "User-agent: GPTBot\nAllow: /\nUser-agent: OAI-SearchBot\nAllow: /\nUser-agent: ChatGPT-User\nAllow: /\n"
            "User-agent: ClaudeBot\nAllow: /\nUser-agent: Claude-SearchBot\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\n"
            "User-agent: Google-Extended\nAllow: /\nUser-agent: Applebot-Extended\nAllow: /\n\n"
            f"Sitemap: {SITE}/sitemap.xml\n")

with open(os.path.join(OUT, "llms.txt"), "w") as f:
    f.write("""# Animal Paradise Gyms

> Full-service gym inside Cumberland Mall, 3849 S Delsea Dr, Suite E000, Vineland, NJ 08360. Open every day 4AM to 12AM. Phone (856) 839-4536.

- Memberships from $60/month (12-month Gold). No-contract Silver is $70/month. Day pass $20, one-week pass $40.
- Equipment: Arsenal, Atlantis, Rogue, Booty Builder, StarTrac. 80-foot functional turf. Posing room.
- Recovery: Hibernation Station (massage chairs, compression therapy) on Premium and Diamond. Sauna rooms included with every plan.
- Lioness Den: code-locked women's-only training area, included with Platinum ($70) and Diamond ($80).
- Personal training and NPC contest prep with coaches Chuck, Hakim and Lauren. Booked separately from membership; first consultation free.
- On site: Animal Cafe (shakes, acai bowls, juice, coffee) and Animal Supps (supplements), same hours as the gym. Daycare available.

## Key pages
""")
    for u in ["/", "/memberships/", "/the-gym/", "/personal-training/", "/lioness-den/", "/animal-cafe/", "/animal-supps/", "/visit/", "/faq/", "/events/", "/blog/"]:
        f.write(f"- {SITE}{u}\n")

with open(os.path.join(OUT, "_headers"), "w") as f:
    f.write("/img/*\n  Cache-Control: public, max-age=31536000, immutable\n/video/*\n  Cache-Control: public, max-age=31536000, immutable\n"
            "/css/*\n  Cache-Control: public, max-age=86400\n/js/*\n  Cache-Control: public, max-age=86400\n")

print(f"consent form {'SET' if CONSENT_FORM else 'NOT SET'}")
print(f"dist: {len(pages)} pages, {len(sitemap)} in sitemap, {len(REDIRECTS)} redirect rules, webhook {'SET' if WEBHOOK else 'NOT SET'}")
