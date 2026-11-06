"""Public immutable-source and negative-boundary checks for WORLD34-R2."""
import hashlib
import json
from pathlib import Path
import struct
import unittest

from tools.stoneage_world34_mapped_pe_source import sections, sections_any, reader

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/recovered/STONEAGE-STAGE-A-WORLD34-R2-MAPPED-PE-SOURCE-R1.json"


class World34MappedPEQualification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(REPORT.read_bytes())
        cls.s31=json.loads((ROOT/"research/recovered/STONEAGE-STAGE-A-WORLD31-RECOVERY-SOURCE-R1.json").read_bytes())
        cls.s33=json.loads((ROOT/"research/recovered/STONEAGE-STAGE-A-WORLD33-BATTLE-ITEM-GATE-SOURCE-R1.json").read_bytes())
        cls.s34=json.loads((ROOT/"research/recovered/STONEAGE-STAGE-A-WORLD34-ORIGINAL-FIELD-PATH-SOURCE-R1.json").read_bytes())

    def test_real_prior_blob_pins_and_source_identity(self):
        for path,sha in self.r["source_git_base"]["prior_report_git_blobs"].items():
            raw=(ROOT/path).read_bytes()
            actual=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
            self.assertEqual(actual,sha)
        self.assertEqual(self.r["archive"]["sha256"],self.s33["archive_sha256"])
        self.assertEqual(self.r["archive"]["sha256"],self.s31["archive_sha256"])

    def test_pe_sections_fit_before_coff_cutoff(self):
        p=self.r["pe"]
        s=self.r["gmsv_decompression"]
        self.assertEqual(p["coff_symbol_table_file_offset"],p["last_file_backed_section_end"])
        self.assertLess(p["last_file_backed_section_end"],s["verified_common_output_prefix_bytes"])
        self.assertLess(s["verified_common_output_prefix_bytes"],p["coff_symbol_records_end"])
        self.assertEqual(p["coff_symbol_records_end"],
                         p["coff_symbol_table_file_offset"]+p["coff_symbol_count"]*p["coff_symbol_record_bytes"])
        self.assertEqual([x["name"] for x in p["sections"]],[".text",".data",".rdata",".idata"])
        self.assertEqual([x["raw_end"] for x in p["sections"]],[1419776,1633280,1739264,1742336])
        for x in p["sections"]:
            self.assertEqual(x["raw_end"],x["raw_offset"]+x["raw_bytes"])
            self.assertEqual(len(x["sha256"]),64)
        self.assertTrue(s["libarchive_read_data_crc_error"])
        self.assertFalse(s["full_original_member_validated"])

    def test_exact_code_path_source_sites(self):
        edges=self.r["qualified_code_evidence"]["additional_static_call_sites"]
        self.assertEqual(len(edges),14)
        self.assertEqual([e["role"] for e in edges][0:3],
                         ["field_message_to_item_use","item_callback_pointer_lookup","item_callback_invoke"])
        self.assertEqual([e["destination"] for e in edges][:2],[0x4746e0,0x4f7fb0])
        self.assertEqual(edges[2]["kind"],"indirect")
        self.assertEqual(self.r["qualified_code_evidence"]["indirect_callback_pointer_stack_displacement"],-0x11c)
        self.assertEqual({x["role"]:x["address"] for x in edges}["field_stat_write_call"],0x4fec52)
        self.assertEqual(self.r["qualified_code_evidence"]["item_callback_pointer_lookup_runtime_key"],19)
        self.assertEqual(self.r["qualified_code_evidence"]["recovery_work_state_runtime_key"],0)
        self.assertEqual([self.r["qualified_code_evidence"][k] for k in
                          ["prior_world31_server_windows","prior_world33_server_windows","prior_world33_client_windows"]],[6,12,5])

    def test_original_row_and_boundaries(self):
        rows=self.r["item_original_rows"]
        self.assertEqual([(x["id"],x["argument"],x["fieldtype"],x["target"]) for x in rows],
                         [(1232,"體600",1,2),(12530,"體320",0,1),(12555,"氣20體185",2,1)])
        for x in rows:
            self.assertEqual(hashlib.sha256(x["argument"].encode("cp950")).hexdigest(),x["argument_sha256"])
        for k,v in self.r["boundaries"].items():
            with self.subTest(boundary=k):
                self.assertIs(v,False)

    def test_synthetic_pe_parser_rejects_missing_bytes_and_non_pe(self):
        with self.assertRaises(ValueError):
            sections(b"x"*2048)
        with self.assertRaises(ValueError):
            sections_any(b"x"*2048)
        with self.assertRaises(ValueError):
            reader(b"",[(".text",0x400000,8,0)])(0x500000,0x500004)


if __name__=="__main__":
    unittest.main()
