"""Protect project-wide two-axis policy against silent cross-conversation task drift."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/"docs"
JSON=ROOT/"research/recovered/STONEAGE-RESTORATION-TWO-AXIS-GOVERNANCE-R1.json"

class TwoAxisGovernance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(JSON.read_text(encoding="utf-8"))
        cls.protocol=(DOC/"PROJECT-CONTINUITY-PROTOCOL-R1.md").read_text(encoding="utf-8")
        cls.design=(DOC/"DESIGN-DECISIONS.md").read_text(encoding="utf-8")
        cls.module=(DOC/"RESTORATION-MODULE-FIRST-20261102.md").read_text(encoding="utf-8")
        cls.pet=(DOC/"STONEAGE-PET-CHRONOLOGICAL-RESTORATION-ORDER-R1.md").read_text(encoding="utf-8")

    def test_startup_reads_and_precedence(self):
        d=self.d
        self.assertIn("## 22. Project-wide two-axis",self.protocol)
        self.assertIn("## DD-033 —",self.design)
        for p in d["startup_required_reads"]:
            self.assertIn(p,self.protocol, p)
        self.assertIn("PET-OFFICIAL-CHRONOLOGY-01",self.protocol)
        self.assertIn("explicit user",self.protocol)
        self.assertEqual(d["source_of_truth"],"CURRENT_REMOTE_GITHUB_MAIN_AND_VERSIONED_PROTOCOL")

    def test_single_active_module_and_order(self):
        d=self.d; modules=d["modules_in_order"]
        self.assertEqual(len(modules),7)
        self.assertEqual([x["module"] for x in modules],
                ["PET","CHARACTER_NPC","MAP_WORLD","ITEM_EQUIPMENT_SHOP","QUEST_STORY","GAMEPLAY_SYSTEM","CROSS_MODULE_REVIEW"])
        self.assertEqual([x["status"] for x in modules].count("ACTIVE"),1)
        self.assertEqual(modules[0]["status"],"ACTIVE")
        self.assertTrue(all(x["status"]=="LOCKED_NOT_ACTIVE" for x in modules[1:]))
        self.assertEqual(d["architecture"]["current_active_module"],"PET")
        self.assertEqual(d["architecture"]["next_frontier"],"PET_INTEGRATED_PER_PET_COMPLETE_PROFILE_AND_OFFLINE_ATLAS")
        self.assertIn("单一",self.module)

    def test_actual_restoration_gate_not_bounded_review(self):
        d=self.d
        gate=d["pet_actual_restoration_gate_20261126"]
        self.assertIn("## 29. Actual complete pet restoration",self.protocol)
        self.assertEqual(d["architecture"]["work_axis"],"ONE_ACTIVE_CONTENT_MODULE_UNTIL_ACTUAL_COMPLETE_CONTENT_RESTORATION_AND_EXPLICIT_USER_UNLOCK")
        self.assertEqual(d["module_switch_gate"],"ACTUAL_COMPLETE_PET_ROSTER_FIELDS_ASSETS_OFFLINE_ATLAS_AND_EXPLICIT_USER_ACCEPTANCE")
        for key in ("source_bounded_review_is_not_completion","prior_closure_request_withdrawn","missing_fields_are_not_complete","explicit_user_acceptance_and_switch_required","source_bounded_delivery_receipts_retained"):
            self.assertIs(gate[key],True,key)
        self.assertIs(gate["npc_unlocked"],False)
        self.assertIsNone(gate["official_species_count"])
        self.assertEqual(gate["active_module"],"PET")
        self.assertEqual(gate["required_deliverable"],"INTEGRATED_PRIVATE_OFFLINE_VISUAL_PER_PET_ATLAS")
        self.assertEqual(set(gate["required_fields"]),{
            "identity_and_version","family","elements","initial_hp_attack_defense_agility_ranges",
            "individual_and_total_growth_ranges","innate_and_learnable_skills",
            "capture_locations_coordinates_levels","all_acquisition_methods","encyclopedia_text",
            "portrait_model_actions_directions","evolution_fusion_rebirth_riding_relations",
            "provenance_conflicts_missing_vs_not_applicable"})
        constitution=(DOC/"STONEAGE-GLOBAL-TWO-AXIS-RESTORATION-CONSTITUTION-R1.md").read_text(encoding="utf-8")
        self.assertIn("2026-11-26 实际完整复原验收",constitution)

    def test_year_axis_is_not_one_module_frontier(self):
        d=self.d
        self.assertEqual(d["architecture"]["current_research_frontier_year_provisional"],1999)
        self.assertIn("each later module restarts its own earliest year",d["architecture"]["independence"])
        self.assertIn("NOT_YEAR_AUDITED",d["unstudied_year_status"])
        self.assertIn("SOURCE_BOUNDED_REVIEWED",d["completed_year_status"])
        self.assertIn("未来",self.pet)

    def test_version_key_and_source_status(self):
        d=self.d
        self.assertEqual(d["version_identity_required_fields"],[
            "product_line_id","region_code","official_operator","server_or_service_era",
            "official_version_or_build_or_unknown","effective_date_or_interval_or_unknown"
        ])
        self.assertIn("source_locator_or_sha",d["cross_module_event_required_fields"])
        self.assertIn("reopen_trigger",d["cross_module_event_required_fields"])
        self.assertIn("DISPUTED_SOURCE",d["source_status_values"])
        self.assertIn("IN_WORLD_SOURCE_CHRONOLOGY",d["time_semantics"])

    def test_world_lore_does_not_inherit_release_date(self):
        d=self.d
        self.assertIn("actual_operator_release",d["timeline_strata"])
        self.assertIn("actual_in_world_lore",d["timeline_strata"])
        self.assertIn("marketing_or_developer_design_intent",d["timeline_strata"])
        self.assertIn("future_reconstruction_design",d["timeline_strata"])
        self.assertIn("do not prove relationship",d["history_to_gameplay_causality"])
        self.assertIn("without independent",d["identity_merge_requirements"].lower())
        self.assertTrue(d["cannot_reinterpret_as_runtime_proof"])

    def test_old_current_and_phase_unchanged(self):
        d=self.d
        self.assertEqual(d["current_state_complete_historical_git_blob_unmodified"],
                         "c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual(d["stage_A"],"7_PARTIAL_2_OPEN")
        self.assertEqual(d["stage_B_wiki"],"GATED")
        self.assertEqual(d["r79"],"PAUSED_NON_BLOCKING")
        self.assertIsNone(d["overall_completion_percent"])


    def test_stage_a_frozen_historical_prefix_survives_module_policy_updates(self):
        import hashlib
        from tools.stoneage_stage_a_review_packet import DEFAULT
        manifest=json.loads(DEFAULT.read_text(encoding="utf-8"))
        pin=next(x for x in manifest["preserved_historical_prefixes"]
                 if x["path"]=="docs/PROJECT-CONTINUITY-PROTOCOL-R1.md")
        body=(ROOT/pin["path"]).read_bytes()
        self.assertGreaterEqual(len(body),pin["bytes"])
        self.assertEqual(hashlib.sha256(body[:pin["bytes"]]).hexdigest(),pin["sha256"])

if __name__=="__main__":
    unittest.main()
