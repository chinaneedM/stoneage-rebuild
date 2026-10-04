import unittest
from tools.stoneage_attack_crazed_model import attack_crazed_callback_setup, parse_attack_crazed_option, resolve_attack_crazed_target_list

class AttackCrazedTests(unittest.TestCase):
    def test_atoi_prefix_and_safe_domain(self):
        for raw,count in [(b'3',3),(b' \t+19suffix',19),(b'01',1),(b'2\xff',2)]:
            self.assertEqual(parse_attack_crazed_option(raw),count)
        for raw in (b'',b'abc',b'0',b'-1',b'20',b'999999999999999',b'3\0'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):parse_attack_crazed_option(raw)

    def test_callback_double_truncation(self):
        r=attack_crazed_callback_setup(actor_kind='enemy',fixed_strength=13,fixed_toughness=19,skill_array=7,submitted_target=9,option=b'3')
        self.assertEqual((r.attack_power,r.defense_power,r.attack_count,r.submitted_target),(10,13,3,9))
        with self.assertRaises(ValueError):attack_crazed_callback_setup(actor_kind='player',fixed_strength=1,fixed_toughness=1,skill_array=0,submitted_target=0,option=b'3')

    def resolve(self,**kw):
        args=dict(actor_slot=10,submitted_target=0,attack_count=3,live_slots=range(20),rand_index=lambda low,high:high,shootchestnut_enabled=True)
        args.update(kw);return resolve_attack_crazed_target_list(**args)

    def test_both_side_last_slots_excluded(self):
        for actor,target,last in [(10,9,8),(0,19,18)]:
            r=self.resolve(actor_slot=actor,submitted_target=target)
            self.assertEqual(r.slots[:4],(last,last,last,-1))
            self.assertEqual(r.selection_draws,3)
            self.assertNotIn(target,r.candidates)

    def test_single_candidate_still_consumes_each_draw(self):
        calls=[]
        r=self.resolve(live_slots=(4,9),rand_index=lambda a,b:(calls.append((a,b)) or 0))
        self.assertEqual(calls,[(0,0)]*3)
        self.assertEqual(r.slots[:4],(4,4,4,-1))

    def test_same_side_profile_difference_precedes_rng(self):
        def forbidden(a,b):raise AssertionError('unexpected RNG')
        r=self.resolve(actor_slot=0,rand_index=forbidden)
        self.assertEqual(r.reason,'same_side_command_none')
        r=self.resolve(actor_slot=0,shootchestnut_enabled=False)
        self.assertEqual(r.reason,'selected')

    def test_no_candidate_keeps_original_twenty_entry_buffer(self):
        r=self.resolve(submitted_target=9,live_slots=(9,))
        self.assertEqual((r.slots,r.selection_draws,r.reason),((9,)*20,0,'no_candidates_initial_buffer'))

    def test_invalid_target_sets_only_index_one_sentinel(self):
        r=self.resolve(submitted_target=20)
        self.assertEqual(r.slots,(20,-1)+(20,)*18)
        self.assertEqual(r.selection_draws,0)

    def test_nineteen_draws_leave_room_for_sentinel(self):
        r=self.resolve(attack_count=19)
        self.assertEqual(len(r.slots),20)
        self.assertEqual(r.slots[-1],-1)

    def test_rng_range_drift_fails(self):
        with self.assertRaises(ValueError):self.resolve(rand_index=lambda a,b:b+1)

if __name__=='__main__':unittest.main()
