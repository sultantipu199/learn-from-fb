import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("data/chrome_fb_page.html", "r", encoding="utf-8") as f:
    html = f.read()

print("HTML Length:", len(html))

# Check for all links
links = re.findall(r'href="([^"]+)"', html)
print(f"Total hrefs: {len(links)}")
fb_links = [l for l in set(links) if 'facebook.com' in l or l.startswith('/')]
print(f"Total Facebook links: {len(fb_links)}")

# Search for any posts, videos, or text
video_links = [l for l in fb_links if '/videos' in l or '/reel' in l or 'watch' in l]
print(f"Video links ({len(video_links)}):")
for v in video_links[:20]:
    print("  ", v)

# Check for modal / login dialog text
for term in ['See more on Facebook', 'Log In', 'Create new account', 'Not now']:
    if term in html:
        print(f"Found dialog text: '{term}'")

# Look for actual posts or text content
text_snippets = re.findall(r'>([^<]{30,})<', html)
print(f"\nText snippets found: {len(text_snippets)}")
for s in text_snippets[:15]:
    cleaned = s.strip()
    if cleaned and not cleaned.startswith('{') and not cleaned.startswith('.'):
        print("  - ", cleaned[:100])
