import json
from pathlib import Path
import unittest
from tools.stoneage_jss_pet_manual_contract import derive, report, URL
from tools.stoneage_pet_capture_model import capture_basic_gate

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "research/recovered/STONEAGE-JSS2001-PET-MANUAL-CONTRACT-R1.json"

class ManualContractTests(unittest.TestCase):
    def test_capture_threshold_matches_normal_descendant_gate_only(self):
        data = json.loads(ARCHIVE.read_text())
        gap = data["contracts"]["capture"]["blocked_if_target_level_minus_player_level_at_least"]
        for player in (1, 10, 80):
            for delta in (0, 5, 6, 20):
                allowed, reason = capture_basic_gate(target_is_enemy=True, target_pet_flag=1,
                    attacker_level=player, target_level=player+delta)
                self.assertEqual(allowed, delta < gap)
        self.assertIsNone(data["contracts"]["capture"]["probability_formula"])
        self.assertFalse(data["boundaries"]["jss1999_or_tw10_same_build_proven"])

    def test_source_qualification_rejects_redirect_or_changed_payload(self):
        with self.assertRaisesRegex(ValueError, "URL changed"):
            report(b"a", URL.replace("20010418", "20040418"))
        with self.assertRaisesRegex(ValueError, "bytes changed"):
            report(b"unverified manual", URL)

    def test_source_must_really_contain_every_business_section(self):
        with self.assertRaisesRegex(ValueError, "missing original manual anchor"):
            derive('<a name="3050">[バトル] 一匹のみ</a>')

    def test_unknowns_not_backfilled_from_other_versions_or_sections(self):
        data = json.loads(ARCHIVE.read_text())
        c = data["contracts"]
        self.assertIsNone(c["capture"]["capacity_number"])
        self.assertIsNone(c["capture"]["initial_loyalty_formula"])
        self.assertIsNone(c["release"]["seconds"])
        self.assertIsNone(c["skills"]["slot_count"])
        self.assertIsNone(c["album"]["bitmap_or_species_ids"])
        self.assertFalse(c["album"]["all_encounters_automatically_include_photo"])
        self.assertFalse(c["rename"]["button_uniformity_proven"])
        self.assertEqual(c["rename"]["button_wording"]["6015"], "RIGHT_CLICK_RENAME_BUTTON")
        self.assertIsNone(c["loyalty"]["numeric_deltas_or_formula"])
        self.assertIsNone(c["crafting"]["recipes_item_ids_success_formula"])

if __name__ == "__main__":
    unittest.main()
