import unittest
from types import SimpleNamespace

from tools.stoneage_recovered25_relife_probe import analyze_runtime_objects


class Recovered25ReLifeProbeTests(unittest.TestCase):
    def test_exact_callback_population_and_positive_counts_are_bounded(self):
        pets=SimpleNamespace(skills={
            500:SimpleNamespace(
                skill_id=500,field=1,target=5,cost=2,illegal=1000,
                function_name="ENEMYSKILL_ReLife",option_bytes=b"",
            ),
            501:SimpleNamespace(
                skill_id=501,field=1,target=5,cost=2,illegal=1000,
                function_name="OTHER",option_bytes=b"",
            ),
        })
        enemies=SimpleNamespace(templates={
            10:SimpleNamespace(
                graphic_id=100,
                skill_slot_ids=(500,0,0,0,0,0,0),
            ),
            11:SimpleNamespace(
                graphic_id=101,
                skill_slot_ids=(0,500,0,0,0,0,0),
            ),
            12:SimpleNamespace(
                graphic_id=102,
                skill_slot_ids=(0,0,500,0,0,0,0),
            ),
        })
        result=analyze_runtime_objects(pets,enemies)
        self.assertTrue(result["population_closed"])
        self.assertEqual(result["callback_ids"],(500,))
        self.assertEqual(result["referenced_ids"],(500,))
        self.assertEqual(result["slot_references"],3)
        self.assertEqual(len(result["templates"]),3)

    def test_exact_recovered_row_and_template_identity_closes(self):
        pets=SimpleNamespace(skills={
            500:SimpleNamespace(
                skill_id=500,field=1,target=2,cost=2,illegal=0,
                function_name="ENEMYSKILL_ReLife",option_bytes=b"",
            ),
        })
        enemies=SimpleNamespace(templates={
            39:SimpleNamespace(
                graphic_id=100370,
                skill_slot_ids=(0,0,0,0,500,0,0),
            ),
            909:SimpleNamespace(
                graphic_id=100071,
                skill_slot_ids=(0,500,0,0,0,0,0),
            ),
            1165:SimpleNamespace(
                graphic_id=101814,
                skill_slot_ids=(0,0,0,500,0,0,0),
            ),
        })
        result=analyze_runtime_objects(pets,enemies)
        self.assertTrue(result["population_closed"])
        self.assertTrue(result["exact_row_closed"])
        self.assertTrue(result["exact_templates_closed"])

    def test_wrong_callback_population_stays_open(self):
        pets=SimpleNamespace(skills={
            500:SimpleNamespace(
                skill_id=500,field=1,target=5,cost=2,illegal=1000,
                function_name="ENEMYSKILL_ReLife",option_bytes=b"",
            ),
            599:SimpleNamespace(
                skill_id=599,field=1,target=5,cost=2,illegal=1000,
                function_name="ENEMYSKILL_ReLife",option_bytes=b"",
            ),
        })
        enemies=SimpleNamespace(templates={
            10:SimpleNamespace(
                graphic_id=100,
                skill_slot_ids=(500,0,0,0,0,0,0),
            ),
            11:SimpleNamespace(
                graphic_id=101,
                skill_slot_ids=(0,500,0,0,0,0,0),
            ),
            12:SimpleNamespace(
                graphic_id=102,
                skill_slot_ids=(0,0,500,0,0,0,0),
            ),
        })
        self.assertFalse(
            analyze_runtime_objects(pets,enemies)["population_closed"]
        )


if __name__=="__main__":
    unittest.main()
