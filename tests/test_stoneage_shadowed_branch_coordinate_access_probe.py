import unittest

from tools.stoneage_shadowed_branch_coordinate_access_probe import (
    InteractionPlacement,
    SelectedStaticMap,
    _distance_to_any,
    _interaction_cells,
)


def _map(width,height,blocked=()):
    blocked=set(blocked)
    return SelectedStaticMap(
        floor_id=1,
        width=width,
        height=height,
        walkable=tuple(
            (x,y) not in blocked
            for y in range(height)
            for x in range(width)
        ),
        copy_status="UNIQUE",
        payload_sha256="0"*64,
    )


class ShadowedBranchCoordinateAccessTests(unittest.TestCase):

    def test_interaction_cells_use_chebyshev_two_and_exclude_npc_cell(self):
        static=_map(7,7)
        cells=_interaction_cells(
            static,
            (InteractionPlacement(1,(3,3,3,3)),),
        )
        self.assertNotIn((3,3),cells)
        self.assertIn((1,1),cells)
        self.assertIn((5,5),cells)
        self.assertNotIn((0,3),cells)

    def test_distance_obeys_diagonal_corner_rule(self):
        static=_map(
            3,3,
            blocked={(1,0)},
        )
        # Direct (0,0)->(1,1) diagonal is blocked by the x-side cell.
        self.assertEqual(
            _distance_to_any(static,{(0,0)},{(1,1)}),
            2,
        )

    def test_unreachable_component_returns_none(self):
        static=_map(
            5,3,
            blocked={(2,0),(2,1),(2,2)},
        )
        self.assertIsNone(
            _distance_to_any(static,{(0,1)},{(4,1)})
        )

    def test_blocked_goal_is_not_accepted(self):
        static=_map(3,3,blocked={(2,2)})
        self.assertIsNone(
            _distance_to_any(static,{(0,0)},{(2,2)})
        )


if __name__=="__main__":
    unittest.main()
