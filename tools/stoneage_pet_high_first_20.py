"""Replay source-bound named capsule projections; no historical issuance inference."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_bytes())
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def main():
    d=read("research/pets/PET-HIGH-FIRST-20-CAPSULE-AND-GALLERY-R1.json")
    for p,s in d["source_pins_git_blob"].items():assert blob((ROOT/p).read_bytes())==s
    m=read("research/pets/PET-HIGH-FIRST-15-TW75-MASTER-FIELD-CATALOG-R1.json")["pet_flag_1_field_projections"]
    n=read("research/pets/PET-HIGH-FIRST-TW85-NATIVE-SPR-ALBUM-R1.json")["records"]
    assert len(d["rows"])==7 and len({x["name"] for x in d["rows"]})==7
    fields=("template_id","graphic","base","elements","initnum","lvup_literal","skill_slots","comparison_status","client_join_status","row_sha256")
    for x in d["rows"]:
        assert x["master"]==[{k:y[k] for k in fields} for y in m if y["name"]==x["name"]]
        assert x["native"]==[dict(program=p,graphic=y["tw85_original_spr_number"],slot=z["local_album_slot"],portrait_alias=z["original_portrait_alias_u32"],row_sha256=z["original_album_row_sha256"]) for y in n for p,z in y["program_routes"].items() if z.get("original_name_cp950")==x["name"]]
        assert x["official_award_verified"] is False
    imgs=d["version_gallery"]["images"]
    assert len(imgs)==10 and len({x["url"] for x in imgs})==10
    assert sum(x["web_fetch_status"]=="VISUALLY_RENDERED" for x in imgs)==4
    assert all(x["raw_sha256"] is None and x["pet_name"] is None and x["source_graphic_id"] is None for x in imgs)
    assert d["official_species_count"] is None and not d["official_deployment_verified"] and not d["original_assets_published"]
    print("PET20: seven named claims, ten gallery references; no official award inference")
if __name__=="__main__":main()
