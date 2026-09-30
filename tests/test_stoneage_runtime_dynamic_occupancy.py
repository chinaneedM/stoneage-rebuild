import unittest
from types import SimpleNamespace

from tools.stoneage_map_collision_model import (
    CHARACTER,
    GOLD,
    ITEM,
    CollisionDecision,
    DynamicOccupant,
)
from tools.stoneage_recovered25_collision_router import (
    Recovered25CollisionRoute,
    RoutedCollisionVerdict,
)
from tools.stoneage_runtime_dynamic_occupancy import (
    DYNAMIC_OCCUPANCY_EVIDENCE_CLASS,
    DYNAMIC_OCCUPANCY_PROFILE,
    resolve_runtime_collision_with_occupancy,
)
from tools.stoneage_singleplayer_domain import MapPosition


class _Router:
    def __init__(self, allowed=True):
        self.allowed = allowed
        self.calls = 0

    def routed_step_verdict(self, *, origin, destination):
        self.calls += 1
        return RoutedCollisionVerdict(
            route=Recovered25CollisionRoute(
                floor_id=origin.floor_id,
                provider_kind="STATIC_TEST",
                evidence_class="STATIC_EVIDENCE",
                semantic_profile="STATIC_PROFILE",
                exact_recovered25_binary_proof=False,
            ),
            decision=CollisionDecision(
                self.allowed,
                None if self.allowed else "static_blocked",
            ),
        )


class RuntimeDynamicOccupancyTests(unittest.TestCase):

    def test_static_denial_is_not_overridden_or_relabelled(self):
        router = _Router(False)
        result = resolve_runtime_collision_with_occupancy(
            router=router,
            origin=MapPosition(1, 0, 0),
            destination=MapPosition(1, 1, 0),
            destination_occupants=(
                DynamicOccupant(kind=GOLD, overable=True),
            ),
        )
        self.assertFalse(result.decision.allowed)
        self.assertEqual(result.decision.reason, "static_blocked")
        self.assertEqual(result.static.route.evidence_class, "STATIC_EVIDENCE")
        self.assertEqual(
            result.dynamic.reason,
            "dynamic_occupancy_not_evaluated_static_denied",
        )

    def test_non_overable_character_blocks_after_static_allow(self):
        result = resolve_runtime_collision_with_occupancy(
            router=_Router(True),
            origin=MapPosition(1, 0, 0),
            destination=MapPosition(1, 1, 0),
            destination_occupants=(
                DynamicOccupant(kind=CHARACTER, overable=False),
            ),
        )
        self.assertTrue(result.static_allowed)
        self.assertFalse(result.dynamic_allowed)
        self.assertFalse(result.decision.allowed)
        self.assertEqual(result.decision.reason, "non_overable_character")
        self.assertEqual(result.dynamic_profile, DYNAMIC_OCCUPANCY_PROFILE)
        self.assertEqual(
            result.dynamic_evidence_class,
            DYNAMIC_OCCUPANCY_EVIDENCE_CLASS,
        )

    def test_non_overable_item_blocks_after_static_allow(self):
        result = resolve_runtime_collision_with_occupancy(
            router=_Router(True),
            origin=MapPosition(1, 0, 0),
            destination=MapPosition(1, 1, 0),
            destination_occupants=(
                DynamicOccupant(kind=ITEM, overable=False),
            ),
        )
        self.assertFalse(result.decision.allowed)
        self.assertEqual(result.decision.reason, "non_overable_item")

    def test_gold_and_overable_character_item_do_not_block(self):
        result = resolve_runtime_collision_with_occupancy(
            router=_Router(True),
            origin=MapPosition(1, 0, 0),
            destination=MapPosition(1, 1, 0),
            destination_occupants=(
                DynamicOccupant(kind=GOLD, overable=False),
                DynamicOccupant(kind=CHARACTER, overable=True),
                DynamicOccupant(kind=ITEM, overable=True),
            ),
        )
        self.assertTrue(result.static_allowed)
        self.assertTrue(result.dynamic_allowed)
        self.assertTrue(result.decision.allowed)

    def test_static_route_provenance_survives_dynamic_block(self):
        result = resolve_runtime_collision_with_occupancy(
            router=_Router(True),
            origin=MapPosition(7, 0, 0),
            destination=MapPosition(7, 1, 0),
            destination_occupants=(
                DynamicOccupant(kind=CHARACTER, overable=False),
            ),
        )
        self.assertEqual(result.static.route.provider_kind, "STATIC_TEST")
        self.assertEqual(result.static.route.semantic_profile, "STATIC_PROFILE")
        self.assertFalse(result.static.route.exact_recovered25_binary_proof)


if __name__ == "__main__":
    unittest.main()
