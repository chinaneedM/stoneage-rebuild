// Public CI: generated synthetic pixels only. Does not open the private observer.
const fs=require('fs'),path=require('path'),crypto=require('crypto'),{pathToFileURL}=require('url');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE);
(async()=>{const[file,out]=process.argv.slice(2);const browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_PATH,args:['--no-sandbox']});
try{const p=await browser.newPage({viewport:{width:1200,height:1000}}),errors=[],external=[];
p.on('pageerror',e=>errors.push(String(e)));p.on('request',r=>{if(!/^(file:|data:)/.test(r.url()))external.push(r.url())});
await p.goto(pathToFileURL(path.resolve(file)).href);
await p.getByText('96 幅候选配色图已解码',{exact:false}).waitFor();
const model=JSON.parse(await p.locator('#evidence').textContent());if(model.synthetic_fixture!==true)throw Error('synthetic-only source gate');
const frames=[];
for(const palette of ['0','1']){await p.getByLabel('候选色表',{exact:true}).selectOption(palette);
for(let direction=0;direction<8;direction++){await p.getByLabel('原方向值',{exact:true}).selectOption(String(direction));
for(let fi=0;fi<6;fi++){await p.getByRole('button',{name:`原帧 ${fi}`,exact:true}).click();
const actual=await p.locator('#actor').evaluate(c=>({rgba:Array.from(c.getContext('2d').getImageData(0,0,c.width,c.height).data),data:{...c.dataset}}));
const sha=crypto.createHash('sha256').update(Buffer.from(actual.rgba)).digest('hex');
const expected=model.canvas_hashes.find(x=>x.palette===palette&&x.direction===direction&&x.frame_index===fi);
if(sha!==expected.RGBA_sha256||Number(actual.data.frame)!==fi||Number(actual.data.direction)!==direction||actual.data.palette!==palette||Number(actual.data.bitmap)!==expected.bitmapno)throw Error(`synthetic canvas ${palette}/${direction}/${fi}`);
frames.push(expected);}}}
await p.locator('#reset').click();await p.locator('#previous').click();if(await p.locator('#actor').getAttribute('data-frame')!=='5')throw Error('previous wraps');
await p.locator('#next').click();if(await p.locator('#actor').getAttribute('data-frame')!=='0')throw Error('next wraps');
await p.locator('#play').click();await p.waitForFunction(()=>Number(document.getElementById('actor').dataset.frame)!==0);
await p.locator('#play').click();if(await p.locator('#play').getAttribute('aria-pressed')!=='false')throw Error('pause');
const stopped=await p.locator('#actor').getAttribute('data-draws');await p.waitForTimeout(250);if(await p.locator('#actor').getAttribute('data-draws')!==stopped)throw Error('pause still drawing');
await p.locator('#play').click();await p.locator('#direction').selectOption('7');if(await p.locator('#play').getAttribute('aria-pressed')!=='false'||await p.locator('#actor').getAttribute('data-frame')!=='0')throw Error('direction switch resets/stops');
await p.locator('#palette').selectOption('0');await p.locator('#reset').click();
const reset=await p.locator('#actor').evaluate(c=>({...c.dataset}));if(reset.direction!=='0'||reset.frame!=='0'||reset.palette!=='1')throw Error('reset');
if(errors.length||external.length)throw Error(JSON.stringify({errors,external}));
fs.writeFileSync(out,JSON.stringify({schema:'stoneage.scene31.synthetic_ui_browser.r1',scope:'SYNTHETIC_PIXELS_ONLY_NO_ORIGINAL_SOURCE_PAGE',browser:browser.version(),canvas_checks:frames.length,all96_synthetic_canvas_hashes_equal:true,frame_wrap_both_ways:true,play_pause_and_switch_stop:true,reset_verified:true,JS_errors:errors,external_requests:external,original_source_browser_verified:false,original_world_entered:false,frames},null,2)+'\n');
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exit(1)});
