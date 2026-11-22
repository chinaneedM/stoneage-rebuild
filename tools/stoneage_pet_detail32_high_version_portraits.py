#!/usr/bin/env python3
"""PET32: trace four TW1 missing album faces through later classic PC resource catalogs.

Read original-research *metadata* archived in the public repo, not proprietary pixels.
No first/last winner for duplicate alias content; versions remain independent.
"""
from __future__ import annotations

import argparse
import json
import lzma
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R43 = ROOT / "research/recovered/STONEAGE-ALBUM-CROSSVERSION-MATERIAL-R43.json.xz"
R43_BLOB = "dbc1b46fe14f105898757d1199ac338e9971c330"
EXPECTED = [
    ("PET-000116", "洛克斯", 100389, 28085, 139),
    ("PET-000117", "阿伊薩", 100390, 28086, 140),
    ("PET-000118", "格洛格魯", 100391, 28087, 141),
    ("PET-000119", "朵洛將恩", 100392, 28088, 142),
]


def verify(ok, label):
    if not ok:
        raise ValueError(label)


def collect(root: Path = ROOT) -> dict:
    raw = (root / R43.relative_to(ROOT)).read_bytes()
    import hashlib
    gitblob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    verify(gitblob == R43_BLOB, "R43 exact published Git blob")
    j = json.loads(lzma.decompress(raw))
    verify(j["schema"] == "stoneage.album_crossversion_material.r43", "R43 schema")
    verify(j["join_kind"] == "RETROSPECTIVE_LOGICAL_ALIAS_COMPATIBILITY_NOT_SAME_BUILD_IDENTITY", "source limits")
    verify(not j["boundaries"]["runtime_alias_winner_proven"], "R43 runtime decision unproven")
    verify(not j["boundaries"]["pixels_read_or_rendered"], "R43 metadata only")
    all_rows = j["rows"]
    output = []
    for pet_id, name, graphic, alias, ordinal in EXPECTED:
        found = [x for x in all_rows if int(x["album_row"]["table_face_value"]) == alias]
        verify(len(found) == 1, "unique R43 alias: " + str(alias))
        source = found[0]
        row = source["album_row"]
        verify(row["name_gbk"] == name.replace("薩","萨").replace("魯","鲁").replace("將","将"), "name source")
        verify(int(row["table_index"]) == ordinal, "album ordinal")
        detail = {
            "pet_id": pet_id, "tw10_original_client_name": name,
            "tw10_original_graphic": graphic, "original_album_face_alias": alias,
            "tw10_album_portrait": None,
            "later_classic_pc_sources": {},
            "candidate_selection": None,
            "native_runtime_face_selector_verified": False,
            "official_original_server_pet_id": None,
            "is_original_TW1_portrait_proven": False,
        }
        for carrier in ("TW10", "CN50", "PATCH129"):
            node = source["profiles"][carrier]
            variants = [
                {
                    "source_catalog_index": int(x["source_index"]),
                    "physical_bitmapno": int(x["physical_bitmapno"]),
                    "rd_bytes": int(x["rd_bytes"]),
                    "rd_sha256": x["rd_sha256"],
                }
                for x in node["references"]
            ]
            detail["later_classic_pc_sources"][carrier] = {
                "status": node["status"], "source_occurrences": len(variants),
                "distinct_rd_contents": node["content_count"],
                "candidates": variants,
            }
        tw = detail["later_classic_pc_sources"]["TW10"]
        cn = detail["later_classic_pc_sources"]["CN50"]
        patch = detail["later_classic_pc_sources"]["PATCH129"]
        verify(tw["status"] == "MISSING_IN_FIXED_CATALOG" and tw["source_occurrences"] == 0, "TW1 face still missing")
        verify(cn["status"] == patch["status"] == "MULTIPLE_CONTENTS", "two genuinely distinct later faces")
        verify(cn["source_occurrences"] == patch["source_occurrences"] == 2, "both later variants retained")
        verify(
            {(x["rd_bytes"],x["rd_sha256"]) for x in cn["candidates"]}
            == {(x["rd_bytes"],x["rd_sha256"]) for x in patch["candidates"]},
            "later original source content sets differ",
        )
        output.append(detail)
    return {
        "schema": "stoneage.pet32.original_tw10_four_missing_face_later_pc_retrieval.r1",
        "source_kind": "REPLAY_PUBLISHED_R43_ORIGINAL_RESOURCE_METADATA",
        "r43_git_blob": R43_BLOB,
        "source_dossier_count": len(output),
        "original_tw10_portraits_recovered": 0,
        "later_pc_aliases_with_two_different_rd_contents": 4,
        "cross_version_material_identical_CN50_PATCH129": True,
        "no_new_original_pixels_read": True,
        "pet_official_live_issuance_newly_proven": 0,
        "overall_percent": None,
        "records": output,
        "next": "Obtain original lawful high-version RD pixel payload and true face selector before choosing a candidate; keep TW1 original face null."
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--full", action="store_true")
    args = p.parse_args()
    j = collect()
    if not args.full:
        j.pop("records")
    print("PET32_JSON_START")
    print(json.dumps(j, ensure_ascii=False, sort_keys=True))
    print("PET32_JSON_END")


if __name__ == "__main__":
    main()
