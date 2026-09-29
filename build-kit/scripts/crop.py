import json,re,sys,os,subprocess
from PIL import Image,ImageOps
from locate import load,headings
from words import PDF,B
DPI=125
EXCL=re.compile(r'contin|TURN OVER|END OF QUESTION|End of Question|Do not write|^SECTION|^Data analysis$|^Recursion and financial|^Matrices$|^Networks and decision|^Working space|^Question and Answer Book',re.I)
def render(key):
    d=f'/tmp/w/pages/{key.replace(" ","_")}'
    if not os.path.exists(d):
        os.makedirs(d); subprocess.run(['pdftoppm','-r',str(DPI),'-gray','-png',B+PDF[key],d+'/p'])
    return d
def page_img(d,p):
    fs=[f for f in os.listdir(d) if f.endswith('.png') and int(re.findall(r'\d+',f)[-1])==p]
    return Image.open(d+'/'+fs[0]).convert('L')
def trim(im,thr=235):
    g=ImageOps.invert(im.point(lambda v:255 if v>thr else v))
    bb=g.getbbox(); return (bb[1],bb[3]) if bb else None
BANDS={}
def bounds(d,p):
    k=(d,p)
    if k not in BANDS:
        im=page_img(d,p); W,H=im.size; px=im.load()
        ys=range(int(H*.2),int(H*.8),7)
        dark=[sum(1 for y in ys if px[x,y]<170)/len(ys) for x in range(W)]
        band=[x for x in range(W) if dark[x]>0.6]
        runs=[];s=None
        for x in range(W+1):
            if x<W and dark[x]>0.6:
                s=x if s is None else s
            elif s is not None: runs.append((s,x-1)); s=None
        L_=[r for r in runs if r[1]<W*0.1 and (r[1]-r[0]>=25 or r[1]<W*0.035)]
        R_=[r for r in runs if r[0]>W*0.9 and (r[1]-r[0]>=25 or r[0]>W*0.965)]
        lb=(max(r[1] for r in L_)+8) if L_ else int(.02*W); rb=(min(r[0] for r in R_)-8) if R_ else int(.98*W)
        BANDS[k]=(lb,rb)
    return BANDS[k]
def slice_page(d,p,y0,y1):
    im=page_img(d,p); W,H=im.size; lb,rb=bounds(d,p)
    c=im.crop((lb,int(y0*H),rb,int(y1*H)))
    px=c.load(); cw,ch=c.size
    def rowdark(y): return sum(1 for x in range(0,cw,3) if px[x,y]<170)/len(range(0,cw,3))
    # blank out near-full-width rule lines (page frames)
    for y in list(range(min(ch,45)))+list(range(max(0,ch-45),ch)):
        if rowdark(y)>0.88:
            for x in range(cw): px[x,y]=255
    bb=ImageOps.invert(c.point(lambda v:255 if v>235 else v)).getbbox()
    if not bb: return None,0
    top=max(0,bb[1]-6); c2=c.crop((0,top,c.size[0],min(c.size[1],bb[3]+6)))
    return c2, int(y0*H)+top
def stitch(slices,gap=14):
    slices=[s for s in slices if s[0] is not None]
    w=max(s[0].size[0] for s in slices); h=sum(s[0].size[1] for s in slices)+gap*(len(slices)-1)
    out=Image.new('L',(w,h),255); y=0; offs=[]
    for im,p,ptop in slices:
        out.paste(im,(0,y)); offs.append((p,ptop,y,im.size[1])); y+=im.size[1]+gap
    return out,offs
def regions(key):
    L=load(key); H=headings(L); d=render(key)
    npages=max(l['p'] for l in L)
    HDR=re.compile(r'Page \\d|of \\d\\d|VCE|Examination|GENERAL|NHT|^\\d+$',re.I)
    top={p:max([l['y1'] for l in L if l['p']==p and ((l['y0']<0.045) or (l['y0']<0.065 and HDR.search(l['t'])) or (l['y0']<0.16 and EXCL.search(l['t'])))]+[0.04]) for p in range(1,npages+1)}
    RAW=json.load(open(f'/tmp/w/ocrw/{key.replace(" ","_")}.json'))
    bot={p:min([w[2]-0.003 for w in RAW if w[0]==p and w[2]>0.8 and re.search(r'TURN|OVER|continue',w[5],re.I)]+[0.95]) for p in range(1,npages+1)}
    Q={}
    for k,(n,i) in enumerate(H):
        endi=H[k+1][1] if k+1<len(H) else len(L)
        start=L[i]; segs=[]; p=start['p']; y=start['y0']-0.004
        cur_end=None
        j=i+1
        # walk lines until next heading, splitting by page, stopping at excluded lines (section headings / END)
        pages={}
        pages[p]=[y,None]
        stop=False
        for j in range(i+1,endi):
            l=L[j]
            if re.search(r'This page is blank|Formula Sheet|Curriculum and Assessment Authority|END OF MULTIPLE|END OF QUESTION|(following information|information below|relates? to).{0,40}Questions? +[0-9]',l['t'],re.I):
                if l['p'] in pages and pages[l['p']][1] is None: pages[l['p']][1]=l['y0']-0.003
                stop=True; break
            if l['y0']<top[l['p']]-0.001: continue
            if EXCL.search(l['t']):
                if re.search(r'END OF QUESTION|End of Question|^Data analysis$|^Recursion and financial|^Matrices$|^Networks and decision|^SECTION',l['t'],re.I) and l['p'] in pages and pages[l['p']][1] is None:
                    pages[l['p']][1]=l['y0']-0.003
                    if re.search(r'END OF QUESTION|End of Question',l['t'],re.I): stop=True; break
                continue
            if l['p'] not in pages: pages[l['p']]=[top[l['p']]+0.002,None]
        if not stop and k+1<len(H):
            nl=L[H[k+1][1]]
            if nl['p'] in pages and pages[nl['p']][1] is None: pages[nl['p']][1]=nl['y0']-0.004
        # stimulus line just before next heading belongs to next question
        if k+1<len(H):
            nxt=H[k+1][1]
            for j in range(nxt-1,max(i,nxt-4),-1):
                if re.search(r'following information|information below|relates? to Questions',L[j]['t'],re.I) and L[j]['p'] in pages:
                    pages[L[j]['p']][1]=min(pages[L[j]['p']][1] or 1,L[j]['y0']-0.004)
        for pp in pages:
            if pages[pp][1] is None: pages[pp][1]=bot[pp]
        Q[n]=dict(pages=[(pp,a,b) for pp,(a,b) in sorted(pages.items()) if b>a+0.005],hi=i,endi=endi)
    # stimulus blocks
    S={}
    for j,l in enumerate(L):
        m=re.search(r'(?:following information|information below|relates? to)\D*Questions?\s+(\d+)(?:\s*(?:,|and|to|–|-)\s*(\d+))?(?:\s*(?:,|and|to|–|-)\s*(\d+))?',l['t'],re.I)
        if m:
            nums=[int(x) for x in m.groups() if x]; rng=list(range(nums[0],max(nums)+1)) if re.search(r'\bto\b|–|-',l['t']) else nums
            nh=next((h for h in H if h[1]>j),None)
            if nh and nh[0] in rng and L[nh[1]]['p']==l['p']:
                for q in rng: S[q]=(l['p'],l['y0']-0.004,L[nh[1]]['y0']-0.004)
    return L,H,Q,S,d
LAB=re.compile(r'^([a-hA-H])\1?[.,]$|^([ivx]{1,4})[.,]$',re.I)
def labels(L,q,offs,d):
    out=[]
    for j in range(q['hi'],q['endi']):
        l=L[j]
        for w in l['ws']:
            if LAB.match(w[5]) and w[1]<0.25:
                for (p,ptop,sy,h) in offs:
                    if p==l['p']:
                        im=page_img(d,p); Hh=im.size[1]
                        yy=int(w[2]*Hh)-ptop
                        if -5<=yy<=h:
                            t=w[5][:-1].lower(); t=t[0] if len(t)==2 and t[0]==t[1] and t[0] not in 'iv' else t
                            out.append((t,sy+max(0,yy-8)))
    # dedupe/order
    out=sorted(set(out),key=lambda x:x[1]); return out
def build(key,outdir='/tmp/w/qimg'):
    os.makedirs(outdir,exist_ok=True)
    L,H,Q,S,d=regions(key); meta={}
    tag=key.replace(' ','_')
    for n,q in Q.items():
        sl=[]
        if n in S and key.endswith('E1'):
            p,a,b=S[n]; im,pt=slice_page(d,p,a,b); 
            if im: sl.append((im,p,pt))
        for p,a,b in q['pages']:
            im,pt=slice_page(d,p,a,b); sl.append((im,p,pt))
        img,offs=stitch(sl)
        fn=f'{tag}_Q{n}.png'
        img.convert('P',palette=Image.ADAPTIVE,colors=16).save(f'{outdir}/{fn}',optimize=True)
        meta[n]=dict(f=fn,w=img.size[0],h=img.size[1],labels=labels(L,q,offs,d) if key.endswith('E2') else [])
    json.dump(meta,open(f'{outdir}/{tag}.json','w'))
    return meta
if __name__=="__main__":
    for key in sys.argv[1:]:
        m=build(key); import os
        sz=sum(os.path.getsize('/tmp/w/qimg/'+v['f']) for v in m.values())
        print(key,len(m),f'{sz//1024}KB')
