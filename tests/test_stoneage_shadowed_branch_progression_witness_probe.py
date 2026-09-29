import unittest
from types import SimpleNamespace

from tools.stoneage_shadowed_branch_progression_witness_probe import (
    _affordable_award_levels,
    _closure_from_ingress,
    _has_nondecreasing_pair,
    _shortest_floor_hops,
    _warp_level_witnesses,
)


def _edge(source,destination):
    return SimpleNamespace(
        source=SimpleNamespace(floor_id=source),
        destination=SimpleNamespace(floor_id=destination),
    )


def _runtime(*pairs):
    return SimpleNamespace(
        topology=SimpleNamespace(
            legacy_warps=tuple(_edge(a,b) for a,b in pairs)
        )
    )


class ShadowedBranchProgressionWitnessTests(unittest.TestCase):

    def test_directed_classic_path_is_not_symmetric(self):
        runtime=_runtime((2020,3000),(3000,811))
        self.assertEqual(_shortest_floor_hops(runtime,2020,811),2)
        self.assertIsNone(_shortest_floor_hops(runtime,811,2020))

    def test_warp_levels_require_target_item_and_joint_lv_window(self):
        levels=_warp_level_witnesses(
            b"LV>10&LV<20&ITEM=55",
            target_item=55,
            maxlevel=140,
        )
        self.assertEqual(levels,tuple(range(11,20)))
        self.assertEqual(
            _warp_level_witnesses(
                b"LV>10&LV<20&ITEM=99",
                target_item=55,
                maxlevel=140,
            ),
            (),
        )

    def test_award_levels_join_lv_gate_and_zero_trans_affordability(self):
        levels=_affordable_award_levels(
            b"TYPE:ACCEPT|EVENT:LV>5|DelStone:LV*100|"
            b"GetItem:55|EventNo:1",
            target_item=55,
            maxlevel=140,
        )
        self.assertEqual(levels[0],6)
        self.assertEqual(levels[-1],140)
        self.assertTrue(levels)

    def test_award_rejects_other_item_prerequisite(self):
        levels=_affordable_award_levels(
            b"TYPE:ACCEPT|EVENT:LV>5&ITEM=77|DelStone:100|"
            b"GetItem:55|EventNo:1",
            target_item=55,
            maxlevel=140,
        )
        self.assertEqual(levels,())

    def test_nondecreasing_progression_pair(self):
        self.assertTrue(_has_nondecreasing_pair((20,21),(21,22)))
        self.assertFalse(_has_nondecreasing_pair((30,31),(10,20)))

    def test_post_ingress_closure_counts_orphans_and_return(self):
        runtime=_runtime(
            (820,821),
            (821,822),
            (822,100),
            (822,9000),
        )
        closure=_closure_from_ingress(
            runtime,
            ingress_floor=820,
            orphan_ids={820,821,822,823},
            preexisting_reached={100,200},
        )
        self.assertEqual(closure.orphan_reached,(820,821,822))
        self.assertEqual(closure.orphan_total,4)
        self.assertTrue(closure.returns_to_preexisting_reached)
        self.assertEqual(closure.max_classic_depth_from_ingress,3)


if __name__=="__main__":
    unittest.main()
