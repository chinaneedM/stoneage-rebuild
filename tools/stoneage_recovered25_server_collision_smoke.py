#!/usr/bin/env python3
"""Bundle-backed smoke for recovered25 server collision runtime binding.

Only aggregate closure facts are emitted. Raw map planes, mapset rows and
movement coordinates are not persisted.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from types import MappingProxyType

from tools.stoneage_local_runtime_core import (
    LocalRuntimeSessionState,
    load_runtime_bootstrap_file,
)
from tools.stoneage_local_runtime_session_coordinator import (
    InMemoryLocalPersistenceStore,
    LocalRuntimeSessionCoordinator,
)
from tools.stoneage_recovered25_local_runtime_stack import (
    Recovered25LocalRuntimeStack,
)
from tools.stoneage_recovered25_server_collision_provider import (
    DIVERGENT_SERVER_DUPLICATE,
    NO_SERVER_MAP,
)
from tools.stoneage_singleplayer_domain import (
    MapPosition,
    PersistentPlayerState,
    PlayerState,
)


OUTPUT_RESOLUTION = "RESOLUTION|RECOVERED25_SERVER_COLLISION_PROVIDER_CLOSED_WITH_GAPS"


def _player_state(_ordinal: int) -> PersistentPlayerState:
    return PersistentPlayerState(
        character=PlayerState(
            MappingProxyType({"name": "collision-smoke", "level": 1})
        )
    )


def _find_allowed_step(stack: Recovered25LocalRuntimeStack):
    provider = stack.collision_provider
    if provider is None:
        raise ValueError("runtime stack lacks collision provider")

    for floor_id in sorted(provider.supported_floor_ids):
        definition = stack.world_adapter.topology.maps[floor_id]
        width, height = int(definition.width), int(definition.height)
        # Bound the search by trying every cell if necessary, but stop at the
        # first cardinal step accepted by the recovered server collision layer.
        for y in range(height):
            for x in range(width):
                destination = MapPosition(floor_id, x, y)
                neighbors = (
                    (x - 1, y),
                    (x + 1, y),
                    (x, y - 1),
                    (x, y + 1),
                )
                for ox, oy in neighbors:
                    if not (0 <= ox < width and 0 <= oy < height):
                        continue
                    origin = MapPosition(floor_id, ox, oy)
                    verdict = provider.ordinary_step_verdict(
                        origin=origin,
                        destination=destination,
                    )
                    if verdict.allowed:
                        return origin, destination
    raise ValueError("no allowed recovered25 server-collision step found")


def run(
    *,
    client_dat_dir: Path,
    npc_dir: Path,
    setup: Path,
    server_map_root: Path,
    mapset_path: Path,
):
    root = Path(__file__).resolve().parents[1]
    profile = load_runtime_bootstrap_file(
        root / "game" / "RUNTIME-BOOTSTRAP-RECOVERED25-R1.json"
    )
    stack = Recovered25LocalRuntimeStack.from_verified_bundle(
        profile=profile,
        player_state_factory=_player_state,
        client_dat_dir=client_dat_dir,
        npc_dir=npc_dir,
        setup=setup,
        server_map_root=server_map_root,
        mapset_path=mapset_path,
    )
    provider = stack.collision_provider
    if provider is None:
        raise ValueError("collision provider was not composed into runtime stack")
    counts = provider.coverage_counts()

    if counts["materializable_floors"] != 826:
        raise ValueError("materializable collision floor count drift")
    if counts["server_collision_closed"] != 635:
        raise ValueError("server collision closed-floor count drift")
    if counts["server_collision_uncovered"] != 191:
        raise ValueError("server collision uncovered-floor count drift")
    if counts[NO_SERVER_MAP] != 189:
        raise ValueError("no-server collision floor count drift")
    if counts[DIVERGENT_SERVER_DUPLICATE] != 2:
        raise ValueError("divergent collision floor count drift")

    origin, destination = _find_allowed_step(stack)
    seed = stack.create_fresh_start(1)
    session = LocalRuntimeSessionState(
        contract_id=profile.contract_id,
        world_profile=profile.runtime_world_profile,
        hometown_ordinal=seed.hometown_ordinal,
        player_position=origin,
        player_state=seed.player_state,
    )
    coordinator = LocalRuntimeSessionCoordinator(
        stack=stack,
        persistence=InMemoryLocalPersistenceStore(),
    )
    moved = coordinator.walk_one_cell_with_server_collision(
        session,
        destination=destination,
    )
    movement_witness = int(moved.resolution.moved)
    if not movement_witness or moved.collision is None or not moved.collision.allowed:
        raise ValueError("server-backed coordinator movement witness failed")

    unsupported_floor = min(provider.unsupported_floor_ids)
    definition = stack.world_adapter.topology.maps[unsupported_floor]
    hard_reject = 0
    try:
        provider.ordinary_step_verdict(
            origin=MapPosition(unsupported_floor, 0, 0),
            destination=MapPosition(
                unsupported_floor,
                min(1, int(definition.width) - 1),
                0,
            ),
        )
    except ValueError:
        hard_reject = 1
    if not hard_reject:
        raise ValueError("uncovered collision floor did not fail closed")

    return counts, movement_witness, hard_reject


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--client-dat-dir", type=Path, required=True)
    ap.add_argument("--npc-dir", type=Path, required=True)
    ap.add_argument("--setup", type=Path, required=True)
    ap.add_argument("--server-map-root", type=Path, required=True)
    ap.add_argument("--mapset", type=Path, required=True)
    args = ap.parse_args()

    counts, movement_witness, hard_reject = run(
        client_dat_dir=args.client_dat_dir,
        npc_dir=args.npc_dir,
        setup=args.setup,
        server_map_root=args.server_map_root,
        mapset_path=args.mapset,
    )
    print("StoneAge recovered25 server collision runtime provider — R1")
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|recovered server LS2MAP + recovered mapset only; "
        "uncovered floors fail closed"
    )
    print(f"COUNT|materializable_floors|{counts['materializable_floors']}")
    print(f"COUNT|server_collision_closed|{counts['server_collision_closed']}")
    print(f"COUNT|server_collision_uncovered|{counts['server_collision_uncovered']}")
    print(f"COUNT|status:NO_SERVER_MAP|{counts[NO_SERVER_MAP]}")
    print(
        "COUNT|status:DIVERGENT_SERVER_DUPLICATE|"
        f"{counts[DIVERGENT_SERVER_DUPLICATE]}"
    )
    print(f"SERVER_BACKED_MOVEMENT_WITNESS|{movement_witness}")
    print(f"UNCOVERED_FAIL_CLOSED_WITNESS|{hard_reject}")
    print(OUTPUT_RESOLUTION)


if __name__ == "__main__":
    main()
