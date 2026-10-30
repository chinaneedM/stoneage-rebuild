"""O7 PUBLIC derived-evidence gate; private original commercial assets never read here.

Replays archived numerical claims only. Does NOT reconstruct historical shop runtime.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATHS={
 "o6":"research/recovered/STONEAGE-O6-PRIVATE-ASSET-EXPORT-ACCEPTANCE-R1.json",
 "scene24":"research/recovered/STONEAGE-SCENE24-SHOP-ITEM-IMAGES-R1.json",
 "scene25":"research/recovered/STONEAGE-SCENE25-ROOM-SHOP-INTEGRATION-R1.json",
 "o7":"research/recovered/STONEAGE-O7-SHOP-ITEM-STATS-AND-SCENE-ACCEPTANCE-R1.json"
}
EXPECTED=(
 (0,"小斧頭",20033,6006,65,0,9,-3,-3),
 (4,"萊伊卡Lv1斧頭",20032,6005,105,0,7,-2,-2),
 (10,"普通普通的斧頭",20013,5986,260,10,14,-5,-5)
)

def require(x,message):
 if not x:raise ValueError(message)

def read():
 return {k:json.loads((ROOT/v).read_text(encoding="utf-8")) for k,v in PATHS.items()}

def validate(g):
 o6,r24,r25,o7=[g[k] for k in ("o6","scene24","scene25","o7")]
 require(o7["schema"]=="stoneage.o7_preserved_shop_item_description_numeric_crosssource.r1","wrong O7 receipt")
 require(o7["provenance"]=="PRESERVED_COMMUNITY_MIXED25_NOT_OFFICIAL_TW1","false official provenance")
 require(o7["original_itemset_source_sha256"]==r24["source_members"]["itemset.txt"]["sha256"],"itemset source SHA drift")
 require(o7["original_shop_argument_source_sha256"]==r24["source_members"]["npc/genout/ss_1001_17_13"]["sha256"],"shop parameter SHA drift")
 require(o7["room_source_map_dat_sha256"]==o6["result"]["input_source_raw_map_DAT_sha256_1001"],"room DAT source SHA drift")
 require(o7["private_original_input_zip_sha256"]["o6"]==o6["private_output"]["zip_sha256"],"O6 private source changed")
 require(o7["private_original_input_zip_sha256"]["scene24"]==r25["parents"]["items_archive"]["sha256"],"SCENE24 private source changed")
 require(o7["private_original_input_zip_sha256"]["scene25"]=="5adf2c4ef0d8bd770bb0d0311da80976371dc00246601f055c47264a90f94663","SCENE25 private source changed")
 b=r25["binding"];s=o7["shop"];bounds=s["o6_room_sample_bounds"]
 require(b["floor"]==s["floor"]==1001 and b["xy"]==s["xy"]==[17,13],"original shop source coordinate drift")
 require(b["functionset"]==s["functionset"]=="ItemShop","original shop source template drift")
 require(bounds==[7,12,13,18],"original room sample bounded range changed")
 require(not(bounds[0]<=s["xy"][0]<=bounds[2] and bounds[1]<=s["xy"][1]<=bounds[3]),"shop coordinate unexpectedly inside proven room sample")
 require(s["shop_inside_o6_sample"] is False,"false shop NPC visibility")
 require(s["original_stock_count"]==r24["original_stock_count"]==17,"shop original stock count drift")
 require(s["displayed_first_3_item_ids"]==[0,4,10],"source first three ids reordered")
 require(s["buy_rate_original_text"]=="1.0" and s["sell_rate_original_text"]=="0.2","source parameters changed")
 require(s["native_runtime_prices_verified"] is False and r24["computed_runtime_prices"] is None,"shop runtime misattributed")
 require(len(r24["items"])==len(r25["items"])==len(o7["items"])==3,"original item bounded count changed")
 for i,(item_id,name,img,alias,cost,level,attack,defense,agility) in enumerate(EXPECTED):
  x,y,z=r24["items"][i],r25["items"][i],o7["items"][i]
  require((x["id"],x["name_original"],x["imagenumber"],x["numeric_fields"]["cost"],x["numeric_fields"]["level"])==(item_id,name,img,cost,level),"source item original row mismatch")
  require((z["id"],z["name"],z["imagenumber"],z["candidate_bitmap"],z["source_cost"],z["source_level"])==(item_id,name,img,alias,cost,level),"O7 source item identity/price mismatch")
  require(z["original_line_1based"]==item_id+1 and z["row_sha256"]==x["row_sha256"]==y["source_row_sha256"],"source item raw row identity mismatch")
  require(x["alias_candidate"]["alias_value"]==img and x["alias_candidate"]["bitmapno"]==alias,"source numeric alias mismatch")
  require(x["literal_bitmap_control"]["bitmapno"]==img and x["literal_bitmap_control"]["RD_sha256"]!=x["alias_candidate"]["RD_sha256"],"source alias vs physical bitmap conflation")
  require(z["source_candidate_png_sha256"]==y["PNG_sha256"]==x["alias_candidate"]["palette_candidates"]["1"]["PNG_sha256"],"original private PNG fingerprint mismatch")
  require(z["png_wh"]==[x["alias_candidate"]["width"],x["alias_candidate"]["height"]],"source PNG dimensions mismatch")
  require(z["description_modifiers"]=={"attack":attack,"defense":defense,"agility":agility},"original text modifier mismatch")
  require(z["raw_duplicate_numeric_columns_0based"]==[37,38,39,40,41,42]
    and z["raw_numeric_values"]==[attack,attack,defense,defense,agility,agility],"source item raw numeric column proof mismatch")
  require(z["source_cost"]==cost and z["source_level"]==level,"source item raw prices/levels mismatch")
 p=o7["private_O7"]
 require(p["inherited_O6_original_files_unchanged"]==o6["private_output"]["zip_entries"]==280,"O6 original 280 asset data changed")
 require(p["added_3_original_png_candidates"]==3 and p["total_original_PNGs"]==o6["result"]["private_png_count"]+3==278,"original PNG count drift")
 require(p["zip_members"]==287 and p["zip_bytes"]==2179790 and len(p["zip_sha256"])==64,"O7 private ZIP custody mismatch")
 require(p["private_zip_library_retrieved_and_byte_equal"] and p["zip_CRC_zero_errors"],"private Library source custody unverified")
 require(p["shop_readonly_json_sha256"]=="fa73a013d1d9750be03f020bae6c115e94802278708233589ef35a104e48082b","bounded shop JSON fingerprint mismatch")
 require(p["pet_frame_positions_visited_in_real_browser"]==o6["result"]["pet_ordered_frame_occurrences"]==352
  and p["unique_pet_bitmaps_decoded_in_real_browser"]==o6["result"]["pet_numeric_original_pngs"]==208,"private source pet replay counts changed")
 require(p["shop_candidate_PNGs_decoded_in_real_browser"]==3 and p["shop_source_item_cards"]==3,"private browser original shop image sample incomplete")
 require(p["incorrect_source_warp_rejected"] is True and p["two_way_manual_door_route_success"] is True,"historical coordinate negative gate changed")
 require(p["external_network_requests"]==p["javascript_errors"]==0,"browser external request or script errors")
 require(p["original_game_exe_executed"] is False and p["original_O7_html_file_url_navigation_verified"] is False,"false original native/local open execution")
 require(not any(o7["historical_limits"].values()),"original historical claim falsely promoted")
 require(r24["native_imagenumber_namespace_verified"] is False and r25["original_transaction_verified"] is False,"original server runtime misrepresented")
 require(o7["new_original_primary_source_bytes_acquired"]==0 and o7["overall_percent"] is None and o7["stage_a"]=="7 PARTIAL + 2 OPEN","completion claimed without source")
 return {"O7_PUBLIC_DERIVED_ORIGINAL_ITEM_GATE":"PASS",
         "source_item_ids":[x[0] for x in EXPECTED],
         "source_modifiers":[[x[6],x[7],x[8]] for x in EXPECTED],
         "original_shop_NPC_in_verified_sample":False,
         "private_browser_pet_positions_as_archived":352,
         "original_copyright_PNGs_present_in_public_CI":False,
         "historical_game_world_entered":False}

if __name__=="__main__":
 print(json.dumps(validate(read()),ensure_ascii=False,sort_keys=True))
