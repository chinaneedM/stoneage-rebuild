import struct
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_spr_probe import analyze


class StoneAgeSprProbeTests(unittest.TestCase):
    def test_spreadrn_and_spr_walk(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            spr=root/"spr.bin"
            idx=root/"spradrn.bin"

            # sprite 100000: one animation, two frames
            a0=struct.pack("<HHII",3,4,320,2)
            a0+=struct.pack("<IhhH",10,-1,2,7)
            a0+=struct.pack("<IhhH",11,1,-2,10001)

            # sprite 100001: one animation, one frame
            off1=len(a0)
            a1=struct.pack("<HHII",1,2,160,1)
            a1+=struct.pack("<IhhH",20,0,0,10100)

            spr.write_bytes(a0+a1)
            idx.write_bytes(
                struct.pack("<IIH2x",100000,0,1)+
                struct.pack("<IIH2x",100001,off1,1)
            )

            r=analyze(idx,spr)
            self.assertEqual(r["record_count"],2)
            self.assertEqual(r["remainder"],0)
            self.assertEqual(r["counts"]["parse_success"],2)
            self.assertEqual(r["counts"]["exact_next_offset"],2)
            self.assertEqual(r["animation_total"],2)
            self.assertEqual(r["frame_total"],3)
            self.assertEqual(r["frame_bmp_min"],10)
            self.assertEqual(r["frame_bmp_max"],20)
            self.assertEqual(len(r["failures"]),0)


if __name__=="__main__":
    unittest.main()
