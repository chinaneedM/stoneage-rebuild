import copy
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from PIL import Image
from tools import stoneage_tw80_mount_certificate_equipment_source as m


def fixture():
 equip='“宠物装备”系统可依照不同类型的宠物，给予不同的装备字段，玩家也可以透过合成系统制作宠物装备。宠物装备区分为 7 大类，分别是头、 牙、 爪、 胸、 背、 翅、 脚(两只脚、四只脚、鱼鳍)。宠物装备本身就带有属性，依照地水火风相生相克关系产生能力的增减效果。'
 mount='8.0 版将开放 2 只骑宠，水魔鬼鱼“史卡鲁”和恐龙系中常被遗忘的“罗多克雷”。“史卡鲁”是这一次新庄园的庄园宠，主要出现在“泪之海”，取得不算困难，不过若是想要骑它，则要新庄园的族长发给骑宠证。'
 craft='原本的合成只到等级 11 级，这一次改版则提升到 15 级，料理、合成。'
 art='<th class=f21 height=44>《石器时代8.0》开放全新宠物装备(图)</th><tr><td height=24 align=center>http://games.sina.com.cn 2005-06-09 15:52 巴哈姆特</td></tr><!-- 内容 begin -->以下是来自中国台湾地区的消息：'+''.join('<p>'+v+'</p>' for v in (equip,mount,craft))+"<a href='"+m.GALLERY.replace('https:','http:')+"' target=_blank><img src='"+m.IMAGES[0]['url'].replace('https:','http:').replace('.jpg','_c.jpg')+"'></a>编辑：梁凌<!-- 内容 end -->"
 url=m.IMAGES[0]['url'].replace('https:','http:')
 gallery='<th class=f14 colspan=2>宠物装备套装</th><td style="padding:20 48 10 0" align=right colspan=2>http://games.sina.com.cn　2005-06-09 15:52　新浪游戏</td><!-- 图片 -->'+"<img name='myImage' src=\""+url+"\" alt='宠物装备套装' >"+'<A HREF='+url+' target=_blank class=n01>点击查看原图</a><td class=l15 bgcolor=#F4F4F4 style="padding:0 20 20 20"><font id="zoom">《石器时代8.0：失落的世界》全新改版今日正式上线。2只新的骑宠，宠物装备系统。<br><!-- 评论 begin -->'
 return {'S1':art.encode('gb18030'),'S2':gallery.encode('gb18030')}


class MountCertificateEquipmentTests(unittest.TestCase):
 def report(self):return json.loads(m.REPORT.read_text())
 def reject_extractions(self,changes):
  for change in changes:
   d=self.report();change(d['extraction']);d['catalog_records']=m.catalog(d['extraction'])
   with self.assertRaises(ValueError):m.validate(d)

 def test_visible_unique_scoped_paragraphs_and_real_gallery_chain(self):
  raw=fixture();ex=m.derive(raw);self.assertEqual(m.semantic(ex),m.semantic(self.report()['extraction']))
  for old,new in [('2005-06-09','2005-06-10'),('台湾地区','大陆地区'),('骑宠证','骑宠券'),('巴哈姆特','华义'),('编辑：梁凌','编辑：别人')]:
   d=dict(raw,S1=raw['S1'].decode('gb18030').replace(old,new).encode('gb18030'))
   with self.assertRaises(ValueError):m.derive(d)
  with self.assertRaises(ValueError):m.derive(dict(raw,S1=raw['S1']+raw['S1']))
  for replacement in ('','<script>新庄园的族长发给骑宠证</script>'):
   text=raw['S1'].decode('gb18030').replace('新庄园的族长发给骑宠证',replacement)+'<div>新庄园的族长发给骑宠证</div>'
   with self.assertRaises(ValueError):m.derive(dict(raw,S1=text.encode('gb18030')))
  with self.assertRaises(ValueError):m.derive(dict(raw,S2=raw['S2'].replace(b'F376D',b'F373D')))

 def test_semantic_negation_and_twenty_changes_are_not_only_fingerprint_guards(self):
  raw=fixture();raw['I1']=b'not used by derive';ex=m.derive(raw)
  self.assertEqual(m.audit(raw,ex),dict(semantic_mutations_without_all_fingerprints=20,gallery_identity_mutations=3,hidden_and_outside_article_counterexamples=2,outside_script_positive=True))
  bad=dict(raw,S1=raw['S1'].decode('gb18030').replace('透过合成系统制作宠物装备','不能透过合成系统制作宠物装备').encode('gb18030'))
  with self.assertRaises(ValueError):m.derive(bad)

 def test_certificate_condition_belongs_only_to_named_shikalu_not_both_or_cn20_courses(self):
  ex=self.report()['extraction'];a,b=ex['riding']['pets'];self.assertEqual(a['name_as_written'],'史卡鲁');self.assertEqual(a['main_habitat_as_written'],'泪之海');self.assertIsNone(b['riding_condition'])
  self.reject_extractions([lambda e:e['riding']['pets'][1].update(riding_condition=e['riding']['pets'][0]['riding_condition']),lambda e:e['riding']['pets'][0].update(certificate_item_id_issuer_name_coordinates_cost_or_consumption=100),lambda e:e['riding'].update(announced_mount_addition_is_new_species_introduction=True),lambda e:e['riding'].update(training_level_loyalty_combat_stats_or_character_compatibility=100)])

 def test_seven_categories_foot_subtypes_pet_type_and_element_effect_not_numeric_rule(self):
  ex=self.report()['extraction'];self.assertEqual(len(ex['equipment']['categories_as_written']),7);self.assertEqual(ex['equipment']['foot_type_parenthetical_as_written'],['两只脚','四只脚','鱼鳍'])
  self.reject_extractions([lambda e:e['equipment'].update(reported_category_count=9),lambda e:e['equipment'].update(slots_depend_on_pet_type=False),lambda e:e['equipment'].update(all_seven_slots_for_every_pet_or_body_type_matrix='ALL'),lambda e:e['equipment'].update(numeric_modifiers_stacking_rounding_or_gear_base_stats=1),lambda e:e['crafting_context'].update(character_level_or_all_recipe_ids=15)])

 def test_republication_and_static_panel_do_not_authenticate_original_build_or_io(self):
  r=self.report();m.validate(r)
  for key in m.BOUNDARIES:
   d=copy.deepcopy(r);d['negative_boundaries'][key]=True
   with self.assertRaises(ValueError):m.validate(d)
  for key in ['depicted_pet_is_reported_shikalu_or_luoduokelei','displayed_stats_are_species_master_or_growth','element_bar_lengths_are_numeric_percentages','static_cursor_proves_successful_equipping','all_pet_types_have_same_slots_proven','historical_2005_pixels_authenticated']:
   d=copy.deepcopy(r);d['visual_observations'][0][key]=True
   with self.assertRaises(ValueError):m.validate(d)
  self.reject_extractions([lambda e:e['source_scope'].update(today_resolved_to_exact_launch_day='2005-06-09'),lambda e:e['source_scope'].update(gnn_original_retrieved_this_round=True)])
  with self.assertRaises((ValueError,OSError)):m.inspect_images({'I1':b'not jpeg'})

 def test_five_documentary_rows_and_original_parent_parser_bytes(self):
  r=self.report();c=json.loads((m.ROOT/m.PARENTS[-1]).read_text())['future_website'];self.assertEqual(len(r['catalog_records']),5)
  for key in c['record_contract']['required']:
   d=copy.deepcopy(r);d['catalog_records'][0].pop(key)
   with self.assertRaises(ValueError):m.validate(d)
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

 def test_each_html_wrapper_identity_is_recorded_without_rewriting_initial_intake(self):
  raw=fixture();ex=m.derive(raw);r=self.report();r['extraction']=ex
  buf=io.BytesIO();Image.new('RGB',(8,8),'white').save(buf,format='JPEG');raw['I1']=buf.getvalue()
  images=copy.deepcopy(m.IMAGES);images[0].update(bytes=len(raw['I1']),sha256=m.sha(raw['I1']),size=[8,8]);sources=copy.deepcopy(m.SOURCES)
  for s in sources:s.update(initial_intake_bytes=len(raw[s['id']]),initial_intake_sha256=m.sha(raw[s['id']]))
  r.update(sources=sources,images=images)
  with patch.object(m,'SOURCES',sources),patch.object(m,'IMAGES',images):
   r['catalog_records']=m.catalog(ex);first=m.replay(raw,r);changed=m.replay(dict(raw,S2=raw['S2']+b'<script>other=1</script>'),r)
   self.assertEqual(first['source_identity']['html_equals_initial_intake'],{'S1':True,'S2':True});self.assertEqual(changed['source_identity']['html_equals_initial_intake'],{'S1':True,'S2':False})
   self.assertEqual(first['extraction'],changed['extraction']);self.assertNotEqual(first['inputs'][1],changed['inputs'][1]);self.assertEqual(sources[1]['initial_intake_sha256'],m.sha(raw['S2']))

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
                  lambda d:d.update(current_bytes_authenticate_2005_original=True),lambda d:d.update(original_operator_script_acquired=True),
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
                  lambda d:d.update(certificate_applies_to_both_mounts=True),lambda d:d.update(seven_categories_are_all_pet_slot_matrix=True),
                  lambda d:d.update(static_cursor_is_equipping_trace=True)]
         for change in changes:
             d=copy.deepcopy(receipt);change(d);out.write_text(json.dumps(d))
             with self.assertRaises(ValueError):m.verify_custody(root)
         out.unlink()
         with self.assertRaises(FileNotFoundError):m.verify_custody(root)

if __name__=='__main__':unittest.main()
