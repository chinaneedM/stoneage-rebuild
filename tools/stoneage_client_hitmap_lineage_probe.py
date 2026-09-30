#!/usr/bin/env python3
"""Pinned multi-lineage audit for the StoneAge client hit-map algorithm.

This probe fetches only public source files at immutable Git commit SHAs. It
extracts a small semantic feature vector from the active readHitMap/checkHitMap
implementation and the ADRNBIN/MAP_ATTR header. It stores no source bodies.

Evidence policy:
- matching public descendant source is strong lineage evidence;
- explicit _SA_VERSION_25 markers strengthen version-family relevance;
- it is NOT byte-level proof for the recovered25 sa_2903 executable.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import urllib.parse
import urllib.request
from dataclasses import dataclass


OUTPUT_RESOLUTION = (
    "RESOLUTION|STONEAGE_CLIENT_HITMAP_DESCENDANT_STABLE_PROFILE_AUDITED"
)


@dataclass(frozen=True)
class SourceSpec:
    label: str
    repository: str
    commit: str
    map_path: str
    header_path: str

    def raw_url(self, path: str) -> str:
        quoted = "/".join(urllib.parse.quote(part, safe="") for part in path.split("/"))
        return (
            f"https://raw.githubusercontent.com/{self.repository}/"
            f"{self.commit}/{quoted}"
        )


SOURCES = (
    SourceSpec(
        label="bismarck",
        repository="BismarckDD/Stoneage",
        commit="2f736808ff4361f5429ee919b718c88fabb60346",
        map_path="client/stoneage/system/map.cpp",
        header_path="client/stoneage/systeminc/loadrealbin.h",
    ),
    SourceSpec(
        label="signally",
        repository="Signally190/sking-sacli",
        commit="40cb67ef090ebc0cffd57ca947871bdfd0b18331",
        map_path="system/map.cpp",
        header_path="systeminc/loadrealbin.h",
    ),
    SourceSpec(
        label="anson",
        repository="anson1788/stoneage",
        commit="1997fc20456dbda36d181b9680ae10bed2e9cdf9",
        map_path="石器时代8.5客户端最新源代码/石器源码/system/map.cpp",
        header_path="石器时代8.5客户端最新源代码/石器源码/systeminc/loadrealbin.h",
    ),
)


ALGORITHM_FEATURES = (
    "active_read_hitmap",
    "tile_adrn_gt99",
    "tile_adrn_60_79",
    "tile_zero_map_see_rule",
    "small_block_codes",
    "small_override_code4",
    "hit0_preserves_override",
    "hit2_override",
    "parts_adrn_gt99",
    "parts_footprint",
    "parts_15680_15732",
    "parts_60_79",
    "event_npc_final_block",
    "check_bounds_block",
    "check_hitmap_value1_blocks",
)

HEADER_FEATURES = (
    "map_attr_atari_xy",
    "map_attr_hit",
    "map_attr_height",
    "map_attr_bmpnumber",
    "adrnbin_embeds_map_attr",
)


def _fetch(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "stoneage-rebuild-hitmap-lineage-audit/1"},
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        return response.read()


def _function_body(text: str, signature_pattern: str) -> str:
    match = re.search(signature_pattern, text, re.I | re.S)
    if not match:
        raise ValueError(f"function not found: {signature_pattern}")
    brace = text.find("{", match.end())
    if brace < 0:
        raise ValueError("function opening brace not found")
    depth = 0
    for index in range(brace, len(text)):
        char = text[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[match.start() : index + 1]
    raise ValueError("function closing brace not found")


def _active_read_hitmap(text: str) -> str:
    # Skip prototypes by requiring the named x1/y1 argument form used by all
    # three pinned active implementations.
    return _function_body(
        text,
        r"void\s+readHitMap\s*\(\s*int\s+x1\s*,\s*int\s+y1",
    )


def _check_hitmap(text: str) -> str:
    return _function_body(
        text,
        r"(?:BOOL|bool)\s+checkHitMap\s*\(\s*int\s+gx\s*,\s*int\s+gy",
    )


def _compact(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def algorithm_features(map_source: str) -> dict[str, bool]:
    read = _active_read_hitmap(map_source)
    check = _check_hitmap(map_source)
    r = _compact(read)
    c = _compact(check)

    cases = {
        int(value)
        for value in re.findall(r"case\s+(\d+)\s*:", read)
    }

    return {
        "active_read_hitmap": bool(read),
        "tile_adrn_gt99": bool(
            re.search(r"tile\s*\[[^\]]+\]\s*>\s*CG_INVISIBLE", r)
        ),
        "tile_adrn_60_79": bool(
            re.search(r"60\s*<=\s*tile\s*\[[^\]]+\].*?<=\s*79", r)
        ),
        "tile_zero_map_see_rule": (
            "case 0" in r and "MAP_SEE_FLAG" in r
        ),
        "small_block_codes": {1, 2, 5, 6, 9, 10}.issubset(cases),
        "small_override_code4": 4 in cases,
        "hit0_preserves_override": bool(
            re.search(r"hit\s*==\s*0.*?hitMap\s*\[[^\]]+\]\s*!=\s*2", r)
        ),
        "hit2_override": bool(
            re.search(r"hit\s*==\s*2", r)
            and re.search(r"hitMap\s*\[[^\]]+\]\s*=\s*2", r)
        ),
        "parts_adrn_gt99": bool(
            re.search(r"parts\s*\[[^\]]+\]\s*>\s*CG_INVISIBLE", r)
        ),
        "parts_footprint": (
            "realGetHitPoints" in r
            and "(i - k)" in r
            and "(j + l)" in r
        ),
        "parts_15680_15732": (
            "15680" in r and "15732" in r and "hit == 1" in r
        ),
        "parts_60_79": bool(
            re.search(r"60\s*<=\s*parts\s*\[[^\]]+\].*?<=\s*79", r)
        ),
        "event_npc_final_block": (
            "0x0fff" in r.lower() and "EVENT_NPC" in r
        ),
        "check_bounds_block": (
            "mapAreaWidth" in c
            and "mapAreaHeight" in c
            and "return TRUE" in c
        ),
        "check_hitmap_value1_blocks": bool(
            re.search(r"hitMap\s*\[[^\]]+\]\s*==\s*1", c)
        ),
    }


def header_features(header_source: str) -> dict[str, bool]:
    h = _compact(header_source)
    return {
        "map_attr_atari_xy": (
            "atari_x" in h and "atari_y" in h and "MAP_ATTR" in h
        ),
        "map_attr_hit": bool(
            re.search(r"unsigned\s+short\s+hit\s*;", h)
        ),
        "map_attr_height": bool(
            re.search(r"short\s+height\s*;", h)
        ),
        "map_attr_bmpnumber": (
            "bmpnumber" in h and "MAP_ATTR" in h
        ),
        "adrnbin_embeds_map_attr": bool(
            re.search(r"struct\s+ADRNBIN", h)
            and re.search(r"MAP_ATTR\s+attr\s*;", h)
        ),
    }


def _feature_signature(features: dict[str, bool], ordered: tuple[str, ...]) -> str:
    payload = "|".join(f"{key}={int(bool(features[key]))}" for key in ordered)
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


@dataclass(frozen=True)
class LineageAudit:
    spec: SourceSpec
    map_sha256: str
    header_sha256: str
    algorithm: dict[str, bool]
    header: dict[str, bool]
    explicit_sa25_marker: bool

    @property
    def algorithm_closed(self) -> bool:
        return all(self.algorithm.get(key, False) for key in ALGORITHM_FEATURES)

    @property
    def header_closed(self) -> bool:
        return all(self.header.get(key, False) for key in HEADER_FEATURES)

    @property
    def algorithm_signature(self) -> str:
        return _feature_signature(self.algorithm, ALGORITHM_FEATURES)

    @property
    def header_signature(self) -> str:
        return _feature_signature(self.header, HEADER_FEATURES)


def audit_source(spec: SourceSpec, map_raw: bytes, header_raw: bytes) -> LineageAudit:
    map_text = map_raw.decode("utf-8", "replace")
    header_text = header_raw.decode("utf-8", "replace")
    return LineageAudit(
        spec=spec,
        map_sha256=hashlib.sha256(map_raw).hexdigest(),
        header_sha256=hashlib.sha256(header_raw).hexdigest(),
        algorithm=algorithm_features(map_text),
        header=header_features(header_text),
        explicit_sa25_marker=(
            "_SA_VERSION_25" in map_text or "_SA_VERSION_25" in header_text
        ),
    )


def run() -> tuple[LineageAudit, ...]:
    rows = []
    for spec in SOURCES:
        rows.append(
            audit_source(
                spec,
                _fetch(spec.raw_url(spec.map_path)),
                _fetch(spec.raw_url(spec.header_path)),
            )
        )
    return tuple(rows)


def emit(rows: tuple[LineageAudit, ...]) -> None:
    print("StoneAge client hit-map multi-lineage provenance audit — R1")
    print(
        "EVIDENCE_ROLE|PUBLIC_PINNED_DESCENDANT_SOURCE|"
        "NOT_RECOVERED25_BINARY_IDENTITY"
    )
    print(
        "RULE|feature agreement supports a descendant-stable reconstruction "
        "profile; it does not prove sa_2903 machine-code identity"
    )
    print(f"COUNT|lineages|{len(rows)}")
    print(
        "COUNT|algorithm_closed_lineages|"
        f"{sum(row.algorithm_closed for row in rows)}"
    )
    print(
        "COUNT|header_closed_lineages|"
        f"{sum(row.header_closed for row in rows)}"
    )
    print(
        "COUNT|explicit_sa25_marker_lineages|"
        f"{sum(row.explicit_sa25_marker for row in rows)}"
    )

    algorithm_signatures = {row.algorithm_signature for row in rows}
    header_signatures = {row.header_signature for row in rows}
    print(f"COUNT|algorithm_feature_signatures|{len(algorithm_signatures)}")
    print(f"COUNT|header_feature_signatures|{len(header_signatures)}")

    for row in rows:
        print(
            "LINEAGE|"
            f"label={row.spec.label}|repository={row.spec.repository}|"
            f"commit={row.spec.commit}|map_sha256={row.map_sha256}|"
            f"header_sha256={row.header_sha256}|"
            f"algorithm_closed={int(row.algorithm_closed)}|"
            f"header_closed={int(row.header_closed)}|"
            f"sa25_marker={int(row.explicit_sa25_marker)}|"
            f"algorithm_signature={row.algorithm_signature}|"
            f"header_signature={row.header_signature}"
        )

    if len(rows) < 3:
        raise ValueError("at least three pinned StoneAge client lineages are required")
    if not all(row.algorithm_closed and row.header_closed for row in rows):
        raise ValueError("one or more lineage feature vectors are incomplete")
    if len(algorithm_signatures) != 1:
        raise ValueError("lineages disagree on audited hit-map semantics")
    if len(header_signatures) != 1:
        raise ValueError("lineages disagree on audited ADRNBIN/MAP_ATTR structure")
    if sum(row.explicit_sa25_marker for row in rows) < 2:
        raise ValueError("insufficient explicit StoneAge 2.5 family markers")

    print(
        "PROFILE|RECOVERED25_DESCENDANT_STABLE_CLIENT_HITMAP_R1|"
        "status=SUPPORTED_FOR_RECONSTRUCTION|"
        "exact_recovered25_binary_proof=0"
    )
    print(OUTPUT_RESOLUTION)


def main() -> None:
    argparse.ArgumentParser().parse_args()
    emit(run())


if __name__ == "__main__":
    main()
