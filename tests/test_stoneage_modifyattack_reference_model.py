import unittest
from tools.stoneage_modifyattack_reference_model import (
    parse_modifyattack_option, modifyattack_helper_damage,
)


class ModifyAttackReferenceTests(unittest.TestCase):
    def test_integer_remainder_boundary_not_fractional_percent(self):
        option=parse_modifyattack_option(b'EA|20')
        self.assertEqual(modifyattack_helper_damage(137,option,(95,0,0,0),raw_rand=99),(164,1))
        self.assertEqual(modifyattack_helper_damage(137,option,(96,0,0,0),raw_rand=100),(301,1))
        self.assertEqual(modifyattack_helper_damage(137,option,(100,0,0,0),raw_rand=104),(301,1))
        self.assertEqual(modifyattack_helper_damage(137,option,(100,0,0,0),raw_rand=105),(164,1))

    def test_only_matched_positive_raw_attribute_owns_rand(self):
        option=parse_modifyattack_option(b'WA|80')
        self.assertEqual(modifyattack_helper_damage(100,option,(100,0,100,100)),(100,0))
        with self.assertRaises(ValueError):
            modifyattack_helper_damage(100,option,(0,1,0,0))
        self.assertEqual(modifyattack_helper_damage(100,option,(0,1,0,0),raw_rand=0),(180,1))

    def test_all_unknown_and_missing_field_are_noop(self):
        for raw in (b'ALL|100',b'ea|100',b' EA|100',b'EA |100',b'EA'):
            with self.subTest(raw=raw):
                self.assertEqual(modifyattack_helper_damage(137,parse_modifyattack_option(raw),(100,100,100,100)),(137,0))

    def test_atoi_prefix_empty_and_extra_fields(self):
        self.assertEqual(parse_modifyattack_option(b'FI| \t+72suffix|ignored').percent,72)
        for raw in (b'FI|',b'FI|abc',b'FI||100'):
            self.assertEqual(parse_modifyattack_option(raw).percent,0)
        self.assertEqual(modifyattack_helper_damage(137,parse_modifyattack_option(b'FI|-20'),(0,0,1,0),raw_rand=0),(109,1))

    def test_undefined_and_unowned_inputs_fail_closed(self):
        for raw in (b'EA|2147483648',b'EA|1\0',b'\xff|1'):
            with self.assertRaises(ValueError):
                parse_modifyattack_option(raw)
        with self.assertRaises(ValueError):
            modifyattack_helper_damage(2**31-1,parse_modifyattack_option(b'EA|100'),(1,0,0,0),raw_rand=0)
        with self.assertRaises(ValueError):
            modifyattack_helper_damage(137,None,(0,0,0,0),raw_rand=0)


if __name__=='__main__':
    unittest.main()
