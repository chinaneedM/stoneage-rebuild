"""O19 source-only guard: one original create-to-argument link, no running original game."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/recovered/STONEAGE-O19-ONE-PETSHOP-CREATE-ARGUMENT-LINK-R1.json"

def need(ok, reason):
    if not ok: raise ValueError(reason)
def validate(d):
    need(d["schema"]=="stoneage.o19.one_npc_original_create_pointer.r1","schema")
    need(d["source_carrier"]=={"bytes":361255180,"sha256":"d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5"},"original carrier")
    a=d["original_create"]
    need((a["path"],a["bytes"],a["sha256"])==("gmsv/data/npc/genout/shop_m.create",20491,"d540e9a1354a0f82839cd30ab315a6dee4a3b0299744a0f63ae5ee461c5b587b"),"original create")
    need(a["exact_original_target_pointer_occurrences"]==1 and a["target_create_block_byte_span"]==[642,802] and a["target_create_block_sha256"]=="669e06a65e61f2346bf424a35e1a4af03f4e1c5f4089e89295115906271b2fe9","exact block")
    need(a["original_cp950_name"]=="寵物店" and a["actual_original_block_roundtrip_cp950"] is True,"name original")
    need(a["floorid"]==1003 and a["borncorner"]==[12,13,12,13] and a["graphicname_raw"]==16038 and a["createnum_raw"]==1 and a["dir_raw"]==4,"actual static creation coordinates")
    need(a["enemy_template"]=="npcgen_petshop" and a["argument_relative_path"]=="genout/ps_1003_12_13","exact pointer")
    p=d["linked_actual_original_argument"]
    need((p["path"],p["bytes"],p["sha256"])==("gmsv/data/npc/genout/ps_1003_12_13",397,"f4759c08d7391033b8fcee4d2580832c77e8210d637009b608be460b51285cbe") and p["referenced_original_file_fully_read"] is True and p["cp950_decode_roundtrip"] is True,"argument file real")
    c=d["client_map_source_cell"]
    need((c["x"],c["y"],c["plane_u16_values"],c["map_sha256"])==(12,13,[5001,0,49152],"fc3037a1850c8baf06ad5874a4cb49ca5e13e9315c020f64c019417c33b694e6") and c["third_plane_gameplay_semantics_proven"] is False,"actual source cell, no collision claim")
    s=d["source_scope"]
    need(s["same_preserved_mixed25_carrier"] is True and s["one_explicit_original_config_to_argument_link_qualified"] is True,"exact only static link")
    for f in ("NPC_original_runtime_instantiated","original_dialogue_executed","original_pet_sale_or_storage_executed","original_pixel_for_graphic16038_recovered_this_turn","official_2003_or_tw10_same_deployment_proven","original_game_world_entered","original_code_or_text_committed_to_public_Git"):
        need(s[f] is False,"unverified game condition "+f)
    need(s["completion_percent"] is None,"no completion percentage")
    q=d["private"]
    need(q["archive_bytes"]==5665 and q["archive_sha256"]=="d7db30ac0a292c37f323e800e26e9bad61f80922d21a5a71c1e7ac3838b7c818" and q["all_5_members_crc_verified"] is True and q["original_src_bytes_public"] is False,"private unchanged")
    return {"floor_id":1003,"static_source_coordinate":[12,13],"same_carrier_original_parameter_link":True,"original_world_entered":False}

if __name__=="__main__":
    print(json.dumps(validate(json.loads(REPORT.read_bytes())),ensure_ascii=False))
