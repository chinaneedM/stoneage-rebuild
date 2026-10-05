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

    def test_mdfyattack_and_modifyattack_have_separate_runtime_rows(self):
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
        self.assertEqual(rows["PETSKILL_Modifyattack"]["status"],"closed_runtime")
        self.assertEqual(rows["PETSKILL_Mdfyattack"]["slot_uses"],2)
        self.assertEqual(rows["PETSKILL_Modifyattack"]["slot_uses"],1)
        self.assertIsNone(result["next_open"])

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
        self.assertEqual(rows["PETSKILL_Modifyattack"]["status"],"closed_runtime")
        self.assertEqual(rows["PETSKILL_Merge"]["status"],"historical_ub")
        self.assertIsNone(result["next_open"])

    def test_modifyattack_closes_only_three_positive_uses_not_unreferenced_wind(self):
        pets=SimpleNamespace(skills={
            **{skill:SimpleNamespace(function_name="PETSKILL_Modifyattack") for skill in range(544,548)},
            636:SimpleNamespace(function_name="PETSKILL_2BattleTimid"),
            200:SimpleNamespace(function_name="PETSKILL_Merge"),
        })
        enemies=SimpleNamespace(templates={
            18:SimpleNamespace(skill_slot_ids=(0,0,0,546,0,0,0)),
            19:SimpleNamespace(skill_slot_ids=(0,0,0,0,545,0,0)),
            20:SimpleNamespace(skill_slot_ids=(0,0,0,544,0,0,0)),
            21:SimpleNamespace(skill_slot_ids=(636,200,0,0,0,0,0)),
        })
        result=analyze_runtime_objects(pets,enemies)
        rows={row["callback"]:row for row in result["rows"]}
        row=rows["PETSKILL_Modifyattack"]
        self.assertEqual((row["status"],row["skill_ids"],row["slot_uses"]),("closed_runtime",(544,545,546),3))
        self.assertEqual(rows["PETSKILL_Merge"]["status"],"historical_ub")
        self.assertEqual(rows["PETSKILL_2BattleTimid"]["status"],"closed_runtime")
        self.assertIsNone(result["next_open"])

    def test_refresh_closure_advances_only_the_exact_callback(self):
        pets=SimpleNamespace(skills={
            583:SimpleNamespace(function_name="PETSKILL_Refresh"),
            592:SimpleNamespace(function_name="PETSKILL_Refresh"),
            601:SimpleNamespace(function_name="PETSKILL_SetMagicPet"),
            606:SimpleNamespace(function_name="PETSKILL_BattleTimid"),
            627:SimpleNamespace(function_name="PETSKILL_Combined"),
            600:SimpleNamespace(function_name="PETSKILL_Vary"),
            200:SimpleNamespace(function_name="PETSKILL_Merge"),
        })
        enemies=SimpleNamespace(templates={
            10:SimpleNamespace(
                skill_slot_ids=(583,583,592,601,606,627,200)
            ),
            11:SimpleNamespace(
                skill_slot_ids=(600,0,0,0,0,0,0)
            ),
        })
        result=analyze_runtime_objects(pets,enemies)
        rows={row["callback"]:row for row in result["rows"]}
        self.assertEqual(rows["PETSKILL_Refresh"]["status"],"closed_runtime")
        self.assertEqual(
            rows["PETSKILL_SetMagicPet"]["status"],
            "closed_runtime",
        )
        self.assertEqual(rows["PETSKILL_Combined"]["status"],"closed_runtime")
        self.assertEqual(rows["PETSKILL_Merge"]["status"],"historical_ub")
        self.assertEqual(rows["PETSKILL_Vary"]["status"],"closed_runtime")
        self.assertIsNone(result["next_open"])

    def test_setmagicpet_closure_advances_only_the_exact_callback(self):
        pets=SimpleNamespace(skills={
            601:SimpleNamespace(function_name="PETSKILL_SetMagicPet"),
            602:SimpleNamespace(function_name="PETSKILL_SetMagicPet"),
            606:SimpleNamespace(function_name="PETSKILL_BattleTimid"),
            627:SimpleNamespace(function_name="PETSKILL_Combined"),
            600:SimpleNamespace(function_name="PETSKILL_Vary"),
            200:SimpleNamespace(function_name="PETSKILL_Merge"),
        })
        enemies=SimpleNamespace(templates={
            10:SimpleNamespace(
                skill_slot_ids=(601,601,606,627,200,600,0)
            ),
        })
        result=analyze_runtime_objects(pets,enemies)
        rows={row["callback"]:row for row in result["rows"]}
        self.assertEqual(
            rows["PETSKILL_SetMagicPet"]["status"],
            "closed_runtime",
        )
        self.assertEqual(
            rows["PETSKILL_BattleTimid"]["status"],
            "closed_runtime",
        )
        self.assertEqual(rows["PETSKILL_Combined"]["status"],"closed_runtime")
        self.assertEqual(rows["PETSKILL_Merge"]["status"],"historical_ub")
        self.assertEqual(
            rows["PETSKILL_Vary"]["status"],
            "closed_runtime",
        )
        self.assertIsNone(result["next_open"])

    def test_2battletimid_closure_is_independent_from_battletimid(self):
        pets=SimpleNamespace(skills={
            606:SimpleNamespace(function_name="PETSKILL_BattleTimid"),
            636:SimpleNamespace(function_name="PETSKILL_2BattleTimid"),
            627:SimpleNamespace(function_name="PETSKILL_Combined"),
            200:SimpleNamespace(function_name="PETSKILL_Merge"),
        })
        enemies=SimpleNamespace(templates={
            10:SimpleNamespace(
                skill_slot_ids=(606,606,636,627,200,0,0)
            ),
        })
        result=analyze_runtime_objects(pets,enemies)
        rows={row["callback"]:row for row in result["rows"]}
        self.assertEqual(
            rows["PETSKILL_BattleTimid"]["status"],
            "closed_runtime",
        )
        self.assertEqual(rows["PETSKILL_2BattleTimid"]["status"],"closed_runtime")
        self.assertEqual(rows["PETSKILL_Combined"]["status"],"closed_runtime")
        self.assertEqual(rows["PETSKILL_Merge"]["status"],"historical_ub")
        self.assertIsNone(result["next_open"])

    def test_combined_closure_advances_to_highest_remaining_open(self):
        pets=SimpleNamespace(skills={
            627:SimpleNamespace(function_name="PETSKILL_Combined"),
            632:SimpleNamespace(function_name="PETSKILL_Combined"),
            637:SimpleNamespace(function_name="PETSKILL_Combined"),
            600:SimpleNamespace(function_name="PETSKILL_Vary"),
            500:SimpleNamespace(function_name="ENEMYSKILL_ReLife"),
            200:SimpleNamespace(function_name="PETSKILL_Merge"),
        })
        enemies=SimpleNamespace(templates={
            10:SimpleNamespace(
                skill_slot_ids=(627,632,637,600,600,500,200)
            ),
            11:SimpleNamespace(
                skill_slot_ids=(627,637,600,600,500,500,0)
            ),
        })
        result=analyze_runtime_objects(pets,enemies)
        rows={row["callback"]:row for row in result["rows"]}
        self.assertEqual(
            rows["PETSKILL_Combined"]["status"],
            "closed_runtime",
        )
        self.assertEqual(rows["PETSKILL_Combined"]["slot_uses"],5)
        self.assertEqual(rows["PETSKILL_Vary"]["status"],"closed_runtime")
        self.assertEqual(rows["PETSKILL_Vary"]["slot_uses"],4)
        self.assertEqual(rows["ENEMYSKILL_ReLife"]["slot_uses"],3)
        self.assertEqual(rows["ENEMYSKILL_ReLife"]["status"],"closed_runtime")
        self.assertEqual(rows["PETSKILL_Merge"]["status"],"historical_ub")
        self.assertIsNone(result["next_open"])

    def test_lighttakeed_closure_advances_without_closing_neighbors(self):
        pets=SimpleNamespace(skills={
            600:SimpleNamespace(function_name="PETSKILL_Vary"),
            500:SimpleNamespace(function_name="ENEMYSKILL_ReLife"),
            609:SimpleNamespace(function_name="PETSKILL_Lighttakeed"),
            610:SimpleNamespace(function_name="PETSKILL_Lighttakeed"),
            611:SimpleNamespace(function_name="PETSKILL_Lighttakeed"),
            636:SimpleNamespace(function_name="PETSKILL_2BattleTimid"),
            200:SimpleNamespace(function_name="PETSKILL_Merge"),
        })
        enemies=SimpleNamespace(templates={
            10:SimpleNamespace(
                skill_slot_ids=(600,600,500,610,636,200,0)
            ),
            11:SimpleNamespace(
                skill_slot_ids=(600,600,500,500,610,611,0)
            ),
        })
        result=analyze_runtime_objects(pets,enemies)
        rows={row["callback"]:row for row in result["rows"]}
        self.assertEqual(rows["PETSKILL_Vary"]["status"],"closed_runtime")
        self.assertEqual(rows["PETSKILL_Vary"]["slot_uses"],4)
        self.assertEqual(
            rows["ENEMYSKILL_ReLife"]["status"],
            "closed_runtime",
        )
        self.assertEqual(rows["PETSKILL_Lighttakeed"]["status"],"closed_runtime")
        self.assertEqual(rows["PETSKILL_Lighttakeed"]["slot_uses"],3)
        self.assertEqual(rows["PETSKILL_Lighttakeed"]["skill_ids"],(610,611))
        self.assertEqual(
            rows["PETSKILL_2BattleTimid"]["status"],
            "closed_runtime",
        )
        self.assertEqual(rows["PETSKILL_Merge"]["status"],"historical_ub")
        self.assertIsNone(result["next_open"])

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
