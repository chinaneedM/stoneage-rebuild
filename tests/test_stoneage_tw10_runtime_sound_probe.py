import struct
import unittest

from tools.stoneage_tw10_runtime_sound_probe import parse_wave, first_diff, common_prefix, common_suffix


class RuntimeSoundProbeTests(unittest.TestCase):
    def make_wave(self,payload=b"\x01\x02\x03\x04"):
        fmt=struct.pack("<HHIIHH",1,1,22050,44100,2,16)
        body=b"fmt "+struct.pack("<I",len(fmt))+fmt+b"data"+struct.pack("<I",len(payload))+payload
        return b"RIFF"+struct.pack("<I",4+len(body))+b"WAVE"+body

    def test_parse_wave(self):
        data=self.make_wave()
        r=parse_wave(data)
        self.assertTrue(r["riff"])
        self.assertEqual(r["fmt_channels"],1)
        self.assertEqual(r["fmt_sample_rate"],22050)
        self.assertEqual(r["fmt_bits_per_sample"],16)
        self.assertEqual(r["data_size"],4)

    def test_diff_helpers(self):
        self.assertEqual(first_diff(b"abc",b"abd"),2)
        self.assertEqual(first_diff(b"abc",b"abc"),-1)
        self.assertEqual(common_prefix(b"abc",b"abd"),2)
        self.assertEqual(common_suffix(b"xbc",b"ybc"),2)


if __name__=="__main__":
    unittest.main()
