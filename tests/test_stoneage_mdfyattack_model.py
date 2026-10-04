import unittest

from tools.stoneage_battle_core_model import attribute_adjusted_damage
from tools.stoneage_mdfyattack_model import (
    COMMAND_NAME, MdfyAttackOption, parse_mdfyattack_option,
    mdfyattack_callback_setup, mdfyattack_attribute_damage,
)


class MdfyAttackTests(unittest.TestCase):
    def test_exact_element_order_and_packing(self):
        for index, code in enumerate((b'EA', b'WA', b'FI', b'WI')):
            with self.subTest(code=code):
                option = parse_mdfyattack_option(code + b'|60')
                self.assertEqual((option.element_index, option.amount), (index, 60))
                self.assertEqual(option.packed_com4, (60 << 16) | index)
                self.assertEqual(option.attack_vector[index], 60)
                self.assertEqual(sum(option.attack_vector), 60)
                self.assertEqual(option.attack_vector[4], 0)

    def test_atoi_and_delimiter_helper_semantics(self):
        for raw, expected in [(b'EA|', 0), (b'WA|abc', 0), (b'FI| \t+72suffix|extra', 72),
                              (b'WI|01', 1), (b'EA||123', 0), (b'EA|-0', 0)]:
            with self.subTest(raw=raw):
                self.assertEqual(parse_mdfyattack_option(raw).amount, expected)

    def test_field_copy_truncates_at_255_bytes(self):
        self.assertEqual(parse_mdfyattack_option(b'EA|' + b' ' * 255 + b'100').amount, 0)
        self.assertEqual(parse_mdfyattack_option(b'EA|' + b' ' * 254 + b'1' + b'99').amount, 1)

    def test_invalid_codes_missing_second_field_and_non_ascii(self):
        for raw in (b'', b'EA', b'ea|100', b'EA |100', b' EA|100', b'NO|100',
                    b'EA|100\0', b'EA|100\xff', b'\x81|EA|100'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                parse_mdfyattack_option(raw)

    def test_undefined_signed_pack_is_rejected(self):
        self.assertEqual(parse_mdfyattack_option(b'WI|32767').amount, 32767)
        for raw in (b'EA|-1', b'EA|32768', b'FI|65535', b'WA|99999999999999999999'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                parse_mdfyattack_option(raw)
        for args in ((4, 100), (-1, 100), (0, -1), (0, 32768), (0, True)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                MdfyAttackOption(*args)

    def test_callback_preserves_explicit_array_and_target(self):
        setup = mdfyattack_callback_setup(submitted_target=9, skill_array=65535, option=b'FI|60')
        self.assertEqual((setup.command_symbol, setup.submitted_target, setup.skill_array),
                         (COMMAND_NAME, 9, 65535))
        self.assertEqual(setup.option.element, 'fire')
        for array in (-1, 65536):
            with self.assertRaises(ValueError):
                mdfyattack_callback_setup(submitted_target=0, skill_array=array, option=b'FI|60')

    def test_neutral_remainder_must_stay_zero(self):
        special = mdfyattack_attribute_damage(100, parse_mdfyattack_option(b'EA|60'), (0, 0, 0, 0))
        ordinary = attribute_adjusted_damage(100, (60, 0, 0, 0), (0, 0, 0, 0))
        self.assertEqual(special, 90)
        self.assertEqual(ordinary, 130)
        self.assertEqual(mdfyattack_attribute_damage(100, parse_mdfyattack_option(b'EA|0'), (0, 0, 0, 0)), 0)

    def test_four_element_dominance_and_loss(self):
        for index, code in enumerate((b'EA', b'WA', b'FI', b'WI')):
            winning = [0] * 4; winning[(index + 1) % 4] = 100
            losing = [0] * 4; losing[(index - 1) % 4] = 100
            same = [0] * 4; same[index] = 100
            option = parse_mdfyattack_option(code + b'|100')
            self.assertEqual(mdfyattack_attribute_damage(100, option, winning), 150)
            self.assertEqual(mdfyattack_attribute_damage(100, option, losing), 60)
            self.assertEqual(mdfyattack_attribute_damage(100, option, same), 100)

    def test_field_rounding_native_witness(self):
        option = parse_mdfyattack_option(b'FI|150')
        self.assertEqual(mdfyattack_attribute_damage(137, option, (30, 20, 10, 0),
                        field_attr='fire', field_power=73), 449)

    def test_safe_non_normalized_amount_above_100(self):
        self.assertEqual(mdfyattack_attribute_damage(100, parse_mdfyattack_option(b'EA|150'), (0, 0, 0, 0)), 225)

    def test_arithmetic_overflow_and_extensions_stay_outside_reference(self):
        option = parse_mdfyattack_option(b'EA|32767')
        with self.assertRaises(ValueError):
            mdfyattack_attribute_damage(1000, option, (100, 0, 0, 0))
        with self.assertRaises(ValueError):
            mdfyattack_attribute_damage(100, option, (100, 0, 0, 0), property_hooks_active=True)
        with self.assertRaises(ValueError):
            mdfyattack_attribute_damage(100, option, (101, 0, 0, 0))
        with self.assertRaises(ValueError):
            mdfyattack_attribute_damage(100, option, (0, 0, 0, 0), field_attr='unknown')


if __name__ == '__main__':
    unittest.main()
