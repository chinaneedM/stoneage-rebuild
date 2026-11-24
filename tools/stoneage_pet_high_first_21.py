"""Replay exact name search in pinned PC source-derived indexes."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_bytes())
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def main():
    d=read("research/pets/PET-HIGH-FIRST-21-LATE-YEAR-BEAST-SOURCE-R1.json")
    for p,s in d["source_pins_git_blob"].items():assert blob((ROOT/p).read_bytes())==s
    m=read("research/pets/PET-HIGH-FIRST-15-TW75-MASTER-FIELD-CATALOG-R1.json")["pet_flag_1_field_projections"]
    n=read("research/pets/PET-HIGH-FIRST-TW85-NATIVE-SPR-ALBUM-R1.json")["records"]
    g=read("research/pets/PET-HIGH-FIRST-TW85-ORIGINAL-PE-ALBUM-GRID-R1.json")["programs"]
    rows=d["rows"];assert len(rows)==8 and len({x["website_record_id"] for x in rows})==8
    assert [x["claimed_year"] for x in rows]==[2007]*4+[2008]*4
    for x in rows:
        names={x["recollection_name"],x["catalogue_name"]}
        found=dict(master=[y["template_id"] for y in m if y["name"] in names],grid=[dict(program=p,slot=y["slot"],name=y["original_name_cp950"]) for p,z in g.items() for y in z["source_records"] if y["original_name_cp950"] in names],native=[dict(program=p,graphic=y["tw85_original_spr_number"],name=z["original_name_cp950"]) for y in n for p,z in y["program_routes"].items() if z.get("original_name_cp950") in names])
        assert found==x["source_matches"] and not any(found.values())
        assert x["element_conflict"]==(x["recollection_elements"]!=x["catalogue_elements"])
        assert x["name_variation"]==(len(names)==2)
        assert sum(x["recollection_elements"])==sum(x["catalogue_elements"])==10
        assert all(len(a)==2 and a[0]<=a[1] for a in x["catalogue_birth_ranges"]+x["catalogue_growth_ranges"])
        assert not x["official_release_verified"] and not x["official_historical_birth_growth_skill_verified"] and x["official_original_graphic_id"] is None
    assert sum(x["element_conflict"] for x in rows)==8 and sum(x["name_variation"] for x in rows)==1
    assert d["official_species_count"] is None and not d["original_assets_published"]
    print("PET21: eight late year-beast candidates; exact original name joins absent; historical and later fields remain separate")
if __name__=="__main__":main()
