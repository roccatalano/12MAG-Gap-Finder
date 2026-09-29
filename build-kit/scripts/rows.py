import sys,re,json; sys.path.insert(0,'/tmp/w'); from tags import T
from docx import Document
R=json.load(open('/tmp/w/reports.json'))
B="/mnt/user-data/outputs/org/02 Past Exams/"
norm=lambda q:re.sub(r'[^0-9a-z]','',q.lower())
META={"2023":("2023",2023,"VCAA Main"),"2024":("2024",2024,"VCAA Main"),"2025":("2025",2025,"VCAA Main"),
"2024N":("2024 NHT",2024,"VCAA NHT"),"2025N":("2025 NHT",2025,"VCAA NHT"),"2026N":("2026 NHT",2026,"VCAA NHT"),"S":("Sample",2022,"VCAA Sample")}
def nht_answers(folder):
    d=Document(B+f"{folder}/{folder} - Exam 1 Report.docx"); a={}
    for t in d.tables:
        for r in t.rows:
            c=[x.text.strip() for x in r.cells]
            if c[0].isdigit(): a[c[0]]=c[1]
    return a
PAPERS=[]
for key,txt in T.items():
    k,ex=key.split(); folder,year,src=META[k]; exam="Exam "+ex[1]
    pid=f"{folder} {'VCAA ' if k in('2023','2024','2025') else ''}E{ex[1]}".replace("Sample E","VCAA Sample E")
    rep=R.get(f"{folder} - Exam {ex[1]}",[])
    rows=[]
    for line in txt.strip().split('\n'):
        f,note=line.split('|',1); f=f.split(); note=note.strip()
        if ex=="E1":
            q,code,sec,task=f; marks=1; ans=None; succ=None; spread=""
            row=next((r for r in rep if r[0]==q),None)
            if row:
                ans=row[1]; nopt=5 if k=="2023" else 4
                pct=dict(zip("ABCDE"[:nopt],map(float,row[2:2+nopt])))
                succ=pct[ans]/100; wrong=max((o for o in pct if o!=ans),key=pct.get)
                spread=f"Most common wrong answer: {wrong} ({pct[wrong]:.0f}%)"
            elif k in("2024N","2025N","2026N"):
                ans=nht_answers(folder).get(q); spread="No statistics published for NHT"
            else: spread="No statistics (sample paper)"
        else:
            q,m,code,sec,task=f; marks=int(m); ans=None; succ=None; spread=""
            row=next((r for r in rep if norm(r['q'])==norm(q) and r.get('stats')),None)
            if row and row.get('stats'):
                vals=[float(v) for v in row['stats'][1][1:-1]]
                if len(vals)==marks+1:
                    succ=round(sum(i*v for i,v in enumerate(vals))/100/marks,3)
                    spread=" | ".join(f"{i} marks: {v:.0f}%" for i,v in enumerate(vals))
                else: spread="marks mismatch"
            elif k in("2024N","2025N","2026N"): spread="No statistics published for NHT"
            elif k=="S": spread="No statistics (sample paper)"
            if "invalidated" in note: succ=None; spread="Invalidated by VCAA – excluded from difficulty"
        rows.append([pid,year,src,exam,q,marks,code,None,None,None if sec=='-' else sec,task,ans,succ,None,spread,note])
    PAPERS.append((pid,rows))
if __name__=="__main__":
    for pid,rows in PAPERS:
        miss=[r[4] for r in rows if r[12] is None]
        print(pid,len(rows),sum(r[5] for r in rows),'no-success:',len(miss), miss[:8] if 'NHT' not in pid and 'Sample' not in pid else '')
        bad=[r[4] for r in rows if 'mismatch' in r[14]]
        if bad: print('  MISMATCH',bad)
