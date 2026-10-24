import copy
import json
from pathlib import Path
import tempfile
import gzip
import csv
import unittest
from tools.stoneage_wayi_adrn129_archive import DIR, contract, replay_rows
from tools.stoneage_wayi_adrn129_payload import export_index
from tests.test_stoneage_wayi_adrn129_payload import record


class ArchiveTests(unittest.TestCase):
    def test_full_current_contract_and_semantic_mutations(self):
        source=json.loads((DIR/'REPORT-R1.json').read_bytes());contract(source)
        changes=[lambda r:r['boundaries'].__setitem__('named_pet_npc_identity_proven',True),
          lambda r:r['boundaries'].__setitem__('original_real_pixel_blocks_verified',True),
          lambda r:r.__setitem__('source_capture','2005-05-18'),
          lambda r:r.__setitem__('source_role','OFFICIAL_CLEAN_80_FULL_CLIENT'),
          lambda r:r['indexes'][0].__setitem__('records',389670),
          lambda r:r['indexes'][0].__setitem__('duplicate_bitmap_occurrences',0),
          lambda r:r['indexes'][0].__setitem__('derived_table','../raw.bin'),
          lambda r:r['members'][0].__setitem__('sha256','0'*64),
          lambda r:r['source_pins'].clear()]
        for i,change in enumerate(changes):
            value=copy.deepcopy(source);change(value)
            with self.subTest(case=i),self.assertRaises(ValueError):contract(value)

    def test_exact_row_replay_preserves_duplicate_order_and_rejects_mutation(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'index.gz';export_index(record()+record(address=18),path,{})
            with gzip.open(path,'rt') as f:rows=list(csv.DictReader(f,delimiter='\t'))
            metrics,extra=replay_rows(rows,{})
            self.assertEqual(metrics['duplicate_bitmap_occurrences'],1)
            self.assertEqual(extra['duplicate_positions'],[{'index':1,'bitmapno':1}])
            for key,value in [('adder','42'),('outpoison','1'),('index','9'),('record_sha256','0'*64)]:
                changed=copy.deepcopy(rows);changed[0][key]=value
                with self.subTest(key=key),self.assertRaises(ValueError):replay_rows(changed,{})


if __name__=='__main__':unittest.main()
