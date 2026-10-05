import unittest

from tools.stoneage_battlemodel_reference_model import (
    PROFILE_BIG5,
    PROFILE_UTF8,
    TYPE_COVER_ALL_BIT,
    TYPE_PHYSICAL_BIT,
    inspect_battlemodel_option,
    resolve_battlemodel_attack_contract,
    resolve_battlemodel_setup,
    resolve_battlemodel_target_plan,
)


def option(*,attack_type="1",objects="2",status="",turn="",hit="",stats="",actions="100 101"):
    return "|".join(
        (attack_type,objects,status,turn,hit,stats,actions)
    ).encode("big5")


class BattleModelReferenceTests(unittest.TestCase):
    def test_positive_count_owns_no_callback_rng_and_above10_clamps(self):
        r=resolve_battlemodel_setup(
            option(objects="15"),profile=PROFILE_BIG5,skill_array=638,
            powers_before=(100,80,70),object_count_roll=None,
        )
        self.assertEqual((r.attack_type,r.object_count,r.rng_draws),(1,10,0))
        self.assertEqual(r.packed_com2,0x000A0001)
        self.assertTrue(r.command_written and r.mode_written and r.com2_written and r.com3_written)
        with self.assertRaisesRegex(ValueError,"owns no callback RNG"):
            resolve_battlemodel_setup(
                option(objects="2"),profile=PROFILE_BIG5,skill_array=638,
                powers_before=(100,80,70),object_count_roll=1,
            )

    def test_nonpositive_count_owns_exactly_one_rand_1_10(self):
        for configured in ("0","-3","nonnumeric"):
            with self.subTest(configured=configured):
                r=resolve_battlemodel_setup(
                    option(objects=configured),profile=PROFILE_BIG5,skill_array=638,
                    powers_before=(100,80,70),object_count_roll=7,
                )
                self.assertEqual((r.object_count,r.rng_draws),(7,1))
        with self.assertRaisesRegex(ValueError,"requires RAND"):
            resolve_battlemodel_setup(
                option(objects="0"),profile=PROFILE_BIG5,skill_array=638,
                powers_before=(100,80,70),object_count_roll=None,
            )

    def test_field6_preserves_sequential_attackpower_baseline_bug(self):
        raw=option(stats="攻%50 防%10 敏20")
        r=resolve_battlemodel_setup(
            raw,profile=PROFILE_BIG5,skill_array=638,
            powers_before=(100,80,70),object_count_roll=None,
        )
        # Attack becomes 150 first. Defence then uses current ATTACK=150 as
        # its percent baseline (165), not old defence=80. Quick is absolute 20.
        self.assertEqual(r.powers,(150,165,20))

    def test_field6_absolute_values_are_positional(self):
        r=resolve_battlemodel_setup(
            option(stats="攻120 防80 敏60"),profile=PROFILE_BIG5,
            skill_array=638,powers_before=(100,90,70),object_count_roll=None,
        )
        self.assertEqual(r.powers,(120,80,60))

    def test_utf8_matching_modifier_fails_closed_on_historical_fixed_byte_offset(self):
        raw="1|2||||攻%50 防%10 敏20|100".encode("utf-8")
        with self.assertRaisesRegex(ValueError,"fixed-byte"):
            resolve_battlemodel_setup(
                raw,profile=PROFILE_UTF8,skill_array=638,
                powers_before=(100,80,70),object_count_roll=None,
            )

    def test_option_inspection_is_derived_only_and_keeps_action_numbers(self):
        raw=option(attack_type="5",objects="3",status="毒",turn="2",hit="40",
                   stats="攻%10",actions="101 102 103 104 999")
        shape=inspect_battlemodel_option(raw)
        self.assertEqual((shape.type_value,shape.configured_object_count),(5,3))
        self.assertEqual((shape.turn_value,shape.hit_value),(2,40))
        self.assertEqual(shape.action_numbers,(101,102,103,104))
        self.assertGreater(shape.status_token_bytes,0)
        self.assertTrue(shape.field7_present)

    def test_fewer_objects_type2_attacks_only_prefix_without_rng(self):
        r=resolve_battlemodel_target_plan(
            attack_type=0,object_count=2,
            living_opposing_slots=(0,2,4,6,8),
            action_numbers=(100,101),excess_target_rolls=(),
        )
        self.assertEqual(
            [(x.object_index,x.target_slot,x.action_number) for x in r.attacks],
            [(0,0,100),(1,2,101)],
        )
        self.assertEqual(r.target_rng_draws,0)
        self.assertFalse(r.covers_all_targets)

    def test_fewer_objects_type1_cycles_objects_over_remaining_targets(self):
        r=resolve_battlemodel_target_plan(
            attack_type=TYPE_COVER_ALL_BIT,object_count=2,
            living_opposing_slots=(0,2,4,6,8),
            action_numbers=(100,101),excess_target_rolls=(),
        )
        self.assertEqual(
            [(x.object_index,x.target_slot,x.action_number) for x in r.attacks],
            [(0,0,100),(1,2,101),(0,4,100),(1,6,101),(0,8,100)],
        )
        self.assertEqual(r.target_rng_draws,0)
        self.assertTrue(r.covers_all_targets)

    def test_excess_objects_each_own_one_random_target_draw_with_replacement(self):
        r=resolve_battlemodel_target_plan(
            attack_type=0,object_count=4,
            living_opposing_slots=(1,3),
            action_numbers=(10,20),excess_target_rolls=(1,0),
        )
        self.assertEqual(
            [(x.object_index,x.target_slot,x.action_number) for x in r.attacks],
            [(0,1,10),(1,3,20),(2,3,10),(3,1,20)],
        )
        self.assertEqual(r.target_rng_draws,2)
        self.assertTrue(r.covers_all_targets)
        with self.assertRaisesRegex(ValueError,"one explicit"):
            resolve_battlemodel_target_plan(
                attack_type=0,object_count=4,living_opposing_slots=(1,3),
                action_numbers=(10,),excess_target_rolls=(0,),
            )

    def test_no_living_target_fails_closed_instead_of_modeling_rand_zero_minus_one(self):
        with self.assertRaisesRegex(ValueError,"RAND\(0,-1\)"):
            resolve_battlemodel_target_plan(
                attack_type=0,object_count=1,living_opposing_slots=(),
                action_numbers=(10,),excess_target_rolls=(),
            )

    def test_type_bit2_is_the_physical_guardian_switch(self):
        nonphysical=resolve_battlemodel_attack_contract(0)
        physical=resolve_battlemodel_attack_contract(TYPE_PHYSICAL_BIT)
        self.assertFalse(nonphysical.physical)
        self.assertFalse(nonphysical.guardian_redirect_enabled)
        self.assertTrue(physical.physical)
        self.assertTrue(physical.guardian_redirect_enabled)
        for contract in (nonphysical,physical):
            self.assertTrue(contract.damage_sub_marker_written)
            self.assertTrue(contract.reflect_return_damage_suppressed)
            self.assertTrue(contract.trap_return_damage_suppressed)
            self.assertTrue(contract.acupuncture_return_damage_suppressed)


if __name__=="__main__":
    unittest.main()
