import re
import json
import html
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/group_page.html', 'r', encoding='utf-8', errors='ignore') as f:
    src = f.read()

# Let's find post nodes. In Facebook group HTML:
# Each post has actor (name), creation_time, post_id, message: { text: ... }
# Look for "message":{"text":"..."} or "comet_sections":{"content":{"story":...}}
posts = []

# Pattern 1: Find message text objects
message_matches = re.findall(r'"message":\{"text":"(.*?)"\}', src)
print(f"Found {len(message_matches)} 'message.text' matches:")
for idx, m in enumerate(message_matches, 1):
    cleaned = m.encode().decode('unicode-escape', errors='ignore')
    cleaned = html.unescape(cleaned)
    if len(cleaned) > 100:
        print(f"\n--- Post {idx} ({len(cleaned)} chars) ---")
        print(cleaned[:300] + "...")
        posts.append({
            'index': idx,
            'text': cleaned
        })

with open('data/parsed_group_full_posts.json', 'w', encoding='utf-8') as f:
    json.dump(posts, f, indent=2, ensure_ascii=False)
