"""PET19 independent replay of source skill-gap receipt from archived original-derived inputs."""
import json
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "research/recovered"
sys.path.insert(0, str(ROOT / "tools"))
from stoneage_pet16_lookup import skill_gap_trace


def read(name):
    return json.loads((R / name).read_text(encoding="utf-8"))


class Pet19Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = read("STONEAGE-PET-MODULE-19-MISSING-SKILL-SOURCE-GAP-AUDIT-R1.json")
        cls.c = read("STONEAGE-PET-MODULE-16-SOURCE-SEPARATED-UNIFIED-CATALOG-R1.json")
        cls.p03 = read("STONEAGE-PET-MODULE-03-SAME-SOURCE-SKILL-JOIN-R1.json")
        cls.p10 = read("STONEAGE-PET-MODULE-10-ORIGINAL-MIXED25-SERVER-TABLES-R1.json")

    def test_later2016_every_absent_positive_skill_replayed_exactly(self):
        defs = {x[1]: x for x in self.p03["skill_definition_rows"]}
        missing, positive, defined, negative = [], 0, 0, 0
        for row in self.c["datasets"]["later2016_templates"]:
            for slot, v in enumerate(row["skill_source_slots"], 1):
                if v is None:
                    continue
                sid = v[0]
                if sid < 0:
                    negative += 1
                elif sid > 0:
                    positive += 1
                    if sid in defs:
                        self.assertEqual(v[1:], defs[sid][::2])
                        defined += 1
                    else:
                        self.assertEqual(v[1:], [None, None])
                        missing.append((row["original_row"], row["template_id"], slot, sid))
        self.assertEqual((positive, defined, negative), (2886, 2784, 20))
        self.assertEqual(Counter(missing), Counter(map(tuple, self.p03["unmatched_positive_slots"])))
        actual = [
            (x["original_row"], x["template_id"], x["slot_1based"], g["skill_id"])
            for g in self.a["missing_by_source"]["later2016_configured_selected_active"]
            for x in g["original_references"]
        ]
        self.assertEqual(Counter(actual), Counter(missing))
        self.assertEqual(len(actual), 102)
        self.assertEqual(len(set(x[3] for x in actual)), 30)
        self.assertEqual(len(set(x[0] for x in actual)), 76)

    def test_fallback_source_is_same_commit_but_not_selected_or_a_fix(self):
        ref = self.a["source_refs"]["later2016_fallback_skill_id_only"]
        self.assertEqual(ref["git_blob"], self.p03["source"]["conditional_fallback_skill"]["blob"])
        self.assertEqual(ref["source_commit"], self.p03["source"]["commit"])
        self.assertEqual(ref["source_id_column_0based"], 4)
        self.assertEqual(len(ref["derived_ids_sorted"]), 56)
        self.assertEqual(len(set(ref["derived_ids_sorted"])), 56)
        absent = {g["skill_id"]
                  for g in self.a["missing_by_source"]["later2016_configured_selected_active"]}
        self.assertFalse(absent.intersection(ref["derived_ids_sorted"]))
        self.assertEqual(self.a["source_refs"]["later2016_skill_join"]["selector"], "petskillfile2")
        self.assertFalse(self.p03["evidence_limits"]["source_binary_built_or_executed"])

    def test_mixed25_missing_alt_skill_is_in_other_not_active_table(self):
        alt_defs = {x[1] for x in self.p10["source_rows"]["petskill1.txt"]}
        main_defs = {x[1]: x for x in self.p10["source_rows"]["petskill.txt"]}
        byrow = {x[0]: x for x in self.p10["source_rows"]["enemybase2.txt"]}
        derived = []
        pos = defined = 0
        for row in self.c["datasets"]["mixed25_alternative"]:
            old = byrow[row["original_row"]]
            self.assertEqual((old[1], old[2], old[3], old[16]),
                             (row["template_id"], row["graphic_number"],
                              1, row["original_fields_sha256"]))
            this_missing = 0
            for slot, sid in enumerate(row["original_skill_slot_ids"], 1):
                if sid is None or sid <= 0:
                    continue
                pos += 1
                if sid in alt_defs:
                    defined += 1
                else:
                    this_missing += 1
                    derived.append((row["original_row"], row["template_id"], slot, sid))
            self.assertEqual(this_missing, row["unresolved_positive_skill_slots"])
        self.assertEqual((pos, defined, len(derived)), (661, 649, 12))
        from_receipt = []
        for group in self.a["missing_by_source"]["mixed25_alternative_paired_not_proven_active"]:
            for x in group["original_references"]:
                sid = group["skill_id"]
                from_receipt.append((x["original_row"], x["template_id"],
                                     x["slot_1based"], sid))
                self.assertNotIn(sid, alt_defs)
                self.assertIn(sid, main_defs)
                self.assertEqual(
                    [x["primary_other_table_numeric_candidate"]["original_skill_row"],
                     x["primary_other_table_numeric_candidate"]["original_skill_row_sha256"]],
                    [main_defs[sid][0], main_defs[sid][2]])
                self.assertEqual(x["original_fields_sha256"],
                                 byrow[x["original_row"]][16])
        self.assertEqual(Counter(from_receipt), Counter(derived))
        self.assertEqual({x[3] for x in derived}, {503, 541, 542, 580, 600})

    def test_main_skill_table_keeps_existing_full_coverage(self):
        ids = {x[1] for x in self.p10["source_rows"]["petskill.txt"]}
        observed = [sid for row in self.c["datasets"]["mixed25_main"]
                    for sid in row["original_skill_slot_ids"] if sid is not None and sid > 0]
        self.assertEqual(len(observed), 1050)
        self.assertTrue(all(sid in ids for sid in observed))
        self.assertEqual(self.a["totals"]["mixed25_primary"]["undefined_in_own_primary_skill_table"], 0)

    def test_lookup_keeps_source_separate_and_limit_changes_no_totals(self):
        g = skill_gap_trace(self.a, 114, limit=1)
        first = g["missing_by_source"]["later2016_configured_selected_active"][0]
        self.assertEqual((first["skill_id"], first["reference_count"],
                          first["returned_references"], first["truncated"]),
                         (114, 18, 1, True))
        self.assertEqual(g["missing_by_source"]["mixed25_alternative_paired_not_proven_active"], [])
        self.assertEqual(g["totals_all_skills_not_filtered"]["later2016"]["missing_in_selected_petskill2"], 102)
        other = skill_gap_trace(self.a, 503)
        self.assertEqual(other["missing_by_source"]["later2016_configured_selected_active"], [])
        self.assertEqual(other["missing_by_source"]["mixed25_alternative_paired_not_proven_active"][0]["reference_count"], 4)
        self.assertEqual(skill_gap_trace(self.a, 999999)["missing_by_source"], {
            "later2016_configured_selected_active": [],
            "mixed25_alternative_paired_not_proven_active": [],
        })

    def test_no_runtime_or_identity_upgrade_and_unknown_negative(self):
        self.assertTrue(all(self.a["evidence_guards"].values()))
        self.assertEqual(self.a["active_module"], "PET")
        self.assertEqual(self.a["preserved_historical_current_blob"],
                         "c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertTrue(skill_gap_trace(self.a)["no_original_pet_skill_effect_or_early_official_identity_verified"])
        for bad in (0, -1, True, "503", None):
            if bad is None:
                continue
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                skill_gap_trace(self.a, bad)
        with self.assertRaises(ValueError):
            skill_gap_trace(self.a, 114, limit=0)


if __name__ == "__main__":
    unittest.main()
