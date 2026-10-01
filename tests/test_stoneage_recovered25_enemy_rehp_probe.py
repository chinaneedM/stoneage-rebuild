import unittest
from types import SimpleNamespace

from tools.stoneage_recovered25_enemy_rehp_probe import (
    analyze_runtime_objects,
    minimum_possible_variant_max_hp,
)
from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillEntry
from tools.stoneage_tw10_25_bridge_model import PetTemplateBridge
from tools.stoneage_tw10_25_encounter_bridge import (
    EncounterAreaBridge,
    EnemyVariantBridge,
    GroupBridge,
)


def template(tempno, skills, *, init_num=100):
    slots=tuple(skills)+(0,)*(7-len(tuple(skills)))
    return PetTemplateBridge(
        tempno=tempno,
        graphic_id=tempno,
        name=None,
        ai=0,
        earth=25,
        water=25,
        fire=25,
        wind=25,
        skill_slots=7,
        skill_ids=tuple(x for x in slots if x>0),
        skill_slot_ids=slots,
        init_num=init_num,
        base_vital=10,
        base_strength=10,
        base_toughness=10,
        base_dexterity=10,
        level_up_point=1,
        size_class=0,
    )


def variant(enemy_id,tempno,lo=5,hi=5):
    return EnemyVariantBridge(
        enemy_id=enemy_id,
        tempno=tempno,
        level_min=lo,
        level_max=hi,
        create_max=1,
        create_min_declared=0,
        tactics=0,
        exp_override=0,
        duel_point=0,
        style=0,
        capturable=True,
    )


class Recovered25EnemyReHpProbeTests(unittest.TestCase):
    def test_minimum_possible_hp_uses_low_offsets_and_nonvital_allocations(self):
        t=template(100,(500,),init_num=10)
        v=variant(1,100,5,5)
        self.assertEqual(minimum_possible_variant_max_hp(t,v),9)

    def test_domain_closes_when_31_refs_targets_are_ge_100_and_no_help_overlap(self):
        rehp=Recovered25PetSkillEntry(500,1,1,2,0,"ENEMYSKILL_ReHP",b"")
        normal=Recovered25PetSkillEntry(501,1,1,2,0,"PETSKILL_NormalAttack",b"")
        skills={500:rehp,501:normal}
        # 31 source slot references across five templates.
        templates={}
        remaining=31
        for n in range(5):
            count=min(7,remaining)
            templates[100+n]=template(100+n,(500,)*count,init_num=100)
            remaining-=count
        templates[200]=template(200,(501,),init_num=100)
        enemies={
            1:variant(1,100,5,5),
            2:variant(2,200,5,5),
        }
        groups={
            10:GroupBridge(10,-1,-1,((1,50),(2,50))),
        }
        areas=(
            EncounterAreaBridge(
                1,1000,0,0,10,10,1,1,10,1,((10,100),)
            ),
        )
        result=analyze_runtime_objects(
            SimpleNamespace(skills=skills),
            SimpleNamespace(templates=templates),
            SimpleNamespace(
                encounter_areas=areas,
                groups=groups,
                enemies=enemies,
            ),
        )
        self.assertEqual(result["enemybase_slot_references"],31)
        self.assertGreaterEqual(result["rehp_target_min_possible_max_hp"],100)
        self.assertEqual(result["runtime_rehp_groups_with_enemyhelp"],0)
        self.assertTrue(result["reversed_rand_closed"])

    def test_enemyhelp_overlap_keeps_domain_open(self):
        skills={
            500:Recovered25PetSkillEntry(
                500,1,1,2,0,"ENEMYSKILL_ReHP",b""
            ),
            600:Recovered25PetSkillEntry(
                600,1,1,2,0,"ENEMYSKILL_EnemyHelp",b""
            ),
        }
        # Keep the exact 31-reference gate satisfied.
        templates={}
        remaining=31
        for n in range(5):
            count=min(7,remaining)
            templates[100+n]=template(100+n,(500,)*count,init_num=100)
            remaining-=count
        templates[200]=template(200,(600,),init_num=100)
        enemies={1:variant(1,100),2:variant(2,200)}
        groups={10:GroupBridge(10,-1,-1,((1,50),(2,50)))}
        areas=(
            EncounterAreaBridge(
                1,1000,0,0,10,10,1,1,10,1,((10,100),)
            ),
        )
        result=analyze_runtime_objects(
            SimpleNamespace(skills=skills),
            SimpleNamespace(templates=templates),
            SimpleNamespace(
                encounter_areas=areas,
                groups=groups,
                enemies=enemies,
            ),
        )
        self.assertEqual(result["runtime_rehp_groups_with_enemyhelp"],1)
        self.assertFalse(result["reversed_rand_closed"])


if __name__ == "__main__":
    unittest.main()
