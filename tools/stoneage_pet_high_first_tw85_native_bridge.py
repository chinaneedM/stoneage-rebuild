"""Query/independently replay source-qualified TW85 native SPR→local album bridges.

These are original *client-local conditional* routes, NOT live official pet IDs.
Source binary/whole disassembly and proprietary graphics are not needed/read.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/pets/PET-HIGH-FIRST-TW85-NATIVE-SPR-ALBUM-R1.json"
SPR = ROOT / "research/pets/PET-HIGH-FIRST-TW85-EXTRA-SPR-GROUPS-R1.json"
ALBUM = ROOT / "research/pets/PET-HIGH-FIRST-TW85-ORIGINAL-PE-ALBUM-GRID-R1.json"
SCHEMA = "stoneage.pet.high_first_08_original_tw85_pc_source_selector_sprite_to_named_album.r1"
PROGRAMS = ("sa.exe", "sb.exe", "sc.exe", "sd.exe")
EXPECTED = {
    "sa.exe": (508, 207, 16, 26, 22),
    "sb.exe": (497, 190, 3, 50, 21),
    "sc.exe": (227, 106, 0, 323, 13),
    "sd.exe": (464, 182, 0, 86, 20),
}


def load():
    obj = json.loads(REPORT.read_text(encoding="utf-8"))
    if obj.get("schema") != SCHEMA or obj.get("source_grade") != (
        "UNVERIFIED_COMMUNITY_PRESERVED_CLAIMED_WAYI85_INSTALLER"
    ):
        raise ValueError("wrong TW85 original source evidence grade")
    return obj


def route_slot(segment_list, graphic):
    if isinstance(graphic, bool) or not isinstance(graphic, int):
        raise ValueError("graphic must be an integer")
    matches = [s for s in segment_list if s["first_graphic"] <= graphic <= s["last_graphic"]]
    if len(matches) != 1:
        raise ValueError("source graphic absent or ambiguous in source-bounded selector segments")
    return graphic + matches[0]["slot_minus_graphic"]


def validate(report=None):
    """Reconcile every native result against both independently retained sources."""
    report = load() if report is None else report
    if report.get("schema") != SCHEMA:
        raise ValueError("bad source report schema")
    if not report["source_program_provenance"]["original_full_EXE_or_code_published"] is False:
        raise ValueError("copyright source boundary breached")
    if report["native_executable_loaded_or_server_issued_pet"] is not False:
        raise ValueError("unproven source operator activation")
    if report["metrics"]["official_confirmed_pet_species"] != 0:
        raise ValueError("local names are not official live pet species")
    if not all(report["boundaries"].values()) or report["boundaries"]["new_official_pet_species_count"] != 0:
        raise ValueError("source evidence gate violated")
    old = json.loads(SPR.read_text(encoding="utf-8"))
    album = json.loads(ALBUM.read_text(encoding="utf-8"))
    if old["metrics"]["tw85_only_distinct_spr_numbers"] != 550 or len(report["records"]) != 550:
        raise ValueError("source graph number coverage changed")
    if old["metrics"]["tw85_only_physical_group_records"] != 554:
        raise ValueError("physical group source multiplicity changed")
    if set(report["programs"]) != set(PROGRAMS):
        raise ValueError("one of the four original program variants missing")
    atlas_names = {
        f: {row["slot"]: row for row in album["programs"][f]["source_records"]}
        for f in PROGRAMS
    }
    atlas_blank = {
        f: {row["slot"]: row for row in album["programs"][f]["blank_or_unqualified"]}
        for f in PROGRAMS
    }
    segments_by_program = {}
    counters = {f: Counter() for f in PROGRAMS}
    seen_slots = {f: set() for f in PROGRAMS}
    records = report["records"]
    seen = set()
    for f in PROGRAMS:
        p = report["programs"][f]
        segments = p["source_rule_segments_for_550_graphic_numbers"]
        if not segments or segments[0]["first_graphic"] != 101501 or segments[-1]["last_graphic"] != 102050:
            raise ValueError(f + " missing exact bounded sprite range")
        for one, two in zip(segments, segments[1:]):
            if one["last_graphic"] + 1 != two["first_graphic"]:
                raise ValueError(f + " noncontiguous selector source range")
        if p["original_pet_album_record_stride_bytes"] != 28:
            raise ValueError(f + " original album row stride changed")
        if p["normalization_compiled_signed_negative_100250"] != "add_eax_0xfffe7866":
            raise ValueError(f + " original native graphic normalization changed")
        if not p["original_run_time_count_and_activation_unverified"]:
            raise ValueError(f + " runtime activation must not be invented")
        if p["original_executable_sha256"] != album["programs"][f]["packed_sha256"]:
            raise ValueError(f + " no exact source executable provenance")
        if p["original_unpacked_sha256"] != album["programs"][f]["unpacked_sha256"]:
            raise ValueError(f + " no exact unpacked source byte provenance")
        segments_by_program[f] = segments
    physical = 0
    variant_conflicts = 0
    for source, record in zip(old["records"], records, strict=True):
        graphic = source["tw85_original_spr_number"]
        if graphic in seen or graphic != record["tw85_original_spr_number"]:
            raise ValueError("source graphic number identity/order drift")
        seen.add(graphic)
        expected_occurrences = [{
            "source_occurrence_index": x["index"],
            "original_spr_segment_sha256": x["segment_sha256"],
            "original_animation_header_count": x["animation_headers"],
        } for x in source["source_occurrences"]]
        if record["source_spr_occurrences"] != expected_occurrences:
            raise ValueError(f"lost duplicate or modified original SPR physical record: {graphic}")
        physical += len(expected_occurrences)
        if set(record["program_routes"]) != set(PROGRAMS):
            raise ValueError("one original program lane missing")
        names = set()
        for filename in PROGRAMS:
            entry = record["program_routes"][filename]
            if entry["source_exe_name"] != filename:
                raise ValueError("mismatched original executable lane")
            if entry["historical_official_live_pet_release_confirmed"]:
                raise ValueError("client graphics do not prove live official pet")
            slot = route_slot(segments_by_program[filename], graphic)
            if entry["local_album_slot"] != slot:
                raise ValueError(f"native original source segment replay mismatch: {graphic} {filename}")
            qualified = atlas_names[filename].get(slot)
            unresolved = atlas_blank[filename].get(slot)
            if qualified is not None:
                if (entry["record_source_status"] != "SOURCE_LOCAL_NAMED_ROUTE"
                        or entry["original_name_cp950"] != qualified["original_name_cp950"]
                        or entry["original_first_i32"] != qualified["original_first_i32"]
                        or entry["original_portrait_alias_u32"] != qualified["source_portrait_alias"]
                        or entry["original_album_row_sha256"] != qualified["original_row_sha256"]):
                    raise ValueError(f"qualified original program name/alias/row proof mismatch {graphic} {filename}")
                counters[filename]["named"] += 1
                seen_slots[filename].add(slot)
                names.add(entry["original_name_cp950"])
            elif unresolved is not None:
                if (entry["record_source_status"] != "SOURCE_BLANK_OR_UNQUALIFIED"
                        or entry["original_album_unqualified_row_sha256"] != unresolved["original_row_sha256"]
                        or entry["original_name_cp950"] is not None):
                    raise ValueError(f"original blank or unqualified native source altered {graphic} {filename}")
                counters[filename]["unknown"] += 1
            elif slot >= album["programs"][filename]["total_grid_slots"] or slot < 0:
                if (entry["record_source_status"] != "OUTSIDE_QUALIFIED_LOCAL_GRID"
                        or entry["original_name_cp950"] is not None):
                    raise ValueError(f"out-of-table sprite incorrectly promoted to named {graphic} {filename}")
                counters[filename]["outside"] += 1
            else:
                raise ValueError(f"source slot not fully accounted {graphic} {filename}")
        conflict = len(names) > 1
        if record["graphic_has_conflicting_names_across_installer_programs"] != conflict:
            raise ValueError("different original source names silently flattened")
        variant_conflicts += int(conflict)
        if record["official_in_game_release_confirmed"] or record["original_server_pet_id"] is not None:
            raise ValueError("pet server identity falsely promoted")
    if len(seen) != 550 or physical != 554 or variant_conflicts != 41:
        raise ValueError("source conservation/conflicting local names mismatch")
    for filename in PROGRAMS:
        e = EXPECTED[filename]
        m = report["metrics"]["per_program"][filename]
        actual = (counters[filename]["named"], len(seen_slots[filename]),
                  counters[filename]["unknown"], counters[filename]["outside"],
                  len(segments_by_program[filename]))
        if actual != e or actual != (
            m["named_graphic_numbers"], m["distinct_named_local_album_slots"],
            m["blank_or_unqualified_graphic_numbers"],
            m["outside_local_source_grid_graphic_numbers"],
            m["source_route_segments"]):
            raise ValueError(filename + " source-clients record conservation mismatch")
    return {"same_build_conditional_source_only": True,
            "source_graphic_numbers": 550,
            "source_physical_sprite_groups": 554,
            "per_program": report["metrics"]["per_program"],
            "source_graphic_name_conflicts_across_programs": variant_conflicts,
            "official_live_pet_species_confirmed": 0}


def query(report, *, graphic=None, name="", program=None, limit=30):
    output = []
    for record in report["records"]:
        if graphic is not None and graphic != record["tw85_original_spr_number"]:
            continue
        for filename, variant in record["program_routes"].items():
            if program and program != filename:
                continue
            if name and name.casefold() not in (variant["original_name_cp950"] or "").casefold():
                continue
            output.append({
                "original_tw85_spr_group": record["tw85_original_spr_number"],
                "original_group_occurrences": record["source_spr_occurrences"],
                "source_program": filename,
                "program_local_action_object_route_only": True,
                "official_live_pet_issued": False,
                "different_source_names": record["graphic_has_conflicting_names_across_installer_programs"],
                **variant,
            })
            if len(output) >= limit:
                return output
    return output


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--sprite", type=int)
    p.add_argument("--name", default="")
    p.add_argument("--program", choices=PROGRAMS)
    p.add_argument("--limit", type=int, default=30)
    p.add_argument("--summary", action="store_true")
    p.add_argument("--verify", action="store_true")
    args = p.parse_args()
    if not 1 <= args.limit <= 3000:
        p.error("--limit must be 1 to 3000")
    obj = load()
    if args.verify:
        print(json.dumps(validate(obj), ensure_ascii=False, indent=2))
    elif args.summary:
        print(json.dumps(obj["metrics"], ensure_ascii=False, indent=2))
    else:
        print(json.dumps(query(obj, graphic=args.sprite, name=args.name,
                               program=args.program, limit=args.limit),
                         ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
