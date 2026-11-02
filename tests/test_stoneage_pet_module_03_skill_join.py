"""Schema and conservation checks for the published derived PET-MODULE-03 index.
The proprietary original pet/skill text is not bundled in this repository.
"""
import json
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "research/recovered/STONEAGE-PET-MODULE-01-BATCH-SOURCE-SPR-INDEX-R1.json"
REPORT = ROOT / "research/recovered/STONEAGE-PET-MODULE-03-SAME-SOURCE-SKILL-JOIN-R1.json"


def validate(batch, report):
    assert report["schema"] == "stoneage.pet_module_03_same_2016_server_pet_template_skill_coverage.r1"
    assert report["evidence_limits"]["official_JSS1999_or_TW10_or_CN182_pet_skills_authenticated"] is False
    assert report["evidence_limits"]["source_skill_callbacks_executed"] is False
    assert report["evidence_limits"]["overall_restoration_percent"] is None
    defs = report["skill_definition_rows"]
    assert len(defs) == 282 and len({r[1] for r in defs}) == 282
    id_to_line = {ident: line for line, ident, callback in defs}
    assert all(callback.startswith("PETSKILL_") for _, _, callback in defs)
    expected_refs = Counter()
    expected_missing = []
    expected_neg = []
    coverage = []
    for row in batch["petflag1_template_tuples"]:
        line, template_id, graphic = row[:3]
        slots = row[14]
        assert len(slots) == 7
        positive = matched = missing = negatives = empty = 0
        for n, value in enumerate(slots, 1):
            if value is None:
                empty += 1
            elif value < 0:
                negatives += 1
                expected_neg.append([line, template_id, n, value])
            else:
                assert value > 0
                positive += 1
                expected_refs[value] += 1
                if value in id_to_line:
                    matched += 1
                else:
                    missing += 1
                    expected_missing.append([line, template_id, n, value])
        coverage.append([line, template_id, graphic, positive, matched, missing, negatives, empty])
    assert coverage == report["source_template_rows"]
    assert expected_missing == report["unmatched_positive_slots"]
    assert expected_neg == report["negative_literal_slots"]
    refs = [[ident, count, id_to_line.get(ident)] for ident, count in sorted(expected_refs.items())]
    assert refs == report["reference_ids"]
    c = report["counts"]
    assert len(coverage) == c["source_template_petflag1_rows"] == 1024
    assert len({r[1] for r in coverage}) == c["source_template_petflag1_distinct_id"] == 1021
    assert c["skill_definitions_active_table"] == 282
    assert c["skill_definitions_fallback_table"] == 56
    assert c["distinct_positive_skill_ids_referenced"] == len(refs) == 190
    assert c["referenced_skill_ids_defined_active"] == sum(r[2] is not None for r in refs) == 160
    assert c["referenced_skill_ids_absent_active"] == sum(r[2] is None for r in refs) == 30
    assert c["positive_skill_slot_occurrences"] == sum(expected_refs.values()) == 2886
    assert c["positive_skill_slots_defined_active"] == sum(count for ident, count in expected_refs.items() if ident in id_to_line) == 2784
    assert c["positive_skill_slots_absent_active"] == len(expected_missing) == 102
    assert c["nonpositive_negative_slot_occurrences"] == len(expected_neg) == 20
    assert c["null_slot_occurrences"] == sum(r[-1] for r in coverage) == 4262
    assert c["template_rows_with_positive_skills"] == sum(r[3] > 0 for r in coverage)
    assert c["template_rows_with_any_unmatched_positive_skills"] == sum(r[5] > 0 for r in coverage)
    assert c["distinct_defined_active_skill_ids_unreferenced_by_petflag1_templates"] == len(id_to_line.keys() - expected_refs.keys())
    assert c["positive_skill_slot_occurrences"] + c["nonpositive_negative_slot_occurrences"] + c["null_slot_occurrences"] == 1024 * 7


class PetModule03EvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.batch = json.loads(BATCH.read_text(encoding="utf-8"))
        cls.report = json.loads(REPORT.read_text(encoding="utf-8"))

    def test_batch_consistency(self):
        validate(self.batch, self.report)

    def test_denial_of_official_promotion(self):
        from copy import deepcopy
        changed = deepcopy(self.report)
        changed["evidence_limits"]["official_JSS1999_or_TW10_or_CN182_pet_skills_authenticated"] = True
        with self.assertRaises(AssertionError):
            validate(self.batch, changed)

    def test_missing_slot_cannot_be_silently_dropped(self):
        from copy import deepcopy
        changed = deepcopy(self.report)
        changed["unmatched_positive_slots"].pop()
        with self.assertRaises(AssertionError):
            validate(self.batch, changed)


if __name__ == "__main__":
    unittest.main()
