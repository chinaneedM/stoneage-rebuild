const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright');
const [file,output]=process.argv.slice(2);
(async()=>{const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{}),args:['--no-sandbox']});try{
 const page=await browser.newPage({viewport:{width:1250,height:1000}}),errors=[],requests=[];page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>{if(!r.url().startsWith('file:')&&!r.url().startsWith('data:'))requests.push(r.url())});await page.goto(pathToFileURL(path.resolve(file)).href);await page.waitForFunction(()=>window.scene21?.model?.frames);const frames=[];
 for(const view of ['expanded','old'])for(const parts of [false,true])for(const npc of [false,true]){
  await page.locator('#view').selectOption(view);await page.locator('#parts').setChecked(parts);await page.locator('#npc').setChecked(npc);
  const got=await page.evaluate(async()=>{const img=document.getElementById('picture');await img.decode();const r=scene21.model.report,key=scene21.state.key,c=document.createElement('canvas');c.width=img.naturalWidth;c.height=img.naturalHeight;c.getContext('2d').drawImage(img,0,0);const rgba=c.getContext('2d').getImageData(0,0,c.width,c.height).data;const digest=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',rgba)),x=>x.toString(16).padStart(2,'0')).join('');if(digest!==r.frames[key].RGBA_sha256)throw Error('frame pixels '+key);return{key,RGBA_sha256:digest,width:c.width,height:c.height,NPC_candidate_drawn:r.frames[key].NPC_candidate_actually_drawn}});frames.push(got);
 }
 if(frames.some(f=>f.key.startsWith('old_')&&f.NPC_candidate_drawn))throw Error('NPC must remain outside old viewport');
 await page.locator('#focusNpc').click();if(!await page.evaluate(()=>scene21.state.selected.join(',')==='63,103'&&document.getElementById('view').value==='expanded'))throw Error('NPC focus');
 await page.locator('#recovered').check();if(await page.locator('#overlay circle[stroke="#6bc4ec"]').count()!==24)throw Error('24 recovered occurrences');
 await page.locator('#focusDoor').click();if(!await page.evaluate(()=>scene21.state.selected.join(',')==='63,99'))throw Error('door focus');
 await page.locator('#overlay circle[data-xy="63,103"]').click();if(!await page.evaluate(()=>scene21.state.selected.join(',')==='63,103'&&document.getElementById('facts').textContent.includes('49152')))throw Error('raw cell inspection');
 await page.locator('#zoom').selectOption('2');if(!await page.evaluate(()=>parseInt(document.getElementById('stage').style.width)===scene21.model.report.canvas_size[0]*2))throw Error('integer modern zoom');
 await page.locator('#view').selectOption('old');if(await page.locator('#overlay circle[stroke="#6bc4ec"]').count()!==0)throw Error('recovered markers must remain outside old window');
 const synthetic=await page.evaluate(()=>!!scene21.model.synthetic_fixture);if(errors.length||requests.length)throw Error(JSON.stringify({errors,requests}));
 fs.writeFileSync(output,JSON.stringify({schema:'stoneage.scene21.browser_UI_QA.r1',scope:synthetic?'SYNTHETIC_UI_NO_ORIGINAL_PIXELS':'ACTUAL_PRIVATE_COMPOSITE_IMAGES',chromium:browser.version(),full_frame_states:frames,all8_frame_RGBA_hashes_equal:true,NPC_outside_old_view_refused:true,NPC_focus_expands_window:true,door_focus_verified:true,raw_NPC_cell_inspected:true,integer_zoom_verified:true,recovered_markers_expanded:24,recovered_markers_old:0,JS_errors:errors,external_requests:requests,actual_source_browser_verified:!synthetic,original_world_entered:false},null,2)+'\n');
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exit(1)});
