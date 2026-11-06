"""PET14: independently replay the two source tables without assuming species identity."""
import json
import unittest
from pathlib import Path
from tools.stoneage_pet14_tw10_mixed25_source_bridge import derive, REPORT, PET07, PET10

class TestPET14(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.actual=derive()
        cls.saved=json.loads(REPORT.read_text(encoding="utf-8"))
        cls.p07=json.loads(PET07.read_text(encoding="utf-8"))
        cls.p10=json.loads(PET10.read_text(encoding="utf-8"))

    def test_exact_source_derived_replay(self):
        self.assertEqual(self.actual,self.saved)
        self.assertEqual(len(self.saved["graphics"]),130)
        self.assertEqual(len({g["original_TW10_spr_numeric_graphic"] for g in self.saved["graphics"]}),130)

    def test_all_original_flags_and_alt_missing_keys_kept(self):
        s=self.saved["summary"]; a=s["mixed25_main"]; b=s["mixed25_alternative"]
        self.assertEqual([a["source_table_total_rows"],b["source_table_total_rows"]],[988,640])
        self.assertEqual([a["graphic_groups_with_PETFLG_1"],b["graphic_groups_with_PETFLG_1"]],[130,124])
        self.assertEqual([a["PETFLG_1_rows_at_TW10_graphic_keys"],b["PETFLG_1_rows_at_TW10_graphic_keys"]],[188,142])
        self.assertEqual([a["PETFLG_0_rows_at_TW10_graphic_keys"],b["PETFLG_0_rows_at_TW10_graphic_keys"]],[121,116])
        self.assertEqual([a["all_source_rows_at_TW10_graphic_keys"],b["all_source_rows_at_TW10_graphic_keys"]],[309,258])
        self.assertEqual(s["TW10_graphics_without_any_mixed25_alternative_rows"],[100454])
        self.assertEqual(s["TW10_graphics_without_mixed25_alternative_PETFLG_1_rows"],[100015,100018,100401,100432,100451,100454])
        for table,label in (("enemybase.txt","mixed25_main"),("enemybase2.txt","mixed25_alternative")):
            for r in self.saved["graphics"]:
                candidate=[x for x in self.p10["source_rows"][table] if x[2]==r["original_TW10_spr_numeric_graphic"]]
                self.assertEqual(r[label]["PETFLG_1_rows"],sum(x[3]==1 for x in candidate))
                self.assertEqual(r[label]["PETFLG_0_rows"],sum(x[3]==0 for x in candidate))
                self.assertEqual(r[label]["source_template_rows"],len(candidate))

    def test_sha_identity_and_negative_identity_bounds(self):
        self.assertEqual(self.saved["source_git_blobs"],{"PET07":"0b5f81b41a642025ab53a12884638fdee887470e","PET10":"25a37aeb134fb180e322e7dc335029b7374452d8"})
        for k,v in self.saved["evidence_boundary"].items():
            if k.startswith("original_") and k!="original_TW10_server_names_stats_or_skills_proven":
                continue
            if k in ("stage_a","stage_b_wiki","r79","overall_percent","PET07_original_pixels_observed_in_earlier_work_not_new_this_run"):continue
            self.assertIs(v,False,k)
        self.assertEqual((self.saved["summary"]["original_pixel_blocks_newly_decoded"],self.saved["summary"]["original_specimens_newly_downloaded"]),(0,0))
        self.assertIsNone(self.saved["evidence_boundary"]["overall_percent"])
        self.assertTrue(self.saved["evidence_boundary"]["PET07_original_pixels_observed_in_earlier_work_not_new_this_run"])

    def test_tampered_source_summary_rejected(self):
        altered=json.loads(json.dumps(self.saved))
        altered["graphics"][0]["mixed25_main"]["PETFLG_0_rows"]+=1
        self.assertNotEqual(self.actual,altered)

if __name__=="__main__":
    unittest.main()
