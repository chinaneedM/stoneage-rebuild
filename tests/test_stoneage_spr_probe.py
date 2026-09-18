import struct
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_spr_probe import analyze


def adrn_record(bitmapno):
    return struct.pack("<I", bitmapno) + bytes(76)


class StoneAgeSprProbeTests(unittest.TestCase):
    def test_spreadrn_spr_and_adrn_crosscheck(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            spr=root/"spr.bin"
            idx=root/"spradrn.bin"
            adrn=root/"adrn.bin"

            a0=struct.pack("<HHII",3,4,320,3)
            a0+=struct.pack("<IhhH",10,-1,2,7)
            a0+=struct.pack("<IhhH",11,1,-2,10001)
            a0+=struct.pack("<IhhH",0xFFFFFFFF,0,0,0)

            off1=len(a0)
            a1=struct.pack("<HHII",1,2,160,1)
            a1+=struct.pack("<IhhH",20,0,0,10100)

            spr.write_bytes(a0+a1)
            idx.write_bytes(
                struct.pack("<IIH2x",100000,0,1)+
                struct.pack("<IIH2x",100001,off1,1)
            )
            adrn.write_bytes(adrn_record(10)+adrn_record(11)+adrn_record(20))

            r=analyze(idx,spr,adrn)
            self.assertEqual(r["record_count"],2)
            self.assertEqual(r["remainder"],0)
            self.assertEqual(r["counts"]["parse_success"],2)
            self.assertEqual(r["counts"]["exact_next_offset"],2)
            self.assertEqual(r["animation_total"],2)
            self.assertEqual(r["frame_total"],4)
            self.assertEqual(r["bitmap_classes"]["direct_adrn_bitmap_match"],3)
            self.assertEqual(r["bitmap_classes"]["sentinel_ffffffff"],1)
            self.assertEqual(len(r["failures"]),0)


if __name__=="__main__":
    unittest.main()
