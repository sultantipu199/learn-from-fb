import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
    'Accept-Language': 'bn-BD,bn;q=0.9,en;q=0.8'
}
req = urllib.request.Request('https://m.facebook.com/ictcare.com.bd/videos/', headers=headers)
try:
    with urllib.request.urlopen(req, timeout=8) as resp:
        content = resp.read().decode('utf-8', errors='ignore')
        print('Status 200 OK. Content length:', len(content))
        links = re.findall(r'href=["\']([^"\']*(?:video|watch|reel)[^"\']*)["\']', content)
        print('Found video-related links on m.facebook.com:', len(links))
        for l in links[:15]:
            print('   Link:', l)
except Exception as e:
    print('Error:', e)
