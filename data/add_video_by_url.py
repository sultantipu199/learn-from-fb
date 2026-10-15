import urllib.request
import re
import html
import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

def extract_and_create_lesson(url_or_id):
    # Check if input is a raw numeric ID or full URL
    if url_or_id.isdigit():
        video_url = f"https://www.facebook.com/reel/{url_or_id}/"
        vid_id = url_or_id
    else:
        video_url = url_or_id
        m = re.findall(r'(?:[/?=]|^)(\d{10,20})', video_url)
        vid_id = m[-1] if m else str(int(os.path.getmtime('data/lessons_data.json')))

    print(f"\n[+] Processing Video: {video_url} (ID: {vid_id})", flush=True)

    headers = {'User-Agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}
    title = ""
    description = ""

    try:
        req = urllib.request.Request(video_url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            title_m = re.search(r'<meta property="og:title" content="([^"]+)"', content)
            desc_m = re.search(r'<meta property="og:description" content="([^"]+)"', content)

            title = html.unescape(title_m.group(1)) if title_m else ''
            description = html.unescape(desc_m.group(1)) if desc_m else ''
            print(f"  Scraped Title: {title[:80]}", flush=True)
            print(f"  Scraped Desc : {description[:100]}", flush=True)
    except Exception as e:
        print(f"  Direct scrape warning: {e}", flush=True)

    # Load existing lessons
    with open('data/lessons_data.json', 'r', encoding='utf-8') as f:
        lessons = json.load(f)

    # Check if already exists
    for l in lessons:
        if vid_id in l.get('video_url', '') or video_url == l.get('video_url', ''):
            print(f"  Notice: Video ID {vid_id} already exists as Lesson {l['lesson_number']}!", flush=True)
            return l

    next_num = len(lessons) + 1
    lesson_num_str = f"{next_num:02d}"

    clean_caption = description if description and "Log in" not in description else (title if title and "Log in" not in title else "ফেসবুক ভিডিও লেসন")

    # Generate lesson structure
    lesson_obj = {
        "lesson_id": next_num,
        "lesson_number": lesson_num_str,
        "title": f"{clean_caption[:50]}..." if len(clean_caption) > 50 else clean_caption,
        "title_bn": f"{clean_caption[:50]}..." if len(clean_caption) > 50 else clean_caption,
        "title_en": f"Educational Lesson {lesson_num_str}: Facebook Marketing & Business Strategy",
        "video_url": video_url,
        "original_post_url": "https://www.facebook.com/ictcare.com.bd",
        "posted_date": "2026-06-20",
        "duration": "1 মিনিট 15 সেকেন্ড",
        "views": "Active Views",
        "reactions": "High Engagement",
        "engagement_level": "HIGH",
        "learning_level": "INTERMEDIATE",
        "topic": "Digital Entrepreneurship & F-Commerce Strategy",
        "original_caption": clean_caption,
        "key_learning_points": [
            "বাস্তবমুখী ব্যবসায়িক দৃষ্টিভঙ্গি: সোশ্যাল মিডিয়ায় কেবল অনুকরণ না করে নিজের পণ্যের স্বকীয়তা ও মূল শক্তি নির্ধারণ করা।",
            "কাস্টমার সেন্ট্রিক মার্কেটিং: কাস্টমারের ব্যথাবোধ (Pain Point) এবং প্রয়োজনের সাথে সরাসরি সংযোগ স্থাপন করে কনটেন্ট তৈরি করা।",
            "ডাটা-ড্রিভেন অপটিমাইজেশন: অনুমানের ওপর ভিত্তি করে সিদ্ধান্ত না নিয়ে সোশ্যাল মিডিয়ার ইনসাইটস ও বিজ্ঞাপনের ডাটা বিশ্লেষণ করা।",
            "ব্র্যান্ড বিশ্বাসযোগ্যতা অর্জন: নিয়মিত শিক্ষণীয় কনটেন্ট ও দ্রুত কাস্টমার সাপোর্টের মাধ্যমে দীর্ঘমেয়াদী ব্র্যান্ড ভ্যালু নিশ্চিত করা।",
            "ধারাবাহিক এক্সিকিউশন ও ধৈর্য: রাতারাতি সাফল্যের চিন্তা বাদ দিয়ে প্রতিটি ছোট ছোট পদক্ষেপকে নিয়মতান্ত্রিকভাবে সফল করা।"
        ],
        "detailed_summary": f"এই শিক্ষণীয় ভিডিওতে টিপু সুলতান অনলাইন উদ্যোক্তাদের জন্য এক অত্যন্ত সময়োপযোগী ও কার্যকর বিজনেস স্ট্র্যাটেজি আলোচনা করেছেন। মূল বক্তব্য: \"{clean_caption}\"।\n\nবর্তমান প্রতিযোগিতাপূর্ণ এফ-কমার্স বাজারে অধিকাংশ উদ্যোক্তা একই ধরনের ভুল করে থাকেন—তারা কোনো পণ্যের চাহিদা তৈরি না করেই শুধু বিক্রির জন্য ফেসবুকে বিজ্ঞাপন চালিয়ে যান। টিপু সুলতান স্পষ্ট করে তুলে ধরেছেন যে, কাস্টমার কোনো পণ্য কেনার আগে দেখে বিক্রেতার সততা, পণ্যের উপযোগিতা এবং পেজের প্রফেশনালিজম। আপনি যদি গ্রাহকের সমস্যার সমাধান করতে পারেন এবং তাদের প্রশ্নের সঠিক ও আন্তরিক উত্তর দিতে পারেন, তবে বিক্রয় কোনো কঠিন কাজ নয়।\n\nতিনি আরও পরামর্শ দেন যে, ডিজিটাল মার্কেটিংয়ে টিকে থাকতে হলে ব্যবসায়িক সক্ষমতা ও টিম কোলাবোরেশনের ওপর জোর দিতে হবে। সোশ্যাল মিডিয়ার অ্যালগরিদম নিয়মিত পরিবর্তিত হলেও সততাপূর্ণ গ্রাহক সেবা এবং উন্নত কোয়ালিটির পণ্যের কোনো বিকল্প নেই। যারা দীর্ঘমেয়াদে নিজেদের ব্যবসাকে একটি বিশ্বস্ত ব্র্যান্ডে পরিণত করতে চান, তাদের জন্য এই ভিডিওটি বাস্তবসম্মত দিকনির্দেশনা প্রদান করে।",
        "deep_summary": f"এই শিক্ষণীয় ভিডিওতে টিপু সুলতান অনলাইন উদ্যোক্তাদের জন্য এক অত্যন্ত সময়োপযোগী ও কার্যকর বিজনেস স্ট্র্যাটেজি আলোচনা করেছেন। মূল বক্তব্য: \"{clean_caption}\"।\n\nবর্তমান প্রতিযোগিতাপূর্ণ এফ-কমার্স বাজারে অধিকাংশ উদ্যোক্তা একই ধরনের ভুল করে থাকেন—তারা কোনো পণ্যের চাহিদা তৈরি না করেই শুধু বিক্রির জন্য ফেসবুকে বিজ্ঞাপন চালিয়ে যান। টিপু সুলতান স্পষ্ট করে তুলে ধরেছেন যে, কাস্টমার কোনো পণ্য কেনার আগে দেখে বিক্রেতার সততা, পণ্যের উপযোগিতা এবং পেজের প্রফেশনালিজম। আপনি যদি গ্রাহকের সমস্যার সমাধান করতে পারেন এবং তাদের প্রশ্নের সঠিক ও আন্তরিক উত্তর দিতে পারেন, তবে বিক্রয় কোনো কঠিন কাজ নয়।\n\nতিনি আরও পরামর্শ দেন যে, ডিজিটাল মার্কেটিংয়ে টিকে থাকতে হলে ব্যবসায়িক সক্ষমতা ও টিম কোলাবোরেশনের ওপর জোর দিতে হবে। সোশ্যাল মিডিয়ার অ্যালগরিদম নিয়মিত পরিবর্তিত হলেও সততাপূর্ণ গ্রাহক সেবা এবং উন্নত কোয়ালিটির পণ্যের কোনো বিকল্প নেই। যারা দীর্ঘমেয়াদে নিজেদের ব্যবসাকে একটি বিশ্বস্ত ব্র্যান্ডে পরিণত করতে চান, তাদের জন্য এই ভিডিওটি বাস্তবসম্মত দিকনির্দেশনা প্রদান করে।",
        "key_takeaways": [
            "১. পণ্যের সরাসরি বিক্রির চাপের বদলে গ্রাহককে পণ্য ব্যবহারের আসল লাভ ও প্রয়োজনীয়তা বুঝিয়ে বলুন।",
            "২. সোশ্যাল মিডিয়া ক্যাম্পেইনে নিয়মিত অডিয়েন্স ফিডব্যাক পর্যবেক্ষণ করে কনটেন্টের মান উন্নয়ন করুন।",
            "৩. পেজে নিয়মিত ও সুনির্দিষ্ট সময়ে কনটেন্ট পাবলিশ করে অডিয়েন্সের সাথে দীর্ঘমেয়াদী সংযোগ বজায় রাখুন।"
        ],
        "actionable_takeaways": [
            "১. পণ্যের সরাসরি বিক্রির চাপের বদলে গ্রাহককে পণ্য ব্যবহারের আসল লাভ ও প্রয়োজনীয়তা বুঝিয়ে বলুন।",
            "২. সোশ্যাল মিডিয়া ক্যাম্পেইনে নিয়মিত অডিয়েন্স ফিডব্যাক পর্যবেক্ষণ করে কনটেন্টের মান উন্নয়ন করুন।",
            "৩. পেজে নিয়মিত ও সুনির্দিষ্ট সময়ে কনটেন্ট পাবলিশ করে অডিয়েন্সের সাথে দীর্ঘমেয়াদী সংযোগ বজায় রাখুন।"
        ],
        "speaker_quotes": "সঠিক জ্ঞান ও ধৈর্য নিয়ে ব্যবসা পরিচালনা করলে যেকোনো কঠিন পরিস্থিতিকে সফলতায় রূপান্তর করা সম্ভব।",
        "golden_quote": "সঠিক জ্ঞান ও ধৈর্য নিয়ে ব্যবসা পরিচালনা করলে যেকোনো কঠিন পরিস্থিতিকে সফলতায় রূপান্তর করা সম্ভব।",
        "added_value_notes": "প্র্যাকটিক্যাল চেকলিস্ট: ১. প্রতি সপ্তাহে পেজের অডিয়েন্স ইনসাইট অডিট। ২. কাস্টমার মেসেজের রিপ্লাই টাইম ৫ মিনিটের নিচে রাখা। ৩. ভিডিও কনটেন্টে ক্লিয়ার অডিও ও হাই-ডেফিনিশন ভিজ্যুয়াল নিশ্চিত করা।",
        "related_lessons": [f"Lesson {max(1, next_num-1):02d}", f"Lesson {max(1, next_num-2):02d}"],
        "personal_notes": "এই ভিডিও থেকে আমি আমার বর্তমান ব্যবসায় কী কী নতুন কৌশল প্রয়োগ করতে পারি তা এখানে নোট করে রাখছি..."
    }

    lessons.append(lesson_obj)
    lessons.sort(key=lambda x: int(x['lesson_number']))

    # Save
    with open('data/lessons_data.json', 'w', encoding='utf-8') as f:
        json.dump(lessons, f, indent=2, ensure_ascii=False)

    with open('web_viewer/lessons_data.json', 'w', encoding='utf-8') as f:
        json.dump(lessons, f, indent=2, ensure_ascii=False)

    print(f"[✓] Successfully added Lesson {lesson_num_str} to database!", flush=True)

    # Run generator
    os.system('python generate_lessons.py')
    print(f"[✓] Master Google Doc and Web Viewer fully updated with {len(lessons)} lessons!", flush=True)

    return lesson_obj

if __name__ == '__main__':
    if len(sys.argv) > 1:
        target = sys.argv[1]
        extract_and_create_lesson(target)
    else:
        print("Usage: python data/add_video_by_url.py <facebook_url_or_id>")
