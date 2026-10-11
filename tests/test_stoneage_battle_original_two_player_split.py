"""Reject missing or corrupted native two-recipient evidence."""
from pathlib import Path
import unittest
from tools.stoneage_battle_original_two_player_split_audit import validate_report
REPORT=Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-BATTLE-ORIGINAL-TWO-PLAYER-SPLIT-R1.txt'

class TwoPlayerSplitEvidenceValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=REPORT.read_text()

    def test_complete_matrix(self):
        self.assertEqual(tuple(map(len,validate_report(self.report))),(28,112))

    def test_all_fourteen_orders_and_four_bag_combinations_required(self):
        for row in self.report.splitlines():
            if '|REAL_HEADER_TWO_PLAYER_' in row:
                with self.assertRaises(ValueError):validate_report(self.report.replace(row,''))

    def test_assignment_every_identity_draw_and_full_state_field(self):
        row=next(r for r in self.report.splitlines() if '|REAL_HEADER_TWO_PLAYER_ASSIGN|mask=5|' in r)
        for field in row.split('|')[3:]:
            name,value=field.split('=',1)
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace(field,name+'=99')))
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace('|'+field,'')))

    def test_payout_every_identity_full_state_transport_and_timer_field(self):
        row=next(r for r in self.report.splitlines() if '|REAL_HEADER_TWO_PLAYER_PAYOUT|mask=5|capacity=3|' in r)
        for field in row.split('|')[3:]:
            name,value=field.split('=',1)
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace(field,name+'=99')))
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace('|'+field,'')))

    def test_players_cannot_exchange_awards(self):
        row=next(r for r in self.report.splitlines() if '|REAL_HEADER_TWO_PLAYER_PAYOUT|mask=5|capacity=3|' in r)
        for wrong in ('winner0=8','owner8=0','owner9=1'):
            name=wrong.split('=')[0];old=next(f for f in row.split('|') if f.startswith(name+'='))
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace(old,wrong)))

    def test_duplicate_unknown_profile_and_invalid_order_rejected(self):
        row=next(r for r in self.report.splitlines() if '|REAL_HEADER_TWO_PLAYER_ASSIGN|' in r)
        for bad in (self.report+'\n'+row,self.report.replace(row,row.replace('ACTUAL|gavin|','ACTUAL|unknown|')),self.report.replace(row,row.replace('mask=1|','mask=0|'))):
            with self.assertRaises(ValueError):validate_report(bad)

    def test_original_chain_and_optimization_proof_required(self):
        for old in ('RESOLUTION|ORIGINAL_REAL_HEADER_TWO_PLAYER_SPLIT_BOUNDED_PASS','RESOLUTION|ORIGINAL_REAL_HEADER_FOUR_DROP_CHAIN_BOUNDED_PASS','optimizations=O0,O2'):
            with self.assertRaises(ValueError):validate_report(self.report.replace(old,'',1))

    def test_release_is_exact_for_full_and_independent_free_bags(self):
        for capacity in range(4):
            row=next(r for r in self.report.splitlines() if '|REAL_HEADER_TWO_PLAYER_PAYOUT|mask=5|capacity='+str(capacity)+'|' in r)
            field=next(f for f in row.split('|') if f.startswith('release8='));wrong='release8='+str(1-int(field.split('=')[1]))
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace(field,wrong)))

if __name__=='__main__':unittest.main()
