import copy
import hashlib
import json
import unittest
from tools import stoneage_tw10_animation_selector_r101 as m

REPORT_SHA = 'b6e0dd1482a675d49d005fb947c1873b0776ba25289c1c03f3ac259fa54ddd92'


def verify_report(d):
    raw = m.REPORT.read_bytes()
    if hashlib.sha256(raw).hexdigest() != REPORT_SHA or d != json.loads(raw):
        raise ValueError('archived original instruction/authority report changed')
    return True


class AnimationSelector(unittest.TestCase):
    def test_original_report_and_boundary_guards(self):
        d = json.loads(m.REPORT.read_text())
        self.assertTrue(verify_report(d))
        self.assertEqual((len(d['native_selector_replays']), len(d['native_countdown_replays'])), (10, 10))
        for field in d['boundaries']:
            changed = copy.deepcopy(d)
            changed['boundaries'][field] = 100 if field == 'overall_percent' else True
            with self.subTest(field=field), self.assertRaises(ValueError):
                verify_report(changed)
        for key, value in [('unmatched_pair_fallback_record', 1), ('compiled_upper_inclusive', 132767), ('upper_endpoint_memory_safety_proven', True), ('tick_milliseconds_proven', True)]:
            changed = copy.deepcopy(d)
            changed['compiled_contract'][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                verify_report(changed)

    def test_normalization_division_clamp_and_no_millisecond_assumption(self):
        self.assertEqual(m.ticks(1000, 12), 5)
        self.assertEqual(m.ticks(1000, 7), 8)
        self.assertEqual(m.ticks(0, 1), 1)
        self.assertEqual(m.ticks(15, 1), 1)
        self.assertEqual(m.ticks(64, 2), 2)
        with self.assertRaises(ValueError):
            m.ticks(1000, 0x10000000)
        with self.assertRaises(ValueError):
            m.ticks(-1, 2)

    def test_zero_count_keeps_raw_duration(self):
        self.assertEqual(m.ticks(1000, 0), 1000)
        self.assertEqual(m.ticks(0, 0), 0)

    def test_exact_first_duplicate_fallback_and_missing(self):
        self.assertEqual(m.first_match([(0, 0), (2, 6)], 2, 6), 1)
        self.assertEqual(m.first_match([(2, 6), (2, 6)], 2, 6), 0)
        self.assertEqual(m.first_match([(0, 0), (2, 6)], 9, 9), 0)
        self.assertIsNone(m.first_match([], 2, 6))

    def test_native_source_identity_required_before_any_execution(self):
        for raw in [b'', b'MZ' + b'\0' * 425982, b'not original source']:
            with self.assertRaises(ValueError):
                m.inspect(raw)

    def test_native_and_reference_saved_outputs_identical(self):
        d = json.loads(m.REPORT.read_text())
        for row in d['native_selector_replays']:
            self.assertEqual(row['native'], row['reference'])
            self.assertEqual(row['reference'], m.expected_select(row['input']))
        for row in d['native_countdown_replays']:
            self.assertEqual(row['native_result'], m.ticks(row['duration'], row['frames']))

    def test_original_source_tables_are_pinned(self):
        result = m.source_tables()
        self.assertEqual(result['SPR-GROUP-R1.tsv.gz']['rows'], 464)
        self.assertEqual(result['SPR-ANIMATION-R1.tsv.gz']['rows'], 39065)
        self.assertEqual(result['derived_countdown'], {'minimum': 1, 'maximum': 75, 'zero_frame_headers': 0, 'max_frame_count': 112})


if __name__ == '__main__':
    unittest.main()
