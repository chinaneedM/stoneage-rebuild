import unittest
from types import SimpleNamespace
from tools.stoneage_enemy_ai_battle_tear_bridge import (
    RECOVERED25_BATTLE_TEAR_IDS,EnemyAiBattleTearSubmission,
    resolve_enemy_ai_battle_tear_submission,
)
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillEntry,Recovered25PetSkillRuntime,
)
def runtime(a=b"20",b=b"50"):
    return Recovered25PetSkillRuntime(skills={
        615:Recovered25PetSkillEntry(615,1,1,2,10000,"PETSKILL_BattleTearDamage",a),
        616:Recovered25PetSkillEntry(616,1,1,2,10000,"PETSKILL_BattleTearDamage",b),
    },source_file="petskill.txt")
def spawned(skill=615):
    return SimpleNamespace(
        participant=SimpleNamespace(participant_id="enemy:tear",attack=200,defense=100),
        template=SimpleNamespace(skill_slot_ids=(skill,0,0,0,0,0,0)),
    )
class EnemyAiBattleTearBridgeTests(unittest.TestCase):
    def test_exact_row_and_setup(self):
        s=resolve_enemy_ai_battle_tear_submission(
            spawned(),skill_slot=0,target_slot=2,petskill_runtime=runtime()
        )
        self.assertIsInstance(s,EnemyAiBattleTearSubmission)
        self.assertEqual(s.wound_percent,20)
        setup=s.callback_setup(fixed_strength=200,fixed_toughness=100)
        self.assertEqual((setup.attack_power,setup.defense_power),(180,80))
        self.assertFalse(hasattr(s,"command1"))
    def test_second_row(self):
        s=resolve_enemy_ai_battle_tear_submission(
            spawned(616),skill_slot=0,target_slot=0,petskill_runtime=runtime()
        )
        self.assertEqual(s.wound_percent,50)
    def test_option_drift_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"wound percent drift"):
            resolve_enemy_ai_battle_tear_submission(
                spawned(),skill_slot=0,target_slot=0,petskill_runtime=runtime(a=b"30")
            )
    def test_id_set(self):
        self.assertEqual(RECOVERED25_BATTLE_TEAR_IDS,(615,616))
if __name__=="__main__": unittest.main()
