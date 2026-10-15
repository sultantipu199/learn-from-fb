import urllib.request
import re
import json
import html
import sys
import time

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

with open('data/ictcare_discovered_videos.json', 'r', encoding='utf-8') as f:
    videos = json.load(f)

all_ids = list(videos.keys())
print(f"Total candidate IDs to scan: {len(all_ids)}")

headers = {'User-Agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}

valid_videos = []

for idx, vid in enumerate(all_ids, 1):
    url = f'https://www.facebook.com/reel/{vid}/'
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=4) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            
            title_m = re.search(r'<meta property="og:title" content="([^"]+)"', content)
            desc_m = re.search(r'<meta property="og:description" content="([^"]+)"', content)
            
            title = html.unescape(title_m.group(1)) if title_m else ''
            desc = html.unescape(desc_m.group(1)) if desc_m else ''
            
            if desc and len(desc.strip()) > 3:
                # Extract views and reactions if present in title
                print(f"[{idx}/{len(all_ids)}] Valid Video ID: {vid}")
                print(f"  Title: {title}")
                print(f"  Desc:  {desc[:120]}...")
                valid_videos.append({
                    'id': vid,
                    'url': url,
                    'title': title,
                    'description': desc
                })
    except Exception:
        pass

print(f"\nTotal authentic videos with captions found: {len(valid_videos)}")

with open('data/all_ictcare_valid_videos.json', 'w', encoding='utf-8') as f:
    json.dump(valid_videos, f, indent=2, ensure_ascii=False)
