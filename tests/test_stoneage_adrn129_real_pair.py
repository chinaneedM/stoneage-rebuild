from pathlib import Path
import struct
import tempfile
import gzip
import csv
import hashlib
import unittest
from tools.stoneage_adrn129_real_pair import inspect_rd,pair_qualification,export_pairing


class PairTests(unittest.TestCase):
    def test_exact_header_and_hash_requires_actual_rd_structure(self):
        data=b'RD'+bytes([1,0])+struct.pack('<iiI',10,12,18)+b'ab'
        row={'adder':0,'size':18,'width':10,'height':12}
        result=inspect_rd(data,row,{})
        self.assertEqual(result[0],'HEADER_MATCH')
        self.assertEqual(pair_qualification([1,2],result[0]),'EXACT_NATIVE_RECORD_AND_RD_STRUCTURE')
        self.assertEqual(pair_qualification([],result[0]),'RD_STRUCTURE_ONLY_NO_EXACT_NATIVE_RECORD')

    def test_cache_does_not_hide_dimension_mismatch_or_bounds(self):
        data=b'RD'+bytes([1,0])+struct.pack('<iiI',10,12,18)+b'ab';cache={}
        row={'adder':0,'size':18,'width':10,'height':12}
        self.assertEqual(inspect_rd(data,row,cache)[0],'HEADER_MATCH')
        self.assertEqual(inspect_rd(data,{**row,'width':99},cache)[0],'HEADER_MISMATCH')
        self.assertEqual(inspect_rd(data,{**row,'size':100},cache)[0],'OUT_OF_BOUNDS_OR_SHORT')
        self.assertEqual(inspect_rd(b'XX'+data[2:],row,{})[0],'BAD_RD_MAGIC')
        self.assertEqual(pair_qualification([1],'BAD_RD_MAGIC'),'RD_STRUCTURE_NOT_QUALIFIED')

    def test_all_exact_native_occurrences_survive_duplicate_number(self):
        block=b'RD'+bytes([1,0])+struct.pack('<iiI',10,12,18)+b'ab'
        record=struct.pack('<IIIiiii',1,0,18,0,0,10,12)+bytes(52)
        sha=hashlib.sha256(record).hexdigest()
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'a').write_bytes(record*2);(root/'r').write_bytes(block)
            with gzip.open(root/'patch.gz','wt') as f:
                f.write('index\tbitmapno\tadder\tsize\txoff\tyoff\twidth\theight\trecord_sha256\n0\t1\t0\t18\t0\t0\t10\t12\t'+sha+'\n')
            with gzip.open(root/'base.gz','wt') as f:f.write('bitmapno\trd_block_sha256\n1\t'+hashlib.sha256(block).hexdigest()+'\n')
            result=export_pairing(root/'a',root/'r',root/'patch.gz',root/'out',root/'base.gz')
            self.assertEqual(result['exact_native_match_multiplicity'],{'2':1})
            self.assertEqual(result['native_duplicate_number_occurrences'],1)
            with gzip.open(root/'out/PAIRS-R1.tsv.gz','rt') as f:rows=list(csv.DictReader(f,delimiter='\t'))
            self.assertEqual(rows[0]['native_exact_indices'],'0,1')


if __name__=='__main__':unittest.main()
