#!/usr/bin/env python3
"""Compare recovered later StoneAge field-map corpora as versioned lineage evidence.

This tool never promotes later maps to Taiwan-v1 membership. It compares
concrete later payload identity and separately records whether each payload is
renderable by the accepted Taiwan-v1 ADRN resource profile.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from tools.stoneage_tw10_25_fieldmap_compat_probe import analyze


def normalize_rows(root: Path, rows):
    out = {}
    for path, info in rows:
        out[str(path.relative_to(root)).replace("\\", "/").lower()] = dict(info)
    return out


def compare_maps(a: dict, b: dict):
    shared = sorted(set(a) & set(b))
    only_a = sorted(set(a) - set(b))
    only_b = sorted(set(b) - set(a))
    same = [p for p in shared if a[p]["sha256"] == b[p]["sha256"]]
    changed = [p for p in shared if a[p]["sha256"] != b[p]["sha256"]]
    same_compat = [
        p for p in same
        if bool(a[p]["compatible"]) and bool(b[p]["compatible"])
    ]
    changed_compat_both = [
        p for p in changed
        if bool(a[p]["compatible"]) and bool(b[p]["compatible"])
    ]
    return {
        "shared": shared,
        "only_a": only_a,
        "only_b": only_b,
        "same": same,
        "changed": changed,
        "same_compatible_both": same_compat,
        "changed_compatible_both": changed_compat_both,
    }


def emit(root_a: Path, root_b: Path, profile: Path, label_a: str, label_b: str, sample_limit: int = 100):
    _, rows_a, invalid_a = analyze(root_a, profile)
    _, rows_b, invalid_b = analyze(root_b, profile)
    a = normalize_rows(root_a, rows_a)
    b = normalize_rows(root_b, rows_b)
    cmp = compare_maps(a, b)

    print("StoneAge later field-map lineage comparison — R1")
    print("SCOPE|later-corpus-byte-identity+tw1-resource-compatibility|does-not-prove-v1-membership|no-payload-retained")
    print(f"SOURCE_A|label={label_a}|valid_maps={len(a)}|invalid={len(invalid_a)}|compatible={sum(bool(x['compatible']) for x in a.values())}")
    print(f"SOURCE_B|label={label_b}|valid_maps={len(b)}|invalid={len(invalid_b)}|compatible={sum(bool(x['compatible']) for x in b.values())}")
    print(f"COUNT|shared_paths|{len(cmp['shared'])}")
    print(f"COUNT|same_path_same_sha256|{len(cmp['same'])}")
    print(f"COUNT|same_path_changed_sha256|{len(cmp['changed'])}")
    print(f"COUNT|same_sha256_and_tw1_compatible_both|{len(cmp['same_compatible_both'])}")
    print(f"COUNT|changed_sha256_and_tw1_compatible_both|{len(cmp['changed_compatible_both'])}")
    print(f"COUNT|only_{label_a}|{len(cmp['only_a'])}")
    print(f"COUNT|only_{label_b}|{len(cmp['only_b'])}")

    for path in cmp["same_compatible_both"][:sample_limit]:
        info = a[path]
        print(
            "STABLE_COMPATIBLE|"
            f"path={path}|width={info['width']}|height={info['height']}|"
            f"bytes={info['bytes']}|sha256={info['sha256']}|"
            f"required_ids={info['required_ids']}|required_cells={info['required_cells']}"
        )

    for path in cmp["changed"][:sample_limit]:
        aa, bb = a[path], b[path]
        print(
            "CHANGED|"
            f"path={path}|sha_a={aa['sha256']}|sha_b={bb['sha256']}|"
            f"compat_a={int(bool(aa['compatible']))}|compat_b={int(bool(bb['compatible']))}|"
            f"size_a={aa['width']}x{aa['height']}|size_b={bb['width']}x{bb['height']}"
        )

    for path in cmp["only_a"][:sample_limit]:
        info = a[path]
        print(f"ONLY_A|path={path}|sha256={info['sha256']}|compatible={int(bool(info['compatible']))}")
    for path in cmp["only_b"][:sample_limit]:
        info = b[path]
        print(f"ONLY_B|path={path}|sha256={info['sha256']}|compatible={int(bool(info['compatible']))}")

    print("RULE|same-path+same-sha256 across later corpora is strong later-lineage persistence, not proof of Taiwan-v1 membership")
    print("RESOLUTION|LATER_FIELDMAP_LINEAGE_CLASSIFIED")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root-a", type=Path, required=True)
    ap.add_argument("--root-b", type=Path, required=True)
    ap.add_argument("--profile", type=Path, required=True)
    ap.add_argument("--label-a", default="a")
    ap.add_argument("--label-b", default="b")
    ap.add_argument("--sample-limit", type=int, default=100)
    args = ap.parse_args()
    emit(args.root_a, args.root_b, args.profile, args.label_a, args.label_b, args.sample_limit)


if __name__ == "__main__":
    main()
