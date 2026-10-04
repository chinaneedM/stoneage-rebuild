import unittest

from tools.stoneage_wildviolent_model import (
    parse_wildviolent_option, resolve_wildviolent_setup,
    plan_wildviolent_nonbow_action, wildviolent_divided_damage,
    WildViolentUndefinedSourceDomain,
)


def setup(raw, **changes):
    args=dict(option=raw,execution_charset='cp950',profile='gavin',target_slot=19,
              fixed_strength=101,fixed_toughness=103,attack_power_before=77,
              defense_power_before=79,packed_com3_before=0x1234abcd)
    args.update(changes)
    return resolve_wildviolent_setup(**args)


class WildViolentReferenceTests(unittest.TestCase):
    def test_double_byte_callback_powers_and_preserved_low(self):
        result=setup('攻%50防%-50避12'.encode('cp950'))
        self.assertEqual((result.attack_power,result.defense_power),(151,52))
        self.assertEqual(result.packed_com3,0x000cabcd)
        self.assertEqual((result.command_name,result.target_slot,result.mode_name),
                         ('BATTLE_COM_S_WILDVIOLENTATTACK',19,'BATTLE_CHARMODE_C_OK'))

    def test_missing_markers_preserve_work_powers_clear_high_only(self):
        result=setup(b'plain')
        self.assertEqual((result.attack_power,result.defense_power),(77,79))
        self.assertEqual(result.packed_com3,0xabcd)

    def test_failed_float_scan_reuses_already_normalized_value(self):
        result=setup('攻%50防%bad'.encode('cp950'),fixed_toughness=10000)
        self.assertEqual((result.attack_power,result.defense_power),(151,10050))

    def test_initial_failed_scans_normalize_twice(self):
        result=setup('攻%bad防%bad'.encode('cp950'),fixed_strength=1000000,fixed_toughness=1000000)
        # The fraction is below decimal 0.0001, but its float32 product rounds
        # back to exactly 100 at this fixed strength.
        self.assertEqual((result.attack_power,result.defense_power),(1000100,1000001))

    def test_utf8_literal_offsets_do_not_parse_intended_percentages(self):
        result=setup('攻%50防%-50避12'.encode(),execution_charset='utf-8',
                     fixed_strength=1000000,fixed_toughness=1000000)
        self.assertEqual((result.attack_power,result.defense_power),(1000100,1000001))
        self.assertEqual(result.packed_com3,0xabcd)

    def test_utf8_source_literals_do_not_match_cp950_option(self):
        result=setup('攻%50防%-50避12'.encode('cp950'),execution_charset='utf-8')
        self.assertEqual((result.attack_power,result.defense_power),(77,79))

    def test_first_duplicate_marker_and_fixed_processing_order(self):
        result=setup('防%bad攻%50攻%200'.encode('cp950'),fixed_toughness=10000)
        self.assertEqual((result.attack_power,result.defense_power),(151,10050))

    def test_nullable_and_empty_profile_boundaries(self):
        result=setup(None)
        self.assertFalse(result.source_return_value)
        self.assertEqual(result.packed_com3,0x1234abcd)
        self.assertEqual(result.target_slot,19)
        self.assertTrue(setup(b'').source_return_value)
        empty=setup(b'',profile='bismarck')
        self.assertFalse(empty.source_return_value)
        self.assertEqual(empty.packed_com3,0x1234abcd)
        with self.assertRaises(WildViolentUndefinedSourceDomain):setup(None,profile='bismarck')

    def test_negative_or_overflow_high_rejected_after_observable_parse(self):
        for value in (-1,32768,2147483647):
            raw=('避'+str(value)).encode('cp950')
            self.assertEqual(parse_wildviolent_option(raw,execution_charset='cp950').additive_dodge_percent_points,value)
            with self.assertRaises(WildViolentUndefinedSourceDomain):setup(raw)

    def test_nonfinite_overflow_and_unbounded_scanners_fail_closed(self):
        for text in ('攻%nan','攻%inf','攻%1e99','攻%0x1p2','攻%1e','避2147483648'):
            with self.subTest(text=text),self.assertRaises(WildViolentUndefinedSourceDomain):setup(text.encode('cp950'))
        with self.assertRaises(WildViolentUndefinedSourceDomain):setup(b'a\0b')
        with self.assertRaises(WildViolentUndefinedSourceDomain):setup('攻%100'.encode('cp950'),fixed_strength=2**31-1)

    def test_exact_decimal_binary32_halfway_rounding(self):
        a=parse_wildviolent_option('攻%1.000000059604644775390625'.encode('cp950'),execution_charset='cp950')
        b=parse_wildviolent_option('攻%1.000000059604644775390626'.encode('cp950'),execution_charset='cp950')
        self.assertLess(a.attack_delta_fraction,b.attack_delta_fraction)

    def test_float32_strength_conversion_is_not_double_arithmetic(self):
        result=setup('攻%100'.encode('cp950'),fixed_strength=16777217)
        self.assertEqual(result.attack_power,33554433)

    def test_action_plan_explicit_count_divisor_and_original_slots(self):
        for count in range(3,11):
            plan=plan_wildviolent_nonbow_action(count_roll_3_10=count,packed_com3=0x12340007,target_slot=19)
            self.assertEqual((plan.attack_count,plan.damage_divisor,plan.additive_dodge_percent_points),(count,count,4660))
            self.assertEqual(plan.original_target_list,(19,)*20)
        for count in (2,11,None):
            with self.assertRaises(ValueError):plan_wildviolent_nonbow_action(count_roll_3_10=count,packed_com3=0,target_slot=0)

    def test_damage_minimum_nonpositive_and_float32_boundary(self):
        self.assertEqual(wildviolent_divided_damage(1,10),1)
        self.assertEqual(wildviolent_divided_damage(0,10),0)
        self.assertEqual(wildviolent_divided_damage(-7,10),-7)
        self.assertEqual(wildviolent_divided_damage(2147483647,3),715827904)
        self.assertEqual(wildviolent_divided_damage(3000,10),300)

    def test_explicit_charset_required(self):
        with self.assertRaises(ValueError):parse_wildviolent_option(b'',execution_charset='unknown')


if __name__=='__main__':unittest.main()
