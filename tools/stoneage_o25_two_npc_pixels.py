"""O25 immutable source-only boundaries for four actual original TW10 RD candidate pixels."""
import json
from pathlib import Path
REPORT=Path(__file__).resolve().parents[1]/"research/recovered/STONEAGE-O25-TWO-NPC-ORIGINAL-PIXELS-R1.json"
PINS={
 16027:(5873,24981183,1771,40,81,-24,-72,
 "ca040cc6bd9eb7cfa0b843c54c2ccff1b059af962f12bab7205a60e3e3dc9371",
 "e0959846a4ee9ab183da4da9bd53e18f487b17e8e77d0fdeaba263215ef1ffc0",
 "0ba6a59f821827497e44497831adb52092173b81935e53c7b5fe8fe42a55eba4",
 "8e13ae03f41790b3527a2038c9c09c82d306f5e4e545002be2adccdd5dc59c0d",
 "e34de42727fc74dc9267b175fdbf5404820b1fbcbee4f212707b81f8bfe6d5cc",1676,
 "4256b4cece2abc14dda9c1a96648d3e13be121bd2b767c797e2a2bfdf59a116a",
 "f235ac26b65c1d62e4533156a82533dc56befa51b7af8a71da51e4cfd418a97a",
 "902a36f339156063dc179878c4547b4c4a0433e1c7e5aff26ae83f9b47a09661",
 "1f66d89e72b1a9e474d9bca363cf7db56741d52d5d1a88f1ab4e605edf0497c5",
 "41bd548f3d6c28543b7c15fa8fae272f485dca28e742f102a230869d0daedfd2",(52,78)),
 16030:(5876,24985914,2113,40,83,-19,-75,
 "f5c515614a224df5aaa1c59fb462ffdeda152621afbcd832a96bda7b9fb60a21",
 "ae3ceca2f3e0d8412588e9cb900dcac1e31f80014651a900deae1f21d2374de4",
 "873f3344eacefcb5fad7dd57121b54fe2b747298595c94ca84239d6c1410d09f",
 "60e1d27b9f27175782e36242df4702642c192b2a0dcf88eab826c28985667c10",
 "3bf81f70bc5970d28c874ed483ae6d8a56ea35b5697bb98c650957b3cc343abc",1423,
 "484004fa4ca357f1276d543b4dedbd1fc9907eb9ce3c9d5e9d28a3fe1ad87436",
 "db683ea1e0ce5d71804029cdd7f4fd7915f9865c97e9702d24a0512be3981ef0",
 "c2689cce7af0a04655348e0d5bac347bd89af6f5b59d3fc17c18af84c584683a",
 "5aa333ef4b7af711014137d7e8596b1d208f8a67ddf0650aeea2fffe575fb25f",
 "8f7f6a8c29d7f76c0d2911e58382bb3f747d89b8c903db6015fe3af4c279281c",(40,81))}
SOURCE={"TW10_P3H_zip":(372626292,"3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24"),
"TW10_ADRN":(10079680,"47254c0ff904d363fb5c3c5297edf553c8eaf24cd933f346d8ce7aabed4155c8"),
"TW10_REAL":(315842228,"408e6ee05c83354349691937da2ad8f7488ac10f65f07e6681b7d92cb1c9ed13"),
"TW10_Palet1":(708,"32870080c47537a59beaf770b6df7bd79820fd52a23825058460900494f0b4b0"),
"R3_observation_zip":(3356562,"fa296ad8e5afb9065fd8a7894fed4f783ad6f393901509f8491383c56a9ee285"),
"mixed25_ADRN":(18765120,"92d0137590d35a7a1f4fb11af3ad13bbc585813a4b0e1e3f933c397007fbff74")}
TRUE=("TW10_ADRN_entire_prefix_byte_identical_to_saved_mixed25_ADRN","alias_unique_within_all_TW10_125996_records","alias_unique_within_all_mixed25_234564_records","four_original_TW10_RD_bytes_actually_extracted","full_TW10_REAL_SHA256_and_ZIP_CRC_read","four_legacy_RD_flag1","two_independent_RD_RLE_decoders_equal_all_four_indices","four_RGBA_modern_Palet1_candidates_png_roundtrip_equal","four_original_source_images_actually_viewed_locally")
FALSE=("mixed25_REAL_full_bytes_read_this_unit","same_deployed_build_or_official_npc_identity_proven","original_NPC_graphic_selector_proven","original_scene_palette_selected","original_client_executed","original_world_entered","original_renderer_or_NPC_spawn_executed","original_source_images_or_png_publicly_uploaded","original_source_browser_canvas_executed_this_unit")
def check(ok,message):
 if not ok:raise ValueError(message)
def validate(d):
 check(d["schema"]=="stoneage.o25.two_npc_original_pixel_aliases.r1" and d["source_main_head"]=="8dd983686e253bda2f2579e673222b824c68f56a","baseline")
 check(d["full_current_original_blob"]=="20050acf279a01555ab06a381dfcdc936bd381a6","preserved full CURRENT")
 check(d["source_crossversion"]=="LATER_MIXED25_STATIC_NPC_GRAPHICNAME_TO_SEPARATE_AUTHENTICATED_TW10_ORIGINAL_ADRN_REAL_PHYSICAL_PIXEL_CANDIDATES","release namespace")
 files=d["originals"];check(set(files)==set(SOURCE),"all source anchors")
 for k,(bytes_,h) in SOURCE.items():check((files[k]["bytes"],files[k]["sha256"])==(bytes_,h),"source "+k)
 check((files["TW10_P3H_zip"]["members"],files["TW10_ADRN"]["records"],files["mixed25_ADRN"]["records"])==(379,125996,234564),"original source members/records")
 check(d["two_source_NPCs"]==[{"floor":2000,"position":[55,92],"original_later_name":"彌生","original_graphicname":16027},{"floor":1000,"position":[57,124],"original_later_name":"日美子","original_graphicname":16030}],"static two named NPC source join")
 records=d["two_aliases"];check(len(records)==2,"bounded two logical aliases")
 for r in records:
  k=r["alias"];check(k in PINS,"unexpected image alias")
  actual=(r["physical"],r["offset"],r["rd_bytes"],r["width"],r["height"],r["xoff"],r["yoff"],r["record_sha"],r["rd_sha"],r["index_sha"],r["rgba_sha"],r["png_sha"],r["zeros"],r["control_record_sha"],r["control_rd_sha"],r["control_index_sha"],r["control_rgba_sha"],r["control_png_sha"],tuple(r["control_wh"]))
  check(actual==PINS[k],"source-derived genuine original RD and four pixels "+str(k))
  check(r["control_physical"]==k and r["physical"]!=r["control_physical"] and r["rd_sha"]!=r["control_rd_sha"],"alias not literal physical bitmap")
  check(r["rd_bytes"]>16 and r["width"]*r["height"]>r["zeros"]>=0,"indexed pixels finite")
 check({r["alias"] for r in records}=={16027,16030},"both source actors")
 p=d["proofs"];check(set(p)==set(TRUE)|set(FALSE)|{"overall_percent"},"all proof keys")
 check(all(p[k] is True for k in TRUE) and all(p[k] is False for k in FALSE) and p["overall_percent"] is None,"no invented original runtime/source provenance")
 pack=d["private_archive"]
 check((pack["library_path"],pack["bytes"],pack["sha256"],pack["members"])==("/石器时代/StoneAge-O25-private-two-NPC-original-pixel-aliases.zip",51705,"3d62b525b87fa6ce4c91d06525de7c701c8fe7396594c3ba1367a0e0d2d77fdd",15) and pack["retrieved_again_after_library_upload_and_SHA_CRC_verified"] is True,"private durable source custody")
 check(d["next"]=="O26_22_DOMAIN_ROTATION_ONE_NEW_GAME_CONTENT_OR_CONTROLLED_INTERACTION_WITH_ACTUAL_SOURCE","bounded next rotation")
 return {"original_RD_blocks":4,"source_NPCs":2,"distinct_alias_candidates":2,"false_literal_physical_controls":2}
if __name__=="__main__":
 print(validate(json.loads(REPORT.read_text(encoding="utf-8"))))
