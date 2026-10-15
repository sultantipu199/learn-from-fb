import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://www.facebook.com/share/g/1Jw5R8cmgq/"
headers = {
    'User-Agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'
}

try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        final_url = resp.geturl()
        content = resp.read().decode('utf-8', errors='ignore')
        print(f"Final URL: {final_url}")
        
        title_m = re.search(r'<meta property="og:title" content="([^"]+)"', content)
        desc_m = re.search(r'<meta property="og:description" content="([^"]+)"', content)
        print("og:title:", title_m.group(1) if title_m else "N/A")
        print("og:description:", desc_m.group(1) if desc_m else "N/A")

        # Save HTML
        with open('data/group_share_inspect.html', 'w', encoding='utf-8') as f:
            f.write(content)
except Exception as e:
    print(f"Error fetching URL: {e}")
