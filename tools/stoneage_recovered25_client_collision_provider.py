#!/usr/bin/env python3
"""Recovered25 client-DAT collision provider.

This provider is intentionally restricted to materializable recovered25 floors
that are not covered by the exact recovered server LS2MAP collision provider.

Data provenance:
- map planes: same-bundle recovered25 client DAT;
- collision attributes: same-bundle recovered25 adrn_15.bin;
- algorithm semantics: RECOVERED25_DESCENDANT_STABLE_CLIENT_HITMAP_R1,
  supported by the pinned multi-lineage source audit, not direct sa_2903
  machine-code identity.

The provider therefore exposes a reconstruction-grade verdict with an explicit
evidence-class boundary rather than relabelling it as exact recovered25 binary
behavior.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_client_hitmap_core import (
    ClientCollisionAttr,
    ClientCollisionProfile,
    ClientHitMap,
    build_client_hit_map,
)
from tools.stoneage_dat_probe import load_adrn
from tools.stoneage_map_collision_model import CollisionDecision
from tools.stoneage_singleplayer_domain import MapPosition


RECOVERED25_ADRN_SHA256 = (
    "92d0137590d35a7a1f4fb11af3ad13bbc585813a4b0e1e3f933c397007fbff74"
)
RECOVERED25_ADRN_BYTES = 18_765_120
RECOVERED25_ADRN_RECORDS = 234_564

SEMANTIC_PROFILE = "RECOVERED25_DESCENDANT_STABLE_CLIENT_HITMAP_R1"
EVIDENCE_ROLE = "LATER_RECOVERED_PLUS_PINNED_DESCENDANT_STABLE_ALGORITHM"
EXACT_RECOVERED25_BINARY_PROOF = False


def _profile_from_recovered25_adrn(path: Path) -> ClientCollisionProfile:
    raw = Path(path).read_bytes()
    if len(raw) != RECOVERED25_ADRN_BYTES:
        raise ValueError("recovered25 ADRN byte-size drift")
    if hashlib.sha256(raw).hexdigest() != RECOVERED25_ADRN_SHA256:
        raise ValueError("recovered25 ADRN SHA-256 drift")

    parsed = load_adrn(Path(path))
    if int(parsed["records"]) != RECOVERED25_ADRN_RECORDS:
        raise ValueError("recovered25 ADRN record-count drift")

    attrs = {}
    for map_number, row in parsed["by_bmp"].items():
        map_number = int(map_number)
        if map_number <= 0:
            continue
        attrs[map_number] = ClientCollisionAttr(
            map_number=map_number,
            bitmapno=int(row["bitmapno"]),
            atari_x=int(row["atari_x"]),
            atari_y=int(row["atari_y"]),
            hit_raw=int(row["hit"]),
            height_flag=int(row["height"]),
        )
    return ClientCollisionProfile(attrs)


class Recovered25ClientCollisionProvider:
    """Lazy recovered25 client hit-map provider for server-collision gaps."""

    def __init__(
        self,
        *,
        profile,
        adapter,
        region_provider,
        fallback_floor_ids,
        client_adrn_path: Path,
    ) -> None:
        self.profile = profile
        self.adapter = adapter
        self.region_provider = region_provider
        if adapter.profile.contract_id != profile.contract_id:
            raise ValueError("client collision adapter/profile contract drift")
        if region_provider.profile.contract_id != profile.contract_id:
            raise ValueError("client collision region/profile contract drift")

        floors = frozenset(int(v) for v in fallback_floor_ids)
        if not floors:
            raise ValueError("client collision fallback floor set is empty")
        if not floors <= region_provider.plan.stable_dat_floor_ids:
            raise ValueError(
                "client collision fallback includes non-client-DAT floor"
            )
        if not floors <= frozenset(adapter.topology.maps):
            raise ValueError(
                "client collision fallback includes floor outside topology"
            )

        self.fallback_floor_ids = floors
        self.client_adrn_path = Path(client_adrn_path)
        self.collision_profile = _profile_from_recovered25_adrn(
            self.client_adrn_path
        )
        self._hit_maps: dict[int, ClientHitMap] = {}

    @property
    def supported_floor_ids(self) -> frozenset[int]:
        return self.fallback_floor_ids

    @property
    def semantic_profile(self) -> str:
        return SEMANTIC_PROFILE

    @property
    def evidence_role(self) -> str:
        return EVIDENCE_ROLE

    @property
    def exact_recovered25_binary_proof(self) -> bool:
        return EXACT_RECOVERED25_BINARY_PROOF

    def _hit_map(self, floor_id: int) -> ClientHitMap:
        floor_id = int(floor_id)
        if floor_id not in self.fallback_floor_ids:
            raise ValueError(
                f"recovered25 client collision unavailable for floor {floor_id}"
            )
        if floor_id in self._hit_maps:
            return self._hit_maps[floor_id]

        (
            width,
            height,
            tile,
            parts,
            event,
            _digest,
            _kind,
            _event_status,
        ) = self.region_provider._stable_payload(floor_id)
        if event is None:
            raise ValueError("client collision requires recovered event plane")

        hit_map = build_client_hit_map(
            width=int(width),
            height=int(height),
            tile=tile,
            parts=parts,
            event=event,
            profile=self.collision_profile,
        )
        definition = self.adapter.topology.maps[floor_id]
        if (hit_map.width, hit_map.height) != (
            int(definition.width),
            int(definition.height),
        ):
            raise ValueError("client collision hit-map/topology dimension drift")
        self._hit_maps[floor_id] = hit_map
        return hit_map

    def ordinary_step_verdict(
        self,
        *,
        origin: MapPosition,
        destination: MapPosition,
        skywalker: bool = False,
    ) -> CollisionDecision:
        if int(origin.floor_id) != int(destination.floor_id):
            return CollisionDecision(False, "floor_change_not_an_ordinary_step")

        dx = int(destination.x) - int(origin.x)
        dy = int(destination.y) - int(origin.y)
        if dx == 0 and dy == 0:
            return CollisionDecision(False, "zero_length_step")
        if abs(dx) > 1 or abs(dy) > 1:
            return CollisionDecision(False, "step_exceeds_one_cell")

        hit_map = self._hit_map(int(origin.floor_id))
        x, y = int(destination.x), int(destination.y)
        if not (0 <= x < hit_map.width and 0 <= y < hit_map.height):
            return CollisionDecision(False, "destination_out_of_bounds")
        if bool(skywalker):
            return CollisionDecision(True)
        if hit_map.blocked_at(x, y):
            return CollisionDecision(False, "client_hitmap_blocked")
        return CollisionDecision(True)

    def cache_status(self) -> Mapping[str, int]:
        return MappingProxyType(
            {
                "supported_floors": len(self.fallback_floor_ids),
                "materialized_hit_maps": len(self._hit_maps),
                "collision_attributes": len(
                    self.collision_profile.by_map_number
                ),
            }
        )
