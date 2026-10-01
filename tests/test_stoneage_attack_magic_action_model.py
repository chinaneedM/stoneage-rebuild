import unittest

from tools.stoneage_attack_magic_action_model import (
    AttackMagicDefenderState,
    AttackMagicRideTargetState,
    AttackMagicTargetRolls,
    EnemyAttackMagicActionRolls,
    EnemyAttackMagicCasterState,
    resolve_enemy_attack_magic_action,
    source_battle_attrs,
)
from tools.stoneage_attack_magic_damage_model import (
    ElementAttrs,
    MagicExpState,
)
from tools.stoneage_recovered25_attack_magic_runtime import (
    NONPLAYER_ITEM_ROLE,
    Recovered25EnemyAttackMagicPlan,
)


def plan(
    *,
    power=100,
    magic_level=1,
    target_order=(0,),
    portable=True,
):
    return Recovered25EnemyAttackMagicPlan(
        skill_id=1001,
        magic_id=301,
        item_config_id=19647,
        item_runtime_role=NONPLAYER_ITEM_ROLE,
        magic_idx=8,
        element=0,
        power=power,
        magic_level=magic_level,
        actor_slot=15,
        source_target_slot=0,
        source_selector=0,
        normalized_selector=0,
        target_membership=tuple(target_order),
        source_sort_portable=portable,
        source_target_order=(tuple(target_order) if portable else None),
    )


def caster():
    return EnemyAttackMagicCasterState(
        participant_id="enemy:1",
        level=56,
        pure_attrs=ElementAttrs(100,0,0,0),
    )


def player(
    *,
    hp=1000,
    resistance=None,
    luck=0,
    equipment_quimagic=0,
    sleep_turns=2,
    pure_attrs=None,
    ride=None,
):
    return AttackMagicDefenderState(
        participant_id="player",
        kind="player",
        level=50,
        hp=hp,
        max_hp=1000,
        pure_attrs=(
            pure_attrs
            if pure_attrs is not None
            else ElementAttrs(0,100,0,0)
        ),
        resistance=(
            resistance
            if resistance is not None
            else MagicExpState(20,0,5,0)
        ),
        luck=luck,
        equipment_quimagic=equipment_quimagic,
        sleep_turns=sleep_turns,
        ride=ride,
    )


class AttackMagicActionModelTests(unittest.TestCase):
    def test_source_battle_attrs_averages_rider_and_pet(self):
        value=source_battle_attrs(
            ElementAttrs(0,100,0,0),
            ride_pet_attrs=ElementAttrs(100,0,0,0),
        )
        self.assertEqual(value,ElementAttrs(50,50,0,0,0))

    def test_exact_enemy_cast_hits_player_and_clears_sleep(self):
        resolved=resolve_enemy_attack_magic_action(
            plan=plan(),
            caster=caster(),
            defenders_by_slot={0:player()},
            rolls=EnemyAttackMagicActionRolls(
                0,
                {0:AttackMagicTargetRolls(100,0)},
            ),
        )
        hit=resolved.targets[0]
        self.assertEqual(resolved.attacker_proficiency,50)
        self.assertTrue(resolved.true_magic_success)
        self.assertEqual(hit.raw_magic_damage,49)
        self.assertEqual(hit.hp_after,951)
        self.assertTrue(hit.sleep_cleared)
        self.assertEqual(resolved.defenders_after[0].sleep_turns,0)
        self.assertFalse(resolved.attacker_training_applied)

    def test_failed_cast_applies_point_seven_after_attribute_adjustment(self):
        resolved=resolve_enemy_attack_magic_action(
            plan=plan(),
            caster=caster(),
            defenders_by_slot={0:player()},
            rolls=EnemyAttackMagicActionRolls(
                99,
                {0:AttackMagicTargetRolls(100,0)},
            ),
        )
        self.assertFalse(resolved.true_magic_success)
        self.assertEqual(resolved.targets[0].raw_magic_damage,34)
        self.assertEqual(resolved.targets[0].hp_after,966)

    def test_dodge_consumes_no_damage_random_and_preserves_training_sleep(self):
        before=MagicExpState(20,90,5,1)
        resolved=resolve_enemy_attack_magic_action(
            plan=plan(power=1000),
            caster=caster(),
            defenders_by_slot={
                0:player(
                    resistance=before,
                    luck=10,
                    equipment_quimagic=10,
                    sleep_turns=3,
                )
            },
            rolls=EnemyAttackMagicActionRolls(
                0,
                {0:AttackMagicTargetRolls(42,None)},
            ),
        )
        hit=resolved.targets[0]
        self.assertTrue(hit.dodged)
        self.assertEqual(hit.raw_magic_damage,0)
        self.assertEqual(hit.hp_after,1000)
        self.assertEqual(hit.resistance_after,before)
        self.assertEqual(resolved.defenders_after[0].sleep_turns,3)

    def test_defense_training_uses_post_penalty_raw_magic_damage_before_hp(self):
        before=MagicExpState(20,90,5,1)
        resolved=resolve_enemy_attack_magic_action(
            plan=plan(power=1000),
            caster=caster(),
            defenders_by_slot={0:player(resistance=before)},
            rolls=EnemyAttackMagicActionRolls(
                0,
                {0:AttackMagicTargetRolls(100,0)},
            ),
        )
        hit=resolved.targets[0]
        self.assertEqual(hit.raw_magic_damage,495)
        self.assertEqual(
            hit.resistance_after,
            MagicExpState(21,0,4,90),
        )
        self.assertEqual(hit.hp_after,505)

    def test_ride_attributes_and_dedicated_magic_split_are_composed(self):
        ride=AttackMagicRideTargetState(
            pet_id="ride:1",
            hp=100,
            max_hp=100,
            pure_attrs=ElementAttrs(100,0,0,0),
        )
        defender=player(
            hp=100,
            pure_attrs=ElementAttrs(0,100,0,0),
            ride=ride,
            sleep_turns=0,
        )
        resolved=resolve_enemy_attack_magic_action(
            plan=plan(),
            caster=caster(),
            defenders_by_slot={0:defender},
            rolls=EnemyAttackMagicActionRolls(
                0,
                {0:AttackMagicTargetRolls(100,0)},
            ),
        )
        hit=resolved.targets[0]
        self.assertEqual(hit.raw_magic_damage,41)
        self.assertEqual(hit.reported_rider_damage,28)
        self.assertEqual(hit.ride_pet_damage,13)
        self.assertEqual(hit.hp_after,72)
        self.assertEqual(hit.ride_pet_hp_after,87)
        self.assertTrue(resolved.defenders_after[0].ride.mounted)

    def test_exact_zero_ride_pet_preserves_source_mounted_quirk(self):
        ride=AttackMagicRideTargetState(
            pet_id="ride:1",
            hp=13,
            max_hp=100,
            pure_attrs=ElementAttrs(100,0,0,0),
        )
        resolved=resolve_enemy_attack_magic_action(
            plan=plan(),
            caster=caster(),
            defenders_by_slot={
                0:player(
                    hp=100,
                    pure_attrs=ElementAttrs(0,100,0,0),
                    ride=ride,
                    sleep_turns=0,
                )
            },
            rolls=EnemyAttackMagicActionRolls(
                0,
                {0:AttackMagicTargetRolls(100,0)},
            ),
        )
        after=resolved.defenders_after[0].ride
        self.assertEqual(after.hp,0)
        self.assertTrue(after.mounted)
        self.assertFalse(after.petfall)


    def test_no_target_multilist_early_return_consumes_no_rng(self):
        empty_plan=Recovered25EnemyAttackMagicPlan(
            skill_id=1001,
            magic_id=301,
            item_config_id=19647,
            item_runtime_role=NONPLAYER_ITEM_ROLE,
            magic_idx=8,
            element=0,
            power=100,
            magic_level=1,
            actor_slot=15,
            source_target_slot=0,
            source_selector=0,
            normalized_selector=None,
            target_membership=(),
            source_sort_portable=True,
            source_target_order=(),
        )
        resolved=resolve_enemy_attack_magic_action(
            plan=empty_plan,
            caster=caster(),
            defenders_by_slot={},
            rolls=EnemyAttackMagicActionRolls(None,{}),
        )
        self.assertIsNone(resolved.true_magic_success)
        self.assertEqual(resolved.targets,())

        with self.assertRaisesRegex(ValueError,"cannot consume cast RNG"):
            resolve_enemy_attack_magic_action(
                plan=empty_plan,
                caster=caster(),
                defenders_by_slot={},
                rolls=EnemyAttackMagicActionRolls(0,{}),
            )

    def test_nonportable_plan_fails_closed_before_rng_execution(self):
        with self.assertRaisesRegex(ValueError,"exact portable"):
            resolve_enemy_attack_magic_action(
                plan=plan(target_order=(0,1),portable=False),
                caster=caster(),
                defenders_by_slot={0:player()},
                rolls=EnemyAttackMagicActionRolls(
                    0,
                    {0:AttackMagicTargetRolls(100,0)},
                ),
            )

    def test_non_dodged_target_requires_damage_random(self):
        with self.assertRaisesRegex(KeyError,"requires damage random"):
            resolve_enemy_attack_magic_action(
                plan=plan(),
                caster=caster(),
                defenders_by_slot={0:player()},
                rolls=EnemyAttackMagicActionRolls(
                    0,
                    {0:AttackMagicTargetRolls(100,None)},
                ),
            )


if __name__=="__main__":
    unittest.main()
