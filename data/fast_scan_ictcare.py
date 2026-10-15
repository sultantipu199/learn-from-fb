import urllib.request
import re
import json
import html
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

with open('data/ictcare_discovered_videos.json', 'r', encoding='utf-8') as f:
    videos = json.load(f)

all_ids = list(videos.keys())
print(f"Total candidate IDs to scan in parallel: {len(all_ids)}")

headers = {'User-Agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}

def check_video(vid):
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
                return {
                    'id': vid,
                    'url': url,
                    'title': title,
                    'description': desc
                }
    except Exception:
        pass
    return None

valid_videos = []

with ThreadPoolExecutor(max_workers=15) as executor:
    futures = {executor.submit(check_video, vid): vid for vid in all_ids}
    for fut in as_completed(futures):
        res = fut.result()
        if res:
            print(f"Found valid video {res['id']}: {res['description'][:80]}...", flush=True)
            valid_videos.append(res)

print(f"\nCompleted! Found {len(valid_videos)} authentic videos/reels with descriptions.", flush=True)

with open('data/all_ictcare_valid_videos.json', 'w', encoding='utf-8') as f:
    json.dump(valid_videos, f, indent=2, ensure_ascii=False)
