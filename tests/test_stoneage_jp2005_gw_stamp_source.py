import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import stoneage_jp2005_gw_stamp_source as m


def fixture():
 head='<!--↓大見出し--><h5>'+m.TITLE+'</h5><!--↑大見出し--><div class="news_txt1">2005/04/15 19:02</div><td class="newstext">'
 pair='<A href="/news/image/2005.04/20050415190236_0big.jpg"><IMG SRC="/news/image/2005.04/20050415190236_0.jpg" WIDTH=180 HEIGHT=135>'
 body='<!-- 本文開始 -->ボーステックから営業譲渡され synthetic（Seirou）footer<!-- 本文終了 -->'
 return (head+pair+body+'<!-- 本文開始 -->\n\t<!-- 本文終了 --><!-- tDialy:END -->').encode('shift_jis')


class GWStampSourceTests(unittest.TestCase):
 def report(self):return json.loads(m.REPORT.read_text())
 def reject_extractions(self,changes):
  for change in changes:
   d=self.report();change(d['extraction']);d['catalog_records']=m.catalog(d['extraction'])
   with self.assertRaises(ValueError):m.validate(d)

 def test_visible_unique_nonempty_body_date_full_link_and_signed_tail(self):
  raw=fixture();body=m.article(raw);self.assertEqual(m.article(raw+b'<script>outside=1</script>'),body)
  self.assertNotIn('footer',body)
  for changed in [raw+raw,raw.replace(b'2005/04/15',b'2005/04/16'),raw.replace(b'0big.jpg',b'1big.jpg'),
   raw.replace(m.TITLE.encode('shift_jis'),b'OTHER'),raw.replace('ボーステック'.encode('shift_jis'),b'<script>'),
   raw.replace('<!-- 本文開始 -->\n\t<!-- 本文終了 -->'.encode('shift_jis'),'<!-- 本文開始 -->another real body<!-- 本文終了 -->'.encode('shift_jis'))]:
   with self.assertRaises(ValueError):m.article(changed)

 def test_publication_and_reported_schedule_are_not_original_bytes_build_or_execution(self):
  r=self.report();m.validate(r)
  changes=[lambda d:d.update(version_profile='TW10'),lambda d:d['source'].update(explicit_verbatim_manufacturer_release=True),
   lambda d:d['source'].update(actual_operator_event_page_acquired=True),lambda d:d['source'].update(current_bytes_authenticate_2005_original=True),
   lambda d:d['source'].update(exact_client_build='1.82'),lambda d:d['source'].update(author_as_signed='operator')]+[
   lambda d,k=k:d['negative_boundaries'].update({k:True}) for k in m.BOUNDARIES]
  for change in changes:
   d=copy.deepcopy(r);change(d)
   with self.assertRaises(ValueError):m.validate(d)
  self.reject_extractions([lambda e:e['event'].update(actual_event_execution_verified=True),
   lambda e:e['event'].update(window_month_day=['04-29','05-10']),
   lambda e:e['event'].update(exact_hours_maintenance_or_timezone='JST_00_TO_24'),
   lambda e:e['event'].update(server_scope_or_account_payment_requirements='ALL_FREE')])

 def test_completed_first_quest_required_to_progress_not_visit_or_reward_only(self):
  self.reject_extractions([lambda e:e['quests'][1].update(progress_prerequisite='VISIT_FOUR_VILLAGES'),
   lambda e:e['quests'][1].update(prerequisite_scope='FINAL_REWARD_ONLY'),
   lambda e:e['quests'][1].update(numeric_level_requirement=60),
   lambda e:e['quests'][0].update(village_count=3),
   lambda e:e['quests'][0].update(named_villages_order_coordinates_npcs_or_map_ids=['サムギル','ジャジャ','マリナス','カルターナ']),
   lambda e:e['quests'][0].update(stamp_count_item_identity_consumption_and_storage={'count':4}),
   lambda e:e['quests'][0].update(no_possible_prerequisites_in_original_server_proven=True),
   lambda e:e['quests'][1].update(concrete_maps_order_npcs_and_stamp_count=[1]),
   lambda e:e.update(repeatability_reset_and_server_quest_flags='DAILY_REPEAT')])

 def test_named_pink_tiger_level_one_reward_does_not_supply_master_or_challenge_item(self):
  self.reject_extractions([lambda e:e['pet_reward'].update(name_as_written='粉红虎'),
   lambda e:e['pet_reward'].update(reported_level=10),lambda e:e['pet_reward'].update(shape_as_reported='竜型'),
   lambda e:e['pet_reward'].update(color_as_reported='黄色'),
   lambda e:e['pet_reward'].update(grant_quantity_repeatability_or_per_account_limit=1),
   lambda e:e['pet_reward'].update(wild_habitat_or_capture_eligibility='FOUR_VILLAGES'),
   lambda e:e['pet_reward'].update(stats_growth_skills_elements_native_id_or_original_sprite={'attack':100}),
   lambda e:e['pet_reward'].update(cross_region_alias_or_same_native_species='TW10_PINK_TIGER'),
   lambda e:e['quests'][1].update(reward_name_quantity_effect_and_original_id='モモトラ'),
   lambda e:e.update(original_server_runtime_verified=True)])
  for group,field in [('jss2001_venues','four_venue_villages_are_gw_four_villages'),
   ('jss2001_venues','old_reception_npcs_coordinates_or_direction_backfilled'),
   ('jp2005_treasure','same_collection_event_or_reward'),('jp2005_treasure','light_spirit_npc_crystal_drop_trade_repeatability_backfilled')]:
   d=self.report();d['comparison'][group][field]=True
   with self.assertRaises(ValueError):m.validate(d)

 def test_static_world_screen_and_navigation_labels_do_not_identify_pet_or_runtime(self):
  r=self.report();self.assertEqual(len(r['visual_observations'][0]['bottom_navigation_labels']),7)
  for field in ['momotora_identity_or_pink_tiger_assigned','stamp_or_quest_text_visible','reward_delivery_or_event_execution_observed',
   'navigation_clicks_or_feature_behavior_verified','original_sprite_model_animation_or_client_build_verified','historical_2005_pixels_authenticated']:
   d=copy.deepcopy(r);d['visual_observations'][0][field]=True
   with self.assertRaises(ValueError):m.validate(d)
  for field,value in [('size',[180,135]),('sha256','0'*64),('frames',2)]:
   d=copy.deepcopy(r);d['images'][0][field]=value
   with self.assertRaises(ValueError):m.validate(d)
  with self.assertRaises((ValueError,OSError)):m.inspect_images({'I1':b'<html>404</html>'})
  self.reject_extractions([lambda e:e['image_link'].update(screenshot_named_pet_binding='モモトラ')])

 def test_six_documentary_rows_have_seven_required_fields_and_no_native_ids(self):
  r=self.report();c=json.loads((m.ROOT/m.PARENTS[-1]).read_text())['future_website'];self.assertEqual(len(r['catalog_records']),6)
  for row in r['catalog_records']:
   self.assertTrue(set(c['record_contract']['required']).issubset(row));self.assertIn(row['collection'],c['required_collections']);self.assertIsNone(row['game_ids'])
  for field in c['record_contract']['required']:
   d=copy.deepcopy(r);d['catalog_records'][0].pop(field)
   with self.assertRaises(ValueError):m.validate(d)
  for field,value in [('entity_type','ORIGINAL_MASTER'),('game_ids',1),('rights_status','RELEASE_APPROVED')]:
   d=copy.deepcopy(r);d['catalog_records'][0][field]=value
   with self.assertRaises(ValueError):m.validate(d)

 def test_parent_and_parser_bytes_cannot_be_missing_or_changed_at_equal_length(self):
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

 def test_custody_rejects_missing_changed_reused_or_authority_promoted_evidence(self):
     receipt=m.verify_custody()
     with tempfile.TemporaryDirectory() as name:
         root=Path(name);out=root/f'research/recovered/{m.STEM}-CUSTODY-R1.json'
         for p in receipt['permanent_pins']:
             target=root/p['path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((m.ROOT/p['path']).read_bytes())
         out.write_text(json.dumps(receipt));m.verify_custody(root)
         for p in receipt['permanent_pins']:
             target=root/p['path'];raw=target.read_bytes();target.write_bytes(raw[:-1]+bytes([raw[-1]^1]))
             with self.assertRaises(ValueError):m.verify_custody(root)
             target.unlink()
             with self.assertRaises(FileNotFoundError):m.verify_custody(root)
             target.write_bytes(raw)
         changes=[lambda d:d.update(content_commit='0'*40),lambda d:d.update(content_tree='0'*40),
                  lambda d:d.update(candidate_branch='main'),lambda d:d.update(server_execution_verified=True),
                  lambda d:d.update(current_bytes_authenticate_2005_original=True),lambda d:d.update(actual_operator_event_page_acquired=True),
                  lambda d:d['runs'].pop(),lambda d:d['runs'].append(d['runs'][0]),lambda d:d['runs'][0].update(conclusion='failure'),
                  lambda d:d['runs'][0].update(id=1),lambda d:d['runs'][0].update(name='OTHER'),
                  lambda d:d['jobs_and_artifacts']['main'].update(job=1),lambda d:d['jobs_and_artifacts']['main']['artifact'].update(id=1),
                  lambda d:d['runs'][0].update(branch='OTHER'),lambda d:d['permanent_pins'].pop(),
                  lambda d:d.update(initial_inputs=[]),lambda d:d.update(candidate_main_raw_bytes_equal=False),
                  lambda d:d['raw_replays']['main'].update(equals_initial_inputs=False),
                  lambda d:d['jobs_and_artifacts']['main'].update(job=d['jobs_and_artifacts']['candidate']['job']),
                  lambda d:d['jobs_and_artifacts']['main']['artifact'].update(id=d['jobs_and_artifacts']['candidate']['artifact']['id']),
                  lambda d:d['jobs_and_artifacts']['main']['artifact']['workflow_run'].update(head_branch='OTHER'),
                  lambda d:d['jobs_and_artifacts']['main'].update(zip_downloaded_and_digest_verified=False),
                  lambda d:d['jobs_and_artifacts']['main']['artifact'].update(digest='sha256:'+'0'*64),
                  lambda d:d['jobs_and_artifacts']['candidate']['artifact'].update(size_in_bytes=1),
                  lambda d:d.update(screenshot_identifies_momotora=True),lambda d:d.update(navigation_interaction_verified=True),
                  lambda d:d.update(pet_stats_or_native_ids_verified=True)]
         for change in changes:
             d=copy.deepcopy(receipt);change(d);out.write_text(json.dumps(d))
             with self.assertRaises(ValueError):m.verify_custody(root)
         out.unlink()
         with self.assertRaises(FileNotFoundError):m.verify_custody(root)

if __name__=='__main__':unittest.main()
