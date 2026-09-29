import unittest

from tools.stoneage_shadowed_branch_warpman_free_probe import (
    parse_free_grammar,
)


class ShadowedBranchWarpManFreeProbeTests(unittest.TestCase):

    def test_free_grammar_preserves_or_and_operator_key_structure_only(self):
        clauses = parse_free_grammar(
            b"LV>10&ENDEV=123,ITEM=456*2,TRANS!=7"
        )
        self.assertEqual(len(clauses), 3)
        self.assertEqual(
            [(atom.key, atom.operator) for atom in clauses[0].atoms],
            [("LV", ">"), ("ENDEV", "=")],
        )
        self.assertEqual(clauses[1].atoms[0].key, "ITEM")
        self.assertEqual(clauses[1].atoms[0].special_reduce, "STAR")
        self.assertEqual(clauses[2].atoms[0].operator, "!=")

    def test_new_warpman_temp_suffix_is_not_part_of_condition_key(self):
        clauses = parse_free_grammar(b"PET-3=100")
        self.assertEqual(clauses[0].atoms[0].key, "PET")


if __name__ == "__main__":
    unittest.main()
