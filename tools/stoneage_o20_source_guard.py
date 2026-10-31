"""O20 public source-only acceptance; original maps, images and NPC text remain private."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/recovered/STONEAGE-O20-MAP1003-NPC16038-ORIGINAL-PIXEL-OBSERVER-R1.json"
def need(ok,msg):
    if not ok: raise ValueError(msg)
def check(x):
    need(x["schema"]=="stoneage.o20.private_original_NPC_source_visual_candidate_derived.r1","schema")
    need(x["source_main_head"]=="b4edc49ff7f7f9a6afdc40ba57ef508955de32b3" and x["source_main_tree"]=="726dc87fc55a8866bd19c93209105ca564846ee3","fresh source head")
    need(x["preserved_current_blob"]=="20050acf279a01555ab06a381dfcdc936bd381a6","historic CURRENT")
    pins={"MIXED25_RAR":(361255180,"d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5"),"TW10_ZIP":(372626292,"3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24"),"TW10_REAL":(315842228,"408e6ee05c83354349691937da2ad8f7488ac10f65f07e6681b7d92cb1c9ed13")}
    need(set(x["source_carriers"])==set(pins),"sources")
    for name,(size,sha) in pins.items():
        need(x["source_carriers"][name]=={"bytes":size,"sha256":sha,"actually_read_full_sha":True},"source "+name)
    c=x["source_create"]
    need((c["full_create_bytes"],c["full_create_sha256"])==(20491,"d540e9a1354a0f82839cd30ab315a6dee4a3b0299744a0f63ae5ee461c5b587b"),"original create")
    need(c["selected_original_block_sha256"]=="669e06a65e61f2346bf424a35e1a4af03f4e1c5f4089e89295115906271b2fe9","source block")
    need((c["floor"],c["xy"],c["logical_graphic_name"],c["client_same_xy_original_3planes"])==(1003,[12,13],16038,[5001,0,49152]),"original position and source ID")
    need(c["argument_original_sha256"]=="f4759c08d7391033b8fcee4d2580832c77e8210d637009b608be460b51285cbe","actual parameter source")
    g=x["original_TW10_graphic"]
    need((g["logical_alias_16038_occurrences"],g["physical_bitmapno_16038_occurrences"],g["aliased_record_index"],g["bitmapno"],g["rd_bytes"],g["RD_flag"])==(1,1,5884,5884,1885,1),"never confuse alias and bitmap")
    need(g["record_sha256"]=="2f00144c0051a55844c773f03daf408f983b5837b8e76a481de93baf1e3cf25e" and g["rd_sha256"]=="6e738f2865269ec5b26b83ebadfa026b431abe0a319fcbaad4d2c067388986b4","source record and RD")
    need(g["decoded_index_sha256"]=="208f076386f0c801474b1467ea8eb4b1fbdab215e78f7deff17cec3822082468","decoded original index")
    need(g["signed_xy_offsets"]==[-20,-78] and g["wh"]==[36,86] and g["independent_decoders_match"] is True,"original image geometry")
    need(g["physical_record_16038_is_different"] is True and g["physical_record_16038_alias"]==0 and g["physical_record_16038_sha256"]=="47147fce541a80a14393f59773b72ffa4e0a4282c3f996d9b2981dff7079e22b","physical-number counterexample")
    v=x["visual_observer"]
    need(v["basis"]=="PRESERVED_MIXED25_MAP1003_AND_QUALIFIED_TW10_ORIGINAL_RD_PIXELS_MODERN_CANDIDATE","modern source-bound basis")
    need(v["source_palette_reference"]=="TW10 Palet_1.sap" and v["source_render_full_dimensions"]==[695,665],"source canvas")
    need(v["candidate_NPC_original_graphic_size"]==[36,86] and v["NPC_canvas_left_top"]==[137,348] and v["map_canvas_anchor"]==[157,426],"candidate placed at original coordinate")
    need(v["source_background_RGBA_SHA256"]=="f0745bba51f8c71a4e059fc7ce2501733048a56ec18f8efba9df4ff7589740ce" and v["scene_with_NPC_RGBA_SHA256"]=="87ec1e0174df22b61ec2cc84b8b254828937dc3522d55a2f95e742ca3eefa7c0","all complete canvas pixels")
    need(v["scene_with_NPC_PNG_SHA256"]=="0eea7ccfcd9b1da8600ab296bad8ff5c5c399243323b0be725fc2d636c7a26c0","candidate PNG")
    need(v["independent_full_scene_pixel_match"] is True and v["actual_browser_original_png_canvas_match_two_states"] is True and v["actual_browser_original_source_png_count"]==2,"real two-source-image browser checks")
    need(v["actual_browser_reset_restored_pixels"] is True and v["actual_browser_mark_and_2x_controls"] is True and v["browser_JS_error_count"]==0 and v["browser_external_requests"]==0,"browser controls/no network")
    need(v["original_RGBA_palette_runtime_proven"] is False and v["actual_mixed25_ADRN_REAL_original_bytes_revalidated_this_turn"] is False,"no false mixed25 or palette certification")
    q=x["private_custody"]
    need((q["zip_bytes"],q["zip_sha256"],q["zip_entries"])==(775999,"f6141d12871bfba5c6ab805ed081d32ea23e50c9527a6406368f1b8519727e9e",10),"private package identity")
    need(q["private_html_sha256"]=="6451ae6c72381fc7fa8841ba0cd8c05f5773506a7a63c51e9e60a37f4ef879a5" and q["zip_full_CRC_and_original_replay_verified"] is True and q["original_assets_committed_public_Git"] is False,"private original scope")
    for name in ("same_deployed_build_TW10_mixed25_2003_verified","original_native_graphicname_selector_executed","original_NPC_runtime_spawn_verified","original_shop_transaction_executed","original_collision_verified","original_game_world_entered"):
        need(x["limits"][name] is False,"unsupported original game execution: "+name)
    need(x["limits"]["overall_percent"] is None,"unknown overall completion")
    return {"actual_original_RD":1,"source_alias":16038,"physical_bitmap":5884,"browser_original_pixel_states_verified":2,"original_world_entered":False}
if __name__=="__main__":
    print(json.dumps(check(json.loads(REPORT.read_bytes())),ensure_ascii=False))
