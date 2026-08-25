#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Insert Adsterra ad slots into techcipher.online static site."""
import re, sys, os

BASE = r"C:\Users\Sourabh Antil\techcipher-site"

SOCIAL_BAR = ('<script src="https://pl31026321.profitableratecpmnetwork.com/'
              'cf/b0/57/cfb057c937e13e558a3a346789e8f77a.js"></script>')

def slot(key, h, w, cls):
    return (
        '<div class="ad-slot {cls}">\n'
        '  <span class="ad-label">Advertisement</span>\n'
        '  <script>\n'
        "    atOptions = {{\n"
        "      'key' : '{key}',\n"
        "      'format' : 'iframe',\n"
        "      'height' : {h},\n"
        "      'width' : {w},\n"
        "      'params' : {{}}\n"
        "    }};\n"
        '  </script>\n'
        '  <script src="https://www.highrevenueformat.com/{key}/invoke.js"></script>\n'
        '</div>'
    ).format(key=key, h=h, w=w, cls=cls)

LEADER = slot('c77112ce4333732f5644f7d13a031bd7', 90, 728, 'ad-leader')   # 728x90
RECT   = slot('62b9a2f8d2e92897d46502e4bdce031c', 250, 300, 'ad-rect')    # 300x250
BANNER = slot('94caf29d0fa07590490e52b9b41b5c8f', 60, 468, 'ad-banner')   # 468x60
MOBILE = slot('3d582dd3bffd08bc1a73b1d6aa8ee6d9', 50, 320, 'ad-mobile')   # 320x50
SKY    = slot('7512cd8a458440e5ccd2930ae886fdfc', 600, 160, 'ad-sky')     # 160x600

NATIVE = (
    '<div class="ad-slot ad-native">\n'
    '  <span class="ad-label">Advertisement</span>\n'
    '  <script async="async" data-cfasync="false" src="https://pl31026322.profitableratecpmnetwork.com/bb89cff7dc90d8f0d64112679549aab1/invoke.js"></script>\n'
    '  <div id="container-bb89cff7dc90d8f0d64112679549aab1"></div>\n'
    '</div>'
)

SIDEBAR = (
    '<aside class="ad-sidebar">\n'
    '  <div class="ad-slot ad-rect">\n'
    '    <span class="ad-label">Advertisement</span>\n'
    '    <script>\n'
    "      atOptions = {\n"
    "        'key' : '62b9a2f8d2e92897d46502e4bdce031c',\n"
    "        'format' : 'iframe',\n"
    "        'height' : 250,\n"
    "        'width' : 300,\n"
    "        'params' : {}\n"
    "      };\n"
    '    </script>\n'
    '    <script src="https://www.highrevenueformat.com/62b9a2f8d2e92897d46502e4bdce031c/invoke.js"></script>\n'
    '  </div>\n'
    '  <div class="ad-slot ad-sky">\n'
    '    <span class="ad-label">Advertisement</span>\n'
    '    <script>\n'
    "      atOptions = {\n"
    "        'key' : '7512cd8a458440e5ccd2930ae886fdfc',\n"
    "        'format' : 'iframe',\n"
    "        'height' : 600,\n"
    "        'width' : 160,\n"
    "        'params' : {}\n"
    "      };\n"
    '    </script>\n'
    '    <script src="https://www.highrevenueformat.com/7512cd8a458440e5ccd2930ae886fdfc/invoke.js"></script>\n'
    '  </div>\n'
    '</aside>'
)

ARTICLES = [
    'common-cybersecurity-threats-and-how-to-avoid-them',
    'how-does-ai-learn',
    'how-does-chatgpt-work-in-simple-terms',
    'how-to-become-ethical-hacker-in-india',
    'how-to-learn-coding-for-beginners-free',
    'how-to-protect-phone-from-hackers',
    'is-cybersecurity-a-good-career-in-india',
    'is-ethical-hacking-legal-in-india',
    'is-it-worth-learning-to-code-in-2026',
    'what-is-sim-swap-attack',
]

def read(p):
    with open(os.path.join(BASE, p), encoding='utf-8') as f:
        return f.read()

def write(p, s):
    with open(os.path.join(BASE, p), 'w', encoding='utf-8') as f:
        f.write(s)

def add_social_bar(html):
    if 'profitableratecpmnetwork.com/cf/b0/57' in html:
        return html
    return html.replace('</head>', '  ' + SOCIAL_BAR + '\n</head>', 1)

def wrap_indent(s, indent):
    return '\n'.join(indent + ln if ln else ln for ln in s.split('\n'))

def process_article(name):
    p = name + '.html'
    html = read(p)
    orig = html
    log = []

    html = add_social_bar(html); log.append('social_bar')

    # 1) two-column layout + open article-main
    a = '<main class="container article-wrap">\n    <article>'
    b = '<main class="container article-wrap layout-sidebar">\n    <div class="article-main">\n    <article>'
    assert a in html, p + ': main/article pattern missing'
    html = html.replace(a, b, 1)

    # 2) leaderboard after article-header close (6-space indent; site-header uses 2)
    m = re.search(r'      </header>', html)
    assert m, p + ': no article-header'
    assert html[m.end():m.end() + 11] == '\n\n      <p>', p + ': header not followed by intro p'
    html = html[:m.end()] + '\n\n' + wrap_indent(LEADER, '      ') + '\n\n' + html[m.end():]
    log.append('leader')

    # 3) 300x250 after first paragraph following the leaderboard (the intro paragraph)
    lp = html.index('<span class="ad-label">Advertisement</span>', m.end())
    first_p_close = html.find('</p>', lp)
    assert first_p_close != -1, p + ': no paragraph after header'
    html = html[:first_p_close + 4] + '\n\n' + wrap_indent(RECT, '      ') + '\n' + html[first_p_close + 4:]
    log.append('rect')

    # 4) 468x60 before the LAST h2 (near the end of content)
    last_h2 = html.rfind('<h2>')
    assert last_h2 != -1, p + ': no h2'
    html = html[:last_h2] + wrap_indent(BANNER, '      ') + '\n\n' + html[last_h2:]
    log.append('banner')

    # 5) close article-main, append sidebar before </main>
    tail = '    </aside>\n  </main>'
    assert tail in html, p + ': author/related aside tail missing'
    html = html.replace(tail, '    </aside>\n    </div>\n\n' + wrap_indent(SIDEBAR, '    ') + '\n  </main>', 1)
    log.append('sidebar')

    write(p, html)
    return p, log

def process_index():
    p = 'index.html'
    html = read(p)
    orig = html
    log = []

    # remove stale nap5k zone script
    html = re.sub(r'<script>\(function\(s\)\{s\.dataset\.zone=.*?</script>\n', '', html, count=1)
    log.append('removed_nap5k')

    html = add_social_bar(html); log.append('social_bar')

    hero_end = '</section>\n\n    <section class="container featured" id="featured">'
    assert hero_end in html, 'index: hero-end pattern'
    html = html.replace(hero_end, '</section>\n\n' + wrap_indent(LEADER, '    ') + '\n\n    <section class="container featured" id="featured">', 1)
    log.append('leader_after_hero')

    # native after 4th card in featured
    cards = list(re.finditer(r'<article class="card">', html))
    assert len(cards) >= 4, 'index: fewer than 4 cards'
    c4 = cards[3].start()
    close4 = html.find('</article>', c4)
    html = html[:close4 + len('</article>')] + '\n\n' + wrap_indent(NATIVE, '    ') + '\n' + html[close4 + len('</article>'):]
    log.append('native_mid_featured')

    feat_end = '</section>\n\n    <section class="container categories" id="ai">'
    assert feat_end in html, 'index: featured-end pattern'
    html = html.replace(feat_end, '</section>\n\n' + wrap_indent(RECT, '    ') + '\n\n    <section class="container categories" id="ai">', 1)
    log.append('rect_before_ai')

    ai_end = '</section>\n\n    <section class="container categories" id="cybersecurity">'
    assert ai_end in html, 'index: ai-end pattern'
    html = html.replace(ai_end, '</section>\n\n' + wrap_indent(BANNER, '    ') + '\n\n    <section class="container categories" id="cybersecurity">', 1)
    log.append('banner_before_cyber')

    html = html.replace('  </main>', wrap_indent(MOBILE, '    ') + '\n  </main>', 1)
    log.append('mobile_before_footer')

    write(p, html)
    return p, log

def process_blog():
    p = 'blog.html'
    html = read(p)
    log = []

    html = add_social_bar(html); log.append('social_bar')

    intro = '<p>All TechCipher articles and guides. New ones drop regularly.</p>'
    assert intro in html, 'blog: intro missing'
    html = html.replace(intro, intro + '\n\n' + wrap_indent(LEADER, '    '), 1)
    log.append('leader_after_intro')

    # native after 4th card
    cards = list(re.finditer(r'<article class="card">', html))
    assert len(cards) >= 4, 'blog: fewer than 4 cards'
    c4 = cards[3].start()
    close4 = html.find('</article>', c4)
    html = html[:close4 + len('</article>')] + '\n\n' + wrap_indent(NATIVE, '    ') + '\n' + html[close4 + len('</article>'):]
    log.append('native_mid_list')

    # 300x250 before 6th card
    c6 = cards[5].start()
    html = html[:c6] + wrap_indent(RECT, '    ') + '\n\n' + html[c6:]
    log.append('rect_before_card6')

    html = html.replace('  </main>', wrap_indent(BANNER, '    ') + '\n  </main>', 1)
    log.append('banner_before_footer')

    write(p, html)
    return p, log

def process_simple(name, extra_banner=False):
    """about.html / contact.html — small pages."""
    p = name + '.html'
    html = read(p)
    log = []

    html = add_social_bar(html); log.append('social_bar')

    # leaderboard after first paragraph
    m = re.search(r'<h1>.*?</h1>', html, re.S)
    assert m, p + ': no h1'
    fp = html.find('</p>', m.end())
    assert fp != -1, p + ': no paragraph'
    html = html[:fp + 4] + '\n\n' + wrap_indent(LEADER, '    ') + '\n' + html[fp + 4:]
    log.append('leader')

    # rect before </article>
    html = html.replace('    </article>', wrap_indent(RECT, '    ') + '\n    </article>', 1)
    log.append('rect')

    if extra_banner:
        html = html.replace('    </article>', wrap_indent(BANNER, '    ') + '\n    </article>', 1)
        log.append('banner')

    write(p, html)
    return p, log

def main():
    results = []
    for a in ARTICLES:
        results.append(process_article(a))
    results.append(process_index())
    results.append(process_blog())
    results.append(process_simple('about', extra_banner=True))
    results.append(process_simple('contact'))
    for p, log in results:
        print('{:<55} {}'.format(p, ', '.join(log)))
    print('\nDone. Files processed:', len(results))

if __name__ == '__main__':
    main()
