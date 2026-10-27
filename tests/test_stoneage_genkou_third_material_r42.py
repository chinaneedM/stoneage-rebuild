import copy,json,unittest
from tools.stoneage_genkou_third_material_r42 import SOURCE,R41,validate
class R42MaterialTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.src=json.loads(SOURCE.read_text());cls.r41=json.loads(R41.read_text())
 def test_exact_report(self):self.assertTrue(validate(self.src,self.r41)['accepted'])
 def reject(self,change):
  mutated=copy.deepcopy(self.src);change(mutated)
  with self.assertRaises(ValueError):validate(mutated,self.r41)
 def test_false_original_official(self):self.reject(lambda j:j.__setitem__('official_same_build_authenticated',True))
 def test_false_quest_claim(self):self.reject(lambda j:j.__setitem__('verified_base_quests_added',1))
 def test_forged_sha(self):self.reject(lambda j:j['receipt']['members'][3].__setitem__('sha256','0'*64))
 def test_missing_third_arg(self):self.reject(lambda j:j['receipt']['members'].pop())
 def test_misrepresented_warp(self):self.reject(lambda j:next(f for f in j['argument_comparison']['third_kgi']['fields'] if f['key']=='warpfl').__setitem__('numbers',[11214]))
 def test_misrepresented_enemy_duplicates(self):self.reject(lambda j:next(f for f in j['argument_comparison']['third_kgi']['fields'] if f['key']=='enemyno').__setitem__('numbers',[1271,1274,1281,1276,1279]))
 def test_misrepresented_delta(self):self.reject(lambda j:j['argument_comparison'].__setitem__('changed_fields',['askbattlemsg1']))
 def test_prior_R41_crossreport_tamper(self):
  old=copy.deepcopy(self.r41);old['argument_delta']['decode_candidates'][0]['fields'][0]['numbers']=[9]
  with self.assertRaises(ValueError):validate(self.src,old)
 def test_false_runtime(self):self.reject(lambda j:j['third_guard_original_reference'].__setitem__('statement_kind','RUNTIME_CONFIRMED'))
 def test_unbounded_download(self):self.reject(lambda j:j['receipt'].__setitem__('actual_range_bytes',17000000))
if __name__=='__main__':unittest.main()
