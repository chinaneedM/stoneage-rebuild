"""Verify source-bounded seven-name classic PC album crosswalk."""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
def load(p):
    return json.loads((ROOT/p).read_text(encoding="utf-8"))

class TestPetDetail35(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e=load("research/pets/PET-DETAIL-EVIDENCE35-CN2002-2003-NAME-TO-CN50-ALBUM-BRIDGE-R1.json")
        cls.cn=load("research/recovered/STONEAGE-PET126R-CN50-PC-ORIGINAL-ALBUM-FULL-362-SLOT-SOURCE-CATALOGUE-R1.json")
        cls.y=load("research/recovered/STONEAGE-PET61-CN2002-SA30-SA40-OPERATOR-PLAYER-PET-EVIDENCE-R1.json")
        cls.r=load("research/recovered/STONEAGE-PET25-OFFICIAL-RELEASE-ROSTER-R1.json")
        cls.s=load("research/recovered/STONEAGE-PET66-2003-TW6-CN7-PET-SOURCE-R1.json")

    def test_compiled_album_source_census(self):
        allrows=self.cn["records"]
        later=[r for r in allrows if r["ordinal"]>=181]
        self.assertEqual((len(allrows),len(later)),(362,181))
        self.assertEqual(len({r["label_as_compiled_GB18030"] for r in later}),181)
        self.assertEqual(sum(bool(r["same_CAB_SPR_group_for_hypothesis_present"]) for r in later),66)
        self.assertEqual(allrows[353]["label_as_compiled_GB18030"],"宠物蛋")

    def test_seven_literally_matching_but_non_native_rows(self):
        records=self.e["records"]
        self.assertEqual(len(records),7)
        self.assertEqual(len({x["name"] for x in records}),7)
        for x in records:
            with self.subTest(name=x["name"]):
                found=[r for r in self.cn["records"] if r["label_as_compiled_GB18030"]==x["name"]]
                self.assertEqual(len(found),1)
                r=found[0]
                self.assertEqual(r["ordinal"],x["local_album_ordinal"])
                self.assertEqual(r["source_exe_row_sha256"],x["original_exe_row_sha256"])
                self.assertEqual(r["source_exe_row_offset"],x["original_exe_row_offset"])
                self.assertEqual(r["source_raw_first_i32"],x["local_first_i32_not_pet_id"])
                self.assertEqual(r["source_raw_trailing_u32"],x["local_tail_u32_not_verified_selector"])
                self.assertFalse(r["same_CAB_SPR_group_for_hypothesis_present"])
                self.assertFalse(r["CN50_name_to_SPR_native_selector_proven"])
                self.assertFalse(x["native_graphic_link_verified"])
                self.assertFalse(x["same_deployment_verified"])
                self.assertFalse(x["original_official_pet_id_verified"])
                self.assertFalse(x["actual_live_grant_verified_by_this_join"])

    def test_early_sources_are_distinct_and_non_transferable(self):
        player_names={x["player_name"] for x in self.y["source_claim_new_exact_player_year_beast_names"]}
        rows=self.e["records"]
        self.assertEqual({x["name"] for x in rows if x["grade"]=="PLAYER_NAME_CLAIM"},player_names)
        self.assertEqual(len(player_names),4)
        releases={x["record_id"]:x["official_name_as_written"] for x in self.r["confirmed_official_release_records"]}
        docs=[x for x in rows if x["grade"]=="OPERATOR_RELEASE_DOCUMENT_EVENT"]
        self.assertEqual(len(docs),2)
        self.assertTrue(all(releases[x["sourceRecord"]]==x["name"] for x in docs))
        suz=next(x for x in self.s["primary_source_records"] if x["id"]=="CN_20031217_SUZAKU_AUCTION")
        self.assertIn("菲奇亚",suz["printed_pet_names"])
        self.assertEqual(next(x for x in rows if x["name"]=="菲奇亚")["grade"],"CN70_AUCTION_PRELAUNCH_NOT_DELIVERY")
        self.assertFalse(self.e["chronology_alert"]["proof_of_2002_or_5_0_live_release"])

    def test_active_scope_and_no_species_promotion(self):
        self.assertEqual(self.e["scope"],"CLASSIC_PC_ONLY")
        self.assertEqual(self.e["active_module"],"PET")
        self.assertEqual(self.e["counts"]["original_same_build_pet_ids_newly_verified"],0)
        self.assertEqual(self.e["counts"]["live_grants_newly_verified"],0)
        self.assertIsNone(self.e["overall_percent"])

if __name__=="__main__":
    unittest.main()
