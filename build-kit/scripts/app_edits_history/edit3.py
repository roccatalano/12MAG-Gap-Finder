t=open('/tmp/w/app/template.html').read()
# modes
t=t.replace('<button id="m-q" aria-pressed="true">By exam question</button>',
 '<button id="m-x" aria-pressed="true">Mark my exam</button>\n      <button id="m-q" aria-pressed="false">One question</button>')
t=t.replace('<div class="row" id="qpick">','<div class="row" id="xpick"><div class="field"><label for="xpaper">Exam I sat</label><select id="xpaper"></select></div></div>\n    <div class="row" id="qpick" hidden>')
t=t.replace("Got an exam question wrong? Pick it below to see what topic it tests, how often it comes up, and exactly what to watch, ask, practise and retry.",
 "Sat a practice exam? Enter your results and get a study guide: the videos to watch, textbook questions to do and exam questions to practise, highest priority first.")
css='''.marker{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;display:flex;flex-direction:column;gap:12px}
.mrow{display:grid;grid-template-columns:70px 1fr;gap:10px;align-items:center;padding:6px 0;border-bottom:1px solid var(--line)}
.mrow .ql{font-family:var(--mono);font-size:.9rem}
.opts{display:flex;flex-wrap:wrap;gap:6px}
.opts button{min-width:40px;font:600 .9rem var(--body);border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:7px;padding:6px 10px;cursor:pointer}
.opts button[aria-pressed="true"]{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.opts button.ok[aria-pressed="true"]{background:var(--good);border-color:var(--good);color:#fff}
.opts button.no[aria-pressed="true"]{background:var(--bad);border-color:var(--bad);color:#fff}
.mgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:0 24px}
.score{display:flex;flex-wrap:wrap;gap:16px;align-items:baseline}
.score .big{font:700 2rem var(--display)}
.gtopic{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px;display:flex;flex-direction:column;gap:12px}
.gtopic h3{font-size:1.1rem}
.glost{font-size:.9rem;color:var(--muted)}
.gsec{display:flex;flex-direction:column;gap:6px}
.gsec h4{margin:0;font:700 .78rem var(--body);letter-spacing:.07em;text-transform:uppercase;color:var(--muted)}
.gsec ul{margin:0;padding-left:18px;display:flex;flex-direction:column;gap:4px}
.gsec a{color:var(--accent);font-weight:600}
.pq{display:flex;flex-direction:column;gap:6px}
.pq .line{display:flex;flex-wrap:wrap;gap:10px;align-items:baseline}
.rank{flex:none;width:28px;height:28px;border-radius:50%;background:var(--ink);color:var(--bg);display:inline-grid;place-items:center;font:700 .85rem var(--display)}
.ghead{display:flex;gap:12px;align-items:flex-start}
.done{color:var(--muted);font-size:.9rem}
'''
t=t.replace("footer{color:var(--muted)",css+"footer{color:var(--muted)")
js=r'''
// ---------- Mark my exam ----------
const store={get(k){try{return JSON.parse(localStorage.getItem(k))}catch(e){return null}},set(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}};
let RES=store.get("gf_results")||{};
let E1MODE=store.get("gf_e1mode")||"letters";
fill($("xpaper"),papers.map(p=>[p,paperLabel(p)]));
function paperQs(p){return D.qs.filter(q=>q.p===p)}
function markUI(){const p=$("xpaper").value,qs=paperQs(p),e1=p.endsWith("E1"),r=RES[p]||(RES[p]={});
  const hasKey=e1&&qs.every(q=>q.a);const mode=e1?(hasKey?E1MODE:"tick"):"marks";
  let h=`<section class="marker"><div class="stephead"><span class="num">1</span><div><h2>Enter your results</h2><p>${e1?(hasKey?"Tap the letter you chose, or switch to ticks if you've already marked it.":"No answer key for this paper, so tick right or wrong."):"Use the examiners' report to mark yourself, then tap the marks you got for each part."}</p></div></div>`;
  if(e1&&hasKey)h+=`<div class="qtoggle" role="group" aria-label="Entry style"><button id="e1l" aria-pressed="${mode==="letters"}">My letters</button><button id="e1t" aria-pressed="${mode==="tick"}">Right / wrong</button></div>`;
  h+=`<div class="mgrid">`+qs.map((q,i)=>{const v=r[q.q];let o="";
    if(mode==="letters")o="ABCDE".slice(0,q.p.startsWith("2023")||q.p.includes("NHT")||q.p.includes("Sample")?5:4).split("").map(L=>`<button data-i="${i}" data-v="${L}" aria-pressed="${v===L}">${L}</button>`).join("");
    else if(mode==="tick")o=`<button class="ok" data-i="${i}" data-v="1" aria-pressed="${v===1}">✓ Right</button><button class="no" data-i="${i}" data-v="0" aria-pressed="${v===0}">✗ Wrong</button>`;
    else o=[...Array(q.m+1).keys()].map(k=>`<button data-i="${i}" data-v="${k}" aria-pressed="${v===k}">${k}</button>`).join("")+`<span class="hint">/ ${q.m}</span>`;
    return `<div class="mrow"><span class="ql">Q${esc(q.q)}</span><div class="opts">${o}</div></div>`}).join("")+`</div>`;
  const done=qs.filter(q=>r[q.q]!==undefined).length;
  h+=`<div class="btnrow"><button class="btn" id="build">Build my study guide</button><span class="hint">${done} of ${qs.length} entered · saved on this device</span><button class="peek" id="clear" style="font:600 .85rem var(--body);color:var(--muted);background:none;border:0;text-decoration:underline;cursor:pointer">Clear this paper</button></div></section><div id="guide" class="wrap" style="gap:16px"></div>`;
  $("out").innerHTML=h;
  if($("e1l")){$("e1l").onclick=()=>{E1MODE="letters";store.set("gf_e1mode",E1MODE);RES[p]={};store.set("gf_results",RES);markUI()};$("e1t").onclick=()=>{E1MODE="tick";store.set("gf_e1mode",E1MODE);RES[p]={};store.set("gf_results",RES);markUI()}}
  document.querySelectorAll(".opts button").forEach(b=>b.onclick=()=>{const q=qs[+b.dataset.i];const v=isNaN(+b.dataset.v)?b.dataset.v:+b.dataset.v;r[q.q]=v;store.set("gf_results",RES);
    b.parentElement.querySelectorAll("button").forEach(x=>x.setAttribute("aria-pressed",x===b));
    const d=qs.filter(x=>r[x.q]!==undefined).length;document.querySelector(".marker .btnrow .hint").textContent=`${d} of ${qs.length} entered · saved on this device`});
  $("clear").onclick=()=>{RES[p]={};store.set("gf_results",RES);markUI()};
  $("build").onclick=()=>buildGuide(p);
  if(done===qs.length)buildGuide(p,true);
}
function scored(q,v,e1){if(v===undefined)return null;if(!e1)return v;if(typeof v==="number")return v;return v===q.a?1:0}
function buildGuide(p,quiet){const qs=paperQs(p),r=RES[p]||{},e1=p.endsWith("E1");
  let got=0,tot=0,miss=0;const lost={};
  qs.forEach(q=>{const s=scored(q,r[q.q],e1);if(s===null){miss++;return}tot+=q.m;got+=s;const l=q.m-s;if(l>0){(lost[q.c]=lost[q.c]||{marks:0,qs:[]}).marks+=l;lost[q.c].qs.push(q)}});
  if(!tot){$("guide").innerHTML=quiet?"":`<p class="hint">Enter at least some results first.</p>`;return}
  const cohort=qs.filter(q=>q.s!=null);const avg=cohort.length===qs.length?Math.round(qs.reduce((a,q)=>a+q.s*q.m,0)/qs.reduce((a,q)=>a+q.m,0)*100):null;
  const order=Object.keys(lost).map(c=>({c,...lost[c],score:lost[c].marks*(1+D.topics[c].sum.lost*25)})).sort((a,b)=>b.score-a.score);
  let h=`<section class="qhead"><div class="stephead"><span class="num">2</span><div><h2>Your study guide</h2><p>Topics where you lost marks, highest priority first. Priority combines the marks you lost with how often the topic is examined.</p></div></div>
   <div class="score"><span class="big">${got} / ${tot}</span><span class="hint">${Math.round(got/tot*100)}% on the questions entered${miss?` (${miss} not entered yet)`:""}${avg!=null?` · state average ${avg}%`:""}</span></div></section>`;
  if(!order.length)h+=`<p class="done">No marks lost on the questions entered. Try another paper.</p>`;
  order.forEach((o,i)=>{const T=D.topics[o.c];
    const vids=[];o.qs.forEach(q=>{if(q.v)vids.push(`<li><a href="${esc(q.v)}" target="_blank" rel="noopener">Worked solution: ${esc(paperLabel(q.p))} Q${esc(q.q)}</a> <span class="hint">MaffsGuru${q.vl==="whole video"?" · full paper video":" · "+esc(q.vl)}</span></li>`)});
    T.vids.filter(Boolean).forEach(v=>vids.push(`<li><a href="https://www.youtube.com/watch?v=${v.id}" target="_blank" rel="noopener">${esc(v.t)}</a> <span class="hint">${esc(v.ch)} · ${esc(v.len)}</span></li>`));
    if(T.cp)vids.push(`<li><a href="https://www.youtube.com/watch?v=${T.cp.id}" target="_blank" rel="noopener">ClassPad: ${esc(T.cp.t)}</a> <span class="hint">${esc(T.cp.len)}</span></li>`);
    if(T.ti)vids.push(`<li><a href="https://www.youtube.com/watch?v=${T.ti.id}" target="_blank" rel="noopener">TI-Nspire: ${esc(T.ti.t)}</a> <span class="hint">${esc(T.ti.len)}</span></li>`);
    const tb=T.skills.map(k=>`<li><b>${esc(k.hw||k.sec)}</b> · ${esc(k.skill.charAt(0).toUpperCase()+k.skill.slice(1))} <span class="hint">(read ${esc(k.ex||"section "+k.sec)})</span></li>`);
    tb.push(`<li>Exam-style revision: Cambridge ${esc(T.rev)}</li>`);
    const types=new Set(o.qs.map(q=>q.t));
    const prac=D.qs.filter(x=>x.c===o.c&&x.p!==p).map(x=>({x,sc:(types.has(x.t)?3:0)+(x.v?1:0)+(x.s!=null?.5:0)})).sort((a,b)=>b.sc-a.sc||(a.x.s??.5)-(b.x.s??.5)).slice(0,5);
    const pq=prac.map(({x})=>`<li class="pq"><div class="line"><span class="mono">${esc(paperLabel(x.p))} Q${esc(x.q)}</span><span>${esc(x.n)}</span>${x.s!=null?`<span class="hint">avg ${pct(x.s)}</span>`:""}${x.img?`<button class="peek" data-i="${D.qs.indexOf(x)}">Show</button>`:""}${x.v?`<a href="${esc(x.v)}" target="_blank" rel="noopener">▶ Solution</a>`:""}</div></li>`);
    h+=`<section class="gtopic"><div class="ghead"><span class="rank">${i+1}</span><div><h3>${esc(T.name)}</h3><div class="glost">Lost ${o.marks} mark${o.marks>1?"s":""} on ${o.qs.map(q=>"Q"+esc(q.q)).join(", ")} · <span class="tier ${tierClass(T.sum.tier)}" style="font-size:.8rem">${esc(T.sum.tier.replace("Not yet examined (still examinable)","Not yet examined"))}</span></div></div></div>
      <div class="gsec"><h4>1 · YouTube videos</h4><ul>${vids.join("")}</ul></div>
      <div class="gsec"><h4>2 · Textbook tasks</h4><ul>${tb.join("")}</ul></div>
      <div class="gsec"><h4>3 · Exam questions to practise</h4><ul>${pq.join("")||'<li class="hint">No other past questions on this topic.</li>'}</ul></div></section>`});
  $("guide").innerHTML=h;
  $("guide").querySelectorAll("button.peek").forEach(b=>b.onclick=()=>{const li=b.closest(".pq");const ex=li.querySelector(".peekbox");if(ex){ex.remove();b.textContent="Show";return}
    const x=D.qs[+b.dataset.i];const d=document.createElement("div");d.className="peekbox";d.innerHTML=`${x.pr?`<p class="hint" style="margin:0 0 6px">Part ${esc(x.q)} is highlighted.</p>`:""}${qImage(x,"whole")}<div class="src">${srcLine(x)}</div>`;li.appendChild(d);b.textContent="Hide"});
  if(!quiet)$("guide").scrollIntoView({behavior:"smooth",block:"start"});
}
'''
t=t.replace("function setMode(m){",js+"function setMode(m){")
t=t.replace('function setMode(m){$("m-q").setAttribute("aria-pressed",m==="q");$("m-t").setAttribute("aria-pressed",m==="t");$("qpick").hidden=m!=="q";$("tpick").hidden=m!=="t";m==="q"?showQ():render($("topic").value,null)}',
 'function setMode(m){$("m-x").setAttribute("aria-pressed",m==="x");$("m-q").setAttribute("aria-pressed",m==="q");$("m-t").setAttribute("aria-pressed",m==="t");$("xpick").hidden=m!=="x";$("qpick").hidden=m!=="q";$("tpick").hidden=m!=="t";store.set("gf_mode",m);m==="x"?markUI():m==="q"?showQ():render($("topic").value,null)}')
t=t.replace('$("m-q").onclick=()=>setMode("q");','$("m-x").onclick=()=>setMode("x");$("xpaper").onchange=()=>{store.set("gf_xpaper",$("xpaper").value);markUI()};$("m-q").onclick=()=>setMode("q");')
# startup: default to mark mode
i=t.index('let saved=null;');j=t.index('</script>',i)
start=t[i:j]
t=t[:i]+start.replace('if(saved&&saved.t&&D.topics[saved.t])','const xp=store.get("gf_xpaper");if(xp&&papers.includes(xp))$("xpaper").value=xp;else $("xpaper").value="2025 VCAA E1";\nif(store.get("gf_mode")!=="q"&&store.get("gf_mode")!=="t"){fillQ();setMode("x")}\nelse if(saved&&saved.t&&D.topics[saved.t])')+t[j:]
open('/tmp/w/app/template.html','w').write(t)
print(t.count('markUI'),t.count('m-x'))
