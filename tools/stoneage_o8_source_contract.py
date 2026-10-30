"""O8 PUBLIC metadata replay. Original MAP DAT, 11 PNGs and private browser stay in Library."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FILES={
 "o8":"research/recovered/STONEAGE-O8-ORIGINAL-SHOP-CROP-ACCEPTANCE-R1.json",
 "o7":"research/recovered/STONEAGE-O7-SHOP-ITEM-STATS-AND-SCENE-ACCEPTANCE-R1.json",
 "o6":"research/recovered/STONEAGE-O6-PRIVATE-ASSET-EXPORT-ACCEPTANCE-R1.json",
 "r14":"research/recovered/STONEAGE-SCENE14-ROOM-SHOP-SOURCE-R1.json"
}
def require(cond,why):
 if not cond:raise ValueError(why)
def read():
 return {k:json.loads((ROOT/v).read_text(encoding="utf-8")) for k,v in FILES.items()}
def validate(v):
 a,b,c,d=(v[k] for k in ("o8","o7","o6","r14"))
 require(a["schema"]=="stoneage.o8_original_shop_source5x5_private_acceptance.r1","O8 schema mismatch")
 require(a["source_grade"]=="PRESERVED_MIXED25_COMMUNITY_MODIFIED_NOT_OFFICIAL_TW1","official lineage falsely promoted")
 require(a["private_inputs"]["O7"]["sha256"]==b["private_O7"]["zip_sha256"],"O7 original private parent mismatch")
 require(a["private_inputs"]["SCENE14"]["sha256"]=="7684267ab528d13ceecb23a25632543ae839225607cbda702a32736e4c4d366a","R14 original parent mismatch")
 require(a["raw_1001_DAT_sha256"]==c["result"]["input_source_raw_map_DAT_sha256_1001"]==b["room_source_map_dat_sha256"]==d["source_members"]["client-map/1001.dat"]["sha256"],"source original DAT SHA mismatch")
 require(a["source_map_size"]==[d["map"]["width"],d["map"]["height"]]==[30,30],"source original map geometry mismatch")
 require(a["source_shop_floor"]==d["npc"]["floor"]==1001,"source shop floor mismatch")
 require(a["source_shop_crop"]==[13,13,17,17],"original 5x5 shop crop mismatch")
 require(a["o6_entrance_crop"]==b["shop"]["o6_room_sample_bounds"]==[7,12,13,18],"source prior room crop mismatch")
 require(a["original_shop_tile_occurrences"]==25 and a["original_shop_part_occurrences"]==5 and a["original_shop_placements"]==30,"original 30 source map occurrences incorrect")
 require(a["original_shop_missing_images"]==0 and a["original_shop_unique_bitmap_ids"]==10,"source original view qualification incorrect")
 require(a["existing_entrance_placements"]==c["result"]["room_1001_original_placements"]==27,"O6 entrance placements mismatch")
 require(a["unique_entrance_plus_shop_placements"]==a["existing_entrance_placements"]+a["original_shop_placements"]-len(a["common_exact_source_cell_layer_id_placements"])==52,"source overlap conservation mismatch")
 exp=[[[13,13],"tile",5002],[[13,14],"tile",5000],[[13,15],"tile",5009],[[13,16],"tile",5015],[[13,17],"tile",5002]]
 require(a["common_exact_source_cell_layer_id_placements"]==exp,"original five source cell-layer-id overlaps altered")
 # The actual original PNG bytes were independently compared in private source replay;
 # public CI verifies immutable archived bitmap hashes and facts, not the private pixels.
 expected={"5000":"8039bdc50d26aa982eb704c52579e08bd4f5fd812c01e5a88db06ca7f0c85de6",
 "5001":"3e76711987a284141695f92c39e1a4b9c3e42b52a95782f9205879a1839c7bd1",
 "5002":"0951ed531c496fa38d5eb6f686c57cf612f23392ec1166d364f561eb66f37746",
 "5005":"f2226153b85dcf46101f808fbf50fd17a86178b9852e97681b8375f89176d623",
 "5007":"6c0d5ab1bd13c9ae9518a47005655252128c8d24fb523bc99be07f6893228cf0",
 "5009":"65d38fddfd36ebc338d6e46c5fab2a54d2484846bc59e35bf8fa346db584fa93",
 "5015":"4e5b9fea71f1e9e974a1d58efa7fc7fc4a7591da344e34e294a6de0e043eccaa"}
 require(a["shared_bitmap_full_sha256"]==expected,"shared original sprite identity changed")
 require(a["added_private_real_png_sha256"]["npc-5863"]=="b1ef1f5f0ba489197bc7c82518ff5e32cf8b5750207d283b3a7ecd618b6d3c0f","source original candidate NPC PNG SHA mismatch")
 require(set(a["added_private_real_png_sha256"])=={"12619","12620","12621","npc-5863"},"unexpected original bitmap inventory")
 npc=a["source_npc_shop"];old=d["npc"]
 require(npc["xy"]==old["borncorner"][:2]==b["shop"]["xy"]==d["map"]["npc_cell_xy"]==[17,13],"original shop NPC coordinate mismatch")
 require(npc["graphicname"]==old["graphicname"]==16017 and npc["source_template"]==old["template"]=="npcgen_shop","source shop NPC graphic/template mismatch")
 require(npc["source_functionset"]==old["functionset"]=="ItemShop" and npc["candidate_bitmapno"]==5863 and npc["candidate_png_size"]==[36,79],"source NPC bitmap/type mismatch")
 require(npc["overlay_opt_in_default_off"] is True and npc["native_render_authenticated"] is False,"unproven original shop NPC render")
 pv=a["private_archive"]
 require(pv["inherited_O7_files_byte_unchanged"]==b["private_O7"]["zip_members"]==287,"O7 existing private archive changed")
 require(pv["additional_original_PNGs"]==4 and pv["total_private_original_PNGs"]==b["private_O7"]["total_original_PNGs"]+4==282,"original private bitmap conservation")
 require(pv["members"]==pv["inherited_O7_files_byte_unchanged"]+8==297,"private archive member count changed")
 require(pv["bytes"]==2523649 and pv["sha256"]=="092c970f94458d31c5fd933d5db40eb9d3eac705ea6d6e105b812655398accd2","private archived SHA changed")
 require(pv["saved_in_private_Library"] is True and pv["downloaded_again_full_byte_compare_equal"] is True and pv["zip_CRC_errors"]==0,"private source custody incomplete")
 browser=a["private_browser"]
 require(browser["shop_bitmap_PNGs_decoded"]==10 and browser["shop_original_item_PNGs_decoded"]==3 and browser["new_npc_PNG_decoded"] is True,"private source browser pixels unverified")
 require(browser["pet_frame_positions_decoded"]==c["result"]["pet_ordered_frame_occurrences"]==352,"original pet source frame total changed")
 require(browser["distinct_original_pet_bitmap_PNGs_decoded"]==c["result"]["pet_numeric_original_pngs"]==208,"original pet bitmap unique count changed")
 for key in ("manual_source_door_two_way_passed","overlap_source_coordinate_manual_crossing_passed","off_source_bounds_rejected"):
  require(browser[key] is True,"manual source coordinate gate failed "+key)
 require(browser["errors"]==browser["external_requests"]==0,"external network or JS errors falsely accepted")
 require(browser["local_file_direct_launch_verified"] is False and browser["historic_original_game_executable_entered"] is False,"false original client browser/game runtime")
 for name in ("native_original_executable_world_entered","official_TW1_same_map_deployment_authenticated","native_collision_or_occlusion_authenticated","native_shop_dialogue_or_transaction_authenticated","pet_species_spawn_authenticated","copyrighful_original_art_public_distribution"):
  require(a[name] is False,"unproven historical status promoted: "+name)
 require(a["overall_percent"] is None and a["stage_a"]=="7 PARTIAL + 2 OPEN" and a["new_independently_acquired_original_source_file_families"]==0,"false restoration progress promotion")
 return {"result":"PASS_O8_DERIVED_SOURCE_ONLY","source_1001_shop_cells":25,
         "source_1001_shop_occurrences":30,"shared_source_cell_entries":5,
         "unique_two_view_source_placements":52,"native_world_entered":False,"private_images_in_public_ci":False}

if __name__=="__main__":print(json.dumps(validate(read()),ensure_ascii=False,sort_keys=True))
