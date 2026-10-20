import copy,json,unittest
from tools.stoneage_jp2009_guild_hakuen_source import REPORT,PHRASES,extract,validate,replay
class GuildHakuenSource(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=json.loads(REPORT.read_text(encoding='utf8'))
 def fails(self,keys,action):
  r=copy.deepcopy(self.r);target=r
  for key in keys[:-1]:target=target[key]
  target[keys[-1]]=action
  with self.assertRaises(ValueError):validate(r)
 def test_archive_and_guild_source_scope(self):
  validate(self.r);self.assertEqual(len(self.r['records']),7)
  self.fails(['boundaries','cross_region_tw_cn_family_guild_identity_proven'],True)
  self.fails(['guild','guild_creation_prerequisites'],{'price':10})
  self.fails(['boundaries','server_executed_or_deployed_proven'],True)
 def test_hakuen_token_and_bag_count_conflict(self):
  self.assertEqual(self.r['hakuen']['ticket_price_gstone'],400)
  self.fails(['hakuen','bag_visible_named_rows'],7)
  self.fails(['hakuen','bag_seventh_name'],'INVENTED')
  self.fails(['boundaries','gstone_equals_gash_or_stone'],True)
 def test_stamp_thresholds_and_first_subsequent_rewards(self):
  self.assertEqual([x['count'] for x in self.r['hakuen']['stamps']],[5,10,15])
  self.fails(['limited_events','first_reward','player_xp_multiplier'],1.3)
  self.fails(['limited_events','shards_per_exchange'],0)
  self.fails(['limited_events','repeat_reward','duration_minutes'],60)
 def test_lucky_rare_enemy_venues_stay_15_and_temporary(self):
  self.assertEqual(len(self.r['limited_events']['mentioned_spawns']),15)
  self.fails(['limited_events','mentioned_spawns'],self.r['limited_events']['mentioned_spawns'][:-1])
  self.fails(['boundaries','spawns_are_original_tw10_world'],True)
  self.fails(['boundaries','spawn_probability_or_enemy_id_proven'],True)
 def test_historical_original_html_is_not_current_http(self):
  self.assertIsNone(self.r['sources'][0]['original_2009_capture_sha256'])
  self.fails(['sources',0,'original_official_notice_html_sha256'],'a'*64)
  self.fails(['boundaries','raw_html_or_original_images_in_git'],True)
 def test_current_source_digest_cannot_be_promoted_or_forged(self):
  r=copy.deepcopy(self.r);r['sources'][0]['current_release_core_sha256']='incorrect'
  with self.assertRaises(ValueError):validate(r)
  r=copy.deepcopy(self.r);r['sources'][0]['current_release_digest_does_not_authenticate_original_2009_html']=False
  with self.assertRaises(ValueError):validate(r)
 def test_published_body_mutation_and_source_enclosure(self):
  marker='メーカー発表文の内容をそのまま掲載しています'
  end='※画像は、実際とは異なる場合があります。ご了承ください。'
  page=('<html><body>'+marker+' '+' '.join(PHRASES)+' ギルドシステム '+end+'</body></html>').encode()
  self.assertEqual(extract(page)['verified_literal_fragments'],len(PHRASES))
  for phrase in ['白炎チケット400Gstone','スタンプ15回','全7種類','はぐれシロベアル','5つ渡した方','15分間キャラクターの取得経験値1.3倍']:
   with self.subTest(phrase=phrase):
    with self.assertRaises(ValueError):extract(page.replace(phrase.encode(),b'CHANGED'))
  with self.assertRaises(ValueError):replay(self.r,b'<html>incomplete</html>')
 def test_candidate_dual_ci_derived_custody_and_native_git_pins(self):
  import hashlib
  from pathlib import Path
  path=REPORT.parent
  c=json.loads((path/'STONEAGE-JP2009-GUILD-HAKUEN-CUSTODY-R1.json').read_text())
  self.assertEqual(c['source_contract'],'stoneage.jp2009_guild_hakuen.source_contract.r1')
  self.assertEqual(len(c['candidate_ci']),2)
  self.assertTrue(all(x['conclusion']=='success' for x in c['candidate_ci']))
  self.assertNotEqual(c['candidate_ci'][0]['artifact_id'],c['candidate_ci'][1]['artifact_id'])
  member_bytes=[(path/n).read_bytes() for n in ['STONEAGE-JP2009-GUILD-HAKUEN-CI-CANDIDATE-REPLAY-R1.json','STONEAGE-JP2009-GUILD-HAKUEN-CI-PINNED-REPLAY-R1.json']]
  self.assertEqual(member_bytes[0],member_bytes[1])
  for b in member_bytes:
   self.assertEqual(len(b),c['raw_derived']['bytes'])
   self.assertEqual(hashlib.sha256(b).hexdigest(),c['raw_derived']['sha256'])
   self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),c['raw_derived']['git_blob'])
  for pin in c['source_pins']:
   b=(REPORT.parents[2]/pin['path']).read_bytes()
   self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),pin['git_blob'])
  self.assertFalse(c['boundaries']['2009_actual_server_execution_verified'])
  self.assertFalse(c['boundaries']['original_2009_press_bytes_recovered'])
  self.assertFalse(c['boundaries']['bag_seventh_type_resolved'])

 def test_ci_custody_distinguishes_full_html_mutation_from_stable_release_core(self):
  import hashlib
  c=json.loads((REPORT.parent/'STONEAGE-JP2009-GUILD-HAKUEN-CUSTODY-R1.json').read_text())
  new=(REPORT.parent/'STONEAGE-JP2009-GUILD-HAKUEN-CI-CUSTODY-REPLAY-R1.json').read_bytes()
  old=(REPORT.parent/'STONEAGE-JP2009-GUILD-HAKUEN-CI-PINNED-REPLAY-R1.json').read_bytes()
  self.assertNotEqual(old,new)
  self.assertEqual(len(new),c['custody_ci']['raw_bytes'])
  self.assertEqual(hashlib.sha256(new).hexdigest(),c['custody_ci']['raw_sha256'])
  self.assertEqual(hashlib.sha1(b'blob '+str(len(new)).encode()+b'\0'+new).hexdigest(),c['custody_ci']['raw_git_blob'])
  a,b=json.loads(old),json.loads(new)
  self.assertNotEqual(a['current_http_sha256'],b['current_http_sha256'])
  self.assertEqual(a['release_digest'],b['release_digest'])
  for k in a.keys() - {'current_http_sha256'}:self.assertEqual(a[k],b[k])
  self.assertEqual(c['custody_ci']['operator_body_digest'],a['release_digest'])
  self.assertFalse(c['custody_ci']['compared_with_candidate']['raw_json_equal'])

if __name__=='__main__':unittest.main()
