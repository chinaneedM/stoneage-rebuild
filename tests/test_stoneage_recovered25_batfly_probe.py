import hashlib
import unittest
from types import SimpleNamespace as S

from tools.stoneage_recovered25_batfly_probe import analyze_runtime_objects


def fixture():
    pets=S(
        skills={
            633:S(
                skill_id=633,
                field=1,
                target=3,
                cost=2,
                illegal=0,
                function_name="PETSKILL_BatFly",
                option_bytes=b"",
            )
        }
    )
    enemies=S(
        templates={
            100:S(
                graphic_id=101813,
                base_vital=10,
                base_strength=20,
                base_toughness=30,
                base_dexterity=40,
                ai=4,
                skill_slot_ids=(633,633,0,0,0,0,0),
            )
        }
    )
    return pets,enemies


class BatFlyProbeTests(unittest.TestCase):
    def test_discovery_closes_pressure_identity_not_unpinned_population(self):
        result=analyze_runtime_objects(*fixture())
        self.assertTrue(result["positive_references_closed"])
        self.assertFalse(result["population_closed"])
        self.assertFalse(result["exact_rows_closed"])
        self.assertFalse(result["exact_templates_closed"])
        self.assertEqual(result["referenced_ids"],(633,))
        self.assertEqual(result["slot_references"],2)

    def test_neighbor_callback_does_not_count(self):
        pets,enemies=fixture()
        pets.skills[633].function_name="PETSKILL_DivideAttack"
        self.assertFalse(
            analyze_runtime_objects(pets,enemies)["positive_references_closed"]
        )

    def test_unreferenced_population_row_is_not_silently_dropped(self):
        pets,enemies=fixture()
        pets.skills[700]=S(
            skill_id=700,
            field=1,
            target=3,
            cost=2,
            illegal=0,
            function_name="PETSKILL_BatFly",
            option_bytes=b"x",
        )
        result=analyze_runtime_objects(
            pets,enemies,expected_callback_ids=(633,)
        )
        self.assertTrue(result["positive_references_closed"])
        self.assertEqual(result["callback_ids"],(633,700))
        self.assertFalse(result["population_closed"])

    def test_exact_metadata_and_template_fields_drift_independently(self):
        pets,enemies=fixture()
        row=(
            633,1,3,2,0,2,0,hashlib.sha256(b"").hexdigest(),
            False,True,True,
        )
        placement=(
            100,101813,10,20,30,40,4,(1,2),(633,633),
        )
        def analyze(p,e):
            return analyze_runtime_objects(
                p,e,
                expected_callback_ids=(633,),
                expected_exact_rows=(row,),
                expected_template_rows=(placement,),
            )
        self.assertTrue(analyze(pets,enemies)["exact_rows_closed"])
        self.assertTrue(analyze(pets,enemies)["exact_templates_closed"])

        pets2,enemies2=fixture()
        pets2.skills[633].target=7
        self.assertFalse(analyze(pets2,enemies2)["exact_rows_closed"])

        pets3,enemies3=fixture()
        enemies3.templates[100].graphic_id=101814
        self.assertFalse(analyze(pets3,enemies3)["exact_templates_closed"])


if __name__=="__main__":
    unittest.main()
