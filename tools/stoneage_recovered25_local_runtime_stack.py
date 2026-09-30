#!/usr/bin/env python3
"""Concrete recovered25 local runtime composition.

This DESIGN layer composes the already-versioned runtime bootstrap contract,
provenance-bearing recovered25 world adapter, concrete map-plane provider,
state-gated transition resolver/evaluator, fresh-start factory, and local
session model behind one engine-neutral entry point.

It does not choose a rendering engine and does not recreate legacy MMO
transport or account services.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from tools.stoneage_local_runtime_core import (
    FreshStartSeed,
    LocalRuntimeSessionState,
    MaterializedWorldRegion,
    ResolvedTransitionBinding,
    RuntimeBootstrapProfile,
    StateGatedTransitionContract,
    TransitionGateDecision,
    WorldRegionRequest,
)
from tools.stoneage_recovered25_region_payload import (
    Recovered25RegionPayloadSource,
)
from tools.stoneage_recovered25_client_collision_provider import (
    Recovered25ClientCollisionProvider,
)
from tools.stoneage_recovered25_collision_router import (
    Recovered25CollisionRouter,
)
from tools.stoneage_recovered25_collision_router import (
    Recovered25CollisionRouter,
)
from tools.stoneage_recovered25_server_collision_provider import (
    Recovered25ServerCollisionProvider,
)
from tools.stoneage_recovered25_world_profile_adapter import (
    Recovered25FreshStartFactory,
    Recovered25TransitionBindingResolver,
    Recovered25TransitionGateEvaluator,
    Recovered25WorldProfileAdapter,
    derive_recovered25_transition_bindings,
)
from tools.stoneage_singleplayer_domain import PersistentPlayerState


@dataclass(frozen=True)
class Recovered25LocalRuntimeStack:
    profile: RuntimeBootstrapProfile
    world_adapter: Recovered25WorldProfileAdapter
    region_provider: Recovered25RegionPayloadSource
    transition_resolver: Recovered25TransitionBindingResolver
    transition_evaluator: Recovered25TransitionGateEvaluator
    fresh_start_factory: Recovered25FreshStartFactory
    collision_provider: Recovered25ServerCollisionProvider | None = None
    client_collision_provider: Recovered25ClientCollisionProvider | None = None
    collision_router: Recovered25CollisionRouter | None = None
    collision_router: Recovered25CollisionRouter | None = None

    @classmethod
    def from_verified_bundle(
        cls,
        *,
        profile: RuntimeBootstrapProfile,
        player_state_factory: Callable[[int], PersistentPlayerState],
        client_dat_dir: Path,
        npc_dir: Path,
        setup: Path,
        server_map_root: Path,
        mapset_path: Path,
        client_adrn_path: Path | None = None,
    ) -> "Recovered25LocalRuntimeStack":
        adapter = Recovered25WorldProfileAdapter.from_repository(profile)
        region_provider = Recovered25RegionPayloadSource(
            profile=profile,
            adapter=adapter,
            client_dat_dir=client_dat_dir,
            server_map_root=server_map_root,
        )
        bindings = derive_recovered25_transition_bindings(
            profile=profile,
            npc_dir=npc_dir,
            setup=setup,
            server_map_root=server_map_root,
            mapset_path=mapset_path,
        )
        resolver = Recovered25TransitionBindingResolver(
            profile=profile,
            adapter=adapter,
            bindings=bindings,
        )
        evaluator = Recovered25TransitionGateEvaluator(profile)
        factory = Recovered25FreshStartFactory(adapter, player_state_factory)
        collision_provider = Recovered25ServerCollisionProvider(
            profile=profile,
            adapter=adapter,
            server_map_root=server_map_root,
            mapset_path=mapset_path,
        )
        client_collision_provider = (
            None
            if client_adrn_path is None
            else Recovered25ClientCollisionProvider(
                profile=profile,
                adapter=adapter,
                region_provider=region_provider,
                fallback_floor_ids=collision_provider.unsupported_floor_ids,
                client_adrn_path=client_adrn_path,
            )
        )
        collision_router = (
            None
            if client_collision_provider is None
            else Recovered25CollisionRouter(
                adapter=adapter,
                server_provider=collision_provider,
                client_provider=client_collision_provider,
            )
        )
        stack = cls(
            profile=profile,
            world_adapter=adapter,
            region_provider=region_provider,
            transition_resolver=resolver,
            transition_evaluator=evaluator,
            fresh_start_factory=factory,
            collision_provider=collision_provider,
            client_collision_provider=client_collision_provider,
            collision_router=collision_router,
        )
        stack._validate()
        return stack

    def _validate(self) -> None:
        if self.world_adapter.profile.contract_id != self.profile.contract_id:
            raise ValueError("runtime stack adapter/profile contract drift")
        if self.region_provider.profile.contract_id != self.profile.contract_id:
            raise ValueError("runtime stack region-provider contract drift")
        if set(self.transition_resolver.bindings) != set(self.profile.transitions):
            raise ValueError("runtime stack transition-set drift")
        if self.region_provider.plan.floor_ids != frozenset(self.world_adapter.topology.maps):
            raise ValueError("runtime stack payload/topology floor-set drift")
        if self.collision_provider is not None:
            if self.collision_provider.profile.contract_id != self.profile.contract_id:
                raise ValueError("runtime stack collision-provider contract drift")
            if frozenset(self.collision_provider.floors) != frozenset(
                self.world_adapter.topology.maps
            ):
                raise ValueError("runtime stack collision/topology floor-set drift")
        if self.client_collision_provider is not None:
            if self.collision_provider is None:
                raise ValueError(
                    "client collision provider requires server collision provider"
                )
            server = self.collision_provider.supported_floor_ids
            client = self.client_collision_provider.supported_floor_ids
            topology = frozenset(self.world_adapter.topology.maps)
            if server & client:
                raise ValueError("server/client collision floor sets overlap")
            if server | client != topology:
                raise ValueError(
                    "server/client collision floor sets do not close topology"
                )
            if self.collision_router is None:
                raise ValueError(
                    "closed server/client collision providers require router"
                )
            if self.collision_router.floor_ids != topology:
                raise ValueError("collision router/topology floor-set drift")
            if self.collision_router is None:
                raise ValueError(
                    "client collision provider requires collision router"
                )
            if self.collision_router.floor_ids != topology:
                raise ValueError("collision router/topology floor-set drift")
        elif self.collision_router is not None:
            raise ValueError(
                "collision router requires client collision provider"
            )

    def create_fresh_start(self, hometown_ordinal: int) -> FreshStartSeed:
        return self.fresh_start_factory.create_fresh_start(
            self.profile,
            int(hometown_ordinal),
        )

    def materialize_region(
        self,
        request: WorldRegionRequest,
    ) -> MaterializedWorldRegion:
        if request.world_profile != self.profile.runtime_world_profile:
            raise ValueError("runtime stack region world-profile mismatch")
        return self.region_provider.materialize_region(request)

    def materialize_player_position(
        self,
        session: LocalRuntimeSessionState,
    ) -> MaterializedWorldRegion:
        if session.contract_id != self.profile.contract_id:
            raise ValueError("runtime stack session contract mismatch")
        if session.world_profile != self.profile.runtime_world_profile:
            raise ValueError("runtime stack session world-profile mismatch")
        p = session.player_position
        return self.materialize_region(
            WorldRegionRequest(
                floor_id=int(p.floor_id),
                x1=int(p.x),
                y1=int(p.y),
                x2=int(p.x),
                y2=int(p.y),
                world_profile=self.profile.runtime_world_profile,
            )
        )

    def transition_contract(
        self,
        transition_id: str,
    ) -> StateGatedTransitionContract:
        try:
            return self.profile.transitions[str(transition_id)]
        except KeyError as exc:
            raise KeyError(f"unknown state-gated transition: {transition_id}") from exc

    def resolve_transition(
        self,
        transition_id: str,
    ) -> ResolvedTransitionBinding:
        contract = self.transition_contract(transition_id)
        return self.transition_resolver.resolve_transition(contract)

    def evaluate_transition(
        self,
        transition_id: str,
        session: LocalRuntimeSessionState,
    ) -> TransitionGateDecision:
        contract = self.transition_contract(transition_id)
        binding = self.transition_resolver.resolve_transition(contract)
        return self.transition_evaluator.evaluate_transition(
            contract,
            binding,
            session,
        )
