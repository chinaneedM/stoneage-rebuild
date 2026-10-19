"""Nine previously unstructured sections in an authenticated JSS manual.

Source descriptions are not server transactions, original IDs, or later-version rules.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from urllib.error import HTTPError,URLError
from urllib.request import Request,urlopen
from tools.stoneage_early_content_probe import section,integer,require

ORIGINAL='http://www.titan.co.jp/stoneage/manual02.html'
CAPTURE='20010418083149'
URL='https://web.archive.org/web/'+CAPTURE+'id_/'+ORIGINAL
SOURCE_SHA='50b9771ec501067136629c8e083a190e979e53dd9ba141903f78b76d43b602cc'
REPORT=Path('research/recovered/STONEAGE-JSS2001-MAIL-ITEMS-SHARED-VENUES-R1.json')
ANCHORS=('3060','3070','7000','7010','7020','8030','8040','8110','8120')
PINS={
 '3060':(346,'ed66b5e7ceabf56069fcbd38aea772d2823e6e2a6bcf3065df25b4f056821c0d'),
 '3070':(422,'a9ec010c1d0c9fc8efb73d283302ba86299d967991071a77a15a2b1033d9124a'),
 '7000':(59,'47119e6d05e502ba0590666b1be6b14bf0b680e3a28c2a1f5d310adba3897139'),
 '7010':(104,'41953da179cf8033ea6f915832830f4b71713a96b93a037f441443b238e1c014'),
 '7020':(40,'dcfda6675dd51d9e1b78feca3e83a78bf22bfadc9890038f65c2269395982c19'),
 '8030':(215,'7bd6367e6bf0331dedb525558ce2b788d49d606c654204aa72a4ebddfe6da20f'),
 '8040':(72,'823d8b2d05c66582b082bbc94fbd51ddc08c10a2f5c9c5ae5db37248700e13d3'),
 '8110':(203,'73d14802f0a5f951471f2cbc782ed7776ed0d88b29a6e40f7b1cf3d30719679b'),
 '8120':(307,'b10e32717d7488e4c55124ab530dc4e6de2a2ed57ee1edcdaca84ebcfd8bc6b4'),
}
VILLAGES=['サムギル','マリナス','ジャジャ','カルターナ']
LABELS=['ITEM_WINDOW_AND_MONEY_PLACEMENT','ORDINARY_AND_PET_MAIL','ITEM_INVENTORY_ENTRY','ITEM_TARGET_SELECTION','GROUND_ITEM_PICKUP','CARD_EXCHANGE_CONSENT','DATED_LOCAL_CHAT_LOG','SHARED_CHATROOM','SHARED_DUEL_ARENA']


def derive(parts):
    require(tuple(parts)==ANCHORS,'Exact selected section order required')
    def mentions(a,*tokens):require(all(t in parts[a] for t in tokens),a+': missing source assertion')
    mentions('3060','ダブルクリック','アイテムによっては','ドラッグ＆ドロップ','金額を調節','地面に置きます')
    mentions('3070','名刺交換','メッセージやアイテム','拾わずにログアウト','戻ってくる前にログアウト','数時間','野良ペット','一定時間で消滅','メールの送受信はできますが、ペットメールの送受信はできません')
    mentions('7000','拾ったり','店でアイテムを買うと','アイテム欄に入ります')
    mentions('7010','ダブルクリック','グループウィンドウ','キャラクターの名前を左クリック')
    mentions('7020','隣接','右クリック')
    mentions('8030','YES','隣接','方向を向いて','メールウィンドウ','ログアウトすると自動的にNO','グループを組んでいる状態のプレイヤー同士')
    mentions('8040','stoneage','chatxxxxxx.txt','日付','保存')
    for a in ('8110','8120'):mentions(a,*VILLAGES,'共通','チケット','地面に落とすと消えて','ログアウトすればSPから再開')
    mentions('8110','無料','大広間','結婚式場','闘技場から入られた方')
    mentions('8120','チケットを購入','以下','場合は無料','回復無料','観戦')
    rooms=integer(parts['8110'],r'([0-9０-９]+)つの部屋','chat room count')
    level=integer(parts['8120'],r'レベルが([0-9０-９]+)以下','arena free level ceiling')
    ranks=re.search(r'ランキングが([0-9０-９]+)位と([0-9０-９]+)位',parts['8120']);require(ranks is not None,'Arena free-rank cases missing')
    rank_values=[int(v.translate(str.maketrans('０１２３４５６７８９','0123456789'))) for v in ranks.groups()]
    matches=integer(parts['8120'],r'試合場が([0-9０-９]+)つ','arena duel match areas')
    require((rooms,level,rank_values,matches)==(3,9,[77,777],4),'Manual numeric source contract changed')
    ticket={'drop_causes_immediate_disappearance_described':True,'resulting_exit_problem_described':True,'logout_restart_at_sp_described':True,'ticket_id_or_same_item_across_venues':None,'restores_ticket_on_login_proven':False,'runtime_inventory_or_save_transaction':None}
    return [
      {'use_control':'DOUBLE_CLICK','target_window_depends_on_item':True,'all_items_always_require_target_window':False,'equip_controls':['DRAG_DROP_EQUIPMENT_FIELD','DOUBLE_CLICK'],'money_placement':'ADJUST_AMOUNT_THEN_PLACE_ON_GROUND','stack_bag_limits_money_validation_or_item_ids':None},
      {'contacts_from_card_exchange':True,'pet_mail_can_carry_message_or_item_described':True,'pet_mail_requires_pet_mail_mode_described':True,'returned_uncollected_pet_plus_logout':'BECOMES_STRAY','logout_before_pet_return':'FOR_SEVERAL_UNSPECIFIED_HOURS_LOGIN_RETURNS_PET_NEAR_PLAYER_THEN_STRAY','stray_expiry':'DISAPPEARS_AFTER_SEPARATE_UNSPECIFIED_TIME','ordinary_mail_send_receive_during_battle':True,'pet_mail_send_receive_during_battle':False,'grace_hours_stray_ttl_pet_ids_or_persistence_format':None},
      {'ground_pickup_and_shop_purchase_enter_inventory_described':True,'inventory_slot_capacity_ids_or_save_fields':None},
      {'source_procedure':['DOUBLE_CLICK_ITEM','GROUP_TARGET_WINDOW','LEFT_CLICK_CHARACTER_NAME'],'every_item_requires_this_target_procedure':False,'item_effect_or_consumption_transaction':None},
      {'adjacent_required_described':True,'control':'RIGHT_CLICK_GROUND_ITEM','range_coordinates_ownership_flags_and_packet':None},
      {'exchange_setting_yes_required':True,'adjacent_and_facing_required':True,'control':'LEFT_CLICK_CARD_EXCHANGE_BUTTON','contact_registered_in_mail_window':True,'logout_resets_exchange_setting_to_no':True,'logout_deletes_contact_records_proven':False,'exchange_between_grouped_players_unavailable_described':True,'all_possible_party_to_nonparty_cases_resolved':False,'wire_and_persistence_fields':None},
      {'local_folder_as_written':'stoneage','filename_pattern_as_written':'chatxxxxxx.txt','placeholder_means_date':True,'server_chat_archive_or_cloud_sync_proven':False,'date_format_encoding_exact_path_or_write_callsite':None},
      {'named_entrances_as_written':VILLAGES,'direct_chatroom_admission_described_as_free':True,'rooms':rooms,'large_hall':True,'wedding_venue':True,'arena_connection_described':True,'arena_origin_visitors_free_movement_described':True,'ticket_warning':dict(ticket),'all_free_chat_visitors_need_paid_ticket_proven':False,'map_id_routes_prices_and_server_events':None},
      {'named_entrances_as_written':VILLAGES,'normal_entry_ticket_purchase_described':True,'free_admission_enumerated_cases':[{'level_at_most':level},{'duel_rank_exact':rank_values[0]},{'duel_rank_exact':rank_values[1]}],'free_cases_combination':'ANY_DESCRIBED_CASE_NOT_ALL_CONDITIONS_TOGETHER','ticket_price_or_other_unmentioned_exemptions':None,'hospital_recovery_free_in_arena_context':True,'all_world_hospitals_free_proven':False,'shops_described':['WEAPON','ARMOR','TOOL'],'duel_match_areas':matches,'can_watch_other_duels':True,'chatroom_connection_described':True,'ticket_warning':dict(ticket),'map_id_routes_prize_or_dp_formula':None},
    ]


def validate_contract(records):
    require(len(records)==9,'Nine selected record contracts required')
    b=[r['source_described_behavior'] for r in records];mail=b[1];card=b[5];chat=b[7];arena=b[8]
    require(b[0]['all_items_always_require_target_window'] is False and b[3]['every_item_requires_this_target_procedure'] is False,'Conditional item target UI generalized')
    require(b[6]['server_chat_archive_or_cloud_sync_proven'] is False,'Local chat filename promoted to server/cloud storage')
    require(mail['ordinary_mail_send_receive_during_battle'] is True and mail['pet_mail_send_receive_during_battle'] is False,'Ordinary and pet mail battle restrictions conflated')
    require(mail['grace_hours_stray_ttl_pet_ids_or_persistence_format'] is None and mail['returned_uncollected_pet_plus_logout']=='BECOMES_STRAY','Mail logout lifecycle or unknown timer boundary lost')
    require(card['logout_resets_exchange_setting_to_no'] is True and card['logout_deletes_contact_records_proven'] is False,'Consent reset is not contact deletion')
    require(chat['direct_chatroom_admission_described_as_free'] is True and chat['all_free_chat_visitors_need_paid_ticket_proven'] is False,'Chatroom free admission and contextual ticket warning conflated')
    require(arena['free_admission_enumerated_cases']==[{'level_at_most':9},{'duel_rank_exact':77},{'duel_rank_exact':777}] and arena['free_cases_combination']=='ANY_DESCRIBED_CASE_NOT_ALL_CONDITIONS_TOGETHER','Arena free-entry cases changed or conjoined')
    require(arena['all_world_hospitals_free_proven'] is False and arena['ticket_price_or_other_unmentioned_exemptions'] is None,'Local arena free recovery generalized or price invented')
    for venue in (chat,arena):
        t=venue['ticket_warning'];require(t['drop_causes_immediate_disappearance_described'] is True and t['ticket_id_or_same_item_across_venues'] is None and t['restores_ticket_on_login_proven'] is False,'Ticket identity/logout restoration invented')
    for r in records:
        require(r['server_runtime_observed'] is False and r['original_entity_ids_and_cross_version_binding'] is None,'Original runtime or same-build identities promoted')
        require(r['rights_status']!='RELEASE_APPROVED','Historical metadata given asset reuse rights')


def build(raw,final):
    require(final==URL,'Manual source host/path/capture mismatch')
    require(len(raw)==28434 and sha256(raw).hexdigest()==SOURCE_SHA,'Authenticated manual byte pin mismatch')
    doc=raw.decode('shift_jis',errors='strict');parts={a:section(doc,a) for a in ANCHORS}
    for a,t in parts.items():require((len(t),sha256(t.encode()).hexdigest())==PINS[a],'Selected section fingerprint changed: '+a)
    facts=derive(parts);records=[]
    for i,(anchor,behavior) in enumerate(zip(ANCHORS,facts)):
        records.append({'record_id':'jss2001-manual:mail-items-venues:'+anchor,'collection':'maps' if i>=7 else 'tutorials',
          'entity_type':'FIRST_PARTY_MANUAL_VENUE_DESCRIPTION' if i>=7 else 'FIRST_PARTY_MANUAL_INTERACTION_DESCRIPTION',
          'record_revision':1,'version_profile':'JSS_JAPAN_WEB_MANUAL_20010418','source_refs':[{'source':ORIGINAL,'actual_capture':CAPTURE,'sha256':SOURCE_SHA,'section_anchor':anchor,'normalized_section_sha256':PINS[anchor][1]}],
          'verification_status':'MANUAL_DESCRIPTION_NOT_SERVER_EXECUTION','rights_status':'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED',
          'topic':LABELS[i],'source_described_behavior':behavior,'original_entity_ids_and_cross_version_binding':None,'server_runtime_observed':False})
    validate_contract(records)
    return {'schema':'stoneage.jss2001.mail_items_shared_venues.r1','date':'2026-10-19','task':'JSS2001-MAIL-ITEM-AND-SHARED-VENUE-CONTENT-01',
      'source':{'original_url':ORIGINAL,'strict_replay_url':final,'actual_capture':CAPTURE,'bytes':len(raw),'sha256':SOURCE_SHA,'encoding':'SHIFT_JIS_STRICT','newly_discovered_source':False,'newly_structured_sections':list(ANCHORS),'previous_generic_fingerprint_catalog':{'path':'research/recovered/JSS-LOGIN-MANUAL-CREATION-CONTRACT-R1.json','already_fingerprinted_selected_anchors':['3070', '7010', '8030'],'manual02_prior_creation_contract':None,'new_material_is_behavior_semantics_not_first_fingerprint':True}},
      'section_fingerprints':{a:{'normalized_characters':n,'sha256':h} for a,(n,h) in PINS.items()},'records':records,
      'coverage':{'newly_discovered_original_urls':0,'known_source_reacquired':1,'newly_structured_sections':9,'source_qualified_interaction_records':7,'source_qualified_venue_records':2,'images_or_binaries_acquired':0},
      'boundaries':{'jss1999_tw10_cn182_same_build_proven':False,'ordinary_ground_expiry_equals_immediate_special_ticket_drop':False,'chatroom_or_duel_arena_equals_later_quiz_theatre_or_arcades':False,'mail_grace_period_equals_stray_expiry_or_ground_item_timer':False,'unknown_original_server_or_save_io_recovered':False,'original_html_images_or_programs_in_git':False,'stage_a_families':'7_PARTIAL_2_OPEN','stage_b_and_wiki':'GATED','r79':'PAUSED_NON_BLOCKING'},
      'next':'EARLY-SOURCE-MAIL-VENUE-CROSS-VERSION-BOUNDARY-01'}


def acquire():
    for attempt in range(2):
        try:
            with urlopen(Request(URL,headers={'User-Agent':'Mozilla/5.0 StoneAgeHistoricalEvidence'}),timeout=35) as r:return r.read(100001),r.url
        except HTTPError as e:
            if attempt or e.code not in (502,503,504):raise
            print('BOUNDED_RETRY_HTTP='+str(e.code),flush=True)
        except (URLError,TimeoutError) as e:
            if attempt:raise
            print('BOUNDED_RETRY_NETWORK='+type(e).__name__,flush=True)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input');ap.add_argument('--output',required=True);a=ap.parse_args()
    raw,final=(Path(a.input).read_bytes(),URL) if a.input else acquire();o=build(raw,final)
    payload=json.dumps(o,ensure_ascii=False,sort_keys=True,indent=2)+'\n';out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(payload,encoding='utf-8')
    print('NEW_STRUCTURED_SECTIONS=9 SOURCE_IS_NEW=False');print('DERIVED_SHA256='+sha256(payload.encode()).hexdigest());print('SOURCE_SHA256='+SOURCE_SHA)


if __name__=='__main__':main()
