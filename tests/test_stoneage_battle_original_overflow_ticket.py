"""Reject weakened, incomplete or contradictory native overflow evidence."""
from pathlib import Path
import unittest
from tools.stoneage_battle_original_overflow_ticket_audit import validate_report
REPORT=Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-BATTLE-ORIGINAL-OVERFLOW-TICKET-R1.txt'

class OverflowEvidenceValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=REPORT.read_text()

    def test_complete_matrix(self):
        assignment,payout=validate_report(self.report)
        self.assertEqual((len(assignment),len(payout)),(8,16))

    def test_every_branch_and_capacity_required(self):
        for row in self.report.splitlines():
            if '|REAL_HEADER_OVERFLOW_' in row:
                with self.assertRaises(ValueError):validate_report(self.report.replace(row,''))

    def test_assignment_rng_victim_and_native_domains(self):
        row=next(r for r in self.report.splitlines() if '|REAL_HEADER_OVERFLOW_ASSIGN|branch=1|' in r)
        for name in ('factory','factory_id','factory_draws','victim','rng','release_calls','count_delta','whole_items','whole_actors','whole_arena','tables_immutable','carried_cleared','original_factory','original_assignment','no_item_control'):
            field=next(f for f in row.split('|') if f.startswith(name+'='))
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace(field,name+'=99')))

    def test_order_and_explicit_binding_required(self):
        row=next(r for r in self.report.splitlines() if '|REAL_HEADER_OVERFLOW_ASSIGN|branch=1|' in r)
        for old,new in [('pending=7,5,6','pending=4,5,6'),('binding=explicit','binding=natural')]:
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace(old,new)))

    def test_each_payout_field_required_and_checked(self):
        row=next(r for r in self.report.splitlines() if '|REAL_HEADER_OVERFLOW_PAYOUT|branch=1|available=1|' in r)
        for field in row.split('|')[3:]:
            name,value=field.split('=',1)
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace(field,name+'=99')))
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace('|'+field,'')))

    def test_duplicate_unknown_and_resolution_rejected(self):
        row=next(r for r in self.report.splitlines() if '|REAL_HEADER_OVERFLOW_PAYOUT|' in r)
        for bad in (self.report+'\n'+row,self.report.replace(row,row.replace('ACTUAL|gavin|','ACTUAL|unknown|')),self.report.replace('RESOLUTION|ORIGINAL_REAL_HEADER_OVERFLOW_TICKET_BOUNDED_PASS','')):
            with self.assertRaises(ValueError):validate_report(bad)

    def test_predecessor_and_optimization_evidence_required(self):
        for old in ('RESOLUTION|ORIGINAL_REAL_HEADER_DISTINCT_ITEM_TICKET_BOUNDED_PASS','optimizations=O0,O2'):
            with self.assertRaises(ValueError):validate_report(self.report.replace(old,'',1))

if __name__=='__main__':unittest.main()
