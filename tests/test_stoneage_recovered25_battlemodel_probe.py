import hashlib
import unittest
from types import SimpleNamespace as S

from tools.stoneage_recovered25_battlemodel_probe import analyze_runtime_objects


def fixture():
    pets=S(skills={
        638:S(
            skill_id=638,field=1,target=3,cost=2,illegal=0,
            function_name="PETSKILL_BattleModel",
            option_bytes=b"5|2|x|3|30|atk",
        ),
    })
    enemies=S(templates={
        100:S(
            graphic_id=101900,base_vital=10,base_strength=20,
            base_toughness=30,base_dexterity=40,ai=4,
            skill_slot_ids=(638,0,0,0,0,0,0),
        ),
        101:S(
            graphic_id=101901,base_vital=11,base_strength=21,
            base_toughness=31,base_dexterity=41,ai=5,
            skill_slot_ids=(0,0,0,638,0,0,0),
        ),
    })
    return pets,enemies


class BattleModelProbeTests(unittest.TestCase):
    def test_discovery_closes_pressure_identity_not_unpinned_population(self):
        result=analyze_runtime_objects(*fixture())
        self.assertTrue(result["positive_references_closed"])
        self.assertFalse(result["population_closed"])
        self.assertFalse(result["exact_rows_closed"])
        self.assertFalse(result["exact_templates_closed"])
        self.assertEqual(result["referenced_ids"],(638,))
        self.assertEqual(result["slot_references"],2)
        self.assertEqual(len(result["templates"]),2)

    def test_neighbor_callback_does_not_count(self):
        pets,enemies=fixture()
        pets.skills[638].function_name="PETSKILL_BecomeFox"
        self.assertFalse(
            analyze_runtime_objects(pets,enemies)["positive_references_closed"]
        )

    def test_unreferenced_population_row_is_not_silently_dropped(self):
        pets,enemies=fixture()
        pets.skills[700]=S(
            skill_id=700,field=1,target=3,cost=2,illegal=0,
            function_name="PETSKILL_BattleModel",option_bytes=b"1|2|X|1|30||100",
        )
        result=analyze_runtime_objects(
            pets,enemies,expected_callback_ids=(638,)
        )
        self.assertTrue(result["positive_references_closed"])
        self.assertEqual(result["callback_ids"],(638,700))
        self.assertFalse(result["population_closed"])

    def test_malformed_unreferenced_option_fails_closed(self):
        pets,enemies=fixture()
        pets.skills[700]=S(
            skill_id=700,field=1,target=3,cost=2,illegal=0,
            function_name="PETSKILL_BattleModel",option_bytes=b"x",
        )
        with self.assertRaisesRegex(ValueError,"requires fields 1 and 2"):
            analyze_runtime_objects(pets,enemies)

    def test_exact_metadata_and_template_fields_drift_independently(self):
        pets,enemies=fixture()
        raw=b"5|2|x|3|30|atk"
        row=(
            638,1,3,2,0,2,len(raw),hashlib.sha256(raw).hexdigest(),
            False,True,True,
        )
        placements=(
            (100,101900,10,20,30,40,4,(1,),(638,)),
            (101,101901,11,21,31,41,5,(4,),(638,)),
        )
        def analyze(p,e):
            return analyze_runtime_objects(
                p,e,
                expected_callback_ids=(638,),
                expected_exact_rows=(row,),
                expected_template_rows=placements,
            )
        self.assertTrue(analyze(pets,enemies)["population_closed"])
        self.assertTrue(analyze(pets,enemies)["exact_rows_closed"])
        self.assertTrue(analyze(pets,enemies)["exact_templates_closed"])

        pets2,enemies2=fixture()
        pets2.skills[638].target=7
        self.assertFalse(analyze(pets2,enemies2)["exact_rows_closed"])

        pets3,enemies3=fixture()
        enemies3.templates[100].graphic_id=101999
        self.assertFalse(analyze(pets3,enemies3)["exact_templates_closed"])


if __name__=="__main__":
    unittest.main()
