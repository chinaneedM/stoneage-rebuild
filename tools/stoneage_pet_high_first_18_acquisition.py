"""Replay PET18 selected acquisition witnesses; no official deployment claims."""
import json
from pathlib import Path
import sys
from tools.stoneage_pet_high_first_18_map_headers import ROOT, blob
from tools.stoneage_pet_high_first_17_comparison import index, n, level, is1

def main(source):
    r=json.loads((ROOT/"research/pets/PET-HIGH-FIRST-18-STARTER-AND-CAPTURE-WITNESSES-R1.json").read_bytes())
    for k in ("official_deployment_verified","official_acquisition_verified","official_birth_skills_verified","source_independence_established"):
        assert r[k] is False
    assert r["original_capture_probability"] is None
    for p,sha in r["derived_input_blobs"].items():
        assert blob((ROOT/p).read_bytes())==sha
    for p,sha in r["comparison_source_blobs"].items():
        assert blob((source/p).read_bytes())==sha
    def load(p,width):
        rows=[line.strip().split(b",") for line in (source/p).read_bytes().splitlines() if line.strip() and not line.lstrip().startswith(b"#")]
        assert all(len(x)==width for x in rows)
        return [[v.strip() for v in x] for x in rows]
    e,g,c,b=[load(p,w) for p,w in [("gmsv/data/enemy1.txt",34),("gmsv/data/group1.txt",24),("gmsv/data/encount.txt",33),("gmsv/data/enemybase1.txt",56)]]
    ei,gi,bi=index(e,3),index(g,1),index(b,6)
    master=json.loads((ROOT/"research/pets/PET-HIGH-FIRST-15-TW75-MASTER-FIELD-CATALOG-R1.json").read_bytes())["pet_flag_1_field_projections"]
    growth=json.loads((ROOT/"research/pets/PET-HIGH-FIRST-16-TW75-CONDITIONAL-BIRTH-GROWTH-R1.json").read_bytes())["rows"]
    pet17=json.loads((ROOT/"research/pets/PET-HIGH-FIRST-17-COMPARISON-SKILL-ENCOUNTER-R1.json").read_bytes())["rows"]
    by_id={x["template_id"]:x for x in master}
    growth_by_id={x["template_id"]:x for x in growth}
    maps={x["floor"]:x for x in json.loads((ROOT/"research/pets/PET-HIGH-FIRST-18-COMPARISON-MAP-HEADERS-R1.json").read_bytes())["rows"]}
    def resolved(f):
        return maps[f]["status"] in ("UNIQUE_HEADER","MULTIPLE_FILES_SAME_HEADER_FIELDS")
    def name(f):
        return maps[f]["candidates"][0]["names"]["gb18030"] if resolved(f) else None
    setup=[x.strip() for x in (source/"gmsv/setup.cf").read_bytes().splitlines()]
    assert all(("PET%d="%i).encode() in setup for i in range(1,5))
    assert b"PETLV=1" in setup
    char=(source/"gmsv/src/char/char.c").read_bytes()
    config=(source/"gmsv/src/configfile.c").read_bytes()
    assert b"#ifdef _NEW_PLAYER_CF" in char and b"if(getNewplayergivepet(0)==-1)" in char
    assert all(("setNewplayergivepet(0,%d)"%i).encode() in char for i in range(1,5))
    assert b"ENEMY_getEnemyArrayFromId( getNewplayergivepet(petNum))" in char
    assert b"config.newplayergivepet[index] = interval;" in config
    for x in r["starters"]:
        expected=[]
        for eid in (x["default_enemy"],x["choice_enemy"]):
            assert len(ei[eid])==1
            v=ei[eid][0]; t=by_id[n(v[4])]
            assert t["name"]==x["name"] and t["comparison_status"]=="EXACT_NONNAME_50_FIELD_TAIL"
            expected.append(dict(enemy_id=eid,template_id=t["template_id"],graphic=t["graphic"],
              instance_level=list(map(n,v[5:7])),instance_petflag=n(v[13]),raw_elements=t["elements"],
              skill_slots=t["skill_slots"],conditional_level1_panel=growth_by_id[t["template_id"]]["level1_unmodified_work_panel_marginal_ranges"]))
        assert expected==x["templates"]
        assert x["historical_element_agrees"]==(x["historical_elements"]==expected[0]["raw_elements"])
    for x in r["coordinate_cases"]:
        tids=[t["template_id"] for t in master if t["name"]==x["name"]]
        assert tids==x["template_ids"]
        out=[];count=0
        for ordinal,row in enumerate(c,1):
            floor=n(row[1])
            if floor not in x["comparison_floor_candidates"]:continue
            for gid,gw in zip(map(n,row[10:20]),map(n,row[20:30])):
                if gid<0 or gw<=0 or gid not in gi:continue
                gr=gi[gid][0]
                er=[eid for eid in map(n,gr[4:14]) if eid>=0 and eid in ei]
                if not er or len(set(er))!=len(er):continue
                for eid,ew in zip(map(n,gr[4:14]),map(n,gr[14:24])):
                    if eid not in ei or ew<=0:continue
                    inst=ei[eid][0];tid=n(inst[4])
                    if tid not in tids or len(bi.get(tid,[]))!=1 or n(inst[13])!=1 or not is1(level(inst)):continue
                    count+=1
                    rect=list(map(n,row[2:6])); points=[p for p in x["coordinates"] if min(rect[0],rect[2])<=p[0]<=max(rect[0],rect[2]) and min(rect[1],rect[3])<=p[1]<=max(rect[1],rect[3])]
                    if points:out.append(dict(template_id=tid,comparison_status=by_id[tid]["comparison_status"],graphic=by_id[tid]["graphic"],floor=floor,map_name_gb18030=name(floor),rect=rect,enemy=eid,group=gid,encounter_ordinal=ordinal,levels=level(inst),matched_points=points))
        assert count==x["level1_route_count"] and out==x["matches"]
    s=r["summary"]
    assert s["target_floors"]==len(maps)==349
    assert s["unambiguous_header_floors"]==sum(resolved(f) for f in maps)==338
    assert s["conflicting_header_floors"]==sum(x["status"]=="CONFLICTING_HEADER_FIELDS" for x in maps.values())
    assert s["missing_header_floors"]==sum(x["status"]=="MISSING" for x in maps.values())
    assert s["all_templates_with_unambiguous_floor"]==sum(any(resolved(f) for f in x["comparison_floor_ids"]) for x in pet17)
    assert s["exact_templates_with_unambiguous_floor"]==sum(x["comparison_status"]=="EXACT_NONNAME_50_FIELD_TAIL" and any(resolved(f) for f in x["comparison_floor_ids"]) for x in pet17)
    assert s["selected_coordinate_pet_cases"]==len(r["coordinate_cases"])==10
    assert s["coordinate_intersection_cases"]==sum(bool(x["matches"]) for x in r["coordinate_cases"])==10
    assert s["exact_tail_cases"]==sum(any(y["comparison_status"]=="EXACT_NONNAME_50_FIELD_TAIL" for y in x["matches"]) for x in r["coordinate_cases"])==9
    assert s["starter_cases"]==len(r["starters"])==4
    assert s["starter_element_agreement"]==sum(x["historical_element_agrees"] for x in r["starters"])==3
    print("PET18 starter and coordinate replay:",json.dumps(s,ensure_ascii=False,sort_keys=True))
    print("Historical deployment, issuance and birth skills remain unverified.")

if __name__=="__main__":
    main(Path(sys.argv[1]))
