"""Stage A blocker triage: source custody, nine-family gate and negative promotions."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/recovered/STONEAGE-STAGE-A-BLOCKER-TRIAGE-R1.json"

class StageABlockerTriageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = json.loads(REPORT.read_text(encoding="utf-8"))
        cls.sources = {
            k: (ROOT / pin["path"]).read_bytes()
            for k, pin in cls.audit["source_pins"].items()
        }
        cls.jsons = {k: json.loads(v) for k, v in cls.sources.items() if k in
                     ("stage_a", "portfolio", "world", "rules", "capture", "npc", "ui", "ui_resource")}

    def test_source_bytes_and_git_blob_exact(self):
        self.assertEqual(len(self.audit["source_pins"]), 10)
        for key, pin in self.audit["source_pins"].items():
            with self.subTest(key=key):
                body = self.sources[key]
                # The phase gate is an append-only living document. Keep the
                # historical pinned prefix exact while allowing dated additions.
                if key == "phase_gate":
                    self.assertGreaterEqual(len(body), pin["bytes"])
                    body = body[:pin["bytes"]]
                self.assertEqual(len(body), pin["bytes"])
                preamble = b"blob " + str(len(body)).encode("ascii") + bytes([0])
                self.assertEqual(hashlib.sha1(preamble + body).hexdigest(), pin["git_blob"])

    def test_nine_immutable_family_gates_not_promoted(self):
        prior = self.jsons["stage_a"]
        prior_gates = {row["id"]: row["portfolio_gate"] for row in prior["families"]}
        self.assertEqual(len(prior_gates), 9)
        self.assertEqual(self.audit["system_gates"], prior_gates)
        self.assertEqual(self.audit["system_family_count"], 9)
        self.assertEqual(list(prior_gates.values()).count("OPEN"), 2)
        self.assertFalse(self.audit["stage_a_accepted"])
        self.assertFalse(self.audit["joint_review_completed"])
        self.assertEqual(self.audit["stage_b_gate"], "GATED")

    def test_four_world_routes_retained_with_version_limits(self):
        w = self.jsons["world"]
        self.assertEqual(len(w["cells"]), 24)
        self.assertEqual(self.audit["world_checkpoint_count"], 24)
        self.assertEqual(len(w["routes"]), 4)
        observed = [
            {key: row[key] for key in ("ordinal", "milestones", "requires_shop",
                       "requires_warpman", "classic_coordinate_reachable")}
            for row in w["routes"]
        ]
        audited = [
            {key: row[key] for key in ("ordinal", "milestones", "requires_shop",
                       "requires_warpman", "classic_coordinate_reachable")}
            for row in self.audit["world_route_evidence"]
        ]
        self.assertEqual(audited, observed)
        self.assertEqual([x["milestones"] for x in audited],
                         ["COMBAT", "COMBAT", "COMBAT>SHOP>WARPMAN",
                          "SHOP>COMBAT>WARPMAN"])
        self.assertTrue(all(not x["original_route_proven"] and
                            x["version_role"]=="LATER_RECOVERED"
                            for x in self.audit["world_route_evidence"]))

    def test_representative_flows_not_historical_proofs(self):
        self.assertEqual(len(self.audit["integrated_playflow_profiles"]), 7)
        self.assertEqual(len(self.jsons["npc"]["content_surfaces"]), 7)
        self.assertEqual(len(self.jsons["rules"]["seams"]), 8)
        self.assertEqual(self.jsons["capture"]["automatic_pet_construction"],
                         "OPEN_EVIDENCE_LIMITED_EXPLICIT_STATE_REQUIRED")
        for p in self.audit["integrated_playflow_profiles"]:
            with self.subTest(profile=p["id"]):
                self.assertFalse(p["original_playthrough_certified"])
                self.assertTrue(p["material_absence"] and p["next_evidence"])
                self.assertTrue(set(p["dependencies"]).issubset(self.audit["system_gates"]))
        self.assertFalse(self.audit["new_original_server_payload_obtained"])
        self.assertFalse(self.audit["original_quest_restored"])

    def test_named_reopen_conditions_and_nonblocking_savedata(self):
        self.assertEqual(len(self.audit["blockers"]), 5)
        for b in self.audit["blockers"]:
            self.assertTrue(b["reopen"])
            self.assertTrue(b["gap"])
            self.assertTrue(set(b["affected"]).issubset(self.audit["system_gates"]))
        r79 = [b for b in self.audit["blockers"] if "R79" in b["id"]]
        self.assertEqual(len(r79),1)
        self.assertEqual(r79[0]["priority"],"PAUSED_NON_BLOCKING")
        self.assertIsNone(self.audit["historical_restoration_percentage"])
        self.assertEqual(self.audit["next_priority"],"STAGE-A-CONSOLIDATED-REVIEW-PACKET-01")
        self.assertGreaterEqual(len(self.audit["no_promotion"]),8)

if __name__ == "__main__":
    unittest.main()
