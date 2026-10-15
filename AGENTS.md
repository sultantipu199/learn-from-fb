# Autonomous Hybrid Agent Protocol - Learn From FB Project

## Project Overview
This project is an automated AI system that extracts, structures, and converts Facebook video content (from pages/profiles like Md Shouvikur Rahman) into sequential, structured educational lessons (Lesson 01, Lesson 02, etc.) ready for Google Docs and web reading.

## Architecture
- `fb_video_orchestrator.py`: Core extraction, sorting, and educational enrichment engine.
- `generate_lessons.py`: Processor that structures each video into full Bengali + English educational lessons following the exact master prompt blueprint.
- `web_viewer/`: Modern interactive web dashboard to review lessons, view video links, edit notes, and one-click export to Google Docs / Markdown / PDF.
- `output/`: Generated lesson documents in Markdown, HTML, and formatted text for direct Google Docs pasting or API sync.

## Standards
- Strict sequential lesson numbering (Lesson 01, Lesson 02, etc.).
- Deep educational content explaining what the speaker taught with practical additions.
- Zero placeholder content.
- Clean vanilla HTML/CSS/JS for the dashboard.
