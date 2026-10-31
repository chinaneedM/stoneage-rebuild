"""O17 source-only contract; original client images and game binaries remain private."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/recovered/STONEAGE-O17-MAP1003-ACTUAL-PIXEL-CANDIDATE-R1.json"
KEYS=(401,5000,5001,5002,5005,5006,5007,5008,5009,5010,5011,5012,5013,5014,5015,5016,5017,5018,5019,5020,5021,5026,10153,10154,10909,10910,12019,12020,12021,12022,12023,12618,12620,12621,12804,12834,12837,12845)

def need(ok, msg):
    if not ok:
        raise ValueError(msg)

def validate(d):
    need(d["schema"]=="stoneage.o17.map1003.tw1_cross_source_pixels.r1","schema")
    need("MIXED25_MAP1003" in d["scope"] and "NOT_OFFICIAL_WORLD" in d["scope"],"source and version boundary")
    need(d["source_head"]=="a6b632bcad474a114ac425391164ece77a8ea69f" and d["source_tree"]=="500af3655ef44a031bf5b4b5f542a52dc2bcf676","source base")
    need(d["preserved_current_blob"]=="20050acf279a01555ab06a381dfcdc936bd381a6","CURRENT original preserved")
    m=d["map"]
    need((m["path"],m["bytes"],m["sha256"],m["dimensions"])==("map/1003.DAT",5408,"fc3037a1850c8baf06ad5874a4cb49ca5e13e9315c020f64c019417c33b694e6",[30,30]),"source map")
    need(m["plane_image_occurrences"]==[107,27] and (m["graphic_id_count"],m["unique_tw10_adrn_alias_count"])==(38,38),"finite original graphics")
    need(m["plane_non_image_value_counts"]==[{"0":793},{"0":69,"2":804}] and m["third_plane_value_counts"]=={"49152":898,"49155":2} and m["third_plane_semantics_known"] is False,"source planes unknown")
    s=d["original_source"]
    need((s["preserved_mixed25_rar_bytes"],s["preserved_mixed25_rar_expected_sha256"])==(361255180,"d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5"),"real RAR")
    need((s["tw10_ADRN_bytes"],s["tw10_ADRN_sha256"])==(10079680,"47254c0ff904d363fb5c3c5297edf553c8eaf24cd933f346d8ce7aabed4155c8"),"TW10 ADRN")
    need((s["tw10_REAL_bytes"],s["tw10_REAL_sha256"])==(315842228,"408e6ee05c83354349691937da2ad8f7488ac10f65f07e6681b7d92cb1c9ed13"),"TW10 REAL")
    need((s["tw10_SAP_bytes"],s["tw10_SAP_sha256"])==(708,"32870080c47537a59beaf770b6df7bd79820fd52a23825058460900494f0b4b0"),"TW10 SAP")
    need(s["mixed25_ADRN_actual_read"] is False and s["mixed25_REAL_actual_read"] is False and s["mixed25_graphic_sha_still_depends_on_archived_prefix_witness"] is True,"no invented mixed source pixels")
    need("Parsing filters is unsupported" in s["mixed25_companion_extraction_error"],"preserve actual extraction blocker")
    a=d["material"]
    need((a["source_placements"],a["source_graphics"],a["source_placements_per_layer"])==(134,38,[107,27]),"placements conserved")
    need(a["rd_flags"]=={"1":38} and a["two_independent_rd_decoders_equal"] is True and a["reserved_nonzero_palette_keys"]=={},"RD decoder and color limits")
    need(tuple(a["distinct_graphic_keys"])==KEYS and len(a["rd_source_digest_order_sha256"])==64,"source IDs and recorded RD identities")
    c=d["candidate"]
    need(c["canvas_dimensions"]==[695,665] and c["canvas_bounds"]==[667,-378,1314,239],"candidate extent")
    need(c["combined_RGBA_sha256"]=="f0745bba51f8c71a4e059fc7ce2501733048a56ec18f8efba9df4ff7589740ce" and c["combined_PNG_sha256"]=="ae1511c3d68cd9335a66d9c91392bde767cd4629ff605c60f557b7f3d5bcc487" and c["independent_full_rgba_overlay_equal"] is True,"whole canvas comparison")
    for flag in ("original_client_runtime_colors_proven","same_deployed_build_proven","original_world_entered","native_collision_and_interaction_proven"):
        need(c[flag] is False,"no original-game claim: "+flag)
    q=d["private"]
    need(q["zip_bytes"]==1176526 and q["zip_sha256"]=="6bc9d015f4bcfde7a62957ce59d7e2b9bc662df9d67ce765868d0a13ec4b1452" and q["zip_readback_verified"] is True and q["proprietary_assets_published"] is False,"private artifact boundary")
    need(d["overall_completion_percent"] is None,"no invented completion percentage")
    return {"source_map_cells":900,"source_original_placements":134,"cross_source_RD_decoded":38,"original_world_entered":False}

if __name__=="__main__":
    print(json.dumps(validate(json.loads(REPORT.read_bytes())),ensure_ascii=False))
