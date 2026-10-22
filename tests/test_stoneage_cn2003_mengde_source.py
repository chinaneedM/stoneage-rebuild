import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import stoneage_cn2003_mengde_source as m


def fixture():
 head='<title>'+m.TITLE+'</title><!-- include 中间内容 begin --><b>'+m.TITLE+'</b>新浪游戏 网友投稿<!-- include 发布时间 begin -->2003-05-29 17:00<!-- include 发布时间 end --><td class=l15z>'
 pairs=[]
 for i in range(12):
  full=m.IMAGES[0]['url'] if i==9 else m.IMAGES[1]['url'] if i==11 else 'https://image2.sina.com.cn/synthetic'+str(i)+'.jpg'
  full=full.replace('https:','http:');pairs.append('<a href='+full+' target=_blank><img src='+full.replace('.jpg','s.jpg')+' border=0></a>')
 return (head+'1.等级要求：synthetic'+''.join(pairs)+'之后再去解会比较保险。<table width=520 cellpadding=0 cellspacing=0 align=center><!-- include 中间内容 end -->').encode('gb18030')


class MengdeSourceTests(unittest.TestCase):
 def report(self):return json.loads(m.REPORT.read_text())

 def test_unique_visible_business_body_dates_and_actual_full_image_pairs(self):
  raw=fixture();ex=m.article(raw);self.assertEqual(len(ex[2]),12)
  self.assertEqual(m.article(raw+b'<script>outside=1</script>'),ex)
  for changed in [raw+raw,raw.replace(b'2003-05-29 17:00',b'2003-05-30 17:00'),
   raw.replace(b'232-572_2003052917425',b'233-572_2003052917425'),raw.replace(b'synthetic',b'<script>synthetic',1),
   raw.replace(m.TITLE.encode('gb18030'),b'other')]:
   with self.assertRaises(ValueError):m.article(changed)

 def test_portal_submission_is_not_official_authorship_version_or_authenticated_history(self):
  r=self.report();m.validate(r)
  for change in [lambda d:d.update(version_profile='TW10'),lambda d:d['source'].update(official_authorship_verified=True),
   lambda d:d['source'].update(named_original_author='Wayi'),lambda d:d['source'].update(authenticated_2003_snapshot=True),
   lambda d:d['source'].update(current_bytes_authenticate_2003_original=True),lambda d:d['source'].update(exact_game_version_or_build='1.82'),
   lambda d:d['negative_boundaries'].update(recommended_60_is_hard_gate=True)]:
   d=copy.deepcopy(r);change(d)
   with self.assertRaises(ValueError):m.validate(d)

 def test_reward_order_and_conditional_bonus_are_not_cash_or_original_flags(self):
  r=self.report()
  for change in [lambda e:e.update(reward_sequence_as_reported=list(reversed(e['reward_sequence_as_reported']))),
   lambda e:e.update(reversed_first_two_warning='ALWAYS_REWARDED'),lambda e:e.update(reward_order_server_flag_or_atomic_transaction=1),
   lambda e:e['rewards'][1].update(automatic_cash_reward=True),lambda e:e['rewards'][1].update(sale_value_as_reported=3000),
   lambda e:e['rewards'][2]['stats'].update(睡眠耐性=100),lambda e:e.update(repeatability_reset_and_item_consumption='AFTER_REBIRTH')]:
   d=copy.deepcopy(r);change(d['extraction']);d['catalog_records']=m.catalog(d['extraction'])
   with self.assertRaises(ValueError):m.validate(d)

 def test_occurrences_coordinate_frames_quoted_password_and_recommendations_stay_bounded(self):
  r=self.report()
  for change in [lambda e:e.update(hard_level_gate=60),lambda e:e.update(prerequisite_as_reported=None),
   lambda e:e['village_interactions'][0].update(local_coord=[43,49]),lambda e:e['village_interactions'][1].update(occurrence='KELKE_GIRL'),
   lambda e:e['dungeon'].update(password='在梦德有卡坦'),lambda e:e['dungeon'].update(numeric_floor_count=6),
   lambda e:e['dungeon'].update(server_case_encoding_or_punctuation_match='QUOTE_REQUIRED'),
   lambda e:e['dungeon'].update(theft_targets_algorithm_probability=0.2),
   lambda e:e['story'].update(developer_intent_or_real_world_history='AUTHOR_INTENDED_CIVILIZATION'),
   lambda e:e['route_advice'].update(meat_quantity_consumption_original_id=1),
   lambda e:e.update(exact_game_build='CN2.0'),lambda e:e.update(original_map_npc_quest_item_ids=[1]),
   lambda e:e.update(original_server_runtime_verified=True)]:
   d=copy.deepcopy(r);change(d['extraction']);d['catalog_records']=m.catalog(d['extraction'])
   with self.assertRaises(ValueError):m.validate(d)

 def test_tooltips_do_not_verify_npc_identity_delivery_effect_or_original_pixels(self):
  r=self.report()
  for field in ['npc_identity_independently_visible','actual_reward_delivery_or_item_effect_tested','original_sprite_or_model','exact_build_or_native_resolution_verified']:
   d=copy.deepcopy(r);d['visual_observations'][0][field]=True
   with self.assertRaises(ValueError):m.validate(d)
  for field,value in [('sha256','0'*64),('size',[320,240]),('frames',2)]:
   d=copy.deepcopy(r);d['images'][1][field]=value
   with self.assertRaises(ValueError):m.validate(d)
  with self.assertRaises((ValueError,OSError)):m.inspect_images({'I1':b'<html>404</html>'})
  for group,field in [('early_recordpoint','nearby_row_equals_village_checkpoint'),('early_recordpoint','missing_village_row_means_no_checkpoint'),('five_brothers','reward_reset_after_rebirth_backfilled'),('five_brothers','beluorn_jilu_ecology_backfilled_to_mengde')]:
   d=copy.deepcopy(r);d['comparison'][group][field]=True
   with self.assertRaises(ValueError):m.validate(d)

 def test_all_seventeen_documentary_records_follow_seven_field_archive_contract(self):
  r=self.report();contract=json.loads((m.ROOT/m.PARENTS[-1]).read_text())['future_website']
  self.assertEqual(len(r['catalog_records']),17)
  for row in r['catalog_records']:
   self.assertTrue(set(contract['record_contract']['required']).issubset(row));self.assertIn(row['collection'],contract['required_collections']);self.assertIsNone(row['game_ids'])
  for field in contract['record_contract']['required']:
   d=copy.deepcopy(r);d['catalog_records'][0].pop(field)
   with self.assertRaises(ValueError):m.validate(d)
  for field,value in [('entity_type','ORIGINAL_MASTER'),('rights_status','RELEASE_APPROVED'),('game_ids',1)]:
   d=copy.deepcopy(r);d['catalog_records'][0][field]=value
   with self.assertRaises(ValueError):m.validate(d)

 def test_exact_parent_parser_pins_reject_equal_length_damage_and_missing_files(self):
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
