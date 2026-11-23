"""Static UPX decompression and bounded pet-album source-table discovery for TW85.

Never execute the original game. Source binaries stay runner-private. Inference
from compressed bytes or mere graphic-value coincidence is never official pet ID.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path
import struct
import subprocess

from tools.stoneage_pet_high_first_tw85_native import (
    CN50, EXTRA, MANIFEST, TW1, name_literal_matches, parse_pe, sha, byte_matches
)

ROOT = Path(__file__).resolve().parents[1]
TARGET_FILES = ("StoneAge2.exe", "sa.exe", "sb.exe", "sc.exe", "sd.exe")


def candidate_row(raw: bytes, at: int):
    if at < 0 or at + 28 > len(raw):
        return None
    original_i = struct.unpack_from("<i", raw, at)[0]
    portrait = struct.unpack_from("<I", raw, at + 24)[0]
    if not -1 <= original_i <= 200000 or not 25000 <= portrait <= 100000:
        return None
    field = raw[at + 4:at + 24]
    encoded_name = field.split(b"\0", 1)[0]
    if not 4 <= len(encoded_name) <= 19:
        return None
    if b"\0" in field and any(field[len(encoded_name) + 1:]):
        return None
    try:
        name = encoded_name.decode("cp950")
    except UnicodeDecodeError:
        return None
    if len(name) < 2 or not any("\u4e00" <= c <= "\u9fff" for c in name):
        return None
    return {"file_offset": at, "first_i32": original_i,
            "name_cp950": name, "trailing_u32": portrait,
            "raw_record_sha256": sha(raw[at:at + 28])}


def detect_28byte_album(raw: bytes, hits: list, max_tables=6):
    """Candidate table seed must be a known TW1 literal at +4 of a 28-byte row."""
    seeds = set()
    for hit in hits:
        if hit["encoding"] != "cp950":
            continue
        seeds.update(x - 4 for x in hit["file_offsets"])
    tables = []
    seen = set()
    for seed in sorted(seeds):
        if candidate_row(raw, seed) is None:
            continue
        start = seed
        while start - 28 >= 0 and candidate_row(raw, start - 28) is not None:
            start -= 28
            if seed - start > 28 * 2000:
                break
        if start in seen:
            continue
        seen.add(start)
        records = []
        ptr = start
        while len(records) < 2000:
            row = candidate_row(raw, ptr)
            if row is None:
                break
            records.append(row)
            ptr += 28
        if len(records) < 8:
            continue
        if len({r["name_cp950"] for r in records}) < 8:
            continue
        tables.append({
            "candidate_first_file_offset": start,
            "candidate_records": len(records),
            "candidate_last_file_offset": ptr - 28,
            "first_records": records[:5],
            "last_records": records[-5:],
            "all_candidate_names": [{"ordinal_in_candidate": i, **r} for i, r in enumerate(records)],
            "status": "28_BYTE_PATTERN_CANDIDATE_NOT_NATIVE_SELECTOR_PROOF",
        })
        if len(tables) >= max_tables:
            break
    return tables


def selftest():
    name = "烏力".encode("cp950")
    row = struct.pack("<i", 17) + name + b"\0" * (20 - len(name)) + struct.pack("<I", 28001)
    assert candidate_row(row, 0)["name_cp950"] == "烏力"
    assert not candidate_row(b"x" * 28, 0)
    assert not candidate_row(row[:27], 0)
    eight = b"".join(struct.pack("<i", i) +
                     (("烏力" + chr(0x4e00 + i)).encode("cp950", errors="ignore") or name)[:20].ljust(20, b"\0") +
                     struct.pack("<I", 28001 + i) for i in range(8))
    assert len(eight) == 8 * 28
    print("PET07_UPX_SELFTEST_PASS", flush=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source-root", type=Path)
    p.add_argument("--output", type=Path)
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--log-json", action="store_true")
    a = p.parse_args()
    if a.self_test:
        selftest()
        return
    if not a.source_root or not a.output:
        p.error("--source-root and --output required")
    inv = json.loads(MANIFEST.read_text(encoding="utf-8"))
    expected = {Path(x["path"]).name: x for x in inv["inspection"]["inventory"]["samples"][0]["files"]
                if x["path"].lower().endswith(".exe")}
    tw_names = sorted({r["name_as_written"] for r in json.loads(TW1.read_text(encoding="utf-8"))["records"]
                       if len(r["name_as_written"]) >= 2})
    cn_names = sorted({r["label_as_compiled_GB18030"] for r in json.loads(CN50.read_text(encoding="utf-8"))["records"]
                       if r["label_as_compiled_GB18030"] and len(r["label_as_compiled_GB18030"]) >= 2})
    no_set = {r["tw85_original_spr_number"] for r in json.loads(EXTRA.read_text(encoding="utf-8"))["records"]}
    assert len(no_set) == 550
    out = {
        "schema": "stoneage.pet.high_first_07_tw85_upx_unpacked_source_triage.r1",
        "source_carrier": "UNVERIFIED_COMMUNITY_PRESERVED_CLAIMED_WAYI85_INSTALLER",
        "input_executable_sha_verified_before_unpacking": True,
        "original_game_executable_never_run": True,
        "decompression_is_static_tool_only": True,
        "native_pet_selector_or_official_release_verified": False,
        "files": [],
    }
    for fname in TARGET_FILES:
        orig = expected[fname]
        packed = a.source_root / orig["path"]
        raw = packed.read_bytes()
        assert len(raw) == orig["size"] and sha(raw) == orig["sha256"], "source exe checksum drift " + fname
        dest = a.output.parent / ("unpacked-" + fname)
        cmd = subprocess.run(["upx", "-d", "-q", "-o", str(dest), str(packed)],
                             text=True, capture_output=True, timeout=120)
        res = {"name": fname, "packed_sha256": orig["sha256"], "packed_bytes": len(raw),
               "decompression_returncode": cmd.returncode}
        if cmd.returncode != 0 or not dest.exists():
            res["static_unpack_status"] = "UPX_FAILED_OR_NOT_SUPPORTED"
            res["reason"] = (cmd.stderr or cmd.stdout)[-400:]
            out["files"].append(res)
            continue
        plain = dest.read_bytes()
        if len(plain) <= len(raw) or len(plain) > 40 * 1024 * 1024:
            raise ValueError("UPX output bounds violation " + fname)
        res.update({"static_unpack_status": "UPX_DECOMPRESSED",
                    "unpacked_bytes": len(plain), "unpacked_sha256": sha(plain),
                    "pe": parse_pe(plain)})
        # Names are tested in the correct source-era encodings. This does not
        # establish a pet table without contiguous original fields.
        tw = name_literal_matches(plain, tw_names, ("cp950", "utf-16le"))
        cn = name_literal_matches(plain, cn_names, ("gb18030", "cp950", "utf-16le"))
        literals = []
        for n in sorted(no_set):
            hits = byte_matches(plain, struct.pack("<I", n), limit=12)
            if hits:
                literals.append({"number": n, "offsets": hits})
        tables = detect_28byte_album(plain, tw)
        res.update({
            "literal_tw10_name_hits": tw,
            "literal_cn50_name_hits": cn,
            "literal_extra_spr_numbers": literals,
            "candidate_28byte_album_tables": tables,
            "name_hit_count_not_pet_species": len(tw),
            "graphic_number_occurrence_not_selector": True,
        })
        out["files"].append(res)
    out["summary"] = {
        "attempted_verified_packed_programs": len(TARGET_FILES),
        "successfully_unpacked_original_programs": sum(x["static_unpack_status"] == "UPX_DECOMPRESSED" for x in out["files"]),
        "tw10_dictionary_names_mentioned": len({x["name"] for f in out["files"]
                                                 for x in f.get("literal_tw10_name_hits", [])}),
        "extra_graphic_literals_mentioned": len({x["number"] for f in out["files"]
                                                 for x in f.get("literal_extra_spr_numbers", [])}),
        "candidate_28byte_tables": sum(len(f.get("candidate_28byte_album_tables", [])) for f in out["files"]),
        "official_new_pet_identities_proven": 0,
    }
    raw = (json.dumps(out, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    a.output.write_bytes(raw)
    print("PET07_UPX_SUMMARY=" + json.dumps(out["summary"], sort_keys=True), flush=True)
    print("PET07_UPX_REPORT_SHA256=" + hashlib.sha256(raw).hexdigest(), flush=True)
    if a.log_json:
        b64 = base64.b64encode(raw).decode("ascii")
        print("PET07_UPX_REPORT_BEGIN")
        for start in range(0, len(b64), 2600):
            print("PET07_UPX_B64 " + b64[start:start+2600])
        print("PET07_UPX_REPORT_END")


if __name__ == "__main__":
    main()
