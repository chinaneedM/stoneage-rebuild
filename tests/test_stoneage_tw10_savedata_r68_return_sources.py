import unittest

from tools.stoneage_tw10_savedata_r68_return_sources import reverse_sources, forward_sources, inspect_raw


def row(at, writes=(), op="nop"):
    return {"site_rva": at, "mnemonic": op, "decoder_written_registers": list(writes)}


class R68Tests(unittest.TestCase):
    def test_unpinned_source_never_becomes_historical_evidence(self):
        with self.assertRaises(ValueError):
            inspect_raw(b'{}')

    def check(self, nodes, edges, rows, want):
        self.assertEqual(reverse_sources(nodes, edges, rows, min(nodes), max(nodes)), want)
        self.assertEqual(forward_sources(nodes, edges, rows, min(nodes), max(nodes)), want)

    def test_full_definition(self):
        self.check({1, 2, 3}, {(1, 2), (2, 3)}, {1: row(1), 2: row(2, ["eax"])}, {("full_eax_definition", 2)})

    def test_partial_write_does_not_define_full_original_value(self):
        self.check({1, 2, 3}, {(1, 2), (2, 3)}, {1: row(1), 2: row(2, ["al"])}, {("partial_eax_unknown", 2)})

    def test_opaque_call_kills_even_if_decoder_only_reports_esp(self):
        self.check({1, 2, 3}, {(1, 2), (2, 3)}, {1: row(1, ["eax"]), 2: row(2, ["esp"], "call")}, {("opaque_call", 2)})

    def test_undecoded_instruction_is_not_noop(self):
        self.check({1, 2, 3}, {(1, 2), (2, 3)}, {1: row(1, ["eax"])}, {("unknown_instruction", 2)})

    def test_merge_preserves_alternatives(self):
        self.check({1, 2, 3, 4}, {(1, 2), (1, 3), (2, 4), (3, 4)},
                   {1: row(1), 2: row(2, ["eax"]), 3: row(3, ["esp"], "call")},
                   {("full_eax_definition", 2), ("opaque_call", 3)})

    def test_cycle_fixed_point(self):
        self.check({1, 2, 3, 4}, {(1, 2), (2, 3), (3, 2), (3, 4)},
                   {1: row(1, ["eax"]), 2: row(2), 3: row(3)}, {("full_eax_definition", 1)})

    def test_new_definition_in_cycle(self):
        self.check({1, 2, 3, 4}, {(1, 2), (2, 3), (3, 2), (2, 4)},
                   {1: row(1, ["eax"]), 2: row(2), 3: row(3, ["eax"])},
                   {("full_eax_definition", 1), ("full_eax_definition", 3)})

    def test_pop_other_register_does_not_kill_eax(self):
        self.check({1, 2, 3}, {(1, 2), (2, 3)}, {1: row(1, ["eax"]), 2: row(2, ["edi", "esp"], "pop")},
                   {("full_eax_definition", 1)})

    def test_unknown_entry_preserved(self):
        self.check({1, 2, 3}, {(1, 2), (2, 3)}, {1: row(1), 2: row(2)}, {("unknown_entry", 1)})


if __name__ == "__main__":
    unittest.main()
