import json
import unittest
from types import MappingProxyType

from tools.stoneage_local_runtime_core import LocalRuntimeSessionState
from tools.stoneage_local_runtime_save import (
    LOCAL_RUNTIME_SAVE_SCHEMA,
    LocalRuntimeSaveSnapshot,
    build_initial_occupancy_registry,
    build_local_runtime_occupancy_delta,
    decode_local_runtime_save,
    encode_local_runtime_save,
    restore_local_runtime_occupancy_registry,
)
from tools.stoneage_singleplayer_domain import (
    MapPosition,
    PersistentPlayerState,
    PlayerState,
)


class _InitialOccupancy:
    profile_id = "TEST_INITIAL_OCCUPANCY_R1"

    def populate_registry(self, registry):
        registry.register_character(
            object_id="npc-placement:1",
            position=MapPosition(1, 1, 1),
            overable=True,
            provenance="test:seed:1",
        )
        registry.register_character(
            object_id="npc-placement:2",
            position=MapPosition(1, 2, 2),
            overable=True,
            provenance="test:seed:2",
        )


def _session():
    return LocalRuntimeSessionState(
        contract_id="test.contract.r1",
        world_profile="recovered25",
        hometown_ordinal=1,
        player_position=MapPosition(1, 0, 0),
        player_state=PersistentPlayerState(
            character=PlayerState(
                MappingProxyType({"name": "save-test", "level": 1})
            )
        ),
        world_flags=frozenset({"flag-a"}),
    )


class LocalRuntimeSaveTests(unittest.TestCase):

    def test_occupancy_delta_persists_only_changes_from_initial_base(self):
        initial = _InitialOccupancy()
        registry = build_initial_occupancy_registry(initial)
        registry.move("npc-placement:1", MapPosition(1, 3, 3))
        registry.set_overable("npc-placement:1", False)
        registry.remove("npc-placement:2")
        registry.register_item(
            object_id="item:drop:7",
            position=MapPosition(1, 4, 4),
            overable=False,
            provenance="test:dropped-item",
        )

        delta = build_local_runtime_occupancy_delta(
            registry=registry,
            initial_occupancy=initial,
        )
        self.assertEqual(
            delta.removed_base_object_ids,
            ("npc-placement:2",),
        )
        self.assertEqual(
            tuple(row.object_id for row in delta.upserts),
            ("item:drop:7", "npc-placement:1"),
        )

        snapshot = LocalRuntimeSaveSnapshot(
            session=_session(),
            occupancy=delta,
        )
        encoded_a = encode_local_runtime_save(snapshot)
        encoded_b = encode_local_runtime_save(snapshot)
        self.assertEqual(encoded_a, encoded_b)
        payload = json.loads(encoded_a)
        self.assertEqual(payload["schema"], LOCAL_RUNTIME_SAVE_SCHEMA)
        self.assertNotIn("collision", encoded_a.lower())
        self.assertEqual(
            len(payload["occupancy"]["upserts"]),
            2,
        )

        decoded = decode_local_runtime_save(
            encoded_a,
            expected_contract_id="test.contract.r1",
            expected_world_profile="recovered25",
        )
        restored = restore_local_runtime_occupancy_registry(
            delta=decoded.occupancy,
            initial_occupancy=initial,
        )
        self.assertNotIn("npc-placement:2", restored.objects)
        self.assertEqual(
            restored.objects["npc-placement:1"].position,
            MapPosition(1, 3, 3),
        )
        self.assertFalse(restored.objects["npc-placement:1"].overable)
        self.assertEqual(
            restored.objects["item:drop:7"].position,
            MapPosition(1, 4, 4),
        )
        self.assertFalse(restored.objects["item:drop:7"].overable)
        self.assertEqual(decoded.session.world_flags, frozenset({"flag-a"}))

    def test_unchanged_initial_occupancy_produces_empty_delta(self):
        initial = _InitialOccupancy()
        registry = build_initial_occupancy_registry(initial)
        delta = build_local_runtime_occupancy_delta(
            registry=registry,
            initial_occupancy=initial,
        )
        self.assertEqual(delta.removed_base_object_ids, ())
        self.assertEqual(delta.upserts, ())

    def test_restore_rejects_initial_profile_drift(self):
        initial = _InitialOccupancy()
        registry = build_initial_occupancy_registry(initial)
        delta = build_local_runtime_occupancy_delta(
            registry=registry,
            initial_occupancy=initial,
        )

        class _OtherInitial(_InitialOccupancy):
            profile_id = "TEST_INITIAL_OCCUPANCY_R2"

        with self.assertRaisesRegex(ValueError, "base-profile mismatch"):
            restore_local_runtime_occupancy_registry(
                delta=delta,
                initial_occupancy=_OtherInitial(),
            )

    def test_empty_initial_profile_persists_explicit_live_objects(self):
        registry = build_initial_occupancy_registry(None)
        registry.register_gold(
            object_id="gold:1",
            position=MapPosition(1, 5, 5),
            provenance="test:gold",
        )
        delta = build_local_runtime_occupancy_delta(
            registry=registry,
            initial_occupancy=None,
        )
        self.assertEqual(
            tuple(row.object_id for row in delta.upserts),
            ("gold:1",),
        )
        restored = restore_local_runtime_occupancy_registry(
            delta=delta,
            initial_occupancy=None,
        )
        self.assertIn("gold:1", restored.objects)


if __name__ == "__main__":
    unittest.main()
