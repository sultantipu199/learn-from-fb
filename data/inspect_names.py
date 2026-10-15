import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/lessons_data.json', 'r', encoding='utf-8') as f:
    lessons = json.load(f)

for l in lessons:
    text = json.dumps(l, ensure_ascii=False)
    matches = re.findall(r'[^।\n]{0,35}[শস]ৌভিক[^।\n]{0,35}', text)
    if matches:
        print(f"Lesson {l['lesson_number']}:")
        for m in matches:
            print(f"   {m.strip()}")
