"""O75 bounded derived-source guards; original commercial files remain private."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "research/recovered/STONEAGE-O75-ORIGINAL-COOKING-CRAFTING-NPC-SOURCE-R1.json"


class O75TeacherChefSourceBoundTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_real_source_identity_and_actor_bindings(self):
        r = self.r
        self.assertEqual(r["source_archive"]["bytes"], 361255180)
        self.assertTrue(r["source_archive"]["full_sha_verified_this_unit"])
        self.assertEqual(len(r["actual_extracted_source_files"]), 9)
        for source in r["actual_extracted_source_files"].values():
            self.assertTrue(source["full_extraction_and_original_member_crc_agree"])
            self.assertTrue(source["cp950_roundtrip"])
            self.assertEqual(len(source["sha256"]), 64)
        actors = r["original_NPC_spawn_from_menu_create"]
        self.assertEqual(len(actors), 6)
        self.assertEqual(
            [(x["kind"], x["floor"], x["xy"], x["graphic_alias"]) for x in actors],
            [("chef", 2009, [25, 41], 16053), ("chef", 3009, [25, 43], 16053),
             ("craft_teacher", 1009, [25, 30], 16209), ("craft_teacher", 4009, [25, 30], 16209),
             ("cook_teacher", 2009, [13, 14], 16066), ("cook_teacher", 3009, [13, 14], 16066)])
        self.assertEqual(
            {k: len(v["window_ids"]) for k, v in r["source_dialogue_window_graphs"].items()},
            {"cook": 10, "craft": 8, "chef2009": 5, "chef3009": 4})
        self.assertTrue(all(v["all_reachable_from_1"] for v in r["source_dialogue_window_graphs"].values()))

    def test_no_fabricated_recipes_or_item_quantities(self):
        r = self.r
        dishes = r["chef_menu_to_itemset"]
        self.assertEqual(len(dishes), 6)
        self.assertEqual([x["item_id"] for x in dishes if x["exact_unique_itemset_name"]],
                         [12607, 12780, 12754])
        self.assertTrue(all(x["item_id"] is None and x["same_entity_proven"] is False for x in dishes[:3]))
        self.assertTrue(all(x["item_type"] == 20 and len(x["full_source_row_sha256"]) == 64 for x in dishes[3:]))
        self.assertEqual([x["item_usefunc"] for x in dishes[3:]],
                         ["ITEM_useStatusChange", "ITEM_useRecovery", "ITEM_useRecovery"])
        self.assertTrue(r["itemset_ingvalue_is_not_menu_quantity_or_proven_success_percentage"])
        self.assertTrue(r["source_menu_conf_exists_but_unreferenced_by_these_two_chefs"])
        self.assertTrue(r["craft_teacher_describes"]["actual_formula_and_success_rate_not_proven"])

    def test_original_sprite_byte_evidence_and_executability_boundaries(self):
        r = self.r
        arts = r["original_TW10_graphic_sources"]["sprites"]
        self.assertEqual({k: v["dimensions"] for k, v in arts.items()},
                         {"16053": [56, 90], "16066": [28, 78], "16209": [36, 84]})
        self.assertTrue(all(v["two_decoders_agree"] and len(v["original_RD_sha256"]) == 64 for v in arts.values()))
        z = r["private_observation"]
        self.assertEqual((z["bytes"], z["members"]), (37761, 7))
        self.assertTrue(z["zip_member_crc_pass"])
        self.assertTrue(z["contained_private_html_source_window_index"])
        self.assertTrue(z["not_original_client_interaction"])
        for key in ("native_client_executed", "native_server_executed", "original_NPC_window_clicked",
                    "original_cook_or_craft_executed", "actual_item_effect_executed",
                    "actual_original_same_build_deployment_confirmed", "earliest_JSS1999_or_TW10_gameplay_confirmed"):
            self.assertIs(r["limits"][key], False)
        self.assertIsNone(r["limits"]["overall_percent"])
        self.assertEqual(r["limits"]["R79"], "PAUSED_NON_BLOCKING")


if __name__ == "__main__":
    unittest.main()
