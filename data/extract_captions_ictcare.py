import json
import re
import sys

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

with open('data/inspect_new_video.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Look for Bengali sentences or text
lines = re.findall(r'"text":"([^"]+)"', html)
valid = []
for l in lines:
    try:
        dec = l.encode().decode('unicode_escape')
        if any('\u0980' <= ch <= '\u09ff' for ch in dec) and len(dec) > 15:
            valid.append(dec)
    except Exception:
        pass

print("Unique Bengali texts found:", len(set(valid)))
for v in list(set(valid))[:15]:
    print("-" * 50)
    print(v)
