import os
import glob
import re
import sys
import json
import urllib.parse

sys.stdout.reconfigure(encoding='utf-8')

all_found_videos = {}

for p in glob.glob('data/page_*.html'):
    print(f"\n==========================================")
    print(f"File: {p} ({os.path.getsize(p)} bytes)")
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        src = f.read()

    # Find all hrefs
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', src)
    print(f"Total hrefs: {len(hrefs)}")

    # Extract all video IDs with slugs or params
    for h in hrefs:
        # Unquote URL
        decoded_h = urllib.parse.unquote(h)
        # Check patterns:
        # /videos/<slug>/<id>/
        # /videos/<id>/
        # /watch/?v=<id>
        # /reel/<id>/
        m = re.search(r'(?:/videos/(?:[^/"]+/)?|/watch/\?v=|/reel/)(\d{10,20})', decoded_h)
        if m:
            vid_id = m.group(1)
            # Filter out known page IDs if they get confused
            if vid_id not in ['100086700362704', '100067541701446', '61593174121107']:
                if vid_id not in all_found_videos:
                    all_found_videos[vid_id] = {
                        'id': vid_id,
                        'href': decoded_h,
                        'file': os.path.basename(p)
                    }
                    print(f"  Found ID: {vid_id} -> {decoded_h[:100]}")

print(f"\n==========================================")
print(f"Total Unique Valid Video IDs Discovered Across All Pages: {len(all_found_videos)}")
print(f"==========================================")

with open('data/discovered_unique_videos.json', 'w', encoding='utf-8') as f:
    json.dump(all_found_videos, f, indent=2, ensure_ascii=False)
