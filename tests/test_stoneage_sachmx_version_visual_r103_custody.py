import copy
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from tools import stoneage_sachmx_version_visual_r103_custody as c

class Custody(unittest.TestCase):
    def test_real_immutable_custody(self):
        result=c.validate()
        self.assertEqual(result['actual_source_runs'],25)
        self.assertTrue(result['raw_candidate_main_local_equal'])
        self.assertFalse(result['original_software_executed'])

    def test_changed_ci_report_even_with_same_length_is_rejected(self):
        receipt=json.loads(c.RECEIPT.read_text());target=c.ROOT/receipt['artifacts'][0]['path'];real=Path.read_bytes
        def corrupt(path):
            raw=real(path)
            return raw[:-1]+b' ' if path==target else raw
        with patch.object(Path,'read_bytes',corrupt),self.assertRaisesRegex(ValueError,'Evidence identity'):
            c.validate()

    def test_receipt_cannot_reroute_or_relabel_the_actual_source(self):
        receipt=json.loads(c.RECEIPT.read_text())
        for key,value in [('source_commit','0'*40),('raw_candidate_main_local_equal',False),('software_executed',True)]:
            altered=copy.deepcopy(receipt);altered[key]=value
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'Mutated receipt'):
                c.validate(altered)
        for key,value in [('artifact',0),('zip_sha256','0'*64),('raw_sha256','0'*64),('download_route','CONNECTOR_METADATA_JSON_WAS_ZIP')]:
            altered=copy.deepcopy(receipt);altered['artifacts'][0][key]=value
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'Mutated receipt'):
                c.validate(altered)

    def test_receipt_hash_and_evidence_repin_cannot_hide_changes(self):
        original=c.RECEIPT.read_bytes();receipt=json.loads(original)
        first=next(iter(receipt['evidence']));receipt['evidence'][first]['sha256']='0'*64
        forged=json.dumps(receipt).encode();real=Path.read_bytes
        def changed(path):return forged if path==c.RECEIPT else real(path)
        with patch.object(Path,'read_bytes',changed),self.assertRaisesRegex(ValueError,'Immutable receipt'):
            c.validate()

if __name__=='__main__':unittest.main()
