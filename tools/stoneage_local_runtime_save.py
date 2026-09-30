#!/usr/bin/env python3
"""Versioned local-runtime save snapshot with occupancy deltas.

The existing stoneage.local-runtime-session.r1 payload remains the authoritative
player/session envelope. This module wraps it without changing that schema and
adds only live occupancy state that differs from the deterministic initial
occupancy baseline supplied by the runtime stack.

Static collision is intentionally absent from this save contract.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Mapping

from tools.stoneage_local_runtime_core import (
    LocalRuntimeSessionState,
    dump_local_runtime_session,
    load_local_runtime_session,
)
from tools.stoneage_runtime_occupancy_registry import (
    LIVE_OCCUPANCY_STATE_PROFILE,
    LiveRuntimeObject,
    RuntimeDynamicOccupancyRegistry,
)
from tools.stoneage_singleplayer_domain import MapPosition


LOCAL_RUNTIME_SAVE_SCHEMA = "stoneage.local-runtime-save.r1"
EMPTY_INITIAL_OCCUPANCY_PROFILE = "STONEAGE_EMPTY_INITIAL_OCCUPANCY_R1"


def _nonempty(value: object, label: str) -> str:
    text = str(value).strip()
    if not text:
        raise ValueError(f"{label} must be non-empty")
    return text


def _initial_profile_id(initial_occupancy: object | None) -> str:
    if initial_occupancy is None:
        return EMPTY_INITIAL_OCCUPANCY_PROFILE
    return _nonempty(
        getattr(initial_occupancy, "profile_id", ""),
        "initial occupancy profile_id",
    )


def build_initial_occupancy_registry(
    initial_occupancy: object | None,
) -> RuntimeDynamicOccupancyRegistry:
    registry = RuntimeDynamicOccupancyRegistry()
    if initial_occupancy is None:
        return registry
    populate = getattr(initial_occupancy, "populate_registry", None)
    if not callable(populate):
        raise TypeError("initial occupancy profile lacks populate_registry")
    populate(registry)
    return registry


@dataclass(frozen=True)
class LocalRuntimeOccupancyDelta:
    base_profile_id: str
    registry_profile_id: str
    removed_base_object_ids: tuple[str, ...]
    upserts: tuple[LiveRuntimeObject, ...]

    def __post_init__(self) -> None:
        base_profile_id = _nonempty(
            self.base_profile_id,
            "occupancy base profile",
        )
        registry_profile_id = _nonempty(
            self.registry_profile_id,
            "occupancy registry profile",
        )
        if registry_profile_id != LIVE_OCCUPANCY_STATE_PROFILE:
            raise ValueError("occupancy registry profile drift")

        removed_raw = tuple(
            _nonempty(value, "removed occupancy object id")
            for value in self.removed_base_object_ids
        )
        if len(removed_raw) != len(set(removed_raw)):
            raise ValueError("duplicate removed occupancy object id")
        removed = tuple(sorted(removed_raw))

        upserts_raw = tuple(self.upserts)
        if any(not isinstance(row, LiveRuntimeObject) for row in upserts_raw):
            raise TypeError("occupancy upserts must be LiveRuntimeObject values")
        ids = [row.object_id for row in upserts_raw]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate occupancy upsert object id")
        upserts = tuple(sorted(upserts_raw, key=lambda row: row.object_id))
        if set(removed) & set(ids):
            raise ValueError("occupancy object cannot be both removed and upserted")

        object.__setattr__(self, "base_profile_id", base_profile_id)
        object.__setattr__(self, "registry_profile_id", registry_profile_id)
        object.__setattr__(self, "removed_base_object_ids", removed)
        object.__setattr__(self, "upserts", upserts)


@dataclass(frozen=True)
class LocalRuntimeSaveSnapshot:
    session: LocalRuntimeSessionState
    occupancy: LocalRuntimeOccupancyDelta

    def __post_init__(self) -> None:
        if not isinstance(self.session, LocalRuntimeSessionState):
            raise TypeError("save snapshot session must be LocalRuntimeSessionState")
        if not isinstance(self.occupancy, LocalRuntimeOccupancyDelta):
            raise TypeError("save snapshot occupancy must be LocalRuntimeOccupancyDelta")


def build_local_runtime_occupancy_delta(
    *,
    registry: RuntimeDynamicOccupancyRegistry,
    initial_occupancy: object | None,
) -> LocalRuntimeOccupancyDelta:
    if not isinstance(registry, RuntimeDynamicOccupancyRegistry):
        raise TypeError("occupancy delta requires RuntimeDynamicOccupancyRegistry")

    base_registry = build_initial_occupancy_registry(initial_occupancy)
    base = dict(base_registry.objects)
    live = dict(registry.objects)

    removed = tuple(sorted(set(base) - set(live)))
    upserts = tuple(
        live[object_id]
        for object_id in sorted(live)
        if object_id not in base or live[object_id] != base[object_id]
    )
    return LocalRuntimeOccupancyDelta(
        base_profile_id=_initial_profile_id(initial_occupancy),
        registry_profile_id=registry.profile_id,
        removed_base_object_ids=removed,
        upserts=upserts,
    )


def restore_local_runtime_occupancy_registry(
    *,
    delta: LocalRuntimeOccupancyDelta,
    initial_occupancy: object | None,
) -> RuntimeDynamicOccupancyRegistry:
    if not isinstance(delta, LocalRuntimeOccupancyDelta):
        raise TypeError("occupancy restore requires LocalRuntimeOccupancyDelta")
    expected_profile = _initial_profile_id(initial_occupancy)
    if delta.base_profile_id != expected_profile:
        raise ValueError(
            "local save occupancy base-profile mismatch: "
            f"{delta.base_profile_id} != {expected_profile}"
        )
    if delta.registry_profile_id != LIVE_OCCUPANCY_STATE_PROFILE:
        raise ValueError("local save occupancy registry-profile mismatch")

    registry = build_initial_occupancy_registry(initial_occupancy)
    base_ids = set(registry.objects)
    unknown_removed = set(delta.removed_base_object_ids) - base_ids
    if unknown_removed:
        raise ValueError(
            "local save removes occupancy objects absent from deterministic base"
        )
    for object_id in delta.removed_base_object_ids:
        registry.remove(object_id)
    for obj in delta.upserts:
        registry.upsert(obj)
    return registry


def _dump_live_object(obj: LiveRuntimeObject) -> dict[str, Any]:
    return {
        "object_id": obj.object_id,
        "kind": obj.kind,
        "position": {
            "floor_id": int(obj.position.floor_id),
            "x": int(obj.position.x),
            "y": int(obj.position.y),
        },
        "overable": bool(obj.overable),
        "provenance": obj.provenance,
    }


def _load_live_object(payload: Mapping[str, Any]) -> LiveRuntimeObject:
    expected = {"object_id", "kind", "position", "overable", "provenance"}
    if set(payload) != expected:
        raise ValueError("live occupancy object has unexpected shape")
    position = payload["position"]
    if not isinstance(position, Mapping) or set(position) != {
        "floor_id",
        "x",
        "y",
    }:
        raise ValueError("live occupancy position has unexpected shape")
    if not isinstance(payload["overable"], bool):
        raise ValueError("live occupancy overable must be boolean")
    return LiveRuntimeObject(
        object_id=_nonempty(payload["object_id"], "occupancy object_id"),
        kind=_nonempty(payload["kind"], "occupancy kind"),
        position=MapPosition(
            int(position["floor_id"]),
            int(position["x"]),
            int(position["y"]),
        ),
        overable=payload["overable"],
        provenance=_nonempty(payload["provenance"], "occupancy provenance"),
    )


def dump_local_runtime_save(
    snapshot: LocalRuntimeSaveSnapshot,
) -> dict[str, Any]:
    if not isinstance(snapshot, LocalRuntimeSaveSnapshot):
        raise TypeError("save dump requires LocalRuntimeSaveSnapshot")
    return {
        "schema": LOCAL_RUNTIME_SAVE_SCHEMA,
        "session": dump_local_runtime_session(snapshot.session),
        "occupancy": {
            "base_profile_id": snapshot.occupancy.base_profile_id,
            "registry_profile_id": snapshot.occupancy.registry_profile_id,
            "removed_base_object_ids": list(
                snapshot.occupancy.removed_base_object_ids
            ),
            "upserts": [
                _dump_live_object(obj)
                for obj in snapshot.occupancy.upserts
            ],
        },
    }


def encode_local_runtime_save(snapshot: LocalRuntimeSaveSnapshot) -> str:
    return json.dumps(
        dump_local_runtime_save(snapshot),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def load_local_runtime_save(
    payload: Mapping[str, Any],
    *,
    expected_contract_id: str | None = None,
    expected_world_profile: str | None = None,
) -> LocalRuntimeSaveSnapshot:
    if set(payload) != {"schema", "session", "occupancy"}:
        raise ValueError("local runtime save has unexpected shape")
    if payload["schema"] != LOCAL_RUNTIME_SAVE_SCHEMA:
        raise ValueError(
            f"unsupported local runtime save schema: {payload['schema']}"
        )
    session_payload = payload["session"]
    occupancy_payload = payload["occupancy"]
    if not isinstance(session_payload, Mapping):
        raise ValueError("local runtime save session must be an object")
    if not isinstance(occupancy_payload, Mapping) or set(occupancy_payload) != {
        "base_profile_id",
        "registry_profile_id",
        "removed_base_object_ids",
        "upserts",
    }:
        raise ValueError("local runtime save occupancy has unexpected shape")

    removed = occupancy_payload["removed_base_object_ids"]
    upserts = occupancy_payload["upserts"]
    if not isinstance(removed, list):
        raise ValueError("removed occupancy ids must be a list")
    if not isinstance(upserts, list):
        raise ValueError("occupancy upserts must be a list")
    if any(not isinstance(row, Mapping) for row in upserts):
        raise ValueError("occupancy upsert rows must be objects")

    session = load_local_runtime_session(
        session_payload,
        expected_contract_id=expected_contract_id,
        expected_world_profile=expected_world_profile,
    )
    occupancy = LocalRuntimeOccupancyDelta(
        base_profile_id=_nonempty(
            occupancy_payload["base_profile_id"],
            "occupancy base profile",
        ),
        registry_profile_id=_nonempty(
            occupancy_payload["registry_profile_id"],
            "occupancy registry profile",
        ),
        removed_base_object_ids=tuple(
            _nonempty(value, "removed occupancy object id")
            for value in removed
        ),
        upserts=tuple(_load_live_object(row) for row in upserts),
    )
    return LocalRuntimeSaveSnapshot(session=session, occupancy=occupancy)


def decode_local_runtime_save(
    data: str,
    *,
    expected_contract_id: str | None = None,
    expected_world_profile: str | None = None,
) -> LocalRuntimeSaveSnapshot:
    try:
        payload = json.loads(str(data))
    except json.JSONDecodeError as exc:
        raise ValueError("invalid local runtime save JSON") from exc
    if not isinstance(payload, Mapping):
        raise ValueError("local runtime save root must be an object")
    return load_local_runtime_save(
        payload,
        expected_contract_id=expected_contract_id,
        expected_world_profile=expected_world_profile,
    )


def local_runtime_payload_schema(data: str) -> str:
    try:
        payload = json.loads(str(data))
    except json.JSONDecodeError as exc:
        raise ValueError("invalid local persistence JSON") from exc
    if not isinstance(payload, Mapping):
        raise ValueError("local persistence root must be an object")
    return _nonempty(payload.get("schema", ""), "local persistence schema")
