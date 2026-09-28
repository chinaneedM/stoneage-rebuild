#!/usr/bin/env python3
"""Audit anonymous NPC graphic/type symbol tokens against fixed mappings.

Raw recovered token strings are used transiently for lookup and never emitted.
The report stores only SHA-256 token identities, source numeric mappings,
cross-source consensus, and Taiwan-v1 SPR-resource membership.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import re
from collections import Counter, defaultdict
from pathlib import Path

from tools.stoneage_npc_world_graph_probe import iter_blocks, magic_kind
from tools.stoneage_versioned_npc_template_binding_probe import _opaque_name_key


SOURCE_VERSION = "recovered25"
EVIDENCE_ROLE = "LATER_RECOVERED"
DEFAULT_TYPE_TOKEN = b"SPR_pet001"

_DEFINE_RE = re.compile(
    rb"^\s*#define\s+([A-Za-z_][A-Za-z0-9_]*)\s+"
    rb"([^\s/]+)"
)


def _token_key(token: bytes) -> str:
    return hashlib.sha256(token.strip().lower()).hexdigest()


def _int_literal(value: bytes) -> int | None:
    value = value.strip().strip(b"()")
    try:
        return int(value, 0)
    except ValueError:
        return None


def parse_anim_defines(path: Path) -> dict[str, int]:
    """Resolve numeric and simple macro-alias defines from anim_tbl.h."""
    raw: dict[str, bytes] = {}
    for line in path.read_bytes().splitlines():
        match = _DEFINE_RE.match(line)
        if not match:
            continue
        raw[match.group(1).decode("ascii")] = match.group(2)

    cache: dict[str, int | None] = {}

    def resolve(name: str, stack: set[str]) -> int | None:
        if name in cache:
            return cache[name]
        if name in stack or name not in raw:
            return None
        value = raw[name]
        literal = _int_literal(value)
        if literal is not None:
            cache[name] = literal
            return literal
        target = value.decode("ascii", "ignore").strip().strip("()")
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", target):
            cache[name] = None
            return None
        result = resolve(target, stack | {name})
        cache[name] = result
        return result

    out = {}
    for name in raw:
        value = resolve(name, set())
        if value is not None:
            out[name.lower()] = value
    return out


def _binding_identity_keys(path: Path) -> set[str]:
    keys = set()
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.startswith("TEMPLATE_IDENTITY|"):
            fields = dict(
                part.split("=", 1) for part in raw.split("|")[1:]
            )
            keys.add(fields["key"])
    if not keys:
        raise ValueError("binding report contains no template identities")
    return keys


def _profile_expected_opaque_keys(
    path: Path,
) -> tuple[set[str], set[str]]:
    graphic = set()
    type_keys = set()
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.startswith("TEMPLATE_PROFILE|"):
            continue
        fields = dict(
            part.split("=", 1) for part in raw.split("|")[1:]
        )
        if fields["graphic_resolution"] == "OPAQUE_SYMBOL":
            graphic.add(fields["graphic_token_key"])
        if fields["type_resolution"] == "OPAQUE_SYMBOL":
            type_keys.add(fields["type_token_key"])
    return graphic, type_keys


def _recover_symbol_tokens(
    *,
    npc_dir: Path,
    identity_keys: set[str],
) -> dict[str, dict[str, object]]:
    found: dict[str, dict[str, object]] = {}

    def add(token: bytes, role: str) -> None:
        token = token.strip()
        if not token:
            return
        try:
            int(token, 10)
            return
        except ValueError:
            pass
        key = _token_key(token)
        entry = found.setdefault(
            key,
            {"token": token, "roles": set(), "occurrences": 0},
        )
        if entry["token"].lower() != token.lower():
            raise ValueError("SHA-256 token identity collision")
        entry["roles"].add(role)
        entry["occurrences"] += 1

    paths = sorted(
        (
            path for path in npc_dir.rglob("*")
            if path.is_file() and magic_kind(path) == "template"
        ),
        key=lambda path: str(path).lower(),
    )
    for path in paths:
        for entries in iter_blocks(path):
            fields = {}
            for key, value in entries:
                fields[key] = value
            name = fields.get(b"templatename", b"").strip()
            if not name:
                continue
            if _opaque_name_key(name.lower()) not in identity_keys:
                continue
            if b"graphicname" in fields:
                add(fields[b"graphicname"], "graphic")
            if b"type" in fields:
                add(fields[b"type"], "type")

    add(DEFAULT_TYPE_TOKEN, "type_default")
    return found


def _spr_group_ids(path: Path) -> set[int]:
    out = set()
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        header = next(handle, "").rstrip("\n").split("\t")
        if "spr_no" not in header:
            raise ValueError("SPR group metadata lacks spr_no column")
        index = header.index("spr_no")
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) <= index:
                continue
            out.add(int(parts[index]))
    return out


def analyze(
    *,
    binding_report: Path,
    profile_report: Path,
    npc_dir: Path,
    gavin_anim: Path,
    iris_anim: Path,
    bismarck_anim: Path,
    tw1_spr_groups: Path,
    recovered_anim: Path | None = None,
):
    identity_keys = _binding_identity_keys(binding_report)
    expected_graphic, expected_type = _profile_expected_opaque_keys(
        profile_report
    )
    tokens = _recover_symbol_tokens(
        npc_dir=npc_dir,
        identity_keys=identity_keys,
    )

    actual_graphic = {
        key for key, entry in tokens.items()
        if "graphic" in entry["roles"]
    }
    actual_type = {
        key for key, entry in tokens.items()
        if "type" in entry["roles"]
    }
    if actual_graphic != expected_graphic:
        raise ValueError(
            "raw graphic symbol tokens do not match profile report hashes"
        )
    if actual_type != expected_type:
        raise ValueError(
            "raw type symbol tokens do not match profile report hashes"
        )

    tables = {
        "gavin": parse_anim_defines(gavin_anim),
        "iris": parse_anim_defines(iris_anim),
        "bismarck": parse_anim_defines(bismarck_anim),
    }
    if recovered_anim is not None:
        tables["recovered25"] = parse_anim_defines(recovered_anim)

    tw1_ids = _spr_group_ids(tw1_spr_groups)
    rows = []
    counts = Counter()
    for key in sorted(tokens):
        entry = tokens[key]
        token = entry["token"]
        lookup = token.decode("ascii", "ignore").lower()
        values = {
            source: table.get(lookup)
            for source, table in tables.items()
        }
        fixed = [
            values["gavin"],
            values["iris"],
            values["bismarck"],
        ]
        nonnull = [value for value in fixed if value is not None]
        fixed_consensus = (
            nonnull[0]
            if len(nonnull) == 3 and len(set(nonnull)) == 1
            else None
        )
        recovered = values.get("recovered25")
        if recovered is not None:
            classification = "RECOVERED25_DIRECT"
            bridge_value = recovered
        elif fixed_consensus is not None:
            classification = "FIXED_THREE_WAY_CONSENSUS"
            bridge_value = fixed_consensus
        elif nonnull and len(set(nonnull)) == 1:
            classification = "FIXED_PARTIAL_CONSENSUS"
            bridge_value = None
        else:
            classification = "UNRESOLVED_OR_DIVERGENT"
            bridge_value = None

        tw1_present = (
            None if bridge_value is None
            else bridge_value in tw1_ids
        )
        bridge_eligible = bool(
            bridge_value is not None
            and tw1_present
            and classification in {
                "RECOVERED25_DIRECT",
                "FIXED_THREE_WAY_CONSENSUS",
            }
        )
        rows.append({
            "key": key,
            "roles": tuple(sorted(entry["roles"])),
            "occurrences": int(entry["occurrences"]),
            "recovered25": recovered,
            "gavin": values["gavin"],
            "iris": values["iris"],
            "bismarck": values["bismarck"],
            "fixed_consensus": fixed_consensus,
            "bridge_value": bridge_value,
            "tw1_spr_present": tw1_present,
            "classification": classification,
            "bridge_eligible": bridge_eligible,
        })
        counts[f"classification:{classification}"] += 1
        counts[f"bridge_eligible:{int(bridge_eligible)}"] += 1

    counts["anonymous_symbol_tokens"] = len(rows)
    counts["opaque_graphic_tokens"] = len(expected_graphic)
    counts["opaque_type_tokens"] = len(expected_type)
    counts["default_type_tokens"] = 1
    counts["tokens_with_tw1_resource_bridge"] = sum(
        row["bridge_eligible"] for row in rows
    )
    return tuple(rows), counts


def _value(value) -> str:
    return "NA" if value is None else str(int(value))


def emit(rows, counts) -> None:
    print("StoneAge anonymous NPC graphic/type symbol resolution audit — R1")
    print(
        "SCOPE|anonymous-token-hashes-and-numeric-mappings-only|"
        "no-raw-symbol-names|no-template-names|no-dialogue|no-source-rows"
    )
    print(f"SEMANTIC_SOURCE_VERSION|{SOURCE_VERSION}")
    print(f"EVIDENCE_ROLE|{EVIDENCE_ROLE}")
    print(
        "SOURCE_REVISION|gavinlinasd/StoneAge|"
        "1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56"
    )
    print(
        "SOURCE_REVISION|iriselia/StoneAge|"
        "9e6c8ce2cd8ed532a7157773acd1c61582c178b5"
    )
    print(
        "SOURCE_REVISION|BismarckDD/stoneage|"
        "999ffdf1d220ec6666eb65339180689c9caf1876"
    )
    for key in sorted(counts):
        print(f"COUNT|{key}|{counts[key]}")
    for row in rows:
        print(
            "SYMBOL_TOKEN|"
            f"key={row['key']}|"
            f"roles={','.join(row['roles'])}|"
            f"occurrences={row['occurrences']}|"
            f"recovered25={_value(row['recovered25'])}|"
            f"gavin={_value(row['gavin'])}|"
            f"iris={_value(row['iris'])}|"
            f"bismarck={_value(row['bismarck'])}|"
            f"fixed_consensus={_value(row['fixed_consensus'])}|"
            f"bridge_value={_value(row['bridge_value'])}|"
            f"tw1_spr_present={('NA' if row['tw1_spr_present'] is None else int(row['tw1_spr_present']))}|"
            f"classification={row['classification']}|"
            f"bridge_eligible={int(row['bridge_eligible'])}"
        )
    print("RESOLUTION|ANONYMOUS_NPC_SYMBOL_RESOLUTION_AUDITED")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binding-report", type=Path, required=True)
    parser.add_argument("--profile-report", type=Path, required=True)
    parser.add_argument("--npc-dir", type=Path, required=True)
    parser.add_argument("--gavin-anim", type=Path, required=True)
    parser.add_argument("--iris-anim", type=Path, required=True)
    parser.add_argument("--bismarck-anim", type=Path, required=True)
    parser.add_argument("--tw1-spr-groups", type=Path, required=True)
    parser.add_argument("--recovered-anim", type=Path)
    args = parser.parse_args()

    rows, counts = analyze(
        binding_report=args.binding_report,
        profile_report=args.profile_report,
        npc_dir=args.npc_dir,
        gavin_anim=args.gavin_anim,
        iris_anim=args.iris_anim,
        bismarck_anim=args.bismarck_anim,
        tw1_spr_groups=args.tw1_spr_groups,
        recovered_anim=args.recovered_anim,
    )
    emit(rows, counts)


if __name__ == "__main__":
    main()
