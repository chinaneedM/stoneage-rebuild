"""Reject incomplete exceptional-ticket evidence, including concealed aliases."""
import unittest
from tests.test_stoneage_battle_original_same_item_full_bag import sample_report as capacity_report
from tools.stoneage_battle_original_ticket_cleanup_audit import validate_report


def sample_report():
    lines = [capacity_report()]
    for profile in ('gavin', 'bismarck'):
        for case in range(4):
            duplicate = case == 3
            fields = dict(case=case, recipient=2 if case == 1 else -1 if case == 2 else 0,
                          item=3, live=int(duplicate), owner=0 if duplicate else -1,
                          references=2 if duplicate else 0, logs=2 if duplicate else 0,
                          data=int(duplicate), one=2 if duplicate and profile == 'bismarck' else 0,
                          second_loop=1, arena_released=1, tickets_cleared=1,
                          whole_items=1, whole_actors=1, whole_arena=1, whole_connections=1, original_timer=1)
            lines.append(f'ACTUAL|{profile}|REAL_HEADER_TICKET_CLEANUP|' +
                         '|'.join(f'{k}={v}' for k,v in fields.items()))
    lines.append('RESOLUTION|ORIGINAL_REAL_HEADER_TICKET_CLEANUP_BOUNDED_PASS')
    return '\n'.join(lines)


class CleanupEvidenceValidation(unittest.TestCase):
    def test_complete_matrix(self):
        self.assertEqual(len(validate_report(sample_report())), 8)

    def test_every_case_required(self):
        report = sample_report()
        for line in report.splitlines():
            if '|REAL_HEADER_TICKET_CLEANUP|' in line:
                with self.subTest(line=line), self.assertRaises(ValueError):
                    validate_report(report.replace(line, ''))

    def test_release_references_and_owner_required(self):
        for field in ('live=0', 'references=0', 'owner=-1'):
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_report(sample_report().replace(field, field.split('=')[0]+'=1', 1))

    def test_duplicate_aliases_cannot_be_hidden(self):
        for field in ('references=2', 'logs=2', 'data=1', 'one=2'):
            report = sample_report()
            row = next(x for x in report.splitlines() if x.startswith('ACTUAL|bismarck|REAL_HEADER_TICKET_CLEANUP|case=3'))
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_report(report.replace(row, row.replace(field, field.split('=')[0]+'=0')))

    def test_whole_domains_required(self):
        for field in ('second_loop', 'arena_released', 'tickets_cleared', 'whole_items',
                      'whole_actors', 'whole_arena', 'whole_connections'):
            report = sample_report()
            row = next(x for x in report.splitlines() if '|REAL_HEADER_TICKET_CLEANUP|' in x)
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_report(report.replace(row, row.replace(field+'=1', field+'=0')))

    def test_duplicate_or_unknown_case_rejected(self):
        report = sample_report()
        row = next(x for x in report.splitlines() if '|REAL_HEADER_TICKET_CLEANUP|' in x)
        for changed in (report+'\n'+row, report.replace(row, row.replace('case=0', 'case=4'))):
            with self.assertRaises(ValueError):
                validate_report(changed)

    def test_timer_execution_scope_cannot_be_promoted(self):
        report = sample_report()
        for profile, before, after in [('bismarck', 'original_timer=1', 'original_timer=0'),
                                       ('gavin', 'original_timer=1', 'original_timer=0')]:
            row = next(x for x in report.splitlines() if x.startswith('ACTUAL|'+profile+'|REAL_HEADER_TICKET_CLEANUP|'))
            with self.subTest(profile=profile), self.assertRaises(ValueError):
                validate_report(report.replace(row, row.replace(before, after)))

    def test_predecessor_and_resolution_required(self):
        report = sample_report()
        for marker in ('RESOLUTION|ORIGINAL_REAL_HEADER_TICKET_CLEANUP_BOUNDED_PASS',
                       'RESOLUTION|ORIGINAL_REAL_HEADER_SAME_ITEM_CAPACITY_BOUNDED_PASS',
                       'optimizations=O0,O2'):
            with self.subTest(marker=marker), self.assertRaises(ValueError):
                validate_report(report.replace(marker, '', 1))


if __name__ == '__main__':
    unittest.main()
