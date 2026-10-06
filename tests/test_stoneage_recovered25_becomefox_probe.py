import hashlib
import unittest
from types import SimpleNamespace as S

from tools.stoneage_recovered25_becomefox_probe import analyze_runtime_objects


def fixture():
    pets=S(skills={
        625:S(skill_id=625,field=1,target=1,cost=2,illegal=0,
              function_name="PETSKILL_BecomeFox",option_bytes=b"")
    })
    enemies=S(templates={
        100:S(graphic_id=1001,base_vital=10,base_strength=20,base_toughness=30,
              base_dexterity=40,ai=50,skill_slot_ids=(625,0,0,0,0,0,0)),
        101:S(graphic_id=1002,base_vital=11,base_strength=21,base_toughness=31,
              base_dexterity=41,ai=51,skill_slot_ids=(0,625,0,0,0,0,0)),
    })
    return pets,enemies


class BecomeFoxProbeTests(unittest.TestCase):
    def test_discovery_closes_only_known_pressure_identity(self):
        result=analyze_runtime_objects(*fixture())
        self.assertTrue(result["positive_references_closed"])
        self.assertFalse(result["population_closed"])
        self.assertFalse(result["exact_rows_closed"])
        self.assertFalse(result["exact_templates_closed"])
        self.assertEqual(result["referenced_ids"],(625,))
        self.assertEqual(result["slot_references"],2)
        self.assertEqual(len(result["templates"]),2)

    def test_neighbor_callback_breaks_positive_identity(self):
        pets,enemies=fixture()
        pets.skills[625].function_name="PETSKILL_BecomePig"
        self.assertFalse(analyze_runtime_objects(pets,enemies)["positive_references_closed"])

    def test_unreferenced_callback_row_is_not_silently_dropped(self):
        pets,enemies=fixture()
        pets.skills[700]=S(skill_id=700,field=1,target=1,cost=1,illegal=0,
                           function_name="PETSKILL_BecomeFox",option_bytes=b"x")
        result=analyze_runtime_objects(pets,enemies,expected_callback_ids=(625,))
        self.assertTrue(result["positive_references_closed"])
        self.assertEqual(result["callback_ids"],(625,700))
        self.assertFalse(result["population_closed"])

    def test_exact_row_and_template_pins_are_independent(self):
        pets,enemies=fixture()
        row=(625,1,1,2,0,2,0,hashlib.sha256(b"").hexdigest(),False,True,True)
        placements=(
            (100,1001,10,20,30,40,50,(1,),(625,)),
            (101,1002,11,21,31,41,51,(2,),(625,)),
        )
        def analyze(p,e):
            return analyze_runtime_objects(
                p,e,expected_callback_ids=(625,),
                expected_exact_rows=(row,),expected_template_rows=placements
            )
        self.assertTrue(analyze(pets,enemies)["population_closed"])
        self.assertTrue(analyze(pets,enemies)["exact_rows_closed"])
        self.assertTrue(analyze(pets,enemies)["exact_templates_closed"])
        pets.skills[625].target=3
        self.assertFalse(analyze(pets,enemies)["exact_rows_closed"])


if __name__=="__main__":
    unittest.main()
