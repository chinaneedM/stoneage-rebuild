import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import stoneage_water_monster_source as m


def fixture(tag='td'):
 r=json.loads(m.REPORT.read_text());body='<html><meta charset=gb2312><body>《石器时代》任务功略-小水怪事件<!-- include 发布时间 begin -->2003-06-03 11:57<!-- include 发布时间 end --><'+tag+' class=l15z>synthetic content'+''.join('<a href="'+u+'">image</a>' for u in r['extraction']['image_references'])+'【我要投稿】【发表查看评论】【进入论坛】</'+tag+'></body></html>'
 return body.encode('gb18030')

class WaterMonsterTests(unittest.TestCase):
 def test_current_and_historical_roots_are_unique_closed_visible_and_footer_scoped(self):
  for tag in ('td','span'):
   raw=fixture(tag);body,links=m.article(raw);self.assertEqual(body,'syntheticcontent'+'image'*18);self.assertEqual(len(links),18)
   self.assertEqual(m.article(raw+b'<script>outside=1</script>'),(body,links))
   for changed in (raw+raw,raw.replace(b'class=l15z',b'class=chrome'),raw.replace(('</'+tag+'>').encode(),b''),raw.replace('2003-06-03 11:57'.encode(),b'2004-06-03 11:57')):
    with self.assertRaises(ValueError):m.article(changed)

 def test_scoped_requirements_routes_unknowns_and_source_authority_are_not_promoted(self):
  r=json.loads(m.REPORT.read_text());m.verify_report(r)
  changes=[lambda d:d.update(version_profile='TW10'),lambda d:d['negative_boundaries'].pop('official_authorship_verified'),
   lambda d:d['archive_discovery'].update(is_2003_original_capture=True),lambda d:d['archive_discovery'].update(closest_timestamp='20031201000000'),lambda d:d['source_pages'][1].update(actual_capture='20031201000000'),
   lambda d:d['extraction'].update(hard_entry_level=105),lambda d:d['extraction'].update(official_authorship_verified=True),
   lambda d:d['extraction']['shell'].update(entrance_key=True),lambda d:d['extraction']['shell'].update(consumed=True),lambda d:d['extraction']['shell'].update(all_three_required=True),
   lambda d:d['extraction']['bark_battle'].update(restriction_scope='WHOLE_QUEST'),lambda d:d['extraction']['bark_battle'].update(help_behavior='FORBIDDEN'),
   lambda d:d['extraction']['bark_battle'].update(mandatory_target_order=['BARK','HENCHMEN']),lambda d:d['extraction']['routes'][1].update(no_parent_battle_server_guarantee=True),
   lambda d:d['extraction']['narrative'].update(child_original_id=1),lambda d:d['extraction']['narrative'].update(child_spelling_conflict_unresolved=False),
   lambda d:d['extraction']['narrative'].update(child_is_reward_pet_proven=True),lambda d:d['extraction']['narrative'].update(actual_reunion_runtime_observed=True),
   lambda d:d['extraction']['narrative'].update(frog_dinner_motif='RUNTIME_FEEDING_AI'),lambda d:d['extraction']['weapon'].update(every_completion_guaranteed=True),
   lambda d:d['extraction']['weapon'].update(quota=1),lambda d:d['extraction']['weapon'].update(deadline_seconds=60),lambda d:d['extraction']['reward_pet'].update(level=1),
   lambda d:d['extraction']['ecology'].update(capturability='ALL'),lambda d:d.update(unacquired_image_reference_count=0)]
  for change in changes:
   d=copy.deepcopy(r);change(d);d['catalog_records']=m.catalog(d['extraction'],d['images'],d['image_observations'])
   with self.assertRaises(ValueError):m.verify_report(d)

 def test_eleven_documentary_records_preserve_roles_rights_and_original_unknown_ids(self):
  r=json.loads(m.REPORT.read_text());self.assertEqual(len(r['catalog_records']),11)
  self.assertEqual([p['collection'] for p in r['catalog_records']],['quests']+['npcs']*4+['items','items','pets','maps','screens','screens'])
  self.assertEqual(len(json.loads((m.ROOT/m.PARENTS[2]).read_text())['future_website']['required_collections']),19)
  for key,value in [('source_refs',['OTHER']),('rights_status','RELEASE_APPROVED'),('game_ids',1),('verification_status','RUNTIME')]:
   d=copy.deepcopy(r);d['catalog_records'][0][key]=value
   with self.assertRaises(ValueError):m.verify_report(d)

 def test_route_outcomes_do_not_merge_families_shell_ids_or_capture_dates(self):
  r=json.loads(m.REPORT.read_text());e=r['extraction'];self.assertIn('FIGHT_PARENT_WATER_MONSTER',e['routes'][0]['sequence']);self.assertNotIn('FIGHT_PARENT_WATER_MONSTER',e['routes'][1]['sequence'])
  self.assertEqual([p['pet_reward'] for p in e['routes']],['尤里蛙','尤里蛙']);self.assertEqual([e['narrative']['child_body_name'],e['narrative']['child_caption_name']],['莫拉司','莫拉斯'])
  self.assertEqual(r['comparison']['source_history']['archive_actual_capture'],'20160929133108')
  for change in [lambda d:d['comparison']['source_history'].update(archive_actual_capture='20031204000000'),lambda d:d['comparison']['family_comparison'].update(shared_family_or_quest_id_proven=True),lambda d:d['comparison']['shell_comparison'].update(same_original_shell_id_proven=True),lambda d:d['comparison'].update(modern_adoption_decided=True)]:
   d=copy.deepcopy(r);change(d)
   with self.assertRaises(ValueError):m.verify_report(d)

 def test_parent_and_shared_parser_files_are_mandatory_original_bytes(self):
  r=json.loads(m.REPORT.read_text())
  with tempfile.TemporaryDirectory() as name:
   root=Path(name)
   for pin in r['parent_pins']+[r['parser_dependency_pin']]:
    p=root/pin['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((m.ROOT/pin['path']).read_bytes())
   with patch.object(m,'ROOT',root):
    m.verify_report(r)
    for pin in r['parent_pins']+[r['parser_dependency_pin']]:
     p=root/pin['path'];raw=p.read_bytes();p.write_bytes(raw[:-1]+bytes([raw[-1]^1]))
     with self.assertRaises(ValueError):m.verify_report(r)
     p.unlink()
     with self.assertRaises(FileNotFoundError):m.verify_report(r)
     p.write_bytes(raw)

 def test_body_and_current_item_sample_agree_without_promoting_player_sample_level(self):
  r=json.loads(m.REPORT.read_text());self.assertEqual(r['extraction']['weapon']['stats_as_reported'],r['image_observations'][1]['displayed_stats']);self.assertEqual(r['image_observations'][1]['displayed_player_level_sample'],87);self.assertIsNone(r['extraction']['hard_entry_level'])
  for change in [lambda d:d['image_observations'][0].update(displayed_target_level=25),lambda d:d['image_observations'][1].update(sample_level_is_entry_gate=True),lambda d:d['image_observations'][1].update(actual_reward_acquisition_observed=True),lambda d:d['images'][0].update(sha256='0'*64),lambda d:d['extraction']['weapon']['stats_as_reported'].update(攻=74)]:
   d=copy.deepcopy(r);change(d);d['catalog_records']=m.catalog(d['extraction'],d['images'],d['image_observations'])
   with self.assertRaises(ValueError):m.verify_report(d)
  with self.assertRaises((ValueError,OSError)):m.inspect_images({'I1':b'<html>error</html>'},r)

 def test_custody_rejects_missing_changed_misattributed_or_promoted_reports(self):
  receipt=m.verify_custody()
  with tempfile.TemporaryDirectory() as name:
   root=Path(name);path=root/f'research/recovered/{m.STEM}-CUSTODY-R1.json'
   for pin in receipt['permanent_pins']:
    p=root/pin['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((m.ROOT/pin['path']).read_bytes())
   path.write_text(json.dumps(receipt));m.verify_custody(root)
   for pin in receipt['permanent_pins']:
    p=root/pin['path'];raw=p.read_bytes();p.write_bytes(raw[:-1]+bytes([raw[-1]^1]))
    with self.assertRaises(ValueError):m.verify_custody(root)
    p.unlink()
    with self.assertRaises(FileNotFoundError):m.verify_custody(root)
    p.write_bytes(raw)
   changes=[lambda d:d.update(schema='OTHER'),lambda d:d['jobs_and_artifacts']['main'].update(job_name='OTHER'),lambda d:d['jobs_and_artifacts']['main']['artifact'].update(id=d['jobs_and_artifacts']['candidate']['artifact']['id']),lambda d:d['runs'].pop(),lambda d:d['runs'][0].update(branch='OTHER'),lambda d:d['runs'].append(d['runs'][0]),lambda d:d.update(content_commit='0'*40),
    lambda d:d['jobs_and_artifacts']['main']['artifact']['workflow_run'].update(head_branch='OTHER'),
    lambda d:d['jobs_and_artifacts']['main'].update(job=d['jobs_and_artifacts']['candidate']['job']),
    lambda d:d.update(current_http_bytes_are_historical_bytes=True),
    lambda d:d['raw_replays']['main'].update(equals_initial_inputs=not receipt['raw_replays']['main']['equals_initial_inputs']),
    lambda d:d.update(candidate_main_raw_bytes_equal=not receipt['candidate_main_raw_bytes_equal']),lambda d:d.update(initial_inputs=[]),
    lambda d:d['permanent_pins'].pop()]
   for change in changes:
    d=copy.deepcopy(receipt);change(d);path.write_text(json.dumps(d))
    with self.assertRaises(ValueError):m.verify_custody(root)
   path.unlink()
   with self.assertRaises(FileNotFoundError):m.verify_custody(root)

if __name__=='__main__':unittest.main()
