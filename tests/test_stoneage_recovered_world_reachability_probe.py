import unittest

from tools.stoneage_recovered_world_reachability_probe import (
    CHANGED,
    DESTINATION_OUT_OF_BOUNDS,
    NO_SERVER_MAP,
    SERVER_ONLY,
    compute_reachability,
)


class RecoveredWorldReachabilityProbeTests(unittest.TestCase):

    def test_recursive_closure_expands_only_runtime_valid_destinations(self):
        audit = compute_reachability(
            stable_ids={1, 10},
            server_dimensions={
                1: ((20, 20),),
                2: ((20, 20),),
                3: ((20, 20),),
                4: ((20, 20),),
                10: ((20, 20),),
            },
            warp_edges=(
                (1, 2, 1, 1),
                (2, 3, 2, 2),
                (3, 4, 3, 3),
                (4, 99, 1, 1),
                (4, 3, 99, 99),
                (50, 51, 1, 1),
            ),
            dat_ids={1, 3, 10},
            client_map_ids=set(),
            changed_ids={3},
        )
        self.assertEqual(
            audit.reached_floor_ids,
            frozenset({1, 2, 3, 4, 10}),
        )
        by_id = {row.floor_id: row for row in audit.supplemental}
        self.assertEqual(by_id[2].depth, 1)
        self.assertEqual(by_id[2].status, SERVER_ONLY)
        self.assertEqual(by_id[3].depth, 2)
        self.assertEqual(by_id[3].status, CHANGED)
        self.assertEqual(by_id[4].depth, 3)
        self.assertNotIn(99, audit.reached_floor_ids)
        self.assertNotIn(50, audit.reached_floor_ids)
        self.assertNotIn(51, audit.reached_floor_ids)

        invalid = {
            (edge.destination_floor, edge.reason)
            for edge in audit.invalid_reachable_edges
        }
        self.assertIn((99, NO_SERVER_MAP), invalid)
        self.assertIn((3, DESTINATION_OUT_OF_BOUNDS), invalid)

    def test_stable_destination_remains_depth_zero(self):
        audit = compute_reachability(
            stable_ids={1, 2},
            server_dimensions={
                1: ((10, 10),),
                2: ((10, 10),),
                3: ((10, 10),),
            },
            warp_edges=((1, 3, 1, 1), (3, 2, 2, 2)),
            dat_ids={1, 2},
            client_map_ids=set(),
            changed_ids=set(),
        )
        self.assertEqual(
            {row.floor_id: row.depth for row in audit.supplemental},
            {3: 1},
        )
        self.assertEqual(audit.counts["max_supplemental_depth"], 1)
        self.assertEqual(
            audit.counts["reachable_runtime_classic_warp_edges"],
            2,
        )

    def test_duplicate_server_copies_accept_coordinate_if_any_copy_contains_it(self):
        audit = compute_reachability(
            stable_ids={1},
            server_dimensions={
                1: ((10, 10),),
                2: ((2, 2), (20, 20)),
            },
            warp_edges=((1, 2, 15, 15),),
            dat_ids={1},
            client_map_ids=set(),
            changed_ids=set(),
        )
        self.assertIn(2, audit.reached_floor_ids)
        self.assertEqual(audit.invalid_reachable_edges, ())


if __name__ == "__main__":
    unittest.main()
