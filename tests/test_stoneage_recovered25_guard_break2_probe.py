import unittest
from types import SimpleNamespace

from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillEntry,
)
from tools.stoneage_recovered25_guard_break2_probe import (
    analyze_runtime_objects,
)


def fixture(*,skill_id=543,callback="PETSKILL_GuardBreak2"):
    pets=SimpleNamespace(skills={
        skill_id:Recovered25PetSkillEntry(
            skill_id,1,3,2,1000,callback,b"ignored-option"
        )
    })
    enemies=SimpleNamespace(templates={
        index:SimpleNamespace(
            skill_slot_ids=(543,0,0,0,0,0,0)
        )
        for index in range(11)
    })
    return pets,enemies


class Recovered25GuardBreak2ProbeTests(unittest.TestCase):
    def test_expected_population_closes_without_interpreting_option(self):
        result=analyze_runtime_objects(*fixture())
        self.assertTrue(result["population_closed"])
        self.assertEqual(
            (result["slot_references"],result["templates"]),
            (11,11),
        )
        self.assertEqual(result["rows"][0]["id"],543)
        self.assertEqual(result["rows"][0]["option_bytes"],14)

    def test_row_id_drift_never_closes(self):
        self.assertFalse(
            analyze_runtime_objects(*fixture(skill_id=542))[
                "population_closed"
            ]
        )

    def test_callback_drift_never_closes(self):
        result=analyze_runtime_objects(*fixture(callback="PETSKILL_Sacrifice"))
        self.assertFalse(result["population_closed"])
        self.assertEqual(result["rows"],())

    def test_reference_count_drift_never_closes(self):
        pets,enemies=fixture()
        del enemies.templates[0]
        self.assertFalse(
            analyze_runtime_objects(pets,enemies)["population_closed"]
        )


if __name__=="__main__":
    unittest.main()
