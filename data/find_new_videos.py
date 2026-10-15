import json
import urllib.request
import re
import html
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/ictcare_discovered_videos.json', 'r', encoding='utf-8') as f:
    disc = json.load(f)

print(f"Total IDs to check: {len(disc)}")

with open('data/lessons_data.json', 'r', encoding='utf-8') as f:
    lessons = json.load(f)

existing_ids = set()
for l in lessons:
    url = l.get('video_url', '')
    m = re.findall(r'/(\d+)/?', url)
    if m:
        existing_ids.add(m[-1])

print(f"Existing lesson IDs: {len(existing_ids)}")

headers = {'User-Agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}

valid_new = []
invalid_or_existing = []

for idx, (vid, info) in enumerate(disc.items(), 1):
    if vid in existing_ids:
        continue
    # Skip known page IDs
    if vid in ['100086700362704', '100067541701446', '61593174121107']:
        continue

    # Try both reel and watch URL
    urls_to_try = [
        f"https://www.facebook.com/reel/{vid}/",
        f"https://www.facebook.com/watch/?v={vid}",
        f"https://www.facebook.com/ictcare.com.bd/videos/{vid}/"
    ]

    found = False
    for test_url in urls_to_try:
        try:
            req = urllib.request.Request(test_url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as resp:
                content = resp.read().decode('utf-8', errors='ignore')
                title_m = re.search(r'<meta property="og:title" content="([^"]+)"', content)
                desc_m = re.search(r'<meta property="og:description" content="([^"]+)"', content)

                title = html.unescape(title_m.group(1)) if title_m else ''
                desc = html.unescape(desc_m.group(1)) if desc_m else ''

                # Check if it has a real description or title that is not just "Log in to Facebook"
                if "Log in" not in title and len(title) > 3:
                    print(f"[{idx}/{len(disc)}] SUCCESS: ID {vid}")
                    print(f"   URL: {test_url}")
                    print(f"   Title: {title[:90]}")
                    print(f"   Desc: {desc[:90]}")
                    valid_new.append({
                        'id': vid,
                        'url': test_url,
                        'title': title,
                        'description': desc
                    })
                    found = True
                    break
        except Exception as e:
            pass
    if not found:
        invalid_or_existing.append(vid)

print(f"\n==========================================")
print(f"Found {len(valid_new)} NEW valid videos not currently in lessons!")
print(f"==========================================")

with open('data/newly_discovered_valid_videos.json', 'w', encoding='utf-8') as f:
    json.dump(valid_new, f, indent=2, ensure_ascii=False)
