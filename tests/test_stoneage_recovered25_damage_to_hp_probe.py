import unittest
from types import SimpleNamespace

from tools.stoneage_recovered25_damage_to_hp_probe import (
    analyze_runtime_objects,
)
from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillEntry


def entry(skill_id,option):
    return Recovered25PetSkillEntry(
        skill_id,1,1,2,0,"PETSKILL_DamageToHp",option
    )


class Recovered25DamageToHpProbeTests(unittest.TestCase):
    def test_three_rows_and_30_refs_close_ascii_two_token_domain(self):
        pets=SimpleNamespace(skills={
            503:entry(503,b"30|20"),
            504:entry(504,b"50|30"),
            505:entry(505,b"100|40"),
        })
        templates={}
        remaining=30
        for n in range(5):
            count=min(7,remaining)
            slots=(503,504,505,503,504,505,503)[:count]
            templates[100+n]=SimpleNamespace(skill_slot_ids=slots)
            remaining-=count
        result=analyze_runtime_objects(
            pets,SimpleNamespace(templates=templates)
        )
        self.assertEqual(len(result["rows"]),3)
        self.assertEqual(result["slot_references"],30)
        self.assertTrue(result["domain_closed"])
        self.assertEqual(result["rows"][0]["attack_adjust_token"],30)
        self.assertEqual(result["rows"][0]["callback_integer_ratio"],0)
        self.assertEqual(result["rows"][0]["recovery_percent"],20)

    def test_nonnumeric_second_token_keeps_domain_open(self):
        pets=SimpleNamespace(skills={
            503:entry(503,b"30|heal"),
            504:entry(504,b"50|30"),
            505:entry(505,b"100|40"),
        })
        templates={
            1:SimpleNamespace(skill_slot_ids=(503,)*7),
            2:SimpleNamespace(skill_slot_ids=(504,)*7),
            3:SimpleNamespace(skill_slot_ids=(505,)*7),
            4:SimpleNamespace(skill_slot_ids=(503,)*7),
            5:SimpleNamespace(skill_slot_ids=(504,504)),
        }
        result=analyze_runtime_objects(
            pets,SimpleNamespace(templates=templates)
        )
        self.assertEqual(result["slot_references"],30)
        self.assertFalse(result["domain_closed"])


if __name__ == "__main__":
    unittest.main()
