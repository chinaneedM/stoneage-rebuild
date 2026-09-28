import unittest
from collections import Counter
from pathlib import Path

from tools.stoneage_singleplayer_world import (
    HistoricalMapDefinition,
    HistoricalWorldTopology,
    LATER_RECOVERED,
    STABLE_LATER_MAP_CANDIDATE,
    V1_RESOURCE_COMPATIBLE,
    WorldMapProvenance,
)
from tools.stoneage_versioned_npc_spawn_catalogue import (
    ISSUE_BIRTH_OUTSIDE_STABLE_MAP,
    ISSUE_GENERATION_DISABLED,
    ISSUE_NON_OCTANT_RAW_DIRECTION,
    VersionedNpcSpawnPlacement,
    build_versioned_npc_spawn_catalogue,
)
from tools.stoneage_versioned_world_geometry import (
    WORLD_GEOMETRY_REPORT_REF,
    VersionedNpcPlacementGeometry,
    VersionedWorldGeometryManifest,
    parse_versioned_world_geometry,
)
from tools.stoneage_versioned_world_manifest import (
    COVERAGE_REPORT_REF,
    VersionedWorldFloor,
    VersionedWorldManifest,
    VersionedWorldSemanticCoverage,
    build_versioned_world_manifest,
)
from tools.stoneage_world_map_library import (
    LINEAGE_REPORT_REF,
    parse_stable_later_map_manifest,
)


_SHA = "a" * 64


def _world_geometry(
    *,
    floor_id=100,
    width=20,
    height=20,
    birth=(5, 5, 5, 5),
    move=(0, 0, 19, 19),
    direction=4,
    create_num=1,
    respawn_time=60000,
):
    provenance = WorldMapProvenance(
        content_role=LATER_RECOVERED,
        resource_role=V1_RESOURCE_COMPATIBLE,
        source_versions=("recovered25", "archived2003"),
        evidence_refs=("lineage",),
        payload_sha256=_SHA,
        qualifiers=(STABLE_LATER_MAP_CANDIDATE,),
    )
    topology = HistoricalWorldTopology.from_provenance_maps({
        floor_id: HistoricalMapDefinition(
            floor_id=floor_id,
            width=width,
            height=height,
            provenance=provenance,
        ),
    })
    world = VersionedWorldManifest(
        floors=(
            VersionedWorldFloor(
                floor_id=floor_id,
                path=f"{floor_id}.dat",
                width=width,
                height=height,
                map_sha256=_SHA,
                semantic=VersionedWorldSemanticCoverage(
                    source_version="recovered25",
                    server_map_present=True,
                    npc_create_count=1,
                    warp_functionset_create_count=0,
                    encounter_row_count=0,
                    active_encounter_row_count=0,
                ),
            ),
        ),
        topology=topology,
        semantic_source_version="recovered25",
    )
    return VersionedWorldGeometryManifest(
        world=world,
        placements=(
            VersionedNpcPlacementGeometry(
                floor_id=floor_id,
                placement_id=0,
                birth_rect=birth,
                move_rect=move,
                direction=direction,
                create_num=create_num,
                respawn_time=respawn_time,
                boundary=1,
                ignore_invincible=0,
                resolved_template_refs=1,
                classic_warp_refs=0,
            ),
        ),
        classic_warps=(),
        encounters=(),
    )


def _real_world_geometry():
    maps = parse_stable_later_map_manifest(
        Path(LINEAGE_REPORT_REF).read_text(encoding="utf-8")
    )
    world = build_versioned_world_manifest(
        maps=maps,
        coverage_text=Path(COVERAGE_REPORT_REF).read_text(encoding="utf-8"),
    )
    return parse_versioned_world_geometry(
        world=world,
        text=Path(WORLD_GEOMETRY_REPORT_REF).read_text(encoding="utf-8"),
    )


class VersionedNpcSpawnCatalogueTests(unittest.TestCase):

    def test_catalogue_preserves_create_layer_and_excludes_template_behavior(self):
        catalogue = build_versioned_npc_spawn_catalogue(_world_geometry())
        self.assertEqual(len(catalogue.placements), 1)
        placement = catalogue.placements[0]

        self.assertEqual(placement.floor_id, 100)
        self.assertEqual(placement.placement_id, 0)
        self.assertEqual(placement.birth_rect, (5, 5, 5, 5))
        self.assertEqual(placement.move_rect, (0, 0, 19, 19))
        self.assertEqual(placement.population_cap, 1)
        self.assertEqual(placement.raw_direction, 4)
        self.assertEqual(placement.normalized_direction, 4)
        self.assertEqual(placement.respawn_delay_ms, 60000)
        self.assertTrue(placement.boundary_enabled)
        self.assertFalse(placement.ignore_invincible_area)
        self.assertTrue(placement.direct_projection_eligible(catalogue.world_geometry))

        fields = set(VersionedNpcSpawnPlacement.__dataclass_fields__)
        self.assertNotIn("template_id", fields)
        self.assertNotIn("template_name", fields)
        self.assertNotIn("dialogue", fields)
        self.assertNotIn("functionset", fields)
        self.assertNotIn("argument", fields)

    def test_descendant_direction_projection_preserves_raw_anomaly(self):
        catalogue = build_versioned_npc_spawn_catalogue(
            _world_geometry(direction=46)
        )
        placement = catalogue.placements[0]
        self.assertEqual(placement.raw_direction, 46)
        self.assertEqual(placement.normalized_direction, 6)
        self.assertEqual(
            placement.direct_projection_issues(catalogue.world_geometry),
            (ISSUE_NON_OCTANT_RAW_DIRECTION,),
        )

    def test_out_of_bounds_move_rect_is_metadata_not_spawn_blocker(self):
        catalogue = build_versioned_npc_spawn_catalogue(
            _world_geometry(move=(-30, -30, 70, 70))
        )
        placement = catalogue.placements[0]
        self.assertFalse(
            placement.move_rect_fully_in_bounds(catalogue.world_geometry)
        )
        self.assertTrue(
            placement.direct_projection_eligible(catalogue.world_geometry)
        )

    def test_out_of_bounds_birth_is_quarantined(self):
        catalogue = build_versioned_npc_spawn_catalogue(
            _world_geometry(birth=(5, 25, 5, 25))
        )
        placement = catalogue.placements[0]
        self.assertEqual(
            placement.direct_projection_issues(catalogue.world_geometry),
            (ISSUE_BIRTH_OUTSIDE_STABLE_MAP,),
        )
        self.assertEqual(catalogue.direct_projection_eligible, ())
        self.assertEqual(catalogue.quarantined, (placement,))

    def test_nonpositive_cap_or_negative_respawn_disables_generation(self):
        for create_num, respawn_time in ((0, 0), (1, -1)):
            with self.subTest(
                create_num=create_num,
                respawn_time=respawn_time,
            ):
                catalogue = build_versioned_npc_spawn_catalogue(
                    _world_geometry(
                        create_num=create_num,
                        respawn_time=respawn_time,
                    )
                )
                placement = catalogue.placements[0]
                self.assertIn(
                    ISSUE_GENERATION_DISABLED,
                    placement.direct_projection_issues(
                        catalogue.world_geometry
                    ),
                )

    def test_real_repository_spawn_catalogue_closure(self):
        geometry = _real_world_geometry()
        catalogue = build_versioned_npc_spawn_catalogue(geometry)

        self.assertEqual(len(catalogue.placements), 3856)
        self.assertEqual(len(catalogue.by_floor), 553)
        self.assertEqual(len(catalogue.direct_projection_eligible), 3852)
        self.assertEqual(len(catalogue.quarantined), 4)
        self.assertEqual(
            dict(catalogue.issue_counts()),
            {
                ISSUE_BIRTH_OUTSIDE_STABLE_MAP: 2,
                ISSUE_NON_OCTANT_RAW_DIRECTION: 2,
            },
        )

        self.assertTrue(
            all(row.population_cap == 1 for row in catalogue.placements)
        )
        self.assertTrue(
            all(row.boundary_enabled for row in catalogue.placements)
        )
        self.assertTrue(
            all(row.birth_is_single_cell for row in catalogue.placements)
        )
        self.assertEqual(
            Counter(row.respawn_delay_ms for row in catalogue.placements),
            Counter({0: 3199, 60000: 642, 200000: 15}),
        )
        self.assertEqual(
            Counter(
                row.ignore_invincible_area
                for row in catalogue.placements
            ),
            Counter({True: 3040, False: 816}),
        )
        self.assertEqual(
            sum(
                row.move_rect_fully_in_bounds(geometry)
                for row in catalogue.placements
            ),
            3772,
        )

        quarantined = {
            row.placement_id: row.direct_projection_issues(geometry)
            for row in catalogue.quarantined
        }
        self.assertEqual(
            quarantined,
            {
                1007: (ISSUE_BIRTH_OUTSIDE_STABLE_MAP,),
                2566: (ISSUE_NON_OCTANT_RAW_DIRECTION,),
                3634: (ISSUE_BIRTH_OUTSIDE_STABLE_MAP,),
                3771: (ISSUE_NON_OCTANT_RAW_DIRECTION,),
            },
        )


if __name__ == "__main__":
    unittest.main()
