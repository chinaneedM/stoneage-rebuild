import json
from pathlib import Path
import unittest


BASELINE_PATH = Path("research/clients/STONEAGE-TW10-GAMEPLAY-SCHEMA-R1.json")
BRIDGE_PATH = Path("research/clients/STONEAGE-TW10-25-GAMEPLAY-BRIDGE-R1.json")


class Taiwan25GameplayBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
        cls.bridge = json.loads(BRIDGE_PATH.read_text(encoding="utf-8"))
        cls.records = cls.baseline["records"]

    def assert_target_field(self, record_name, field_name):
        self.assertIn(record_name, self.records)
        names = {field["name"] for field in self.records[record_name]["fields"]}
        self.assertIn(field_name, names, msg=f"{record_name}.{field_name} missing")

    def test_bridge_identity_and_baseline_reference(self):
        self.assertEqual(self.bridge["schema_id"], "stoneage.tw10.25.gameplay-bridge.r1")
        self.assertEqual(self.bridge["schema_version"], 1)
        self.assertEqual(
            self.bridge["baseline_schema"],
            "research/clients/STONEAGE-TW10-GAMEPLAY-SCHEMA-R1.json",
        )

    def test_pet_bridge_targets_exist(self):
        pet = self.bridge["bridges"]["pet_template_to_pet_state"]
        for mapping in pet["mappings"]:
            self.assert_target_field(mapping["target_record"], mapping["target_field"])
            self.assertEqual(mapping["baseline_evidence"], "V1_DIRECT")
            self.assertEqual(mapping["bridge_evidence"], "BRIDGE_2_5")
        self.assertEqual(
            pet["template_identity"]["target_is_wire_field"],
            False,
        )
        self.assert_target_field(
            pet["skill_assignment_bridge"]["target_record"],
            pet["skill_assignment_bridge"]["target_field"],
        )

    def test_pet_skill_bridge_is_exactly_five_client_view_fields(self):
        bridge = self.bridge["bridges"]["pet_skill_template_to_view"]
        mapped = {m["target_field"]: m["source_field"] for m in bridge["mappings"]}
        self.assertEqual(
            mapped,
            {
                "skill_id": "ID",
                "field_context": "FIELD",
                "target_class": "TARGET",
                "name": "NAME",
                "comment": "COMMENT",
            },
        )
        self.assertEqual(
            set(mapped),
            {f["name"] for f in self.records["pet_skill_view_slot"]["fields"]},
        )
        for forbidden in ("COST", "ILLEGAL", "FUNCNAME", "OPTION"):
            self.assertIn(forbidden, bridge["server_only_fields"])

    def test_item_bridge_never_equates_template_id_with_slot(self):
        bridge = self.bridge["bridges"]["item_template_to_item_view"]
        self.assertEqual(bridge["template_identity"]["source_field"], "id")
        self.assertFalse(bridge["template_identity"]["target_is_wire_field"])
        mappings = {m["target_field"]: m for m in bridge["mappings"]}
        for record in ("inventory_full_slot", "inventory_incremental_record"):
            for target_field in mappings:
                if target_field == "inventory_slot":
                    continue
                self.assert_target_field(record, target_field)
        self.assertNotIn("inventory_slot", mappings)
        self.assertIsNone(mappings["secondary_or_secret_name"]["source_field"])
        self.assertIsNone(mappings["send_or_use_flags"]["source_field"])
        quarantined = " ".join(bridge["server_only_or_versioned_fields"]).lower()
        for token in ("durability", "campile", "magicid", "useaction"):
            self.assertIn(token, quarantined)

    def test_npc_bridge_is_architecture_only(self):
        bridge = self.bridge["bridges"]["npc_master_to_world_and_window"]
        self.assertTrue(all(m["status"] == "architecture_bridge_only" for m in bridge["mappings"]))
        joined = " ".join(bridge["explicit_non_equivalences"]).lower()
        self.assertIn("template name != v1 runtime_object_id", joined)
        self.assertIn("functionset name != v1 object_type", joined)
        self.assertIn("windowman conff window number != v1 runtime object index", joined)

    def test_required_identity_guards_are_present(self):
        rules = {r["rule"]: r["status"] for r in self.bridge["identity_rules"]}
        for name in (
            "runtime_object_id_is_not_template_id",
            "inventory_slot_is_not_item_template_id",
            "pet_slot_is_not_enemybase_tempno",
            "v1_wire_fields_must_not_be_backfilled_from_2_5",
        ):
            self.assertEqual(rules.get(name), "REQUIRED")

    def test_every_explicit_bridge_uses_known_evidence_labels(self):
        allowed = set(self.bridge["evidence_levels"])
        for group in self.bridge["bridges"].values():
            for mapping in group.get("mappings", []):
                for key in ("baseline_evidence", "semantic_evidence", "bridge_evidence"):
                    if key in mapping:
                        self.assertIn(mapping[key], allowed)
            for key in ("template_identity", "skill_assignment_bridge"):
                item = group.get(key)
                if item and "bridge_evidence" in item:
                    self.assertIn(item["bridge_evidence"], allowed)


if __name__ == "__main__":
    unittest.main()
