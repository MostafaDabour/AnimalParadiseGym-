# Animal Paradise Gyms website

Static site on Cloudflare Workers (static assets). Live: https://animalparadisegyms.com

- `dist/` is what goes live. Cloudflare deploys it on every push to `main` (`npx wrangler deploy`).
- Source: `build.py` (pages), `posts.py` + `old_posts/` (blog), `site/` (css, js, images, video), `prod.py` (clean URLs, tracking, redirects, sitemap).
- Rebuild: `python3 build.py && APG_WEBHOOK=<ghl webhook url> python3 prod.py`
