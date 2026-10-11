"""Adversarial validation of source-gate evidence completeness."""
import unittest
from tools.stoneage_battle_original_same_item_full_bag_audit import validate_report


def sample_report():
    lines = []
    for profile, first, last, one in [('gavin', 11, 23, 0), ('bismarck', 9, 28, 1)]:
        lines.append(f'PROFILE|{profile}|optimizations=O0,O2|sha256=fixture')
        for case in range(3):
            full = case == 1
            fields = dict(case=case, actor=6, registered_item=3, recipient=0,
                          bag_slot=-1 if full else last if case == 2 else first,
                          owner=-1 if full else 0, item_live=int(not full),
                          released=int(full), second_loop=1, original_finish=1,
                          profit=1, exp_gold=1, whole_items=1, whole_actors=1,
                          whole_arena=1, arena_released=1, logs=int(not full),
                          data=int(not full), one=0 if full else one)
            lines.append(f'ACTUAL|{profile}|REAL_HEADER_SAME_ITEM_CAPACITY|' +
                         '|'.join(f'{k}={v}' for k, v in fields.items()))
    lines.append('RESOLUTION|ORIGINAL_REAL_HEADER_SAME_ITEM_CAPACITY_BOUNDED_PASS')
    return '\n'.join(lines)


class CapacityEvidenceValidation(unittest.TestCase):
    def test_requires_complete_capacity_matrix(self):
        self.assertEqual(len(validate_report(sample_report())), 6)

    def test_missing_profile_or_case_rejected(self):
        report = sample_report()
        for line in report.splitlines():
            if '|REAL_HEADER_SAME_ITEM_CAPACITY|' in line:
                with self.subTest(line=line), self.assertRaises(ValueError):
                    validate_report(report.replace(line, ''))

    def test_live_item_or_owner_after_full_release_rejected(self):
        for before, after in [('owner=-1', 'owner=0'), ('item_live=0', 'item_live=1'),
                              ('released=1', 'released=0'), ('logs=0', 'logs=1')]:
            with self.subTest(after=after), self.assertRaises(ValueError):
                validate_report(sample_report().replace(before, after, 1))

    def test_missing_whole_domain_or_loop_rejected(self):
        for field in ['whole_items', 'whole_actors', 'whole_arena', 'arena_released',
                      'second_loop', 'original_finish', 'profit', 'exp_gold']:
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_report(sample_report().replace(field + '=1', field + '=0', 1))

    def test_duplicate_witness_rejected(self):
        report = sample_report()
        row = next(x for x in report.splitlines() if x.startswith('ACTUAL|'))
        with self.assertRaises(ValueError):
            validate_report(report + '\n' + row)

    def test_missing_paired_optimization_or_resolution_rejected(self):
        for text in ['optimizations=O0,O2', 'RESOLUTION|ORIGINAL_REAL_HEADER_SAME_ITEM_CAPACITY_BOUNDED_PASS']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                validate_report(sample_report().replace(text, '', 1))

    def test_last_slot_must_be_later_than_initial_empty(self):
        with self.assertRaises(ValueError):
            validate_report(sample_report().replace('bag_slot=23', 'bag_slot=11'))


if __name__ == '__main__':
    unittest.main()
