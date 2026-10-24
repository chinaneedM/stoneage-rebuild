#!/usr/bin/env python3
"""Read actual Stoneage-5 DATA1.CAB ranges, verify/decompress, archive hashes only."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import tempfile
from tools.stoneage_sa_arena_ia_probe import SECTOR, logical_sector_read, mode_layout
from tools.stoneage_stoneage5_msi_probe import load_root, find_entry
from tools.stoneage_stoneage5_cab_probe import (
    iso_file_slice, parse_cab_header, parse_cab_files, parse_cab_folders)

EXPECTED_SIZE = 612584670
EXPECTED_FILES = 413
EXPECTED_FOLDERS = 26
CHUNK_SECTORS = 2048


def safe_name(name):
    name = name.replace("\\", "/")
    parts = name.split("/")
    if (not name or name.startswith("/") or "\x00" in name or
        any(ord(ch) < 32 for ch in name) or
        any(x in ("", ".", "..") for x in parts) or ":" in parts[0]):
        raise ValueError("unsafe-cab-member")
    return "/".join(parts)


def verify_range(content_range, start, end, total):
    if content_range != f"bytes {start}-{end}/{total}":
        raise ValueError("incorrect-content-range")


def checked_layout(prefix):
    h = parse_cab_header(prefix)
    folders = list(parse_cab_folders(prefix, h))
    files, end = parse_cab_files(prefix, h)
    if (h["cb_cabinet"] != EXPECTED_SIZE or h["flags"] != 0 or
        h["c_files"] != EXPECTED_FILES or h["c_folders"] != EXPECTED_FOLDERS or
        len(files) != EXPECTED_FILES or len(folders) != EXPECTED_FOLDERS or
        any(x["compress_base"] != 3 for x in folders)):
        raise ValueError("changed-cab-layout")
    seen = set()
    for f in files:
        n = safe_name(f["name"]).casefold()
        if n in seen or int(f["i_folder"]) >= len(folders) or int(f["size"]) > 4*1024**3:
            raise ValueError("ambiguous-or-invalid-member")
        seen.add(n)
    if sum(int(f["size"]) for f in files) > 5*1024**3:
        raise ValueError("decompression-limit")
    return h, files


def download_cab(url, cab, track, carrier_size, destination):
    stride, _, _ = mode_layout(track["mode"])
    nsectors = math.ceil(int(cab["size"])/SECTOR)
    digest = hashlib.sha256()
    with destination.open("xb") as dst:
        for offset in range(0, nsectors, CHUNK_SECTORS):
            count = min(CHUNK_SECTORS, nsectors-offset)
            lba = int(cab["extent"])+offset
            first = (int(track["index_frames"])+lba)*stride
            last = first+count*stride-1
            if last >= carrier_size:
                raise ValueError("carrier-length-exceeded")
            status, header, block, honored = logical_sector_read(
                url, lba, count, track["index_frames"], track["mode"])
            if not honored or status != 206:
                raise ValueError("archive-ignored-range")
            verify_range(header, first, last, carrier_size)
            take = min(len(block), int(cab["size"])-offset*SECTOR)
            if take != min(count*SECTOR,int(cab["size"])-offset*SECTOR):
                raise ValueError("short-logical-sector")
            dst.write(block[:take])
            digest.update(block[:take])
            if offset % (CHUNK_SECTORS * 20) == 0:
                print(f"REAL_DOWNLOAD|{offset*SECTOR+take}/{cab['size']}",flush=True)
    if destination.stat().st_size != int(cab["size"]):
        raise ValueError("cab-size-mismatch")
    return digest.hexdigest()


def hash_file(path):
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as f:
        while part := f.read(1024*1024):
            size += len(part)
            if size > 4*1024**3:
                raise ValueError("decompressed-file-too-large")
            h.update(part)
    return h.hexdigest(), size


def extracted_inventory(directory, files):
    expected = {safe_name(f["name"]).casefold(): f for f in files}
    seen = {}
    for item in directory.rglob("*"):
        if item.is_symlink():
            raise ValueError("extracted-symlink")
        if not item.is_file():
            continue
        name = safe_name(item.relative_to(directory).as_posix())
        key = name.casefold()
        if key in seen or key not in expected:
            raise ValueError("unexpected-or-duplicate-file")
        digest, size = hash_file(item)
        src = expected[key]
        if size != int(src["size"]):
            raise ValueError("decompressed-size-mismatch")
        seen[key] = {"index":int(src["index"]),"name":src["name"],"size":size,
                     "sha256":digest,"cab_folder":int(src["i_folder"])}
    if seen.keys() != expected.keys():
        raise ValueError("missing-extracted-files")
    return sorted(seen.values(),key=lambda x:x["index"])


def known_hashes(repo, sample):
    known={}
    if sample=="TW10":
        for line in (repo/"research/recovered/STONEAGE-TW10-CLIENT-INVENTORY-R1.txt").read_text(encoding="utf8").splitlines():
            if not line.startswith("CORE_FILE|"):
                continue
            d=dict(x.split("=",1) for x in line.split("|")[1:] if "=" in x)
            known.setdefault((int(d["size"]),d["sha256"]),[]).append(d["path"])
    elif sample=="TW85":
        d=json.loads((repo/"research/recovered/STONEAGE-WAYI85-MSI-CLIENT-PAYLOAD-R1.json").read_text(encoding="utf8"))
        sample_list=d["inspection"]["inventory"]["samples"]
        if len(sample_list)!=1 or sample_list[0]["file_count"]!=557:
            raise ValueError("bad-tw85-source")
        for row in sample_list[0]["files"]:
            known.setdefault((int(row["size"]),row["sha256"]),[]).append(row["path"])
    return known


def exact_matches(rows,known):
    return [{"index":r["index"],"name":r["name"],"sha256":r["sha256"],
             "size":r["size"],"other_paths":sorted(known[(r["size"],r["sha256"])])}
            for r in rows if (r["size"],r["sha256"]) in known]


def acquire(output):
    meta,cue_name,cue_bytes,track,bin_row,url,volume,entries=load_root()
    cab=find_entry(entries,"DATA1.CAB")
    if cab is None or int(cab["size"])!=EXPECTED_SIZE:
        raise ValueError("known-cab-not-present")
    prefix,status,cr=iso_file_slice(url,cab,track,0,65536)
    if status!=206 or len(prefix)!=65536:
        raise ValueError("cab-prefix-unavailable")
    header,files=checked_layout(prefix)
    repo=Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix="stoneage5-real-cab-") as tmp:
        cabinet=Path(tmp)/"DATA1.CAB"
        sha=download_cab(url,cab,track,int(bin_row["size"]),cabinet)
        with cabinet.open("rb") as fh:
            if fh.read(len(prefix))!=prefix:
                raise ValueError("full-cab-prefix-source-mismatch")
        target=Path(tmp)/"expanded"
        target.mkdir()
        run=subprocess.run(["cabextract","-q","-d",str(target),str(cabinet)],
                           capture_output=True,text=True,timeout=1200)
        if run.returncode:
            raise RuntimeError(f"cabextract-error-{run.returncode}:{run.stderr[-200:]}")
        rows=extracted_inventory(target,files)
        matches={name:exact_matches(rows,known_hashes(repo,name))
                 for name in ("TW10","TW85")}
        file_stream="".join(f'{r["index"]}|{r["name"]}|{r["size"]}|{r["sha256"]}\n' for r in rows)
        report={
          "schema":"stoneage.stoneage5.real_cab_payload_r1",
          "status":"REAL_FULL_CAB_EXTRACTED_AND_413_FILES_HASHED",
          "source":{"archive_identifier":"Stoneage-5",
              "provenance":"THIRD_PARTY_ARCHIVE_NOT_PROVEN_OFFICIAL_CLEAN_RELEASE",
              "carrier_bin":bin_row["name"],"carrier_catalogue_size":int(bin_row["size"]),
              "carrier_catalogue_sha1":bin_row.get("sha1"),
              "cue_name":cue_name,"cue_sha256":hashlib.sha256(cue_bytes).hexdigest(),
              "cab_iso_extent":int(cab["extent"]),"cab_size":int(cab["size"]),
              "cab_sha256":sha,"cab_set_id":header["set_id"],
              "cab_folders":EXPECTED_FOLDERS,"cab_files":EXPECTED_FILES,
              "volume_id":volume["volume_id"]},
          "files":{"count":len(rows),"total_bytes":sum(x["size"] for x in rows),
                   "manifest_sha256":hashlib.sha256(file_stream.encode()).hexdigest(),
                   "inventory":rows},
          "cross_version_exact_byte_matches":matches,
          "boundaries":{"official_clean_proven":False,"historical_server_master_recovered":False,
                        "pet_quest_entity_identity_proven":False,
                        "original_binary_committed":False,"original_bytes_durably_stored":False,
                        "carrier_sha1_rehashed":False}
        }
        output.parent.mkdir(parents=True,exist_ok=True)
        output.write_text(json.dumps(report,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
        print(f"RESULT|{report['status']}|cab_sha256={sha}|files={len(rows)}|"
              f"tw10={len(matches['TW10'])}|tw85={len(matches['TW85'])}",flush=True)
        return report


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    acquire(a.output)


if __name__=="__main__":
    main()
