"""PET-DETAIL03: 2003 official operator reported GM prize vs 124 TW10/362 CN50 source rows."""
import hashlib
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/pets/PET-DETAIL-EVIDENCE03-CN2003-GM-ROLE-BRIDGE-R1.json"
def load(path): return json.loads(path.read_text(encoding="utf-8"))
def git_blob(path):
    data=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(data)).encode("ascii")+b"\0"+data).hexdigest()
class PetDetail03OperatorAward(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out=load(REPORT)
        pins=cls.out["source_pins"]
        for pin in pins.values():
            assert git_blob(ROOT/pin["path"])==pin["git_blob"], pin
        cls.cn=load(ROOT/pins["CN50_preserved_exe_compiled_362"]["path"])
        cls.tw=load(ROOT/pins["TW10_catalogue_permanent_ids"]["path"])
        cls.year=load(ROOT/pins["contemporaneous_operator_GM_2003_PET68"]["path"])
    def test_operator_report_role_not_native_server_log(self):
        reward=self.year["first_party_reported_live_pet_prize"]
        self.assertEqual(reward["name"],"波比")
        self.assertEqual(reward["exchange_input_actual_reported"],"奇娜")
        self.assertEqual(reward["two_other_eligible_exchange_inputs_as_promised"],["多鲁宝","洛卡伦恩"])
        self.assertFalse(reward["raw_original_award_database_proven"])
        self.assertEqual(reward["actual_reported_exchange_date"],"2003-11-12")
        self.assertEqual([x["original_operator_literal"] for x in self.out["records"]],
                         ["波比","奇娜","多鲁宝","洛卡伦恩"])
        roles=[x["operator_2003_event_role"] for x in self.out["records"]]
        self.assertTrue(roles[0].startswith("OPERATOR_REPORTED_ACTUAL_GM_AWARD"))
        self.assertTrue(roles[1].startswith("OPERATOR_REPORTED_ACTUAL_EXCHANGE"))
        self.assertTrue(all(x.startswith("ELIGIBLE_") for x in roles[2:]))
    def test_original_client_matches_are_rederived_and_not_same_server_pet(self):
        self.assertEqual(len(self.cn["records"]),362)
        self.assertEqual(len(self.tw["catalog_entries"]),124)
        expected=[(None,None),("PET-000075",94),("PET-000081",100),("PET-000091",110)]
        for row,(tw_id,slot) in zip(self.out["records"],expected):
            nm=row["original_operator_literal"]
            cn=[x for x in self.cn["records"] if x["label_as_compiled_GB18030"]==nm]
            tw=[x for x in self.tw["catalog_entries"] if x["display_name_simplified"]==nm]
            self.assertEqual(len(cn),int(slot is not None))
            self.assertEqual(len(tw),int(tw_id is not None))
            self.assertEqual(row["name_absent_from_checked_124_TW10_and_362_CN50_album_rows"],slot is None)
            if slot is not None:
                source=row["original_CN50_preserved_compiled_client_source_literal"]
                self.assertEqual(source["album_slot_zero_based"],slot)
                self.assertEqual(source["source_exe_row_sha256"],cn[0]["source_exe_row_sha256"])
                self.assertEqual(source["original_exe_row_offset"],cn[0]["source_exe_row_offset"])
                self.assertEqual(source["original_same_CAB_SPR_sha_if_ordinal_guess"],cn[0]["same_CAB_SPR_group_hash_for_hypothesis"])
                self.assertFalse(source["original_name_to_SPR_selector_proven"])
                self.assertIsNone(source["actual_official_same_deployment_pet_id"])
                self.assertEqual(row["original_TW10_client_source_exact_or_simplified_name_candidate"]["catalog_pet_id"],tw_id)
                profile=load(ROOT/tw[0]["machine_dossier_path"])
                self.assertFalse(profile["actual_official_pet_identity"]["official_living_pet_release_proven"])
                self.assertIsNone(profile["actual_official_pet_identity"]["source_pet_id"])
                self.assertIsNone(profile["skills"]["innate_at_acquisition"])
                self.assertIsNone(profile["growth"]["growth_rate"])
                self.assertEqual(profile["combat_stats"]["status"],"OPEN_NOT_PROVEN")
            else:
                self.assertIsNone(row["original_CN50_preserved_compiled_client_source_literal"])
                self.assertIsNone(row["original_TW10_client_source_exact_or_simplified_name_candidate"])
            self.assertIsNone(row["assigned_new_permanent_PET_id"])
            self.assertIsNone(row["historical_2003_original_native_source_pet_id"])
            self.assertIsNone(row["original_2003_PC_pet_skills"])
            self.assertIsNone(row["original_2003_PC_level1_stats"])
            self.assertIsNone(row["original_2003_PC_growth"])
            self.assertIsNone(row["original_2003_PC_graphic_binding"])
            self.assertFalse(row["authentic_2003_operator_server_logs_obtained"])
            self.assertTrue(row["no_identity_promotion_from_text_or_cross_build"])
    def test_gates_and_index_links(self):
        cnt=self.out["source_rederived_counts"]
        self.assertEqual((cnt["documentary_named_roles"],cnt["matched_exact_CN50_names"],cnt["matched_TW10_display_names"],cnt["not_present_in_two_checked_catalogues"]),(4,3,3,1))
        self.assertEqual((cnt["new_permanent_PET_ids"],cnt["fully_completed_pet_profiles_added"],cnt["new_authentic_2003_CNpc_master_rows"]),(0,0,0))
        self.assertEqual(self.tw["counts"]["assigned_catalog_pet_ids"],124)
        self.assertEqual(self.tw["policy"]["next_unassigned_catalog_pet_id"],"PET-000125")
        self.assertEqual(git_blob(ROOT/"docs/CURRENT-STATE.md"),self.out["grade_boundary"]["historic_CURRENT_blob_unchanged"])
        self.assertEqual(self.out["grade_boundary"]["year_2026"],"NOT_YEAR_AUDITED")
        self.assertIsNone(self.out["grade_boundary"]["overall_percent"])
        self.assertTrue(self.out["grade_boundary"]["operator_report_of_actual_award_is_documentary_evidence_not_native_server_log"])
        self.assertTrue(self.out["grade_boundary"]["absence_of_BOBI_not_negative_proof_of_historical_release"])
        view=(ROOT/"docs/pets/CN2003-OPERATOR-AWARD-SOURCE-CROSSWALK.md").read_text(encoding="utf-8")
        self.assertIn("OBS-CN2003-GM-BOBI-0001",view)
        self.assertIn("不分配PET-000125",view)
        for pet_id,filename in (("PET-000075","TW10-G100344.md"),("PET-000081","TW10-G100350.md"),("PET-000091","TW10-G100360.md")):
            self.assertIn(pet_id,view)
            self.assertIn("CN2003-OPERATOR-AWARD-SOURCE-CROSSWALK.md",(ROOT/"docs/pets"/filename).read_text(encoding="utf-8"))
        self.assertIn("CN2003-OPERATOR-AWARD-SOURCE-CROSSWALK.md",(ROOT/"docs/pets/INDEX.md").read_text(encoding="utf-8"))
if __name__=="__main__": unittest.main()
