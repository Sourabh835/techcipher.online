#!/usr/bin/env python3
"""DuckDuckGo html second opinion on top gap picks."""
import urllib.request, urllib.parse, re, time

def ddg(q):
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q)
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    })
    try:
        with urllib.request.urlopen(req, timeout=12) as r:
            html = r.read().decode("utf-8", "ignore")
    except Exception as e:
        return [("ERROR", str(e)[:50])]
    res = re.findall(r'<a rel="nofollow" class="result__a"[^>]*>(.*?)</a>', html, re.S)
    out = []
    for a in res[:6]:
        title = re.sub(r'<[^>]+>', '', a).strip()
        out.append(title[:65])
    return out

for q in ["how does ai learn",
          "is it worth learning python in 2026",
          "chatgpt for upsc",
          "ai vs ml vs dl difference",
          "ai tools for teachers in india"]:
    print(f"\n[{q}]")
    for t in ddg(q):
        print(f"   :: {t}")
    time.sleep(1.5)
