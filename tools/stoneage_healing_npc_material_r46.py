"""Offline R46 material evidence replay; no original commercial script execution."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
from tools.stoneage_preserved_healing_npc_r46 import (
    EXPECTED_BYTES, EXPECTED_SHA256, SOURCE_SCOPE, ORIGIN, PREFIX, RELATIVE_PATH,
    sha, require, MAX_SELECTED
)

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"research/recovered/STONEAGE-PRESERVED-HEALING-NPC-SOURCE-R46.json"
MATERIAL=ROOT/"research/recovered/STONEAGE-PRESERVED-HEALING-NPC-MATERIAL-R46.json"
CUSTODY=ROOT/"research/recovered/STONEAGE-PRESERVED-HEALING-NPC-CUSTODY-R46.json"
SOURCE_GIT_BLOB="a0e5391ab70d5636fe55e196ec5b6081d4825ddc"
SOURCE_RUN=40502401619
SOURCE_JOB=122183066222
SOURCE_HEAD="0cea990336ff52699b4faa3212bb59fb3dbd8a3f"
SOURCE_ARTIFACT=12732389728
API_ZIP_DIGEST="1962baed3c42e7dbf23afe15b0caa11b42caeb6a1e970f2d1847024ee3e31416"
NAMES=["家族小護士"]*3
FLOORS=[1041,2031,3031]
CORNERS=[[4,8,4,8],[13,8,13,8],[2,9,2,9]]
DRAW_IDS=[16023]*3
REFS=["npcgen_fmhealer|1"]*3

def blob_sha(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def verified_source_bytes():
    data=SOURCE.read_bytes()
    require(blob_sha(data)==SOURCE_GIT_BLOB,"R46 permanent original derived report git blob differs")
    return data

def validate(d):
    require(set(d)=={"schema","source_scope","status","origin_class",
                    "official_tw10_npc_authenticated","original_server_executed",
                    "raw_original_npc_script_published","receipt","material"},
            "unknown/unsafe original report properties")
    require(d["schema"]=="stoneage.preserved_healing_npc_material_source.r46" and
            d["source_scope"]==SOURCE_SCOPE and d["origin_class"]==ORIGIN and
            d["status"]=="ONE_ORIGINAL_MEMBER_AND_UP_TO_THREE_NPC_CREATIONS_QUALIFIED",
            "source scope/source acquisition unresolved")
    require(type(d["official_tw10_npc_authenticated"]) is int and
            d["official_tw10_npc_authenticated"]==0 and
            d["original_server_executed"] is False and
            d["raw_original_npc_script_published"] is False,
            "source fact promoted to historical/runtime authenticity")
    r=d["receipt"]
    require(set(r)=={"headers_visited","range_requests","actual_range_bytes","range_receipts",
                    "public_pages","archive_part_or_whole_redownloaded",
                    "two_decoders_share_same_http_source_not_independent_archives",
                    "original_member"}, "unexpected source custody properties")
    require(r["headers_visited"]==7954 and r["range_requests"]==184 and
            r["actual_range_bytes"]==12013836 and
            r["archive_part_or_whole_redownloaded"] is False and
            r["two_decoders_share_same_http_source_not_independent_archives"] is True,
            "original archive scope/budget/HTTP source mismatch")
    ranges=r["range_receipts"]
    require(len(ranges)==184 and
            sum(v["bytes"] for v in ranges)==r["actual_range_bytes"]<=16*1024*1024,
            "original source range conservation")
    require(ranges[0]=={"part":1,"start":0,"end":65535,"bytes":65536,
            "sha256":"f745aa227fe796fa38c1257879c67ed72e2d0d308e0ea7ee462dd57667be9b22"},
            "known original first HTTP206 range SHA differs")
    seen=set()
    for q in ranges:
        require(set(q)=={"part","start","end","bytes","sha256"} and
                type(q["part"]) is int and q["part"] in (1,2) and
                type(q["start"]) is int and q["start"]>=0 and
                q["end"]-q["start"]+1==q["bytes"] and
                re.fullmatch("[a-f0-9]{64}",q["sha256"]) is not None,
                "one strict original HTTP206 region")
        key=q["part"],q["start"]
        require(key not in seen,"duplicate range receipt")
        seen.add(key)
    orig=r["original_member"]
    require(orig["path"]==PREFIX+RELATIVE_PATH and
            (orig["bytes"],orig["sha256"])==(EXPECTED_BYTES,EXPECTED_SHA256) and
            orig["crc32"]==3313982981 and orig["packed_bytes"]==210 and
            orig["compression_method"]==53 and orig["flags"]&(1|2|4|16)==0 and
            orig["header_offset"]<orig["data_offset"] and
            orig["data_offset"]+orig["packed_bytes"]<=361255180 and
            orig["unar_exit_status"]==0 and
            orig["two_independent_decompressors_agree"] is True and
            type(orig["libarchive_version"]) is int and orig["libarchive_version"]>0,
            "one actual original member/file integrity")
    for k in ("original_header_sha256","compressed_payload_sha256"):
        require(re.fullmatch("[a-f0-9]{64}",orig[k]) is not None,
                "original header/payload hash")
    mat=d["material"]
    require(mat["raw_original_file"]=={"bytes":EXPECTED_BYTES,"sha256":EXPECTED_SHA256} and
            mat["qualified_decoders"]==["cp950","big5"] and
            mat["cp950_big5_exact_unicode_agreement"] is True and
            mat["original_creation_block_count"]==4 and
            mat["selected_creation_count"]==MAX_SELECTED==3 and
            mat["selected_rule"]=="FIRST_UP_TO_THREE_SOURCE_ORDER_NOT_ALL_NPCS",
            "bounded selected original records or number of unseen blocks")
    for flag in ("npc_function_bound_to_healer_runtime_proven","original_spawn_position_executed",
                 "same_build_with_taiwan_1_0_proven","four_hometown_healer_identity_proven",
                 "original_healing_prices_or_game_rules_proven",
                 "original_dialogue_or_script_body_published"):
        require(mat[flag] is False,"source-to-gameplay or script publication promotion: "+flag)
    require(mat["verified_base_game_quests_added"]==0,"unknown quest origin promoted")
    require(len(mat["selected_creation_occurrences"])==MAX_SELECTED,"all first three original create slots conserved")
    entries=[]
    for i,rec in enumerate(mat["selected_creation_occurrences"]):
        require(rec["source_block_order"]==i and rec["original_service_executed"] is False and
                0<rec["open_line"]<rec["close_line"]<=mat["physical_line_count"],
                "record identity or execution promoted")
        fields=rec["block_field_fingerprints"]
        require(len(fields)==len(rec["all_field_keys_as_written_lowercased"]) and
                [f["key"] for f in fields]==rec["all_field_keys_as_written_lowercased"] and
                len({f["key"] for f in fields})==len(fields),
                "full source-record field positions not preserved")
        for f in fields:
            require(re.fullmatch("[a-f0-9]{64}",f["value_utf8_sha256"]) is not None and
                    type(f["value_chars"]) is int and f["value_chars"]>=0,
                    "invalid script redaction fingerprint")
            require("raw_value" not in f and "text" not in f,"unredacted script value")
        indexed={x["key"]:x for x in fields}
        def numbers(key):
            return indexed[key]["integer_values"]
        require(indexed["name"]["original_name"]==NAMES[i] and
                sha(NAMES[i].encode("utf-8"))==indexed["name"]["value_utf8_sha256"] and
                numbers("floorid")==[FLOORS[i]] and
                numbers("borncorner")==CORNERS[i] and
                numbers("graphicname")==[DRAW_IDS[i]] and
                numbers("dir")==[4] and numbers("time")==[0] and
                numbers("createnum")==[1] and numbers("ignoreinvincible")==[1] and
                indexed["enemy"]["declared_reference_token"]==REFS[i],
                "original bounded healer NPC statement mutated")
        require(rec["bounded_selected_fields"]["name"]==indexed["name"] and
                rec["bounded_selected_fields"]["floorid"]==indexed["floorid"] and
                rec["bounded_selected_fields"]["enemy"]==indexed["enemy"],
                "original selected projection disagrees with complete metadata")
        entries.append({
          "source_block_order":i, "open_line":rec["open_line"],"close_line":rec["close_line"],
          "name_original_cp950_big5":NAMES[i],"name_sha256":sha(NAMES[i].encode()),
          "floorid_original":FLOORS[i],"borncorner_original_four_ints":CORNERS[i],
          "graphicname_original":DRAW_IDS[i], "dir_original":4, "createnum_original":1,
          "time_original_uninterpreted":0, "ignoreinvincible_original":1,
          "enemy_declared_token_original":REFS[i],
          "original_function_or_service_runtime_binding_proven":False
        })
    return entries

def material_from_source(raw):
    rows=validate(json.loads(raw))
    return {"schema":"stoneage.preserved_healing_npc_material.r46",
            "source_scope":SOURCE_SCOPE,"origin_class":ORIGIN,
            "original_file_sha256":EXPECTED_SHA256,
            "source_report": {"path":str(SOURCE.relative_to(ROOT)),
                              "bytes":len(raw),"sha256":sha(raw),"git_blob":blob_sha(raw)},
            "source_run_id":SOURCE_RUN,"source_job_id":SOURCE_JOB,
            "source_artifact_id":SOURCE_ARTIFACT,
            "source_artifact_zip_sha256_api_reported_only":API_ZIP_DIGEST,
            "source_file_original_creation_blocks":4,
            "bounded_first_three_creation_rows":rows,
            "fourth_create_block_fields_analyzed_this_package":False,
            "original_server_executed":False,"official_tw10_npc_authenticated":0,
            "same_build_or_original_function_binding_proven":False,
            "four_hometown_identity_confirmed":False,
            "verified_base_game_quests_added":0,
            "whole_original_source_published":False,
            "overall_restoration_percent":None,
            "next":"22_DOMAIN_SOURCE_QUEUE_NEW_NAMED_ENTITY_OR_CORE_QUEST_PRIMARY_CARRIER"}

def replay():
    raw=verified_source_bytes()
    expected=json.dumps(material_from_source(raw),ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    require(MATERIAL.read_text()==expected,"permanent named NPC source projection differs")
    custody=json.loads(CUSTODY.read_text())
    require(custody["source_run_id"]==SOURCE_RUN and
            custody["source_job_id"]==SOURCE_JOB and
            custody["source_head"]==SOURCE_HEAD and
            custody["artifact_id"]==SOURCE_ARTIFACT and
            custody["artifact_zip_sha256_api_only"]==API_ZIP_DIGEST and
            custody["independently_downloaded_artifact_zip_verified"] is False,
            "R46 actual CI provenance or independent ZIP claim differs")
    require(custody["original_qualified_report"]==material_from_source(raw)["source_report"],
            "R46 derived report source pin changed")
    require(custody["original_copyrighted_source_bytes_published"] is False and
            custody["raw_original_healer_dialogue_published"] is False and
            custody["official_build_authenticated"] is False,
            "original source or build was promoted")
    return {"status":"PASS","original_create_blocks":4,"derived_first_three":3,
            "source_git_blob":SOURCE_GIT_BLOB,"original_same_build_authenticated":0}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--write",action="store_true")
    a=p.parse_args()
    raw=verified_source_bytes()
    output=json.dumps(material_from_source(raw),ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if a.write:
        MATERIAL.write_text(output)
    else:
        print(json.dumps(replay(),ensure_ascii=False))
if __name__=="__main__":
    main()
