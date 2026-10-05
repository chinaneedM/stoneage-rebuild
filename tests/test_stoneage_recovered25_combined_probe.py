from dataclasses import replace
from types import SimpleNamespace
import unittest

from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillEntry
from tools.stoneage_recovered25_combined_probe import analyze_runtime_objects


def fixture():
    skills={
        627:Recovered25PetSkillEntry(
            627,1,6,2,0,"PETSKILL_Combined",b"marker|2|301|302"
        ),
        632:Recovered25PetSkillEntry(
            632,1,6,2,0,"PETSKILL_Combined",b"marker|1|303"
        ),
        637:Recovered25PetSkillEntry(
            637,1,6,2,0,"PETSKILL_Combined",b"marker|3|304|305|306"
        ),
    }
    templates={
        1:SimpleNamespace(skill_slot_ids=(627,0,0,0,0,0,0)),
        2:SimpleNamespace(skill_slot_ids=(627,0,0,0,0,0,0)),
        3:SimpleNamespace(skill_slot_ids=(632,0,0,0,0,0,0)),
        4:SimpleNamespace(skill_slot_ids=(637,0,0,0,0,0,0)),
        5:SimpleNamespace(skill_slot_ids=(637,0,0,0,0,0,0)),
    }
    return SimpleNamespace(skills=skills),SimpleNamespace(templates=templates)


class CombinedProbeTests(unittest.TestCase):
    def test_expected_population_and_wellformed_structure_close(self):
        result=analyze_runtime_objects(
            *fixture(),expected_exact_rows=None
        )
        self.assertTrue(result["population_closed"])
        self.assertTrue(result["all_well_formed"])
        self.assertFalse(result["exact_rows_closed"])
        self.assertEqual(result["callback_ids"],(627,632,637))
        self.assertEqual(result["slot_references"],5)
        self.assertEqual(result["templates"],5)

    def test_five_references_across_only_four_templates_stays_open(self):
        pets,enemies=fixture()
        templates=dict(enemies.templates)
        templates[2]=SimpleNamespace(
            skill_slot_ids=(627,632,0,0,0,0,0)
        )
        templates[3]=SimpleNamespace(
            skill_slot_ids=(0,0,0,0,0,0,0)
        )
        result=analyze_runtime_objects(
            pets,SimpleNamespace(templates=templates),
            expected_exact_rows=None,
        )
        self.assertEqual(result["slot_references"],5)
        self.assertEqual(result["templates"],4)
        self.assertFalse(result["population_closed"])

    def test_extra_callback_row_breaks_population(self):
        pets,enemies=fixture()
        skills=dict(pets.skills)
        skills[638]=replace(skills[637],skill_id=638)
        result=analyze_runtime_objects(
            SimpleNamespace(skills=skills),enemies,
            expected_exact_rows=None,
        )
        self.assertFalse(result["population_closed"])

    def test_nonpositive_count_is_not_wellformed(self):
        pets,enemies=fixture()
        skills=dict(pets.skills)
        skills[627]=replace(skills[627],option_bytes=b"marker|0")
        result=analyze_runtime_objects(
            SimpleNamespace(skills=skills),enemies,
            expected_exact_rows=None,
        )
        self.assertFalse(result["all_well_formed"])

    def test_missing_magic_token_is_not_wellformed(self):
        pets,enemies=fixture()
        skills=dict(pets.skills)
        skills[627]=replace(
            skills[627],option_bytes=b"marker|3|301|302"
        )
        result=analyze_runtime_objects(
            SimpleNamespace(skills=skills),enemies,
            expected_exact_rows=None,
        )
        self.assertFalse(result["all_well_formed"])

    def test_exact_rows_are_independent_second_pass_pin(self):
        pets,enemies=fixture()
        loose=analyze_runtime_objects(
            pets,enemies,expected_exact_rows=None
        )
        self.assertFalse(loose["exact_rows_closed"])
        fake=tuple(
            (
                row["id"],row["field"],row["target"],row["cost"],
                row["illegal"],row["slot_references"],
                row["option_bytes"],row["option_sha256"],
                row["option_contains_nul"],row["marker_sha256"],
                row["declared_count"],row["effective_count"],
                row["magic_ids"],row["well_formed"],
            )
            for row in loose["rows"]
        )
        pinned=analyze_runtime_objects(
            pets,enemies,expected_exact_rows=fake
        )
        self.assertTrue(pinned["exact_rows_closed"])


if __name__=="__main__":
    unittest.main()
