import json,sys
s=json.load(open('/tmp/w/doc.json'))['content'] if False else open('/tmp/w/doc.md').read()
R=[("### Tag 1: topic code (33 codes, from the study design)","### Tag 1: topic code (35 codes, from the study design)"),
("- RF8 Finance solver (TVM) use for practical problems\n","- RF8 Finance solver (TVM) use for practical problems\n- RF9 Interest-only loans (balance constant: interest each period = repayment). A sub-type VCAA examines; traceable to reducing balance loans / recurrence relations.\n"),
("- MA6 Populations with culling/restocking (S_{n+1} = T S_n + B)\n","- MA6 Populations with culling/restocking (S_{n+1} = T S_n + B)\n- MA7 Leslie-type (age-structured) population matrices: birth and survival rates from life-cycle diagrams. Not named in the study design but examined (2025 Exam 1 Q29); traceable to transition matrices modelling populations.\n"),
("- **Keep 33 codes.** Don't add finer codes up front.","- **Keep 35 codes.** Don't add finer codes up front."),
("""## Source files
Folder: `C:\\Users\\10941934\\Desktop\\12MAG Masterclass`
- **Study design:** `2023MathematicsSD (7).docx`
- **Samples:** VCAA sample exams, formula sheets and exam specifications. These count as current design.
- **Past papers and reports:** 2023, 2024 and 2025 Exams 1 and 2, plus 2024, 2025 and 2026 NHT Exams 1 and 2, with examiners' reports and assessment guides. File them into the four "current study design" folders.""",
"""## Source files
Folder: `C:\\Users\\10941934\\Desktop\\12MAG Masterclass`
- `01 Study Design & Exam Info`: the study design (`VCE Mathematics Study Design 2023-2027.docx`), exam specifications, formula sheets and the multiple-choice answer sheet.
- `02 Past Exams`: one folder per sitting (`2023`, `2024`, `2025`, `2024 NHT`, `2025 NHT`, `2026 NHT`, `VCAA Sample (current study design)`). Files are named like `2025 - Exam 1.pdf`, `2025 - Exam 1 Report.docx` and `2025 - Exam 2 Assessment Guide.docx`.
- `03 Teacher PD`: 2024 Chief Assessor PL commentary on Exam 2.
- `04 Analysis`: `GM Exam Question Analysis.xlsx`, the master tagging workbook. It has a tab per paper, a Master tab, Summary, Trends and Codes.
- `05 Textbook - Cambridge Skills Checklists` (to be added): Cambridge skills checklists, which map to textbook homework questions.

## Role of the Cambridge skills checklists
- **Their job is the resource map, not the ranking.** Map each checklist skill to one study design code. Then an exam question can point a student to the exact textbook section and homework questions to redo.
- **They're not a tag source.** Ranking and priority stay on the study design codes only.
- **Flag anything untraceable.** A checklist skill that doesn't trace back to the study design is flagged, not counted.
- **Chain for students:** exam question → study design code → checklist skill → textbook section and homework questions / video / AI tutor prompt → re-attempt the exam question.

## Difficulty measures (as built in the workbook)
- **Success rate.** Exam 1: % of students choosing the correct answer. Exam 2: average mark ÷ marks available (from the score distribution).
- **Marks lost.** marks × (1 − success rate).
- **Exam % lost per sitting.** Per code, averaged over the papers included. Exam 1 and Exam 2 count equally, since each is 30% of the study score. This drives the ranking: ranks 1–8 are Must master, 9–18 are Should master, the rest are Know it. Codes with no questions show as "Not yet examined (still examinable)".
- **Guessing caveat.** Exam 1 success rates include guessing (a 25% floor)."""),
("   - textbook section and worked examples (ask which textbook if unknown)","   - textbook section, worked examples and Cambridge checklist homework questions (Cambridge Senior Maths)")]
for a,b in R:
    assert a in s,a[:40]; s=s.replace(a,b)
open('/tmp/w/doc_new.md','w').write(s)
