import sys
import json
import re
from bs4 import BeautifulSoup

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

with open('data/inspect_new_video.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

print('=== Title ===')
print(soup.title.string if soup.title else 'No Title')

print('\n=== Meta Tags ===')
for m in soup.find_all('meta'):
    name = m.get('name') or m.get('property') or ''
    content = m.get('content') or ''
    if any(k in name.lower() for k in ['title', 'description', 'og:', 'author', 'twitter:']):
        print(f'{name} -> {content}')

print('\n=== Scripts containing key data ===')
for s in soup.find_all('script'):
    txt = s.string or ''
    if '1393149402569950' in txt:
        print(f'Found script tag of length {len(txt)}')
        # Search for creator / page name
        names = re.findall(r'"name":"([^"]+)"', txt)
        print('Found names:', names[:10])
        messages = re.findall(r'"text":"([^"]+)"', txt)
        print('Found texts:', messages[:10])
        urls = re.findall(r'"url":"([^"]+)"', txt)
        print('Found URLs:', urls[:5])
