import unittest

from tools.stoneage_recovered25_descendant_stable_client_hitmap import (
    HIT_BLOCKED,
    HIT_OVERRIDE,
    HIT_PASSABLE,
    PROFILE_ID,
    DescendantStableCollisionAttr,
    DescendantStableCollisionProfile,
    build_descendant_stable_client_hit_map,
)
from tools.stoneage_tw10_hit_map_model import (
    TaiwanV10CollisionAttr,
    TaiwanV10CollisionProfile,
    build_taiwan_v10_hit_map,
)


def recovered_profile():
    return DescendantStableCollisionProfile(
        {
            60: DescendantStableCollisionAttr(60, 600, 1, 1, 1),
            61: DescendantStableCollisionAttr(61, 601, 1, 1, 0),
            100: DescendantStableCollisionAttr(100, 1000, 1, 1, 1),
            101: DescendantStableCollisionAttr(101, 1001, 1, 1, 0),
            102: DescendantStableCollisionAttr(102, 1002, 1, 1, 2),
            103: DescendantStableCollisionAttr(103, 1003, 2, 2, 0),
            15680: DescendantStableCollisionAttr(15680, 9000, 3, 3, 1),
        },
        source_sha256="0" * 64,
        source_records=7,
        duplicate_map_numbers=0,
    )


def taiwan_profile():
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


class Recovered25DescendantStableClientHitmapTests(unittest.TestCase):

    def test_profile_is_explicitly_reconstruction_not_binary_identity(self):
        profile = recovered_profile()
        self.assertEqual(profile.profile_id, PROFILE_ID)
        self.assertFalse(profile.exact_recovered25_binary_proof)

    def test_core_hit_map_semantics(self):
        result = build_descendant_stable_client_hit_map(
            width=3,
            height=2,
            tile=(100, 101, 102, 60, 61, 100),
            parts=(0, 0, 0, 103, 0, 15680),
            event=(0, 0, 0, 0, 0, 0),
            profile=recovered_profile(),
        )
        self.assertEqual(result.value_at(0, 0), HIT_PASSABLE)
        self.assertEqual(result.value_at(1, 0), HIT_BLOCKED)
        self.assertEqual(result.value_at(2, 0), HIT_OVERRIDE)
        self.assertTrue(result.blocked_at(0, 1))
        self.assertTrue(result.blocked_at(2, 1))

    def test_reconstruction_matches_audited_taiwan_implementation_feature_for_feature(self):
        tile = (100, 101, 102, 60, 61, 4, 0, 100, 100)
        parts = (0, 0, 0, 0, 0, 0, 103, 15680, 0)
        event = (0, 0, 0, 0, 0, 0, 0, 0, 1)
        recovered = build_descendant_stable_client_hit_map(
            width=3,
            height=3,
            tile=tile,
            parts=parts,
            event=event,
            profile=recovered_profile(),
        )
        early = build_taiwan_v10_hit_map(
            width=3,
            height=3,
            tile=tile,
            parts=parts,
            event=event,
            profile=taiwan_profile(),
        )
        self.assertEqual(recovered.cells, early.cells)

    def test_unknown_adrn_id_fails_instead_of_guessing(self):
        with self.assertRaises(KeyError):
            build_descendant_stable_client_hit_map(
                width=1,
                height=1,
                tile=(9999,),
                parts=(0,),
                event=(0,),
                profile=recovered_profile(),
            )


if __name__ == "__main__":
    unittest.main()
