"""Replay bounded PET19B derived source comparisons, not official capture evidence."""
import hashlib,json
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
def blob(b): return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def read(p): return json.loads((ROOT/p).read_bytes())
def main():
    d=read("research/pets/PET-HIGH-FIRST-19B-GRAPHIC-AND-COORDINATE-R1.json")
    for p,s in d["source_pins_git_blob"].items(): assert blob((ROOT/p).read_bytes())==s
    m=read("research/pets/PET-HIGH-FIRST-15-TW75-MASTER-FIELD-CATALOG-R1.json")["pet_flag_1_field_projections"]
    v=read("research/pets/PET-HIGH-FIRST-TW85-VISUAL-ACTION-REFERENCES-R1.json")["records"]
    e={x["template_id"]:x for x in read("research/pets/PET-HIGH-FIRST-17-COMPARISON-SKILL-ENCOUNTER-R1.json")["rows"]}
    maps={x["floor"]:x for x in read("research/pets/PET-HIGH-FIRST-18-COMPARISON-MAP-HEADERS-R1.json")["rows"]}
    assert len(m)==467
    assert dict(Counter(x["client_join_status"] for x in m))==d["summary"]["join_status_counts"]
    byid={x["template_id"]:x for x in m}
    expected=[]
    for x in m:
        if x["client_join_status"]!="TW85_NATIVE_GRAPHIC_OTHER_NAME":continue
        gs=[y["tw85_original_spr_no_not_official_pet_id"] for y in v if any(z.get("original_name_cp950")==x["name"] for z in y["original_native_program_routes"].values())]
        ds=[g-x["graphic"] for g in gs]
        expected.append(dict(template_id=x["template_id"],name=x["name"],master_graphic=x["graphic"],native_names=x["tw85_native_graphic_names"],independent_name_groups=gs,nearest_deltas=[q for q in ds if abs(q)==min(map(abs,ds))],comparison_status=x["comparison_status"]))
    assert expected==d["tw85_conflicts"]
    assert sum(x["nearest_deltas"]==[1] for x in expected)==10
    assert sum(x["nearest_deltas"]==[-1] for x in expected)==4
    assert [dict(template_id=x["template_id"],name=x["name"],master_graphic=x["graphic"],early_names=x["tw10_names_at_graphic"]) for x in m if x["client_join_status"]=="TW10_GRAPHIC_OTHER_NAME"]==d["tw10_conflicts"]
    assert [dict(group=x["tw85_original_spr_no_not_official_pet_id"],names={k:y.get("original_name_cp950",y.get("status")) for k,y in x["original_native_program_routes"].items()}) for x in v if 101865<=x["tw85_original_spr_no_not_official_pet_id"]<=101883]==d["tw85_local_window"]
    assert len(d["coordinate_cases"])==26
    assert len({x["source_pos"] for x in d["coordinate_cases"]})==26
    for x in d["coordinate_cases"]:
        t=byid[x["template_id"]];assert t["name"]==x["master_name"] and t["comparison_status"]==x["comparison_status"]
        route=e[x["template_id"]]["first_lv1_route"]
        assert route==x["representative_lv1_route"]
        p=maps[route["floor"]];assert p["status"] in ("UNIQUE_HEADER","MULTIPLE_FILES_SAME_HEADER_FIELDS")
        assert p["candidates"][0]["names"]["gb18030"]==x["comparison_map_name"]
        a,b,c,f=route["rect"]
        assert [pt for pt in x["source_points"] if min(a,c)<=pt[0]<=max(a,c) and min(b,f)<=pt[1]<=max(b,f)]==x["matched_points"]
        assert x["matched_points"]
    assert sum(x["source_cn_appearance_explicitly_unconfirmed"] for x in d["coordinate_cases"])==2
    assert sum(x["name_variant_candidate_only"] for x in d["coordinate_cases"])==1
    assert all(d[k] is False for k in ("official_deployment_verified","official_capture_verified","original_graphic_ids_changed"))
    assert d["official_species_count"] is None
    print("PET19B: 467 rows, 14 late graphic conflicts, 26 representative coordinate intersections; official capture unverified")
if __name__=="__main__": main()
