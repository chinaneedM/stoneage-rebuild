"""Require original distinct-object creation and every ordered capacity oracle."""
import unittest
from tests.test_stoneage_battle_original_last_slot_ticket import sample_report as preceding_report
from tools.stoneage_battle_original_distinct_item_ticket_audit import PERMUTATIONS,validate_report


def sample_report():
    rows=[preceding_report()]
    for profile in ('gavin','bismarck'):
        rows.append(f'ACTUAL|{profile}|REAL_HEADER_DISTINCT_DROP_CREATE|mode=3|actor=4|indices=4,5,6|ids=1,2,1|prob=1000|objects=3|templates=2|count_delta=3|factory_draws=66|spawn_draws=215|ticket_draws=3|pending=4,5,6|owner=4|whole_items=1|whole_other_actors=1|whole_arena=1|tables_immutable=1|carried_cleared=1|original_disposal=1|original_allocator=1')
        for available in (0,1):
            for order,pattern in enumerate(PERMUTATIONS):
                w=pattern[0] if available else -1;b=84 if profile=='bismarck' else 54
                f=dict(available=available,order=order,pattern=','.join(map(str,pattern)),winner=w,winner_id=(2 if w==5 else 1) if available else -1,accepted_mask=available,awards=available,bag_slot=(53 if profile=='bismarck' else 23) if available else -1,active_limit=54 if profile=='bismarck' else 24,named_items=available if profile=='bismarck' else 0,pool_size=256,count_delta=available-3)
                for i in (4,5,6):f.update({f'live{i}':int(w==i),f'owner{i}':0 if w==i else -1,f'ref{i}':int(w==i),f'release{i}':int(w!=i)})
                f.update(release_empty=b,baseline_release=b,release_calls=b+3-available,logs=available,data=available,one=available if profile=='bismarck' else 0,rs=1)
                for n in ('packet_oracle','second_loop','arena_released','tickets_cleared','whole_items','whole_fillers','whole_actors','whole_arena','whole_connections','original_timer','original_creation','original_ticket_assignment'):f[n]=1
                rows.append(f'ACTUAL|{profile}|REAL_HEADER_DISTINCT_ITEM_TICKET|'+'|'.join(f'{k}={v}' for k,v in f.items()))
    rows.append('RESOLUTION|ORIGINAL_REAL_HEADER_DISTINCT_ITEM_TICKET_BOUNDED_PASS')
    return '\n'.join(rows)


class DistinctEvidenceValidation(unittest.TestCase):
    def test_complete_matrix(self):self.assertEqual(len(validate_report(sample_report())),24)

    def test_every_original_creation_required(self):
        r=sample_report()
        for row in r.splitlines():
            if '|REAL_HEADER_DISTINCT_DROP_CREATE|' in row:
                with self.assertRaises(ValueError):validate_report(r.replace(row,''))

    def test_creation_objects_templates_pending_and_owners(self):
        r=sample_report();row=next(x for x in r.splitlines() if '|REAL_HEADER_DISTINCT_DROP_CREATE|' in x)
        for old,new in [('indices=4,5,6','indices=4,4,4'),('ids=1,2,1','ids=1,1,1'),('pending=4,5,6','pending=6,5,4'),('objects=3','objects=2'),('templates=2','templates=1'),('count_delta=3','count_delta=0'),('owner=4','owner=0'),('factory_draws=66','factory_draws=0'),('spawn_draws=215','spawn_draws=214'),('tables_immutable=1','tables_immutable=0'),('original_allocator=1','original_allocator=0')]:
            with self.assertRaises(ValueError):validate_report(r.replace(row,row.replace(old,new)))

    def test_every_capacity_and_permutation_required(self):
        r=sample_report()
        for row in r.splitlines():
            if '|REAL_HEADER_DISTINCT_ITEM_TICKET|' in row:
                with self.assertRaises(ValueError):validate_report(r.replace(row,''))

    def test_first_ticket_identity_and_type_required(self):
        r=sample_report();row=next(x for x in r.splitlines() if '|REAL_HEADER_DISTINCT_ITEM_TICKET|available=1|order=2|' in x)
        for old,new in [('winner=5','winner=4'),('winner_id=2','winner_id=1'),('pattern=5,4,6','pattern=4,5,6'),('accepted_mask=1','accepted_mask=2'),('bag_slot=23','bag_slot=22')]:
            with self.assertRaises(ValueError):validate_report(r.replace(row,row.replace(old,new)))

    def test_each_object_live_owner_reference_and_release_required(self):
        r=sample_report();row=next(x for x in r.splitlines() if '|REAL_HEADER_DISTINCT_ITEM_TICKET|available=1|' in x)
        for n in ('live4','live5','live6','owner4','owner5','owner6','ref4','ref5','ref6','release4','release5','release6','release_empty','release_calls','baseline_release','count_delta'):
            old=next(x for x in row.split('|') if x.startswith(n+'='))
            with self.assertRaises(ValueError):validate_report(r.replace(row,row.replace(old,n+'=99')))

    def test_presentation_and_complete_native_domains_required(self):
        r=sample_report();row=next(x for x in r.splitlines() if '|REAL_HEADER_DISTINCT_ITEM_TICKET|available=1|' in x)
        for n in ('logs','data','named_items','one','rs','packet_oracle','whole_items','whole_fillers','whole_actors','whole_arena','whole_connections','original_timer','original_creation','original_ticket_assignment'):
            old=next(x for x in row.split('|') if x.startswith(n+'='))
            with self.assertRaises(ValueError):validate_report(r.replace(row,row.replace(old,n+'=99')))

    def test_full_bag_releases_all_three_distinct_objects(self):
        r=sample_report();row=next(x for x in r.splitlines() if '|REAL_HEADER_DISTINCT_ITEM_TICKET|available=0|' in x)
        for old,new in [('count_delta=-3','count_delta=-1'),('live5=0','live5=1'),('release6=1','release6=0'),('winner=-1','winner=6')]:
            with self.assertRaises(ValueError):validate_report(r.replace(row,row.replace(old,new)))

    def test_duplicates_unknown_profiles_and_missing_fields_rejected(self):
        r=sample_report();row=next(x for x in r.splitlines() if '|REAL_HEADER_DISTINCT_ITEM_TICKET|' in x)
        for bad in (r+'\n'+row,r.replace(row,row.replace('ACTUAL|gavin|','ACTUAL|unknown|')),r.replace(row,row.replace('order=0','order=6')),r.replace(row,row.replace('|release4=1',''))):
            with self.assertRaises(ValueError):validate_report(bad)

    def test_all_preceding_witnesses_and_resolutions_retained(self):
        r=sample_report()
        for marker in ('RESOLUTION|ORIGINAL_REAL_HEADER_DISTINCT_ITEM_TICKET_BOUNDED_PASS','RESOLUTION|ORIGINAL_REAL_HEADER_LAST_SLOT_TICKET_BOUNDED_PASS','optimizations=O0,O2'):
            with self.assertRaises(ValueError):validate_report(r.replace(marker,'',1))


if __name__=='__main__':unittest.main()
