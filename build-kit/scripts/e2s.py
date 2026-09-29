import re,sys,subprocess
B="/mnt/user-data/outputs/org/02 Past Exams/"
P={"2023":B+"2023/2023 - Exam 2.pdf","2024":"/tmp/ocr/2024_-_Exam_2.txt","2024N":B+"2024 NHT/2024 NHT - Exam 2.pdf","2025N":"/tmp/ocr/2025_NHT_-_Exam_2.txt","2026N":B+"2026 NHT/2026 NHT - Exam 2.pdf","S":B+"VCAA Sample (current study design)/Sample - Exam 2.pdf"}
p=P[sys.argv[1]]
t=open(p).read() if p.endswith('.txt') else subprocess.run(['pdftotext',p,'-'],capture_output=True,text=True).stdout
t=re.sub(r'(?m)^.*(Do not write|Page \d|TURN OVER|©|Formula Sheet).*$','',t)
t=re.sub(r'\n\s*\n+','\n',t)
L=[l.strip() for l in t.split('\n')]
keep=[]
for i,l in enumerate(L):
    if re.match(r'^(Question \d+|Data analysis|Recursion|Matrices|Networks|[a-e]\.|[ivx]+\.)',l) or re.search(r'\d marks?$',l) or re.search(r'[?]$|(Find|Calculate|Determine|Show|Write|State|Explain|Describe|Identify|Complete|Using|Use|What|How|Draw|Plot|Name|List|Round|Give)\b',l[:12]):
        keep.append(l[:170])
print('\n'.join(keep))
