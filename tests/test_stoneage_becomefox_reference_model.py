import unittest

from tools.stoneage_becomefox_reference_model import (
    FOX_IMAGE, NO_FOX_ROUND, FoxState,
    apply_active_fox_action_powers, dexcalc_source_order_fact,
    resolve_battle_exit, resolve_petin_reset,
    resolve_postattack_transform, resolve_round_recovery,
)


def base(**kw):
    values=dict(
        base_image=101743,base_base_image=101743,
        attack_power=40,defence_power=26,quick=30,
        fix_str=40,fix_tough=26,fix_dex=30,
        fox_round=NO_FOX_ROUND,ride_pet=-1,petfall=0,
    )
    values.update(kw)
    return FoxState(**values)


class BecomeFoxReferenceModelTests(unittest.TestCase):
    def decide(self, **kw):
        args=dict(
            command_is_becomefox=True,attack_result="HIT",target_alive=True,
            draw_mod_100=0,target_is_player=False,target_petflag=1,
            attacker_pig_marker=-1,arrange_guard_active=True,
            pig_guard_active=True,current_turn=7,
        )
        args.update(kw)
        return resolve_postattack_transform(base(),**args)

    def test_pre_rng_result_and_liveness_gates_consume_no_draw(self):
        for result in ("MISS","DODGE","ALLGUARD","ARRANGE"):
            got=self.decide(attack_result=result,draw_mod_100=None)
            self.assertFalse(got.draw_consumed,result)
            self.assertFalse(got.transformed,result)
        got=self.decide(target_alive=False,draw_mod_100=None)
        self.assertTrue(got.target_check_consumed)
        self.assertFalse(got.draw_consumed)

    def test_bismarck_arrange_gate_can_be_profile_disabled(self):
        got=self.decide(
            attack_result="ARRANGE",arrange_guard_active=False,draw_mod_100=0
        )
        self.assertTrue(got.draw_consumed)
        self.assertTrue(got.transformed)

    def test_draw_boundary_is_30_success_31_failure(self):
        self.assertTrue(self.decide(draw_mod_100=30).transformed)
        self.assertFalse(self.decide(draw_mod_100=31).transformed)

    def test_ineligible_target_still_consumes_draw(self):
        cases=(
            dict(target_is_player=True),
            dict(target_petflag=0),
            dict(attacker_pig_marker=0),
        )
        for case in cases:
            got=self.decide(**case)
            self.assertTrue(got.draw_consumed,case)
            self.assertFalse(got.transformed,case)

    def test_success_sets_turn_image_and_dismounts(self):
        state=base(ride_pet=55)
        got=resolve_postattack_transform(
            state,command_is_becomefox=True,attack_result="HIT",
            target_alive=True,draw_mod_100=30,target_is_player=False,
            target_petflag=1,attacker_pig_marker=-1,current_turn=9,
        )
        self.assertTrue(got.transformed)
        self.assertTrue(got.ride_image_changed)
        self.assertEqual(got.state.fox_round,9)
        self.assertEqual(got.state.base_image,FOX_IMAGE)
        self.assertEqual(got.state.ride_pet,-1)
        self.assertEqual(got.state.petfall,1)

    def test_active_action_powers_use_fixed_baselines_and_c_truncation(self):
        got=apply_active_fox_action_powers(base(
            fox_round=1,fix_str=41,fix_tough=27,fix_dex=33
        ))
        self.assertEqual(
            (got.attack_power,got.defence_power,got.quick),(32,21,26)
        )
        self.assertEqual(
            apply_active_fox_action_powers(base()).attack_power,40
        )

    def test_recovery_boundary_is_strictly_greater_than_two(self):
        state=base(
            fox_round=4,base_image=999,
            attack_power=32,defence_power=20,quick=24
        )
        hold=resolve_round_recovery(state,current_turn=6,battle_slot=7)
        self.assertFalse(hold.recovered)
        self.assertEqual(hold.state.base_image,FOX_IMAGE)
        done=resolve_round_recovery(state,current_turn=7,battle_slot=7)
        self.assertTrue(done.recovered)
        self.assertEqual(done.notify_owner_slot,2)
        self.assertEqual(done.state.fox_round,NO_FOX_ROUND)
        self.assertEqual(
            (done.state.attack_power,done.state.defence_power,done.state.quick),
            (40,26,30),
        )

    def test_exit_restores_image_and_marker_but_not_power_fields(self):
        state=base(
            fox_round=3,base_image=FOX_IMAGE,
            attack_power=32,defence_power=20,quick=24
        )
        got=resolve_battle_exit(state)
        self.assertEqual(got.base_image,101743)
        self.assertEqual(got.fox_round,NO_FOX_ROUND)
        self.assertEqual(
            (got.attack_power,got.defence_power,got.quick),(32,20,24)
        )

    def test_petin_profile_split_and_reset_precedes_noreturn(self):
        state=base(
            base_image=FOX_IMAGE,attack_power=32,defence_power=20,quick=24
        )
        old=resolve_petin_reset(
            state,accessor_profile="ordinary_int",
            ordinary_int_marker=5,work_int_marker=6,no_return=True,
        )
        self.assertTrue(old.reset_applied)
        self.assertTrue(old.no_return_blocked_after_reset)
        self.assertEqual(old.ordinary_int_marker_after,-1)
        self.assertEqual(old.work_int_marker_after,6)
        self.assertEqual(
            (old.state.attack_power,old.state.defence_power,old.state.quick),
            (40,20,30),
        )
        new=resolve_petin_reset(
            state,accessor_profile="work_int",
            ordinary_int_marker=5,work_int_marker=6,no_return=False,
        )
        self.assertEqual(new.ordinary_int_marker_after,5)
        self.assertEqual(new.work_int_marker_after,-1)

    def test_dexcalc_comment_does_not_become_runtime_rule(self):
        for profile in ("gavin","iris","bismarck"):
            fact=dexcalc_source_order_fact(profile)
            self.assertTrue(fact["default_overwrites_fox_dex"])
            self.assertFalse(
                fact["effective_extra_fox_20pct_initiative_penalty_accepted"]
            )
        self.assertEqual(
            dexcalc_source_order_fact("gavin")["default_rand_upper_fraction"],0.3
        )
        self.assertEqual(
            dexcalc_source_order_fact("bismarck")["default_rand_upper_fraction"],0.1
        )


if __name__=="__main__":
    unittest.main()
