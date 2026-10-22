"""R79 content: early operator-hosted interaction descriptions and a name-card screen.

This content task is unrelated to the paused local savedata R79 branch.
"""
import argparse
import hashlib
import io
import json
import re
import urllib.request
from pathlib import Path
from PIL import Image
from tools.stoneage_jp2005_treasure_source import VisibleMarkup, plain, one, require, sha

ROOT=Path(__file__).resolve().parents[1]
STEM='STONEAGE-CN20-OPERATION-UI'
REPORT=ROOT/f'research/recovered/{STEM}-SOURCE-R1.json'
URL='https://web.archive.org/web/20011204000349id_/http://www.waei.com.cn/ZHUANQU/stoneage2/tyro/operation.asp'
IMAGE_URL='https://web.archive.org/web/20011227175240id_/http://waei.com.cn/ZHUANQU/stoneage2/tyro/img/4.gif'
PROFILE='EARLY_LINEAGE_CN_WAEI_SITE_2_0_CAPTURE_20011204_EXACT_BUILD_UNKNOWN'
PARSER='tools/stoneage_jp2005_treasure_source.py'
PARENTS=['research/recovered/STONEAGE-CN20-RECORDPOINT-SOURCE-R1.json',
 'research/recovered/STONEAGE-CN2003-UI-TEAM-TRADE-SOURCE-R1.json',
 'research/recovered/STONEAGE-JSS2001-MAIL-ITEMS-SHARED-VENUES-R1.json',
 'research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json']
LABELS=['一、移动','二、方向转移','三、对话','四、看板、告示板','五、道具','六、功能视窗栏',
 'a.系统视窗','b.地图视窗','c.状态视窗','d.宠物视窗','e.道具视窗','f.邮件视窗','七、相簿视窗','八、功能按键',
 'a.选项键','b.名片交换键','c.组队键','d.交易键','e.家族键','f.参战键','g.决斗键','h.动作键']
BOUNDARIES={k:False for k in ('operator_authorship_verified','capture_date_is_publication_or_build',
 'body_and_image_same_capture_or_build','tw10_or_jss1999_membership_verified','original_server_runtime_verified',
 'static_online_label_is_live_connection_test','mail_or_delete_button_execution_verified',
 'four_visible_slots_are_total_contact_capacity','english_label_authenticates_client_region',
 'cn_body_describes_double_trade_confirmation','cn_body_describes_leader_follow_or_team_yes',
 'cn_body_describes_jss_logout_permission_reset','help_limit_includes_pets','riding_permission_is_skill_or_pet_master',
 'invitation_means_all_manors_or_production_access','album_is_proven_automatic_complete_history',
 'pet_mail_proves_permanent_ownership_transfer',
 'audio_settings_prove_specific_audio_event','original_html_or_assets_committed','stage_b_started')}
VISUAL={'id':'I1','manual_visual_review':True,'kind':'STATIC_NAME_CARD_WINDOW_OVER_OUTDOOR_SCENE',
 'readable_title':'名片','readable_controls':['Mail','Delete'],'readable_fields':['LV','DP'],
 'status_labels':['Online','Offline'],'visible_rows':4,'populated_rows':3,'empty_rows':1,
 'visible_rows_are_total_capacity':False,'original_contact_or_character_ids':None,
 'actual_button_action_or_message_delivery_observed':False,'actual_online_state_verified':False,
 'bottom_right_label':'Eng','region_or_build_authenticated_by_label':False,
 'native_client_resolution_proven':False,'viewport_page_index_transcribed':False}


def article(raw):
 p=VisibleMarkup();p.feed(raw.decode('gb18030',errors='strict'));text=''.join(p.parts)
 require('<title>石器时代2.0</title>' in text,'Page title changed')
 begin='(稿务必注明所在服务器、作者及作品名称)';end='<span class="p12b">'
 require(text.count(begin)==1 and text.count(end)==1,'Unique article boundaries required')
 fragment=text.split(begin)[1].split(end)[0]
 require(plain(one(r'<div align="center"><font[^>]*>(.*?)</font></div>',fragment,re.S))=='基本操作','Article heading changed')
 rows=re.findall(r'<p><font\b[^>]*>(.*?)</font><br>(.*?)</p>',fragment,re.S|re.I)
 labels=[plain(a) for a,b in rows];require(labels==LABELS,'22 ordered visible sections required')
 sections={plain(a):plain(b) for a,b in rows}
 require(re.findall(r'<a href="([^"]+)" target="_blank"><img src="([^"]+)" width="(\d+)" height="(\d+)"',fragment)==[('img/4.gif','img/4s.gif','240','180')],'Actual article image/thumbnail changed')
 return plain(fragment),sections


def derive(raw):
 core,s=article(raw)
 def must(label,*clauses):require(all(c in s[label] for c in clauses),'Changed source clause: '+label)
 must('一、移动','点击鼠标左键，会往点击的地点移动','持续点住左键','跟随着鼠标指针移动','第一次抵达的地方，有时移动上会有有所延迟')
 must('二、方向转移','点鼠标右键','人物的方向就会依鼠标指针的方向变换')
 must('三、对话','按ENTER键','附近的玩家或团队内的人物','"Ctrl"+"空格"','画面下方','NPC面对面','任意输入文字并按"回车（Enter）"键')
 must('四、看板、告示板','面对对着看板或告示板按鼠标左键')
 must('五、道具','由地面拾起，或店内购得，以及战斗胜利后取得','记录到道具视窗内')
 panels=one(r'包括(.*?)。点击栏位',s['六、功能视窗栏']).split('、')
 must('六、功能视窗栏','鼠标指针移到画面最下方','"关闭"及"回上页"','Esc键关闭')
 must('a.系统视窗','对话文字的表示颜色及表示行数','背景音乐及节奏','音效的音量','立体音响的切换')
 must('b.地图视窗','玩家目前所在位置')
 must('c.状态视窗','人物的各种状态','组队后其他队友的状态信息')
 pet=s['d.宠物视窗'];modes=one(r'(战斗：.*)',pet)
 battle,waiting,rest,mail,ride=one(r'战斗：(.*?)等待：(.*?)休息：(.*?)邮件：(.*?)骑乘：(.*)',modes)
 require('一开始就可参加战斗' in battle and '只能设定一只' in battle and '战斗时和其他宠物交换' in waiting and rest=='让宠物休息。' and '叫宠物送信，只能设定一只' in mail,'Pet mode meaning changed')
 require('只有学习了骑乘宠物之后并且点选可以骑乘的宠物时才会出现该选项，一次只能设定一只' in ride,'Conjunctive riding visibility/limit changed')
 must('d.宠物视窗','"状态"键或者直接点击宠物的名字','详细列出宠物的属性资料')
 must('e.道具视窗','道具一览表及目前的装备状态','咒术：打开咒术画面，显示可使用的咒术表单')
 must('f.邮件视窗','已交换过名片的其他玩家','点击玩家姓名可以接收玩家发过来的邮件','普通邮件和宠物邮件','利用宠物作为送货员','朋友需要的道具')
 must('七、相簿视窗','从游戏开始到现在所拥有过的宠物都可以拍照留念','保存这些照片')
 must('八、功能按键','画面的左上方','战斗中点击鼠标左键可以选择指令、动作及人物','点击鼠标右键即取消指令')
 buttons=[x.split('.',1)[1] for x in LABELS[14:]]
 permissions=one(r'可进行(.*?)的设定',s['a.选项键']).split('、')
 must('b.名片交换键','在交换名片时使用');must('c.组队键','玩家可以组成冒险队伍')
 permission=one(r'接受交易要求的玩家必须将交易设定为([A-Z]+)',s['d.交易键'])
 require(permission=='YES','Recipient permission changed')
 family=s['e.家族键']
 require('可分为多个频道和家族全体频道' in family and '只有身为家族族长才能行使的职能' in family and '所有在线的家族成员都能看到' in family,'Family chat/authority/audience changed')
 require('可更改家族成员信息，并可设定家族是否继续招募成员' in family and '让位给家族的其他成员' in family,'Family membership/succession changed')
 require('只有四大庄园的族长才有权利制作家族邀请函' in family and '有邀请函的玩家可以在邀请函所属庄园内任意出入各个房间' in family,'Invitation issuer/access scope changed')
 require('学习同意书：就是玩家最关心的骑宠同意书，只有持此同意书的玩家才可在相应的庄园内学习骑宠技能' in family,'Study consent scope changed')
 must('f.参战键','出现HELP符号','靠近他们并将方向转为面向他们后','按下此键即可加入战斗帮助玩家')
 limit=int(one(r'战斗中的玩家人数最多为(\d+)个',s['f.参战键']))
 duel=one(r'准备接受战斗要求的玩家，须在功能选项里面将决斗设定为([A-Z]+)',s['g.决斗键']);require(duel=='YES','Duel opt-in changed')
 count=int(one(r'《石器时代2.0》中一共提供了(\d+)种',s['h.动作键']));must('h.动作键','点选此键后会出现动作的明细表')
 return {'pointer_and_text':{'move':'LEFT_CLICK_TARGET_OR_HOLD_FOLLOW_POINTER','face':'RIGHT_CLICK_DIRECTION','first_visit_delay':'SOMETIMES_REPORTED_NOT_FIXED_DURATION',
  'chat_recipients':'NEARBY_PLAYERS_OR_TEAM_AS_REPORTED','submit':'ENTER','chinese_input_shortcut_as_written':['Ctrl','空格'],'input_line':'BOTTOM',
  'npc':'FACE_NPC_THEN_TEXT_ENTER','sign':'FACE_SIGN_THEN_LEFT_CLICK'},
 'windows':{'bar_reveal':'POINTER_AT_SCREEN_BOTTOM','labels_as_listed':panels,'close_controls_as_written':['关闭','回上页','Esc'],
  'status_subsection_label':'状态视窗','status_includes_party_members_as_reported':True,'map':'CURRENT_PLAYER_LOCATION',
  'settings':['CHAT_COLOR_AND_LINE_COUNT','BGM_AND_RHYTHM_AS_WRITTEN','SFX_VOLUME_AND_STEREO_SWITCH'],'actual_audio_event':None,
  'items':'CARRIED_ITEMS_AND_EQUIPMENT_WITH_SPELL_LIST','item_sources':['GROUND_PICKUP','SHOP','BATTLE_VICTORY_AS_REPORTED_NOT_GUARANTEED']},
 'pet_modes':{'labels':['战斗','等待','休息','邮件','骑乘'],'single_pet_limits_as_reported':['战斗','邮件','骑乘'],
  'waiting':'CAN_EXCHANGE_WITH_OTHER_PETS_DURING_BATTLE','rest':'REST_DESCRIPTION_ONLY','details_controls':['状态','PET_NAME'],
  'ride_visibility':'LEARNED_RIDING_AND_SELECTED_RIDEABLE_PET','numeric_mode_ids':None,'extra_hidden_modes':None},
 'mail_album':{'contacts':'EXCHANGED_CARDS','click_player_name':'RECEIVE_MAIL_AS_DESCRIBED','mail_types':['普通邮件','宠物邮件'],
  'pet_mail':'MESSAGES_AND_ITEM_DELIVERY_DESCRIPTION','actual_delivery_or_save':None,
  'album_scope':'PETS_OWNED_SINCE_GAME_START_CAN_BE_PHOTOGRAPHED','automatic_complete_history':None,'storage_format':None},
 'top_buttons':{'position':'UPPER_LEFT','source_order':buttons,'order_is_explicit_left_to_right':False,'options':permissions,
  'team':'FORM_PARTY_ONLY','card_exchange':'EXCHANGE_USE_ONLY','trade_recipient_permission':permission,
  'double_ok_trade_or_leader_follow_described':False,'battle_left':'SELECT_COMMAND_ACTION_OR_ACTOR','battle_right':'CANCEL_COMMAND'},
 'family':{'channels':'MULTIPLE_AND_WHOLE_FAMILY','leader_functions_only_leader':True,'broadcast_audience':'ALL_ONLINE_FAMILY_MEMBERS',
  'management':['CHANGE_MEMBER_INFORMATION','CHANGE_RECRUITMENT_SETTING'],'succession':'OTHER_FAMILY_MEMBER',
  'invitation_issuers':'LEADERS_OF_FOUR_MANORS_AS_WRITTEN','invitation_access':'ROOMS_OF_ISSUING_MANOR','invitation_original_item_id':None,
  'study_document_label':'学习同意书','study_document_alias_as_written':'骑宠同意书','study_scope':'HOLDER_MAY_LEARN_RIDING_AT_CORRESPONDING_MANOR',
  'manor_names_ids_skill_or_pet_roster_prices':None},
 'help_duel_emotes':{'help_preconditions':['HELP_MARKER','APPROACH','FACE_PLAYER','PRESS_HELP_BUTTON'],'help_player_max_as_reported':limit,
  'pets_included_in_limit':None,'duel_recipient_permission':duel,'duel_exp_or_capturability':None,'emote_count_as_reported':count,'emote_names_or_sprite_ids':None},
 'image_reference':{'full':'img/4.gif','thumbnail':'img/4s.gif','inline_declared_size':[240,180]},
 'section_fingerprints':[{'label':k,'characters':len(v),'sha256':sha(v.encode())} for k,v in s.items()],
 'core_fingerprint':{'characters':len(core),'utf8_bytes':len(core.encode()),'sha256':sha(core.encode())},
 'exact_client_build':None,'publication_date':None,'operator_authorship_verified':False,'original_server_runtime_verified':False}


def pin(path):
 b=(ROOT/path).read_bytes();return {'path':path,'bytes':len(b),'sha256':sha(b),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}


def comparison():
 prior=json.loads((ROOT/PARENTS[0]).read_text());later=json.loads((ROOT/PARENTS[1]).read_text());jss=json.loads((ROOT/PARENTS[2]).read_text())
 return {'same_archived_html_as_recordpoint_package':{'url':prior['sources'][1]['url'],'bytes':prior['sources'][1]['bytes'],'sha256':prior['sources'][1]['sha256'],
  'previous_scope':'IN_PLACE_LOGOUT_AND_TRADE_YES_ONLY','new_body_discovered':False,'newly_structured_full_sections':22},
  'later_portal':{'source':later['sources'][0],'added_conditions_not_backfilled':['DOUBLE_OK_TRADE','TEAM_LEADER_FOLLOW_AND_TEAM_YES','SHORTCUT_CTRL_I_VS_CTRL_L'],
   'same_author_copying_or_same_build_proven':False,'earlier_capture_is_not_proof_of_feature_first_release':True},
  'jss':{'source':jss['source'],'card_exchange_logout_no_reset_backfilled_to_cn':False,'mail_battle_restrictions_or_stray_timers_backfilled_to_cn':False,'same_contact_ids_or_capacity_proven':False},
  'modern_adoption_decided':False}


def catalog(ex, image):
 rows=[(k,'tutorials','DOCUMENTARY_EARLY_UI_BEHAVIOR',ex[k],['S1']) for k in ('pointer_and_text','windows','pet_modes','mail_album','top_buttons','family','help_duel_emotes')]
 rows.append(('NAME_CARD_SCREEN','screens','DOCUMENTARY_STATIC_NAME_CARD_WINDOW',{'image':image,'observation':VISUAL},['S1','I1']))
 return [{'record_id':'CN20-R79-'+ident,'entity_type':kind,'collection':coll,'version_profile':PROFILE,'source_refs':refs,
  'verification_status':'OPERATOR_HOSTED_GUIDE_OR_STATIC_IMAGE_NOT_RUNTIME','rights_status':'RESEARCH_METADATA_NOT_RELEASE_APPROVED','record_revision':1,'game_ids':None,'content':content} for ident,coll,kind,content,refs in rows]


def validate(r):
 require(r['schema']=='stoneage.cn20_operation_ui.source.r1' and r['version_profile']==PROFILE and r['negative_boundaries']==BOUNDARIES,'Version/authority boundary changed')
 require(r['source']['url']==URL and r['source']['capture']=='20011204000349' and r['source']['authority']=='OPERATOR_HOSTED_UNSIGNED_GUIDE_AUTHOR_UNVERIFIED','Source authority changed')
 require(r['source']['first_publication'] is None and r['source']['http_status']==200 and r['source']['encoding']=='GB18030_STRICT' and r['source']['no_redirect'] is True,'Publication/intake promoted')
 require(r['parent_pins']==[pin(p) for p in PARENTS] and r['parser_pin']==pin(PARSER),'Parent/parser bytes changed')
 require(r['comparison']==comparison(),'Prior version differences overwritten')
 old=r['comparison']['same_archived_html_as_recordpoint_package']
 require(all(r['source'][k]==old[k] for k in ('url','bytes','sha256')) and r['source']['new_source_url'] is False,'Known source identity/discovery history changed')
 ex=r['extraction']
 require(all(ex[k] is None for k in ('exact_client_build','publication_date')) and ex['operator_authorship_verified'] is False and ex['original_server_runtime_verified'] is False,'Unknown history promoted')
 require(ex['pet_modes']['ride_visibility']=='LEARNED_RIDING_AND_SELECTED_RIDEABLE_PET' and ex['pet_modes']['numeric_mode_ids'] is None and ex['pet_modes']['extra_hidden_modes'] is None,'Pet visibility or original mode IDs invented')
 require(ex['top_buttons']['order_is_explicit_left_to_right'] is False and ex['top_buttons']['double_ok_trade_or_leader_follow_described'] is False,'Later ordering/confirmation conditions backfilled')
 require(ex['family']['invitation_access']=='ROOMS_OF_ISSUING_MANOR' and ex['family']['broadcast_audience']=='ALL_ONLINE_FAMILY_MEMBERS' and ex['family']['invitation_original_item_id'] is None and ex['family']['manor_names_ids_skill_or_pet_roster_prices'] is None,'Family scope promoted')
 require(all(ex['help_duel_emotes'][k] is None for k in ('pets_included_in_limit','duel_exp_or_capturability','emote_names_or_sprite_ids')) and all(ex['mail_album'][k] is None for k in ('actual_delivery_or_save','automatic_complete_history','storage_format')) and ex['windows']['actual_audio_event'] is None,'Unspecified rules inferred')
 image=r['image'];require(image['url']==IMAGE_URL and image['capture']=='20011227175240' and image['bytes']==155995 and image['sha256']=='e91b36552855db65420ca2c0762f7409ef797ce8d88c2d87532c6bac92322a4b' and image['size']==[640,480] and image['frames']==1 and image['format']=='GIF' and image['mode']=='P','Reviewed image identity changed')
 require(image['initial_request']=='https://web.archive.org/web/20011204000349id_/http://www.waei.com.cn/ZHUANQU/stoneage2/tyro/img/4.gif' and image['resolved_url']==IMAGE_URL and image['initial_request_same_capture_as_actual'] is False and image['initial_www_dropped_by_archive'] is True and image['thumbnail_pixels_acquired'] is False,'Image redirect/coverage history changed')
 require(r['visual_observation']==VISUAL and r['catalog_records']==catalog(ex,image),'Visual or catalog detached')
 contract=json.loads((ROOT/PARENTS[-1]).read_text())['future_website']
 require(len(r['catalog_records'])==8 and len({v['record_id'] for v in r['catalog_records']})==8,'Bounded record count changed')
 require(all(set(contract['record_contract']['required']).issubset(v) and v['collection'] in contract['required_collections'] for v in r['catalog_records']),'Incomplete archive contract')


MUTATIONS=[('最下方','最上方'),('地图、状况、宠物、道具、邮件、相簿、系统','地图、状况、宠物、道具、邮件、相簿'),
 ('按ENTER键','按ESC键'),('NPC面对面','NPC背对背'),('只能设定一只宠物','能设定两只宠物'),
 ('叫宠物送信，只能设定一只','叫宠物送信，可以设定两只'),('之后并且点选','之后或者点选'),
 ('接受交易要求的玩家必须将交易设定为YES','接受交易要求的玩家必须将交易设定为NO'),
 ('四大庄园的族长','任意家族的成员'),('邀请函所属庄园内','所有庄园内'),('所有在线的家族成员','所有家族成员'),
 ('只有持此同意书的玩家','任何玩家'),('相应的庄园内学习','任何庄园内学习'),
 ('最多为5个','最多为6个'),('点击鼠标右键即取消指令','点击鼠标右键即退出战斗'),('设定为YES','设定为NO'),
 ('提供了13种','提供了14种'),('已交换过名片','未交换过名片'),('拥有过的宠物都可以拍照','拥有过的宠物自动拍照'),
 ('立体音响的切换','固定攻击音效'),('组队后其他队友','所有玩家'),('战斗时和其他宠物交换','战斗时不可交换'),('任意出入各个房间','仅可出入大厅')]


def semantic(ex):
 return {k:v for k,v in ex.items() if k not in ('section_fingerprints','core_fingerprint')}


def audit(raw,expected):
 text=raw.decode('gb18030');target=semantic(expected)
 for old,new in MUTATIONS:
  require(old in text,'Missing real source mutation: '+old)
  try:actual=derive(text.replace(old,new).encode('gb18030'))
  except (ValueError,IndexError):continue
  require(semantic(actual)!=target,'Semantic change masked by fingerprint: '+old)
 require(derive(raw+b'<script>outside=1</script>')==expected,'Outer script changed source meaning')
 old='战斗中的玩家人数最多为5个。'
 for replacement in ('','<script>'+old+'</script>'):
  changed=text.replace(old,replacement)+'<div>'+old+'</div>'
  try:derive(changed.encode('gb18030'))
  except ValueError:pass
  else:raise ValueError('Outside/hidden evidence repaired missing article claim')
 return {'semantic_mutations_without_all_fingerprints':len(MUTATIONS),'hidden_and_outside_article_counterexamples':2,'outside_script_positive':True}


def inspect_image(raw,r):
 p=r['image']
 with Image.open(io.BytesIO(raw)) as im:
  im.load();actual={'bytes':len(raw),'sha256':sha(raw),'size':list(im.size),'format':im.format,'mode':im.mode,'frames':getattr(im,'n_frames',1)}
 require(all(p[k]==v for k,v in actual.items()),'Actual image bytes or complete decode changed')


def replay(inputs,r):
 validate(r);ex=derive(inputs['S1']);require(ex==r['extraction'],'Source semantics or fingerprints changed');inspect_image(inputs['I1'],r)
 require(len(inputs['S1'])==r['source']['bytes'] and sha(inputs['S1'])==r['source']['sha256'],'Archived original body bytes changed')
 return {'schema':'stoneage.cn20_operation_ui.replay.r1','inputs':[{'id':k,'url':URL if k=='S1' else IMAGE_URL,'bytes':len(v),'sha256':sha(v)} for k,v in inputs.items()],
  'extraction':ex,'image':r['image'],'visual_observation':r['visual_observation'],'comparison':comparison(),'catalog_records':catalog(ex,r['image']),
  'audit':audit(inputs['S1'],ex),'original_html_or_assets_in_output':False,'original_server_runtime_verified':False}


def read_inputs(directory=None):
 result={}
 for key,url in [('S1',URL),('I1',IMAGE_URL)]:
  if directory:result[key]=(Path(directory)/(key+('.html' if key=='S1' else '.gif'))).read_bytes()
  else:
   with urllib.request.urlopen(url,timeout=50) as h:
    require(h.status==200 and h.url==url,'Exact capture/status changed');result[key]=h.read()
 return result


def verify_custody(root=None):
 root=ROOT if root is None else Path(root)
 receipt=json.loads((root/f'research/recovered/{STEM}-CUSTODY-R1.json').read_text())
 require(receipt['schema']=='stoneage.cn20_operation_ui.custody.r1','Custody schema')
 require(receipt['content_commit']=='416cbe29e663b02665f0a24e1fef131ad9069941' and receipt['content_tree']=='2a06ae793788cdeb46664b78a39c97fb753fd851','Content Git identity')
 require(receipt['candidate_branch']=='agent/named-content-r79-ui-20261023','Candidate branch')
 require(receipt['server_execution_verified'] is False and receipt['same_build_body_image_proven'] is False and receipt['capture_date_is_publication_date'] is False,'Custody authority promoted')
 paths=[f'research/recovered/{STEM}-SOURCE-R1.json']+PARENTS+[PARSER]+[f'research/recovered/{STEM}-CI-{role}-R1.json' for role in ('CANDIDATE','MAIN')]
 pins=receipt['permanent_pins'];require([p['path'] for p in pins]==paths,'Eight mandatory permanent evidence pins changed')
 for p in pins:
  b=(root/p['path']).read_bytes()
  require(p=={'path':p['path'],'bytes':len(b),'sha256':sha(b),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()},'Permanent original bytes changed')
 source=json.loads((root/paths[0]).read_text())
 initial=[{'id':'S1','url':URL,'bytes':source['source']['bytes'],'sha256':source['source']['sha256']},
          {'id':'I1','url':IMAGE_URL,'bytes':source['image']['bytes'],'sha256':source['image']['sha256']}]
 require(receipt['initial_inputs']==initial,'Original intake/input dates lost')
 runs=receipt['runs'];require(len(runs)==21 and len({v['id'] for v in runs})==21,'Actual gate inventory missing/duplicated')
 branches={'candidate':receipt['candidate_branch'],'main':'main'}
 for role,count in (('candidate',10),('main',11)):
  group=[v for v in runs if v['branch']==branches[role]]
  require(len(group)==count and len({v['name'] for v in group})==count,'Branch gate inventory changed')
 require(all(v['head']==receipt['content_commit'] and v['status']=='completed' and v['conclusion']=='success' for v in runs),'Unverified/failed gate promoted')
 raw_files=[];jobs=[];artifacts=[]
 for role,branch in branches.items():
  proof=receipt['jobs_and_artifacts'][role];artifact=proof['artifact'];run=artifact['workflow_run']
  require(run['id']==proof['run'] and run['head_sha']==receipt['content_commit'] and run['head_branch']==branch,'Artifact origin detached')
  matching=[v for v in runs if v['id']==proof['run']]
  require(len(matching)==1 and matching[0]['branch']==branch and matching[0]['name']=='Verify early CN20 interaction conditions and name-card screen provenance','Wrong source workflow')
  require(proof['job_name']=='bounded-source-replay' and proof['job_conclusion']=='success' and artifact['name']=='cn20-operation-ui-derived-r79','Wrong job/artifact')
  require(proof['zip_downloaded_and_digest_verified'] is True and artifact['size_in_bytes']>0 and re.fullmatch(r'sha256:[0-9a-f]{64}',artifact['digest']),'ZIP custody missing')
  jobs.append(proof['job']);artifacts.append(artifact['id'])
  path=f'research/recovered/{STEM}-CI-{role.upper()}-R1.json';raw=(root/path).read_bytes();raw_files.append(raw);replayed=json.loads(raw)
  record=receipt['raw_replays'][role];p=next(v for v in pins if v['path']==path)
  require(all(record[k]==p[k] for k in p) and record['inputs']==replayed['inputs'] and record['equals_initial_inputs']==(replayed['inputs']==initial),'Raw identity/input equality misreported')
  require(all(replayed[k]==source[k] for k in ('extraction','image','visual_observation','comparison','catalog_records')),'Raw replay semantics detached')
  require(replayed['audit']=={'semantic_mutations_without_all_fingerprints':23,'hidden_and_outside_article_counterexamples':2,'outside_script_positive':True} and replayed['original_html_or_assets_in_output'] is False and replayed['original_server_runtime_verified'] is False,'Raw audit/authority promoted')
 require(len(set(jobs))==len(set(artifacts))==2 and receipt['candidate_main_raw_bytes_equal']==(raw_files[0]==raw_files[1]),'Candidate/main evidence substituted')
 return receipt


def main():
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--fetch',action='store_true');g.add_argument('--input-dir');p.add_argument('--output',required=True);a=p.parse_args()
 r=json.loads(REPORT.read_text());out=replay(read_inputs(a.input_dir),r)
 verify_custody()
 path=Path(a.output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('R79 early UI source replay passed; no original server execution or complete contact capacity proven.')


if __name__=='__main__':main()
