from dataclasses import replace
from types import SimpleNamespace
import unittest

from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillEntry
from tools.stoneage_recovered25_setmagicpet_probe import analyze_runtime_objects


def fixture():
    skills={
        601:Recovered25PetSkillEntry(
            601,1,2,2,0,"PETSKILL_SetMagicPet",b"3|25|STR"
        ),
        701:Recovered25PetSkillEntry(
            701,1,2,2,0,"PETSKILL_SetMagicPet",b"4|30|HP"
        ),
    }
    templates={
        n:SimpleNamespace(skill_slot_ids=(601,0,0,0,0,0,0))
        for n in range(6)
    }
    return SimpleNamespace(skills=skills),SimpleNamespace(templates=templates)


class SetMagicPetProbeTests(unittest.TestCase):
    def test_initial_unpinned_population_remains_open(self):
        result=analyze_runtime_objects(*fixture(),expected_ids=None)
        self.assertTrue(result["references_match"])
        self.assertFalse(result["population_closed"])
        self.assertTrue(result["all_options_parse_safe"])
        self.assertTrue(result["all_kinds_recognized"])
        self.assertEqual(result["rows"][1]["slot_references"],0)

    def test_explicit_full_population_pin(self):
        result=analyze_runtime_objects(*fixture(),expected_ids=(601,701))
        self.assertTrue(result["population_closed"])
        self.assertEqual(result["callback_ids"],(601,701))

    def test_unreferenced_extra_or_missing_row_breaks_pin(self):
        for mode in ("extra","missing"):
            pets,enemies=fixture()
            skills=dict(pets.skills)
            if mode=="extra":
                skills[702]=replace(skills[701],skill_id=702)
            else:
                del skills[701]
            self.assertFalse(
                analyze_runtime_objects(
                    SimpleNamespace(skills=skills),enemies,
                    expected_ids=(601,701),
                )["population_closed"]
            )

    def test_bad_option_is_reported_without_hiding_population(self):
        pets,enemies=fixture()
        skills=dict(pets.skills)
        skills[701]=replace(skills[701],option_bytes=b"bad")
        result=analyze_runtime_objects(
            SimpleNamespace(skills=skills),enemies,expected_ids=(601,701)
        )
        self.assertTrue(result["population_closed"])
        self.assertFalse(result["all_options_parse_safe"])

    def test_unknown_kind_is_separate_from_parser_safety(self):
        pets,enemies=fixture()
        skills=dict(pets.skills)
        skills[701]=replace(skills[701],option_bytes=b"3|20|???")
        result=analyze_runtime_objects(
            SimpleNamespace(skills=skills),enemies,expected_ids=(601,701)
        )
        self.assertTrue(result["all_options_parse_safe"])
        self.assertFalse(result["all_kinds_recognized"])

    def test_metadata_and_hash_are_derived_independently(self):
        pets,enemies=fixture()
        skills=dict(pets.skills)
        skills[601]=replace(skills[601],field=9,target=6,cost=11,illegal=2000)
        result=analyze_runtime_objects(
            SimpleNamespace(skills=skills),enemies,expected_ids=(601,701)
        )
        row=result["rows"][0]
        self.assertEqual(
            (row["field"],row["target"],row["cost"],row["illegal"]),
            (9,6,11,2000),
        )
        self.assertEqual(len(row["option_sha256"]),64)


if __name__=="__main__":
    unittest.main()
