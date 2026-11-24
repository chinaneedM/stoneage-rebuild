"""Replay source-pinned 2009 pet acquisitions, names, and evidence separation."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_bytes())
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def main():
    d=read("research/pets/PET-HIGH-FIRST-23-2009-ACQUISITION-DOSSIERS-R1.json")
    for p,s in d["source_pins_git_blob"].items():assert blob((ROOT/p).read_bytes())==s
    p80,p81,p82,w,b,old=[read(p) for p in d["source_pins_git_blob"]]
    rows=d["records"];lookup={x["original_name"]:x for x in rows}
    oldnames={(x["region"],x["name"]) for x in old["rows"]};newnames={(x["region"],x["original_name"]) for x in rows}
    assert len(rows)==len(newnames)==8 and not oldnames&newnames and len(oldnames|newnames)==37
    assert len({x["research_id"] for x in rows})==8
    assert set(lookup)=={w["hakuen"]["name"],b["extraction"]["pet_name"],"플라티우스"}|{x["original_korean_name"] for x in p81["korean_named_event_pet_candidates"]}
    for x in rows:
        assert not x["actual_player_grant_verified"] and all(x[k] is None for k in ("official_first_release","native_id","original_sprite_id","original_animation","base_stat_ranges","element_values","growth_formula","innate_skills","skill_slots","riding","wild_spawn_coordinates"))
    white=lookup["ハクエン"]["acquisition"];assert white["declared_bag_item_types"]==w["hakuen"]["bag_declared_distinct_item_types"]==7 and white["visible_named_rows"]==w["hakuen"]["bag_visible_named_rows"]==6 and white["unidentified_item_count"]==1
    black=lookup["コクエン"];assert black["acquisition"]["conversion"]==b["extraction"]["conversion"] and black["acquisition"]["bag"]==b["extraction"]["bag"]
    sample=black["status_samples"][0];assert all(sample[k]==v for k,v in b["visual_reference"]["sample"].items()) and sample["source_sha256"]==b["visual_reference"]["image_metadata"]["sha256"] and not sample["species_base_values"]
    assert lookup["설표"]["acquisition"]["required_level_for_eligibility"]==30 and not lookup["설표"]["acquisition"]["automatic_permanent_grant_verified"]
    assert lookup["플라티우스"]["acquisition"]["map_piece_count_separate_item_reward"]==6
    assert len(d["existing_named_dossier_attestations"])==5 and all((x["region"],x["name"]) in oldnames for x in d["existing_named_dossier_attestations"])
    a=next(x for x in p80["sources"] if x["id"]=="JP2009-1013-TENTH-ANNIVERSARY-PET-BAG")
    assert [x["name"] for x in d["appearance_only_relations"]]==a["morph_armor_target_names_not_issued_new_species"] and all(x["native_id"] is None and not x["actual_pet_grant_verified"] for x in d["appearance_only_relations"])
    assert len(d["unresolved_reward_labels"])==3 and all(x["exact_native_name"] is None for x in d["unresolved_reward_labels"])
    assert d["planned_unverified_december_updates"]==p82["source_records"][0] and not d["planned_unverified_december_updates"]["actual_dec_updates_verified"]
    assert d["official_species_count"] is None and not d["original_assets_published"]
    print("PET23: eight new regional acquisition dossiers; five prior names reattested; pinned status sample kept distinct from base stats")
if __name__=="__main__":main()
