"""Read preserved PC NPC data for source-qualified pet references and VIP field shapes."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import tempfile
import zlib

from tools import stoneage_pet_high_first_50_accept as pet50
from tools.stoneage_native_album_source_r36 import SparseParts, fetcher_factory, isolated_rar
from tools.stoneage_preserved_item_shop_r44 import PREFIX

ROSTER = pet50.source.R / "STONEAGE-CHARACTER-NPC-MODULE-09-ORIGINAL-NPCENEMY-ROSTER-BRIDGE-R1.json"
ROSTER_BLOB = "3d827b98d00c3caa6e779f34a36d28bd70945b75"
INSTANCE_IDS = {1642, 2187, 2429, 2430, 2431, 2432, 2455, 2456}
DIRECTED_GROUPS = {1167, 1168, 1169, 1170, 1171, 1173, 1194, 1195, 1196, 1297, 1298}
TEMPLATE_IDS = {131, 132, 145, 146, 809}
VIP_NPC = pet50.source.NPCS[:4]
INSTANCE_FIELDS = {b"enemyno", b"enemypetno", b"getpet", b"addpet", b"vippet"}
GROUP_FIELDS = {b"group", b"groupid", b"groupno", b"enemygroup", b"enemygroupid", b"battlegrp"}
TEMPLATE_FIELDS = {b"enemy", b"enemytemp", b"enemytempno", b"petid", b"petno", b"tempno"}
FIELDS = INSTANCE_FIELDS | GROUP_FIELDS | TEMPLATE_FIELDS
FIELD = re.compile(rb"(?:^|[|{])[ \t]*([A-Za-z_][A-Za-z_0-9]{0,35})[ \t]*[:=][ \t]*([^|}\r\n]*)")
NUMBER = re.compile(rb"(?<![0-9])-?[0-9]+(?![0-9])")
NUMERIC_LIST = re.compile(rb"[+-]?[0-9]+(?:[ \t]*,[ \t]*[+-]?[0-9]+)*")
VIP_FIELD = re.compile(rb"^[ \t]*VipPet[ \t]*[:=][ \t]*(.*)$")


def digest(raw):
    return sha256(raw).hexdigest()


def input_context():
    report, _, data = pet50.accept(None)
    vip = pet50.accept_vip(report, None)
    raw = ROSTER.read_bytes()
    assert pet50.source.r40.git_blob(raw) == ROSTER_BLOB
    roster = json.loads(raw)
    targets = []
    for row in report["projection"]["records"]:
        selected = row["source_pairs"][0]["group_variants"][0]["group_memberships"]
        if selected:
            targets.append({
                "position": row["tw75_row_index"], "name": row["name"],
                "template": row["template_id"], "master_row_sha256": row["row_sha256"],
                "same_id_exact_template": row["source_pairs"][0]["match"] == "EXACT_ROW",
                "groups": sorted({m["group_id"] for m in selected}),
                "instances": sorted({m["enemy_id"] for m in selected}),
            })
    assert {i for x in targets for i in x["groups"]} == DIRECTED_GROUPS
    assert {i for x in targets for i in x["instances"]} == INSTANCE_IDS
    assert {x["template"] for x in targets} == TEMPLATE_IDS
    return data, vip, roster, targets


def expected_members(data):
    r18 = {r["path"]: r for r in data["r18"]["all_server_occurrences"]}
    npc = {f[0]: f for f in data["char01"]["source_files"]}
    assert len(npc) == 2205
    assert {"npc/" + path for path in npc} == {path for path in r18 if path.startswith("npc/")}
    result = {}
    for relative, (_, size, sha, crc, _) in npc.items():
        path = "npc/" + relative
        assert (size, sha) == (r18[path]["size"], r18[path]["sha256"])
        result[path] = (size, sha, int(crc, 16))
    for path in ("enemy.txt", "enemybase.txt"):
        p = data["pet10"]["verified_original_archive_members"][path]
        assert (p["bytes"], p["sha256"]) == (r18[path]["size"], r18[path]["sha256"])
        result[path] = (p["bytes"], p["sha256"], int(p["archive_record_crc32"], 16))
    assert sum(v[0] for k, v in result.items() if k.startswith("npc/")) == 1930332
    return result


def unpack_all(expected):
    import libarchive
    import rarfile

    fetch, pages = fetcher_factory()
    reader = SparseParts(fetch)
    prefix = PREFIX + "data/"
    selected = {}
    headers = 0

    def index(info):
        nonlocal headers
        headers += 1
        assert headers <= 10000
        if info.type != rarfile.RAR_BLOCK_FILE or info.is_dir():
            return
        name = info.filename.replace("\\", "/")
        if name.startswith(prefix):
            rel = name.removeprefix(prefix)
            if rel.startswith("npc/"):
                assert rel in expected, rel
            if rel in expected:
                assert rel not in selected and info.flags & 23 == 0, rel
                assert (info.file_size, info.CRC) == (expected[rel][0], expected[rel][2]), rel
                assert 0 <= info.compress_size <= 1024 * 1024
                selected[rel] = info

    with rarfile.RarFile(reader, info_callback=index, errors="strict"):
        pass
    assert selected.keys() == expected.keys(), sorted(expected.keys() ^ selected.keys())[:10]
    originals = {}
    ledger = {}
    fallback = []
    with tempfile.TemporaryDirectory(prefix="pet51-") as temporary:
        tmp = Path(temporary)
        for n, (name, info) in enumerate(sorted(selected.items())):
            header = reader.at(info.header_offset, info.data_offset - info.header_offset)
            packed = reader.at(info.data_offset, info.compress_size)
            wrapped = isolated_rar(header, packed, info.flags)
            try:
                with libarchive.memory_reader(wrapped) as archive:
                    entries = [(e.pathname.replace("\\", "/"), b"".join(e.get_blocks())) for e in archive]
                assert len(entries) == 1 and entries[0][0] == prefix + name
                raw = entries[0][1]
                assert (len(raw), digest(raw), zlib.crc32(raw)) == expected[name]
            except (libarchive.ArchiveError, AssertionError):
                assert len(fallback) < 100, "bounded secondary extraction"
                fallback.append(name)
                src, dst = tmp / f"{n}.rar", tmp / str(n)
                src.write_bytes(wrapped)
                subprocess.run(["unar", "-f", "-o", str(dst), str(src)], check=True, capture_output=True, timeout=30)
                paths = [p for p in dst.rglob("*") if p.is_file()]
                assert len(paths) == 1 and paths[0].as_posix().endswith(prefix + name)
                raw = paths[0].read_bytes()
            assert (len(raw), digest(raw), zlib.crc32(raw)) == expected[name], name
            originals[name] = raw
            ledger[name] = [len(raw), digest(raw), f"{zlib.crc32(raw):08x}",
                            info.header_offset, digest(header), digest(packed)]
    return originals, {
        "headers_visited": headers, "range_receipts": reader.receipts,
        "public_pages": pages, "range_bytes": reader.fetched,
        "unique_member_count": len(originals), "member_bytes": sum(map(len, originals.values())),
        "member_ledger_sha256": digest(json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()),
        "unar_fallback_paths": fallback, "whole_archive_rehashed": False,
    }


def scan_npc(originals, creation_ids):
    hits = []
    field_counts = Counter()
    other_instances = set()
    other_groups = set()
    other_templates = set()
    for path, raw in originals.items():
        if not path.startswith("npc/"):
            continue
        for line_no, line in enumerate(raw.splitlines(), 1):
            if line.lstrip().startswith((b"#", b"//")):
                continue
            candidates = {int(i) for i in NUMBER.findall(line)}
            if candidates & INSTANCE_IDS:
                other_instances.add(path)
            if candidates & DIRECTED_GROUPS:
                other_groups.add(path)
            if candidates & TEMPLATE_IDS:
                other_templates.add(path)
            for field in FIELD.finditer(line):
                key, value = field[1].lower(), field[2].strip()
                if key not in FIELDS:
                    continue
                field_counts[key.decode()] += 1
                if key == b"vippet":
                    value = value.split(b",", 1)[0].strip()
                if not NUMERIC_LIST.fullmatch(value):
                    continue
                ids = {int(x) for x in value.split(b",")}
                targets = INSTANCE_IDS if key in INSTANCE_FIELDS else (
                    DIRECTED_GROUPS if key in GROUP_FIELDS else TEMPLATE_IDS
                )
                if ids & targets:
                    hits.append({
                        "path": path, "line": line_no, "field": field[1].decode(),
                        "matched_ids": sorted(ids & targets), "line_sha256": digest(line.strip()),
                        "file_sha256": digest(raw), "create_ref_count": creation_ids[path.removeprefix("npc/")],
                        "backup_path": Path(path).suffix.lower() in {".bak", ".old"},
                    })
    return {
        "field_counts": dict(field_counts), "literal_hits": hits,
        "lexical_path_counts": {"instances": len(other_instances), "groups": len(other_groups),
                                "templates": len(other_templates)},
    }


def vip_token_shape(token):
    # Output only non-content shapes and hashes. Keep numeric namespace separate
    # from string equality and never publish the original labels or opaque tokens.
    if token.isdigit():
        return {"shape": "ASCII_DECIMAL", "numeric_candidate": int(token)}
    if re.fullmatch(rb"MM[1-4]", token):
        return {"shape": "CONDITIONAL_MM_ALIAS", "numeric_candidate": None}
    if not token:
        return {"shape": "EMPTY", "numeric_candidate": None}
    # Compare full-width digits explicitly. Do not turn arbitrary compatibility
    # characters, local names or numeric suffixes into a live enemy instance.
    for codec in ("cp950", "cp936", "utf-8"):
        try:
            decoded = token.decode(codec)
        except UnicodeDecodeError:
            continue
        if decoded and all("０" <= c <= "９" for c in decoded):
            return {"shape": "FULLWIDTH_DECIMAL", "numeric_candidate": int(decoded), "codec_candidate": codec}
    prefix = re.match(rb"[+-]?[0-9]+", token)
    if prefix:
        return {"shape": "C_ATOI_PREFIX_CANDIDATE", "numeric_candidate": int(prefix[0])}
    return {"shape": "TEXT_OR_SYMBOLIC" if not token.isascii() else "ASCII_SYMBOLIC",
            "numeric_candidate": None}


def scan_vip(originals, vip, data):
    before = [r for f in vip["menu_files"] for r in f["rows"]]
    rows = []
    bases = pet50.source.r40.rows(originals["enemybase.txt"], 56, 6)
    instances = pet50.source.r40.rows(originals["enemy.txt"], 34, 3)
    master = {row["template_id"]: (i, row["row_sha256"])
              for i, row in enumerate(data["master"]["pet_flag_1_field_projections"])}
    residual = set(data["prev"]["remaining_gap_row_indices"])
    template_hash = {r[1]: r[16] for r in data["pet10"]["source_rows"]["enemybase.txt"]}
    assert len(bases) == len(template_hash) == 988 and len(instances) == 2087
    template_name = {int(a[6]): a[0] for _, a in bases}
    instance_by_id = {int(a[3]): (int(a[4]), a[0]) for _, a in instances}
    assert len(template_name) == 988 and len(instance_by_id) == 2087
    for f in vip["menu_files"]:
        raw = originals["npc/" + f["path"]]
        for row in f["rows"]:
            line = raw.splitlines()[row["physical_line"] - 1]
            assert (m := VIP_FIELD.fullmatch(line)), (f["path"], row["physical_line"])
            assert digest(m[1].strip()) == row["value_sha256"]
            field = re.split(rb"[|:]", m[1].strip(), maxsplit=1)[0].strip()
            token = field.split(b",", 1)[0].strip()
            shape = vip_token_shape(token)
            exact_name_templates = [tid for tid, name in template_name.items() if token and name == token]
            exact_name_instances = [eid for eid, (_, name) in instance_by_id.items() if token and name == token]
            num = shape["numeric_candidate"]
            tpl = instance_by_id[num][0] if num in instance_by_id else None
            exact = master[tpl][0] if tpl in master and master[tpl][1] == template_hash.get(tpl) else None
            rows.append({
                "path": f["path"], "line": row["physical_line"], "value_sha256": row["value_sha256"],
                "token_bytes": len(token), "token_sha256": digest(token),
                "raw_vip_points": row["raw_vip_points"], "previously_unparsed": row["unparsed_value"],
                "create_ref_count": f["create_reference_count"],
                **shape, "numeric_candidate_selected_template": tpl,
                "exact_shared_master_position": exact,
                "among_67_residual_positions": exact in residual,
                "raw_name_matches_template_ids": exact_name_templates,
                "raw_name_matches_instance_ids": exact_name_instances,
            })
    assert len(rows) == len(before) == 42
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data, vip, roster, targets = input_context()
    originals, custody = unpack_all(expected_members(data))
    creation_ids = Counter(ref[0] for row in data["char01"]["create_rows"] for ref in row[-1])
    previous = sorted({n for arg in roster["argument_files"] for n in arg[3] + arg[4]} & INSTANCE_IDS)
    npc = scan_npc(originals, creation_ids)
    menu = scan_vip(originals, vip, data)
    result = {
        "schema": "stoneage.pet51.original_npc_vip_reference_census.r1",
        "source_scope": "MIXED25_PRESERVATION_STATIC_SOURCE",
        "source_pc_official_deployment_verified": False, "runtime_executed": False,
        "original_payload_published": False, "official_acquisition_closed": 0,
        "source_pins": {"r18": pet50.source.PINS["r18"][1], "char01": pet50.source.PINS["char01"][1],
                        "char09": ROSTER_BLOB, "pet50": pet50.REPORT_BLOB, "pet50_vip": pet50.VIP_REPORT_BLOB},
        "custody": custody, "target_rows": targets, "previous_char09_args": len(roster["argument_files"]),
        "previous_char09_instance_hits": previous, "npc": npc, "vip": menu,
    }
    raw = (json.dumps(result, sort_keys=True, ensure_ascii=False, indent=2) + "\n").encode()
    args.output.write_bytes(raw)
    print("PET51_CUSTODY", custody["unique_member_count"], custody["range_bytes"],
          len(custody["range_receipts"]), custody["member_ledger_sha256"], len(custody["unar_fallback_paths"]))
    print("PET51_NPC", json.dumps(npc, ensure_ascii=False, separators=(",", ":")))
    print("PET51_VIP", json.dumps(Counter((r["shape"] for r in menu)), sort_keys=True),
          len({r["token_sha256"] for r in menu if r["previously_unparsed"]}),
          sum(r["among_67_residual_positions"] for r in menu))
    print("PET51_REPORT", len(raw), digest(raw), pet50.source.r40.git_blob(raw))


if __name__ == "__main__":
    main()
