import unittest
import hashlib
from unittest.mock import patch
from tools import stoneage_party_pet_original_player_level_audit as level
from tools import stoneage_party_pet_original_finish_dispatch_audit as finish


class PlayerLevelTests(unittest.TestCase):
    def test_seeds_cross_exactly_the_declared_thresholds(self):
        for profile in ('gavin','bismarck'):
            thresholds=level.THRESHOLDS[profile]
            for seed,levels,residual,_ in level.fixture_cases(profile):
                total=seed+level.PAYOUTS[profile]
                self.assertGreaterEqual(seed,0)
                self.assertEqual(total-sum(thresholds[:levels]),residual)
                self.assertLess(residual,thresholds[min(levels,1)])

    def test_one_exp_changes_exact_boundary_to_one_below(self):
        for profile in ('gavin','bismarck'):
            cases=level.fixture_cases(profile)
            self.assertEqual(cases[0][0]-cases[3][0],1)
            self.assertEqual(cases[0][1:3],(1,0))
            self.assertEqual(cases[3][1],0)

    def test_bismarck_fame_threshold_arithmetic(self):
        self.assertEqual(level.THRESHOLDS['bismarck'],(21345723-20000000,22788045-21345723))
        self.assertEqual(sum(t//20000 for t in level.THRESHOLDS['bismarck']),139)
        self.assertIn('mode==1?67:(mode==2?139:0)',level.level_observations('bismarck'))
        self.assertNotIn('CHAR_FAME',level.level_observations('gavin'))

    def test_preceding_no_upgrade_witness_is_preserved(self):
        for p in ('gavin','bismarck'):
            original=finish.finish_observations(p)
            positive=level.level_observations(p)
            self.assertNotIn('seed_exp',original)
            self.assertIn('whole seven actor terminal oracle',positive)
            self.assertIn('whole arena terminal oracle',positive)
            self.assertNotIn('memcpy(slots,round_baseline',positive)
            self.assertNotIn('Total_BattleNum=final_total',positive)

    def test_drifted_inherited_reward_anchor_fails_closed(self):
        with patch.object(finish,'finish_observations',return_value='changed'):
            with self.assertRaisesRegex(ValueError,'anchor drift'):
                level.level_observations('gavin')

    def test_original_dependency_mutation_or_added_stub_is_rejected(self):
        bodies={'CHAR_earnFame':'unchanged original body'}
        expected={k:hashlib.sha256(v.encode()).hexdigest() for k,v in bodies.items()}
        self.assertEqual(level.validate_bodies(bodies,expected),expected)
        for changed in ({'CHAR_earnFame':'dummy body'},bodies|{'CHAR_HandleExp':'fake'}):
            with self.assertRaisesRegex(ValueError,'dependency drift'):
                level.validate_bodies(changed,expected)


if __name__=='__main__':unittest.main()
