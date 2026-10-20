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
 def test_three_exact_source_digests_and_historical_boundary(self):
  self.assertEqual(len(self.r['sources']),3)
  for i,s in enumerate(self.r['sources']):
   self.assertEqual(len(s['current_quote_digest_sha256']),64)
   self.assertIsNone(s['historical_original_2006_html_sha256'])
   self.assertFalse(s['current_2026_capture_is_2006_original'])
  r=copy.deepcopy(self.r);r['sources'][1]['current_quote_digest_sha256']='not-a-hash'
  with self.assertRaises(ValueError):validate(r)
 def test_source_section_mutations_rejected(self):
  for i,tokens in enumerate(PHRASES):
   prefix='以下リリースより' if i<2 else '香颯の地（リリースより）'
   first='雨祝の森（リリースより）' if i==2 else ''
   fixture=('<html><body>ストーンエイジ '+prefix+' '+' '.join(tokens[:5])+' '+first+' '+' '.join(tokens[5:])+' ストーンエイジ■開発元 新しいマップでは</body></html>').encode()
   with self.subTest(source=i):
    self.assertEqual(extract(fixture,i)['verified_quote_fragments'],len(tokens))
    with self.assertRaises(ValueError):extract(fixture.replace(tokens[2].encode(),b'UNVERIFIED'),i)
  with self.assertRaises(ValueError):replay(self.r,[b''])
 def test_permanent_raw_report_and_two_candidate_ci_custody(self):
  import hashlib
  c=json.loads((REPORT.parent/'STONEAGE-JP2006-WORLD-GEOGRAPHY-CUSTODY-R1.json').read_text())
  a=c['passing_candidate_ci'];b=c['pinned_candidate_ci']
  self.assertEqual((a['conclusion'],b['conclusion']),('success','success'))
  self.assertNotEqual(a['artifact_id'],b['artifact_id'])
  self.assertNotEqual(a['zip_sha256'],b['zip_sha256'])
  self.assertEqual(a['raw_sha256'],b['raw_sha256'])
  raw=(REPORT.parent/'STONEAGE-JP2006-WORLD-GEOGRAPHY-CI-CANDIDATE-REPLAY-R1.json').read_bytes()
  self.assertEqual(len(raw),a['raw_bytes'])
  self.assertEqual(hashlib.sha256(raw).hexdigest(),a['raw_sha256'])
  self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),a['raw_git_blob'])
  for row in c['source_pins']:
   data=(REPORT.parents[2]/row['path']).read_bytes()
   self.assertEqual(hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(),row['git_blob'])
  self.assertEqual(c['failed_first_ci']['conclusion'],'failure')
  self.assertFalse(c['boundaries']['original_game_map_ids_validated'])

if __name__=='__main__':unittest.main()
