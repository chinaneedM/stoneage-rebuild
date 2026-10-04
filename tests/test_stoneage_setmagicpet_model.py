import unittest

from tools.stoneage_setmagicpet_model import (
    SetMagicPetSourceDomain,
    SetMagicPetTargetState,
    apply_setmagicpet_buff,
    parse_setmagicpet_option,
    recalculate_setmagicpet_fixed_stats,
    resolve_setmagicpet_setup,
    tick_setmagicpet_turns,
)


class SetMagicPetReferenceTests(unittest.TestCase):
    def test_three_field_parser_and_source_priority(self):
        row=parse_setmagicpet_option(b"3|25|STR")
        self.assertEqual((row.turn,row.amount,row.kind),(3,25,"STR"))
        self.assertEqual(parse_setmagicpet_option(b"+4|-20|xxHPSTR").kind,"HP")
        self.assertEqual(parse_setmagicpet_option(b"x| 17tail|TGH").turn,0)
        self.assertEqual(parse_setmagicpet_option(b"x| 17tail|TGH").amount,17)
        self.assertIsNone(parse_setmagicpet_option(b"3|20|UNKNOWN").kind)
        for raw in (None,b"",b"3|20",b"3\0|20|STR"):
            with self.subTest(raw=raw),self.assertRaises(SetMagicPetSourceDomain):
                parse_setmagicpet_option(raw)

    def test_nominal_three_use_limit_does_not_increment(self):
        for count in (0,1,2):
            setup=resolve_setmagicpet_setup(
                target_slot=7,skill_array=601,
                packed_com3_before=0x12340000,use_count=count,
            )
            self.assertTrue(setup.accepted)
            self.assertEqual(setup.use_count_after,count)
            self.assertEqual(setup.packed_com3,0x12340259)
        rejected=resolve_setmagicpet_setup(
            target_slot=7,skill_array=601,packed_com3_before=0,use_count=3,
        )
        self.assertFalse(rejected.accepted)
        self.assertTrue(rejected.rejected_by_nominal_three_use_limit)

    def test_buff_storage_is_mutually_blocked_by_duck_or_magicpet_state(self):
        option=parse_setmagicpet_option(b"3|30|STR")
        states=(
            SetMagicPetTargetState(),
            SetMagicPetTargetState(duck_turn=1),
            SetMagicPetTargetState(tgh_turn=2,tgh_power=10),
        )
        result=apply_setmagicpet_buff(option,states)
        self.assertEqual(result.applied,(True,False,False))
        self.assertEqual(
            (result.targets[0].str_turn,result.targets[0].str_power),
            (3,30),
        )

    def test_unknown_kind_returns_no_storage_mutation_in_bounded_model(self):
        option=parse_setmagicpet_option(b"3|30|???")
        state=SetMagicPetTargetState()
        result=apply_setmagicpet_buff(option,(state,))
        self.assertEqual(result.targets,(state,))
        self.assertEqual(result.applied,(False,))

    def test_hp_branch_is_separate_from_buff_storage(self):
        with self.assertRaises(SetMagicPetSourceDomain):
            apply_setmagicpet_buff(
                parse_setmagicpet_option(b"3|50|HP"),
                (SetMagicPetTargetState(),),
            )

    def test_all_three_stat_buffs_use_pre_suit_toughness_basis(self):
        for kind,field in (("STR","fixed_str"),("TGH","fixed_tough"),("DEX","fixed_dex")):
            state=apply_setmagicpet_buff(
                parse_setmagicpet_option(f"3|25|{kind}".encode()),
                (SetMagicPetTargetState(),),
            ).targets[0]
            out=recalculate_setmagicpet_fixed_stats(
                fixed_str=100,fixed_tough=80,fixed_dex=60,
                pre_suit_tough=80,state=state,
            )
            expected={"fixed_str":100,"fixed_tough":80,"fixed_dex":60}
            expected[field]+=20
            self.assertEqual(
                (out.fixed_str,out.fixed_tough,out.fixed_dex),
                (expected["fixed_str"],expected["fixed_tough"],expected["fixed_dex"]),
            )

    def test_c_integer_truncation_and_overlap_fail_closed(self):
        state=SetMagicPetTargetState(str_turn=1,str_power=-33)
        out=recalculate_setmagicpet_fixed_stats(
            fixed_str=100,fixed_tough=7,fixed_dex=50,
            pre_suit_tough=7,state=state,
        )
        self.assertEqual(out.fixed_str,98)
        with self.assertRaises(SetMagicPetSourceDomain):
            recalculate_setmagicpet_fixed_stats(
                fixed_str=1,fixed_tough=1,fixed_dex=1,pre_suit_tough=1,
                state=SetMagicPetTargetState(str_turn=1,tgh_turn=1),
            )

    def test_turn_tick_leaves_stale_power_inert(self):
        state=SetMagicPetTargetState(str_turn=1,str_power=25)
        after=tick_setmagicpet_turns(state)
        self.assertEqual((after.str_turn,after.str_power),(0,25))
        out=recalculate_setmagicpet_fixed_stats(
            fixed_str=100,fixed_tough=80,fixed_dex=60,
            pre_suit_tough=80,state=after,
        )
        self.assertEqual((out.fixed_str,out.fixed_tough,out.fixed_dex),(100,80,60))


if __name__=="__main__":
    unittest.main()
