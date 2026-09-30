import unittest

from tools.stoneage_runtime_occupancy_registry import (
    RuntimeDynamicOccupancyRegistry,
)
from tools.stoneage_local_runtime_save import (
    build_local_runtime_occupancy_delta,
)
from tools.stoneage_versioned_npc_overability_profile import (
    INHERITED_DEFAULT_OVERABLE,
    STATIC_OVERABLE,
    load_recovered25_npc_overability_profile,
)
from tools.stoneage_recovered25_npc_initial_occupancy import (
    load_recovered25_npc_initial_occupancy_manifest,
)


class Recovered25NpcInitialOccupancyTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.profile = load_recovered25_npc_overability_profile()
        cls.manifest = load_recovered25_npc_initial_occupancy_manifest()

    def test_overability_profile_closes_all_recovered25_placements(self):
        self.assertEqual(len(self.profile.rules), 33)
        self.assertEqual(self.profile.total_placements, 3856)
        self.assertEqual(self.profile.closed_placement_count, 3856)
        self.assertEqual(self.profile.unresolved_rules, ())
        self.assertEqual(
            self.profile.rule_for_functionset("Warp").classification,
            STATIC_OVERABLE,
        )
        self.assertTrue(
            self.profile.initial_overable_for_functionset("Warp")
        )
        self.assertEqual(
            self.profile.rule_for_functionset("<none>").classification,
            INHERITED_DEFAULT_OVERABLE,
        )
        self.assertTrue(
            self.profile.initial_overable_for_functionset("<none>")
        )

    def test_real_initial_occupancy_manifest_preserves_spawn_quarantine(self):
        manifest = self.manifest
        self.assertEqual(len(manifest.rows), 3856)
        self.assertEqual(len(manifest.seedable_rows), 3852)
        self.assertEqual(len(manifest.quarantined_rows), 4)
        self.assertEqual(
            dict(manifest.classification_counts),
            {
                STATIC_OVERABLE: 2264,
                INHERITED_DEFAULT_OVERABLE: 1592,
            },
        )
        self.assertTrue(all(row.overable for row in manifest.rows))
        self.assertTrue(
            all(row.position is not None for row in manifest.rows)
        )

    def test_seedable_npcs_enter_live_registry_with_provenance(self):
        registry = RuntimeDynamicOccupancyRegistry()
        object_ids = self.manifest.populate_registry(registry)
        self.assertEqual(len(object_ids), 3852)
        self.assertEqual(len(registry.objects), 3852)
        self.assertTrue(
            all(obj.overable for obj in registry.objects.values())
        )

        warp = next(
            row
            for row in self.manifest.seedable_rows
            if row.functionset == "Warp"
        )
        query = registry.query(warp.position)
        self.assertIn(warp.object_id, query.object_ids)
        seeded = registry.objects[warp.object_id]
        self.assertEqual(seeded.position, warp.position)
        self.assertTrue(seeded.overable)
        self.assertIn(
            "overability:STATIC_OVERABLE",
            seeded.provenance,
        )

    def test_real_initial_baseline_serializes_as_zero_delta(self):
        registry = RuntimeDynamicOccupancyRegistry()
        self.manifest.populate_registry(registry)
        delta = build_local_runtime_occupancy_delta(
            registry=registry,
            initial_occupancy=self.manifest,
        )
        self.assertEqual(
            delta.base_profile_id,
            "RECOVERED25_INITIAL_NPC_OCCUPANCY_R1",
        )
        self.assertEqual(delta.removed_base_object_ids, ())
        self.assertEqual(delta.upserts, ())

        row = self.manifest.seedable_rows[0]
        registry.move(
            row.object_id,
            type(row.position)(
                row.position.floor_id,
                row.position.x,
                row.position.y,
            ),
        )
        registry.set_overable(row.object_id, not row.overable)
        changed = build_local_runtime_occupancy_delta(
            registry=registry,
            initial_occupancy=self.manifest,
        )
        self.assertEqual(changed.removed_base_object_ids, ())
        self.assertEqual(len(changed.upserts), 1)
        self.assertEqual(changed.upserts[0].object_id, row.object_id)

    def test_population_is_idempotent_but_rejects_conflicting_seed(self):
        registry = RuntimeDynamicOccupancyRegistry()
        first = self.manifest.populate_registry(registry)
        second = self.manifest.populate_registry(registry)
        self.assertEqual(first, second)

        row = self.manifest.seedable_rows[0]
        registry.set_overable(row.object_id, not row.overable)
        with self.assertRaisesRegex(ValueError, "conflicting pre-existing"):
            self.manifest.populate_registry(registry)


if __name__ == "__main__":
    unittest.main()
