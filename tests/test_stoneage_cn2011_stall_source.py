import copy
import json
import unittest
from tools.stoneage_cn2011_stall_source import REPORT, ROOT, STEM, jpeg_dimensions, validate


class StallSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(REPORT.read_text())

    def reject(self, keys, value):
        r = copy.deepcopy(self.r)
        node = r
        for k in keys[:-1]:
            node = node[k]
        node[keys[-1]] = value
        with self.assertRaises(ValueError):
            validate(r)

    def test_seven_unique_versioned_records_and_limited_authority(self):
        validate(self.r)
        self.reject(['records', 0, 'version_profile'], 'TW10')
        self.reject(['records', 0, 'game_ids'], [1])
        self.reject(['sources', '2011', 'authority'], 'AUTHENTICATED_OFFICIAL_ORIGINAL')
        self.reject(['sources', '2012', 'core_sha256'], '0' * 64)

    def test_button_crop_not_absolute_original_coordinates(self):
        self.reject(['extracted', 'entry', 'position_reported'], 'LOWER_RIGHT')
        self.reject(['extracted', 'entry', 'exact_original_coordinates'], [160, 0])
        self.reject(['visual_observations', 'button_crop', 'proves_original_click_coordinates'], True)

    def test_listing_items_and_pets_sample_price_not_master(self):
        self.reject(['extracted', 'listing_steps', 0], 'SELECT_ITEMS_ONLY')
        self.reject(['visual_observations', 'listing_window', 'sample_is_standard_or_species_price'], True)
        self.reject(['visual_observations', 'listing_window', 'currency_unit'], 'Stone')
        self.reject(['extracted', 'currency_price_limits_slots_offline_buyer_settlement_rules'], {'slots': 7})

    def test_red_sell_means_listed_not_completed_sale(self):
        self.reject(['extracted', 'sale_marker', 'text'], 'SOLD')
        self.reject(['extracted', 'sale_marker', 'meaning_reported'], 'ALREADY_SOLD')
        self.reject(['visual_observations', 'listing_window', 'proves_purchase_completed'], True)

    def test_bargaining_channels_and_heading_not_auction_algorithm(self):
        self.reject(['extracted', 'bargaining_channels', 2], '世界')
        self.reject(['visual_observations', 'listing_window', 'heading_proves_auction_rules'], True)
        self.reject(['extracted', 'automatic_bargaining_or_auction_rules_proven'], True)

    def test_exact_fee_wording_not_all_taxes_zero_or_map_permission(self):
        self.reject(['extracted', 'fee_and_location_claim', 'fee_wording_as_written'], '无须缴纳任何费用')
        self.reject(['extracted', 'fee_and_location_claim', 'all_taxes_zero_proven'], True)
        self.reject(['extracted', 'fee_and_location_claim', 'verified_map_permission_table'], 'ALL_MAPS')

    def test_copy_and_similar_scene_not_same_build_or_original_capture(self):
        self.reject(['extracted', 'numeric_version_or_build'], '8.5')
        self.reject(['extracted', 'cross_date_relation', 'same_build_proven'], True)
        self.reject(['images', 0, 'authenticated_capture_date'], '2011-01-12')
        self.reject(['images', 1, 'native_client_resolution_proven'], True)
        self.reject(['visual_observations', 'scene_relation', 'image_bytes_identical'], True)

    def test_actual_22_source_mutations_and_two_outer_positives(self):
        r = json.loads((ROOT / ('research/recovered/' + STEM + '-LOCAL-REPLAY-R1.json')).read_text())
        cases = r['audit']['real_body_mutations']
        self.assertEqual(len(cases), 22)
        self.assertEqual(len({x['input_sha256'] for x in cases}), 22)
        self.assertTrue(all(x['rejected_without_digest_gate'] for x in cases))
        self.assertEqual(r['audit']['outer_script_positives'], {'2011': True, '2012': True})
        self.assertEqual(r['extracted'], self.r['extracted'])
        self.assertFalse(r['raw_html_or_assets_in_output'])

    def test_exact_article_linked_images_and_malformed_jpeg_rejected(self):
        self.reject(['images', 0, 'url_as_written'], 'http://example.com/not-linked.jpg')
        self.reject(['images', 0, 'requested_url'], 'https://example.com/not-requested.jpg')
        # A structural test, not an assertion that a header-only file is a complete image.
        soi_sof = b'\xff\xd8\xff\xc0\x00\x0b\x08\x01\x9d\x02\x26\x01\x01\x11\x00'
        self.assertEqual(jpeg_dimensions(soi_sof), (550, 413))
        for bad in [b'<html>error</html>', b'\xff\xd8\xff\xc0\x00\x01', soi_sof[:10]]:
            with self.assertRaises(ValueError):
                jpeg_dimensions(bad)

    def test_test_promise_unproven_claims_and_stage_gates(self):
        self.reject(['extracted', 'test_context_2011', 'launch_or_retention_observed'], True)
        self.reject(['sources', '2011', 'authenticated_historical_original_bytes'], True)
        for key in self.r['unproven']:
            with self.subTest(key=key):
                self.reject(['unproven', key], True)
        self.reject(['status', 'stage_b_wiki'], 'OPEN')
        self.reject(['next'], 'EXPAND_STALL_HELPERS')

    def test_required_permanent_custody_and_independent_main_artifact(self):
        import hashlib
        p = ROOT / ('research/recovered/' + STEM + '-CUSTODY-R1.json')
        self.assertTrue(p.is_file(), 'Accepted source requires a permanent custody receipt')
        r = json.loads(p.read_text())
        self.assertEqual(r['schema'], 'stoneage.cn2011_2012_stall.custody.r1')
        for pin in r['source_pins']:
            b = (ROOT / pin['path']).read_bytes()
            self.assertEqual(len(b), pin['bytes'])
            self.assertEqual(hashlib.sha256(b).hexdigest(), pin['sha256'])
            self.assertEqual(hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest(), pin['git_blob'])
        self.assertEqual(len(r['startup_prefixes']), 9)
        for pin in r['startup_prefixes']:
            b = (ROOT / pin['path']).read_bytes()[:pin['bytes']]
            self.assertEqual(hashlib.sha256(b).hexdigest(), pin['sha256'])
            self.assertEqual(hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest(), pin['git_blob'])
        for key in ('run_id', 'job_id', 'artifact_id'):
            self.assertNotEqual(r['candidate'][key], r['main'][key])
        self.assertEqual(len(r['workflow_runs']), 21)
        self.assertTrue(all(x['conclusion'] == 'success' for x in r['workflow_runs']))
        copies = []
        for label in ('candidate', 'main'):
            meta = r[label]
            self.assertTrue(meta['all_applicable_workflows_success'])
            self.assertEqual(meta['actual_unit_tests'], 10)
            self.assertEqual(meta['skipped_tests'], 0)
            b = (ROOT / ('research/recovered/' + STEM + '-CI-' + label.upper() + '-REPLAY-R1.json')).read_bytes()
            self.assertEqual(len(b), meta['raw_bytes'])
            self.assertEqual(hashlib.sha256(b).hexdigest(), meta['raw_sha256'])
            self.assertEqual(hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest(), meta['raw_git_blob'])
            replay = json.loads(b)
            self.assertEqual(replay['extracted'], self.r['extracted'])
            self.assertEqual(len(replay['images']), 4)
            self.assertFalse(replay['raw_html_or_assets_in_output'])
            copies.append(b)
        self.assertEqual(copies[0], copies[1])
        self.assertTrue(all(v is False for v in r['bounds'].values()))


if __name__ == '__main__':
    unittest.main()
