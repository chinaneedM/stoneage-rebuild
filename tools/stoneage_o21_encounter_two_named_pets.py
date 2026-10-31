"""O21 material boundary guard: public derived records only, no original art/text."""
import json
from pathlib import Path
REPORT=Path(__file__).resolve().parents[1]/"research/recovered/STONEAGE-O21-ENCOUNTER-TWO-NAMED-PET-SOURCE-R1.json"
SHA=lambda x:isinstance(x,str) and len(x)==64 and all(c in "0123456789abcdef" for c in x)
PINS={
"encount.txt":(43420,"70bbd997d98508a0587df183b5bdd48222ff42db91bf21bea632e0ed6f2fea87"),
"group1.txt":(70176,"4a02f2a3fa3d2dcf5589d8a2a560313c35d5a0a7e5e0589cc8df5f7df159ea8f"),
"enemy.txt":(222463,"cc7418d3b6726f1c458fef9e44a24696d05f076b67c62a56ed2293e26ae63bb6"),
"enemybase.txt":(147750,"1be7d5226798f7abaabe1f1e74aa1533fcd10e3eaf43f6497d63afa91df3e8b7")}
def require(x,msg):
    if not x: raise ValueError(msg)
def validate(d):
    require(d["schema"]=="stoneage.o21.bounded_original_encounter_two_named_pet_pixel_view.r1","schema")
    require(d["source_scope"].endswith("NOT_SAME_DEPLOYMENT"),"cross-era qualification")
    require(d["source_head"]=="a3133faf5b341d4524f54f5d6c433621dc5aa26b" and d["source_tree"]=="4b0a8f16de7e00b0958087737d3cef8a39b029fd","original remote baseline")
    require(d["current_preserved_blob"]=="20050acf279a01555ab06a381dfcdc936bd381a6","original CURRENT not replaced")
    for k,(n,s) in PINS.items():
        require((d["original_sources"][k]["bytes"],d["original_sources"][k]["sha256"])==(n,s),"original source "+k)
    require(d["original_sources"]["TW10_SPR"]["sha256"]=="53d5b2d40453a30fd1569637ebf0db7b3010542b00970ec83af0295a3b3ae31a","verified TW1 raw SPR")
    require(d["original_sources"]["TW10_REAL"]["sha256"]=="408e6ee05c83354349691937da2ad8f7488ac10f65f07e6681b7d92cb1c9ed13","verified TW1 RD REAL")
    e=d["bounded_original_encounter"]
    require((e["raw_row_index"],e["source_line_number"],e["floor"],e["rectangle_inclusive"])==(21,1,100,[582,399,783,560]),"original area identity")
    require(e["source_row_sha256"]=="78dd537235bee8d0f74fdf610a7cb46915c1d949b39de6f9dfeebba1ee8f9358","original encounter row")
    require(e["two_selected_positive_group_weight_pairs"]==[[88,50],[91,50]] and e["selected_groups_only_not_all_encounter_groups"] is True and e["trigger_executed"] is False,"bounded encounter never executed")
    rows=d["source_named_pet_links"]
    require(len(rows)==2 and [r["pet_name_original_CP950"] for r in rows]==["昆伊","凱比特"],"one two-pet finite set")
    for i,r in enumerate(rows):
        expected=[(88,119,113,100297,287,1032,8,109539),(91,122,114,100298,288,1096,16,109771)][i]
        require(tuple(r[k] for k in ("group_id","enemy_id","template_no","enemybase_IMGNUMBER","TW10_SPR_group_index","TW10_SPR_total_frame_positions","selected_frame_count","selected_first_frame_bitmapno"))==expected,"exact chain "+str(i))
        require(r["CP950_and_Big5_same"] is True and r["TW10_SPR_56_animation_records"]==56 and r["selected_direction"]==r["selected_action_raw"]==0,"exact raw source "+str(i))
        for k in ("original_group1_row_sha256","original_enemy_row_sha256","original_enemybase_row_sha256","TW10_SPR_group_segment_sha256","selected_original_RD_sha256","full_"+str(expected[6])+"_frame_canvas_sha_list_digest"):
            require(SHA(r.get(k)), "source SHA "+k)
    require(rows[0]["full_8_frame_canvas_sha_list_digest"]=="12f69df0d0cef15c1b38ab57242b8850b45bcb27a1e4a79bb7859ff4ff0d54b7","eight original frame identities")
    require(rows[1]["full_16_frame_canvas_sha_list_digest"]=="0ae909c748c4514c8f20288e2f8f4d5b7f57f3ef4bfc8cb3e4ffc56e64afba02","sixteen original frame identities")
    p=d["original_pixel_replay"]
    require(p["source_24_frame_ordered_canvas_digest"]=="6a1ddd9b23a3d2434a146bd3ec315e47a7c29a89b50c53547438b6b7c8802edf","24 source frame evidence")
    for k in ("two_independent_RD_decoders_all_24_states_match","24_frame_pixels_all_same_actual_chromium_canvas","manual_next_wrap_previous_zoom_reset_observed"):
        require(p[k] is True,"actual pixel replay "+k)
    require(p["browser_JS_errors"]==p["browser_external_requests"]==0 and p["user_local_file_navigation_verified"] is False,"browser boundaries")
    q=d["private_custody"]
    require((q["private_zip_bytes"],q["private_zip_sha256"],q["private_zip_member_count"])==(133437,"551a4008f214b10b7566b2c311b2d383d3683a02f3a818f6e4263eefd7ef1e73",29),"private archive actual")
    require(q["private_zip_all_CRC_pass"] is True and q["copyrighted_client_assets_in_public_Git"] is False,"private custody")
    lim=d["strict_boundaries"]
    for k in ("TW10_official_named_species_identity_proven","mixed25_and_TW10_same_live_build_proven","historical_gameplay_encounter_executed","original_game_world_entered","native_FPS_proven","source_audio_events_proven","original_encounter_probability_semantics_proven"):
        require(lim[k] is False,"do not promote unknown "+k)
    require(lim["overall_completion_percent"] is None,"no percent")
    return {"later_preserved_named_pet_templates":2,"original_TW10_first_selected_frames_checked":24,"original_game_world_entered":False}
if __name__=="__main__":
    print(json.dumps(validate(json.loads(REPORT.read_bytes())),ensure_ascii=False))
