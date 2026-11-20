# Blog agent: how to write and publish a post

You publish one blog post per run for animalparadisegyms.com. Read this whole file, then `content/FACTS.md`, then `content/keyword-plan.json`.

## 1. Pick the topic
- Take the FIRST item in `content/keyword-plan.json` whose `status` is `"todo"`.
- If the item has a `must_link` slug, link to that post inside the body. Use the `secondary` keywords naturally in headings or the FAQ, and follow the `notes`.
- If none are left, do not write anything. Report "Keyword plan finished, add new topics" and stop.
- Before writing, check `old_posts/` and `content/posts/` so you do not repeat an existing post's angle. Link to related existing posts instead.

## 2. Research
- Use web search to check current, reputable guidance (health bodies, peer-reviewed reviews, major sports-science sources) for every training, nutrition or health claim. Do not invent numbers.
- Keep claims conservative. For anything medical (pregnancy, postpartum, injuries, conditions), tell readers to check with a healthcare professional.

## 3. Write the file
Create `content/posts/<slug>.md` using the `slug` from the plan. Exact format:

```
title: <the plan's title, 60 characters or less ideally>
date: <today, YYYY-MM-DD, America/New_York>
cat: <the plan's cat>
img: <one photo key from photos.json that fits the topic>
desc: <meta description, 130 to 155 characters, includes the keyword, no em dashes>
keyword: <the plan's keyword>
lead: <2 to 3 sentences that directly answer the main question. This shows as the "Short answer" box and is what Google and AI tools quote.>
links: <3 internal links: page.html|Anchor text; page.html|Anchor text; page.html|Anchor text>
---
<markdown body>

## Frequently asked questions

### <question people actually search>
<2 to 4 sentence answer>

(4 to 6 questions)
```

Body rules:
- 1,100 to 1,600 words. Plain, friendly, direct. Written for real people in Vineland, many of them beginners. Not hype.
- Start with 1 or 2 short paragraphs, then `##` sections. Use `###` only inside a section (never before the FAQ heading).
- Use the keyword naturally in the first paragraph and in at least one `##` heading. No keyword stuffing.
- Use lists, and markdown tables where they help (plans, comparisons). Tables become mobile cards automatically.
- Include 2 to 4 links INSIDE the body to other pages, written as `[anchor](page.html)` using these files: index.html, memberships.html, the-gym.html, personal-training.html, lioness-den.html, animal-cafe.html, animal-supps.html, visit.html, faq.html, events.html, blog.html, coach-chuck.html, coach-hakim.html, coach-lauren.html, or another post as `<slug>.html`.
- End with one short local section tying the topic to Animal Paradise (only facts from FACTS.md) and a soft call to action (free tour at visit.html, or free coach consultation at personal-training.html).
- NEVER use em dashes (—) or en dashes used as dashes. Use commas, periods or "to" for ranges.
- No fake quotes, no fake reviews, no made-up member stories, no "studies show" without a real source behind it.
- Do not mention AI. Posts are by "the Animal Paradise coaching team" (the template adds this).

## 4. Check and publish
1. `pip install markdown pillow --break-system-packages -q` if needed.
2. Run `python3 build.py && python3 prod.py`. Both must succeed.
3. Check: `grep -c "—" content/posts/<slug>.md` must be 0. `dist/<slug>/index.html` must exist and contain `FAQPage`.
4. In `content/keyword-plan.json`, set this item's `status` to `"done"` and `published` to today's date.
5. Commit everything (including `dist/`) with message `Blog: <title>`, then push to `main`. Cloudflare deploys automatically in about a minute.
6. Wait about 90 seconds, then fetch `https://animalparadisegyms.com/<slug>/` to confirm it is live.

## 5. Report
Finish with a short message: the title, the live link, the target keyword, and the next topic in the plan.
If anything fails (build error, push rejected, page not live), do not force it: report exactly what failed.
