#!/usr/bin/env python3
"""Harvest long-tail keywords from Google Autocomplete for AI + Tech niches."""
import json, time, urllib.request, urllib.parse

def autocomplete(seed):
    url = ("https://suggestqueries.google.com/complete/search?client=firefox&q="
           + urllib.parse.quote(seed))
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            d = json.loads(r.read().decode("utf-8", "ignore"))
        return d[1] if len(d) > 1 else []
    except Exception as e:
        return []

seeds = [
    # AI niche
    "ai tools for",
    "what is ai",
    "artificial intelligence in",
    "chatgpt for",
    "ai vs",
    "is ai",
    "how does ai",
    "free ai tools",
    # Tech niche
    "how to learn",
    "what is a",
    "tech careers in",
    "is it worth learning",
    "best free",
    "how to become a",
    "what is the difference between",
]

all_sugs = {}
for s in seeds:
    sugs = autocomplete(s)
    all_sugs[s] = sugs
    print(f"[{s}] -> {len(sugs)}")
    for x in sugs:
        print(f"    {x}")
    time.sleep(1.0)

# Save for next step
with open("kw_harvest.json", "w", encoding="utf-8") as f:
    json.dump(all_sugs, f, ensure_ascii=False, indent=1)
