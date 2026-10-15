import urllib.request
import re
import json
import sys

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

with open('data/ictcare_discovered_videos.json', 'r', encoding='utf-8') as f:
    videos = json.load(f)

# Let's inspect some reel IDs
sample_ids = [
    '1393149402569950', # The user's shared video
    '1839538380157514',
    '743850411433803',
    '687018514255613',
    '1402416007536005',
    '632708143267779',
    '1141317115286920',
    '1639246724606159',
    '1635855486666999',
    '2487180278436382'
]

results = []

headers = {'User-Agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}

for vid in sample_ids:
    url = f'https://www.facebook.com/reel/{vid}/'
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            
            title_m = re.search(r'<meta property="og:title" content="([^"]+)"', content)
            desc_m = re.search(r'<meta property="og:description" content="([^"]+)"', content)
            
            title = title_m.group(1) if title_m else ''
            desc = desc_m.group(1) if desc_m else ''
            
            print(f"ID {vid}:")
            print("  Title:", title[:100])
            print("  Desc :", desc[:150])
            results.append({
                'id': vid,
                'url': url,
                'title': title,
                'description': desc
            })
    except Exception as e:
        print(f"ID {vid} error: {e}")

with open('data/ictcare_reels_metadata.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
