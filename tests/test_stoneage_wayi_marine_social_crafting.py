"""Evidence admission and material misinterpretation regression checks."""
import json
from pathlib import Path
import unittest

from tools.stoneage_wayi_marine_social_crafting import (
    ANCHORS, FINAL, REPORT, build, section_fingerprints,
)


class OfficialSourceBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(Path(REPORT).read_text(encoding="utf-8"))

    def test_wrong_host_date_path_and_replay_wrapper_rejected(self):
        for final in (FINAL.replace("www.wayi.com.tw", "example.org"),
                      FINAL.replace("20050614005817", "20060614005817"),
                      FINAL.replace("03.asp", "02.asp"), FINAL.replace("id_/", "/")):
            with self.subTest(final=final), self.assertRaises(ValueError):
                build(b"<html>untrusted</html>", final)

    def test_error_or_rewritten_response_cannot_be_accepted(self):
        for raw in (b"", b"<html>HTTP 403</html>", b"x" * 26642):
            with self.subTest(size=len(raw)), self.assertRaises(ValueError):
                build(raw, FINAL)

    def test_poll_or_footer_cannot_substitute_for_game_sections(self):
        with self.assertRaises(ValueError):
            section_fingerprints(["poll: planned20", "corporate footer"])
        with self.assertRaises(ValueError):
            section_fingerprints(list(ANCHORS) + [ANCHORS[0]])
        with self.assertRaises(ValueError):
            section_fingerprints(list(reversed(ANCHORS)))

    def test_headings_alone_do_not_certify_body(self):
        with self.assertRaises(ValueError):
            section_fingerprints(list(ANCHORS))

    def test_five_classes_twenty_pets_not_a_complete_roster(self):
        f = self.report["marine_fusion"]
        self.assertEqual((f["planned_class_count"], f["planned_pet_count"]), (5, 20))
        self.assertEqual(f["named_classes_in_source_order"], ["水母", "一角鯨", "海蠍", "滄龍"])
        self.assertIsNone(f["missing_class_name"])
        self.assertFalse(f["four_pets_per_class_proven"])
        self.assertFalse(f["actual_release_or_server_execution_proven"])
        self.assertIsNone(f["fusion_recipe_or_inputs"])

    def test_cards_retention_overwrite_and_manual_exchange_are_distinct(self):
        c = self.report["business_cards"]
        self.assertEqual((c["ordinary_capacity_before_described"], c["ordinary_capacity_after_described"], c["additional_dedicated_slot_described"]), (40, 79, 1))
        self.assertEqual(c["end_of_summoning_task"], "DEDICATED_CARDS_DESCRIBED_AS_RETAINED")
        self.assertEqual(c["next_role_assignment"], "DEDICATED_CARDS_DESCRIBED_AS_AUTOMATICALLY_OVERWRITTEN")
        self.assertFalse(c["reexchange_is_automatic_copy_proven"])
        self.assertFalse(c["two_roles_imply_two_extra_slots"])
        self.assertIsNone(c["logout_persistence_or_server_transaction"])

    def test_crafting_description_does_not_fill_recipe_or_chance(self):
        c = self.report["crafting"]
        self.assertEqual([f["label"] for f in c["functions_in_source_order"]], ["強化系統", "鑿孔系統", "新合成裝備", "鑑定系統", "精鍊系統"])
        self.assertFalse(c["armor_20_is_item_id_or_numeric_stat"])
        self.assertFalse(c["identification_label_normalized_to_other_version_rule"])
        self.assertIsNone(c["recipes_item_ids_success_rates_socket_limits_or_costs"])

    def test_source_time_and_baseline_boundaries_remain_explicit(self):
        s, b = self.report["source"], self.report["boundaries"]
        self.assertEqual(s["actual_capture"], "20050614005817")
        self.assertFalse(s["capture_is_publication_or_deployment_date"])
        self.assertFalse(b["jss1999_or_tw10_rule_promoted"])
        self.assertFalse(b["source_html_or_assets_in_git"])
        self.assertEqual(b["stage_b_and_wiki_production"], "GATED")


if __name__ == "__main__":
    unittest.main()
