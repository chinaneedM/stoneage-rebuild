import struct
import unittest

from tools.stoneage_tw10_savedata_entrygraph_r4 import explore
from tools.stoneage_tw10_savedata_callsite_r5 import (
    shortest_paths, predecessor_summary, file_api_candidates,
    MAX_FWD_NODES, MAX_FWD_RVA_SPAN,
)

BASE = 0x400000
RVA = 0x1000
IAT = 0x403000


def graph(data):
    return explore(data, RVA, BASE, RVA)


class TestR5StaticAudit(unittest.TestCase):
    def test_entrypoint_candidate_sequential_predecessor(self):
        # nop -> push immediate -> ret
        blob = b"\x90\x68" + struct.pack("<I", 0x463634) + b"\xc3"
        g = graph(blob)
        summary = predecessor_summary(0x1001, g["visited"], g["edges"])
        self.assertEqual(summary, {
            "incoming_total":1,
            "incoming_sequential":1,
            "incoming_branch":0,
        })
        self.assertEqual(shortest_paths(g["edges"], RVA)[0x1001], 1)

    def test_direct_jmp_predecessor_not_confused_with_fallthrough(self):
        # jump 0x1003; unused nop; push imm; ret
        blob = b"\xeb\x01\x90\x68" + struct.pack("<I", 0x463634) + b"\xc3"
        g = graph(blob)
        summary = predecessor_summary(0x1003, g["visited"], g["edges"])
        self.assertEqual(summary["incoming_total"], 1)
        self.assertEqual(summary["incoming_branch"], 1)
        self.assertEqual(summary["incoming_sequential"], 0)

    def test_same_path_direct_IAT_call_is_only_lexical_evidence(self):
        blob = (b"\x68" + struct.pack("<I", 0x463634)
                + b"\xff\x15" + struct.pack("<I", IAT) + b"\xc3")
        g = graph(blob)
        result = file_api_candidates(blob, BASE, RVA, g, RVA,
                                     {IAT:("KERNEL32.dll","CreateFileA")})
        self.assertEqual(result["api_counts"], {"CreateFileA":1})
        self.assertTrue(result["createfilea_lexical_present"])
        self.assertEqual(result["visited_local"],3)
        self.assertFalse(result["limit_hit"])
        self.assertEqual(result["api_events"][0]["rva"], "0x1005")

    def test_nonfile_api_not_admitted(self):
        blob = (b"\x68" + struct.pack("<I", 0x463634)
                + b"\xff\x15" + struct.pack("<I", IAT) + b"\xc3")
        g = graph(blob)
        result = file_api_candidates(blob,BASE,RVA,g,RVA,
                                     {IAT:("KERNEL32.dll","GetTickCount")})
        self.assertEqual(result["api_events"],[])
        self.assertFalse(result["createfilea_lexical_present"])

    def test_not_graph_reachable_site_ignored_even_with_push_bytes(self):
        blob = b"\xc3\x68" + struct.pack("<I", 0x463634) + b"\xc3"
        result = file_api_candidates(blob,BASE,RVA,graph(blob),0x1001,{})
        self.assertEqual(result["visited_local"],0)
        self.assertFalse(result["createfilea_lexical_present"])

    def test_ret_blocks_false_api_path(self):
        blob = (b"\x68" + struct.pack("<I", 0x463634)
                + b"\xc3\xff\x15" + struct.pack("<I", IAT))
        result = file_api_candidates(blob,BASE,RVA,graph(blob),RVA,
                                     {IAT:("KERNEL32.dll","ReadFile")})
        self.assertEqual(result["api_counts"],{})

    def test_conditional_branch_is_possible_not_proven_runtime(self):
        # push; jz +1; nop; call [IAT]; ret
        blob = (b"\x68" + struct.pack("<I", 0x463634)
                + b"\x74\x01\x90\xff\x15" + struct.pack("<I", IAT)
                + b"\xc3")
        result=file_api_candidates(blob,BASE,RVA,graph(blob),RVA,
                                   {IAT:("KERNEL32.dll","WriteFile")})
        self.assertEqual(result["api_counts"],{"WriteFile":1})

    def test_region_and_node_limits(self):
        blob = b"\x90"*40 + b"\xc3"
        g=graph(blob)
        result=file_api_candidates(blob,BASE,RVA,g,RVA,{},max_nodes=4)
        self.assertTrue(result["limit_hit"])
        self.assertEqual(result["visited_local"],4)
        for kwargs in ({"max_nodes":0},
                       {"max_nodes":MAX_FWD_NODES+1},
                       {"span":0},
                       {"span":MAX_FWD_RVA_SPAN+1}):
            with self.subTest(kwargs=kwargs):
                with self.assertRaisesRegex(ValueError,"bounds"):
                    file_api_candidates(blob,BASE,RVA,g,RVA,{},**kwargs)

    def test_predecessor_same_fallthrough_when_explicit_edge(self):
        decoded={0x1000:2,0x1002:5}
        edges={(0x1000,0x1002)}
        self.assertEqual(predecessor_summary(0x1002,decoded,edges),
                         {"incoming_total":1,"incoming_sequential":1,"incoming_branch":0})


if __name__=="__main__":
    unittest.main()
