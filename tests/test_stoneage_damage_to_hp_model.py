import unittest

from tools.stoneage_damage_to_hp_model import (
    c_atoi,
    c_int_div,
    damage_to_hp_attack_power,
    parse_damage_to_hp_option,
    resolve_damage_to_hp_recovery,
)


class DamageToHpModelTests(unittest.TestCase):
    def test_c_atoi_and_integer_division_follow_source_shape(self):
        self.assertEqual(c_atoi("  -37tail"),-37)
        self.assertEqual(c_atoi("x99"),0)
        self.assertEqual(c_int_div(-99,100),0)
        self.assertEqual(c_int_div(-101,100),-1)

    def test_callback_preserves_integer_division_bug(self):
        opt=parse_damage_to_hp_option("30|50")
        self.assertEqual(opt.callback_integer_ratio,0)
        self.assertEqual(damage_to_hp_attack_power(123,opt),123)

        opt=parse_damage_to_hp_option("100|50")
        self.assertEqual(opt.callback_integer_ratio,1)
        self.assertEqual(damage_to_hp_attack_power(123,opt),0)

    def test_recovery_uses_damage_plus_petdamage_and_caps_to_missing_hp(self):
        opt=parse_damage_to_hp_option("30|50")
        result=resolve_damage_to_hp_recovery(
            damage=80,
            petdamage=20,
            attacker_hp=470,
            attacker_max_hp=500,
            target_damage_react=0,
            option=opt,
        )
        self.assertTrue(result.attempted)
        self.assertEqual(result.damage_basis,100)
        self.assertEqual(result.reported_recovery,30)
        self.assertEqual(result.attacker_hp_after,500)

    def test_damage_react_blocks_recovery(self):
        opt=parse_damage_to_hp_option("30|50")
        result=resolve_damage_to_hp_recovery(
            damage=100,
            petdamage=0,
            attacker_hp=100,
            attacker_max_hp=500,
            target_damage_react=1,
            option=opt,
        )
        self.assertFalse(result.attempted)
        self.assertTrue(result.target_damage_react_blocked)
        self.assertEqual(result.attacker_hp_after,100)

    def test_nonpositive_damage_basis_skips_recovery(self):
        opt=parse_damage_to_hp_option("30|50")
        result=resolve_damage_to_hp_recovery(
            damage=0,
            petdamage=0,
            attacker_hp=100,
            attacker_max_hp=500,
            target_damage_react=0,
            option=opt,
        )
        self.assertFalse(result.attempted)
        self.assertEqual(result.reported_recovery,0)


if __name__ == "__main__":
    unittest.main()
