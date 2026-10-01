import unittest

from tools.stoneage_attack_magic_footprint_model import (
    TARGET_SIDE_0_B_ROW,
)
from tools.stoneage_attack_magic_model import (
    BATTLE_COM_S_ATTACK_MAGIC,
    command3_high,
    command3_low,
)
from tools.stoneage_enemy_ai_attack_magic_bridge import (
    ATTACK_MAGIC_CALLBACK,
    resolve_enemy_ai_attack_magic_submission,
)
from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_recovered25_attack_magic_runtime import (
    NONPLAYER_ITEM_ROLE,
    Recovered25AttackMagicEntry,
    Recovered25AttackMagicRuntime,
)
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillEntry,
    Recovered25PetSkillRuntime,
)
from tools.stoneage_singleplayer_battle import BattleParticipant
from tools.stoneage_tw10_25_bridge_model import (
    PetTemplateBridge,
    build_pet_birth_bridge,
)
from tools.stoneage_tw10_25_encounter_bridge import EnemyVariantBridge


CENTER=(
    (0,0,0,0,0),
    (0,0,1,0,0),
    (0,0,0,0,0),
)


def spawned_with_slots(slots):
    template=PetTemplateBridge.from_enemybase(
        {
            "TEMPNO":88,"INITNUM":1,"LVUPPOINT":5,
            "BASEVITAL":20,"BASESTR":20,"BASETGH":20,"BASEDEX":20,
            "MODAI":0,"GET":0,
            "EARTHAT":50,"WATERAT":50,"FIREAT":0,"WINDAT":0,
            "SLOT":4,"IMGNUMBER":1,"SIZE":0,
            **{f"PETSKILL{i}":value for i,value in enumerate(slots,1)},
        }
    )
    variant=EnemyVariantBridge.from_enemy(
        {
            "ID":700,"TEMPNO":88,"LV_MIN":5,"LV_MAX":5,
            "CREATEMAXNUM":1,"CREATEMINNUM":1,"TACTICS":1,
            "EXP":100,"DUELPOINT":0,"STYLE":0,"PETFLG":1,
        }
    )
    birth=build_pet_birth_bridge(
        template,
        level=5,
        birth_offsets=(0,0,0,0),
        spawn_allocation_rolls=(0,1,2,3,0,1,2,3,0,1),
    )
    p=birth.combat_projection()
    participant=BattleParticipant(
        participant_id="enemy:0",side="enemy",kind="enemy",
        level=5,hp=p["hp"],max_hp=p["max_hp"],
        attack=p["attack"],defense=p["defense"],quick=p["quick"],
        name=None,
    )
    return SpawnedEnemy(
        spawn_index=0,variant=variant,template=template,
        birth=birth,participant=participant,
    )


def runtime():
    entries={}
    skills={}
    for offset,magic_id in enumerate(range(301,326)):
        skill_id=1001+offset
        item_id=19647+offset
        entries[skill_id]=Recovered25AttackMagicEntry(
            skill_id=skill_id,
            magic_id=magic_id,
            item_config_id=item_id,
            item_magicusemp=5,
            magic_idx=2+offset,
            element=offset%4,
            power=100,
            magic_level=1,
            attacker_side1_matrix=CENTER,
            attacker_side0_matrix=CENTER,
        )
        skills[skill_id]=Recovered25PetSkillEntry(
            skill_id=skill_id,
            field=1,
            target=3,
            cost=0,
            illegal=0,
            function_name=ATTACK_MAGIC_CALLBACK,
            option_bytes=f"magic={magic_id} item={item_id}".encode("ascii"),
        )
    return (
        Recovered25AttackMagicRuntime(
            entries=entries,
            itemset_file="itemset.txt",
        ),
        Recovered25PetSkillRuntime(
            skills=skills,
            source_file="petskill.txt",
        ),
    )


class EnemyAiAttackMagicBridgeTests(unittest.TestCase):
    def test_single_target_submission_reuses_closed_command_boundary(self):
        attack_runtime,petskills=runtime()
        spawned=spawned_with_slots((1001,0,0,0,0,0,0))
        result=resolve_enemy_ai_attack_magic_submission(
            spawned,
            skill_slot=0,
            target_slot=3,
            petskill_runtime=petskills,
            attack_magic_runtime=attack_runtime,
        )
        self.assertEqual(result.command.command1,BATTLE_COM_S_ATTACK_MAGIC)
        self.assertEqual(result.command.command2,3)
        self.assertEqual(command3_low(result.command.command3),301)
        self.assertEqual(command3_high(result.command.command3),19647)
        self.assertEqual(result.direct_use_request.target,3)
        self.assertEqual(
            result.nonplayer_item_runtime_role,
            NONPLAYER_ITEM_ROLE,
        )

    def test_row_magic_direct_use_selector_is_projected_without_footprint(self):
        attack_runtime,petskills=runtime()
        spawned=spawned_with_slots((1003,0,0,0,0,0,0))
        result=resolve_enemy_ai_attack_magic_submission(
            spawned,
            skill_slot=0,
            target_slot=2,
            petskill_runtime=petskills,
            attack_magic_runtime=attack_runtime,
        )
        self.assertEqual(result.command.magic_id,303)
        self.assertEqual(
            result.direct_use_request.target,
            TARGET_SIDE_0_B_ROW,
        )
        self.assertEqual(result.direct_use_request.source_target,2)

    def test_selected_callback_must_be_attackmagic(self):
        attack_runtime,petskills=runtime()
        skills=dict(petskills.skills)
        skills[1001]=Recovered25PetSkillEntry(
            skill_id=1001,field=1,target=3,cost=0,illegal=0,
            function_name="PETSKILL_NormalAttack",
            option_bytes=b"",
        )
        petskills=Recovered25PetSkillRuntime(
            skills=skills,
            source_file="petskill.txt",
        )
        with self.assertRaisesRegex(ValueError,"outside AttackMagic"):
            resolve_enemy_ai_attack_magic_submission(
                spawned_with_slots((1001,0,0,0,0,0,0)),
                skill_slot=0,
                target_slot=0,
                petskill_runtime=petskills,
                attack_magic_runtime=attack_runtime,
            )

    def test_command_runtime_crosslink_drift_fails_closed(self):
        attack_runtime,petskills=runtime()
        skills=dict(petskills.skills)
        skills[1001]=Recovered25PetSkillEntry(
            skill_id=1001,field=1,target=3,cost=0,illegal=0,
            function_name=ATTACK_MAGIC_CALLBACK,
            option_bytes=b"magic=301 item=19648",
        )
        petskills=Recovered25PetSkillRuntime(
            skills=skills,
            source_file="petskill.txt",
        )
        with self.assertRaisesRegex(ValueError,"item-config drift"):
            resolve_enemy_ai_attack_magic_submission(
                spawned_with_slots((1001,0,0,0,0,0,0)),
                skill_slot=0,
                target_slot=0,
                petskill_runtime=petskills,
                attack_magic_runtime=attack_runtime,
            )


if __name__=="__main__":
    unittest.main()
