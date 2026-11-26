"""Build an offline source-record atlas from the existing verified PET lookup.
Not an official species roster or a private original-pixel viewer.
"""
import argparse
import json
from pathlib import Path
import stoneage_pet_source_lookup as lookup

FIELDS = [
    "身份与正式发行", "名称、别名及系列", "属性", "初始数值与区间",
    "成长算法与范围", "自带／可学技能", "头像与图鉴说明", "原2D图与动作",
    "捕获地点、坐标、等级", "任务、奖励及其他取得", "来源、冲突、未知"
]

# PET31 is an immutable historical audit; PET32/33 subsequently appended
# later-carrier portrait variants to these four dossiers, not TW1 portraits.
PORTRAIT_SUPERSESSIONS = {
    "PET-000116": [
        "c30074eea6d3a512dd770e98128dacf7c24b5949",
        "12b9cf7eacffffb79a99a969a0f548fd44de3f29"
    ],
    "PET-000117": [
        "7c26aa68f09a78a1aa3fd604a9b43012ab27c5c7",
        "b273779f037a3964adb038cff1f4631d1bf5ba9f"
    ],
    "PET-000118": [
        "478fb629a402e008239cbcdfc3d4310c8c6de9c6",
        "951fcb88fd6ccb4892546068072c11b4f246ef5c"
    ],
    "PET-000119": [
        "0c5af1a2d02e12da747f257e2219d361a59c6053",
        "b95ce83701681c66713e0e963c2aaacdf4f941bb"
    ]
}

def payload():
    manifest, data = lookup.load()
    rows = lookup.build(data)
    lookup.verify(manifest, data, rows)
    sources = {k: {"path": v["path"], "git_blob": v["git_blob"]}
               for k, v in manifest["sources"].items()}
    profiles = {}
    for row in rows:
        if row["source"] != "tw10":
            continue
        detail = row["detail"]
        path = detail["dossier_path"]
        assert path.startswith("research/pets/profiles/") and ".." not in Path(path).parts
        raw = (lookup.ROOT / path).read_bytes()
        source_row = lookup.resolve(data, row["source"], row["pointer"])
        current_blob = lookup.blob(raw)
        audit_blob = source_row["dossier_git_blob"]
        if detail["pet_id"] in PORTRAIT_SUPERSESSIONS:
            assert [audit_blob, current_blob] == PORTRAIT_SUPERSESSIONS[detail["pet_id"]]
        else:
            assert current_blob == audit_blob
        profile = json.loads(raw)
        assert profile["profile_id"] == detail["pet_id"]
        assert profile["names"]["original_client"] in row["labels"]
        assert profile["appearance"]["graphic_number"] == detail["graphic"]
        assert not profile["status"]["all_fields_historically_complete"]
        if detail["pet_id"] in PORTRAIT_SUPERSESSIONS:
            candidates = profile["appearance"]["cross_version_original_portrait_rd_candidates"]
            assert candidates["original_TW10_portrait_remains_missing"]
            assert candidates["original_TW10_source_RDto_appearance_portrait_not_backfilled"]
            assert len(candidates["TW85_saved_PC_higher_variants"]) == 2
            assert profile["appearance"]["portrait"]["source_rd_bitmap_number"] is None
        profiles[profile["profile_id"]] = {"path": path, "git_blob": current_blob, "historical_audit_git_blob": audit_blob, "profile": profile}
    return {
        "profiles": profiles,
        "schema": "stoneage.pet.offline_source_atlas.r1",
        "summary": lookup.summary(rows),
        "fields": FIELDS,
        "historically_complete": False,
        "official_species_count": None,
        "original_pixels_included": False,
        "sources": sources,
        "rows": rows,
    }

def safe_json(data):
    # No source text can close the inert script element or inject HTML.
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")

PAGE = """<!doctype html>
<html lang="zh-Hans"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'none'; img-src 'none'; base-uri 'none'; form-action 'none'">
<title>石器时代｜离线宠物来源档案 R1</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#f4f3ef;color:#262820;font:15px/1.55 system-ui,sans-serif}header{background:#293c34;color:white;padding:22px 28px}h1{font-size:24px;margin:0 0 6px}main{padding:18px 24px;max-width:1450px;margin:auto}.notice{padding:12px;background:#fff4d8;border:1px solid #e5d5a5;margin-bottom:15px}.controls{display:flex;gap:8px;flex-wrap:wrap;align-items:center}input,select,button{font:inherit;padding:8px;border:1px solid #a8aca4;border-radius:5px;background:white;color:#26392f}input{flex:1;min-width:200px}.layout{display:grid;grid-template-columns:minmax(250px,1fr) minmax(0,2fr);gap:15px;margin-top:14px}.panel{background:white;padding:15px;border:1px solid #ddd;border-radius:7px;min-width:0}#list button{display:block;width:100%;text-align:left;margin:5px 0;overflow-wrap:anywhere}button:hover,button:focus{border-color:#2d6d50}pre{font:13px/1.5 ui-monospace,monospace;white-space:pre-wrap;overflow-wrap:anywhere;background:#f5f5f1;padding:12px}h2{font-size:19px;margin:0}h3{font-size:15px;margin:16px 0 4px}small{color:#555}ul{padding-left:20px;overflow-wrap:anywhere}@media(max-width:760px){.layout{grid-template-columns:1fr}main{padding:12px}}
</style><header><h1>石器时代 · 宠物来源档案</h1>离线研究入口 R1 ｜ 原版经典 PC ｜ 来源位置互相独立</header>
<main><div class="notice">本页是来源记录整合，不是全量官服物种图鉴。没有原图像文件；图像哈希和动作引用不等于可观看原图。正式身份、初值、成长、技能和取得没有同部署证据时仍为未知。</div>
<div id="summary"></div><div class="controls"><input id="query" aria-label="搜索名称或来源编号" placeholder="名称或精确来源编号"><select id="source" aria-label="来源"><option value="">全部来源</option></select><button id="prev">上一页</button><button id="next">下一页</button><span id="page"></span></div>
<div class="layout"><section class="panel"><h2>来源记录</h2><div id="list"></div></section><section class="panel" id="detail"><h2>选择左侧记录</h2><p>显示证据与字段缺口，不把相同名称合并为物种。</p></section></div></main>
<script type="application/json" id="data">__DATA__</script>
<script>
"use strict";
const d=JSON.parse(document.getElementById("data").textContent);
const el=id=>document.getElementById(id), pageSize=40;
let page=0, matches=[];
function make(tag,text,parent){const n=document.createElement(tag);n.textContent=text;parent.appendChild(n);return n;}
function json(parent,title,value){if(value===undefined||value===null)return;make("h3",title,parent);make("pre",JSON.stringify(value,null,2),parent);}
function label(r){return r.labels.join(" / ")||"（无名称，保留来源位置）";}
for(const [k,v] of Object.entries(d.summary.by_source)){const o=make("option",k+" · "+v,el("source"));o.value=k;}
el("summary").textContent=d.summary.source_record_occurrences+" 个来源位置 · "+d.summary.literal_labels+" 个不同字面 · 官服正式物种数未知";
function show(r){
 const p=el("detail");p.replaceChildren();make("h2",label(r),p);
 make("p","来源："+r.source+" ｜ "+r.role,p);
 json(p,"来源定位与编号",{pointer:r.pointer,source_keys:r.source_keys,source_file:d.sources[r.source]});
 make("h3","正式字段验收（非本页已完成项）",p);
 const u=make("ul","",p);for(const field of d.fields)make("li",field+"：参见下方来源数据；缺同部署原证不得晋升为正式字段",u);
 if(r.source==="tw75"&&r.detail){
  const v=r.detail;
  json(p,"来源属性（标称7.5模板，非正式官服数值）",v.elements);
  json(p,"条件一级面板范围（非原服实值）",v.conditional_lv1_panel);
  json(p,"条件每级内部增量（非原服成长算法）",v.conditional_per_level_internal);
  json(p,"配置技能槽（非官服出生技能）",v.skill_slots);
  json(p,"保存档取得／地图配置（非正式抓捕证明）",v.saved_mixed25_acquisition);
 }
 if(r.source==="tw10"&&r.detail){
  const q=d.profiles[r.detail.pet_id], f=q.profile;
  json(p,"原零售档案编号与来源",{id:f.profile_id,version:f.version_scope,path:q.path,git_blob:q.git_blob,historical_audit_git_blob:q.historical_audit_git_blob});
  json(p,"名称、系列与官服身份",{names:f.names,family:f.encyclopedia.category_or_family,identity:f.actual_official_pet_identity});
  json(p,"属性与一级初值范围（null = 未证）",f.combat_stats);
  json(p,"成长与算法（null = 未证）",f.growth);
  json(p,"原生技能（null = 未证）",f.skills);
  json(p,"捕捉和其他取得（null = 未证）",f.acquisition);
  json(p,"图鉴、头像及动作原证索引",{encyclopedia:f.encyclopedia,appearance:f.appearance});
  json(p,"融合／进化／骑乘",f.pet_systems);
  json(p,"私人观察凭证（本页不含原图）",f.provenance);
  json(p,"独立同期及后期字段参考，不回填官方值",r.detail.field_reference);
  json(p,"仍需证据",f.next_evidence_gap);
 }
 json(p,"现存来源字段和视觉证据索引",r.detail);
 json(p,"关联来源及资格（本地仓库路径可追溯）",r.linked_records.map(x=>({source:x.source,pointer:x.pointer,qualification:x.qualification,file:d.sources[x.source]})));
}
function render(){
 const q=el("query").value.trim().toLocaleLowerCase(), src=el("source").value;
 matches=d.rows.filter(r=>(!src||r.source===src)&&(!q||r.labels.some(n=>n.toLocaleLowerCase().includes(q))||r.source_keys.some(n=>n.toLocaleLowerCase()===q)));
 const pages=Math.max(1,Math.ceil(matches.length/pageSize));page=Math.min(Math.max(page,0),pages-1);
 el("page").textContent=matches.length+" 条 · "+(page+1)+"/"+pages;
 el("prev").disabled=page===0;el("next").disabled=page===pages-1;
 const list=el("list");list.replaceChildren();
 for(const r of matches.slice(page*pageSize,(page+1)*pageSize)){const b=make("button",label(r)+" ｜ "+r.source,list);b.type="button";b.onclick=()=>show(r);}
}
el("query").oninput=el("source").onchange=()=>{page=0;render();};
el("prev").onclick=()=>{page--;render();};el("next").onclick=()=>{page++;render();};render();
</script></html>
"""

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, required=True)
    args=p.parse_args()
    data=payload()
    args.output.write_text(PAGE.replace("__DATA__", safe_json(data), 1), encoding="utf-8")
    print(json.dumps(data["summary"], ensure_ascii=False))

if __name__=="__main__":
    main()
