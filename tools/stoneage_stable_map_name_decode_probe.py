#!/usr/bin/env python3
"""Decode provenance-safe recovered server-map names for stable map candidates.

Promotion rule:
- server floor ID and dimensions must match the stable map candidate;
- raw name must decode strictly under both Big5 and CP950;
- the two decoders must produce exactly the same Unicode text;
- all dimension-matched server copies for a floor must converge to one text.

Conflicts are preserved as candidates and never silently selected.
All decoded names remain recovered25/LATER_RECOVERED semantics, not Taiwan-v1
historical membership.
"""

from __future__ import annotations

import argparse
import hashlib
import unicodedata
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_client_server_map_probe import collect_server_maps
from tools.stoneage_world_map_library import parse_stable_later_map_manifest


RESOLVED = "RESOLVED_BIG5_CP950_CONSENSUS"
TEXT_CONFLICT = "SERVER_COPY_TEXT_CONFLICT"
ENCODING_DISAGREEMENT = "BIG5_CP950_DISAGREEMENT"
EMPTY = "EMPTY_SERVER_NAME"


def _safe_text(value: str) -> str:
    return (
        str(value)
        .replace("\\", "\\\\")
        .replace("|", "\\|")
        .replace("\n", "\\n")
        .replace("\r", "\\r")
    )


def _decode_consensus(raw: bytes) -> tuple[str | None, str]:
    try:
        big5 = raw.decode("big5", "strict")
        cp950 = raw.decode("cp950", "strict")
    except UnicodeDecodeError:
        return None, ENCODING_DISAGREEMENT
    if big5 != cp950:
        return None, ENCODING_DISAGREEMENT
    if any(unicodedata.category(ch).startswith("C") for ch in big5):
        return None, ENCODING_DISAGREEMENT
    if not big5:
        return "", EMPTY
    return big5, RESOLVED


@dataclass(frozen=True)
class MapNameTextRow:
    floor_id: int
    raw_name_hashes: tuple[str, ...]
    candidate_texts: tuple[str, ...]
    status: str

    @property
    def resolved_text(self) -> str | None:
        if self.status == RESOLVED and len(self.candidate_texts) == 1:
            return self.candidate_texts[0]
        return None


def analyze(
    *,
    lineage_report: Path,
    server_map_root: Path,
) -> tuple[tuple[MapNameTextRow, ...], Counter]:
    manifest = parse_stable_later_map_manifest(
        lineage_report.read_text(encoding="utf-8")
    )
    server_by_id, _total, _ls2, _invalid = collect_server_maps(
        server_map_root,
        sample_limit=0,
    )
    rows = []
    counts = Counter()
    distinct_resolved_texts = set()

    for candidate in manifest.candidates:
        entries = [
            entry for entry in server_by_id.get(candidate.floor_id, [])
            if (
                int(entry["width"]) == candidate.width
                and int(entry["height"]) == candidate.height
            )
        ]
        if not entries:
            continue

        raw_names = sorted({bytes(entry["name"]) for entry in entries})
        hashes = tuple(
            hashlib.sha256(raw).hexdigest() for raw in raw_names
        )
        decoded = []
        statuses = set()
        for raw in raw_names:
            text, status = _decode_consensus(raw)
            statuses.add(status)
            if text is not None:
                decoded.append(text)

        texts = tuple(sorted(set(decoded)))
        if ENCODING_DISAGREEMENT in statuses:
            status = ENCODING_DISAGREEMENT
        elif texts == ("",):
            status = EMPTY
        elif len(texts) == 1:
            status = RESOLVED
            distinct_resolved_texts.add(texts[0])
        else:
            status = TEXT_CONFLICT

        row = MapNameTextRow(
            floor_id=candidate.floor_id,
            raw_name_hashes=hashes,
            candidate_texts=texts,
            status=status,
        )
        rows.append(row)
        counts[f"status:{status}"] += 1
        if len(raw_names) > 1:
            counts["floors_with_multiple_raw_name_variants"] += 1
        if len(raw_names) > 1 and len(texts) == 1:
            counts["raw_variant_conflict_collapsed_to_same_text"] += 1

    counts["stable_floor_candidates"] = len(manifest.candidates)
    counts["stable_with_dimension_matched_server_name"] = len(rows)
    counts["stable_without_dimension_matched_server_name"] = (
        len(manifest.candidates) - len(rows)
    )
    counts["distinct_resolved_name_texts"] = len(distinct_resolved_texts)
    return tuple(rows), counts


def emit(rows: tuple[MapNameTextRow, ...], counts: Counter) -> None:
    print("StoneAge stable-world decoded server-map names — R1")
    print(
        "SCOPE|short-map-header-place-names|"
        "big5+cp950-consensus|no-map-payload"
    )
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "PROMOTION_RULE|stable-floor-id+dimensions"
        "+strict-big5-cp950-identical-text"
        "+server-copy-text-consensus"
    )
    for key in sorted(counts):
        print(f"COUNT|{key}|{counts[key]}")
    for row in rows:
        if row.status == RESOLVED:
            print(
                "MAP_NAME|"
                f"floor={row.floor_id}|"
                f"name={_safe_text(row.resolved_text or '')}|"
                f"raw_variants={len(row.raw_name_hashes)}|"
                f"raw_sha256={','.join(row.raw_name_hashes)}|"
                f"status={row.status}"
            )
        else:
            print(
                "MAP_NAME_UNRESOLVED|"
                f"floor={row.floor_id}|"
                f"candidate_count={len(row.candidate_texts)}|"
                f"candidates={';'.join(_safe_text(x) for x in row.candidate_texts)}|"
                f"raw_variants={len(row.raw_name_hashes)}|"
                f"raw_sha256={','.join(row.raw_name_hashes)}|"
                f"status={row.status}"
            )
    print("RESOLUTION|STABLE_SERVER_MAP_NAMES_DECODED")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lineage-report", type=Path, required=True)
    parser.add_argument("--server-map-root", type=Path, required=True)
    args = parser.parse_args()
    rows, counts = analyze(
        lineage_report=args.lineage_report,
        server_map_root=args.server_map_root,
    )
    emit(rows, counts)


if __name__ == "__main__":
    main()
