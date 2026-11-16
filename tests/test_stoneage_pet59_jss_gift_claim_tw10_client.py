"""PET59: a 2001 player article's nine unstarred Japanese award claims cannot become official release from TW1 local art."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"research"/"recovered"

class TestPET59(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.x=json.loads((SRC/"STONEAGE-PET59-2001-JSS-PLAYER-GIFT-TW10-CLIENT-NAME-BOUNDARY-R1.json").read_text(encoding="utf-8"))
        cls.tw=json.loads((SRC/"STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json").read_text(encoding="utf-8"))
        cls.q=json.loads((SRC/"STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json").read_text(encoding="utf-8"))

    def test_source_claim_not_operator_fact_or_firsthand(self):
        x=self.x
        self.assertEqual((x["source_player_article"]["page_displayed_date"],x["source_player_article"]["byline"]),("2001-06-14","依波波"))
        self.assertIsNone(x["source_player_article"]["original_2001_html_byte_sha256"])
        self.assertEqual([z["source_article_ordinal"] for z in x["rows"]],[4,5,10,77,85,93,94,111,114])
        self.assertEqual(len(x["rows"]),9)
        self.assertTrue(all(z["player_article_JSS_gift_claim"] and not z["player_author_star_marked"] for z in x["rows"]))
        self.assertTrue(all(not z["historical_JSS_gift_issued_confirmed"] and not z["TW1_resource_proves_JP2001_deployment"] for z in x["rows"]))

    def test_exact_client_derived_source_sha_and_missing_alias(self):
        originals={z["name_as_written"]:z for z in self.tw["records"]}
        actual=[z for z in self.x["rows"] if z["tw10_exact_album_name_present"]]
        self.assertEqual(len(actual),8)
        self.assertEqual(len(self.x["rows"])-len(actual),1)
        self.assertEqual([z["player_article_name"] for z in self.x["rows"] if not z["tw10_exact_album_name_present"]],["多洛普斯"])
        self.assertEqual(sum(z["previously_considered_in_R97"] for z in actual),2)
        for z in actual:
            r=originals[z["tw10_original_album_name"]]
            self.assertEqual(r["graphic_number"],z["tw10_local_graphic"])
            self.assertEqual(r["source_row_sha256"],z["tw10_original_album_row_sha256"])
            self.assertEqual(r["spr_original_segment_sha256"],z["tw10_original_whole_SPR_sha256"])
            self.assertEqual(r["source_frame_positions"],z["tw10_original_frame_positions"])
            self.assertEqual(r["portrait_rd"]["sha256"],z["tw10_original_portrait_RD_sha256"])
            self.assertEqual(len(z["tw10_original_whole_SPR_sha256"]),64)
            self.assertFalse(r["official_live_release_confirmed"])

    def test_cursor_and_no_unearned_year_completion(self):
        x,q=self.x,self.q
        self.assertEqual(x["bounds"]["newly_explicitly_linked_TW10_original_name_SPR_candidates"],6)
        self.assertEqual((x["bounds"]["verified_actual_JP_JSS_2001_prize_gift_names"],x["bounds"]["verified_live_2001_official_pets_added"]),(0,0))
        self.assertIsNone(x["bounds"]["historical_official_species_total"])
        self.assertEqual(q["active_module"],"PET")
        self.assertGreaterEqual(q["current_frontier"]["year"],2001)
        self.assertEqual(q["current_frontier"]["status"],"OPEN_NOT_YEAR_CLOSED")
        self.assertIn(q["yearly_work_queue"][2]["research_gate"],{"NOT_YEAR_AUDITED","SOURCE_BOUNDED_REVIEWED"})
        self.assertEqual(sum(z["id"]==x["id"] for z in q["root_source_census_receipts"]),1)
        self.assertFalse(x["bounds"]["year_closed"])
        self.assertTrue(x["no_paid_marketplace_research"])
        self.assertEqual(x["historical_current_git_blob_unchanged"],"c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual((x["stage_A"],x["stage_B_wiki"],x["r79"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING"))
        self.assertIsNone(x["overall_percent"])

if __name__=="__main__":
    unittest.main()
