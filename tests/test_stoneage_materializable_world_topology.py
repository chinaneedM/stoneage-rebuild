import unittest

from tools.stoneage_materializable_world_topology import (
    load_materializable_runtime_topology,
)


class MaterializableWorldTopologyTests(unittest.TestCase):

    def test_real_topology_activates_only_unambiguous_unconditional_edges(self):
        runtime = load_materializable_runtime_topology()

        self.assertEqual(len(runtime.topology.maps), 826)
        self.assertEqual(runtime.raw_materializable_warp_records, 2826)
        self.assertEqual(len(runtime.topology.legacy_warps), 2692)
        self.assertEqual(len(runtime.exact_duplicate_groups), 39)
        self.assertEqual(len(runtime.ambiguous_sources), 32)
        self.assertEqual(len(runtime.deferred_conditional_warps), 14)
        self.assertEqual(len(runtime.quarantined_warps), 8)

        active_sources = [edge.source for edge in runtime.topology.legacy_warps]
        self.assertEqual(len(active_sources), len(set(active_sources)))
        self.assertNotIn(130, runtime.topology.maps)

    def test_multi_destination_source_is_preserved_not_selected(self):
        runtime = load_materializable_runtime_topology()
        key = next(
            source for source in runtime.ambiguous_by_source
            if (
                source.floor_id == 21016
                and source.x == 13
                and source.y == 21
            )
        )
        group = runtime.ambiguous_by_source[key]
        self.assertEqual(len(group.candidates), 6)
        self.assertEqual(
            len({row.destination for row in group.candidates}),
            6,
        )
        self.assertIsNone(runtime.topology.active_warp_at(key))

    def test_exact_duplicate_source_collapses_to_one_active_edge(self):
        runtime = load_materializable_runtime_topology()
        group = next(
            row for row in runtime.exact_duplicate_groups
            if (
                row.source.floor_id == 30614
                and row.source.x == 41
                and row.source.y == 3
            )
        )
        self.assertEqual(len(group.placement_ids), 3)
        edge = runtime.topology.active_warp_at(group.source)
        self.assertIsNotNone(edge)
        self.assertEqual(edge.destination, group.destination)

    def test_conditional_edges_remain_deferred_and_inactive(self):
        runtime = load_materializable_runtime_topology()
        for row in runtime.deferred_conditional_warps:
            self.assertIsNone(runtime.topology.active_warp_at(row.source))


if __name__ == "__main__":
    unittest.main()
