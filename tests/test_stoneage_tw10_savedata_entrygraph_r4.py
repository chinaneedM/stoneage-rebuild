import struct
import unittest

from tools.stoneage_tw10_savedata_entrygraph_r4 import (
    explore, MAX_NODES, CANDIDATE_STARTS
)


class OriginalEntrygraphR4Tests(unittest.TestCase):
    BASE = 0x400000
    TEXT = 0x1000

    def inspect(self, data, entry=None, bound=MAX_NODES):
        return explore(data, self.TEXT, self.BASE,
                       self.TEXT if entry is None else entry,
                       max_nodes=bound)

    def test_direct_jump_reaches_push_but_skips_unused_padding(self):
        # jmp +1 | unused NOP | push absolute | ret
        raw = b"\xeb\x01\x90\x68" + struct.pack("<I", 0x463634) + b"\xc3"
        graph = self.inspect(raw)
        self.assertEqual(set(graph["visited"]), {0x1000, 0x1003, 0x1008})
        self.assertIn((0x1000, 0x1003), graph["edges"])
        self.assertNotIn(0x1002, graph["visited"])
        self.assertFalse(graph["limit_hit"])

    def test_ret_blocks_false_fallthrough_and_does_not_prove_data(self):
        raw = b"\xc3\x68" + struct.pack("<I", 0x463634) + b"\xc3"
        graph = self.inspect(raw)
        self.assertEqual(set(graph["visited"]), {self.TEXT})

    def test_indirect_jump_stops_without_inventing_target(self):
        graph = self.inspect(b"\xff\xe0\x90\xc3")
        self.assertEqual(set(graph["visited"]), {self.TEXT})
        self.assertEqual(graph["statistics"]["indirect_transfer"], 1)

    def test_call_has_target_and_fallthrough_candidates(self):
        # call 0x1007; nop; ret; ret
        raw = b"\xe8\x02\x00\x00\x00\x90\xc3\xc3"
        graph = self.inspect(raw)
        self.assertEqual(set(graph["visited"]), {0x1000, 0x1005, 0x1006, 0x1007})
        self.assertIn((0x1000, 0x1007), graph["edges"])
        self.assertIn((0x1000, 0x1005), graph["edges"])

    def test_self_loop_terminates_by_visited_address(self):
        graph = self.inspect(b"\xeb\xfe")
        self.assertEqual(set(graph["visited"]), {self.TEXT})
        self.assertIn((self.TEXT, self.TEXT), graph["edges"])
        self.assertFalse(graph["limit_hit"])

    def test_outside_text_entrypoint_does_not_generate_evidence(self):
        graph = self.inspect(b"\x90\xc3", entry=0x900)
        self.assertFalse(graph["entry_in_text"])
        self.assertEqual(graph["visited"], {})
        self.assertFalse(graph["limit_hit"])

    def test_node_bound_is_explicit_not_inferred_exhaustion(self):
        graph = self.inspect(b"\x90"*30+b"\xc3", bound=3)
        self.assertTrue(graph["limit_hit"])
        self.assertEqual(len(graph["visited"]), 3)

    def test_reject_invalid_node_bounds(self):
        for value in (0, MAX_NODES+1, -1):
            with self.assertRaisesRegex(ValueError, "bound"):
                self.inspect(b"\xc3", bound=value)

    def test_original_candidate_offsets_are_specific_and_stable(self):
        self.assertEqual(tuple(hex(x) for x in CANDIDATE_STARTS),
                         ("0x40064","0x400e4","0x40115","0x402a0"))


if __name__ == "__main__":
    unittest.main()
