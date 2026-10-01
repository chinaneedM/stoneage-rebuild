import unittest
from types import SimpleNamespace

from tools.stoneage_recovered25_fall_ground_probe import analyze_runtime_objects
from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillEntry


def entry(skill_id,option):
    return Recovered25PetSkillEntry(
        skill_id,1,6,2,0,"PETSKILL_FallGround",option
    )


class Recovered25FallGroundProbeTests(unittest.TestCase):
    def test_one_row_and_23_refs_close_cp950_big5_attack_marker_domain(self):
        pets=SimpleNamespace(skills={
            502:entry(502,"攻%50".encode("cp950")),
        })
        templates={}
        remaining=23
        for n in range(4):
            count=min(7,remaining)
            templates[100+n]=SimpleNamespace(
                skill_slot_ids=(502,)*count
            )
            remaining-=count
        result=analyze_runtime_objects(
            pets,SimpleNamespace(templates=templates)
        )
        self.assertEqual(len(result["rows"]),1)
        self.assertEqual(result["slot_references"],23)
        self.assertTrue(result["domain_closed"])
        self.assertEqual(result["rows"][0]["attack_percent"],50.0)

    def test_missing_marker_keeps_domain_open(self):
        pets=SimpleNamespace(skills={
            502:entry(502,b"50"),
        })
        templates={
            1:SimpleNamespace(skill_slot_ids=(502,)*7),
            2:SimpleNamespace(skill_slot_ids=(502,)*7),
            3:SimpleNamespace(skill_slot_ids=(502,)*7),
            4:SimpleNamespace(skill_slot_ids=(502,502)),
        }
        result=analyze_runtime_objects(
            pets,SimpleNamespace(templates=templates)
        )
        self.assertFalse(result["domain_closed"])


if __name__=="__main__":
    unittest.main()
