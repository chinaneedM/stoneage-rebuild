import unittest
from tools.stoneage_shadowed_branch_fresh_start_dialogue_warp_bridge_probe import DialogueWarp,WARPMAN
from tools.stoneage_shadowed_branch_fresh_start_warpman_bridge_item_surface_probe import _requirements
class Tests(unittest.TestCase):
    def test_item_gate(self):
        e=DialogueWarp(WARPMAN,1,(1,1,1,1),2,3,4,argument_data=b"WARP:2,3,4|FREE:ITEM=123")
        r=_requirements(3,(e,))
        self.assertEqual((r[0].operator,r[0].item_id),("=",123))
    def test_compound_rejected(self):
        e=DialogueWarp(WARPMAN,1,(1,1,1,1),2,3,4,argument_data=b"WARP:2,3,4|FREE:ITEM=1&LV>1")
        with self.assertRaises(ValueError): _requirements(3,(e,))
if __name__=="__main__": unittest.main()
