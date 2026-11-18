"""PET93 2013 original PC source-bound pet names, version separation and source gates."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/"research/recovered/STONEAGE-PET93-YEAR2013-CN-SNAKE-TW-KR-PC-SOURCE-GATES-R1.json"
Q=ROOT/"research/recovered/STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
class PET93(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(R.read_text(encoding="utf-8"))
        cls.q=json.loads(Q.read_text(encoding="utf-8"))
    def test_pet_year_still_open(self):
        r,q=self.r,self.q
        self.assertEqual((r["yearFrontierBefore"],r["yearFrontierAfter"]),(2013,2013))
        self.assertGreaterEqual(q["current_frontier"]["year"],2014)
        self.assertEqual(q["active_module"],"PET")
        self.assertEqual(q["yearly_work_queue"][14]["research_gate"],"SOURCE_BOUNDED_REVIEWED")
        self.assertEqual(r["reviewStatus"],"PARTIAL_NOT_YEAR_AUDITED")
        self.assertFalse(r["annualAuditComplete"])
        self.assertIsNone(r["globalPetSpeciesTotal"])
        self.assertIsNone(r["firstRelease2013SpeciesTotal"])
        self.assertTrue(q["current_frontier"]["next"].startswith("PET96:"))
    def test_five_sources_six_regions_and_negative_gates(self):
        r=self.r
        self.assertEqual(r["sourceCount"],5)
        self.assertEqual(len(r["sources"]),5)
        self.assertEqual(len({x["url"] for x in r["sources"]}),5)
        self.assertEqual(set(r["regions"]),{"CN","TW","HK_MO","KR","JP","OTHER"})
        self.assertTrue(all(r["negativeControls"].values()))
    def test_snake_lanes_and_label_cardinality(self):
        s=next(x for x in self.r["sources"] if "versionEligibility" in x)
        self.assertEqual(s["versionEligibility"]["2.5"],{"minRebirth":2,"minLevel":100})
        self.assertEqual(s["versionEligibility"]["8.5"],{"minRebirth":3,"minLevel":120})
        self.assertEqual(len(s["names"]),6)
        self.assertEqual(len(set(s["names"])),6)
        self.assertEqual(s["elementCount"],4)
        self.assertFalse(s["serverRewardsVerified"])
        self.assertEqual(s["originalClientBytes"],0)
    def test_katan_item_taiwan_later_guide_and_korean_items(self):
        s=self.r["sources"]
        cn=next(x for x in s if "questInputPets" in x)
        self.assertEqual(len(cn["questInputPets"]),4)
        self.assertEqual(cn["itemNotPet"],"火难的戒子")
        self.assertFalse(cn["firstRelease2013Verified"])
        tw=next(x for x in s if "candidates" in x and x["region"]=="TW")
        self.assertEqual([x["filename"] for x in tw["candidates"]],["Sa_Free_installation","Sa_Setup_20120113","Launch.exe"])
        self.assertIsNone(tw["sha256"])
        self.assertEqual(tw["originalBytesAcquired"],0)
        fb=next(x for x in s if "claimed2010DigiparkSourceDiscs" in x)
        self.assertEqual(fb["claimed2010DigiparkSourceDiscs"],5)
        self.assertFalse(fb["originalSourceAcquired"])
        kr=next(x for x in s if x["region"]=="KR")
        self.assertEqual(len([x for x in kr["candidates"] if x["kind"]=="PET_TRANSFORMATION_ITEM"]),2)
        self.assertEqual(kr["originalPCServiceNoticesVerified"],0)
    def test_additive_receipts_original_current_blob_and_zero_new_bytes(self):
        r,q=self.r,self.q
        ids=[x["id"] for x in q["root_source_census_receipts"]]
        self.assertIn(r["id"],ids)
        self.assertEqual(len(ids),len(set(ids)))
        self.assertIn(r["id"],[x["id"] for x in q["yearly_work_queue"][14]["partial_source_review_receipts"]])
        self.assertEqual(r["startup"]["currentGitBlob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual(set(r["sourceCustody"].values()),{0})
        self.assertEqual((q["stage_A"],q["stage_B_wiki"],q["r79"],q["overall_game_completion_percent"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING",None))
if __name__ == "__main__": unittest.main()
