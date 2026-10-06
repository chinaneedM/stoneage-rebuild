"""Pure, exact ID638 placement capability; never command-entry admission.

The file-verification factory binds complete loaded semantics to pinned raw
files. A detached hash string or forged callback token is not a certificate.
Original OPTIONs stay transient; only their digests enter the binding.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path

from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillRuntime, _active_petskill_path, load_recovered25_petskill_runtime,
)
from tools.stoneage_recovered25_enemybase_runtime import (
    Recovered25EnemybaseRuntime, _active_enemybase_path, load_recovered25_enemybase_runtime,
)
from tools.stoneage_recovered25_battlemodel_probe import EXPECTED_PETSKILL_SHA256
from tools.stoneage_enemy_ai_battlemodel_bridge import (
    CALLBACK_NAME, EXPECTED_CALLBACK_IDS, EXPECTED_TEMPLATE_IDENTITIES,
    validate_recovered25_battlemodel_population, _validate_template,
)

EXPECTED_ENEMYBASE_SHA256 = "1be7d5226798f7abaabe1f1e74aa1533fcd10e3eaf43f6497d63afa91df3e8b7"
CONDITIONAL_CAPABILITY_SCOPE = "ID638_enemy_explicit_selected_empty_equipment_bounded_runtime_R1"
CONDITIONAL_CAPABILITY_KIND = "CONDITIONAL_BOUNDED_CAPABILITY"


def _semantic_identity(petskills, enemybase):
    if not isinstance(petskills, Recovered25PetSkillRuntime) or not isinstance(enemybase, Recovered25EnemybaseRuntime):
        raise TypeError("typed recovered25 population required")
    skills = []
    for key, entry in sorted(petskills.skills.items()):
        row = asdict(entry)
        row["option_bytes"] = hashlib.sha256(entry.option_bytes).hexdigest()
        skills.append((key, row))
    content = dict(skills=skills, source_file=petskills.source_file,
        source_version=(petskills.source_version, enemybase.source_version),
        evidence_role=(petskills.evidence_role, enemybase.evidence_role),
        name_encoding_status=enemybase.name_encoding_status,
        templates=[(key, asdict(template)) for key, template in sorted(enemybase.templates.items())])
    return hashlib.sha256(json.dumps(content, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


@dataclass(frozen=True, init=False)
class VerifiedPlacementPopulation:
    petskill_sha256: str
    enemybase_sha256: str
    semantic_sha256: str

    def __init__(self):
        raise TypeError("use verify_placement_population with exact source files")


def verify_placement_population(petskills, enemybase, *, data_dir: Path, setup: Path | None):
    """Reparse pinned files and bind caller objects; no caller-asserted hashes.

    Both files are checked before and after parsing to detect replacement
    during verification. Replaced/stale objects cannot reuse this certificate.
    This is evidence identity, not a Python-process security boundary.
    """
    paths = (_active_petskill_path(Path(data_dir), setup), _active_enemybase_path(Path(data_dir), setup))
    expected = (EXPECTED_PETSKILL_SHA256, EXPECTED_ENEMYBASE_SHA256)
    def check():
        actual = tuple(hashlib.sha256(path.read_bytes()).hexdigest() for path in paths)
        if actual != expected:
            raise ValueError("BattleModel placement whole-file identity drift")
    check()
    loaded = (load_recovered25_petskill_runtime(data_dir=data_dir, setup=setup),
              load_recovered25_enemybase_runtime(data_dir=data_dir, setup=setup))
    identity = _semantic_identity(*loaded)
    if _semantic_identity(petskills, enemybase) != identity:
        raise ValueError("BattleModel placement loaded-object identity drift")
    check()
    certificate = object.__new__(VerifiedPlacementPopulation)
    for key, value in zip(("petskill_sha256", "enemybase_sha256", "semantic_sha256"), (*expected, identity)):
        object.__setattr__(certificate, key, value)
    return certificate


def conditional_battlemodel_placements(petskills, enemybase, *, identity=None,
                                      scope=CONDITIONAL_CAPABILITY_SCOPE):
    """Return exact qualified (template, runtime-slot, skill-ID) triples.

    Incomplete/drifted populations stay OPEN as a whole. This pure capability
    predicate does not issue commands or certify an AI weight, actor's work,
    RNG/status/death composition or natural encounter. Those remain subject
    to the accepted explicit runtime scopes and separate entry audit.
    """
    if type(identity) is not VerifiedPlacementPopulation or type(scope) is not str or scope != CONDITIONAL_CAPABILITY_SCOPE:
        return frozenset()
    try:
        if ((identity.petskill_sha256, identity.enemybase_sha256)
                != (EXPECTED_PETSKILL_SHA256, EXPECTED_ENEMYBASE_SHA256)
                or _semantic_identity(petskills, enemybase) != identity.semantic_sha256):
            return frozenset()
        validate_recovered25_battlemodel_population(petskills)
        observed = {(tempno, slot, skill) for tempno, template in enemybase.templates.items()
                    for slot, skill in enumerate(template.skill_slot_ids) if skill in EXPECTED_CALLBACK_IDS}
        expected = {(tempno, slot, skill) for tempno, (_graphic, _base, slots) in EXPECTED_TEMPLATE_IDENTITIES.items()
                    for slot, skill in slots.items()}
        if observed != expected:
            return frozenset()
        for tempno, slot, skill in expected:
            template = enemybase.templates[tempno]
            if petskills.skills[skill].function_name != CALLBACK_NAME:
                return frozenset()
            _validate_template(tempno, template.graphic_id,
                (template.base_vital, template.base_strength, template.base_toughness, template.base_dexterity, template.ai),
                tuple(template.skill_slot_ids), slot)
        return frozenset(expected)
    except (ValueError, TypeError, KeyError, AttributeError):
        return frozenset()
