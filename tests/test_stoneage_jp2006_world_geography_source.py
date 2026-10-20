import copy,json,unittest
from tools.stoneage_jp2006_world_geography_source import REPORT,PHRASES,extract,validate,replay
class WorldGeography(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=json.loads(REPORT.read_text())
 def rejected(self,keys,value):
  r=copy.deepcopy(self.r);cur=r
  for k in keys[:-1]:cur=cur[k]
  cur[keys[-1]]=value
  with self.assertRaises(ValueError):validate(r)
 def test_archive_world_nodes(self):
  validate(self.r)
  self.assertEqual(len(self.r['nodes']),6)
  self.rejected(['nodes',1,'game_ids'],[100])
  self.rejected(['nodes',2,'coordinate'],[5,10])
 def test_map_lineage_is_jp2006_not_early(self):
  self.rejected(['boundaries','early_jss1999_map_membership'],True)
  self.rejected(['boundaries','tw10_original_map_membership'],True)
  self.rejected(['boundaries','real_2006_server_update_trace_verified'],True)
 def test_dungeon_conditional_branch_not_forged_key(self):
  self.rejected(['relations',2,'actual_entry_conditions'],['NEED_FIRE_STONE'])
  self.rejected(['content','boss_name'],'FIRE_KING')
  self.rejected(['content','fire_species_roster'],['KNOWN_SPECIES'])
 def test_source_section_mutations_rejected(self):
  for i,tokens in enumerate(PHRASES):
   prefix='以下リリースより' if i<2 else '香颯の地（リリースより）'
   first='雨祝の森（リリースより）' if i==2 else ''
   fixture=('<html><body>ストーンエイジ '+prefix+' '+' '.join(tokens[:5])+' '+first+' '+' '.join(tokens[5:])+' ストーンエイジ■開発元 新しいマップでは</body></html>').encode()
   with self.subTest(source=i):
    self.assertEqual(extract(fixture,i)['verified_quote_fragments'],len(tokens))
    with self.assertRaises(ValueError):extract(fixture.replace(tokens[2].encode(),b'UNVERIFIED'),i)
  with self.assertRaises(ValueError):replay(self.r,[b''])
if __name__=='__main__':unittest.main()
