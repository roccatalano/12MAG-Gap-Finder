const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const e=[];
for(const [pp,w,lab] of [['2025 VCAA E1',1200,'A'],['2025 VCAA E2',390,'1']]){const p=await b.newPage({viewport:{width:w,height:900}});p.on('pageerror',x=>e.push(x.message));
await p.goto('file:///tmp/w/app/gap-finder.html');await p.click('#m-x');await p.selectOption('#xpaper',pp);await p.waitForTimeout(200);
const bs=await p.$$(`.mgrid button:text-is("${lab}")`);for(let i=0;i<bs.length;i+=2)await bs[i].click();
await p.click('#build');await p.waitForTimeout(400);console.log(await p.$eval('#guide',g=>g.innerText.slice(0,200)));
await p.locator('section.card',{hasText:'Question by question'}).first().screenshot({path:`/tmp/w/res_${w}.png`});}
console.log(e);await b.close()})();
