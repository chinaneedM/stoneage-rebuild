import copy
import hashlib
import json
import unittest
from tools import stoneage_jp2004_chat_update_source as m


class ChatUpdateSource(unittest.TestCase):
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

    def test_six_records_keep_attribution_version_and_no_game_ids(self):
        m.validate(self.r)
        self.reject(['records', 0, 'game_ids'], [100])
        self.reject(['records', 0, 'version_profile'], 'TW10')
        self.reject(['records', 3, 'runtime_verified'], True)
        self.reject(['records', 4, 'evidence'], self.r['records'][3]['evidence'])

    def test_press_report_and_body_byline_not_verbatim_operator_release(self):
        self.assertEqual(self.r['extracted']['body_byline'], 'Kawamura')
        self.assertTrue(self.local['audit']['meta_author_positive'])
        self.reject(['source', 'authority'], 'VERBATIM_OPERATOR_RELEASE')
        self.reject(['source', 'authenticated_2004_original_bytes'], True)
        self.assertEqual(self.r['extracted']['template_slots'], {'content_slots': 1, 'empty_slots': 4})

    def test_current_service_first_major_not_original_jss_start(self):
        c = self.r['extracted']['context']
        self.assertEqual(c['reported_formal_service_month'], '2004-06')
        self.assertEqual(c['planned_maintenance_clock_hours'], [15, 16])
        self.assertEqual(c['trial_days_reported'], 10)
        for k, v in [('first_major_update_scope', 'FIRST_IN_GAME_HISTORY'), ('actual_deployment_or_completion_verified', True), ('maintenance_timezone', 'Asia/Tokyo'), ('numeric_client_build', '1.74a'), ('trial_audience', 'ALL_PLAYERS')]:
            self.reject(['extracted', 'context', k], v)

    def test_unnamed_island_and_dungeons_do_not_gain_names_routes_or_ids(self):
        self.assertEqual(self.r['extracted']['exploration']['dungeon_regions_as_written'], ['サイナス島', 'ジャルガ島'])
        for k, v in [('new_island_name_or_id', 'ミライア島'), ('island_route', [1, 2]), ('actual_npc_migration_verified', True), ('dungeon_names_ids_entrances_routes', {'cave': 1})]:
            self.reject(['extracted', 'exploration', k], v)

    def test_mana_is_named_guide_but_secret_is_speculation(self):
        self.assertEqual(self.r['extracted']['guide']['name_as_written'], 'マーナ')
        self.reject(['extracted', 'guide', 'secret_assessment_as_written'], '確認している')
        self.reject(['extracted', 'guide', 'confirmed_hidden_story_or_boss'], 'DARK_KING')
        self.reject(['extracted', 'guide', 'original_npc_id_or_same_person_in_images'], 'IMAGE_CHARACTER')

    def test_counterpart_chat_block_not_account_or_trade_ban(self):
        self.assertEqual(self.r['extracted']['chat_filter']['reported_target'], 'REGISTERED_COUNTERPART_CHAT')
        self.reject(['extracted', 'chat_filter', 'account_ban_or_trade_restriction_proven'], True)
        self.reject(['extracted', 'chat_filter', 'ui_controls_list_capacity_channels_persistence_identity_matching'], {'capacity': 100})
        self.reject(['extracted', 'chat_filter', 'actual_filter_execution_verified'], True)

    def test_npc_dates_and_approximate_maintenance_not_guaranteed_quest_activation(self):
        s = self.r['extracted']['staging']
        self.assertEqual(s['npc_placement_days_as_reported'], [3, 6])
        self.assertEqual((s['maintenance_minutes_as_reported'], s['maintenance_duration_qualifier_as_written']), (30, '程度'))
        self.reject(['extracted', 'staging', 'quest_activation_days_are_media_inference'], False)
        self.reject(['extracted', 'staging', 'quests_actually_available_on_those_dates_proven'], True)
        self.reject(['extracted', 'staging', 'exact_maintenance_clocks_or_timezone'], ['00:00', '00:30'])

    def test_three_actual_images_are_not_chat_filter_ui_or_map_identity(self):
        self.assertEqual([im['path_as_written'].split('_')[-1] for im in self.r['images']], ['0.jpg', '2.jpg', '1.jpg'])
        for k, v in [('capture_date', '2004-08-01'), ('shows_chat_filter_ui', True), ('native_client_resolution_proven', True), ('original_map_npc_id_or_named_island_identity_proven', True)]:
            self.reject(['images', 0, k], v)

    def test_twenty_real_source_mutations_without_digest_gate(self):
        cases = self.local['audit']['real_source_mutations']
        self.assertEqual(len(cases), 20)
        self.assertEqual(len({x['input_sha256'] for x in cases}), 20)
        self.assertTrue(all(x['rejected_without_digest_gate'] for x in cases))
        self.assertTrue(self.local['audit']['outer_script_positive'])
        self.assertTrue(self.local['audit']['meta_author_positive'])

    def test_evidence_and_production_gates_remain_bounded(self):
        for k in self.r['unproven']:
            self.reject(['unproven', k], True)
        self.reject(['status', 'stage_b_wiki'], 'OPEN')
        self.reject(['next'], 'EXPAND_CHAT_OR_SECRET_MAP_HELPERS')

    def test_permanent_receipt_required_and_actual_dual_replays_pinned(self):
        p = m.ROOT / ('research/recovered/' + m.STEM + '-CUSTODY-R1.json')
        self.assertTrue(p.is_file(), 'Accepted source material requires permanent custody')
        r = json.loads(p.read_text())
        self.assertEqual(r['schema'], 'stoneage.jp2004_chat_update.custody.r1')
        self.assertEqual(len(r['source_pins']), 10)
        self.assertEqual(len(r['startup_prefixes']), 9)
        for pin in r['source_pins'] + r['startup_prefixes']:
            b = (m.ROOT / pin['path']).read_bytes()
            if pin in r['startup_prefixes']:
                b = b[:pin['bytes']]
            self.assertEqual(len(b), pin['bytes'])
            self.assertEqual(hashlib.sha256(b).hexdigest(), pin['sha256'])
            self.assertEqual(hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest(), pin['git_blob'])
        self.assertEqual(len(r['workflow_runs']), 21)
        self.assertTrue(all(x['status'] == 'completed' and x['conclusion'] == 'success' and x['head_sha'] == r['content_head'] for x in r['workflow_runs']))
        copies = []
        for label in ('candidate', 'main'):
            meta = r[label]
            self.assertEqual(meta['actual_unit_tests'], 10)
            self.assertEqual(meta['skipped_tests'], 0)
            self.assertEqual(meta['head'], r['content_head'])
            self.assertEqual(meta['tree'], r['content_tree'])
            self.assertEqual(meta['real_source_mutations'], 20)
            self.assertEqual(meta['actual_html_bytes'], 10860)
            self.assertEqual(meta['actual_image_bytes'], [31490, 26016, 24235])
            self.assertTrue(meta['outer_script_positive'] and meta['meta_author_positive'])
            self.assertTrue(meta['all_applicable_workflows_success'])
            b = (m.ROOT / meta['derived_git_path']).read_bytes()
            self.assertEqual(len(b), meta['raw_bytes'])
            self.assertEqual(hashlib.sha256(b).hexdigest(), meta['raw_sha256'])
            self.assertEqual(hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest(), meta['raw_git_blob'])
            copies.append(b)
            branch = 'main' if label == 'main' else 'agent/jp2004-chat-update-r50-20261021'
            runs = [x for x in r['workflow_runs'] if x['head_branch'] == branch]
            self.assertEqual(len(runs), meta['own_workflow_count'])
            self.assertEqual(meta['own_workflow_count'], 11 if label == 'main' else 10)
            self.assertIn(meta['run_id'], [x['id'] for x in runs])
        for k in ('run_id', 'job_id', 'artifact_id'):
            self.assertNotEqual(r['candidate'][k], r['main'][k])
        self.assertEqual(copies[0], copies[1])
        self.assertEqual(copies[0], (m.ROOT / ('research/recovered/' + m.STEM + '-LOCAL-REPLAY-R1.json')).read_bytes())
        self.assertTrue(all(x is False for x in r['bounds'].values()))


if __name__ == '__main__':
    unittest.main()
