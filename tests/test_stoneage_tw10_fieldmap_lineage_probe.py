import unittest

from tools.stoneage_tw10_fieldmap_lineage_probe import compare_maps


def row(sha, compatible=True):
    return {
        "sha256": sha,
        "compatible": compatible,
        "width": 10,
        "height": 10,
        "bytes": 608,
        "required_ids": 1,
        "required_cells": 1,
    }


class FieldMapLineageProbeTests(unittest.TestCase):
    def test_classifies_stable_changed_and_unique_paths(self):
        a = {
            "1.dat": row("aaa", True),
            "2.dat": row("bbb", True),
            "3.dat": row("ccc", False),
            "onlya.dat": row("ddd", True),
        }
        b = {
            "1.dat": row("aaa", True),
            "2.dat": row("zzz", True),
            "3.dat": row("ccc", False),
            "onlyb.dat": row("eee", True),
        }
        got = compare_maps(a, b)
        self.assertEqual(got["shared"], ["1.dat", "2.dat", "3.dat"])
        self.assertEqual(got["same"], ["1.dat", "3.dat"])
        self.assertEqual(got["changed"], ["2.dat"])
        self.assertEqual(got["same_compatible_both"], ["1.dat"])
        self.assertEqual(got["changed_compatible_both"], ["2.dat"])
        self.assertEqual(got["only_a"], ["onlya.dat"])
        self.assertEqual(got["only_b"], ["onlyb.dat"])

    def test_compatibility_must_hold_in_both_corpora(self):
        a = {"1.dat": row("same", True)}
        b = {"1.dat": row("same", False)}
        got = compare_maps(a, b)
        self.assertEqual(got["same"], ["1.dat"])
        self.assertEqual(got["same_compatible_both"], [])


if __name__ == "__main__":
    unittest.main()
