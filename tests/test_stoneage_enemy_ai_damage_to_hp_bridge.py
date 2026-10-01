import unittest
from types import SimpleNamespace

from tools.stoneage_enemy_ai_damage_to_hp_bridge import (
    RECOVERED25_DAMAGE_TO_HP_IDS,
    EnemyAiDamageToHpSubmission,
    resolve_enemy_ai_damage_to_hp_submission,
)
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillEntry,
    Recovered25PetSkillRuntime,
)


def runtime():
    rows={}
    for skill_id,option in (
        (503,b"30|50"),
        (504,b"20|70"),
        (505,b"10|100"),
    ):
        rows[skill_id]=Recovered25PetSkillEntry(
            skill_id,1,6,2,0,"PETSKILL_DamageToHp",option
        )
    return Recovered25PetSkillRuntime(
        skills=rows,source_file="petskill.txt"
    )


def spawned(skill_id=503):
    return SimpleNamespace(
        participant=SimpleNamespace(participant_id="enemy:drain"),
        template=SimpleNamespace(
            skill_slot_ids=(skill_id,0,0,0,0,0,0),
        ),
    )


class EnemyAiDamageToHpBridgeTests(unittest.TestCase):
    def test_hard_probed_rows_emit_semantic_submission_without_numeric_com1(self):
        submission=resolve_enemy_ai_damage_to_hp_submission(
            spawned(),
            skill_slot=0,
            target_slot=2,
            petskill_runtime=runtime(),
        )
        self.assertIsInstance(submission,EnemyAiDamageToHpSubmission)
        self.assertEqual(submission.skill_id,503)
        self.assertEqual(submission.option.attack_adjust_token,30)
        self.assertEqual(submission.option.callback_integer_ratio,0)
        self.assertEqual(submission.option.recovery_percent,50)
        self.assertFalse(hasattr(submission,"command1"))
        self.assertFalse(hasattr(submission,"command"))

    def test_callback_population_must_match_all_three_hard_probed_ids(self):
        rows=dict(runtime().skills)
        del rows[505]
        with self.assertRaisesRegex(ValueError,"503/504/505"):
            resolve_enemy_ai_damage_to_hp_submission(
                spawned(),
                skill_slot=0,
                target_slot=0,
                petskill_runtime=Recovered25PetSkillRuntime(
                    skills=rows,source_file="petskill.txt"
                ),
            )

    def test_recovered_id_set_is_stable(self):
        self.assertEqual(RECOVERED25_DAMAGE_TO_HP_IDS,(503,504,505))


if __name__ == "__main__":
    unittest.main()
