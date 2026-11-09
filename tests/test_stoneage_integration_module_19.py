"""INTEGRATION19: source-backed service joins, asymmetric directions, and evidence limits."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/recovered/STONEAGE-INTEGRATION19-THREE-PET-SERVICES-SOURCE-R1.json"


def git_blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


class OriginalThreePetServiceSourceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(REPORT.read_bytes())
        cls.source = {}
        for key, pin in cls.report["upstream_git_blobs"].items():
            raw = (ROOT / pin["path"]).read_bytes()
            assert git_blob(raw) == pin["git_blob"], key + " original derived source changed"
            cls.source[key] = json.loads(raw)
        cls.creates = {(row[0], row[1]): row for row in cls.source["char01"]["create_rows"]}

    def test_three_qualified_source_rooms_have_no_invented_private_canvas(self):
        r = self.report
        self.assertEqual(r["baseline"]["CURRENT_git_blob"], "c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual(r["baseline"]["CURRENT_bytes"], 2709173)
        self.assertEqual([room["floor"] for room in r["rooms"]], [3303, 3403, 4003])
        for room in r["rooms"]:
            floor = room["floor"]
            source = self.source["maps"]["maps"][str(floor)]
            self.assertEqual(room["dat"]["sha256"], source["source_sha256"])
            self.assertEqual(room["dat"]["bytes"], source["source_bytes"])
            self.assertEqual(room["dat"]["geometry"], [30, 30])
            self.assertEqual(room["dat"]["canvas_size"], [1889, 1425])
            self.assertEqual(room["dat"]["combined_RGBA_sha256"], source["frame_RGBA_sha256"]["combined"])
            self.assertIs(room["actual_DAT_and_full_PNG_replayed_in_private_this_unit"], floor == 4003)
        self.assertNotIn("3400", self.source["maps"]["maps"])

    def test_six_original_create_and_parameter_refs_stay_distinct(self):
        for room in self.report["rooms"]:
            floor = room["floor"]
            pet, trainer = room["services"]
            self.assertEqual([pet["role"], trainer["role"]], ["PetShop", "PetSkillShop"])
            original_pet = next(x for x in self.source["shops"]["original_CREATE_refs_and_derived_numeric_fields"]
                                if x["floorid"] == floor and x["source_function"] == "npcgen_petshop")
            original_trainer = next(x for x in self.source["skills"]["original_skillshop_CREATE_to_parameter_rows"]
                                    if x["source_floorid"] == floor)
            self.assertEqual((pet["create_file"], pet["create_ordinal"], pet["create_sha256"],
                              pet["graphic"], pet["parameter_path"], pet["parameter_sha256"], pet["original_fields"]),
                             (original_pet["create_path"], original_pet["create_ordinal"],
                              original_pet["create_block_sha256"], original_pet["graphicname"],
                              original_pet["source_parameter_path"], original_pet["source_parameter_sha256"],
                              original_pet["source_fields"]))
            self.assertEqual((trainer["create_file"], trainer["create_ordinal"], trainer["create_sha256"],
                              trainer["graphic"], trainer["parameter_path"], trainer["parameter_sha256"],
                              trainer["skill_rate"], trainer["skill_ids"]),
                             (original_trainer["create_file"], original_trainer["create_ordinal"],
                              original_trainer["create_block_sha256"], original_trainer["source_graphicnum"],
                              original_trainer["parameter_path"], original_trainer["source_original_sha256"],
                              original_trainer["source_skill_rate_literal"], original_trainer["source_pet_skill_ids_ordered"]))
            for service in (pet, trainer):
                row = self.creates[(service["create_file"], service["create_ordinal"])]
                self.assertEqual((row[4], row[5], row[6], row[7]),
                                 (service["create_sha256"], floor, service["graphic"], service["xy"] * 2))
                self.assertEqual(row[11], "npcgen_petshop" if service["role"] == "PetShop"
                                 else "npcgen_petskillshop")
        self.assertEqual([len(r["services"][1]["skill_ids"]) for r in self.report["rooms"]], [7, 7, 9])
        self.assertEqual([r["services"][0]["original_fields"]["pool_flg_raw"] for r in self.report["rooms"]],
                         [None, None, "1"])
        self.assertEqual([r["services"][0]["original_fields"]["pool_cost_raw"] for r in self.report["rooms"]],
                         [None, None, "200"])

    def test_eleven_original_directed_edges_and_single_missing_reverse(self):
        r = self.report
        self.assertEqual(r["exact_original_source_files"]["mapwarp"]["sha256"],
                         self.source["integration17"]["original_mapwarp_sha256"])
        edges = r["directed_warp_edges"]
        self.assertEqual(len(edges), 11)
        self.assertEqual([x["mapwarp_line"] for x in edges],
                         [664, 665, 666, 667, 735, 736, 737, 752, 753, 754, 755])
        directions = {(tuple(e["start"]), tuple(e["target"])) for e in edges}
        self.assertEqual(len(directions), 11)
        for e in edges:
            source_row = self.creates[(e["create_file"], e["create_ordinal"])]
            self.assertEqual((source_row[4], source_row[5], source_row[7][:2], source_row[11]),
                             (e["create_sha256"], e["start"][0], e["start"][1:], "npcgen_warp"))
            self.assertIs(e["reverse_present"], (tuple(e["target"]), tuple(e["start"])) in directions)
        unpaired = [e for e in edges if not e["reverse_present"]]
        self.assertEqual([(x["start"], x["target"]) for x in unpaired],
                         [([3303, 16, 20], [3300, 51, 60])])
        self.assertNotIn(((3300, 51, 60), (3303, 16, 20)), directions)

    def test_4003_original_dat_cells_tutor_and_3403_static_alias(self):
        r = self.report
        self.assertEqual([x["u16"] for x in r["original_4003_dat_cells"]],
                         [[5002,0,49152], [5000,0,49152], [5002,12802,49152],
                          [5024,0,49155], [5013,0,49155]])
        for c in r["original_4003_dat_cells"]:
            x,y = c["xy"]
            self.assertEqual(c["modern_marker"], [16+32*(x+y), 712+24*(y-x)])
        old = next(x for x in self.source["scene26r2"]["source_tutor_four_CREATE_rows"]
                   if x["source_floor_id"] == 4003)
        tut = r["original_4003_tutor"]
        self.assertEqual((tut["graphic"], tut["script_sha256"], tut["create_sha256"]),
                         (old["original_source_graphicname"], old["original_script_sha256"],
                          self.source["integration17"]["tutor_source_preflight"]["candidate_rooms"][-1]["create"][2]))
        graph = next(x for x in self.source["integration17"]["graphics"] if x["graphic"] == 16033)
        obj = r["qualified_3403_static_original_alias_16033"]
        self.assertEqual((obj["source_RD_sha256"], obj["source_PNG_sha256"],
                          obj["source_RGBA_sha256"], obj["dimensions"]),
                         (graph["rd_sha256"], graph["png_sha256"], graph["rgba_sha256"], graph["dimensions"]))
        self.assertFalse(obj["original_3403_scene_composite_with_sprite_verified"])

    def test_no_source_promoted_to_native_game_and_private_custody(self):
        r = self.report
        for key in ("original_shop_storage_purchase_or_skill_training_executed",
                    "original_warp_and_collision_executed", "official_same_deployment_verified",
                    "original_3303_3403_private_DAT_bytes_replayed_this_work",
                    "original_3400_DAT_replayed_this_work", "missing_original_NPC_sprites_invented",
                    "proprietary_original_source_published"):
            self.assertIs(r["bounds"][key], False, key)
        self.assertEqual((r["bounds"]["stage_A"], r["bounds"]["stage_B_wiki"],
                          r["bounds"]["R79"], r["bounds"]["overall_percent"]),
                         ("7_PARTIAL_2_OPEN", "GATED", "PAUSED_NON_BLOCKING", None))
        pkg = r["private_package"]
        self.assertEqual((pkg["bytes"],pkg["members"]), (534764,16))
        self.assertTrue(pkg["private_Library_uploaded_and_downloaded_SHA_CRC"])
        self.assertFalse(pkg["browser_executed_this_work"])
        self.assertTrue(pkg["full_4003_source_scene_only"])


if __name__ == "__main__":
    unittest.main()
