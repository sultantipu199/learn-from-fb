import os
import re
import json
import glob
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/lessons_data.json', 'r', encoding='utf-8') as f:
    lessons = json.load(f)

existing_ids = set()
for l in lessons:
    m = re.findall(r'(?:[/?=]|^)(\d{10,20})', l.get('video_url', ''))
    if m:
        for mid in m:
            existing_ids.add(mid)

print(f"Total current lessons: {len(lessons)}")
print(f"Total existing unique lesson IDs: {len(existing_ids)}")

all_found_ids = {}

for root, dirs, files in os.walk('.'):
    # ignore .git, .system_generated
    if '.git' in root or '.system_generated' in root:
        continue
    for file in files:
        if file.endswith(('.py', '.json', '.txt', '.html', '.md')):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    matches = re.findall(r'(?:watch\/?\?v=|reel\/|videos\/)(\d{10,20})', content)
                    for mid in matches:
                        if mid not in existing_ids and mid not in ['100086700362704', '100067541701446', '61593174121107']:
                            if mid not in all_found_ids:
                                all_found_ids[mid] = []
                            all_found_ids[mid].append(path)
            except Exception:
                pass

print(f"\nUnprocessed candidate IDs found anywhere in workspace: {len(all_found_ids)}")
for mid, paths in list(all_found_ids.items())[:20]:
    print(f"ID {mid} found in: {list(set(paths))[:2]}")
