import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import stoneage_cn2011_mammoth_source as m

class MammothSourceTests(unittest.TestCase):
 def test_visible_unique_closed_article_and_selected_scope(self):
  r=json.loads(m.REPORT.read_text());ex=r['extraction']
  paragraphs=['在原始大陆上的测试站点','如何才能乘坐测试车','一边乘坐测试车','更多精彩，敬请继续锁定胜思网络《石器时代》！','后续研发以及运营由广东胜思网络科技有限公司全权负责；8.5魔域大冒险；2.5“精灵王传说”版本服务器']
  text='<h1 id="artibodyTitle">'+ex['title']+'</h1><span id="pub_date">2011年12月19日 11:08</span><div id="artibody">'+''.join('<p>'+p+'</p>' for p in paragraphs)+'<a href="http://sa.cins.cn">site</a>'+''.join('<img src="'+i['src']+'" alt="'+i['alt']+'">' for i in ex['image_references'])+'</div>'
  raw=text.encode('gb18030');actual=m.parse(raw);self.assertEqual(actual['parts'],paragraphs[:3]);self.assertNotIn('8.5',actual['core'])
  self.assertEqual(m.parse(raw+b'<script>outside=1</script>'),actual)
  for changed in (raw+raw,raw.replace(b'id="artibody"',b'id="footer"'),raw.removesuffix(b'</div>'),raw.replace('如何才能乘坐测试车'.encode('gb18030'),'<script>如何才能乘坐测试车</script>'.encode('gb18030'))):
   with self.assertRaises(ValueError):m.parse(changed)

 def test_unknowns_authority_and_displayed_scene_cannot_be_promoted(self):
  r=json.loads(m.REPORT.read_text());m.verify_report(r)
  changes=[lambda d:d.update(version_profile='TW10'),lambda d:d['negative_boundaries'].pop('early_jss_go_command_backfilled'),
   lambda d:d['extraction']['unknown_rules'].update(fare=20),lambda d:d['extraction']['unknown_rules'].update(passenger_capacity=4),
   lambda d:d['extraction']['unknown_rules'].update(normal_wait_minutes=3),lambda d:d['extraction']['unknown_rules'].update(random_encounters=False),
   lambda d:d['extraction']['version_context'].update(transport_bound_to_either_build='BOTH'),
   lambda d:d['extraction']['fast_departure'].update(case_variants=['GO']),lambda d:d['extraction']['fast_departure'].update(authorization_or_minimum_passengers=1),
   lambda d:d['extraction']['fast_departure'].update(accepted_server_command_observed=True),
   lambda d:d['extraction']['exit'].update(refund=0),lambda d:d['extraction']['boarding'].update(exact_icon_or_coordinates=[1,2]),
   lambda d:d['extraction'].update(source_layer='DIRECT_OFFICIAL'),lambda d:d['image_observations'][1].update(label_scope='DIRECTED_ROUTE_EDGES'),
   lambda d:d['image_observations'][0].update(native_client_resolution=[550,413]),lambda d:d['images'][0].update(sha256='0'*64),
   lambda d:d['unselected_image'].update(pixels_acquired=True)]
  for change in changes:
   d=copy.deepcopy(r);change(d);d['catalog_records']=m.catalog(d['extraction'],d['image_observations'])
   with self.assertRaises(ValueError):m.verify_report(d)

 def test_catalog_preserves_source_image_roles_and_nonproduction_rights(self):
  r=json.loads(m.REPORT.read_text());self.assertEqual([p['collection'] for p in r['catalog_records']],['tutorials','screens','screens'])
  contract=json.loads((m.ROOT/m.PARENTS[2]).read_text())['future_website'];self.assertEqual(len(contract['required_collections']),19)
  for key,value in [('source_refs',['OTHER']),('rights_status','RELEASE_APPROVED'),('game_ids',123),('verification_status','RUNTIME')]:
   d=copy.deepcopy(r);d['catalog_records'][0][key]=value
   with self.assertRaises(ValueError):m.verify_report(d)

 def test_early_numbers_and_aviation_words_do_not_fill_later_bus_unknowns(self):
  r=json.loads(m.REPORT.read_text());c=r['comparison'];self.assertEqual(c['jss2001']['bus']['stop_minutes'],3);self.assertEqual(c['jss2001']['bus']['passenger_limit'],4)
  self.assertIn('go',c['cn2003_player_guide']['aviation_departure_words']);self.assertIsNone(r['extraction']['unknown_rules']['fare'])
  for key in ('same_original_npc_map_or_command_id_proven','jss_go_support_proven','early_numbers_fill_2011_unknowns','both_2011_advertised_versions_verified','modern_adoption_decided'):
   d=copy.deepcopy(r);d['comparison'][key]=True
   with self.assertRaises(ValueError):m.verify_report(d)

 def test_parent_and_both_shared_parser_bytes_are_mandatory(self):
  r=json.loads(m.REPORT.read_text())
  with tempfile.TemporaryDirectory() as name:
   root=Path(name)
   for pin in r['parent_pins']+r['parser_dependency_pins']:
    p=root/pin['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((m.ROOT/pin['path']).read_bytes())
   with patch.object(m,'ROOT',root):
    m.verify_report(r)
    for pin in r['parent_pins']+r['parser_dependency_pins']:
     p=root/pin['path'];raw=p.read_bytes();p.write_bytes(raw[:-1]+bytes([raw[-1]^1]))
     with self.assertRaises(ValueError):m.verify_report(r)
     p.unlink()
     with self.assertRaises(FileNotFoundError):m.verify_report(r)
     p.write_bytes(raw)

 def test_actual_image_links_and_missing_or_non_jpeg_pixels_are_not_repaired(self):
  r=json.loads(m.REPORT.read_text())
  self.assertEqual(len(r['images']),2);self.assertNotEqual(r['images'][0]['sha256'],r['images'][1]['sha256'])
  for p,ref in zip(r['images'],r['extraction']['image_references']):self.assertEqual(p['url_as_written'],ref['src'])
  with self.assertRaises(KeyError):m.inspect_images({},r)
  with self.assertRaises((ValueError,OSError)):m.inspect_images({'I1':b'<html>error</html>'},r)

if __name__=='__main__':unittest.main()
