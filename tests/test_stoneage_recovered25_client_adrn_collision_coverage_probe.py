import unittest

from tools.stoneage_recovered25_client_adrn_collision_coverage_probe import (
    classify_planes,
    requires_adrn_lookup,
)


class Recovered25ClientAdrnCollisionCoverageTests(unittest.TestCase):

    def test_adrn_lookup_domain_matches_client_collision_family_boundary(self):
        self.assertFalse(requires_adrn_lookup(0))
        self.assertFalse(requires_adrn_lookup(59))
        self.assertTrue(requires_adrn_lookup(60))
        self.assertTrue(requires_adrn_lookup(79))
        self.assertFalse(requires_adrn_lookup(80))
        self.assertFalse(requires_adrn_lookup(99))
        self.assertTrue(requires_adrn_lookup(100))
        self.assertTrue(requires_adrn_lookup(16000))

    def test_floor_closes_when_all_required_ids_resolve(self):
        row = classify_planes(
            floor_id=7,
            tile=(0, 60, 100, 1),
            parts=(0, 79, 200, 2),
            adrn_map_numbers={60, 79, 100, 200},
        )
        self.assertTrue(row.closed)
        self.assertEqual(row.tile_required_refs, 2)
        self.assertEqual(row.parts_required_refs, 2)
        self.assertEqual(row.unresolved_ids, ())

    def test_unresolved_ids_are_deduplicated_and_sorted(self):
        row = classify_planes(
            floor_id=8,
            tile=(100, 100, 60, 61),
            parts=(200, 60, 200),
            adrn_map_numbers={60, 100},
        )
        self.assertFalse(row.closed)
        self.assertEqual(row.unresolved_ids, (61, 200))
        self.assertEqual(row.tile_required_ids, 3)
        self.assertEqual(row.parts_required_ids, 2)

    def test_reserved_non_adrn_small_codes_do_not_create_false_gaps(self):
        row = classify_planes(
            floor_id=9,
            tile=(1, 2, 4, 5, 6, 9, 10, 20, 40, 80, 99),
            parts=(0, 1, 2, 4, 5, 6, 9, 10, 20, 40, 80, 99),
            adrn_map_numbers=set(),
        )
        self.assertTrue(row.closed)
        self.assertEqual(row.tile_required_refs, 0)
        self.assertEqual(row.parts_required_refs, 0)


if __name__ == "__main__":
    unittest.main()
