import unittest
from types import SimpleNamespace

from tools.stoneage_recovered25_nocast_probe import analyze_runtime_objects
from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillEntry


def fixture(option="turn=3 成=50", *, field=1):
    pets = SimpleNamespace(skills={580: Recovered25PetSkillEntry(
        580, field, 6, 2, 10000, "PETSKILL_Nocast", option.encode("big5"))})
    enemies = SimpleNamespace(templates={
        index: SimpleNamespace(skill_slot_ids=(580, 580 if index < 2 else 0, 0, 0, 0, 0, 0))
        for index in range(16)
    })
    return pets, enemies


class Recovered25NocastProbeTests(unittest.TestCase):
    def test_18_slot_uses_across_16_templates_and_codecs_close(self):
        result = analyze_runtime_objects(*fixture())
        self.assertTrue(result["domain_closed"])
        self.assertEqual((result["slot_references"], result["templates"]), (18, 16))
        self.assertEqual((result["rows"][0]["turn"], result["rows"][0]["success_offset"]), (3, 50))

    def test_malformed_or_undefined_options_never_close(self):
        for option in ("成=50", "turn=x 成=50", "turn=3", "turn=0 成=50", "turn=3 成=-1"):
            with self.subTest(option=option):
                self.assertFalse(analyze_runtime_objects(*fixture(option))["domain_closed"])

    def test_population_drift_never_closes(self):
        pets, enemies = fixture()
        pets.skills[581] = Recovered25PetSkillEntry(581, 1, 6, 2, 10000, "PETSKILL_Nocast", b"turn=3")
        self.assertFalse(analyze_runtime_objects(pets, enemies)["domain_closed"])

    def test_missing_reference_and_wrong_field_never_close(self):
        pets, enemies = fixture()
        del enemies.templates[0]
        self.assertFalse(analyze_runtime_objects(pets, enemies)["domain_closed"])
        self.assertFalse(analyze_runtime_objects(*fixture(field=2))["domain_closed"])

    def test_codec_error_keeps_domain_open(self):
        pets, enemies = fixture()
        pets.skills[580] = Recovered25PetSkillEntry(580, 1, 6, 2, 10000, "PETSKILL_Nocast", b"\xff")
        self.assertFalse(analyze_runtime_objects(pets, enemies)["domain_closed"])


if __name__ == "__main__":
    unittest.main()
