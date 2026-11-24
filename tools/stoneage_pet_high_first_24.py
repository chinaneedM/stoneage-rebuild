"""Replay exact named source crosswalks without promoting historical identity."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_bytes())
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def main():
    d=read("research/pets/PET-HIGH-FIRST-24-CN2010-NAMED-PANEL-CROSSWALK-R1.json")
    for p,s in d["source_pins_git_blob"].items():assert blob((ROOT/p).read_bytes())==s
    p83,p84,m,g,n,c,b,s=[read(p) for p in d["source_pins_git_blob"]]
    rows=d["rows"];assert len(rows)==8
    for x in rows:
        names=set(x["names"])
        master=[y for y in m["pet_flag_1_field_projections"] if y["name"] in names]
        grid=[dict(program=p,**y) for p,z in g["programs"].items() for y in z["source_records"] if y["original_name_cp950"] in names]
        native=[dict(graphic=y["tw85_original_spr_number"],occurrences=y["source_spr_occurrences"],conflicting_names=y["graphic_has_conflicting_names_across_installer_programs"],all_program_routes={p:z["original_name_cp950"] for p,z in y["program_routes"].items()}) for y in n["records"] if any(z["original_name_cp950"] in names for z in y["program_routes"].values())]
        expected=dict(claimed_tw75_master=master,tw85_program_grid=grid,tw85_extra_spr_groups=native,cn50_native_spr=[y for y in c["records"] if y["compiled_name"] in names],conditional_tw75_ranges=[y for y in b["rows"] if any(z["template_id"]==y["template_id"] for z in master)],later_comparison_encounters=[y for y in s["rows"] if any(z["template_id"]==y["template_id"] for z in master)])
        assert x["source_candidates"]==expected
        assert all(x[k] is None for k in ("cn2010_native_pet_id","cn2010_original_sprite_id","cn2010_birth_stat_range","cn2010_growth","cn2010_skills","first_release_date"))
        assert not x["actual_live_release_verified"] and not x["actual_player_grant_verified"]
        if x["sample"]:assert x["sample"]["raw_response_sha256"] is None and x["sample"]["level"]==1 and x["sample"]["element_numeric_values"] is None
    samples=[x["sample"] for x in rows if x["sample"]]
    assert len(samples)==7 and sum(all(y is not None for y in x["hp_attack_defense_agility"]) for x in samples)==5
    assert sum(bool(x["source_candidates"]["tw85_program_grid"]) for x in rows)==4
    assert sum(bool(x["source_candidates"]["tw85_extra_spr_groups"]) for x in rows)==2
    assert sum(bool(x["source_candidates"]["claimed_tw75_master"]) for x in rows)==2
    assert sum(bool(x["source_candidates"]["cn50_native_spr"]) for x in rows)==2
    assert d["official_species_count"] is None and not d["original_assets_published"] and d["summary"]["original_cn2010_client_bytes"]==0
    print("PET24: seven source-labelled panel samples and eight bounded records; independent cross-version routes replayed")
if __name__=="__main__":main()
