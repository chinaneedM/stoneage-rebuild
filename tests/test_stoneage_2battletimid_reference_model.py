import unittest
from tools.stoneage_2battletimid_reference_model import (
    PROFILE_BIG5,PROFILE_UTF8,resolve_2battletimid_setup,resolve_2battletimid_post_damage,
    parse_2battletimid_chance,
)


class TwoBattleTimidReferenceTests(unittest.TestCase):
    def setup_result(self,raw,profile=PROFILE_BIG5,**extra):
        return resolve_2battletimid_setup(raw,profile=profile,target_slot=5,skill_array=23,
            packed_com3_before=0x12340000,fixed_powers=(101,99,77),powers_before=(900,800,700),**extra)

    def test_dynamic_keep_ratio_plus_order_and_packed_skill(self):
        r=self.setup_result('-攻%70|+攻%20|-防%40|-敏%80'.encode('big5'))
        self.assertEqual(r.powers,(121,39,61))
        self.assertEqual(r.packed_com3,0x12340017)
        self.assertTrue(r.accepted)

    def test_raw_big5_bytes_do_not_match_utf8_literals(self):
        raw='-攻%70|-防%40|-敏%80|命%15'.encode('big5')
        self.assertEqual(self.setup_result(raw,PROFILE_UTF8).powers,(900,800,700))
        self.assertEqual(parse_2battletimid_chance(raw,profile=PROFILE_UTF8),0)

    def test_utf8_literal_match_keeps_historical_fixed_byte_offsets(self):
        raw='-攻%70|-防%40|-敏%80|命%15'.encode('utf-8')
        self.assertEqual(self.setup_result(raw,PROFILE_UTF8).powers,(0,0,0))
        self.assertEqual(parse_2battletimid_chance(raw,profile=PROFILE_UTF8),0)

    def test_failed_float_scan_reuses_already_scaled_fraction(self):
        r=self.setup_result('-攻%70|-防%bad|-敏%bad'.encode('big5'))
        self.assertEqual(r.powers,(70,0,0))

    def test_missing_marker_preserves_existing_work_power_and_invalid_actor(self):
        self.assertEqual(self.setup_result(b'').powers,(900,800,700))
        r=self.setup_result(b'',valid_actor=False)
        self.assertFalse(r.accepted)
        self.assertFalse(r.command_written)
        self.assertFalse(r.skill_written)
        self.assertEqual(r.packed_com3,0x12340000)

    def test_draw_precedes_damage_threshold_and_nonpet_check(self):
        raw='命%15'.encode('big5')
        for damage,pet,draw,request in ((1,True,0,False),(2,False,0,False),(2,True,14,True),(2,True,15,False)):
            r=resolve_2battletimid_post_damage(raw,profile=PROFILE_BIG5,damage=damage,draw=draw,target_is_pet=pet)
            self.assertEqual((r.rng_draws,r.pet_recall_requested),(1,request))
            self.assertFalse(r.player_battle_exit)
            self.assertEqual(r.be_frames,0)

    def test_noreturn_blocks_withdrawal_but_not_owner_notifications(self):
        raw='命%100'.encode('big5')
        for blocked in (False,True):
            r=resolve_2battletimid_post_damage(raw,profile=PROFILE_BIG5,damage=2,draw=0,target_is_pet=True,pet_noreturn=blocked)
            self.assertTrue(r.pet_recall_requested)
            self.assertEqual(r.pet_withdrawn,not blocked)
            self.assertEqual(r.owner_default_pet_after,2 if blocked else -1)
            self.assertEqual((r.owner_slot,r.status_notifications),(0,2))

    def test_demoted_zero_damage_or_reaction_owns_no_effect_draw(self):
        for kwargs in ({'damage':0},{'damage':2,'active_original_reaction':True}):
            r=resolve_2battletimid_post_damage(b'',profile=PROFILE_BIG5,draw=None,target_is_pet=True,**kwargs)
            self.assertEqual(r.rng_draws,0)
            with self.assertRaises(ValueError):
                resolve_2battletimid_post_damage(b'',profile=PROFILE_BIG5,draw=0,target_is_pet=True,**kwargs)


if __name__=='__main__':unittest.main()
