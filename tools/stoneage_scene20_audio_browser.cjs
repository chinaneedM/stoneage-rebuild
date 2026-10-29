// Runs on synthetic fixtures in public CI. Can inspect a private page locally.
const fs=require('fs'),crypto=require('crypto'),path=require('path'),{pathToFileURL}=require('url');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright');
const [html,output]=process.argv.slice(2);if(!html||!output)throw Error('HTML path and output JSON required');
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{}),args:['--no-sandbox']});
 try{
 const page=await browser.newPage({viewport:{width:1200,height:900}}),errors=[],requests=[];
 page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>{if(!r.url().startsWith('file:')&&!r.url().startsWith('data:'))requests.push(r.url())});
 await page.goto(pathToFileURL(path.resolve(html)).href);await page.waitForFunction(()=>window.audioObserver?.files.length===127);
 if(await page.locator('#list button').count()!==127)throw Error('initial 127 rows');
 const initiallySilent=await page.evaluate(()=>document.getElementById('player').paused&&document.getElementById('player').getAttribute('src')===null);if(!initiallySilent)throw Error('unexpected autoplay');
 const decoded=await page.evaluate(async()=>{
  const out=[];const hex=b=>Array.from(new Uint8Array(b),x=>x.toString(16).padStart(2,'0')).join('');
  for(const f of audioObserver.files){
   const b=Uint8Array.from(atob(f.dataURI.split(',')[1]),c=>c.charCodeAt(0));
   const context=new OfflineAudioContext(f.channels,1,f.sample_rate),audio=await context.decodeAudioData(b.buffer),hashes=[];
   for(let c=0;c<audio.numberOfChannels;c++)hashes.push(hex(await crypto.subtle.digest('SHA-256',audio.getChannelData(c).buffer)));
   if(audio.numberOfChannels!==f.channels||audio.sampleRate!==f.sample_rate||audio.length!==f.frames)throw Error('decoded format/frame mismatch: '+f.original_path);
   // Chromium can map positive U8 samples by /127 rather than /128.
   // Verify the exact recovered ORIGINAL integer PCM, without rewriting audio.
   const negativeScale=f.sample_width_bytes===1?128:32768;let recovered=null;
   for(const model of ['SYMMETRIC_POWER_OF_TWO','ASYMMETRIC_POSITIVE_MAX']){
    const raw=new Uint8Array(f.frames*f.channels*f.sample_width_bytes),view=new DataView(raw.buffer);let withinRange=true;
    for(let i=0;i<f.frames;i++)for(let c=0;c<f.channels;c++){
     const v=audio.getChannelData(c)[i],scale=model==='ASYMMETRIC_POSITIVE_MAX'&&v>0?negativeScale-1:negativeScale,n=Math.round(v*scale),at=(i*f.channels+c)*f.sample_width_bytes;
     if(!Number.isFinite(v)||n< -negativeScale||n>negativeScale-1){withinRange=false;continue;}
     if(f.sample_width_bytes===1)raw[at]=n+128;else view.setInt16(at,n,true);
    }
    if(withinRange&&hex(await crypto.subtle.digest('SHA-256',raw.buffer))===f.PCM_sha256){recovered=model;break;}
   }
   if(recovered===null)throw Error('decoded integer PCM mismatch: '+f.original_path);
   out.push({path:f.original_path,frames:audio.length,channels:audio.numberOfChannels,sample_rate:audio.sampleRate,raw_float32_channel_sha256:hashes,raw_float32_matches_reference:JSON.stringify(hashes)===JSON.stringify(f.reference_float32_channel_sha256),recovered_original_PCM_sha256:f.PCM_sha256,recovery_normalization_model:recovered});
  }return out;
 });
 await page.locator('#category').selectOption('BGM_DIRECTORY');if(await page.locator('#list button').count()!==11)throw Error('BGM filtering');
 await page.locator('#category').selectOption('SFX_DIRECTORY');if(await page.locator('#list button').count()!==116)throw Error('SFX filtering');
 await page.locator('#category').selectOption('ALL');const first=await page.locator('#list button').first().getAttribute('data-path');
 await page.locator('#search').fill(path.basename(first));if(await page.locator('#list button').count()!==1)throw Error('exact basename search');
 await page.locator('#list button').click();await page.locator('#play').click();await page.waitForFunction(()=>document.getElementById('player').currentTime>0.03);
 await page.locator('#pause').click();if(!await page.evaluate(()=>document.getElementById('player').paused))throw Error('pause');
 await page.locator('#loop').check();if(!await page.evaluate(()=>document.getElementById('player').loop))throw Error('modern loop');
 await page.locator('#search').fill('');await page.locator('#list button').nth(1).click();
 if(!await page.evaluate(()=>document.getElementById('player').paused&&!document.getElementById('player').loop))throw Error('selection must stop/reset loop');
 if(errors.length||requests.length)throw Error(JSON.stringify({errors,requests}));
 const synthetic=decoded.every(x=>x.path.startsWith('SYNTHETIC_NOT_ORIGINAL/'));
 fs.writeFileSync(output,JSON.stringify({schema:'stoneage.scene20.browser_audio_QA.r1',scope:synthetic?'SYNTHETIC_FIXTURE_ONLY_NO_ORIGINAL_AUDIO_READ':'ACTUAL_PRIVATE_ORIGINAL_AUDIO',chromium:browser.version(),decoded_files:decoded.length,all_recovered_integer_PCM_hashes_equal:true,raw_float32_reference_match_count:decoded.filter(x=>x.raw_float32_matches_reference).length,initially_silent:true,directory_filter_counts:[11,116],exact_name_search:true,media_time_advanced:true,pause_verified:true,selection_stops_playback_and_resets_modern_loop:true,JS_errors:errors,external_requests:requests,original_audio_verified:!synthetic,assistant_heard_audio:false,audio_output_to_speaker_verified:false,original_game_world_entered:false,decoded},null,2)+'\n');
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
