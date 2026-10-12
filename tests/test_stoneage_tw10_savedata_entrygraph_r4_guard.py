import copy
import json
import unittest

from tools.stoneage_tw10_savedata_entrygraph_r4_guard import (
    validate, RUNTIME_SHA, SAVEDATA_SHA, WORDS, STARTS
)


def sample():
    return {
        "schema":"tw10-savedata-four-word-entrygraph-r4",
        "scope":"verified-original-bytes-bounded-entrypoint-direct-graph",
        "runtime_sha256":RUNTIME_SHA,
        "savedata_sha256":SAVEDATA_SHA,
        "entry_rva":"0x1000",
        "text_rva":"0x1000",
        "text_raw_size":327680,
        "entry_in_text":True,
        "graph_limit_hit":False,
        "graph_statistics":{
            "decoded_nodes":42,"direct_or_fallthrough_edges":41,
            "indirect_transfer":2,"terminal_instruction":1,
            "pending_at_stop":0},
        "sites":[{
            "word_rva":w,
            "push_candidate_start_rva":s,
            "entrypoint_graph_candidate_seen":False,
            "entrypoint_graph_word_overlap_count":0,
            "entrypoint_graph_incoming_edges":0,
            "independently_proven_executed_code":False,
            "data_ownership_proven":False}
                 for w,s in zip(WORDS,STARTS)],
        "original_runtime_reachability_admitted":False,
        "savedata_io_semantics_admitted":False,
        "fixed_128_byte_schema_admitted":False,
        "original_bytes_published":False,
    }


def check(v):
    return validate(json.dumps(v,sort_keys=True))


class EntrygraphR4GuardTests(unittest.TestCase):
    def test_valid_empty_candidate_observation_does_not_claim_data(self):
        result=check(sample())
        self.assertEqual(result["observed_candidate_starts"],0)
        self.assertFalse(result["actual_data_ownership_proven"])

    def test_valid_observed_candidate_is_not_executed_claim(self):
        v=sample()
        v["sites"][0]["entrypoint_graph_candidate_seen"]=True
        v["sites"][0]["entrypoint_graph_word_overlap_count"]=1
        v["sites"][0]["entrypoint_graph_incoming_edges"]=1
        result=check(v)
        self.assertEqual(result["observed_candidate_starts"],1)
        self.assertFalse(result["native_runtime_proven"])

    def test_source_hash_rejection(self):
        v=sample();v["runtime_sha256"]="0"*64
        with self.assertRaisesRegex(ValueError,"hash identity"):check(v)

    def test_unrecognized_extra_fields_rejected(self):
        v=sample();v["raw_disassembly"]="unsafe"
        with self.assertRaisesRegex(ValueError,"schema"):check(v)

    def test_runtime_semantics_cannot_be_promoted(self):
        for key in ("original_runtime_reachability_admitted",
                    "savedata_io_semantics_admitted","fixed_128_byte_schema_admitted",
                    "original_bytes_published"):
            v=sample();v[key]=True
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,"promotion"):
                check(v)

    def test_candidate_ownership_promotion_rejected(self):
        v=sample();v["sites"][0]["data_ownership_proven"]=True
        with self.assertRaisesRegex(ValueError,"ownership"):check(v)

    def test_site_graph_count_must_fit_total(self):
        v=sample();v["sites"][1]["entrypoint_graph_incoming_edges"]=42
        with self.assertRaisesRegex(ValueError,"totals"):check(v)

    def test_observed_start_requires_overlap(self):
        v=sample();v["sites"][0]["entrypoint_graph_candidate_seen"]=True
        with self.assertRaisesRegex(ValueError,"overlap"):check(v)

    def test_outside_entrypoint_requires_absence(self):
        v=sample()
        v["entry_rva"]="0x900"
        v["entry_in_text"]=False
        v["graph_statistics"]={"entry_outside_text":1}
        result=check(v)
        self.assertFalse(result["entry_in_text"])
        v["sites"][0]["entrypoint_graph_word_overlap_count"]=1
        with self.assertRaisesRegex(ValueError,"totals|outside"):check(v)

    def test_bad_entry_section_relation_rejected(self):
        v=sample();v["entry_in_text"]=False
        with self.assertRaisesRegex(ValueError,"entry/text"):check(v)

    def test_missing_or_reordered_original_word_rejected(self):
        v=sample();v["sites"]=list(reversed(v["sites"]))
        with self.assertRaisesRegex(ValueError,"candidate site"):check(v)

    def test_oversized_or_unknown_stats_rejected(self):
        v=sample();v["graph_statistics"]["stray_original_code"]="0x90"
        with self.assertRaisesRegex(ValueError,"statistics"):check(v)
        with self.assertRaisesRegex(ValueError,"oversized"):
            validate("a"*9001)

    def test_bools_not_valid_integer_counts(self):
        v=sample();v["graph_statistics"]["decoded_nodes"]=True
        with self.assertRaisesRegex(ValueError,"integer bound"):check(v)


if __name__=="__main__":
    unittest.main()
