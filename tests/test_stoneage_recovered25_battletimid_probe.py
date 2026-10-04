from dataclasses import replace
from types import SimpleNamespace
import unittest

from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillEntry
from tools.stoneage_recovered25_battletimid_probe import (\n    EXPECTED_EXACT_ROW,\n    analyze_runtime_objects,\n)


def fixture():
    skills={
        606:Recovered25PetSkillEntry(
            606,1,1,2,0,"PETSKILL_BattleTimid",b"opaque"
        ),
    }
    templates={
        n:SimpleNamespace(skill_slot_ids=(606,0,0,0,0,0,0))
        for n in range(5)
    }
    return SimpleNamespace(skills=skills),SimpleNamespace(templates=templates)


class BattleTimidProbeTests(unittest.TestCase):
    def test_expected_population_closes_independently_of_row_pin(self):
        result=analyze_runtime_objects(*fixture(),expected_exact_row=None)
        self.assertTrue(result["population_closed"])
        self.assertFalse(result["exact_row_closed"])
        self.assertEqual(result["callback_ids"],(606,))
        self.assertEqual(result["slot_references"],5)
        self.assertEqual(result["templates"],5)

    def test_extra_callback_row_breaks_population(self):
        pets,enemies=fixture()
        skills=dict(pets.skills)
        skills[607]=replace(skills[606],skill_id=607)
        result=analyze_runtime_objects(
            SimpleNamespace(skills=skills),enemies,expected_exact_row=None
        )
        self.assertFalse(result["population_closed"])

    def test_reference_count_drift_breaks_population(self):
        pets,enemies=fixture()
        templates=dict(enemies.templates)
        templates[99]=SimpleNamespace(skill_slot_ids=(606,0,0,0,0,0,0))
        result=analyze_runtime_objects(
            pets,SimpleNamespace(templates=templates),expected_exact_row=None
        )
        self.assertFalse(result["population_closed"])

    def test_exact_row_pin_is_independent(self):
        pets,enemies=fixture()
        result=analyze_runtime_objects(pets,enemies,expected_exact_row=(
            606,1,1,2,0,6,
            "b5357d...intentionally-wrong",False,
        ))
        self.assertTrue(result["population_closed"])
        self.assertFalse(result["exact_row_closed"])
        row=result["rows"][0]
        self.assertEqual(row["option_bytes"],6)
        self.assertEqual(len(row["option_sha256"]),64)

    def test_verified_exact_row_pin_closes(self):
        pets,enemies=fixture()
        skills={
            606:Recovered25PetSkillEntry(
                606,1,6,2,3000,"PETSKILL_BattleTimid",b""
            ),
        }
        result=analyze_runtime_objects(
            SimpleNamespace(skills=skills),enemies,
            expected_exact_row=EXPECTED_EXACT_ROW,
        )
        self.assertTrue(result["population_closed"])
        self.assertTrue(result["exact_row_closed"])
        self.assertEqual(result["rows"][0]["option_bytes"],0)
        self.assertEqual(
            result["rows"][0]["option_sha256"],
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        )

    def test_nul_presence_is_derived_not_hidden(self):
        pets,enemies=fixture()
        skills=dict(pets.skills)
        skills[606]=replace(skills[606],option_bytes=b"a\0b")
        result=analyze_runtime_objects(
            SimpleNamespace(skills=skills),enemies,expected_exact_row=None
        )
        self.assertTrue(result["rows"][0]["option_contains_nul"])


if __name__=="__main__":
    unittest.main()
