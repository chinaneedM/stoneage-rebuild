import json
from pathlib import Path
import unittest


SCHEMA_PATH = Path("research/clients/STONEAGE-TW10-GAMEPLAY-SCHEMA-R1.json")


class TaiwanGameplaySchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    def test_identity_and_evidence_levels(self):
        self.assertEqual(self.schema["schema_id"], "stoneage.tw10.gameplay.r1")
        self.assertEqual(self.schema["schema_version"], 1)
        self.assertEqual(
            set(self.schema["evidence_levels"]),
            {"V1_DIRECT", "EARLY_LINEAGE", "BRIDGE_2_5", "VERSIONED_OPEN"},
        )

    def test_all_record_positions_are_dense_and_evidence_tagged(self):
        for name, record in self.schema["records"].items():
            fields = record["fields"]
            positions = [field["position"] for field in fields]
            self.assertEqual(
                positions,
                list(range(1, len(fields) + 1)),
                msg=f"{name} positions are not dense",
            )
            expected_width = record.get("record_width", record.get("full_record_width"))
            self.assertEqual(expected_width, len(fields), msg=f"{name} width mismatch")
            for field in fields:
                self.assertEqual(field["position_evidence"], "V1_DIRECT")
                self.assertEqual(field["semantic_evidence"], "EARLY_LINEAGE")
                self.assertTrue(field["name"])
                self.assertTrue(field["wire_type"])

    def test_direct_v1_status_layout_boundaries(self):
        records = self.schema["records"]
        self.assertEqual(records["status_player_full"]["full_record_width"], 26)
        self.assertEqual(records["status_player_full"]["fields"][-2]["position"], 25)
        self.assertEqual(records["status_player_full"]["fields"][-2]["wire_type"], "escaped_string")
        self.assertEqual(records["status_player_full"]["fields"][-1]["position"], 26)
        self.assertEqual(records["status_pet_full"]["full_record_width"], 21)
        self.assertEqual(records["status_pet_full"]["fields"][-2]["position"], 20)
        self.assertEqual(records["status_pet_full"]["fields"][-1]["position"], 21)

    def test_inventory_and_pet_skill_hard_counts(self):
        records = self.schema["records"]
        full_item = records["inventory_full_slot"]
        incremental = records["inventory_incremental_record"]
        pet_skill = records["pet_skill_view_slot"]

        self.assertEqual(full_item["slot_count"], 20)
        self.assertEqual(full_item["record_width"], 9)
        self.assertEqual(incremental["record_width"], 10)
        self.assertEqual(pet_skill["slot_count"], 7)
        self.assertEqual(pet_skill["record_width"], 5)
        self.assertEqual(
            [field["name"] for field in full_item["fields"]],
            [
                "name",
                "secondary_display_text",
                "color",
                "memo_or_effect_text",
                "graphic_id",
                "field_context",
                "target_class",
                "level",
                "send_or_use_flags",
            ],
        )
        self.assertEqual(
            [field["name"] for field in incremental["fields"]][1:],
            [field["name"] for field in full_item["fields"]],
        )

        self.assertEqual(
            [field["name"] for field in pet_skill["fields"]],
            ["skill_id", "field_context", "target_class", "name", "comment"],
        )

    def test_world_object_variant_widths(self):
        records = self.schema["records"]
        self.assertEqual(records["world_character_record"]["record_width"], 12)
        self.assertEqual(records["world_ground_item_record"]["record_width"], 6)
        self.assertEqual(records["world_ground_money_record"]["record_width"], 4)
        self.assertNotIn(
            "popup_name_color",
            {f["name"] for f in records["world_character_record"]["fields"]},
        )

    def test_window_forwarding_boundary(self):
        record = self.schema["records"]["npc_window_session"]
        self.assertEqual(record["record_width"], 5)
        self.assertEqual(record["transport"]["callback_rva"], "0x328c0")
        self.assertEqual(record["transport"]["forward_target_rva"], "0x12930")

    def test_later_item_extensions_are_quarantined(self):
        excluded = "\n".join(self.schema["direct_version_exclusions"]).lower()
        for token in ("durability", "pile", "alchemy", "jigsaw", "countdown"):
            self.assertIn(token, excluded)


if __name__ == "__main__":
    unittest.main()
