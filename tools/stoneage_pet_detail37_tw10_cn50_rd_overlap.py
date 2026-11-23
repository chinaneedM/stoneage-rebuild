#!/usr/bin/env python3
"""PET-DETAIL37: original TW1 named-SPR -> preserved CN5 album crosswalk.

Derived evidence only. The CN5 ADRN source table was reduced to last-record
projection: it does NOT enumerate all original alias collisions or prove
native drawing behavior, live release, or original server-controlled values.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
  'CN': "research/pets/PET-DETAIL-EVIDENCE36-CN50-ALBUM-ADRN-RD-PROJECTION-R1.json",
  'TW': "research/recovered/STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json",
  'W': "research/recovered/STONEAGE-PET126W-TW10-CN50-ALL-124-ORIGINAL-PC-NAME-VARIANTS-R1.json",
  'FOUR': "research/pets/PET-DETAIL-EVIDENCE33-FOUR-PC-PORTRAIT-PIXEL-PAIRS-R1.json"
}
PINS = {
  "research/pets/PET-DETAIL-EVIDENCE36-CN50-ALBUM-ADRN-RD-PROJECTION-R1.json": "8e06ddfcf1a080c7591c0a8300811b0b770cd425",
  "research/recovered/STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json": "1aada81d7314769bf683b816cc5a8762c3bd9400",
  "research/recovered/STONEAGE-PET126W-TW10-CN50-ALL-124-ORIGINAL-PC-NAME-VARIANTS-R1.json": "244251c54b5f8f274502daff984eacdd1a0b7c97",
  "research/pets/PET-DETAIL-EVIDENCE33-FOUR-PC-PORTRAIT-PIXEL-PAIRS-R1.json": "c638bebc992604a9742dee14f2b8b613c38cf615"
}
BASE_HEAD = "5e0c01f0c854af7aefa75fd0485ddf728d069168"
BASE_TREE = "58bec514bacb6eaec545f71f7de03c0185d8b404"
ORIGINAL_CURRENT_BLOB = "c89e0e33537990aa2132b47c40fef49a985a935c"


def git_blob(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def audit(root=ROOT):
    root = Path(root)
    loaded = {}
    for path, pin in PINS.items():
        raw = (root / path).read_bytes()
        if git_blob(raw) != pin:
            raise ValueError("Original pinned derived source changed: " + path)
        loaded[path] = json.loads(raw)
    cn = loaded[SOURCES['CN']]
    tw = loaded[SOURCES['TW']]
    bridge = loaded[SOURCES['W']]
    four = loaded[SOURCES['FOUR']]
    cn_rows = cn["records"]
    assert len(cn_rows) == 305 and cn["counts"]["all_album_slots"] == 362
    assert len(tw["records"]) == len(bridge["records"]) == 124
    w_by_ordinal = {x["album_ordinal"]: x for x in bridge["records"]}
    tw_by_graphic = {x["graphic_number"]: x for x in tw["records"]}
    four_by_alias = {x["logical_portrait_alias"]: x for x in four["records"]}
    rows, variants = [], []
    for c in cn_rows:
        b = w_by_ordinal.get(c["album_ordinal"])
        t = None
        grade = "CN50_NAMED_LOCAL_ONLY_NO_TW10_BRIDGE"
        if b is not None:
            t = tw_by_graphic[b["ordinal_graphic_hypothesis"]]
            assert t["name_as_written"] == b["tw10_original_literal"]
            assert c["client_compiled_name"] == b["cn50_preserved_compiled_literal"]
            assert c["source_exe_row_sha256"] == b["cn50_original_row_sha256"]
            assert t["spr_original_segment_sha256"] == b["shared_full_original_spr_segment_sha256"]
            assert t["portrait_logical_alias"] == c["source_compiled_alias_u32"]
            if t["portrait_rd"] is not None:
                assert t["portrait_rd"]["sha256"] == c["same_CAB_rd_block_sha256"]
                grade = "TW10_ORIGINAL_RD_SHA256_EXACT_CN50"
            else:
                f = four_by_alias[c["source_compiled_alias_u32"]]
                assert f["cn50_collision_projection_last_bitmap"] == c["last_projected_physical_rd_bitmapno"]
                assert len(f["variants"]) == 2
                assert f["variants"][1]["rd_sha256"] == c["same_CAB_rd_block_sha256"]
                grade = "TW10_NATIVE_PORTRAIT_ABSENT_TWO_LATER_VARIANTS"
                variants.append({
                    "tw10_original_name": t["name_as_written"],
                    "cn50_compiled_name": c["client_compiled_name"],
                    "logical_alias": c["source_compiled_alias_u32"],
                    "original_tw10_source_portrait_present": False,
                    "later_carrier_variant_bitmapnos": [v["physical_bitmap_number"] for v in f["variants"]],
                    "later_carrier_variant_rd_sha256": [v["rd_sha256"] for v in f["variants"]],
                    "cn50_last_projection_is_not_native_selector": True,
                })
        rows.append({
            "cn50_album_ordinal": c["album_ordinal"],
            "cn50_compiled_name": c["client_compiled_name"],
            "cn50_original_exe_row_sha256": c["source_exe_row_sha256"],
            "cn50_compiled_portrait_alias_u32": c["source_compiled_alias_u32"],
            "cn50_last_projected_rd_bitmapno": c["last_projected_physical_rd_bitmapno"],
            "cn50_last_projected_rd_sha256": c["same_CAB_rd_block_sha256"],
            "tw10_original_name": t["name_as_written"] if t is not None else None,
            "tw10_original_graphic_number": t["graphic_number"] if t is not None else None,
            "tw10_full_original_spr_sha256": t["spr_original_segment_sha256"] if t is not None else None,
            "tw10_original_portrait_rd_sha256": t["portrait_rd"]["sha256"] if t is not None and t["portrait_rd"] is not None else None,
            "comparison_grade": grade,
            "all_native_adrn_alias_candidates_enumerated": False,
            "official_live_release_verified_by_this_crosswalk": False,
        })
    counts = {
        "cn50_compiled_album_total_slots": 362,
        "cn50_compiled_named_rows": len(rows),
        "tw10_source_qualified_named_spr_bridges": sum(x["tw10_original_name"] is not None for x in rows),
        "tw10_original_portrait_exact_rd_sha256_reuse": sum(x["comparison_grade"] == "TW10_ORIGINAL_RD_SHA256_EXACT_CN50" for x in rows),
        "tw10_native_portrait_missing_with_two_later_rd_variants": len(variants),
        "cn50_named_local_rows_without_qualified_tw10_identity_bridge": sum(x["comparison_grade"] == "CN50_NAMED_LOCAL_ONLY_NO_TW10_BRIDGE" for x in rows),
        "cn50_last_projection_rd_hashes_unique": len({x["cn50_last_projected_rd_sha256"] for x in rows}),
        "new_official_live_pet_species_verified": 0,
        "new_original_same_build_pet_server_ids_verified": 0,
    }
    assert (counts["cn50_compiled_named_rows"],
            counts["tw10_source_qualified_named_spr_bridges"],
            counts["tw10_original_portrait_exact_rd_sha256_reuse"],
            counts["tw10_native_portrait_missing_with_two_later_rd_variants"],
            counts["cn50_named_local_rows_without_qualified_tw10_identity_bridge"],
            counts["cn50_last_projection_rd_hashes_unique"]) == (305, 124, 120, 4, 181, 305)
    return {
        "schema": "stoneage.pet_detail37.tw10_cn50_source_qualified_portrait_sha_overlap.r1",
        "date": "2026-11-23",
        "active_module": "PET",
        "scope": "ORIGINAL_CLASSIC_PC_ONLY",
        "source_baseline_main_head": BASE_HEAD,
        "source_baseline_main_tree": BASE_TREE,
        "original_current_state_git_blob_preserved": ORIGINAL_CURRENT_BLOB,
        "source_git_pins": PINS,
        "source_qualifications": {
            "tw10": "AUTHENTICATED_TW10_ORIGINAL_PC_RETAIL",
            "cn50": "THIRD_PARTY_PRESERVED_CN50_PC_5_0_CAB_UNCERTIFIED_OFFICIAL_CLEAN_PRESSING",
            "cn50_adrn_join": "SAME_PRESERVED_CAB_LAST_RECORD_PROJECTION_NOT_FULL_COLLISION_SCAN",
            "comparison": "EXACT_FULL_RD_BLOCK_SHA256_FOR_120_ONLY",
            "new_source_original_binary_bytes_read_this_unit": False,
        },
        "counts": counts,
        "four_original_tw10_portrait_gaps_with_existing_later_variants": variants,
        "claims_not_made": {
            "cn50_named_rows_are_issued_species": False,
            "all_cn50_adrn_collision_variants_enumerated": False,
            "native_renderer_selector_confirmed": False,
            "original_same_deployment_server_pet_master_or_birth_growth_skills_capture_confirmed": False,
            "cn50_local_label_5_0_certifies_first_release_year": False,
            "late_181_named_rows_are_new_species": False,
            "official_history_completed": False,
        },
        "governance": {
            "stage_a": "7_PARTIAL_2_OPEN", "stage_b_wiki": "GATED",
            "r79": "PAUSED_NON_BLOCKING", "overall_percent": None,
            "original_commercial_assets_published": False,
        },
        "next": "PET-DETAIL38: if original source bytes are lawfully accessible, scan complete same-CAB CN50 ADRN +76 rows for all 305 aliases (not last-record projection) and verify TW85 original candidates/native selector; otherwise precisely preserve blocked source and continue original-PC same-build server pet master, birth, skills, capture, release verification.",
        "records": rows,
    }


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, sort_keys=True, separators=(",", ":")))
