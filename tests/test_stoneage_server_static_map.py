import hashlib
import struct
import unittest

from tools.stoneage_server_static_map import (
    parse_ls2map,
    parse_mapset_collision_profile,
    summarize_static_collision,
)


def _ls2map(floor, width, height, tiles, objects):
    header = (
        b"LS2MAP"
        + struct.pack(">H", floor)
        + b"test" + (b"\0" * 28)
        + struct.pack(">HH", width, height)
    )
    return (
        header
        + struct.pack(f">{len(tiles)}H", *tiles)
        + struct.pack(f">{len(objects)}H", *objects)
    )


class ServerStaticMapTests(unittest.TestCase):

    def test_ls2map_decodes_two_static_image_planes(self):
        raw = _ls2map(20002, 2, 2, (1, 2, 3, 4), (5, 6, 7, 8))
        parsed = parse_ls2map(raw)
        self.assertEqual(parsed.floor_id, 20002)
        self.assertEqual((parsed.width, parsed.height), (2, 2))
        self.assertEqual(parsed.tile_ids, (1, 2, 3, 4))
        self.assertEqual(parsed.object_ids, (5, 6, 7, 8))
        self.assertEqual(parsed.payload_sha256, hashlib.sha256(raw).hexdigest())
        collision = parsed.collision_map()
        self.assertEqual(collision.cell_at.__self__.floor_id, 20002)
        self.assertEqual(collision.cells[(1, 1)].tile_image_id, 4)
        self.assertEqual(collision.cells[(1, 1)].object_image_id, 8)

    def test_mapset_uses_source_column_offsets_defaults_and_last_definition(self):
        raw = b"\n".join(
            [
                b"# comment",
                b"1 ignored ignored 1 0",
                b"2 ignored ignored 0 1",
                b"3 ignored ignored",
                b"2 ignored ignored 2 0",
            ]
        )
        profile = parse_mapset_collision_profile(raw)
        self.assertEqual(profile.row_count, 4)
        self.assertEqual(profile.duplicate_image_ids, (2,))
        self.assertEqual(profile.images[1].walkable, 1)
        self.assertFalse(profile.images[1].have_height)
        self.assertEqual(profile.images[2].walkable, 2)
        self.assertFalse(profile.images[2].have_height)
        self.assertEqual(profile.images[3].walkable, 1)
        self.assertFalse(profile.images[3].have_height)

    def test_collision_summary_refuses_to_invent_missing_metadata(self):
        server = parse_ls2map(_ls2map(7, 1, 1, (1,), (9,)))
        mapset = parse_mapset_collision_profile(b"1 x x 1 0\n")
        summary = summarize_static_collision(server, mapset)
        self.assertEqual(summary.missing_image_ids, (9,))
        self.assertIsNone(summary.ordinary_walkable_cells)
        with self.assertRaisesRegex(ValueError, "absent from mapset"):
            mapset.collision_profile_for(server)

    def test_collision_summary_matches_existing_walkable_semantics(self):
        server = parse_ls2map(
            _ls2map(
                8,
                2,
                2,
                (1, 1, 2, 2),
                (10, 11, 12, 13),
            )
        )
        mapset = parse_mapset_collision_profile(
            b"\n".join(
                [
                    b"1 x x 1 0",
                    b"2 x x 0 1",
                    b"10 x x 0 0",
                    b"11 x x 1 0",
                    b"12 x x 2 0",
                    b"13 x x 1 0",
                ]
            )
        )
        summary = summarize_static_collision(server, mapset)
        # obj 10 blocks; obj 11 defers to walkable tile 1; obj 12 forces
        # walkable; obj 13 defers to non-walkable tile 2.
        self.assertEqual(summary.ordinary_walkable_cells, 2)
        # Flying ignores WALKABLE but tile 2 has height, blocking its two cells.
        self.assertEqual(summary.flying_walkable_cells, 2)


if __name__ == "__main__":
    unittest.main()
