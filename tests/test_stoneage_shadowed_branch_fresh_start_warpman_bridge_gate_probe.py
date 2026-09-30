import unittest

from tools.stoneage_shadowed_branch_fresh_start_dialogue_warp_bridge_probe import (
    DialogueWarp,
    WARPMAN,
)
from tools.stoneage_shadowed_branch_fresh_start_warpman_bridge_gate_probe import (
    _classify_edge,
)


class FreshStartWarpManBridgeGateProbeTests(unittest.TestCase):

    def _edge(self,data:bytes)->DialogueWarp:
        return DialogueWarp(
            WARPMAN,1,(1,1,1,1),2,3,4,argument_data=data
        )

    def test_allfree_bridge_is_classified_without_payload_exposure(self):
        row=_classify_edge(
            3,1,self._edge(
                b"WARP:2,3,4|FREE:ALLFREE|CHECKPARTY:FALSE|MONEY:-1"
            )
        )
        self.assertIsNotNone(row)
        self.assertEqual(row.ordinal,3)
        self.assertEqual(row.ordinary_route_class,"UNCONDITIONALLY_FREE")
        self.assertTrue(row.free_allfree)
        self.assertTrue(row.checkparty_explicit_false)
        self.assertEqual(row.money_class,"NEGATIVE_DISABLED")

    def test_condition_shape_is_preserved_as_derived_categories(self):
        row=_classify_edge(
            4,1,self._edge(
                b"WARP:2,3,4|FREE:LV>10&ITEM=20|NomalMsg:x|NEWTIME:1"
            )
        )
        self.assertIsNotNone(row)
        self.assertEqual(row.ordinary_route_class,"CONDITION_DEPENDENT")
        self.assertEqual(row.free_condition_kinds,("ITEM","LEVEL"))
        self.assertTrue(row.normalmsg_present)
        self.assertTrue(row.newtime_present)

    def test_missing_argument_payload_remains_unproven(self):
        edge=DialogueWarp(WARPMAN,1,(1,1,1,1),2,3,4)
        self.assertIsNone(_classify_edge(3,1,edge))


if __name__=="__main__":
    unittest.main()
