import re,json
t=open('/tmp/tb.txt').read()
lines=t.split('\n')
starts=[i for i,l in enumerate(lines) if l.strip()=='Skills checklist']
out=[]
for s in starts:
    end=next(i for i in range(s,len(lines)) if 'Multiple-choice questions' in lines[i])
    blk=lines[s:end]
    cur=None
    for l in blk:
        m=re.match(r'^\s*(?:Review\s+\d+.*)?\s*(\d+[A-Z])\s+(\d+)\s+(I can .*)$',l)
        if m:
            cur=dict(section=m.group(1),n=int(m.group(2)),skill=m.group(3).strip()); out.append(cur); continue
        m=re.search(r'See (.*?), and Exercise (\d+[A-Z]) Question (\d+)',l)
        if m and cur: cur['see']=m.group(1); cur['ex']=m.group(2); cur['exq']=int(m.group(3)); continue
        if cur and 'see' not in cur and l.strip() and not l.strip().startswith(('ISBN','Photocop','Review','Chapter')) and len(l)-len(l.lstrip())>20:
            cur['skill']+=' '+l.strip()
json.dump(out,open('/tmp/w/checklist.json','w'),indent=0)
print(len(out)); import collections
print(collections.Counter(o['section'][:-1] for o in out))
print([o for o in out if 'see' not in o][:5])
