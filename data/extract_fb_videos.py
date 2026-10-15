import sys, urllib.request, re, json
sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

# Try the videos tab
url = 'https://www.facebook.com/mdshouvikurrahman/videos/'
req = urllib.request.Request(url, headers=headers)
try:
    resp = urllib.request.urlopen(req, timeout=20)
    html = resp.read().decode('utf-8', errors='replace')
    print(f'Status: {resp.status}, HTML Length: {len(html)} bytes')
    
    # Save raw HTML for analysis
    with open('data/fb_raw_html.txt', 'w', encoding='utf-8') as f:
        f.write(html)
    print('Saved raw HTML to data/fb_raw_html.txt')
    
    # Search for video IDs in various patterns
    video_ids = set(re.findall(r'/videos/(\d+)', html))
    reel_ids = set(re.findall(r'/reel/(\d+)', html))
    watch_ids = set(re.findall(r'watch/\?v=(\d+)', html))
    all_video_refs = set(re.findall(r'"videoID":"(\d+)"', html))
    story_ids = set(re.findall(r'"story_id":"(\d+)"', html))
    
    print(f'\n=== FACEBOOK VIDEO EXTRACTION RESULTS ===')
    print(f'Video path IDs: {len(video_ids)}')
    for v in sorted(video_ids):
        print(f'  /videos/{v}')
    
    print(f'Reel IDs: {len(reel_ids)}')
    for r in sorted(reel_ids):
        print(f'  /reel/{r}')
    
    print(f'Watch IDs: {len(watch_ids)}')
    for w in sorted(watch_ids):
        print(f'  ?v={w}')
        
    print(f'videoID refs: {len(all_video_refs)}')
    for vr in sorted(all_video_refs):
        print(f'  videoID: {vr}')
    
    print(f'story_id refs: {len(story_ids)}')
    
    # Try to find total video count
    count_match = re.findall(r'(\d+)\s*(?:Videos|videos|video)', html)
    if count_match:
        print(f'\nVideo count text found: {count_match}')
    
    # Look for any text about videos
    snippets = re.findall(r'[^<]{0,100}[Vv]ideo[^<]{0,100}', html[:50000])
    print(f'\nVideo-related text snippets (first 10):')
    for s in snippets[:10]:
        print(f'  ...{s.strip()[:120]}...')
        
except Exception as e:
    print(f'Error accessing videos page: {e}')

# Also try the profile page
print('\n\n=== TRYING PROFILE PAGE ===')
url2 = 'https://www.facebook.com/mdshouvikurrahman'
req2 = urllib.request.Request(url2, headers=headers)
try:
    resp2 = urllib.request.urlopen(req2, timeout=20)
    html2 = resp2.read().decode('utf-8', errors='replace')
    print(f'Profile page: {resp2.status}, {len(html2)} bytes')
    
    video_ids2 = set(re.findall(r'/videos/(\d+)', html2))
    reel_ids2 = set(re.findall(r'/reel/(\d+)', html2))
    print(f'Videos found on profile: {len(video_ids2)}')
    print(f'Reels found on profile: {len(reel_ids2)}')
    
    for v in sorted(video_ids2):
        print(f'  /videos/{v}')
    for r in sorted(reel_ids2):
        print(f'  /reel/{r}')
        
except Exception as e:
    print(f'Error: {e}')
