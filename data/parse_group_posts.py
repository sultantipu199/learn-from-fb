import re
import json
import html
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

with open('data/group_page.html', 'r', encoding='utf-8', errors='ignore') as f:
    src = f.read()

print(f"Total HTML size: {len(src)} bytes")

# Check for text mentioning Shouvikur / Shouvik / ICT Care
matches_shouvik = re.findall(r'[^।\n]{0,50}(?:শৌভিক|সৌভিক|শফিক|Shouvik)[^।\n]{0,50}', src)
print(f"Direct text matches for Shouvik/Shofiqur: {len(matches_shouvik)}")
for m in matches_shouvik[:10]:
    print("  ", m.strip())

# Check for relay store or embedded JSON data
# Facebook encodes group post text in GraphQL relays with "text":"..." or "story":{...}
# Let's search for "text":"..." blocks that are longer than 100 characters
text_blocks = re.findall(r'"text":"([^"]{80,3000})"', src)
print(f"\nFound {len(text_blocks)} long text blocks in JSON payloads.")

# Find post permalinks: /groups/ictcarecommunity/posts/<id>/ or /permalink/<id>/
post_links = re.findall(r'href="([^"]*(?:posts|permalink)[^"]*)"', src)
print(f"Found {len(post_links)} post links:")
for pl in list(set(post_links))[:10]:
    print("  Link:", pl)

# Let's inspect long texts to find articles by Md Shouvikur Rahman / Admin
articles = []
for idx, tb in enumerate(text_blocks, 1):
    unescaped = tb.encode().decode('unicode-escape', errors='ignore')
    unescaped = html.unescape(unescaped)
    if len(unescaped) > 150:
        articles.append(unescaped)
        print(f"\n[Article {idx} - {len(unescaped)} chars]:")
        print(unescaped[:200] + "...")

with open('data/group_extracted_articles.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, indent=2, ensure_ascii=False)
