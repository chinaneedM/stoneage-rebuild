import unittest
from types import SimpleNamespace

from tools.stoneage_map_collision_model import CollisionDecision
from tools.stoneage_recovered25_collision_router import (
    CLIENT_PROVIDER_KIND,
    SERVER_PROVIDER_KIND,
    Recovered25CollisionRouter,
)
from tools.stoneage_singleplayer_domain import MapPosition
from tools.stoneage_singleplayer_world import (
    HistoricalMapDefinition,
    HistoricalWorldTopology,
)


class _Provider:
    def __init__(self, floors, allowed=True, *, client=False):
        self.supported_floor_ids = frozenset(floors)
        self.allowed = allowed
        self.calls = 0
        if client:
            self.evidence_role = (
                "LATER_RECOVERED_PLUS_PINNED_DESCENDANT_STABLE_ALGORITHM"
            )
            self.semantic_profile = (
                "RECOVERED25_DESCENDANT_STABLE_CLIENT_HITMAP_R1"
            )
            self.exact_recovered25_binary_proof = False

    def ordinary_step_verdict(self, *, origin, destination):
        self.calls += 1
        return CollisionDecision(self.allowed, None if self.allowed else "blocked")


class Recovered25CollisionRouterTests(unittest.TestCase):

    def setUp(self):
        self.adapter = SimpleNamespace(
            topology=HistoricalWorldTopology(
                maps={
                    1: HistoricalMapDefinition(1, 2, 2),
                    2: HistoricalMapDefinition(2, 2, 2),
                    3: HistoricalMapDefinition(3, 2, 2),
                }
            )
        )

    def test_disjoint_sources_cover_topology(self):
        server = _Provider({1, 2})
        client = _Provider({3}, client=True)
        router = Recovered25CollisionRouter(
            adapter=self.adapter,
            server_provider=server,
            client_provider=client,
        )
        self.assertEqual(router.coverage_counts()["materializable_floors"], 3)
        self.assertEqual(router.coverage_counts()["server_routed_floors"], 2)
        self.assertEqual(
            router.coverage_counts()["client_reconstruction_routed_floors"],
            1,
        )
        self.assertEqual(router.coverage_counts()["provider_overlap_floors"], 0)
        self.assertEqual(router.coverage_counts()["unrouted_floors"], 0)

    def test_route_preserves_evidence_class(self):
        server = _Provider({1, 2})
        client = _Provider({3}, client=True)
        router = Recovered25CollisionRouter(
            adapter=self.adapter,
            server_provider=server,
            client_provider=client,
        )
        self.assertEqual(router.route_for_floor(1).provider_kind, SERVER_PROVIDER_KIND)
        client_route = router.route_for_floor(3)
        self.assertEqual(client_route.provider_kind, CLIENT_PROVIDER_KIND)
        self.assertEqual(
            client_route.semantic_profile,
            "RECOVERED25_DESCENDANT_STABLE_CLIENT_HITMAP_R1",
        )
        self.assertFalse(client_route.exact_recovered25_binary_proof)

    def test_verdict_dispatches_to_one_provider_only(self):
        server = _Provider({1, 2}, allowed=True)
        client = _Provider({3}, allowed=False, client=True)
        router = Recovered25CollisionRouter(
            adapter=self.adapter,
            server_provider=server,
            client_provider=client,
        )
        server_result = router.routed_step_verdict(
            origin=MapPosition(1, 0, 0),
            destination=MapPosition(1, 1, 0),
        )
        self.assertTrue(server_result.decision.allowed)
        self.assertEqual(server.calls, 1)
        self.assertEqual(client.calls, 0)

        client_result = router.routed_step_verdict(
            origin=MapPosition(3, 0, 0),
            destination=MapPosition(3, 1, 0),
        )
        self.assertFalse(client_result.decision.allowed)
        self.assertEqual(server.calls, 1)
        self.assertEqual(client.calls, 1)

    def test_overlap_or_missing_floor_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "overlap"):
            Recovered25CollisionRouter(
                adapter=self.adapter,
                server_provider=_Provider({1, 2}),
                client_provider=_Provider({2, 3}, client=True),
            )

        with self.assertRaisesRegex(ValueError, "missing"):
            Recovered25CollisionRouter(
                adapter=self.adapter,
                server_provider=_Provider({1}),
                client_provider=_Provider({3}, client=True),
            )


if __name__ == "__main__":
    unittest.main()
