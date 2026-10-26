"""R28: source-qualified, read-only TW8.5 SPR137 native animation material.

Requires the exact two client payload files. The claimed-version MSI inventory is
not publisher authentication. Retain every source-index and animation/frame row;
never store proprietary originals or infer species, roles, FPS or server identities.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import json
from pathlib import Path

from tools.stoneage_cn50_spr_metadata import export_cn50_spr
from tools.stoneage_tw10_resource_metadata import SPRADRN_RECORD_SIZE

ROOT = Path(__file__).resolve().parents[1]
CLAIM = "TW85-INSTALLER-MSI-CLIENT_UNVERIFIED_COMMUNITY_PRESERVED"
SUBPATH = Path("Program Files/WAYI/石器時代 魔域大冒險/data")
ORIGINALS = {
    "spradrn_137.bin": (20868, "f31c00789321c948cde8c60769023567d8f89657231860e6ba730bc4a719206d"),
    "spr_137.bin": (8721504, "cf046548a0ed73ebbdd7d148400fcba3a0ff8d57d835d7b67ed90864d4975ce9"),
}
BASE = ROOT / "research/recovered"
REFERENCES = {
    "TW10": BASE / "tw10-resource-metadata/SPR-GROUP-R1.tsv.gz",
    "CN50": BASE / "cn50-resource-metadata/SPR-GROUP-R1.tsv.gz",
}
# Full original-derived byte pins, not just a document excerpt.
REFERENCE_SHA256 = {
    "TW10": "4db7809de4197eb90cca6dc04bda8550025e022c8232e2ebb902db0e9faf0175",
    "CN50": "67660d3d8ba5e05293f61f60ab3e1bfe736d7b6bdc4159ed96fcb59f5acfa228",
}


def require(ok, why):
    if not ok:
        raise ValueError(why)


def sha_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def qualify_pair(directory):
    directory = Path(directory)
    verified = {}
    for name, (length, digest) in ORIGINALS.items():
        path = directory / name
        require(path.is_file() and not path.is_symlink(), "missing/linked original: " + name)
        require(path.stat().st_size == length, "original byte length drift: " + name)
        require(sha_file(path) == digest, "original byte SHA256 drift: " + name)
        verified[name] = {"bytes": length, "sha256": digest}
    require(ORIGINALS["spradrn_137.bin"][0] % SPRADRN_RECORD_SIZE == 0,
            "non-integral original group index")
    return verified


def source_rows(path):
    with gzip.open(path, "rt", encoding="utf-8", newline="") as f:
        yield from csv.DictReader(f, delimiter="\t")


def pinned_reference_groups():
    result = {}
    for label, path in REFERENCES.items():
        require(path.is_file() and sha_file(path) == REFERENCE_SHA256[label],
                "complete reference group source changed: " + label)
        items = defaultdict(list)
        for row in source_rows(path):
            items[int(row["spr_no"])].append({
                "index": int(row["index"]),
                "segment_sha256": row["segment_sha256"],
            })
        result[label] = items
    return result


def compare(groups, refs):
    source_names = Counter()
    occurrence_count = len(groups)
    matches = defaultdict(list)
    duplicate_groups = {}
    for row in groups:
        n = int(row["spr_no"])
        source_names[n] += 1
        for label, table in refs.items():
            for reference in table.get(n, []):
                relation = "SAME_ID_AND_EXACT_FULL_SPR_SEGMENT" if reference["segment_sha256"] == row["segment_sha256"] else "SAME_ID_DIFFERENT_SPR_SEGMENT"
                matches[label].append({
                    "tw85_index": int(row["index"]), "spr_no": n,
                    "reference_index": reference["index"], "relation": relation,
                })
    duplicate_groups = {str(k): v for k, v in sorted(source_names.items()) if v > 1}
    return {
        "source_occurrences": occurrence_count,
        "unique_numeric_group_keys": len(source_names),
        "duplicate_source_group_keys": duplicate_groups,
        "reference_relationships": {label: values for label, values in matches.items()},
        "per_reference_relationship_counts": {
            label: dict(Counter(r["relation"] for r in matches.get(label, [])))
            for label in refs
        },
        "no_same_number_is_not_absence_in_other_versions": True,
        "same_number_does_not_certify_same_entity": True,
    }


def build(directory, out):
    out = Path(out)
    require(not out.resolve().is_relative_to(ROOT / "research/recovered"),
            "source-produced reports must be staged outside tracked archive until independently accepted")
    out.mkdir(parents=True, exist_ok=True)
    files = qualify_pair(directory)
    outputs = {s: out / ("SPR-" + s + "-R28.tsv.gz") for s in ("GROUP", "ANIMATION", "FRAME")}
    parsed = export_cn50_spr(Path(directory) / "spradrn_137.bin",
                             Path(directory) / "spr_137.bin",
                             outputs["GROUP"], outputs["ANIMATION"], outputs["FRAME"])
    groups = list(source_rows(outputs["GROUP"]))
    animations = list(source_rows(outputs["ANIMATION"]))
    frames = list(source_rows(outputs["FRAME"]))
    require(parsed["groups"] == len(groups) == files["spradrn_137.bin"]["bytes"] // 12,
            "exact SPR index row conservation broken")
    require(parsed["animations"] == len(animations) and parsed["frames"] == len(frames),
            "native header/frame conservation broken")
    require(parsed["exact_group_spans"] == len(groups), "trailing/overlapped group byte gap")
    require(all(int(row["end_offset"]) == int(row["next_offset"]) for row in groups),
            "undecoded source payload")
    require(all(int(row["group_index"]) < len(groups) for row in animations),
            "animation group index out of range")
    require(all(int(row["group_index"]) < len(groups) for row in frames),
            "frame group index out of range")
    links = compare(groups, pinned_reference_groups())
    result = {
        "schema": "stoneage.tw85_original_spr137_material.r28",
        "source": CLAIM,
        "source_inventory": "research/recovered/STONEAGE-WAYI85-MSI-CLIENT-PAYLOAD-R1.json",
        "pair": files,
        "parsed": parsed,
        "joins": links,
        "outputs": {name: {"bytes": file.stat().st_size, "sha256": sha_file(file)}
                    for name, file in outputs.items()},
        "limitations": {
            "publisher_clean_build_verified": False,
            "original_program_executed": False,
            "server_species_or_npc_identified": False,
            "source_bitmap_rd_payloads_available_in_this_pair": False,
            "original_rendered_pixels_available_in_this_pair": False,
            "fps_or_gameplay_action_meaning_proven": False,
            "original_payload_files_in_public_artifact": False,
            "cross_version_same_deployed_build_proven": False,
            "stage_a": "7_PARTIAL_2_OPEN",
            "stage_b_wiki": "GATED",
            "r79": "PAUSED_NON_BLOCKING",
            "restoration_percent": None,
        },
    }
    (out / "SOURCE-DERIVED-R28.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--payload-root", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    original_dir = args.payload_root / SUBPATH
    result = build(original_dir, args.output)
    print(json.dumps({"status": "ORIGINAL_PAIR_BYTES_AUTHENTICATED_AND_PARSED",
                      "source_grade": CLAIM,
                      "groups": result["parsed"]["groups"],
                      "animations": result["parsed"]["animations"],
                      "frames": result["parsed"]["frames"],
                      "pixels_or_entity_names_restored": False}, sort_keys=True))


if __name__ == "__main__":
    main()
