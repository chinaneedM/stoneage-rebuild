"""Independently replay PET16 ranges with the existing source-bounded PC models."""
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib
import json
from tools.stoneage_pet_growth_model import (
    RANK_ROLL_RANGES, pet_rank_from_template_base, project_pet_birth,
    pet_level_increments,
)
from tools.stoneage_pet_detail30_base_panel import project_pet_source_base_panel

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "research/pets/PET-HIGH-FIRST-15-TW75-MASTER-FIELD-CATALOG-R1.json"
REPORT = ROOT / "research/pets/PET-HIGH-FIRST-16-TW75-CONDITIONAL-BIRTH-GROWTH-R1.json"

def blob(p):
    data = p.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def compositions():
    for a in range(11):
        for b in range(11-a):
            for c in range(11-a-b):
                yield (a, b, c, 10-a-b-c)

ALLOCATIONS = tuple(compositions())

def rolls(counts):
    return tuple(i for i, n in enumerate(counts) for _ in range(n))

BIRTH_ROLLS = tuple(rolls(c) for c in ALLOCATIONS)

def ranges(samples):
    return [[min(v), max(v)] for v in zip(*samples)]

@lru_cache(None)
def one_growth(base, rank):
    # Every component count 0..10 is feasible, with remaining draws
    # assigned to another component. Each possible stored offset and rank
    # multiplier is enumerated, through the source model (binary32).
    lo, hi = RANK_ROLL_RANGES[rank]
    minimum, maximum = float("inf"), -float("inf")
    for offset, count, roll in product(range(-2, 3), range(11), range(lo, hi+1)):
        value = pet_level_increments(
            (base+offset, 20, 20, 20), rank,
            (0,)*count + (1,)*(10-count), roll
        )[0]
        minimum, maximum = min(minimum, value), max(maximum, value)
    return [minimum, maximum]

def project(row):
    base = row["base"]
    init = row["initnum"]
    if len(base) != 4 or any(not 2 <= v <= 253 for v in base) or init < 0:
        raise ValueError("unsupported growth base")
    rank = pet_rank_from_template_base(*base)
    internal = []
    panel = []
    # Positive monotone coefficients; simultaneous extreme offsets bound
    # every intermediate choice for each marginal output. Exhaust all 286
    # shared ten-point allocation compositions at both offset corners.
    for offset in (-2, 2):
        for draws in BIRTH_ROLLS:
            core = project_pet_birth(
                template_base=base, init_num=init,
                lvup_point=0, level=1, offsets=(offset,)*4,
                birth_rolls=draws,
            )
            # Lv1 makes the wild-level coefficient irrelevant; do NOT
            # coerce the source decimal coefficient for higher levels.
            assert core.rank == rank
            internal.append(core.internal_stats)
            p = project_pet_source_base_panel(core.internal_stats)
            panel.append((p.max_hp, p.attack, p.defense, p.quick))
    return dict(template_id=row["template_id"], source_row_sha256=row["row_sha256"],
                rank=rank, level1_internal_marginal_ranges=ranges(internal),
                level1_unmodified_work_panel_marginal_ranges=ranges(panel),
                per_level_internal_increment_marginal_ranges=[one_growth(b, rank) for b in base])

def verify():
    s, r = json.loads(SOURCE.read_bytes()), json.loads(REPORT.read_bytes())
    assert r["scope"] == "CLAIMED_TW75_TEMPLATE_X_LATER_PC_DEFAULT_MODEL_CONDITIONAL_NOT_OFFICIAL"
    for key in ("official_deployment_verified", "official_birth_stats_verified",
                "official_growth_verified", "actual_level1_availability_verified"):
        assert r[key] is False
    assert r["official_species_count"] is None
    assert r["input_git_blobs"] == {p: blob(ROOT/p) for p in (
        "research/pets/PET-HIGH-FIRST-15-TW75-MASTER-FIELD-CATALOG-R1.json", "tools/stoneage_pet_growth_model.py", "tools/stoneage_pet_detail30_base_panel.py"
    )}
    assert len(ALLOCATIONS) == r["allocation_compositions"] == 286
    assert r["offset_range"] == [-2, 2]
    assert r["panel_order"] == ["max_hp", "attack", "defense", "quick"]
    assert r["internal_order"] == ["vital", "strength", "toughness", "dexterity"]
    rows = s["pet_flag_1_field_projections"]
    assert len(rows) == len(r["rows"]) == len({x["template_id"] for x in rows}) == 467
    assert all(x["pet_flag"] == 1 and x["official_live_pet_release_verified"] is False for x in rows)
    for a, b in zip(rows, r["rows"]):
        expected = project(a)
        if b != expected:
            raise AssertionError((a["template_id"], b, expected))
    groups = defaultdict(list)
    for x in rows:
        groups[x["name"]].append(x)
    dup = []
    for name, v in groups.items():
        if len(v) == 1:
            continue
        dup.append(dict(name=name, template_ids=[x["template_id"] for x in v],
                        distinct_graphics=len({x["graphic"] for x in v}),
                        distinct_birth_coefficients=len({(tuple(x["base"]), x["initnum"], x["lvup_literal"]) for x in v}),
                        distinct_skill_slots=len({tuple(x["skill_slots"]) for x in v}),
                        distinct_elements=len({tuple(x["elements"]) for x in v})))
    assert dup == r["duplicate_groups"]
    exceptions = [dict(template_id=x["template_id"], raw_elements=x["elements"])
                  for x in rows if sum(x["elements"]) != 100]
    assert exceptions == r["element_sum_exceptions"]
    expected_summary = dict(templates=len(rows),
        rank_counts=dict(Counter(str(x["rank"]) for x in r["rows"])),
        duplicate_name_groups=len(dup),
        duplicate_groups_different_graphic=sum(x["distinct_graphics"] > 1 for x in dup),
        duplicate_groups_different_birth_coefficients=sum(x["distinct_birth_coefficients"] > 1 for x in dup),
        duplicate_groups_different_skill_slots=sum(x["distinct_skill_slots"] > 1 for x in dup),
        element_sum_counts=dict(Counter(str(sum(x["elements"])) for x in rows)),
        skill_capacity_exceeded=[x["template_id"] for x in rows if sum(k is not None for k in x["skill_slots"]) > x["skill_slot_capacity"]])
    assert r["summary"] == expected_summary
    print(json.dumps(expected_summary, ensure_ascii=False, sort_keys=True))
    print("467 independent conditional projections matched; no historical official promotion.")

if __name__ == "__main__":
    verify()
