// Actual Chromium qualification of a PRIVATE source-bound observer.
// Screenshots stay at caller-selected private paths. No original payload in Git.
'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const {chromium}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES?process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright':'playwright');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
(async()=>{
 const html=path.resolve(process.argv[2]),output=path.resolve(process.argv[3]);
 const bytes=fs.readFileSync(html),text=bytes.toString('utf8');
 const pack=JSON.parse(text.split('<script id="evidence" type="application/json">')[1].split('</script>')[0]);
 for(const [id,png] of Object.entries(pack.actor_images))assert.equal(sha(Buffer.from(png,'base64')),pack.actors.bitmaps.find(b=>b.bitmapno===+id).PNG_sha256);
 for(const [id,png] of Object.entries(pack.room.sprites))assert.equal(sha(Buffer.from(png,'base64')),pack.room.sprite_sha256[id]);
 const browser=await chromium.launch({headless:true,...(process.env.STONEAGE_CHROMIUM_PATH?{executablePath:process.env.STONEAGE_CHROMIUM_PATH}:{}),args:['--no-sandbox','--disable-dev-shm-usage','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 try{
  const page=await browser.newPage({viewport:{width:1320,height:1100}}),errors=[],requests=[];
  page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url())});
  await page.goto('file://'+html);await page.waitForFunction(()=>window.__stoneageR7?.getState().ready);
  await page.click('#pause');assert.equal((await page.evaluate(()=>window.__stoneageR7.getState())).playing,false);
  const canvasHash=()=>page.evaluate(()=>{const c=document.getElementById('world');return c.toDataURL()}).then(s=>sha(Buffer.from(s.split(',')[1],'base64')));
  let sequenceChanges=0;
  for(let direction=0;direction<8;direction++)for(const action of [2,6]){
   await page.selectOption('#direction',String(direction));await page.selectOption('#action',String(action));
   const before=await canvasHash();await page.click('#step');const after=await canvasHash();
   assert.notEqual(before,after,'source first two frames must be visibly distinct');sequenceChanges++;
  }
  await page.selectOption('#direction','0');await page.selectOption('#action','6');
  await page.click('#reset');const initial=await canvasHash();
  await page.click('#actors');const background=await canvasHash();assert.notEqual(background,initial);
  await page.click('#actors');assert.equal(await canvasHash(),initial);
  for(const id of ['tiles','parts']){await page.click('#'+id);assert.notEqual(await canvasHash(),initial);await page.click('#'+id);assert.equal(await canvasHash(),initial)}
  await page.click('#moveRight');assert.equal((await page.evaluate(()=>window.__stoneageR7.getState())).x,16);assert.notEqual(await canvasHash(),initial);
  for(let i=0;i<8;i++)await page.click('#moveRight');assert.equal((await page.evaluate(()=>window.__stoneageR7.getState())).x,17);
  await page.click('#reset');assert.equal(await canvasHash(),initial);
  await page.locator('h1').click();await page.keyboard.press('w');assert.equal((await page.evaluate(()=>window.__stoneageR7.getState())).y,14);
  await page.click('#reset');await page.click('#zoomIn');assert.equal((await page.evaluate(()=>window.__stoneageR7.getState())).scale,3.75);
  await page.click('#reset');const box=await page.locator('#world').boundingBox();await page.mouse.move(box.x+100,box.y+100);await page.mouse.down();await page.mouse.move(box.x+150,box.y+125);await page.mouse.up();assert.notEqual((await page.evaluate(()=>window.__stoneageR7.getState())).dx,0);
  await page.click('#reset');assert.equal(await canvasHash(),initial);
  await page.selectOption('#rate','100');await page.click('#pause');
  const start=await page.evaluate(()=>window.__stoneageR7.getState().frame);await page.waitForFunction(n=>window.__stoneageR7.getState().frame>n,start);
  await page.click('#pause');await page.click('#reset');
  fs.mkdirSync(output,{recursive:true});await page.screenshot({path:path.join(output,'internal-browser-review.png'),fullPage:true});
  const rgba=await page.evaluate(()=>Array.from(document.getElementById('world').getContext('2d').getImageData(0,0,960,720).data));
  fs.writeFileSync(path.join(output,'internal-canvas-rgba.bin'),Buffer.from(rgba));
  assert.deepEqual(errors,[]);assert.deepEqual(requests,[]);
  const state=await page.evaluate(()=>window.__stoneageR7.getState());assert.equal(state.loaded,Object.keys(pack.room.sprites).length+Object.keys(pack.actor_images).length);
  const receipt={schema:'stoneage.scene07.actual_chromium.r1',browser:await browser.version(),private_html_sha256:sha(bytes),source_images_decoded:state.loaded,source_sequences_changed:sequenceChanges,groups_per_sequence:pack.actors.groups.length,animation_pause_step:true,manual_movement_and_bounds:true,keyboard_movement:true,layer_roundtrip_pixel_exact:true,pan_zoom_reset:true,no_http_requests:true,js_errors:errors,canvas_rgba_sha256:sha(Buffer.from(rgba)),original_world_entered:false,native_actor_occlusion_verified:false};
  fs.writeFileSync(path.join(output,'browser-acceptance.json'),JSON.stringify(receipt,null,2)+'\n');console.log(JSON.stringify(receipt));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
