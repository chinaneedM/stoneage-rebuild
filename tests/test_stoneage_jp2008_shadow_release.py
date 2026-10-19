import copy
import hashlib
import json
from pathlib import Path
import unittest

from tools.stoneage_jp2008_shadow_release import REPORT, compact, extract, replay, validate_report


class ShadowRelease(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(REPORT.read_text())

    def test_current_contract_and_archive_fields(self):
        validate_report(self.report)
        archive = json.loads((REPORT.parent / 'STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())
        contract = archive['future_website']
        for record in self.report['records']:
            self.assertIn(record['collection'], contract['required_collections'])
            self.assertTrue(set(contract['record_contract']['required']) <= record.keys())

    def test_independently_reviewed_chapter_eligibility(self):
        facts = [x['source_reported'] for x in self.report['records']]
        self.assertEqual([x['minimum_level_reported'] for x in facts], [10, 25, 45])
        self.assertEqual([x['previous_chapter_required_reported'] for x in facts], [None, 1, 2])
        self.assertEqual([x['exclusive_first_chapter_routes_reported'] for x in facts], [True, None, None])
        self.assertEqual([x['prior_chapter_changes_npc_presence_reported'] for x in facts], [None, True, True])

    def test_hint_roles_are_not_acceptance_or_story_aliases(self):
        facts = [x['source_reported'] for x in self.report['records']]
        self.assertEqual([x['npc_label_as_written'] for x in facts[0]['entry_or_hint_roles']], ['青年', '少年'])
        for row in facts[1:]:
            self.assertEqual(row['entry_or_hint_roles'], [{'village_as_written': 'キヌイの村',
                'npc_label_as_written': 'テケスタ', 'role': 'HINT_NOT_PROVEN_START'}])

    def test_publication_is_not_launch_or_world_year(self):
        self.assertEqual(self.report['sources'][0]['visible_publication'], '2008/09/22 12:24')
        self.assertEqual(self.report['records'][0]['announced_start_date'], '2008-09-23')
        self.assertEqual(self.report['records'][2]['chapter_title_as_written'], '影の支配者 3章（破）')
        self.assertIsNone(self.report['records'][2]['ending_or_unmasked_identity'])
        self.assertEqual(self.report['sources'][1]['official_link_as_published'],
                         self.report['sources'][2]['official_link_as_published'])

    def rejects(self, mutate):
        report = copy.deepcopy(self.report)
        mutate(report)
        with self.assertRaises(ValueError):
            validate_report(report)

    def test_runtime_original_build_and_rights_promotions_rejected(self):
        for key, value in [('server_execution_verified', True), ('tw10_backfill', True),
                           ('historical_2008_snapshot_authenticated', True), ('exact_client_build', '8.0')]:
            with self.subTest(key=key):
                self.rejects(lambda r: r['boundaries'].__setitem__(key, value))
        self.rejects(lambda r: r['records'][0].__setitem__('rights_status', 'RELEASE_APPROVED'))

    def test_campaign_reward_and_hidden_identity_rejected(self):
        self.rejects(lambda r: r['records'][0].__setitem__('reward', 'ナイトゲイル'))
        self.rejects(lambda r: r['records'][2].__setitem__('ending_or_unmasked_identity', 'パパスカー'))

    def test_fake_snapshot_and_first_party_host_rejected(self):
        self.rejects(lambda r: r['sources'][0].__setitem__('historical_2008_raw_sha256', 'a' * 64))
        self.rejects(lambda r: r['sources'][1].__setitem__('authority', 'DIRECT_OFFICIAL_HOST'))

    def test_hint_and_future_chapter_promotion_rejected(self):
        self.rejects(lambda r: r['records'][1]['source_reported']['entry_or_hint_roles'][0].__setitem__('role', 'QUEST_START'))
        self.rejects(lambda r: r['relations'].append({'from_chapter': 3, 'to_chapter': 4,
                                                     'kind': 'SOURCE_EXPLICIT_COMPLETION_PREREQUISITE'}))

    def test_visible_parser_ignores_script_style_and_whitespace(self):
        self.assertEqual(compact('<p>A &amp; B</p><script>Lv999以上</script><style>x</style><p>C</p>'), 'A&BC')

    @staticmethod
    def sample(level='25', predecessor='1', before='', after=''):
        return (before + '<p>メーカー発表文の内容をそのまま掲載しています</p>'
                '株式会社デジパーク<p>新クエストアップデート</p>■クエスト概要<br>'
                f'Lv{level}以上<br>「影の支配者 {predecessor}章（序）」をクリアしていること<br>'
                '「キヌイの村」にいるNPC「テケスタ」<p>ストーンエイジ公式サイト</p>' + after).encode()

    def test_editorial_and_campaign_levels_not_used(self):
        r = extract(self.sample(before='<p>Lv999以上</p>', after='<p>Lv888以上</p>'), 2)
        self.assertEqual(r['source_facts']['minimum_level_reported'], 25)

    def test_duplicate_or_absent_source_gate_fails(self):
        for raw in [self.sample().replace('Lv25以上'.encode(), b''),
                    self.sample().replace('Lv25以上'.encode(), 'Lv25以上Lv26以上'.encode()),
                    self.sample().replace('メーカー発表文の内容をそのまま掲載しています'.encode(), b'')]:
            with self.subTest(raw=raw[:30]), self.assertRaises((ValueError, IndexError)):
                extract(raw, 2)

    def test_whitespace_and_template_changes_leave_core_stable(self):
        a = extract(self.sample(), 2)
        b = extract(self.sample(before='<div>new navigation</div>', after='<div>new footer</div>').replace(b'<br>', b' <br>\n'), 2)
        self.assertEqual(a, b)

    def test_live_replay_rejects_changed_source_and_partial_source_set(self):
        with self.assertRaises(ValueError):
            replay(self.report, [self.sample(), self.sample(), self.sample()])
        with self.assertRaises(ValueError):
            replay(self.report, [self.sample()])

    def test_permanent_ci_replay_matches_source_core_and_all_fields(self):
        saved = json.loads((REPORT.parent / 'STONEAGE-JP2008-SHADOW-CI-REPLAY-R1.json').read_text())
        self.assertEqual(len(saved['verified_sources']), 3)
        self.assertFalse(saved['raw_html_in_output'])
        self.assertFalse(saved['historical_snapshot_or_server_execution_verified'])
        for actual, source, record in zip(saved['verified_sources'], self.report['sources'], self.report['records']):
            self.assertEqual(actual['source_id'], source['id'])
            self.assertEqual(actual['core_sha256'], source['release_core_sha256'])
            self.assertEqual(actual['source_facts'], record['source_reported'])

    def test_permanent_source_and_replay_hash_chain(self):
        receipt = json.loads((REPORT.parent / 'STONEAGE-JP2008-SHADOW-CUSTODY-R1.json').read_text())
        for pin in receipt['permanent_derived_files']:
            payload = (REPORT.parents[2] / pin['path']).read_bytes()
            self.assertEqual(len(payload), pin['bytes'])
            self.assertEqual(hashlib.sha256(payload).hexdigest(), pin['sha256'])
            self.assertEqual(hashlib.sha1(b'blob ' + str(len(payload)).encode() + b'\0' + payload).hexdigest(), pin['git_blob'])
        self.assertFalse(receipt['original_2008_bytes_or_runtime_verified'])
        self.assertEqual(receipt['artifact']['zip_bytes'], 1002)
        self.assertEqual(receipt['artifact']['zip_sha256'], '804304f36950e4ff8af773defeb3fd9c46f9c1b68db630c426e498547a50dafd')


if __name__ == '__main__':
    unittest.main()
