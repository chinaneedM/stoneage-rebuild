import unittest
from types import SimpleNamespace
from unittest.mock import patch

from tools.stoneage_client_hitmap_core import (
    ClientCollisionAttr,
    ClientCollisionProfile,
)
from tools.stoneage_recovered25_client_collision_provider import (
    Recovered25ClientCollisionProvider,
)
from tools.stoneage_singleplayer_domain import MapPosition
from tools.stoneage_singleplayer_world import (
    HistoricalMapDefinition,
    HistoricalWorldTopology,
)


def _collision_profile():
    return ClientCollisionProfile(
        {
            100: ClientCollisionAttr(100, 1000, 1, 1, 1),
            101: ClientCollisionAttr(101, 1001, 1, 1, 0),
        }
    )


class _RegionProvider:
    def __init__(self, profile):
        self.profile = profile
        self.plan = SimpleNamespace(stable_dat_floor_ids=frozenset({7, 8}))

    def _stable_payload(self, floor_id):
        if int(floor_id) == 7:
            return (
                2,
                2,
                (100, 101, 100, 100),
                (0, 0, 0, 0),
                (0, 0, 0, 0),
                "0" * 64,
                "CLIENT_DAT_THREE_PLANE",
                "EVENT_PLANE_PRESENT",
            )
        raise KeyError(floor_id)


class Recovered25ClientCollisionProviderTests(unittest.TestCase):

    def setUp(self):
        self.profile = SimpleNamespace(contract_id="test")
        self.adapter = SimpleNamespace(
            profile=self.profile,
            topology=HistoricalWorldTopology(
                maps={
                    7: HistoricalMapDefinition(7, 2, 2),
                    8: HistoricalMapDefinition(8, 1, 1),
                }
            ),
        )
        self.region = _RegionProvider(self.profile)

    def _provider(self):
        with patch(
            "tools.stoneage_recovered25_client_collision_provider."
            "_profile_from_recovered25_adrn",
            return_value=_collision_profile(),
        ):
            return Recovered25ClientCollisionProvider(
                profile=self.profile,
                adapter=self.adapter,
                region_provider=self.region,
                fallback_floor_ids={7},
                client_adrn_path="not-read-in-test.bin",
            )

    def test_client_hitmap_blocks_and_allows_destination(self):
        provider = self._provider()
        allowed = provider.ordinary_step_verdict(
            origin=MapPosition(7, 0, 0),
            destination=MapPosition(7, 0, 1),
        )
        self.assertTrue(allowed.allowed)

        blocked = provider.ordinary_step_verdict(
            origin=MapPosition(7, 0, 0),
            destination=MapPosition(7, 1, 0),
        )
        self.assertFalse(blocked.allowed)
        self.assertEqual(blocked.reason, "client_hitmap_blocked")

    def test_skywalker_bypasses_hitmap_but_not_bounds(self):
        provider = self._provider()
        verdict = provider.ordinary_step_verdict(
            origin=MapPosition(7, 0, 0),
            destination=MapPosition(7, 1, 0),
            skywalker=True,
        )
        self.assertTrue(verdict.allowed)

        outside = provider.ordinary_step_verdict(
            origin=MapPosition(7, 1, 1),
            destination=MapPosition(7, 2, 1),
            skywalker=True,
        )
        self.assertFalse(outside.allowed)
        self.assertEqual(outside.reason, "destination_out_of_bounds")

    def test_non_fallback_floor_fails_closed(self):
        provider = self._provider()
        with self.assertRaisesRegex(ValueError, "unavailable"):
            provider.ordinary_step_verdict(
                origin=MapPosition(8, 0, 0),
                destination=MapPosition(8, 0, 1),
            )

    def test_semantic_profile_keeps_binary_proof_boundary_explicit(self):
        provider = self._provider()
        self.assertEqual(
            provider.semantic_profile,
            "RECOVERED25_DESCENDANT_STABLE_CLIENT_HITMAP_R1",
        )
        self.assertFalse(provider.exact_recovered25_binary_proof)


if __name__ == "__main__":
    unittest.main()
