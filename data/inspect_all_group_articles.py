import re
import json
import html
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/group_page_deep.html', 'r', encoding='utf-8', errors='ignore') as f:
    src = f.read()

message_matches = re.findall(r'"message":\{"text":"(.*?)"\}', src)
print(f"Total raw message matches: {len(message_matches)}")

unique_posts = []
seen_texts = set()

for idx, m in enumerate(message_matches, 1):
    cleaned = m.encode('utf-8', errors='ignore').decode('unicode-escape', errors='ignore')
    cleaned = html.unescape(cleaned)
    # Remove surrogate characters
    cleaned = cleaned.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
    
    first_line = cleaned.strip().split('\n')[0] if cleaned else ''
    if len(cleaned) > 200 and first_line not in seen_texts:
        seen_texts.add(first_line)
        unique_posts.append({
            'post_number': len(unique_posts) + 1,
            'length': len(cleaned),
            'first_line': first_line,
            'full_text': cleaned
        })
        print(f"\n==========================================")
        print(f"Post {len(unique_posts)} ({len(cleaned)} chars): {first_line[:80]}")
        print(f"==========================================")
        lines = [l for l in cleaned.split('\n') if l.strip()]
        for l in lines[:6]:
            print("  ", l[:90])

with open('data/group_articles_clean.json', 'w', encoding='utf-8', errors='ignore') as f:
    json.dump(unique_posts, f, indent=2, ensure_ascii=False)

print(f"\nSaved {len(unique_posts)} unique comprehensive articles to data/group_articles_clean.json")
