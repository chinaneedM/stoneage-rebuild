import unittest

from tools.stoneage_recovered_world_reachability_probe import (
    CHANGED,
    NO_SERVER_MAP,
    SERVER_ONLY,
    compute_reachability,
)


class RecoveredWorldReachabilityProbeTests(unittest.TestCase):

    def test_recursive_closure_expands_server_backed_supplemental_floors(self):
        audit = compute_reachability(
            stable_ids={1, 10},
            server_ids={1, 2, 3, 4, 10},
            warp_edges=((1, 2), (2, 3), (3, 4), (4, 99), (50, 51)),
            dat_ids={1, 3, 10},
            client_map_ids=set(),
            changed_ids={3},
        )
        self.assertEqual(audit.reached_floor_ids, frozenset({1, 2, 3, 4, 10, 99}))
        by_id = {row.floor_id: row for row in audit.supplemental}
        self.assertEqual(by_id[2].depth, 1)
        self.assertEqual(by_id[2].status, SERVER_ONLY)
        self.assertEqual(by_id[3].depth, 2)
        self.assertEqual(by_id[3].status, CHANGED)
        self.assertEqual(by_id[4].depth, 3)
        self.assertEqual(by_id[99].depth, 4)
        self.assertEqual(by_id[99].status, NO_SERVER_MAP)
        self.assertNotIn(50, audit.reached_floor_ids)
        self.assertNotIn(51, audit.reached_floor_ids)

    def test_stable_destination_remains_depth_zero(self):
        audit = compute_reachability(
            stable_ids={1, 2},
            server_ids={1, 2, 3},
            warp_edges=((1, 3), (3, 2)),
            dat_ids={1, 2},
            client_map_ids=set(),
            changed_ids=set(),
        )
        self.assertEqual(
            {row.floor_id: row.depth for row in audit.supplemental},
            {3: 1},
        )
        self.assertEqual(audit.counts["max_supplemental_depth"], 1)
        self.assertEqual(audit.counts["reachable_classic_warp_edges"], 2)


if __name__ == "__main__":
    unittest.main()
