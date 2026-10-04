import unittest
from tools.stoneage_refresh_model import (
    parse_refresh_option, resolve_refresh_setup, resolve_refresh_recovery,
    RefreshSourceDomain, PROFILE_FACTS,
)


def vector(profile='iris', **states):
    result = [0]*PROFILE_FACTS[profile][0]
    for status, value in states.items():
        result[int(status)] = value
    return tuple(result)


class RefreshReferenceTests(unittest.TestCase):
    def test_cp950_single_status_and_wildcard(self):
        for marker, status in (('全',0),('默',10),('虛',7),('劇',8),('障',9)):
            self.assertEqual(parse_refresh_option(marker.encode('cp950'),profile='iris',execution_charset='cp950'),status)

    def test_utf8_two_byte_collision_selects_first_label(self):
        # Eye/sleep share E7 9C although they are different full characters.
        self.assertEqual(parse_refresh_option('眼'.encode(),profile='iris',execution_charset='utf-8'),3)
        self.assertEqual(parse_refresh_option('虚弱'.encode(),profile='bismarck',execution_charset='utf-8'),7)

    def test_empty_and_null_and_short_table_nonmatch(self):
        self.assertIsNone(parse_refresh_option(b'',profile='iris',execution_charset='cp950'))
        for raw in (None,b'x',b'\xff','默'.encode(),b'x'+ '默'.encode('cp950'),b'\0'):
            with self.subTest(raw=raw),self.assertRaises(RefreshSourceDomain):
                parse_refresh_option(raw,profile='iris',execution_charset='cp950')

    def test_complete_bismarck_table_can_scan_and_return_no_match(self):
        self.assertIsNone(parse_refresh_option(b'plain',profile='bismarck',execution_charset='utf-8'))
        self.assertEqual(parse_refresh_option(b'x'+ '沉默'.encode(),profile='bismarck',execution_charset='utf-8'),10)

    def test_unencodable_whole_profile_build_is_rejected(self):
        for profile in ('gavin','bismarck'):
            with self.assertRaises(RefreshSourceDomain):
                parse_refresh_option(b'',profile=profile,execution_charset='cp950')

    def test_callback_preserves_high_and_ignores_option(self):
        for before, expected in ((0x12345678,0x12340017),(-65535,-65513)):
            result=resolve_refresh_setup(target_slot=19,skill_array=23,packed_com3_before=before)
            self.assertEqual((result.packed_com3,result.target_slot,result.source_return_value),(expected,19,True))

    def test_clean_actor_can_clear_target_but_returns_false(self):
        result=resolve_refresh_recovery(10,profile='iris',actor_counters=vector(),target_counters=(vector(**{'10':3}),))
        self.assertFalse(result.source_return_value)
        self.assertEqual(result.receive_effect_name,'SPR_hoshi')
        self.assertEqual(result.cleared_statuses,(10,))
        self.assertEqual(result.silence_clear_targets,(0,))

    def test_affected_actor_returns_true_even_with_no_target_recovery(self):
        result=resolve_refresh_recovery(7,profile='iris',actor_counters=vector(**{'7':2}),target_counters=(vector(),vector(**{'10':3})))
        self.assertTrue(result.source_return_value)
        self.assertEqual(result.receive_effect_name,'SPR_tyusya')
        self.assertEqual(result.cleared_statuses,(None,None))

    def test_specific_status_is_masked_by_higher_positive_counter(self):
        row=vector(**{'1':3,'10':2})
        result=resolve_refresh_recovery(1,profile='iris',actor_counters=vector(),target_counters=(row,))
        self.assertEqual(result.target_counters,(row,))

    def test_wildcard_clears_only_highest_including_extended_state(self):
        result=resolve_refresh_recovery(0,profile='iris',actor_counters=vector(),target_counters=(vector(**{'1':3,'10':2,'43':7}),))
        self.assertFalse(result.source_return_value)
        self.assertEqual(result.cleared_statuses,(43,))
        self.assertEqual((result.target_counters[0][1],result.target_counters[0][10]),(3,2))
        self.assertEqual(result.silence_clear_targets,())

    def test_negative_zero_counters_are_inactive_and_targets_independent(self):
        result=resolve_refresh_recovery(0,profile='iris',actor_counters=vector(),target_counters=(vector(**{'1':3,'10':-2}),vector(**{'10':1})))
        self.assertEqual(result.cleared_statuses,(1,10))
        self.assertEqual(result.silence_clear_targets,(1,))

    def test_no_marker_stops_before_effect_and_recovery(self):
        row=vector(**{'10':3})
        result=resolve_refresh_recovery(None,profile='iris',actor_counters=vector(),target_counters=(row,))
        self.assertIsNone(result.receive_effect_name)
        self.assertEqual(result.target_counters,(row,))

    def test_invalid_vector_and_work_domain_rejected(self):
        for row in ((0,),vector(**{'0':1}),vector(**{'10':2**31})):
            with self.assertRaises(RefreshSourceDomain):
                resolve_refresh_recovery(10,profile='iris',actor_counters=row,target_counters=())
        with self.assertRaises(RefreshSourceDomain):
            resolve_refresh_setup(target_slot=0,skill_array=True,packed_com3_before=0)


if __name__ == '__main__':
    unittest.main()
