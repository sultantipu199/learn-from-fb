import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/lessons_data.json', 'r', encoding='utf-8') as f:
    lessons = json.load(f)
print(f'Total current lessons in lessons_data.json: {len(lessons)}')

lesson_urls = set()
for l in lessons:
    url = l.get('video_url', '')
    lesson_urls.add(url)
    # Also strip trailing slashes or normalize
    clean_url = url.rstrip('/')
    lesson_urls.add(clean_url)

print('Current lessons breakdown:')
for l in lessons:
    print(f"Lesson {int(l['lesson_number']):02d}: {l['title_en']} | {l['video_url']}")

print("\n--- Checking all_ictcare_valid_videos.json ---")
if os.path.exists('data/all_ictcare_valid_videos.json'):
    with open('data/all_ictcare_valid_videos.json', 'r', encoding='utf-8') as f:
        all_ict = json.load(f)
    print(f'Total items in all_ictcare_valid_videos.json: {len(all_ict)}')
    unprocessed_ict = []
    for item in all_ict:
        url = item if isinstance(item, str) else item.get('url', '')
        if url.rstrip('/') not in lesson_urls:
            unprocessed_ict.append(item)
    print(f'Unprocessed from all_ictcare_valid_videos: {len(unprocessed_ict)}')
    for u in unprocessed_ict[:10]:
        print("  Unprocessed:", u)

print("\n--- Checking ictcare_discovered_videos.json ---")
if os.path.exists('data/ictcare_discovered_videos.json'):
    with open('data/ictcare_discovered_videos.json', 'r', encoding='utf-8') as f:
        disc = json.load(f)
    print(f'Total items in ictcare_discovered_videos.json: {len(disc)}')
    unprocessed_disc = []
    for item in disc:
        url = item if isinstance(item, str) else item.get('url', '')
        if url.rstrip('/') not in lesson_urls:
            unprocessed_disc.append(item)
    print(f'Unprocessed from ictcare_discovered_videos: {len(unprocessed_disc)}')
    for u in unprocessed_disc[:10]:
        print("  Unprocessed disc:", u)
