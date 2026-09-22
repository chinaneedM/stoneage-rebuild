import struct
import unittest

from tools.stoneage_japan174a_payload_probe import (
    parse_timemap_link,
    pe_header_summary,
    select_capture_rows,
    signature,
)


class Japan174aPayloadProbeTests(unittest.TestCase):
    def test_timemap_link_normalizes_exact_mementos(self):
        rows=parse_timemap_link(
            (
                '<http://x/sa174hg.exe>; rel="original",\n'
                '<http://web.archive.org/web/20031214010101/'
                'http://x/sa174hg.exe>; rel="first memento"; '
                'datetime="Sun, 14 Dec 2003 01:01:01 GMT",\n'
                '<http://web.archive.org/web/20040102030405id_/'
                'http://x/sa174hg.exe>; rel="last memento"; '
                'datetime="Fri, 02 Jan 2004 03:04:05 GMT"'
            ).encode("utf-8"),
            "http://x/sa174hg.exe",
        )
        self.assertEqual(
            [row["timestamp"] for row in rows],
            ["20031214010101","20040102030405"],
        )
        self.assertTrue(all(row["source"]=="timemap" for row in rows))

    def test_signature_detects_pe(self):
        self.assertEqual(signature(b"MZ"+b"\0"*80),"pe-mz")

    def test_pe_header_summary_reads_minimal_header(self):
        data=bytearray(512)
        data[:2]=b"MZ"
        struct.pack_into("<I",data,0x3C,0x80)
        data[0x80:0x84]=b"PE\0\0"
        struct.pack_into("<HHIIIHH",data,0x84,0x14C,3,1071400000,0,0,224,0x010F)
        struct.pack_into("<H",data,0x98,0x10B)
        data[0x9A]=7
        data[0x9B]=10
        struct.pack_into("<H",data,0x98+68,2)
        out=pe_header_summary(data)
        self.assertTrue(out["complete"])
        self.assertEqual(out["machine"],0x14C)
        self.assertEqual(out["sections"],3)
        self.assertEqual(out["optional_magic"],0x10B)
        self.assertEqual(out["subsystem"],2)

    def test_capture_rows_preserve_timemap_source(self):
        rows=select_capture_rows(
            "http://x/sa174hg.exe",
            [],
            [{
                "timestamp":"20031214010101",
                "status":"200",
                "url":"http://x/sa174hg.exe",
                "source":"timemap",
            }],
        )
        self.assertEqual(rows[0]["source"],"timemap")

    def test_capture_rows_keep_cdx_metadata(self):
        rows=select_capture_rows(
            "http://x/sa174hg.exe",
            [{
                "timestamp":"20031214000000",
                "original":"http://x/sa174hg.exe",
                "statuscode":"200",
                "mimetype":"application/octet-stream",
                "digest":"ABC",
                "length":"123456",
                "redirect":"",
            }],
            [],
        )
        self.assertEqual(rows[0]["digest"],"ABC")
        self.assertEqual(rows[0]["length"],"123456")
        self.assertEqual(rows[0]["source"],"cdx")


if __name__=="__main__":
    unittest.main()
