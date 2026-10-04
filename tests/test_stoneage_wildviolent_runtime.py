import unittest

from tools.stoneage_enemy_ai_wildviolent_bridge import (
    CONDITIONAL_EXECUTION_CHARSET,
    EnemyAiWildViolentSubmission,
    validate_recovered25_wildviolent_population,
)
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillEntry,
    Recovered25PetSkillRuntime,
)
from tools.stoneage_wildviolent_model import (
    CALLBACK_NAME,
    resolve_wildviolent_setup,
)


def synthetic_setup(target=0, packed=0x1234):
    return resolve_wildviolent_setup(
        option="攻%95防%-35避30".encode("cp950"),
        execution_charset="cp950",
        profile="gavin",
        target_slot=target,
        fixed_strength=100,
        fixed_toughness=100,
        attack_power_before=80,
        defense_power_before=90,
        packed_com3_before=packed,
    )


class WildViolentTypedAdmissionTests(unittest.TestCase):
    def test_typed_submission_keeps_symbolic_identity_and_conditional_charset(self):
        setup=synthetic_setup(target=0,packed=0x2345)
        submission=EnemyAiWildViolentSubmission(
            participant_id="enemy",
            skill_slot=0,
            skill_id=541,
            callback=CALLBACK_NAME,
            source_target_slot=0,
            setup=setup,
        )
        self.assertEqual(submission.conditional_execution_charset,CONDITIONAL_EXECUTION_CHARSET)
        self.assertEqual(submission.semantic_command_name,"BATTLE_COM_S_WILDVIOLENTATTACK")
        self.assertEqual(submission.setup.packed_com3 & 0xffff,0x2345)
        self.assertEqual(submission.setup.option.additive_dodge_percent_points,30)

    def test_unreferenced_652_cannot_be_selected_submission(self):
        with self.assertRaisesRegex(ValueError,"selected ID"):
            EnemyAiWildViolentSubmission(
                participant_id="enemy",
                skill_slot=0,
                skill_id=652,
                callback=CALLBACK_NAME,
                source_target_slot=0,
                setup=synthetic_setup(),
            )

    def test_population_validator_rejects_nonexact_synthetic_rows(self):
        bad=Recovered25PetSkillRuntime(
            skills={
                541:Recovered25PetSkillEntry(
                    541,1,6,2,1000,CALLBACK_NAME,
                    "攻%95防%-35避30".encode("cp950"),
                ),
                652:Recovered25PetSkillEntry(
                    652,1,6,2,1000,CALLBACK_NAME,
                    "攻%60防%-50避50".encode("cp950"),
                ),
            },
            source_file="petskill.txt",
        )
        with self.assertRaisesRegex(ValueError,"metadata/OPTION hash drift"):
            validate_recovered25_wildviolent_population(bad)


if __name__=="__main__":
    unittest.main()
