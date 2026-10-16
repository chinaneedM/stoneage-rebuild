"""Adversarial source-custody/negative-promotion tests for STAGE-A-NPC-CONTENT-BOUNDARY-01."""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/recovered/STONEAGE-STAGE-A-NPC-CONTENT-BOUNDARY-R1.json"

def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()

def count_line(data: str, key: str) -> int:
    for line in data.splitlines():
        if line.startswith("COUNT|" + key + "|"):
            return int(line.split("|")[-1])
    raise AssertionError("missing source count: " + key)

class NPCContentBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = json.loads(REPORT.read_text(encoding="utf-8"))
        cls.sources = {k:(ROOT / entry["path"]).read_text(encoding="utf-8")
                       for k,entry in cls.audit["source_pins"].items()}

    def test_original_source_pins_git_blob_and_size(self):
        self.assertEqual(len(self.audit["source_pins"]), 13)
        for key,pin in self.audit["source_pins"].items():
            with self.subTest(source=key):
                raw = (ROOT / pin["path"]).read_bytes()
                self.assertEqual(len(raw), pin["bytes"])
                self.assertEqual(git_blob(raw), pin["git_blob"])

    def test_create_and_transport_partitions(self):
        c = self.audit["derived_counts"]
        s = self.sources["npc_secondary"]
        g = self.sources["npc_graph"]
        self.assertEqual(c["create_refs"], count_line(g, "create_blocks_raw"))
        for name,field in [
            ("unambiguous_refs", "create_refs_resolved_unambiguous"),
            ("ambiguous_refs", "create_refs_ambiguous"),
            ("secondary_file_args", "create_refs_file_argument_resolved_unambiguous"),
            ("secondary_inline_args", "create_refs_inline_argument_resolved_unambiguous"),
            ("secondary_no_args", "create_refs_no_argument_resolved_unambiguous"),
            ("missing_secondary_files", "secondary_argument_files_missing")]:
            self.assertEqual(c[name], count_line(s,field))
        self.assertEqual(c["create_refs"],c["unambiguous_refs"] + c["ambiguous_refs"])
        self.assertEqual(c["unambiguous_refs"],c["secondary_file_args"] + c["secondary_inline_args"] + c["secondary_no_args"])
        self.assertGreater(c["ambiguous_refs"],0)
        self.assertGreater(c["missing_secondary_files"],0)

    def test_presentation_and_window_missing_configs_cannot_vanish(self):
        c = self.audit["derived_counts"]
        p = self.sources["npc_presentation"]
        w = self.sources["npc_window"]
        for name,field in [
            ("townpeople_refs","TownPeople|refs"),("townpeople_resolved_files","TownPeople|resolved_files"),
            ("townpeople_inline","TownPeople|inline"),("townpeople_noargs","TownPeople|noarg"),
            ("townpeople_missing_files","TownPeople|missing_files"),
            ("signboard_refs","SignBoard|refs")]:
            self.assertEqual(c[name], count_line(p,field))
        for name,field in [("windowman_refs","refs"),("windowman_resolved_configs","resolved_conff"),
                           ("windowman_missing_configs","missing_conff_file")]:
            self.assertEqual(c[name],count_line(w,field))
        self.assertEqual(c["townpeople_refs"],sum(c[k] for k in
            ("townpeople_resolved_files","townpeople_inline","townpeople_noargs","townpeople_missing_files")))
        self.assertEqual(c["windowman_refs"],c["windowman_resolved_configs"]+c["windowman_missing_configs"])
        self.assertGreater(c["windowman_missing_configs"],0)
        self.assertIn("never applies either value",self.sources["window_semantics"])

    def test_npcenemy_and_conditional_travel_are_versioned(self):
        c = self.audit["derived_counts"]
        self.assertEqual(c["npcenemy_refs"],count_line(self.sources["npc_enemy"],"create_refs_npcenemy"))
        self.assertEqual(c["npcenemy_resolved_args"],count_line(self.sources["npc_enemy"],"argument_files_resolved"))
        self.assertEqual(c["npcenemy_prompts"],count_line(self.sources["npc_enemy"],"askbattle_prompt_blocks"))
        self.assertEqual(c["npcenemy_refs"],c["npcenemy_resolved_args"])
        self.assertEqual(c["warpman_spatial_candidates"],count_line(self.sources["dialogue_warp"],"WarpMan:candidate_edges"))
        m = re.search(r"^FUNCTIONSET_USAGE\|WarpMan\|refs=(\d+)\|",self.sources["npc_secondary"],re.M)
        self.assertIsNotNone(m)
        self.assertEqual(c["warpman_refs"],int(m.group(1)))
        self.assertEqual(c["keyitem_matching_create_rows"],count_line(self.sources["npc_key_refs"],"matching_create_rows"))

    def test_original_window_wire_shape_is_not_quest_content(self):
        matrix=self.sources["v1_matrix"]
        self.assertIn("C→S | `WN` | 5 ints + 1 string",matrix)
        self.assertIn("S→C | `WN` | 4 ints + 1 string",matrix)
        self.assertIn("zero standalone core files",self.sources["v1_client"])
        self.assertIn("LATER_DERIVED_ATTRIBUTION_NOT_EARLY_QUEST_RESTORATION",self.sources["keyitem_award"])
        a=self.audit
        self.assertFalse(a["stage_a_accepted"])
        self.assertFalse(a["original_server_content_recovered"])
        self.assertEqual(a["stage_b_gate"],"GATED")
        self.assertIsNone(a["historical_restoration_percentage"])
        self.assertEqual(len(a["content_surfaces"]),7)
        self.assertEqual(len(a["critical_playflow"]),6)
        self.assertTrue(all("reopen" in x and x["missing"] for x in a["content_surfaces"]))
        self.assertTrue(all(x["evidence_role"] != "V1_DIRECT_SERVER_CONTENT" for x in a["content_surfaces"]))

    def test_finite_next_not_savedata_helper_exhaustion(self):
        self.assertEqual(self.audit["next_priority"],"STAGE-A-REVIEW-BLOCKER-TRIAGE-01")
        self.assertTrue(any("R79" in x for x in self.audit["explicit_prohibitions"]))

if __name__ == "__main__":
    unittest.main()
