import unittest
from pathlib import Path

from tools.stoneage_singleplayer_world import (
    HistoricalMapDefinition,
    HistoricalWorldTopology,
    LATER_RECOVERED,
    STABLE_LATER_MAP_CANDIDATE,
    V1_RESOURCE_COMPATIBLE,
    WorldMapProvenance,
)
from tools.stoneage_versioned_world_geometry import (
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


_SHA_A = "a" * 64
_SHA_B = "b" * 64


def _provenance(sha):
    return WorldMapProvenance(
        content_role=LATER_RECOVERED,
        resource_role=V1_RESOURCE_COMPATIBLE,
        source_versions=("recovered25", "archived2003"),
        evidence_refs=("lineage",),
        payload_sha256=sha,
        qualifiers=(STABLE_LATER_MAP_CANDIDATE,),
    )


def _world():
    maps = {
        100: HistoricalMapDefinition(
            100, 20, 20, provenance=_provenance(_SHA_A)
        ),
        200: HistoricalMapDefinition(
            200, 10, 10, provenance=_provenance(_SHA_B)
        ),
    }
    topology = HistoricalWorldTopology.from_provenance_maps(maps)
    floors = (
        VersionedWorldFloor(
            floor_id=100,
            path="100.dat",
            width=20,
            height=20,
            map_sha256=_SHA_A,
            semantic=VersionedWorldSemanticCoverage(
                source_version="recovered25",
                server_map_present=True,
                npc_create_count=1,
                warp_functionset_create_count=1,
                encounter_row_count=1,
                active_encounter_row_count=1,
            ),
        ),
        VersionedWorldFloor(
            floor_id=200,
            path="200.dat",
            width=10,
            height=10,
            map_sha256=_SHA_B,
            semantic=VersionedWorldSemanticCoverage(
                source_version="recovered25",
                server_map_present=True,
                npc_create_count=0,
                warp_functionset_create_count=0,
                encounter_row_count=0,
                active_encounter_row_count=0,
            ),
        ),
    )
    return VersionedWorldManifest(
        floors=floors,
        topology=topology,
        semantic_source_version="recovered25",
    )


def _geometry(*, conditional=0, duplicate=False):
    warps = [
        "CLASSIC_WARP|floor=100|placement=0|source=5,5,5,5|"
        f"to=200,2,3|conditional_time={conditional}|destination_stable=1"
    ]
    if duplicate:
        warps.append(
            "CLASSIC_WARP|floor=100|placement=0|source=5,5,5,5|"
            "to=200,4,4|conditional_time=0|destination_stable=1"
        )
    return "\n".join([
        "StoneAge recovered-2.5 stable-map world geometry — R1",
        "SEMANTIC_SOURCE_VERSION|recovered25",
        "EVIDENCE_ROLE|LATER_RECOVERED",
        "COUNT|stable_floor_candidates|2",
        "COUNT|npc_placements|1",
        f"COUNT|classic_warp_edges|{len(warps)}",
        "COUNT|encounter_areas|1",
        "NPC_PLACEMENT|floor=100|placement=0|birth=5,5,5,5|"
        "move=5,5,5,5|dir=0|create_num=1|respawn_time=0|"
        "boundary=1|ignore_invincible=0|resolved_templates=1|classic_warp_refs=1",
        *warps,
        "ENCOUNTER_AREA|index=1|floor=100|rect=1,1,10,10|"
        "prob_min=10|prob_max=20|enemy_max=3|zorder=1|positive_group_refs=1",
        "RESOLUTION|VERSIONED_WORLD_GEOMETRY_CLASSIFIED",
    ])


class VersionedWorldGeometryTests(unittest.TestCase):

    def test_parses_geometry_and_projects_unambiguous_classic_warp(self):
        geometry = parse_versioned_world_geometry(
            world=_world(),
            text=_geometry(),
        )
        self.assertEqual(len(geometry.placements), 1)
        self.assertEqual(len(geometry.classic_warps), 1)
        self.assertEqual(len(geometry.encounters), 1)

        edges = geometry.projectable_legacy_warp_edges()
        self.assertEqual(len(edges), 1)
        self.assertEqual(edges[0].source.floor_id, 100)
        self.assertEqual((edges[0].source.x, edges[0].source.y), (5, 5))
        self.assertEqual(edges[0].destination.floor_id, 200)
        self.assertEqual(
            (edges[0].destination.x, edges[0].destination.y),
            (2, 3),
        )

        topology = geometry.topology_with_projectable_legacy_warps()
        self.assertIsNotNone(topology.active_warp_at(edges[0].source))

    def test_conditional_time_warp_is_not_auto_projected(self):
        geometry = parse_versioned_world_geometry(
            world=_world(),
            text=_geometry(conditional=1),
        )
        self.assertEqual(geometry.projectable_legacy_warp_edges(), ())

    def test_duplicate_source_warps_are_not_auto_projected(self):
        geometry = parse_versioned_world_geometry(
            world=_world(),
            text=_geometry(duplicate=True),
        )
        self.assertEqual(geometry.projectable_legacy_warp_edges(), ())

    def test_geometry_must_match_world_coverage_counts(self):
        drifted = _geometry().replace(
            "COUNT|npc_placements|1",
            "COUNT|npc_placements|0",
        )
        with self.assertRaisesRegex(ValueError, "detail count drift"):
            parse_versioned_world_geometry(
                world=_world(),
                text=drifted,
            )

    def test_real_repository_geometry_closes_full_world_join(self):
        lineage_text = Path(LINEAGE_REPORT_REF).read_text(encoding="utf-8")
        coverage_text = Path(COVERAGE_REPORT_REF).read_text(encoding="utf-8")
        geometry_text = Path(
            "research/recovered/STONEAGE-25-STABLE-WORLD-GEOMETRY-R1.txt"
        ).read_text(encoding="utf-8")

        maps = parse_stable_later_map_manifest(lineage_text)
        world = build_versioned_world_manifest(
            maps=maps,
            coverage_text=coverage_text,
        )
        geometry = parse_versioned_world_geometry(
            world=world,
            text=geometry_text,
        )

        self.assertEqual(len(geometry.world.floors), 761)
        self.assertEqual(len(geometry.placements), 3856)
        self.assertEqual(len(geometry.classic_warps), 2264)
        self.assertEqual(len(geometry.encounters), 402)
        self.assertEqual(
            sum(warp.conditional_time for warp in geometry.classic_warps),
            5,
        )
        self.assertEqual(
            sum(
                warp.destination_is_stable_candidate
                for warp in geometry.classic_warps
            ),
            1909,
        )

        edges = geometry.projectable_legacy_warp_edges()
        self.assertEqual(len(edges), 1784)
        topology = geometry.topology_with_projectable_legacy_warps()
        self.assertEqual(len(topology.maps), 761)
        self.assertEqual(len(topology.legacy_warps), 1784)
        self.assertTrue(topology.require_structured_provenance)

    def test_placement_floor_cannot_escape_world_manifest(self):
        drifted = _geometry().replace(
            "NPC_PLACEMENT|floor=100",
            "NPC_PLACEMENT|floor=999",
        )
        with self.assertRaisesRegex(ValueError, "absent from world"):
            parse_versioned_world_geometry(
                world=_world(),
                text=drifted,
            )


if __name__ == "__main__":
    unittest.main()
