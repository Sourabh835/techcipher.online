#!/usr/bin/env python3
"""Bing SERP gap analysis for AI + Tech long-tail candidates."""
import urllib.request, urllib.parse, re, time

def bing_serp(q):
    url = "https://www.bing.com/search?q=" + urllib.parse.quote(q) + "&count=10"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    })
    try:
        with urllib.request.urlopen(req, timeout=12) as r:
            html = r.read().decode("utf-8", "ignore")
    except Exception as e:
        return [("ERROR", str(e)[:40])]
    blocks = re.findall(r'<li class="b_algo".*?</li>', html, re.S)
    out = []
    for blk in blocks[:6]:
        tm = re.search(r'<h2[^>]*>(.*?)</h2>', blk, re.S)
        title = re.sub(r'<[^>]+>', '', tm.group(1)).strip() if tm else ""
        cm = re.search(r'<cite[^>]*>(.*?)</cite>', blk, re.S)
        cite = re.sub(r'<[^>]+>', '', cm.group(1)).strip() if cm else "?"
        dom = re.sub(r'https?://(www\.)?', '', cite).split('/')[0].split(' ')[0]
        out.append((dom, title[:60]))
    return out

candidates = [
    "ai tools for teachers in india",
    "artificial intelligence in hindi",
    "how does ai learn",
    "ai vs ml vs dl difference",
    "free ai tools for students",
    "chatgpt for upsc",
    "how to learn ai for free",
    "ai tools for presentation",
    "artificial intelligence in daily life",
    "is it worth learning python in 2026",
    "is it worth learning to code in 2026",
    "what is api for beginners",
    "is it worth learning n8n in 2026",
    "how to learn python",
    "tech careers in 2026",
]

for q in candidates:
    res = bing_serp(q)
    print(f"\n[{q}] ({len(res)} results)")
    for dom, t in res:
        print(f"   {dom:35s} :: {t}")
    time.sleep(1.5)
