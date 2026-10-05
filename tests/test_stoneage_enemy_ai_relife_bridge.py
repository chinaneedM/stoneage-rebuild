import unittest
from types import SimpleNamespace

from tools.stoneage_enemy_ai_relife_bridge import (
    RECOVERED25_RELIFE_SKILL_ID,
    resolve_enemy_ai_relife_submission,
)
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillEntry,
    Recovered25PetSkillRuntime,
)


def runtime(*,field=1,target=2,cost=2,illegal=0,option=b""):
    return Recovered25PetSkillRuntime(
        skills={
            500:Recovered25PetSkillEntry(
                skill_id=500,
                field=field,
                target=target,
                cost=cost,
                illegal=illegal,
                function_name="ENEMYSKILL_ReLife",
                option_bytes=option,
            )
        },
        source_file="petskill.txt",
    )


def spawned(tempno=39,slot=4,graphic_id=None):
    ids=[0]*7
    ids[slot]=500
    graphics={39:100370,909:100071,1165:101814}
    if graphic_id is None:
        graphic_id=graphics.get(tempno,999999)
    return SimpleNamespace(
        participant=SimpleNamespace(participant_id="enemy:relife"),
        template=SimpleNamespace(
            tempno=tempno,
            graphic_id=graphic_id,
            skill_slot_ids=tuple(ids),
        ),
    )


class EnemyAiReLifeBridgeTests(unittest.TestCase):
    def test_exact_id500_slot_becomes_symbolic_submission(self):
        submission=resolve_enemy_ai_relife_submission(
            spawned(),
            skill_slot=4,
            target_slot=3,
            petskill_runtime=runtime(),
        )
        self.assertEqual(submission.skill_id,RECOVERED25_RELIFE_SKILL_ID)
        self.assertEqual(submission.callback,"ENEMYSKILL_ReLife")
        self.assertEqual(submission.source_attack_target_slot,3)
        self.assertEqual(
            submission.semantic_command_name,
            "BATTLE_COM_S_ENEMYRELIFE",
        )
        self.assertFalse(hasattr(submission,"command1"))
        self.assertFalse(hasattr(submission,"command"))

    def test_all_three_positive_template_slots_are_admitted(self):
        for tempno,slot in ((39,4),(909,1),(1165,3)):
            submission=resolve_enemy_ai_relife_submission(
                spawned(tempno,slot),
                skill_slot=slot,
                target_slot=0,
                petskill_runtime=runtime(),
            )
            self.assertEqual(submission.skill_slot,slot)

    def test_template_or_slot_drift_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"positive template"):
            resolve_enemy_ai_relife_submission(
                spawned(40,4),
                skill_slot=4,
                target_slot=0,
                petskill_runtime=runtime(),
            )
        with self.assertRaisesRegex(ValueError,"selected slot drift"):
            resolve_enemy_ai_relife_submission(
                spawned(39,0),
                skill_slot=0,
                target_slot=0,
                petskill_runtime=runtime(),
            )

    def test_graphic_identity_drift_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"graphic identity drift"):
            resolve_enemy_ai_relife_submission(
                spawned(graphic_id=123),
                skill_slot=4,
                target_slot=0,
                petskill_runtime=runtime(),
            )

    def test_exact_row_metadata_drift_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"exact row drift"):
            resolve_enemy_ai_relife_submission(
                spawned(),
                skill_slot=4,
                target_slot=0,
                petskill_runtime=runtime(target=1),
            )


if __name__=="__main__":
    unittest.main()
