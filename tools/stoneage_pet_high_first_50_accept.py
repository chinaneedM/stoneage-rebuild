"""Check PET50 archival custody, independently replay its joins, and audit VipPet."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
from zipfile import ZipFile
import zlib

from tools import stoneage_pet_high_first_50_source as source
from tools.stoneage_native_album_source_r36 import (
    SparseParts,
    fetcher_factory,
    isolated_rar,
)
from tools.stoneage_preserved_item_shop_r44 import PREFIX

REPORT = source.P / "PET-HIGH-FIRST-50-ORIGINAL-ACQUISITION-R1.json"
ZIP_SHA256 = "ac513a71258260c3b50baef502be9e89e99a69512e928432f77380099fa8234f"
REPORT_SHA256 = "0f57d7a41e57d22080fc72e4a871063c389da162ca262a59e20f8603fcdcb52e"
REPORT_BLOB = "4d0b31a7fa196cf8f227a7b0b1aea7183d9598f0"
TRAINERS = {2481: 161, 2482: 162, 2483: 163, 2484: 164}
EXPECTED_SUMMARY = {
    "target_rows": 67,
    "selected_exact_with_instance": 62,
    "selected_with_instance": 65,
    "alternate_exact_with_instance": 1,
    "alternate_exact_positive_double_templates": 0,
    "npc_member_count": 6,
    "npc_candidate_lines": 37,
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def physical_lines(pet10, path):
    member = pet10["verified_original_archive_members"][path]
    return [line for line in range(1, member["physical_lines"] + 1)
            if line not in member["blank_physical_lines"]]


def accept(artifact):
    raw = REPORT.read_bytes()
    assert (len(raw), sha(raw), source.r40.git_blob(raw)) == (
        243336, REPORT_SHA256, REPORT_BLOB,
    )
    if artifact:
        assert sha(artifact.read_bytes()) == ZIP_SHA256
        with ZipFile(artifact) as archive:
            assert archive.namelist() == ["pet50-derived.json"]
            assert archive.read("pet50-derived.json") == raw

    report = json.loads(raw)
    assert report["scope"] == "PRESERVED_MIXED25_NOT_OFFICIAL_DEPLOYMENT"
    assert report["input_git_blobs"] == {k: digest for k, (_, digest) in source.PINS.items()}
    assert report["original_payload_published"] is False
    d = source.load()
    rec = report["member_receipt"]
    members = {m["path"].removeprefix(PREFIX): m for m in rec["members"]}
    expected = {"setup.cf"} | {"data/" + n for n in source.TABLES} | {
        "data/npc/" + n for n in source.NPCS
    }
    assert len(members) == len(rec["members"]) == report["original_member_count"] == 12
    assert members.keys() == expected
    inventory = {f["path"]: f for f in d["r18"]["all_server_occurrences"]}
    for path, m in members.items():
        if path == "setup.cf":
            expected_member = source.r40.PINS[path]
        else:
            prior = inventory[path.removeprefix("data/")]
            expected_member = (prior["size"], prior["sha256"])
        assert (m["bytes"], m["sha256"]) == expected_member
        pet10 = d["pet10"]["verified_original_archive_members"].get(path.removeprefix("data/"))
        if pet10:
            assert m["crc32"] == int(pet10["archive_record_crc32"], 16)
        assert m["data_offset"] > m["header_offset"]
        assert m["flags"] & 23 == 0
    ranges = rec["range_receipts"]
    assert rec["whole_archive_or_parts_rehashed"] is False
    assert rec["headers_visited"] == 7954
    assert len(ranges) == rec["range_requests"] == 184
    assert sum(r["bytes"] for r in ranges) == rec["actual_range_bytes"] == 12013836

    p = report["projection"]
    for k in ("official_acquisition_verified", "runtime_executed", "alternate_config_deployed"):
        assert p[k] is False
    assert p["official_species_count"] is None
    assert p["instance_schema"]["enemy2.txt"] == {
        "id": 2, "template": 3, "pet_flag": None, "levels": None,
    }
    assert p["summary"] == EXPECTED_SUMMARY
    records = p["records"]
    assert [r["tw75_row_index"] for r in records] == d["prev"]["remaining_gap_row_indices"]
    matches = Counter()
    tiger_links = {}
    nonempty_group_positions = set()
    for pair_index, (base, enemy) in enumerate((
        ("enemybase.txt", "enemy.txt"), ("enemybase2.txt", "enemy2.txt"),
    )):
        templates = {r[1]: r for r in d["pet10"]["source_rows"][base]}
        instances = defaultdict(dict)
        positions = physical_lines(d["pet10"], enemy)
        for ordinal, instance, template, _, _ in d["pet10"]["source_rows"][enemy]:
            instances[template][instance] = positions[ordinal - 1]
        for r in records:
            index, tid = r["tw75_row_index"], r["template_id"]
            master = d["master"]["pet_flag_1_field_projections"][index]
            assert {k: r[k] for k in ("template_id", "graphic", "name", "row_sha256")} == {
                k: master[k] for k in ("template_id", "graphic", "name", "row_sha256")
            }
            row = templates.get(tid)
            q = r["source_pairs"][pair_index]
            match = "ABSENT" if row is None else (
                "EXACT_ROW" if row[16] == master["row_sha256"] else "SAME_ID_DIFFERENT_ROW"
            )
            assert (q["base"], q["enemy"], q["match"]) == (base, enemy, match)
            assert q["base_pet_flag"] == (row[3] if row else None)
            assert q["base_row_sha256"] == (row[16] if row else None)
            assert {v["instance_id"]: v["physical_line"] for v in q["instances"]} == instances[tid]
            matches[pair_index, match, bool(q["instances"])] += 1
            for instance in q["instances"]:
                eid = instance["instance_id"]
                if pair_index:
                    assert all(instance[k] is None for k in ("pet_flag", "level", "raw_level_fields"))
                elif eid in TRAINERS:
                    assert match == "EXACT_ROW" and row[3] == instance["pet_flag"] == 1
                    assert instance["level"] == instance["raw_level_fields"] == [1, 1]
                    tiger_links[eid] = tid
            for group_index, v in enumerate(q["group_variants"]):
                assert v["group"] == ("group1.txt", "group.txt")[group_index]
                assert (v["configuration"] == "SELECTED") == (pair_index == group_index == 0)
                assert v["positive_routes"] == 0
                assert all(not m["positive_area_slots"] for m in v["group_memberships"])
                assert all(m["enemy_id"] in instances[tid] for m in v["group_memberships"])
                if v["group_memberships"]:
                    nonempty_group_positions.add(index)
                for k in ("double_flag_routes", "lv1_double_flag_routes"):
                    assert v[k] == (None if pair_index else 0)
    assert matches[0, "EXACT_ROW", True] == 62
    assert matches[0, "SAME_ID_DIFFERENT_ROW", True] == 3
    assert [r["template_id"] for r in records if not r["source_pairs"][0]["instances"]] == [993, 994]
    assert [r["template_id"] for r in records if r["source_pairs"][1]["match"] == "EXACT_ROW"
            and r["source_pairs"][1]["instances"]] == [854]
    assert nonempty_group_positions == {91, 92, 101, 102, 293}
    assert tiger_links == TRAINERS
    npc = {f["path"]: f for f in p["npc_source_files"]}
    assert set(npc) == set(source.NPCS)
    assert [len(npc[k]["create_refs"]) for k in source.NPCS] == [1, 1, 1, 0, 4, 4]
    literals = [l for f in npc.values() for l in f["candidate_lines"]
                if l["qualification"] == "GETPET_OR_ADDPET_INSTANCE_LITERAL_CANDIDATE"]
    assert len(literals) == 12 and all(l["key"] == "AddPet" for l in literals)
    assert Counter(token for l in literals for token in l["matching_instance_tokens"]) == {
        eid: 3 for eid in TRAINERS
    }
    return report, members, d


def reacquire(report, members):
    from libarchive import ffi, memory_reader

    fetch, _ = fetcher_factory()
    reader = SparseParts(fetch, max_bytes=1024 * 1024, max_requests=16)
    data = {}
    for path, m in members.items():
        header = reader.at(m["header_offset"], m["data_offset"] - m["header_offset"])
        compressed = reader.at(m["data_offset"], m["compressed_bytes"])
        assert (sha(header), sha(compressed)) == (m["header_sha256"], m["compressed_payload_sha256"])
        wrapped = isolated_rar(header, compressed, m["flags"])
        with memory_reader(wrapped) as archive:
            entries = [(e.pathname.replace("\\", "/"), b"".join(e.get_blocks())) for e in archive]
        assert len(entries) == 1 and entries[0][0] == m["path"]
        raw = entries[0][1]
        assert (len(raw), sha(raw), zlib.crc32(raw)) == (m["bytes"], m["sha256"], m["crc32"])
        data[path] = raw
    prior_ranges = {(r["part"], r["start"]): r for r in report["member_receipt"]["range_receipts"]}
    for r in reader.receipts:
        assert prior_ranges[r["part"], r["start"]] == r
    custody = {
        "extractor": "libarchive",
        "extractor_version": ffi.version_number(),
        "matching_member_count": len(data),
        "matching_ranges": reader.receipts,
        "range_bytes": reader.fetched,
    }
    return data, custody


def vip_menu(data, d, report):
    catalogs = d["master"]["pet_flag_1_field_projections"]
    catalog_by_template = {r["template_id"]: (i, r) for i, r in enumerate(catalogs)}
    selected_base = {r[1]: r for r in d["pet10"]["source_rows"]["enemybase.txt"]}
    selected_enemy = {r[1]: r for r in d["pet10"]["source_rows"]["enemy.txt"]}
    positions = physical_lines(d["pet10"], "enemy.txt")
    reference = {f["path"]: f for f in report["projection"]["npc_source_files"]}
    repeat = set(d["prev"]["remaining_gap_row_indices"])
    files = []
    for path in source.NPCS[:4]:
        menu = data["data/npc/" + path]
        rows = []
        for block in menu.split(b"}"):
            labels = re.findall(rb"(?mi)^\s*MenuStr\s*[:=]", block)
            fields = re.findall(rb"(?mi)^\s*VipPet\s*[:=]\s*([^\r\n]*)", block)
            if not fields:
                assert not labels
                continue
            assert len(fields) == len(labels) == 1
            value = fields[0].strip()
            m = re.fullmatch(rb"([0-9]+|MM[1-4])\s*,\s*(-?[0-9]+)", value)
            assert m is not None, (path, sha(value), len(value))
            token, price = m.groups()
            # MM aliases depend on a descendant build macro. Keep those unresolved.
            instance = selected_enemy.get(int(token)) if token.isdigit() else None
            template = selected_base.get(instance[2]) if instance else None
            catalog = catalog_by_template.get(instance[2]) if instance else None
            exact = bool(template and catalog and template[16] == catalog[1]["row_sha256"])
            rows.append({
                "menu_position": len(rows) + 1,
                "value_sha256": sha(value),
                "enemy_id": int(token) if token.isdigit() else None,
                "conditional_alias": None if token.isdigit() else token.decode("ascii"),
                "raw_vip_points": int(price),
                "selected_template_id": instance[2] if instance else None,
                "selected_instance_physical_line": positions[instance[0] - 1] if instance else None,
                "exact_tw75_template_position": catalog[0] if exact else None,
                "among_67_residual_positions": bool(exact and catalog[0] in repeat),
            })
        assert len(rows) == reference[path]["key_counts"]["VipPet"]
        files.append({
            "path": path,
            "create_reference_count": len(reference[path]["create_refs"]),
            "rows": rows,
        })
    return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", type=Path)
    parser.add_argument("--replay-output", type=Path)
    args = parser.parse_args()
    report, members, d = accept(args.artifact)
    print("PET50_ARCHIVE_PASS", EXPECTED_SUMMARY, "trainer_template_links", TRAINERS)
    if args.replay_output:
        data, custody = reacquire(report, members)
        assert source.derive(d, data) == report["projection"]
        menu = vip_menu(data, d, report)
        out = {
            "schema": "stoneage.pet50.original_vip_menu_candidate.r1",
            "archive_git_blob": REPORT_BLOB,
            "source_custody": custody,
            "source_projection_exact": True,
            "menu_files": menu,
            "official_acquisition_verified": False,
            "original_payload_published": False,
        }
        raw = (json.dumps(out, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()
        args.replay_output.write_bytes(raw)
        for f in menu:
            print("PET50_VIP", f["path"], f["create_reference_count"], len(f["rows"]),
                  sum(r["selected_template_id"] is not None for r in f["rows"]),
                  sum(r["exact_tw75_template_position"] is not None for r in f["rows"]),
                  sum(r["among_67_residual_positions"] for r in f["rows"]))
        print("PET50_REPLAY_REPORT", len(raw), sha(raw), source.r40.git_blob(raw))


if __name__ == "__main__":
    main()
