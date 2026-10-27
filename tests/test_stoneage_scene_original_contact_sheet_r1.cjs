#!/usr/bin/env node
"use strict";
// Browser-DOM and WebCrypto synthetic regression. No network or commercial resources.
const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const vm=require("node:vm");
const {createHash}=require("node:crypto");

const html=fs.readFileSync(path.join(__dirname,"../tools/scene-original-graphic-contact-sheet.html"),"utf8");
const scripts=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
assert.equal(scripts.length,1);
assert(html.includes("default-src 'none'"));
assert(!html.includes("fetch("));
assert(!html.includes("http://")&&!html.includes("https://"));

const image=Buffer.alloc(50);
image.writeUInt32BE(0x89504e47,0);
image.writeUInt32BE(0x0d0a1a0a,4);
image.writeUInt32BE(13,8);
image.writeUInt32BE(0x49484452,12);
image.writeUInt32BE(2,16);
image.writeUInt32BE(3,20);
image[24]=8;image[25]=0;
const sha=b=>createHash("sha256").update(b).digest("hex");

function manifest(){
  return {
    schema:"stoneage.private_recovered25_scene_graphic_join.r1",
    source_profile:"LATER_RECOVERED",
    source_bundle_role:"RECOVERED25_PRESERVED_UNVERIFIED_OFFICIAL_RELEASE",
    source_pins_match_preserved_bundle:true,
    source_adrn_sha256:"92d0137590d35a7a1f4fb11af3ad13bbc585813a4b0e1e3f933c397007fbff74",
    source_real_sha256:"c7640643804d550bc07e33661103fb7b5f557ee01e68a5a5d92382c5305c2b0d",
    original_client_executed:false,original_world_entered:false,authentic_scene_rendered:false,
    scene_projection_verified:false,palette_selection_verified:false,alpha_semantics_verified:false,
    collision_lookup_not_draw_selection:true,
    private_pngs_are_original_index_data_not_original_game_capture:true,
    draw_rule_grade:"DESCENDANT_SOURCE_LINEAGE_NOT_RECOVERED25_SAME_BUILD",
    source_map_payload_sha256:"a".repeat(64),
    floor_id:100,viewport_inclusive:[0,0,1,1],map_plane_cell_count:4,
    source_kind:"CLIENT_DAT_THREE_PLANE",event_plane_status:"RECOVERED_CLIENT_DAT",
    map_ids_required:[100],preview_count:1,
    resources:[{
      map_id:100,occurrences:[{map_number:100,bitmapno:8,source_record_sha256:"c".repeat(64)}],
      rendered_artwork:true,status:"PRIVATE_INDEXED_PIXEL_PREVIEW_ONLY",
      filename:"map-id-00100.png",private_grayscale_png_sha256:sha(image),
      rd_block_sha256:"d".repeat(64),decoded_palette_indices_sha256:"e".repeat(64)
    }]
  };
}

function browser({decodeFails=false}={}){
  const el={};
  class FakeElement{
    constructor(tag){
      this.tag=tag;this.items=[];this.textContent="";this.value="";this.files=[];
      this.naturalWidth=2;this.naturalHeight=3;this.srcValue="";
    }
    replaceChildren(){this.items=[]}
    append(...children){this.items.push(...children)}
    set src(value){
      this.srcValue=value;
      if(this.tag==="img")queueMicrotask(()=>{
        if(decodeFails)this.onerror?.();
        else this.onload?.();
      });
    }
    get src(){return this.srcValue}
  }
  for(const id of ["files","manifest","status","gallery"])el[id]=new FakeElement(id);
  let activeUrls=0,revoked=0;
  const fakeURL={
    createObjectURL(){activeUrls++;return"blob:synthetic-"+activeUrls},
    revokeObjectURL(){revoked++}
  };
  const crypto={subtle:{async digest(alg,bytes){
    assert.equal(alg,"SHA-256");
    return Uint8Array.from(createHash("sha256").update(Buffer.from(bytes)).digest()).buffer;
  }}};
  vm.runInNewContext(scripts[0][1],{
    document:{getElementById:id=>el[id],createElement:tag=>new FakeElement(tag)},
    window:{addEventListener(){}},URL:fakeURL,crypto,console,queueMicrotask
  },{filename:"scene-original-graphic-contact-sheet.html",timeout:2000});
  const pngFile={
    name:"map-id-00100.png",size:image.byteLength,
    async arrayBuffer(){return Uint8Array.from(image).buffer;}
  };
  async function load(m){
    const body=JSON.stringify(m);
    el.manifest.files=[{size:Buffer.byteLength(body),async text(){return body}}];
    await el.manifest.onchange();
    return {cards:el.gallery.items.length,message:el.status.textContent};
  }
  el.files.onchange({target:{files:[pngFile]}});
  return {load,el,urls:()=>({activeUrls,revoked})};
}

(async()=>{
  let b=browser();
  const ok=await b.load(manifest());
  assert.equal(ok.cards,1);
  assert.match(ok.message,/逐PNG SHA256与来源清单匹配：1张/);
  const f=b.el.gallery.items[0];
  assert.match(f.items[1].textContent,/map_number=100 \/ bitmapno=8/);
  assert.match(f.items[0].alt,/不是原游戏画面/);

  b=browser();let doc=manifest();doc.source_real_sha256="0".repeat(64);
  let res=await b.load(doc);
  assert.equal(res.cards,0);assert.match(res.message,/拒绝显示：来源标识/);

  b=browser();doc=manifest();doc.resources[0].private_grayscale_png_sha256="0".repeat(64);
  res=await b.load(doc);
  assert.equal(res.cards,0);assert.match(res.message,/PNG SHA256不匹配/);

  b=browser();doc=manifest();doc.event_plane_status="RECOVERED_CLIENT_DAT";
  doc.source_kind="SERVER_LS2MAP_TWO_PLANE";
  res=await b.load(doc);
  assert.equal(res.cards,0);assert.match(res.message,/事件层来源不合格/);

  b=browser();doc=manifest();doc.authentic_scene_rendered=true;
  res=await b.load(doc);
  assert.equal(res.cards,0);assert.match(res.message,/历史绘制资格声明不合格/);

  b=browser({decodeFails:true});
  res=await b.load(manifest());
  assert.equal(res.cards,0);assert.match(res.message,/浏览器无法解码PNG/);
  assert.equal(b.urls().activeUrls,b.urls().revoked);
  console.log("SCENE_ORIGINAL_GRAPHIC_CONTACT_SHEET_SYNTHETIC_BROWSER=PASS; ACTUAL_GAME_WORLD_ENTERED=FALSE");
})().catch(err=>{console.error(err);process.exitCode=1});
