import unittest
from types import SimpleNamespace

from tools.stoneage_enemy_ai_rehp_bridge import (
    RECOVERED25_REHP_SKILL_ID,
    resolve_enemy_ai_rehp_submission,
)
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillEntry,
    Recovered25PetSkillRuntime,
)


def runtime(callback="ENEMYSKILL_ReHP", skill_id=RECOVERED25_REHP_SKILL_ID):
    return Recovered25PetSkillRuntime(
        skills={
            skill_id:Recovered25PetSkillEntry(
                skill_id=skill_id,
                field=1,
                target=1,
                cost=2,
                illegal=0,
                function_name=callback,
                option_bytes=b"",
            )
        },
        source_file="petskill.txt",
    )


def spawned(skill_id=RECOVERED25_REHP_SKILL_ID):
    return SimpleNamespace(
        participant=SimpleNamespace(participant_id="enemy:rehp"),
        template=SimpleNamespace(
            skill_slot_ids=(skill_id,0,0,0,0,0,0),
        ),
    )


class EnemyAiReHpBridgeTests(unittest.TestCase):
    def test_hard_probed_id_becomes_semantic_submission_without_numeric_com1(self):
        submission=resolve_enemy_ai_rehp_submission(
            spawned(),
            skill_slot=0,
            target_slot=3,
            petskill_runtime=runtime(),
        )
        self.assertEqual(submission.skill_id,501)
        self.assertEqual(submission.callback,"ENEMYSKILL_ReHP")
        self.assertEqual(submission.source_target_slot,3)
        self.assertEqual(
            submission.semantic_command_name,
            "BATTLE_COM_S_ENEMYREHP",
        )
        self.assertFalse(hasattr(submission,"command1"))
        self.assertFalse(hasattr(submission,"command"))

    def test_callback_population_drift_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"exactly one callback row"):
            resolve_enemy_ai_rehp_submission(
                spawned(),
                skill_slot=0,
                target_slot=0,
                petskill_runtime=Recovered25PetSkillRuntime(
                    skills={},
                    source_file="petskill.txt",
                ),
            )

    def test_selected_slot_must_be_exact_recovered_id_501(self):
        with self.assertRaisesRegex(ValueError,"outside recovered25 ReHP ID 501"):
            resolve_enemy_ai_rehp_submission(
                spawned(500),
                skill_slot=0,
                target_slot=0,
                petskill_runtime=runtime(),
            )


if __name__ == "__main__":
    unittest.main()
