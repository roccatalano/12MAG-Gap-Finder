t=open('/tmp/w/app/template.html').read()
def rep(old,new,cnt=1):
    global t
    assert old in t, old[:80]
    t=t.replace(old,new,cnt)
# ---------- shared helpers ----------
rep("function likelihood(code){",'''function freqInfo(code){const n=sittingsWith(code);const l=n>=6?"Every exam":n>=4?"Most exams":n>=2?"Sometimes":"Rarely";const c=n>=6?"f4":n>=4?"f3":n>=2?"f2":"f1";return {n,l,c}}
function succInfo(s){if(s==null)return {l:"No data",c:"sN"};return s>=.7?{l:"Most get it right",c:"s3"}:s>=.4?{l:"Mixed",c:"s2"}:{l:"Most get it wrong",c:"s1"}}
function chip(i){return `<span class="chip ${i.c}">${esc(i.l)}</span>`}
function likelihood(code){''')
old=t[t.index("function likelihood(code){"):t.index("function vidLinks(code,q)")]
rep(old,'''function likelihood(code){const T=D.topics[code].sum;const f=freqInfo(code);const s=succInfo(T.succ);
  return `<div class="fact"><span class="eyebrow">How often it's examined</span>${chip(f)}
  <div class="stack"><span>Came up in <b>${f.n} of ${SITTINGS}</b> sittings</span><span>About <b>${T.per}</b> question${T.per==1?"":"s"} per sitting</span><span><b>${(T.share*100).toFixed(1)}%</b> of exam marks</span></div>
  <span class="eyebrow" style="margin-top:8px">How students go on this topic</span>${chip(s)}<div class="stack"><span>Average score <b>${pct(T.succ)}</b> across ${T.q} past questions</span></div></div>`}
''')
# ---------- one-question: hide answer, difficulty fallback ----------
rep('${q.a?` · answer ${esc(q.a)}`:""}</div>','</div>')
rep('<span class="eyebrow">Difficulty</span><span class="v" style="color:${d.c}">${d.t}${q.s!=null?` · avg ${pct(q.s)}`:""}</span><div class="bar"><i style="width:${Math.round(d.w*100)}%;background:${d.c}"></i></div>${q.s!=null?`<div class="stack">${q.sp.split(" | ").map(x=>`<span>${esc(x.replace("1 marks","1 mark"))} of students</span>`).join("")}</div>`:`<span class="s">NHT and sample papers have no published statistics</span>`}</div>`;',
 '<span class="eyebrow">How students went on this question</span>${q.s!=null?`${chip(succInfo(q.s))}<span class="v">Average ${pct(q.s)}</span><div class="bar"><i style="width:${Math.round(q.s*100)}%;background:${d.c}"></i></div><div class="stack">${q.sp.split(" | ").map(x=>`<span>${esc(x.replace("1 marks","1 mark"))} of students</span>`).join("")}</div>`:`${chip({l:"No data",c:"sN"})}<span class="s">NHT and sample papers have no published statistics. The topic average is ${pct(T.sum.succ)}.</span>`}</div>`;')
rep('else head+=`<div class="fact"><span class="eyebrow">Topic difficulty</span><span class="v" style="color:${diff(T.sum.succ).c}">${diff(T.sum.succ).t} · avg ${pct(T.sum.succ)}</span><div class="bar"><i style="width:${Math.round(T.sum.succ*100)}%;background:${diff(T.sum.succ).c}"></i></div><span class="s">Average score across ${T.sum.q} past questions</span></div>`;','')
rep('''if(q&&q.cm)head+=`<details><summary>Examiners' comment on this question</summary><div class="note" style="margin-top:8px">${esc(q.cm)}</div></details>`;''',
 '''if(q&&(q.cm||q.a))head+=`<details><summary>Show the answer${q.cm?" and examiners' comment":""}</summary><div class="note" style="margin-top:8px">${q.a?`<b>Answer: ${esc(q.a)}</b>${q.cm?"<br>":""}`:""}${esc(q.cm||"")}</div></details>`;''')
# ---------- option count ----------
rep('"ABCDE".slice(0,q.p.startsWith("2023")||q.p.includes("NHT")||q.p.includes("Sample")?5:4)','"ABCDE".slice(0,q.no||4)')
# ---------- guide ----------
rep('''function scored(q,v,e1){if(v===undefined)return null;''','''function scored(q,v,e1){if(v===undefined)return 0;''')
rep('''  qs.forEach(q=>{const s=scored(q,r[q.q],e1);if(s===null){miss++;return}tot+=q.m;got+=s;''','''  qs.forEach(q=>{if(r[q.q]===undefined)miss++;const s=scored(q,r[q.q],e1);tot+=q.m;got+=s;''')
rep('''  if(!tot){$("guide").innerHTML=quiet?"":`<p class="hint">Enter at least some results first.</p>`;return}''','''  if(miss===qs.length){$("guide").innerHTML=quiet?"":`<p class="hint">Enter your results first.</p>`;return}''')
rep('''  const order=Object.keys(lost).map(c=>({c,...lost[c],score:lost[c].marks*(1+D.topics[c].sum.lost*25)})).sort((a,b)=>b.score-a.score);''',
'''  const LBL={qw:{l:"Quick win",c:"qw",why:"Comes up a lot and most students get these marks. Fix these first."},we:{l:"Worth the effort",c:"we",why:"Comes up a lot but is hard for most students. Big payoff, more work."},lp:{l:"Lower priority",c:"lp",why:"Rarely examined. Do these after the others."}};
  const order=Object.keys(lost).map(c=>{const o=lost[c];const f=freqInfo(c);const withS=o.qs.filter(q=>q.s!=null);
    const qs_=withS.length?withS.reduce((a,q)=>a+q.s*q.m,0)/withS.reduce((a,q)=>a+q.m,0):D.topics[c].sum.succ;
    const k=f.n>=4?(qs_>=.5?"qw":"we"):"lp";return {c,...o,f,qs_,k,score:o.marks*(0.25+f.n/7)*(0.25+qs_)}})
    .sort((a,b)=>({qw:0,we:1,lp:2}[a.k]-{qw:0,we:1,lp:2}[b.k])||b.score-a.score);''')
rep('''${Math.round(got/tot*100)}% on the questions entered${miss?` (${miss} not entered yet)`:""}''','''${Math.round(got/tot*100)}%${miss?` · ${miss} question${miss>1?"s":""} left blank, counted as wrong`:""}''')
rep('''<p>Topics where you lost marks, highest priority first. Priority combines the marks you lost with how often the topic is examined.</p>''','''<p>Topics where you lost marks, in the order to study them. <b>Quick wins</b> first: topics that come up a lot where most students get the marks. Then <b>Worth the effort</b>: common but hard. Then <b>Lower priority</b>: rarely examined.</p>''')
old=t[t.index('    const secs={};T.skills.forEach'):t.index('    tb.push(`<li>Exam-style revision')]
rep(old,'''    const idx=[...new Set(o.qs.flatMap(q=>q.sk||[]))];const use=idx.length?idx.map(i=>T.skills[i]):T.skills;
    const secs={};use.forEach(k=>{const s=secs[k.sec]=secs[k.sec]||{title:k.title,qs:[],ex:[]};const m=(k.hw||"").replace(/^Ex \\S+ /,"");if(m&&!s.qs.includes(m))s.qs.push(m);(k.ex||"").replace(/Examples?|CAS \\d+/g,"").split(/[, ]+/).filter(Boolean).forEach(n=>{if(!s.ex.includes(n))s.ex.push(n)});if(k.es&&!s.es)s.es=k.es.replace(/^Ex \\S+ /,"")});
    const tb=Object.entries(secs).map(([sec,s])=>`<li><b>Ex ${esc(sec)}</b> ${esc(s.title)}: questions <b>${esc(s.qs.join(", "))}</b>${s.es?`, then exam-style ${esc(s.es)}`:""} <span class="hint">(worked examples ${esc(s.ex.join(", "))})</span></li>`);
    const tests=o.qs.map(q=>{const ks=(q.sk||[]).map(i=>T.skills[i]);return `<li class="pq"><div class="line"><span class="mono">Q${esc(q.q)}</span><span>${ks.length?ks.map(k=>`${esc(k.skill.charAt(0).toUpperCase()+k.skill.slice(1).replace(/\\.$/,""))} <span class="hint">(${esc(k.sec)})</span>`).join("; "):`<span class="hint">${esc(q.n)}</span>`}</span>${q.img?`<button class="peek" data-i="${D.qs.indexOf(q)}">Show</button>`:""}</div></li>`}).join("");
''')
rep('''<div class="glost">Lost ${o.marks} mark${o.marks>1?"s":""} on ${o.qs.map(q=>"Q"+esc(q.q)).join(", ")} · <span class="tier ${tierClass(T.sum.tier)}" style="font-size:.8rem">${esc(T.sum.tier.replace("Not yet examined (still examinable)","Not yet examined"))}</span></div></div></div>''',
 '''<div class="glost"><span class="chip ${LBL[o.k].c}">${LBL[o.k].l}</span> Lost ${o.marks} mark${o.marks>1?"s":""} · ${chip(o.f)} ${chip(succInfo(o.qs_))}</div><div class="hint" style="margin-top:4px">${LBL[o.k].why}</div></div></div>
      <div class="gsec"><h4>Cambridge skills tested by the questions you got wrong</h4><ul>${tests}</ul>${idx.length?"":'<p class="hint">These questions could not be matched to a specific skill, so all sections for the topic are listed below.</p>'}</div>''')
rep('''<div class="gsec"><h4>2 · Textbook tasks</h4><ul>${tb.join("")}</ul></div>''','''<div class="gsec"><h4>2 · Textbook tasks</h4><ul>${tb.join("")}</ul>${idx.length&&use.length<T.skills.length?`<details><summary class="hint">All sections for this topic</summary><ul>${[...new Set(T.skills.map(k=>k.sec))].map(s=>`<li>Ex ${esc(s)} ${esc(T.skills.find(k=>k.sec===s).title)}</li>`).join("")}</ul></details>`:""}</div>''')
rep('''    const x=D.qs[+b.dataset.i];const d=document.createElement("div");d.className="peekbox";d.innerHTML=`${x.pr?`<p class="hint" style="margin:0 0 6px">Part ${esc(x.q)} is highlighted.</p>`:""}''','''    const x=D.qs[+b.dataset.i];const d=document.createElement("div");d.className="peekbox";d.innerHTML=`${x.pr?`<p class="hint" style="margin:6px 0">Part ${esc(x.q)} is highlighted.</p>`:""}''')
# css chips
css='''.chip{display:inline-block;border-radius:999px;padding:2px 10px;font-weight:700;font-size:.8rem;width:fit-content;margin:2px 0}
.f4{background:#D7E6FA;color:#123A6B}.f3{background:#E3EEFB;color:#1D4C85}.f2{background:#EEF2F7;color:#3B4D63}.f1{background:#F2F2F2;color:#5A5F66}
.s3{background:#D6EED6;color:#1F5A22}.s2{background:#FBEBB8;color:#6B4D00}.s1{background:#F6D1C8;color:#7A2012}.sN{background:#ECEDEE;color:#555}
.qw{background:#0E6E62;color:#fff}.we{background:#B26A00;color:#fff}.lp{background:#6B7280;color:#fff}
.pq .line{align-items:center}
@media (max-width:520px){.pq .line{display:grid;grid-template-columns:1fr auto;gap:2px 10px}.pq .line>.mono{grid-column:1/-1}}
'''
t=t.replace("footer{color:var(--muted)",css+"footer{color:var(--muted)",1)
open('/tmp/w/app/template.html','w').write(t)
print('ok')
