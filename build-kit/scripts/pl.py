import json
s=json.load(open('/dev/stdin'))['content']
s=s.replace("(as of 28 Sep 2026)","(as of 29 Sep 2026)")
old="A student picks the paper and question (or a topic) and gets:"
new="""It has three modes.

**Mark my exam (the default, main mode).**
- The student picks the paper they sat.
- **Exam 1:** they tap the letters they chose, and it auto-marks against the key; or they tick right/wrong. The VCAA sample has no key, so it's ticks only.
- **Exam 2:** they tap the marks they got for each part, marking themselves with the examiners' report.
- It shows their score and the state average.
- Then it builds a **study guide**: topics where they lost marks, ranked by marks lost × topic priority. Each topic has only three lists, as the teacher asked:
  1. YouTube videos: the walkthroughs of the questions they got wrong, plus teaching and calculator videos.
  2. Textbook tasks, grouped by Cambridge section.
  3. Exam questions to practise from other papers, each with Show and Solution.
- Results are saved on the student's own device only (browser storage). There's no class view.

**One question** and **By topic** (the earlier lookup). A student picks the paper and question (or a topic) and gets:"""
assert old in s; s=s.replace(old,new)
print(s)
