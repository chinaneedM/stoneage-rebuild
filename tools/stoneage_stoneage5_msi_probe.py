#!/usr/bin/env python3
"""Recover the small STA5.MSI installer database from the preserved Stoneage-5 BIN.

Only the exact sectors covering the MSI and a few tiny installer configuration
files are read.  The full optical image and large DATA1.CAB are never
downloaded.  The MSI is written transiently for msitools inspection by CI.
"""
from __future__ import annotations

import argparse
import hashlib
import math

from tools.stoneage_sa_arena_ia_probe import (
    SECTOR,
    clean,
    decode_text,
    get_json,
    logical_sector_read,
    optical_candidates,
    parse_cue,
    parse_directory,
    parse_pvd,
    small_get,
)
from tools.stoneage_stoneage5_optical_probe import IDENTIFIER, META, item_download_url

MAX_MSI_BYTES = 2 * 1024 * 1024
TEXT_NAMES = {"0X0804.INI", "SETUP.INI"}


def find_entry(entries, name):
    want = name.upper()
    for row in entries:
        if str(row.get("name") or "").upper() == want:
            return row
    return None


def read_entry(bin_url, entry, track):
    size = int(entry["size"])
    count = math.ceil(size / SECTOR)
    status, content_range, data, honored = logical_sector_read(
        bin_url,
        int(entry["extent"]),
        count,
        int(track["index_frames"]),
        str(track["mode"]),
    )
    if not honored:
        raise RuntimeError(
            f"range-not-honored status={status} content_range={content_range}"
        )
    return data[:size], status, content_range


def load_root():
    meta = get_json(META)
    candidates = optical_candidates(meta.get("files", []))
    by_name = {str(r.get("name") or "").lower(): r for r in candidates}
    cue_rows = [
        r for r in candidates
        if str(r.get("name") or "").lower().endswith(".cue")
    ]
    if not cue_rows:
        raise RuntimeError("no-cue")
    cue_name = str(cue_rows[0].get("name") or "")
    status, cue_bytes = small_get(item_download_url(cue_name))
    tracks = parse_cue(cue_bytes.decode("utf-8", "replace"))
    track = next((t for t in tracks if t["mode"].startswith("MODE")), None)
    if track is None:
        raise RuntimeError("no-mode-track")
    bin_row = by_name.get(str(track["file"]).lower())
    if bin_row is None:
        raise RuntimeError("cue-bin-missing")
    bin_url = item_download_url(bin_row.get("name"))
    status2, cr2, pvd, honored = logical_sector_read(
        bin_url, 16, 1, track["index_frames"], track["mode"]
    )
    if not honored:
        raise RuntimeError(f"pvd-range-not-honored:{status2}:{cr2}")
    info = parse_pvd(pvd)
    root_count = math.ceil(int(info["root_size"]) / SECTOR)
    status3, cr3, root, honored3 = logical_sector_read(
        bin_url,
        int(info["root_extent"]),
        root_count,
        track["index_frames"],
        track["mode"],
    )
    if not honored3:
        raise RuntimeError(f"root-range-not-honored:{status3}:{cr3}")
    return meta, cue_name, cue_bytes, track, bin_row, bin_url, info, parse_directory(root)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-msi", required=True)
    args = ap.parse_args()

    print("StoneAge Stoneage-5 MSI inventory bridge — R1")
    print(
        "SCOPE|metadata+CUE+ISO9660-root+tiny-configs+STA5.MSI-only|"
        "no-full-disc-download|no-DATA1.CAB-download|no-proprietary-payload-commit"
    )
    meta, cue_name, cue_bytes, track, bin_row, bin_url, info, entries = load_root()
    md = meta.get("metadata", {})
    print(
        f"ITEM|identifier={clean(md.get('identifier') or IDENTIFIER)}|"
        f"title={clean(md.get('title'))}|date={clean(md.get('date') or md.get('year'))}|"
        f"creator={clean(md.get('creator'))}|uploader={clean(md.get('uploader'))}"
    )
    print(
        f"CARRIER|cue={clean(cue_name)}|cue_bytes={len(cue_bytes)}|"
        f"track_mode={clean(track['mode'])}|track_start_frames={track['index_frames']}|"
        f"bin={clean(bin_row.get('name'))}|bin_size={clean(bin_row.get('size'))}|"
        f"bin_md5={clean(bin_row.get('md5'))}|bin_sha1={clean(bin_row.get('sha1'))}|"
        f"volume_id={clean(info['volume_id'])}"
    )

    for name in sorted(TEXT_NAMES):
        entry = find_entry(entries, name)
        if entry is None:
            print(f"CONFIG_MISSING|name={name}")
            continue
        data, status, cr = read_entry(bin_url, entry, track)
        enc, text = decode_text(data)
        print(
            f"CONFIG|name={name}|size={entry['size']}|status={status}|"
            f"sha256={hashlib.sha256(data).hexdigest()}|encoding={clean(enc)}|"
            f"content_range={clean(cr)}"
        )
        for n, line in enumerate(text.replace("\x00", "").splitlines(), 1):
            line = " ".join(line.split())
            if line:
                print(f"CONFIG_LINE|name={name}|n={n}|value={clean(line,1200)}")

    data1 = find_entry(entries, "DATA1.CAB")
    if data1:
        print(
            f"CAB_OBJECT|name=DATA1.CAB|size={data1['size']}|extent={data1['extent']}|"
            "read=0|reason=large-payload-bounded-by-MSI-first-strategy"
        )

    msi = find_entry(entries, "STA5.MSI")
    if msi is None:
        raise RuntimeError("STA5.MSI-not-found")
    if int(msi["size"]) > MAX_MSI_BYTES:
        raise RuntimeError(f"MSI-too-large:{msi['size']}")
    body, status, cr = read_entry(bin_url, msi, track)
    with open(args.output_msi, "wb") as fh:
        fh.write(body)
    print(
        f"MSI_OBJECT|name=STA5.MSI|size={len(body)}|extent={msi['extent']}|"
        f"status={status}|sha256={hashlib.sha256(body).hexdigest()}|"
        f"content_range={clean(cr)}|transient_path={clean(args.output_msi)}"
    )
    print(
        "EVIDENCE_BOUNDARY|the recovered MSI bytes and installer tables describe the "
        "preserved optical object; IA catalogue date/creator remain uploader metadata "
        "unless independently corroborated, and installer metadata alone does not "
        "prove mastering/pressing identity."
    )


if __name__ == "__main__":
    main()
