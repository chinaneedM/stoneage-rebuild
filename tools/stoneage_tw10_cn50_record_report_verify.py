#!/usr/bin/env python3
"""Adversarial consistency gate for stored source-derived CN5/TW1 RD/SPR results.

This is not a second original-byte download; assert the exact verification
boundary and invariants of a previously source-qualified JSON report.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

SOURCE = "research/recovered/STONEAGE-TW10-CN50-REAL-RECORD-DIFF-R1.json"
CAB = "research/recovered/STONEAGE-STONEAGE5-REAL-CAB-PAYLOAD-R1.json"
TW = "research/recovered/STONEAGE-TW10-CLIENT-INVENTORY-R1.txt"


def source_tw10_files(text):
    out = {}
    for line in text.splitlines():
        if line.startswith("CORE_FILE|"):
            fields = dict(x.split("=", 1) for x in line.split("|")[1:] if "=" in x)
            out[fields["path"]] = (int(fields["size"]), fields["sha256"])
    if len(out) != 383:
        raise ValueError("expected-existing-tw10-file-manifest")
    return out


def verify(report, cab, tw_manifest):
    if (report.get("schema") != "stoneage.tw10_cn50.record_level_resource_diff_r1"
        or report.get("result") != "DERIVED_RECORD_LEVEL_DIFF_OF_REACQUIRED_ORIGINAL_RESOURCE_BYTES"):
        raise ValueError("missing-real-byte-source-provenance")
    if not isinstance(cab,dict) or cab.get("status") != "REAL_FULL_CAB_EXTRACTED_AND_413_FILES_HASHED":
        raise ValueError("missing-existing-cn50-cab")
    if report.get("source_claims",{}).get("CN50",{}).get("cab_sha256") != cab["source"]["cab_sha256"]:
        raise ValueError("cn50-cab-digest-mismatch")
    known_cn = {row["name"]:(row["size"],row["sha256"]) for row in cab["files"]["inventory"]}
    if len(known_cn)!=413:
        raise ValueError("incomplete-cn50-manifest")
    known_tw = source_tw10_files(tw_manifest)
    pairs = {
        "adrn":("adrn_31.bin","StoneAge/data/adrn_1.bin"),
        "real":("real_31.bin","StoneAge/data/real_1.bin"),
        "spradrn":("spradrn_17.bin","StoneAge/data/spradrn_1.bin"),
        "spr":("spr_17.bin","StoneAge/data/spr_1.bin"),
    }
    for key,(cn,tw) in pairs.items():
        cn_row = report["source_claims"]["CN50"]["files"][key]
        tw_row = report["source_claims"]["TW10"]["files"][key]
        if (cn_row["bytes"],cn_row["sha256"]) != known_cn[cn]:
            raise ValueError("source-cn50-four-container-hash-mismatch")
        if (tw_row["bytes"],tw_row["sha256"]) != known_tw[tw]:
            raise ValueError("source-tw10-four-container-hash-mismatch")
    if report["source_claims"]["CN50"].get("official_clean_release_mastering_authenticated") is not False:
        raise ValueError("invented-pressing-authentication")
    if report["evidence_boundaries"].get("original_server_npc_quest_growth_master_recovered") is not False:
        raise ValueError("invented-historical-server-data")
    if report["evidence_boundaries"].get("proprietary_bytes_emitted") is not False:
        raise ValueError("proprietary-payload-leak-claim")
    if report["prerequisites"].get("cn50_413_files_rehashed_again") is not True:
        raise ValueError("no-source-original-byte-rehash")
    expected={"bitmap_rd":125996,"animation_spr":464}
    stats={}
    for family,old_total in expected.items():
        node=report["families"][family]
        old,new,comp=node["old"],node["new"],node["comparison"]
        if old["index_count"]!=old_total or old["valid_payload_rows" if family=="bitmap_rd" else "valid_segments"]!=old_total:
            raise ValueError("tw10-original-record-count-inconsistent")
        if comp["old_total_ids"]!=old_total or comp["old_duplicate_ids"]!=0:
            raise ValueError("non-unique-early-resource-ids")
        if comp["common_unique_id_count"]+comp["old_unique_ids_absent_in_new_count"]+comp["ambiguous_shared_id_count"] > old_total:
            raise ValueError("impossible-unique-id-coverage")
        if comp["exact_payload_or_segment_count"]+comp["changed_payload_or_segment_count"] != comp["common_unique_id_count"]:
            raise ValueError("changed-and-exact-do-not-partition-common")
        if comp["same_geometry_or_animation_count"] > comp["common_unique_id_count"]:
            raise ValueError("impossible-geometry-coverage")
        if comp["same_index_descriptor_or_frame_count"] > comp["common_unique_id_count"]:
            raise ValueError("impossible-frame-coverage")
        if comp["old_total_ids"] > old["index_count"] or comp["new_total_ids"] > new["index_count"]:
            raise ValueError("resource-ids-exceed-record-count")
        if comp["exact_payload_or_segment_count"] < 0 or comp["changed_payload_or_segment_count"] < 0:
            raise ValueError("negative-record-comparison")
        if comp["new_unique_ids_absent_in_old_count"] > comp["new_total_ids"]:
            raise ValueError("invented-new-resource-id")
        if comp["old_unique_ids_absent_in_new_count"] > comp["old_total_ids"]:
            raise ValueError("invented-lost-resource-id")
        for prop in ("common_unique_ids_sha256","missing_old_ids_sha256","new_ids_sha256","ambiguous_ids_sha256"):
            digest=comp[prop]
            if len(digest)!=64 or any(ch not in "0123456789abcdef" for ch in digest):
                raise ValueError("malformed-id-list-digest")
        stats[family]={
            "old_records":old_total,"new_records":new["index_count"],
            "shared_unique_ids":comp["common_unique_id_count"],
            "byte_identical_payloads":comp["exact_payload_or_segment_count"],
            "changed_payloads":comp["changed_payload_or_segment_count"],
            "new_unique_ids":comp["new_unique_ids_absent_in_old_count"],
            "missing_old_unique_ids":comp["old_unique_ids_absent_in_new_count"],
            "ambiguous_shared_ids":comp["ambiguous_shared_id_count"],
            "new_invalid_or_unparsed":new["index_count"]-new["valid_payload_rows" if family=="bitmap_rd" else "valid_segments"],
        }
    if (stats["bitmap_rd"]["new_records"],stats["bitmap_rd"]["byte_identical_payloads"],stats["bitmap_rd"]["new_unique_ids"]) != (303197,125996,177201):
        raise ValueError("5.0-bitmap-actual-source-acceptance-changed")
    if (stats["animation_spr"]["new_records"],stats["animation_spr"]["byte_identical_payloads"],stats["animation_spr"]["new_unique_ids"]) != (1185,464,721):
        raise ValueError("5.0-animation-actual-source-acceptance-changed")
    return stats


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1])
    args=p.parse_args()
    root=args.root
    report=json.loads((root/SOURCE).read_text(encoding="utf8"))
    cab=json.loads((root/CAB).read_text(encoding="utf8"))
    stats=verify(report,cab,(root/TW).read_text(encoding="utf8"))
    print(json.dumps(stats,sort_keys=True,ensure_ascii=False))


if __name__=="__main__":
    main()
