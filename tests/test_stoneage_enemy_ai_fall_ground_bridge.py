import unittest
from types import SimpleNamespace

from tools.stoneage_enemy_ai_fall_ground_bridge import (
    RECOVERED25_FALL_GROUND_IDS,
    EnemyAiFallGroundSubmission,
    resolve_enemy_ai_fall_ground_submission,
)
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillEntry,
    Recovered25PetSkillRuntime,
)


def runtime(option="攻%-30"):
    return Recovered25PetSkillRuntime(
        skills={
            210:Recovered25PetSkillEntry(
                210,1,6,2,3000,"PETSKILL_FallGround",
                option.encode("cp950"),
            ),
        },
        source_file="petskill.txt",
    )


def spawned():
    return SimpleNamespace(
        participant=SimpleNamespace(
            participant_id="enemy:fall",
            attack=200,
        ),
        template=SimpleNamespace(
            skill_slot_ids=(210,0,0,0,0,0,0),
        ),
    )


class EnemyAiFallGroundBridgeTests(unittest.TestCase):
    def test_exact_recovered_row_emits_semantic_submission(self):
        submission=resolve_enemy_ai_fall_ground_submission(
            spawned(),
            skill_slot=0,
            target_slot=2,
            petskill_runtime=runtime(),
        )
        self.assertIsInstance(submission,EnemyAiFallGroundSubmission)
        self.assertEqual(submission.skill_id,210)
        self.assertEqual(submission.option.attack_percent,-30.0)
        self.assertEqual(submission.callback_attack_power(200),140)
        self.assertFalse(hasattr(submission,"command1"))
        self.assertFalse(hasattr(submission,"command"))

    def test_attack_percent_drift_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"attack percent drift"):
            resolve_enemy_ai_fall_ground_submission(
                spawned(),
                skill_slot=0,
                target_slot=0,
                petskill_runtime=runtime("攻%-20"),
            )

    def test_recovered_id_set_is_stable(self):
        self.assertEqual(RECOVERED25_FALL_GROUND_IDS,(210,))


if __name__=="__main__":
    unittest.main()
