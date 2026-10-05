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
    def test_gavin_iris_match_preserves_defender_charge_and_overwrites_attacker(self):
        r=resolve(
            marker=DAMAGE_REACT_VANISH,
            attacker=BaseDamageReactState(absorb=4,reflect=5,vanish=9),
            defender=BaseDamageReactState(vanish=2),
        )
        self.assertTrue(r.matched_reaction)
        self.assertTrue(r.lighttake_case_executed)
        self.assertFalse(r.demoted_to_ordinary)
        self.assertEqual(r.transferred_count,2)
        self.assertEqual(r.defender_state_after.vanish,2)
        self.assertEqual(r.attacker_state_after.vanish,2)
        self.assertEqual(r.attacker_state_after.absorb,4)
        self.assertEqual(r.attacker_state_after.reflect,5)
        self.assertFalse(r.damage_react_resolution.charge_consumed)
        self.assertEqual(r.damage_react_resolution.effective_kind,DAMAGE_REACT_NONE)
        self.assertEqual(r.damage_react_resolution.defender_hp_after,50)

    def test_bismarck_match_adds_one_to_observed_defender_count(self):
        r=resolve(
            profile=PROFILE_BISMARCK_COPY_PLUS_ONE,
            marker=DAMAGE_REACT_ABSROB,
            attacker=BaseDamageReactState(absorb=8),
            defender=BaseDamageReactState(absorb=3),
        )
        self.assertEqual(r.transferred_count,4)
        self.assertEqual(r.attacker_state_after.absorb,4)
        self.assertEqual(r.defender_state_after.absorb,3)
        # Matching Lighttake neutralizes ABSROB, so damage harms the defender
        # rather than healing and does not consume the ABSROB charge.
        self.assertEqual(r.damage_react_resolution.defender_hp_after,50)

    def test_zero_damage_still_transfers_when_marker_matches(self):
        r=resolve(
            marker=DAMAGE_REACT_REFLEC,
            attacker=BaseDamageReactState(),
            defender=BaseDamageReactState(reflect=2),
            damage=0,
        )
        self.assertTrue(r.matched_reaction)
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
        self.assertIsNone(r.transferred_count)
        self.assertEqual(r.damage_react_resolution.defender_hp_after,50)

    def test_matching_reflect_bypasses_reflection_even_for_throwing_weapon(self):
        r=resolve(
            marker=DAMAGE_REACT_REFLEC,
            defender=BaseDamageReactState(reflect=2),
            throwing=True,
        )
        self.assertTrue(r.matched_reaction)
        self.assertEqual(r.defender_state_after.reflect,2)
        self.assertEqual(r.damage_react_resolution.defender_hp_after,50)
        self.assertEqual(r.damage_react_resolution.attacker_hp_after,100)
        self.assertFalse(r.damage_react_resolution.reflect_blocked_by_throwing_weapon)

    def test_mismatched_reflect_retains_ordinary_throwing_weapon_bypass(self):
        r=resolve(
            marker=DAMAGE_REACT_ABSROB,
            defender=BaseDamageReactState(reflect=2),
            throwing=True,
        )
        self.assertTrue(r.demoted_to_ordinary)
        self.assertEqual(r.defender_state_after.reflect,2)
        self.assertTrue(r.damage_react_resolution.reflect_blocked_by_throwing_weapon)
        self.assertEqual(r.damage_react_resolution.defender_hp_after,50)

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
