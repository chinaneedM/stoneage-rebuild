"""O24 public derived-event witness guards; original assets/scripts remain private."""
import json
from pathlib import Path
REPORT=Path(__file__).resolve().parents[1]/"research/recovered/STONEAGE-O24-TWO-TOWN-EVENT-SOURCE-R1.json"
SOURCE_PIN={
 "event02.create":(6598,534,"2b15884736a19d06caffa32e335c3604e5f8593c8ea051d2040f0c5d3b52e1e4","7d30152c","RAR_DIRECT_SHA_CRC"),
 "event02_1":(6599,1185,"6f4d04e6be5c34ce989bb4cba8adb1e87ef7d852835583adeaf569cc8ec6c49c","1f8535ba","RAR_DIRECT_SHA_CRC"),
 "event02_2":(6600,1131,"eb3f9a9c9bbf1776de7533f57c529c1948c2cc8c1fb22945c49d61950f153e9b","745d963a","RAR_DIRECT_SHA_CRC"),
 "itemset.txt":(3741,3392473,"a415e78f9aab2e5ea5ca92ecb7430253f7be1ba7c876d6b0bb6d067b1b466688","96397928","RAR_DIRECT_SHA_CRC"),
 "2000.DAT":(2010,135008,"d75231434c69118a518a8d5dd34f266264b8551fe4f2d55a20cdfa11b46584b3","35bf728a","RAR_DIRECT_SHA_CRC"),
 "1000.DAT":(1664,153608,"94b19cb59d72b7b48da70d2741ba68516caad970297fd48ed11ef720fa3ea97e","cd608784","SCENE21_VERIFIED_NESTED_ZIP_NOT_FRESH_RAR")
}
NPC_PIN=((2000,(55,92),"彌生",16027,4,"event02_1",(150,150),(6014,0,49152),"adcca18ff35c3689c2f482becb27f73d60f19e36531efb693f3d925384d7c7c9"),
 (1000,(57,124),"日美子",16030,6,"event02_2",(160,160),(373,0,49152),"411f63d767286823af1bf7aa78b834c167caa210ddaf9fa7b4e1a5ab9fa92888"))
ITEM_PIN=((2414,"不可思議的貝殼",1997,506658,214,24130,"84a495deef3afe7c0dbeffee8c49ca8a211b83afc555b7f2f8af2e64ce07d741"),
 (2415,"仙尼亞的花",1998,506872,206,24173,"bdfd3a3632918f936f94e877e0cbbea49af424dd9abc0cb79ee1c782f8009e91"))
BRANCH_PIN={
"event02_1":((-1,"CLEAN","ENDEV=2&ITEM!=2414&SP=0,ENDEV=2&ITEM!=2414&SP=3",None,None,None,2,"f480cc1cd88b288ed0103a64e61bb49cf7ebe4b6bf3962d4984a3348b852d49d"),
 (2,"ACCEPT","NOWEV=2&ITEM=2415",2414,2415,2,None,"93646a5c26065f5dedd83a5bf1d05a35199046e7cf96f101ce8bcbb6d8aa8a07"),
 (2,"REQUEST","LV>0&SP=1,LV>0&SP=2",2414,None,None,None,"360364ce7236abeb35598173a8a5c84173e8c4d67d81010b39543707953ed736")),
"event02_2":((-1,"CLEAN","ENDEV=2&ITEM!=2415&SP=1,ENDEV=2&ITEM!=2415&SP=2",None,None,None,2,"d4b1850128f721c93ab1d92de444a3b6fc93e0b54a2de3395313cb903ce1da3f"),
 (2,"ACCEPT","NOWEV=2&ITEM=2414",2415,2414,2,None,"b6f307876c78c04e231e739adfae5c54826e16b9eaaefd58049ad020e7fa8427"),
 (2,"REQUEST","LV>0&SP=0,LV>0&SP=3",2415,None,None,None,"be0fbcd17b31489b2ef6045816627504f12dcdfd35d62dd894cdc564e83b85ed"))}
def need(ok,label):
    if not ok: raise ValueError(label)
def validate(d):
    need(d["schema"]=="stoneage.o24.two_town_exchange_source.r1","schema")
    need(d["baseline"]=={"main_head":"1b3c91d970d8096784ed27e521aba2798d41805d","tree":"fad53f40dd44261a434d9a2d2dcae368262276b8","current_state_blob":"20050acf279a01555ab06a381dfcdc936bd381a6"},"baseline provenance")
    need(d["era"]=="LATER_PRESERVED_MIXED25_STATIC_SOURCE_NOT_TW10_OR_JSS1999_PROOF","version boundary")
    need(d["original_archive"]=={"bytes":361255180,"sha256":"d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5","member_count":7952},"archive")
    sources=d["source_files"]
    need(len(sources)==6 and {s["name"] for s in sources}==set(SOURCE_PIN),"six member source identities")
    for s in sources:
        need((s["ordinal"],s["bytes"],s["sha256"],s["crc32"],s["verification"])==SOURCE_PIN[s["name"]],"source "+s["name"])
    need(d["scene21_private_zip"]=={"bytes":2745658,"sha256":"4d35351e6db222cac889abcce2fdbe97c498abc252d24a3000968a58c9d2605a","crc_verified":True},"old verified private ZIP")
    need(len(d["actors"])==2,"NPC count")
    for a,expected in zip(d["actors"],NPC_PIN):
        actual=(a["floor"],tuple(a["xy"]),a["name"],a["graphicname"],a["dir_raw"],a["script"],tuple(a["map_size"]),tuple(a["raw_cell_u16"]),a["create_block_sha256"])
        need(actual==expected,"create-to-script/map pointer")
        need(0<=a["xy"][0]<a["map_size"][0] and 0<=a["xy"][1]<a["map_size"][1],"coordinate bounds")
    need(len(d["items"])==2,"item count")
    for a,expected in zip(d["items"],ITEM_PIN):
        need((a["id"],a["name"],a["line"],a["offset"],a["length"],a["image_number"],a["source_row_sha256"])==expected,"itemset row")
    need(d["branch_field_order"]==["event_no","TYPE","EVENT","GetItem","DelItem","EndSetFlg","CleanFlg","branch_sha256"],"source fields")
    need(set(d["event_branches"])==set(BRANCH_PIN),"two script branches")
    for script,expected in BRANCH_PIN.items():
        need(tuple(map(tuple,d["event_branches"][script]))==expected,"script predicates and original block SHA "+script)
    need(d["event_branches"]["event02_1"][1][3:5]==[2414,2415] and d["event_branches"]["event02_2"][1][3:5]==[2415,2414],"reciprocal static item chain")
    lim=d["read_limits"]
    yes={"five_current_rar_members_fully_extracted_and_sha_crc_verified","source_1000_rar_libarchive_crc_error","source_1000_byte_identity_from_prior_scene21_zip_crc_and_sha","two_named_static_NPC_create_references"}
    no={"all_six_original_source_members_validated_in_one_library_archive","tw10_same_deployed_build","jss1999_identity","original_client_world_entered","original_server_script_executed","original_item_grant_or_removal_executed","original_graphic_frames_rendered_this_unit","raw_plane_3_game_semantics_confirmed","source_event_is_limited_time_activity"}
    need(set(lim)==yes|no|{"overall_completion_percent"},"evidence flag keys")
    need(all(lim[k] is True for k in yes) and all(lim[k] is False for k in no) and lim["overall_completion_percent"] is None,"negative evidence claims")
    need(d["next"]=="O25_BOUNDED_ACTOR_GRAPHIC_VISIBLE_MATERIAL_OR_22_DOMAIN_ROTATION","next")
    return {"actors":len(d["actors"]),"original_event_branches":sum(map(len,d["event_branches"].values())),"item_source_rows":len(d["items"]),"source_paths":len(sources)}
if __name__=="__main__":
    print(validate(json.loads(REPORT.read_text(encoding="utf-8"))))
