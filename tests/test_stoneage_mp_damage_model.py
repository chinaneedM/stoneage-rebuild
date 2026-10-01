import unittest

from tools.stoneage_mp_damage_model import (
    mp_damage_attack_power,
    parse_mp_damage_option,
    resolve_mp_damage,
)


class MpDamageModelTests(unittest.TestCase):
    def test_callback_preserves_integer_division_bug(self):
        opt=parse_mp_damage_option("30|50")
        self.assertEqual(opt.callback_integer_ratio,0)
        self.assertEqual(mp_damage_attack_power(123,opt),123)
        opt=parse_mp_damage_option("100|50")
        self.assertEqual(opt.callback_integer_ratio,1)
        self.assertEqual(mp_damage_attack_power(123,opt),0)

    def test_mp_damage_uses_current_mp_percent_not_physical_damage(self):
        opt=parse_mp_damage_option("30|50")
        result=resolve_mp_damage(
            physical_damage=1,
            target_kind="player",
            target_mp=41,
            target_damage_react=0,
            option=opt,
        )
        self.assertTrue(result.attempted)
        self.assertEqual(result.mp_damage,20)
        self.assertEqual(result.mp_after,21)

    def test_enemy_and_pet_targets_are_excluded(self):
        opt=parse_mp_damage_option("30|50")
        for kind in ("enemy","pet"):
            result=resolve_mp_damage(
                physical_damage=100,
                target_kind=kind,
                target_mp=40,
                target_damage_react=0,
                option=opt,
            )
            self.assertFalse(result.attempted)
            self.assertEqual(result.mp_after,40)

    def test_damage_react_or_zero_damage_blocks_effect(self):
        opt=parse_mp_damage_option("30|50")
        self.assertFalse(resolve_mp_damage(
            physical_damage=100,target_kind="player",target_mp=40,
            target_damage_react=1,option=opt,
        ).attempted)
        self.assertFalse(resolve_mp_damage(
            physical_damage=0,target_kind="player",target_mp=40,
            target_damage_react=0,option=opt,
        ).attempted)

    def test_zero_mp_skips_effect(self):
        opt=parse_mp_damage_option("30|50")
        result=resolve_mp_damage(
            physical_damage=100,target_kind="player",target_mp=0,
            target_damage_react=0,option=opt,
        )
        self.assertFalse(result.attempted)
        self.assertEqual(result.mp_damage,0)


if __name__ == "__main__":
    unittest.main()
