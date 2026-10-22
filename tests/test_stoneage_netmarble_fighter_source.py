import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import stoneage_netmarble_fighter_source as m


def fixture():
 return ('<html lang="ja"><title>ストーンエイジ：放置冒険</title><meta property="og:title" content="ストーンエイジ：放置冒険"><link rel="canonical" href="'+m.URL+'"><section class="character"><div class="detail"><div class="name"><span><em>テスト</em><em>テスト</em></span></div><div class="info"><span>synthetic background</span></div><figure class="image-main"><img src="https://sgimage.netmarble.com/images/netmarble/test.png"></figure></div></section><p class="copyright">ⓒ Netmarble Corp. &amp; Netmarble N2 Inc. All Rights Reserved.</p></html>').encode()

class FighterSourceTests(unittest.TestCase):
 def test_visible_unique_closed_active_detail_and_dynamic_biography_fields(self):
  raw=fixture();p=m.parse(raw);self.assertEqual(p['name'],'テスト');self.assertEqual(p['name_render_instances'],2)
  self.assertEqual(m.parse(raw+b'<script>unrelated=1</script>'),p)
  for changed in (raw+raw,raw.replace(b'class="detail"',b'class="thumbnail"'),raw.replace(b'</section>',b''),raw.replace(b'synthetic background',b'<script>synthetic background</script>'),raw.replace('<em>テスト</em><em>テスト</em>'.encode(),'<em>テスト</em><em>別人</em>'.encode())):
   with self.assertRaises(ValueError):m.parse(changed)
  fake=dict(p,biography='テスト村で暮らしており内気、慎重、親切な性格。冒険を経て落ち着いた姿を徐々に見せるようになる。')
  with patch.object(m,'parse',return_value=fake):ex=m.extract(b'synthetic')
  self.assertEqual(ex['residence']['village_as_written'],'テスト村');self.assertEqual(ex['personality']['traits_as_written'],['内気','慎重','親切']);self.assertEqual(ex['narrative_arc']['qualities_as_written'],'落ち着いた')
  self.assertIsNone(ex['narrative_arc']['stat_delta'])

 def test_unknowns_story_product_and_static_art_cannot_be_promoted(self):
  r=json.loads(m.REPORT.read_text());m.verify_report(r)
  changes=[lambda d:d.update(version_profile='JSS1999'),lambda d:d['negative_boundaries'].pop('personality_is_combat_stats'),
   lambda d:d['extraction'].update(publication_date='2026-02-09'),lambda d:d['extraction'].update(exact_client_build='20260209'),
   lambda d:d['extraction'].update(logical_characters_in_selected_detail=2),lambda d:d['extraction']['residence'].update(map_id=1000),
   lambda d:d['extraction']['residence'].update(scope='PLAYER_SPAWN'),lambda d:d['extraction']['personality'].update(scope='COMBAT_STATS'),
   lambda d:d['extraction']['narrative_arc'].update(level_or_quest_trigger=10),lambda d:d['extraction']['narrative_arc'].update(stat_delta=5),
   lambda d:d['extraction']['unknowns'].update(age=18),lambda d:d['extraction']['unknowns'].update(gender_as_stated_in_text='MALE'),
   lambda d:d['image_observations'][0].update(client_model_or_sprite_binding=123),lambda d:d['image_observations'][0].update(release_rights_granted=True),
   lambda d:d['images'][0].update(sha256='0'*64)]
  for change in changes:
   d=copy.deepcopy(r);change(d);d['catalog_records']=m.catalog(d['extraction'],d['images'],d['image_observations'])
   with self.assertRaises(ValueError):m.verify_report(d)

 def test_single_character_catalog_keeps_source_image_roles_and_rights(self):
  r=json.loads(m.REPORT.read_text());self.assertEqual(len(r['catalog_records']),1);self.assertEqual(r['catalog_records'][0]['collection'],'characters')
  contract=json.loads((m.ROOT/m.PARENTS[1]).read_text())['future_website'];self.assertEqual(len(contract['required_collections']),19)
  for key,value in [('source_refs',['OTHER']),('rights_status','RELEASE_APPROVED'),('game_ids',123),('verification_status','RUNTIME')]:
   d=copy.deepcopy(r);d['catalog_records'][0][key]=value
   with self.assertRaises(ValueError):m.verify_report(d)

 def test_mobile_named_fighter_does_not_rename_twelve_early_pc_positions(self):
  r=json.loads(m.REPORT.read_text());self.assertEqual(r['comparison']['pc_hangame2003']['web_positions'],12)
  self.assertTrue(r['comparison']['pc_hangame2003']['operator_describes_no_fixed_names'])
  for key,value in [('current_name_applied_to_pc_position',1),('same_original_model_or_body_id_proven',True),('same_worldline_or_retcon_proven',True),('early_naming_description_contradicted',True),('modern_adoption_decided',True)]:
   d=copy.deepcopy(r);d['comparison'][key]=value
   with self.assertRaises(ValueError):m.verify_report(d)

 def test_parent_and_shared_parser_bytes_are_mandatory(self):
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

 def test_main_art_attachment_is_not_social_thumbnail_or_invalid_pixels(self):
  r=json.loads(m.REPORT.read_text());self.assertEqual(r['images'][0]['url'],r['extraction']['artwork_url']);self.assertEqual(r['images'][0]['mode'],'P');self.assertEqual(r['images'][0]['frames'],1)
  with self.assertRaises((ValueError,OSError)):m.inspect_image(b'<html>error</html>',r)
  changed=fixture().replace(b'class="image-main"',b'class="thumbnail"')
  with self.assertRaises(ValueError):m.parse(changed)

if __name__=='__main__':unittest.main()
