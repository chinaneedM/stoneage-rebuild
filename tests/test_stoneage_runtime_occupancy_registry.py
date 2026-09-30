import unittest
from types import SimpleNamespace

from tools.stoneage_map_collision_model import CHARACTER, GOLD, ITEM
from tools.stoneage_runtime_occupancy_registry import (
    LiveRuntimeObject,
    RuntimeDynamicOccupancyRegistry,
)
from tools.stoneage_singleplayer_domain import MapPosition


class RuntimeOccupancyRegistryTests(unittest.TestCase):

    def test_query_is_coordinate_scoped_and_deterministic(self):
        registry = RuntimeDynamicOccupancyRegistry()
        registry.upsert(
            LiveRuntimeObject(
                object_id="b",
                kind=ITEM,
                position=MapPosition(1, 2, 3),
                overable=False,
                provenance="test:item",
            )
        )
        registry.upsert(
            LiveRuntimeObject(
                object_id="a",
                kind=CHARACTER,
                position=MapPosition(1, 2, 3),
                overable=True,
                provenance="test:char",
            )
        )
        registry.register_gold(
            object_id="g",
            position=MapPosition(1, 5, 5),
            provenance="test:gold",
        )

        query = registry.query(MapPosition(1, 2, 3))
        self.assertEqual(query.object_ids, ("a", "b"))
        self.assertEqual(
            tuple((o.kind, o.overable) for o in query.occupants),
            ((CHARACTER, True), (ITEM, False)),
        )

    def test_move_remove_and_overable_updates_are_live_state(self):
        registry = RuntimeDynamicOccupancyRegistry()
        registry.register_character(
            object_id="char:1",
            position=MapPosition(2, 1, 1),
            overable=False,
            provenance="test",
        )
        registry.move("char:1", MapPosition(2, 2, 1))
        self.assertEqual(
            registry.query(MapPosition(2, 2, 1)).object_ids,
            ("char:1",),
        )
        registry.set_overable("char:1", True)
        self.assertTrue(registry.objects["char:1"].overable)
        removed = registry.remove("char:1")
        self.assertIsNotNone(removed)
        self.assertEqual(registry.query(MapPosition(2, 2, 1)).object_ids, ())

    def test_gold_is_registered_nonblocking(self):
        registry = RuntimeDynamicOccupancyRegistry()
        obj = registry.register_gold(
            object_id="gold:1",
            position=MapPosition(3, 4, 5),
            provenance="drop",
        )
        self.assertEqual(obj.kind, GOLD)
        self.assertTrue(obj.overable)

    def test_npc_registration_never_infers_overability_from_walkable(self):
        registry = RuntimeDynamicOccupancyRegistry()
        state = SimpleNamespace(
            runtime_object_id=7,
            floor_id=10,
            x=11,
            y=12,
            walkable=1,
        )
        obj = registry.register_npc_runtime_state(
            state,
            overable=False,
            provenance="recovered25:npc-runtime",
        )
        self.assertEqual(obj.object_id, "char:7")
        self.assertFalse(obj.overable)
        self.assertEqual(obj.position, MapPosition(10, 11, 12))

        state.walkable = 0
        obj = registry.register_npc_runtime_state(
            state,
            overable=True,
            provenance="recovered25:npc-runtime",
        )
        self.assertTrue(obj.overable)


if __name__ == "__main__":
    unittest.main()
