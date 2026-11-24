"""Verify PET51 custody, replay the full original archive sample, and resolve PETABI fields."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
from zipfile import ZipFile
import zlib

from tools import stoneage_pet_high_first_51_source as source

RAW_SCAN = source.pet50.source.P / "PET-HIGH-FIRST-51-ORIGINAL-NPC-CENSUS-R1.json"
DEEP_SCAN = source.pet50.source.P / "PET-HIGH-FIRST-51-PETABI-SOURCE-LINKS-R1.json"
RAW_SCAN_SHA = "7a654c7c9118d0c577f3a2fe9dc8188c3b10e1945bf5e7eed651e32fddd9191f"
RAW_SCAN_BLOB = "14103aa39eba7e98c53e050394c0dff02cd0c7e2"
ZIP_SHA = "d7bf5efdbab82be28b329914056fb633860bb9c883c64bda7e8799f85e16d40b"
DEEP_SCAN_SHA = "9e98d7c300ce0f99d76c4cd2b775441dc1444ff61b9c98401b6abaf151d6fb0f"
DEEP_SCAN_BLOB = "ab826bd89e5d1f39f8f219b5a2803efba02248b9"
ARCHIVE_SHA = "d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5"
GMSV_SHA = "d5b08dbcbf9e8736ba8598e38e5901f123d2bff544a9cae53a9ff88ce1971e00"
UNRAR_COMMIT = "cacdcb8cbe1813b6151e3f92f2ccec7afe4d6a41"
LV1_IDS = {2415, 2416}
EVENT_ACTION_BLOB = "a89b744394079cc476e7e87f6e353d66208e0150"
STRING_UTIL_BLOB = "8065a372bfa0c1d4e74d39fd73b405c7b6a7b569"


def verify_raw(artifact, targets, data):
    raw = RAW_SCAN.read_bytes()
    assert (len(raw), source.digest(raw), source.pet50.source.r40.git_blob(raw)) == (
        67660, RAW_SCAN_SHA, RAW_SCAN_BLOB,
    )
    if artifact:
        assert source.digest(artifact.read_bytes()) == ZIP_SHA
        with ZipFile(artifact) as archive:
            assert archive.namelist() == ["pet51-metadata.json"]
            assert archive.read("pet51-metadata.json") == raw
    scan = json.loads(raw)
    assert scan["target_rows"] == targets
    assert scan["source_pins"] == {
        "r18": source.pet50.source.PINS["r18"][1], "char01": source.pet50.source.PINS["char01"][1],
        "char09": source.ROSTER_BLOB, "pet50": source.pet50.REPORT_BLOB, "pet50_vip": source.pet50.VIP_REPORT_BLOB,
    }
    for field in ("source_pc_official_deployment_verified", "runtime_executed", "original_payload_published"):
        assert scan[field] is False
    assert scan["official_acquisition_closed"] == 0
    c = scan["custody"]
    assert c["unique_member_count"] == len(source.expected_members(data)) == 2207
    assert c["member_bytes"] == 2300545
    assert c["headers_visited"] == 7954
    assert len(c["range_receipts"]) == 184
    assert sum(r["bytes"] for r in c["range_receipts"]) == c["range_bytes"] == 12013836
    assert c["whole_archive_rehashed"] is False and not c["unar_fallback_paths"]
    assert not scan["previous_char09_instance_hits"] and not scan["npc"]["literal_hits"]
    assert scan["previous_char09_args"] == 260
    assert Counter(r["shape"] for r in scan["vip"]) == dict(
        ASCII_DECIMAL=12, CONDITIONAL_MM_ALIAS=2, ASCII_SYMBOLIC=28,
    )
    return scan


def local_members(original_dir, expected):
    data = original_dir / "data"
    assert {p.relative_to(data).as_posix() for p in (data / "npc").rglob("*") if p.is_file()} == {
        k for k in expected if k.startswith("npc/")
    }
    output = {}
    for name, pin in expected.items():
        raw = (data / name).read_bytes()
        assert (len(raw), source.digest(raw), zlib.crc32(raw)) == pin, name
        output[name] = raw
    return output


def compiled_vip_boundary(original_dir, originals):
    path = original_dir / "gmsv.exe"
    raw = path.read_bytes()
    assert (len(raw), source.digest(raw), zlib.crc32(raw)) == (1897867, GMSV_SHA, 0x6e31b63a)
    assert raw.startswith(b"MZ")
    binary = raw.lower()
    names = ("VipShop", "VipPet", "PETABI", "PetShopInit", "GetPet", "AddPet")
    strings = {
        name: {"ascii_occurrences": binary.count(name.lower().encode()),
               "utf16le_occurrences": binary.count(name.lower().encode("utf-16le"))}
        for name in names
    }
    symbols = {}
    for line in subprocess.check_output(["nm", "-P", "-n", str(path)], text=True).splitlines():
        parts = line.split()
        if len(parts) >= 3:
            symbols[parts[0]] = int(parts[2], 16)
    symbol_view = {key: symbols.get(key) for key in (
        "_NPC_VipShopInit", "_NPC_ActionVipPet", "_NPC_ActionNewVipPet",
        "_NPC_PetShopInit", "_NPC_ActionAddPet", "_ActionNpc_CheckMenuFree", "_Action_RunDoEventAction",
    )}
    template = originals["npc/my/vipshop/vipshop.template"]
    assert re.search(rb"(?mi)^functionset=VipShop\s*$", template)
    assert all(not any(strings[key].values()) for key in ("VipShop", "VipPet", "PETABI"))
    assert all(symbol_view[k] is None for k in ("_NPC_VipShopInit", "_NPC_ActionVipPet", "_NPC_ActionNewVipPet"))
    assert all(symbol_view[k] for k in ("_NPC_PetShopInit", "_NPC_ActionAddPet", "_ActionNpc_CheckMenuFree",
                                        "_Action_RunDoEventAction"))
    return {"sha256": GMSV_SHA, "bytes": len(raw), "crc32": f"{zlib.crc32(raw):08x}",
            "string_probes": strings, "symbol_probes": symbol_view,
            "vip_functionset_template_sha256": source.digest(template),
            "configured_functionset": "VipShop", "matching_loader_located_in_preserved_exe": False}


def resolved_petabi(originals, remote, data):
    r40 = source.pet50.source.r40
    p = data["pet10"]["source_rows"]
    bases = {int(a[6]): (line, a) for line, a in r40.rows(originals["enemybase.txt"], 56, 6)}
    instances = {int(a[3]): (line, a) for line, a in r40.rows(originals["enemy.txt"], 34, 3)}
    base_rows = {r[1]: r for r in p["enemybase.txt"]}
    master = data["master"]["pet_flag_1_field_projections"]
    master_ids = {r["template_id"] for r in master}
    residual = set(data["prev"]["remaining_gap_row_indices"])
    spr = {r[1]: r[0] for r in p["spradrn_5.bin"]}
    result = []
    for old in remote["vip"]:
        if not old["previously_unparsed"]:
            continue
        path, line_no = old["path"], old["line"]
        line = originals["npc/" + path].splitlines()[line_no - 1].strip()
        values = re.fullmatch(rb"VipPet:\s*(PETABI(?:[ \t]+[0-9]+){7})\s*,\s*([0-9]+)[ \t]*\|?", line)
        assert values and source.digest(values[1]) == old["token_sha256"], (path, line_no)
        eid, level, trans, hp, attack, defence, speed = [int(x) for x in values[1].split()[1:]]
        price = int(values[2])
        assert price == old["raw_vip_points"]
        e_line, e = instances[eid]
        template = int(e[4])
        b_line, b = bases[template]
        graphic = int(b[36])
        assert graphic == base_rows[template][2]
        template_name = b[0].decode("cp950")
        available_names = [
            {"position": i, "template_id": m["template_id"], "in_prior_residual": i in residual}
            for i, m in enumerate(master)
            if (m["name"], m["graphic"]) == (template_name, graphic)
        ]
        result.append({
            "arg_path": path, "arg_line": line_no, "arg_token_sha256": old["token_sha256"],
            "instance_id": eid, "instance_line": e_line, "instance_name": e[0].decode("cp950"),
            "instance_pet_flag": int(e[13]), "instance_level_range": r40.level(e),
            "template_id": template, "template_line": b_line, "template_name": template_name,
            "template_pet_flag": int(b[37]), "template_row_sha256": base_rows[template][16],
            "graphic_no": graphic, "same_saved_spr_index_candidate": spr.get(graphic),
            "present_in_claimed_tw75_catalog_by_id": template in master_ids,
            "tw75_name_and_graphic_only_references": available_names,
            "preset_fields": {"level": level, "transmigration": trans, "vital": hp,
                              "strength": attack, "toughness": defence, "dexterity": speed},
            "vip_points": price, "official_delivery_verified": False,
        })
    assert len(result) == len({r["instance_id"] for r in result}) == 28
    return result


def independent_npc_lexical_scan(originals):
    instance_ids = source.INSTANCE_IDS | LV1_IDS
    record = []
    for path, raw in originals.items():
        if not path.startswith("npc/"):
            continue
        for line_no, line in enumerate(raw.splitlines(), 1):
            text = line.strip()
            if text.startswith((b"#", b"//")):
                continue
            for part in re.split(rb"[|{}]", text):
                candidate = re.match(rb"\s*([A-Za-z_][A-Za-z_0-9]*)\s*[:=](.*)", part)
                if not candidate:
                    continue
                key, raw_value = candidate.groups()
                nums = {int(i) for i in re.findall(rb"(?<![0-9])-?[0-9]+(?![0-9])", raw_value)}
                instance_hits = nums & instance_ids
                group_hits = nums & source.DIRECTED_GROUPS
                if instance_hits or group_hits:
                    record.append({
                        "source_path": path, "physical_line": line_no, "field": key.decode(),
                        "instance_value_collisions": sorted(instance_hits),
                        "group_value_collisions": sorted(group_hits),
                        "field_digest": source.digest(part.strip()),
                    })
    return record


def reproduce(original_dir, archive_path, remote, data, vip):
    with archive_path.open("rb") as stream:
        assert hashlib.file_digest(stream, "sha256").hexdigest() == ARCHIVE_SHA
    assert archive_path.stat().st_size == 361255180
    originals = local_members(original_dir, source.expected_members(data))
    creation_ids = Counter(ref[0] for row in data["char01"]["create_rows"] for ref in row[-1])
    assert source.scan_npc(originals, creation_ids) == remote["npc"]
    assert source.scan_vip(originals, vip, data) == remote["vip"]
    collisions = independent_npc_lexical_scan(originals)
    assert all(r["field"].lower().encode() not in source.INSTANCE_FIELDS | source.GROUP_FIELDS for r in collisions)
    return {
        "schema": "stoneage.pet51.petabi_preserved_config_links.r1",
        "source_run_projection_git_blob": RAW_SCAN_BLOB,
        "whole_original_archive_bytes": 361255180, "whole_original_archive_sha256": ARCHIVE_SHA,
        "local_unrar_source_commit": UNRAR_COMMIT, "matching_raw_cfg_and_tables": len(originals),
        "ci_projection_matches_local_bytes": True,
        "all_selected_instance_ids_reviewed": sorted(source.INSTANCE_IDS | LV1_IDS),
        "source_authorized_reference_hits": 0, "npc_lexical_collisions": collisions,
        "compiled_vip_boundary": compiled_vip_boundary(original_dir, originals),
        "descendant_code": {"repository": "BismarckDD/Stoneage", "commit": "2f736808ff4361f5429ee919b718c88fabb60346",
                            "action_blob": EVENT_ACTION_BLOB, "token_util_blob": STRING_UTIL_BLOB,
                            "conditional_macro": "_NPC_GET_PETABI",
                            "preset_target_fields": ["CHAR_LV", "CHAR_TRANSMIGRATION", "CHAR_VITAL", "CHAR_STR", "CHAR_TOUGH", "CHAR_DEX"],
                            "attribute_write_multipliers": [20, 80, 80, 100]},
        "petabi_rows": resolved_petabi(originals, remote, data),
        "official_acquisition_closed": 0, "original_payload_published": False, "runtime_executed": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path)
    parser.add_argument("--original-dir", type=Path)
    parser.add_argument("--archive", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data, vip, _, targets = source.input_context()
    remote = verify_raw(args.artifact, targets, data)
    if args.original_dir and args.archive:
        value = reproduce(args.original_dir, args.archive, remote, data, vip)
        if args.output:
            args.output.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    else:
        raw = DEEP_SCAN.read_bytes()
        assert (len(raw), source.digest(raw), source.pet50.source.r40.git_blob(raw)) == (
            46311, DEEP_SCAN_SHA, DEEP_SCAN_BLOB,
        )
        value = json.loads(raw)
    assert value["whole_original_archive_sha256"] == ARCHIVE_SHA
    assert value["source_run_projection_git_blob"] == RAW_SCAN_BLOB
    assert value["local_unrar_source_commit"] == UNRAR_COMMIT
    assert value["ci_projection_matches_local_bytes"] is True and value["matching_raw_cfg_and_tables"] == 2207
    assert value["all_selected_instance_ids_reviewed"] == sorted(source.INSTANCE_IDS | LV1_IDS)
    assert len(value["npc_lexical_collisions"]) == 39
    assert value["compiled_vip_boundary"]["matching_loader_located_in_preserved_exe"] is False
    rows = value["petabi_rows"]
    assert all(r["preset_fields"]["level"] == 1 and r["preset_fields"]["transmigration"] == 0 for r in rows)
    assert len(rows) == 28 and {r["instance_id"] for r in rows} == set(range(2578, 2607)) - {2596}
    assert sum(r["instance_pet_flag"] == r["template_pet_flag"] == 1 for r in rows) == 27
    assert all(not r["present_in_claimed_tw75_catalog_by_id"] and not r["official_delivery_verified"] for r in rows)
    assert all(r["same_saved_spr_index_candidate"] is not None for r in rows)
    assert sum(len(r["tw75_name_and_graphic_only_references"]) for r in rows) == 33
    assert {ref["position"] for r in rows for ref in r["tw75_name_and_graphic_only_references"]
            if ref["in_prior_residual"]} == {144, 208}
    assert value["source_authorized_reference_hits"] == value["official_acquisition_closed"] == 0
    assert value["original_payload_published"] is False and value["runtime_executed"] is False
    print("PET51_ACCEPTANCE_PASS", len(rows), len(value["npc_lexical_collisions"]),
          sum(r["same_saved_spr_index_candidate"] is not None for r in rows))


if __name__ == "__main__":
    main()
