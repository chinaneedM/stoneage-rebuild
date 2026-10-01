import unittest
from dataclasses import replace

from tools.stoneage_attack_magic_action_model import (
    AttackMagicTargetRolls,
    EnemyAttackMagicActionRolls,
)
from tools.stoneage_attack_magic_damage_model import ElementAttrs
from tools.stoneage_attack_magic_model import (
    PROFILE_RECOVERED25,
    build_magic_direct_use_request,
    encode_attack_magic_command,
)
from tools.stoneage_attack_magic_round_state_adapter import (
    AttackMagicResistanceRuntime,
    AttackMagicRoundOverlay,
    resolve_persistent_enemy_attack_magic_state,
)
from tools.stoneage_battle_ride_damage_model import RidePetRuntime
from tools.stoneage_battle_round_model import BattleCombatProfile
from tools.stoneage_battle_state_model import begin_persistent_battle
from tools.stoneage_battle_status_model import (
    BaseBattleStatusRuntime,
    BaseBattleStatusState,
)
from tools.stoneage_enemy_ai_attack_magic_bridge import (
    ATTACK_MAGIC_CALLBACK,
    EnemyAiAttackMagicSubmission,
)
from tools.stoneage_recovered25_attack_magic_runtime import (
    NONPLAYER_ITEM_ROLE,
    Recovered25AttackMagicEntry,
    Recovered25AttackMagicRuntime,
)
from tools.stoneage_singleplayer_battle import (
    BattleParticipant,
    BattleSession,
)
from tools.stoneage_singleplayer_domain import MapPosition


CENTER=(
    (0,0,0,0,0),
    (0,0,1,0,0),
    (0,0,0,0,0),
)
WHOLE=(
    (1,1,1,1,1),
    (1,1,1,1,1),
    (0,0,0,0,0),
)


def participant(
    participant_id,
    *,
    side,
    kind,
    level,
    hp=1000,
    max_hp=1000,
    source_pet_slot=None,
):
    return BattleParticipant(
        participant_id=participant_id,
        side=side,
        kind=kind,
        level=level,
        hp=hp,
        max_hp=max_hp,
        attack=100,
        defense=100,
        quick=100,
        name=participant_id,
        source_pet_slot=source_pet_slot,
    )


def runtime():
    entries={}
    for offset,magic_id in enumerate(range(301,326)):
        matrix=WHOLE if magic_id == 305 else CENTER
        skill_id=1001+offset
        entries[skill_id]=Recovered25AttackMagicEntry(
            skill_id=skill_id,
            magic_id=magic_id,
            item_config_id=19647+offset,
            item_magicusemp=5,
            magic_idx=2+offset,
            element=0,
            power=(1000 if magic_id == 301 else 100),
            magic_level=1,
            attacker_side1_matrix=matrix,
            attacker_side0_matrix=matrix,
        )
    return Recovered25AttackMagicRuntime(
        entries=entries,
        itemset_file="itemset.txt",
    )


def submission(magic_id=301,target_slot=0):
    offset=magic_id-301
    skill_id=1001+offset
    item_id=19647+offset
    command=encode_attack_magic_command(
        target_slot,
        f"magic={magic_id} item={item_id}",
        profile=PROFILE_RECOVERED25,
    )
    return EnemyAiAttackMagicSubmission(
        participant_id="enemy",
        skill_slot=0,
        skill_id=skill_id,
        callback=ATTACK_MAGIC_CALLBACK,
        command=command,
        direct_use_request=build_magic_direct_use_request(command),
        nonplayer_item_runtime_role=NONPLAYER_ITEM_ROLE,
    )


def profile(earth,water,fire=0,wind=0,luck=0):
    return BattleCombatProfile(
        fixed_dex=50,
        fixed_luck=luck,
        earth=earth,
        water=water,
        fire=fire,
        wind=wind,
    )


def battle_state(*,with_pet=False,with_ride=False,sleep=3,ride_hp=100):
    player=participant(
        "player",side="player",kind="player",level=50
    )
    allied=(
        (
            participant(
                "pet:1",
                side="player",
                kind="pet",
                level=40,
                source_pet_slot=1,
            ),
        )
        if with_pet else ()
    )
    enemy=participant(
        "enemy",side="enemy",kind="enemy",level=56
    )
    ride=(
        participant(
            "ride:2",
            side="player",
            kind="pet",
            level=40,
            hp=ride_hp,
            max_hp=100,
            source_pet_slot=2,
        )
        if with_ride else None
    )
    session=BattleSession(
        origin_position=MapPosition(0,0,0),
        encounter=object(),
        player=player,
        allied_pets=allied,
        enemies=(enemy,),
        ride_pet=ride,
    )
    slots={"player":0,"enemy":15}
    if with_pet:
        slots["pet:1"]=1
    ride_runtime=(
        RidePetRuntime(
            rider_id="player",
            pet_id="ride:2",
            hp=ride_hp,
            max_hp=100,
            defense_power=100,
        )
        if with_ride else None
    )
    state=begin_persistent_battle(
        session,
        slots=slots,
        ride_pet_runtime=ride_runtime,
    )
    statuses=dict(state.base_status_runtime_by_participant_id)
    statuses["player"]=BaseBattleStatusRuntime(
        status=BaseBattleStatusState(sleep=sleep),
        work_quick=100,
    )
    return replace(
        state,
        base_status_runtime_by_participant_id=statuses,
    )


def overlay(*,include_pet=False):
    values={
        "player":AttackMagicResistanceRuntime(
            levels=(20,5,0,0),
            exps=(90,1,0,0),
        )
    }
    if include_pet:
        values["pet:1"]=AttackMagicResistanceRuntime(
            levels=(10,3,0,0),
            exps=(0,0,0,0),
        )
    return AttackMagicRoundOverlay(values)


class AttackMagicRoundStateAdapterTests(unittest.TestCase):
    def test_updates_hp_sleep_and_four_element_training_overlay(self):
        state=battle_state()
        result=resolve_persistent_enemy_attack_magic_state(
            state,
            submission=submission(),
            attack_magic_runtime=runtime(),
            profiles={
                "enemy":profile(100,0),
                "player":profile(0,100),
            },
            overlay=overlay(),
            rolls=EnemyAttackMagicActionRolls(
                0,{0:AttackMagicTargetRolls(100,0)}
            ),
        )
        hit=result.action.targets[0]
        self.assertEqual(hit.raw_magic_damage,495)
        self.assertEqual(result.after.hp_by_participant_id["player"],505)
        self.assertEqual(
            result.after.base_status_runtime_by_participant_id[
                "player"
            ].status.sleep,
            0,
        )
        trained=result.overlay_after.resistance_by_participant_id["player"]
        self.assertEqual(trained.levels,(21,4,0,0))
        self.assertEqual(trained.exps,(0,90,0,0))
        self.assertEqual(result.after.turn,state.turn)
        self.assertEqual(result.after.phase,state.phase)

    def test_dodge_preserves_hp_sleep_and_resistance(self):
        state=battle_state(sleep=4)
        before=overlay()
        result=resolve_persistent_enemy_attack_magic_state(
            state,
            submission=submission(),
            attack_magic_runtime=runtime(),
            profiles={
                "enemy":profile(100,0),
                "player":profile(0,100,luck=20),
            },
            overlay=before,
            rolls=EnemyAttackMagicActionRolls(
                0,{0:AttackMagicTargetRolls(1,None)}
            ),
        )
        self.assertTrue(result.action.targets[0].dodged)
        self.assertEqual(
            result.after.hp_by_participant_id["player"],1000
        )
        self.assertEqual(
            result.after.base_status_runtime_by_participant_id[
                "player"
            ].status.sleep,
            4,
        )
        self.assertEqual(result.overlay_after,before)

    def test_ride_hp_and_mount_state_are_written_back(self):
        state=battle_state(with_ride=True,sleep=0)
        result=resolve_persistent_enemy_attack_magic_state(
            state,
            submission=submission(),
            attack_magic_runtime=runtime(),
            profiles={
                "enemy":profile(100,0),
                "player":profile(0,100),
                "ride:2":profile(100,0),
            },
            overlay=overlay(),
            rolls=EnemyAttackMagicActionRolls(
                0,{0:AttackMagicTargetRolls(100,0)}
            ),
        )
        self.assertLess(
            result.after.hp_by_participant_id["player"],
            state.hp_by_participant_id["player"],
        )
        self.assertLess(
            result.after.ride_pet_runtime.hp,
            state.ride_pet_runtime.hp,
        )
        self.assertEqual(
            result.after.ride_pet_runtime.pet_id,
            state.ride_pet_runtime.pet_id,
        )

    def test_exact_zero_ride_hp_keeps_source_mounted_quirk(self):
        state=battle_state(with_ride=True,sleep=0,ride_hp=100)
        # Lower power through a copy of the runtime so this witness exercises
        # the dedicated action model without fabricating ordinary ride rules.
        rt=runtime()
        entries=dict(rt.entries)
        first=entries[1001]
        entries[1001]=replace(first,power=100)
        rt=Recovered25AttackMagicRuntime(
            entries=entries,itemset_file="itemset.txt"
        )
        result=resolve_persistent_enemy_attack_magic_state(
            state,
            submission=submission(),
            attack_magic_runtime=rt,
            profiles={
                "enemy":profile(100,0),
                "player":profile(0,100),
                "ride:2":profile(100,0),
            },
            overlay=overlay(),
            rolls=EnemyAttackMagicActionRolls(
                0,{0:AttackMagicTargetRolls(100,0)}
            ),
        )
        self.assertTrue(result.after.ride_pet_runtime.mounted)

    def test_multi_target_nonportable_source_order_fails_before_state_write(self):
        state=battle_state(with_pet=True)
        with self.assertRaisesRegex(ValueError,"SortLoc/qsort"):
            resolve_persistent_enemy_attack_magic_state(
                state,
                submission=submission(305,0),
                attack_magic_runtime=runtime(),
                profiles={
                    "enemy":profile(100,0),
                    "player":profile(0,100),
                    "pet:1":profile(0,100),
                },
                overlay=overlay(include_pet=True),
                rolls=EnemyAttackMagicActionRolls(
                    0,{
                        0:AttackMagicTargetRolls(100,0),
                        1:AttackMagicTargetRolls(100,0),
                    }
                ),
            )
        self.assertEqual(state.hp_by_participant_id["player"],1000)
        self.assertEqual(state.hp_by_participant_id["pet:1"],1000)

    def test_exact_rng_slots_cannot_include_unused_target_rolls(self):
        state=battle_state()
        with self.assertRaisesRegex(ValueError,"RNG target slots"):
            resolve_persistent_enemy_attack_magic_state(
                state,
                submission=submission(),
                attack_magic_runtime=runtime(),
                profiles={
                    "enemy":profile(100,0),
                    "player":profile(0,100),
                },
                overlay=overlay(),
                rolls=EnemyAttackMagicActionRolls(
                    0,{
                        0:AttackMagicTargetRolls(100,0),
                        1:AttackMagicTargetRolls(100,0),
                    }
                ),
            )

    def test_mounted_ride_requires_element_profile(self):
        state=battle_state(with_ride=True)
        with self.assertRaisesRegex(KeyError,"ride-pet profile"):
            resolve_persistent_enemy_attack_magic_state(
                state,
                submission=submission(),
                attack_magic_runtime=runtime(),
                profiles={
                    "enemy":profile(100,0),
                    "player":profile(0,100),
                },
                overlay=overlay(),
                rolls=EnemyAttackMagicActionRolls(
                    0,{0:AttackMagicTargetRolls(100,0)}
                ),
            )


if __name__=="__main__":
    unittest.main()
