import struct
import unittest

from tools.stoneage_tw10_technical_probe import (
    pe_sections,
    parse_addr_table,
)


class TaiwanV10TechnicalProbeTests(unittest.TestCase):
    def test_parse_address_table(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"x.txt"
            p.write_text("0:4:a.bin 4:2:b.bin\n6:3:c.bin", encoding="utf-8")
            self.assertEqual(
                parse_addr_table(p),
                [(0,4,"a.bin"),(4,2,"b.bin"),(6,3,"c.bin")],
            )

    def test_pe_sections_rejects_non_pe(self):
        self.assertIsNone(pe_sections(b"not pe"))

    def test_pe_sections_minimal_header(self):
        data=bytearray(512)
        data[:2]=b"MZ"
        struct.pack_into("<I",data,0x3C,0x80)
        data[0x80:0x84]=b"PE\0\0"
        struct.pack_into("<HHI",data,0x84,0x14c,0,123)
        struct.pack_into("<H",data,0x94,0)
        r=pe_sections(bytes(data))
        self.assertIsNotNone(r)
        self.assertEqual(r["machine"],0x14c)
        self.assertEqual(r["timestamp"],123)


if __name__=="__main__":
    unittest.main()
