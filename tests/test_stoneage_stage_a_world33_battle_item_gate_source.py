from collections import Counter
import json
import unittest

from tools.stoneage_battle_item_gate_source import (
    ARCHIVE_SHA, CLIENT, REPORT, SCENE33, SCOPE, WORLD31, sha,
)


class World33BattleItemGateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(REPORT.read_bytes())
        cls.previous = json.loads(WORLD31.read_bytes())
        cls.witnesses = {(w['row']['scene'], w['row']['target']): w
                         for w in cls.report['source_class_witnesses']}

    def assertQueued(self, run, target):
        self.assertEqual(run['parsed_slot_target'], [7, target])
        self.assertEqual(run['battle_work_writes'], [[4, target], [3, 7], [5, 7], [0, 3]])
        self.assertEqual(run['action_setting_calls'], [0])

    def assertWait(self, run):
        self.assertEqual(run['battle_work_writes'], [[3, 11], [0, 3]])
        self.assertEqual(run['action_setting_calls'], [])

    def test_original_members_and_scope(self):
        self.assertEqual(self.report['scope'], SCOPE)
        self.assertEqual(self.report['archive_sha256'], ARCHIVE_SHA)
        self.assertEqual(self.report['world31_receipt_sha256'], sha(WORLD31.read_bytes()))
        client, = [m for m in json.loads(SCENE33.read_bytes())['original_RAR_witness']['members']
                   if m['target'] == CLIENT]
        self.assertEqual(self.report['member_witnesses'], self.previous['selected_source_members'] + [client])
        for flag in ('client_or_server_started', 'network_packets_sent',
                     'live_battle_effect_or_inventory_change_observed', 'official_same_deployment_proven'):
            self.assertIs(self.report[flag], False)

    def test_all_physical_classes_and_original_example_hashes(self):
        counts = Counter()
        for _, field, target, count in self.previous['catalog']['shape_scene_target_counts']:
            counts[field, target] += count
        self.assertEqual(self.report['configured_recovery_rows'], 644)
        self.assertEqual(len(self.report['source_class_witnesses']), 7)
        self.assertEqual({pair: row['source_rows'] for pair, row in self.witnesses.items()}, counts)
        samples = {r['id']: r for r in self.previous['catalog']['sample_rows']}
        for field, target in ((0, 0), (0, 1), (2, 1)):
            row = self.witnesses[field, target]['row']
            self.assertEqual(row['row_sha256'], samples[row['id']]['row_sha256'])
        comment = self.witnesses[1, 1]['row']
        self.assertIs(comment['raw_hash_prefix'], True)
        self.assertEqual([comment['id']], self.previous['catalog']['raw_hash_prefix_ids'])

    def test_client_scene_gates_and_the_actual_formatter_arguments(self):
        for (field, target), case in self.witnesses.items():
            with self.subTest(field=field, target=target):
                client = case['client']
                self.assertEqual(client['battle_slot_selectable'], field != 2)
                self.assertEqual(client['field_use_gate_passed'], field != 1)
                self.assertEqual(client['selector_endpoints'],
                                 [0x404a38 if field == 2 else 0x404a8d,
                                  0x433ae4 if field == 1 else 0x4339ce])
                if field == 2:
                    self.assertNotIn('client_format_args', client)
                    self.assertIsNone(case['client_command_server_replay'])
                else:
                    expected = {0: 2, 1: 7, 2: 20}[target]
                    self.assertEqual(client['client_format_args'], [7, expected])
                    self.assertQueued(case['client_command_server_replay'], expected)
        for client in self.report['client_selection_controls'].values():
            self.assertFalse(client['battle_slot_selectable'])
            self.assertFalse(client['field_use_gate_passed'])

    def test_server_item_reads_and_ordinary_slots_independent_of_scene(self):
        columns = self.report['program']['item_columns']
        self.assertEqual([(x['column_zero_based'], x['runtime_int_key'], x['item_record_offset']) for x in columns],
                         [(20, 4, 20), (21, 5, 24)])
        self.assertEqual(self.report['program']['client_target_type_0_picker']['entry'], 0x404ab3)
        for case in self.witnesses.values():
            for target in (7, 17):
                run = case['server'][str(target)]
                self.assertQueued(run, target)
                self.assertEqual(run['item_instance_reads'], [[0, 4], [0, 4], [24, 4]])
            self.assertWait(case['server']['23'])
        self.assertFalse(self.witnesses[2, 1]['client']['battle_slot_selectable'])
        self.assertQueued(self.witnesses[2, 1]['server']['7'], 7)

    def test_group_target_side_and_wrong_selector_rejection(self):
        for case in self.report['group_target_controls']:
            kind, side = case['target_type'], case['caster_side']
            expected = {2: 20 + side, 3: 21 - side, 4: 22}[kind]
            self.assertEqual(case['client']['client_format_args'], [7, expected])
            for target in (20, 21, 22):
                run = case['server'][str(target)]
                if target == expected:
                    self.assertQueued(run, target)
                else:
                    self.assertWait(run)
        self.assertWait(self.witnesses[0, 0]['server']['20'])

    def test_missing_inventory_malformed_input_and_login(self):
        cases = self.report['negative_controls']
        for key in ('missing_inventory_item', 'malformed_command'):
            self.assertWait(cases[key])
            self.assertEqual(cases[key]['item_instance_reads'], [])
        self.assertEqual(cases['malformed_command']['parsed_slot_target'], [])
        self.assertEqual(cases['not_logged_in']['battle_work_writes'], [])


if __name__ == '__main__':
    unittest.main()
