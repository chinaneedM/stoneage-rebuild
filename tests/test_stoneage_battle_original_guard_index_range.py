"""Reject damaged original guard range and no-state-mutation evidence."""
from pathlib import Path
import unittest
from tools.stoneage_battle_original_guard_index_range_audit import validate_report

REPORT=Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-BATTLE-ORIGINAL-GUARD-INDEX-RANGE-R1.txt'


class GuardIndexRangeEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=REPORT.read_text()

    def row(self,identity):
        return next(s for s in self.report.splitlines() if '|REAL_HEADER_GUARD_INDEX_RANGE|'+identity in s)

    def test_complete_matrix(self):
        self.assertEqual(len(validate_report(self.report)),96)

    def test_every_index_type_use_alias_range_required(self):
        for row in self.report.splitlines():
            if '|REAL_HEADER_GUARD_INDEX_RANGE|' in row:
                with self.assertRaises(ValueError):validate_report(self.report.replace(row,''))

    def test_every_return_warning_and_whole_state_field_required(self):
        for identity in ('fdnum=2|index=2|type=PLAYER|active=1|alias=1|','fdnum=3|index=2|type=PET|active=1|alias=1|'):
            row=self.row(identity)
            for field in row.split('|')[3:]:
                name,value=field.split('=',1)
                with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace(field,name+'=99')))
                with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace('|'+field,'')))

    def test_included_pet_blocks_and_excluded_player_allows(self):
        included=self.row('fdnum=3|index=2|type=PET|active=1|alias=1|')
        excluded=self.row('fdnum=2|index=2|type=PLAYER|active=1|alias=1|')
        self.assertIn('|result=0|',included);self.assertIn('|result=1|',excluded)
        for row,old,new in ((included,'result=0','result=1'),(excluded,'result=1','result=0')):
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace(old,new)))

    def test_inactive_or_missing_alias_never_blocks(self):
        for identity in ('fdnum=3|index=2|type=PET|active=0|alias=1|','fdnum=3|index=0|type=PLAYER|active=1|alias=0|'):
            row=self.row(identity)
            self.assertIn('|result=1|guard_warnings=0|diagnostic_delta=0|',row)
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace('result=1','result=0')))

    def test_guard_decision_does_not_release_or_change_owner(self):
        row=self.row('fdnum=2|index=2|type=PET|active=1|alias=1|')
        for old,new in (('release_calls=0','release_calls=1'),('count_delta=0','count_delta=-1'),('victim_live=1','victim_live=0'),('victim_owner=6','victim_owner=-1')):
            with self.assertRaises(ValueError):validate_report(self.report.replace(row,row.replace(old,new)))

    def test_duplicates_unknown_fields_and_identity_rejected(self):
        row=self.row('fdnum=2|index=0|type=PLAYER|active=0|alias=0|')
        for altered in (self.report+'\n'+row,self.report.replace(row,row+'|extra=1'),self.report.replace(row,row+'|result=1'),self.report.replace(row,row.replace('ACTUAL|gavin|','ACTUAL|unknown|')),self.report.replace(row,row.replace('fdnum=2','fdnum=4')),self.report.replace(row,row.replace('index=0','index=3')),self.report.replace(row,row.replace('type=PLAYER','type=NPC'))):
            with self.assertRaises(ValueError):validate_report(altered)

    def test_prior_resolution_and_optimizer_proof_required(self):
        for old in ('RESOLUTION|ORIGINAL_REAL_HEADER_GUARD_INDEX_RANGE_BOUNDED_PASS','RESOLUTION|ORIGINAL_REAL_HEADER_PLAYER_PET_PARTITION_BOUNDED_PASS','optimizations=O0,O2'):
            with self.assertRaises(ValueError):validate_report(self.report.replace(old,'',1))


if __name__=='__main__':unittest.main()
