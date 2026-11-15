import sys,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"tools"))
from stoneage_pet_official_release_lookup import load,search
class PET26(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.old,cls.new=load()
 def test_global_count_is_unknown(self):
  a,b=self.old,self.new
  self.assertEqual(a["counts"]["release_documentary_records"],24)
  self.assertEqual(len(b["new_japan_classic_official_release_events"]),4)
  self.assertEqual(b["counts"]["combined_release_events_not_species"],28)
  self.assertIsNone(b["counts"]["global_individual_species_count"])
 def test_new_official_launches_are_not_community_pets(self):
  rows=self.new["new_japan_classic_official_release_events"]
  self.assertEqual(sum(r["identity_kind"]=="NAMED_PET" for r in rows),3)
  self.assertEqual({r["official_name_as_written_or_null"] for r in rows if r["official_name_as_written_or_null"]},{"フクゥーリ","ハクエン","コクエン"})
  self.assertTrue(all(not r["private_server_provenance"] for r in rows))
  self.assertTrue(all(r["region"]=="JP" and not r["native_gameplay_personally_run"] for r in rows))
 def test_japan_company_snapshots_not_added_as_229_records(self):
  self.assertEqual([x["publisher_reported_species"] for x in self.new["japan_official_version_species_count_snapshots"]],[200,229])
  self.assertTrue(all(not x["itemized_individual_pet_names"] for x in self.new["japan_official_version_species_count_snapshots"]))
 def test_evolution_base_names_not_new_species(self):
  assert len(self.new["japan_2008_existing_base_evolution_records"])==4
  self.assertTrue(all(not x["is_four_new_named_species"] for x in self.new["japan_2008_existing_base_evolution_records"]))
 def test_queries_and_unverified_taiwan(self):
  self.assertEqual(len(search(self.old,self.new,region="JP")),4)
  self.assertEqual(len(search(self.old,self.new,region="CN")),20)
  self.assertEqual(len(search(self.old,self.new,region="KR")),4)
  self.assertEqual(len(search(self.old,self.new,region="TW")),0)
  self.assertEqual(len(search(self.old,self.new,region="TW",name="狼人",leads=True)),1)
  self.assertEqual(len(search(self.old,self.new,name="コクエン")),1)
 def test_sources_links_and_original_current_preserved(self):
  b=self.new;s={x["id"] for x in b["sources"]}
  self.assertEqual(len(s),11)
  for key in ("new_japan_classic_official_release_events","japan_2008_existing_base_evolution_records","japan_official_version_species_count_snapshots","japan_taiwan_prelaunch_or_mechanic_leads"):
   self.assertTrue(all(set(x["source_ids"])<=s for x in b[key]))
  self.assertEqual(b["preserved_current_state_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
if __name__=="__main__":unittest.main()
