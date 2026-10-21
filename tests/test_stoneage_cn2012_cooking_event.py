import copy
import hashlib
import json
import unittest
from tools import stoneage_cn2012_cooking_event as m


class CookingEvent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(m.REPORT.read_text())
        cls.local = json.loads((m.ROOT / ('research/recovered/' + m.STEM + '-LOCAL-REPLAY-R1.json')).read_text())

    def reject(self, keys, value):
        r = copy.deepcopy(self.r)
        node = r
        for key in keys[:-1]:
            node = node[key]
        node[keys[-1]] = value
        with self.assertRaises(ValueError):
            m.validate(r)

    def test_named_chain_preserves_order_without_recipe_invention(self):
        m.validate(self.r)
        x = self.r['extracted']['flow']
        self.assertEqual(x['vendors_as_written'], ['扑满乌力', '黑乌力'])
        self.assertEqual(x['products_as_written'], ['扑满乌力的蔬菜色拉', '黑乌力的蔬菜色拉'])
        self.assertEqual((x['delivery_location_as_written'], x['recipient_as_written']), ('加加村24店', '大厨'))
        for key, val in [('both_products_required', True), ('vendor_to_product_exact_recipe_mapping', [0, 1]), ('ingredients_recipes_prices_coordinates_ids', {'cabbage': 1})]:
            self.reject(['extracted', 'flow', key], val)

    def test_schedule_is_claim_with_unknown_endpoints_timezone_and_limits(self):
        self.assertEqual(self.r['extracted']['schedule']['start_clock'], '19:00')
        for key, val in [('timezone', 'Asia/Shanghai'), ('endpoint_inclusivity', 'CLOSED'), ('daily_limit', 1), ('live_execution_verified', True), ('launch_date', '2012-02-10')]:
            self.reject(['extracted', 'schedule', key], val)

    def test_pet_training_does_not_supply_skill_id_or_price(self):
        self.reject(['extracted', 'pet', 'skill_id_price_or_species_limits'], {'skill': 1, 'price': 0})
        self.reject(['extracted', 'pet', 'prerequisite'], 'PLAYER_COOKING_SKILL')

    def test_honor_not_stones_cash_or_known_reward_table(self):
        for key, val in [('currency_as_written', '石币'), ('amount_rate_daily_cap_or_stock', 100), ('cash_equivalence_or_tradeability', True)]:
            self.reject(['extracted', 'reward', key], val)

    def test_two_advertised_versions_do_not_assign_event_to_either(self):
        self.assertEqual(self.r['extracted']['server_context']['advertised_labels'], ['8.5魔域大冒险', '2.5精灵王传说'])
        for key, val in [('event_applicable_groups', ['8.5', '2.5']), ('exact_client_build', '8.5'), ('belongs_to_original_2002_25', True), ('belongs_to_tw10_or_jss1999', True)]:
            self.reject(['extracted', 'server_context', key], val)

    def test_crowd_images_are_not_recipe_or_delivery_screenshots(self):
        for key, val in [('cooking_event_or_recipe_proven', True), ('capture_date', '2012-02-10'), ('native_client_resolution_proven', True)]:
            self.reject(['images', 0, key], val)
        self.reject(['images', 1, 'requested_url'], 'https://example.invalid/image.jpg')

    def test_five_records_keep_source_profile_and_evidence_alignment(self):
        self.reject(['records', 2, 'game_ids'], [100])
        self.reject(['records', 1, 'version_profile'], 'TW10')
        self.reject(['records', 2, 'evidence'], self.r['records'][3]['evidence'])

    def test_nineteen_actual_source_mutations_bypass_digest_gate(self):
        cases = self.local['audit']['real_source_mutations']
        self.assertEqual(len(cases), 19)
        self.assertEqual(len({x['input_sha256'] for x in cases}), 19)
        self.assertTrue(all(x['rejected_without_digest_gate'] for x in cases))
        self.assertTrue(self.local['audit']['outer_script_positive'])

    def test_authority_and_stage_remain_bounded(self):
        self.reject(['source', 'authority'], 'AUTHENTICATED_OFFICIAL_SERVER')
        self.reject(['source', 'authenticated_2012_original_bytes'], True)
        for k in self.r['unproven']:
            self.reject(['unproven', k], True)
        self.reject(['status', 'stage_b_wiki'], 'OPEN')
        self.reject(['next'], 'EXPAND_COOKING_HELPERS')

    def test_permanent_receipt_is_required_and_pins_actual_dual_replays(self):
        p = m.ROOT / ('research/recovered/' + m.STEM + '-CUSTODY-R1.json')
        self.assertTrue(p.is_file(), 'Accepted source material requires permanent custody')
        r = json.loads(p.read_text())
        self.assertEqual(r['schema'], 'stoneage.cn2012_cooking_event.custody.r1')
        self.assertEqual(len(r['source_pins']), 10)
        self.assertEqual(len(r['startup_prefixes']), 9)
        for pin in r['source_pins'] + r['startup_prefixes']:
            b = (m.ROOT / pin['path']).read_bytes()
            if pin in r['startup_prefixes']:
                b = b[:pin['bytes']]
            self.assertEqual(len(b), pin['bytes'])
            self.assertEqual(m.sha(b), pin['sha256'])
            self.assertEqual(hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest(), pin['git_blob'])
        self.assertEqual(len(r['workflow_runs']), 21)
        self.assertTrue(all(x['conclusion'] == 'success' and x['head_sha'] == r['content_head'] for x in r['workflow_runs']))
        copies = []
        for label in ('candidate', 'main'):
            meta = r[label]
            self.assertEqual(meta['actual_unit_tests'], 9)
            self.assertEqual(meta['skipped_tests'], 0)
            self.assertEqual(meta['head'], r['content_head'])
            self.assertEqual(meta['tree'], r['content_tree'])
            self.assertEqual(meta['real_source_mutations'], 19)
            self.assertTrue(meta['all_applicable_workflows_success'])
            b = (m.ROOT / meta['derived_git_path']).read_bytes()
            self.assertEqual(len(b), meta['raw_bytes'])
            self.assertEqual(m.sha(b), meta['raw_sha256'])
            self.assertEqual(hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest(), meta['raw_git_blob'])
            copies.append(b)
            runs = [x for x in r['workflow_runs'] if x['head_branch'] == ('main' if label == 'main' else 'agent/cn2012-cooking-event-r48-20261021')]
            self.assertEqual(len(runs), meta['own_workflow_count'])
            self.assertIn(meta['run_id'], [x['id'] for x in runs])
        for k in ('run_id', 'job_id', 'artifact_id'):
            self.assertNotEqual(r['candidate'][k], r['main'][k])
        self.assertEqual(copies[0], copies[1])
        self.assertEqual(copies[0], (m.ROOT / ('research/recovered/' + m.STEM + '-LOCAL-REPLAY-R1.json')).read_bytes())
        self.assertTrue(all(x is False for x in r['bounds'].values()))


if __name__ == '__main__':
    unittest.main()
