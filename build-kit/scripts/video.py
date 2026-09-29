import re
RAW=open('/root/.claude/uploads/75cea519-58c7-5f86-be21-e9ad4607fab7/d532ec4b-attachment.txt').read()
VID={"2025 VCAA E1":"xDkHrPH4ysQ","2025 VCAA E2":"uPKcmglOdpg","2025 NHT E1":"nWsXfniMFJM","2025 NHT E2":"-TQWDTpBi5Y",
"2024 VCAA E1":"NmVEQH9c6tw","2024 VCAA E2":"MJD-lyztjDY","2024 NHT E1":"jJZFIfajOHs","2024 NHT E2":"ygP9Z0Dnv5Q",
"2023 VCAA E1":"5zgWrmTvIzA","2023 VCAA E2":"y2uGBKEM1cg"}
HEADS={"2025 VCAA E1":"2025 VCE General Maths Paper 1","2025 NHT E1":"2025 VCE (NHT) General Maths Paper 1","2025 NHT E2":"2025 VCE (NHT) General Maths Paper 2","2024 VCAA E2":"2024 General Maths VCE Paper 2","2023 VCAA E1":"VCAA 2023 VCE General Maths Paper 1","2023 VCAA E2":"2023 VCAA VCE General Maths Paper 2"}
EXTRA_2025E2="""01:09 Question 1a|03:54 Question 1b|04:18 Question 1ci|06:18 Question 1cii|06:48 Question 1d|07:42 Question 2a|08:24 Question 2b|09:25 Question 3|13:26 Question 4a|14:01 Question 4b|15:16 Question 4c|16:23 Question 4d|17:50 Question 4e|18:55 Question 4fi|20:49 Question 4fii|21:28 Question 5a|23:53 Question 5b|24:56 Question 6a|25:54 Question 6b|30:17 Question 7a|31:26 Question 7b|31:54 Question 7c|34:21 Question 7d|35:59 Question 8ai|36:40 Question 8aii|37:05 Question 8b|37:42 Question 9a|39:04 Question 9bi|40:24 Question 9bii|41:26 Question 10|44:38 Question 11a|45:46 Question 11b|46:18 Question 11c|47:12 Question 12a|49:41 Question 12b|53:02 Question 13a|53:45 Question 13bi|55:32 Question 13bii|57:55 Question 14a|59:05 Question 14b|1:01:53 Question 15a|1:02:38 Question 15b|1:03:06 Question 15c|1:03:28 Question 15d|1:03:49 Question 16|1:05:13 Question 17a|1:06:55 Question 17b|1:08:36 Question 18a|1:12:20 Question 18b|1:12:33 Question 18c|1:13:00 Question 18d"""
def secs(t):
    p=[int(x) for x in t.split(':')]; s=0
    for x in p: s=s*60+x
    return s
norm=lambda q:re.sub(r'[^0-9a-z]','',q.lower())
def block(head):
    i=RAW.index(head); j=RAW.find('This maths video',i); return RAW[i:j]
TS={}
for pid,head in HEADS.items():
    d={}
    for t,q in re.findall(r'(\d[\d:]*)\s+(?:[A-Za-z ]+: )?Quest?ion (\w+)',block(head)):
        d.setdefault(norm(q),secs(t))
    TS[pid]=d
TS["2025 VCAA E2"]={norm(q):secs(t) for t,q in (x.split(' Question ') for x in EXTRA_2025E2.split('|'))}
# corrections
TS["2025 NHT E1"]["3"]=secs("04:24"); TS["2025 NHT E1"]["2"]=secs("03:18")
n=TS["2025 NHT E2"]; n["16ei"]=n.pop("14ei"); n["16eii"]=n.pop("14eii")
TS["2024 VCAA E2"]["8"]=TS["2024 VCAA E2"].pop("8a")
def link(pid,q):
    v=VID.get(pid)
    if not v: return None,None
    d=TS.get(pid,{}); k=norm(q)
    if k in d: s=d[k]; lab="exact"
    else:
        num=re.match(r'\d+',k).group()
        c=[s for kk,s in d.items() if re.match(r'\d+',kk).group()==num]
        if c: s=min(c); lab="question start"
        else: return f"https://www.youtube.com/watch?v={v}","whole video"
    return f"https://www.youtube.com/watch?v={v}&t={s}s", f"{s//3600}:{s%3600//60:02d}:{s%60:02d}" if s>=3600 else f"{s//60}:{s%60:02d}"
if __name__=="__main__":
    import sys; sys.path.insert(0,'/tmp/w'); from rows import PAPERS
    for pid,rows in PAPERS:
        res=[link(pid,r[4]) for r in rows]
        print(pid, sum(1 for u,l in res if u and 't=' in u), sum(1 for u,l in res if u and 't=' not in u), [r[4] for r,(u,l) in zip(rows,res) if u and pid in HEADS and norm(r[4]) not in TS[pid]][:12])
