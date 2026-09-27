import unittest
from pathlib import Path

from tools.stoneage_singleplayer_domain import SinglePlayerHistoricalDomain
from tools.stoneage_singleplayer_world import (
    HistoricalMapDefinition,
    HistoricalWorldTopology,
    LATER_RECOVERED,
    STABLE_LATER_MAP_CANDIDATE,
    V1_RESOURCE_COMPATIBLE,
    WorldMapProvenance,
)
from tools.stoneage_tw10_25_encounter_bridge import (
    EncounterAreaBridge,
    EnemyVariantBridge,
    GroupBridge,
)
from tools.stoneage_versioned_encounter_runtime import (
    build_versioned_encounter_runtime_adapter,
)
from tools.stoneage_versioned_world_geometry import (
    VersionedEncounterAreaGeometry,
    VersionedWorldGeometryManifest,
)
from tools.stoneage_versioned_world_manifest import (
    VersionedWorldFloor,
    VersionedWorldManifest,
    VersionedWorldSemanticCoverage,
)


_SHA = "a" * 64


def _world_geometry(*, positive_group_refs=1):
    provenance = WorldMapProvenance(
        content_role=LATER_RECOVERED,
        resource_role=V1_RESOURCE_COMPATIBLE,
        source_versions=("recovered25", "archived2003"),
        evidence_refs=("lineage",),
        payload_sha256=_SHA,
        qualifiers=(STABLE_LATER_MAP_CANDIDATE,),
    )
    topology = HistoricalWorldTopology.from_provenance_maps({
        100: HistoricalMapDefinition(
            floor_id=100,
            width=20,
            height=20,
            provenance=provenance,
        ),
    })
    world = VersionedWorldManifest(
        floors=(
            VersionedWorldFloor(
                floor_id=100,
                path="100.dat",
                width=20,
                height=20,
                map_sha256=_SHA,
                semantic=VersionedWorldSemanticCoverage(
                    source_version="recovered25",
                    server_map_present=True,
                    npc_create_count=0,
                    warp_functionset_create_count=0,
                    encounter_row_count=1,
                    active_encounter_row_count=1,
                ),
            ),
        ),
        topology=topology,
        semantic_source_version="recovered25",
    )
    geometry = VersionedEncounterAreaGeometry(
        index=21,
        floor_id=100,
        rect=(0, 0, 19, 19),
        probability_min=10,
        probability_max=20,
        enemy_max_num=3,
        zorder=1,
        positive_group_ref_count=positive_group_refs,
    )
    return VersionedWorldGeometryManifest(
        world=world,
        placements=(),
        classic_warps=(),
        encounters=(geometry,),
    )


def _area(group_id):
    row = {
        "INDEX": 21,
        "FLOOR": 100,
        "X1": 0,
        "Y1": 0,
        "X2": 19,
        "Y2": 19,
        "PROB_MIN": 10,
        "PROB_MAX": 20,
        "ENEMY_MAX": 3,
        "ZORDER": 1,
        "GROUP_ID1": group_id,
        "GROUP_PROB1": 100,
    }
    return EncounterAreaBridge.from_encount(row)


def _group():
    return GroupBridge.from_group({
        "GROUP_ID": 7,
        "ENEMY_ID1": 700,
        "CREATE_PROB1": 100,
    })


def _enemy():
    return EnemyVariantBridge.from_enemy({
        "ID": 700,
        "TEMPNO": 88,
        "LV_MIN": 3,
        "LV_MAX": 5,
        "CREATEMAXNUM": 2,
        "CREATEMINNUM": 1,
        "TACTICS": 1,
        "EXP": -1,
        "DUELPOINT": 0,
        "STYLE": 0,
        "PETFLG": 1,
    })


class VersionedEncounterRuntimeAdapterTests(unittest.TestCase):

    def test_validated_stable_area_runs_through_existing_strict_resolver(self):
        adapter = build_versioned_encounter_runtime_adapter(
            world_geometry=_world_geometry(),
            all_encounter_areas=(_area(7),),
            groups={7: _group()},
            enemies={700: _enemy()},
        )
        self.assertEqual(adapter.specimen_defect_area_indices, ())

        domain = SinglePlayerHistoricalDomain(static=adapter.static_data)
        domain.move_player(floor_id=100, x=5, y=5)

        group_request = domain.request_encounter_group(group_roll=0)
        self.assertIsNotNone(group_request)
        self.assertEqual(group_request.area_index, 21)
        self.assertEqual(group_request.group_id, 7)

        request = domain.request_encounter(
            group_roll=0,
            enemy_roll=0,
            level_roll=1,
        )
        self.assertIsNotNone(request)
        self.assertEqual(request.group_id, 7)
        self.assertEqual(request.enemy_variant_id.value, 700)
        self.assertEqual(request.pet_template_id.value, 88)
        self.assertEqual(request.level, 4)

    def test_positive_missing_group_is_preserved_as_defect_and_hard_fails(self):
        adapter = build_versioned_encounter_runtime_adapter(
            world_geometry=_world_geometry(),
            all_encounter_areas=(_area(999),),
            groups={},
            enemies={},
        )
        self.assertEqual(adapter.specimen_defect_area_indices, (21,))
        self.assertEqual(len(adapter.unresolved_positive_group_refs), 1)
        defect = adapter.unresolved_positive_group_refs[0]
        self.assertEqual(defect.group_id, 999)
        self.assertEqual(defect.weight, 100)

        domain = SinglePlayerHistoricalDomain(static=adapter.static_data)
        domain.move_player(floor_id=100, x=5, y=5)
        with self.assertRaisesRegex(KeyError, "unresolved group 999"):
            domain.request_encounter_group(group_roll=0)

    def test_defect_inventory_is_order_independent_across_source_slots(self):
        area = EncounterAreaBridge.from_encount({
            "INDEX": 21,
            "FLOOR": 100,
            "X1": 0,
            "Y1": 0,
            "X2": 19,
            "Y2": 19,
            "PROB_MIN": 10,
            "PROB_MAX": 20,
            "ENEMY_MAX": 3,
            "ZORDER": 1,
            "GROUP_ID1": 999,
            "GROUP_PROB1": 40,
            "GROUP_ID2": 998,
            "GROUP_PROB2": 60,
        })
        adapter = build_versioned_encounter_runtime_adapter(
            world_geometry=_world_geometry(positive_group_refs=2),
            all_encounter_areas=(area,),
            groups={},
            enemies={},
        )
        self.assertEqual(
            {d.group_id for d in adapter.unresolved_positive_group_refs},
            {998, 999},
        )
        self.assertEqual(adapter.specimen_defect_area_indices, (21,))

    def test_geometry_mismatch_is_rejected_before_runtime(self):
        bad_area = EncounterAreaBridge.from_encount({
            "INDEX": 21,
            "FLOOR": 100,
            "X1": 1,
            "Y1": 0,
            "X2": 19,
            "Y2": 19,
            "PROB_MIN": 10,
            "PROB_MAX": 20,
            "ENEMY_MAX": 3,
            "ZORDER": 1,
            "GROUP_ID1": 7,
            "GROUP_PROB1": 100,
        })
        with self.assertRaisesRegex(ValueError, "geometry/master-data drift"):
            build_versioned_encounter_runtime_adapter(
                world_geometry=_world_geometry(),
                all_encounter_areas=(bad_area,),
                groups={7: _group()},
                enemies={700: _enemy()},
            )

    def test_real_stable_world_encounter_audit_boundary(self):
        path = Path(
            "research/recovered/STONEAGE-25-STABLE-ENCOUNTER-RUNTIME-R1.txt"
        )
        self.assertTrue(path.is_file())
        counts = {}
        defects = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("COUNT|"):
                _prefix, name, value = line.split("|")
                counts[name] = int(value)
            elif line.startswith("SPECIMEN_DEFECT_AREA|"):
                fields = dict(
                    part.split("=", 1)
                    for part in line.split("|")[1:]
                )
                defects.append(fields)

        self.assertEqual(counts["stable_encounter_areas"], 402)
        self.assertEqual(
            counts["stable_unresolved_positive_group_refs"],
            23,
        )
        self.assertEqual(
            counts["stable_affected_encounter_areas"],
            19,
        )
        self.assertEqual(counts["stable_referenced_groups"], 469)
        self.assertEqual(
            counts["stable_referenced_group_missing_enemy_refs"],
            0,
        )
        self.assertEqual(
            counts["stable_referenced_groups_affected_by_missing_enemy"],
            0,
        )
        self.assertEqual(len(defects), 19)
        self.assertEqual(
            sum(int(row["unresolved_positive_group_refs"]) for row in defects),
            23,
        )

    def test_missing_or_extra_stable_area_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "do not match versioned geometry"):
            build_versioned_encounter_runtime_adapter(
                world_geometry=_world_geometry(),
                all_encounter_areas=(),
                groups={7: _group()},
                enemies={700: _enemy()},
            )


if __name__ == "__main__":
    unittest.main()
