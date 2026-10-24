"""Negative evidence-promotion regressions for original named-entity joins."""
import copy
import json
import unittest
from tools import stoneage_client_named_entity_primary_source_gate as gate

class Gate(unittest.TestCase):
    def test_pins_and_real_rows(self):
        self.assertTrue(gate.verify())

    def test_invalid_evidence_promotions(self):
        original = json.loads(gate.REPORT.read_text(encoding="utf-8"))
        for index in range(8):
            mutated = copy.deepcopy(original)
            if index == 0: mutated["result"]["confirmed_original_named_entity_to_bitmap_or_animation_id_pairs"] = 1
            if index == 1: mutated["result"]["tw10_cn50_same_original_physical_bitmap_candidates"] = 100
            if index == 2: mutated["result"]["tw10_same_build_authenticated_npc_names"] = 101
            if index == 3: mutated["result"]["jss2001_or_tw10_same_build_proven"] = True
            if index == 4: mutated["result"]["korea_2000_complete_installer_acquired_by_evidence_sources"] = True
            if index == 5: mutated["source_pins"][0]["git_blob_sha"] = "0"*40
            if index == 6: mutated["named_original_client_acquisition_leads"][0]["downloaded_and_hashed"] = True
            if index == 7: mutated["result"]["overall_restoration_percent"] = 100
            with self.subTest(index=index), self.assertRaises(AssertionError):
                gate.verify(mutated)

if __name__ == "__main__":
    unittest.main()
