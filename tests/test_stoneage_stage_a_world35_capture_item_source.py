"""Verify WORLD35's derived mixed25 evidence without proprietary bytes."""

from collections import Counter
from fractions import Fraction
import json
import unittest

from tools.stoneage_capture_item_source import CODE, DATA, REPORT, WORLD19, WORLD34
from tools.stoneage_recovery_source import RNG_HIGH


class CaptureItemSourceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(REPORT.read_bytes())
        cls.items = {row['id']: row for row in cls.report['item_rows']}
        cls.controls = {name: case['trace'] for name, case in cls.report['control_cases'].items()}
        cls.world19 = json.loads(WORLD19.read_bytes())

    def test_source_provenance_and_original_rows(self):
        self.assertEqual(self.report['archive_sha256'], self.world19['source']['archive_sha256'])
        self.assertEqual(self.report['alternate_item_source'], self.world19['source']['B'])
        self.assertEqual(self.report['source_members'][0]['member_sha256'],
                         self.world19['partial_executable']['previous_WORLD18_complete_member_sha256'])
        self.assertEqual(len(self.report['item_rows']), len(self.items))
        self.assertEqual(Counter((r['type'], r['fieldtype'], r['target']) for r in self.items.values()),
                         {(20, 1, 0): 25, (16, 1, 1): 1})
        self.assertEqual({r['useaction'] for r in self.items.values()}, {-1})
        self.assertEqual(self.items[2702]['base_option'], 80)
        self.assertEqual([tuple(w[:2]) for w in self.report['source_windows']], list(CODE + DATA))
        for _, _, digest in self.report['source_windows']:
            self.assertRegex(digest, r'^[0-9a-f]{64}$')

        shards = (REPORT.parent / 'item-module-01').glob('*.json')
        item_index = {row[0]: row for path in shards for row in json.loads(path.read_bytes())['rows']}
        for item, row in self.items.items():
            self.assertEqual(item_index[item][1:3], [row['row_without_line_ending_sha256']] * 2)

    def test_random_endpoints_apply_to_recipient_then_consume_item(self):
        cases = self.report['ordinary_cases']
        self.assertEqual(len(cases), 52)
        self.assertEqual({(case['id'], case['random']) for case in cases},
                         {(item, rand) for item in self.items for rand in (0, RNG_HIGH)})
        for case in cases:
            item, rand, trace = case['id'], case['random'], case['trace']
            with self.subTest(item=item, rand=rand):
                row = self.items[item]
                base = row['base_option']
                low = Fraction(9 * base, 10)
                width = Fraction(base, 5) + 1
                bonus = int(low + int(width * rand / 2**31))
                slot, recipient = (7, 9) if item == 2702 else (2, 8)
                self.assertEqual(trace['settlement_args'], [[0, 2, slot, base, 100612, 100605]])
                self.assertEqual(trace['selected_slots'], [slot])
                self.assertEqual(trace['item_rand'], [rand])
                self.assertEqual(trace['item_work_writes'], [[recipient, 32, 0, bonus]])
                self.assertEqual(trace['delete_args'], [[8, 7, 1, 0]])
                self.assertEqual((trace['slot_after'], trace['item_live_after'],
                                  trace['active_item_count_after']), (-1, 0, 0))
                self.assertEqual(trace['score']['modifier_before'], bonus if recipient == 8 else 0)
                self.assertEqual(trace['score']['points'], 10 + trace['score']['modifier_before'])
                self.assertEqual(trace['score']['modifier_after'], 0)

    def test_fallback_and_nonplayer_still_reach_deletion(self):
        nonplayer = self.controls['nonplayer']
        self.assertEqual(nonplayer['selected_slots'], [17])
        self.assertFalse(nonplayer['item_work_writes'])
        self.assertFalse(nonplayer['item_rand'])
        self.assertEqual(nonplayer['delete_args'], [[8, 7, 1, 0]])
        fallback = self.controls['dead_target_same_side_fallback']
        self.assertEqual(fallback['settlement_args'][0][2], 7)
        self.assertEqual(fallback['selected_slots'], [2])
        self.assertEqual(fallback['item_work_writes'], [[8, 32, 0, 72]])

    def test_early_returns_and_synthetic_options(self):
        for name in ('field_mode', 'initializing_battle', 'missing_item'):
            trace = self.controls[name]
            self.assertEqual(trace['settlement_args'], [])
            self.assertEqual(trace['item_work_writes'], [])
            self.assertEqual(trace['delete_args'], [])
            self.assertEqual(trace['item_live_after'], int(name != 'missing_item'))
        for name in ('failed_scan_default_5', 'empty_option_default_5'):
            self.assertTrue(self.report['control_cases'][name]['synthetic_option'])
            self.assertEqual(self.controls[name]['settlement_args'][0][3], 5)
            self.assertEqual(self.controls[name]['item_work_writes'], [[8, 32, 0, 4]])
        self.assertEqual(self.controls['add_existing']['item_work_writes'], [[8, 32, 12, 16]])
        self.assertEqual(self.controls['middle_random']['item_work_writes'], [[8, 32, 0, 6]])

    def test_score_consumes_the_actors_own_key_and_resets_it(self):
        case = self.controls['teammate_consumes_own_bonus']
        self.assertEqual(case['post_item_modifiers'], [0, 72, 0])
        score = case['score']
        self.assertEqual((score['character'], score['modifier_before'], score['points']), (9, 72, 82))
        self.assertEqual(score['work_writes'], [[9, 32, 72, 0]])
        self.assertEqual(score['modifier_after'], 0)
        self.assertEqual(self.controls['sleep_bonus']['score']['points'], 29)
        for name, points, roll, flag in (
            ('score_equal_rejected', 1, 1, 0),
            ('score_bonus_changes_comparison', 2, 1, 1),
            ('cap_roll_98', 99, 98, 1),
            ('cap_roll_99', 99, 99, 0),
            ('cap_and_high_random', 99, 100, 0),
        ):
            score = self.controls[name]['score']
            self.assertEqual((score['points'], score['integer_roll'], score['comparison_flag']), (points, roll, flag))
            self.assertEqual(score['modifier_after'], 0)

    def test_world34_additive_column_correction_keeps_material_results(self):
        correction = self.report['world34_useaction_correction']
        schema = correction['schema_evidence']
        self.assertEqual(len(schema['paired_descriptors']), 15)
        self.assertEqual((schema['descriptor_ordinal'], schema['physical_column'], schema['runtime_int_key']),
                         (62, 77, 46))
        prior = {(case['item'], case['scenario']): case['trace']
                 for case in json.loads(WORLD34.read_bytes())['cases']}
        rows = correction['rechecks']
        self.assertEqual(len(rows), 18)
        self.assertEqual(len({(row['id'], row['scenario']) for row in rows}), 18)
        for row in rows:
            expected = {1232: -1, 12530: 6, 12555: 7}[row['id']]
            self.assertEqual(row['useaction'], expected)
            self.assertEqual(row['action_notice_called'], expected != -1 and not row['scenario'].startswith('pet'))
            old = prior[row['id'], row['scenario']]
            for key in ('stat_writes', 'delete_args', 'slot_after', 'item_live_after', 'intake_returned'):
                self.assertEqual(row[key], old[key])

    def test_evidence_boundary(self):
        for key in ('original_process_started', 'capture_ownership_executed', 'network_messages_delivered',
                    'historical_official_deployment_verified'):
            self.assertIs(self.report[key], False)
