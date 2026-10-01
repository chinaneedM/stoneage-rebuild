#!/usr/bin/env python3
"""Smoke the recovered25 AttackMagic runtime index against a verified bundle."""

from __future__ import annotations

import argparse
from pathlib import Path

from tools.stoneage_recovered25_attack_magic_runtime import (
    NONPLAYER_ITEM_ROLE,
    load_recovered25_attack_magic_runtime,
)


def emit(data_dir: Path, setup: Path | None = None) -> None:
    runtime = load_recovered25_attack_magic_runtime(
        data_dir=data_dir,
        setup=setup,
    )
    fully_alive = tuple(range(10))
    scenarios = 0
    portable = 0
    always_portable = []
    for entry in runtime.entries.values():
        entry_portable = 0
        for target in range(10):
            plan = runtime.resolve_enemy_footprint(
                skill_id=entry.skill_id,
                actor_slot=15,
                target_slot=target,
                alive_player_slots=fully_alive,
                require_exact_source_order=False,
            )
            scenarios += 1
            if plan.source_sort_portable:
                portable += 1
                entry_portable += 1
        if entry_portable == 10:
            always_portable.append(entry.magic_id)

    dynamic_skill = runtime.skill_id_for_magic(305)
    dynamic = runtime.resolve_enemy_footprint(
        skill_id=dynamic_skill,
        actor_slot=15,
        target_slot=0,
        alive_player_slots=(0,),
    )

    print("StoneAge recovered25 AttackMagic runtime index — R1")
    print("No recovered names/comments/options or binary payload bytes stored.")
    print(f"COUNT|attackmagic_entries|{len(runtime.entries)}")
    print(f"COUNT|full_side_scenarios|{scenarios}")
    print(f"COUNT|full_side_source_sort_portable|{portable}")
    print(f"COUNT|full_side_source_sort_nonportable|{scenarios - portable}")
    print(
        "FULL_SIDE_ALWAYS_PORTABLE_MAGIC_IDS|"
        + ",".join(str(x) for x in sorted(always_portable))
    )
    print(
        "ITEM_CONFIG_MAGICUSEMP_SET|"
        + ",".join(
            str(x)
            for x in sorted(
                {entry.item_magicusemp for entry in runtime.entries.values()}
            )
        )
    )
    print(f"NONPLAYER_ITEM_RUNTIME_ROLE|{runtime.nonplayer_item_role}")
    print(
        "DYNAMIC_PORTABILITY_WITNESS|"
        f"magic=305|alive=1|targets={len(dynamic.target_membership)}|"
        f"portable={int(dynamic.source_sort_portable)}"
    )
    closed = (
        len(runtime.entries) == 25
        and scenarios == 250
        and portable == 110
        and scenarios - portable == 140
        and runtime.nonplayer_item_role == NONPLAYER_ITEM_ROLE
        and {entry.item_magicusemp for entry in runtime.entries.values()} == {5}
        and dynamic.source_sort_portable
    )
    print(
        "RESOLUTION|"
        + (
            "RECOVERED25_ATTACKMAGIC_RUNTIME_INDEX_CLOSED"
            if closed
            else "RECOVERED25_ATTACKMAGIC_RUNTIME_INDEX_OPEN"
        )
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=Path, required=True)
    ap.add_argument("--setup", type=Path)
    args = ap.parse_args()
    emit(args.data_dir, args.setup)


if __name__ == "__main__":
    main()
