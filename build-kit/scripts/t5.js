const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const errs=[];
for(const [w,dark,n] of [[1200,false,'d'],[390,false,'m'],[390,true,'k']]){const p=await b.newPage({viewport:{width:w,height:900},colorScheme:dark?'dark':'light'});p.on('pageerror',e=>errs.push(e.message));
await p.goto('file:///tmp/w/app/gap-finder.html');await p.click('#m-o');await p.waitForTimeout(300);await p.screenshot({path:`/tmp/w/ov_${n}.png`,fullPage:true});
if(n==='d'){await p.click('#m-x');await p.selectOption('#xpaper','2025 NHT E1').catch(()=>{});await p.waitForTimeout(200);console.log('E buttons:',await p.$$eval('button',bs=>bs.filter(b=>b.textContent.trim()==='E').length));
await p.selectOption('#xpaper','2025 VCAA E1');await p.waitForTimeout(200);const bs=await p.$$('button');let k=0;for(const x of bs){if((await x.textContent()).trim()==='A'&&k++<20)await x.click()}
const g=await p.$$('text=/Build|study guide/i');if(g[0])await g[0].click().catch(()=>{});await p.waitForTimeout(300);await p.screenshot({path:'/tmp/w/guide.png',fullPage:true});
await p.click('#m-o');await p.click('.ov-tbl tbody tr');await p.waitForTimeout(200);console.log('topic after click:',await p.$eval('#topic',s=>s.value));
await p.click('#m-q');await p.waitForTimeout(200);await p.screenshot({path:'/tmp/w/oneq.png'});}}
console.log('errors',errs);await b.close()})();
