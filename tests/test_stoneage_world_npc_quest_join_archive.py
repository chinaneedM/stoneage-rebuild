import copy,hashlib,json,unittest
from tools.stoneage_world_npc_quest_catalog import ROOT,RAW,WITNESS,CATALOG,build_catalog,validate_catalog
class ArchiveTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=build_catalog()
 def test_exact_catalog_replay(self):self.assertEqual(json.loads((ROOT/CATALOG).read_text()),self.r)
 def test_fixed_scope_and_active_item_names(self):
  self.assertEqual((len(self.r['npcs']),len(self.r['maps']),len(self.r['items']),len(self.r['event_records'])),(2,2,2,6))
  self.assertEqual([i['label']for i in self.r['items']],['不可思議的貝殼','仙尼亞的花'])
 def reject(self,key,value):
  r=copy.deepcopy(self.r);r[key]=value
  with self.assertRaises(ValueError):validate_catalog(r)
 def test_no_original_version_promotion(self):self.reject('original_tw10_quest_restored',True)
 def test_no_complete_logic_from_item_atoms(self):self.reject('complete_quest_logic_verified',True)
 def test_guide_coordinates_not_spawn_tiles(self):self.reject('guide_coordinates_are_source_spawn_tiles',True)
 def test_no_completion_from_static_exchange(self):self.reject('original_server_executed',True)
 def test_do_not_conflate_shell_with_flower(self):
  r=copy.deepcopy(self.r);r['items'][0]['item_id']=2415
  with self.assertRaises(ValueError):validate_catalog(r)
 def test_custody_and_history_prefixes(self):
  receipt=json.loads((ROOT/'research/recovered/STONEAGE-WORLD-NPC-QUEST-ACCEPTANCE-R1.json').read_text())
  for f,p in receipt['reports'].items():self.assertEqual(hashlib.sha256((ROOT/f).read_bytes()).hexdigest(),p['sha256'])
  for f,p in receipt['continuity_prefixes'].items():
   b=(ROOT/f).read_bytes();self.assertGreater(len(b),p['bytes']);self.assertEqual(hashlib.sha256(b[:p['bytes']]).hexdigest(),p['sha256'])
if __name__=='__main__':unittest.main()
