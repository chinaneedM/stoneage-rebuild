// Private HTML DOM simulation; explicitly not Chromium or original gameplay.
'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const html=fs.readFileSync(process.argv[2],'utf8');
const model=JSON.parse(html.split('<script id="evidence" type="application/json">')[1].split('</script>')[0]);
const script=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];assert.equal(script.length,1);
const elements={},drawn=[];
const ctx=new Proxy({drawImage(im,x,y){drawn.push([im.mapId,x,y]);},clearRect(){drawn.length=0;}},
 {get(o,k){return o[k]??(()=>{});}});
for(const id of ['status','world','tiles','parts','gaps','nativeOrder','zoomIn','zoomOut','reset'])
 elements[id]={checked:true,width:960,height:720,textContent:'',addEventListener(){},getContext(){return ctx;}};
elements.evidence={textContent:JSON.stringify(model)};
class SourcePNG {
 set src(s){
  const value=s.split(',')[1],b=Buffer.from(value,'base64');
  this.mapId=+Object.entries(model.sprites).find(([k,v])=>v===value)[0];
  this.width=b.readUInt32BE(16);this.height=b.readUInt32BE(20);
  queueMicrotask(()=>this.onload());
 }
}
const window={};
vm.runInNewContext(script[0][1],{document:{getElementById:id=>elements[id]},Image:SourcePNG,window,
 addEventListener(){},console,queueMicrotask},{timeout:2000});
setImmediate(()=>{
 const old=model.placements.map(p=>[p.map_id,p.draw_x,p.draw_y]);
 const current=model.R6_native_sorted_queue_numbers.map(i=>old[i]);
 assert.deepEqual(drawn,current);assert.equal(window.__stoneageR6.getState().loaded,10);
 elements.nativeOrder.checked=false;elements.nativeOrder.onchange();assert.deepEqual(drawn,old);
 elements.nativeOrder.checked=true;elements.nativeOrder.onchange();assert.deepEqual(drawn,current);
 elements.parts.checked=false;elements.parts.onchange();assert.equal(drawn.length,25);
 elements.parts.checked=true;elements.parts.onchange();assert.deepEqual(drawn,current);
 elements.zoomIn.onclick();assert.equal(window.__stoneageR6.getState().scale,3.75);
 elements.reset.onclick();assert.equal(window.__stoneageR6.getState().scale,3);
 console.log(JSON.stringify({schema:'stoneage.scene06.private_DOM_simulation',images:10,placements:30,
  order_comparison_toggle:true,layers_zoom_reset:true,actual_chromium:false,original_world_entered:false}));
});
