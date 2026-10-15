import json
import sys

# Ensure UTF-8 output in Windows PowerShell
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def list_all_lessons():
    with open('data/lessons_data.json', 'r', encoding='utf-8') as f:
        lessons = json.load(f)

    print("=" * 70)
    print(f"📚 FACEBOOK VIDEO LEARNING SERIES : ENGR. MD SHOUVIKUR RAHMAN (ICT CARE)")
    print(f"📊 মোট লেসন সংখ্যা: {len(lessons)} টি (Lesson 01 থেকে Lesson {len(lessons):02d})")
    print(f"🔗 সোর্স: mdshouvikurrahman & ICT CARE (https://www.facebook.com/share/v/19Le17KWpv/)")
    print("=" * 70)
    print("\n[ক্রমানুসারে সম্পন্ন হওয়া লেসনগুলোর তালিকা]:\n")
    
    for l in lessons:
        print(f"[{l['lesson_number']}] {l['title']}")
        print(f"     বিষয়: {l['topic']} | লেভেল: {l['learning_level']} | সময়কাল: {l['duration']}")
        print(f"     লিঙ্ক: {l['video_url']}")
        print("-" * 70)

if __name__ == '__main__':
    list_all_lessons()
