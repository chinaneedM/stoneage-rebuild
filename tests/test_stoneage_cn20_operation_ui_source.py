import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import stoneage_cn20_operation_ui_source as m


def fixture():
    head='<html><title>石器时代2.0</title>(稿务必注明所在服务器、作者及作品名称)<div align="center"><font>基 本 操 作</font></div>'
    rows=''.join('<p><font>'+label+'</font><br>synthetic '+label+'</p>' for label in m.LABELS)
    image='<a href="img/4.gif" target="_blank"><img src="img/4s.gif" width="240" height="180"></a>'
    return (head+rows+image+'<span class="p12b"></span></html>').encode('gb18030')


class OperationUITests(unittest.TestCase):
    def report(self):return json.loads(m.REPORT.read_text())

    def test_unique_ordered_visible_sections_do_not_borrow_hidden_or_footer_evidence(self):
        raw=fixture();core,sections=m.article(raw)
        self.assertEqual(list(sections),m.LABELS)
        self.assertEqual(m.article(raw+b'<script>outside=1</script>'),(core,sections))
        for changed in (raw+raw,raw.replace('基 本 操 作'.encode('gb18030'),b'other'),
                        raw.replace('h.动作键'.encode('gb18030'),'h.其他键'.encode('gb18030')),
                        raw.replace('<p><font>一、移动</font>'.encode('gb18030'),'<script><p><font>一、移动</font>'.encode('gb18030'))):
            with self.assertRaises(ValueError):m.article(changed)

    def test_early_capture_operator_hosting_and_later_image_dates_remain_distinct(self):
        r=self.report();m.validate(r)
        for change in (
            lambda d:d.update(version_profile='TW10'),
            lambda d:d['source'].update(authority='OPERATOR_WRITTEN'),
            lambda d:d['source'].update(new_source_url=True),
            lambda d:d['source'].update(sha256='0'*64),
            lambda d:d['image'].update(capture='20011204000349'),
            lambda d:d['image'].update(initial_request_same_capture_as_actual=True),
            lambda d:d['image'].update(thumbnail_pixels_acquired=True),
            lambda d:d['negative_boundaries'].update(body_and_image_same_capture_or_build=True),
            lambda d:d['extraction'].update(publication_date='2001-12-04'),
            lambda d:d['extraction'].update(exact_client_build='CN2.0 retail'),
            lambda d:d['extraction'].update(operator_authorship_verified=True)):
            d=copy.deepcopy(r);change(d);d['catalog_records']=m.catalog(d['extraction'],d['image'])
            with self.assertRaises(ValueError):m.validate(d)

    def test_static_name_card_rows_buttons_and_english_label_do_not_prove_live_actions(self):
        r=self.report()
        for change in (
            lambda d:d['visual_observation'].update(visible_rows_are_total_capacity=True),
            lambda d:d['visual_observation'].update(actual_online_state_verified=True),
            lambda d:d['visual_observation'].update(actual_button_action_or_message_delivery_observed=True),
            lambda d:d['visual_observation'].update(region_or_build_authenticated_by_label=True),
            lambda d:d['visual_observation'].update(viewport_page_index_transcribed=True),
            lambda d:d['visual_observation'].update(original_contact_or_character_ids=[1,2,3]),
            lambda d:d['image'].update(sha256='0'*64)):
            d=copy.deepcopy(r);change(d);d['catalog_records']=m.catalog(d['extraction'],d['image'])
            with self.assertRaises(ValueError):m.validate(d)
        with self.assertRaises((ValueError,OSError)):m.inspect_image(b'<html>404</html>',r)

    def test_riding_conjunction_and_family_document_permissions_remain_scoped(self):
        r=self.report()
        for change in (
            lambda d:d['extraction']['pet_modes'].update(ride_visibility='LEARNED_OR_RIDEABLE_PET'),
            lambda d:d['extraction']['pet_modes'].update(numeric_mode_ids=[0,1,2,3,4]),
            lambda d:d['extraction']['family'].update(invitation_access='ALL_MANORS'),
            lambda d:d['extraction']['family'].update(broadcast_audience='EVERYONE'),
            lambda d:d['extraction']['family'].update(invitation_original_item_id=1),
            lambda d:d['extraction']['family'].update(manor_names_ids_skill_or_pet_roster_prices=['A']),
            lambda d:d['extraction']['help_duel_emotes'].update(pets_included_in_limit=True)):
            d=copy.deepcopy(r);change(d);d['catalog_records']=m.catalog(d['extraction'],d['image'])
            with self.assertRaises(ValueError):m.validate(d)

    def test_later_confirmation_shortcuts_jss_timers_and_storage_are_not_backfilled(self):
        r=self.report()
        for change in (
            lambda d:d['comparison']['later_portal'].update(same_author_copying_or_same_build_proven=True),
            lambda d:d['comparison']['jss'].update(card_exchange_logout_no_reset_backfilled_to_cn=True),
            lambda d:d['comparison']['jss'].update(mail_battle_restrictions_or_stray_timers_backfilled_to_cn=True),
            lambda d:d['extraction']['top_buttons'].update(double_ok_trade_or_leader_follow_described=True),
            lambda d:d['extraction']['top_buttons'].update(order_is_explicit_left_to_right=True),
            lambda d:d['extraction']['mail_album'].update(automatic_complete_history=True),
            lambda d:d['extraction']['mail_album'].update(storage_format='savedata.dat'),
            lambda d:d['extraction']['help_duel_emotes'].update(duel_exp_or_capturability='ZERO_EXP'),
            lambda d:d['extraction']['windows'].update(actual_audio_event='ATTACK_WAV')):
            d=copy.deepcopy(r);change(d);d['catalog_records']=m.catalog(d['extraction'],d['image'])
            with self.assertRaises(ValueError):m.validate(d)

    def test_all_eight_catalog_rows_satisfy_existing_record_contract(self):
        r=self.report();contract=json.loads((m.ROOT/m.PARENTS[-1]).read_text())['future_website']
        self.assertEqual([v['collection'] for v in r['catalog_records']],['tutorials']*7+['screens'])
        for v in r['catalog_records']:self.assertTrue(set(contract['record_contract']['required']).issubset(v))
        for key in contract['record_contract']['required']:
            d=copy.deepcopy(r);d['catalog_records'][0].pop(key)
            with self.assertRaises(ValueError):m.validate(d)
        for key,value in [('entity_type','ORIGINAL_MASTER'),('game_ids',1),('rights_status','RELEASE_APPROVED')]:
            d=copy.deepcopy(r);d['catalog_records'][0][key]=value
            with self.assertRaises(ValueError):m.validate(d)

    def test_parent_and_shared_parser_require_original_bytes_and_keep_later_null_hashes(self):
        r=self.report()
        self.assertIsNone(r['comparison']['later_portal']['source']['raw_html_sha256'])
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
