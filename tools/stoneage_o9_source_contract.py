"""O9 public-source receipt verifier: private game resources are never loaded by CI."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]/"research/recovered/STONEAGE-O9-ORIGINAL-FULL-ROOM1001-ACCEPTANCE-R1.json"
SOURCE={"room_DAT":"62dbef1614ede0ba032ca9c69cbfdc3d43938e45baba78701885790937b86b90",
"tw1_ADRN":"47254c0ff904d363fb5c3c5297edf553c8eaf24cd933f346d8ce7aabed4155c8",
"tw1_REAL":"408e6ee05c83354349691937da2ad8f7488ac10f65f07e6681b7d92cb1c9ed13",
"tw1_Palet1":"32870080c47537a59beaf770b6df7bd79820fd52a23825058460900494f0b4b0"}
IDS=(401,5000,5001,5002,5005,5006,5007,5008,5009,5010,5011,5012,5013,5015,5016,5017,5018,5019,5020,5021,5024,5026,12019,12020,12021,12022,12023,12613,12614,12615,12619,12620,12621,12656,12657,12804,12815,12845)
def need(v,msg):
    if not v: raise ValueError(msg)
def validate(d):
    need(d["schema"]=="stoneage.o9.original_full_room_1001.source_only.r1","schema")
    need(d["scope"]=="PRESERVED_MODIFIED_MIXED25_ROOM_WITH_VERIFIED_TW1_RESOURCE_BYTE_PREFIX_NOT_OFFICIAL_TW1_WORLD","source scope")
    need(d["source_sha256"]==SOURCE and d["current_state_original_blob"]=="20050acf279a01555ab06a381dfcdc936bd381a6","original bytes pin")
    need(tuple(d["map_graphic_ids"])==IDS and len(set(IDS))==38,"source ID domain")
    room=d["room"]
    need([room[k] for k in ("width","height","plane_cells_per_layer","tile_appearances","part_appearances","visible_appearances","distinct_map_graphics")]==[30,30,900,107,26,133,38],"original map coverage")
    need(room["third_plane_counts"]=={"49152":818,"16384":80,"49155":2} and room["third_plane_collision_proven"] is False,"third plane unknown")
    need(d["o8_overlap"]=={"original_30_cell_layer_map_triples_exact":30,"new_outside_o8":103,"original_o8_PNG_10_full_bytes_exact":10,"other_prior_PNG_reused":8,"new_private_images":20},"O8 material increment")
    facts=d["independent_actual_local_original_source"]
    need(len(facts)==7 and all(v is True for v in facts.values()),"source replay witness")
    image=d["image"]
    need(image["dimensions"]==[647,617] and image["candidate_full_RGBA_SHA256"]=="9a1f2a8e9c635ec961c43e53929e44ea9ed6c06ddd465c679806751dfef4d2fb" and image["native_palette_and_draw_order_authenticated"] is False,"candidate canvas not native")
    need(len(image["candidate_layer_RGBA_SHA256"])==2 and all(len(x)==64 for x in image["candidate_layer_RGBA_SHA256"]),"candidate layer")
    b=d["browser"]
    need(b["real_source_PNG_memory_page_rendered"] is True and b["layer_zoom_coordinates_reset_pass"] is True and b["js_errors"]==0 and b["external_HTTP_requests"]==0,"actual browser source")
    need(b["local_file_error"]=="ERR_BLOCKED_BY_ADMINISTRATOR" and b["user_local_file_verified"] is False,"failed file attempt")
    p=d["private"]
    need(p["zip_sha256"]=="2340ee84f4df6a92d5a9e8f4bcea851f3f9e6e78e1c293629429c4b7e2ce1306" and p["zip_bytes"]==3969208 and p["members"]==328 and p["prior_o8_members_bytes_unchanged"]==297,"private complete custody")
    need(p["library_upload_and_readback_full_bytes_equal"] is True and p["library_path"].startswith("/石器时代/"),"private durable upload")
    need(all(len(p[k])==64 for k in ("private_derived_report_sha256","private_independent_report_sha256","private_browser_report_sha256")),"report hashes")
    status=d["status"]
    for k in ("original_game_world_entered","original_client_executed_this_round","official_TW1_map_deployment_verified","native_camera_collision_sprite_selector_verified","NPC_shop_or_trade_executed","private_art_in_public_git"):
        need(status[k] is False,k)
    need(status["stage_A_partial"]==7 and status["stage_A_open"]==2 and status["stage_B_gated"] is True and status["wiki_gated"] is True and status["R79_paused_nonblocking"] is True and status["overall_completion_percent"] is None,"conservative stage status")
    return {"original_source_placements":133,"distinct_graphics":38,"new_placements":103,"original_world_entered":False}
def main():
    print("STONEAGE_O9_DERIVED_SOURCE_ONLY=PASS",json.dumps(validate(json.loads(R.read_text(encoding="utf-8")))))
if __name__=="__main__":main()
