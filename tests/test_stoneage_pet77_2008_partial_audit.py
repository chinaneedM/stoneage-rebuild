"""PET77 2008 source-bounded global official PET first-pass regression."""
import json, unittest, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"research"/"recovered"
def get(name): return json.loads((DATA/name).read_text(encoding="utf-8"))
class PET77Partial(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.a=get("STONEAGE-PET77-YEAR2008-OFFICIAL-PET-PARTIAL-SOURCE-AUDIT-R1.json")
  cls.q=get("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")
 def test_both_receipts_and_2008_open(self):
  a,q=self.a,self.q
  # The historical PET77 partial receipt is immutable; current year may advance.
  self.assertEqual((a["year"],a["year_cursor_after"]),(2008,2008))
  self.assertGreaterEqual(q["current_frontier"]["year"],2008)
  self.assertEqual(q["yearly_work_queue"][9]["research_gate"],"NOT_YEAR_AUDITED" if q["current_frontier"]["year"]==2008 else "SOURCE_BOUNDED_REVIEWED")
  self.assertFalse(a["historically_complete"])
  self.assertEqual(sum(x["id"]==a["id"] for x in q["root_source_census_receipts"]),1)
  self.assertEqual(sum(x["id"]==a["id"] for x in q["yearly_work_queue"][9]["partial_source_review_receipts"]),1)
  ids=[x["id"] for x in q["root_source_census_receipts"]]
  self.assertEqual(len(ids),len(set(ids)))
 def test_evidence_boundaries(self):
  a=self.a
  self.assertEqual((a["new_2008_original_client_bytes"],a["new_2008_native_pet_ids"],a["actual_2008_original_grant_logs"]),(0,0,0))
  self.assertIsNone(a["confirmed_global_2008_species_count"])
  self.assertEqual(set(a["region_reviews"]),{"CN","TW","JP","KR","OTHER"})
  self.assertTrue(all(x["species_count"] is None for x in a["region_reviews"].values()))
  self.assertTrue(all(a["bounds"].values()))
  self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING"))
 def test_kr_and_jp_names_not_new_species(self):
  s={x["id"]:x for x in self.a["sources"]}
  self.assertEqual(len(s),9)
  self.assertEqual(s["KR-2008-0114-ICE-CASTLE"]["claimed_new_pets"],9)
  self.assertEqual(s["KR-2008-0114-ICE-CASTLE"]["actual_native_names_found"],0)
  self.assertEqual(s["JP-2008-1111-SABER-EVOLUTION"]["original_pet_evolution_input_names"],["ベルガー","ベルイガー","ゴルシス","キングサーベル"])
  self.assertEqual(s["JP-2008-1111-SABER-EVOLUTION"]["output_native_pet_ids_found"],0)
  self.assertEqual(s["JP-2008-0715-FUKUURI"]["reused_existing_event_id"],"JP-2008-FUKUURI")
 def test_historical_current_blob_unmodified(self):
  raw=(ROOT/"docs"/"CURRENT-STATE.md").read_bytes()
  self.assertEqual(len(raw),2709173)
  self.assertEqual(hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest(),"c89e0e33537990aa2132b47c40fef49a985a935c")
if __name__=="__main__": unittest.main()
