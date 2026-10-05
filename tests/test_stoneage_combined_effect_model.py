import unittest

from tools.stoneage_battle_status_model import (
    BaseBattleStatusRuntime, BaseBattleStatusState,
)
from tools.stoneage_combined_effect_model import (
    CombinedEffectDomain,
    resolve_combined_att_reverse240_effect,
    resolve_combined_recovery21_effect,
    resolve_combined_single_target,
    resolve_combined_status_change_effect,
    resolve_combined_status_recovery61_effect,
)
from tools.stoneage_nocast_runtime_state import NocastParticipantRuntime


def late(**kw):
    base=dict(vital=25,strength=25,toughness=25,dexterity=25)
    base.update(kw)
    return NocastParticipantRuntime(**base)


class CombinedEffectModelTests(unittest.TestCase):
    def test_live_single_target_consumes_no_retarget_rng(self):
        target=resolve_combined_single_target(0,alive_slots=(0,1))
        self.assertEqual(target.resolved_target_slot,0)
        self.assertEqual(target.retarget_draws_consumed,0)
        self.assertFalse(target.retargeted)
        with self.assertRaisesRegex(ValueError,"live single target"):
            resolve_combined_single_target(
                0,alive_slots=(0,1),retarget_draws_0_9=(0,)
            )

    def test_dead_single_target_uses_explicit_multilist_draw(self):
        target=resolve_combined_single_target(
            0,alive_slots=(1,5),retarget_draws_0_9=(1,)
        )
        self.assertEqual(target.resolved_target_slot,5)
        self.assertEqual(target.retarget_draws_consumed,1)
        self.assertTrue(target.retargeted)

    def test_recovery21_links_hp_gain_and_target_recovery_rate(self):
        effect=resolve_combined_recovery21_effect(
            source_target_slot=0,alive_slots=(0,),current_hp=900,max_hp=1000,
            target_vital=2000,target_is_player=True,rolled_power=100,riding=False,
        )
        self.assertEqual(effect.raw_gain,120)
        self.assertEqual(effect.hp_after,1000)
        self.assertEqual(effect.effect_rng_draws_consumed,1)
        self.assertEqual(effect.target.resolved_target_slot,0)

    def test_recovery21_rejects_unclosed_riding_and_bad_roll(self):
        common=dict(
            source_target_slot=0,alive_slots=(0,),current_hp=1,max_hp=100,
            target_vital=25,target_is_player=False,rolled_power=100,
        )
        with self.assertRaisesRegex(CombinedEffectDomain,"riding split"):
            resolve_combined_recovery21_effect(**common,riding=True)
        with self.assertRaisesRegex(CombinedEffectDomain,"90..110"):
            resolve_combined_recovery21_effect(
                **{**common,"rolled_power":111},riding=False
            )

    def test_iris_status_change_uses_turn5_offset15_and_command_cancel(self):
        effect=resolve_combined_status_change_effect(
            magic_id=189,source_target_slot=0,alive_slots=(0,),
            current_status=BaseBattleStatusState(),late_status_domain_clear=True,
            roll_1_100=1,attacker_level=100,defender_level=1,pvp=False,
            attacker_fixed_luck=100,defender_vital=1,defender_str=1,
            defender_tough=1,defender_dex=1,defender_resistance=0,
        )
        self.assertEqual((effect.status_index,effect.turn,effect.success_offset),(3,5,15))
        self.assertEqual(effect.status_after.sleep,5)
        self.assertEqual(effect.status_rng_draws_consumed,1)
        self.assertTrue(effect.command_cleared)

    def test_existing_base_status_blocks_status_rng_and_replacement(self):
        current=BaseBattleStatusState(poison=2)
        args=dict(
            magic_id=189,source_target_slot=0,alive_slots=(0,),
            current_status=current,late_status_domain_clear=True,
            attacker_level=100,defender_level=1,pvp=False,attacker_fixed_luck=100,
            defender_vital=1,defender_str=1,defender_tough=1,defender_dex=1,
            defender_resistance=0,
        )
        effect=resolve_combined_status_change_effect(**args,roll_1_100=None)
        self.assertEqual(effect.status_after,current)
        self.assertEqual(effect.status_rng_draws_consumed,0)
        with self.assertRaisesRegex(CombinedEffectDomain,"blocks StatusAttackCheck RNG"):
            resolve_combined_status_change_effect(**args,roll_1_100=1)

    def test_status_change_keeps_late_status_interaction_fail_closed(self):
        with self.assertRaisesRegex(CombinedEffectDomain,"late/unmodeled"):
            resolve_combined_status_change_effect(
                magic_id=139,source_target_slot=0,alive_slots=(0,),
                current_status=BaseBattleStatusState(),late_status_domain_clear=False,
                roll_1_100=1,attacker_level=1,defender_level=1,pvp=False,
                attacker_fixed_luck=0,defender_vital=1,defender_str=1,
                defender_tough=1,defender_dex=1,defender_resistance=0,
            )

    def test_status_recovery61_clears_only_highest_modeled_state(self):
        effect=resolve_combined_status_recovery61_effect(
            source_target_slot=0,alive_slots=(0,),
            base_runtime=BaseBattleStatusRuntime(
                status=BaseBattleStatusState(poison=2)
            ),
            late_runtime=late(counter=3,nc_flag=1),
        )
        self.assertEqual(effect.cleared_status,10)
        self.assertEqual(effect.base_runtime.status.poison,2)
        self.assertEqual(effect.late_runtime.counter,0)
        self.assertEqual(effect.late_runtime.nc_flag,0)

    def test_status_recovery61_rejects_unmodeled_higher_status(self):
        with self.assertRaisesRegex(ValueError,"unmodeled active status"):
            resolve_combined_status_recovery61_effect(
                source_target_slot=0,alive_slots=(0,),
                base_runtime=BaseBattleStatusRuntime(),
                late_runtime=late(unmodeled_status_active=True),
            )

    def test_att_reverse240_toggles_flag_and_swaps_immediately(self):
        effect=resolve_combined_att_reverse240_effect(
            source_target_slot=0,alive_slots=(0,),battle_flags=0,
            reverse_bit=0x20,earth=10,water=20,fire=30,wind=40,
        )
        self.assertEqual(effect.battle_flags,0x20)
        self.assertEqual(
            (effect.earth,effect.water,effect.fire,effect.wind),(30,40,10,20)
        )


if __name__=="__main__":
    unittest.main()
