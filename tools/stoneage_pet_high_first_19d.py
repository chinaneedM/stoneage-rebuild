"""Replay PET19D derived joins and source-position coverage."""
import hashlib,json
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_bytes())
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def main():
    d=read("research/pets/PET-HIGH-FIRST-19D-2001-DIRECTORY-CLOSURE-R1.json")
    for p,s in d["source_pins_git_blob"].items():assert blob((ROOT/p).read_bytes())==s
    m=read("research/pets/PET-HIGH-FIRST-15-TW75-MASTER-FIELD-CATALOG-R1.json")["pet_flag_1_field_projections"]
    e={x["template_id"]:x for x in read("research/pets/PET-HIGH-FIRST-17-COMPARISON-SKILL-ENCOUNTER-R1.json")["rows"]}
    maps={x["floor"]:x for x in read("research/pets/PET-HIGH-FIRST-18-COMPARISON-MAP-HEADERS-R1.json")["rows"]}
    o=read("research/pets/PET-HIGH-FIRST-18-STARTER-AND-CAPTURE-WITNESSES-R1.json");b=read("research/pets/PET-HIGH-FIRST-19B-GRAPHIC-AND-COORDINATE-R1.json");c=read("research/pets/PET-HIGH-FIRST-19C-QUEST-AND-GIFT-WITNESSES-R1.json")
    prior={x["source_pos"] for x in o["starters"]+o["coordinate_cases"]+b["coordinate_cases"]}|{x["pos"] for x in c["rows"]}
    assert len(prior)==88
    assert [x["pos"] for x in d["rows"]]==sorted(set(range(1,125))-prior)
    assert len(d["rows"])==36
    for x in d["rows"]:
        expected=[]
        for t in m:
            if t["name"]!=x["master_name"]:continue
            route=e[t["template_id"]]["first_lv1_route"]
            p=maps.get(route["floor"]) if route else None
            pts=[]
            if route:
                a,b,c,f=route["rect"]
                pts=[q for q in x["points"] if min(a,c)<=q[0]<=max(a,c) and min(b,f)<=q[1]<=max(b,f)]
            expected.append(dict(template_id=t["template_id"],graphic=t["graphic"],join=t["client_join_status"],comparison_status=t["comparison_status"],representative_lv1_route=route,map_status=p["status"] if p else None,map_names=[y["names"]["gb18030"] for y in p["candidates"]] if p else [],matched_points=pts))
        assert expected==x["candidates"]
        qualified=any(y["matched_points"] and y["map_status"] in ("UNIQUE_HEADER","MULTIPLE_FILES_SAME_HEADER_FIELDS") for y in expected)
        any_match=any(y["matched_points"] for y in expected)
        status=("PLACE_ONLY_NO_COORDINATES" if not x["points"] else ("COORDINATE_INTERSECTION_NAME_VARIANT_ONLY" if x["name_variant_only"] else "COORDINATE_INTERSECTION_UNAMBIGUOUS_HEADER") if qualified else "COORDINATE_INTERSECTION_MAP_HEADER_UNRESOLVED" if any_match else "NO_INTERSECTION_IN_REPRESENTATIVE_ROUTE")
        assert x["status"]==status and x["official_capture_verified"] is False
    assert dict(Counter(x["status"] for x in d["rows"]))==d["summary"]["status_counts"]
    assert d["summary"]["covered"]==124 and d["official_species_count"] is None and d["official_capture_verified"] is False
    print("PET19D: 124/124 source positions indexed; official capture remains unverified")
if __name__=="__main__":main()
