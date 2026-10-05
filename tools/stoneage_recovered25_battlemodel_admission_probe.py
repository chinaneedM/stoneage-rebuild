"""Verify runtime admission against hash-verified recovered data; derived output only."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from types import SimpleNamespace

from tools.stoneage_enemy_ai_battlemodel_bridge import (
    EXPECTED_TEMPLATE_IDENTITIES, resolve_enemy_ai_battlemodel_submission,
    validate_recovered25_battlemodel_population,
)
from tools.stoneage_enemy_ai_2battletimid_bridge import (
    resolve_enemy_ai_2battletimid_submission,
)
from tools.stoneage_battlemodel_reference_model import (
    BASE_STATUS_LITERALS_BY_SOURCE, PROFILE_BIG5, PROFILE_UTF8,
)
from tools.stoneage_recovered25_battlemodel_probe import EXPECTED_PETSKILL_SHA256
from tools.stoneage_recovered25_petskill_runtime import load_recovered25_petskill_runtime
from tools.stoneage_recovered25_enemybase_runtime import load_recovered25_enemybase_runtime
from tools.stoneage_recovered25_2battletimid_probe import EXPECTED_TEMPLATE_ROWS as TIMID_ROWS


def analyze_admission(petskills, enemybase) -> tuple[int, int]:
    validate_recovered25_battlemodel_population(petskills)
    observed = sorted((tempno, index, skill)
                      for tempno, template in enemybase.templates.items()
                      for index, skill in enumerate(template.skill_slot_ids)
                      if skill in (638, 641, 649, 650))
    expected = sorted((tempno, index, skill)
                      for tempno, (_graphic, _base, allowed) in EXPECTED_TEMPLATE_IDENTITIES.items()
                      for index, skill in allowed.items())
    if observed != expected:
        raise ValueError("BattleModel complete positive placement drift")
    count = 0
    for tempno, slot, _skill in expected:
        spawned = SimpleNamespace(template=enemybase.templates[tempno], participant=SimpleNamespace(
            participant_id=f"probe:{tempno}", kind="enemy", side="enemy",
        ))
        for profile in (PROFILE_BIG5, PROFILE_UTF8):
            for source in BASE_STATUS_LITERALS_BY_SOURCE:
                for before, big5_after in (((100, 80, 60), (70, 80, 60)),
                                           ((137, 91, 53), (96, 91, 53))):
                    submission = resolve_enemy_ai_battlemodel_submission(
                        spawned, skill_slot=slot, target_slot=5, petskill_runtime=petskills,
                        profile=profile, source_profile=source, powers_before=before,
                    )
                    shape = submission.option_shape
                    expected_power = big5_after if profile == PROFILE_BIG5 else before
                    expected_status = 2 if profile == PROFILE_BIG5 else None
                    if (submission.setup.powers != expected_power
                        or submission.setup.object_count != 4 or submission.setup.attack_type != 5
                        or submission.setup.rng_draws != 0 or shape.status_index != expected_status
                        or shape.turn_value != 1 or shape.hit_value != 30
                        or shape.action_numbers != (101867, 101868)):
                        raise ValueError("BattleModel accepted conditional setup/shape drift")
                    plan = submission.target_plan(living_opposing_slots=(0, 5), excess_target_rolls=(0, 1))
                    if tuple(a.target_slot for a in plan.attacks) != (0, 5, 0, 5):
                        raise ValueError("BattleModel target-plan seam drift")
                    count += 1

    observed_timid = sorted((tempno, index, skill)
                           for tempno, template in enemybase.templates.items()
                           for index, skill in enumerate(template.skill_slot_ids) if skill == 636)
    expected_timid = sorted((tempno, slot - 1, skill)
                           for tempno, _graphic, slots, skills in TIMID_ROWS
                           for slot, skill in zip(slots, skills))
    if observed_timid != expected_timid:
        raise ValueError("2BattleTimid complete positive placement drift")
    timid_count = 0
    for tempno, slot, _skill in expected_timid:
        spawned = SimpleNamespace(template=enemybase.templates[tempno], participant=SimpleNamespace(
            participant_id=f"probe:{tempno}", kind="enemy", side="enemy",
        ))
        for profile in (PROFILE_BIG5, PROFILE_UTF8):
            submission = resolve_enemy_ai_2battletimid_submission(
                spawned, skill_slot=slot, target_slot=5, petskill_runtime=petskills,
                profile=profile, fixed_strength=200, fixed_toughness=80, fixed_dex=100,
            )
            if submission.skill_slot != 2 or submission.skill_id != 636:
                raise ValueError("2BattleTimid runtime slot-base drift")
            timid_count += 1
    return count, timid_count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--setup", type=Path)
    args = parser.parse_args()
    petskills = load_recovered25_petskill_runtime(data_dir=args.data_dir, setup=args.setup)
    digest = hashlib.sha256((args.data_dir / petskills.source_file).read_bytes()).hexdigest()
    if digest != EXPECTED_PETSKILL_SHA256:
        raise ValueError("complete recovered25 petskill identity drift")
    enemybase = load_recovered25_enemybase_runtime(data_dir=args.data_dir, setup=args.setup)
    battlemodel, timid = analyze_admission(petskills, enemybase)
    print("StoneAge recovered25 runtime admission — derived facts only")
    print(f"DATA_SHA256|petskill={digest}")
    print(f"COUNT|battlemodel_conditional_admissions={battlemodel}")
    print(f"COUNT|2battletimid_corrected_admissions={timid}")
    print("FACT|report_skill_column3_maps_to_runtime_index2")
    print("RESOLUTION|RECOVERED25_BATTLEMODEL_ADMISSION_AND_2BATTLETIMID_SLOT_BASE_PASS")
    print("BOUNDARY|typed_setup_and_target_plan_only_full_BattleModel_ordered_runtime_OPEN")


if __name__ == "__main__":
    main()
