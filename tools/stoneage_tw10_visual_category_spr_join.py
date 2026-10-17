"""TW1.0 original SPR frame reference intersections with *player-labeled* 2001 bitmap ranges.
No original pet, avatar, or NPC species/role attribution can be concluded from a numeric join.
"""
from __future__ import annotations
import argparse
import collections
import json
from pathlib import Path
from tools.stoneage_pet_asset_growth_catalog import META, SOURCE_GZIP_SHA256, ROOT_MANIFEST_BLOB, gitblob, require, sha256file, tsv

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "research/recovered/STONEAGE-EARLY-VISUAL-ID-RANGES-INPUT-R1.json"
INPUT_BLOB = "11bb14ef00c2ed354c5f00f510da8783376f1f28"
SELECTED = ("npc_candidate", "pet_portrait", "character_portrait", "items", "ui", "character_actions", "pet_actions")
SOURCE_MANIFEST = META / "MANIFEST-R1.txt"

def audit():
    require(gitblob(INPUT.read_bytes()) == INPUT_BLOB, "changed period-label input")
    require(gitblob(SOURCE_MANIFEST.read_bytes()) == ROOT_MANIFEST_BLOB, "changed original TW1 manifest")
    for filename, digest in SOURCE_GZIP_SHA256.items():
        require(sha256file(META / filename) == digest, "mismatched original dataset " + filename)
    raw = json.loads(INPUT.read_text(encoding="utf-8"))
    require(raw["source_grade"] == "2001_DATED_PLAYER_CLAIM_NOT_DIRECT_JSS_OR_TW10_UI_PROOF", "source grade upgraded")
    source_ranges = {x["id"]: x for x in raw["claimed_ranges"]}
    require(set(SELECTED) <= set(source_ranges), "missing player category")
    spans = {name:(source_ranges[name]["from"], source_ranges[name]["to"]) for name in SELECTED}
    require(spans["pet_portrait"] == (7246,7366) and spans["pet_actions"] == (95883,125995), "target image labels changed")
    require(all(source_ranges[name]["actual_tw10_semantic_certified"] is False for name in SELECTED), "semantic fact not grounded")
    original_bitmap_ids = set()
    for row in tsv(META/"ADRN-R1.tsv.gz"):
        bid = int(row["bitmapno"])
        require(bid not in original_bitmap_ids, "duplicate original bitmap ID")
        original_bitmap_ids.add(bid)
    require(original_bitmap_ids == set(range(125996)), "original TW1.0 bitmap ID envelope changed")
    groups={}
    for row in tsv(META/"SPR-GROUP-R1.tsv.gz"):
        idx=int(row["index"])
        require(idx not in groups, "duplicate SPR group")
        groups[idx]=(int(row["spr_no"]),int(row["anim_count"]))
    require(len(groups)==464, "original group count changed")
    animations={}
    for row in tsv(META/"SPR-ANIMATION-R1.tsv.gz"):
        g=int(row["group_index"]); a=int(row["anim_index"])
        require(g in groups and int(row["spr_no"])==groups[g][0], "original animation/group mismatch")
        require((g,a) not in animations, "duplicate animation")
        animations[(g,a)]=int(row["frame_count"])
    require(len(animations)==39065, "original animation count changed")
    frame_hits=collections.Counter()
    group_nonempty=collections.Counter()
    references=collections.Counter()
    referenced_ids={name:set() for name in SELECTED}
    seen_groups={name:set() for name in SELECTED}
    seen_animations={name:set() for name in SELECTED}
    per_group={name:collections.Counter() for name in SELECTED}
    used_ids=set()
    sentinel=0
    total_frames=0
    last_frame_index=collections.Counter()
    for row in tsv(META/"SPR-FRAME-R1.tsv.gz"):
        total_frames+=1
        g=int(row["group_index"]); a=int(row["anim_index"]); f=int(row["frame_index"])
        bid=int(row["bmp_no"]); s=int(row["sentinel"])
        require(g in groups and (g,a) in animations, "orphan SPR frame")
        require(int(row["spr_no"])==groups[g][0], "frame group ID mismatch")
        require(f == last_frame_index[(g,a)], "broken frame sequence")
        last_frame_index[(g,a)]+=1
        if s:
            require(bid==4294967295, "invalid sentinel")
            sentinel+=1
            continue
        require(bid in original_bitmap_ids, "unresolved SPR bitmap reference")
        group_nonempty[g]+=1
        used_ids.add(bid)
        for name,(lo,hi) in spans.items():
            if lo <= bid <= hi:
                references[name]+=1
                referenced_ids[name].add(bid)
                seen_groups[name].add(g)
                seen_animations[name].add((g,a))
                per_group[name][g]+=1
    require(total_frames==242085 and sentinel==3492 and sum(group_nonempty.values())==238593, "global original frame census changed")
    require(all(last_frame_index.get(key,0)==n for key,n in animations.items()), "animation frame fill changed")
    rows=[]
    for name in SELECTED:
        lo,hi=spans[name]
        present=set(range(lo,hi+1)) & original_bitmap_ids
        hit=referenced_ids[name]
        exclusive=sorted(g for g in seen_groups[name] if group_nonempty[g]>0 and group_nonempty[g]==per_group[name][g])
        rows.append({
          "category_id":name,
          "player_label":source_ranges[name]["claim"],
          "version_of_label":"UNSPECIFIED_2001_PLAYER_ARTICLE_CURRENT_MIGRATION",
          "tw10_bitmap_id_span":[lo,hi],
          "candidate_bitmap_ids_present_in_tw10":len(present),
          "original_spr_frame_references":references[name],
          "original_distinct_bitmap_ids_referenced_by_spr":len(hit),
          "original_distinct_bitmap_ids_not_referenced_by_spr":len(present-hit),
          "original_spr_groups_touching_range":len(seen_groups[name]),
          "original_animations_touching_range":len(seen_animations[name]),
          "original_spr_groups_with_all_nonsentinel_frames_in_range":len(exclusive),
          "sample_spr_group_ids":[groups[g][0] for g in sorted(seen_groups[name])[:6]],
          "sample_unreferenced_bitmap_ids":sorted(present-hit)[:6],
          "historical_game_semantic_certified":False,
          "species_master_or_avatar_identity_certified":False,
          "original_render_selection_proven":False
        })
    cross_group_count=sum(1 for g in groups if sum(1 for name in SELECTED if g in seen_groups[name])>1)
    return {
     "schema":"stoneage.tw10_original_spr_player_category_intersection.r1",
     "task":"TW10-RESOURCE-CATEGORY-SPR-JOIN-01",
     "source_profile":"TW10_ORIGINAL_RESOURCE_INDEX_PLUS_UNCERTIFIED_PLAYER_LABELS",
     "original_manifest_blob":ROOT_MANIFEST_BLOB,
     "player_range_input_blob":INPUT_BLOB,
     "source_dataset_sha256":SOURCE_GZIP_SHA256,
     "original_tw10_bitmap_ids":[0,125995],
     "original_tw10_bitmap_count":len(original_bitmap_ids),
     "original_spr_group_count":len(groups),
     "original_animation_count":len(animations),
     "original_frame_count":total_frames,
     "sentinel_frame_count":sentinel,
     "non_sentinel_frame_count":sum(group_nonempty.values()),
     "original_total_distinct_bitmaps_referenced_by_spr":len(used_ids),
     "original_spr_groups_touching_multiple_selected_ranges":cross_group_count,
     "categories":rows,
     "same_build_pet_master_available":False,
     "same_build_avatar_identity_available":False,
     "any_player_category_upgraded_to_original_semantic_fact":False,
     "original_client_render_execution_tested":False,
     "copyrighted_original_bitmaps_committed":False,
     "historical_pet_species_total":None,
     "historical_quest_data_connected":False
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--write",type=Path)
    args=parser.parse_args()
    doc=audit()
    output=json.dumps(doc,ensure_ascii=False,sort_keys=True,separators=(",",":"))
    if args.write:
        args.write.parent.mkdir(parents=True,exist_ok=True)
        args.write.write_text(json.dumps(doc,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("VISUAL_CATEGORY_JOIN_JSON="+output)

if __name__=="__main__": main()
