#!/usr/bin/env python3
"""Audit recovered server-map header names for stable map candidates.

R1 deliberately emits no raw name bytes and no decoded names. It establishes:
- which provenance-safe stable floors have dimension-matched server maps;
- whether duplicate server-map copies agree on the raw name field;
- anonymous raw-name identities (SHA-256);
- strict decodability under candidate historical encodings.

Decoded place names are a later layer only after encoding provenance is clear.
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


ENCODINGS = ("ascii", "utf-8", "cp950", "big5", "gbk", "gb18030", "shift_jis")


def _clean_decode(raw: bytes, encoding: str) -> str | None:
    try:
        text = raw.decode(encoding, "strict")
    except UnicodeDecodeError:
        return None
    if any(
        unicodedata.category(ch).startswith("C")
        and ch not in "\t\n\r"
        for ch in text
    ):
        return None
    return text


@dataclass(frozen=True)
class StableMapNameAuditRow:
    floor_id: int
    server_variant_count: int
    dimension_matched_variant_count: int
    raw_name_hashes: tuple[str, ...]
    raw_name_lengths: tuple[int, ...]
    decodable_encodings: tuple[str, ...]

    @property
    def has_dimension_matched_server_map(self) -> bool:
        return self.dimension_matched_variant_count > 0

    @property
    def name_variant_count(self) -> int:
        return len(self.raw_name_hashes)

    @property
    def raw_name_consistent(self) -> bool:
        return self.name_variant_count <= 1

    @property
    def empty_name(self) -> bool:
        return bool(
            self.has_dimension_matched_server_map
            and self.raw_name_lengths == (0,)
        )


def analyze(
    *,
    lineage_report: Path,
    server_map_root: Path,
) -> tuple[tuple[StableMapNameAuditRow, ...], Counter]:
    manifest = parse_stable_later_map_manifest(
        lineage_report.read_text(encoding="utf-8")
    )
    server_by_id, _total, _ls2, _invalid = collect_server_maps(
        server_map_root,
        sample_limit=0,
    )
    rows = []
    counts = Counter()

    for candidate in manifest.candidates:
        entries = server_by_id.get(candidate.floor_id, [])
        matched = [
            entry for entry in entries
            if (
                int(entry["width"]) == candidate.width
                and int(entry["height"]) == candidate.height
            )
        ]
        raw_names = [bytes(entry["name"]) for entry in matched]
        hashes = tuple(sorted({
            hashlib.sha256(raw).hexdigest()
            for raw in raw_names
        }))
        lengths = tuple(sorted({len(raw) for raw in raw_names}))
        decodable = tuple(
            encoding
            for encoding in ENCODINGS
            if (
                raw_names
                and all(
                    _clean_decode(raw, encoding) is not None
                    for raw in raw_names
                )
            )
        )
        row = StableMapNameAuditRow(
            floor_id=candidate.floor_id,
            server_variant_count=len(entries),
            dimension_matched_variant_count=len(matched),
            raw_name_hashes=hashes,
            raw_name_lengths=lengths,
            decodable_encodings=decodable,
        )
        rows.append(row)

        counts["stable_floor_candidates"] += 1
        if entries:
            counts["stable_with_server_id"] += 1
        if matched:
            counts["stable_with_dimension_matched_server_map"] += 1
        if row.empty_name:
            counts["stable_with_empty_server_name"] += 1
        if matched and row.raw_name_consistent:
            counts["stable_with_consistent_server_name"] += 1
        if row.name_variant_count > 1:
            counts["stable_with_server_name_conflict"] += 1
        if len(matched) > 1:
            counts["stable_with_duplicate_dimension_matched_server_copies"] += 1
        for encoding in decodable:
            counts[f"all_matched_names_decodable:{encoding}"] += 1

    counts["distinct_nonempty_server_name_hashes"] = len({
        name_hash
        for row in rows
        if not row.empty_name
        for name_hash in row.raw_name_hashes
    })
    return tuple(rows), counts


def emit(rows: tuple[StableMapNameAuditRow, ...], counts: Counter) -> None:
    print("StoneAge stable-world server-map name encoding audit — R1")
    print(
        "SCOPE|anonymous-server-header-name-metadata|"
        "no-raw-name-bytes|no-decoded-place-names|no-map-payload"
    )
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|server header names are admitted only from entries whose "
        "floor ID and dimensions match the provenance-safe stable candidate"
    )
    for key in sorted(counts):
        print(f"COUNT|{key}|{counts[key]}")
    for row in rows:
        if not row.has_dimension_matched_server_map:
            continue
        print(
            "MAP_NAME_AUDIT|"
            f"floor={row.floor_id}|"
            f"server_variants={row.server_variant_count}|"
            f"dimension_matched={row.dimension_matched_variant_count}|"
            f"name_variants={row.name_variant_count}|"
            f"name_sha256={','.join(row.raw_name_hashes)}|"
            f"name_lengths={','.join(map(str,row.raw_name_lengths))}|"
            f"decodable={','.join(row.decodable_encodings)}"
        )
    print("RESOLUTION|STABLE_SERVER_MAP_NAME_ENCODING_AUDITED")


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
