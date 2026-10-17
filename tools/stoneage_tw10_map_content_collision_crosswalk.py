"""Original TW1.0 map-number/collision metadata, grouped by *unverified* 2001 bitmap labels.

This is genuine original ADRN source data, but not actual world floor DAT/terrain,
NPC placement, teleport graph or historical scene identity.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
from tools.stoneage_pet_asset_growth_catalog import (
    ROOT, META, ROOT_MANIFEST_BLOB, gitblob, sha256file, require, tsv,
)

SOURCE_NAME="COLLISION-ATTR-R1.tsv.gz"
SOURCE_SHA="d26b318ea73833bd7cc68abc8b5798a81b76ef9309cc91b137f7a55c6c8275dc"
RANGE_SOURCE=ROOT/"research/recovered/STONEAGE-EARLY-VISUAL-ID-RANGES-INPUT-R1.json"
RANGE_BLOB="11bb14ef00c2ed354c5f00f510da8783376f1f28"
MAP_CHAIN=ROOT/"research/recovered/STONEAGE-TW10-RECEIVE-MAP-JOIN-R1.txt"
MAP_CHAIN_BLOB="f8792fb6c7ad22001d8400b293c775304caeb6a0"
METADATA_MANIFEST=ROOT/"research/recovered/tw10-resource-metadata/MANIFEST-R1.txt"
# The two current labels below originate from the 2001 player source, not v1 official.
BUCKETS=("tiles_small","tiles_large","npc_candidate")
ORIGINAL_MAX_BITMAP=125995

def audit():
    require(gitblob(METADATA_MANIFEST.read_bytes())==ROOT_MANIFEST_BLOB,"original v1 metadata provenance changed")
    require(sha256file(META/SOURCE_NAME)==SOURCE_SHA,"original v1 collision attributes source drift")
    require(gitblob(RANGE_SOURCE.read_bytes())==RANGE_BLOB,"player range source drift")
    require(gitblob(MAP_CHAIN.read_bytes())==MAP_CHAIN_BLOB,"v1 receive/map file chain report drift")
    chain=MAP_CHAIN.read_text(encoding="utf-8")
    require("MAP_FILE_XREF|rva=0x1da50" in chain,"v1 writable map cache absent")
    require("MAP_FILE_XREF|rva=0x1dda0" in chain,"v1 read/check map cache absent")
    p=json.loads(RANGE_SOURCE.read_text(encoding="utf-8"))
    require(p["source_grade"]=="2001_DATED_PLAYER_CLAIM_NOT_DIRECT_JSS_OR_TW10_UI_PROOF","player label source upgraded")
    candidate={x["id"]:x for x in p["claimed_ranges"]}
    require(all(k in candidate for k in BUCKETS),"missing player candidate range")
    spans={k:(candidate[k]["from"],candidate[k]["to"]) for k in BUCKETS}
    require(spans=={"tiles_small":(1,4574),"tiles_large":(4575,5845),"npc_candidate":(5846,5946)},
            "player source ranges changed")
    require(all(candidate[k]["actual_tw10_semantic_certified"] is False for k in BUCKETS),"player categories falsely certified")
    distributions={k:{"number":0,"map_nums":[],"bitmapnos":[],"hits":Counter(),"priorities":Counter(),
                      "widths":Counter(),"footprints":Counter(),"height_flags":Counter()}
                   for k in (*BUCKETS,"not_in_player_terrain_object_ranges")}
    seen_map=set()
    map_to_bitmap={}
    out_of_bitmap_range=[]
    for row in tsv(META/SOURCE_NAME):
        n=int(row["map_number"]); b=int(row["bitmapno"])
        hit_raw=int(row["hit_raw"]);hit=int(row["hit_flag"]);priority=int(row["priority_type"])
        require(n>0 and n not in seen_map,"collision TSV must have positive unique map numbers")
        require(hit_raw%100==hit and hit_raw//100==priority,"raw hit flag or priority inconsistent")
        seen_map.add(n)
        require(0<=b<=ORIGINAL_MAX_BITMAP,"original collision number not in original bitmap")
        map_to_bitmap[n]=b
        k=next((k for k,(lo,hi) in spans.items() if lo<=b<=hi),"not_in_player_terrain_object_ranges")
        d=distributions[k]; d["number"]+=1
        d["map_nums"].append(n);d["bitmapnos"].append(b)
        d["hits"][hit]+=1;d["priorities"][priority]+=1
        d["footprints"][(int(row["atari_x"]),int(row["atari_y"]))]+=1
        d["height_flags"][int(row["height_flag"])]+=1
    require(len(seen_map)==9286,"original TW1 map number unique count drift")
    require(sum(d["number"] for d in distributions.values())==9286,"partition does not cover original map numbers")
    totals=Counter()
    rows=[]
    for k,d in distributions.items():
        totals.update(d["hits"])
        rows.append({
         "id":k,
         "source_label_is_2001_player_hypothesis":True,
         "original_tw10_collision_map_numbers":d["number"],
         "unique_original_tw10_bitmap_numbers":len(set(d["bitmapnos"])),
         "original_map_number_min_max":[min(d["map_nums"]),max(d["map_nums"])] if d["map_nums"] else None,
         "bitmap_number_min_max":[min(d["bitmapnos"]),max(d["bitmapnos"])] if d["bitmapnos"] else None,
         "raw_hit_flag_counts":[{"hit_flag":v,"count":n} for v,n in sorted(d["hits"].items())],
         "raw_priority_type_counts":[{"priority_type":v,"count":n} for v,n in sorted(d["priorities"].items())],
         "height_flag_counts":[{"height_flag":v,"count":n} for v,n in sorted(d["height_flags"].items())],
         "collision_footprint_x_y_common":[{"atari_x":xy[0],"atari_y":xy[1],"count":n}
                                       for xy,n in sorted(d["footprints"].items(),key=lambda v:(-v[1],v[0]))[:8]],
         "sample_original_map_number_bitmap_pairs":[{"map_number":n,"bitmapno":map_to_bitmap[n]}
              for n in sorted(d["map_nums"])[:5]],
         "actual_early_village_or_region_membership_verified":False,
         "concrete_field_map_dat_payload_acquired":False,
         "original_v1_server_spawn_or_event_records_verified":False
        })
    return {
      "schema":"stoneage.tw10_original_map_number_collision_player_category_crosswalk.r1",
      "task":"TW10-MAP-CONTENT-ORIGINAL-RESOURCE-BOUNDARY-01",
      "original_corpus":"TW10_ADRN_MAP_NUMBER_COLLISION_DERIVED_DATA",
      "original_source_manifest_blob":ROOT_MANIFEST_BLOB,
      "original_collision_dataset_sha256":SOURCE_SHA,
      "source_player_label_blob":RANGE_BLOB,
      "original_v1_binary_m_mc_cache_chain_blob":MAP_CHAIN_BLOB,
      "original_collision_unique_map_numbers":len(seen_map),
      "original_bitmap_number_max":ORIGINAL_MAX_BITMAP,
      "original_map_number_hit_flag_counts":[{"hit_flag":v,"count":n} for v,n in sorted(totals.items())],
      "original_source_order_duplicate_map_numbers":3,
      "source_order_last_wins_taken_from_existing_original_export_not_recomputed_in_deduped_table":True,
      "partition_rows":rows,
      "tw10_retail_disc_concrete_field_map_files":0,
      "v1_message_M_to_map_cache_write_path_verified":True,
      "v1_message_MC_to_map_cache_read_check_path_verified":True,
      "v1_cache_filename":"map\\%d.dat",
      "v1_sameday_fieldmap_payloads_present":False,
      "source_layer_only_not_world_map_restoration":True,
      "unverified_later_compatible_map_promoted_to_tw10":False,
      "original_server_npc_encounter_reward_data_connected":False,
      "all_early_world_regions_restored":False,
      "stage_b_production_started":False,
      "next":"TW10-AUDIO-EVENT-SOURCE-GATE-01"
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--write",type=Path)
    args=parser.parse_args()
    r=audit()
    if args.write:
        args.write.parent.mkdir(parents=True,exist_ok=True)
        args.write.write_text(json.dumps(r,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("TW10_ORIGINAL_MAP_COLLISION_CROSSWALK="+json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(",",":")))

if __name__=="__main__":main()
