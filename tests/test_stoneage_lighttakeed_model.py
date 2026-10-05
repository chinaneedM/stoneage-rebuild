import unittest

from tools.stoneage_battle_damage_react_model import (
    DAMAGE_REACT_ABSROB,
    DAMAGE_REACT_NONE,
    DAMAGE_REACT_REFLEC,
    DAMAGE_REACT_VANISH,
    BaseDamageReactState,
)
from tools.stoneage_lighttakeed_model import (
    PROFILE_BISMARCK_COPY_PLUS_ONE,
    PROFILE_GAVIN_IRIS_COPY,
    resolve_lighttakeed_reaction,
)


def resolve(
    *,
    profile=PROFILE_GAVIN_IRIS_COPY,
    marker=DAMAGE_REACT_VANISH,
    attacker=BaseDamageReactState(),
    defender=BaseDamageReactState(),
    damage=30,
    attacker_hp=100,
    defender_hp=80,
    throwing=False,
):
    return resolve_lighttakeed_reaction(
        profile=profile,
        marker_kind=marker,
        attacker_state=attacker,
        defender_state=defender,
        raw_damage=damage,
        attacker_hp=attacker_hp,
        attacker_max_hp=100,
        defender_hp=defender_hp,
        defender_max_hp=100,
        attacker_uses_throwing_weapon=throwing,
    )


class LighttakeedModelTests(unittest.TestCase):
    def test_gavin_iris_vanish_positive_hit_consumes_then_copies_remaining(self):
        r=resolve(
            marker=DAMAGE_REACT_VANISH,
            attacker=BaseDamageReactState(absorb=4,reflect=5,vanish=9),
            defender=BaseDamageReactState(vanish=2),
        )
        self.assertTrue(r.matched_reaction)
        self.assertTrue(r.lighttake_case_executed)
        self.assertFalse(r.demoted_to_ordinary)
        self.assertEqual(r.post_branch_read_target,"defender")
        self.assertEqual(r.observed_counter_value,1)
        self.assertEqual(r.transferred_count,1)
        self.assertEqual(r.defender_state_after.vanish,1)
        self.assertEqual(r.attacker_state_after.vanish,1)
        self.assertEqual(r.attacker_state_after.absorb,4)
        self.assertEqual(r.attacker_state_after.reflect,5)
        self.assertTrue(r.damage_react_resolution.charge_consumed)
        self.assertEqual(r.damage_react_resolution.effective_kind,DAMAGE_REACT_VANISH)
        self.assertEqual(r.damage_react_resolution.defender_hp_after,80)

    def test_bismarck_absorb_positive_hit_transfers_remaining_plus_one(self):
        r=resolve(
            profile=PROFILE_BISMARCK_COPY_PLUS_ONE,
            marker=DAMAGE_REACT_ABSROB,
            attacker=BaseDamageReactState(absorb=8),
            defender=BaseDamageReactState(absorb=3),
        )
        self.assertEqual(r.post_branch_read_target,"defender")
        self.assertEqual(r.observed_counter_value,2)
        self.assertEqual(r.transferred_count,3)
        self.assertEqual(r.attacker_state_after.absorb,3)
        self.assertEqual(r.defender_state_after.absorb,2)
        self.assertEqual(r.damage_react_resolution.defender_hp_after,100)

    def test_zero_damage_returns_before_refetch_but_still_transfers(self):
        r=resolve(
            marker=DAMAGE_REACT_REFLEC,
            attacker=BaseDamageReactState(reflect=7),
            defender=BaseDamageReactState(reflect=2),
            damage=0,
        )
        self.assertTrue(r.matched_reaction)
        self.assertEqual(r.post_branch_read_target,"defender")
        self.assertEqual(r.observed_counter_value,2)
        self.assertEqual(r.transferred_count,2)
        self.assertEqual(r.attacker_state_after.reflect,2)
        self.assertEqual(r.defender_state_after.reflect,2)
        self.assertEqual(r.damage_react_resolution.raw_damage,0)
        self.assertFalse(r.damage_react_resolution.charge_consumed)

    def test_active_mismatch_demotes_and_runs_ordinary_highest_priority_reaction(self):
        r=resolve(
            marker=DAMAGE_REACT_REFLEC,
            attacker=BaseDamageReactState(reflect=7),
            defender=BaseDamageReactState(vanish=2,reflect=4),
        )
        self.assertFalse(r.matched_reaction)
        self.assertFalse(r.lighttake_case_executed)
        self.assertTrue(r.demoted_to_ordinary)
        self.assertIsNone(r.post_branch_read_target)
        self.assertIsNone(r.transferred_count)
        self.assertEqual(r.selected_reaction_kind,DAMAGE_REACT_VANISH)
        self.assertEqual(r.defender_state_after.vanish,1)
        self.assertEqual(r.defender_state_after.reflect,4)
        self.assertEqual(r.attacker_state_after.reflect,7)
        self.assertEqual(r.damage_react_resolution.effective_kind,DAMAGE_REACT_VANISH)
        self.assertEqual(r.damage_react_resolution.defender_hp_after,80)

    def test_no_active_reaction_keeps_lighttake_case_but_transfers_nothing(self):
        r=resolve(
            marker=DAMAGE_REACT_ABSROB,
            defender=BaseDamageReactState(),
        )
        self.assertEqual(r.selected_reaction_kind,DAMAGE_REACT_NONE)
        self.assertFalse(r.matched_reaction)
        self.assertTrue(r.lighttake_case_executed)
        self.assertFalse(r.demoted_to_ordinary)
        self.assertIsNone(r.post_branch_read_target)
        self.assertIsNone(r.transferred_count)
        self.assertEqual(r.damage_react_resolution.defender_hp_after,50)

    def test_nonthrowing_reflect_redirect_makes_gavin_iris_post_branch_self_copy(self):
        r=resolve(
            marker=DAMAGE_REACT_REFLEC,
            attacker=BaseDamageReactState(reflect=7),
            defender=BaseDamageReactState(reflect=2),
            attacker_hp=100,
        )
        self.assertTrue(r.matched_reaction)
        self.assertEqual(r.defender_state_after.reflect,1)
        self.assertEqual(r.damage_react_resolution.attacker_hp_after,70)
        self.assertEqual(r.damage_react_resolution.defender_hp_after,80)
        self.assertEqual(r.post_branch_read_target,"attacker")
        self.assertEqual(r.observed_counter_value,7)
        self.assertEqual(r.transferred_count,7)
        self.assertEqual(r.attacker_state_after.reflect,7)

    def test_nonthrowing_reflect_bismarck_increments_attacker_own_counter(self):
        r=resolve(
            profile=PROFILE_BISMARCK_COPY_PLUS_ONE,
            marker=DAMAGE_REACT_REFLEC,
            attacker=BaseDamageReactState(reflect=7),
            defender=BaseDamageReactState(reflect=2),
        )
        self.assertEqual(r.defender_state_after.reflect,1)
        self.assertEqual(r.post_branch_read_target,"attacker")
        self.assertEqual(r.observed_counter_value,7)
        self.assertEqual(r.transferred_count,8)
        self.assertEqual(r.attacker_state_after.reflect,8)

    def test_throwing_reflect_bypasses_consumption_and_reads_defender(self):
        r=resolve(
            marker=DAMAGE_REACT_REFLEC,
            attacker=BaseDamageReactState(reflect=7),
            defender=BaseDamageReactState(reflect=2),
            throwing=True,
        )
        self.assertTrue(r.matched_reaction)
        self.assertEqual(r.defender_state_after.reflect,2)
        self.assertTrue(r.damage_react_resolution.reflect_blocked_by_throwing_weapon)
        self.assertEqual(r.damage_react_resolution.defender_hp_after,50)
        self.assertEqual(r.damage_react_resolution.attacker_hp_after,100)
        self.assertEqual(r.post_branch_read_target,"defender")
        self.assertEqual(r.observed_counter_value,2)
        self.assertEqual(r.attacker_state_after.reflect,2)

    def test_mismatched_reflect_retains_ordinary_throwing_weapon_bypass(self):
        r=resolve(
            marker=DAMAGE_REACT_ABSROB,
            attacker=BaseDamageReactState(reflect=7),
            defender=BaseDamageReactState(reflect=2),
            throwing=True,
        )
        self.assertTrue(r.demoted_to_ordinary)
        self.assertFalse(r.lighttake_case_executed)
        self.assertEqual(r.defender_state_after.reflect,2)
        self.assertTrue(r.damage_react_resolution.reflect_blocked_by_throwing_weapon)
        self.assertEqual(r.damage_react_resolution.defender_hp_after,50)
        self.assertEqual(r.attacker_state_after.reflect,7)

    def test_invalid_profile_and_marker_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"profile"):
            resolve_lighttakeed_reaction(
                profile="original",
                marker_kind=DAMAGE_REACT_VANISH,
                attacker_state=BaseDamageReactState(),
                defender_state=BaseDamageReactState(),
                raw_damage=0,
                attacker_hp=1,
                attacker_max_hp=1,
                defender_hp=1,
                defender_max_hp=1,
            )
        with self.assertRaisesRegex(ValueError,"marker"):
            resolve_lighttakeed_reaction(
                profile=PROFILE_GAVIN_IRIS_COPY,
                marker_kind=DAMAGE_REACT_NONE,
                attacker_state=BaseDamageReactState(),
                defender_state=BaseDamageReactState(),
                raw_damage=0,
                attacker_hp=1,
                attacker_max_hp=1,
                defender_hp=1,
                defender_max_hp=1,
            )


if __name__=="__main__":
    unittest.main()
