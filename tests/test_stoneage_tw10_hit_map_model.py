from pathlib import Path
import struct
import unittest

from tools.stoneage_tw10_hit_map_model import (
    HIT_BLOCKED,
    HIT_OVERRIDE,
    HIT_PASSABLE,
    MAP_SEE_FLAG,
    TaiwanV10CollisionAttr,
    TaiwanV10CollisionProfile,
    build_taiwan_v10_hit_map,
    build_taiwan_v10_hit_map_from_dat,
    load_taiwan_v10_collision_profile,
    parse_stoneage_dat_map_cache,
)


def profile():
    return TaiwanV10CollisionProfile(
        {
            60: TaiwanV10CollisionAttr(60, 600, 1, 1, 1),
            61: TaiwanV10CollisionAttr(61, 601, 1, 1, 0),
            100: TaiwanV10CollisionAttr(100, 1000, 1, 1, 1),
            101: TaiwanV10CollisionAttr(101, 1001, 1, 1, 0),
            102: TaiwanV10CollisionAttr(102, 1002, 1, 1, 2),
            103: TaiwanV10CollisionAttr(103, 1003, 2, 2, 0),
            15680: TaiwanV10CollisionAttr(15680, 9000, 3, 3, 1),
        }
    )


def dat_cache_bytes(*, width, height, tile, parts, event):
    values = tuple(tile) + tuple(parts) + tuple(event)
    return (
        struct.pack("<II", int(width), int(height))
        + struct.pack(f"<{len(values)}H", *values)
    )


class TaiwanV10HitMapTests(unittest.TestCase):
    def test_tile_attr_hit_zero_blocks_and_hit_two_overrides(self):
        p = profile()
        blocked = build_taiwan_v10_hit_map(
            width=1,
            height=1,
            tile=(101,),
            parts=(0,),
            event=(0,),
            profile=p,
        )
        self.assertEqual(blocked.cells, (HIT_BLOCKED,))
        self.assertTrue(blocked.blocked_at(0, 0))

        override = build_taiwan_v10_hit_map(
            width=1,
            height=1,
            tile=(102,),
            parts=(0,),
            event=(0,),
            profile=p,
        )
        self.assertEqual(override.cells, (HIT_OVERRIDE,))
        self.assertFalse(override.blocked_at(0, 0))

    def test_small_tile_codes_match_active_v1_branch(self):
        p = profile()
        unseen_zero = build_taiwan_v10_hit_map(
            width=1, height=1, tile=(0,), parts=(0,), event=(0,), profile=p
        )
        self.assertEqual(unseen_zero.cells, (HIT_PASSABLE,))

        seen_zero = build_taiwan_v10_hit_map(
            width=1,
            height=1,
            tile=(0,),
            parts=(0,),
            event=(MAP_SEE_FLAG,),
            profile=p,
        )
        self.assertEqual(seen_zero.cells, (HIT_BLOCKED,))

        override_four = build_taiwan_v10_hit_map(
            width=1, height=1, tile=(4,), parts=(0,), event=(0,), profile=p
        )
        self.assertEqual(override_four.cells, (HIT_OVERRIDE,))

    def test_zero_parts_code_does_not_block(self):
        hit = build_taiwan_v10_hit_map(
            width=1,
            height=1,
            tile=(100,),
            parts=(0,),
            event=(0,),
            profile=profile(),
        )
        self.assertEqual(hit.cells, (HIT_PASSABLE,))

    def test_parts_hit_zero_projects_atari_footprint_up_and_right(self):
        p = profile()
        result = build_taiwan_v10_hit_map(
            width=3,
            height=3,
            tile=(100,) * 9,
            parts=(0, 0, 0, 0, 0, 0, 0, 103, 0),
            event=(0,) * 9,
            profile=p,
        )
        expected_blocked = {(1, 2), (2, 2), (1, 1), (2, 1)}
        for y in range(3):
            for x in range(3):
                self.assertEqual(
                    result.blocked_at(x, y),
                    (x, y) in expected_blocked,
                )

    def test_override_marker_survives_later_blocking_footprint(self):
        p = profile()
        result = build_taiwan_v10_hit_map(
            width=2,
            height=2,
            tile=(102, 100, 100, 100),
            parts=(0, 0, 103, 0),
            event=(0, 0, 0, 0),
            profile=p,
        )
        self.assertEqual(result.value_at(0, 0), HIT_OVERRIDE)
        self.assertFalse(result.blocked_at(0, 0))

    def test_parts_hit_two_projects_override_footprint(self):
        p = TaiwanV10CollisionProfile(
            {
                100: TaiwanV10CollisionAttr(100, 1000, 1, 1, 1),
                104: TaiwanV10CollisionAttr(104, 1004, 2, 2, 2),
            }
        )
        result = build_taiwan_v10_hit_map(
            width=2,
            height=2,
            tile=(100,) * 4,
            parts=(0, 0, 104, 0),
            event=(0,) * 4,
            profile=p,
        )
        self.assertEqual(result.cells, (HIT_OVERRIDE, HIT_OVERRIDE, HIT_OVERRIDE, HIT_OVERRIDE))

    def test_special_15680_to_15732_hit_one_blocks_origin_only(self):
        p = profile()
        result = build_taiwan_v10_hit_map(
            width=3,
            height=3,
            tile=(100,) * 9,
            parts=(0, 0, 0, 0, 0, 0, 0, 15680, 0),
            event=(0,) * 9,
            profile=p,
        )
        self.assertTrue(result.blocked_at(1, 2))
        self.assertFalse(result.blocked_at(2, 2))
        self.assertFalse(result.blocked_at(1, 1))

    def test_60_to_79_use_adrn_mapping_despite_being_below_invisible_cutoff(self):
        p = profile()
        result = build_taiwan_v10_hit_map(
            width=2,
            height=1,
            tile=(60, 61),
            parts=(0, 0),
            event=(0, 0),
            profile=p,
        )
        self.assertEqual(result.cells, (HIT_PASSABLE, HIT_BLOCKED))

    def test_event_npc_forces_target_cell_blocked(self):
        result = build_taiwan_v10_hit_map(
            width=1,
            height=1,
            tile=(100,),
            parts=(0,),
            event=(1,),
            profile=profile(),
        )
        self.assertEqual(result.cells, (HIT_BLOCKED,))

    def test_unknown_positive_map_number_fails_instead_of_guessing(self):
        with self.assertRaises(KeyError):
            build_taiwan_v10_hit_map(
                width=1,
                height=1,
                tile=(9999,),
                parts=(0,),
                event=(0,),
                profile=profile(),
            )


    def test_strict_dat_cache_parser_exposes_three_planes(self):
        cache = parse_stoneage_dat_map_cache(
            dat_cache_bytes(
                width=2,
                height=1,
                tile=(100, 101),
                parts=(0, 103),
                event=(0, 1),
            )
        )
        self.assertEqual((cache.width, cache.height), (2, 1))
        self.assertEqual(cache.tile, (100, 101))
        self.assertEqual(cache.parts, (0, 103))
        self.assertEqual(cache.event, (0, 1))

    def test_dat_cache_parser_rejects_payload_size_mismatch(self):
        valid = dat_cache_bytes(
            width=1,
            height=1,
            tile=(100,),
            parts=(0,),
            event=(0,),
        )
        with self.assertRaisesRegex(ValueError, "does not match expected"):
            parse_stoneage_dat_map_cache(valid + b"\\x00")

    def test_dat_cache_composes_directly_into_v1_hit_map(self):
        result = build_taiwan_v10_hit_map_from_dat(
            dat_cache_bytes(
                width=2,
                height=1,
                tile=(100, 101),
                parts=(0, 0),
                event=(0, 0),
            ),
            profile=profile(),
        )
        self.assertEqual(result.cells, (HIT_PASSABLE, HIT_BLOCKED))

    def test_committed_derived_collision_profile_loads_without_adrn_payload(self):
        path = (
            Path(__file__).resolve().parents[1]
            / "research"
            / "recovered"
            / "tw10-resource-metadata"
            / "COLLISION-ATTR-R1.tsv.gz"
        )
        loaded = load_taiwan_v10_collision_profile(path)
        self.assertEqual(len(loaded.by_map_number), 9286)
        self.assertTrue(all(key > 0 for key in loaded.by_map_number))


if __name__ == "__main__":
    unittest.main()
