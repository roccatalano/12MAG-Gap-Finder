t=open('/tmp/w/app/template.html').read()
t=t.replace('''  return `<div class="paper full"><img src="${IMG+q.img}" loading="lazy" alt="${esc(paperLabel(q.p))} question ${esc(String(q.q).match(/^\\d+/)[0])}"></div>`}''',
'''  const hl=q.pr?`<div class="hl" style="top:${(q.pr[0]/q.ih*100).toFixed(3)}%;height:${((q.pr[1]-q.pr[0])/q.ih*100).toFixed(3)}%"><span>Part ${esc(q.q)}</span></div>`:"";
  return `<div class="paper full"><div class="imgwrap"><img src="${IMG+q.img}" loading="lazy" alt="${esc(paperLabel(q.p))} question ${esc(String(q.q).match(/^\\d+/)[0])}">${hl}</div></div>`}''')
t=t.replace('r.innerHTML=`<td colspan="6">${qImage(x,x.pr?"part":"whole")}','r.innerHTML=`<td colspan="6">${x.pr?`<p class="hint" style="margin:0 0 6px">Full question shown so you can attempt it. <b>Part ${esc(x.q)}</b> is the highlighted section.</p>`:""}${qImage(x,"whole")}')
css='''.imgwrap{position:relative}
.hl{position:absolute;left:-6px;right:-6px;border:2px solid #E8A500;background:rgba(255,214,0,.13);border-radius:6px;pointer-events:none}
.hl span{position:absolute;right:6px;top:-11px;background:#E8A500;color:#1a1300;font:700 .72rem var(--body);padding:1px 7px;border-radius:999px}
.stack{display:flex;flex-direction:column;gap:2px;font-size:.85rem;color:var(--muted)}
.stack b{color:var(--ink)}
.tiermean{font-size:.82rem;color:var(--muted)}
.starters{margin-top:6px;display:flex;flex-direction:column;gap:6px}
.starters .kw{display:flex;flex-wrap:wrap;gap:4px}
.starters .kw span{background:var(--accent-soft);color:var(--accent);border-radius:5px;padding:1px 7px;font-size:.8rem;font-weight:600}
.starters .say{font-size:.85rem;border-left:3px solid var(--accent);padding-left:8px;font-style:italic;color:var(--ink)}
'''
t=t.replace("footer{color:var(--muted)",css+"footer{color:var(--muted)")
old='''  return `<div class="fact"><span class="eyebrow">Likelihood on the exam</span><span class="tier ${tierClass(T.tier)}">${esc(T.tier)}</span>
  <span class="s">Came up in <b>${n} of ${SITTINGS}</b> sittings · about <b>${T.per}</b> question${T.per==1?"":"s"} per sitting · ${(T.share*100).toFixed(1)}% of exam marks · rank #${T.rank} of 35</span></div>`}'''
assert old in t
t=t.replace(old,'''  const M={"Must":"One of the 9 topics that costs students the most marks. Top priority.","Should":"Comes up regularly or trips students up. Revise after the Must master topics.","Know":"A smaller share of marks, or students usually do well. Still examinable.","Not":"Not examined yet, but still examinable."};
  return `<div class="fact"><span class="eyebrow">Likelihood on the exam</span><span class="tier ${tierClass(T.tier)}">${esc(T.tier.replace("Not yet examined (still examinable)","Not yet examined"))}</span>
  <span class="tiermean">${M[tierClass(T.tier)]||""}</span>
  <div class="stack"><span>Came up in <b>${n} of ${SITTINGS}</b> sittings</span><span>About <b>${T.per}</b> question${T.per==1?"":"s"} per sitting</span><span><b>${(T.share*100).toFixed(1)}%</b> of exam marks</span><span>Priority rank <b>#${T.rank}</b> of 35 topics</span></div></div>`}''')
old='<span class="s">${q.s!=null?esc(q.sp):"NHT and sample papers have no published statistics"}</span>'
assert old in t
t=t.replace(old,'${q.s!=null?`<div class="stack">${q.sp.split(" | ").map(x=>`<span>${esc(x.replace("1 marks","1 mark"))} of students</span>`).join("")}</div>`:`<span class="s">NHT and sample papers have no published statistics</span>`}')
old='''  if(q)head+=`<div class="fact"><span class="eyebrow">Question type</span><span class="v">${TASK[q.t][0]}</span><span class="s">${TASK[q.t][1]}</span></div>'''
assert old in t
t=t.replace(old,old.replace('</span></div>','</span>${starters(code,q.t)}</div>',1) if False else '''  if(q)head+=`<div class="fact"><span class="eyebrow">Question type</span><span class="v">${TASK[q.t][0]}</span><span class="s">${TASK[q.t][1]}</span>${starters(code,q.t)}</div>''')
js='''const KW={C:{k:["show working","substitute","round as instructed","units"],s:"Write the rule, substitute the values, then give the answer to the required decimal places."},
I:{k:["on average","in context","refer to both variables","quote the numbers"],s:"Answer in a full sentence that uses the question's own variable names and numbers."},
K:{k:["label everything","correct order / notation","check it adds up","use the given template"],s:"Build it step by step and check it against the information given."},
T:{k:["enter data carefully","check the settings","write the values you used","round at the end"],s:"Write down what you entered into the CAS as your working."}};
function starters(code,t){const k=KW[t];const say=TB[code]?TB[code][3]:"";
  return `<div class="starters"><span class="eyebrow">Key words</span><div class="kw">${k.k.map(x=>`<span>${esc(x)}</span>`).join("")}</div><span class="eyebrow">How to write it</span><div class="say">${esc(say||k.s)}</div></div>`}
'''
t=t.replace("function render(code,q){",js+"function render(code,q){",1)
old='<div class="btnrow"><button class="btn" id="copy">Copy prompt</button><span class="hint" id="copied" role="status"></span></div>'
assert old in t
t=t.replace(old,'<div class="btnrow"><button class="btn" id="copy">1. Copy prompt</button>${q&&q.img?`<button class="btn" id="copyimg">2. Copy question image</button><a class="hint" href="${IMG+q.img}" target="_blank" rel="noopener">Open image</a>`:""}<span class="hint" id="copied" role="status"></span></div>')
import re
t=re.sub(r'<p class="hint">Paste into ChatGPT.*?</p>',"<p class=\"hint\">Paste the prompt into ChatGPT, Claude, Gemini or Copilot, then copy the question image and paste it into the same message. If copying the image doesn't work on your device, use Open image and save it, or take a screenshot.</p>",t,count=1)
t=t.replace('  $("copy").onclick=','''  if($("copyimg"))$("copyimg").onclick=async()=>{try{const blob=await (await fetch(IMG+q.img)).blob();await navigator.clipboard.write([new ClipboardItem({"image/png":blob})]);$("copied").textContent="Question image copied. Paste it into your AI tutor chat (Ctrl+V / Cmd+V)."}catch(e){$("copied").textContent="Your browser blocked copying the image. Use Open image and save it, or take a screenshot."}};
  $("copy").onclick=''',1)
open('/tmp/w/app/template.html','w').write(t)
print(t.count('copyimg'),t.count('starters(code'),t.count('tiermean'),t.count('class="hl"'))
