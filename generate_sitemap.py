#!/usr/bin/env python3
"""Generate sitemap.xml with all static pages + every episode URL."""
import json
from datetime import date

BASE = "https://nightswimpod.com"
today = date.today().isoformat()

with open("src/data/episodes.json") as f:
    episodes = json.load(f)

# newest episode date for homepage/episodes lastmod
newest = max((ep.get("publishDate", today) for ep in episodes), default=today)

urls = []
urls.append((f"{BASE}/", newest, "daily", "1.0"))
urls.append((f"{BASE}/episodes", newest, "daily", "0.9"))
urls.append((f"{BASE}/about", "2026-03-17", "monthly", "0.7"))
urls.append((f"{BASE}/privacy", "2026-03-17", "yearly", "0.3"))

for ep in episodes:
    loc = f"{BASE}/episodes/{ep['id']}"
    lastmod = ep.get("publishDate", today)
    urls.append((loc, lastmod, "monthly", "0.8"))

lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for loc, lastmod, freq, prio in urls:
    lines.append("  <url>")
    lines.append(f"    <loc>{loc}</loc>")
    lines.append(f"    <lastmod>{lastmod}</lastmod>")
    lines.append(f"    <changefreq>{freq}</changefreq>")
    lines.append(f"    <priority>{prio}</priority>")
    lines.append("  </url>")
lines.append("</urlset>")

with open("public/sitemap.xml", "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"Wrote public/sitemap.xml with {len(urls)} URLs ({len(episodes)} episodes).")
