"""Public source-only O10 gate. Original client artwork remains PRIVATE."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/recovered/STONEAGE-O10-VILLAGE-EXPANDED-SOURCE-ACCEPTANCE-R1.json"
PINS={
"P3H":(372626292,"3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24"),
"MAP":(153608,"94b19cb59d72b7b48da70d2741ba68516caad970297fd48ed11ef720fa3ea97e"),
"ADRN":(10079680,"47254c0ff904d363fb5c3c5297edf553c8eaf24cd933f346d8ce7aabed4155c8"),
"REAL":(315842228,"408e6ee05c83354349691937da2ad8f7488ac10f65f07e6681b7d92cb1c9ed13"),
"SAP":(708,"32870080c47537a59beaf770b6df7bd79820fd52a23825058460900494f0b4b0"),
"O9ZIP":(3969208,"2340ee84f4df6a92d5a9e8f4bcea851f3f9e6e78e1c293629429c4b7e2ce1306"),
}
PRIVATE_ZIP_SHA="b3f04b571b4b64b654ee4f314a33d6ab1a85e2d8a8ddaf21b2c102fc5a45c197"
FULL_RGBA_SHA="098f369a7c926e6d676abce65c0c6e8407fedf4ff751a0d96689936b64794532"
EXPECTED_IDS=(100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,162,164,165,167,168,170,172,173,174,175,176,177,179,180,181,182,183,184,185,186,187,188,189,190,191,192,200,201,202,203,204,205,206,207,208,209,211,213,214,215,216,217,218,219,221,223,260,261,262,263,264,265,266,267,268,269,270,273,274,275,276,277,279,280,281,282,283,285,286,287,288,289,290,291,293,294,295,360,361,362,363,364,365,367,372,373,375,376,377,378,381,383,385,386,387,389,390,391,392,394,400,401,402,403,404,405,406,407,414,416,418,424,426,429,798,799,800,801,802,804,809,811,812,814,815,816,820,822,824,825,826,827,828,830,832,10012,10130,10137,10138,10139,10142,10204,10214,11020,11024,12837,12843,12845,13010)
def need(ok,message):
    if not ok: raise ValueError(message)
def validate(d):
    need(d["schema"]=="stoneage.o10.expanded_1000_village.original_source_derived.r1","schema")
    need(d["scope"]=="PRESERVED_MIXED25_MAP1000_SOURCE_TILE_LAYOUT_CROSSSOURCE_TW1_ACTUAL_RD_PIXELS_NOT_OFFICIAL_TW1_WORLD","source scope")
    need(d["old_complete_current_blob"]=="20050acf279a01555ab06a381dfcdc936bd381a6","CURRENT preserved")
    for k,pin in PINS.items():
        need((d["original_source_pins"][k]["bytes"],d["original_source_pins"][k]["sha256"])==pin,"source pin "+k)
    m=d["material_delta"]
    need(m["original_map_full_dimensions"]==[160,160] and m["source_view_inclusive"]==[55,89,73,113] and m["view_cell_count"]==475,"source region")
    need((m["actual_map_tile_and_parts_appearances"],m["distinct_ADRN_graphic_aliases"],m["exact_old_O4_placements"],m["old_O4_distinct_graphic_ids"],m["new_outside_old_O4_placements"],m["additional_distinct_graphic_ids_vs_O4"])==(492,183,85,55,407,128),"material delta counts")
    need(tuple(m["source_graphic_ids"])==EXPECTED_IDS and len(set(m["source_graphic_ids"]))==183,"exact numeric original aliases")
    need(m["original_O4_view_inclusive"]==[60,96,66,106] and m["third_plane_source_value_counts"]=={"49152":469,"49155":6} and m["third_plane_semantics_verified"] is False,"unverified game plane")
    a=d["actual_private_replay"]
    need(len(a)==9 and all(v is True for v in a.values()),"actual source+independent replay")
    v=d["candidate_visual"]
    need(v["image_size"]==[1408,1055] and v["world_bounds"]==[4576,360,5984,1415] and v["full_pixel_rgba_sha256"]==FULL_RGBA_SHA,"full candidate pixel source")
    need(v["full_PNG_sha256"]=="f23098c474c321d28799a37b87ad372fc73aac90b4b689d3d2c22726586461fd" and v["scene_native_draw_or_palette_proven"] is False,"candidate is not native")
    b=d["browser"]
    need(b=={"original_PNG_same_bytes_in_memory":True,"real_browser_positive_cases":8,"js_errors":0,"external_http_requests":0,"file_navigation_error":"ERR_BLOCKED_BY_ADMINISTRATOR","end_user_file_open_verified":False},"actual browser plus file block")
    c=d["private_custody"]
    need(c["zip_bytes"]==7764347 and c["zip_sha256"]==PRIVATE_ZIP_SHA and c["zip_members"]==888 and c["prior_O9_members_unchanged"]==328 and c["added_private_members"]==560,"private artifact source")
    need(c["private_original_report_sha256"]=="845175343b2ecf1e93060bd055008dfd659e4feb1d635720afa1b642441d4e2e" and c["browser_acceptance_sha256"]=="1163d78e420dbc2fdd0dbf2dba82489563718e686acba72a603a4c7daa3ff26c","private reports")
    need(c["archive_actual_postzip_independent_source_replay"] is True and c["contains_original_full_client_REAL_or_EXE"] is False,"bounded archived bytes")
    need(c["persistent_library_upload_completed"] is False and c["persistent_library_error"]=="CONTAINER_SESSION_EXPIRED" and c["current_conversation_artifact_created"] is True,"no fake persistent library")
    hist=d["historical_guards"]
    for k in ("original_native_client_map_world_entered","official_TW1_or_JSS1999_deployment_map_verified","original_collision_or_walkability_verified","original_NPC_dialogue_trade_or_battle_executed","original_audio_event_association_verified","original_proprietary_assets_committed_to_public_git"):
        need(hist[k] is False,k)
    need(hist["stage_A_partial"]==7 and hist["stage_A_open"]==2 and hist["stage_B_gated"] is True and hist["wiki_gated"] is True and hist["R79_paused_nonblocking"] is True and hist["overall_completion_percent"] is None,"project gates")
    return {"actual_placements":492,"distinct_original_source_graphics":183,"new_outside_old_view":407,"independent_pixel_evidence":True,"native_game_world_entered":False}
def main():
    print("STONEAGE_O10_SOURCE_ONLY=PASS",json.dumps(validate(json.loads(REPORT.read_text(encoding="utf-8")))))
if __name__=="__main__":main()
