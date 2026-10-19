import copy
import hashlib
import json
import struct
import unittest

from tools.stoneage_cn70_suzaku_source import REPORT, SNAPSHOT, URLS, extract_release, jpeg_dimensions, replay, validate_report, verify_snapshot


class SuzakuSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(REPORT.read_text())

    def test_seven_archive_records_with_live_source_references(self):
        validate_report(self.report)
        contract = json.loads((REPORT.parent / 'STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']
        known = {x['id'] for x in self.report['inputs']}
        for row in self.report['records']:
            self.assertTrue(set(contract['record_contract']['required']) <= row.keys())
            self.assertIn(row['collection'], contract['required_collections'])
            self.assertTrue(set(row['source_refs']) <= known)
        self.assertEqual(len({r['record_id'] for r in self.report['records']}), 7)

    def test_four_mythic_skill_affiliations_not_species_vectors(self):
        rows = self.report['records'][:4]
        self.assertEqual([(r['label_as_written'], r['narrative_skill_element']) for r in rows],
                         [('白虎', '水'), ('青龙', '风'), ('玄武', '地'), ('朱雀', '火')])
        self.assertTrue(all(r['pet_attribute_vector'] is None and r['growth_profile'] is None for r in rows))
        self.assertEqual(rows[3]['source_named_form'], '菲奇亚')

    def test_current_bytes_are_not_publication_era_bytes(self):
        sources = self.report['inputs']
        self.assertEqual([x['visible_publication'] for x in sources[:2]], ['2003-12-16 14:38', '2002-2-5'])
        self.assertTrue(all(x['historical_original_byte_sha256'] is None for x in sources))
        self.assertNotEqual(sources[0]['authority'], sources[1]['authority'])

    def test_images_are_two_different_source_surfaces(self):
        images = self.report['inputs'][2:]
        self.assertEqual([x['dimensions'] for x in images], [[400, 261], [400, 299]])
        self.assertEqual([x['http']['bytes'] for x in images], [19475, 27547])
        self.assertEqual(images[0]['caption_as_written'], '图为：神秘朱雀设定图')
        self.assertEqual(images[1]['caption_as_written'], '图为：神秘朱雀属性')
        self.assertNotEqual(images[0]['http']['sha256'], images[1]['http']['sha256'])

    def test_single_display_sample_and_unreadable_name_stay_bounded(self):
        observed = self.report['visual_observations']['status_image']
        self.assertEqual([observed['observed_individual_values'][x] for x in ('level', 'attack', 'defense', 'agility')], [1, 21, 7, 11])
        self.assertIsNone(observed['name_line_transcription'])
        self.assertIsNone(observed['growth_rates'])
        self.assertIsNone(observed['numeric_element_weights'])

    def rejects(self, mutate):
        r = copy.deepcopy(self.report)
        mutate(r)
        with self.assertRaises(ValueError):
            validate_report(r)

    def test_false_original_build_and_retcon_claims_rejected(self):
        for key, value in [('original_server_execution_verified', True), ('exact_client_build', '7.0.exe'),
                           ('retcon_or_contradiction_proven', True), ('both_articles_share_one_canon_or_chronology', True),
                           ('tw10_or_jss1999_backfill', True)]:
            with self.subTest(key=key):
                self.rejects(lambda r: r['boundaries'].__setitem__(key, value))

    def test_stat_growth_or_numeric_element_promotion_rejected(self):
        self.rejects(lambda r: r['visual_observations']['status_image'].__setitem__('growth_rates', {'attack': 21}))
        self.rejects(lambda r: r['visual_observations']['status_image'].__setitem__('numeric_element_weights', [0, 0, 10, 0]))
        self.rejects(lambda r: r['visual_observations']['status_image'].__setitem__('name_line_transcription', '菲奇亚'))

    def test_source_author_and_reproduction_rights_promotions_rejected(self):
        self.rejects(lambda r: r['inputs'][1].__setitem__('authority', r['inputs'][0]['authority']))
        self.rejects(lambda r: r['records'][3].__setitem__('rights_status', 'RELEASE_APPROVED'))
        self.rejects(lambda r: r['inputs'][0].__setitem__('historical_original_byte_sha256', 'a' * 64))

    @staticmethod
    def sample(credit=True):
        images = ''.join('<img src="' + u.replace('https:', 'http:') + '">' for u in URLS[2:])
        text = ('<!-- 内容 begin --><p>' + ('以下是来自华义的最新官方消息：' if credit else '')
                + '石器时代7.0</p>' + images + '<p>传说四大神兽，'
                '[白虎]封印着关于水的技能；[青龙]封印着关于风的技能；'
                '[玄武]封印着关于地的技能；[朱雀]封印着关于火的技能。'
                '被分别封印在水神殿，风神殿，地神殿，火神殿，久久不能得到自由。'
                '光明精灵王与黑暗精灵王一战；纯火属性的朱雀攻高，敏高，防低；'
                '7.0石头就业所：朱雀——菲奇亚吧！拍卖现场：不属于故事正文</p><!-- 内容 end -->')
        return text.encode('gb18030')

    def test_credit_outside_article_and_missing_image_do_not_qualify(self):
        with self.assertRaises(ValueError):
            extract_release('以下是来自华义的最新官方消息：'.encode('gb18030') + self.sample(False))
        with self.assertRaises(ValueError):
            extract_release(self.sample().replace(b'<img', b'<not-an-image', 1))

    def test_campaign_tail_does_not_change_story_core(self):
        a = extract_release(self.sample())
        b = extract_release(self.sample().replace('不属于故事正文'.encode('gb18030'), b'9999'))
        self.assertEqual(a, b)

    def test_duplicate_beast_or_missing_relative_stats_fails(self):
        for before, after in [('青龙', '白虎'), ('朱雀攻高，敏高，防低', '朱雀数值未知')]:
            with self.subTest(before=before), self.assertRaises(ValueError):
                extract_release(self.sample().replace(before.encode('gb18030'), after.encode('gb18030')))

    def test_jpeg_sof_dimensions_and_invalid_format(self):
        jpeg = b'\xff\xd8\xff\xc0' + struct.pack('>HBHHB', 8, 8, 299, 400, 1)
        self.assertEqual(jpeg_dimensions(jpeg), [400, 299])
        for payload in [b'PNG', jpeg[:8], b'\xff\xd8\xff\xe0\x00\x01']:
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                jpeg_dimensions(payload)

    def test_replay_rejects_partial_inputs_or_replaced_story(self):
        with self.assertRaises(ValueError):
            replay(self.report, [self.sample()])
        with self.assertRaises(ValueError):
            replay(self.report, [self.sample(), b'', b'', b''])

    def test_historical_capture_is_distinct_from_current_page_and_images(self):
        h = json.loads(SNAPSHOT.read_text())
        self.assertEqual(h['capture_timestamp'], '20031225115132')
        self.assertEqual(h['bytes'], 15189)
        self.assertNotEqual(h['sha256'], self.report['inputs'][0]['http']['sha256'])
        self.assertEqual(h['core_sha256'], self.report['inputs'][0]['core_sha256'])
        self.assertFalse(h['historical_image_bytes_verified'])
        self.assertFalse(h['original_server_or_wayi_host_verified'])
        self.assertTrue(h['prior_checkpoint_not_rewritten'])

    def test_current_or_synthetic_html_cannot_replace_historical_byte_pin(self):
        h = json.loads(SNAPSHOT.read_text())
        with self.assertRaises(ValueError):
            verify_snapshot(h, self.sample(), self.report)
        h['capture_timestamp'] = '20261020'
        with self.assertRaises(ValueError):
            verify_snapshot(h, b'', self.report)

    def test_permanent_initial_ci_replay_is_only_the_four_input_checkpoint(self):
        saved = json.loads((REPORT.parent / 'STONEAGE-CN70-SUZAKU-CI-REPLAY-R1.json').read_text())
        self.assertEqual(len(saved['current_http']), 4)
        self.assertFalse(saved['historical_snapshot_species_master_or_runtime_verified'])
        self.assertFalse(saved['raw_html_or_image_bytes_in_output'])
        self.assertEqual([r['facts'] for r in saved['narrative_cores']], [r['extracted_facts'] for r in self.report['inputs'][:2]])
        self.assertEqual([r['sha256'] for r in saved['images']], [r['http']['sha256'] for r in self.report['inputs'][2:]])

    def test_permanent_initial_custody_exact_hashes_and_head_scope(self):
        receipt = json.loads((REPORT.parent / 'STONEAGE-CN70-SUZAKU-CUSTODY-R1.json').read_text())
        self.assertEqual(len(receipt['permanent_derived_files']), 3)
        for pin in receipt['permanent_derived_files']:
            payload = (REPORT.parents[2] / pin['path']).read_bytes()
            self.assertEqual(len(payload), pin['bytes'])
            self.assertEqual(hashlib.sha256(payload).hexdigest(), pin['sha256'])
            self.assertEqual(hashlib.sha1(b'blob ' + str(len(payload)).encode() + b'\0' + payload).hexdigest(), pin['git_blob'])
        for name, count in [('candidate', 10), ('main', 11)]:
            rows = receipt['validation'][name]
            self.assertEqual(len(rows), count)
            self.assertTrue(all(r['head'] == receipt['content_commit']['sha'] and r['conclusion'] == 'success' for r in rows))


if __name__ == '__main__':
    unittest.main()
