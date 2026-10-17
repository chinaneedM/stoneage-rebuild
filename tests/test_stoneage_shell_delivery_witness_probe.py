import unittest
from tools.stoneage_shell_delivery_witness_probe import derive
class WitnessTests(unittest.TestCase):
 def docs(self):return {'compilation':'弥生 日美子 仙尼亚的花 扣两点魅力', 'december_player':'<div id="newsriqi">2001-12-10</div><div id="zhuozhe_left">诗雨</div>1、北岛送贝壳任务 玛丽娜斯[114，662]弥生 萨姆吉尔[637，491]日美子 不可思议的贝壳 2、南岛','later_delivery':'2003-05-29 友谊（一）友谊（二）扣魅力一点'}
 def test_coordinate_reference_not_spawn_tile(self):
  r=derive(self.docs());self.assertEqual(r['profiles']['december_player']['reported_npc_location_references'][0]['coordinates'],[114,662]);self.assertFalse(r['current_html_authenticated_in_2001'])
 def test_article_chronology_not_footer(self):
  d=self.docs();d['december_player']=d['december_player'].replace('id="newsriqi"','id="footer"')
  with self.assertRaises(ValueError):derive(d)
 def test_wrong_location_requires_requalification(self):
  d=self.docs();d['december_player']=d['december_player'].replace('114，662','55，92')
  with self.assertRaises(ValueError):derive(d)
 def test_shell_is_not_automatically_final_reward(self):
  r=derive(self.docs());self.assertFalse(r['profiles']['december_player']['shell_is_final_reward_rather_than_intermediate_verified'])
if __name__=='__main__':unittest.main()
