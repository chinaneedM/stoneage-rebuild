"""Adversarial negative controls for original source/name provenance R31."""
import copy
import json
import unittest

from tools.stoneage_original_named_entity_r31 import ROOT, INPUTS, evaluate, verify

class OriginalNamedEntityR31Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = []
        for p in INPUTS:
            x = (ROOT / p).read_text(encoding="utf-8")
            cls.source.append(json.loads(x) if p.endswith(".json") else x)

    def mutate(self, index, mutate):
        copies = copy.deepcopy(self.source)
        mutate(copies[index])
        with self.assertRaises(ValueError):
            evaluate(*copies)

    def test_replay_real_five_pinned_inputs(self):
        self.assertEqual(evaluate(*self.source)["inventory"]["declared_files"], 557)

    def test_exact_pins_and_report_match(self):
        self.assertEqual(verify()["sample"]["matched_original_RD_sha256_count"], 8)

    def test_reject_changed_original_rd_block(self):
        self.mutate(2, lambda x: x["frames"][0].__setitem__("source_RD_sha256", "0" * 64))

    def test_reject_changed_original_adrn_record(self):
        self.mutate(2, lambda x: x["frames"][0].__setitem__("source_record_sha256", "0" * 64))

    def test_reject_wrong_original_sprite_group(self):
        self.mutate(1, lambda x: x["sample"].__setitem__("original_spr_no", 777777))

    def test_reject_unsupported_original_species_identity(self):
        self.mutate(2, lambda x: x.__setitem__("named_pet_or_avatar_verified", True))

    def test_reject_unproven_clean_official_build_promotion(self):
        self.mutate(0, lambda x: x.__setitem__("official_clean_client_authenticated", True))

    def test_reject_missing_inventory_file(self):
        self.mutate(0, lambda x: x["inspection"]["inventory"]["samples"][0]["files"].pop())

    def test_reject_new_named_master_filename(self):
        self.mutate(0, lambda x: x["inspection"]["inventory"]["samples"][0]["files"][0].__setitem__("path", "data/PetMaster.dat"))

    def test_reject_history_promoted_to_original_pet_master(self):
        self.mutate(3, lambda x: x["identity_fields"].__setitem__("original_pet_master_id", 123))

    def test_reject_taiwan_v1_range_fabrication(self):
        changed = list(self.source)
        changed[4] = changed[4].replace("METRIC|adrn_records|125996", "METRIC|adrn_records|303047")
        with self.assertRaises(ValueError):
            evaluate(*changed)

if __name__ == "__main__":
    unittest.main()
