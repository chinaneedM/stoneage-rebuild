import copy
import json
import unittest

from tools.stoneage_tw10_savedata_callsite_r5_guard import validate
from tools.stoneage_tw10_savedata_instruction_probe import (
    RUNTIME_SHA256, SAVEDATA_SHA256, WORD_RVAS
)


def document():
    return {
        "schema":"stoneage-tw10-savedata-r5-static-api-neighborhood",
        "status":"PINNED_ORIGINAL_STATIC_SURFACE_NOT_NATIVE_IO",
        "original_runtime_sha256":RUNTIME_SHA256,
        "original_savedata_sha256":SAVEDATA_SHA256,
        "entry_rva":"0x4980a",
        "r4_graph_nodes":31665,
        "r4_graph_edges":35092,
        "r4_graph_limit_hit":False,
        "sites":[{
            "word_rva":f"0x{w:x}",
            "push_candidate_start_rva":f"0x{w-1:x}",
            "entrypoint_graph_min_hops":12,
            "predecessors":{"incoming_total":1,"incoming_sequential":1,
                            "incoming_branch":0},
            "local_graph":{"visited_local":10,"limit_hit":False,
                           "api_events":[],"api_counts":{},
                           "createfilea_lexical_present":False},
            "actual_path_feasibility_proven":False,
            "filename_argument_to_file_api_proven":False,
            "native_read_write_size_proven":False}
            for w in WORD_RVAS],
        "filename_argument_to_CreateFileA_proven":False,
        "ReadFile_WriteFile_buffer_size_proven":False,
        "native_save_io_executed":False,
        "original_bytes_published":False,
    }


def validate_doc(d):
    return validate(json.dumps(d,sort_keys=True))


class TestR5ReportGuard(unittest.TestCase):
    def test_valid_zero_api_original_derived_shape(self):
        result=validate_doc(document())
        self.assertEqual(result["site_count"],4)
        self.assertEqual(result["api_events"],0)
        self.assertFalse(result["native_io_semantics_admitted"])

    def test_valid_file_api_lexical_event_never_promotes_native_io(self):
        d=document()
        s=d["sites"][0]["local_graph"]
        s["api_events"]=[{"rva":"0x40069","api":"CreateFileA","dll":"KERNEL32.dll"}]
        s["api_counts"]={"CreateFileA":1}
        s["createfilea_lexical_present"]=True
        result=validate_doc(d)
        self.assertEqual(result["api_events"],1)
        self.assertTrue(result["sites"][0]["lexical_createfilea"])
        self.assertFalse(result["dataflow_argument_proven"])

    def test_reject_fake_original_hash(self):
        d=document();d["original_runtime_sha256"]="0"*64
        with self.assertRaisesRegex(ValueError,"hashes"):validate_doc(d)

    def test_reject_runtime_claim_flags(self):
        for field in ("r4_graph_limit_hit",
                      "filename_argument_to_CreateFileA_proven",
                      "ReadFile_WriteFile_buffer_size_proven",
                      "native_save_io_executed","original_bytes_published"):
            d=document();d[field]=True
            with self.subTest(field=field),self.assertRaisesRegex(ValueError,"promotion"):
                validate_doc(d)

    def test_reject_site_native_dataflow_promotions(self):
        for field in ("actual_path_feasibility_proven",
                      "filename_argument_to_file_api_proven",
                      "native_read_write_size_proven"):
            d=document();d["sites"][0][field]=True
            with self.subTest(field=field),self.assertRaisesRegex(ValueError,"promotion"):
                validate_doc(d)

    def test_reject_wrong_site_or_order(self):
        d=document();d["sites"]=d["sites"][::-1]
        with self.assertRaisesRegex(ValueError,"word candidate"):validate_doc(d)

    def test_reject_count_divergence(self):
        d=document();d["sites"][0]["predecessors"]["incoming_total"]=4
        with self.assertRaisesRegex(ValueError,"predecessor counts"):validate_doc(d)

    def test_reject_bogus_API_metadata(self):
        d=document()
        s=d["sites"][0]["local_graph"]
        s["api_events"]=[{"rva":"0x40069","api":"VirusCall","dll":"SUSPECT.dll"}]
        s["api_counts"]={"VirusCall":1}
        with self.assertRaisesRegex(ValueError,"API metadata"):validate_doc(d)

    def test_reject_API_count_without_event(self):
        d=document();d["sites"][0]["local_graph"]["api_counts"]={"ReadFile":1}
        with self.assertRaisesRegex(ValueError,"API counts"):validate_doc(d)

    def test_reject_event_outside_bounded_local_range(self):
        d=document()
        s=d["sites"][0]["local_graph"]
        s["api_events"]=[{"rva":"0x42000","api":"ReadFile","dll":"KERNEL32.dll"}]
        s["api_counts"]={"ReadFile":1}
        with self.assertRaisesRegex(ValueError,"outside candidate"):validate_doc(d)

    def test_reject_duplicate_api_rows(self):
        d=document()
        s=d["sites"][0]["local_graph"]
        r={"rva":"0x40069","api":"ReadFile","dll":"KERNEL32.dll"}
        s["api_events"]=[r,r]
        s["api_counts"]={"ReadFile":2}
        with self.assertRaisesRegex(ValueError,"duplicate"):validate_doc(d)

    def test_reject_unknown_field_and_oversize(self):
        d=document();d["raw_pe"]="disallowed"
        with self.assertRaisesRegex(ValueError,"schema"):validate_doc(d)
        with self.assertRaisesRegex(ValueError,"oversized"):
            validate("A"*18001)

    def test_reject_boolean_as_count(self):
        d=document();d["sites"][0]["local_graph"]["visited_local"]=True
        with self.assertRaisesRegex(ValueError,"integer"):validate_doc(d)


if __name__=="__main__":
    unittest.main()
