"""PET-DETAIL11: frozen public-PC K serializer snapshots vs original TW1 client.

This is a metadata cross-source contract, not execution of original source
code or proof of official same-build birth data. Source files were inspected
at pinned upstream commits and their exact Git blob hashes retained.
"""
import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EVIDENCE="research/pets/PET-DETAIL-EVIDENCE11-THREE-PC-K-SENDER-LINEAGES-R1.json"
DOC="docs/continuity/STONEAGE-PET-DETAIL11-THREE-PC-K-SENDERS-20261122.md"

def read(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

def git_blob(path):
    b=(ROOT/path).read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode("ascii")+b"\0"+b).hexdigest()

class ThreePCSendersAgainstTW1Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=read(EVIDENCE)
        cls.tw1=read(cls.d["early_client"]["repository_path"])
        cls.pet10=read(cls.d["prior_pet10"]["path"])

    def test_early_client_receipt_and_immutable_historical_state(self):
        e=self.d["early_client"]
        self.assertEqual(git_blob(e["repository_path"]),e["repository_git_blob"])
        self.assertEqual(e["source_exe_sha256"],self.tw1["original_source"]["exe_sha256"])
        self.assertEqual(self.tw1["k_parser"]["field_count"],20)
        m=self.tw1["k_parser"]["field_map"]
        self.assertEqual([x["token"] for x in m],list(range(2,22)))
        self.assertEqual([x["name_from_early_lineage"] for x in m][-2:],["name","free_name"])
        self.assertEqual(git_blob("docs/CURRENT-STATE.md"),self.d["original_history_scope"]["original_CURRENT_git_blob"])
        self.assertEqual(git_blob(self.d["prior_pet10"]["path"]),self.d["prior_pet10"]["git_blob"])
        self.assertEqual(self.pet10["k_packet_source_alignment"]["first_schema_difference_at_token"],20)

    def test_three_distinct_exact_snapshots_and_numeric_prefix(self):
        sources=self.d["later_community_source_snapshots"]
        self.assertEqual(len(sources),3)
        self.assertEqual(len({(x["repo"],x["ref"],x["file"]) for x in sources}),3)
        self.assertEqual(sum(bool(x["optional_fusion_macro"]) for x in sources),2)
        for x in sources:
            self.assertEqual(len(x["ref"]),40)
            self.assertEqual(len(x["git_blob"]),40)
            self.assertEqual(x["default_k_printf_integer_count"],20)
            self.assertEqual(x["default_k_data_token_20"],"transmigration_integer")
            self.assertEqual(x["default_k_data_tokens_21_22"],["name_text","custom_name_text"])
            self.assertEqual(x["default_k_format"],"K<slot>|1|19_int_fields|")
            self.assertTrue(x["serializes_numeric_fields_tokens_2_through_19_compatible_in_position"])
            self.assertFalse(x["source_historically_authenticated_early_official_server"])
            if x["optional_fusion_macro"]:
                self.assertEqual(x["fusion_k_printf_integer_count"],21)
                self.assertEqual(x["fusion_data_token_21"],"fusion_flag_integer")
            else:
                self.assertIsNone(x["fusion_k_printf_integer_count"])
                self.assertIsNone(x["fusion_data_token_21"])

    def test_first_mismatch_and_negative_claim_guards(self):
        a=self.d["cross_source_observation"]
        self.assertEqual(a["snapshots_inspected"],3)
        self.assertEqual(a["snapshots_with_unconditional_transmigration_before_names"],3)
        self.assertEqual(a["shared_early_numeric_position_prefix_token_count"],18)
        self.assertEqual(a["first_incompatible_early_token"],20)
        self.assertEqual(a["default_server_K_total_data_fields_after_mask"],21)
        self.assertEqual(a["early_client_K_total_data_fields_after_mask"],20)
        self.assertTrue(a["no_direct_full_packet_compatibility_proven"])
        self.assertFalse(a["native_runtime_test_executed"])
        self.assertFalse(a["shared_historical_ancestor_by_repo_dates_proven"])
        self.assertFalse(self.d["early_client"]["original_same_build_server_sender_found"])
        h=self.d["original_history_scope"]
        self.assertFalse(h["official_1999_2002_pet_master_obtained"])
        self.assertFalse(h["authenticated_original_official_1999_2002_K_server_sender_obtained"])
        self.assertEqual(h["new_early_official_birth_attributes_confirmed"],0)
        self.assertEqual(h["old_pet_dossiers_unchanged_count"],124)
        self.assertEqual(h["old_pet_dossiers_fully_restored_count"],0)
        self.assertEqual(h["new_official_pet_species_confirmed"],0)
        self.assertIsNone(h["overall_completion_percent"])

    def test_docs_remain_classic_pc_source_separated(self):
        s=(ROOT/DOC).read_text(encoding="utf-8")
        idx=(ROOT/"docs/pets/INDEX.md").read_text(encoding="utf-8")
        for x in self.d["later_community_source_snapshots"]:
            self.assertIn(x["repo"],s)
        self.assertIn("PET-DETAIL11",idx)
        self.assertIn('PET-DETAIL11',s)
        self.assertIn("124档案皆PARTIAL",idx)

if __name__=="__main__":
    unittest.main()
