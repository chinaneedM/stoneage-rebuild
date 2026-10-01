import unittest
from types import SimpleNamespace

from tools.stoneage_enemy_ai_mp_damage_bridge import (
    RECOVERED25_MP_DAMAGE_IDS,
    resolve_enemy_ai_mp_damage_submission,
)
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillEntry,
    Recovered25PetSkillRuntime,
)


def runtime():
    rows={}
    for skill_id,option in (
        (506,b"50|50"),
        (507,b"50|75"),
        (508,b"50|100"),
    ):
        rows[skill_id]=Recovered25PetSkillEntry(
            skill_id,1,6,2,0,"PETSKILL_MpDamage",option
        )
    return Recovered25PetSkillRuntime(
        skills=rows,source_file="petskill.txt"
    )


def spawned(skill_id=506):
    return SimpleNamespace(
        participant=SimpleNamespace(participant_id="enemy:mp"),
        template=SimpleNamespace(
            skill_slot_ids=(skill_id,0,0,0,0,0,0),
        ),
    )


class EnemyAiMpDamageBridgeTests(unittest.TestCase):
    def test_hard_probed_row_emits_semantic_submission_without_numeric_com1(self):
        submission=resolve_enemy_ai_mp_damage_submission(
            spawned(),
            skill_slot=0,
            target_slot=2,
            petskill_runtime=runtime(),
        )
        self.assertEqual(submission.skill_id,506)
        self.assertEqual(submission.option.attack_adjust_token,50)
        self.assertEqual(submission.option.callback_integer_ratio,0)
        self.assertEqual(submission.option.mp_percent,50)
        self.assertFalse(hasattr(submission,"command1"))
        self.assertFalse(hasattr(submission,"command"))

    def test_population_must_match_all_three_hard_probed_ids(self):
        rows=dict(runtime().skills)
        del rows[508]
        with self.assertRaisesRegex(ValueError,"506/507/508"):
            resolve_enemy_ai_mp_damage_submission(
                spawned(),
                skill_slot=0,
                target_slot=0,
                petskill_runtime=Recovered25PetSkillRuntime(
                    skills=rows,source_file="petskill.txt"
                ),
            )

    def test_recovered_id_set_is_stable(self):
        self.assertEqual(RECOVERED25_MP_DAMAGE_IDS,(506,507,508))


if __name__=="__main__":
    unittest.main()
