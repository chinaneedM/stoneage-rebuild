import copy
import json
import struct
import unittest
from tools.stoneage_adrn129_real_archive import DIR, contract, structural_status
from tools.stoneage_rd_codec import decode_rd_block


class ArchiveTests(unittest.TestCase):
    def test_raw_size_exception_follows_existing_decoder(self):
        block=b'RD'+bytes([0,0])+struct.pack('<iiI',4,2,24+8621844)+b'12345678'
        row={'adder':0,'size':24,'width':4,'height':2,'rd_width':4,'rd_height':2,'rd_size':24+8621844,
            'rd_flag':0,'rd_status':'HEADER_MISMATCH','rd_sha256':'a'*64}
        self.assertEqual(decode_rd_block(block,24)[1],b'12345678')
        self.assertEqual(structural_status(row,24),'RAW_FLAG0_ADRN_SIZE_AUTHORITATIVE')
        for mutation in ({'width':3},{'size':23},{'rd_flag':1},{'rd_status':'BAD_RD_MAGIC'},{'adder':1},{'rd_sha256':''}):
            with self.subTest(mutation=mutation):self.assertEqual(structural_status({**row,**mutation},24),'NOT_QUALIFIED')

    def test_contract_rejects_promotions_and_wrong_source(self):
        report=json.loads((DIR/'REPORT-R1.json').read_bytes());contract(report)
        mutations=[('schema','wrong'),('task','wrong'),('tables',{}),('containers',{})]
        for key in report['boundaries']:
            changed=copy.deepcopy(report);changed['boundaries'][key]=True
            with self.subTest(boundary=key),self.assertRaises(ValueError):contract(changed)
        for key,value in mutations:
            changed=copy.deepcopy(report);changed[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):contract(changed)
        changed=copy.deepcopy(report);changed['source_pins'].pop(next(iter(changed['source_pins'])))
        with self.assertRaises(ValueError):contract(changed)


if __name__=='__main__':unittest.main()
