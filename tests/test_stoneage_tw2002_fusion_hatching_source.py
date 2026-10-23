import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import stoneage_tw2002_fusion_hatching_source as m


def fixture():
 head='<h1>'+m.TITLE+'</h1><span class="GN-lbox3C">（GNN 記者  報導） 2002-11-14 21:41:11</span>'
 body='<!-- 新聞內容 --><div>寵物養成的線上 synthetic<br /><br />此外華義國際還 synthetic<br /><br />從「石器時代- synthetic<br /><br />除了外型和能力 synthetic</div><!-- 新聞內容結束 -->'
 gallery='<!-- 圖片區塊 -->'+''.join('<img src="'+u+'" name="gnnPIC" title="" alt="">' for u in m.GALLERY)+'<!-- 圖片區塊結束 -->'
 return (head+body+gallery).encode()


class FusionHatchingSourceTests(unittest.TestCase):
 def report(self):return json.loads(m.REPORT.read_text())

 def reject_extractions(self,changes):
  r=self.report()
  for change in changes:
   d=copy.deepcopy(r);change(d['extraction']);d['catalog_records']=m.catalog(d['extraction'])
   with self.assertRaises(ValueError):m.validate(d)

 def test_unique_visible_body_byline_order_and_eight_actual_small_references(self):
  raw=fixture();body,parts=m.article(raw);self.assertEqual(len(parts),4)
  self.assertEqual(m.article(raw+b'<script>outside=1</script>'),(body,parts))
  for changed in [raw+raw,raw.replace(b'2002-11-14',b'2019-08-21'),raw.replace(b'/S/2KU/',b'/B/2KU/'),
   raw.replace('此外華義國際還'.encode(),'另一段'.encode()),raw.replace('<!-- 新聞內容 -->'.encode(),b'<script>'),
   raw.replace(m.TITLE.encode(),b'other'),raw.replace(b'0000092628.JPG',b'0000092629.JPG')]:
   with self.assertRaises(ValueError):m.article(changed)
  self.assertEqual([m.GALLERY[i] for i in (0,7)],[v['url'] for v in m.IMAGES])

 def test_publication_capture_current_failure_region_and_numeric_version_are_separate(self):
  r=self.report();m.validate(r)
  changes=[lambda d:d.update(version_profile='TW10'),lambda d:d['source'].update(capture='20021114214111'),
   lambda d:d['source'].update(visible_publication='2019-08-21'),lambda d:d['source'].update(current_article_request_status=200),
   lambda d:d['source'].update(current_article_body_acquired=True),lambda d:d['source'].update(current_body_archive_equality_verified=True),
   lambda d:d['source'].update(named_reporter='Wayi'),lambda d:d['source'].update(official_authorship_verified=True),
   lambda d:d['source'].update(authenticated_2002_original_bytes=True)]+[
   lambda d,k=k:d['negative_boundaries'].update({k:True}) for k in m.BOUNDARIES]
  for change in changes:
   d=copy.deepcopy(r);change(d)
   with self.assertRaises(ValueError):m.validate(d)
  self.reject_extractions([lambda e:e['release'].update(numeric_version_in_body='5.0'),
   lambda e:e['release'].update(exact_deployment_date_or_successful_server_execution='2002-11-14'),
   lambda e:e['release'].update(marketing_third_generation_is_filial_generation=True),
   lambda e:e['third_generation'].update(previous_two_generations_are_two_specific_client_versions=['1.0','2.0'])])

 def test_three_different_pets_egg_and_feed_do_not_invent_species_recipe_or_consumption(self):
  self.reject_extractions([lambda e:e['fusion_hatching'].update(input_pet_count=2),
   lambda e:e['fusion_hatching'].update(egg_count_as_reported=3),
   lambda e:e['fusion_hatching'].update(distinctness_species_or_individual_criterion='THREE_DISTINCT_SPECIES'),
   lambda e:e['fusion_hatching'].update(input_sex_level_rebirth_or_kinship_requirement={'sex':'MALE_FEMALE'}),
   lambda e:e['fusion_hatching'].update(drug_or_feed_item_ids_recipe_and_quantity={'food':1}),
   lambda e:e['fusion_hatching'].update(feeding_interval_hatching_duration_or_offline_clock=3600),
   lambda e:e['fusion_hatching'].update(input_consumption_failure_probability_success_rate_and_retry={'success':1}),
   lambda e:e['fusion_hatching'].update(offspring_species_selection_inheritance_or_model_composition='MIX_HEAD_BODY_TAIL'),
   lambda e:e['fusion_hatching'].update(egg_transfer_inventory_slot_capacity_persistence='SAVED_IN_ITEM_SLOT'),
   lambda e:e['fusion_hatching'].update(reported_stage_order=list(reversed(e['fusion_hatching']['reported_stage_order'])))])

 def test_category_restrictions_credit_and_advertising_do_not_authenticate_game_entities(self):
  self.reject_extractions([lambda e:e['third_generation'].update(named_species_list=['狼人']),
   lambda e:e['third_generation'].update(restriction_scope='ALL_PETS_ALL_VERSIONS'),
   lambda e:e['third_generation'].update(capture_or_quest_acquisition_as_reported=True),
   lambda e:e['third_generation'].update(native_species_ids_stats_growth_skills=[1]),
   lambda e:e['third_generation'].update(original_model_or_sprite_ids=[1]),
   lambda e:e['design_credit'].update(sole_mmo_creator_or_formula_author_verified=True),
   lambda e:e['advertising_context'].update(lyrics_extracted=True),
   lambda e:e['advertising_context'].update(game_bgm_or_fusion_hatching_sound_binding_verified=True),
   lambda e:e['advertising_context'].update(audio_bytes_acquired=True),lambda e:e.update(original_server_runtime_verified=True)])
  for group,field in [('jp2008_evolution','same_mechanism_as_tw2002_fusion'),
   ('jp2008_evolution','four_saber_pet_labels_or_failure_level1_backfilled'),
   ('tw2002_werewolf','werewolf_or_card_beasts_are_third_generation_fusion_outputs'),
   ('tw2002_werewolf','human_wolf_battle_transition_is_fusion_or_hatching'),
   ('tw2002_werewolf','same_artist_credit_means_same_native_asset_id')]:
   d=self.report();d['comparison'][group][field]=True
   with self.assertRaises(ValueError):m.validate(d)

 def test_two_event_photos_are_not_pet_models_gameplay_or_pixel_authenticated_people(self):
  r=self.report()
  for field in ['named_pet_or_third_generation_species_assigned','in_game_fusion_or_hatching_observed',
   'original_sprite_model_or_animation','exact_person_identity_from_pixels_alone']:
   d=copy.deepcopy(r);d['visual_observations'][0][field]=True
   with self.assertRaises(ValueError):m.validate(d)
  for field,value in [('full_original_acquired',True),('historical_2002_pixels_authenticated',True),('size',[640,480]),('sha256','0'*64)]:
   d=copy.deepcopy(r);d['images'][1][field]=value
   with self.assertRaises(ValueError):m.validate(d)
  with self.assertRaises((ValueError,OSError)):m.inspect_images({'I1':b'<html>404</html>'})
  self.reject_extractions([lambda e:e['gallery'].update(pet_names_or_models_assigned_by_order=True)])

 def test_nine_documentary_rows_have_seven_required_fields_and_no_native_ids(self):
  r=self.report();c=json.loads((m.ROOT/m.PARENTS[-1]).read_text())['future_website'];self.assertEqual(len(r['catalog_records']),9)
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
