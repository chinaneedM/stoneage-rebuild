"""Require full last-slot competition and original release observations."""
import unittest
from tests.test_stoneage_battle_original_mixed_item_ticket import sample_report as mixed_report
from tools.stoneage_battle_original_last_slot_ticket_audit import prior,validate_report


def sample_report():
    rows=[mixed_report()]
    for profile in ('gavin','bismarck'):
        for available in (0,1):
            for kind in (0,1):
                for bad in range(5 if kind else 6):
                    for position in range(3):
                        mask=7-(1<<position) if kind else 1<<position
                        first=next(i for i in range(3) if mask&(1<<i))
                        ri=(1 if kind else 2) if bad<3 else 0;r3=kind+1-available
                        f=dict(available=available,kind=kind,bad=bad,position=position,invalid=prior.INVALID[bad],
                               pending_mask=mask,accepted_mask=(1<<first) if available else 0,pending_valid=kind+1,awards=available,
                               bag_slot=(53 if profile=='bismarck' else 23) if available else -1,active_limit=54 if profile=='bismarck' else 24,
                               named_items=available if profile=='bismarck' else 0,leak=0 if profile=='bismarck' else 1,secret_empty=1,item=3,
                               live=available,owner=0 if available else -1,pool_size=256,count_delta=0 if available else -1,
                               references=available,logs=available,data=available,one=available if profile=='bismarck' else 0,
                               release_calls=(84 if profile=='bismarck' else 54)+r3+ri,release_item3=r3,release_invalid=ri,release_empty=84 if profile=='bismarck' else 54,baseline_release=84 if profile=='bismarck' else 54,rs=1,packet_oracle=1,second_loop=1,
                               arena_released=1,tickets_cleared=1,whole_items=1,whole_fillers=1,whole_actors=1,whole_arena=1,
                               whole_connections=1,original_timer=1)
                        rows.append(f'ACTUAL|{profile}|REAL_HEADER_LAST_SLOT_TICKET|'+'|'.join(f'{k}={v}' for k,v in f.items()))
    rows.append('RESOLUTION|ORIGINAL_REAL_HEADER_LAST_SLOT_TICKET_BOUNDED_PASS')
    return '\n'.join(rows)


class LastSlotEvidenceValidation(unittest.TestCase):
    def test_complete_matrix(self):self.assertEqual(len(validate_report(sample_report())),132)

    def test_every_capacity_pattern_position_required(self):
        r=sample_report()
        for row in r.splitlines():
            if '|REAL_HEADER_LAST_SLOT_TICKET|' in row:
                with self.subTest(row=row),self.assertRaises(ValueError):validate_report(r.replace(row,''))

    def test_only_first_valid_ticket_can_fill_last_slot(self):
        r=sample_report()
        for row in r.splitlines():
            if '|REAL_HEADER_LAST_SLOT_TICKET|available=1|' in row:
                old=next(x for x in row.split('|') if x.startswith('accepted_mask='))
                with self.assertRaises(ValueError):validate_report(r.replace(row,row.replace(old,'accepted_mask=7')))

    def test_declined_alias_keeps_live_shared_item(self):
        r=sample_report();row=next(x for x in r.splitlines() if '|REAL_HEADER_LAST_SLOT_TICKET|available=1|kind=1|' in x)
        for old,new in [('live=1','live=0'),('owner=0','owner=-1'),('references=1','references=0'),('count_delta=0','count_delta=-1')]:
            with self.assertRaises(ValueError):validate_report(r.replace(row,row.replace(old,new)))

    def test_full_bag_releases_only_once(self):
        r=sample_report();row=next(x for x in r.splitlines() if '|REAL_HEADER_LAST_SLOT_TICKET|available=0|kind=1|' in x)
        for old,new in [('live=0','live=1'),('owner=-1','owner=0'),('count_delta=-1','count_delta=-2'),('references=0','references=1')]:
            with self.assertRaises(ValueError):validate_report(r.replace(row,row.replace(old,new)))

    def test_original_release_attempt_counts_required(self):
        r=sample_report();row=next(x for x in r.splitlines() if '|REAL_HEADER_LAST_SLOT_TICKET|available=1|kind=1|' in x)
        for field in ('release_calls','release_item3','release_invalid','release_empty','baseline_release'):
            old=next(x for x in row.split('|') if x.startswith(field+'='))
            with self.assertRaises(ValueError):validate_report(r.replace(row,row.replace(old,field+'=9')))

    def test_native_domains_filler_and_packet_required(self):
        r=sample_report();row=next(x for x in r.splitlines() if '|REAL_HEADER_LAST_SLOT_TICKET|' in x)
        for field in ('whole_items','whole_fillers','whole_actors','whole_arena','whole_connections','original_timer','packet_oracle','second_loop','tickets_cleared','arena_released'):
            with self.assertRaises(ValueError):validate_report(r.replace(row,row.replace(field+'=1',field+'=0')))

    def test_exact_active_slot_and_profile_names_required(self):
        r=sample_report()
        for old,new in [('bag_slot=23','bag_slot=22'),('bag_slot=53','bag_slot=52'),('active_limit=54','active_limit=24'),('named_items=0','named_items=1')]:
            row=next(x for x in r.splitlines() if '|REAL_HEADER_LAST_SLOT_TICKET|' in x and '|'+old+'|' in x)
            with self.assertRaises(ValueError):validate_report(r.replace(row,row.replace(old,new)))

    def test_unknown_duplicate_and_missing_fields_rejected(self):
        r=sample_report();row=next(x for x in r.splitlines() if '|REAL_HEADER_LAST_SLOT_TICKET|' in x)
        for altered in (r+'\n'+row,r.replace(row,row.replace('available=0','available=2')),r.replace(row,row.replace('|release_item3=1',''))):
            with self.assertRaises(ValueError):validate_report(altered)

    def test_predecessor_optimization_and_resolution_required(self):
        r=sample_report()
        for marker in ('RESOLUTION|ORIGINAL_REAL_HEADER_LAST_SLOT_TICKET_BOUNDED_PASS','RESOLUTION|ORIGINAL_REAL_HEADER_MIXED_ITEM_TICKET_BOUNDED_PASS','optimizations=O0,O2'):
            with self.assertRaises(ValueError):validate_report(r.replace(marker,'',1))


if __name__=='__main__':unittest.main()
