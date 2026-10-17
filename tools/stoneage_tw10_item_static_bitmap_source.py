"""Same-build TW1.0 item-message graphic fields vs original static bitmap metadata.

An exact original bitmap ID existing in an old player's item-number range does
NOT certify any concrete item -> bitmap linkage or actual client draw call.
No copyrighted bitmap payload is read or exported.
"""
from __future__ import annotations
import argparse
from collections import Counter
import json
from pathlib import Path

from tools.stoneage_pet_asset_growth_catalog import (
    ROOT, META, ROOT_MANIFEST_BLOB, SOURCE_GZIP_SHA256,
    gitblob, require, sha256file, tsv,
)

INPUT = ROOT/"research/recovered/STONEAGE-EARLY-VISUAL-ID-RANGES-INPUT-R1.json"
INPUT_BLOB = "11bb14ef00c2ed354c5f00f510da8783376f1f28"
SCHEMA = ROOT/"research/clients/STONEAGE-TW10-GAMEPLAY-SCHEMA-R1.json"
SCHEMA_BLOB = "e39a3a6020b578da017ab0bfa9369dc083e0b700"
CALLBACKS = ROOT/"research/recovered/STONEAGE-TW10-GAMEPLAY-CALLBACKS-R1.txt"
CALLBACKS_BLOB = "bdcd7b7ed5295db78b5d8cbdad58d5ce94802f31"
VISUAL = ROOT/"research/recovered/STONEAGE-TW10-VISUAL-CATEGORY-SPR-JOIN-R1.json"
VISUAL_BLOB = "20a82e4d35661785c4e50b44855cf8e8a4e98f3e"
SELECTED = ("npc_candidate","items","magic","pet_portrait","ui")

def read_pinned(path:Path, blob:str):
    raw=path.read_bytes()
    require(gitblob(raw)==blob,"pinned repository source drift: "+path.name)
    return raw.decode("utf-8")

def observe():
    require(gitblob((META/"MANIFEST-R1.txt").read_bytes())==ROOT_MANIFEST_BLOB,"TW1.0 manifest drift")
    for name,digest in SOURCE_GZIP_SHA256.items():
        require(sha256file(META/name)==digest,"TW1.0 source dataset drift: "+name)
    raw_ranges=json.loads(read_pinned(INPUT,INPUT_BLOB))
    original=json.loads(read_pinned(SCHEMA,SCHEMA_BLOB))
    callback_text=read_pinned(CALLBACKS,CALLBACKS_BLOB)
    prev=json.loads(read_pinned(VISUAL,VISUAL_BLOB))
    require(raw_ranges["source_grade"]=="2001_DATED_PLAYER_CLAIM_NOT_DIRECT_JSS_OR_TW10_UI_PROOF",
            "not same-build official player labels")
    ranges={x["id"]:x for x in raw_ranges["claimed_ranges"]}
    require({x for x in SELECTED} <= ranges.keys(),"candidate range missing")
    require((ranges["items"]["from"],ranges["items"]["to"])==(5973,7003),"item range drift")
    require(all(ranges[k]["actual_tw10_semantic_certified"] is False for k in SELECTED),
            "player category wrongly certified")
    source_records=original["records"]
    definitions=(
      ("inventory_full_slot","S:I","0x30922",9,5,20),
      ("inventory_incremental_record","I","0x325f0",10,6,None),
      ("world_ground_item_record","C","0x31260",6,4,None),
    )
    locations=[]
    for name,wire,callback,width,position,slots in definitions:
        rec=source_records[name]
        n=rec.get("record_width",rec.get("full_record_width"))
        require(n==width and len(rec["fields"])==width,"record width drift "+name)
        field=rec["fields"][position-1]
        require(field["position"]==position and field["name"]=="graphic_id",
                "original wire-image position drift "+name)
        require(field["position_evidence"]=="V1_DIRECT" and field["semantic_evidence"]=="EARLY_LINEAGE",
                "wire position or semantic provenance changed "+name)
        require(rec["transport"]["callback_rva"].lower()==callback,"callback RVA drift")
        if slots is not None:
            require(rec["slot_count"]==slots,"full inventory slot count drift")
        locations.append({
          "record":name,"wire":wire,"callback_rva":callback,
          "field_position":position,"field_name":"graphic_id",
          "field_wire_type":field["wire_type"],
          "position_evidence":"V1_DIRECT","semantic_label_evidence":"EARLY_LINEAGE",
          "actual_runtime_values_observed":False,
          "direct_selector_to_original_adrn_bitmapno_verified":False
        })
    require("S_CATEGORY|char=I|code=73|slot=3|target_rva=0x30922" in callback_text,
            "original S:I jump target drift")
    require("CALLBACK|name=I|rva=0x325f0" in callback_text,
            "original incremental I callback drift")
    require("CALLBACK|name=C|rva=0x31260" in callback_text,
            "original ground object callback drift")
    previous={x["category_id"]:x for x in prev["categories"]}
    require(previous["items"]["original_spr_frame_references"]==0,
            "prior independently verified item range SPR membership changed")
    bounds={key:(ranges[key]["from"],ranges[key]["to"]) for key in SELECTED}
    bands={k:[] for k in SELECTED}
    idset=set()
    total=0
    for row in tsv(META/"ADRN-R1.tsv.gz"):
        total+=1
        image=int(row["bitmapno"])
        require(image not in idset,"duplicate original bitmap number")
        idset.add(image)
        for name,(lo,hi) in bounds.items():
            if lo<=image<=hi:
                bands[name].append(row)
                break
    require(total==125996 and idset==set(range(125996)),
            "original bitmap numeric namespace changed")
    def describe(key,entries):
        lo,hi=bounds[key]
        require(len(entries)==hi-lo+1,"original entire band not present: "+key)
        widths=[int(x["width"]) for x in entries]
        heights=[int(x["height"]) for x in entries]
        xoff=[int(x["xoff"]) for x in entries]
        yoff=[int(x["yoff"]) for x in entries]
        flags=Counter(x["rd_flag"] for x in entries)
        pairs=Counter((int(x["width"]),int(x["height"])) for x in entries)
        hashes=[x.get("rd_block_sha256","") for x in entries]
        nohash=sum(not s for s in hashes)
        size_vals=[int(x["size"]) for x in entries]
        first=sorted(entries,key=lambda r:int(r["bitmapno"]))[:5]
        return {
          "player_category_id":key,
          "player_category_text":ranges[key]["claim"],
          "displayed_2001_player_text_not_original_tw10_semantic":True,
          "original_tw10_bitmap_range":[lo,hi],
          "original_bitmap_id_membership_count":len(entries),
          "original_bitmap_ids_with_nonpositive_dimensions":sum(w<=0 or h<=0 for w,h in zip(widths,heights)),
          "dimension_width_min_max":[min(widths),max(widths)],
          "dimension_height_min_max":[min(heights),max(heights)],
          "offset_x_min_max":[min(xoff),max(xoff)],
          "offset_y_min_max":[min(yoff),max(yoff)],
          "metadata_encoded_size_min_max":[min(size_vals),max(size_vals)],
          "dimension_pair_distinct_count":len(pairs),
          "top_dimension_pairs":[{"width":w,"height":h,"records":n}
                                 for (w,h),n in sorted(pairs.items(),key=lambda x:(-x[1],x[0]))[:8]],
          "rd_flag_value_counts":[{"raw_value":s,"count":n} for s,n in sorted(flags.items())],
          "missing_rd_block_sha256_records":nohash,
          "distinct_nonempty_rd_block_sha256":len(set(x for x in hashes if x)),
          "example_original_records":[{
            "bitmapno":int(x["bitmapno"]),
            "width":int(x["width"]), "height":int(x["height"]),
            "xoff":int(x["xoff"]),"yoff":int(x["yoff"]),
            "rd_flag":x["rd_flag"],"rd_block_sha256":x.get("rd_block_sha256","")
          } for x in first],
          "original_game_item_identity_verified":False,
          "original_static_draw_call_verified":False
        }
    out=[describe(k,bands[k]) for k in SELECTED]
    return {
      "schema":"stoneage.tw10_item_static_bitmap_message_source_boundary.r1",
      "task":"TW10-ITEM-STATIC-BITMAP-SOURCE-SELECTOR-01",
      "evidence_basis":"ORIGINAL_TW10_COMPILED_WIRE_POSITIONS_PLUS_DIRECT_ADRN_METADATA_AND_2001_PLAYER_BAND_LABEL",
      "source_files_git_blobs":{
        "original_wire_schema":SCHEMA_BLOB,
        "original_callback_report":CALLBACKS_BLOB,
        "original_bitmap_manifest":ROOT_MANIFEST_BLOB,
        "player_labeled_visual_ranges":INPUT_BLOB,
        "prior_direct_sprite_membership_report":VISUAL_BLOB
      },
      "original_dataset_sha256":SOURCE_GZIP_SHA256,
      "original_total_bitmap_numbers":total,
      "original_bitmap_number_min_max":[min(idset),max(idset)],
      "item_graphic_message_fields":locations,
      "bitmap_metadata_bands":out,
      "item_player_band_id_count":len(bands["items"]),
      "item_player_band_spr_frame_refs":previous["items"]["original_spr_frame_references"],
      "compiled_same_build_wire_position_observed":True,
      "transmitted_real_graphic_values_observed":False,
      "draw_selector_graphic_id_to_bitmapno_certified":False,
      "original_game_item_master_source_acquired":False,
      "original_item_name_price_recipe_catalog_complete":False,
      "item_count_equal_to_bitmap_candidate_count_proven":False,
      "original_client_executed":False,
      "copyrighted_game_pixels_published":False,
      "stage_b_production_started":False,
      "conclusion":"BOUNDED_ORIGINAL_RESOURCE_METADATA_AND_PROTOCOL_FIELD_JOIN_OPEN_DRAW_SELECTOR",
      "next":"TW10-MAP-CONTENT-ORIGINAL-RESOURCE-BOUNDARY-01"
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--write",type=Path)
    args=parser.parse_args()
    report=observe()
    if args.write:
        args.write.parent.mkdir(parents=True,exist_ok=True)
        args.write.write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("TW10_ITEM_STATIC_SOURCE_REPORT="+json.dumps(report,ensure_ascii=False,sort_keys=True,separators=(",",":")))

if __name__=="__main__":
    main()
