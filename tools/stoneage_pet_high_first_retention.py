"""Compare CN50 named pet art with the preserved TW85 client and WAEI patch."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
import re

from tools.stoneage_adrn129_real_archive import structural_status
from tools.stoneage_pet126l_cn50_table_graphic_probe import read_gz_rows
from tools.stoneage_pet_high_first_cn50_catalog import ROOT, git_blob

BASE = Path("research/recovered")
PETS = Path("research/pets")
TARGET = ROOT / PETS / "PET-HIGH-FIRST-CN50-TW85-ART-RETENTION-R1.json"
INPUTS = {
    "native": (PETS / "PET-HIGH-FIRST-CN50-NATIVE-SPR-ALBUM-R1.json", "98fea71c051dfa887b91154a8a72d17c67b57744"),
    "fusion": (PETS / "PET-HIGH-FIRST-CN50-FUSION-PANELS-R1.json", "060e290573b0b0075a462015a10f6e810fd33dec"),
    "cn_groups": (BASE / "cn50-resource-metadata/SPR-GROUP-R1.tsv.gz", "f4a41ba999167185b55a42c89ece9e24d456e637"),
    "cn_frames": (BASE / "cn50-resource-metadata/SPR-FRAME-R1.tsv.gz", "6e98e5fea26a69aa5c7042bab1707c7a330c6bf7"),
    "cn_ad": (BASE / "cn50-resource-metadata/ADRN-R1.tsv.gz", "127670eaf2bc19ba9d15776d090a8307058f729d"),
    "tw_groups": (BASE / "tw85-spr137-r28/SPR-GROUP-R28.tsv.gz", "f201f85ced4a55d59d38ef774711406c59cddbd4"),
    "tw_frames": (BASE / "tw85-spr137-r28/SPR-FRAME-R28.tsv.gz", "831fa633adc5bb1f401ee17fca186d476d146196"),
    "tw_ad": (BASE / "adrn129-tw85-real-pair/NATIVE-R1.tsv.gz", "ffb7b3340116ecaf57daa08242c1ce271e3ad86f"),
    "patch": (BASE / "wayi-adrn129-patch-metadata/INDEX-1-R1.tsv.gz", "065ecc874adc637098dc7c8f177e478bc7b6f054"),
    "pairs": (BASE / "adrn129-tw85-real-pair/PAIRS-R1.tsv.gz", "7f41ca49ff576914764b77f22684fbc113e1d90e"),
    "acceptance": (BASE / "STONEAGE-ADRN129-REAL-ACCEPTANCE-R1.json", "04940c6e9a0944bd756657665350c2cb7ae9d412"),
    "cn_files": (BASE / "STONEAGE-STONEAGE5-REAL-CAB-MSI-PATH-JOIN-R1.json", "b2532248355b35cd9d4ed7d15d3f59aeeb9beadf"),
    "tw_files": (BASE / "STONEAGE-WAYI85-MSI-CLIENT-PAYLOAD-R1.json", "18a68c9d4275763ef0ed7a347cca940cffe0fee2"),
}
FRAME_FIELDS = ("anim_index", "frame_index", "bmp_no", "pos_x", "pos_y", "sound_no", "sentinel")
RECORD_FIELDS = ("adder", "size", "xoff", "yoff", "width", "height", "rd_flag", "rd_width", "rd_height")
RAW_SIZE = "RAW_FLAG0_ADRN_SIZE_AUTHORITATIVE"


def ensure(condition, label):
    if not condition:
        raise ValueError(label)


def source_paths():
    paths = {}
    for key, (path, pin) in INPUTS.items():
        paths[key] = ROOT / path
        ensure(git_blob(paths[key].read_bytes()) == pin, f"input pin changed: {path}")
    return paths


def groups(path):
    index = defaultdict(list)
    for row in read_gz_rows(path):
        number, fingerprint = int(row["spr_no"]), row["segment_sha256"]
        index[(number, fingerprint)].append((int(row["index"]), int(row["anim_count"])))
    return index


def frames(path, indices):
    counters = {i: Counter() for i in indices}
    descriptors = {i: sha256() for i in indices}
    for row in read_gz_rows(path):
        group = int(row["group_index"])
        if group in counters:
            key = None if row["sentinel"] == "1" else int(row["bmp_no"])
            counters[group][key] += 1
            descriptors[group].update(("\t".join(row[k] for k in FRAME_FIELDS) + "\n").encode("ascii"))
    return counters, {i: digest.hexdigest() for i, digest in descriptors.items()}


def bitmap_rows(path, wanted, side, real_size):
    out = {}
    for source in read_gz_rows(path):
        bitmap = int(source["bitmapno"])
        if bitmap not in wanted:
            continue
        ensure(bitmap not in out, f"duplicate physical bitmap {side} {bitmap}")
        rd = {key: int(source[key]) for key in RECORD_FIELDS}
        rd["rd_sha256"] = source["rd_sha256" if side == "tw" else "rd_block_sha256"]
        rd["rd_size"] = int(source["rd_size" if side == "tw" else "rd_size_field"])
        rd["rd_status"] = source.get("rd_status", "HEADER_MATCH")
        status = structural_status(rd, real_size)
        ensure(status != "NOT_QUALIFIED", f"unqualified RD {side} {bitmap}")
        out[bitmap] = (int(source["index"]), source["attr_sha256"], rd, status)
    ensure(set(out) == wanted, f"missing referenced bitmaps in {side}")
    return out


def summary(records, frame_bitmaps):
    routes = [r for pet in records for r in pet["routes"]]
    return {
        "cn50_named_album_slots": len(records),
        "exact_sprite_groups": len(routes),
        "frame_positions": sum(r["frames"] for r in routes),
        "sentinel_positions": sum(r["sentinels"] for r in routes),
        "exact_rd_frame_positions": sum(r["frames"] - r["sentinels"] for r in routes),
        "unique_physical_frame_bitmaps": len(frame_bitmaps),
        "exact_selected_portrait_blocks": sum(bool(r["tw85_same_physical_portrait_rd_sha256"]) for r in records),
        "selected_portraits_matched_by_official_patch_alias": sum(
            any(p["same_cn50_selected_rd"] for p in r["official_patch_alias_matches"]) for r in records
        ),
        "alternate_patch_portraits": sum(
            not p["same_cn50_selected_rd"] for r in records for p in r["official_patch_alias_matches"]
        ),
    }


def build():
    p = source_paths()
    def read_json(key):
        return json.loads(p[key].read_bytes())

    native = read_json("native")["records"]
    fusion = read_json("fusion")
    # The July panel resolves the single May spelling discrepancy at printed 255.
    cohort = {r["cn50_album_ordinal"] for r in fusion["records"]} | {
        r["cn50_album_ordinal_by_exact_name"] for r in fusion["may_editorial_catalogue"]["rows"]
        if r["cn50_album_ordinal_by_exact_name"] is not None
    }
    ensure(len(native) == 305 and len(cohort) == 45 and cohort == set(range(308, 353)), "named cohort changed")
    cn_groups, tw_groups = groups(p["cn_groups"]), groups(p["tw_groups"])
    route_indices = {}
    for row in native:
        for group in row["spr_groups"]:
            number = group["spr_group"]
            key = (number, group["sha256"])
            cn, = cn_groups[key]
            tw, = tw_groups[key]
            ensure(cn[1] == tw[1] == group["animation_header_count"], "animation counts disagree")
            ensure(number not in route_indices, "CN50 route duplicated")
            route_indices[number] = (cn[0], tw[0])
    ensure(len(route_indices) == 594, "native named group extent changed")

    cn_f, cn_f_sha = frames(p["cn_frames"], {x[0] for x in route_indices.values()})
    tw_f, tw_f_sha = frames(p["tw_frames"], {x[1] for x in route_indices.values()})
    for c, t in route_indices.values():
        ensure(cn_f_sha[c] == tw_f_sha[t] and cn_f[c] == tw_f[t], "ordered frame reference difference")
    wanted_frames = set().union(*(set(f) for f in cn_f.values())) - {None}
    wanted = wanted_frames | {r["portrait_lookup_after_ordered_load"] for r in native}
    cn_files = read_json("cn_files")["installed_files"]
    tw_files = read_json("tw_files")["inspection"]["inventory"]["samples"][0]["files"]
    cn_real = next(row["size"] for row in cn_files if row["installed_path"].endswith("real_31.bin"))
    tw_real = next(row["size"] for row in tw_files if row["path"].endswith("real_158.bin"))
    cn_ad = bitmap_rows(p["cn_ad"], wanted, "cn", cn_real)
    tw_ad = bitmap_rows(p["tw_ad"], wanted, "tw", tw_real)
    for bitmap in wanted:
        _, c_attr, a, s = cn_ad[bitmap]
        _, t_attr, b, t = tw_ad[bitmap]
        # Physical pack offsets can differ. Placement, attributes and RD data must agree.
        ensure(c_attr == t_attr and s == t and
               all(a[k] == b[k] for k in a if k not in {"adder", "rd_status"}), f"bitmap mismatch {bitmap}")

    aliases = {r["portrait_alias"] for r in native}
    alias_rows = defaultdict(list)
    for row in read_gz_rows(p["patch"]):
        alias = int(row["map_number"])
        if alias in aliases:
            alias_rows[alias].append(row)
    patch_indices = {int(row["index"]) for rows in alias_rows.values() for row in rows}
    pair = {int(r["patch_index"]): r for r in read_gz_rows(p["pairs"]) if int(r["patch_index"]) in patch_indices}
    acceptance = read_json("acceptance")
    accepted_native = {r["index"]: r for r in acceptance["native_raw_length_exceptions"]}
    accepted_patch = {r["patch_index"]: r for r in acceptance["patch_raw_length_exceptions"]}
    records = []
    for named in native:
        alias = named["portrait_alias"]
        bitmap = named["portrait_lookup_after_ordered_load"]
        rd_sha = cn_ad[bitmap][2]["rd_sha256"]
        ensure(rd_sha == named["portrait_lookup_rd_sha256"], "CN50 portrait fingerprint changed")
        alias_matches = []
        for source in alias_rows[alias]:
            idx = int(source["index"])
            matched = pair[idx]
            ensure(source["record_sha256"] == matched["patch_record_sha256"], "official patch record changed")
            native_index, = map(int, matched["native_exact_indices"].split(","))
            patch_bitmap = int(matched["bitmapno"])
            patch_qualification = "EXACT_NATIVE_RECORD_AND_RD_STRUCTURE"
            if matched["qualification"] != patch_qualification:
                corrected = accepted_patch[idx]
                exception = accepted_native[native_index]
                ensure(corrected["native_exact_indices"] == [native_index] and
                       corrected["bitmapno"] == patch_bitmap == exception["bitmapno"] and
                       matched["rd_sha256"] == exception["rd_sha256"], "patch flag-0 exception drift")
                patch_qualification = RAW_SIZE
            alias_matches.append({
                "patch_row": idx, "tw85_adrn_row": native_index, "physical_bitmap": patch_bitmap,
                "original_patch_full_adrn_record_sha256": source["record_sha256"],
                "rd_sha256": matched["rd_sha256"],
                "same_cn50_selected_rd": matched["rd_sha256"] == rd_sha,
                "qualification": patch_qualification,
            })
        routes = []
        for group in named["spr_groups"]:
            c, t = route_indices[group["spr_group"]]
            counts = cn_f[c]
            ensure(counts.total() == group["frame_record_count"], "original group frame count changed")
            routes.append({
                "sprite_group": group["spr_group"], "cn50_index": c, "tw85_index": t,
                "same_original_spr_sha256": group["sha256"], "frames": counts.total(),
                "sentinels": counts.get(None, 0),
            })
        records.append({
            "cn50_album_ordinal": named["ordinal"], "cn50_compiled_name": named["compiled_name"],
            "also_in_2003_fusion_catalogues": named["ordinal"] in cohort,
            "cn50_portrait_alias": alias, "cn50_selected_physical_bitmap": bitmap,
            "tw85_same_physical_portrait_rd_sha256": tw_ad[bitmap][2]["rd_sha256"],
            "official_patch_alias_matches": alias_matches, "routes": routes,
        })

    def palettes(records, path_key):
        files = {}
        for r in records:
            match = re.fullmatch(r"palet+_(\d+)\.sap", Path(r[path_key]).name, re.I)
            if match:
                files[int(match[1])] = (r["size"], r["sha256"])
        return files

    cn_pal = palettes(cn_files, "installed_path")
    tw_pal = palettes(tw_files, "path")
    ensure(cn_pal == tw_pal and set(cn_pal) == set(range(16)), "installed palettes differ")
    fusion_records = [r for r in records if r["also_in_2003_fusion_catalogues"]]
    fusion_frames = set().union(*(set(cn_f[x["cn50_index"]]) for r in fusion_records for x in r["routes"])) - {None}
    raw_exceptions = sorted(b for b in wanted if cn_ad[b][3] == RAW_SIZE)
    later_only = tw_groups.keys() - cn_groups.keys()
    cn_numbers = {key[0] for key in cn_groups}
    cn_hashes = {key[1] for key in cn_groups}
    ensure(all(number not in cn_numbers and fingerprint not in cn_hashes for number, fingerprint in later_only),
           "later SPR difference is not a distinct number and digest")
    return {
        "schema": "stoneage.pet.cn50_tw85_art_retention.r1",
        "scope": "TWO_PRESERVED_PC_CARRIERS_AND_AN_OFFICIAL_PATCH_METADATA",
        "tw85_runtime_pet_selector_or_name_table_verified": False,
        "official_release_or_gameplay_verified": False,
        "source_git_blobs": {str(path): pin for path, pin in INPUTS.values()},
        "metrics": {
            "name_slots": summary(records, wanted_frames),
            "fusion_slots": summary(fusion_records, fusion_frames),
            "cn50_preserved_spr_groups_with_same_tw85_number_and_digest": len(cn_groups.keys() & tw_groups.keys()),
            "cn50_preserved_spr_groups_without_same_tw85_number_and_digest": len(cn_groups.keys() - tw_groups.keys()),
            "tw85_additional_distinct_sprite_group_numbers": len({key[0] for key in later_only}),
            "tw85_additional_physical_sprite_groups": sum(len(tw_groups[key]) for key in later_only),
            "same_static_palette_files": len(cn_pal),
            "rd_flag0_adrn_length_exceptions": raw_exceptions,
        },
        "records": records,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build()
    records = report.pop("records")
    body = json.dumps(report, ensure_ascii=False, indent=2)
    rows = ",\n".join("    " + json.dumps(r, ensure_ascii=False) for r in records)
    result = body[:-2] + ',\n  "records": [\n' + rows + "\n  ]\n}"
    if args.write:
        TARGET.write_text(result + "\n", encoding="utf-8")
    else:
        ensure(TARGET.read_text(encoding="utf-8") == result + "\n", "saved retention report changed")
    print(json.dumps(report["metrics"], ensure_ascii=False))


if __name__ == "__main__":
    main()
