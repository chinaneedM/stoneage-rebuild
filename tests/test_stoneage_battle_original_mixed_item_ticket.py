"""Require the complete ordered mixed-ticket matrix and native domains."""
import unittest
from tests.test_stoneage_battle_original_invalid_item_ticket import sample_report as invalid_report
from tools.stoneage_battle_original_mixed_item_ticket_audit import INVALID,validate_report


def sample_report():
    rows=[invalid_report()]
    for profile in ('gavin','bismarck'):
        for kind in (0,1):
            for bad in range(5 if kind else 6):
                for position in range(3):
                    awards=kind+1
                    f=dict(kind=kind,bad=bad,position=position,invalid=INVALID[bad],
                           valid_mask=7-(1<<position) if kind else 1<<position,
                           awards=awards,named_items=awards if profile=='bismarck' else 0,leak=0 if profile=='bismarck' else 1,secret_empty=1,item=3,live=1,owner=0,pool_size=256,count_unchanged=1,
                           references=awards,logs=awards,data=1,one=awards if profile=='bismarck' else 0,
                           rs=1,packet_oracle=1,second_loop=1,arena_released=1,tickets_cleared=1,
                           whole_items=1,whole_actors=1,whole_arena=1,whole_connections=1,original_timer=1)
                    rows.append(f'ACTUAL|{profile}|REAL_HEADER_MIXED_ITEM_TICKET|'+'|'.join(f'{k}={v}' for k,v in f.items()))
    rows.append('RESOLUTION|ORIGINAL_REAL_HEADER_MIXED_ITEM_TICKET_BOUNDED_PASS')
    return '\n'.join(rows)


class MixedTicketEvidenceValidation(unittest.TestCase):
    def test_complete_matrix(self):self.assertEqual(len(validate_report(sample_report())),66)

    def test_every_profile_kind_invalid_and_position_required(self):
        r=sample_report()
        for row in r.splitlines():
            if '|REAL_HEADER_MIXED_ITEM_TICKET|' in row:
                with self.subTest(row=row),self.assertRaises(ValueError):validate_report(r.replace(row,''))

    def test_exact_slot_masks_cannot_be_flattened(self):
        r=sample_report()
        for row in r.splitlines():
            if '|REAL_HEADER_MIXED_ITEM_TICKET|' in row:
                field=next(x for x in row.split('|') if x.startswith('valid_mask='))
                with self.subTest(field=field),self.assertRaises(ValueError):validate_report(r.replace(row,row.replace(field,'valid_mask=0')))

    def test_duplicate_alias_multiplicity_preserved(self):
        r=sample_report();row=next(x for x in r.splitlines() if '|REAL_HEADER_MIXED_ITEM_TICKET|kind=1|' in x)
        for field in ('awards','references','logs'):
            with self.subTest(field=field),self.assertRaises(ValueError):validate_report(r.replace(row,row.replace(field+'=2',field+'=1')))

    def test_complete_native_domains_timer_and_packet_required(self):
        r=sample_report();row=next(x for x in r.splitlines() if '|REAL_HEADER_MIXED_ITEM_TICKET|' in x)
        for field in ('whole_items','whole_actors','whole_arena','whole_connections','count_unchanged','original_timer','rs','packet_oracle','second_loop','tickets_cleared','arena_released'):
            with self.subTest(field=field),self.assertRaises(ValueError):validate_report(r.replace(row,row.replace(field+'=1',field+'=0')))

    def test_exact_invalid_index_required(self):
        r=sample_report()
        for row in r.splitlines():
            if '|REAL_HEADER_MIXED_ITEM_TICKET|' in row:
                field=next(x for x in row.split('|') if x.startswith('invalid='))
                with self.subTest(field=field),self.assertRaises(ValueError):validate_report(r.replace(row,row.replace(field,'invalid=3')))

    def test_profile_single_slot_send_distinction_required(self):
        r=sample_report()
        for profile,wrong in [('gavin',1),('bismarck',0)]:
            row=next(x for x in r.splitlines() if x.startswith(f'ACTUAL|{profile}|REAL_HEADER_MIXED_ITEM_TICKET|'))
            one=next(x for x in row.split('|') if x.startswith('one='))
            with self.assertRaises(ValueError):validate_report(r.replace(row,row.replace(one,'one='+str(wrong))))

    def test_name_and_identification_profiles_cannot_be_flattened(self):
        r=sample_report();row=next(x for x in r.splitlines() if x.startswith('ACTUAL|gavin|REAL_HEADER_MIXED_ITEM_TICKET|'))
        for old,new in [('named_items=0','named_items=1'),('leak=1','leak=0'),('secret_empty=1','secret_empty=0')]:
            with self.assertRaises(ValueError):validate_report(r.replace(row,row.replace(old,new)))

    def test_unknown_duplicate_and_missing_fields_rejected(self):
        r=sample_report();row=next(x for x in r.splitlines() if '|REAL_HEADER_MIXED_ITEM_TICKET|' in x)
        for altered in (r+'\n'+row,r.replace(row,row.replace('position=0','position=3')),r.replace(row,row.replace('kind=0','kind=2')),r.replace(row,row.replace('|valid_mask=1',''))):
            with self.assertRaises(ValueError):validate_report(altered)

    def test_predecessor_optimization_and_resolution_required(self):
        r=sample_report()
        for marker in ('RESOLUTION|ORIGINAL_REAL_HEADER_MIXED_ITEM_TICKET_BOUNDED_PASS','RESOLUTION|ORIGINAL_REAL_HEADER_INVALID_ITEM_TICKET_BOUNDED_PASS','optimizations=O0,O2'):
            with self.subTest(marker=marker),self.assertRaises(ValueError):validate_report(r.replace(marker,'',1))


if __name__=='__main__':unittest.main()
