"""SCENE16: source-pinned nearby NPC qualification, without publishing original scripts.

The public repository has original file *inventory* evidence, not the original
npc/genout/1000npc_m.create content. Without that byte-identical file this
module MUST NOT claim to have identified, rendered or interacted with an NPC.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = "npc/genout/1000npc_m.create"
SOURCE_SIZE = 4413
SOURCE_SHA256 = "c9b000a836b0aae3d88358097039f1beea020d92ba84f6ccc338bb54bc478240"
TEMPLATE_SIZE = 4950
TEMPLATE_SHA256 = "0c5a58d5e31cafd3b58ccc1fa88fee7d1f95d12c0b87b04db9f06fea3b2a4df3"
TARGET = (1000, 63, 103)
INDEX = ROOT / "research/recovered/STONEAGE-MIXED25-SERVER-FULL-SOURCE-R18.json"
DOORWAY = ROOT / "research/recovered/STONEAGE-SCENE15-DOORWAY-SOURCE-R1.json"
FALSE = (
    "original_client_executed", "original_server_executed",
    "original_world_entered", "original_npc_interaction_verified",
    "same_deployed_build_authenticated", "official_tw10_npc_authenticated",
    "native_npc_rendering_verified", "original_dialogue_published",
)


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def check(ok: bool, label: str) -> None:
    if not ok:
        raise ValueError(label)


def public_index(root: Path = ROOT) -> dict:
    """Independently check the one original manifest row and the preceding door."""
    index = json.loads((root / INDEX.relative_to(ROOT)).read_text(encoding="utf-8"))
    rows = [r for r in index["all_server_occurrences"] if r["path"] == SOURCE_PATH]
    check(len(rows) == 1, "one authoritative indexed source occurrence required")
    row = rows[0]
    check((row["size"], row["sha256"]) == (SOURCE_SIZE, SOURCE_SHA256),
          "source inventory is not the established R18 member")
    check(index["source_claim"] ==
          "ARCHIVED_MIXED_COMMUNITY_PRESERVATION_ACTUAL_FILE_HASHES_NOT_OFFICIAL_RELEASE",
          "wrong source provenance")
    scene = json.loads((root / DOORWAY.relative_to(ROOT)).read_text(encoding="utf-8"))
    arrivals = [d for d in scene["doorway_pair"] if
                d["source_floor"] == 1001 and d["source_xy"] == [10, 15]]
    check(len(arrivals) == 1 and arrivals[0]["destination_floor"] == 1000
          and arrivals[0]["destination_xy"] == [63, 99], "prior exact doorway anchor")
    check(scene["original_world_entered"] is False, "do not promote modern observer")
    return {
        "file": SOURCE_PATH, "bytes": SOURCE_SIZE, "sha256": SOURCE_SHA256,
        "catalog_schema": index["schema"], "catalog_source": str(INDEX.relative_to(ROOT)),
        "doorway_source": str(DOORWAY.relative_to(ROOT)),
        "anchor_arrival": [1000, 63, 99],
        "investigation_target": list(TARGET),
        "target_is_npc_source_verified": False,
    }


def parse_blocks(raw: bytes, magic: bytes) -> list[dict]:
    """Bounded byte parser; do not decode or publish name/dialogue values."""
    check(raw.splitlines()[:1] == [magic], "unexpected original config header")
    matches = list(re.finditer(rb"(?ms)^\{\r?\n.*?^\}", raw))
    opens = len(re.findall(rb"(?m)^\{\r?$", raw))
    closes = len(re.findall(rb"(?m)^\}\r?$", raw))
    check(bool(matches) and len(matches) == opens == closes,
          "source config block delimiter mismatch")
    result = []
    for m in matches:
        fields = {}
        for line in m.group().splitlines()[1:-1]:
            if not line.strip() or line.lstrip().startswith(b"#"):
                continue
            check(b"=" in line, "unrecognized config field")
            key, value = line.split(b"=", 1)
            try:
                key = key.strip().decode("ascii")
            except UnicodeDecodeError as exc:
                raise ValueError("non-ASCII config key") from exc
            check(key and key not in fields, "duplicate or empty field")
            fields[key] = value.strip()
        result.append({
            "ordinal": len(result), "byte_start": m.start(), "byte_end": m.end(),
            "block_sha256": digest(m.group()), "fields": fields,
        })
    return result


def inside_target(fields: dict, target: tuple[int, int, int] = TARGET) -> bool:
    if fields.get("floorid") != str(target[0]).encode():
        return False
    try:
        coords = [int(x) for x in fields["borncorner"].split(b",")]
    except (ValueError, KeyError):
        raise ValueError("source spawn coordinate grammar is not qualified")
    check(len(coords) == 4, "expected four source borncorner coordinates")
    x0, y0, x1, y1 = coords
    check(x0 <= x1 and y0 <= y1, "source spawn range inverted")
    return x0 <= target[1] <= x1 and y0 <= target[2] <= y1


def _safe_ascii_token(raw: bytes) -> str | None:
    try:
        value = raw.decode("ascii")
    except UnicodeDecodeError:
        return None
    return value if re.fullmatch(r"[A-Za-z0-9_]{1,80}", value) else None


def summarize_candidate(block: dict, templates: list[dict] | None) -> dict:
    f = block["fields"]
    for name in ("floorid", "borncorner", "graphicname", "createnum", "dir", "time"):
        check(name in f, "original NPC config missing " + name)
    try:
        coords = [int(n) for n in f["borncorner"].split(b",")]
        numeric = {k: int(f[k]) for k in ("floorid", "graphicname", "createnum", "dir", "time")}
    except ValueError as exc:
        raise ValueError("source numeric field grammar unresolved") from exc
    check(len(coords) == 4, "original four-coordinate spawn required")
    token = _safe_ascii_token(f.get("enemy", b"").split(b"|", 1)[0])
    row = {
        "ordinal": block["ordinal"], "source_byte_range": [block["byte_start"], block["byte_end"]],
        "source_block_sha256": block["block_sha256"],
        "borncorner": coords, "numeric_source_fields": numeric,
        "name_original_raw_bytes": len(f.get("name", b"")),
        "name_original_sha256": digest(f.get("name", b"")),
        "enemy_field_sha256": digest(f.get("enemy", b"")),
        "template_lookup_token": token,
        "original_dialogue": None,
    }
    if templates is None:
        row["template_binding"] = "TEMPLATE_SOURCE_NOT_SUPPLIED"
    elif token is None:
        row["template_binding"] = "TEMPLATE_TOKEN_UNQUALIFIED"
    else:
        found = [t for t in templates
                 if t["fields"].get("templatename") == token.encode()]
        if len(found) == 1:
            t = found[0]
            row["template_binding"] = "EXACT_TEMPLATE_NAME_IN_PINNED_MEMBER"
            row["template_source_block_sha256"] = t["block_sha256"]
            row["functionset_token"] = _safe_ascii_token(t["fields"].get("functionset", b""))
        else:
            row["template_binding"] = ("MISSING_MATCH" if not found else "AMBIGUOUS_DUPLICATES")
            row["matching_template_blocks"] = len(found)
    return row


def probe(create: bytes | None, template: bytes | None = None, root: Path = ROOT) -> dict:
    anchor = public_index(root)
    result = {
        "schema": "stoneage.scene16.town1000_nearby_npc_source_gate.r1",
        "scope": "MIXED25_ORIGINAL_MEMBER_PIN_NOT_OFFICIAL_TW10_OR_NATIVE_RUNTIME",
        "catalog_anchor": anchor, "source_status": "SOURCE_NOT_SUPPLIED",
        "matched_candidates": [], "matched_count": None,
        "original_npc_population_complete": False,
        "overall_completion_percent": None,
        **{key: False for key in FALSE},
    }
    check(create is not None or template is None, "template without original NPC create source")
    if create is None:
        return result
    check((len(create), digest(create)) == (SOURCE_SIZE, SOURCE_SHA256),
          "original 1000npc_m.create size and sha256 mismatch: no source promotion")
    if template is not None:
        check((len(template), digest(template)) == (TEMPLATE_SIZE, TEMPLATE_SHA256),
              "original template size and sha256 mismatch")
    blocks = parse_blocks(create, b"NPCCREATE")
    templates = parse_blocks(template, b"NPCTEMPLATE") if template is not None else None
    matches = [b for b in blocks if inside_target(b["fields"])]
    result["source_status"] = (
        "PINNED_MEMBER_NO_MATCH_AT_TARGET" if not matches else
        "PINNED_MEMBER_ONE_TARGET_CANDIDATE" if len(matches) == 1 else
        "PINNED_MEMBER_AMBIGUOUS_TARGET_CANDIDATES"
    )
    result["catalog_anchor"]["target_is_npc_source_verified"] = bool(matches)
    result["authenticated_create_blocks"] = len(blocks)
    result["authenticated_template_blocks"] = len(templates) if templates is not None else None
    result["matched_count"] = len(matches)
    result["matched_candidates"] = [summarize_candidate(b, templates) for b in matches]
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--create", type=Path, help="Private original 1000npc_m.create; SHA required")
    parser.add_argument("--template", type=Path, help="Optional exact original npcgen.template")
    args = parser.parse_args()
    check(not args.template or args.create, "cannot supply template without original create file")
    result = probe(args.create.read_bytes() if args.create else None,
                   args.template.read_bytes() if args.template else None)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
