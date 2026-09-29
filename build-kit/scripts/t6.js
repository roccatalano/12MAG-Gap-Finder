const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:900}});const e=[];p.on('pageerror',x=>e.push(x.message));
await p.goto('file:///tmp/w/app/gap-finder.html');await p.click('#m-x');await p.selectOption('#xpaper','2025 VCAA E1');for(let i=0;i<12;i++){const bs=await p.$$('button:text-is("A")');await bs[i].click()}
await p.click('text=Build my study guide');await p.waitForTimeout(400);await p.screenshot({path:'g2.png',fullPage:true});console.log(e);await b.close()})();
