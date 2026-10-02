import unittest
from types import SimpleNamespace

from tools.stoneage_recovered25_petskill_pressure_probe import (
    analyze_runtime_objects,
)


class Recovered25PetSkillPressureProbeTests(unittest.TestCase):
    def test_ranking_counts_slot_pressure_and_selects_highest_open_callback(self):
        pets=SimpleNamespace(skills={
            1:SimpleNamespace(function_name="PETSKILL_NormalAttack"),
            210:SimpleNamespace(function_name="PETSKILL_FallGround"),
            300:SimpleNamespace(function_name="PETSKILL_Explode"),
            301:SimpleNamespace(function_name="PETSKILL_Explode"),
            400:SimpleNamespace(function_name="PETSKILL_Timid"),
            500:SimpleNamespace(function_name="PETSKILL_Merge"),
            580:SimpleNamespace(function_name="PETSKILL_Nocast"),
            543:SimpleNamespace(function_name="PETSKILL_GuardBreak2"),
        })
        enemies=SimpleNamespace(templates={
            10:SimpleNamespace(skill_slot_ids=(1,300,300,400,500,580,543)),
            11:SimpleNamespace(skill_slot_ids=(210,301,300,400,0,0,0)),
        })
        result=analyze_runtime_objects(pets,enemies)
        rows={row["callback"]:row for row in result["rows"]}
        self.assertEqual(result["total_positive_slot_uses"],11)
        self.assertEqual(rows["PETSKILL_Explode"]["slot_uses"],4)
        self.assertEqual(rows["PETSKILL_Explode"]["skill_ids"],(300,301))
        self.assertEqual(rows["PETSKILL_NormalAttack"]["status"],"closed_runtime")
        self.assertEqual(rows["PETSKILL_FallGround"]["status"],"closed_runtime")
        self.assertEqual(rows["PETSKILL_Nocast"]["status"],"closed_runtime")
        self.assertEqual(rows["PETSKILL_GuardBreak2"]["status"],"closed_runtime")
        self.assertEqual(rows["PETSKILL_Merge"]["status"],"historical_ub")
        self.assertEqual(result["next_open"]["callback"],"PETSKILL_Explode")

    def test_missing_positive_skill_id_is_reported_not_silently_dropped(self):
        pets=SimpleNamespace(skills={
            1:SimpleNamespace(function_name="PETSKILL_NormalAttack"),
        })
        enemies=SimpleNamespace(templates={
            10:SimpleNamespace(skill_slot_ids=(1,999,0,0,0,0,0)),
        })
        result=analyze_runtime_objects(pets,enemies)
        self.assertEqual(result["unresolved_skill_ids"],(999,))


if __name__=="__main__":
    unittest.main()
