"""WORLD34 cross-receipt regression only; no original executable in CI."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'research/recovered/STONEAGE-STAGE-A-WORLD34-FIELD-ITEM-BRIDGE-R1.json'


def git_blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii') + b'\0' + raw).hexdigest()


class World34FieldItemBridgeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(REPORT.read_bytes())
        cls.sources = {}
        for name, witness in cls.report['sources'].items():
            raw = (ROOT / witness['path']).read_bytes()
            if git_blob(raw) != witness['git_blob']:
                raise AssertionError('WORLD34 upstream original witness changed: ' + name)
            cls.sources[name] = raw
        cls.w31 = json.loads(cls.sources['w31'])
        cls.w33 = json.loads(cls.sources['w33'])

    def test_scope_and_original_source_pair(self):
        self.assertEqual(self.report['scope'], 'CROSS_RECEIPT_SOURCE_BOUND_NO_NEW_NATIVE_EXECUTION')
        self.assertEqual(self.report['parent_archive_sha256'], self.w31['archive_sha256'])
        self.assertEqual(self.report['parent_archive_sha256'], self.w33['archive_sha256'])
        self.assertEqual(self.report['server_program']['character_use'],
                         self.w31['program']['symbols']['_CHAR_ItemUse'])
        self.assertEqual(self.report['server_program']['recovery_callback'],
                         self.w31['program']['symbols']['_ITEM_useRecovery'])
        self.assertEqual(self.report['server_program']['field_recovery_callback'],
                         self.w31['program']['symbols']['_ITEM_useRecovery_Field'])
        self.assertEqual(self.report['server_program']['field_packet_entry'], 0x413130)
        self.assertEqual(self.report['server_program']['field_intake_branch_to_character_use'], 0x41324c)

    def test_three_actual_original_row_witnesses_and_client_gates(self):
        by_id = {r['item_id']: r for r in self.report['original_items']}
        self.assertEqual(set(by_id), {1232, 12530, 12555})
        classes = {r['row']['id']: r for r in self.w33['source_class_witnesses']}
        self.assertEqual([by_id[i]['physical_row']['scene'] for i in (1232, 12530, 12555)],
                         [1, 0, 2])
        self.assertEqual([by_id[i]['physical_row']['target'] for i in (1232, 12530, 12555)],
                         [2, 1, 1])
        for item_id, row in by_id.items():
            with self.subTest(item_id=item_id):
                witness = classes[item_id]
                self.assertEqual(row['physical_row'], witness['row'])
                self.assertEqual(row['client_field_gate_passed'],
                                 witness['client']['field_use_gate_passed'])
                self.assertEqual(row['client_battle_gate_passed'],
                                 witness['client']['battle_slot_selectable'])
                self.assertTrue(row['prior_native_intake_preflight_reached_callback_entry'])
                self.assertEqual(row['prior_native_intake_preflight_item_int_keys'], [46, 3, 3, 0])
                self.assertTrue(row['physical_row']['row_sha256'])
        self.assertFalse(by_id[1232]['client_field_gate_passed'])
        self.assertTrue(by_id[12530]['client_field_gate_passed'])
        self.assertTrue(by_id[12555]['client_field_gate_passed'])

    def test_separately_replayed_callback_fixtures_are_not_end_to_end(self):
        by_id = {r['item_id']: r for r in self.report['original_items']}
        self.assertIsNone(by_id[1232]['independent_recovery_callback_fixture'])
        samples = {s['id']: s for s in self.w31['catalog']['sample_rows']}
        replay = self.w31['emulated']['ordinary_option_replays']
        for item_id in (12530, 12555):
            fixture = by_id[item_id]['independent_recovery_callback_fixture']
            sample = samples[item_id]
            tokens = [list(x) for x in sample['values'].items()]
            matches = [r for r in replay if r['tokens'] == tokens]
            self.assertEqual(len(matches), 1)
            self.assertEqual(fixture['option_tokens'], tokens)
            self.assertEqual(fixture['field_written_stats_at_rand_zero'], matches[0]['field_rand_0'])
            self.assertEqual(fixture['field_written_stats_at_rand_max'], matches[0]['field_rand_max'])
            self.assertIs(fixture['fixture_is_direct_callback_not_intake_chain'], True)
        self.assertEqual(by_id[12530]['independent_recovery_callback_fixture']
                         ['field_written_stats_at_rand_zero'], [388])
        self.assertEqual(by_id[12555]['independent_recovery_callback_fixture']
                         ['field_written_stats_at_rand_zero'], [266, 28])

    def test_prior_target_dispatch_is_a_bounded_transcription(self):
        f = self.report['prior_field_intake_preflight']
        self.assertEqual(f['observed_work_guard_keys'], [64, 0])
        self.assertEqual(f['observed_out_of_range_or_missing_pet_target_value'], -1)
        self.assertEqual(f['observed_target_dispatch'],
                         [{'input': i, 'lookup': ('caster' if i == 0 else
                            'pet_slot' if i <= 5 else 'party_slot'),
                           'slot': (None if i == 0 else i - 1 if i <= 5 else i - 6)}
                          for i in range(11)])
        self.assertIn('halted at ITEM_useRecovery entry', f['result_scope'])

    def test_all_unobserved_results_stay_false(self):
        for key, observed in self.report['boundaries'].items():
            with self.subTest(key=key):
                self.assertIs(observed, False)


if __name__ == '__main__':
    unittest.main()
