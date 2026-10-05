from dataclasses import replace
from types import SimpleNamespace
import unittest

from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillEntry,
)
from tools.stoneage_recovered25_vary_probe import (
    analyze_runtime_objects,
)


def fixture(*,tempnos=(981,982,983,984),raw=b"x"):
    pets=SimpleNamespace(skills={
        600:Recovered25PetSkillEntry(
            600,1,3,2,0,"PETSKILL_Vary",raw
        ),
    })
    templates={}
    for n,tempno in enumerate(tempnos):
        templates[tempno]=SimpleNamespace(
            graphic_id=101400+n,
            skill_slot_ids=(600,0,0,0,0,0,0),
        )
    return pets,SimpleNamespace(templates=templates)


class Recovered25VaryProbeTests(unittest.TestCase):
    def test_population_and_base_tempno_domain_are_independent(self):
        result=analyze_runtime_objects(*fixture())
        self.assertTrue(result["population_closed"])
        self.assertTrue(result["all_positive_templates_base_allowed"])
        self.assertEqual(result["slot_references"],4)

    def test_outside_981_984_keeps_population_but_opens_base_domain(self):
        result=analyze_runtime_objects(*fixture(tempnos=(981,982,983,1200)))
        self.assertTrue(result["population_closed"])
        self.assertFalse(result["all_positive_templates_base_allowed"])

    def test_marker_matrix_never_stores_raw_option(self):
        raw="攻%30 敏%20".encode("utf-8")
        result=analyze_runtime_objects(*fixture(raw=raw))
        row=result["rows"][0]
        self.assertTrue(row["markers"]["utf8_attack"])
        self.assertTrue(row["markers"]["utf8_quick"])
        self.assertFalse(row["markers"]["utf8_defense"])
        self.assertEqual(row["ascii_percent_count"],2)
        self.assertNotIn("option_raw",row)

    def test_extra_callback_row_breaks_full_population_pin(self):
        pets,enemies=fixture()
        skills=dict(pets.skills)
        skills[601]=replace(
            skills[600],skill_id=601,option_bytes=b"other"
        )
        result=analyze_runtime_objects(
            SimpleNamespace(skills=skills),enemies
        )
        self.assertFalse(result["population_closed"])

    def test_repeated_slot_use_counts_pressure_not_only_templates(self):
        pets,enemies=fixture()
        templates=dict(enemies.templates)
        templates[981]=SimpleNamespace(
            graphic_id=101400,
            skill_slot_ids=(600,600,0,0,0,0,0),
        )
        result=analyze_runtime_objects(
            pets,SimpleNamespace(templates=templates)
        )
        self.assertEqual(result["slot_references"],5)
        self.assertFalse(result["population_closed"])


if __name__=="__main__":
    unittest.main()
