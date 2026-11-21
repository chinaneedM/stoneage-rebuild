"""PET126I cross-year player name identity is NOT official pet first release."""
import hashlib
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/"research/recovered"/name).read_text(encoding="utf-8"))
class Pet126IBounded(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.d=load("STONEAGE-PET126I-2006-2019-EIGHT-NAME-RECONCILIATION-R1.json")
    cls.prior=load("STONEAGE-PET116-TW2019-PLAYER-PET-EVIDENCE-R1.json")
    cls.year=load("STONEAGE-PET118-YEAR2019-SIX-REGION-CLASSIC-PC-BOUNDED-AUDIT-R1.json")
    cls.queue=load("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")
  def test_eight_names_and_prior_year_class_distinction(self):
    d=self.d
    names=[n for g in d["grouping"] for n in g["names"]]
    self.assertEqual(names,["奧普薩斯","利普多爾","邦克普斯","拉佛洛斯","畢格艾斯","裘比斯","阿卡西斯","洛可洛斯"])
    self.assertEqual(len(set(names)),8)
    self.assertEqual(d["exact_name_matches"],8)
    self.assertTrue(all(n in self.prior["events"][0]["mentions"] for n in names))
    self.assertEqual(d["grouping"][0]["name_2006"],"肥龍")
    self.assertEqual(d["grouping"][1]["name_2006"],"海怪")
    self.assertEqual(d["grouping"][1]["name_2019"],"海龍（暑假活動）")
  def test_do_not_override_newer_year_review_or_raise_species(self):
    d=self.d
    self.assertEqual(d["active_module"],"PET")
    self.assertTrue(d["pc_only"])
    self.assertTrue(all(d["no_promotion"].values()))
    self.assertEqual(self.year["review_status"],"SOURCE_BOUNDED_REVIEWED")
    self.assertEqual(d["preserved_state"]["year2019"],self.year["review_status"])
    self.assertEqual(self.queue["current_frontier"]["year"],2026)
    self.assertEqual(d["preserved_state"]["year2026"],"NOT_YEAR_AUDITED")
    self.assertEqual(d["preserved_state"]["pet_module"],"SOURCE_BOUNDED_PARTIAL")
    self.assertIsNone(d["preserved_state"]["completion_percent"])
    self.assertEqual(d["source_access"]["new_classic_pc_original_client_bytes"],0)
    self.assertEqual(d["source_access"]["new_original_pet_id_spr_binding"],0)
    current=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
    self.assertEqual(len(current),2709173)
    self.assertEqual(hashlib.sha1(b"blob "+str(len(current)).encode()+bytes([0])+current).hexdigest(),d["source_base"]["original_current_blob"])
if __name__=="__main__":unittest.main()
