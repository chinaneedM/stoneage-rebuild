import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import stoneage_jp2005_autumn_source as m


def fixture():
 head='<!--↓大見出し--><h5>'+m.TITLE+'</h5><!--↑大見出し--><div class="news_txt1">2005/09/21 20:23</div><td class="newstext">'
 image='<IMG SRC="/news/image/2005.09/20050921202336_0.jpg" WIDTH=232 HEIGHT=310>'
 body='ガイアックスは10月のイベントスケジュールを発表した<A href="http://www.4gamer.net/DataContents/game/1377.html">game</A>'
 body+=''.join('<FONT class="headline">■'+v+'</FONT>synthetic '+str(i) for i,v in enumerate(m.LABELS))+'（aueki）'
 return (head+image+'<!-- 本文開始 -->'+body+'<!-- 本文終了 --><!-- 本文開始 --> <!-- 本文終了 --><!-- tDialy:END -->').encode('cp932')


class AutumnSourceTests(unittest.TestCase):
 def report(self):return json.loads(m.REPORT.read_text())

 def test_article_requires_unique_visible_ordered_body_and_actual_image(self):
  raw=fixture();core,sections=m.article(raw);self.assertEqual(list(sections),m.LABELS)
  self.assertEqual(m.article(raw+b'<script>outside=1</script>'),(core,sections))
  variants=[raw+raw,raw.replace(b'2005/09/21',b'2005/09/22'),raw.replace(b'WIDTH=232',b'WIDTH=233'),
   raw.replace(m.LABELS[0].encode('cp932'),b'other'),raw.replace(b'synthetic 0',b'<script>synthetic 0'),
   raw.replace(b'<!-- tDialy:END -->',b'<A href="https://example.com">other</A><!-- tDialy:END -->')]
  # The extra link outside the article is harmless, unlike an extra article link.
  self.assertEqual(m.article(variants.pop()),(core,sections))
  variants.append(raw.replace(b'game</A>',b'game</A><A href="https://example.com">details</A>'))
  for changed in variants:
   with self.assertRaises(ValueError):m.article(changed)

 def test_journalism_not_verbatim_release_operator_page_or_historical_bytes(self):
  r=self.report();m.validate(r)
  for change in [lambda d:d.update(version_profile='TW10'),lambda d:d['source'].update(authority='DIRECT_OFFICIAL'),
   lambda d:d['source'].update(explicit_verbatim_manufacturer_release=True),
   lambda d:d['source'].update(actual_operator_event_page_acquired=True),
   lambda d:d['source'].update(current_bytes_authenticate_2005_original=True),
   lambda d:d['source'].update(official_event_detail_link_in_article='http://stoneage.to/info/event_020.html'),
   lambda d:d['negative_boundaries'].update(schedule_proves_event_execution=True)]:
   d=copy.deepcopy(r);change(d)
   with self.assertRaises(ValueError):m.validate(d)

 def test_quest_and_contest_prizes_unknown_recipes_and_actor_control_stay_separate(self):
  r=self.report()
  changes=[lambda e:e['challenge'].update(reward='秋の満腹セット'),
   lambda e:e['challenge'].update(role_controller_npc_or_gm='NPC'),
   lambda e:e['challenge'].update(recipes_quantities_turnin_consumption_repeatability='ONE_RECIPE'),
   lambda e:e['contest'].update(venue='CHATROOM'),
   lambda e:e['contest']['best_prize'].update(verified_world_instance_count=1),
   lambda e:e['contest']['best_prize'].update(stats_growth_skills_habitat_native_id=1),
   lambda e:e['contest']['honorable_mentions'][0].update(effect='RENAME_ANY_EQUIPMENT'),
   lambda e:e['contest']['honorable_mentions'][1].update(formula_duration_guarantee='100_PERCENT'),
   lambda e:e['contest'].update(winner_count_each_winner_gets_both_and_actual_award=True)]
  for change in changes:
   d=copy.deepcopy(r);change(d['extraction']);d['semantic_contract']=m.semantic(d['extraction']);d['catalog_records']=m.catalog(d['extraction'])
   with self.assertRaises(ValueError):m.validate(d)

 def test_sale_and_lesson_servers_provisional_title_and_version_rules_not_expanded(self):
  r=self.report()
  for change in [lambda e:e['sale'].update(goods='ALL_ITEMS'),lambda e:e['sale'].update(servers='MARS_ONLY'),
   lambda e:e['sale'].update(base_prices_currency_rounding_inventory_transactions=1000),
   lambda e:e['lessons']['sessions'][0].update(server='ALL'),lambda e:e['lessons'].update(actual_recipes_and_gm_names=['water']),
   lambda e:e['halloween'].update(provisional_title=False),lambda e:e['halloween'].update(item_names_forms_duration_spawn_algorithm_and_drop_rules='MONSTER_LOOT'),
   lambda e:e.update(timezone='JST'),lambda e:e.update(actual_execution_verified=True),lambda e:e.update(exact_client_build='JP2005')]:
   d=copy.deepcopy(r);change(d['extraction']);d['semantic_contract']=m.semantic(d['extraction']);d['catalog_records']=m.catalog(d['extraction'])
   with self.assertRaises(ValueError):m.validate(d)
  for key,field in [('cn20_crafting','shared_native_village_recipe_or_item_ids_verified'),('cn20_crafting','cn_partial_categories_complete_jp_recipes'),('jp_treasure','trade_or_repeat_rules_backfilled')]:
   d=copy.deepcopy(r);d['comparison'][key][field]=True
   with self.assertRaises(ValueError):m.validate(d)

 def test_illustration_is_not_gavi_npc_recipe_ui_or_original_sprite(self):
  r=self.report()
  for field in ['identified_as_gavi_or_gourmet_master','game_screenshot','recipe_ui_or_reward_delivery','original_sprite_model_animation','native_client_resolution_proven']:
   d=copy.deepcopy(r);d['visual_observation'][field]=True
   with self.assertRaises(ValueError):m.validate(d)
  for field,value in [('sha256','0'*64),('size',[640,480]),('frames',2)]:
   d=copy.deepcopy(r);d['image'][field]=value
   with self.assertRaises(ValueError):m.validate(d)
  with self.assertRaises((ValueError,OSError)):m.inspect_image(b'<html>404</html>')

 def test_all_eleven_records_have_seven_required_fields_without_original_ids_or_rights(self):
  r=self.report();contract=json.loads((m.ROOT/m.PARENTS[-1]).read_text())['future_website']
  self.assertEqual(len(r['catalog_records']),11)
  for row in r['catalog_records']:
   self.assertTrue(set(contract['record_contract']['required']).issubset(row))
   self.assertIn(row['collection'],contract['required_collections']);self.assertIsNone(row['game_ids'])
  for key in contract['record_contract']['required']:
   d=copy.deepcopy(r);d['catalog_records'][0].pop(key)
   with self.assertRaises(ValueError):m.validate(d)
  for key,value in [('entity_type','ORIGINAL_MASTER'),('game_ids',1),('rights_status','RELEASE_APPROVED')]:
   d=copy.deepcopy(r);d['catalog_records'][0][key]=value
   with self.assertRaises(ValueError):m.validate(d)

 def test_all_parent_and_parser_pins_reject_missing_or_equal_length_changes(self):
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
                  lambda d:d.update(current_bytes_authenticate_2005_original=True),lambda d:d.update(direct_operator_source_acquired=True),
                  lambda d:d['runs'].pop(),lambda d:d['runs'].append(d['runs'][0]),lambda d:d['runs'][0].update(conclusion='failure'),
                  lambda d:d['runs'][0].update(id=1),lambda d:d['runs'][0].update(name='OTHER'),
                  lambda d:d['jobs_and_artifacts']['main'].update(job=1),lambda d:d['jobs_and_artifacts']['main']['artifact'].update(id=1),
                  lambda d:d['runs'][0].update(branch='OTHER'),lambda d:d['permanent_pins'].pop(),
                  lambda d:d.update(initial_inputs=[]),lambda d:d.update(candidate_main_raw_bytes_equal=False),
                  lambda d:d['raw_replays']['main'].update(equals_initial_inputs=False),
                  lambda d:d['jobs_and_artifacts']['main'].update(job=d['jobs_and_artifacts']['candidate']['job']),
                  lambda d:d['jobs_and_artifacts']['main']['artifact'].update(id=d['jobs_and_artifacts']['candidate']['artifact']['id']),
                  lambda d:d['jobs_and_artifacts']['main']['artifact']['workflow_run'].update(head_branch='OTHER'),
                  lambda d:d['jobs_and_artifacts']['main'].update(zip_downloaded_and_digest_verified=False)]
         for change in changes:
             d=copy.deepcopy(receipt);change(d);out.write_text(json.dumps(d))
             with self.assertRaises(ValueError):m.verify_custody(root)
         out.unlink()
         with self.assertRaises(FileNotFoundError):m.verify_custody(root)

if __name__=='__main__':unittest.main()
