"""PET126V: three-carrier bounded pet name variants checked against original-derived SHA evidence."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
R=ROOT/"research"/"recovered"
NEW=R/"STONEAGE-PET126V-TW10-CN50-WAEI2001-THREE-CARRIER-PET-NAME-VARIANTS-R1.json"

def blob_hash(p):
    b=p.read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode("ascii")+b"\0"+b).hexdigest()

class PET126VThreeCarrierSourceGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m=json.loads(NEW.read_text(encoding="utf-8"))
        cls.tw=json.loads((R/"STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json").read_text(encoding="utf-8"))
        cls.cn=json.loads((R/"STONEAGE-PET126R-CN50-PC-ORIGINAL-ALBUM-FULL-362-SLOT-SOURCE-CATALOGUE-R1.json").read_text(encoding="utf-8"))
        cls.web=json.loads((R/"STONEAGE-PET42-TW10-OPERATOR-MUSEUM-BIDIRECTIONAL-GAP-R1.json").read_text(encoding="utf-8"))

    def test_provenance_exact_source_git_blobs(self):
        for key in ("tw10","cn50","web_museum"):
            src=self.m["sources"][key]
            self.assertEqual(blob_hash(ROOT/src["path"]),src["git_blob"])
        self.assertEqual(blob_hash(ROOT/"docs"/"CURRENT-STATE.md"),
                         self.m["boundaries"]["historical_CURRENT_original_blob_sha"])
        self.assertEqual((ROOT/"docs"/"CURRENT-STATE.md").stat().st_size,2709173)

    def test_all_124_taiwan_names_share_complete_spr_hash_not_live_issuance(self):
        tw=self.tw["records"]
        cn=self.cn["records"]
        self.assertEqual(len(tw),124)
        self.assertEqual(len(cn),362)
        equal_names=0
        graphics=set()
        for x in tw:
            num=x["graphic_number"]
            ordinal=num-100250
            self.assertGreaterEqual(ordinal,0)
            self.assertLess(ordinal,181)
            self.assertNotIn(num,graphics)
            graphics.add(num)
            y=cn[ordinal]
            self.assertEqual(y["ordinal"],ordinal)
            self.assertTrue(y["TW10_retail_exact_same_SPR_segment_at_this_ordinal"])
            self.assertEqual(x["spr_original_segment_sha256"],y["same_CAB_SPR_group_hash_for_hypothesis"])
            self.assertIsNone(y["original_server_species_identifier"])
            self.assertFalse(y["CN50_name_to_SPR_native_selector_proven"])
            self.assertFalse(y["original_official_live_pet_release_proven"])
            equal_names+=x["name_as_written"]==y["label_as_compiled_GB18030"]
        s=self.m["independent_scan_summary"]
        self.assertEqual((len(graphics),equal_names,len(graphics)-equal_names),
                         (s["tw10_rows_with_cn50_same_complete_SPR_SHA256"],
                          s["same_ordinal_tw10_cn50_literal_names_exact_unicode"],
                          s["same_ordinal_tw10_cn50_literal_names_differ"]))
        self.assertEqual((len(graphics),equal_names,len(graphics)-equal_names),(124,49,75))

    def test_exact_three_nonorthographic_variants_match_third_source_names(self):
        rows=self.m["name_variant_relationships"]
        self.assertEqual(len(rows),3)
        expected={
            100320:("卡搭寶斯","卡拉寶斯","卡拉宝斯",106,"搭→拉"),
            100383:("拉可洛斯","拉可拉斯","拉可拉斯",88,"洛→拉"),
            100384:("巴洛洛克斯","邦洛洛克斯","邦洛洛克斯",55,"巴→邦")
        }
        for row in rows:
            t,c,w,n=(row[k] for k in ("tw10_original_client","cn50_preserved_client","tw2001_operator_hosted_player_museum","name_relation"))
            num=t["graphic_number"]
            self.assertIn(num,expected)
            tn,wn,cn,webord,change=expected[num]
            self.assertEqual((t["printed_name"],w["name_as_archived"],c["printed_name"],w["index_row"],n["non_orthographic_source_literal_difference"]),
                             (tn,wn,cn,webord,change))
            tw=next(v for v in self.tw["records"] if v["graphic_number"]==num)
            cr=self.cn["records"][num-100250]
            web=next(v for v in self.web["website_non_exact_client_name_rows"] if v["web_ordinal"]==webord)
            self.assertEqual((t["original_album_row_sha256"],c["original_album_row_sha256"]),
                             (tw["source_row_sha256"],cr["source_exe_row_sha256"]))
            self.assertEqual(t["full_original_SPR_segment_sha256"],c["complete_SPR_segment_sha256"])
            self.assertEqual(t["full_original_SPR_segment_sha256"],tw["spr_original_segment_sha256"])
            self.assertEqual(w["name_as_archived"],web["website_name_as_written"])
            self.assertEqual(w["as_recorded_image_url"],web["website_image_url"])
            self.assertEqual(w["source_page"],web["source_page"])
            self.assertTrue(any(x["client_graphic_number"]==num for x in web["single_edit_client_name_candidates"]))
            self.assertTrue(n["web_and_cn50_text_spellings_equivalent_after_explicit_script_conversion"])
            self.assertFalse(n["release_issued_identity_or_same_species_proven"])
            self.assertFalse(w["client_pet_identity_confirmed"])
            self.assertFalse(c["native_name_to_sprite_selector_proven"])

    def test_only_official_original_pc_evidence_and_no_species_or_progress_promotion(self):
        b=self.m["boundaries"]
        self.assertEqual(self.m["scope"],"OFFICIAL_HISTORICAL_CLASSIC_2D_PC_SOURCE_ONLY")
        self.assertEqual(b["original_proprietary_game_or_GIF_bytes_acquired_this_unit"],0)
        self.assertEqual(b["new_official_live_pet_species_verified"],0)
        self.assertTrue(b["historical_2003_1_82_5_0_server_client_compatibility_already_in_repository_not_duplicate"])
        self.assertFalse(b["PET_module_closed"])
        self.assertFalse(b["NPC_module_started"])
        self.assertEqual(b["year_2026"],"NOT_YEAR_AUDITED")
        self.assertEqual(b["stage_A"],"7_PARTIAL_2_OPEN")
        self.assertIsNone(b["overall_completion_percent"])

if __name__=="__main__":
    unittest.main()
