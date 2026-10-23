import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import stoneage_cn2003_qiang_en_source as m


def fixture(index):
 s=m.SOURCES[index]
 head='<!-- include 中间内容 begin --><b>'+s['visible_title']+'</b>新浪游戏 网友投稿<!-- include 发布时间 begin -->'+s['visible_publication']+'<!-- include 发布时间 end -->'
 if index==0:
  pairs=[]
  for i in range(20):
   full=m.IMAGES[0]['url'] if i==8 else m.IMAGES[1]['url'] if i==11 else 'https://image2.sina.com.cn/synthetic'+str(i)+'.jpg'
   full=full.replace('https:','http:');pairs.append('<a href="'+full+'" target="_blank"><img src="'+full.replace('.jpg','s.jpg')+'" border="0" width="150" height="113">')
  body='<td class=l15z>1.等级要求：synthetic'+''.join(pairs)+'沙拉的房间<table width=520 cellpadding=0 cellspacing=0 align=center>'
 else:
  ex=json.loads(m.REPORT.read_text())['extraction']['dungeon']['map_table_source']
  body='<td width="18%" align="center" class=l15>强恩一族洞窟</td>285，926构造：地上8楼敌Lv：Lv30～40敌种：山贼59.齐尔格尔顿72.格鲁西斯有强恩一族任务'
  body+=''.join(v['from']+'-'+v['to']+'('+str(v['coord'][0])+'.'+str(v['coord'][1])+')' for v in ex['transitions_in_printed_row_order'])
  body+='4F-5F要说密语(红色月亮的光芒)5F-6F要说密语(蓝色山脉即力量)6F-7F要说密语(白色之风即速度)<td width="18%" align="center" class=l15>基努伊海底通路</td>'
 return (head+body+'<!-- include 中间内容 end -->').encode('gb18030')


class QiangEnSourceTests(unittest.TestCase):
 def report(self):return json.loads(m.REPORT.read_text())

 def test_unique_visible_business_body_dates_actual_links_and_selected_map_row(self):
  for index,parser in [(0,m.article),(1,m.map_row)]:
   raw=fixture(index);result=parser(raw);self.assertEqual(parser(raw+b'<script>outside=1</script>'),result)
   for changed in [raw+raw,raw.replace(m.SOURCES[index]['visible_publication'].encode(),b'2000-01-01'),
    raw.replace(m.SOURCES[index]['visible_title'].encode('gb18030'),b'OTHER',1),
    raw.replace(b'<!-- include',b'<script><!-- include',1)]:
    with self.assertRaises(ValueError):parser(changed)
  self.assertEqual(len(m.article(fixture(0))[2]),20)
  self.assertEqual(len(m.map_row(fixture(1))[1]['transitions_in_printed_row_order']),13)
  with self.assertRaises(ValueError):m.article(fixture(0).replace(b'0530_009.jpg',b'0530_010.jpg'))
  with self.assertRaises(ValueError):m.map_row(fixture(1).replace(b'Lv30',b'Lv99')+b'Lv30')

 def test_portal_authority_and_version_remain_unverified(self):
  r=self.report();m.validate(r)
  for change in [lambda d:d.update(version_profile='TW10'),lambda d:d['sources'][0].update(official_authorship_verified=True),
   lambda d:d['sources'][1].update(named_original_author='Wayi'),lambda d:d['sources'][0].update(current_bytes_authenticate_2003_original=True),
   lambda d:d['sources'][1].update(exact_game_version_or_build='1.82')]+[
   lambda d,k=k:d['negative_boundaries'].update({k:True}) for k in m.BOUNDARIES]:
   d=copy.deepcopy(r);change(d)
   with self.assertRaises(ValueError):m.validate(d)

 def test_family_choice_optional_document_and_rewards_are_not_fabricated_runtime(self):
  r=self.report()
  changes=[lambda e:e['family_outcome'].update(escort_to_birth_father=True),
   lambda e:e['family_outcome'].update(daughter_choice_as_reported='RETURN_TO_BIRTH_FATHER'),
   lambda e:e['family_outcome'].update(letter_title_proves_birth_mother_alive=True),
   lambda e:e['dungeon']['optional_document'].update(required_for_passing=True),
   lambda e:e['dungeon']['optional_document'].update(drop_as_reported='GUARANTEED'),
   lambda e:e['dungeon']['fixed_blocking_trio'].update(same_instances_as_random_encounters=True),
   lambda e:e['chief_reward'].update(sample_is_guaranteed=True),lambda e:e['item_flow'][-1]['stats_as_written'].update(石=5),
   lambda e:e['item_flow'][-1].update(abbreviated_status_semantics='IMMUNITY_PERCENT'),
   lambda e:e['backstory'].update(current_age_computed=20),lambda e:e['backstory'].update(mountain_native_alias_verified=True),
   lambda e:e.update(original_server_runtime_verified=True),lambda e:e.update(repeatability_reset_and_item_consumption='DAILY')]
  for change in changes:
   d=copy.deepcopy(r);change(d['extraction']);d['catalog_records']=m.catalog(d['extraction'])
   with self.assertRaises(ValueError):m.validate(d)

 def test_coordinates_gates_and_ecology_keep_scope_and_direction(self):
  r=self.report()
  changes=[lambda e:e.update(hard_level_gate=50),lambda e:e['village'].update(coordinate_roles=['ENTRY','EXIT']),
   lambda e:e['npcs'][1].update(local_coord=[58,66]),lambda e:e['dungeon']['password_guards'][0].update(password='蓝色山脉即力量'),
   lambda e:e['dungeon'].update(total_floor_count_from_article=7),lambda e:e['dungeon'].update(room_equals_eighth_floor=True),
   lambda e:e['dungeon'].update(ecology_difference_resolution='PATCH_CHANGED_LEVELS'),
   lambda e:e['dungeon']['map_table_source'].update(catalogue_numbers_are_original_ids=True),
   lambda e:e['dungeon']['map_table_source']['transitions_in_printed_row_order'][0].update(to='7F'),
   lambda e:e['dungeon']['article_ecology'].update(enemy_level_as_reported=[30,40]),
   lambda e:e.update(original_map_npc_quest_item_ids=[59,72])]
  for change in changes:
   d=copy.deepcopy(r);change(d['extraction']);d['catalog_records']=m.catalog(d['extraction'])
   with self.assertRaises(ValueError):m.validate(d)
  for group,field in [('liuli','family_reunion_or_father_death_backfilled'),('mengde','same_native_faction_ids'),
   ('mengde','mengde_adult_ceremony_or_reward_order_backfilled'),('two_portal_pages','same_exact_build_verified'),
   ('two_portal_pages','geerdun_labels_forced_to_alias'),('two_portal_pages','seven_captions_vs_eight_floor_table_is_proven_contradiction')]:
   d=copy.deepcopy(r);d['comparison'][group][field]=True
   with self.assertRaises(ValueError):m.validate(d)

 def test_screens_do_not_prove_choices_native_ids_reward_delivery_or_effect(self):
  r=self.report()
  for field in ['actual_reward_delivery_or_item_effect_tested','original_sprite_or_model','exact_build_or_historical_pixels_verified','native_npc_id_verified']:
   d=copy.deepcopy(r);d['visual_observations'][0][field]=True
   with self.assertRaises(ValueError):m.validate(d)
  for field,value in [('sha256','0'*64),('size',[320,240]),('frames',2)]:
   d=copy.deepcopy(r);d['images'][1][field]=value
   with self.assertRaises(ValueError):m.validate(d)
  with self.assertRaises((ValueError,OSError)):m.inspect_images({'I1':b'<html>404</html>'})

 def test_eighteen_documentary_records_follow_seven_field_archive_contract(self):
  r=self.report();contract=json.loads((m.ROOT/m.PARENTS[-1]).read_text())['future_website'];self.assertEqual(len(r['catalog_records']),18)
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
                  lambda d:d.update(current_bytes_authenticate_2003_original=True),lambda d:d.update(official_authorship_verified=True),
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
                  lambda d:d['jobs_and_artifacts']['candidate']['artifact'].update(size_in_bytes=1)]
         for change in changes:
             d=copy.deepcopy(receipt);change(d);out.write_text(json.dumps(d))
             with self.assertRaises(ValueError):m.verify_custody(root)
         out.unlink()
         with self.assertRaises(FileNotFoundError):m.verify_custody(root)

if __name__=='__main__':unittest.main()
