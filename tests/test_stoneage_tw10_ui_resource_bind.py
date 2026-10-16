"""Original v1 battle container, lineage candidate decoder and unmapped pet view."""
import json
from pathlib import Path
import unittest

from tools.stoneage_tw10_battle_scene_spec import (
    decode_sab_candidate, indexed_battle_resources, pet_graphic_identity_boundary,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/recovered/STONEAGE-TW10-UI-RESOURCE-BIND-SCOPE-R1.json"


class OriginalV1ResourceBindingBoundary(unittest.TestCase):
    def test_exactly_two_qualified_ui_selection_seams(self):
        report = json.loads(REPORT.read_text(encoding="utf-8"))
        self.assertEqual("stoneage.tw10.ui-resource-bind.01", report["schema"])
        self.assertEqual(2, len(report["investigations"]))
        self.assertEqual(["A_SAB_GRID_TO_BITMAP_IDENTITY", "B_PET_GRAPHIC_TO_REAL_SPR_SELECTION"],
                         [x["item"] for x in report["investigations"]])
        self.assertFalse(report["historical_ui_binding_complete"])
        self.assertFalse(report["stage_a_accepted"])
        self.assertEqual("GATED", report["stage_b_gate"])
        self.assertIsNone(report["historical_completion_percentage"])
        self.assertTrue(all(x["not_proven"] and x["reopen_if"] for x in report["investigations"]))

    def test_source_pins_are_original_git_blob_ids(self):
        import hashlib
        report = json.loads(REPORT.read_text(encoding="utf-8"))
        for path, pinned in report["source_pins"].items():
            content = (ROOT / path).read_bytes()
            self.assertEqual(len(content), pinned["bytes"])
            self.assertEqual(hashlib.sha1(b"blob " + str(len(content)).encode() + b"\x00" + content).hexdigest(), pinned["git_blob"], path)

    def test_original_battle_address_container_not_233_maps(self):
        records = indexed_battle_resources()
        self.assertEqual(233, len(records))
        maps = [r for r in records if r["category"] == "battle_map"]
        palettes = [r for r in records if r["category"] == "palette"]
        self.assertEqual((218, 15), (len(maps), len(palettes)))
        self.assertEqual(185892, sum(r["size"] for r in records))
        self.assertEqual("battle00.sab", maps[0]["name"])
        self.assertEqual("battle217.sab", maps[-1]["name"])
        self.assertEqual("Palet_1.sap", palettes[0]["name"])
        self.assertEqual("Palet_15.sap", palettes[-1]["name"])
        self.assertFalse(any(r["name"] == "Palet_0.sap" for r in records))
        self.assertLess(records.index(palettes[0]), records.index(maps[-1]))

    def test_candidate_layout_only_no_actual_scene_selection(self):
        blob = b"SAB " + (b"\x00\x01" * 400)
        result = decode_sab_candidate(blob)
        self.assertEqual([1] * 20, result["candidate_grid"][0])
        self.assertEqual((20, 20), (result["grid_width"], result["grid_height"]))
        self.assertIsNone(result["selected_battle_map_index"])
        self.assertIsNone(result["selected_palette"])
        self.assertFalse(result["original_runtime_selection_verified"])
        assert "NOT_DIRECT_V1" in result["layout_evidence"]
        mixed = b"SAB " + b"\x12\x34" + b"\x34\x12" + b"\x00\x00" * 398
        self.assertEqual([0x1234, 0x3412], decode_sab_candidate(mixed)["candidate_grid"][0][:2])

    def test_short_wrong_header_and_wrong_input_type_rejected(self):
        for bad in (b"", b"SAB", b"SAB " + b"\x00" * 798,
                    b"BAD " + b"\x00" * 800, "SAB " + "0" * 800, None):
            with self.assertRaises(ValueError):
                decode_sab_candidate(bad)

    def test_pet_graphic_value_does_not_fake_animation_or_bitmap(self):
        result = pet_graphic_identity_boundary(12345)
        self.assertEqual(12345, result["graphic_identity"])
        self.assertIsNone(result["v1_spr_group"])
        self.assertIsNone(result["v1_adrn_bitmap"])
        self.assertFalse(result["v1_draw_call_verified"])
        for bad in (-1, True, "12345", None):
            with self.assertRaises(ValueError):
                pet_graphic_identity_boundary(bad)


if __name__ == "__main__":
    unittest.main()
