from collections import Counter
from fractions import Fraction
import json
import unittest

from tools.stoneage_battle_recovery_source import ARCHIVE_SHA, CODE, DATA, REPORT, SCOPE, SYMBOLS, WORLD31, sha


class World32BattleRecoveryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads(WORLD31.read_bytes())
        cls.report = json.loads(REPORT.read_bytes())
        cls.cases = cls.report['observations']

    def test_scope_and_provenance(self):
        report = self.report
        self.assertEqual(report['scope'], SCOPE)
        self.assertEqual(report['archive_sha256'], ARCHIVE_SHA)
        self.assertEqual(report['world31_receipt_sha256'], sha(WORLD31.read_bytes()))
        self.assertEqual(report['original_member'], self.source['selected_source_members'][0])
        self.assertEqual(report['program']['symbols'], SYMBOLS)
        self.assertEqual([tuple(window[:2]) for window in report['program']['source_windows']], list(CODE + DATA))
        self.assertEqual(report['program']['rng_constants'], [0.9, 1.1, 2**-31])
        self.assertEqual(report['fixture']['x87_control_word'], 0x037f)
        for key in ('original_client_or_server_started', 'live_battle_outcome_observed',
                    'inventory_actually_mutated', 'official_early_version_equivalence_proven'):
            self.assertIs(report[key], False)

    def test_all_ordinary_requests_and_independent_arithmetic(self):
        options, rows = Counter(), Counter()
        for source in self.source['emulated']['ordinary_option_replays']:
            kind, power, percent = source['battle_request_kind_value_percent']
            self.assertEqual(percent, 0)
            options[kind, power] += 1
            rows[kind, power] += source['source_rows']
        batch = self.report['ordinary_request_batch']
        self.assertEqual(len(batch), 79)
        self.assertEqual(sum(options.values()), 116)
        self.assertEqual(sum(rows.values()), 583)
        for case in batch:
            with self.subTest(request=case['world31_request']):
                battle, caster, target, kind, power, percent, effect, subtype = case['world31_request']
                self.assertEqual((battle, caster, target, percent, effect), (4, 2, 9, 0, 0x18904))
                self.assertEqual(subtype, 0x188f9 + (power > 100) + (power > 300))
                self.assertEqual(case['ordinary_options'], options.pop((kind, power)))
                self.assertEqual(case['source_rows'], rows.pop((kind, power)))
                start = (100, 10)[kind]
                lower = Fraction(power * 0.9)
                width = Fraction(power * 1.1 - float(lower) + 1)
                expected = []
                for rand in (0, 2**31 - 1):
                    gain = int(lower + int(width * Fraction(rand, 2**31)))
                    expected.append([[9, 10 + kind, start, start + gain]])
                self.assertEqual(case['unclamped_writes'], expected)
        self.assertFalse(options or rows)

    def test_cap_is_applied_to_write_but_not_battle_buffer(self):
        for kind, hp_mp, initial, maximum, gain in ((0, 'hp', 980, 1000, 288), (1, 'mp', 95, 100, 22)):
            for suffix, current in (('cap', initial), ('full', maximum)):
                case = self.cases[f'{hp_mp}_{suffix}']
                self.assertEqual(case['writes'], [[9, 10 + kind, current, maximum]])
                self.assertTrue(case['battle_buffer'].endswith(f'BD|r7|{kind:X}|1|d{gain:X}|p0|'))
                self.assertTrue(case['settlement_returned'])

    def test_hp_gate_runs_after_selection_and_mp_does_not_call_it(self):
        hp = self.cases['hp_cure_denied']
        self.assertEqual(hp['selected_slots'], [7])
        self.assertEqual(hp['cure_checks'], [9])
        self.assertEqual(hp['writes'], [])
        self.assertEqual(hp['rand'], [])
        self.assertEqual(hp['battle_buffer'], 'BJ|a2|mA|e18904|e188FB|r7|FF|')
        self.assertTrue(hp['settlement_returned'])
        mp = self.cases['mp_cure_denied_fixture']
        self.assertEqual(mp['cure_checks'], [])
        self.assertEqual(mp['writes'], [[9, 11, 10, 32]])

    def test_rejected_targets_retarget_within_the_original_side(self):
        for key in ('dead_requested_slot', 'inactive_mode', 'excluded_mode_5',
                    'required_flag_1_clear', 'excluded_flag_8_set'):
            case = self.cases[key]
            self.assertEqual(case['selected_slots'], [0])
            self.assertEqual(case['rand'], [0, 0])
            self.assertEqual(case['writes'], [[10, 10, 100, 388]])
        case = self.cases['dead_second_side_slot']
        self.assertEqual(case['selected_slots'], [10])
        self.assertEqual(case['writes'], [[10, 11, 10, 32]])
        retry = self.cases['retarget_retry']
        self.assertEqual(retry['selected_slots'], [0])
        self.assertEqual(retry['rand'], [9, 10, 2**31 - 1])
        self.assertEqual(retry['writes'], [[10, 10, 100, 452]])

    def test_empty_side_stops_at_unfilled_native_list(self):
        case = self.cases['no_eligible_slot']
        self.assertEqual(case['incomplete_list']['return_value'], -1)
        self.assertEqual(case['incomplete_list']['stack_words_before_call'], [0x12345678, 0x23456789])
        self.assertEqual(case['incomplete_list']['stack_words_after_call'],
                         case['incomplete_list']['stack_words_before_call'])
        self.assertFalse(case['settlement_returned'])
        self.assertEqual(case['diagnostics'], [[1, 10]])
        for field in ('writes', 'selected_slots', 'cure_checks', 'rand'):
            self.assertEqual(case[field], [])
        self.assertEqual(case['battle_buffer'], '')


if __name__ == '__main__':
    unittest.main()
