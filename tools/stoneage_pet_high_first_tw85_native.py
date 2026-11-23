"""Bounded static inspection of source-verified TW85 preserved PC executable bytes.

All game binaries stay in a private temporary runner directory. The output is
source-qualified, short derived evidence; numeric matches are NOT pet identities.
"""
from __future__ import annotations

import argparse
import base64
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "research/recovered/STONEAGE-WAYI85-MSI-CLIENT-PAYLOAD-R1.json"
EXTRA = ROOT / "research/pets/PET-HIGH-FIRST-TW85-EXTRA-SPR-GROUPS-R1.json"
TW1 = ROOT / "research/recovered/STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json"
CN50 = ROOT / "research/recovered/STONEAGE-PET126R-CN50-PC-ORIGINAL-ALBUM-FULL-362-SLOT-SOURCE-CATALOGUE-R1.json"
SCHEMA = "stoneage.pet.high_first_07_tw85_original_pe_static_inspection.r1"
EXPECTED_PROGRAMS = ("Startup.exe", "StoneAge2.exe", "sa.exe", "sb.exe", "sc.exe", "sd.exe")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def entropy(raw: bytes) -> float:
    if not raw:
        return 0.0
    c = Counter(raw)
    return round(-sum((x / len(raw)) * math.log2(x / len(raw)) for x in c.values()), 3)


def parse_pe(raw: bytes) -> dict:
    """Report PE structure only; never execute, unpack, or infer game behavior."""
    if len(raw) < 128 or raw[:2] != b"MZ":
        return {"status": "NOT_MZ"}
    pe = struct.unpack_from("<I", raw, 0x3c)[0]
    if pe + 24 > len(raw) or raw[pe:pe + 4] != b"PE\0\0":
        return {"status": "MZ_WITHOUT_VALID_PE"}
    machine, nsec, timestamp, _, _, optlen, flags = struct.unpack_from("<HHIIIHH", raw, pe + 4)
    if not 0 < nsec < 64 or pe + 24 + optlen + 40 * nsec > len(raw):
        return {"status": "PE_SECTION_BOUNDS_INVALID"}
    optoff = pe + 24
    magic = struct.unpack_from("<H", raw, optoff)[0]
    sections = []
    for i in range(nsec):
        p = optoff + optlen + 40 * i
        name = raw[p:p + 8].rstrip(b"\0").decode("ascii", "backslashreplace")
        vsize, vaddr, rawsize, rawptr = struct.unpack_from("<IIII", raw, p + 8)
        if rawptr > len(raw) or rawsize > len(raw) - rawptr:
            raise ValueError(f"PE section {name} outside verified source bytes")
        sections.append({"name": name, "virtual_size": vsize, "virtual_address": vaddr,
                         "raw_size": rawsize, "file_offset": rawptr,
                         "entropy": entropy(raw[rawptr:rawptr + rawsize])})
    return {"status": "PE_PARSED_NOT_EXECUTED", "machine": machine,
            "sections": sections, "timestamp_raw": timestamp,
            "characteristics": flags, "optional_magic": magic}


def byte_matches(raw: bytes, needle: bytes, limit: int = 40) -> list[int]:
    out = []
    if not needle:
        return out
    i = raw.find(needle)
    while i >= 0:
        out.append(i)
        if len(out) >= limit:
            break
        i = raw.find(needle, i + 1)
    return out


def name_literal_matches(raw: bytes, names: list[str], encodings: tuple[str, ...]):
    matches = []
    for name in names:
        for encoding in encodings:
            try:
                b = name.encode(encoding)
            except UnicodeEncodeError:
                continue
            if len(b) < 4:
                continue
            offsets = byte_matches(raw, b, limit=3)
            if offsets:
                matches.append({"name": name, "encoding": encoding, "file_offsets": offsets})
    return matches


def self_test():
    assert entropy(b"\0" * 20) == 0.0
    assert byte_matches(b"xyz123xyz123", b"xyz") == [0, 6]
    assert byte_matches(b"\0\0\0\0", b"xyz") == []
    assert parse_pe(b"what")["status"] == "NOT_MZ"
    assert parse_pe(b"MZ" + b"\0" * 200)["status"] == "MZ_WITHOUT_VALID_PE"
    assert name_literal_matches("烏力".encode("cp950"), ["烏力"], ("cp950",))
    assert byte_matches(struct.pack("<I", 101501) + b"\0\0", struct.pack("<I", 101501)) == [0]
    print("PET07_SELFTEST_PASS")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--log-json", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if not args.source_root or not args.output:
        parser.error("--source-root and --output required")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    items = manifest["inspection"]["inventory"]["samples"][0]["files"]
    per_file = {v["path"]: v for v in items if v["path"].lower().endswith(".exe")}
    if len(per_file) != len(EXPECTED_PROGRAMS):
        raise ValueError("TW85 inventory EXE count changed")
    extra = json.loads(EXTRA.read_text(encoding="utf-8"))
    numbers = {r["tw85_original_spr_number"] for r in extra["records"]}
    assert len(numbers) == 550 and min(numbers) == 101501 and max(numbers) == 102050
    tw = json.loads(TW1.read_text(encoding="utf-8"))
    cn = json.loads(CN50.read_text(encoding="utf-8"))
    tw_names = sorted({r["name_as_written"] for r in tw["records"] if len(r["name_as_written"]) >= 2})
    cn_names = sorted({r["label_as_compiled_GB18030"] for r in cn["records"]
                       if r["label_as_compiled_GB18030"] is not None
                       and len(r["label_as_compiled_GB18030"]) >= 2})
    result = {
        "schema": SCHEMA,
        "source": {
            "source_class": "UNVERIFIED_COMMUNITY_PRESERVED_CLAIMED_WAYI85_INSTALLER",
            "msi_sha256": manifest["inspection"]["msi_sha256"],
            "container_sha256": manifest["assembled_installer"]["sha256"],
            "program_bytes_read_and_sha256_verified": True,
            "original_client_executed": False,
            "private_original_program_bytes_published": False,
        },
        "comparison": {
            "tw85_only_sprite_number_range": [101501, 102050],
            "candidate_sprite_numbers_in_pinned_atlas": len(numbers),
            "tw10_early_client_name_dictionary_count": len(tw_names),
            "cn50_later_client_name_dictionary_count": len(cn_names),
            "same_build_tw85_name_table_proven": False,
            "same_build_tw85_pet_sprite_selector_proven": False,
            "same_build_pet_id_verified": False,
            "official_in_game_release_proven": False,
        },
        "files": [],
    }
    observed = set()
    for path, meta in sorted(per_file.items()):
        filename = Path(path).name
        assert filename in EXPECTED_PROGRAMS
        p = args.source_root / path
        if not p.is_file():
            raise FileNotFoundError("MSI extracted program unavailable: " + path)
        raw = p.read_bytes()
        if len(raw) != meta["size"] or sha(raw) != meta["sha256"]:
            raise ValueError("Source-verified MSI executable bytes changed: " + path)
        pe = parse_pe(raw)
        numeric = []
        for no in sorted(numbers):
            offsets = byte_matches(raw, struct.pack("<I", no), limit=20)
            if offsets:
                numeric.append({"sprite_number": no, "file_offsets": offsets})
        tw_hits = name_literal_matches(raw, tw_names, ("cp950", "utf-16le"))
        cn_hits = name_literal_matches(raw, cn_names, ("gb18030", "cp950", "utf-16le"))
        result["files"].append({
            "path": path, "sha256": meta["sha256"], "bytes": len(raw),
            "pe": pe,
            "literal_tw85_extra_sprite_numbers": numeric,
            "tw10_name_dictionary_literal_hits": tw_hits,
            "cn50_name_dictionary_literal_hits": cn_hits,
            "literal_search_is_not_same_build_pet_selector": True,
        })
        observed.add(filename)
    assert observed == set(EXPECTED_PROGRAMS)
    result["summary"] = {
        "verified_original_executables": len(result["files"]),
        "parsed_pe_files": sum(f["pe"]["status"] == "PE_PARSED_NOT_EXECUTED" for f in result["files"]),
        "files_with_extra_sprite_number_literals": sum(bool(f["literal_tw85_extra_sprite_numbers"]) for f in result["files"]),
        "distinct_extra_sprite_number_literals": len({v["sprite_number"] for f in result["files"]
                                                      for v in f["literal_tw85_extra_sprite_numbers"]}),
        "files_with_early_tw_name_literals": sum(bool(f["tw10_name_dictionary_literal_hits"]) for f in result["files"]),
        "files_with_cn50_name_literals": sum(bool(f["cn50_name_dictionary_literal_hits"]) for f in result["files"]),
        "same_build_qualified_pet_identity_new": 0,
        "official_pet_species_new": 0,
    }
    rawout = (json.dumps(result, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(rawout)
    print("PET07_SUMMARY=" + json.dumps(result["summary"], ensure_ascii=False, sort_keys=True), flush=True)
    print("PET07_REPORT_SHA256=" + sha(rawout), flush=True)
    if args.log_json:
        b64 = base64.b64encode(rawout).decode("ascii")
        print("PET07_REPORT_BEGIN")
        for i in range(0, len(b64), 2800):
            print("PET07_B64 " + b64[i:i + 2800])
        print("PET07_REPORT_END")


if __name__ == "__main__":
    main()
