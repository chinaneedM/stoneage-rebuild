"""Public O18 source-only guard: original server map / NPC dialogue bytes remain private."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/recovered/STONEAGE-O18-MAP1003-SAME-CARRIER-NAMED-CONTENT-R1.json"
ORIGINALS={"msg_1003_16_13":(220,"a96b0aa7dc09abde9ab2ff872f5fdc38255ef6e78ec2054ae95fa0244b9170a5"),"ps_1003_12_13":(397,"f4759c08d7391033b8fcee4d2580832c77e8210d637009b608be460b51285cbe"),"psks_1003_18_13":(105,"c4063d4fe350ff3b1ed4638e72f62f919b229e042112c0f6e7aec7af24e41558")}

def need(ok,reason):
    if not ok: raise ValueError(reason)
def validate(a):
    need(a["schema"]=="stoneage.o18.same_carrier_map1003_named_content.r1","schema")
    need(a["original_carrier"]=={"bytes":361255180,"sha256":"d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5","private_actual_whole_archive_sha256_verified":True},"actual source carrier")
    c=a["original_client_map"]
    need((c["bytes"],c["sha256"],c["width"],c["height"])==(5408,"fc3037a1850c8baf06ad5874a4cb49ca5e13e9315c020f64c019417c33b694e6",30,30),"original client map")
    s=a["original_server_map"]
    need((s["bytes"],s["sha256"],s["header_magic"],s["big_endian_floor_id"],s["width"],s["height"])==(3644,"d297801034864d09f52e76d20b7c71137b9330f28ef7be90b931705f94d60567","LS2MAP",1003,30,30),"server source")
    need(s["original_CP950_location_label"]=="薩姆吉爾的寵物店|0" and s["original_label_CP950_sha256"]=="c63c24e2f99f8df6172d6fa2219fd3630d35ceaacc3debc56675e3bb5c1e0a75","original source label")
    need(s["original_tile_plane_big_endian_matches_client_little_endian_cells"]==900 and s["original_object_plane_big_endian_matches_client_little_endian_cells"]==900 and s["difference_count_by_plane"]==[0,0],"two actual 900-cell exact comparisons")
    p=a["original_aux_map"]
    need((p["bytes"],p["sha256"])==(1808,"f9597ba0cfdf9d77176e0fab6058de99b9b07932c18fa2058a477e344c9fcec0"),"original aux file")
    need(p["same_as_client_third_plane"] is False and p["semantics_known"] is False,"do not invent collision semantics")
    n=a["original_NPC_message_members"]
    need(set(n)==set(ORIGINALS),"exact source member scope")
    for name,(size,sha) in ORIGINALS.items():
        d=n[name]
        need((d["bytes"],d["sha256"])==(size,sha) and d["cp950_roundtrip"] is True,"source text qualified "+name)
        need(d["actual_NPC_create_pointer_proven"] is False and d["actual_dialogue_or_trade_or_skill_executed"] is False and d["text_is_copyright_source_only_private"] is True,"unproven NPC behaviors "+name)
        need(d["source_filename_coordinate_only"]==[int(x) for x in name.split("_")[-2:]],"filename only positions "+name)
    need(n["ps_1003_12_13"]["field_labels"]==["cost_msg","getfull_msg","main_msg","nomal_rate","over_msg","pool_cost","pool_flg","poolfull_msg","pooltanks_msg","realy_msg","special_pet","special_rate","thanks_msg"],"preserve original field spelling")
    need(n["psks_1003_18_13"]["field_labels"]==["main_msg","pet_skill","skill_rate"],"original skill fields")
    b=a["bounds"]
    need(b["server_map_name_proven_for_this_preserved_mixed25_carrier"] is True,"same preserved carrier scope")
    for key in ("name_proven_for_2003_or_official_TW10","client_server_same_deployed_release_proven","original_NPC_runtime_spawns_proven","original_shop_transaction_executed","original_pet_skill_training_executed","original_game_world_entered","original_script_and_message_bytes_committed_publicly"):
        need(b[key] is False,"unsupported runtime/version claim: "+key)
    need(b["overall_completion_percent"] is None,"overall percent unknown")
    q=a["private_source_package"]
    need(q["bytes"]==3724 and q["sha256"]=="892bf7f282e38978abfa9c5f976e715bed78a3b009d24f461b7de6a0b47c1578" and q["zip_members"]==7 and q["all_original_members_readback_verified"] is True and q["committed_to_public_Git"] is False,"private custody")
    return {"floor_id":1003,"matching_original_source_cells":1800,"private_NPC_source_members":3,"original_game_world_entered":False}
if __name__=="__main__":
    print(json.dumps(validate(json.loads(REPORT.read_bytes())),ensure_ascii=False))
