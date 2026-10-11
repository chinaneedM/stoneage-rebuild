"""Require complete native single-creation four-drop-chain evidence."""
from pathlib import Path
import unittest
from tools.stoneage_battle_original_four_drop_chain_audit import validate_report
REPORT=Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-BATTLE-ORIGINAL-FOUR-DROP-CHAIN-R1.txt'

class FourDropChainEvidenceValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=REPORT.read_text()

    def test_complete_matrix(self):
        self.assertEqual(tuple(map(len,validate_report(self.report))),(2,8,16))

    def test_every_creation_assignment_branch_capacity_required(self):
        for row in self.report.splitlines():
            if '|REAL_HEADER_FOUR_DROP_' in row:
                with self.assertRaises(ValueError):validate_report(self.report.replace(row,''))

    def test_creation_identities_draws_native_domains_and_no_rebinding(self):
        row=next(r for r in self.report.splitlines() if '|REAL_HEADER_FOUR_DROP_CREATE|' in r)
        for field in row.split('|')[3:]:
            name,value=field.split('=',1)
            replacement='0' if name in ('blockers','cleared_inactive_refs') else '99'
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace(field,name+'='+replacement)))
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace('|'+field,'')))

    def test_assignment_empty_initial_slots_one_call_and_exact_rng(self):
        row=next(r for r in self.report.splitlines() if '|REAL_HEADER_FOUR_DROP_ASSIGN|branch=1|' in r)
        for field in row.split('|')[3:]:
            name,value=field.split('=',1)
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace(field,name+'=99')))
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace('|'+field,'')))

    def test_every_payout_state_release_transport_and_timer_field(self):
        row=next(r for r in self.report.splitlines() if '|REAL_HEADER_FOUR_DROP_PAYOUT|branch=1|available=1|' in r)
        for field in row.split('|')[3:]:
            name,value=field.split('=',1)
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace(field,name+'=99')))
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace('|'+field,'')))

    def test_overflow_victim_cannot_release_again(self):
        row=next(r for r in self.report.splitlines() if '|REAL_HEADER_FOUR_DROP_PAYOUT|branch=1|available=0|' in r)
        with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace('release8=0','release8=1')))

    def test_duplicate_unknown_profile_and_resolution_rejected(self):
        row=next(r for r in self.report.splitlines() if '|REAL_HEADER_FOUR_DROP_ASSIGN|' in r)
        for bad in (self.report+'\n'+row,self.report.replace(row,row.replace('ACTUAL|gavin|','ACTUAL|unknown|')),self.report.replace('RESOLUTION|ORIGINAL_REAL_HEADER_FOUR_DROP_CHAIN_BOUNDED_PASS','')):
            with self.assertRaises(ValueError):validate_report(bad)

    def test_predecessor_and_optimization_evidence_required(self):
        for old in ('RESOLUTION|ORIGINAL_REAL_HEADER_OVERFLOW_TICKET_BOUNDED_PASS','optimizations=O0,O2'):
            with self.assertRaises(ValueError):validate_report(self.report.replace(old,'',1))

if __name__=='__main__':unittest.main()
