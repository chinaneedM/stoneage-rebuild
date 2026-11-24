"""Replay source positions, named source references and conditional field links. Historical web claims are separately attributed, not runtime proof."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_bytes())
def blob(raw):return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def main():
    d=read("research/pets/PET-HIGH-FIRST-26-27-2012-2013-NAMED-ACQUISITION-CROSSWALK-R1.json")
    for p,s in d["source_pins_git_blob"].items():assert blob((ROOT/p).read_bytes())==s
    p88,p89,p91,p92,p93,m,g,n,c,b,e,mp=[read(p) for p in d["source_pins_git_blob"]]
    def spell(x):return list(dict.fromkeys([x,"".join(d["character_map"].get(ch,ch) for ch in x)]))
    def lookup(ns):
        master=[y for y in m["pet_flag_1_field_projections"] if y["name"] in ns]
        ids={y["template_id"] for y in master}
        encounters=[y for y in e["rows"] if y["template_id"] in ids]
        floors={f for y in encounters for f in y["comparison_floor_ids"]}
        return dict(
            claimed_tw75_templates=[{k:y[k] for k in ("name","template_id","graphic","physical_line","row_sha256","elements","skill_slots","skill_slot_capacity")} for y in master],
            tw85_album_slots=[dict(program=p,slot=y["slot"],name=y["original_name_cp950"],portrait_alias=y["source_portrait_alias"],row_sha256=y["original_row_sha256"]) for p,z in g["programs"].items() for y in z["source_records"] if y["original_name_cp950"] in ns],
            tw85_extra_spr=[dict(graphic=y["tw85_original_spr_number"],conflicting_names=y["graphic_has_conflicting_names_across_installer_programs"],program_names={p:z["original_name_cp950"] for p,z in y["program_routes"].items()},occurrences=y["source_spr_occurrences"]) for y in n["records"] if any(z["original_name_cp950"] in ns for z in y["program_routes"].values())],
            cn50_named_slots=[dict(name=y["compiled_name"],ordinal=y["ordinal"],portrait_rd_sha256=y["portrait_lookup_rd_sha256"],graphics=[z["spr_group"] for z in y["spr_groups"]]) for y in c["records"] if y["compiled_name"] in ns],
            conditional_tw75_ranges=[y for y in b["rows"] if y["template_id"] in ids],
            comparison_encounters=encounters,
            comparison_map_headers=[dict(floor=y["floor"],status=y["status"],header_candidates=[dict(path=z["path"],blob=z["blob"],name=z["names"]["gb18030"],header_sha256=z["header_sha256"]) for z in y["candidates"]]) for y in mp["rows"] if y["floor"] in floors])
    expect=[]
    expect.extend((2012,"PET88",x["source_id"],i,x["name"],x["source_context"],x["version_lane"]) for i,x in enumerate(p88["named_pet_source_mentions"]))
    expect.extend((2012,"PET89",x["source_id"],i,x["name"],x["claim_role"],"SOURCE_SPECIFIC") for i,x in enumerate(p89["named_pet_source_mentions"]))
    for x in p91["sources"]:
        if x["product_line"]=="ORIGINAL_PC":
            expect.extend((2013,"PET91",x["id"],i,name,"PUBLISHED_LABEL",x["version"]) for i,name in enumerate(x["pet_name_attestations"]))
    x,y=p93["sources"][:2]
    expect.extend((2013,"PET93",x["url"],i,name,"SNAKE_TASK_NAMED_LABEL_NOT_MAPPED_TO_FOUR_ELEMENTS","CN85_AND_CN25_SEPARATE") for i,name in enumerate(x["names"]))
    expect.extend((2013,"PET93",y["url"],i,name,"QUEST_INPUT","CN_UNRESOLVED") for i,name in enumerate(y["questInputPets"]))
    expect.extend((2013,"PET93",y["url"],i,name,"PROMISED_PET_REWARD","CN_UNRESOLVED") for i,name in enumerate(y["promisedPetRewards"]))
    manual=d["manual_web_claims"]
    gold2012=manual["gold2012"]["url"];gold2013=manual["gold2013"]["url"]
    expect.extend([(2012,"WEB_GOLD2012",gold2012,0,"斑尼迪克","TASK_ACQUISITION_DESCRIPTION","CN_UNRESOLVED"),(2012,"WEB_GOLD2012",gold2012,1,"朵拉比斯","RIDING_SHOWCASE","CN_UNRESOLVED"),(2012,"WEB_GOLD2012",gold2012,2,"金格萨贝鲁","TASK_ACQUISITION_DESCRIPTION","CN_UNRESOLVED"),(2013,"WEB_GOLD2013",gold2013,0,"金格萨贝鲁","EDITORIAL_BIRTH_RANGE_AND_SKILL_CLAIM","CN_UNRESOLVED")])
    rows=d["rows"]
    assert len(rows)==len(expect)
    for q,expected in zip(rows,expect):
        assert tuple(q[k] for k in ("year","receipt","source_id","position","name","role","version"))==expected
        if q["receipt"]=="PET89":
            prior=p89["named_pet_source_mentions"][q["position"]]
            assert q["reported_location"]==prior["reported_location"] and q["reported_element"]==prior["source_element_summary"]
        assert q["spellings"]==spell(q["name"])
        assert q["direct"]==lookup(spell(q["name"]))
        rel=d["related_labels"].get(q["name"])
        assert q["related_label"]==rel and q["related_candidates"]==(lookup(spell(rel)) if rel else None)
        assert not q["original_same_deployment_verified"] and not q["actual_grant_or_capture_verified"]
        assert all(q[k] is None for k in ("official_native_pet_id","official_growth","official_skill_ids","first_release_date"))
    def hit(q):return any(q[k] for k in ("claimed_tw75_templates","tw85_album_slots","tw85_extra_spr","cn50_named_slots"))
    def stats(rs):
        return dict(attestations=len(rs),distinct_labels=len({q["name"] for q in rs}),direct_name_matches=sum(bool(hit(q["direct"])) for q in rs),tw75_template_matches=sum(bool(q["direct"]["claimed_tw75_templates"]) for q in rs),tw85_album_matches=sum(bool(q["direct"]["tw85_album_slots"]) for q in rs),cn50_name_matches=sum(bool(q["direct"]["cn50_named_slots"]) for q in rs),related_label_only=sum(not hit(q["direct"]) and q["related_candidates"] is not None and bool(hit(q["related_candidates"])) for q in rs),unmatched=sum(not hit(q["direct"]) and not (q["related_candidates"] and hit(q["related_candidates"])) for q in rs))
    assert d["summary"]["year2012"]==stats([q for q in rows if q["year"]==2012])
    assert d["summary"]["year2013"]==stats([q for q in rows if q["year"]==2013])
    assert d["summary"]["all"]==stats(rows)
    assert manual["capture_article"]["claims"][0]["element"]==[0,0,100,0]
    assert manual["older_catalog"]["claims"][0]["element"]==[0,0,60,40]
    assert lookup(spell("呼拔拔"))["claimed_tw75_templates"][0]["elements"]==[0,0,60,40]
    assert manual["snake2013"]["named_labels"]==x["names"] and manual["snake2013"]["version_eligibility"]==x["versionEligibility"]
    assert manual["snake2013"]["element_to_name_assignment"] is None and not manual["snake2013"]["actual_grant_verified"]
    assert manual["gold2013"]["reported_birth_ranges"]==[[38,47],[8,10],[5,7],[6,9]]
    assert lookup(spell("金格萨贝鲁"))["conditional_tw75_ranges"][0]["level1_unmodified_work_panel_marginal_ranges"]==[[37,51],[8,11],[5,9],[6,10]]
    assert d["official_species_count"] is None and not d["original_assets_published"] and d["summary"]["new_original_client_bytes"]==0
    print("PET26-27: source positions, exact named links, conditional stat/map records and conflict guards replayed")
if __name__=="__main__":main()
