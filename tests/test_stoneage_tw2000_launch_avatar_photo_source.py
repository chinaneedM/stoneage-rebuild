import copy
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from PIL import Image
from tools import stoneage_tw2000_launch_avatar_photo_source as m


def fixture():
 quote='網路電玩石器時代上線了'+''.join(m.CLAUSES).replace('37版/3C新聞網','37版/3C 新聞網')+'。'
 caption='華義國際今年3月底將推出 圖／聯合報系資料照 （2000/02/10 林信昌攝影）'
 return ('<article class="article"><h1 id="story_art_title" class="story_art_title">'+m.TITLE+'</h1><div id="story_bady_info" class="story_bady_info_author">2023-04-13 13:22 報時光</div>'
  +'<figure class="photo_center"><img src="'+m.IMAGES[0]['url']+'"><figcaption>'+caption+'</figcaption></figure>'
  +'而計算費用方式採計次而非計時，外文騎乘介紹不在引文內。<blockquote class="article-blockquote article-blockquote__1">'+quote+'</blockquote><div id="story_end"></div></article>').encode()


class LaunchAvatarPhotoTests(unittest.TestCase):
 def report(self):return json.loads(m.REPORT.read_text())
 def reject_extractions(self,changes):
  for change in changes:
   d=self.report();change(d['extraction']);d['catalog_records']=m.catalog(d['extraction'])
   with self.assertRaises(ValueError):m.validate(d)

 def test_unique_visible_quote_reprint_date_independent_photo_credit_and_actual_proxy_link(self):
  raw=fixture();ex=m.derive(raw);self.assertEqual(m.semantic(ex),m.semantic(self.report()['extraction']))
  self.assertEqual(m.derive(raw+b'<script>outside=1</script>'),ex)
  for changed in [raw+raw,raw.replace(b'2023-04-13',b'2000-04-11'),raw.replace(b'2000/02/10',b'2000/04/11'),raw.replace(b'fw=800',b'fw=1600'),raw.replace(b'2000-04-11',b'2000-04-12'),raw.replace(m.TITLE.encode(),b'OTHER')]:
   with self.assertRaises(ValueError):m.derive(changed)
  for replacement in ('','<script>'+m.COUNT+'</script>'):
   changed=raw.decode().replace(m.COUNT,replacement)+'<div>'+m.COUNT+'</div>'
   with self.assertRaises(ValueError):m.derive(changed.encode())

 def test_publisher_reprint_is_not_original_scan_operator_source_or_exact_build(self):
  r=self.report();m.validate(r)
  for key in m.BOUNDARIES:
   d=copy.deepcopy(r);d['negative_boundaries'][key]=True
   with self.assertRaises(ValueError):m.validate(d)
  for key,value in [('original_2000_paper_scan_acquired',True),('original_2000_digital_photo_master_acquired',True),('official_operator_authorship_verified',True),('current_bytes_authenticate_2000_original',True),('exact_client_build','TW1.0')]:
   d=copy.deepcopy(r);d['source'][key]=value
   with self.assertRaises(ValueError):m.validate(d)

 def test_wrapper_changes_preserve_selected_core_and_actual_input_identity_is_honest(self):
  raw=fixture();ex=m.derive(raw);r=self.report();r['extraction']=ex;r['catalog_records']=m.catalog(ex)
  buf=io.BytesIO();Image.new('RGB',(8,8),'white').save(buf,format='JPEG');pixels=buf.getvalue()
  images=copy.deepcopy(m.IMAGES);images[0].update(bytes=len(pixels),sha256=m.sha(pixels),size=[8,8])
  source=copy.deepcopy(m.SOURCE);source.update(initial_intake_bytes=len(raw),initial_intake_sha256=m.sha(raw));r.update(source=source,images=images)
  with patch.object(m,'SOURCE',source),patch.object(m,'IMAGES',images):
   r['catalog_records']=m.catalog(ex);m.validate(r)
   first=m.replay({'S1':raw,'I1':pixels},r);changed=m.replay({'S1':raw+b'<script>outside=2</script>','I1':pixels},r)
   self.assertTrue(first['source_identity']['full_html_equals_initial_intake']);self.assertFalse(changed['source_identity']['full_html_equals_initial_intake'])
   self.assertNotEqual(first['inputs'][0]['sha256'],changed['inputs'][0]['sha256']);self.assertEqual(first['extraction'],changed['extraction'])
   with self.assertRaises(ValueError):m.replay({'S1':raw.replace(b'48',b'49'),'I1':pixels},r)
   self.assertEqual(source['initial_intake_sha256'],m.sha(raw))

 def test_four_and_forty_eight_not_192_twelve_models_or_native_roster_values(self):
  e=self.report()['extraction'];self.assertEqual(e['character_selection']['reported_color_count'],4);self.assertEqual(e['character_selection']['reported_different_appearance_count'],48)
  self.reject_extractions([lambda e:e['character_selection'].update(computed_192_or_12_base_models=192),lambda e:e['character_selection'].update(original_names_ids_selector_values_or_complete_roster=list(range(48))),
   lambda e:e['character_selection'].update(same_exact_build_as_preserved_tw10_client_or_cn20_guide=True),lambda e:e['quoted_report'].update(exact_server_launch_day_inferred='2000-04-10'),
   lambda e:e['defeat_claim'].update(hp_zero_injury_revive_exact_penalty_or_condition_formula=1),lambda e:e['payment_claim'].update(per_minute_or_per_session_unit_prices_and_all_titles_equal_cost='PER_SESSION'),lambda e:e.update(excluded_outer_claims=[])])
  for group,key in [('tw10','native_13_create_field_values_or_layout_filled'),('cn20','counts_backfilled_from_tw_report')]:
   d=self.report();d['comparison'][group][key]=True
   with self.assertRaises(ValueError):m.validate(d)

 def test_photographed_title_menu_is_not_native_screenshot_login_trace_or_count_display(self):
  r=self.report();self.assertEqual(r['images'][0]['size'],[800,450]);self.assertEqual(r['visual_observations'][0]['visible_modern_watermark'],'報時光')
  for key in ['button_text_or_account_fields_readable','native_screenshot_pixel_coordinates_or_resolution_verified','button_interaction_audio_or_server_login_verified','48_avatar_choices_visible','native_avatar_names_ids_or_animation_verified','historical_2000_pixels_authenticated','caption_credit_is_actual_2000_file_authentication']:
   d=copy.deepcopy(r);d['visual_observations'][0][key]=True
   with self.assertRaises(ValueError):m.validate(d)
  self.reject_extractions([lambda e:e['photo_context'].update(photograph_is_direct_screenshot=True),lambda e:e['photo_context'].update(photo_date_is_quoted_report_date=True),lambda e:e['photo_context'].update(direct_master_bytes_acquired=True)])
  with self.assertRaises((ValueError,OSError)):m.inspect_images({'I1':b'<html>403</html>'})

 def test_four_documentary_rows_keep_seven_required_fields_rights_and_no_native_ids(self):
  r=self.report();c=json.loads((m.ROOT/m.PARENTS[-1]).read_text())['future_website'];self.assertEqual(len(r['catalog_records']),4)
  for row in r['catalog_records']:
   self.assertTrue(set(c['record_contract']['required']).issubset(row));self.assertIn(row['collection'],c['required_collections']);self.assertIsNone(row['game_ids'])
  for key in c['record_contract']['required']:
   d=copy.deepcopy(r);d['catalog_records'][0].pop(key)
   with self.assertRaises(ValueError):m.validate(d)
  d=copy.deepcopy(r);d['catalog_records'][0]['rights_status']='RELEASE_APPROVED'
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
         for index,p in enumerate(receipt['permanent_pins']):
             target=root/p['path'];raw=target.read_bytes();corrupt=raw[:-1]+bytes([raw[-1]^1]);target.write_bytes(corrupt)
             d=copy.deepcopy(receipt);d['permanent_pins'][index].update(bytes=len(corrupt),sha256=m.sha(corrupt),git_blob=m.hashlib.sha1(b'blob '+str(len(corrupt)).encode()+b'\0'+corrupt).hexdigest())
             out.write_text(json.dumps(d))
             with self.assertRaises(ValueError):m.verify_custody(root)
             target.write_bytes(raw)
         changes=[lambda d:d.update(content_commit='0'*40),lambda d:d.update(content_tree='0'*40),
                  lambda d:d.update(candidate_branch='main'),lambda d:d.update(server_execution_verified=True),
                  lambda d:d.update(current_bytes_authenticate_2000_original=True),lambda d:d.update(original_2000_paper_scan_acquired=True),
                  lambda d:d['runs'].pop(),lambda d:d['runs'].append(d['runs'][0]),lambda d:d['runs'][0].update(conclusion='failure'),
                  lambda d:d['runs'][0].update(id=1),lambda d:d['runs'][0].update(name='OTHER'),
                  lambda d:d['jobs_and_artifacts']['main'].update(job=1),lambda d:d['jobs_and_artifacts']['main']['artifact'].update(id=1),
                  lambda d:d['runs'][0].update(branch='OTHER'),lambda d:d['permanent_pins'].pop(),
                  lambda d:d.update(initial_inputs=[]),lambda d:d.update(candidate_main_raw_bytes_equal=not d['candidate_main_raw_bytes_equal']),
                  lambda d:d['raw_replays']['main'].update(equals_initial_inputs=not d['raw_replays']['main']['equals_initial_inputs']),
                  lambda d:d['jobs_and_artifacts']['main'].update(job=d['jobs_and_artifacts']['candidate']['job']),
                  lambda d:d['jobs_and_artifacts']['main']['artifact'].update(id=d['jobs_and_artifacts']['candidate']['artifact']['id']),
                  lambda d:d['jobs_and_artifacts']['main']['artifact']['workflow_run'].update(head_branch='OTHER'),
                  lambda d:d['jobs_and_artifacts']['main'].update(zip_downloaded_and_digest_verified=False),
                  lambda d:d['jobs_and_artifacts']['main']['artifact'].update(digest='sha256:'+'0'*64),
                  lambda d:d['jobs_and_artifacts']['candidate']['artifact'].update(size_in_bytes=1),
                  lambda d:d.update(reported_counts_fill_native_roster=True),lambda d:d.update(photo_is_direct_screenshot=True),
                  lambda d:d.update(outer_riding_is_launch_rule=True)]
         for change in changes:
             d=copy.deepcopy(receipt);change(d);out.write_text(json.dumps(d))
             with self.assertRaises(ValueError):m.verify_custody(root)
         out.unlink()
         with self.assertRaises(FileNotFoundError):m.verify_custody(root)

if __name__=='__main__':unittest.main()
