import json
import urllib.request
import re
import html
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

with open('data/ictcare_discovered_videos.json', 'r', encoding='utf-8') as f:
    disc = json.load(f)

with open('data/lessons_data.json', 'r', encoding='utf-8') as f:
    lessons = json.load(f)

existing_ids = set()
for l in lessons:
    url = l.get('video_url', '')
    m = re.findall(r'/(\d+)/?', url)
    if m:
        existing_ids.add(m[-1])

headers = {'User-Agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}

def check_video_id(vid):
    if vid in existing_ids:
        return None
    if vid in ['100086700362704', '100067541701446', '61593174121107']:
        return None

    urls = [
        f"https://www.facebook.com/reel/{vid}/",
        f"https://www.facebook.com/watch/?v={vid}"
    ]

    for u in urls:
        try:
            req = urllib.request.Request(u, headers=headers)
            with urllib.request.urlopen(req, timeout=3) as resp:
                content = resp.read().decode('utf-8', errors='ignore')
                title_m = re.search(r'<meta property="og:title" content="([^"]+)"', content)
                desc_m = re.search(r'<meta property="og:description" content="([^"]+)"', content)

                title = html.unescape(title_m.group(1)) if title_m else ''
                desc = html.unescape(desc_m.group(1)) if desc_m else ''

                if "Log in" not in title and len(title) > 3:
                    return {
                        'id': vid,
                        'url': u,
                        'title': title,
                        'description': desc
                    }
        except Exception:
            pass
    return None

candidate_ids = [vid for vid in disc.keys() if vid not in existing_ids and vid not in ['100086700362704', '100067541701446', '61593174121107']]
print(f"Scanning {len(candidate_ids)} candidates in parallel...", flush=True)

valid_videos = []
with ThreadPoolExecutor(max_workers=15) as executor:
    futures = {executor.submit(check_video_id, vid): vid for vid in candidate_ids}
    for future in as_completed(futures):
        res = future.result()
        if res:
            print(f"-> VALID: {res['id']} | {res['title'][:60]} | {res['description'][:60]}", flush=True)
            valid_videos.append(res)

print(f"\nTotal Valid New Videos Found: {len(valid_videos)}", flush=True)
with open('data/parallel_valid_new_videos.json', 'w', encoding='utf-8') as f:
    json.dump(valid_videos, f, indent=2, ensure_ascii=False)
