import unittest

from tools.stoneage_player_creation_model import (
    BASE_STAT_TOTAL,
    DEFAULT_CHARM,
    DEFAULT_FREE_STAT_POINTS,
    DEFAULT_LEVEL,
    DEFAULT_MP,
    ELEMENT_POINT_TOTAL,
    build_creation_state,
    validate_base_stats,
    validate_element_points,
)
from tools.stoneage_player_growth_model import base_derived_stats


class PlayerCreationModelTests(unittest.TestCase):
    def test_allocation_totals(self):
        self.assertEqual(BASE_STAT_TOTAL,20)
        self.assertEqual(ELEMENT_POINT_TOTAL,10)
        self.assertEqual(validate_base_stats(10,5,3,2),(10,5,3,2))
        self.assertEqual(validate_element_points(5,5,0,0),(5,5,0,0))

    def test_reject_bad_base_stat_allocations(self):
        for values in ((10,5,3,1),(20,1,0,0),(-1,10,10,1),(21,0,0,0)):
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    validate_base_stats(*values)

    def test_reject_bad_element_allocations(self):
        for values in (
            (9,0,0,0),
            (11,0,0,-1),
            (5,0,5,0),
            (0,5,0,5),
            (4,3,3,0),
        ):
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    validate_element_points(*values)

    def test_persistent_scales_and_defaults(self):
        state=build_creation_state(10,5,3,2,5,5,0,0)
        self.assertEqual(state["level"],DEFAULT_LEVEL)
        self.assertEqual(state["exp"],0)
        self.assertEqual(state["free_stat_points"],DEFAULT_FREE_STAT_POINTS)
        self.assertEqual(state["charm"],DEFAULT_CHARM)
        self.assertEqual(state["mp"],DEFAULT_MP)
        self.assertEqual(state["max_mp"],DEFAULT_MP)
        self.assertEqual(
            (state["vital"],state["strength"],state["toughness"],state["dexterity"]),
            (1000,500,300,200),
        )
        self.assertEqual(
            (state["earth"],state["water"],state["fire"],state["wind"]),
            (50,50,0,0),
        )

    def test_creation_composes_with_player_growth_model(self):
        state=build_creation_state(10,5,3,2,0,10,0,0)
        derived=base_derived_stats(
            state["vital"],state["strength"],state["toughness"],state["dexterity"]
        )
        self.assertEqual(derived["max_hp"],50)
        self.assertEqual(derived["fix_str"],6)
        self.assertEqual(derived["fix_tough"],4)
        self.assertEqual(derived["quick"],2)


if __name__=="__main__":
    unittest.main()
