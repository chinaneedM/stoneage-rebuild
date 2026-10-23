import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import stoneage_cn2003_zoo_rescue_source as m


def fixture():
 pairs=''.join('<a href="http://image2.sina.com.cn/gm/newgames/0303/images/dongwu0603_0'+str(i)+'.jpg" target="_blank"><img src="http://image2.sina.com.cn/gm/newgames/0303/images/dongwu0603_0'+str(i)+'s.jpg" border="0" width="150" height="113">' for i in range(1,27))
 return ('<!-- include 中间内容 begin -->'+m.TITLE+'作者：新浪游戏我要投稿<!-- include 发布时间 begin -->2003-06-03 17:58<!-- include 发布时间 end -->'
  +'<td width=500 class=l15z><span>1.等级要求：synthetic'+pairs+'伊甸地下信道第五层</td></tr></table><br><br><!-- include 中间内容 end -->').encode('gb18030')


class ZooRescueTests(unittest.TestCase):
 def report(self):return json.loads(m.REPORT.read_text())
 def reject_extractions(self,changes):
  for change in changes:
   d=self.report();change(d['extraction']);d['catalog_records']=m.catalog(d['extraction'])
   with self.assertRaises(ValueError):m.validate(d)

 def test_unique_visible_body_date_and_twenty_six_actual_image_pairs(self):
  raw=fixture();core,body=m.article(raw);self.assertEqual(m.article(raw+b'<script>outside=1</script>'),(core,body))
  for changed in [raw+raw,raw.replace(b'2003-06-03',b'2003-06-04'),raw.replace(b'_08.jpg',b'_08big.jpg'),raw.replace(b'_020.jpg',b'_020big.jpg'),raw.replace(m.TITLE.encode('gb18030'),b'OTHER')]:
   with self.assertRaises(ValueError):m.article(changed)
  for replacement in ('','<script>'+m.SAFETY+'</script>'):
   changed=raw.decode('gb18030').replace('synthetic',replacement)+'<div>'+m.SAFETY+'</div>'
   with self.assertRaises(ValueError):m.derive(changed.encode('gb18030'))

 def test_portal_authority_quest_header_and_catalogue_overlap_do_not_supply_native_ids(self):
  r=self.report();m.validate(r)
  for key in m.BOUNDARIES:
   d=copy.deepcopy(r);d['negative_boundaries'][key]=True
   with self.assertRaises(ValueError):m.validate(d)
  for key,value in [('official_authorship_verified',True),('actual_operator_script_acquired',True),('exact_client_build','1.82'),('current_bytes_authenticate_2003_original',True)]:
   d=copy.deepcopy(r);d['source'][key]=value
   with self.assertRaises(ValueError):m.validate(d)
  self.reject_extractions([lambda e:e.update(hard_level_gate=90),lambda e:e.update(prerequisite_as_reported='NONE'),lambda e:e.update(original_server_runtime_verified=True)])
  d=self.report();d['comparison']['cn20_web_pets']['web_positions_are_native_pet_ids']=True
  with self.assertRaises(ValueError):m.validate(d)

 def test_moving_sites_coordinate_frames_restart_notes_stat_qualifiers_and_duplicate_attack(self):
  ex=self.report()['extraction'];self.assertEqual([len(ex['npcs'][i]['sites_as_reported']) for i in (3,4)],[22,5])
  sites=ex['npcs'][3]['sites_as_reported'];self.assertTrue(sites[2]['restart_only_as_guide_claim']);self.assertEqual(sites[16]['coordinate_scope'],'INTERIOR_AS_NAMED_NOT_WORLD')
  boss=ex['enemy_samples'][3];self.assertEqual([v['value_as_written'] for v in boss['ordered_stat_entries'] if v['label_as_written']=='攻击力'],['500','700'])
  self.reject_extractions([lambda e:e['npcs'][3]['sites_as_reported'][2].update(restart_only_as_guide_claim=False),
   lambda e:e['npcs'][3]['sites_as_reported'][16].update(coordinate_scope='WORLD'),lambda e:e['npcs'][4].update(cycle_period_and_actual_path=60),
   lambda e:e['npcs'][4]['sites_as_reported'].reverse(),lambda e:e['enemy_samples'][3]['ordered_stat_entries'][3].update(label_as_written='防御力'),
   lambda e:e['enemy_samples'][0]['ordered_stat_entries'][1].update(value_as_written='2400'),lambda e:e['dungeon'].update(header_coordinate=[20,64]),
   lambda e:e['dungeon']['floor_pairs'][0].update(entry_local_coord=[0,64])])
  table='actors</p><table><tr><td>坐标</td><td>备注</td></tr><tr><td>（0,12）</td><td>肉店内</td></tr></table>'
  self.assertEqual(m.moving_table(table,'actors',1,0)[0]['coordinate'],[0,12])
  with self.assertRaises(ValueError):m.moving_table(table.replace('（0,12）','unknown'),'actors',1,0)
  with self.assertRaises(ValueError):m.moving_table(table+table,'actors',1,0)

 def test_target_feed_appraisal_radish_tokens_confiscation_and_ground_loss_remain_scoped(self):
  self.reject_extractions([lambda e:e['rescue_targets'][0].update(valid_target='ANY_BUIPANG'),lambda e:e['rescue_targets'][1].update(valid_target_level_as_reported=2),
   lambda e:e['rescue_targets'][0].update(pet_consumed_at_appraisal=True),lambda e:e['capture_advice'].update(encounter_or_capture_rates=1),
   lambda e:e['shell_communication'].update(consumption_or_all_other_prerequisites='CONSUMED_EACH_TALK'),
   lambda e:e['gardener_and_radish_flow'].update(spoken_tokens=['伯特','锄头','拉拉']),lambda e:e['gardener_and_radish_flow'].update(native_alias_verified=True),
   lambda e:e['gardener_and_radish_flow'].update(carrying_shovel_confiscates=['铲子']),lambda e:e['gardener_and_radish_flow'].update(carrying_red_radish_confiscates=['红萝卜']),
   lambda e:e['gardener_and_radish_flow'].update(before_rabbit_discard_shovel=False),lambda e:e['gardener_and_radish_flow'].update(radish_ground_disappears_as_reported=False)])

 def test_story_decoy_disguised_rescuers_and_pre_return_safety_reward_gate(self):
  e=self.report()['extraction'];self.assertEqual(e['rabbit_story_order'][-1]['source_occurrence'],'FOLLOWUP_AFTER_FIFTH_NOT_NUMBERED_SERVER_COUNTER')
  self.reject_extractions([lambda e:e['rabbit_story_order'][-1].update(source_occurrence='SERVER_FLAG_6'),lambda e:e['sige_story'].update(rabbit_release_plan_was_theirs=True),
   lambda e:e['sige_story'].update(zoo_training_center='OBJECTIVELY_PROVEN'),lambda e:e['clue_item_flow'][0].update(reclaimed=False),
   lambda e:e['completion_order'].update(report_lasiji_safety_to_rabbit_before_returning_three=False),
   lambda e:e['completion_order']['zoo_reward'].update(verified_numeric_level_or_stats=1),
   lambda e:e['completion_order']['armour_followup'].update(missed_safety_report_loses_armour_as_guide_claim=False),
   lambda e:e['completion_order']['armour_followup'].update(spirit_level=3),lambda e:e['completion_order']['armour_followup'].update(stats_as_written={'防':40,'敏':-10})])

 def test_named_level_one_status_sample_is_not_species_master_or_reward_execution(self):
  r=self.report();v=r['visual_observations'][1];self.assertEqual(v['displayed_pet_name'],'动物园养的拉斯基');self.assertEqual(v['displayed_stats']['耐久力'],{'current':17,'maximum':17})
  for key,value in [('displayed_level',2),('element_numeric_ratios',[7,3]),('one_displayed_pet_proves_species_initial_stats_or_growth',True),('actual_combat_handover_or_reward_verified',True),('original_sprite_animation_or_native_id_verified',True)]:
   d=copy.deepcopy(r);d['visual_observations'][1][key]=value
   with self.assertRaises(ValueError):m.validate(d)
  with self.assertRaises((ValueError,OSError)):m.inspect_images({'I1':b'<html>404</html>'})
  c=json.loads((m.ROOT/m.PARENTS[-1]).read_text())['future_website'];self.assertEqual(len(r['catalog_records']),16)
  for row in r['catalog_records']:
   self.assertTrue(set(c['record_contract']['required']).issubset(row));self.assertIn(row['collection'],c['required_collections']);self.assertIsNone(row['game_ids'])
  for key in c['record_contract']['required']:
   d=copy.deepcopy(r);d['catalog_records'][0].pop(key)
   with self.assertRaises(ValueError):m.validate(d)
  d=copy.deepcopy(r);d['catalog_records'][0]['rights_status']='RELEASE_APPROVED'
  with self.assertRaises(ValueError):m.validate(d)

 def test_parent_and_parser_original_bytes_reject_missing_or_equal_length_damage(self):
  r=self.report()
  with tempfile.TemporaryDirectory() as name:
   root=Path(name)
   for p in r['parent_pins']+[r['parser_pin']]:
    target=root/p['path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((m.ROOT/p['path']).read_bytes())
   with patch.object(m,'ROOT',root):
    m.validate(r)
    for p in r['parent_pins']+[r['parser_pin']]:
     target=root/p['path'];raw=target.read_bytes();target.write_bytes(raw[:-1]+bytes([raw[-1]^1]))
     with self.assertRaises(ValueError):m.validate(r)
     target.unlink()
     with self.assertRaises(FileNotFoundError):m.validate(r)
     target.write_bytes(raw)

if __name__=='__main__':unittest.main()
