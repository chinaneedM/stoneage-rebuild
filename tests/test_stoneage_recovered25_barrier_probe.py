import unittest
from types import SimpleNamespace

from tools.stoneage_recovered25_barrier_probe import analyze_runtime_objects
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillEntry,
)


def fixture():
    pets=SimpleNamespace(skills={
        579:Recovered25PetSkillEntry(
            579,1,3,2,1000,
            "PETSKILL_Barrier",
            "turn=2 成=40".encode("big5"),
        ),
        594:Recovered25PetSkillEntry(
            594,1,3,2,1000,
            "PETSKILL_Barrier",
            "turn=3 成=50".encode("big5"),
        ),
    })
    enemies=SimpleNamespace(templates={
        index:SimpleNamespace(
            skill_slot_ids=(
                579 if index < 5 else 594,
                0,0,0,0,0,0,
            )
        )
        for index in range(10)
    })
    return pets,enemies


class Recovered25BarrierProbeTests(unittest.TestCase):
    def test_expected_population_closes_and_options_parse(self):
        result=analyze_runtime_objects(*fixture())
        self.assertTrue(result["population_closed"])
        self.assertEqual(
            (result["slot_references"],result["templates"]),
            (10,10),
        )
        self.assertEqual(
            tuple(row["id"] for row in result["rows"]),
            (579,594),
        )
        self.assertTrue(
            all(row["parsed_equal"] for row in result["rows"])
        )

    def test_missing_row_never_closes(self):
        pets,enemies=fixture()
        del pets.skills[594]
        self.assertFalse(
            analyze_runtime_objects(pets,enemies)["population_closed"]
        )

    def test_reference_count_drift_never_closes(self):
        pets,enemies=fixture()
        del enemies.templates[0]
        self.assertFalse(
            analyze_runtime_objects(pets,enemies)["population_closed"]
        )


if __name__=="__main__":
    unittest.main()
