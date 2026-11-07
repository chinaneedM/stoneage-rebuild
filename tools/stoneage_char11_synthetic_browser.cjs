/* Modern observer controls only; no original pixels or original client. */
const fs=require('fs'),http=require('http'),{chromium}=require(process.env.PLAYWRIGHT_MODULE||process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright');
(async()=>{
 const [file,out]=process.argv.slice(2),html=fs.readFileSync(file);
 if(!html.includes(Buffer.from('metadata-and-test-pixels-only')))throw Error('synthetic fixture required');
 const pixel=Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGNI6dnyHwAFoAKkDAPw+wAAAABJRU5ErkJggg==','base64');
 let invalidSentinelRequests=0;
 const server=http.createServer((req,res)=>{
  if(req.url==='/'){res.setHeader('content-type','text/html; charset=utf-8');res.end(html)}
  else if(/^\/images\/\d+\.png$/.test(req.url)){
   if(req.url.includes('4294967295'))invalidSentinelRequests++;
   res.setHeader('content-type','image/png');res.end(pixel)
  }else{res.statusCode=404;res.end()}
 });
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const origin='http://127.0.0.1:'+server.address().port;
 let browser;
 try{
  browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{}),args:['--no-sandbox']});
  const page=await browser.newPage(),errors=[],external=[];
  page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>{if(!r.url().startsWith(origin+'/'))external.push(r.url())});
  await page.goto(origin);
  const result=await page.evaluate(()=>{
   const data=JSON.parse(document.querySelector('#source').textContent),before=JSON.stringify(data),$=id=>document.getElementById(id);
   if(Object.values(data.bitmaps).some(b=>b.status!=='SYNTHETIC_BROWSER_FIXTURE'))throw Error('original pixels forbidden');
   let sequences=0,positions=0,sentinelVisits=0;
   for(const group of data.groups){
    $('graphic').value=group.graphic;$('graphic').dispatchEvent(new Event('change'));
    for(const seq of group.sequences){
     $('action').value=seq.action;$('direction').value=seq.direction;$('action').dispatchEvent(new Event('change'));
     if(Number($('frame').max)!==seq.frames.length-1)throw Error('frame range changed');
     for(let i=0;i<seq.frames.length;i++){
      if(i!==0&&i!==seq.frames.length-1&&seq.frames[i][0]!==4294967295)continue;
      $('frame').value=i;$('frame').dispatchEvent(new Event('input'));
      const info=JSON.parse($('info').textContent),f=seq.frames[i];
      if(info.graphic!==group.graphic||info.bitmap!==f[0]||info.frame!==i+1||info.duration_raw!==seq.duration||
         info.offset_x_raw!==f[1]||info.offset_y_raw!==f[2]||info.sound_word_raw!==f[3])throw Error('source words changed');
      if(f[0]===4294967295){if(!$('picture').hidden||$('picture').hasAttribute('src'))throw Error('sentinel retains stale image');sentinelVisits++}
     }
     sequences++;positions+=seq.frames.length;
    }
   }
   if(before!==JSON.stringify(data))throw Error('source model mutated');
   return {groups:data.groups.length,sequences,source_frame_positions:positions,sentinel_positions_checked:sentinelVisits};
  });
  await page.selectOption('#graphic','100102');await page.selectOption('#direction','6');await page.selectOption('#action','8');
  if(await page.locator('#picture').isHidden())throw Error('valid frame missing before sentinel');
  await page.click('#next');if(!await page.locator('#picture').isHidden())throw Error('sentinel not hidden');
  await page.click('#prev');if(await page.locator('#picture').isHidden())throw Error('valid image not restored');
  await page.locator('#picture').evaluate(img=>img.decode());
  await page.selectOption('#graphic','100001');await page.selectOption('#direction','0');await page.selectOption('#action','0');
  await page.click('#play');await page.waitForTimeout(210);await page.click('#play');
  if(Number(await page.locator('#frame').inputValue())===0)throw Error('modern playback did not advance');
  if(errors.length||external.length||invalidSentinelRequests)throw Error(JSON.stringify({errors,external,invalidSentinelRequests}));
  const report={schema:'stoneage.char11.synthetic_observer_browser.r1',scope:'SOURCE_NUMERIC_METADATA_AND_SYNTHETIC_ONE_PIXEL_ONLY',
   ...result,browser:browser.version(),sentinel_valid_frame_transition_verified:true,modern_playback_verified:true,
   JS_errors:errors,external_requests:external,invalid_sentinel_image_requests:invalidSentinelRequests,
   original_pixels_loaded:false,original_client_executed:false};
  fs.writeFileSync(out,JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
 }finally{if(browser)await browser.close();await new Promise(resolve=>server.close(resolve))}
})().catch(e=>{console.error(e);process.exit(1)});
