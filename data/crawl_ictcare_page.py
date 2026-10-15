import time
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def extract_ictcare_videos():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--lang=bn-BD')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    driver = webdriver.Chrome(options=options)
    
    urls_to_crawl = [
        'https://www.facebook.com/ictcare.com.bd/videos/',
        'https://www.facebook.com/ictcare.com.bd/reels/',
        'https://www.facebook.com/reel/1393149402569950/'
    ]
    
    all_found_videos = []

    for target_url in urls_to_crawl:
        print(f"Crawling {target_url}...")
        try:
            driver.get(target_url)
            time.sleep(6)
            
            # Scroll down multiple times to load dynamic grid
            for i in range(5):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                
            page_src = driver.page_source
            
            # Extract video IDs and links
            # Pattern 1: /watch/?v=ID
            # Pattern 2: /reel/ID/
            # Pattern 3: /videos/ID/
            matches_watch = re.findall(r'href="([^"]*(?:watch\/\?v=|reel\/|videos\/)(\d+)[^"]*)"', page_src)
            for href, vid_id in matches_watch:
                all_found_videos.append({
                    'id': vid_id,
                    'href': href,
                    'source_page': target_url
                })
                
            # Also extract from script tags
            script_ids = re.findall(r'"(?:video_id|id)":"(\d{10,20})"', page_src)
            for sid in script_ids:
                all_found_videos.append({
                    'id': sid,
                    'href': f'https://www.facebook.com/reel/{sid}/',
                    'source_page': target_url
                })

            print(f"Done crawling {target_url}, found {len(matches_watch)} dom matches and {len(script_ids)} script matches.")
        except Exception as e:
            print(f"Error crawling {target_url}: {e}")

    driver.quit()

    # Deduplicate by ID
    unique_videos = {}
    for item in all_found_videos:
        vid = item['id']
        if vid not in unique_videos:
            unique_videos[vid] = item

    print(f"\nTotal unique video/reel IDs discovered: {len(unique_videos)}")
    with open('data/ictcare_discovered_videos.json', 'w', encoding='utf-8') as f:
        json.dump(unique_videos, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    extract_ictcare_videos()
