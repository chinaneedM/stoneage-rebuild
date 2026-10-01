import unittest
from types import SimpleNamespace

from tools.stoneage_recovered25_mp_damage_probe import analyze_runtime_objects
from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillEntry


def entry(skill_id,option):
    return Recovered25PetSkillEntry(
        skill_id,1,6,2,0,"PETSKILL_MpDamage",option
    )


class Recovered25MpDamageProbeTests(unittest.TestCase):
    def test_three_rows_and_25_refs_close_numeric_two_field_domain(self):
        pets=SimpleNamespace(skills={
            600:entry(600,b"30|20"),
            601:entry(601,b"20|40"),
            602:entry(602,b"10|60"),
        })
        templates={}
        remaining=25
        for n in range(4):
            count=min(7,remaining)
            slots=(600,601,602,600,601,602,600)[:count]
            templates[100+n]=SimpleNamespace(skill_slot_ids=slots)
            remaining-=count
        result=analyze_runtime_objects(
            pets,SimpleNamespace(templates=templates)
        )
        self.assertEqual(len(result["rows"]),3)
        self.assertEqual(result["slot_references"],25)
        self.assertTrue(result["domain_closed"])

    def test_nonnumeric_option_keeps_domain_open(self):
        pets=SimpleNamespace(skills={
            600:entry(600,b"30|x"),
            601:entry(601,b"20|40"),
            602:entry(602,b"10|60"),
        })
        templates={
            1:SimpleNamespace(skill_slot_ids=(600,)*7),
            2:SimpleNamespace(skill_slot_ids=(601,)*7),
            3:SimpleNamespace(skill_slot_ids=(602,)*7),
            4:SimpleNamespace(skill_slot_ids=(600,)*4),
        }
        result=analyze_runtime_objects(
            pets,SimpleNamespace(templates=templates)
        )
        self.assertEqual(result["slot_references"],25)
        self.assertFalse(result["domain_closed"])


if __name__=="__main__":
    unittest.main()
