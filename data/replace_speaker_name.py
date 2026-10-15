import json
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Replacement pairs - ordered from longest to shortest to prevent partial substring match issues
replacements = [
    # Bengali replacements
    ("ইঞ্জিনিয়ার মোঃ সৌভিকুর রহমান", "টিপু সুলতান"),
    ("ইঞ্জিনিয়ার মো. সৌভিকুর রহমান", "টিপু সুলতান"),
    ("ইঞ্জি. মোঃ শৌভিকুর রহমান", "টিপু সুলতান"),
    ("ইঞ্জি. মো. শৌভিকুর রহমান", "টিপু সুলতান"),
    ("ইঞ্জিনিয়ার শৌভিকুর রহমান", "টিপু সুলতান"),
    ("ইঞ্জিনিয়ার সৌভিকুর রহমান", "টিপু সুলতান"),
    ("মোঃ সৌভিকুর রহমানের", "টিপু সুলতানের"),
    ("মো. সৌভিকুর রহমানের", "টিপু সুলতানের"),
    ("মোঃ শৌভিকুর রহমানের", "টিপু সুলতানের"),
    ("মো. শৌভিকুর রহমানের", "টিপু সুলতানের"),
    ("মোঃ সৌভিকুর রহমান", "টিপু সুলতান"),
    ("মো. সৌভিকুর রহমান", "টিপু সুলতান"),
    ("মোঃ শৌভিকুর রহমান", "টিপু সুলতান"),
    ("মো. শৌভিকুর রহমান", "টিপু সুলতান"),
    ("সৌভিকুর রহমানের", "টিপু সুলতানের"),
    ("শৌভিকুর রহমানের", "টিপু সুলতানের"),
    ("সৌভিকুর রহমান", "টিপু সুলতান"),
    ("শৌভিকুর রহমান", "টিপু সুলতান"),
    ("সৌভিক রহমানের", "টিপু সুলতানের"),
    ("শৌভিক রহমানের", "টিপু সুলতানের"),
    ("সৌভিক রহমান", "টিপু সুলতান"),
    ("শৌভিক রহমান", "টিপু সুলতান"),
    ("সৌভিকের", "টিপু সুলতানের"),
    ("শৌভিকের", "টিপু সুলতানের"),
    
    # English replacements
    ("Engr. Md. Shouvikur Rahman", "Tipu Sultan"),
    ("Engr. Md Shouvikur Rahman", "Tipu Sultan"),
    ("Md. Shouvikur Rahman", "Tipu Sultan"),
    ("Md Shouvikur Rahman", "Tipu Sultan"),
    ("MD SHOUVIKUR RAHMAN", "TIPU SULTAN"),
    ("Shouvikur Rahman", "Tipu Sultan"),
    ("SHOUVIKUR RAHMAN", "TIPU SULTAN"),
    ("Engr. Shouvikur Rahman", "Tipu Sultan"),
]

def apply_replacements(text):
    for old, new in replacements:
        text = text.replace(old, new)
    return text

print("--- Updating data/lessons_data.json ---")
with open('data/lessons_data.json', 'r', encoding='utf-8') as f:
    lessons_text = f.read()

lessons_text = apply_replacements(lessons_text)

with open('data/lessons_data.json', 'w', encoding='utf-8') as f:
    f.write(lessons_text)

with open('web_viewer/lessons_data.json', 'w', encoding='utf-8') as f:
    f.write(lessons_text)
print("Updated lessons_data.json in both data/ and web_viewer/!")

print("--- Updating generate_lessons.py ---")
with open('generate_lessons.py', 'r', encoding='utf-8') as f:
    gen_text = f.read()

gen_text = apply_replacements(gen_text)
# Also check for any standalone Shouvik references
gen_text = gen_text.replace("Md Shouvikur Rahman", "Tipu Sultan")
gen_text = gen_text.replace("MD SHOUVIKUR RAHMAN", "TIPU SULTAN")

with open('generate_lessons.py', 'w', encoding='utf-8') as f:
    f.write(gen_text)
print("Updated generate_lessons.py!")

print("--- Updating web_viewer/index.html ---")
with open('web_viewer/index.html', 'r', encoding='utf-8') as f:
    html_text = f.read()

html_text = apply_replacements(html_text)

with open('web_viewer/index.html', 'w', encoding='utf-8') as f:
    f.write(html_text)
print("Updated web_viewer/index.html!")

print("--- Updating web_viewer/app.js ---")
with open('web_viewer/app.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

js_text = apply_replacements(js_text)

with open('web_viewer/app.js', 'w', encoding='utf-8') as f:
    f.write(js_text)
print("Updated web_viewer/app.js!")

print("--- Updating README.md ---")
with open('README.md', 'r', encoding='utf-8') as f:
    readme_text = f.read()

readme_text = apply_replacements(readme_text)

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme_text)
print("Updated README.md!")

print("--- Updating data/add_video_by_url.py ---")
with open('data/add_video_by_url.py', 'r', encoding='utf-8') as f:
    tool_text = f.read()

tool_text = apply_replacements(tool_text)

with open('data/add_video_by_url.py', 'w', encoding='utf-8') as f:
    f.write(tool_text)
print("Updated data/add_video_by_url.py!")

print("\n--- Regenerating Master Documents via generate_lessons.py ---")
os.system("python generate_lessons.py")
print("Regeneration completed!")
