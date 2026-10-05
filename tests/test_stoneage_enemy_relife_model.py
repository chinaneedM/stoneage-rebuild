import unittest

from tools.stoneage_enemy_relife_model import (
    EnemyReLifeDeadEntry,
    EnemyReLifeRolls,
    resolve_enemy_relife_effect,
)


def dead(pid,slot,max_hp,**kwargs):
    return EnemyReLifeDeadEntry(
        participant_id=pid,
        slot=slot,
        hp=kwargs.pop("hp",0),
        max_hp=max_hp,
        **kwargs,
    )


class EnemyReLifeModelTests(unittest.TestCase):
    def test_selects_ascending_dead_slot_then_applies_half_hp_variance(self):
        result=resolve_enemy_relife_effect(
            adjusted_attack_target_slot=2,
            entries_by_slot={
                18:dead("late",18,100),
                11:dead("first",11,101),
                14:dead("middle",14,80),
            },
            rolls=EnemyReLifeRolls(
                dead_target_index=1,
                revive_amount_roll=40,
            ),
        )
        self.assertTrue(result.success)
        self.assertFalse(result.fallback_to_attack)
        self.assertEqual(result.candidate_slots,(11,14,18))
        self.assertEqual(result.selected_slot,14)
        self.assertEqual(result.selected_participant_id,"middle")
        self.assertEqual(result.base_power,40)
        self.assertEqual(result.revive_amount,40)
        self.assertEqual((result.hp_before,result.hp_after),(0,40))
        self.assertTrue(result.cleared_die_flag)

    def test_odd_max_hp_uses_integer_half_before_variance(self):
        result=resolve_enemy_relife_effect(
            adjusted_attack_target_slot=0,
            entries_by_slot={10:dead("odd",10,101)},
            rolls=EnemyReLifeRolls(
                dead_target_index=0,
                revive_amount_roll=55,
            ),
        )
        self.assertEqual(result.base_power,50)
        self.assertEqual(result.hp_after,55)

    def test_ineligible_dead_entries_produce_fallback_without_rng(self):
        result=resolve_enemy_relife_effect(
            adjusted_attack_target_slot=1,
            entries_by_slot={
                10:dead("ultimate",10,100,ultimate_exited=True),
                11:dead("not-attacked",11,100,is_attacked=False),
                12:dead("rescue",12,100,rescue_mode=True),
                13:dead("alive",13,100,hp=1,is_die=False),
            },
            rolls=EnemyReLifeRolls(),
        )
        self.assertFalse(result.success)
        self.assertTrue(result.fallback_to_attack)
        self.assertEqual(result.candidate_slots,())

    def test_no_candidate_rejects_unused_effect_rng(self):
        with self.assertRaisesRegex(ValueError,"no-candidate"):
            resolve_enemy_relife_effect(
                adjusted_attack_target_slot=1,
                entries_by_slot={},
                rolls=EnemyReLifeRolls(dead_target_index=0),
            )

    def test_single_candidate_still_requires_source_selection_draw(self):
        with self.assertRaisesRegex(ValueError,"target-selection"):
            resolve_enemy_relife_effect(
                adjusted_attack_target_slot=1,
                entries_by_slot={10:dead("one",10,100)},
                rolls=EnemyReLifeRolls(revive_amount_roll=50),
            )

    def test_amount_roll_bounds_are_source_shaped(self):
        with self.assertRaisesRegex(ValueError,"45..55"):
            resolve_enemy_relife_effect(
                adjusted_attack_target_slot=1,
                entries_by_slot={10:dead("one",10,100)},
                rolls=EnemyReLifeRolls(
                    dead_target_index=0,
                    revive_amount_roll=56,
                ),
            )


if __name__=="__main__":
    unittest.main()
