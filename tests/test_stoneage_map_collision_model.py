import unittest

from tools.stoneage_map_collision_model import (
    CHARACTER,
    GOLD,
    ITEM,
    CollisionProfile,
    DynamicOccupant,
    ImageCollisionMeta,
    MapCellImages,
    StaticCollisionMap,
    dynamic_overlap_allowed,
    ordinary_step_allowed,
    point_entry_allowed,
    static_point_walkable,
)
from tools.stoneage_singleplayer_domain import MapPosition


def profile():
    return CollisionProfile(
        {
            1: ImageCollisionMeta(1, walkable=1, have_height=False),
            2: ImageCollisionMeta(2, walkable=0, have_height=False),
            3: ImageCollisionMeta(3, walkable=1, have_height=True),
            10: ImageCollisionMeta(10, walkable=0, have_height=False),
            11: ImageCollisionMeta(11, walkable=1, have_height=False),
            12: ImageCollisionMeta(12, walkable=2, have_height=False),
            13: ImageCollisionMeta(13, walkable=1, have_height=True),
            14: ImageCollisionMeta(14, walkable=9, have_height=False),
        }
    )


def collision_map():
    cells = {}
    for y in range(3):
        for x in range(3):
            cells[(x, y)] = MapCellImages(1, 11)
    return StaticCollisionMap(1000, 3, 3, cells)


class MapCollisionModelTests(unittest.TestCase):
    def test_nonflying_object_mode_zero_blocks(self):
        out = static_point_walkable(
            tile=ImageCollisionMeta(1, 1),
            object_part=ImageCollisionMeta(10, 0),
        )
        self.assertFalse(out.allowed)
        self.assertEqual(out.reason, "object_walkable_mode_0")

    def test_nonflying_object_mode_one_defers_to_tile(self):
        self.assertTrue(
            static_point_walkable(
                tile=ImageCollisionMeta(1, 1),
                object_part=ImageCollisionMeta(11, 1),
            ).allowed
        )
        out = static_point_walkable(
            tile=ImageCollisionMeta(2, 0),
            object_part=ImageCollisionMeta(11, 1),
        )
        self.assertFalse(out.allowed)
        self.assertEqual(out.reason, "tile_walkable_not_1")

    def test_nonflying_object_mode_two_forces_walkable(self):
        out = static_point_walkable(
            tile=ImageCollisionMeta(2, 0),
            object_part=ImageCollisionMeta(12, 2),
        )
        self.assertTrue(out.allowed)

    def test_unknown_object_walkable_mode_blocks_instead_of_guessing(self):
        out = static_point_walkable(
            tile=ImageCollisionMeta(1, 1),
            object_part=ImageCollisionMeta(14, 9),
        )
        self.assertFalse(out.allowed)
        self.assertEqual(out.reason, "unknown_object_walkable_mode")

    def test_flying_uses_height_not_walkable(self):
        allowed = static_point_walkable(
            tile=ImageCollisionMeta(2, 0, False),
            object_part=ImageCollisionMeta(10, 0, False),
            is_flying=True,
        )
        self.assertTrue(allowed.allowed)

        blocked = static_point_walkable(
            tile=ImageCollisionMeta(3, 1, True),
            object_part=ImageCollisionMeta(11, 1, False),
            is_flying=True,
        )
        self.assertFalse(blocked.allowed)
        self.assertEqual(blocked.reason, "height_blocks_flying")

    def test_dynamic_character_and_item_overability_are_separate_from_static_map(self):
        self.assertFalse(
            dynamic_overlap_allowed(
                (DynamicOccupant(CHARACTER, overable=False),)
            ).allowed
        )
        self.assertFalse(
            dynamic_overlap_allowed(
                (DynamicOccupant(ITEM, overable=False),)
            ).allowed
        )
        self.assertTrue(
            dynamic_overlap_allowed(
                (
                    DynamicOccupant(CHARACTER, overable=True),
                    DynamicOccupant(ITEM, overable=True),
                    DynamicOccupant(GOLD, overable=False),
                )
            ).allowed
        )

    def test_point_entry_requires_known_image_metadata(self):
        grid = collision_map()
        p = profile()
        self.assertTrue(
            point_entry_allowed(
                grid,
                p,
                MapPosition(1000, 1, 1),
            ).allowed
        )

        unknown = StaticCollisionMap(
            1000,
            1,
            1,
            {(0, 0): MapCellImages(999, 11)},
        )
        with self.assertRaises(KeyError):
            point_entry_allowed(
                unknown,
                p,
                MapPosition(1000, 0, 0),
            )

    def test_diagonal_requires_both_orthogonal_static_side_cells(self):
        base = collision_map()
        cells = dict(base.cells)
        cells[(2, 1)] = MapCellImages(2, 11)
        grid = StaticCollisionMap(1000, 3, 3, cells)

        result = ordinary_step_allowed(
            grid,
            profile(),
            origin=MapPosition(1000, 1, 1),
            destination=MapPosition(1000, 2, 2),
        )
        self.assertFalse(result.allowed)
        self.assertEqual(result.reason, "diagonal_x_side")

    def test_diagonal_side_dynamic_occupants_are_not_checked_by_static_corner_rule(self):
        grid = collision_map()
        result = ordinary_step_allowed(
            grid,
            profile(),
            origin=MapPosition(1000, 1, 1),
            destination=MapPosition(1000, 2, 2),
            destination_occupants=(),
        )
        self.assertTrue(result.allowed)

    def test_target_dynamic_blocker_rejects_after_static_checks(self):
        grid = collision_map()
        result = ordinary_step_allowed(
            grid,
            profile(),
            origin=MapPosition(1000, 1, 1),
            destination=MapPosition(1000, 2, 1),
            destination_occupants=(
                DynamicOccupant(CHARACTER, overable=False),
            ),
        )
        self.assertFalse(result.allowed)
        self.assertEqual(result.reason, "non_overable_character")

    def test_only_one_cell_steps_are_accepted(self):
        grid = collision_map()
        p = profile()
        same = ordinary_step_allowed(
            grid,
            p,
            origin=MapPosition(1000, 1, 1),
            destination=MapPosition(1000, 1, 1),
        )
        self.assertFalse(same.allowed)
        self.assertEqual(same.reason, "zero_length_step")

        long_step = ordinary_step_allowed(
            grid,
            p,
            origin=MapPosition(1000, 0, 0),
            destination=MapPosition(1000, 2, 0),
        )
        self.assertFalse(long_step.allowed)
        self.assertEqual(long_step.reason, "step_exceeds_one_cell")


if __name__ == "__main__":
    unittest.main()
