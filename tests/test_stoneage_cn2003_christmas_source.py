import copy
from hashlib import sha256
import json
import struct
import unittest

from tools.stoneage_cn2003_christmas_source import REPORT, URLS, extract, jpeg_dimensions, replay, validate


class ChristmasSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(REPORT.read_text())

    @staticmethod
    def sample():
        # Deliberately synthetic parser fixture, never an original-source hash.
        text = ('2003-12-23 15:28<!-- 内容 begin --><p>以下是来自华义的最新官方消息：</p>'
                '<img src="' + URLS[2].replace('https:', 'http:') + '">'
                '<p>从12月24日起，所有石器时代的服务器中都将大雪普降。</p>'
                '<p>活动自2003/12/24起到2003/12/26止。石器时代6.0及7.0服务器组四大村五大城将出现NPC——圣诞兑奖员和美丽的圣诞树。'
                '玩家通过和他们的对话，交出圣诞兑奖员需要的道具后可以得到神秘圣诞大礼包一份。</p>'
                '<p>兑奖条件：1.每个人物在同一服务器组只限领一套圣诞大礼包；'
                '2.领取礼物的人物必须达到30级以上并完成成人仪式；'
                '3.兑换奖品需要的道具请按照圣诞兑奖员的要求自行准备哦！</p>'
                '点击此处查询全部<!-- 内容 end -->')
        return text.encode('gb18030')

    def rejects(self, mutate):
        r = copy.deepcopy(self.report)
        mutate(r)
        with self.assertRaises(ValueError):
            validate(r)

    def test_contract_and_version_scoped_references(self):
        validate(self.report)
        contract = json.loads((REPORT.parent / 'STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']
        refs = {s['id'] for s in self.report['inputs']}
        self.assertEqual(len({r['record_id'] for r in self.report['records']}), 4)
        for row in self.report['records']:
            self.assertTrue(set(contract['record_contract']['required']) <= row.keys())
            self.assertIn(row['collection'], contract['required_collections'])
            self.assertTrue(set(row['source_refs']) <= refs)
            self.assertIn('CN_WAYI_60_AND_70', row['version_profile'])

    def test_extraction_matches_actual_source_derived_core_and_rules(self):
        got = extract(self.sample())
        self.assertEqual(got, self.report['inputs'][0]['extracted'])
        self.assertEqual(got, self.report['inputs'][1]['extracted'])

    def test_npc_scope_is_not_snow_scope(self):
        facts = extract(self.sample())['facts']
        self.assertEqual(facts['exchange_server_versions'], ['6.0', '7.0'])
        self.assertEqual(facts['snow_scope_as_written'], '所有石器时代')
        self.assertEqual(facts['location_scope_as_written'], '四大村五大城')
        self.rejects(lambda r: r['boundaries'].__setitem__('all_server_snow_claim_expands_exchange_scope', True))

    def test_character_server_group_limit_is_not_account_daily(self):
        f = extract(self.sample())['facts']
        self.assertEqual([f[k] for k in ('limit_subject_as_written', 'limit_scope_as_written', 'limit_quantity_as_written')], ['人物', '同一服务器组', '一套'])
        self.rejects(lambda r: r['records'][1].__setitem__('reset_rule', 'DAILY'))
        self.rejects(lambda r: r['boundaries'].__setitem__('once_per_character_group_means_account_global_or_daily', True))

    def test_literal_level_and_conjunction_do_not_create_numeric_predicate(self):
        q = self.report['records'][1]
        self.assertEqual(q['source_rules']['level_condition_as_written'], '30级以上')
        self.assertEqual(q['source_rules']['required_milestone'], '成人仪式')
        self.assertIsNone(q['level_predicate'])
        self.rejects(lambda r: r['records'][1].__setitem__('level_predicate', {'ge': 30}))
        self.rejects(lambda r: r['records'][1].__setitem__('eligibility_logic', 'LEVEL_OR_ADULT_CEREMONY'))
        with self.assertRaises(ValueError):
            extract(self.sample().replace('并完成'.encode('gb18030'), '或完成'.encode('gb18030')))

    def test_no_invented_locations_materials_rewards_or_clock(self):
        for row, key, value in [(0, 'map_names', ['萨姆吉尔']), (0, 'spawn_coordinates', [10, 20]),
                                (1, 'required_item_list', [{'id': 1, 'count': 10}]),
                                (1, 'exact_dialogue', '送礼物'), (1, 'original_script', 'lua'),
                                (1, 'server_time_window', '00:00+08:00'), (2, 'contents', ['月兔'])]:
            with self.subTest(key=key):
                self.rejects(lambda r: r['records'][row].__setitem__(key, value))

    def test_authority_must_be_inside_single_article_not_navigation(self):
        sample = self.sample()
        credit = '以下是来自华义的最新官方消息：'.encode('gb18030')
        for bad in [credit + sample.replace(credit, b''), sample.replace(credit, b'<script>' + credit + b'</script>'),
                    sample + '<!-- 内容 begin -->'.encode('gb18030'), sample.replace(b'2003-12-23 15:28', b'2005-01-01')]:
            with self.subTest(bad=bad[:30]), self.assertRaises(ValueError):
                extract(bad)

    def test_semantic_mutations_change_extracted_facts_or_fail(self):
        for before, after in [('2003/12/26', '2003/12/27'), ('6.0及7.0', '7.0及8.0'),
                              ('同一服务器组', '全部服务器组'), ('30级以上', '40级以上')]:
            with self.subTest(before=before):
                self.assertNotEqual(extract(self.sample().replace(before.encode('gb18030'), after.encode('gb18030'))), self.report['inputs'][0]['extracted'])
        for before, after in [('圣诞兑奖员需要', '圣诞老人需要'), ('一份。', '二份。')]:
            with self.subTest(before=before), self.assertRaises(ValueError):
                extract(self.sample().replace(before.encode('gb18030'), after.encode('gb18030')))

    def test_unrelated_wrapper_and_hidden_text_do_not_change_event(self):
        self.assertEqual(extract(self.sample()), extract(b'<script>fake</script><nav>other</nav>' + self.sample()))
        self.assertEqual(extract(self.sample()), extract(self.sample().replace(b'<p>', b'<p><style>fake</style>', 1)))

    def test_actual_image_link_is_required(self):
        with self.assertRaises(ValueError):
            extract(self.sample().replace(b'<img', b'<not-img'))
        with self.assertRaises(ValueError):
            extract(self.sample().replace(b'F167', b'F364'))

    def test_current_html_cannot_substitute_for_early_snapshot(self):
        fake_jpeg = b'\xff\xd8\xff\xc0' + struct.pack('>HBHHB', 8, 8, 337, 450, 1)
        with self.assertRaisesRegex(ValueError, 'Historical/image bytes changed'):
            replay(self.report, [self.sample(), self.sample(), fake_jpeg])
        self.assertNotEqual(sha256(self.sample()).hexdigest(), self.report['inputs'][1]['http']['sha256'])

    def test_early_html_is_same_release_not_independent_or_image_capture(self):
        self.assertEqual(self.report['inputs'][1]['capture_timestamp'], '20040218034443')
        self.assertEqual(self.report['inputs'][1]['http']['bytes'], 14942)
        self.assertNotEqual(self.report['inputs'][0]['http']['sha256'], self.report['inputs'][1]['http']['sha256'])
        self.rejects(lambda r: r['inputs'][1].__setitem__('same_publication_not_independent_witness', False))
        self.rejects(lambda r: r['inputs'][2].__setitem__('historical_image_bytes_verified', True))

    def test_jpeg_dimensions_and_invalid_source_rejected(self):
        jpeg = b'\xff\xd8\xff\xc0' + struct.pack('>HBHHB', 8, 8, 337, 450, 1)
        self.assertEqual(jpeg_dimensions(jpeg), [450, 337])
        for bad in [b'PNG', jpeg[:9], b'\xff\xd8\xff\xe0\x00\x01']:
            with self.subTest(payload=bad), self.assertRaises(ValueError):
                jpeg_dimensions(bad)

    def test_no_runtime_sprite_rights_or_early_version_promotion(self):
        for key, val in [('original_server_execution_verified', True), ('exact_client_build', '7.exe'), ('tw10_or_jss1999_backfill', True)]:
            self.rejects(lambda r: r['boundaries'].__setitem__(key, val))
        self.rejects(lambda r: r['records'][3].__setitem__('avatar_or_npc_sprite_binding', 123))
        self.rejects(lambda r: r['records'][0].__setitem__('rights_status', 'RELEASE_APPROVED'))

    def test_partial_source_set_rejected(self):
        with self.assertRaises(ValueError):
            replay(self.report, [self.sample()])

    def test_permanent_ci_replay_and_exact_custody_survive_artifact_expiry(self):
        receipt = json.loads((REPORT.parent / 'STONEAGE-CN2003-CHRISTMAS-CUSTODY-R1.json').read_text())
        saved = json.loads((REPORT.parent / 'STONEAGE-CN2003-CHRISTMAS-CI-REPLAY-R1.json').read_text())
        for pin in receipt['permanent_derived_files']:
            b = (REPORT.parents[2] / pin['path']).read_bytes()
            self.assertEqual(len(b), pin['bytes'])
            self.assertEqual(sha256(b).hexdigest(), pin['sha256'])
            import hashlib
            self.assertEqual(hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest(), pin['git_blob'])
        self.assertEqual(saved['announcement'], self.report['inputs'][0]['extracted'])
        self.assertEqual(saved['early_capture'], self.report['inputs'][1]['extracted'])
        self.assertFalse(saved['raw_html_or_image_bytes_in_output'])
        self.assertFalse(saved['original_server_or_historical_image_execution_verified'])
        for group, count in [('candidate', 10), ('main', 11)]:
            rows = receipt['validation'][group]
            self.assertEqual(len(rows), count)
            self.assertTrue(all(r['conclusion'] == 'success' and r['head'] == receipt['content_commit']['sha'] for r in rows))


if __name__ == '__main__':
    unittest.main()
