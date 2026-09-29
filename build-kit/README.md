# 12MAG Gap Finder — build kit

Everything needed to rebuild or extend the Gap Finder student app. Built with Claude; the easiest way to change it is to open a new Claude chat in the 12MAG Masterclass project, attach or point to this kit, and ask.

## What's here
- The live website is `index.html` + `images.js` at the top of this repository (GitHub Pages serves them).
- `template.html` — the app source. The data is injected at `__DATA__` (from `data/appdata.json`) and `__TUTOR__` (from `scripts/tutor.py`, variable `TB`).
- `data/appdata.json` — every question: paper, number, marks, topic code (`c`), task type (`t`), answer (`a`), state success rate (`s`), video (`v`), image (`img`), matched Cambridge skills (`sk`), option count (`no`); plus each topic's name, videos, skills and textbook sections.
- `scripts/` — the pipeline:
  - `tags.py` — the hand tagging for every paper (one line per question/part). **Add a new paper here first.**
  - `data.py` — the 35 study design codes; `reports.json` — success rates from the examiners' reports.
  - `words.py` / `locate.py` / `crop.py` / `parts.py` — find each question in the PDF and crop the images (tesseract OCR for scanned papers).
  - `video.py` / `res.py` — MaffsGuru walkthrough timestamps and the topic teaching videos.
  - `build.py` / `export.py` — the teacher Excel workbook and `appdata.json`.
  - `t5.js`–`t7.js` — Playwright screenshot tests.

## Rebuild the page
```
python3 -c "import json,sys;sys.path.insert(0,'scripts');from tutor import TB; t=open('template.html').read().replace('__DATA__',open('data/appdata.json').read()).replace('__TUTOR__',json.dumps(TB,ensure_ascii=False)); open('site/index.html','w').write(t)"
```
Scripts assume the working folder `/tmp/w` and the exam PDFs under `02 Past Exams`; adjust paths at the top of `words.py`.

## Adding a new exam (e.g. 2026)
1. Put the PDFs and examiners' report in `02 Past Exams/2026`.
2. Tag each question against the study design in `tags.py` (code + task type), and add its success rates to `reports.json`.
3. Run the crop pipeline to make the `q/` images; check them.
4. Add walkthrough video timestamps if available.
5. Re-export `appdata.json`, rebuild `site/index.html`, run the tests, push to GitHub.
