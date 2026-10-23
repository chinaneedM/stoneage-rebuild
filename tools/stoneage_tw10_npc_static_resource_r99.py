"""R99 original TW1.0 bitmap -> map resource number: 101 anonymous player-labeled NPC candidates.

The original retail ADRN and collision TSVs are real source-derived metadata.
The labels NPC and related classification originate from an unverified 2001
player range list. map_number is a RESOURCE MAP NUMBER, NOT a world floor ID.
This program neither decodes/publishes original images nor invents game NPCs.
"""
from __future__ import annotations
import argparse
from collections import Counter
import json
from pathlib import Path
from tools.stoneage_pet_asset_growth_catalog import ROOT, META, gitblob, tsv, require, sha256file, ROOT_MANIFEST_BLOB, SOURCE_GZIP_SHA256

RANGE_PATH=ROOT/"research/recovered/STONEAGE-EARLY-VISUAL-ID-RANGES-INPUT-R1.json"
RANGE_BLOB="11bb14ef00c2ed354c5f00f510da8783376f1f28"
OLD_COLLISION=ROOT/"research/recovered/STONEAGE-TW10-MAP-CONTENT-COLLISION-R1.json"
OLD_COLLISION_BLOB="7d4d5d2cae224c093b3e85e8ef1bfc49b54c5981"
OLD_STATIC=ROOT/"research/recovered/STONEAGE-TW10-ITEM-STATIC-BITMAP-SOURCE-R1.json"
OLD_STATIC_BLOB="1210b0f910c353d58a3d6a4c458dda38f48aba86"
OLD_SPR=ROOT/"research/recovered/STONEAGE-TW10-VISUAL-CATEGORY-SPR-JOIN-R1.json"
OLD_SPR_BLOB="20a82e4d35661785c4e50b44855cf8e8a4e98f3e"
COLLISION_SHA="d26b318ea73833bd7cc68abc8b5798a81b76ef9309cc91b137f7a55c6c8275dc"
BAND_LO=5846
BAND_HI=5946

def audit():
    require(gitblob((META/"MANIFEST-R1.txt").read_bytes())==ROOT_MANIFEST_BLOB, "source manifest drift")
    for name in ("ADRN-R1.tsv.gz","SPR-FRAME-R1.tsv.gz"):
        require(sha256file(META/name)==SOURCE_GZIP_SHA256[name], "original source drift "+name)
    require(sha256file(META/"COLLISION-ATTR-R1.tsv.gz")==COLLISION_SHA,"collision source drift")
    pins=[(RANGE_PATH,RANGE_BLOB),(OLD_COLLISION,OLD_COLLISION_BLOB),(OLD_STATIC,OLD_STATIC_BLOB),(OLD_SPR,OLD_SPR_BLOB)]
    for p,sha in pins:
        require(gitblob(p.read_bytes())==sha,"parent changed: "+p.name)
    ranges=json.loads(RANGE_PATH.read_text(encoding="utf-8"))
    claimed=[x for x in ranges["claimed_ranges"] if x["id"]=="npc_candidate"]
    require(len(claimed)==1 and (claimed[0]["from"],claimed[0]["to"])==(BAND_LO,BAND_HI), "player label band drift")
    require(claimed[0]["actual_tw10_semantic_certified"] is False,"player label wrongly promoted")
    c=json.loads(OLD_COLLISION.read_text(encoding="utf-8"))
    p=next(x for x in c["partition_rows"] if x["id"]=="npc_candidate")
    require(p["original_tw10_collision_map_numbers"]==101 and p["original_map_number_min_max"]==[16000,16226], "prior collision census drift")
    require(p["raw_hit_flag_counts"]==[{"count":101,"hit_flag":0}],"prior collision type drift")
    st=json.loads(OLD_STATIC.read_text(encoding="utf-8"))
    oldband=next(x for x in st["bitmap_metadata_bands"] if x["player_category_id"]=="npc_candidate")
    require(oldband["original_bitmap_id_membership_count"]==101 and oldband["distinct_nonempty_rd_block_sha256"]==101,"prior raw image census drift")
    spr=json.loads(OLD_SPR.read_text(encoding="utf-8"))
    oldspr=next(x for x in spr["categories"] if x["category_id"]=="npc_candidate")
    require(oldspr["original_spr_frame_references"]==0,"prior original SPR zero drift")

    images={}
    num_adrn=0
    for row in tsv(META/"ADRN-R1.tsv.gz"):
        num_adrn+=1
        b=int(row["bitmapno"])
        if BAND_LO<=b<=BAND_HI:
            require(b not in images,"duplicate original image slot")
            images[b]={
              "bitmapno":b,
              "width":int(row["width"]),"height":int(row["height"]),
              "xoff":int(row["xoff"]),"yoff":int(row["yoff"]),
              "rd_flag":row["rd_flag"],"encoded_bytes":int(row["size"]),
              "rd_block_sha256":row["rd_block_sha256"]
            }
    require(num_adrn==125996 and set(images)==set(range(BAND_LO,BAND_HI+1)),"original ADRN size/band drift")
    require(all(rec["width"]>0 and rec["height"]>0 and len(rec["rd_block_sha256"])==64 for rec in images.values()),"unusable RD metadata")
    require(len({rec["rd_block_sha256"] for rec in images.values()})==101,"original hashed content is not unique")

    join={}
    total_collision=0
    for row in tsv(META/"COLLISION-ATTR-R1.tsv.gz"):
        total_collision+=1
        b=int(row["bitmapno"])
        if b in images:
            require(b not in join,"multiple map-resource numbers for same original bitmap")
            hit=int(row["hit_flag"]);priority=int(row["priority_type"])
            require(int(row["hit_raw"])==priority*100+hit,"raw hit inconsistent")
            join[b]={
             "map_number":int(row["map_number"]),
             "hit_flag":hit,"priority_type":priority,
             "atari_x":int(row["atari_x"]),"atari_y":int(row["atari_y"]),
             "height_flag":int(row["height_flag"])
            }
    require(total_collision==9286 and set(join)==set(images),"not a 101/101 original join")
    require(len({x["map_number"] for x in join.values()})==101,"nonunique map resource number")
    require(all(x["hit_flag"]==0 and x["priority_type"]==0 and x["height_flag"]==0 and (x["atari_x"],x["atari_y"])==(1,1) for x in join.values()),"NPC candidate resources' original collision flags changed")
    require([min(x["map_number"] for x in join.values()),max(x["map_number"] for x in join.values())]==[16000,16226],"map resource envelope drift")
    spr_hits=0
    frame_total=0
    for row in tsv(META/"SPR-FRAME-R1.tsv.gz"):
        frame_total+=1
        spr_hits += row["sentinel"]=="0" and BAND_LO<=int(row["bmp_no"])<=BAND_HI
    require(frame_total==242085 and spr_hits==0,"source SPR has unexpected references to static image band")
    rows=[]
    for bid in sorted(images):
        rows.append({**images[bid],**join[bid],"original_npc_id":None,"world_floor_id":None,"npc_name":None,"drawn_npc_role_verified":False})
    return {
        "schema":"stoneage.tw10_original_static_candidate_resource_join.r99",
        "task":"OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-99",
        "historical_scope":"ORIGINAL_TAIWAN_1_0_RETAIL_ADRN_COLLISION_METADATA_ONLY",
        "player_label":"NPC (2001 player bitmap number range; unconfirmed intended original category)",
        "source_pins":{
            "manifest_git_blob":ROOT_MANIFEST_BLOB,
            "adrn_gzip_sha256":SOURCE_GZIP_SHA256["ADRN-R1.tsv.gz"],
            "collision_gzip_sha256":COLLISION_SHA,
            "spr_frame_gzip_sha256":SOURCE_GZIP_SHA256["SPR-FRAME-R1.tsv.gz"],
            "player_range_git_blob":RANGE_BLOB,
            "parent_collision_report_git_blob":OLD_COLLISION_BLOB,
            "parent_static_report_git_blob":OLD_STATIC_BLOB,
            "parent_spr_report_git_blob":OLD_SPR_BLOB
        },
        "measured":{
           "original_bitmap_band":[BAND_LO,BAND_HI],
           "bitmap_rows":len(rows),
           "distinct_original_map_resource_numbers":len({r["map_number"] for r in rows}),
           "resource_map_number_range":[16000,16226],
           "original_collision_entries_total":total_collision,
           "original_bitmap_records_total":num_adrn,
           "original_spr_frames_checked":frame_total,
           "sprite_frame_refs_to_this_band":spr_hits,
           "same_build_original_server_NPC_table_obtained":False,
           "actual_world_map_dat_payloads_obtained":False,
           "true_npc_render_selector_traced":False
        },
        "rows":rows,
        "limits":{
          "map_number_is_world_floor_id":False,
          "map_resource_number_is_npc_entity_id":False,
          "player_bitmap_range_is_official_category":False,
          "same_build_npc_identity_available":False,
          "server_spawn_coordinates_available":False,
          "original_pixels_committed":False,
          "recreated_art_owned_for_release":False,
          "original_client_render_execution_observed":False,
          "other_original_sprite_animation_paths_disproved_by_zero":False,
          "stage_a_closed":False,
          "stage_b_started":False,
          "overall_restoration_percent":None,
          "next":"OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-100"
        }
    }

def validate_report(x,truth):
    require(x==truth,"immutable derived source row or provenance modified")
    require(x["schema"]=="stoneage.tw10_original_static_candidate_resource_join.r99", "schema")
    require(x["task"]=="OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-99", "task")
    require(len(x["rows"])==101 and [v["bitmapno"] for v in x["rows"]]==list(range(5846,5947)), "row count/order")
    require(all(v["original_npc_id"] is None and v["world_floor_id"] is None and v["npc_name"] is None and v["drawn_npc_role_verified"] is False for v in x["rows"]),"not original NPC identities")
    require(set(x["limits"].values())=={False,None,"OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-100"},"authority boundary")
    return True


REPORT=ROOT/"research/recovered/STONEAGE-TW10-NPC-STATIC-RESOURCE-JOIN-R99.json"
REPORT_BLOB="21d49800a1191f87a006aaa5af4a6f7975f91bf7"

def check_saved(truth):
    raw=REPORT.read_bytes()
    require(gitblob(raw)==REPORT_BLOB,"R99 source Git blob changed")
    actual=json.loads(raw.decode("utf-8"))
    validate_report(actual,truth)
    canon=(json.dumps(truth,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode("utf-8")
    require(raw==canon,"R99 derived report not byte-identical to fresh original-source replay")
    return True

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--write",type=Path)
    ap.add_argument("--print-rows",action="store_true")
    args=ap.parse_args()
    r=audit()
    validate_report(r,r)
    check_saved(r)
    payload=json.dumps(r,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if args.write:
        args.write.parent.mkdir(parents=True,exist_ok=True)
        args.write.write_text(payload,encoding="utf-8")
    print("R99_META_JSON="+json.dumps({k:v for k,v in r.items() if k!="rows"},ensure_ascii=False,separators=(",",":"),sort_keys=True))
    if args.print_rows:
        for item in r["rows"]:
            print("R99_ROW_JSON="+json.dumps(item,ensure_ascii=False,separators=(",",":"),sort_keys=True))
    print("R99 PASS: original 101/101 bitmap-to-map-resource physical join, zero SPR frame reference and no NPC role")
if __name__=="__main__":
    main()
