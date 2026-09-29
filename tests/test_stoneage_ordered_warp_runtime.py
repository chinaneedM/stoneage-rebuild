import unittest

from tools.stoneage_ordered_warp_runtime import (
    load_ordered_materializable_runtime,
)


class OrderedWarpRuntimeTests(unittest.TestCase):

    def test_real_create_order_resolves_all_same_file_ambiguities(self):
        runtime = load_ordered_materializable_runtime()
        self.assertEqual(len(runtime.topology.maps), 826)
        self.assertEqual(
            len(runtime.strict_runtime.topology.legacy_warps),
            2692,
        )
        self.assertEqual(len(runtime.ordered_resolutions), 32)
        self.assertEqual(len(runtime.unresolved_ambiguous_sources), 0)
        self.assertEqual(len(runtime.topology.legacy_warps), 2724)

        selected = sum(
            1 for row in runtime.ordered_resolutions
        )
        shadowed = sum(
            len(row.shadowed) for row in runtime.ordered_resolutions
        )
        self.assertEqual(selected, 32)
        self.assertEqual(shadowed, 37)

    def test_quiz_gateway_uses_first_created_warp_to_809(self):
        runtime = load_ordered_materializable_runtime()
        by = runtime.ordered_by_source

        row_a = next(
            row for source, row in by.items()
            if (source.floor_id, source.x, source.y) == (810, 28, 27)
        )
        row_b = next(
            row for source, row in by.items()
            if (source.floor_id, source.x, source.y) == (810, 29, 27)
        )
        self.assertEqual(row_a.selected.placement_id, 3139)
        self.assertEqual(row_a.selected.destination.floor_id, 809)
        self.assertEqual(row_b.selected.placement_id, 3141)
        self.assertEqual(row_b.selected.destination.floor_id, 809)
        self.assertEqual(
            {row.destination.floor_id for row in row_a.shadowed},
            {829},
        )
        self.assertEqual(
            {row.destination.floor_id for row in row_b.shadowed},
            {829},
        )

    def test_ordered_runtime_identifies_shadowed_supplemental_branch(self):
        runtime = load_ordered_materializable_runtime()
        self.assertEqual(len(runtime.reachable_floor_ids), 815)
        self.assertEqual(
            runtime.unreachable_resolved_supplemental_ids,
            (820, 821, 822, 823, 824, 825, 826, 827, 828, 829, 831),
        )
        self.assertEqual(
            len(runtime.resolved_supplemental_floor_ids),
            65,
        )
        self.assertEqual(
            len(
                runtime.resolved_supplemental_floor_ids
                & runtime.reachable_floor_ids
            ),
            54,
        )

    def test_floor130_remains_absent_from_default_runtime(self):
        runtime = load_ordered_materializable_runtime()
        self.assertNotIn(130, runtime.topology.maps)
        self.assertNotIn(130, runtime.reachable_floor_ids)


if __name__ == "__main__":
    unittest.main()
