import copy
import json
import unittest
from tools import stoneage_cn20_healing_spells_source as m


class HealingSpellsSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(m.REPORT.read_text())
        cls.local = json.loads((m.ROOT / ('research/recovered/' + m.STEM + '-LOCAL-REPLAY-R1.json')).read_text())
        m.validate(cls.r)

    def reject(self, keys, value):
        r = copy.deepcopy(self.r); node = r
        for k in keys[:-1]:
            node = node[k]
        node[keys[-1]] = value
        with self.assertRaises(ValueError):
            m.validate(r)

    def test_thirteen_rowspan_rows_and_original_order(self):
        m.validate(self.r)
        rows = self.r['extracted']['rows']
        self.assertEqual([sum(x['table_label_as_written'] == label for x in rows) for label in ['治愈的精灵','滋润的精灵','恩惠的精灵','复活的精灵']], [4,4,3,2])
        self.assertEqual([x['listed_cost'] for x in rows], [5,8,11,14,8,12,16,20,20,30,40,20,35])
        self.reject(['extracted', 'rows', 0, 'listed_cost'], 6)

    def test_non_monotonic_plus10_is_preserved_without_correction(self):
        row = self.r['extracted']['rows'][5]
        self.assertEqual((row['table_label_as_written'], row['level_as_written'], row['listed_recovery_amount']), ('滋润的精灵','LV2',10))
        self.assertEqual(row['effect_as_written'], '回复单体的耐久力+10')
        self.reject(['extracted', 'rows', 5, 'listed_recovery_amount'], 100)
        self.reject(['records', 6, 'source_reported', 'listed_recovery_amount'], 100)

    def test_intro_shenen_and_table_enhui_are_separate_labels(self):
        intro = self.r['extracted']['intro']
        self.assertEqual(intro['healing_roles_and_names_as_written'][2], {'role':'神恩精灵','name':'提欧'})
        self.assertEqual(self.r['extracted']['rows'][8]['table_label_as_written'], '恩惠的精灵')
        self.reject(['extracted', 'rows', 8, 'table_label_as_written'], '神恩的精灵')

    def test_player_only_self_single_and_allied_all_scopes_not_flattened(self):
        intro = self.r['extracted']['intro']; rows = self.r['extracted']['rows']
        self.assertEqual(intro['halu_scope_as_written'], '只能回复玩家')
        self.assertEqual(intro['freya_scope_as_written'], '我方一人或宠物一匹')
        self.assertEqual([rows[i]['target_as_written'] for i in [0,4,8,11]], ['自己','单体','己方全体','单体'])
        self.reject(['extracted', 'rows', 0, 'target_as_written'], '单体')

    def test_three_revival_names_do_not_map_to_two_level_rows(self):
        intro = self.r['extracted']['intro']; rows = self.r['extracted']['rows']
        self.assertEqual(intro['revival_names_as_written'], ['希鲁菲尔','雅鲁','哈恩'])
        self.assertIsNone(intro['order_direction_and_name_to_lv_mapping'])
        self.assertTrue(all(x['revival_described'] for x in rows[-2:]))
        self.reject(['extracted', 'intro', 'order_direction_and_name_to_lv_mapping'], {'LV1':'希鲁菲尔','LV2':'雅鲁'})

    def test_pet_revive_loyalty_and_experience_are_qualified_advice(self):
        intro = self.r['extracted']['intro']
        self.assertEqual(intro['loyalty_phrase_as_written'], '不会下降很多')
        self.assertEqual(intro['experience_phrase_as_written'], '又有经验值')
        self.reject(['extracted', 'intro', 'exact_loyalty_loss_experience_amount_or_no_penalty'], {'loyalty_loss':0,'exp_return':'FULL'})

    def test_equipment_parent_is_qualitative_context_only(self):
        self.assertEqual(self.r['extracted']['intro']['equipment_mainly_as_written'], ['衣服','铠甲','等防具'])
        self.reject(['prior_battle_context', 'same_client_build_or_runtime_formula_proven'], True)
        self.reject(['prior_battle_context', 'parent', 'sha256'], '0' * 64)
        self.reject(['extracted', 'intro', 'all_equipment_or_exclusive_rule'], 'ARMOR_ONLY')

    def test_table_levels_values_and_cost_do_not_become_runtime_fields(self):
        for row in self.r['extracted']['rows']:
            self.assertEqual(row['stat_as_written'], '耐久力')
            self.assertEqual(row['cost_column_as_written'], '消耗气力')
            self.assertIsNone(row['player_level_requirement_or_original_spell_id'])
        self.reject(['extracted', 'rows', 0, 'runtime_stat_field_formula_caps_or_timing'], {'hp':50,'mp':-5})
        self.reject(['records', 1, 'game_ids'], [100])

    def test_research_records_keep_version_source_rights_and_revision(self):
        for row in self.r['records']:
            self.assertTrue(set(['record_id','entity_type','version_profile','source_refs','verification_status','rights_status','record_revision']).issubset(row))
        self.reject(['records', 1, 'version_profile'], 'TW10')
        self.reject(['records', 1, 'rights_status'], 'RELEASE_APPROVED')
        self.reject(['records', 1, 'source_refs'], ['N1'])
        self.reject(['sources', 1, 'publication_date'], '2001-12-04')

    def test_eighteen_real_source_mutations_no_screenshot_or_production_promotion(self):
        cases = self.local['audit']['real_source_mutations']
        self.assertEqual(len(cases), 18)
        self.assertEqual(len({x['input_sha256'] for x in cases}), 18)
        self.assertTrue(all(x['rejected_without_digest_gate'] for x in cases))
        self.assertEqual(self.r['extracted']['content_images'], 0)
        for k in self.r['unproven']:
            self.reject(['unproven', k], True)
        self.reject(['status', 'stage_b_wiki'], 'OPEN')
        self.reject(['next'], 'IMPLEMENT_ORIGINAL_HEALING_OR_FETCH_ALL_SPELLS')

    def test_permanent_receipt_required_and_actual_dual_replays_pinned(self):
        p = m.ROOT / ('research/recovered/' + m.STEM + '-CUSTODY-R1.json')
        self.assertTrue(p.is_file(), 'Accepted source material requires permanent custody')
        r = json.loads(p.read_text())
        self.assertEqual(r['schema'], 'stoneage.cn20_healing_spells.custody.r1')
        self.assertEqual(len(r['source_pins']), 11)
        self.assertEqual(len(r['startup_prefixes']), 9)
        for pin in r['source_pins'] + r['startup_prefixes']:
            b = (m.ROOT / pin['path']).read_bytes()
            if pin in r['startup_prefixes']:
                b = b[:pin['bytes']]
            self.assertEqual(len(b), pin['bytes'])
            self.assertEqual(m.sha(b), pin['sha256'])
            self.assertEqual(m.blob(b), pin['git_blob'])
        self.assertEqual(len(r['workflow_runs']), 21)
        self.assertTrue(all(x['status'] == 'completed' and x['conclusion'] == 'success' and x['head_sha'] == r['content_head'] for x in r['workflow_runs']))
        copies = []
        for label in ('candidate', 'main'):
            meta = r[label]
            self.assertEqual(meta['actual_unit_tests'], 10)
            self.assertEqual(meta['skipped_tests'], 0)
            self.assertEqual(meta['head'], r['content_head'])
            self.assertEqual(meta['tree'], r['content_tree'])
            self.assertEqual(meta['actual_html_bytes'], [69317, 67848])
            self.assertEqual((meta['spell_level_rows'], meta['context_records']), (13, 1))
            self.assertEqual(meta['rowspan_group_lengths'], [4, 4, 3, 2])
            self.assertEqual(meta['real_source_mutations'], 18)
            self.assertTrue(meta['outer_script_positive'] and meta['all_applicable_workflows_success'])
            self.assertEqual(meta['content_images_fetched'], 0)
            self.assertFalse(meta['old_battle_originals_reacquired'])
            self.assertEqual(meta['zip_entry_names'], ['replay.json'])
            b = (m.ROOT / meta['derived_git_path']).read_bytes()
            self.assertEqual(len(b), meta['raw_bytes'])
            self.assertEqual(m.sha(b), meta['raw_sha256'])
            self.assertEqual(m.blob(b), meta['raw_git_blob'])
            copies.append(b)
            branch = 'main' if label == 'main' else 'agent/cn20-healing-spells-r53-20261021'
            runs = [x for x in r['workflow_runs'] if x['head_branch'] == branch]
            self.assertEqual(len(runs), meta['own_workflow_count'])
            self.assertEqual(meta['own_workflow_count'], 11 if label == 'main' else 10)
            self.assertIn(meta['run_id'], [x['id'] for x in runs])
        for k in ('run_id', 'job_id', 'artifact_id'):
            self.assertNotEqual(r['candidate'][k], r['main'][k])
        self.assertEqual(copies[0], copies[1])
        self.assertEqual(copies[0], (m.ROOT / ('research/recovered/' + m.STEM + '-LOCAL-REPLAY-R1.json')).read_bytes())
        self.assertTrue(r['independent_checks']['source_plus10_preserved_and_not_corrected'])
        self.assertTrue(all(x is False for x in r['bounds'].values()))


if __name__ == '__main__':
    unittest.main()
