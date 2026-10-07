import unittest

from tools.stoneage_becomepig_native_audit import checked_decimal_prefix, _post_expected, INT_MAX, INT_MIN


class NativeDomainTests(unittest.TestCase):
    def test_empty_and_partial_parse_are_not_three_initialized_ints(self):
        self.assertEqual(checked_decimal_prefix(b""), ())
        self.assertEqual(checked_decimal_prefix(b"30"), (30,))
        self.assertEqual(checked_decimal_prefix(b"30 60"), (30, 60))

    def test_decimal_prefix_tracks_adjacent_signs_and_failure_stop(self):
        self.assertEqual(checked_decimal_prefix(b"30+60-100250"), (30,60,-100250))
        self.assertEqual(checked_decimal_prefix(b"30 x 60"), (30,))
        self.assertEqual(checked_decimal_prefix(b"0x20 60"), (0,))
        self.assertEqual(checked_decimal_prefix(b"  +30\t060\r100250tail"), (30,60,100250))

    def test_overflow_is_rejected_before_native_decimal_conversion(self):
        for raw in (b"2147483648 60", b"-2147483649 60", b"30 2147483648", b"30 60 2147483648"):
            with self.subTest(raw=raw):
                with self.assertRaisesRegex(ValueError,"conversion overflow"):
                    checked_decimal_prefix(raw)
        self.assertEqual(checked_decimal_prefix(b"2147483647 -2147483648"), (INT_MAX, INT_MIN))

    def test_non_ascii_nul_and_buffer_overrun_domains_are_excluded(self):
        for raw in (b"30\0 60", b"\xff", b" "*256):
            with self.subTest(raw=raw):
                with self.assertRaises(ValueError):
                    checked_decimal_prefix(raw)

    def test_first_hit_intermediate_overflow_is_not_cancelled_by_minus_one(self):
        v=(1,0,1,0,1,0,-1,-1)
        with self.assertRaisesRegex(ValueError,"signed addition"):
            _post_expected(v,100,INT_MAX,100250,guarded=True)

    def test_repeat_addition_overflow_is_excluded_before_execution(self):
        v=(1,0,1,0,1,0,1999999999,-1)
        with self.assertRaisesRegex(ValueError,"signed addition"):
            _post_expected(v,100,200000000,100250,guarded=True)

    def test_preaddition_guard_excludes_draw_even_when_hypothetical_sum_is_huge(self):
        v=(1,0,1,0,1,0,2000000000,-1)
        row=_post_expected(v,100,INT_MAX,100250,guarded=True)
        self.assertEqual(row[4:7], (0,0,0))
        self.assertEqual(row[9], 2000000000)


if __name__=="__main__":
    unittest.main()
