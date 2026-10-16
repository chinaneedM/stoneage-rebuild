"""Independent original TW1.0 5-surface source/semantic negative-claim gates."""
import hashlib
import json
from pathlib import Path
import unittest
from tools.stoneage_tw10_ui_semantics import (
    crosswalk, project_decoded_full_record, classify_v1_received_battle_envelope)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "research/clients/STONEAGE-TW10-GAMEPLAY-SCHEMA-R1.json"
PROTOCOL = ROOT / "research/recovered/STONEAGE-TW10-GAMEPLAY-PROTOCOL-R1.txt"
BATTLE = ROOT / "research/recovered/STONEAGE-TW10-BATTLE-DATASET-R1.txt"


class TW10UISemantics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = crosswalk()
        cls.original = json.loads(SCHEMA.read_text(encoding="utf-8"))
        cls.protocol_rows = PROTOCOL.read_text(encoding="utf-8").splitlines()
        cls.battle_lines = BATTLE.read_text(encoding="utf-8").splitlines()

    def test_original_version_and_no_false_stage_a_acceptance(self):
        q = self.report
        self.assertEqual("stoneage.tw10.ui-semantics.01", q["schema"])
        self.assertFalse(q["stage_a_accepted"])
        self.assertEqual("GATED", q["stage_b_gate"])
        self.assertIsNone(q["historical_completion_percentage"])
        self.assertIn("VISUAL_BINDINGS_OPEN", q["result"])
        self.assertEqual("UI-RESOURCE-BIND-01", q["next_highest"])

    def test_source_git_blobs_are_reproducible(self):
        for key, info in self.report["source_pins"].items():
            content = (ROOT / info["path"]).read_bytes()
            if info["bytes"] is not None:
                self.assertEqual(info["bytes"], len(content), key)
            gitsha = hashlib.sha1(b"blob " + str(len(content)).encode() + bytes([0]) + content).hexdigest()
            self.assertEqual(info["git_blob"], gitsha, key)

    def test_exact_five_surfaces_and_all_sixteen_source_records(self):
        expected = [
            "FIELD_AND_POSITION_STATUS", "CHARACTER_STATUS_AND_HUD",
            "INVENTORY_AND_ITEMS", "PET_STATUS_SKILLS", "BATTLE_AND_NPC_WINDOWS"]
        self.assertEqual(expected, [s["id"] for s in self.report["surfaces"]])
        seen = {}
        for surf in self.report["surfaces"]:
            self.assertEqual("SOURCE_SHAPE_CROSSWALK_ONLY_VISUAL_BINDING_OPEN", surf["status"])
            for key in ("render_geometry", "button_coordinates", "verified_graphic_selection_map"):
                self.assertIsNone(surf[key])
            self.assertTrue(surf["material_unresolved"])
            self.assertTrue(surf["forbidden_inferences"])
            for item in surf["record_contracts"]:
                record_id = item["schema_record"]
                self.assertNotIn(record_id, seen)
                seen[record_id] = surf["id"]
                original = self.original["records"][record_id]
                self.assertEqual(item["transport"], original["transport"])
                self.assertEqual(item["field_count"], len(original["fields"]))
                self.assertEqual(item["fields"], original["fields"])
                self.assertIsNone(item["visual_field_binding"])
                self.assertTrue(item["full_record_only"])
        self.assertEqual(set(self.original["records"]), set(seen))

    def test_envelope_arities_were_in_original_compiled_region(self):
        for s in self.report["surfaces"]:
            for e in s["envelopes"]:
                rows = [x for x in self.protocol_rows if x.startswith("PROTOCOL|") and
                        "|region=" + e["direction"] + "|name=" + e["message"] + "|" in x]
                self.assertEqual(1, len(rows), e)
                self.assertIn("|int_fields=" + str(e["int_fields"]) + "|", rows[0])
                self.assertIn("|string_fields=" + str(e["string_fields"]) + "|", rows[0])
                self.assertIn("|xref_rva=" + e["compiled_region_rva"] + "|", rows[0])
                self.assertFalse(e["render_command_proven"])

    def test_original_battle_receive_branches_distinct(self):
        b = self.report["battle_receive"]
        o = self.original["protocol_state_machines"]["battle_receive"]
        self.assertEqual(1, b["second_byte_offset"])
        self.assertEqual(o["transport"]["callback_rva"], b["callback_rva"])
        for key, row in b["branches"].items():
            self.assertEqual(row["direct_behavior"], o["discriminator"]["branches"][key]["direct_behavior"])
            self.assertEqual(row["queue_slots"], o["discriminator"]["branches"][key].get("ring_slots"))
            self.assertEqual(row["queue_slot_bytes"], o["discriminator"]["branches"][key].get("slot_bytes"))
        self.assertEqual(4, b["branches"]["C"]["queue_slots"])
        self.assertEqual(4096, b["branches"]["default"]["queue_slot_bytes"])
        self.assertIsNone(b["visual_sequence_binding"])

    def test_original_battle_dataset_does_not_conflate_palette(self):
        txt = "\n".join(self.battle_lines)
        self.assertIn("ADDRESS_TABLE_CATEGORY|label=battle|category=battle_map|records=218|", txt)
        self.assertIn("ADDRESS_TABLE_CATEGORY|label=battle|category=palette|records=15|", txt)
        self.assertIn("Palet_0.sap is disc-resident but not referenced by the battle address table", txt)
        n = self.report["qualified_resource_counts"]
        self.assertEqual((218, 15, 1), (n["battle_scene_address_entries"],
                         n["battle_indexed_palettes"], n["battle_unindexed_palettes"]))

    def test_projection_allows_only_full_decoded_original_positions(self):
        k = "status_player_full"
        fields = self.original["records"][k]["fields"]
        values = ["" if f["wire_type"] == "escaped_string" else 0 for f in fields]
        out = project_decoded_full_record("CHARACTER_STATUS_AND_HUD", k, values)
        self.assertEqual(26, len(out["decoded_full_record"]))
        self.assertEqual("hp", out["decoded_full_record"][1]["lineage_name"])
        self.assertIsNone(out["historical_layout"])
        self.assertIsNone(out["visual_resource_selection"])
        self.assertFalse(out["original_display_verified"])
        for bad in [values[:-1], values + [0]]:
            with self.assertRaises(ValueError):
                project_decoded_full_record("CHARACTER_STATUS_AND_HUD", k, bad)
        with self.assertRaises(ValueError):
            project_decoded_full_record("PET_STATUS_SKILLS", k, values)
        with self.assertRaises(ValueError):
            project_decoded_full_record("CHARACTER_STATUS_AND_HUD", k, [True] + values[1:])
        with self.assertRaises(ValueError):
            project_decoded_full_record("CHARACTER_STATUS_AND_HUD", k, "wrong")

    def test_pet_graphic_identity_is_not_render_binding(self):
        k = "status_pet_full"
        original = self.original["records"][k]["fields"]
        values = ["" if f["wire_type"] == "escaped_string" else 7 for f in original]
        p = project_decoded_full_record("PET_STATUS_SKILLS", k, values)
        self.assertEqual("graphic_id", p["decoded_full_record"][1]["lineage_name"])
        self.assertEqual(7, p["decoded_full_record"][1]["value"])
        self.assertIsNone(p["visual_resource_selection"])
        w = self.original["records"]["pet_skill_view_slot"]["fields"]
        sample = ["" if f["wire_type"] == "escaped_string" else 4 for f in w]
        s = project_decoded_full_record("PET_STATUS_SKILLS", "pet_skill_view_slot", sample)
        self.assertEqual(5, len(s["decoded_full_record"]))

    def test_battle_dispatch_no_later_subcommand_or_fake_scene(self):
        for cmd, branch in [("BCpayload","C"),("BPpayload","P"),("BApayload","A"),
                            ("BUpayload","U"),("BZpayload","default"),("BFpayload","default")]:
            result = classify_v1_received_battle_envelope(cmd)
            self.assertEqual(branch, result["branch"])
            self.assertFalse(result["original_display_verified"])
            self.assertIsNone(result["animation_id"])
            self.assertIsNone(result["scene_map_id"])
        for bad in ("", "B", None):
            with self.assertRaises(ValueError):
                classify_v1_received_battle_envelope(bad)

    def test_negative_borrowed_protocol_and_asset_claims(self):
        excluded = self.original["direct_version_exclusions"]
        self.assertTrue(any("S:P tokens after 26" in a for a in excluded))
        self.assertTrue(any("S:K tokens after 21" in a for a in excluded))
        for s in self.report["surfaces"]:
            self.assertIsNone(s["verified_graphic_selection_map"])
        self.assertTrue(self.report["unknowns"])
        self.assertTrue(self.report["reopen_if"])


if __name__ == "__main__":
    unittest.main()
