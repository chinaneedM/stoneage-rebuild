"""Evidence completeness and cross-profile guard divergence acceptance."""
import unittest
from tests.test_stoneage_battle_original_ticket_cleanup import sample_report as cleanup_report
from tools.stoneage_battle_original_recipient_side_audit import validate_report


def sample_report():
    rows = [cleanup_report()]
    for profile in ('gavin','bismarck'):
      for side in range(2):
        for case in range(4):
            accepted = int(case%2==0 if profile=='bismarck' else case<2)
            fields = dict(side=side,case=case,recipient=0,npc=case%2,non_player_side=int(case>=2),
                          acquired=accepted,bag_slot=9 if accepted else -1,
                          item=3,live=accepted,owner=0 if accepted else -1,references=accepted,
                          logs=accepted,data=accepted,one=accepted if profile=='bismarck' else 0,
                          second_loop=1,arena_released=1,tickets_cleared=1,
                          whole_items=1,whole_actors=1,whole_arena=1,whole_connections=1,original_timer=1)
            rows.append(f'ACTUAL|{profile}|REAL_HEADER_RECIPIENT_SIDE|' +
                        '|'.join(f'{k}={v}' for k,v in fields.items()))
    rows.append('RESOLUTION|ORIGINAL_REAL_HEADER_RECIPIENT_SIDE_BOUNDED_PASS')
    return '\n'.join(rows)


class RecipientSideEvidenceValidation(unittest.TestCase):
    def test_complete_cross_matrix(self):
        self.assertEqual(len(validate_report(sample_report())),16)

    def test_every_profile_and_case_required(self):
        r=sample_report()
        for row in r.splitlines():
            if '|REAL_HEADER_RECIPIENT_SIDE|' in row:
                with self.subTest(row=row),self.assertRaises(ValueError):
                    validate_report(r.replace(row,''))

    def test_profile_divergence_cannot_be_flattened(self):
        r=sample_report()
        for profile,case in [('gavin',1),('gavin',2),('bismarck',1),('bismarck',2)]:
            row=next(x for x in r.splitlines() if x.startswith(f'ACTUAL|{profile}|REAL_HEADER_RECIPIENT_SIDE|side=0|case={case}|'))
            with self.subTest(profile=profile,case=case),self.assertRaises(ValueError):
                validate_report(r.replace(row,row.replace('acquired=1','acquired=0') if 'acquired=1' in row else row.replace('acquired=0','acquired=1')))

    def test_rejected_item_must_have_no_owner_or_reference(self):
        r=sample_report();row=next(x for x in r.splitlines() if x.startswith('ACTUAL|gavin|REAL_HEADER_RECIPIENT_SIDE|side=0|case=2|'))
        for field in ('owner=-1','references=0','live=0','logs=0'):
            with self.subTest(field=field),self.assertRaises(ValueError):
                validate_report(r.replace(row,row.replace(field,field.split('=')[0]+'=1')))

    def test_native_domains_and_timer_required(self):
        r=sample_report();row=next(x for x in r.splitlines() if '|REAL_HEADER_RECIPIENT_SIDE|' in x)
        for field in ('whole_items','whole_actors','whole_arena','whole_connections','original_timer','second_loop','tickets_cleared','arena_released'):
            with self.subTest(field=field),self.assertRaises(ValueError):
                validate_report(r.replace(row,row.replace(field+'=1',field+'=0')))

    def test_actual_bag_slot_required(self):
        with self.assertRaises(ValueError):
            validate_report(sample_report().replace('bag_slot=9|item=3','bag_slot=10|item=3',1))

    def test_duplicate_and_unknown_case_rejected(self):
        r=sample_report();row=next(x for x in r.splitlines() if '|REAL_HEADER_RECIPIENT_SIDE|' in x)
        for altered in (r+'\n'+row,r.replace(row,row.replace('case=0','case=4')),
                        r.replace(row,row.replace('side=0','side=2'))):
            with self.assertRaises(ValueError):validate_report(altered)

    def test_predecessor_optimization_and_resolution_required(self):
        r=sample_report()
        for marker in ('RESOLUTION|ORIGINAL_REAL_HEADER_RECIPIENT_SIDE_BOUNDED_PASS',
                       'RESOLUTION|ORIGINAL_REAL_HEADER_TICKET_CLEANUP_BOUNDED_PASS',
                       'optimizations=O0,O2'):
            with self.subTest(marker=marker),self.assertRaises(ValueError):
                validate_report(r.replace(marker,'',1))


if __name__=='__main__':unittest.main()
