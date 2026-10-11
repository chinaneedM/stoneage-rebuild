"""Reject incomplete or falsely promoted invalid-ticket runtime evidence."""
import unittest
from tests.test_stoneage_battle_original_recipient_side import sample_report as side_report
from tools.stoneage_battle_original_invalid_item_ticket_audit import CASES, validate_report


def sample_report():
    rows=[side_report()]
    for profile in ('gavin','bismarck'):
        for case,ticket in enumerate(CASES):
            fields=dict(case=case,ticket=ticket,recipient=0,pool_size=256,pool_unchanged=1,count_unchanged=1,
                        references=0,logs=0,data=0,one=0,second_loop=1,arena_released=1,tickets_cleared=1,
                        whole_items=1,whole_actors=1,whole_arena=1,whole_connections=1,original_timer=1)
            rows.append(f'ACTUAL|{profile}|REAL_HEADER_INVALID_ITEM_TICKET|'+'|'.join(f'{k}={v}' for k,v in fields.items()))
    rows.append('RESOLUTION|ORIGINAL_REAL_HEADER_INVALID_ITEM_TICKET_BOUNDED_PASS')
    return '\n'.join(rows)


class InvalidTicketEvidenceValidation(unittest.TestCase):
    def test_complete_matrix(self):
        self.assertEqual(len(validate_report(sample_report())),12)

    def test_every_profile_and_edge_case_required(self):
        r=sample_report()
        for row in r.splitlines():
            if '|REAL_HEADER_INVALID_ITEM_TICKET|' in row:
                with self.subTest(row=row),self.assertRaises(ValueError):validate_report(r.replace(row,''))

    def test_exact_indices_cannot_be_substituted(self):
        r=sample_report()
        for row in r.splitlines():
            if '|REAL_HEADER_INVALID_ITEM_TICKET|' in row:
                ticket=next(p for p in row.split('|') if p.startswith('ticket='))
                with self.subTest(ticket=ticket),self.assertRaises(ValueError):validate_report(r.replace(row,row.replace(ticket,'ticket=-1')))

    def test_complete_native_domains_required(self):
        r=sample_report();row=next(x for x in r.splitlines() if '|REAL_HEADER_INVALID_ITEM_TICKET|' in x)
        for field in ('whole_items','whole_actors','whole_arena','whole_connections','pool_unchanged','count_unchanged','original_timer','second_loop','tickets_cleared','arena_released'):
            with self.subTest(field=field),self.assertRaises(ValueError):validate_report(r.replace(row,row.replace(field+'=1',field+'=0')))

    def test_no_reference_or_presentation_allowed(self):
        r=sample_report();row=next(x for x in r.splitlines() if '|REAL_HEADER_INVALID_ITEM_TICKET|' in x)
        for field in ('references','logs','data','one'):
            with self.subTest(field=field),self.assertRaises(ValueError):validate_report(r.replace(row,row.replace(field+'=0',field+'=1')))

    def test_missing_fields_rejected(self):
        r=sample_report();row=next(x for x in r.splitlines() if '|REAL_HEADER_INVALID_ITEM_TICKET|' in x)
        with self.assertRaises(ValueError):validate_report(r.replace(row,row.replace('|pool_size=256','')))

    def test_duplicates_unknown_cases_and_profiles_rejected(self):
        r=sample_report();row=next(x for x in r.splitlines() if '|REAL_HEADER_INVALID_ITEM_TICKET|' in x)
        for altered in (r+'\n'+row,r.replace(row,row.replace('case=0','case=6')),r.replace(row,row.replace('ACTUAL|gavin','ACTUAL|iris'))):
            with self.assertRaises(ValueError):validate_report(altered)

    def test_predecessor_optimization_and_resolution_required(self):
        r=sample_report()
        for marker in ('RESOLUTION|ORIGINAL_REAL_HEADER_INVALID_ITEM_TICKET_BOUNDED_PASS','RESOLUTION|ORIGINAL_REAL_HEADER_RECIPIENT_SIDE_BOUNDED_PASS','optimizations=O0,O2'):
            with self.subTest(marker=marker),self.assertRaises(ValueError):validate_report(r.replace(marker,'',1))


if __name__=='__main__':unittest.main()
