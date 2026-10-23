import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import stoneage_cn2003_ladora_crimson_source as m


def fixture():
 r=json.loads(m.REPORT.read_text());ex=r['extraction']
 intro=''.join(m.CLAUSES).replace('四条路线分别通往四座不同的山顶','四条路线分别通往四座不同的山顶：')
 for route in ex['four_routes']:
  intro+=route['label']+''.join(v['from_floor']+'楼通往'+v['to_floor']+'楼的洞口（东'+str(v['source_floor_local_coord'][0])+'，南'+str(v['source_floor_local_coord'][1])+'）' for v in route['directed_edges'])
 intro+='◆不死鸟！</font></p>'
 eco=''
 for v in ex['geography_occurrences']:
  eco+=v['name_as_written']+('“'+v['coordinate_frame']+'”内' if not v['coordinate_frame'].startswith('WORLD') else '')+'坐标：'
  eco+='、'.join('（东'+str(x)+'，南'+str(y)+'）' for x,y in v['coordinate_literals'])
  eco+='怪物等级：'+str(v['monster_levels_as_reported'][0])+'~'+str(v['monster_levels_as_reported'][1])+'级怪物种类：'+'、'.join(v['enemy_labels_as_written'])
 eco=eco.replace('拉多拉的回廊','<p>　　7. 拉多拉的回廊',1)
 return ('<!-- include 中间内容 begin -->'+m.TITLE+'作者：新浪游戏我要投稿<!-- include 发布时间 begin -->2003-06-09 14:03<!-- include 发布时间 end -->'
  +'<td width=500 class=l15z><span>'+intro+'<p>　　深红洞窟（二）——口渴的多洛加</p>excluded'+eco
  +'<img src="http://image2.sina.com.cn/gm/newgames/0303/images/tuxing0610_03.jpg"></td></tr></table><br><br><!-- include 中间内容 end -->').encode('gb18030')


class LadoraCrimsonTests(unittest.TestCase):
 def report(self):return json.loads(m.REPORT.read_text())
 def reject_extractions(self,changes):
  for change in changes:
   d=self.report();change(d['extraction']);d['catalog_records']=m.catalog(d['extraction'])
   with self.assertRaises(ValueError):m.validate(d)

 def test_unique_visible_selected_scope_and_hidden_outside_cannot_repair(self):
  raw=fixture();ex=m.derive(raw);self.assertEqual(m.semantic(ex),m.semantic(self.report()['extraction']))
  self.assertEqual(m.derive(raw+b'<script>outside=1</script>'),ex)
  for changed in [raw+raw,raw.replace(b'2003-06-09',b'2003-06-10'),raw.replace(b'tuxing0610_03.jpg',b'other.jpg'),raw.replace(m.TITLE.encode('gb18030'),b'OTHER')]:
   with self.assertRaises(ValueError):m.derive(changed)
  for replacement in ('','<script>'+m.ANCHOR+'</script>'):
   changed=raw.decode('gb18030').replace(m.ANCHOR,replacement)+'<div>'+m.ANCHOR+'</div>'
   with self.assertRaises(ValueError):m.derive(changed.encode('gb18030'))

 def test_dated_portal_scope_is_not_official_script_or_both_complete_quests(self):
  r=self.report();m.validate(r)
  for key in m.BOUNDARIES:
   d=copy.deepcopy(r);d['negative_boundaries'][key]=True
   with self.assertRaises(ValueError):m.validate(d)
  for field,value in [('official_authorship_verified',True),('exact_game_build','1.82'),('current_bytes_authenticate_2003_original',True),('publisher_field','operator')]:
   d=copy.deepcopy(r);d['source'][field]=value
   with self.assertRaises(ValueError):m.validate(d)
  self.reject_extractions([lambda e:e.update(excluded_scope=[]),lambda e:e['quest_header_context_only'].update(hard_map_gate=80),lambda e:e.update(original_server_runtime_verified=True)])

 def test_four_directed_routes_and_corridor_coordinates_are_separate_frames(self):
  ex=self.report()['extraction'];self.assertEqual([len(v['directed_edges']) for v in ex['four_routes']],[3]*4)
  self.assertEqual(ex['four_routes'][0]['directed_edges'][0],ex['four_routes'][1]['directed_edges'][0])
  self.reject_extractions([lambda e:e['four_routes'][0]['directed_edges'][1].update(source_floor_local_coord=[11,7]),
   lambda e:e['four_routes'][0]['directed_edges'][0].update(from_floor='2',to_floor='1'),
   lambda e:e.update(route_entry_mapping=[1,2,3,4]),lambda e:e['geography_occurrences'][1].update(coordinate_frame='WORLD'),
   lambda e:e['geography_occurrences'][4].update(coordinate_frame='巴那姆的洞窟地下1楼'),lambda e:e['village'].update(coordinate_roles=['ENTRY','EXIT'])])

 def test_repeated_map_occurrences_level_ranges_and_spelling_not_pet_master(self):
  e=self.report()['extraction']['geography_occurrences'];self.assertEqual(len(e),7)
  self.assertEqual([e[i]['enemy_labels_as_written'][-1] for i in (4,6)],['格鲁西','格鲁西斯'])
  self.reject_extractions([lambda e:e['geography_occurrences'].pop(),lambda e:e['geography_occurrences'][4].update(enemy_labels_as_written=e['geography_occurrences'][6]['enemy_labels_as_written']),
   lambda e:e['geography_occurrences'][0].update(monster_levels_as_reported=[25,31]),lambda e:e['geography_occurrences'][6].update(native_map_id_or_capture_eligibility='CAPTURABLE')])
  d=self.report();d['comparison']['pet_commission_target_means_capturable_ecology']=True
  with self.assertRaises(ValueError):m.validate(d)

 def test_world_myth_phoenix_form_and_diagram_code_are_not_runtime(self):
  self.reject_extractions([lambda e:e['world_story'].update(non_eruption_duration_as_told='千余年'),lambda e:e['world_story'].update(calendar_or_simulation_verified=True),
   lambda e:e['phoenix_context'].update(observed_runtime_template_or_original_native_pet_id=1),lambda e:e['diagram_relationship'].update(native_instance_resolution='ONE_SUMMIT')])
  for key in ['printed_codes_are_verified_native_map_ids','arrow_geometry_or_walkable_tiles_verified','one_summit_label_proves_one_native_summit_instance','original_client_build_or_historical_pixels_authenticated']:
   d=self.report();d['visual_observations'][0][key]=True
   with self.assertRaises(ValueError):m.validate(d)
  with self.assertRaises((ValueError,OSError)):m.inspect_images({'I1':b'<html>404</html>'})

 def test_ten_catalog_rows_keep_contract_rights_and_no_game_ids(self):
  r=self.report();c=json.loads((m.ROOT/m.PARENTS[-1]).read_text())['future_website'];self.assertEqual(len(r['catalog_records']),10)
  for row in r['catalog_records']:
   self.assertTrue(set(c['record_contract']['required']).issubset(row));self.assertIn(row['collection'],c['required_collections']);self.assertIsNone(row['game_ids'])
  for field in c['record_contract']['required']:
   d=copy.deepcopy(r);d['catalog_records'][0].pop(field)
   with self.assertRaises(ValueError):m.validate(d)
  d=copy.deepcopy(r);d['catalog_records'][0]['rights_status']='RELEASE_APPROVED'
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

if __name__=='__main__':unittest.main()
