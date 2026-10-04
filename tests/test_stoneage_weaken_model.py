"""Source-semantic witnesses, including clock interference and parser defaults."""
from dataclasses import replace
import unittest

from tools.stoneage_weaken_model import (
    WeakenOption, WeakenCheckInputs, parse_weaken_option,
    resolve_weaken_target, weaken_probability_value, resolve_weaken_self_tick,
    resolve_weaken_multilist,
    resolve_weaken_recalculation,
)
from tools.stoneage_nocast_model import resolve_nocast_tick
from tools.stoneage_barrier_model import resolve_barrier_self_tick


def inputs(**kwargs):
    return replace(WeakenCheckInputs(20,20,False,0,100,100,100,100,0,0,False,'player'),**kwargs)


class WeakenModelTests(unittest.TestCase):
    def test_cp950_big5_and_both_utf8_source_spellings(self):
        for encoding in ('cp950','big5','utf-8'):
            self.assertEqual(parse_weaken_option('虛 turn=3 成=50'.encode(encoding),
                             encoding=encoding),WeakenOption(3,50))
        self.assertEqual(parse_weaken_option('虚 turn=5 成=70'.encode(),
            encoding='utf-8',simplified_utf8=True),WeakenOption(5,70))

    def test_loop_increment_and_sizeof_skip_are_bytes(self):
        raw='虛turn=3 成=50'.encode('cp950')
        with self.assertRaises(ValueError):
            parse_weaken_option(raw,encoding='cp950')
        # UTF-8 consumes all three bytes of the initial character, no separator.
        self.assertEqual(parse_weaken_option('虛turn=12 成=50'.encode(),
            encoding='utf-8'),WeakenOption(12,50))
        self.assertEqual(parse_weaken_option('虛 turn345 成=50'.encode('cp950'),
            encoding='cp950'),WeakenOption(45,50))

    def test_failed_turn_sscanf_retains_three(self):
        self.assertEqual(parse_weaken_option('虛 turn=abc 成=55'.encode('cp950'),
                         encoding='cp950'),WeakenOption(3,55))

    def test_success_search_starts_after_turn_marker(self):
        for text in ('虛 成=90 turn=3','虛 turn=3','虛 turn=3 成=abc'):
            self.assertEqual(parse_weaken_option(text.encode('cp950'),encoding='cp950'),
                             WeakenOption(3,0))

    def test_signed_integer_prefix_and_duplicate_turn(self):
        self.assertEqual(parse_weaken_option('虛 turn= +5tail turn=8 成=+70suffix'.encode('cp950'),
            encoding='cp950'),WeakenOption(5,70))

    def test_undefined_and_unverified_parser_domains_fail_closed(self):
        for raw in (b'',b'turn=3',b'\xff',b'\0',
                    '虛 nothing'.encode('cp950'),'虛 turn'.encode('cp950'),
                    '虛 turn=3 成'.encode('cp950'),
                    '虛 turn=2147483647'.encode('cp950'),
                    '虛 turn=3 成=2147483648'.encode('cp950')):
            with self.subTest(raw=raw),self.assertRaises(ValueError):
                parse_weaken_option(raw,encoding='cp950')

    def test_probability_strict_hit_boundary_and_upper_cap(self):
        self.assertEqual(weaken_probability_value(inputs(),50),40)
        for roll,hit in ((39,True),(40,False),(41,False)):
            actual=resolve_weaken_target(inputs(),WeakenOption(3,50),roll_1_100=roll)
            self.assertEqual(actual.hit_check_succeeded,hit)
        self.assertEqual(weaken_probability_value(inputs(attacker_fixed_luck=500),50),80)

    def test_level_clamp_pvp_and_all_resistance_terms(self):
        self.assertEqual(weaken_probability_value(inputs(attacker_level=100),50),70)
        self.assertEqual(weaken_probability_value(inputs(defender_level=100),50),10)
        self.assertEqual(weaken_probability_value(inputs(attacker_level=100,pvp=True),50),40)
        self.assertEqual(weaken_probability_value(inputs(defender_mod_weaken=7,
            defender_suit_resist=8,attacker_fixed_luck=4),50),29)

    def test_existing_status_blocks_before_rng_and_does_not_refresh(self):
        out=resolve_weaken_target(inputs(any_existing_status=True),WeakenOption(3,50),
                                 roll_1_100=None)
        self.assertEqual((out.rng_consumed,out.counter_written),(False,None))
        with self.assertRaises(ValueError):
            resolve_weaken_target(inputs(any_existing_status=True),WeakenOption(3,50),roll_1_100=1)

    def test_pet_and_enemy_targets_allowed_counter_plus_one_false_return(self):
        for kind in ('player','pet','enemy','other'):
            out=resolve_weaken_target(inputs(target_kind=kind),WeakenOption(5,70),roll_1_100=1)
            self.assertEqual((out.counter_written,out.source_return_value),(6,False))

    def test_numeric_undefined_domains(self):
        for inp,success in ((inputs(defender_vital=0,defender_strength=0,
            defender_toughness=0,defender_dexterity=0),50),
            (inputs(attacker_level=2**31-1,defender_level=-2**31),50),
            (inputs(attacker_fixed_luck=2**31-1),50)):
            with self.assertRaises(ValueError):
                weaken_probability_value(inp,success)
        with self.assertRaises(ValueError):
            resolve_weaken_target(inputs(),WeakenOption(2**31-1,50),roll_1_100=1)

    def test_self_freeze_and_counter_one_expiry(self):
        for before,after,expired in ((0,0,False),(1,0,True),(2,2,False),(4,4,False)):
            tick=resolve_weaken_self_tick(before)
            self.assertEqual((tick.counter_after,tick.expired),(after,expired))

    def test_barrier_restores_storage_even_when_local_weaken_expiry_fires(self):
        tick=resolve_weaken_self_tick(1,barrier_active_at_visit=True)
        self.assertEqual((tick.counter_after,tick.expired),(1,True))

    def test_visit_order_changes_nocast_freeze_and_notification(self):
        for weaken in (1,2):
            w=resolve_weaken_self_tick(weaken)
            b=resolve_barrier_self_tick(0,weaken_active_at_visit=w.counter_after>0)
            n=resolve_nocast_tick(2,weaken_active_at_visit=w.counter_after>0,
                                 barrier_active_at_visit=b.counter_after>0)
            self.assertEqual(n.counter_after,1 if weaken==1 else 2)
        # Mutual freeze retains counters but expiry/NC uses decremented locals.
        w=resolve_weaken_self_tick(1,barrier_active_at_visit=True)
        b=resolve_barrier_self_tick(1,weaken_active_at_visit=w.counter_after>0)
        n=resolve_nocast_tick(1,weaken_active_at_visit=w.counter_after>0,
                             barrier_active_at_visit=b.counter_after>0)
        self.assertEqual((w.counter_after,b.counter_after,n.counter_after,n.nc_flag),(1,1,1,0))

    def test_shared_multilist_retargets_before_status_rng(self):
        out=resolve_weaken_multilist(2,alive_slots=(0,3,10),retarget_draws_0_9=(8,1))
        self.assertEqual((out.slots,out.retarget_draws_consumed),((3,),2))
        self.assertEqual(resolve_weaken_multilist(20,alive_slots=(0,3,10)).slots,(0,3))
        with self.assertRaises(ValueError):
            resolve_weaken_multilist(22,alive_slots=(0,10))

    def test_recalculation_reduces_all_three_powers_and_both_counters(self):
        out=resolve_weaken_recalculation(105,201,333,weaken_counter=4,barrier_counter=2)
        self.assertEqual((out.strength,out.toughness,out.dexterity,
                          out.weaken_counter,out.barrier_counter),(84,160,266,3,1))
        self.assertEqual(resolve_weaken_recalculation(105,201,333,weaken_counter=0,
            barrier_counter=1).strength,105)

    def test_recalculation_counter_one_is_reduced_before_reaching_zero(self):
        out=resolve_weaken_recalculation(5,9,11,weaken_counter=1,barrier_counter=0)
        self.assertEqual((out.strength,out.toughness,out.dexterity,out.weaken_counter),(4,7,8,0))
        # A future compliance event receives newly rebuilt baseline powers,
        # rather than multiplying the previous weakened work state again.
        out=resolve_weaken_recalculation(5,9,11,weaken_counter=out.weaken_counter,barrier_counter=0)
        self.assertEqual((out.strength,out.toughness,out.dexterity),(5,9,11))


if __name__=='__main__':
    unittest.main()
