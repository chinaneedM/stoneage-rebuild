"""Mutation gates for shared retention, no-alias controls and full payout."""
from pathlib import Path
import unittest
from tools.stoneage_battle_original_player_pet_partition_audit import validate_report
REPORT=Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-BATTLE-ORIGINAL-PLAYER-PET-PARTITION-R1.txt'

class PlayerPetPartitionEvidenceValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=REPORT.read_text()

    def test_complete_matrix(self):
        self.assertEqual(tuple(map(len,validate_report(self.report))),(48,192))

    def test_every_alias_recipient_replacement_capacity_required(self):
        for row in self.report.splitlines():
            if '|REAL_HEADER_PLAYER_PET_PARTITION_' in row:
                with self.assertRaises(ValueError):validate_report(self.report.replace(row,''))

    def test_assignment_identity_and_every_retention_field(self):
        row=next(r for r in self.report.splitlines() if '|REAL_HEADER_PLAYER_PET_PARTITION_ASSIGN|recipient=1|branch=2|alias=0|' in r)
        for field in row.split('|')[3:]:
            name,value=field.split('=',1)
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace(field,name+'=99')))
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace('|'+field,'')))

    def test_payout_every_state_release_packet_and_timer_field(self):
        row=next(r for r in self.report.splitlines() if '|REAL_HEADER_PLAYER_PET_PARTITION_PAYOUT|recipient=1|branch=1|alias=0|victim=8|' in r)
        for field in row.split('|')[3:]:
            name,value=field.split('=',1)
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace(field,name+'=99')))
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace('|'+field,'')))

    def test_alias_retained_original_enemy_owner_and_one_reference(self):
        for alias in (0,1):
            for branch in (1,2,3):
                row=next(r for r in self.report.splitlines() if '|REAL_HEADER_PLAYER_PET_PARTITION_PAYOUT|recipient=1|branch='+str(branch)+'|alias='+str(alias)+'|' in r)
                victim=7+branch
                for field,value in ((f'live{victim}','0'),(f'owner{victim}',str(alias)),(f'ref{victim}','0'),(f'release{victim}','1')):
                    old=next(p for p in row.split('|') if p.startswith(field+'='))
                    with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace(old,field+'='+value)))

    def test_no_alias_control_releases_once_at_assignment(self):
        row=next(r for r in self.report.splitlines() if '|REAL_HEADER_PLAYER_PET_PARTITION_ASSIGN|recipient=0|branch=1|alias=-1|' in r)
        for old,new in (('release_calls=1','release_calls=0'),('count_delta=-1','count_delta=0'),('victim_live=0','victim_live=1'),('victim_owner=-1','victim_owner=6')):
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace(old,new)))

    def test_duplicate_unknown_profile_recipient_branch_and_alias(self):
        row=next(r for r in self.report.splitlines() if '|REAL_HEADER_PLAYER_PET_PARTITION_ASSIGN|' in r)
        for bad in (self.report+'\n'+row,self.report.replace(row,row.replace('ACTUAL|gavin|','ACTUAL|unknown|')),self.report.replace(row,row.replace('recipient=0|','recipient=2|')),self.report.replace(row,row.replace('branch=1|','branch=0|')),self.report.replace(row,row.replace('alias=-1|','alias=3|'))):
            with self.assertRaises(ValueError):validate_report(bad)

    def test_predecessor_resolution_and_optimization_proof_required(self):
        for old in ('RESOLUTION|ORIGINAL_REAL_HEADER_PLAYER_PET_PARTITION_BOUNDED_PASS','RESOLUTION|ORIGINAL_REAL_HEADER_TWO_PLAYER_CONCENTRATED_BOUNDED_PASS','optimizations=O0,O2'):
            with self.assertRaises(ValueError):validate_report(self.report.replace(old,'',1))

class PetPartitionIndependentChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=REPORT.read_text()
    def test_pet_alias_released_but_reference_survives(self):
        for profile in ('gavin','bismarck'):
            for branch in (1,2,3):
                victim=7+branch
                row=next(r for r in self.report.splitlines() if f'ACTUAL|{profile}|REAL_HEADER_PLAYER_PET_PARTITION_PAYOUT|recipient=1|branch={branch}|alias=2|' in r)
                for old,new in ((f'live{victim}=0',f'live{victim}=1'),(f'owner{victim}=-1',f'owner{victim}=6'),(f'ref{victim}=1',f'ref{victim}=0'),(f'release{victim}=0',f'release{victim}=1')):
                    self.assertIn(old,row)
                    with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace(old,new)))

    def test_pet_assignment_guard_never_retains(self):
        row=next(r for r in self.report.splitlines() if '|REAL_HEADER_PLAYER_PET_PARTITION_ASSIGN|recipient=0|branch=1|alias=2|' in r)
        for old,new in (('guard_warnings=0','guard_warnings=1'),('release_calls=1','release_calls=0'),('count_delta=-1','count_delta=0'),('victim_live=0','victim_live=1'),('victim_owner=-1','victim_owner=6'),('victim_refs=1','victim_refs=0')):
            self.assertIn(old,row)
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace(old,new)))

if __name__=='__main__':unittest.main()
