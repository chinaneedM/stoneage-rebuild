#!/usr/bin/env python3
"""Bounded optical-filesystem probe for Internet Archive item Stoneage-5.

This deliberately reuses the already-tested raw-sector/ISO9660 primitives from
the sa-arena negative-control probe.  It never downloads the full disc image:
only metadata, the tiny CUE, ISO9660 metadata sectors, small text files and
bounded EXE prefixes are read.
"""
from __future__ import annotations

import urllib.parse

from tools.stoneage_sa_arena_ia_probe import (
    clean,
    emit_tree,
    get_json,
    optical_candidates,
    parse_cue,
    small_get,
)

IDENTIFIER = "Stoneage-5"
META = f"https://archive.org/metadata/{IDENTIFIER}"
DOWNLOAD = f"https://archive.org/download/{IDENTIFIER}/"


def item_download_url(name):
    return DOWNLOAD + urllib.parse.quote(str(name), safe="/")


def main():
    print("StoneAge Stoneage-5 Internet Archive optical-carrier probe — R1")
    print(
        "SCOPE|IA-metadata+CUE+bounded-raw-sector-filesystem+small-text+"
        "EXE-prefix-reads|no-full-disc-download|no-payload-commit"
    )
    errors = []
    try:
        meta = get_json(META)
    except Exception as exc:
        print(f"FATAL|metadata|kind={type(exc).__name__}|message={clean(exc)}")
        return

    md = meta.get("metadata", {}) if isinstance(meta, dict) else {}
    print(
        "ITEM|identifier=" + clean(md.get("identifier") or IDENTIFIER)
        + "|title=" + clean(md.get("title"))
        + "|date=" + clean(md.get("date") or md.get("year"))
        + "|creator=" + clean(md.get("creator"))
        + "|uploader=" + clean(md.get("uploader"))
        + "|mediatype=" + clean(md.get("mediatype"))
        + "|collection=" + clean(md.get("collection"))
        + "|description=" + clean(md.get("description"), 3000)
    )

    candidates = optical_candidates(meta.get("files", []))
    print(f"COUNT|optical_candidates|{len(candidates)}")
    by_name = {}
    for i, row in enumerate(candidates, 1):
        name = str(row.get("name") or "")
        by_name[name.lower()] = row
        print(
            f"OPTICAL|index={i}|name={clean(name,2200)}|size={clean(row.get('size'))}|"
            f"md5={clean(row.get('md5'))}|sha1={clean(row.get('sha1'))}|"
            f"crc32={clean(row.get('crc32'))}|source={clean(row.get('source'))}|"
            f"format={clean(row.get('format'))}"
        )

    parsed = 0
    cue_rows = [
        r for r in candidates
        if str(r.get("name") or "").lower().endswith(".cue")
    ]
    for ci, cue_row in enumerate(cue_rows, 1):
        cue_name = str(cue_row.get("name") or "")
        try:
            status, cue_bytes = small_get(item_download_url(cue_name))
            cue_text = cue_bytes.decode("utf-8", "replace")
            tracks = parse_cue(cue_text)
            print(
                f"CUE|index={ci}|name={clean(cue_name)}|status={status}|"
                f"bytes={len(cue_bytes)}|tracks={len(tracks)}"
            )
            for track in tracks:
                print(
                    f"TRACK|cue={ci}|number={track['number']}|mode={clean(track['mode'])}|"
                    f"file={clean(track['file'])}|index_frames={track['index_frames']}"
                )
            for track in tracks:
                if not track["mode"].startswith("MODE"):
                    continue
                row = by_name.get(str(track["file"]).lower())
                if row is None:
                    print(
                        f"TRACK_SKIP|cue={ci}|number={track['number']}|"
                        "reason=referenced-bin-not-in-IA-metadata"
                    )
                    continue
                try:
                    if emit_tree(
                        ci,
                        item_download_url(row.get("name")),
                        track,
                        errors,
                    ):
                        parsed += 1
                        break
                except ValueError as exc:
                    print(
                        f"TRACK_SKIP|cue={ci}|number={track['number']}|"
                        f"reason={clean(exc)}"
                    )
                except Exception as exc:
                    errors.append(
                        (f"track:{track['number']}", type(exc).__name__, str(exc))
                    )
        except Exception as exc:
            errors.append((f"cue:{cue_name}", type(exc).__name__, str(exc)))

    iso_rows = [
        r for r in candidates
        if str(r.get("name") or "").lower().endswith(".iso")
    ]
    for i, row in enumerate(iso_rows, 1):
        try:
            track = {"number": 1, "mode": "MODE1/2048", "index_frames": 0}
            if emit_tree(
                1000 + i,
                item_download_url(row.get("name")),
                track,
                errors,
            ):
                parsed += 1
        except Exception as exc:
            errors.append((f"iso:{row.get('name')}", type(exc).__name__, str(exc)))

    for scope, kind, msg in errors:
        print(
            f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}"
        )
    print(f"COUNT|cue_candidates|{len(cue_rows)}")
    print(f"COUNT|iso_candidates|{len(iso_rows)}")
    print(f"COUNT|filesystem_tracks_parsed|{parsed}")
    print(f"COUNT|errors|{len(errors)}")
    if parsed:
        print(
            "RESOLUTION|OPTICAL_FILESYSTEM_METADATA_RECOVERED|"
            "classify carrier/version from volume, directory, text and executable traits"
        )
    elif candidates:
        print(
            "RESOLUTION|OPTICAL_METADATA_ONLY|"
            "bounded sector surface did not yield a supported ISO9660 filesystem"
        )
    else:
        print(
            "RESOLUTION|NO_OPTICAL_IMAGE_IN_ITEM_METADATA|"
            "item is not a usable optical-image lead"
        )
    print(
        "EVIDENCE_BOUNDARY|IA title/date/creator are uploader metadata unless "
        "independently sourced; preserved BIN/CUE hashes and filesystem structures "
        "describe the archived object but do not alone prove original pressing/"
        "mastering, historical release date, or clean-client version."
    )


if __name__ == "__main__":
    main()
