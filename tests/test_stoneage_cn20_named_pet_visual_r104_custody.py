import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
from tools import stoneage_cn20_named_pet_visual_r104_custody as c

class Custody(unittest.TestCase):
    def test_real_source_custody(self):
        result=c.validate();self.assertEqual(result['evidence_pins'],13);self.assertEqual(result['actual_source_runs'],23)
        self.assertTrue(result['candidate_main_local_raw_equal']);self.assertFalse(result['native_game_species_ids_recovered'])
    def test_same_length_corrupted_report_rejected(self):
        d=json.loads(c.RECEIPT.read_text());target=c.ROOT/d['artifacts'][0]['path'];real=Path.read_bytes
        def corrupt(p):
            b=real(p);return b[:-1]+b' ' if p==target else b
        with patch.object(Path,'read_bytes',corrupt),self.assertRaisesRegex(ValueError,'Evidence identity'):c.validate()
    def test_mutated_custody_cannot_relabel_native_identity_or_zip(self):
        d=json.loads(c.RECEIPT.read_text())
        for key,value in [('source_commit','0'*40),('candidate_main_local_raw_equal',False),('native_game_species_ids_recovered',True)]:
            altered=copy.deepcopy(d);altered[key]=value
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'Mutated receipt'):c.validate(altered)
        for key,value in [('artifact',0),('zip_sha256','0'*64),('raw_sha256','0'*64)]:
            altered=copy.deepcopy(d);altered['artifacts'][0][key]=value
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'Mutated receipt'):c.validate(altered)
    def test_repinning_receipt_is_not_accepted(self):
        real=Path.read_bytes;d=json.loads(c.RECEIPT.read_text());first=next(iter(d['evidence']));d['evidence'][first]['sha256']='0'*64;b=json.dumps(d).encode()
        def corrupt(p):return b if p==c.RECEIPT else real(p)
        with patch.object(Path,'read_bytes',corrupt),self.assertRaisesRegex(ValueError,'Immutable receipt'):c.validate()
if __name__=='__main__':unittest.main()
