import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import stoneage_tw2002_werewolf_source as m


def fixture():
 head='<h1>'+m.TITLE+'</h1><span class="GN-lbox3C">（GNN 記者  報導） 2002-09-13 21:06:37</span>'
 body='<!-- 新聞內容 --><div>在石器虛擬的 synthetic<br /><br />狼人寵平時是 synthetic<br /><br />除了新增變身 synthetic<br /><br />預計推出第一 synthetic</div><!-- 新聞內容結束 -->'
 gallery='<!-- 圖片區塊 -->'+''.join('<img src="'+v['url']+'" name="gnnPIC" title="" alt="">' for v in m.IMAGES)+'<!-- 圖片區塊結束 -->'
 return (head+body+gallery).encode()


class WerewolfSourceTests(unittest.TestCase):
 def report(self):return json.loads(m.REPORT.read_text())

 def test_unique_visible_body_byline_paragraphs_and_actual_small_image_links(self):
  raw=fixture();body,parts=m.article(raw);self.assertEqual(len(parts),4)
  self.assertEqual(m.article(raw+b'<script>outside=1</script>'),(body,parts))
  for changed in [raw+raw,raw.replace(b'2002-09-13',b'2019-08-20'),raw.replace(b'/S/2KU/',b'/B/2KU/'),
   raw.replace('狼人寵平時是'.encode(),'滿月夜晚才是'.encode()),raw.replace('<!-- 新聞內容 -->'.encode(),b'<script>'),
   raw.replace(m.TITLE.encode(),b'other')]:
   with self.assertRaises(ValueError):m.article(changed)

 def test_publication_capture_failed_current_intake_and_region_inference_remain_separate(self):
  r=self.report();m.validate(r)
  for change in [lambda d:d.update(version_profile='TW10'),lambda d:d['source'].update(capture='20020913210637'),
   lambda d:d['source'].update(visible_publication='2019-08-20'),lambda d:d['source'].update(current_article_request_status=200),
   lambda d:d['source'].update(current_article_body_acquired=True),lambda d:d['source'].update(current_body_archive_equality_verified=True),
   lambda d:d['source'].update(named_reporter='Wayi'),lambda d:d['source'].update(official_authorship_verified=True),
   lambda d:d['source'].update(authenticated_2002_original_bytes=True),lambda d:d['negative_boundaries'].update(capture_is_publication_date=True)]:
   d=copy.deepcopy(r);change(d)
   with self.assertRaises(ValueError):m.validate(d)

 def test_battle_transition_not_moon_gate_playable_human_numeric_strength_or_original_skill(self):
  r=self.report()
  for change in [lambda e:e['werewolf'].update(reported_transition='FULL_MOON'),
   lambda e:e['werewolf'].update(lunar_phase_or_clock_condition='NIGHT'),lambda e:e['werewolf'].update(reverse_transition_on_battle_end=True),
   lambda e:e['werewolf'].update(skill_label_as_written='暗月變身'),lambda e:e['werewolf'].update(actual_cast_action_cost_duration_or_skill_id=1),
   lambda e:e['werewolf'].update(stats_growth_elements_and_native_pet_id={'attack':999}),
   lambda e:e['werewolf'].update(original_form_sprite_or_model_ids=[1,2]),lambda e:e.update(region_or_exact_server_build_authenticated=True)]:
   d=copy.deepcopy(r);change(d['extraction']);d['catalog_records']=m.catalog(d['extraction'])
   with self.assertRaises(ValueError):m.validate(d)

 def test_sale_plan_bundle_contents_and_phone_conditions_do_not_become_wild_catch_or_price(self):
  r=self.report()
  for change in [lambda e:e['werewolf_acquisition'].update(purchase_price=360),lambda e:e['werewolf_acquisition'].update(pet_count_as_reported=2),
   lambda e:e['werewolf_acquisition'].update(actual_sale_or_redemption_executed=True),lambda e:e['werewolf_acquisition'].update(current_world_instances_or_capture_probability=10000),
   lambda e:e['werewolf_acquisition'].update(media_label_authenticates_exact_pet_build_or_first_release=True),
   lambda e:e['werewolf_acquisition']['phone_offer'].update(actual_fulfillment_or_pet_redemption_precondition=True),
   lambda e:e['first_card_pack'].update(release_status_as_written='已推出'),lambda e:e['first_card_pack'].update(exact_pack_launch_date_or_actual_execution='2002-09-19')]:
   d=copy.deepcopy(r);change(d['extraction']);d['catalog_records']=m.catalog(d['extraction'])
   with self.assertRaises(ValueError):m.validate(d)

 def test_card_game_dice_beasts_and_unnamed_small_illustrations_stay_scoped(self):
  r=self.report()
  for change in [lambda e:e['card_product_context'].update(dice_mechanic='MMO_DAMAGE_RNG'),
   lambda e:e['card_product_context'].update(designer_is_verified_sole_mmo_creator=True),lambda e:e['first_card_pack'].update(in_game_pet_count_from_140=140),
   lambda e:e['first_card_pack'].update(beast_medium_redemption_or_native_ids=[1,2]),
   lambda e:e['first_card_pack'].update(beast_stats_skills_or_element_proportions=[10,0,0,0]),
   lambda e:e['gallery'].update(forms_or_beast_names_assigned_by_order=True),lambda e:e.update(original_server_runtime_verified=True)]:
   d=copy.deepcopy(r);change(d['extraction']);d['catalog_records']=m.catalog(d['extraction'])
   with self.assertRaises(ValueError):m.validate(d)
  for change in [lambda d:d['images'][0].update(full_original_acquired=True),lambda d:d['images'][1].update(size=[640,480]),
   lambda d:d['visual_observations'][1].update(assigned_to_named_fire_beast=True),lambda d:d['visual_observations'][0].update(in_game_form_transition_observed=True),
   lambda d:d['comparison']['cn30_special_skills'].update(t_prefix_school_donation_or_dismount_rules_backfilled=True),
   lambda d:d['comparison']['jp2005_candy'].update(gm_transformation_candy_is_werewolf_pet_skill=True)]:
   d=copy.deepcopy(r);change(d)
   with self.assertRaises(ValueError):m.validate(d)
  with self.assertRaises((ValueError,OSError)):m.inspect_images({'I1':b'<html>404</html>'})

 def test_ten_documentary_rows_have_all_seven_contract_fields_without_native_ids_or_rights(self):
  r=self.report();c=json.loads((m.ROOT/m.PARENTS[-1]).read_text())['future_website'];self.assertEqual(len(r['catalog_records']),10)
  for row in r['catalog_records']:
   self.assertTrue(set(c['record_contract']['required']).issubset(row));self.assertIn(row['collection'],c['required_collections']);self.assertIsNone(row['game_ids'])
  for field in c['record_contract']['required']:
   d=copy.deepcopy(r);d['catalog_records'][0].pop(field)
   with self.assertRaises(ValueError):m.validate(d)
  for field,value in [('entity_type','ORIGINAL_MASTER'),('game_ids',1),('rights_status','RELEASE_APPROVED')]:
   d=copy.deepcopy(r);d['catalog_records'][0][field]=value
   with self.assertRaises(ValueError):m.validate(d)

 def test_original_parent_and_parser_bytes_cannot_be_missing_or_changed_at_equal_length(self):
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
