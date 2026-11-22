"""PET-DETAIL17: cross-era 200/201 candidate tables must never become original skill facts."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DATA = "research/pets/PET-DETAIL-EVIDENCE17-200-201-LATE-PC-SKILL-CANDIDATE-BOUNDARY-R1.json"

def load(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8"))

def git_blob(p):
    raw = (ROOT / p).read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

class Detail17SourceCandidate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = load(DATA)

    def test_original_primary_receipt_remains_authoritative(self):
        d = self.d
        o = d["original_tw10_client"]
        self.assertEqual(git_blob(o["receipt_path"]), o["receipt_blob_sha"])
        r = load(o["receipt_path"])
        self.assertEqual(sorted(x["original_exe_compiled_ID_decimal"] for x in
            r["cross_carried_pet_skill_id_lookup"]["candidate_callers"]), [200, 201])
        self.assertEqual(o["observed_compiled_numeric_ids"], [200, 201])
        self.assertEqual(o["original_executable_sha256"], r["source"]["original_executable_sha256"])
        self.assertIsNone(o["original_skill_names"]["200"])
        self.assertIsNone(o["original_skill_names"]["201"])
        self.assertIsNone(o["original_skill_effects"]["200"])
        self.assertIsNone(o["original_skill_effects"]["201"])
        self.assertFalse(o["same_build_numeric_identity_to_later_community_master_confirmed"])
        self.assertFalse(o["private_TW10_original_binary_reopened_during_this_work"])
        self.assertIsNone(o["authenticated_original_server_petskill_master"])
        self.assertIsNone(o["authenticated_original_server_W_packet"])

    def test_three_pinned_tables_have_two_candidates_not_three_independent_witnesses(self):
        d = self.d
        self.assertEqual(len(d["later_community_PC_skill_tables"]), 3)
        self.assertEqual(len({x["repository"] for x in d["later_community_PC_skill_tables"]}), 2)
        self.assertIsNone(d["independent_lineage_count_confirmed"])
        self.assertTrue(d["dependent_copy_or_derivative_possible"])
        self.assertEqual(d["later_community_ID_name_candidates"], {"200": "加工", "201": "料理"})
        assert_fields = [(12, 6, [29, 30]), (9, 4, [29, 30]), (12, 6, [36, 37])]
        for s, (count, idcol, linenos) in zip(d["later_community_PC_skill_tables"], assert_fields):
            self.assertEqual(len(s["commit"]), 40)
            self.assertEqual(len(s["git_blob"]), 40)
            self.assertEqual(s["record_width"], count)
            self.assertEqual(s["id_column_zero_based"], idcol)
            self.assertEqual([x["line"] for x in s["rows"]], linenos)
            self.assertEqual([(x["id"], x["name"]) for x in s["rows"]], [(200, "加工"), (201, "料理")])
            for x in s["rows"]:
                self.assertEqual(x["callback"], "PETSKILL_Merge")
                self.assertEqual(x["field_context"], 2)
                self.assertEqual(x["target_class"], 0)

    def test_historical_boundary_and_no_pet_claim_promotion(self):
        d = self.d
        g = d["guardrails"]
        self.assertEqual(git_blob("docs/CURRENT-STATE.md"), g["current_state_git_blob_preserved"])
        self.assertEqual(git_blob(d["dated_skill_name_only_player_context"]["path"]),
                         d["dated_skill_name_only_player_context"]["git_blob_sha"])
        self.assertTrue(g["original_client_200_201_names_remain_null"])
        self.assertTrue(g["later_community_ID_equals_original_era_ID_not_proven"])
        self.assertTrue(g["community_source_lines_are_not_early_official_server_masters"])
        self.assertTrue(g["data_schemas_must_use_per_file_id_columns"])
        self.assertTrue(g["original_TW10_124_pet_dossiers_all_partial"])
        self.assertEqual(g["original_TW10_historically_complete_pet_dossiers"], 0)
        self.assertIsNone(g["overall_percent"])
        f = d["findings"]
        for name in ("fully_verified_early_official_ID_to_name_pairs",
                     "early_official_birth_skill_names_new", "original_era_Server_skill_masters_new",
                     "original_era_server_skill_W_packets_new", "newly_confirmed_official_pet_species"):
            self.assertEqual(f[name], 0)
        self.assertIn("PET-DETAIL17", (ROOT / "docs/pets/INDEX.md").read_text(encoding="utf-8"))
        self.assertIn("同构建", (ROOT / "docs/continuity/STONEAGE-PET-DETAIL17-200-201-LATE-PC-SKILL-CROSSWALK-20261122.md").read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
