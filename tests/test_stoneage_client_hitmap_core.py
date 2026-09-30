import unittest

from tools.stoneage_client_hitmap_core import (
    ClientCollisionAttr,
    ClientCollisionProfile,
    build_client_hit_map,
)
from tools.stoneage_tw10_hit_map_model import (
    TaiwanV10CollisionAttr,
    TaiwanV10CollisionProfile,
    build_taiwan_v10_hit_map,
)


def _generic_profile():
    return ClientCollisionProfile(
        {
            60: ClientCollisionAttr(60, 600, 1, 1, 1),
            61: ClientCollisionAttr(61, 601, 1, 1, 0),
            100: ClientCollisionAttr(100, 1000, 1, 1, 1),
            101: ClientCollisionAttr(101, 1001, 1, 1, 0),
            102: ClientCollisionAttr(102, 1002, 1, 1, 2),
            103: ClientCollisionAttr(103, 1003, 2, 2, 0),
            15680: ClientCollisionAttr(15680, 9000, 3, 3, 1),
        }
    )


def _tw10_profile():
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


class ClientHitmapCoreTests(unittest.TestCase):

    def test_generic_core_matches_existing_v1_reference_on_semantic_fixture(self):
        width, height = 4, 3
        tile = (
            60, 61, 102, 100,
            100, 101, 100, 100,
            100, 100, 100, 100,
        )
        parts = (
            0, 0, 0, 0,
            0, 103, 0, 0,
            0, 15680, 0, 0,
        )
        event = (
            0, 0, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 0,
        )
        generic = build_client_hit_map(
            width=width,
            height=height,
            tile=tile,
            parts=parts,
            event=event,
            profile=_generic_profile(),
        )
        reference = build_taiwan_v10_hit_map(
            width=width,
            height=height,
            tile=tile,
            parts=parts,
            event=event,
            profile=_tw10_profile(),
        )
        self.assertEqual(generic.cells, reference.cells)

    def test_unknown_adrn_backed_id_fails_closed(self):
        with self.assertRaises(KeyError):
            build_client_hit_map(
                width=1,
                height=1,
                tile=(9999,),
                parts=(0,),
                event=(0,),
                profile=_generic_profile(),
            )


if __name__ == "__main__":
    unittest.main()
