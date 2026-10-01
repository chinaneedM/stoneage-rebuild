import shutil
import subprocess
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from tools.stoneage_nocast_model import (
    NocastCheckInputs, NocastOption, NocastUndefinedSourceDomain,
    nocast_blocks_direct_magic, nocast_probability_value, parse_nocast_option,
    resolve_nocast_multilist, resolve_nocast_target, resolve_nocast_tick,
)


def inputs(**changes):
    return replace(NocastCheckInputs(
        20, 20, False, 0, 25, 25, 25, 25, 0, 0, False, "player"), **changes)


class NocastModelTests(unittest.TestCase):
    def test_option_codecs_converge(self):
        for codec in ("cp950", "big5", "utf-8"):
            self.assertEqual(parse_nocast_option("turn=3 成=50".encode(codec), encoding=codec),
                             NocastOption(3, 50))

    def test_success_search_starts_after_turn_marker(self):
        self.assertEqual(parse_nocast_option("成=99 turn=4 成=25".encode("big5"), encoding="big5"),
                         NocastOption(4, 25))

    def test_source_skip_byte_is_not_a_flexible_delimiter_parser(self):
        self.assertEqual(parse_nocast_option("turn12 成50".encode("big5"), encoding="big5"),
                         NocastOption(2, 0))

    def test_scanf_prefix_and_signed_values(self):
        self.assertEqual(parse_nocast_option("turn= -2x 成= +17x".encode("big5"), encoding="big5"),
                         NocastOption(-2, 17))

    def test_missing_or_malformed_turn_is_undefined(self):
        for text in ("成=50", "turn=x 成=50", "turn"):
            with self.subTest(text=text), self.assertRaises(NocastUndefinedSourceDomain):
                parse_nocast_option(text.encode("big5"), encoding="big5")

    def test_missing_or_malformed_success_retains_zero(self):
        for text in ("turn=3", "turn=3 成=x"):
            self.assertEqual(parse_nocast_option(text.encode("big5"), encoding="big5"), NocastOption(3, 0))

    def test_nul_terminates_c_string(self):
        self.assertEqual(parse_nocast_option(b"turn=3\0" + "成=99".encode("big5"), encoding="big5"),
                         NocastOption(3, 0))

    def test_int_overflow_and_unsupported_codec_fail_closed(self):
        with self.assertRaises(NocastUndefinedSourceDomain):
            parse_nocast_option(b"turn=2147483648", encoding="big5")
        with self.assertRaises(ValueError):
            parse_nocast_option(b"turn=3", encoding="latin1")

    def test_strict_hit_boundary(self):
        self.assertEqual(nocast_probability_value(inputs(), 50), 40)
        self.assertEqual(resolve_nocast_target(inputs(), NocastOption(3, 50), roll_1_100=39).turn_written, 3)
        self.assertIsNone(resolve_nocast_target(inputs(), NocastOption(3, 50), roll_1_100=40).turn_written)

    def test_success_returns_false_and_does_not_add_one_to_turn(self):
        result = resolve_nocast_target(inputs(), NocastOption(2, 100), roll_1_100=1)
        self.assertTrue(result.hit_check_succeeded)
        self.assertEqual((result.turn_written, result.nc_flag, result.source_return_value), (2, 1, False))

    def test_pet_exclusion_is_after_rng(self):
        result = resolve_nocast_target(inputs(target_kind="pet"), NocastOption(3, 50), roll_1_100=1)
        self.assertTrue(result.rng_consumed)
        self.assertTrue(result.hit_check_succeeded)
        self.assertTrue(result.pet_excluded)
        self.assertIsNone(result.turn_written)

    def test_enemy_is_not_excluded_by_pet_gate(self):
        result = resolve_nocast_target(inputs(target_kind="enemy"), NocastOption(3, 50), roll_1_100=1)
        self.assertEqual(result.turn_written, 3)

    def test_existing_later_status_blocks_without_rng(self):
        result = resolve_nocast_target(inputs(any_existing_status=True), NocastOption(3, 50), roll_1_100=None)
        self.assertFalse(result.rng_consumed)
        with self.assertRaises(ValueError):
            resolve_nocast_target(inputs(any_existing_status=True), NocastOption(3, 50), roll_1_100=1)

    def test_explicit_mod_and_general_suit_resistance(self):
        self.assertEqual(nocast_probability_value(inputs(defender_mod_nocast=3, defender_suit_resist=4), 50), 33)

    def test_pvp_removes_level_delta_and_cap_is_upper_only(self):
        self.assertEqual(nocast_probability_value(inputs(attacker_level=100, pvp=True), 50), 40)
        self.assertEqual(nocast_probability_value(inputs(attacker_level=100), 50), 70)
        self.assertEqual(nocast_probability_value(inputs(attacker_fixed_luck=100), 50), 80)
        self.assertLess(nocast_probability_value(inputs(defender_mod_nocast=100), 50), 0)

    def test_undefined_stat_domain_is_rejected(self):
        with self.assertRaises(NocastUndefinedSourceDomain):
            nocast_probability_value(inputs(defender_vital=0, defender_strength=0,
                                           defender_toughness=0, defender_dexterity=0), 50)

    def test_missing_and_invalid_random_rolls_rejected(self):
        for roll in (None, 0, 101):
            with self.assertRaises(ValueError):
                resolve_nocast_target(inputs(), NocastOption(3, 50), roll_1_100=roll)

    def test_positive_counter_blocks_direct_magic_only(self):
        self.assertTrue(nocast_blocks_direct_magic(1))
        self.assertFalse(nocast_blocks_direct_magic(0))
        self.assertFalse(nocast_blocks_direct_magic(-1))

    def test_tick_expiry_and_active_notifications(self):
        flags = {"weaken_active_at_visit": False, "barrier_active_at_visit": False}
        result = resolve_nocast_tick(1, **flags)
        self.assertEqual((result.counter_after, result.nc_flag, result.expired), (0, 0, True))
        result = resolve_nocast_tick(3, **flags)
        self.assertEqual((result.counter_after, result.nc_flag, result.expired), (2, 1, False))
        self.assertIsNone(resolve_nocast_tick(0, **flags).nc_flag)

    def test_freeze_storage_and_expiry_use_different_counters(self):
        for weaken, barrier in ((True, False), (False, True)):
            result = resolve_nocast_tick(1, weaken_active_at_visit=weaken, barrier_active_at_visit=barrier)
            self.assertEqual((result.counter_after, result.nc_flag, result.expired), (1, 0, True))
            self.assertTrue(nocast_blocks_direct_magic(result.counter_after))

    def test_live_single_needs_no_target_adjust_or_randomness(self):
        self.assertEqual(resolve_nocast_multilist(3, alive_slots=(1, 3)).slots, (3,))
        with self.assertRaises(ValueError):
            resolve_nocast_multilist(3, alive_slots=(3,), retarget_draws_0_9=(0,))

    def test_dead_single_rejection_rng_order(self):
        result = resolve_nocast_multilist(3, alive_slots=(1, 4, 11), retarget_draws_0_9=(9, 8, 1))
        self.assertEqual((result.slots, result.retarget_draws_consumed), ((4,), 3))
        with self.assertRaises(ValueError):
            resolve_nocast_multilist(3, alive_slots=(1,), retarget_draws_0_9=(0, 0))

    def test_empty_single_and_target_all_ub_remain_fail_closed(self):
        for selector in (0, 22):
            with self.assertRaises(NocastUndefinedSourceDomain):
                resolve_nocast_multilist(selector, alive_slots=(10,))

    def test_side_and_row_order_and_fallback(self):
        self.assertEqual(resolve_nocast_multilist(20, alive_slots=(8, 3, 12)).slots, (3, 8))
        self.assertEqual(resolve_nocast_multilist(26, alive_slots=(8, 7, 12)).slots, (7, 8))
        self.assertEqual(resolve_nocast_multilist(23, alive_slots=(0,)).slots, ())

    @unittest.skipUnless(shutil.which("cc"), "C compiler unavailable")
    def test_probability_matches_c_float_assignment_boundaries(self):
        # Independent C arithmetic oracle validates rounding/truncation boundaries.
        code = r'''
        #include <stdio.h>
        int main(void) {
          int v,s,l,r,u,off;
          while(scanf("%d%d%d%d%d%d",&v,&s,&l,&r,&u,&off)==6) {
            float sum=s, share=(float)v/sum, penalty;
            penalty=share/0.25; penalty*=10.0;
            if(l>30)l=30; if(l < -30)l=-30;
            int per=off+l-r-penalty-u;
            if(per>80)per=80;
            printf("%d\n",per);
          }
          return 0;
        }'''
        cases = [(v, s, l, r, u, 50)
                 for v, s in ((25, 100), (7, 40), (1, 3), (16777217, 16777219))
                 for l, r, u in ((0, 0, 0), (99, 3, 4), (-99, 50, 1))]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "oracle.c").write_text(code)
            subprocess.run(["cc", "-std=c99", "-O0", str(root / "oracle.c"), "-o", str(root / "oracle")], check=True)
            output = subprocess.check_output([str(root / "oracle")], text=True,
                input="".join(" ".join(map(str, case)) + "\n" for case in cases))
        actual = [nocast_probability_value(inputs(
            defender_vital=v, defender_strength=s-v, defender_toughness=0,
            defender_dexterity=0, attacker_level=100+l, defender_level=100,
            defender_mod_nocast=r, defender_suit_resist=u), off)
            for v, s, l, r, u, off in cases]
        self.assertEqual(actual, list(map(int, output.splitlines())))


if __name__ == "__main__":
    unittest.main()
