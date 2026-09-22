import struct
import unittest

from tools.stoneage_japan174a_exact_install_probe import (
    dos_timestamp,
    interesting_html_refs,
    parse_cab,
    select_snapshots,
    signature,
    url_variants,
)


class Japan174aExactInstallProbeTests(unittest.TestCase):
    def test_signature_distinguishes_cab_and_html(self):
        self.assertEqual(signature(b"MSCF"+b"\x00"*40),"cab-mscf")
        self.assertEqual(signature(b"<HTML><BODY>"),"html")

    def test_url_variants_toggle_explicit_port_80(self):
        rows=url_variants("http://www.hangame.co.jp:80/publish/sa/HgSA.cab")
        self.assertIn("http://www.hangame.co.jp:80/publish/sa/HgSA.cab",rows)
        self.assertIn("http://www.hangame.co.jp/publish/sa/HgSA.cab",rows)

    def test_html_reference_extraction_keeps_install_chain_targets(self):
        body=(
            b'<object codebase="HgSA.cab#version=1,2,3,4"></object>'
            b'<a href="sasetup2.asp">next</a>'
        )
        refs=interesting_html_refs(body)
        self.assertTrue(any("HgSA.cab" in row for row in refs))
        self.assertIn("sasetup2.asp",refs)

    def test_parse_minimal_cab_member_table(self):
        name=b"HgSA.dll\x00"
        file_row=struct.pack(
            "<IIHHHH",
            1234,
            0,
            0,
            ((2003-1980)<<9)|(12<<5)|15,
            (9<<11)|(30<<5),
            0x20,
        )+name
        total=36+len(file_row)
        header=struct.pack(
            "<4sIIIII BBHHHHH",
            b"MSCF",0,total,0,36,0,3,1,0,1,0,0,0
        )
        parsed=parse_cab(header+file_row)
        self.assertEqual(parsed["claimed_size"],total)
        self.assertEqual(parsed["files"],1)
        self.assertTrue(parsed["member_table_complete"])
        self.assertEqual(parsed["members"][0]["name"],"HgSA.dll")
        self.assertEqual(parsed["members"][0]["size"],1234)
        self.assertEqual(parsed["members"][0]["timestamp"],"2003-12-15T09:30:00")

    def test_snapshot_selection_prefers_earliest_unique_captures(self):
        rows=[
            {"timestamp":"20040428000000","original":"http://x/HgSA.cab","statuscode":"200"},
            {"timestamp":"20031215000000","original":"http://x/HgSA.cab","statuscode":"200"},
        ]
        selected=select_snapshots(rows,[])
        self.assertEqual(selected[0]["timestamp"],"20031215000000")

    def test_dos_timestamp_rejects_invalid_month(self):
        self.assertEqual(dos_timestamp(0,0),"")


if __name__=="__main__":
    unittest.main()
