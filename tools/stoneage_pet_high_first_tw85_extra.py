"""Source-only inventory of TW85 preserved SPR groups absent from CN50's preserved index.

Do not treat these resource records as pet species or proof of official live issuance.
No proprietary binary or decoded sprite imagery is written to the repository.
"""
from __future__ import annotations

import argparse
import base64
from collections import defaultdict
import csv
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CN = Path("research/recovered/cn50-resource-metadata/SPR-GROUP-R1.tsv.gz")
TW = Path("research/recovered/tw85-spr137-r28/SPR-GROUP-R28.tsv.gz")
SOURCE_BLOBS = {
    str(CN): "f4a41ba999167185b55a42c89ece9e24d456e637",
    str(TW): "f201f85ced4a55d59d38ef774711406c59cddbd4",
}


def git_blob(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\\0" + raw).hexdigest()


def read_groups(path: Path):
    raw = (ROOT / path).read_bytes()
    assert git_blob(raw) == SOURCE_BLOBS[str(path)], "source-git-blob-changed: " + str(path)
    with gzip.open(ROOT / path, mode="rt", encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream, delimiter="\\t"):
            yield {
                "index": int(row["index"]),
                "spr_no": int(row["spr_no"]),
                "segment_sha256": row["segment_sha256"],
                "animation_headers": int(row["anim_count"]),
            }


def make_inventory():
    cn = list(read_groups(CN))
    tw = list(read_groups(TW))
    assert len(cn) == 1185 and len(tw) == 1739, "source record counts changed"
    cn_pairs = {(g["spr_no"], g["segment_sha256"]) for g in cn}
    tw_pairs = {(g["spr_no"], g["segment_sha256"]) for g in tw}
    assert len(cn_pairs) == 1185 and cn_pairs <= tw_pairs, "CN50 exact-segment bridge broke"
    extra = [g for g in tw if (g["spr_no"], g["segment_sha256"]) not in cn_pairs]
    assert len(extra) == 554, "TW85 additional physical group count changed"
    by_num = defaultdict(list)
    for g in extra:
        by_num[g["spr_no"]].append(g)
    assert len(by_num) == 550, "TW85 distinct extra group count changed"
    assert len({g["index"] for g in tw}) == len(tw), "nonunique original group index"
    rows = []
    for number, occurrences in sorted(by_num.items()):
        rows.append({
            "tw85_original_spr_number": number,
            "source_occurrences": sorted(occurrences, key=lambda z: z["index"]),
            "cn50_same_number_exists": any(c["spr_no"] == number for c in cn),
            "native_tw85_name_or_pet_identity": None,
            "native_tw85_pet_selector_proven": False,
            "official_in_game_release_confirmed": False,
        })
    assert sum(len(r["source_occurrences"]) for r in rows) == 554
    assert sum(len(r["source_occurrences"]) - 1 for r in rows) == 4
    return {
        "schema": "stoneage.pet.tw85_additional_source_spr_groups.r1",
        "scope": "PRESERVED_CLASSIC_PC_RESOURCE_DELTA_NOT_PET_ROSTER",
        "cn50_source": "PRESERVED_CN50_PC_UNCERTIFIED_OFFICIAL_PRESSING",
        "tw85_source": "UNVERIFIED_COMMUNITY_PRESERVED_CLAIMED_WAYI85_INSTALLER",
        "source_git_blobs": SOURCE_BLOBS,
        "metrics": {
            "cn50_physical_groups": len(cn),
            "tw85_physical_groups": len(tw),
            "exact_cn50_groups_present_in_tw85": len(cn_pairs),
            "tw85_only_physical_group_records": len(extra),
            "tw85_only_distinct_spr_numbers": len(rows),
            "tw85_only_duplicate_extra_occurrences": 4,
            "tw85_only_numbers_not_in_cn50": sum(not r["cn50_same_number_exists"] for r in rows),
            "tw85_only_numbers_also_in_cn50_but_different_bytes":
                sum(r["cn50_same_number_exists"] for r in rows),
            "original_tw85_pet_names_verified_for_extra_groups": 0,
            "official_pet_species_verified_by_extra_groups": 0,
        },
        "boundaries": {
            "group_is_not_pet_or_species": True,
            "higher_version_superset_not_assumed": True,
            "source_bytes_are_derived_index_only": True,
            "new_first_appearance_not_inferred": True,
            "source_date_not_live_release_date": True,
        },
        "records": rows,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=Path)
    ap.add_argument("--log-json", action="store_true")
    args = ap.parse_args()
    report = make_inventory()
    raw = (json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\\n").encode("utf-8")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(raw)
    print("PET06_METRICS=" + json.dumps(report["metrics"], sort_keys=True))
    print("PET06_REPORT_SHA256=" + hashlib.sha256(raw).hexdigest())
    if args.log_json:
        encoded = base64.b64encode(raw).decode("ascii")
        print("PET06_LOG_B64_BEGIN")
        for i in range(0, len(encoded), 3000):
            print("PET06_B64 " + encoded[i:i+3000])
        print("PET06_LOG_B64_END")


if __name__ == "__main__":
    main()
