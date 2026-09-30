import unittest

from tools.stoneage_shadowed_branch_fresh_start_dialogue_warp_bridge_probe import (
    FMWARPMAN,
    WARPMAN,
    DialogueWarp,
    _parse_points,
)


class FreshStartDialogueWarpBridgeProbeTests(unittest.TestCase):

    def test_parse_points_keeps_valid_triples(self):
        self.assertEqual(
            _parse_points(b"1,2,3;4,5,6"),
            ((1,2,3),(4,5,6)),
        )

    def test_parse_points_skips_invalid_or_nonpositive_floor(self):
        self.assertEqual(
            _parse_points(b"bad,2,3;0,4,5;7,8,9,extra"),
            ((7,8,9),),
        )

    def test_dialogue_warp_kind_is_restricted(self):
        DialogueWarp(WARPMAN,1,(1,1,1,1),2,3,4)
        DialogueWarp(FMWARPMAN,1,(1,1,1,1),2,3,4)
        with self.assertRaises(ValueError):
            DialogueWarp("Bus",1,(1,1,1,1),2,3,4)


if __name__=="__main__":
    unittest.main()
