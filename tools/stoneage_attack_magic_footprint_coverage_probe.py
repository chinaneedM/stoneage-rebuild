#!/usr/bin/env python3
"""Measure recovered25 AttackMagic footprint/order coverage without payload text."""

from __future__ import annotations

import argparse
import collections
from pathlib import Path

from tools.stoneage_attmagic_probe import parse_attmagic
from tools.stoneage_attack_magic_model import (
    ATTACK_MAGIC_TARGET_INDEX,
    remap_attack_magic_target,
)
from tools.stoneage_attack_magic_footprint_model import (
    footprint_target_set,
    matrix_from_attmagic_record,
    source_sort_is_portable,
)

RECOVERED_MAGIC_IDS = tuple(range(301, 326))


def _magic_idx_by_id(path):
    out = {}
    malformed = 0
    for raw in path.read_bytes().splitlines():
        line = raw.strip()
        if not line or line.startswith(b"#"):
            continue
        fields = [
            x.strip()
            for x in line.replace(b"\t", b" ").split(b",")
        ]
        if len(fields) < 9:
            continue
        try:
            magic_id = int(fields[4], 10)
        except ValueError:
            malformed += 1
            continue
        if not fields[8]:
            continue
        try:
            idx = int(fields[8], 10)
        except ValueError:
            malformed += 1
            continue
        if magic_id in out:
            raise ValueError(f"duplicate magic ID {magic_id}")
        out[magic_id] = idx
    return out, malformed


def analyze(data_dir):
    data_dir = Path(data_dir)
    records = parse_attmagic(data_dir / "attmagic.bin")
    if len(records) % 2:
        raise ValueError("attmagic record count is not even")
    magic_index_count = len(records) // 2
    idx_by_id, malformed = _magic_idx_by_id(data_dir / "magic.txt")

    rows = []
    target_count_scenarios = collections.Counter()
    side_pair_matrix_equal = 0

    for magic_id in RECOVERED_MAGIC_IDS:
        idx = idx_by_id.get(magic_id)
        if idx is None or not 0 <= idx < magic_index_count:
            rows.append(
                {
                    "magic_id": magic_id,
                    "idx": idx,
                    "missing": True,
                }
            )
            continue

        # Recovered local runtime maps player participants to slots 0..9 and
        # enemies to 10..19. Enemy AttackMagic therefore uses the even IDX*2
        # record and targets side 0.
        even_matrix = matrix_from_attmagic_record(records[idx * 2])
        odd_matrix = matrix_from_attmagic_record(records[idx * 2 + 1])
        if even_matrix == odd_matrix:
            side_pair_matrix_equal += 1

        scenario_sizes = []
        portable = 0
        multi = 0
        empty = 0
        for initial_target in range(10):
            selector = remap_attack_magic_target(
                magic_id,
                initial_target,
            )
            targets = footprint_target_set(
                selector=selector,
                matrix=even_matrix,
                alive_slots=range(10),
            )
            size = len(targets)
            scenario_sizes.append(size)
            target_count_scenarios[size] += 1
            if size == 0:
                empty += 1
            if size > 1:
                multi += 1
            if source_sort_is_portable(targets):
                portable += 1

        rows.append(
            {
                "magic_id": magic_id,
                "idx": idx,
                "missing": False,
                "area": ATTACK_MAGIC_TARGET_INDEX[magic_id],
                "even_nonzero": sum(
                    bool(value)
                    for matrix_row in even_matrix
                    for value in matrix_row
                ),
                "odd_nonzero": sum(
                    bool(value)
                    for matrix_row in odd_matrix
                    for value in matrix_row
                ),
                "matrix_equal": even_matrix == odd_matrix,
                "min_targets": min(scenario_sizes),
                "max_targets": max(scenario_sizes),
                "portable": portable,
                "multi": multi,
                "empty": empty,
            }
        )

    present = tuple(row for row in rows if not row["missing"])
    total_scenarios = len(present) * 10
    portable = sum(row["portable"] for row in present)
    multi = sum(row["multi"] for row in present)
    empty = sum(row["empty"] for row in present)

    return {
        "magic_index_count": magic_index_count,
        "rows": tuple(rows),
        "present": len(present),
        "malformed": malformed,
        "total_scenarios": total_scenarios,
        "portable": portable,
        "multi": multi,
        "empty": empty,
        "target_count_scenarios": target_count_scenarios,
        "side_pair_matrix_equal": side_pair_matrix_equal,
        "complete": len(present) == 25 and malformed == 0,
    }


def emit(data_dir):
    r = analyze(data_dir)
    print("StoneAge recovered25 AttackMagic footprint coverage — R1")
    print(
        "Scenario = enemy side-1 caster using even IDX*2 record against "
        "fully alive player side 0; no recovered names/options/payload bytes stored."
    )
    print(f"SOURCE_MAGIC_INDEX_COUNT|{r['magic_index_count']}")
    print(f"RECOVERED_MAGIC_ROWS_PRESENT|{r['present']}")
    print(f"MAGIC_PARSE_BAD|{r['malformed']}")
    print(
        "RECOVERED_SIDE_PAIR_MATRIX_EQUAL|"
        f"{r['side_pair_matrix_equal']}"
    )
    print(f"SCENARIOS|{r['total_scenarios']}")
    print(f"SOURCE_SORT_PORTABLE_SCENARIOS|{r['portable']}")
    print(
        "SOURCE_SORT_NONPORTABLE_SCENARIOS|"
        f"{r['total_scenarios'] - r['portable']}"
    )
    print(f"MULTI_TARGET_SCENARIOS|{r['multi']}")
    print(f"EMPTY_TARGET_SCENARIOS|{r['empty']}")
    for target_count, count in sorted(r["target_count_scenarios"].items()):
        print(
            f"TARGET_COUNT_SCENARIOS|{target_count}|{count}"
        )
    for row in r["rows"]:
        if row["missing"]:
            print(
                f"MAGIC_COVERAGE|magic={row['magic_id']}|missing=1"
            )
            continue
        print(
            "MAGIC_COVERAGE|"
            f"magic={row['magic_id']}|"
            f"idx={row['idx']}|"
            f"area={row['area']}|"
            f"even_nonzero={row['even_nonzero']}|"
            f"odd_nonzero={row['odd_nonzero']}|"
            f"side_matrix_equal={int(row['matrix_equal'])}|"
            f"min_targets={row['min_targets']}|"
            f"max_targets={row['max_targets']}|"
            f"portable_scenarios={row['portable']}|"
            f"multi_scenarios={row['multi']}|"
            f"empty_scenarios={row['empty']}"
        )
    print(
        "RESOLUTION|"
        + (
            "RECOVERED25_ATTACKMAGIC_FOOTPRINT_COVERAGE_AUDITED"
            if r["complete"]
            else "RECOVERED25_ATTACKMAGIC_FOOTPRINT_COVERAGE_OPEN"
        )
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=Path, required=True)
    args = ap.parse_args()
    emit(args.data_dir)


if __name__ == "__main__":
    main()
