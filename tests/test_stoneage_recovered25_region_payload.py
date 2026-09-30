import unittest
from pathlib import Path

from tools.stoneage_local_runtime_core import load_runtime_bootstrap_file
from tools.stoneage_recovered25_region_payload import (
    EVENT_PLANE_PRESENT,
    EVENT_PLANE_SEPARATE,
    CLIENT_DAT_THREE_PLANE,
    SERVER_LS2MAP_TWO_PLANE,
    EngineNeutralMapRegion,
    _slice_plane,
    build_payload_source_plan,
)
from tools.stoneage_recovered25_world_profile_adapter import (
    Recovered25WorldProfileAdapter,
)

ROOT=Path(__file__).resolve().parents[1]


class Recovered25RegionPayloadTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        profile=load_runtime_bootstrap_file(
            ROOT/"game"/"RUNTIME-BOOTSTRAP-RECOVERED25-R1.json"
        )
        cls.adapter=Recovered25WorldProfileAdapter.from_repository(profile)

    def test_source_plan_covers_exactly_826_materializable_floors(self):
        plan=build_payload_source_plan(self.adapter)
        self.assertEqual(len(plan.stable_dat_floor_ids),761)
        self.assertEqual(len(plan.supplemental_ls2map_floor_ids),65)
        self.assertEqual(len(plan.floor_ids),826)
        self.assertEqual(plan.floor_ids,frozenset(self.adapter.topology.maps))
        self.assertNotIn(130,plan.floor_ids)

    def test_row_major_region_slicing_is_inclusive(self):
        values=tuple(range(20))
        self.assertEqual(
            _slice_plane(values,map_width=5,x1=1,y1=1,x2=3,y2=2),
            (6,7,8,11,12,13),
        )

    def test_client_dat_region_requires_event_plane(self):
        region=EngineNeutralMapRegion(
            floor_id=1,map_width=2,map_height=2,
            x1=0,y1=0,x2=0,y2=0,
            tile_ids=(1,),object_ids=(2,),event_ids=(3,),
            source_kind=CLIENT_DAT_THREE_PLANE,
            event_plane_status=EVENT_PLANE_PRESENT,
            payload_sha256="a"*64,
        )
        self.assertEqual(region.event_ids,(3,))
        with self.assertRaises(ValueError):
            EngineNeutralMapRegion(
                floor_id=1,map_width=2,map_height=2,
                x1=0,y1=0,x2=0,y2=0,
                tile_ids=(1,),object_ids=(2,),event_ids=None,
                source_kind=CLIENT_DAT_THREE_PLANE,
                event_plane_status=EVENT_PLANE_PRESENT,
                payload_sha256="a"*64,
            )

    def test_server_ls2map_region_requires_absent_event_plane(self):
        region=EngineNeutralMapRegion(
            floor_id=1,map_width=2,map_height=2,
            x1=0,y1=0,x2=0,y2=0,
            tile_ids=(1,),object_ids=(2,),event_ids=None,
            source_kind=SERVER_LS2MAP_TWO_PLANE,
            event_plane_status=EVENT_PLANE_SEPARATE,
            payload_sha256="a"*64,
        )
        self.assertIsNone(region.event_ids)
        with self.assertRaises(ValueError):
            EngineNeutralMapRegion(
                floor_id=1,map_width=2,map_height=2,
                x1=0,y1=0,x2=0,y2=0,
                tile_ids=(1,),object_ids=(2,),event_ids=(0,),
                source_kind=SERVER_LS2MAP_TWO_PLANE,
                event_plane_status=EVENT_PLANE_SEPARATE,
                payload_sha256="a"*64,
            )


if __name__=="__main__":
    unittest.main()
