import tempfile
import unittest
from pathlib import Path
import struct
from tools.stoneage_tw10_cn50_record_resource_diff import parse_adrn, parse_spr, compare_id_rows


class RecordSourceDiffTest(unittest.TestCase):
    def test_adrn_real_record_digests_include_payload_not_offset_only(self):
        with tempfile.TemporaryDirectory() as d:
            r=Path(d)
            payload=b"RD\x00\x00"+struct.pack("<III",1,1,20)+b"test"
            (r/"real.bin").write_bytes(b"\x00"*5+payload)
            rec=struct.pack("<IIIiiii",777,5,len(payload),0,0,1,1)+bytes(52)
            (r/"adrn.bin").write_bytes(rec)
            row=parse_adrn(r/"adrn.bin",r/"real.bin")
            self.assertEqual(row["valid_payload_rows"],1)
            self.assertEqual(row["rows"][0]["id"],777)
            (r/"real.bin").write_bytes(b"\x00"*5+payload[:-1]+b"X")
            changed=parse_adrn(r/"adrn.bin",r/"real.bin")
            a=compare_id_rows(row["rows"],changed["rows"],"adrn")
            self.assertEqual(a["changed_payload_or_segment_count"],1)

    def test_adrn_truncated_record_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            (p/"adrn.bin").write_bytes(b"\x00"*81)
            (p/"real.bin").write_bytes(b"a")
            with self.assertRaises(ValueError):
                parse_adrn(p/"adrn.bin",p/"real.bin")

    def test_spr_semantic_and_segment_hash(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            frame=struct.pack("<IhhH",5,0,0,1)
            seg=struct.pack("<HHII",0,1,5,1)+frame
            (p/"spr.bin").write_bytes(seg)
            (p/"spradrn.bin").write_bytes(struct.pack("<IIH",100001,0,1)+bytes(2))
            got=parse_spr(p/"spradrn.bin",p/"spr.bin")
            self.assertEqual((got["valid_segments"],got["rows"][0]["frame_count"]),(1,1))
            self.assertTrue(got["rows"][0]["exact_segment_span"])
            (p/"spr.bin").write_bytes(seg[:-1]+b"\x22")
            other=parse_spr(p/"spradrn.bin",p/"spr.bin")
            self.assertEqual(compare_id_rows(got["rows"],other["rows"],"spr")["exact_payload_or_segment_count"],0)

    def test_duplicates_do_not_prove_identity(self):
        def entry(n,hash):
            return {"id":n,"index":n,"payload_sha256":hash,"raw_sha256":hash,
                    "geometry":[0,0,1,1],"size":16}
        x=compare_id_rows([entry(10,"a"),entry(10,"a"),entry(11,"b")],
                          [entry(10,"a"),entry(11,"b"),entry(12,"c")],"adrn")
        self.assertEqual(x["ambiguous_shared_id_count"],1)
        self.assertEqual(x["common_unique_id_count"],1)
        self.assertEqual(x["new_unique_ids_absent_in_old_count"],1)
        self.assertEqual(x["exact_payload_or_segment_count"],1)
        self.assertEqual(x["old_unique_ids_absent_in_new_count"],0)

    def test_trailing_spr_data_is_reported_not_inflated(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            (p/"spr.bin").write_bytes(struct.pack("<HHII",0,1,0,0)+b"EXTRA")
            (p/"spradrn.bin").write_bytes(struct.pack("<IIH",100001,0,1)+bytes(2))
            got=parse_spr(p/"spradrn.bin",p/"spr.bin")
            self.assertEqual(got["problems"].get("trailing_segment_bytes"),1)
            self.assertFalse(got["rows"][0]["exact_segment_span"])
