import json,re,sys
def lines(W):
    L=[];W=sorted(W,key=lambda w:(w[0],round(w[2],3),w[1]))
    for w in W:
        if L and L[-1]['p']==w[0] and abs(L[-1]['y0']-w[2])<0.006: 
            l=L[-1]; l['ws'].append(w); l['x1']=max(l['x1'],w[3]); l['y1']=max(l['y1'],w[4])
        else: L.append(dict(p=w[0],y0=w[2],y1=w[4],x0=w[1],x1=w[3],ws=[w]))
    for l in L:
        l['ws'].sort(key=lambda w:w[1]); l['x0']=l['ws'][0][1]; l['t']=' '.join(w[5] for w in l['ws'])
    return L
def load(key):
    W=json.load(open(f'/tmp/w/ocrw/{key.replace(" ","_")}.json'))
    W=[w for w in W if 0.085<(w[1]+w[3])/2<0.915 or re.match(r'^([a-hA-H])\1?[.,]$|^([ivx]{1,4})[.,]$',w[5],re.I) or (w[5].startswith('Q') and w[1]>0.03)]
    return lines(W)
def headings(L):
    H=[]
    for i,l in enumerate(L):
        m=re.match(r'^\W{0,2}Q[uo]estion\s+(\d{1,2})\b(.*)',l['t'])
        if m and not re.search(r'contin',l['t'],re.I) and l['x0']<0.45:
            n=int(m.group(1))
            if not H or n>H[-1][0]: H.append((n,i))
    return H
if __name__=="__main__":
    for key in sys.argv[1:]:
        L=load(key); H=headings(L); ns=[h[0] for h in H]
        exp=40 if key.endswith('E1') else max(ns)
        miss=[n for n in range(1,exp+1) if n not in ns]
        print(key,len(H),'missing',miss)
