import unittest

from tools.stoneage_shadowed_branch_coordinate_access_probe import SelectedStaticMap
from tools.stoneage_shadowed_branch_fresh_start_coordinate_probe import (
    FloorComponents,
)


def _map(width,height,blocked_static=()):
    static_blocked=set(blocked_static)
    return SelectedStaticMap(
        floor_id=1,
        width=width,
        height=height,
        walkable=tuple(
            (x,y) not in static_blocked
            for y in range(height)
            for x in range(width)
        ),
        copy_status="UNIQUE",
        payload_sha256="0"*64,
    )


class FreshStartCoordinateProbeTests(unittest.TestCase):

    def test_component_respects_conservative_dynamic_blockers(self):
        nav=FloorComponents(
            _map(5,3),
            frozenset({(2,0),(2,1),(2,2)}),
        )
        left=nav.component((0,1))
        right=nav.component((4,1))
        self.assertIsNotNone(left)
        self.assertIsNotNone(right)
        self.assertNotEqual(left,right)

    def test_spawn_origin_may_be_admitted_despite_birth_mask(self):
        nav=FloorComponents(
            _map(3,3),
            frozenset({(1,1)}),
            admitted_origins=frozenset({(1,1)}),
        )
        center=nav.component((1,1))
        side=nav.component((2,1))
        self.assertIsNotNone(center)
        self.assertEqual(center,side)

    def test_diagonal_corner_rule_splits_corner_touch(self):
        nav=FloorComponents(
            _map(2,2,blocked_static={(1,0),(0,1)}),
            frozenset(),
        )
        first=nav.component((0,0))
        diagonal=nav.component((1,1))
        self.assertIsNotNone(first)
        self.assertIsNotNone(diagonal)
        self.assertNotEqual(first,diagonal)

    def test_nonadmitted_blocked_point_has_no_component(self):
        nav=FloorComponents(
            _map(3,3),
            frozenset({(1,1)}),
        )
        self.assertIsNone(nav.component((1,1)))


if __name__=="__main__":
    unittest.main()
