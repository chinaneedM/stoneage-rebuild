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


def late_profiles(rows, data):
    """Project existing source-qualified fields, never consolidate by species name."""
    a = data["hf45"]["projection"]
    assert a["route_columns"] == ["area_id","area_group_slot","group_id","group_enemy_slot",
                                  "enemy_instance_id","area_group_weight","group_enemy_weight"]
    areas = {v["id"]: v for v in a["area_metadata"]}
    instances = {v["id"]: v for v in a["instance_metadata"]}
    routes = {v["template_id"]: v for v in a["mixed25_template_routes"]}
    floor_names = {v["floor_id"]: v["later_recovered_name"] for v in data["hf45_floor"]["rows"]}
    out = {}
    for row in rows:
        if row["source"] != "tw75":
            continue
        raw = lookup.resolve(data, row["source"], row["pointer"])
        i = row["pointer"][-1]
        k = raw["template_id"]
        v = row["detail"]
        selected = data["hf76"]["rows"][i]
        birth = data["tw75_birth"]["rows"][selected["conditional_range_index"]]
        ac = a["claimed_tw75_rows"][i]
        assert selected["position"] == i == ac["tw75_row_index"]
        assert selected["row_sha256"] == birth["source_row_sha256"] == ac["tw75_row_sha256"] == raw["row_sha256"]
        assert selected["template_id"] == birth["template_id"] == ac["template_id"] == k
        assert v["template_id"] == k and raw["pet_flag"] == 1
        assert selected["selected_table_grade"] == ac["match_status"]
        source_id = f"TW75-TEMPLATE-{k}"
        assert source_id not in out
        exact = ac["match_status"] == "EXACT_SHARED_TEMPLATE_ROW"
        rr = []
        if ac["positive_route_count"]:
            assert exact
            route = routes[k]
            assert route["source_template_row_sha256"] == raw["row_sha256"]
            for aid, agslot, gid, geslot, eid, aw, ew in route["routes"]:
                area, instance = areas[aid], instances[eid]
                assert instance["template_id"] == k and aw > 0 and ew > 0
                floor = area["floor"]
                name = floor_names.get(floor)
                rr.append(dict(floor_id=floor, map_name_candidate=name["display_name_candidate"] if name else None,
                               rectangle=area["raw_rectangle"], inverted_rectangle=area["inverted_rectangle"],
                               level=instance["level"], instance_pet_flag=instance["pet_flag"],
                               area_id=aid, group_id=gid, instance_id=eid, area_group_slot=agslot, group_enemy_slot=geslot,
                               area_group_weight=aw, group_enemy_weight=ew,
                               raw_rate_fields=area["raw_rate_fields"], raw_event_fields=area["raw_event_fields"],
                               area_source_line=area["source_line"], instance_source_line=instance["source_line"]))
        assert len(rr) == ac["positive_route_count"]
        assert sum(r["instance_pet_flag"] == 1 for r in rr) == ac["double_pet_flag_route_count"]
        assert sum(r["instance_pet_flag"] == 1 and r["level"][0] <= 1 <= r["level"][1] for r in rr) == ac["lv1_double_flag_route_count"]
        skills = v["saved_selected_master_fields"]["configured_skill_slots"]
        assert len(skills) == len(selected["configured_skill_slots"])
        assert exact or (not rr and not skills and selected["saved_reward_instance_id"] is None)
        # These are candidate records, not canonical official PET numbers.
        row["source_keys"].append(source_id)
        out[source_id] = dict(
            source_observation_id=source_id, original_name=raw["name"], template_id=k, source_position=i,
            physical_line=raw["physical_line"], row_sha256=raw["row_sha256"], graphic=raw["graphic"],
            carrier="CLAIMED_TW75_UNAUTHENTICATED_PC_MASTER", official_identity_verified=False,
            formal_fields={"official_pet_id":None,"official_release_date":None,"official_level1_ranges":None,
                           "official_growth_ranges":None,"official_total_panel_growth":None,
                           "official_innate_skills":None,"official_learnable_skills":None,
                           "official_capture":None,"official_other_acquisition":None,
                           "official_encyclopedia":None,"official_family":None},
            comparison_grade=ac["match_status"], selected_row_sha256=selected["selected_row_sha256"],
            selected_field_conflicts=selected["selected_fields_differing_from_claim"],
            claimed_elements_raw=raw["elements"], claimed_internal_base=raw["base"],
            claimed_initnum=raw["initnum"], claimed_lvup_literal=raw["lvup_literal"],
            model_rank=birth["rank"], conditional_internal_level1=birth["level1_internal_marginal_ranges"],
            conditional_panel_level1=birth["level1_unmodified_work_panel_marginal_ranges"],
            conditional_internal_increment=birth["per_level_internal_increment_marginal_ranges"],
            conditional_panel_total_growth=None, conditional_model_sources=data["tw75_birth"]["input_git_blobs"],
            claimed_skill_slots=raw["skill_slots"], claimed_skill_slot_capacity=raw["skill_slot_capacity"],
            saved_named_skill_slots=skills, saved_reward_instance_id=selected["saved_reward_instance_id"],
            positive_routes=rr, acquisition_gap=v["saved_mixed25_acquisition"]["gap_classification"],
            dated_family_references=v.get("dated_family_references", []),
            visual_reference_grade=v.get("visual_reference", {}).get("qualification"),
            original_pixels_included=False, official_deployment_verified=False)
    return out

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
    late = late_profiles(rows, data)
    return {
        "late_profiles": late,
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
.data-table{border-collapse:collapse;width:100%;font-size:13px;margin:6px 0 14px}.data-table th,.data-table td{border:1px solid #dedfd9;text-align:left;padding:5px 7px;overflow-wrap:anywhere}.data-table th{background:#eeefe9}.panel{overflow-x:auto}</style><header><h1>石器时代 · 宠物来源档案</h1>离线研究入口 R1 ｜ 原版经典 PC ｜ 来源位置互相独立</header>
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

function table(parent,title,headers,rows){
 make("h3",title,parent);if(!rows.length){make("p","本来源无合格记录（不等于历史不存在）",parent);return;}
 const t=make("table","",parent);t.className="data-table";
 const head=make("tr","",make("thead","",t));for(const h of headers)make("th",h,head);
 const body=make("tbody","",t);for(const row of rows){const tr=make("tr","",body);for(const v of row)make("td",v==null?"未证":String(v),tr);}
}
function showLate(p,r){
 const v=d.late_profiles["TW75-TEMPLATE-"+r.detail.template_id];
 make("h3","独立高版本来源档案 · "+v.source_observation_id,p);
 make("p","标称台湾7.5的保存主表，版本归属和官服投放未认证。相同名称模板保持分开。",p);
 table(p,"原始主表字段",["字段","原值"],[
 ["名称",v.original_name],["模板号",v.template_id],["物理行",v.physical_line],["原图号",v.graphic],
 ["属性原四槽（未改写）",v.claimed_elements_raw.join(" / ")],["内部基础四槽",v.claimed_internal_base.join(" / ")],
 ["initnum",v.claimed_initnum],["lvup原字面",v.claimed_lvup_literal],["对照主档资格",v.comparison_grade]]);
 const fmt=a=>a.join("–");
 table(p,"条件一级面板范围（非原服实值）",["血量","攻击","防御","敏捷"],[v.conditional_panel_level1.map(fmt)]);
 table(p,"条件每级内部增量（非面板成长率）",["体力","力量","耐力","敏捷"],[v.conditional_internal_increment.map(fmt)]);
 make("p","条件模型以该模板和后期PC算法计算各项边际范围；各项最大值不能直接相加为总成长，原服成长率未证。",p);
 table(p,"配置技能槽（保存档同指纹具名定义，不是出生技能）",["槽","ID","名称","同档学习配置"],v.saved_named_skill_slots.map(s=>[s.slot_index,s.skill_id,s.name,s.saved_skillshop_reference?.qualification||"未证"]));
 make("p","标称主表原技能槽："+v.claimed_skill_slots.map(x=>x==null?"空":x).join(" / ")+"；实际出生、可学资格仍未证。",p);
 table(p,"保存档取得／地图配置（非正式抓捕证明）",["地图号","地图名候选","坐标原范围","等级","实例","宠标记","权重原值"],v.positive_routes.map(x=>[x.floor_id,x.map_name_candidate,x.rectangle.join(", ")+(x.inverted_rectangle?"（反向）":""),x.level.join("–"),x.instance_id,x.instance_pet_flag,x.area_group_weight+" / "+x.group_enemy_weight]));
 make("p","保存档奖励实例："+(v.saved_reward_instance_id==null?"未证":v.saved_reward_instance_id)+"；上述遇敌和奖励配置不等于官服实际取得。",p);
 if(v.dated_family_references.length)table(p,"同期宠物系别参考",["系别","日期","相容状态"],v.dated_family_references.map(x=>[x.family,x.source_date,x.element_status]));
 json(p,"取得缺件分类",v.acquisition_gap);
 json(p,"正式原服字段（未证为 null）",v.formal_fields);
 json(p,"原始行及模型来源",{row_sha256:v.row_sha256,selected_row_sha256:v.selected_row_sha256,selected_field_conflicts:v.selected_field_conflicts,model_sources:v.conditional_model_sources,visual_reference_grade:v.visual_reference_grade,original_pixels_included:v.original_pixels_included});
}

function show(r){
 const p=el("detail");p.replaceChildren();make("h2",label(r),p);
 make("p","来源："+r.source+" ｜ "+r.role,p);
 json(p,"来源定位与编号",{pointer:r.pointer,source_keys:r.source_keys,source_file:d.sources[r.source]});
 make("h3","正式字段验收（非本页已完成项）",p);
 const u=make("ul","",p);for(const field of d.fields)make("li",field+"：参见下方来源数据；缺同部署原证不得晋升为正式字段",u);
 if(r.source==="tw75"&&r.detail)showLate(p,r);
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
