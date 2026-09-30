#!/usr/bin/env python3
"""Recovered25 enemybase numeric runtime bridge.

Display-name decoding is deliberately excluded while the active enemybase
CP950-vs-Big5 ambiguity remains open. Numeric/template mechanics are still
loaded with explicit recovered25 provenance.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_enemybase_probe import parse_file, setup_value
from tools.stoneage_singleplayer_world import LATER_RECOVERED
from tools.stoneage_tw10_25_bridge_model import PetTemplateBridge
from tools.stoneage_versioned_encounter_runtime import (
    VersionedEncounterRuntimeAdapter,
)


SOURCE_VERSION = "recovered25"
NAME_ENCODING_STATUS = "OPEN_CP950_BIG5_TWO_ROW_AMBIGUITY"


@dataclass(frozen=True)
class Recovered25EnemybaseRuntime:
    templates: Mapping[int, PetTemplateBridge]
    source_version: str = SOURCE_VERSION
    evidence_role: str = LATER_RECOVERED
    name_encoding_status: str = NAME_ENCODING_STATUS

    def __post_init__(self) -> None:
        templates = {int(key): value for key, value in self.templates.items()}
        if self.source_version != SOURCE_VERSION:
            raise ValueError("enemybase runtime source-version drift")
        if self.evidence_role != LATER_RECOVERED:
            raise ValueError("enemybase runtime must remain LATER_RECOVERED")
        for key, template in templates.items():
            if key != int(template.tempno):
                raise ValueError(
                    f"enemybase template key {key} != TEMPNO {template.tempno}"
                )
            if template.name is not None:
                raise ValueError(
                    "R1 recovered25 enemybase runtime must not guess decoded names"
                )
        object.__setattr__(self, "templates", MappingProxyType(templates))

    def referenced_template_ids(
        self,
        encounter: VersionedEncounterRuntimeAdapter,
    ) -> tuple[int, ...]:
        group_ids = {
            int(group_id)
            for area in encounter.encounter_areas
            for group_id, weight in area.group_slots
            if int(group_id) >= 0
            and int(weight) > 0
            and int(group_id) in encounter.groups
        }
        enemy_ids = {
            int(enemy_id)
            for group_id in group_ids
            for enemy_id, _weight in encounter.groups[group_id].enemy_slots
            if int(enemy_id) >= 0
        }
        missing_enemy_ids = tuple(
            sorted(enemy_id for enemy_id in enemy_ids if enemy_id not in encounter.enemies)
        )
        if missing_enemy_ids:
            raise ValueError(
                "stable encounter groups reference unresolved enemy IDs"
            )
        return tuple(
            sorted({
                int(encounter.enemies[enemy_id].tempno)
                for enemy_id in enemy_ids
            })
        )

    def unresolved_template_ids(
        self,
        encounter: VersionedEncounterRuntimeAdapter,
    ) -> tuple[int, ...]:
        return tuple(
            tempno
            for tempno in self.referenced_template_ids(encounter)
            if tempno not in self.templates
        )


def _active_enemybase_path(data_dir: Path, setup: Path | None) -> Path:
    configured = setup_value(setup, "enemybasefile")
    name = (
        Path(configured.replace("\\", "/")).name
        if configured
        else "enemybase.txt"
    )
    path = Path(data_dir) / name
    if not path.is_file():
        raise ValueError(f"active recovered25 enemybase file not found: {name}")
    return path


def load_recovered25_enemybase_runtime(
    *,
    data_dir: Path,
    setup: Path | None = None,
) -> Recovered25EnemybaseRuntime:
    """Load numeric/template semantics without decoding display names."""

    data_dir = Path(data_dir)
    if not data_dir.is_dir():
        raise ValueError("recovered25 enemybase data_dir must be a directory")
    if setup is not None and not Path(setup).is_file():
        raise ValueError("recovered25 enemybase setup must be a file")

    path = _active_enemybase_path(data_dir, setup)
    rows, _field_counts, malformed, raw_rows, _profiles = parse_file(path)
    if malformed or len(rows) != len(raw_rows):
        raise ValueError(
            "active recovered25 enemybase source has malformed rows"
        )

    templates: dict[int, PetTemplateBridge] = {}
    for row in rows:
        source = dict(row)
        # NAME is intentionally unresolved. The separate encoding audit proves
        # two active rows have CP950/Big5 mapping ambiguity.
        source["NAME"] = None
        template = PetTemplateBridge.from_enemybase(source)
        if template.tempno in templates:
            raise ValueError(
                f"duplicate recovered25 enemybase TEMPNO {template.tempno}"
            )
        templates[template.tempno] = template

    return Recovered25EnemybaseRuntime(templates=templates)
