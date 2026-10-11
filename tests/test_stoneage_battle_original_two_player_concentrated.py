"""Require every native concentrated-recipient overflow and payout witness."""
from pathlib import Path
import unittest
from tools.stoneage_battle_original_two_player_concentrated_audit import validate_report
REPORT=Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-BATTLE-ORIGINAL-TWO-PLAYER-CONCENTRATED-R1.txt'

class ConcentratedEvidenceValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=REPORT.read_text()

    def test_complete_matrix(self):
        self.assertEqual(tuple(map(len,validate_report(self.report))),(16,64))

    def test_every_recipient_branch_capacity_required(self):
        for row in self.report.splitlines():
            if '|REAL_HEADER_TWO_PLAYER_CONCENTRATED_' in row:
                with self.assertRaises(ValueError):validate_report(self.report.replace(row,''))

    def test_assignment_every_identity_victim_draw_and_state_field(self):
        row=next(r for r in self.report.splitlines() if '|REAL_HEADER_TWO_PLAYER_CONCENTRATED_ASSIGN|recipient=1|branch=2|' in r)
        for field in row.split('|')[3:]:
            name,value=field.split('=',1)
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace(field,name+'=99')))
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace('|'+field,'')))

    def test_payout_every_state_release_packet_and_timer_field(self):
        row=next(r for r in self.report.splitlines() if '|REAL_HEADER_TWO_PLAYER_CONCENTRATED_PAYOUT|recipient=1|branch=1|victim=8|other_bag_unchanged=1|capacity=3|' in r)
        for field in row.split('|')[3:]:
            name,value=field.split('=',1)
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace(field,name+'=99')))
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace('|'+field,'')))

    def test_overflow_victim_never_released_again(self):
        for recipient in (0,1):
            for branch in range(4):
                row=next(r for r in self.report.splitlines() if '|REAL_HEADER_TWO_PLAYER_CONCENTRATED_PAYOUT|recipient='+str(recipient)+'|branch='+str(branch)+'|' in r)
                victim=7+branch if branch else 11
                with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace(f'release{victim}=0',f'release{victim}=1')))

    def test_other_free_player_receives_no_item_or_notification(self):
        row=next(r for r in self.report.splitlines() if '|REAL_HEADER_TWO_PLAYER_CONCENTRATED_PAYOUT|recipient=1|branch=1|victim=8|other_bag_unchanged=1|capacity=1|' in r)
        for old,new in (('winner0=-1','winner0=11'),('logs0=0','logs0=1'),('data0=0','data0=1'),('other_bag_unchanged=1','other_bag_unchanged=0')):
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace(old,new)))

    def test_duplicate_unknown_profile_recipient_and_branch(self):
        row=next(r for r in self.report.splitlines() if '|REAL_HEADER_TWO_PLAYER_CONCENTRATED_ASSIGN|' in r)
        for bad in (self.report+'\n'+row,self.report.replace(row,row.replace('ACTUAL|gavin|','ACTUAL|unknown|')),self.report.replace(row,row.replace('recipient=0|','recipient=2|')),self.report.replace(row,row.replace('branch=0|','branch=4|'))):
            with self.assertRaises(ValueError):validate_report(bad)

    def test_predecessor_resolution_and_optimization_proof_required(self):
        for old in ('RESOLUTION|ORIGINAL_REAL_HEADER_TWO_PLAYER_CONCENTRATED_BOUNDED_PASS','RESOLUTION|ORIGINAL_REAL_HEADER_TWO_PLAYER_SPLIT_BOUNDED_PASS','optimizations=O0,O2'):
            with self.assertRaises(ValueError):validate_report(self.report.replace(old,'',1))

if __name__=='__main__':unittest.main()
