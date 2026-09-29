import json,re,sys
sys.path.insert(0,'/tmp/w')
from rows import PAPERS
def parse(q):
    m=re.match(r'^(\d+)\.?([a-h])?\.?((?:i|ii|iii|iv|v))?\.?$',q.replace(' ',''))
    return int(m.group(1)),m.group(2),m.group(3)
def part_range(meta,q):
    n,let,rom=parse(q); m=meta.get(str(n))
    if not m: return None
    labs=m['labels']; H=m['h']
    if not let: return (0,H) if not rom else None
    # sequence of (letter,roman,y)
    seq=[];cur=None
    for t,y in labs:
        if re.fullmatch(r'[a-h]',t) and t not in ('i','v'): cur=t; seq.append((t,None,y))
        elif re.fullmatch(r'i|ii|iii|iv|v',t): seq.append((cur,t,y))
        elif t in ('i','v'): seq.append((cur,t,y))
    # start
    idx=None
    for k,(L,R,y) in enumerate(seq):
        if L==let and R is None and (rom is None or rom=='i'): idx=k; break
    if rom and rom!='i':
        idx=next((k for k,(L,R,y) in enumerate(seq) if L==let and R==rom),None)
    if idx is None: return None
    y0=seq[idx][2]
    end=H
    for k in range(idx+1,len(seq)):
        L,R,y=seq[k]
        if seq[idx][1] is None and L==let and R=='i': continue
        if y>y0+5: end=y-2; break
    return (y0,end)
if __name__=="__main__":
    tot=miss=0
    for pid,rows in PAPERS:
        if not pid.endswith('E2'): continue
        meta=json.load(open(f'/tmp/w/qimg/{pid.replace(" ","_")}.json'))
        bad=[]
        for r in rows:
            tot+=1; pr=part_range(meta,r[4])
            if pr is None: bad.append(r[4]); miss+=1
        print(pid,'missing:',bad)
    print(tot,miss)
