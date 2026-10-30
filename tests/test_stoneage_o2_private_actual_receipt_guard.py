"""Synthetic/public-only guard for a PRIVATE source rerun receipt.

The public pipeline intentionally has no raw copyrighted files. This guard
checks only the compatibility between already archived source-derived records,
new independent external receipt and explicit negative historical gates.
"""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ACTUAL = ROOT / "research/recovered/STONEAGE-O2-ACTUAL-PRIVATE-SOURCE-ACCEPTANCE-R1.json"
MAP = ROOT / "research/recovered/STONEAGE-SCENE21-TOWN1000-SOURCE-R1.json"

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

class O2PrivateActualReceiptGuard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = ACTUAL.read_bytes()
        cls.a = json.loads(cls.raw)
        cls.m = json.loads(MAP.read_bytes())

    def test_archived_map_identity_and_bounded_original_source(self):
        a, m = self.a, self.m
        self.assertEqual(a["schema"], "stoneage.o2_actual_private_source_and_browser_acceptance.r1")
        self.assertEqual(a["source_material_1"]["report_sha256"], digest(MAP.read_bytes()))
        self.assertEqual(a["source_material_1"]["original_source_report_git_blob_sha1"],
                         hashlib.sha1(b"blob "+str(MAP.stat().st_size).encode()+b"\x00"+MAP.read_bytes()).hexdigest())
        self.assertEqual(a["source_material_1"]["map_1000_dat_sha256"], m["source_map_sha256"])
        self.assertEqual(a["source_material_1"]["palette1_sap_sha256"], m["source_palette_sha256"])
        self.assertEqual(a["source_material_1"]["private_archive_bytes"], m["source_packages"].get("r21", {}).get("bytes", 2745658))
        self.assertEqual(a["executed_replay"]["private_original_map_cells_verified"], len(m["cells"]) == 77 and 77)
        self.assertEqual(a["executed_replay"]["private_original_map_placements_verified"], len(m["placements"]) == 85 and 85)
        self.assertEqual(a["executed_replay"]["original_rd_source_payloads_independently_decoded"], len(m["resources"]))
        self.assertEqual(a["executed_replay"]["original_rgba_full_candidate_scenes_recomposed"],len(m["frames"]))
        self.assertEqual(a["executed_replay"]["original_private_html_embedded_images_verified"],8)
        self.assertFalse(m["same_official_deployed_build_authenticated"])
        self.assertFalse(m["original_world_entered"])

    def test_tw1_member_identity_and_duplicate_frames_not_overcounted(self):
        a = self.a
        spr = a["source_material_2"]
        pinned = {
          "spr_1_bin": "53d5b2d40453a30fd1569637ebf0db7b3010542b00970ec83af0295a3b3ae31a",
          "spradrn_1_bin": "275b64ff55667aec633a7e82e09d65c84141380521f0f2e64c9a28e0d3aa6c25",
          "adrn_1_bin": "47254c0ff904d363fb5c3c5297edf553c8eaf24cd933f346d8ce7aabed4155c8",
          "real_1_bin": "408e6ee05c83354349691937da2ad8f7488ac10f65f07e6681b7d92cb1c9ed13",
        }
        self.assertEqual(spr["member_sha256"],pinned)
        actor = a["original_tw1_animation_sample"]
        self.assertEqual((actor["spr_no"],actor["direction"],actor["action_code"]), (100000,0,6))
        self.assertEqual(actor["unique_bitmap_numbers"],[10185,10186])
        self.assertEqual(actor["source_frame_positions"],7)
        self.assertEqual(len(actor["source_frame_png_sha256_ordered"]),7)
        self.assertEqual(len(set(actor["source_frame_png_sha256_ordered"])),2)
        self.assertEqual(actor["preview_canvas_pixels"],[60,64])

    def test_browser_genuine_pixels_but_not_native_runtime(self):
        a = self.a
        self.assertEqual(a["executed_replay"]["source_html_browser_test_states"],8)
        self.assertEqual(a["browser_private_combined"]["original_png_map_states_verified"],8)
        self.assertEqual(a["browser_private_combined"]["external_requests"],0)
        self.assertEqual(a["browser_private_combined"]["js_errors"],0)
        for key in ("tw1_sprite_original_frame_rendered", "manual_keyboard_and_button_movement_verified",
                    "actor_visibility_toggle_verified","integer_zoom_verified","pause_and_reset_verified"):
            self.assertIs(a["browser_private_combined"][key],True)
        self.assertTrue(a["browser_private_combined"]["browser_file_url_navigation_blocked_by_administrator"])
        self.assertTrue(a["browser_private_combined"]["actual_in_memory_same_html_bytes_rendered"])
        for key, val in a["evidence_limits"].items():
            self.assertIs(val,False,key)

    def test_private_only_outputs_and_retained_stage_boundary(self):
        a = self.a
        self.assertEqual(a["private_output"]["private_archive_file_count"],15)
        self.assertEqual(a["private_output"]["private_zip_bytes"],2078427)
        self.assertIs(a["private_output"]["original_images_or_html_committed_public"],False)
        self.assertTrue(a["private_output"]["private_library_path"].startswith("/石器时代/"))
        self.assertEqual(a["project_state"]["stage_a"],"7 PARTIAL + 2 OPEN")
        self.assertEqual(a["project_state"]["stage_b"],"GATED")
        self.assertEqual(a["project_state"]["wiki"],"GATED")
        self.assertEqual(a["project_state"]["r79"],"PAUSED_NON_BLOCKING")
        self.assertIsNone(a["project_state"]["overall_percent"])
        self.assertEqual(len(a["source_material_1"]["private_archive_sha256"]),64)
        self.assertEqual(len(a["private_output"]["private_zip_sha256"]),64)
        self.assertEqual(a["preserve_current_blob_sha"],"20050acf279a01555ab06a381dfcdc936bd381a6")

if __name__ == "__main__":
    unittest.main()
