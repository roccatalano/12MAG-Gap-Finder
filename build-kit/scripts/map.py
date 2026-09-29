import json,re
c=json.load(open('/tmp/w/checklist.json')); ex0=json.load(open('/tmp/w/ex.json'))
ex={}
for k,gs in ex0.items():
    m=[]
    for g in gs:
        h=g['heading']; noisy=(not g['examples']) and m and not h.startswith('Exam') and (len(h)>45 or h.split(' ')[0] in('If','The','After','Each','Five','Use','Find','Note:','Write','What','How','Determine','Calculate'))
        if noisy: m[-1]['qs']+=g['qs']
        else: m.append(dict(g,qs=list(g['qs'])))
    ex[k]=m
T={"1A":"Types of data","1B":"Displaying and describing the distributions of categorical variables","1C":"Displaying and describing numerical data","1D":"Dot plots and stem plots","1E":"Using a logarithmic (base 10) scale to display data","1F":"Measures of centre and spread","1G":"The five-number summary and the boxplot","1H":"The normal distribution and the 68–95–99.7% rule","2A":"Bivariate data – classifying the variables","2B":"Investigating associations between categorical variables","2C":"Investigating the association between a numerical and a categorical variable","2D":"Investigating associations between two numerical variables","2E":"How to interpret a scatterplot","2F":"Strength of a linear relationship: the correlation coefficient","2G":"The coefficient of determination","2H":"Correlation and causality","2I":"Which graph?","3A":"Fitting a least squares regression line to numerical data","3B":"Using the least squares regression line to model a relationship between two numerical variables","3C":"Conducting a regression analysis using data","4A":"The squared transformation","4B":"The log transformation","4C":"The reciprocal transformation","4D":"Choosing and applying the appropriate transformation","5A":"Time series data","5B":"Smoothing a time series using moving means","5C":"Smoothing a time series plot using moving medians","5D":"Seasonal indices","5E":"Fitting a trend line and forecasting","7A":"Sequences and recurrence relations","7B":"Modelling linear growth and decay","7C":"Using an explicit rule for linear growth or decay","7D":"Modelling geometric growth and decay","7E":"Using an explicit rule for geometric growth or decay","7F":"Interest rates over different time periods and effective interest rates","8A":"Compound interest investments with additions to the principal","8B":"Recurrence relations for reducing balance loans and annuities","8C":"Amortisation tables","8D":"Analysing financial situations using amortisation tables","8E":"Using a finance solver to find the balance and final payment","8F":"Using a finance solver to find interest rates, time taken and regular payments","8G":"Solving harder financial problems","8H":"Interest-only loans","8I":"Perpetuities","10A":"What is a matrix?","10B":"Using matrices to represent information","10C":"Matrix arithmetic: addition, subtraction and scalar multiplication","10D":"Matrix arithmetic: the product of two matrices","10E":"Matrix inverse, the determinant and matrix equations","10F":"Binary, permutation and communication matrices","10G":"Dominance matrices","11A":"Setting up a transition matrix","11B":"Interpreting transition matrices","11C":"Transition matrices – using recursion","11D":"Transition matrices – using the rule Sn+1 = TSn + B","11E":"Leslie matrices","13A":"Graphs and networks","13B":"Adjacency matrices","13C":"Exploring and travelling","13D":"Weighted graphs and networks","13E":"Dijkstra's algorithm","13F":"Trees and minimum connector problems","14A":"Flow problems","14B":"Matching problems","14C":"Precedence tables and activity networks","14D":"Scheduling problems","14E":"Crashing"}
SEC={"1A":"DA1","1B":"DA2","1C":"DA2","1D":"DA2","1E":"DA2","1F":"DA3","1G":"DA3","1H":"DA4","2A":"DA5","2B":"DA5","2C":"DA5","2D":"DA5","2E":"DA6","2F":"DA6","2G":"DA7","2H":"DA6","2I":"DA5","3A":"DA7","3B":"DA7","3C":"DA7","4A":"DA8","4B":"DA8","4C":"DA8","4D":"DA8","5A":"DA9","5B":"DA9","5C":"DA9","5D":"DA10","5E":"DA11","7A":"RF1","7B":"RF2","7C":"RF2","7D":"RF3","7E":"RF3","7F":"RF4","8A":"RF7","8B":"RF5","8C":"RF5","8D":"RF5","8E":"RF8","8F":"RF8","8G":"RF8","8H":"RF9","8I":"RF6","10A":"MA1","10B":"MA1","10C":"MA1","10D":"MA1","10E":"MA2","10F":"MA1","10G":"MA3","11A":"MA4","11B":"MA4","11C":"MA5","11D":"MA6","11E":"MA7","13A":"ND1","13B":"ND1","13C":"ND3","13D":"ND6","13E":"ND6","13F":"ND4","14A":"ND5","14B":"ND7","14C":"ND8","14D":"ND8","14E":"ND8"}
def code(sec,s):
    s=s.lower()
    if sec=="1F" and ("mean" in s or "standard deviation" in s): return "DA4"
    if sec=="1H" and "mean and standard deviation" in s: return "DA4"
    if sec in("3A",) and "correlation coefficient" in s: return "DA6"
    if sec=="3B" and "coefficient of determination" in s: return "DA7"
    if sec=="3B" and "residual" in s: return "DA8"
    if sec=="7B" and "graph the terms" in s: return "RF1"
    if sec=="7C" and "convert a recurrence" in s: return "RF1"
    if sec=="7D" and "graph the terms" in s: return "RF1"
    if sec=="8A" and ("generate a sequence" in s or "annual interest rate from" in s): return "RF1"
    if sec in("8B","8C","8D","8E","8F","8G") and "annuity" in s and "loan" not in s: return "RF6"
    if sec in("8E","8F") and ("investment" in s): return "RF7"
    if sec=="8C" and "investment" in s: return "RF7"
    if sec=="10B" and "network" in s: return "ND1"
    if sec=="10E" and "recognise that two matrices are inverses" in s: return "MA2"
    if sec=="10F" and "communication" in s: return "MA3"
    if sec=="13A" and ("planar" in s or "euler" in s): return "ND2"
    return SEC[sec]
out=[];seen=set()
for o in c:
    k=(o['section'],o['n'])
    if k in seen: continue
    seen.add(k)
    sk=o['skill']
    m=re.search(r'\s*See (.*?)[,.]?\s*(?:and )?Exercise (\d+[A-Z]) Question (\d+)',sk)
    if m: o['see']=o.get('see') or m.group(1); o['ex']=m.group(2); o['exq']=int(m.group(3)); sk=sk[:m.start()]
    sk=re.sub(r'\s*See .*$','',sk).strip().rstrip('.')+'.'
    sec=o['section']; ch=re.match(r'\d+',sec).group()
    exnums=re.findall(r'\d+',o.get('see') or '') if 'Example' in (o.get('see') or '') else []
    grp=None; gsec=o.get('ex',sec)
    if o.get('ex') in ex and o.get('ex')==sec and not (ch=='13' and sec in('13D','13E') and o['n']>=16):
        for g in ex[o['ex']]:
            if o['exq'] in g['qs']: grp=g
    if ch=='13' and o['n']>=16: exnums=exnums
    else: exnums=[] if grp else exnums
    for n in exnums:
        for s2,gs in ex.items():
            if re.match(r'\d+',s2).group()!=ch: continue
            for g in gs:
                if n in re.findall(r'\d+',g['examples']): grp=g; gsec=s2; break
            if grp: break
        if grp: break
    if not grp and o.get('ex') in ex:
        for g in ex[o['ex']]:
            if o['exq'] in g['qs']: grp=g; gsec=o['ex']
    qs=grp['qs'] if grp else ([o['exq']] if o.get('exq') else [])
    exam=[q for g in ex.get(gsec,[]) if g['heading'].startswith('Exam 1 style') for q in g['qs']]
    fmt=lambda q:(f"Q{q[0]}" if len(q)==1 else (f"Q{q[0]}–{q[-1]}" if q==list(range(q[0],q[-1]+1)) else "Q"+", ".join(map(str,q))))
    out.append(dict(code=code(gsec if gsec in SEC else sec,sk),chapter=int(ch),section=gsec,section_title=T.get(gsec,''),n=o['n'],skill=sk,
        example=(o.get('see') or '').replace(' and ',', '),homework=f"Ex {gsec} "+fmt(qs) if qs else '',exam_style=(f"Ex {gsec} "+fmt(exam)) if exam else '',
        checklist_section=sec))
json.dump(out,open('/tmp/w/skills.json','w'),indent=0)
import collections;print(len(out),collections.Counter(o['code'] for o in out))
for o in out:
    if o['section']!=o['checklist_section'] or not o['homework']: print('!',o['checklist_section'],o['section'],o['n'],o['skill'][:60],o['homework'])
for o in out:
    if o['chapter']==13 and o['n']==16:
        o.update(section='13E',section_title=T['13E'],homework='Ex 13E Q1–2',example='Example 10',exam_style='')
json.dump(out,open('/tmp/w/skills.json','w'),indent=0)
