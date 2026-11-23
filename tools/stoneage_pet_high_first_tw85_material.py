"""PET-HIGH-FIRST-09: TW85 source-only visual/action references, never live species.

Reuse pinned archived indexes. No commercial image, binary, sprite, or pixel
payload is downloaded or placed into public Git. No native game is executed.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

from tools.stoneage_pet126l_cn50_table_graphic_probe import read_gz_rows
from tools.stoneage_pet_high_first_cn50_catalog import git_blob

ROOT = Path(__file__).resolve().parents[1]
P = Path("research/pets")
R = Path("research/recovered")
TARGET = ROOT / P / "PET-HIGH-FIRST-TW85-VISUAL-ACTION-REFERENCES-R1.json"
INPUTS = {
    "bridge": (P / "PET-HIGH-FIRST-TW85-NATIVE-SPR-ALBUM-R1.json", "e7cff0d53585964c9d755ef1fbd2bc5531d883d6"),
    "cn50": (P / "PET-HIGH-FIRST-CN50-NATIVE-SPR-ALBUM-R1.json", "98fea71c051dfa887b91154a8a72d17c67b57744"),
    "r28_groups": (R / "tw85-spr137-r28/SPR-GROUP-R28.tsv.gz", "f201f85ced4a55d59d38ef774711406c59cddbd4"),
    "r28_frames": (R / "tw85-spr137-r28/SPR-FRAME-R28.tsv.gz", "831fa633adc5bb1f401ee17fca186d476d146196"),
    "r29_groups": (R / "tw85-frame-bitmap-r29/GROUP-MATERIAL-R29.tsv.gz", "273e0c00ab1e1f7aee40815679b00631cd302231"),
    "patch": (R / "wayi-adrn129-patch-metadata/INDEX-1-R1.tsv.gz", "065ecc874adc637098dc7c8f177e478bc7b6f054"),
    "pairs": (R / "adrn129-tw85-real-pair/PAIRS-R1.tsv.gz", "7f41ca49ff576914764b77f22684fbc113e1d90e"),
    "native": (R / "adrn129-tw85-real-pair/NATIVE-R1.tsv.gz", "ffb7b3340116ecaf57daa08242c1ce271e3ad86f"),
}
PROGRAMS = ("sa.exe", "sb.exe", "sc.exe", "sd.exe")
FRAME_FIELDS = ("anim_index", "frame_index", "bmp_no", "pos_x", "pos_y", "sound_no", "sentinel")
GROUP_FIELDS = ("frame_occurrences", "sentinel_frames", "mapped_frames", "missing_frames",
                "distinct_bitmap_ids", "missing_bitmap_ids", "distinct_mapped_rd_contents",
                "raw_sound_word_occurrences")


def must(condition, message):
    if not condition:
        raise ValueError(message)


def verified_paths():
    out = {}
    for key, (relative, pin) in INPUTS.items():
        path = ROOT / relative
        must(path.is_file() and git_blob(path.read_bytes()) == pin, "input changed: " + str(relative))
        out[key] = path
    return out


def as_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def build():
    paths = verified_paths()
    bridge = as_json(paths["bridge"])
    cn50 = as_json(paths["cn50"])
    must(bridge["schema"] == "stoneage.pet.high_first_08_original_tw85_pc_source_selector_sprite_to_named_album.r1",
         "wrong native selector provenance")
    must(bridge["native_executable_loaded_or_server_issued_pet"] is False
         and bridge["metrics"]["official_confirmed_pet_species"] == 0,
         "native route or live status invented")
    must(len(bridge["records"]) == 550, "missing original extra SPR graph records")

    original = list(read_gz_rows(paths["r28_groups"]))
    material = list(read_gz_rows(paths["r29_groups"]))
    must(len(original) == len(material) == 1739, "original group index changed")
    wanted = {
        o["source_occurrence_index"]
        for record in bridge["records"] for o in record["source_spr_occurrences"]
    }
    must(len(wanted) == 554, "duplicates or original physical index lost")
    for index in wanted:
        g, m = original[index], material[index]
        must(int(g["index"]) == int(m["group_index"]) == index
             and g["spr_no"] == m["spr_no"], "physical group mismatch")
        must(m["source_scope"] == "R28_UNMATCHED_CN50_SPR_SEGMENT",
             "extra high-version group scope changed")

    # Hash original ordered frame descriptors; preserve raw animation indices
    # without pretending they are an observed attack/walk/special semantic.
    hashes = {i: hashlib.sha256() for i in wanted}
    frame_counts = Counter()
    sentinels = Counter()
    raw_anim = defaultdict(Counter)
    for row in read_gz_rows(paths["r28_frames"]):
        index = int(row["group_index"])
        if index not in wanted:
            continue
        hashes[index].update(("\t".join(row[key] for key in FRAME_FIELDS) + "\n").encode("ascii"))
        frame_counts[index] += 1
        sentinels[index] += int(row["sentinel"])
        raw_anim[index][int(row["anim_index"])] += 1

    # Original 28B table +24 is an *alias*, not a physical bitmap index.
    # The official patch contributes alias labels; saved native ADRN/REAL
    # supplies physical bitmap and exact RD source hashes. Preserve duplicates.
    aliases = {
        int(route["original_portrait_alias_u32"])
        for record in bridge["records"] for route in record["program_routes"].values()
        if route["record_source_status"] == "SOURCE_LOCAL_NAMED_ROUTE"
    }
    must(len(aliases) == 207, "native named album alias coverage changed")
    alias_patch = defaultdict(list)
    for row in read_gz_rows(paths["patch"]):
        alias = int(row["map_number"])
        if alias in aliases:
            alias_patch[alias].append({
                "patch_index": int(row["index"]),
                "full_patch_adrn_record_sha256": row["record_sha256"],
            })
    patch_indices = {row["patch_index"] for rows in alias_patch.values() for row in rows}
    pairs = {}
    selected_native = set()
    for row in read_gz_rows(paths["pairs"]):
        idx = int(row["patch_index"])
        if idx not in patch_indices:
            continue
        must(idx not in pairs, "duplicate patch physical row")
        natives = [int(x) for x in row["native_exact_indices"].split(",") if x]
        pairs[idx] = {
            "bitmapno": int(row["bitmapno"]),
            "patch_record_sha256": row["patch_record_sha256"],
            "rd_sha256": row["rd_sha256"],
            "source_pair_qualification": row["qualification"],
            "exact_native_indices": natives,
        }
        selected_native.update(natives)
    must(set(pairs) == patch_indices, "missing source patch/REAL pair")

    native = {}
    for row in read_gz_rows(paths["native"]):
        idx = int(row["index"])
        if idx in selected_native:
            native[idx] = {
                "bitmapno": int(row["bitmapno"]),
                "width": int(row["width"]),
                "height": int(row["height"]),
                "rd_sha256": row["rd_sha256"],
                "original_adrn_record_sha256": row["record_sha256"],
                "rd_status": row["rd_status"],
            }
    must(set(native) == selected_native, "missing original native RD rows")
    portrait = {}
    portrait_metrics = Counter()
    for alias in sorted(aliases):
        matches = []
        for patch in alias_patch[alias]:
            pair = pairs[patch["patch_index"]]
            must(pair["patch_record_sha256"] == patch["full_patch_adrn_record_sha256"],
                 "patch record/RD pair mismatch")
            candidates = []
            for native_idx in pair["exact_native_indices"]:
                record = native[native_idx]
                must(record["bitmapno"] == pair["bitmapno"]
                     and record["rd_sha256"] == pair["rd_sha256"],
                     "exact native physical RD mismatch")
                candidates.append({"original_native_index": native_idx, **record})
            matches.append({
                **patch,
                "physical_bitmapno": pair["bitmapno"],
                "saved_tw85_real_rd_sha256": pair["rd_sha256"],
                "patch_to_native_qualification": pair["source_pair_qualification"],
                "native_exact_candidates": candidates,
                "renderer_default_choice_proven": False,
            })
        portrait[str(alias)] = matches
        portrait_metrics["aliases_with_patch_records" if matches else "aliases_not_in_patch"] += 1
        portrait_metrics["patch_candidate_rows"] += len(matches)
        portrait_metrics["exact_native_record_candidates"] += sum(len(x["native_exact_candidates"]) for x in matches)

    records = []
    named_by_program = Counter()
    named_graphic_count = 0
    for source in bridge["records"]:
        graphic = source["tw85_original_spr_number"]
        groups = []
        for occurrence in source["source_spr_occurrences"]:
            index = occurrence["source_occurrence_index"]
            g, m = original[index], material[index]
            must(int(g["spr_no"]) == graphic
                 and g["segment_sha256"] == occurrence["original_spr_segment_sha256"]
                 and int(g["anim_count"]) == occurrence["original_animation_header_count"],
                 "native SPR source span changed")
            measurements = {key: int(m[key]) for key in GROUP_FIELDS}
            must(measurements["frame_occurrences"] == frame_counts[index]
                 and measurements["sentinel_frames"] == sentinels[index],
                 "frame / R29 conservation changed")
            must(measurements["frame_occurrences"] ==
                 measurements["sentinel_frames"] + measurements["mapped_frames"] + measurements["missing_frames"],
                 "incomplete frame classification")
            groups.append({
                "original_source_group_index": index,
                "original_full_spr_segment_sha256": g["segment_sha256"],
                "original_animation_headers": int(g["anim_count"]),
                "raw_animation_index_frame_counts": [
                    {"original_raw_index": k, "frame_positions": v}
                    for k, v in sorted(raw_anim[index].items())
                ],
                "ordered_frame_reference_sha256": hashes[index].hexdigest(),
                "all_frame_bitmap_references_qualified_in_same_saved_carrier":
                    measurements["missing_frames"] == 0,
                **measurements,
            })
        routes = {}
        have_name = False
        for filename in PROGRAMS:
            lane = source["program_routes"][filename]
            status = lane["record_source_status"]
            if status == "SOURCE_LOCAL_NAMED_ROUTE":
                named_by_program[filename] += 1
                have_name = True
            routes[filename] = {
                "local_album_slot": lane["local_album_slot"],
                "status": status,
                "original_name_cp950": lane["original_name_cp950"],
                "original_first_i32": lane["original_first_i32"],
                "original_28b_record_sha256": lane["original_album_row_sha256"],
                "source_portrait_alias": lane["original_portrait_alias_u32"],
                "historical_official_live_release_verified": False,
            }
        named_graphic_count += have_name
        records.append({
            "tw85_original_spr_no_not_official_pet_id": graphic,
            "original_physical_sprite_occurrences": groups,
            "original_native_program_routes": routes,
            "cross_executable_name_conflict": source["graphic_has_conflicting_names_across_installer_programs"],
            "original_skill_stats_capture_birth_growth_and_release": None,
            "native_runtime_action_semantics_verified": False,
        })
    must(named_graphic_count == 514 and dict(named_by_program) == {
        "sa.exe": 508, "sb.exe": 497, "sc.exe": 227, "sd.exe": 464
    }, "native qualified name evidence drift")
    must(sum(x["cross_executable_name_conflict"] for x in records) == 41,
         "source program variants collapsed")
    cn_alias = {row["portrait_alias"] for row in cn50["records"]}
    new_alias = aliases - cn_alias
    must(len(new_alias) == 203, "high version original alias candidates changed")
    all_groups = [g for r in records for g in r["original_physical_sprite_occurrences"]]
    totals = Counter()
    for g in all_groups:
        for key in GROUP_FIELDS:
            totals[key] += g[key]
    return {
        "schema": "stoneage.pet.high_first_09.tw85_source_visual_action_reference.r1",
        "source_scope": "PRESERVED_TW85_CLASSIC_PC_UNCERTIFIED_OFFICIAL_PRESSING",
        "source_pins_git_blob": {key: {"path": str(path.relative_to(ROOT)),
                                       "blob_sha": INPUTS[key][1]}
                                 for key, path in paths.items()},
        "metrics": {
            "extra_source_graphic_numbers_not_species": len(records),
            "source_physical_sprite_occurrences": len(all_groups),
            "graphic_numbers_with_any_source_local_name": named_graphic_count,
            "graphic_numbers_without_source_local_name": 550 - named_graphic_count,
            "per_program_named_graphic_numbers": dict(named_by_program),
            "cross_executable_name_conflict_graphics": 41,
            "distinct_source_local_portrait_aliases": len(aliases),
            "source_local_portrait_aliases_not_in_cn50_named_catalog": len(new_alias),
            **dict(portrait_metrics),
            "source_physical_group_frame_metrics": dict(totals),
            "official_live_species_newly_verified": 0,
            "original_rd_pixels_rendered_in_this_work": 0,
        },
        "boundaries": {
            "source_local_name_is_not_official_live_release": True,
            "patch_alias_is_not_physical_rd_bitmapno": True,
            "no_default_winner_for_duplicate_patch_or_adrn_records": True,
            "raw_animation_indices_are_not_observed_gameplay_actions": True,
            "full_original_program_execution_verified": False,
            "original_private_pixels_in_public_report": False,
            "historic_same_deployment_pet_master_skill_capture": False,
        },
        "portrait_alias_to_saved_tw85_native_rd_candidates": portrait,
        "records": records,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("generate", "verify"), default="verify")
    args = parser.parse_args()
    expected = json.dumps(build(), ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.mode == "generate":
        TARGET.write_text(expected, encoding="utf-8")
    else:
        must(TARGET.read_text(encoding="utf-8") == expected,
             "published derived report differs from pinned original source replay")
    m = json.loads(expected)["metrics"]
    print(json.dumps({"mode": args.mode, **{k: m[k] for k in (
        "extra_source_graphic_numbers_not_species",
        "source_physical_sprite_occurrences",
        "graphic_numbers_with_any_source_local_name",
        "distinct_source_local_portrait_aliases",
        "aliases_with_patch_records",
        "aliases_not_in_patch",
        "patch_candidate_rows",
        "exact_native_record_candidates",
    )}}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
