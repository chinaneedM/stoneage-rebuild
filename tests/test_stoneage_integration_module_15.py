"""Verify exact source-bound Hotoru 1303 pet-service joins (public metadata only)."""
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
def load(name):
    return json.loads((ROOT / "research" / "recovered" / name).read_text(encoding="utf-8"))

class Integration15SourceBridgeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bridge = load("STONEAGE-INTEGRATION15-HOTORU-PET-SERVICE-BRIDGE-R1.json")
        cls.rooms = load("STONEAGE-INTEGRATION13-HOTORU-FIVE-ROOMS-SOURCE-R1.json")
        cls.skills = load("STONEAGE-GAMEPLAY03-ORIGINAL-21-PET-SKILL-SHOP-SOURCE-R1.json")
        cls.petshop = load("STONEAGE-GAMEPLAY05-ORIGINAL-PETSHOP-SAVEPOINT-HEAL-SOURCE-R1.json")
        cls.room = cls.rooms["rooms"]["1303"]

    def test_room_same_source_coordinates_and_canvas(self):
        r = self.bridge["room"]
        self.assertEqual(r["floor"], 1303)
        self.assertEqual(r["original_name"], self.room["original_name"])
        self.assertEqual(r["original_dat_sha256"], self.room["dat"]["sha256"])
        self.assertEqual(r["original_ls2map_sha256"], self.room["server_map"]["sha256"])
        self.assertEqual(r["map07_private_canvas_png_sha256"], self.room["map07_canvas"]["png_sha256"])
        self.assertEqual(r["map07_private_canvas_rgba_sha256"], self.room["map07_canvas"]["rgba_sha256"])
        self.assertEqual(r["source_create_count"], len(self.room["source_create"]))
        self.assertEqual(len(self.room["source_create"]), 11)

    def test_pet_shop_source_sha_and_absent_fields(self):
        row = self.bridge["service_joins"][0]
        cr = next(x for x in self.room["source_create"] if x["ordinal"] == row["create_ordinal"] and x["path"] == row["create_path"])
        upstream = next(x for x in self.petshop["original_CREATE_refs_and_derived_numeric_fields"] if x["create_ordinal"] == row["create_ordinal"] and x["create_path"] == row["create_path"])
        self.assertEqual(row["catalog_role"], "pet_storage_configuration")
        self.assertEqual((row["create_ordinal"], row["xy"], row["graphic_alias"]), (53, [16, 13], 16048))
        self.assertEqual(row["function_token"], cr["functionset"])
        self.assertEqual(row["create_block_sha256"], cr["block_sha256"])
        self.assertEqual(row["create_block_sha256"], upstream["create_block_sha256"])
        self.assertEqual(row["original_parameter_path"], cr["parameters"][0]["path"])
        self.assertEqual(row["original_parameter_path"], upstream["source_parameter_path"])
        self.assertEqual(row["original_parameter_sha256"], cr["parameters"][0]["sha256"])
        self.assertEqual(row["original_parameter_sha256"], upstream["source_parameter_sha256"])
        self.assertEqual(row["parameter_literals"], upstream["source_fields"])
        self.assertIsNone(row["parameter_literals"]["pool_flg_raw"])
        self.assertIsNone(row["parameter_literals"]["pool_cost_raw"])
        self.assertTrue(row["parameter_literals"]["special_pet_source_is_empty"])

    def test_skill_shop_exact_order_and_both_candidate_masters(self):
        row = self.bridge["service_joins"][1]
        cr = next(x for x in self.room["source_create"] if x["ordinal"] == row["create_ordinal"] and x["path"] == row["create_path"])
        upstream = next(x for x in self.skills["original_skillshop_CREATE_to_parameter_rows"] if x["create_ordinal"] == row["create_ordinal"] and x["create_file"] == row["create_path"])
        self.assertEqual(row["catalog_role"], "pet_skill_course_configuration")
        self.assertEqual((row["create_ordinal"], row["xy"], row["graphic_alias"]), (54, [13, 13], 16049))
        self.assertEqual(row["function_token"], cr["functionset"])
        self.assertEqual(row["create_block_sha256"], cr["block_sha256"])
        self.assertEqual(row["create_block_sha256"], upstream["create_block_sha256"])
        self.assertEqual(row["original_parameter_path"], cr["parameters"][0]["path"])
        self.assertEqual(row["original_parameter_path"], upstream["parameter_path"])
        self.assertEqual(row["original_parameter_sha256"], cr["parameters"][0]["sha256"])
        self.assertEqual(row["original_parameter_sha256"], upstream["source_original_sha256"])
        self.assertEqual(row["skill_rate_literal"], upstream["source_skill_rate_literal"])
        self.assertEqual(row["skill_rate_literal"], "1.1")
        self.assertEqual(row["skill_ids_ordered"], upstream["source_pet_skill_ids_ordered"])
        self.assertEqual(row["skill_ids_ordered"], [0, 1, 2, 3, 50, 61, 130])
        self.assertFalse(row["skill_trailing_empty_token"])
        for sid in row["skill_ids_ordered"]:
            matching = [x for x in self.skills["source_skill_id_master_presence_candidates"] if x["skill_id"] == sid]
            self.assertEqual(len(matching), 1)
            self.assertTrue(matching[0]["primary_petskill_txt"]["row_sha256"])
            self.assertTrue(matching[0]["alternative_petskill1_txt"]["row_sha256"])

    def test_co_room_same_graphic_does_not_merge_npc(self):
        constraints = self.bridge["co_room_constraints"]
        town = constraints["townpeople"]
        cr = next(x for x in self.room["source_create"] if x["ordinal"] == town["create_ordinal"])
        self.assertEqual(town["create_ordinal"], 61)
        self.assertEqual(town["xy"], [11, 6])
        self.assertEqual(town["create_block_sha256"], cr["block_sha256"])
        self.assertEqual(town["original_parameter_sha256"], cr["parameters"][0]["sha256"])
        self.assertEqual(town["original_parameter_path"], cr["parameters"][0]["path"])
        self.assertEqual(town["graphic_alias"], self.bridge["service_joins"][1]["graphic_alias"])
        self.assertNotEqual(town["create_block_sha256"], self.bridge["service_joins"][1]["create_block_sha256"])
        self.assertTrue(constraints["pet_skill_and_townpeople_share_graphic_alias_only"])
        self.assertTrue(constraints["distinct_create_blocks_and_positions"])
        self.assertEqual(constraints["unnamed_mugon_configurations"], sum(x["enemy_template"] == "npcgen_mugon" for x in self.room["source_create"]))
        self.assertEqual(constraints["warp_source_create_ordinals"], [x["ordinal"] for x in self.room["source_create"] if x["functionset"] == "Warp"])
        self.assertEqual({x["target"][0] for x in self.room["source_create"] if x["functionset"] == "Warp"}, {1300})

    def test_no_unverified_native_or_private_renderer_claims(self):
        bounds = self.bridge["boundaries"]
        self.assertEqual(set(bounds.values()), {False, 0})
        self.assertEqual(bounds["new_original_pixel_decodes"], 0)
        self.assertFalse(bounds["private_observer_html_modified"])
        self.assertFalse(bounds["original_game_interaction_verified"])
        self.assertFalse(bounds["official_same_deployment_verified"])
        self.assertNotEqual(self.bridge["source_scope"], "OFFICIAL_SAME_DEPLOYMENT")

if __name__ == "__main__":
    unittest.main()
