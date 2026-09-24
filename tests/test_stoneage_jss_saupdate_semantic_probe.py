import struct
import unittest

from tools.stoneage_jss_saupdate_semantic_probe import (
    find_fixed_file_info,
    section_flags,
    string_table_values,
    utf16_runs,
    version_tuple,
)


class JssSaUpdateSemanticProbeTests(unittest.TestCase):
    def test_version_tuple(self):
        self.assertEqual(version_tuple(0x00010002,0x00030004),(1,2,3,4))

    def test_fixed_file_info(self):
        fields=[
            0xFEEF04BD,0x00010000,0x00010000,0x00000001,
            0x00010000,0x00000001,0x3f,0,0x40004,1,0,0,0,
        ]
        blob=b"xx"+struct.pack("<13I",*fields)+b"yy"
        out=find_fixed_file_info(blob)
        self.assertEqual(version_tuple(out["file_version_ms"],out["file_version_ls"]),(1,0,0,1))
        self.assertEqual(out["file_type"],1)

    def test_utf16_runs_keeps_japanese(self):
        blob="SaUpdate\x00更新開始\x00".encode("utf-16le")
        vals=utf16_runs(blob,2)
        self.assertIn("SaUpdate",vals)
        self.assertIn("更新開始",vals)

    def test_string_table(self):
        parts=[]
        for i in range(16):
            text="Hello" if i==2 else ""
            raw=text.encode("utf-16le")
            parts.append(struct.pack("<H",len(text))+raw)
        vals=string_table_values(b"".join(parts),7)
        self.assertEqual(vals,((98,"Hello"),))

    def test_section_flags(self):
        vals=section_flags(0xC0000040)
        self.assertIn("INIT_DATA",vals)
        self.assertIn("READ",vals)
        self.assertIn("WRITE",vals)


if __name__=="__main__":
    unittest.main()
