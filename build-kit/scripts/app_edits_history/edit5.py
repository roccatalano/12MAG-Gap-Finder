p='/tmp/w/app/template.html';t=open(p).read()
t=t.replace('<button id="m-q" aria-pressed="false">One question</button>','<button id="m-o" aria-pressed="false">What\'s on the exam</button>\n      <button id="m-q" aria-pressed="false">One question</button>',1)
css='''
.ov-bar{display:flex;height:34px;border-radius:8px;overflow:hidden;font-size:.8rem;font-weight:700}
.ov-bar div{display:flex;align-items:center;justify-content:center;color:#fff;white-space:nowrap;overflow:hidden}
.ov-leg{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:.85rem;margin-top:8px}
.ov-leg i{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:5px;vertical-align:-1px}
.ov-tbl{width:100%;border-collapse:collapse;font-size:.88rem}
.ov-tbl th{text-align:left;cursor:pointer;border-bottom:2px solid var(--line,#ccc);padding:6px 4px;white-space:nowrap}
.ov-tbl td{border-bottom:1px solid var(--line,#ddd);padding:6px 4px;vertical-align:top}
.ov-tbl tbody tr{cursor:pointer}.ov-tbl tbody tr:hover{background:rgba(127,127,127,.1)}
.ov-scroll{overflow-x:auto}
.ov-sc text{fill:currentColor;font-size:11px}
@media(max-width:560px){.ov-tbl .hm{display:none}}
</style>'''
t=t.replace('</style>',css,1)
js=r'''
const AOSC={"Data analysis":"#2f6fb3","Recursion and financial modelling":"#2e8b57","Matrices":"#c77d12","Networks and decision mathematics":"#8a4fb3"};
function ovStats(){const tot=D.qs.reduce((a,q)=>a+q.m,0);return Object.keys(D.topics).map(c=>{const qs=D.qs.filter(q=>q.c===c);const m=qs.reduce((a,q)=>a+q.m,0);const w=qs.filter(q=>q.s!=null);const wm=w.reduce((a,q)=>a+q.m,0);const s=wm?w.reduce((a,q)=>a+q.s*q.m,0)/wm:null;return {c,T:D.topics[c],f:freqInfo(c),m,sh:m/tot,s,nq:qs.length}})}
let ovSort={k:"sh",d:-1};
function overview(){const R=ovStats();const tot=D.qs.reduce((a,q)=>a+q.m,0);const nP=new Set(D.qs.map(q=>q.p.replace(/ E[12]$/,""))).size;
const A={};R.forEach(r=>{A[r.T.aos]=(A[r.T.aos]||0)+r.m});
const bar=Object.entries(A).map(([a,m])=>`<div style="width:${m/tot*100}%;background:${AOSC[a]}" title="${esc(a)}">${Math.round(m/tot*100)}%</div>`).join("");
const leg=Object.entries(A).map(([a,m])=>`<span><i style="background:${AOSC[a]}"></i>${esc(a)} (${Math.round(m/tot*100)}%)</span>`).join("");
// scatter
const W=560,H=320,L=44,B=34,Tp=10,Rt=12;const xs=n=>L+(n-0.5)/(nP)*(W-L-Rt),ys=s=>Tp+(1-s)*(H-Tp-B);
let pts=R.filter(r=>r.s!=null&&r.f.n>0).map(r=>{const j=((r.c.charCodeAt(r.c.length-1)*7)%11-5)*2.2;return `<g style="cursor:pointer" onclick="goTopic('${r.c}')"><circle cx="${xs(r.f.n)+j}" cy="${ys(r.s)}" r="${4+r.sh*120}" fill="${AOSC[r.T.aos]}" fill-opacity=".75" stroke="#fff"/><title>${r.c} ${esc(r.T.name)}: ${r.f.n}/${nP} sittings, avg ${Math.round(r.s*100)}%</title><text x="${xs(r.f.n)+j+7}" y="${ys(r.s)+4}">${r.c}</text></g>`}).join("");
const mx=xs(3.5),my=ys(.6);
const sc=`<svg class="ov-sc" viewBox="0 0 ${W} ${H}" width="100%" role="img" aria-label="How often each topic appears vs how students go">
<rect x="${mx}" y="${Tp}" width="${W-Rt-mx}" height="${my-Tp}" fill="#2e8b57" fill-opacity=".08"/><rect x="${mx}" y="${my}" width="${W-Rt-mx}" height="${H-B-my}" fill="#c0392b" fill-opacity=".08"/>
<line x1="${L}" y1="${H-B}" x2="${W-Rt}" y2="${H-B}" stroke="currentColor" stroke-opacity=".4"/><line x1="${L}" y1="${Tp}" x2="${L}" y2="${H-B}" stroke="currentColor" stroke-opacity=".4"/>
${[0,.25,.5,.75,1].map(s=>`<text x="${L-6}" y="${ys(s)+4}" text-anchor="end">${s*100}%</text>`).join("")}
${Array.from({length:nP},(_,i)=>`<text x="${xs(i+1)}" y="${H-B+15}" text-anchor="middle">${i+1}</text>`).join("")}
<text x="${(L+W)/2}" y="${H-3}" text-anchor="middle">Number of sittings it appeared in (out of ${nP}) →</text>
<text x="${W-Rt-6}" y="${Tp+14}" text-anchor="end" font-weight="700">Common and most get it right: don't drop these marks</text>
<text x="${W-Rt-6}" y="${H-B-8}" text-anchor="end" font-weight="700">Common and hard: where marks are won</text>
${pts}</svg>`;
// table
const rows=R.slice().sort((a,b)=>{const k=ovSort.k;const v=r=>k==="c"?r.c:k==="n"?r.f.n:k==="s"?(r.s==null?-1:r.s):r.sh;return (v(a)>v(b)?1:v(a)<v(b)?-1:0)*ovSort.d||a.c.localeCompare(b.c)});
const th=(k,l,cl="")=>`<th class="${cl}" onclick="ovSortBy('${k}')">${l}${ovSort.k===k?(ovSort.d>0?" ▲":" ▼"):""}</th>`;
const tb=rows.map(r=>`<tr onclick="goTopic('${r.c}')"><td><b>${r.c}</b> ${esc(r.T.name)}</td><td>${r.f.n}/${nP}<br>${chip(r.f)}</td><td>${r.m?(r.sh*100).toFixed(1)+"%":"0%"}${r.m?"":"<br><small>Not yet examined (still examinable)</small>"}</td><td>${r.s==null?"–":Math.round(r.s*100)+"%"}<br>${chip(succInfo(r.s))}</td></tr>`).join("");
// task types
const TT={C:"Calculate",I:"Interpret",K:"Construct",T:"Technology"};
const tt=Object.keys(TT).map(k=>{const w=D.qs.filter(q=>q.t===k&&q.s!=null);const wm=w.reduce((a,q)=>a+q.m,0);const s=wm?w.reduce((a,q)=>a+q.s*q.m,0)/wm:null;const n=D.qs.filter(q=>q.t===k).length;return `<div class="card" style="padding:12px"><b>${TT[k]}</b><div style="font-size:1.6rem;font-weight:800">${s==null?"–":Math.round(s*100)+"%"}</div><small>average score · ${n} questions</small><br>${chip(succInfo(s))}</div>`}).join("");
// hardest
const hard=D.qs.filter(q=>q.s!=null).sort((a,b)=>a.s-b.s).slice(0,5).map(q=>`<li><a href="#" onclick="goQ('${q.p}','${q.q}');return false">${esc(q.p)} Q${esc(q.q)}</a>: ${esc(D.topics[q.c].name)} (${q.c}), ${Math.round(q.s*100)}% average</li>`).join("");
$("out").innerHTML=`<section class="card"><h2>What's on the exam</h2><p>Based on ${D.qs.length} questions from ${papers.length} papers (${nP} sittings, 2023 onwards, including NHT and the VCAA sample). Every topic in the study design can be examined, even ones that haven't come up yet.</p></section>
<section class="card"><h3>Where the marks are</h3><div class="ov-bar">${bar}</div><div class="ov-leg">${leg}</div></section>
<section class="card"><h3>How often vs how students go</h3><p class="tiermean">Each dot is a topic. Further right = appears in more exams. Lower = students score worse. Bigger dot = more marks. Tap a dot to open the topic.</p>${sc}</section>
<section class="card"><h3>Every topic</h3><p class="tiermean">Tap a heading to sort. Tap a row to see videos, textbook tasks and past questions.</p><div class="ov-scroll"><table class="ov-tbl"><thead><tr>${th("c","Topic")}${th("n","How often")}${th("sh","Share of marks")}${th("s","Average score")}</tr></thead><tbody>${tb}</tbody></table></div></section>
<section class="card"><h3>By type of question</h3><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px">${tt}</div></section>
<section class="card"><h3>The 5 hardest questions</h3><ol>${hard}</ol></section>`}
function ovSortBy(k){ovSort=ovSort.k===k?{k,d:-ovSort.d}:{k,d:k==="c"?1:-1};overview()}
function goTopic(c){$("topic").value=c;setMode("t");window.scrollTo(0,0)}
function goQ(p,q){$("paper").value=p;fillQ();$("qnum").value=q;setMode("q");window.scrollTo(0,0)}
function setMode(m){["x","o","q","t"].forEach(k=>$("m-"+k).setAttribute("aria-pressed",m===k));$("xpick").hidden=m!=="x";$("qpick").hidden=m!=="q";$("tpick").hidden=m!=="t";store.set("gf_mode",m);m==="x"?markUI():m==="o"?overview():m==="q"?showQ():render($("topic").value,null)}
'''
old=t[t.index('function setMode(m){'):t.index('\n',t.index('function setMode(m){'))]
t=t.replace(old,js.strip())
t=t.replace('$("m-q").onclick=()=>setMode("q");','$("m-q").onclick=()=>setMode("q");$("m-o").onclick=()=>setMode("o");')
t=t.replace('if(store.get("gf_mode")!=="q"&&store.get("gf_mode")!=="t"){fillQ();setMode("x")}','if(store.get("gf_mode")==="o"){fillQ();setMode("o")}\nelse if(store.get("gf_mode")!=="q"&&store.get("gf_mode")!=="t"){fillQ();setMode("x")}')
open(p,'w').write(t);print("ok")
