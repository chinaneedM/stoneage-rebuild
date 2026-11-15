import json
import unittest
from pathlib import Path

from tools.stoneage_jss1999_pet_source_census import SHA


class Pet31PublishedEvidence(unittest.TestCase):
    def test_all_1999_dates_bounded(self):
        d = json.loads(Path("research/recovered/STONEAGE-PET31-JSS1999-ALL-CLAUSE-CENSUS-R1.json").read_text())
        old = json.loads(Path("research/recovered/STONEAGE-JSS-PET-PATCH-HISTORY-R1.json").read_text())
        self.assertEqual(d["source"]["sha256"], SHA)
        self.assertEqual(d["source"]["sha256"], old["source"]["sha256"])
        rows = d["dated_rows_1999"]
        self.assertEqual(len(rows), 15)
        self.assertEqual(sum(r["clause_count"] for r in rows), 65)
        self.assertEqual(sorted(r["original_source_order"] for r in rows), list(range(25, 40)))
        self.assertEqual(d["lexical_hit_clause_counts"]["PET"], 7)
        self.assertEqual(d["lexical_hit_clause_counts"]["PET_MAIL"], 5)
        self.assertEqual(d["lexical_hit_clause_counts"]["URIURI_LITERAL"], 1)
        for r in rows:
            self.assertEqual(r["entry_body_sha256"], old["dated_index"][r["original_source_order"]]["body_fingerprint"]["sha256"])
        self.assertFalse(d["year_1999_source_bounded_reviewed"])
        self.assertFalse(d["negative_non_matches_prove_no_pets"])
        self.assertEqual(d["new_official_species_records"], [])
        self.assertTrue(all(not c["official_obtainable_pet_record_proven"] for r in rows for c in r["clauses"]))


if __name__ == "__main__":
    unittest.main()
