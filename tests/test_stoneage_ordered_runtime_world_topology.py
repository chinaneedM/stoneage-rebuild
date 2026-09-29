import unittest

from tools.stoneage_ordered_runtime_world_topology import (
    load_ordered_materializable_runtime_topology,
)


class OrderedRuntimeWorldTopologyTests(unittest.TestCase):

    def test_real_create_order_resolves_all_32_ambiguous_sources(self):
        runtime = load_ordered_materializable_runtime_topology()

        self.assertEqual(len(runtime.topology.maps), 826)
        self.assertEqual(len(runtime.base.topology.legacy_warps), 2692)
        self.assertEqual(len(runtime.ordered_resolutions), 32)
        self.assertEqual(len(runtime.unresolved_cross_file_sources), 0)
        self.assertEqual(runtime.shadowed_candidate_records, 37)
        self.assertEqual(len(runtime.topology.legacy_warps), 2724)
        self.assertEqual(len(runtime.base.deferred_conditional_warps), 14)

        active_sources = [edge.source for edge in runtime.topology.legacy_warps]
        self.assertEqual(len(active_sources), len(set(active_sources)))

    def test_810_gateway_uses_first_same_file_candidate_and_shadows_829(self):
        runtime = load_ordered_materializable_runtime_topology()
        keys = [
            source
            for source in runtime.resolution_by_source
            if source.floor_id == 810
            and source.y == 27
            and source.x in {28, 29}
        ]
        self.assertEqual(len(keys), 2)

        by_x = {
            source.x: runtime.resolution_by_source[source]
            for source in keys
        }
        self.assertEqual(by_x[28].selected.placement_id, 3139)
        self.assertEqual(
            (
                by_x[28].selected.destination.floor_id,
                by_x[28].selected.destination.x,
                by_x[28].selected.destination.y,
            ),
            (809, 18, 13),
        )
        self.assertEqual(
            [row.placement_id for row in by_x[28].shadowed],
            [3197],
        )
        self.assertEqual(
            by_x[28].shadowed[0].destination.floor_id,
            829,
        )

        self.assertEqual(by_x[29].selected.placement_id, 3141)
        self.assertEqual(
            (
                by_x[29].selected.destination.floor_id,
                by_x[29].selected.destination.x,
                by_x[29].selected.destination.y,
            ),
            (809, 19, 13),
        )
        self.assertEqual(
            [row.placement_id for row in by_x[29].shadowed],
            [3199],
        )
        self.assertEqual(
            by_x[29].shadowed[0].destination.floor_id,
            829,
        )

    def test_shadowed_candidates_remain_evidence_not_active_edges(self):
        runtime = load_ordered_materializable_runtime_topology()
        source = next(
            source
            for source in runtime.resolution_by_source
            if source.floor_id == 810 and source.x == 28 and source.y == 27
        )
        resolution = runtime.resolution_by_source[source]

        active = [
            edge
            for edge in runtime.topology.legacy_warps
            if edge.source == source
        ]
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0].destination, resolution.selected.destination)
        self.assertNotEqual(
            active[0].destination,
            resolution.shadowed[0].destination,
        )


if __name__ == "__main__":
    unittest.main()
