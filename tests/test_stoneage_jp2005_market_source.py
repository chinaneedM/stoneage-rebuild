import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import stoneage_jp2005_market_source as m

class MarketSourceTests(unittest.TestCase):
 def test_article_boundaries_are_unique_visible_and_not_menu_headings(self):
  r=json.loads(m.REPORT.read_text())
  for sid in ('S1','S2'):
   a=r['extraction']['articles'][sid]
   html=('<meta charset=shift_jis><h5>menu</h5><!--↓大見出し--><h5>'+a['title']+'</h5><!--↑大見出し--><div class="news_txt1">'+a['publication_as_written']+'</div><td class="newstext"><!-- 本文開始 -->synthetic evidence<!-- 本文終了 -->'+''.join('<a href="'+u+'">image</a>' for u in a['wrapper_urls'])+'<!-- tDialy:END -->').encode('cp932')
   actual=m.article(html,sid);self.assertEqual(actual['body'],'syntheticevidence')
   self.assertEqual(m.article(html+b'<script>outside=1</script>',sid),actual)
   for changed in (html+html,html.replace(b'class="newstext"',b'class="footer"'),html.replace(b'synthetic evidence',b'<script>synthetic evidence</script>'),html.replace(b'<!-- tDialy:END -->',b'')):
    with self.assertRaises(ValueError):m.article(changed,sid)

 def test_version_eligibility_and_unknowns_cannot_be_promoted_even_with_rebuilt_catalog(self):
  r=json.loads(m.REPORT.read_text());m.verify_report(r)
  changes=[lambda d:d.update(version_profile='JSS1999'),lambda d:d['negative_boundaries'].pop('freely_trade_means_zero_tax'),
   lambda d:d['extraction']['trade_system'].update(tax=0),lambda d:d['extraction'].update(market_attendee_eligibility='PAID'),
   lambda d:d['extraction']['venue'].update(map_id=123),lambda d:d['extraction']['announcement_service'].update(scope='MARKET_ATTENDEE'),
   lambda d:d['extraction']['announcement_service'].update(posting_status='PUBLISHED'),
   lambda d:d['extraction']['announcement_service'].update(exact_posting_cadence_days=14),
   lambda d:d['extraction']['announcement_service']['applicant_logic'].update(join='PAID_OR_SITE'),
   lambda d:d['extraction']['official_markets'][0].update(status='DEPLOYED'),
   lambda d:d['extraction']['retrospective'].update(independent_runtime_verification=True),
   lambda d:d['extraction'].update(exact_build='2005.06'),lambda d:d['extraction'].update(source_layer='DIRECT_OFFICIAL'),
   lambda d:d['image_observations'][0].update(actual_kind='GAME_MAP'),lambda d:d['images'][0].update(sha256='0'*64)]
  for change in changes:
   with self.subTest(change=change):
    d=copy.deepcopy(r);change(d);d['catalog_records']=m.catalog(d['extraction'])
    with self.assertRaises(ValueError):m.verify_report(d)

 def test_catalog_preserves_source_roles_rights_and_documentary_entities(self):
  r=json.loads(m.REPORT.read_text());self.assertEqual([e['collection'] for e in r['catalog_records']],['maps','tutorials','tutorials'])
  for key,value in [('source_refs',['OTHER']),('rights_status','RELEASE_APPROVED'),('game_ids',123),('verification_status','RUNTIME')]:
   d=copy.deepcopy(r);d['catalog_records'][0][key]=value
   with self.assertRaises(ValueError):m.verify_report(d)
  contract=json.loads((m.ROOT/m.PARENTS[2]).read_text())
  self.assertEqual(len(contract['future_website']['required_collections']),19)

 def test_cross_version_venue_and_listing_ui_are_not_shared_entities(self):
  r=json.loads(m.REPORT.read_text())
  for k in ('same_map_id_proven','same_stall_ui_proven','historical_evolution_proven','modern_adoption_decided'):
   d=copy.deepcopy(r);d['comparison'][k]=True
   with self.assertRaises(ValueError):m.verify_report(d)

 def test_parent_and_parser_bytes_are_mandatory(self):
  r=json.loads(m.REPORT.read_text())
  with tempfile.TemporaryDirectory() as name:
   root=Path(name)
   for pin in r['parent_pins']+[r['parser_dependency_pin']]:
    p=root/pin['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((m.ROOT/pin['path']).read_bytes())
   with patch.object(m,'ROOT',root):
    m.verify_report(r)
    for pin in r['parent_pins']+[r['parser_dependency_pin']]:
     p=root/pin['path'];b=p.read_bytes();p.write_bytes(b[:-1]+bytes([b[-1]^1]))
     with self.assertRaises(ValueError):m.verify_report(r)
     p.unlink()
     with self.assertRaises(FileNotFoundError):m.verify_report(r)
     p.write_bytes(b)

 def test_image_wrappers_are_actual_links_not_inferred_screen_evidence(self):
  r=json.loads(m.REPORT.read_text());self.assertEqual(len(r['images']),3)
  for i in r['images']:
   self.assertIn(i['wrapper_url'],r['extraction']['articles'][i['article']]['wrapper_urls'])
   self.assertEqual(i['image_url'],i['wrapper_url'].removesuffix('.html')+'.jpg')
  self.assertNotEqual(r['images'][0]['sha256'],r['images'][2]['sha256'])
  self.assertTrue(all(i['game_entity_identity'] is None for i in r['image_observations']))

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
   changes=[lambda d:d['runs'].append(d['runs'][0]),lambda d:d.update(content_commit='0'*40),
    lambda d:d['jobs_and_artifacts']['main']['artifact']['workflow_run'].update(head_branch='OTHER'),
    lambda d:d['jobs_and_artifacts']['main'].update(job=d['jobs_and_artifacts']['candidate']['job']),
    lambda d:d.update(current_http_bytes_are_historical_bytes=True),
    lambda d:d['raw_replays']['main'].update(equals_initial_inputs=False),
    lambda d:d.update(candidate_main_raw_bytes_equal=False),lambda d:d.update(initial_inputs=[]),
    lambda d:d['permanent_pins'].pop()]
   for change in changes:
    d=copy.deepcopy(receipt);change(d);path.write_text(json.dumps(d))
    with self.assertRaises(ValueError):m.verify_custody(root)
   path.unlink()
   with self.assertRaises(FileNotFoundError):m.verify_custody(root)

if __name__=='__main__':unittest.main()
