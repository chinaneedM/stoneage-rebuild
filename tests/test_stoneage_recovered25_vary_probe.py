from dataclasses import replace
from types import SimpleNamespace
import unittest

from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillEntry,
)
from tools.stoneage_recovered25_vary_probe import (
    EXPECTED_EXACT_ROW,
    EXPECTED_TEMPLATE_ROWS,
    _c_float_after,
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

    def test_c_float_prefix_parser_matches_sscanf_style_prefix(self):
        marker="攻%".encode("cp950")
        self.assertEqual(_c_float_after(marker+b"  +25.5tail",marker),25.5)
        self.assertEqual(_c_float_after(marker+b"-7e1|",marker),-70.0)
        self.assertIsNone(_c_float_after(marker+b"abc",marker))
        self.assertIsNone(_c_float_after(b"other",marker))


    def test_production_exact_pins_are_not_satisfied_by_synthetic_fixture(self):
        result=analyze_runtime_objects(*fixture())
        self.assertFalse(result["exact_row_closed"])
        self.assertFalse(result["exact_templates_closed"])
        self.assertEqual(EXPECTED_EXACT_ROW[0],600)
        self.assertEqual(
            tuple(row[0] for row in EXPECTED_TEMPLATE_ROWS),
            (981,982,983,984),
        )

    def test_exact_template_pin_includes_graphic_and_slot_not_only_tempno(self):
        pets,enemies=fixture()
        templates={
            tempno:SimpleNamespace(
                graphic_id=graphic,
                skill_slot_ids=(0,0,600,0,0,0,0),
            )
            for tempno,graphic in (
                (981,101427),(982,101424),
                (983,101425),(984,101426),
            )
        }
        result=analyze_runtime_objects(
            pets,SimpleNamespace(templates=templates)
        )
        self.assertTrue(result["exact_templates_closed"])
        self.assertFalse(result["exact_row_closed"])



if __name__=="__main__":
    unittest.main()
