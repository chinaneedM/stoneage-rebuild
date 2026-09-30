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
INHERITED_DEFAULT_OVERABLE = "INHERITED_DEFAULT_OVERABLE"
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
    default_player_path: str
    char_base_path: str
    char_data_path: str
    npcgen_path: str

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
        "gmsv/src/char/defaultPlayer.h",
        "gmsv/src/include/char_base.h",
        "gmsv/src/char/char_data.c",
        "gmsv/src/npc/npcgen.c",
    ),
    SourceSpec(
        "iris",
        "iriselia/StoneAge",
        "9e6c8ce2cd8ed532a7157773acd1c61582c178b5",
        "Source/gmsv/npc",
        "Source/gmsv/npc/npctemplate.c",
        "Source/gmsv/char/defaultPlayer.h",
        "Source/gmsv/include/char_base.h",
        "Source/gmsv/char/char_data.c",
        "Source/gmsv/npc/npcgen.c",
    ),
    SourceSpec(
        "bismarck",
        "BismarckDD/Stoneage",
        "2f736808ff4361f5429ee919b718c88fabb60346",
        "server/gmsv/npc",
        "server/gmsv/npc/npctemplate.c",
        "server/gmsv/include/defaultPlayer.h",
        "server/gmsv/include/char_base.h",
        "server/gmsv/char/char_data.c",
        "server/gmsv/npc/npcgen.c",
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


def default_player_overable_value(
    *,
    default_player_source: str,
    char_base_source: str,
) -> int:
    base = _strip_comments(char_base_source)
    sequence = re.search(
        r"CHAR_ISATTACK\s*,\s*CHAR_ISATTACKED\s*,\s*"
        r"CHAR_ISOVER\s*,\s*CHAR_ISOVERED\s*,",
        base,
        re.S,
    )
    if not sequence:
        raise ValueError("CHAR_ISOVERED flag order is not lineage-compatible")

    player = _strip_comments(default_player_source)
    match = re.search(
        r"static\s+Char\s+player\s*=.*?"
        r"SETFLG\s*\(\s*([01])\s*,\s*([01])\s*,\s*"
        r"([01])\s*,\s*([01])\s*,\s*([01])\s*,\s*"
        r"([01])\s*,\s*([01])\s*,\s*([01])\s*\)",
        player,
        re.S,
    )
    if not match:
        raise ValueError("default player SETFLG row was not parsed")
    return int(match.group(4))


def default_chain_closed(*, char_data_source: str, npcgen_source: str) -> bool:
    char_data = _strip_comments(char_data_source)
    array_match = re.search(
        r"static\s+defaultCharacterGet\s+CHAR_defaultCharacterGet\s*\[\s*\]"
        r"\s*=\s*\{(.*?)\};",
        char_data,
        re.S,
    )
    if not array_match:
        raise ValueError("CHAR_defaultCharacterGet array was not parsed")
    array_body = array_match.group(1)
    refs = set(re.findall(r"&([A-Za-z_][A-Za-z0-9_]*)", array_body))
    data_refs = {value for value in refs if not value.startswith("lv")}
    if data_refs != {"player"}:
        raise ValueError(
            "default character array no longer resolves exclusively to player"
        )
    get_default = _function_body(char_data, "CHAR_getDefaultChar")
    if "nc->flg[j] = defaultchar->flg[j]" not in re.sub(r"\s+", " ", get_default):
        compact = re.sub(r"\s+", "", get_default)
        if "nc->flg[j]=defaultchar->flg[j]" not in compact:
            raise ValueError("CHAR_getDefaultChar no longer copies default flags")

    npcgen = _strip_comments(npcgen_source)
    body = _function_body(npcgen, "NPC_generateNPC")
    positions = [
        body.find("CHAR_getDefaultChar"),
        body.find("NPC_copyFunctionSetToChar"),
        body.find("CHAR_initCharOneArray"),
    ]
    if any(value < 0 for value in positions):
        raise ValueError("NPC generation initialization chain is incomplete")
    return positions[0] < positions[1] < positions[2]


def _template_direct_override_count(path: Path) -> int:
    counts = {}
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("COUNT|direct_override_count:"):
            parts = line.split("|")
            if len(parts) != 3:
                raise ValueError("malformed template direct-override count")
            key = parts[1].split(":", 1)[1]
            counts[int(key)] = int(parts[2])
    if not counts:
        raise ValueError("template profile report lacks direct-override counts")
    return sum(key * count for key, count in counts.items())


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


def analyze(
    binding_report: Path,
    template_profile_report: Path,
) -> tuple[LineageFunctionsetResult, ...]:
    counts = _binding_counts(binding_report)
    if _template_direct_override_count(template_profile_report) != 0:
        raise ValueError(
            "recovered template profiles contain direct callback overrides"
        )

    default_values = {}
    default_chains = {}
    for spec in SOURCES:
        default_values[spec.label] = default_player_overable_value(
            default_player_source=_fetch(spec.raw_url(spec.default_player_path)),
            char_base_source=_fetch(spec.raw_url(spec.char_base_path)),
        )
        default_chains[spec.label] = default_chain_closed(
            char_data_source=_fetch(spec.raw_url(spec.char_data_path)),
            npcgen_source=_fetch(spec.raw_url(spec.npcgen_path)),
        )
    if set(default_values.values()) != {1}:
        raise ValueError(f"lineages disagree on default CHAR_ISOVERED: {default_values}")
    if not all(default_chains.values()):
        raise ValueError("one or more NPC default initialization chains are open")

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

            body = None
            for symbol in (initfunc, f"NPC_{initfunc}"):
                try:
                    body = _function_body(source, symbol)
                    break
                except ValueError:
                    continue
            if body is None:
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
            # All audited lineages inherit default CHAR_ISOVERED=1 and the
            # recovered template layer has zero direct callback overrides.
            # No same-file setter was found for these functionsets.
            final = INHERITED_DEFAULT_OVERABLE
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
    print("DEFAULT_CHAR_ISOVERED|value=1|lineages=3")
    print("NPC_DEFAULT_CHAIN|CHAR_getDefaultChar->functionset->CHAR_initCharOneArray|lineages=3")
    print("TEMPLATE_DIRECT_CALLBACK_OVERRIDES|count=0")

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
        INHERITED_DEFAULT_OVERABLE,
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
        "RULE|INHERITED_DEFAULT_OVERABLE means no direct INITFUNC or same-file "
        "setter was found, template direct overrides are zero, and all three "
        "lineages inherit default CHAR_ISOVERED=1 before INITFUNC"
    )
    print(
        "RULE|UNRESOLVED remains reserved for a source/mapping gap; "
        "no default is guessed when the default chain is not closed"
    )
    print(
        "RULE|DYNAMIC means same source file contains both CHAR_ISOVERED=0 "
        "and CHAR_ISOVERED=1 while init is directly evidenced"
    )
    print(OUTPUT_RESOLUTION)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binding-report", type=Path, required=True)
    parser.add_argument("--template-profile-report", type=Path, required=True)
    args = parser.parse_args()
    emit(
        analyze(
            args.binding_report,
            args.template_profile_report,
        )
    )


if __name__ == "__main__":
    main()
