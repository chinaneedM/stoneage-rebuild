"""Replay late PC source object-role crosswalk; never infer official live pet identity."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_bytes())
def blob(raw):return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def main():
    d=read("research/pets/PET-HIGH-FIRST-28-29-2014-2018-OBJECT-ROLE-CROSSWALK-R1.json")
    for p,s in d["source_pins_git_blob"].items():assert blob((ROOT/p).read_bytes())==s,(p,s)
    receipts={int(k):read(p) for k,p in d["receipt_paths"].items()}
    m,g,n,c=[read(p) for p in d["resource_paths"]]
    mp=d["character_map"];inv={v:k for k,v in mp.items()}
    def spell(x):return list(dict.fromkeys([x,"".join(mp.get(ch,ch) for ch in x),"".join(inv.get(ch,ch) for ch in x)]))
    def lookup(ns):
        return dict(
            tw75=[{k:y[k] for k in ("name","template_id","graphic","row_sha256","elements","skill_slots")} for y in m["pet_flag_1_field_projections"] if y["name"] in ns],
            tw85_album=[dict(program=p,slot=y["slot"],name=y["original_name_cp950"],portrait_alias=y["source_portrait_alias"],row_sha256=y["original_row_sha256"]) for p,z in g["programs"].items() for y in z["source_records"] if y["original_name_cp950"] in ns],
            tw85_spr=[dict(graphic=y["tw85_original_spr_number"],program_names={k:z["original_name_cp950"] for k,z in y["program_routes"].items()},conflict=y["graphic_has_conflicting_names_across_installer_programs"]) for y in n["records"] if any(z["original_name_cp950"] in ns for z in y["program_routes"].values())],
            cn50=[dict(name=y["compiled_name"],ordinal=y["ordinal"],graphics=[z["spr_group"] for z in y["spr_groups"]],portrait_sha256=y["portrait_lookup_rd_sha256"]) for y in c["records"] if y["compiled_name"] in ns])
    expected=[]
    for gi,z in enumerate(d["groups"]):
        node=receipts[z["receipt"]]
        for k in z["pointer"]:node=node[k]
        serialized=json.dumps(node,ensure_ascii=False)
        for i,label in enumerate(z["labels"]):
            name,role=label[:2];rel=label[2] if len(label)==3 else None
            assert name in serialized,(z["receipt"],z["pointer"],name)
            eligible=role in ("PET_NAME_CANDIDATE","ENCOUNTER_LABEL","PET_CONTEXT_ALIAS")
            expected.append(dict(group=gi,position=i,year=z["year"],receipt=z["receipt"],lane=z["lane"],name=name,role=role,spellings=spell(name) if eligible else [],direct=lookup(spell(name)) if eligible else None,related_label=rel,related_candidates=lookup(spell(rel)) if rel else None,official_native_pet_id=None,first_release_date=None,official_same_deployment_verified=False,actual_grant_verified=False))
    assert d["rows"]==expected
    def hit(q):return q is not None and any(q.values())
    def stats(rs):
        return dict(source_positions=len(rs),pet_name_candidate_positions=sum(q["role"]=="PET_NAME_CANDIDATE" for q in rs),nonpet_items=sum(q["role"]=="ITEM" for q in rs),encounter_labels=sum(q["role"]=="ENCOUNTER_LABEL" for q in rs),lookup_eligible=sum(q["direct"] is not None for q in rs),direct_name_links=sum(hit(q["direct"]) for q in rs),related_only=sum(not hit(q["direct"]) and hit(q["related_candidates"]) for q in rs),unmatched_eligible=sum(q["direct"] is not None and not hit(q["direct"]) and not hit(q["related_candidates"]) for q in rs))
    assert d["summary"]["all"]==stats(expected)
    assert d["summary"]["by_year"]=={str(y):stats([q for q in expected if q["year"]==y]) for y in range(2014,2019)}
    assert all(q["direct"] is None for q in expected if q["role"]=="ITEM")
    assert sum(q["name"]=="藍虎" for q in expected)==2
    assert all(q["lane"]=="TW_TAOZHU_DADI" for q in expected if q["name"]=="藍虎")
    h=receipts[104]["sources"][0]
    assert sum(k=="NAMED_PET_REWARD_CANDIDATE" for k in h["announced_reward_kinds"])==5
    assert not receipts[102]["new_evidence"][0]["box_opening_pet_contents_verified"]
    assert not receipts[112]["announced_second_wave"]["new_user_cohort"]["native_auto_grant_verified"]
    assert d["official_species_count"] is None and not d["original_assets_published"] and d["summary"]["new_original_client_bytes"]==0
    print("PET28-29: source label positions, role exclusions, name crosswalk and realm boundaries replayed",len(expected))
if __name__=="__main__":main()
