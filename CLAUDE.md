# CLAUDE.md - Learn From FB Project Guidelines

## Commands
- Run Orchestrator: `python fb_video_orchestrator.py`
- Generate All Lessons: `python generate_lessons.py`
- Launch Local Lesson Viewer: `python -m http.server 8080 --directory web_viewer`

## Project Scope
1. Process Facebook video series into sequential lessons (Lesson 01, Lesson 02, etc.).
2. Extract or formulate:
   - Lesson Title & Topic
   - Video Metadata (URL, Date, Level, Duration)
   - Key Points (3-5 bullet points)
   - Detailed Summary (150-200 words on what speaker taught)
   - Key Takeaways & Value-add tips
   - Notes & Additions section
3. Export outputs in Google Docs-ready format, Markdown (`MASTER_LESSONS.md`), and HTML interactive viewer.
