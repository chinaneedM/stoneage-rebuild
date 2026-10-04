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
            579:SimpleNamespace(function_name="PETSKILL_Barrier"),
        })
        enemies=SimpleNamespace(templates={
            10:SimpleNamespace(skill_slot_ids=(1,300,300,400,500,580,543)),
            11:SimpleNamespace(skill_slot_ids=(210,301,300,400,579,0,0)),
        })
        result=analyze_runtime_objects(pets,enemies)
        rows={row["callback"]:row for row in result["rows"]}
        self.assertEqual(result["total_positive_slot_uses"],12)
        self.assertEqual(rows["PETSKILL_Explode"]["slot_uses"],4)
        self.assertEqual(rows["PETSKILL_Explode"]["skill_ids"],(300,301))
        self.assertEqual(rows["PETSKILL_NormalAttack"]["status"],"closed_runtime")
        self.assertEqual(rows["PETSKILL_FallGround"]["status"],"closed_runtime")
        self.assertEqual(rows["PETSKILL_Nocast"]["status"],"closed_runtime")
        self.assertEqual(rows["PETSKILL_GuardBreak2"]["status"],"closed_runtime")
        self.assertEqual(rows["PETSKILL_Barrier"]["status"],"closed_runtime")
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

    def test_mdfyattack_runtime_closure_does_not_close_modifyattack(self):
        pets=SimpleNamespace(skills={
            548:SimpleNamespace(function_name="PETSKILL_Mdfyattack"),
            544:SimpleNamespace(function_name="PETSKILL_Modifyattack"),
        })
        enemies=SimpleNamespace(templates={
            10:SimpleNamespace(skill_slot_ids=(548,548,544,0,0,0,0)),
        })
        result=analyze_runtime_objects(pets,enemies)
        rows={row["callback"]:row for row in result["rows"]}
        self.assertEqual(rows["PETSKILL_Mdfyattack"]["status"],"closed_runtime")
        self.assertEqual(rows["PETSKILL_Modifyattack"]["status"],"open")
        self.assertEqual(result["next_open"]["callback"],"PETSKILL_Modifyattack")

    def test_wildviolent_closure_advances_only_the_exact_callback(self):
        pets=SimpleNamespace(skills={
            541:SimpleNamespace(function_name="PETSKILL_WildViolentAttack"),
            652:SimpleNamespace(function_name="PETSKILL_WildViolentAttack"),
            544:SimpleNamespace(function_name="PETSKILL_Modifyattack"),
            200:SimpleNamespace(function_name="PETSKILL_Merge"),
        })
        enemies=SimpleNamespace(templates={
            10:SimpleNamespace(skill_slot_ids=(541,541,544,200,0,0,0)),
        })
        result=analyze_runtime_objects(pets,enemies)
        rows={row["callback"]:row for row in result["rows"]}
        self.assertEqual(
            rows["PETSKILL_WildViolentAttack"]["status"],
            "closed_runtime",
        )
        self.assertEqual(rows["PETSKILL_Modifyattack"]["status"],"open")
        self.assertEqual(rows["PETSKILL_Merge"]["status"],"historical_ub")
        self.assertEqual(result["next_open"]["callback"],"PETSKILL_Modifyattack")

    def test_refresh_closure_advances_only_the_exact_callback(self):
        pets=SimpleNamespace(skills={
            583:SimpleNamespace(function_name="PETSKILL_Refresh"),
            592:SimpleNamespace(function_name="PETSKILL_Refresh"),
            601:SimpleNamespace(function_name="PETSKILL_SetMagicPet"),
            200:SimpleNamespace(function_name="PETSKILL_Merge"),
        })
        enemies=SimpleNamespace(templates={
            10:SimpleNamespace(skill_slot_ids=(583,583,592,601,200,0,0)),
        })
        result=analyze_runtime_objects(pets,enemies)
        rows={row["callback"]:row for row in result["rows"]}
        self.assertEqual(rows["PETSKILL_Refresh"]["status"],"closed_runtime")
        self.assertEqual(rows["PETSKILL_SetMagicPet"]["status"],"open")
        self.assertEqual(rows["PETSKILL_Merge"]["status"],"historical_ub")
        self.assertEqual(result["next_open"]["callback"],"PETSKILL_SetMagicPet")

    def test_weaken_closure_advances_only_the_exact_callback(self):
        pets=SimpleNamespace(skills={
            575:SimpleNamespace(function_name="PETSKILL_Weaken"),
            576:SimpleNamespace(function_name="PETSKILL_Weaken"),
            577:SimpleNamespace(function_name="PETSKILL_Deeppoison"),
            200:SimpleNamespace(function_name="PETSKILL_Merge"),
        })
        enemies=SimpleNamespace(templates={
            10:SimpleNamespace(skill_slot_ids=(575,576,577,200,0,0,0)),
        })
        result=analyze_runtime_objects(pets,enemies)
        rows={row["callback"]:row for row in result["rows"]}
        self.assertEqual(rows["PETSKILL_Weaken"]["status"],"closed_runtime")
        self.assertEqual(rows["PETSKILL_Merge"]["status"],"historical_ub")
        self.assertEqual(rows["PETSKILL_Deeppoison"]["status"],"open")
        self.assertEqual(result["next_open"]["callback"],"PETSKILL_Deeppoison")


if __name__=="__main__":
    unittest.main()
