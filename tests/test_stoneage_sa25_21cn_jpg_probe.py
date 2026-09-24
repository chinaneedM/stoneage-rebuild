import struct
import unittest

from tools.stoneage_sa25_21cn_jpg_probe import jpeg_metadata


def segment(marker,payload):
    return bytes([0xFF,marker])+struct.pack(">H",len(payload)+2)+payload


class SA25JpgProbeTests(unittest.TestCase):
    def test_minimal_jpeg_metadata(self):
        jfif=b"JFIF\x00"+bytes([1,2,1])+struct.pack(">HH",72,72)+b"\x00\x00"
        sof=bytes([8])+struct.pack(">HH",120,320)+bytes([3])+b"\x01\x11\x00\x02\x11\x00\x03\x11\x00"
        data=b"\xff\xd8"+segment(0xE0,jfif)+segment(0xFE,b"hello")+segment(0xC0,sof)+b"\xff\xda\x00\x02"
        m=jpeg_metadata(data)
        self.assertEqual((m["width"],m["height"]),(320,120))
        self.assertEqual(m["bits"],8)
        self.assertEqual(m["components"],3)
        self.assertEqual(m["comments"],("hello",))
        self.assertEqual(m["jfif"]["xdensity"],72)

    def test_reject_non_jpeg(self):
        with self.assertRaises(ValueError):
            jpeg_metadata(b"not-jpeg")


if __name__=="__main__":
    unittest.main()
