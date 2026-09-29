import re,json
lines=open('/tmp/tb.txt').read().split('\n')
ans=next(i for i,l in enumerate(lines) if re.fullmatch(r'\s*Exercise 1A\s*',l) and i>40000)
heads=[]
for i,l in enumerate(lines[:ans]):
    m=re.fullmatch(r'(?:\S+\s+)?\s*Exercise (\d+[A-Z])\s*',l)
    if m and m.group(1) not in [h[1] for h in heads]: heads.append((i,m.group(1)))
res={};lastheading=""
for k,(i,sec) in enumerate(heads):
    end=heads[k+1][0] if k+1<len(heads) else ans
    for j in range(i,end):
        if lines[j].strip() in ('Skills checklist','Chapter summary') : end=j;break
    groups=[];cur=None;expect=1
    for l in lines[i+1:end]:
        m=re.match(r'^\s*Example[s]?\s+([\d, and]+?)\s{2,}(\d{1,2})\s{2,}\S',l)
        if m and int(m.group(2))==expect:
            cur={'examples':m.group(1).strip(),'qs':[expect],'heading':lastheading}; groups.append(cur); expect+=1; continue
        m=re.match(r'^\s{5,40}(\d{1,2})\s{2,}\S',l)
        if m and int(m.group(1))==expect:
            if cur is None: cur={'examples':'','qs':[],'heading':lastheading}; groups.append(cur)
            cur['qs'].append(expect); expect+=1; continue
        s=l.strip()
        if re.match(r'^\s{10,20}[A-Z][a-z]',l) and not re.search(r'\d{2,}|Chapter|ISBN|Photocop',s) and len(s)<90 and s[-1] not in '.?:,':
            lastheading=s; cur=None
            continue
    if k==0: pass
    res[sec]=groups
    lastheading=''
json.dump(res,open('/tmp/w/ex.json','w'))
for s in ['1B','1F','8H','11E','14D']: print(s,res.get(s))
