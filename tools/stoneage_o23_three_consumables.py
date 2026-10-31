"""O23 public source-only derived witnesses: original bytes and art stay PRIVATE."""
import json
from pathlib import Path
REPORT=Path(__file__).resolve().parents[1]/"research/recovered/STONEAGE-O23-THREE-CONSUMABLE-SOURCE-PIXELS-R1.json"
PIN_FILE={
"preserved_mixed25_rar":(361255180,"d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5"),
"original_itemset.txt":(3392473,"a415e78f9aab2e5ea5ca92ecb7430253f7be1ba7c876d6b0bb6d067b1b466688"),
"TW10_ADRN":(10079680,"47254c0ff904d363fb5c3c5297edf553c8eaf24cd933f346d8ce7aabed4155c8"),
"TW10_REAL":(315842228,"408e6ee05c83354349691937da2ad8f7488ac10f65f07e6681b7d92cb1c9ed13"),
"TW10_Palet1":(708,"32870080c47537a59beaf770b6df7bd79820fd52a23825058460900494f0b4b0")}
PIN_ITEMS=(
(1234,1229,328408,212,"409ffc21456e7b73abf5f635afdd4de6049099655b21d9ec807cb1b066be1dee","小塊肉","ITEM_useRecovery",20,24008,6926,525,"79f434e8885c63025f5a50b1a4e77f21487669e6881cbc6b6f5fe621234e0acb","918d36e49cea3c18a9f0af5bd6cd3d1f9dae9941afe500aebaf31d7f4418de6f","75df3bcf7a37aaaf01f3c6c6b4a017fb9d0ce44b6fe03f4c32ab8ed673b6ac89","68d2b989e84fabdd9e02a225311b8c05fb34ddae6aef158fb32a91a957dd2acd"),
(1247,1242,331271,224,"2ac2ff5a87a3845216abef579de0c62a11eb769974916860e4d808f5f0c55f5d","治療中毒的肉","ITEM_useStatusRecovery",120,24043,6961,1629,"df055db71bbd048b5fabf5e59e64f5e156145e38101c2882e832f22f7574ad87","7c310ba3b0cb218fbd167f953cfa0b32b6b7a9f13c94153786dfe51033c4f80f","8ff619dd140ac10726b9c1f76dc78f1e6eface469b4fb823ded9e30b803c9b43","cb4f4095f4a081673b1859736bfa360066185e49e984f1fa8b11891008cbaaa5"),
(1530,1505,395774,223,"b0f0732e5f136853f70594d90e82237b3cd4d898981ac908f0467337c3305fc9","復活藥(100)","ITEM_useRessurect",100,23021,6557,303,"ad6db3666ca609d2ea4add83d08380e043e0ffc439862795543fb3159594d044","46b4ee8e8266b8dd85bb79e8457c22cdc38f11a3c59227f412481b5cf7f06183","63913bfa7c61f2282f07923764fa20939d91e02d6d331510adad3fa6c4272479","68fb75042f7fbbf3446539a53252530c073d38390bbe68b0a6d9d51166d272e8"))
FALSE=(
"same_deployed_official_item_master_proven","native_item_selector_proven","mixed25_original_REAL_directly_extracted_this_turn",
"original_treatment_healing_poison_cure_or_resurrection_executed","runtime_price_or_inventory_change_proven",
"original_client_world_entered","official_TW10_or_1999_item_names_authenticated",
"native_palette_and_occlusion_verified","copyrighted_original_payloads_in_public_repo")
def need(ok,why):
    if not ok:raise ValueError(why)
def validate(d):
    need(d["schema"]=="stoneage.o23.three_consumable_source_pixels.r1","schema")
    need(d["source_main_head"]=="05cfce6cfeda9d0a8b4e014241d53140a3a33efe" and d["source_main_tree"]=="77de03ce1ca3f36f54b3c2866b84e47d330b5f63","source HEAD/tree baseline")
    need(d["full_current_original_blob"]=="20050acf279a01555ab06a381dfcdc936bd381a6","original 2.7MB CURRENT preserved")
    need(d["evidence_scope"]=="PRESERVED_MIXED25_ITEMSET_TO_SEPARATE_TW10_ORIGINAL_ADRN_REAL_NUMERIC_ALIAS_CANDIDATES_NOT_SAME_DEPLOYED_BUILD","era/provenance separation")
    src=d["source_files"]
    need(set(src)==set(PIN_FILE),"five exact sources")
    for k,expected in PIN_FILE.items():need((src[k]["bytes"],src[k]["sha256"])==expected,"whole source "+k)
    need(src["original_itemset.txt"]["parsed_item_rows"]==13252,"complete item schema count")
    need(src["TW10_ADRN"]["record_count"]==125996,"original TW1 ADRN total")
    items=d["items"];need(len(items)==3,"three finite items")
    for row,expected in zip(items,PIN_ITEMS):
        vals=(row["item_id"],row["source_physical_line"],row["source_byte_offset"],row["source_original_row_bytes"],row["source_row_sha256"],row["source_original_name"],row["original_callback_string"],row["original_cost_raw"],row["original_imagenumber"],row["tw10_unique_alias_target_bitmap"],row["alias_RD_bytes"],row["actual_alias_RD_sha256"],row["alias_candidate_canvas_RGBA_sha256"],row["literal_physical_RD_sha256"],row["literal_canvas_RGBA_sha256"])
        need(vals==expected,"one exact original source item/alias/pixel witness "+str(expected[0]))
        need(row["literal_physical_control_bitmap"]==row["original_imagenumber"],"literal physical counterexample number")
        need(row["tw10_unique_alias_target_bitmap"]!=row["literal_physical_control_bitmap"],"two namespaces remain distinct")
        need(row["actual_alias_RD_sha256"]!=row["literal_physical_RD_sha256"],"distinct actual original RD source pixels")
        need(row["source_original_name"] in row["source_original_name"],"nonempty original short label")
    i=d["identity_controls"];need(all(v is True for v in i.values()),"all six source and independent pixel controls")
    br=d["actual_private_browser"]
    need(br["Chromium"]=="144.0.7559.96" and br["real_original_pixel_PNG_canvas_states_verified"]==6 and br["canvas_size"]==[160,160],"actual real-original image browser")
    need(br["all_six_full_RGBA_equal_independent_Python"] is True and br["all_three_alias_literal_toggle_zoom_reset_verified"] is True,"browser independent comparison")
    need(br["JS_errors"]==0 and br["external_HTTP_requests"]==0 and br["user_file_open_on_local_machine_verified"] is False,"no invented filesystem test")
    need(br["screenshot_png_sha256"]=="6d1bbe9470f42bf92426c3bff3300978cfc925cc18af5964c33cf6d0eaaf8da3","screenshot identity")
    need(br["observer_HTML_sha256"]=="bc48cfaf5a860581ee19d70c5d1e63cd3db31c376c32f98a67d67c837931bf9b","source viewer identity")
    ar=d["private_archive"];need((ar["bytes"],ar["sha256"],ar["member_count"])==(193578,"63092c83c4688fe3f451239013844bfc34709e87de51e375007525e92307798b",25),"actual private ZIP")
    need(ar["all_zip_member_CRC_verified"] is True and ar["original_client_binary_text_image_publicly_committed"] is False,"private custody")
    limit=d["limits"]
    need(set(limit)==set(FALSE)|{"overall_percent"},"no unnoticed source promotion")
    need(all(limit[k] is False for k in FALSE) and limit["overall_percent"] is None,"unsupported old-game and release claims")
    need(d["next"]=="O24_ONE_NEW_ORIGINAL_BATTLE_OR_MAP_EVENT_VISIBLE_MATERIAL_OR_ROTATE_22_DOMAINS","bounded next content domain")
    return {"original_item_rows":3,"TW1_original_RDs_actually_decoded":6,"actual_browser_canvas_states":6,"original_game_world_entered":False}
if __name__=="__main__":
    print(json.dumps(validate(json.loads(REPORT.read_bytes())),ensure_ascii=False))
