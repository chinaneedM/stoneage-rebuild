"""PET-DETAIL29: C-compiled descendant-PC birth/growth arithmetic regression."""

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_pet_growth_model import (
    RANK_ROLL_RANGES,
    advance_pet_growth,
    pack_growth_base,
    pet_level_increments,
    project_pet_birth,
    unpack_growth_base,
)

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "research/pets/PET-DETAIL-EVIDENCE29-PC-GROWTH-SOURCE-FLOAT32-R1.json"

# Independently built C arithmetic oracle; no protected original source embedded.
C_ORACLE = r"""
#include <stdio.h>
int main(void) {
    int base, points, rank_roll;
    while (scanf("%d %d %d", &base, &points, &rank_roll) == 3) {
        float fRand = (float)rank_roll * 0.01;
        float vital = (float)base;
        float Param = (float)points;
        vital = (float)vital * fRand + Param * fRand;
        printf("%d\n", (int)vital);
    }
    return 0;
}
"""


class PetDetail29SourceFloatTests(unittest.TestCase):
    def test_birth_separates_template_rank_growth_identity_and_spawn_points(self):
        b = project_pet_birth(
            template_base=(20, 12, 15, 25),
            init_num=10,
            lvup_point=2,
            level=1,
            offsets=(-2, 1, 2, 0),
            birth_rolls=(0, 0, 0, 1, 1, 2, 2, 3, 3, 3),
        )
        self.assertEqual(b.rank, 5)  # original sum 72, not individualized 73
        self.assertEqual(b.individualized_growth_base, (18, 13, 17, 25))
        self.assertEqual(b.packed_alloc_point, pack_growth_base(18, 13, 17, 25))
        self.assertEqual(unpack_growth_base(b.packed_alloc_point), (18, 13, 17, 25))
        self.assertEqual(b.birth_allocation_counts, (3, 2, 2, 3))
        self.assertEqual(b.internal_stats, (210, 150, 190, 280))

        higher = project_pet_birth(
            template_base=(20, 12, 15, 25),
            init_num=10,
            lvup_point=2,
            level=5,
            offsets=(-2, 1, 2, 0),
            birth_rolls=(0, 0, 0, 1, 1, 2, 2, 3, 3, 3),
        )
        self.assertEqual(higher.internal_stats, (378, 270, 342, 504))
        self.assertEqual(higher.packed_alloc_point, b.packed_alloc_point)

    def test_birth_input_guards(self):
        common = dict(template_base=(20, 12, 15, 25), init_num=10,
                      lvup_point=2, level=1, offsets=(0, 0, 0, 0),
                      birth_rolls=(0,) * 10)
        for change in (
            dict(template_base=(20, 15, 25)),
            dict(template_base=(256, 1, 1, 1)),
            dict(level=0), dict(init_num=-1), dict(lvup_point=-1),
            dict(offsets=(3, 0, 0, 0)),
            dict(birth_rolls=(0,) * 9),
        ):
            with self.subTest(change=change), self.assertRaises(ValueError):
                project_pet_birth(**dict(common, **change))

    def test_source_float32_not_idealized_binary64_on_integer_boundaries(self):
        cases = ((17, 3, 470, 1, 93, 94),
                 (20, 5, 472, 1, 117, 118),
                 (22, 3, 508, 1, 126, 127),
                 (20, 0, 500, 0, 100, 100))
        for base, points, roll, rank, source_expected, old_expected in cases:
            with self.subTest(base=base, points=points, roll=roll):
                allocation = (0,) * points + (1,) * (10-points)
                actual = pet_level_increments((base, 0, 0, 0), rank,
                                              allocation, roll)[0]
                self.assertEqual(actual, source_expected)
                self.assertEqual(int((base + points) * (roll * .01)), old_expected)

    def test_full_byte_allocation_roll_corpus_has_documented_old_model_mismatch(self):
        # 256 stored growth bases × 11 allocated points × 151 legal roll values.
        mismatch = 0
        total = 0
        from tools.stoneage_pet_growth_model import _source_float32
        for roll in range(450, 601):
            factor = _source_float32(roll * .01)
            for base in range(256):
                left = _source_float32(base * factor)
                for count in range(11):
                    actual = int(_source_float32(
                        left + _source_float32(count * factor)))
                    old = int((base + count) * (roll * .01))
                    mismatch += (actual != old)
                    total += 1
        self.assertEqual((total, mismatch), (425216, 1636))

    def test_compiled_c_source_expression_parity_all_rank_bands(self):
        if not shutil.which("gcc"):
            self.skipTest("gcc absent; CI Ubuntu gcc acceptance still required")
        vectors = [(17, 3, 470, 1), (20, 5, 472, 1),
                   (22, 3, 508, 1), (20, 0, 500, 0)]
        for rank, (lo, hi) in enumerate(RANK_ROLL_RANGES):
            for n in range(200):
                vectors.append(((n * 37 + rank * 11) % 256,
                                (n * 7 + rank) % 11,
                                lo + (n * 13) % (hi - lo + 1), rank))
        with tempfile.TemporaryDirectory() as tmp:
            cfile = Path(tmp) / "check.c"
            binfile = Path(tmp) / "check"
            cfile.write_text(C_ORACLE, encoding="utf-8")
            subprocess.run(["gcc", "-std=c11", "-O0",
                            "-fexcess-precision=standard", str(cfile),
                            "-o", str(binfile)], check=True,
                           capture_output=True, text=True)
            inp = "".join(f"{base} {points} {roll}\n"
                          for base, points, roll, rank in vectors)
            proc = subprocess.run([str(binfile)], input=inp,
                                  capture_output=True, text=True, check=True)
        got = [int(x) for x in proc.stdout.splitlines()]
        self.assertEqual(len(got), len(vectors))
        for (base, points, roll, rank), expected in zip(vectors, got):
            allocation = (0,) * points + (1,) * (10-points)
            actual = pet_level_increments((base, 0, 0, 0), rank,
                                          allocation, roll)[0]
            self.assertEqual(actual, expected, (base, points, roll, rank))

    def test_provenance_ledger_and_early_official_nonsubstitution(self):
        evidence = json.loads(LEDGER.read_text(encoding="utf-8"))
        self.assertEqual(len(evidence["source_code_snapshots"]), 4)
        self.assertEqual(evidence["arithmetic_corpus"]["total_combinations"], 425216)
        self.assertEqual(evidence["arithmetic_corpus"]["old_model_mismatches"], 1636)
        self.assertEqual(evidence["historical_qualification"],
                         "DESCENDANT_PC_SOURCE_ONLY_NOT_EARLY_OFFICIAL")
        p = json.loads((ROOT / "research/pets/profiles/TW10-G100289.json")
                       .read_text(encoding="utf-8"))
        self.assertIsNone(p["combat_stats"]["level_1"]["values"]["derived_hp"])
        self.assertIsNone(p["growth"]["stat_growth_formula"])
        self.assertFalse(p["actual_official_pet_identity"]["official_living_pet_release_proven"])


if __name__ == "__main__":
    unittest.main()
