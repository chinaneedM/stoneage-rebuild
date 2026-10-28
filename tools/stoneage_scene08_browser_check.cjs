// Real browser checks of a private source-bound page or explicit synthetic fixture.
'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const {chromium}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES?process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright':'playwright');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
(async()=>{
 const html=path.resolve(process.argv[2]),output=path.resolve(process.argv[3]),raw=fs.readFileSync(html);
 const pack=JSON.parse(raw.toString().split('<script id="evidence" type="application/json">')[1].split('</script>')[0]);
 for(const [n,b64] of Object.entries(pack.actor_images))assert.equal(sha(Buffer.from(b64,'base64')),pack.actors.bitmaps.find(b=>b.bitmapno===+n).PNG_sha256);
 for(const [n,b64] of Object.entries(pack.room.sprites))assert.equal(sha(Buffer.from(b64,'base64')),pack.room.sprite_sha256[n]);
 const browser=await chromium.launch({headless:true,...(process.env.STONEAGE_CHROMIUM_PATH?{executablePath:process.env.STONEAGE_CHROMIUM_PATH}:{}),args:['--no-sandbox','--disable-dev-shm-usage','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 try{
  const page=await browser.newPage({viewport:{width:1320,height:1200}}),errors=[],requests=[];
  page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url())});
  await page.goto('file://'+html);await page.waitForFunction(()=>window.__stoneageR8?.getState().ready);await page.click('#pause');
  const state=()=>page.evaluate(()=>window.__stoneageR8.getState());
  const canvasHash=()=>page.evaluate(()=>document.getElementById('world').toDataURL()).then(s=>sha(Buffer.from(s.split(',')[1],'base64')));
  assert.deepEqual(await page.locator('#action option').evaluateAll(a=>a.map(v=>v.value)),['2']);
  await page.click('#showHuman');let cases=0,framesChecked=0,repeatedCanvasChecks=0;
  for(const g of pack.actors.groups.slice(1))for(let d=0;d<8;d++){
   await page.selectOption('#pet',String(g.spr_no));await page.selectOption('#direction',String(d));
   const a=g.animations.find(a=>a.direction===d&&a.action===2);
   assert.equal(await page.locator('#identity').textContent().then(t=>t.includes(g.preserved_template_name)),true);
   const first=await canvasHash();await page.click('#step');assert.notEqual(await canvasHash(),first,'pet changes even with human hidden');
   await page.click('#reset');const seen=new Map();
   for(let f=0;f<a.frames.length;f++){
    const st=await state();assert.equal(st.petFrameIndex,f);assert.equal(st.petBitmap,a.frames[f][0]);framesChecked++;
    if(g.spr_no===100252&&d===0){const image=await canvasHash(),key=JSON.stringify(a.frames[f].slice(0,3));if(seen.has(key)){assert.equal(image,seen.get(key));repeatedCanvasChecks++}else seen.set(key,image)}
    await page.click('#step');
   }
   assert.equal((await state()).petFrameIndex,0);cases++;
  }
  assert.ok(repeatedCanvasChecks>0,'preserve repeated source frame positions visibly');
  await page.selectOption('#pet','100250');await page.selectOption('#direction','0');await page.click('#showHuman');await page.click('#reset');
  const initial=await canvasHash();
  for(const id of ['actors','showHuman','tiles','parts']){await page.click('#'+id);assert.notEqual(await canvasHash(),initial);await page.click('#'+id);assert.equal(await canvasHash(),initial)}
  for(let i=0;i<9;i++)await page.click('#moveRight');assert.equal((await state()).x,17);await page.click('#reset');
  await page.locator('h1').click();await page.keyboard.press('w');assert.equal((await state()).y,14);await page.click('#reset');
  await page.click('#zoomIn');assert.equal((await state()).scale,3.75);await page.click('#reset');
  const box=await page.locator('#world').boundingBox();await page.mouse.move(box.x+120,box.y+120);await page.mouse.down();await page.mouse.move(box.x+175,box.y+150);await page.mouse.up();assert.notEqual((await state()).dx,0);await page.click('#reset');assert.equal(await canvasHash(),initial);
  await page.selectOption('#rate','100');await page.click('#pause');const f=(await state()).frame;await page.waitForFunction(n=>window.__stoneageR8.getState().frame>n,f);await page.click('#pause');await page.click('#reset');
  fs.mkdirSync(output,{recursive:true});await page.screenshot({path:path.join(output,'internal-browser-review.png'),fullPage:true});
  const rgba=await page.evaluate(()=>Array.from(document.getElementById('world').getContext('2d').getImageData(0,0,960,720).data));fs.writeFileSync(path.join(output,'internal-canvas-rgba.bin'),Buffer.from(rgba));
  assert.deepEqual(errors,[]);assert.deepEqual(requests,[]);const st=await state();assert.equal(st.loaded,Object.keys(pack.actor_images).length+Object.keys(pack.room.sprites).length);
  const r={schema:'stoneage.scene08.actual_chromium.r1',browser:await browser.version(),scope:pack.actors.source_scope,private_html_sha256:sha(raw),images_decoded:st.loaded,pet_direction_cases:cases,all_pet_frame_positions_checked:framesChecked,repeated_source_frames_same_canvas:repeatedCanvasChecks,human_hidden_pet_pixel_changes_verified:true,missing_action6_no_fallback:true,manual_movement_bounds_keyboard:true,pause_step_playback:true,layers_pan_zoom_reset_pixel_exact:true,http_requests:requests.length,js_errors:errors,canvas_RGBA_sha256:sha(Buffer.from(rgba)),original_world_entered:false,official_species_identity_authenticated:false};
  fs.writeFileSync(path.join(output,'browser-acceptance.json'),JSON.stringify(r,null,2)+'\n');console.log(JSON.stringify(r));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
