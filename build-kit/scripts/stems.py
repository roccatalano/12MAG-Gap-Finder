import re,sys,subprocess
B="/mnt/user-data/outputs/org/02 Past Exams/"
P={"2023 E1":B+"2023/2023 - Exam 1.pdf","2024 E1":"/tmp/ocr/2024_-_Exam_1.txt","2024N E1":B+"2024 NHT/2024 NHT - Exam 1.pdf","2025N E1":"/tmp/ocr/2025_NHT_-_Exam_1.txt","2026N E1":B+"2026 NHT/2026 NHT - Exam 1.pdf","S E1":B+"VCAA Sample (current study design)/Sample - Exam 1.pdf"}
def get(p):
    return open(p).read() if p.endswith('.txt') else subprocess.run(['pdftotext',p,'-'],capture_output=True,text=True).stdout
k=sys.argv[1]; t=get(P[k])
t=re.sub(r'(?m)^.*(Do not write|Page \d|TURN OVER|SECTION|Instructions|©).*$','',t)
parts=re.split(r'\n\s*Question (\d{1,2})\s*\n',t)
for i in range(1,len(parts),2):
    s=re.sub(r'\s+',' ',parts[i+1])
    s=re.split(r'\sA[\.\s]',s)[0]
    print(parts[i],':',s[-260:])
