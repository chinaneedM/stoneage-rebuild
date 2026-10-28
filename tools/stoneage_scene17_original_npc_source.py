"""SCENE17 bounded retrieval of two original mixed25 NPC source members.

Source requires genuine HTTP206 ranges, exact RAR file headers and full extracted
member hashes; no copyrighted NPC script, images or dialogue enter stdout/Git.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import pathlib
import subprocess
import tempfile
import zlib

from tools.stoneage_native_album_source_r36 import SparseParts, fetcher_factory, isolated_rar
from tools.stoneage_scene16_nearby_npc import (
    SOURCE_PATH, SOURCE_SIZE, SOURCE_SHA256, TEMPLATE_SIZE, TEMPLATE_SHA256,
    digest, probe,
)
from tools.stoneage_scene14_room_shop import blocks

ROOT = pathlib.Path(__file__).resolve().parents[1]
PREFIX = "石器2.5客戶端+服務端+登入器/SA2.5服務端/gmsv/data/"
TARGETS = {
    SOURCE_PATH: (SOURCE_SIZE, SOURCE_SHA256),
    "npc/genout/npcgen.template": (TEMPLATE_SIZE, TEMPLATE_SHA256),
}
MAX_HTTP_BYTES = 32 * 1024 * 1024
MAX_HTTP_REQUESTS = 512


def need(test, message):
    if not test:
        raise ValueError(message)


def member_subset(reader):
    import rarfile
    located = {}
    seen = 0
    def on_info(info):
        nonlocal seen
        seen += 1
        need(seen <= 10000, "bounded original RAR header visit limit")
        if info.type != rarfile.RAR_BLOCK_FILE:
            return
        pathname = info.filename.replace("\\", "/")
        for rel, expected in TARGETS.items():
            if pathname != PREFIX + rel:
                continue
            need(rel not in located, "duplicate original archive member")
            need(info.file_size == expected[0] and 0 < info.compress_size <= 131072,
                 "unexpected original member size")
            need(info.flags & (1|2|4|16) == 0, "original member split/encrypted/solid")
            located[rel] = {
                "name": pathname, "bytes": info.file_size,
                "header_offset": info.header_offset,
                "data_offset": info.data_offset, "packed_bytes": info.compress_size,
                "flags": info.flags, "crc32": info.CRC,
                "compression_method": info.compress_type,
            }
    rarfile.RarFile(reader, info_callback=on_info, errors="strict")
    need(set(located) == set(TARGETS), "incomplete targeted original member set")
    return located, seen


def extract_both(work, receipt):
    import libarchive
    from libarchive import ffi
    fetch, pages = fetcher_factory()
    reader = SparseParts(fetch, max_bytes=MAX_HTTP_BYTES, max_requests=MAX_HTTP_REQUESTS)
    acquired = {}
    source_details = []
    try:
        located, visited = member_subset(reader)
        for number, rel in enumerate(TARGETS):
            r = located[rel]
            header = reader.at(r["header_offset"], r["data_offset"] - r["header_offset"])
            packed = reader.at(r["data_offset"], r["packed_bytes"])
            isolated = isolated_rar(header, packed, r["flags"])
            pathname = work / ("member-%s.rar" % number)
            pathname.write_bytes(isolated)
            out = work / ("extract-%s" % number)
            out.mkdir()
            p = subprocess.run(["unar", "-f", "-o", str(out), str(pathname)],
                               capture_output=True, timeout=100)
            need(p.returncode == 0, "unar extraction of source member failed")
            files = [f for f in out.rglob("*") if f.is_file()
                     and f.as_posix().endswith(r["name"])]
            need(len(files) == 1, "original member extraction path ambiguous")
            raw = files[0].read_bytes()
            need((len(raw), digest(raw)) == TARGETS[rel],
                 "original member full SHA256 mismatch")
            need((zlib.crc32(raw) & 0xffffffff) == r["crc32"],
                 "original RAR CRC mismatch")
            with libarchive.memory_reader(isolated) as archive:
                other = [(e.pathname.replace("\\", "/"), b"".join(e.get_blocks()))
                         for e in archive]
            need(other == [(r["name"], raw)],
                 "independent libarchive extraction did not match unar")
            source_details.append({
                **r, "sha256": digest(raw),
                "original_header_sha256": digest(header),
                "compressed_payload_sha256": digest(packed),
                "isolated_member_sha256": digest(isolated),
                "unar_result": p.returncode,
                "libarchive_version": ffi.version_number(),
                "dual_decompressor_byte_equal": True,
            })
            acquired[rel] = raw
        return acquired, {
            "headers_visited": visited,
            "range_requests": len(reader.receipts),
            "http206_bytes": reader.fetched,
            "range_receipts": reader.receipts,
            "public_pages": pages,
            "whole_archive_or_part_redownloaded": False,
            "two_original_members": source_details,
        }
    finally:
        receipt.update({
            "source_range_calls": len(reader.receipts),
            "source_http206_bytes": reader.fetched,
            "sparse_source_budget_bytes": MAX_HTTP_BYTES,
            "sparse_source_budget_requests": MAX_HTTP_REQUESTS,
            "source_page_retrievals": len(pages),
            "copyrighted_source_archive_uploaded": False,
            "original_NPC_scripts_uploaded": False,
        })


def run():
    result = {
        "schema": "stoneage.scene17.original_town1000_npc_source_r1",
        "source_scope": "COMMUNITY_MIXED25_ORIGINAL_MEMBER_BYTES_NOT_AUTHENTICATED_OFFICIAL_TW10",
        "source_status": "NOT_ACQUIRED",
        "original_archive_complete_sha256_reverified": False,
        "original_server_executed": False,
        "original_client_world_entered": False,
        "official_tw10_NPC_identity_authenticated": False,
        "original_dialogue_published": False,
        "raw_original_scripts_published": False,
        "original_npc_rendered": False,
        "overall_completion_percent": None,
        "receipt": {},
    }
    with tempfile.TemporaryDirectory(prefix="scene17-original-source-") as work:
        try:
            originals, custody = extract_both(pathlib.Path(work), result["receipt"])
            result["receipt"].update(custody)
            qualified = probe(originals[SOURCE_PATH],
                              originals["npc/genout/npcgen.template"])
            result["source_status"] = qualified["source_status"]
            result["source_qualification"] = qualified
            result["original_member_hashes_verified"] = True
            result["original_bytes_downloaded_for_analysis_only"] = True
            result["template_source_member"] = {
                "bytes": TEMPLATE_SIZE, "sha256": TEMPLATE_SHA256,
                "source_creation_blocks": qualified["authenticated_template_blocks"],
            }
        except Exception as error:
            result["source_status"] = "SOURCE_ACQUISITION_OR_PARSING_FAILED"
            result["error"] = {"type": type(error).__name__,
                               "message": str(error)[:300]}
    return result


def main():
    arg = argparse.ArgumentParser(description=__doc__)
    arg.add_argument("--report", type=pathlib.Path, required=True)
    args = arg.parse_args()
    r = run()
    args.report.write_text(json.dumps(r, ensure_ascii=False, indent=2, sort_keys=True)+"\n")
    print("SCENE17_PUBLIC_SOURCE_RESULT_BEGIN")
    print(args.report.read_text())
    print("SCENE17_PUBLIC_SOURCE_RESULT_END")
    if r["source_status"] == "SOURCE_ACQUISITION_OR_PARSING_FAILED":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
