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
        self.assertIn("PET-OFFICIAL-CHRONOLOGY-01",d["architecture"]["next_frontier"])
        self.assertIn("单一",self.module)

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
