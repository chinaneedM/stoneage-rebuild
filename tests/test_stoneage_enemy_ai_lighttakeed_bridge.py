from types import SimpleNamespace
from dataclasses import replace
import unittest

from tools.stoneage_battle_damage_react_model import (
    DAMAGE_REACT_REFLEC,
    DAMAGE_REACT_VANISH,
)
from tools.stoneage_enemy_ai_lighttakeed_bridge import (
    PROFILE_BISMARCK_COPY_PLUS_ONE,
    PROFILE_GAVIN_IRIS_COPY,
    resolve_enemy_ai_lighttakeed_submission,
    validate_recovered25_lighttakeed_population,
)
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillEntry,
    Recovered25PetSkillRuntime,
)


def runtime(*, target=7, bad_610=None, omit_609=False):
    rows={}
    for skill_id,option in (
        (609,b"ABSROB"),
        (610,b"REFLEC"),
        (611,b"VANISH"),
    ):
        if omit_609 and skill_id==609:
            continue
        raw=bad_610 if skill_id==610 and bad_610 is not None else option
        rows[skill_id]=Recovered25PetSkillEntry(
            skill_id=skill_id,
            field=1,
            target=target,
            cost=2,
            illegal=5000,
            function_name="PETSKILL_Lighttakeed",
            option_bytes=raw,
        )
    return Recovered25PetSkillRuntime(rows,"petskill.txt")


def spawned(*,tempno=70,graphic=101550,slots=None,side="enemy",kind="enemy"):
    if slots is None:
        slots=(0,0,0,610,0,0,0)
    return SimpleNamespace(
        template=SimpleNamespace(
            tempno=tempno,
            graphic_id=graphic,
            skill_slot_ids=tuple(slots),
        ),
        participant=SimpleNamespace(
            participant_id="enemy-light",
            side=side,
            kind=kind,
        ),
    )


class EnemyAiLighttakeedBridgeTests(unittest.TestCase):
    def test_typed_submission_cannot_relabel_recovered_skill_effect_or_slot(self):
        # These records can enter the ordered runtime directly, bypassing the
        # raw-data bridge. A valid marker must still belong to the claimed ID.
        for skill_slot,skill_id,wrong_marker,wrong_slot in (
            (3,610,DAMAGE_REACT_VANISH,4),
            (4,611,DAMAGE_REACT_REFLEC,3),
        ):
            actor=spawned(tempno=157,graphic=101283,
                          slots=(0,0,0,610,611,0,0))
            row=resolve_enemy_ai_lighttakeed_submission(
                actor,skill_slot=skill_slot,target_slot=0,
                petskill_runtime=runtime(),profile=PROFILE_GAVIN_IRIS_COPY,
                fixed_strength=100,fixed_toughness=80,
            )
            with self.subTest(skill_id=skill_id,drift="marker"):
                with self.assertRaisesRegex(ValueError,"skill/marker identity"):
                    replace(row,marker_kind=wrong_marker)
            with self.subTest(skill_id=skill_id,drift="slot"):
                with self.assertRaisesRegex(ValueError,"skill/slot identity"):
                    replace(row,skill_slot=wrong_slot)

    def test_exact_complete_callback_population_is_required(self):
        validate_recovered25_lighttakeed_population(runtime())
        with self.assertRaisesRegex(ValueError,"population"):
            validate_recovered25_lighttakeed_population(runtime(omit_609=True))
        with self.assertRaisesRegex(ValueError,"metadata"):
            validate_recovered25_lighttakeed_population(runtime(target=6))
        with self.assertRaisesRegex(ValueError,"hash"):
            validate_recovered25_lighttakeed_population(runtime(bad_610=b"REFLEX"))

    def test_tempno70_slot4_admits_reflect_and_callback_work_powers(self):
        row=resolve_enemy_ai_lighttakeed_submission(
            spawned(),
            skill_slot=3,
            target_slot=0,
            petskill_runtime=runtime(),
            profile=PROFILE_GAVIN_IRIS_COPY,
            fixed_strength=101,
            fixed_toughness=99,
        )
        self.assertEqual(row.skill_id,610)
        self.assertEqual(row.marker_kind,DAMAGE_REACT_REFLEC)
        self.assertEqual(row.attack_power,70)
        self.assertEqual(row.defense_power,49)
        self.assertEqual(row.source_target_slot,0)

    def test_tempno157_exact_slots_admit_reflect_and_vanish(self):
        actor=spawned(
            tempno=157,
            graphic=101283,
            slots=(0,0,0,610,611,0,0),
        )
        ref=resolve_enemy_ai_lighttakeed_submission(
            actor,
            skill_slot=3,
            target_slot=2,
            petskill_runtime=runtime(),
            profile=PROFILE_BISMARCK_COPY_PLUS_ONE,
            fixed_strength=100,
            fixed_toughness=80,
        )
        vanish=resolve_enemy_ai_lighttakeed_submission(
            actor,
            skill_slot=4,
            target_slot=2,
            petskill_runtime=runtime(),
            profile=PROFILE_BISMARCK_COPY_PLUS_ONE,
            fixed_strength=100,
            fixed_toughness=80,
        )
        self.assertEqual(ref.marker_kind,DAMAGE_REACT_REFLEC)
        self.assertEqual(vanish.marker_kind,DAMAGE_REACT_VANISH)
        self.assertEqual((ref.skill_id,vanish.skill_id),(610,611))

    def test_zero_reference_id609_is_not_promoted_to_executable_enemy_use(self):
        actor=spawned(
            tempno=157,
            graphic=101283,
            slots=(0,0,0,610,609,0,0),
        )
        with self.assertRaisesRegex(ValueError,"exact positive"):
            resolve_enemy_ai_lighttakeed_submission(
                actor,
                skill_slot=4,
                target_slot=0,
                petskill_runtime=runtime(),
                profile=PROFILE_GAVIN_IRIS_COPY,
                fixed_strength=100,
                fixed_toughness=100,
            )

    def test_wrong_template_graphic_side_target_and_profile_fail_closed(self):
        common=dict(
            skill_slot=3,
            target_slot=0,
            petskill_runtime=runtime(),
            profile=PROFILE_GAVIN_IRIS_COPY,
            fixed_strength=100,
            fixed_toughness=100,
        )
        with self.assertRaisesRegex(ValueError,"graphic"):
            resolve_enemy_ai_lighttakeed_submission(
                spawned(graphic=1),**common
            )
        with self.assertRaisesRegex(ValueError,"enemy actors"):
            resolve_enemy_ai_lighttakeed_submission(
                spawned(side="player",kind="player"),**common
            )
        with self.assertRaisesRegex(ValueError,"target"):
            resolve_enemy_ai_lighttakeed_submission(
                spawned(),**{**common,"target_slot":10}
            )
        with self.assertRaisesRegex(ValueError,"profile"):
            resolve_enemy_ai_lighttakeed_submission(
                spawned(),**{**common,"profile":"original"}
            )


if __name__=="__main__":
    unittest.main()
