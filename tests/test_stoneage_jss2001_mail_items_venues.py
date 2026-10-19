"""Early mail/item/venue distinctions; synthetic section fragments, no original HTML."""
from copy import deepcopy
import json
from pathlib import Path
import unittest
from tools.stoneage_jss2001_mail_items_venues import ANCHORS,URL,REPORT,derive,build,validate_contract


def minimal_parts():
    return dict(zip(ANCHORS,[
      'ダブルクリック アイテムによっては ドラッグ＆ドロップ 金額を調節 地面に置きます',
      '名刺交換 メッセージやアイテム 拾わずにログアウト 戻ってくる前にログアウト 数時間 野良ペット 一定時間で消滅 メールの送受信はできますが、ペットメールの送受信はできません',
      '拾ったり 店でアイテムを買うと アイテム欄に入ります',
      'ダブルクリック グループウィンドウ キャラクターの名前を左クリック',
      '隣接 右クリック',
      'YES 隣接 方向を向いて メールウィンドウ ログアウトすると自動的にNO グループを組んでいる状態のプレイヤー同士',
      'stoneage chatxxxxxx.txt 日付 保存',
      'サムギル マリナス ジャジャ カルターナ 共通 チケット 地面に落とすと消えて ログアウトすればSPから再開 無料 大広間 結婚式場 闘技場から入られた方 ３つの部屋',
      'サムギル マリナス ジャジャ カルターナ 共通 チケット 地面に落とすと消えて ログアウトすればSPから再開 チケットを購入 レベルが9以下の場合とデュエルランキングが77位と777位の場合は無料 回復無料 観戦 試合場が４つ',
    ]))


def records():return json.loads(REPORT.read_text())['records']


class EarlyMailItemsVenueTests(unittest.TestCase):
    def test_nine_sections_numeric_cases_and_separate_lifecycles(self):
        b=derive(minimal_parts());self.assertEqual(len(b),9)
        self.assertEqual(b[7]['rooms'],3);self.assertEqual(b[8]['duel_match_areas'],4)
        self.assertEqual(b[8]['free_admission_enumerated_cases'],[{'level_at_most':9},{'duel_rank_exact':77},{'duel_rank_exact':777}])
        self.assertNotEqual(b[1]['logout_before_pet_return'],b[1]['stray_expiry'])

    def test_source_numeric_boundaries_not_rounded_or_substring_matched(self):
        for anchor,old,new in [('8110','３つ','４つ'),('8120','9以下','10以下'),('8120','77位と','78位と'),('8120','777位','7777位'),('8120','４つ','５つ')]:
            p=minimal_parts();p[anchor]=p[anchor].replace(old,new)
            with self.assertRaises(ValueError):derive(p)
        p=minimal_parts();p.pop('3070')
        with self.assertRaisesRegex(ValueError,'section order'):derive(p)

    def test_battle_ordinary_mail_is_not_pet_mail(self):
        for key,wrong in [('ordinary_mail_send_receive_during_battle',False),('pet_mail_send_receive_during_battle',True)]:
            r=records();r[1]['source_described_behavior'][key]=wrong
            with self.assertRaisesRegex(ValueError,'battle restrictions'):validate_contract(r)

    def test_mail_logout_is_stray_not_immediate_deletion_and_timers_unknown(self):
        for key,wrong in [('returned_uncollected_pet_plus_logout','IMMEDIATELY_DELETED'),('grace_hours_stray_ttl_pet_ids_or_persistence_format',{'seconds':3600})]:
            r=records();r[1]['source_described_behavior'][key]=wrong
            with self.assertRaisesRegex(ValueError,'lifecycle'):validate_contract(r)

    def test_card_consent_reset_is_not_deleting_registered_contacts(self):
        r=records();r[5]['source_described_behavior']['logout_deletes_contact_records_proven']=True
        with self.assertRaisesRegex(ValueError,'contact deletion'):validate_contract(r)

    def test_free_entry_enumerated_cases_are_not_a_conjunction(self):
        r=records();r[8]['source_described_behavior']['free_cases_combination']='ALL_CONDITIONS_REQUIRED'
        with self.assertRaisesRegex(ValueError,'conjoined'):validate_contract(r)

    def test_free_chat_entry_not_all_visitors_pay_for_arena_ticket(self):
        r=records();r[7]['source_described_behavior']['all_free_chat_visitors_need_paid_ticket_proven']=True
        with self.assertRaisesRegex(ValueError,'ticket warning'):validate_contract(r)

    def test_ticket_drop_not_generic_item_expiry_or_same_item_id(self):
        for key,value in [('drop_causes_immediate_disappearance_described',False),('ticket_id_or_same_item_across_venues',123),('restores_ticket_on_login_proven',True)]:
            r=records();r[8]['source_described_behavior']['ticket_warning'][key]=value
            with self.assertRaisesRegex(ValueError,'Ticket identity'):validate_contract(r)

    def test_arena_hospital_free_is_local_not_all_world_hospitals(self):
        r=records();r[8]['source_described_behavior']['all_world_hospitals_free_proven']=True
        with self.assertRaisesRegex(ValueError,'Local arena'):validate_contract(r)

    def test_optional_item_target_and_local_log_not_generalized(self):
        for index,key,value in [(0,'all_items_always_require_target_window',True),(3,'every_item_requires_this_target_procedure',True),(6,'server_chat_archive_or_cloud_sync_proven',True)]:
            r=records();r[index]['source_described_behavior'][key]=value
            with self.assertRaises(ValueError):validate_contract(r)

    def test_wrong_original_capture_or_same_size_error_body_rejected(self):
        for url in (URL.replace('titan.co.jp','example.org'),URL.replace('20010418083149','19991101000000'),URL):
            with self.assertRaises(ValueError):build(b'x'*28434,url)

    def test_per_record_archive_provenance_new_sections_and_unknowns(self):
        o=json.loads(REPORT.read_text());c=json.loads(Path('research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']
        self.assertFalse(o['source']['newly_discovered_source']);self.assertEqual(o['source']['newly_structured_sections'],list(ANCHORS))
        old=json.loads(Path('research/recovered/STONEAGE-JSS2001-PET-MANUAL-CONTRACT-R1.json').read_text())
        old2=json.loads(Path('research/recovered/STONEAGE-EARLY-CONTENT-GUIDE-MANUAL-R1.json').read_text())
        self.assertFalse(set(ANCHORS)&(set(old['section_sha256'])|set(old2['observations']['manual_section_hashes'])))
        validate_contract(o['records'])
        for r in o['records']:
            self.assertLessEqual(set(c['record_contract']['required']),r.keys());self.assertIn(r['collection'],c['required_collections'])
            self.assertEqual(r['source_refs'][0]['actual_capture'],'20010418083149');self.assertIsNone(r['original_entity_ids_and_cross_version_binding'])
            self.assertFalse(r['server_runtime_observed'])


if __name__=='__main__':unittest.main()
