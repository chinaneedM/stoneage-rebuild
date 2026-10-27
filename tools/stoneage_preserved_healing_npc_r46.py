"""R46: source-bound, non-executing, finite healing NPC creation evidence.

The source is a mixed community preserved RAR, NOT an official TW1.0 build.
Only three bounded creation occurrences may be named. Raw scripts and dialogue
never enter the derived report or Git.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import zlib

ROOT = Path(__file__).resolve().parents[1]
PREFIX = "石器2.5客戶端+服務端+登入器/SA2.5服務端/gmsv/data/"
RELATIVE_PATH = "npc/family/fmhealer.create"
EXPECTED_BYTES = 649
EXPECTED_SHA256 = "1d7d71960958cc60c5e6ba686fede736b5d66ec15f5d58300041a8a2de893847"
SOURCE_SCOPE = "COMMUNITY_MIXED25_PRESERVED_FAMILY_NPC_NOT_OFFICIAL_TW10_OR_SAME_DEPLOYMENT"
ORIGIN = "ORIGIN_UNRESOLVED"
MAX_SELECTED = 3
STRUCTURAL_KEYS = frozenset(("floorid","borncenter","movecenter","createnum","time","dir","graphicname"))
REFERENCE_KEYS = frozenset(("healer","windowhealer","functionset","function","template","npc","enemy","talked","type","heal","arg","script","service"))
CODECS = ("cp950", "big5")

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def require(ok, message):
    if not ok:
        raise ValueError(message)

def fingerprint(raw):
    return {"bytes": len(raw), "sha256": sha(raw)}

def decode_qualified(raw):
    require(len(raw) == EXPECTED_BYTES and sha(raw) == EXPECTED_SHA256,
            "preserved source file length/hash differs from existing R18 manifest")
    cp = raw.decode("cp950", "strict")
    bi = raw.decode("big5", "strict")
    require(cp == bi, "CP950 and Big5 interpret original names differently")
    return cp

def parse_create_text(text):
    """Syntax-aware, fail-closed projection of NPCCREATE blocks."""
    blocks = []
    opened = None
    seen_header = False
    line_no = 0
    for line_no, line in enumerate(text.splitlines(), 1):
        value = line.strip()
        if not value or value.startswith("#") or value.startswith("//"):
            continue
        if not seen_header:
            require(value == "NPCCREATE", "unqualified original create header")
            seen_header = True
            continue
        if value == "{":
            require(opened is None, "nested create block")
            opened = {"open_line": line_no, "fields": [], "seen": set()}
            continue
        if value == "}":
            require(opened is not None, "unmatched create closing brace")
            require(len(opened["fields"]) > 0, "empty create block")
            blocks.append({"open_line": opened["open_line"],
                           "close_line": line_no, "fields": opened["fields"]})
            opened = None
            continue
        require(opened is not None, "unexpected data outside NPC block")
        match = re.fullmatch(r"([A-Za-z_][A-Za-z_0-9 ]{0,39})\s*[:=]\s*(.*)", value)
        require(match is not None, "unclassified original NPC assignment")
        key, cell = match.groups()
        key = key.strip().lower()
        require(key not in opened["seen"], "duplicate key within original NPC occurrence")
        opened["seen"].add(key)
        row = {"line": line_no, "key": key,
               "value_utf8_sha256": sha(cell.encode("utf-8")),
               "value_chars": len(cell)}
        if re.fullmatch(r"-?\d+(\s*,\s*-?\d+)*", cell) is not None:
            integers = [int(a.strip()) for a in cell.split(",")]
            row["integer_values"] = integers
        elif key == "name":
            require(0 < len(cell) <= 80 and "\x00" not in cell, "name extent")
            row["original_name"] = cell
            row["original_name_cp950_sha256"] = sha(cell.encode("cp950"))
        elif key in REFERENCE_KEYS and re.fullmatch(r"[A-Za-z_][A-Za-z_0-9./:|+-]{0,119}", cell):
            row["declared_reference_token"] = cell
        opened["fields"].append(row)
    require(seen_header and opened is None and 0 < len(blocks) <= 128, "unterminated or absent original create blocks")
    return blocks, line_no

def derive_from_verified_bytes(raw):
    text = decode_qualified(raw)
    blocks, physical_lines = parse_create_text(text)
    chosen = blocks[:MAX_SELECTED]
    occurrences = []
    for ix, block in enumerate(chosen):
        bykey = {row["key"]: row for row in block["fields"]}
        selected = {}
        for key in ("name", "floorid", "borncenter", "graphicname", "dir", "functionset", "function",
                    "healer", "windowhealer", "npc", "enemy", "template", "service"):
            if key in bykey:
                selected[key] = bykey[key]
        occurrences.append({"source_block_order": ix,
                            "open_line": block["open_line"], "close_line": block["close_line"],
                            "all_field_keys_as_written_lowercased": list(bykey),
                            "bounded_selected_fields": selected,
                            "block_field_fingerprints": block["fields"],
                            "original_service_executed": False})
    return {
        "raw_original_file": fingerprint(raw),
        "qualified_decoders": list(CODECS),
        "cp950_big5_exact_unicode_agreement": True,
        "physical_line_count": physical_lines,
        "original_creation_block_count": len(blocks),
        "selected_rule": "FIRST_UP_TO_THREE_SOURCE_ORDER_NOT_ALL_NPCS",
        "selected_creation_count": len(occurrences),
        "selected_creation_occurrences": occurrences,
        "npc_function_bound_to_healer_runtime_proven": False,
        "original_spawn_position_executed": False,
        "same_build_with_taiwan_1_0_proven": False,
        "four_hometown_healer_identity_proven": False,
        "original_healing_prices_or_game_rules_proven": False,
        "original_dialogue_or_script_body_published": False,
        "verified_base_game_quests_added": 0
    }

def acquire_one(work, receipt):
    import rarfile
    import libarchive
    from libarchive import ffi
    from tools.stoneage_native_album_source_r36 import SparseParts, fetcher_factory, isolated_rar
    fetch, pages = fetcher_factory()
    reader = SparseParts(fetch)
    filename = PREFIX + RELATIVE_PATH
    found = None
    visited = 0

    def visit(info):
        nonlocal found, visited
        visited += 1
        require(visited <= 10000, "bounded RAR header traversal")
        if info.type != rarfile.RAR_BLOCK_FILE:
            return
        if info.filename.replace("\\", "/") != filename:
            return
        require(found is None, "duplicate source path occurrence")
        require(info.file_size == EXPECTED_BYTES and 0 < info.compress_size <= 65536,
                "unexpected original member extent")
        require(info.flags & (1|2|4|16) == 0, "original split/encrypted/solid member")
        found = {
            "path": filename, "bytes": info.file_size, "packed_bytes": info.compress_size,
            "header_offset": info.header_offset, "data_offset": info.data_offset,
            "flags": info.flags, "crc32": info.CRC, "compression_method": info.compress_type
        }

    try:
        rarfile.RarFile(reader, info_callback=visit, errors="strict")
        require(found is not None, "original file not found within bounded archive traversal")
        header = reader.at(found["header_offset"], found["data_offset"] - found["header_offset"])
        packed = reader.at(found["data_offset"], found["packed_bytes"])
        isolated = isolated_rar(header, packed, found["flags"])
        rar_path = work / "one-member.rar"
        rar_path.write_bytes(isolated)
        out = work / "unpacked"
        process = subprocess.run(["unar", "-f", "-o", str(out), str(rar_path)],
                                 capture_output=True, timeout=90)
        require(process.returncode == 0, "static unar original extraction failure")
        files = [f for f in out.rglob("*") if f.is_file() and f.as_posix().endswith(filename)]
        require(len(files) == 1, "ambiguous extracted original source member")
        original = files[0].read_bytes()
        require(len(original) == EXPECTED_BYTES and sha(original) == EXPECTED_SHA256,
                "original R18 sha256/length conflict")
        require(zlib.crc32(original) & 0xffffffff == found["crc32"], "original RAR CRC conflict")
        with libarchive.memory_reader(isolated) as archive:
            independently = [(entry.pathname.replace("\\", "/"), b"".join(entry.get_blocks()))
                             for entry in archive]
        require(len(independently) == 1 and independently[0] == (filename, original),
                "libarchive independent decode mismatch")
        receipt["original_member"] = {
            **found, "sha256": sha(original), "original_header_sha256": sha(header),
            "compressed_payload_sha256": sha(packed), "unar_exit_status": process.returncode,
            "libarchive_version": ffi.version_number(),
            "two_independent_decompressors_agree": True
        }
        return original
    finally:
        receipt.update(headers_visited=visited, range_requests=len(reader.receipts),
                       actual_range_bytes=reader.fetched, range_receipts=reader.receipts,
                       public_pages=pages, archive_part_or_whole_redownloaded=False,
                       two_decoders_share_same_http_source_not_independent_archives=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = {
        "schema": "stoneage.preserved_healing_npc_material_source.r46",
        "source_scope": SOURCE_SCOPE,
        "status": "NOT_ACQUIRED",
        "origin_class": ORIGIN,
        "official_tw10_npc_authenticated": 0,
        "original_server_executed": False,
        "raw_original_npc_script_published": False,
        "receipt": {}
    }
    try:
        with tempfile.TemporaryDirectory(prefix="r46-one-original-") as directory:
            original = acquire_one(Path(directory), report["receipt"])
            report["status"] = "ONE_ORIGINAL_MEMBER_HASH_AND_DUAL_DECODING_VERIFIED_DERIVATION_PENDING"
            report["material"] = derive_from_verified_bytes(original)
            report["status"] = "ONE_ORIGINAL_MEMBER_AND_UP_TO_THREE_NPC_CREATIONS_QUALIFIED"
    except Exception as exc:
        report["error"] = {"type": type(exc).__name__, "message": str(exc)[:300]}
    args.output.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2)+"\n")
    print("R46_REPORT_BEGIN")
    print(args.output.read_text(), end="")
    print("R46_REPORT_END")

if __name__ == "__main__":
    main()
