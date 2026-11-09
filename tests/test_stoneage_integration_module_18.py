"""Original four-tutor source-bound candidate placement checks; no copyrighted pixels in CI."""
import copy
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
FILENAME = "STONEAGE-INTEGRATION18-SCENE26-R4-BOUNDED-TUTOR-LAYOUT-R1.json"


def pinned_json(path, git_blob):
    raw = (ROOT / path).read_bytes()
    actual = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
    if actual != git_blob:
        raise AssertionError(f"Original source blob changed: {path}")
    return json.loads(raw)


class Integration18TutorLayoutEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT / "research/recovered" / FILENAME).read_bytes())
        cls.sources = {
            k: pinned_json(row["path"], row["sha"])
            for k, row in cls.report["verified_upstream_Git_blobs"].items()
        }

    def verify_join(self, report):
        s = self.sources
        preflight = s["integration17"]["tutor_source_preflight"]
        r2 = s["scene26r2"]["source_tutor_four_CREATE_rows"]
        r3 = s["scene26r3"]["source_original_NPC_CREATE"]["four_pet_tutor_floors"]
        origin = s["scene26source"]["rows"]
        room_rows = report["four_rooms"]
        self.assertEqual([r["floor"] for r in room_rows], [1003, 2003, 3003, 4003])
        self.assertEqual(len(room_rows), len(r2), 4)
        self.assertFalse(preflight["placed_in_tutor_rooms"])
        self.assertTrue(preflight["actual_mixed25_RD_and_RGBA_replayed"])
        sprites = {r["graphic"]: r for r in preflight["graphics"]}
        self.assertEqual(set(sprites), {16122, 16127})
        for i, room in enumerate(room_rows):
            old, cross, first = r2[i], r3[i], origin[i]
            floor = old["source_floor_id"]
            self.assertEqual(floor, room["floor"])
            self.assertEqual(floor, cross["floor"])
            self.assertEqual(floor, first["source_original_floorid"])
            self.assertEqual(room["original_source_DAT_sha256"], old["original_DAT_whole_sha256"])
            self.assertEqual(old["original_DAT_whole_sha256"], s["map09"]["maps"][str(floor)]["source_sha256"])
            self.assertEqual(room["source_three_original_DAT_u16"],
                             old["original_DAT_three_u16_words_at_original_borncenter"])
            create = room["original_create"]
            self.assertEqual(create["ordinal"], old["source_CREATE_ordinal"])
            self.assertEqual(create["borncenter"], old["original_borncenter"])
            self.assertEqual(create["borncenter"], cross["borncenter"])
            self.assertEqual(create["borncenter"], first["source_original_borncenter"])
            self.assertEqual(create["graphic_alias"], cross["graphicname"])
            self.assertEqual(create["graphic_alias"], old["original_source_graphicname"])
            self.assertEqual(create["graphic_alias"], first["source_original_graphicname"])
            self.assertEqual(create["block_sha256"], preflight["candidate_rooms"][i]["create"][2])
            self.assertEqual(create["direction"], old["original_directions"])
            graphic = sprites[create["graphic_alias"]]
            for k, field in (("rd_sha256", "candidate_sprite_original_RD_sha256"),
                             ("png_sha256", "candidate_sprite_original_PNG_sha256"),
                             ("rgba_sha256", "candidate_sprite_original_RGBA_sha256")):
                self.assertEqual(room[field], graphic[k])
            from_r3 = s["scene26r3"]["derived_original_reference_query"]["sources"][str(graphic["graphic"])]
            self.assertEqual({x["reference"]["profile"] for x in from_r3["logical_alias_entries"]},
                             {"CN50", "PATCH129"})
            self.assertTrue(all(x["content"]["rd_sha256"] == graphic["rd_sha256"]
                                for x in from_r3["logical_alias_entries"]))
            map_row = s["map09"]["maps"][str(floor)]
            geometry = room["candidate_pixel_geometry"]
            x, y = create["borncenter"]
            marker = [map_row["origin"][0] + (x+y)*32, map_row["origin"][1] + (y-x)*24]
            top_left = [a+b for a,b in zip(marker, graphic["signed_adrn_offset"])]
            self.assertEqual(geometry["modern_marker_xy"], marker)
            self.assertEqual(geometry["modern_marker_xy"], old["modern_marker_xy"])
            self.assertEqual(geometry["modern_sprite_top_left_xy"], top_left)
            self.assertEqual(geometry["modern_sprite_top_left_xy"],
                             preflight["candidate_rooms"][i]["graphic_px"])
            self.assertEqual(geometry["source_qualified_sprite_dimensions"], graphic["dimensions"])
            self.assertEqual(geometry["canvas_size"], map_row["canvas_size"])
            self.assertTrue(all(0 <= top_left[j] and top_left[j] + graphic["dimensions"][j] <= map_row["canvas_size"][j]
                                for j in (0,1)))
            self.assertEqual(room["source_qualified_MAP09_canvas_RGBA_sha256"],
                             map_row["frame_RGBA_sha256"]["combined"])
            self.assertFalse(room["candidate_sprite_pixels_in_this_private_R4_package"])
            self.assertFalse(room["native_original_client_render_verified"])

    def test_four_original_CREATE_DAT_and_real_graphic_candidate_positions(self):
        self.verify_join(self.report)

    def test_negative_swapped_alias_and_moved_point_rejected(self):
        for field, value in (("graphic_alias", 16127), ("borncenter", [0,0])):
            changed = copy.deepcopy(self.report)
            changed["four_rooms"][0]["original_create"][field] = value
            with self.assertRaises(AssertionError):
                self.verify_join(changed)

    def test_negative_foreign_rd_or_canvas_hash_rejected(self):
        changed = copy.deepcopy(self.report)
        changed["four_rooms"][1]["candidate_sprite_original_RD_sha256"] = "0"*64
        with self.assertRaises(AssertionError):
            self.verify_join(changed)
        changed = copy.deepcopy(self.report)
        changed["four_rooms"][2]["source_qualified_MAP09_canvas_RGBA_sha256"] = "0"*64
        with self.assertRaises(AssertionError):
            self.verify_join(changed)

    def test_original_text_and_proprietary_boundary_not_promoted(self):
        report = self.report
        self.assertEqual(report["preserved_historical_current_blob"],
                         "c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual(report["shared_private_original_script"]["sha256"],
                         self.sources["scene26r2"]["original_carrier_context"]["original_petmaster_sha256"])
        self.assertEqual(report["shared_private_original_script"]["dialogue_original_window_count"], 9)
        self.assertFalse(report["shared_private_original_script"]["native_event_execution_verified"])
        self.assertFalse(report["private_replay"]["original_RD_PNG_16122_16127_available_to_this_replay"])
        self.assertEqual(report["private_replay"]["rendered_original_tutor_PNG_count"], 0)
        self.assertEqual(report["private_replay"]["visible_source_bounded_outline_count"], 4)
        self.assertTrue(report["private_replay"]["uploaded_to_persistent_library"])
        self.assertTrue(report["private_replay"]["library_roundtrip_whole_zip_SHA256_and_CRC_verified"])
        self.assertEqual(report["private_replay"]["library_roundtrip_sha256"], report["private_replay"]["new_private_zip_sha256"])
        for key in ("original_sprite_character_pixels_placed", "original_game_client_executed",
                    "original_game_server_NPC_event_executed", "official_same_deployment_proven",
                    "native_render_order_collision_palette_verified", "raw_proprietary_assets_published_in_Git"):
            self.assertIs(report["bounds"][key], False)
        self.assertIsNone(report["bounds"]["overall_percent"])
        self.assertEqual(report["bounds"]["stage_A"], "7_PARTIAL_2_OPEN")
        self.assertEqual(report["bounds"]["stage_B_wiki"], "GATED")
        self.assertEqual(report["bounds"]["R79"], "PAUSED_NON_BLOCKING")


if __name__ == "__main__":
    unittest.main()
