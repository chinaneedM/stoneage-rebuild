import unittest

from tools.stoneage_ordered_runtime_world_reachability_probe import (
    load_ordered_runtime_reachability,
)


class OrderedRuntimeWorldReachabilityTests(unittest.TestCase):

    def test_real_ordered_runtime_has_11_resolved_supplemental_orphans(self):
        audit = load_ordered_runtime_reachability()
        counts = audit.counts

        self.assertEqual(counts["stable_seed_floors"], 761)
        self.assertEqual(counts["materializable_floor_ids"], 826)
        self.assertEqual(counts["active_runtime_warps"], 2724)
        self.assertEqual(counts["ordered_source_resolutions"], 32)
        self.assertEqual(counts["shadowed_candidate_records"], 37)
        self.assertEqual(counts["unresolved_cross_file_sources"], 0)
        self.assertEqual(counts["deferred_conditional_warps"], 14)
        self.assertEqual(counts["reachable_floor_ids"], 815)
        self.assertEqual(
            counts["reachable_resolved_supplemental_floors"],
            54,
        )
        self.assertEqual(
            counts["orphan_resolved_supplemental_floors"],
            11,
        )
        self.assertEqual(
            counts["max_reachable_resolved_supplemental_depth"],
            12,
        )
        self.assertEqual(
            {row.floor_id for row in audit.orphan_rows},
            {820, 821, 822, 823, 824, 825, 826, 827, 828, 829, 831},
        )

    def test_only_shadowed_810_to_829_candidates_feed_orphan_component(self):
        audit = load_ordered_runtime_reachability()
        rows = audit.shadowed_ingress

        self.assertEqual(len(rows), 2)
        self.assertEqual(
            {
                (
                    row.source_floor,
                    row.source_x,
                    row.source_y,
                    row.selected_placement,
                    row.selected_destination_floor,
                    row.shadowed_placement,
                    row.shadowed_destination_floor,
                    row.shadowed_destination_x,
                    row.shadowed_destination_y,
                )
                for row in rows
            },
            {
                (810, 28, 27, 3139, 809, 3197, 829, 18, 13),
                (810, 29, 27, 3141, 809, 3199, 829, 19, 13),
            },
        )

    def test_orphans_have_internal_active_edges_but_no_reachable_active_ingress(self):
        audit = load_ordered_runtime_reachability()
        orphan_ids = {row.floor_id for row in audit.orphan_rows}
        reached = set(audit.reached_floor_ids)

        self.assertTrue(orphan_ids)
        self.assertFalse(orphan_ids & reached)
        self.assertTrue(
            all(row.active_incoming > 0 for row in audit.orphan_rows)
        )
        self.assertTrue(
            all(row.active_outgoing > 0 for row in audit.orphan_rows)
        )


if __name__ == "__main__":
    unittest.main()
