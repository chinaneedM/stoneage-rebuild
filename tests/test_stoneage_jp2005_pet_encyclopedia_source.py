import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import stoneage_jp2005_pet_encyclopedia_source as m


def fixture():
 return ('<!--↓大見出し--><h5>'+m.TITLE+'</h5><!--↑大見出し--><div class="news_txt1">2005/07/05 16:22</div>'
  +'<td class="newstext"><IMG SRC="/news/image/2005.07/20050705162235_0.jpg" WIDTH=96 HEIGHT=104>'
  +'<!-- 本文開始 -->'+''.join(m.CLAUSES)+'（TET）<!-- 本文終了 --><!-- 本文開始 -->\n\t<!-- 本文終了 --><!-- tDialy:END -->').encode('shift_jis')


class PetEncyclopediaTests(unittest.TestCase):
 def report(self):return json.loads(m.REPORT.read_text())
 def reject_extractions(self,changes):
  for change in changes:
   d=self.report();change(d['extraction']);d['catalog_records']=m.catalog(d['extraction'])
   with self.assertRaises(ValueError):m.validate(d)

 def test_unique_visible_body_date_signature_and_actual_small_image(self):
  raw=fixture();ex=m.derive(raw);self.assertEqual(m.semantic(ex),m.semantic(self.report()['extraction']))
  self.assertEqual(m.derive(raw+b'<script>outside=1</script>'),ex)
  for changed in [raw+raw,raw.replace(b'2005/07/05',b'2005/07/06'),raw.replace(b'_0.jpg',b'_0big.jpg'),raw.replace(b'WIDTH=96',b'WIDTH=192'),raw.replace(b'TET',b'GM'),raw.replace(m.TITLE.encode('shift_jis'),b'OTHER'),raw.replace(b'<!-- tDialy:END -->',b'<!-- END -->')]:
   with self.assertRaises(ValueError):m.derive(changed)
  for replacement in ('','<script>'+m.TRIGGER+'</script>'):
   changed=raw.decode('shift_jis').replace(m.TRIGGER,replacement)+'<div>'+m.TRIGGER+'</div>'
   with self.assertRaises(ValueError):m.derive(changed.encode('shift_jis'))

 def test_reported_update_is_not_official_script_build_or_actual_deployment(self):
  r=self.report();m.validate(r)
  for key in m.BOUNDARIES:
   d=copy.deepcopy(r);d['negative_boundaries'][key]=True
   with self.assertRaises(ValueError):m.validate(d)
  for key,value in [('exact_client_build','1.82'),('explicit_verbatim_manufacturer_release',True),('actual_operator_update_page_acquired',True),('current_bytes_authenticate_2005_original',True),('author_as_signed','operator')]:
   d=copy.deepcopy(r);d['source'][key]=value
   with self.assertRaises(ValueError):m.validate(d)

 def test_two_patch_stages_do_not_make_graphics_into_live_spawns_or_exact_gm_event(self):
  e=self.report()['extraction'];self.assertEqual([v['date_month_day'] for v in e['rollout']['stages']],['07-05','07-12'])
  self.reject_extractions([lambda e:e['rollout']['stages'][0].update(new_creatures_live_in_world_on_this_stage=True),
   lambda e:e['rollout']['stages'][1].update(date_month_day='07-05'),lambda e:e['rollout']['stages'][1].update(reported_new_field_level=10),
   lambda e:e['rollout']['stages'][1].update(specific_names_counts_locations_coordinates_and_spawn_rates={'count':1}),
   lambda e:e['rollout'].update(actual_deployment_verified=True),lambda e:e['rollout'].update(patch_distribution_and_world_activation_are_distinct=False),
   lambda e:e['gm_showcase'].update(exact_minute_or_timezone='JST_22_00'),lambda e:e['gm_showcase'].update(status_as_reported='COMPLETED'),
   lambda e:e['gm_showcase'].update(actual_showcase_execution_verified=True),lambda e:e['gm_showcase'].update(only_gm_pets_can_register=True)])

 def test_screen_display_registers_reported_new_pet_name_not_capture_stats_or_all_versions(self):
  self.reject_extractions([lambda e:e['encyclopedia'].update(reported_trigger='CAPTURE_OR_OWN_PET'),lambda e:e['encyclopedia'].update(reported_result='ALL_STATS_REGISTERED'),
   lambda e:e['encyclopedia'].update(capture_or_ownership_required_by_this_sentence=True),lambda e:e['encyclopedia'].update(all_possible_conditions_or_exclusions_known=True),
   lambda e:e['encyclopedia'].update(applies_to_all_old_pets_or_other_versions=True),lambda e:e['encyclopedia'].update(actual_ui_interaction_verified=True),
   lambda e:e['encyclopedia'].update(exact_button_layout_input_action_persistence_duplicates_or_storage_format='SAVE_TO_DISK'),lambda e:e.update(original_server_runtime_verified=True)])
  for group,key in [('cn20_album','same_registration_trigger_as_jp2005'),('cn20_album','cn20_scope_backfilled'),('jp_official_website_pet_catalog','is_same_as_ingame_encyclopedia'),('jp_official_website_pet_catalog','web_names_numbers_bind_this_illustration')]:
   d=self.report();d['comparison'][group][key]=True
   with self.assertRaises(ValueError):m.validate(d)

 def test_small_unlabelled_illustration_cannot_supply_species_count_sprite_or_ui(self):
  r=self.report();self.assertEqual(r['images'][0]['size'],[96,104]);self.assertEqual(r['visual_observations'][0]['kind'],'SMALL_UNCAPTIONED_CREATURE_ILLUSTRATION_NOT_UI_SCREEN')
  for key in ['pet_name_text_visible','encyclopedia_window_visible','native_species_or_original_sprite_assigned','registration_or_capture_interaction_observed','historical_2005_pixels_authenticated']:
   d=copy.deepcopy(r);d['visual_observations'][0][key]=True
   with self.assertRaises(ValueError):m.validate(d)
  self.reject_extractions([lambda e:e['new_pet_identity'].update(number_of_new_species=1),lambda e:e['image_link'].update(named_pet_or_ui_binding='CRAB_SPECIES_123'),lambda e:e['image_link'].update(unlinked_big_image_guessed_or_acquired=True)])
  with self.assertRaises((ValueError,OSError)):m.inspect_images({'I1':b'<html>404</html>'})

 def test_five_documentary_rows_keep_seven_required_fields_rights_and_no_native_ids(self):
  r=self.report();c=json.loads((m.ROOT/m.PARENTS[-1]).read_text())['future_website'];self.assertEqual(len(r['catalog_records']),5)
  for row in r['catalog_records']:
   self.assertTrue(set(c['record_contract']['required']).issubset(row));self.assertIn(row['collection'],c['required_collections']);self.assertIsNone(row['game_ids'])
  for key in c['record_contract']['required']:
   d=copy.deepcopy(r);d['catalog_records'][0].pop(key)
   with self.assertRaises(ValueError):m.validate(d)
  for key,value in [('game_ids',1),('rights_status','RELEASE_APPROVED'),('entity_type','ORIGINAL_MASTER')]:
   d=copy.deepcopy(r);d['catalog_records'][0][key]=value
   with self.assertRaises(ValueError):m.validate(d)

 def test_original_parent_and_parser_bytes_reject_missing_or_equal_length_damage(self):
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
