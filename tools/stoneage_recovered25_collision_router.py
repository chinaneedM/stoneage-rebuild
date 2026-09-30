#!/usr/bin/env python3
"""Provenance-bearing recovered25 collision router.

The router preserves two distinct evidence classes:
- recovered server LS2MAP + recovered mapset collision where that path is closed;
- recovered client DAT + ADRN using the explicitly labelled descendant-stable
  client hit-map reconstruction profile for the remaining floors.

It never silently swaps one source for the other on the same floor.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_map_collision_model import CollisionDecision
from tools.stoneage_singleplayer_domain import MapPosition


SERVER_PROVIDER_KIND = "RECOVERED25_SERVER_COLLISION"
CLIENT_PROVIDER_KIND = "RECOVERED25_CLIENT_HITMAP_RECONSTRUCTION"

SERVER_EVIDENCE_CLASS = "LATER_RECOVERED_SERVER_PAYLOAD_AND_MAPSET"
CLIENT_EVIDENCE_CLASS = "LATER_RECOVERED_PLUS_PINNED_DESCENDANT_STABLE_ALGORITHM"

SERVER_SEMANTIC_PROFILE = "RECOVERED25_SERVER_LS2MAP_MAPSET_R1"


@dataclass(frozen=True)
class Recovered25CollisionRoute:
    floor_id: int
    provider_kind: str
    evidence_class: str
    semantic_profile: str
    exact_recovered25_binary_proof: bool | None = None


@dataclass(frozen=True)
class RoutedCollisionVerdict:
    route: Recovered25CollisionRoute
    decision: CollisionDecision


class Recovered25CollisionRouter:

    def __init__(
        self,
        *,
        adapter,
        server_provider,
        client_provider,
    ) -> None:
        self.adapter = adapter
        self.server_provider = server_provider
        self.client_provider = client_provider

        topology = frozenset(int(v) for v in adapter.topology.maps)
        server = frozenset(int(v) for v in server_provider.supported_floor_ids)
        client = frozenset(int(v) for v in client_provider.supported_floor_ids)

        overlap = server & client
        if overlap:
            raise ValueError(
                f"collision router provider overlap: {sorted(overlap)[:10]}"
            )
        missing = topology - (server | client)
        extra = (server | client) - topology
        if missing:
            raise ValueError(
                f"collision router missing materializable floors: "
                f"{sorted(missing)[:10]}"
            )
        if extra:
            raise ValueError(
                f"collision router contains floors outside topology: "
                f"{sorted(extra)[:10]}"
            )

        self.server_floor_ids = server
        self.client_floor_ids = client
        self.floor_ids = topology

    def route_for_floor(self, floor_id: int) -> Recovered25CollisionRoute:
        floor_id = int(floor_id)
        if floor_id in self.server_floor_ids:
            return Recovered25CollisionRoute(
                floor_id=floor_id,
                provider_kind=SERVER_PROVIDER_KIND,
                evidence_class=SERVER_EVIDENCE_CLASS,
                semantic_profile=SERVER_SEMANTIC_PROFILE,
                exact_recovered25_binary_proof=None,
            )
        if floor_id in self.client_floor_ids:
            return Recovered25CollisionRoute(
                floor_id=floor_id,
                provider_kind=CLIENT_PROVIDER_KIND,
                evidence_class=self.client_provider.evidence_role,
                semantic_profile=self.client_provider.semantic_profile,
                exact_recovered25_binary_proof=(
                    self.client_provider.exact_recovered25_binary_proof
                ),
            )
        raise KeyError(f"floor {floor_id} is outside collision router topology")

    def routed_step_verdict(
        self,
        *,
        origin: MapPosition,
        destination: MapPosition,
    ) -> RoutedCollisionVerdict:
        route = self.route_for_floor(origin.floor_id)
        if route.provider_kind == SERVER_PROVIDER_KIND:
            decision = self.server_provider.ordinary_step_verdict(
                origin=origin,
                destination=destination,
            )
        elif route.provider_kind == CLIENT_PROVIDER_KIND:
            decision = self.client_provider.ordinary_step_verdict(
                origin=origin,
                destination=destination,
            )
        else:
            raise AssertionError("unknown collision route provider")
        return RoutedCollisionVerdict(route=route, decision=decision)

    def ordinary_step_verdict(
        self,
        *,
        origin: MapPosition,
        destination: MapPosition,
    ) -> CollisionDecision:
        return self.routed_step_verdict(
            origin=origin,
            destination=destination,
        ).decision

    def coverage_counts(self) -> Mapping[str, int]:
        return MappingProxyType(
            {
                "materializable_floors": len(self.floor_ids),
                "server_routed_floors": len(self.server_floor_ids),
                "client_reconstruction_routed_floors": len(self.client_floor_ids),
                "provider_overlap_floors": len(
                    self.server_floor_ids & self.client_floor_ids
                ),
                "unrouted_floors": len(
                    self.floor_ids
                    - (self.server_floor_ids | self.client_floor_ids)
                ),
            }
        )
