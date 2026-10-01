import unittest
from types import SimpleNamespace

from tools.stoneage_recovered25_battle_tear_probe import analyze_runtime_objects
from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillEntry


def entry(skill_id,option):
    return Recovered25PetSkillEntry(
        skill_id,1,6,2,0,"PETSKILL_BattleTearDamage",option
    )


class Recovered25BattleTearProbeTests(unittest.TestCase):
    def test_two_rows_nineteen_refs_and_numeric_options_close_domain(self):
        pets=SimpleNamespace(skills={
            615:entry(615,b"30"),
            616:entry(616,b"50"),
        })
        templates={}
        # 19 total uses across 19 distinct templates.
        for n in range(19):
            sid=615 if n<10 else 616
            templates[100+n]=SimpleNamespace(
                skill_slot_ids=(sid,0,0,0,0,0,0)
            )
        r=analyze_runtime_objects(pets,SimpleNamespace(templates=templates))
        self.assertTrue(r["domain_closed"])
        self.assertEqual(r["slot_references"],19)
        self.assertEqual(tuple(x["atoi_percent"] for x in r["rows"]),(30,50))

    def test_nonnumeric_option_keeps_domain_open(self):
        pets=SimpleNamespace(skills={
            615:entry(615,b"x30"),
            616:entry(616,b"50"),
        })
        templates={
            100+n:SimpleNamespace(
                skill_slot_ids=((615 if n<10 else 616),0,0,0,0,0,0)
            )
            for n in range(19)
        }
        self.assertFalse(
            analyze_runtime_objects(
                pets,SimpleNamespace(templates=templates)
            )["domain_closed"]
        )


if __name__=="__main__":
    unittest.main()
