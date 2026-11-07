const fs=require('fs'),path=require('path'),http=require('http');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright');
const [file,output]=process.argv.slice(2);
(async()=>{const root=path.dirname(path.resolve(file));
 const server=http.createServer((req,res)=>{const p=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://127.0.0.1').pathname));
  if(!p.startsWith(root+path.sep)||!fs.existsSync(p)||!fs.statSync(p).isFile()){res.writeHead(404);return res.end();}
  res.setHeader('Content-Type',p.endsWith('.html')?'text/html; charset=utf-8':p.endsWith('.js')?'text/javascript; charset=utf-8':p.endsWith('.png')?'image/png':'application/octet-stream');res.end(fs.readFileSync(p));});
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const base='http://127.0.0.1:'+server.address().port;
 const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{}),args:['--no-sandbox']});try{
 const page=await browser.newPage({viewport:{width:1100,height:900}}),errors=[],external=[];
 page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>{if(!r.url().startsWith(base+'/')&&!r.url().startsWith('data:'))external.push(r.url())});
 await page.goto(base+'/'+path.basename(file));await page.waitForFunction(()=>window.map09?.state.ready);
 if(!await page.evaluate(()=>map09.data.synthetic_fixture===true))throw Error('Synthetic fixture required; no original assets allowed in public CI');
 const frames=[];
 for(const floor of ['100','200','300'])for(const mode of ['plane0','plane1','combined']){
  await page.locator('#floor').selectOption(floor);await page.locator('#mode').selectOption(mode);
  await page.waitForFunction(({floor,mode})=>map09.state.ready&&map09.state.floor===floor&&map09.state.mode===mode,{floor,mode});
  frames.push(await page.evaluate(async()=>{const c=document.getElementById('scene'),rgba=c.getContext('2d').getImageData(0,0,c.width,c.height).data;
   const digest=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',rgba)),x=>x.toString(16).padStart(2,'0')).join('');
   const {floor,mode}=map09.state;if(digest!==map09.data.maps[floor].frame_RGBA_sha256[mode])throw Error('Complete synthetic canvas mismatch '+floor+'/'+mode);
   return{floor,mode,RGBA_sha256:digest,canvas:[c.width,c.height]};}));
 }
 await page.locator('#search').fill('20');await page.waitForFunction(()=>map09.state.ready&&map09.state.floor==='200');
 if(await page.locator('#floor option').count()!==1)throw Error('numeric filter');
 await page.locator('#next').click();await page.waitForFunction(()=>map09.state.ready);if(await page.locator('#floor').inputValue()!=='200')throw Error('filtered next wrap');
 await page.locator('#search').fill('no-match');if(await page.locator('#floor option').count()!==0||!await page.locator('#next').isDisabled())throw Error('empty filter');
 await page.locator('#search').fill('');await page.waitForFunction(()=>map09.state.ready);
 await page.locator('#floor').selectOption('300');await page.waitForFunction(()=>map09.state.ready&&map09.state.floor==='300');
 await page.locator('#next').click();await page.waitForFunction(()=>map09.state.ready&&map09.state.floor==='100');
 await page.locator('#prev').click();await page.waitForFunction(()=>map09.state.ready&&map09.state.floor==='300');
 await page.locator('#zoom').selectOption('2');if(!await page.evaluate(()=>parseInt(document.getElementById('scene').style.width)===document.getElementById('scene').width*2))throw Error('integer zoom');
 await page.locator('#zoom').selectOption('fit');if(!await page.evaluate(()=>!document.getElementById('scene').classList.contains('native')))throw Error('fit zoom');
 if(!await page.evaluate(async()=>{document.getElementById('floor').value='100';const first=show();document.getElementById('floor').value='200';const last=show();await Promise.all([first,last]);return map09.state.ready&&map09.state.floor==='200';}))throw Error('latest selection must win');
 if(errors.length||external.length)throw Error(JSON.stringify({errors,external}));
 fs.writeFileSync(output,JSON.stringify({schema:'stoneage.map09.synthetic_browser_acceptance.r1',scope:'SYNTHETIC_ONLY_NO_ORIGINAL_ASSETS',transport:'LOOPBACK_HTTP_SYNTHETIC_FIXTURE',chromium:browser.version(),frames,full_frame_states:frames.length,all_RGBA_hashes_equal:true,filter_empty_and_wrap_verified:true,integer_and_fit_zoom_verified:true,latest_selection_wins:true,JS_errors:errors,external_requests:external,actual_original_assets_browser_executed:false,original_client_executed:false},null,2)+'\n');
}finally{await browser.close();await new Promise(resolve=>server.close(resolve))}})().catch(e=>{console.error(e);process.exit(1)});
