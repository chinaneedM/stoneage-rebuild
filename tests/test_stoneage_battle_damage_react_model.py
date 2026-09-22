import unittest

from tools.stoneage_battle_damage_react_model import (
    DAMAGE_REACT_ABSROB,
    DAMAGE_REACT_NONE,
    DAMAGE_REACT_REFLEC,
    DAMAGE_REACT_VANISH,
    BaseDamageReactState,
    apply_base_magic_def,
    base_damage_react_active,
    base_damage_react_blocks_main_continuation,
    base_damage_react_kind,
    resolve_base_damage_react,
)


class BattleDamageReactModelTests(unittest.TestCase):
    def test_reaction_priority_is_vanish_absorb_reflect(self):
        state=BaseDamageReactState(absorb=2,reflect=3,vanish=1)
        self.assertEqual(base_damage_react_kind(state),DAMAGE_REACT_VANISH)
        self.assertEqual(
            base_damage_react_kind(BaseDamageReactState(absorb=2,reflect=3)),
            DAMAGE_REACT_ABSROB,
        )
        self.assertEqual(
            base_damage_react_kind(BaseDamageReactState(reflect=3)),
            DAMAGE_REACT_REFLEC,
        )
        self.assertEqual(
            base_damage_react_kind(BaseDamageReactState()),
            DAMAGE_REACT_NONE,
        )

    def test_magic_def_directly_overwrites_selected_charge(self):
        state=BaseDamageReactState(absorb=1,reflect=2,vanish=3)
        state=apply_base_magic_def(state,kind=DAMAGE_REACT_REFLEC,count=7)
        self.assertEqual(state,BaseDamageReactState(absorb=1,reflect=7,vanish=3))
        state=apply_base_magic_def(state,kind=DAMAGE_REACT_VANISH,count=0)
        self.assertEqual(state.vanish,0)

    def test_nonpositive_damage_consumes_no_charge(self):
        state=BaseDamageReactState(vanish=2)
        result=resolve_base_damage_react(
            state,
            raw_damage=0,
            attacker_hp=100,
            attacker_max_hp=100,
            defender_hp=80,
            defender_max_hp=100,
        )
        self.assertEqual(result.state_after,state)
        self.assertFalse(result.charge_consumed)
        self.assertEqual(result.damage_target,"none")
        self.assertIsNone(result.wakeup_target)

    def test_vanish_preserves_hp_and_consumes_one_charge(self):
        result=resolve_base_damage_react(
            BaseDamageReactState(vanish=2),
            raw_damage=40,
            attacker_hp=100,
            attacker_max_hp=100,
            defender_hp=80,
            defender_max_hp=100,
        )
        self.assertEqual(result.selected_kind,DAMAGE_REACT_VANISH)
        self.assertEqual(result.effective_kind,DAMAGE_REACT_VANISH)
        self.assertEqual(result.defender_hp_after,80)
        self.assertEqual(result.attacker_hp_after,100)
        self.assertEqual(result.state_after.vanish,1)
        self.assertEqual(result.damage_target,"none")
        self.assertIsNone(result.wakeup_target)

    def test_absorb_heals_to_cap_and_consumes_one_charge(self):
        result=resolve_base_damage_react(
            BaseDamageReactState(absorb=2),
            raw_damage=40,
            attacker_hp=100,
            attacker_max_hp=100,
            defender_hp=80,
            defender_max_hp=100,
        )
        self.assertEqual(result.effective_kind,DAMAGE_REACT_ABSROB)
        self.assertEqual(result.defender_hp_after,100)
        self.assertEqual(result.state_after.absorb,1)
        self.assertEqual(result.damage_target,"none")
        self.assertIsNone(result.wakeup_target)

    def test_reflect_hits_attacker_and_consumes_one_charge(self):
        result=resolve_base_damage_react(
            BaseDamageReactState(reflect=2),
            raw_damage=40,
            attacker_hp=70,
            attacker_max_hp=100,
            defender_hp=80,
            defender_max_hp=100,
        )
        self.assertEqual(result.effective_kind,DAMAGE_REACT_REFLEC)
        self.assertEqual(result.attacker_hp_after,30)
        self.assertEqual(result.defender_hp_after,80)
        self.assertEqual(result.state_after.reflect,1)
        self.assertEqual(result.damage_target,"attacker")
        self.assertEqual(result.wakeup_target,"attacker")

    def test_throwing_weapon_bypasses_reflect_without_consuming_charge(self):
        state=BaseDamageReactState(reflect=2)
        result=resolve_base_damage_react(
            state,
            raw_damage=40,
            attacker_hp=70,
            attacker_max_hp=100,
            defender_hp=80,
            defender_max_hp=100,
            attacker_uses_throwing_weapon=True,
        )
        self.assertEqual(result.selected_kind,DAMAGE_REACT_REFLEC)
        self.assertEqual(result.effective_kind,DAMAGE_REACT_NONE)
        self.assertTrue(result.reflect_blocked_by_throwing_weapon)
        self.assertEqual(result.state_after,state)
        self.assertEqual(result.defender_hp_after,40)
        self.assertEqual(result.wakeup_target,"defender")

    def test_normal_damage_hits_defender(self):
        result=resolve_base_damage_react(
            BaseDamageReactState(),
            raw_damage=40,
            attacker_hp=70,
            attacker_max_hp=100,
            defender_hp=30,
            defender_max_hp=100,
        )
        self.assertEqual(result.defender_hp_after,0)
        self.assertEqual(result.damage_target,"defender")
        self.assertEqual(result.wakeup_target,"defender")

    def test_any_reaction_on_either_side_blocks_main_continuation(self):
        empty=BaseDamageReactState()
        reflect=BaseDamageReactState(reflect=1)
        vanish=BaseDamageReactState(vanish=1)
        self.assertFalse(base_damage_react_active(empty))
        self.assertTrue(base_damage_react_active(reflect))
        self.assertTrue(
            base_damage_react_blocks_main_continuation(reflect,empty)
        )
        self.assertTrue(
            base_damage_react_blocks_main_continuation(empty,vanish)
        )
        self.assertFalse(
            base_damage_react_blocks_main_continuation(empty,empty)
        )

    def test_negative_counts_and_invalid_kind_fail_closed(self):
        with self.assertRaises(ValueError):
            BaseDamageReactState(reflect=-1)
        with self.assertRaises(ValueError):
            apply_base_magic_def(BaseDamageReactState(),kind=0,count=1)
        with self.assertRaises(ValueError):
            apply_base_magic_def(
                BaseDamageReactState(),
                kind=DAMAGE_REACT_ABSROB,
                count=-1,
            )


if __name__=="__main__":
    unittest.main()
