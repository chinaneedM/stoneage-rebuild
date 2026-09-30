#!/usr/bin/env python3
"""Audit recovered25 NPC functionset CHAR_ISOVERED initialization lineage.

The recovered world binding report supplies the functionsets actually used by
stable-world placements. Three pinned public descendant server lineages supply:
- functionset -> INITFUNC mapping from npctemplate.c;
- INITFUNC bodies and same-file CHAR_ISOVERED setters.

The output is a placement-weighted behavior profile. It does not claim exact
recovered25 binary identity and it does not infer overability when an INITFUNC
contains no direct setter.
"""

from __future__ import annotations

import argparse
import re
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


OUTPUT_RESOLUTION = "RESOLUTION|RECOVERED25_NPC_OVERABILITY_LINEAGE_AUDITED"

STATIC_BLOCKING = "STATIC_BLOCKING"
STATIC_OVERABLE = "STATIC_OVERABLE"
DYNAMIC = "DYNAMIC"
UNRESOLVED = "UNRESOLVED"
LINEAGE_DIVERGENT = "LINEAGE_DIVERGENT"


@dataclass(frozen=True)
class SourceSpec:
    label: str
    repository: str
    commit: str
    npc_prefix: str
    template_path: str

    def raw_url(self, path: str) -> str:
        quoted = "/".join(
            urllib.parse.quote(part, safe="") for part in path.split("/")
        )
        return (
            f"https://raw.githubusercontent.com/{self.repository}/"
            f"{self.commit}/{quoted}"
        )


SOURCES = (
    SourceSpec(
        "gavin",
        "gavinlinasd/StoneAge",
        "1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56",
        "gmsv/src/npc",
        "gmsv/src/npc/npctemplate.c",
    ),
    SourceSpec(
        "iris",
        "iriselia/StoneAge",
        "9e6c8ce2cd8ed532a7157773acd1c61582c178b5",
        "Source/gmsv/npc",
        "Source/gmsv/npc/npctemplate.c",
    ),
    SourceSpec(
        "bismarck",
        "BismarckDD/Stoneage",
        "2f736808ff4361f5429ee919b718c88fabb60346",
        "server/gmsv/npc",
        "server/gmsv/npc/npctemplate.c",
    ),
)


def _fetch(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "stoneage-rebuild-npc-overability-audit/1"},
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        return response.read().decode("utf-8", "replace")


def _strip_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"//[^\n\r]*", "", text)
    return text


def parse_functionset_init_map(text: str) -> dict[str, str]:
    cleaned = _strip_comments(text)
    out: dict[str, str] = {}
    pattern = re.compile(
        r'\{\s*"([^"]+)"\s*,\s*"([^"]*)"',
        re.S,
    )
    for match in pattern.finditer(cleaned):
        functionset = match.group(1)
        initfunc = match.group(2)
        if functionset in out and out[functionset] != initfunc:
            raise ValueError(f"functionset init mapping drift: {functionset}")
        out[functionset] = initfunc
    if not out:
        raise ValueError("npctemplate functionSet table was not parsed")
    return out


def _function_body(text: str, function_name: str) -> str:
    if not function_name:
        return ""
    cleaned = _strip_comments(text)
    match = re.search(
        rf"\b{re.escape(function_name)}\s*\([^;{{}}]*\)\s*\{{",
        cleaned,
        re.S,
    )
    if not match:
        raise ValueError(f"init function body not found: {function_name}")
    brace = cleaned.find("{", match.start())
    depth = 0
    for index in range(brace, len(cleaned)):
        char = cleaned[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return cleaned[match.start() : index + 1]
    raise ValueError(f"unterminated init function: {function_name}")


def overability_setter_values(text: str) -> tuple[int, ...]:
    cleaned = _strip_comments(text)
    values = {
        int(value)
        for value in re.findall(
            r"CHAR_setFlg\s*\([^;]*?CHAR_ISOVERED\s*,\s*([01])\s*\)",
            cleaned,
            re.S,
        )
    }
    return tuple(sorted(values))


def classify_init_and_file(
    *,
    init_values: tuple[int, ...],
    file_values: tuple[int, ...],
) -> str:
    init = set(init_values)
    file = set(file_values)
    if not init:
        return UNRESOLVED
    if len(init) > 1 or len(file) > 1:
        return DYNAMIC
    value = next(iter(init))
    if value == 0:
        return STATIC_BLOCKING
    if value == 1:
        return STATIC_OVERABLE
    raise AssertionError("unexpected CHAR_ISOVERED value")


def _binding_counts(path: Path) -> Counter:
    counts = Counter()
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line.startswith("PLACEMENT_TEMPLATE|"):
            continue
        fields = {}
        for part in line.split("|")[1:]:
            if "=" in part:
                key, value = part.split("=", 1)
                fields[key] = value
        if "functionset_consensus" not in fields:
            raise ValueError("binding placement lacks functionset_consensus")
        counts[fields["functionset_consensus"]] += 1
    if not counts:
        raise ValueError("binding report contains no placement rows")
    return counts


@dataclass(frozen=True)
class LineageFunctionsetResult:
    functionset: str
    placement_count: int
    classification: str
    lineage_classifications: tuple[tuple[str, str], ...]
    init_values: tuple[int, ...]
    file_values: tuple[int, ...]


def _source_path(functionset: str, spec: SourceSpec) -> str:
    return f"{spec.npc_prefix}/npc_{functionset.lower()}.c"


def analyze(binding_report: Path) -> tuple[LineageFunctionsetResult, ...]:
    counts = _binding_counts(binding_report)
    template_maps = {
        spec.label: parse_functionset_init_map(_fetch(spec.raw_url(spec.template_path)))
        for spec in SOURCES
    }

    rows = []
    for functionset, placement_count in sorted(
        counts.items(), key=lambda item: (-item[1], item[0])
    ):
        if functionset == "<none>":
            rows.append(
                LineageFunctionsetResult(
                    functionset=functionset,
                    placement_count=placement_count,
                    classification=UNRESOLVED,
                    lineage_classifications=tuple(
                        (spec.label, UNRESOLVED) for spec in SOURCES
                    ),
                    init_values=(),
                    file_values=(),
                )
            )
            continue

        per_lineage = []
        all_init_values = set()
        all_file_values = set()
        for spec in SOURCES:
            initfunc = template_maps[spec.label].get(functionset)
            if initfunc is None:
                # Functionset casing can differ across packages.
                folded = {
                    key.lower(): value
                    for key, value in template_maps[spec.label].items()
                }
                initfunc = folded.get(functionset.lower())
            if not initfunc:
                per_lineage.append((spec.label, UNRESOLVED))
                continue

            path = _source_path(functionset, spec)
            try:
                source = _fetch(spec.raw_url(path))
            except urllib.error.HTTPError as exc:
                if exc.code == 404:
                    per_lineage.append((spec.label, UNRESOLVED))
                    continue
                raise

            try:
                body = _function_body(source, initfunc)
            except ValueError:
                per_lineage.append((spec.label, UNRESOLVED))
                continue
            init_values = overability_setter_values(body)
            file_values = overability_setter_values(source)
            classification = classify_init_and_file(
                init_values=init_values,
                file_values=file_values,
            )
            per_lineage.append((spec.label, classification))
            all_init_values.update(init_values)
            all_file_values.update(file_values)

        classes = {value for _label, value in per_lineage}
        resolved = {value for value in classes if value != UNRESOLVED}
        if not resolved:
            final = UNRESOLVED
        elif len(resolved) == 1 and classes <= (resolved | {UNRESOLVED}):
            final = next(iter(resolved))
        else:
            final = LINEAGE_DIVERGENT

        rows.append(
            LineageFunctionsetResult(
                functionset=functionset,
                placement_count=placement_count,
                classification=final,
                lineage_classifications=tuple(per_lineage),
                init_values=tuple(sorted(all_init_values)),
                file_values=tuple(sorted(all_file_values)),
            )
        )
    return tuple(rows)


def emit(rows: tuple[LineageFunctionsetResult, ...]) -> None:
    print("StoneAge recovered25 NPC overability lineage audit — R1")
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print(
        "EVIDENCE_ROLE|PINNED_STABLE_DESCENDANT_FUNCTIONSET_BEHAVIOR|"
        "NOT_RECOVERED25_BINARY_IDENTITY"
    )
    for spec in SOURCES:
        print(
            f"SOURCE_REVISION|{spec.repository}|{spec.commit}"
        )

    placement_counts = Counter()
    functionset_counts = Counter()
    for row in rows:
        placement_counts[row.classification] += row.placement_count
        functionset_counts[row.classification] += 1

    print(f"COUNT|functionsets|{len(rows)}")
    print(f"COUNT|placements|{sum(row.placement_count for row in rows)}")
    for classification in (
        STATIC_BLOCKING,
        STATIC_OVERABLE,
        DYNAMIC,
        UNRESOLVED,
        LINEAGE_DIVERGENT,
    ):
        print(
            f"COUNT|functionsets:{classification}|"
            f"{functionset_counts[classification]}"
        )
        print(
            f"COUNT|placements:{classification}|"
            f"{placement_counts[classification]}"
        )

    for row in rows:
        lineage = ",".join(
            f"{label}:{classification}"
            for label, classification in row.lineage_classifications
        )
        print(
            "FUNCTIONSET_OVERABILITY|"
            f"functionset={row.functionset}|"
            f"placements={row.placement_count}|"
            f"classification={row.classification}|"
            f"init_values={','.join(map(str,row.init_values))}|"
            f"file_values={','.join(map(str,row.file_values))}|"
            f"lineages={lineage}"
        )

    print(
        "RULE|UNRESOLVED means no direct INITFUNC setter was proven; "
        "no default CHAR flag value is guessed"
    )
    print(
        "RULE|DYNAMIC means same source file contains both CHAR_ISOVERED=0 "
        "and CHAR_ISOVERED=1 while init is directly evidenced"
    )
    print(OUTPUT_RESOLUTION)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binding-report", type=Path, required=True)
    args = parser.parse_args()
    emit(analyze(args.binding_report))


if __name__ == "__main__":
    main()
