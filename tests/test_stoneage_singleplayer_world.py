import unittest

from tools.stoneage_singleplayer_domain import (
    HistoricalStaticData,
    MapPosition,
    SinglePlayerHistoricalDomain,
)
from tools.stoneage_singleplayer_world import (
    HistoricalMapDefinition,
    HistoricalWorldTopology,
    LegacyWarpEdge,
    place_player_on_topology,
    resolve_player_walk,
)
from tools.stoneage_tw10_25_encounter_bridge import (
    EncounterAreaBridge,
    EnemyVariantBridge,
    GroupBridge,
)


def topology_with_warp():
    return HistoricalWorldTopology(
        maps={
            1000: HistoricalMapDefinition(1000, 20, 20),
            2000: HistoricalMapDefinition(2000, 30, 30),
        },
        legacy_warps=(
            LegacyWarpEdge.from_legacy_arg(
                source=MapPosition(1000, 5, 5),
                arg="2000|10|11|N",
            ),
        ),
    )


def encounter_static():
    enemy = EnemyVariantBridge.from_enemy(
        {
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
        }
    )
    group = GroupBridge.from_group(
        {
            "GROUP_ID": 100,
            "ENEMY_ID1": 700,
            "CREATE_PROB1": 100,
        }
    )
    area = EncounterAreaBridge.from_encount(
        {
            "INDEX": 21,
            "FLOOR": 2000,
            "X1": 0,
            "Y1": 0,
            "X2": 20,
            "Y2": 20,
            "PROB_MIN": 10,
            "PROB_MAX": 20,
            "ENEMY_MAX": 3,
            "ZORDER": 1,
            "GROUP_ID1": 100,
            "GROUP_PROB1": 100,
        }
    )
    return HistoricalStaticData(
        encounter_areas=(area,),
        encounter_groups={100: group},
        enemy_variants={700: enemy},
    )


class SinglePlayerWorldTopologyTests(unittest.TestCase):
    def test_map_bounds_are_explicit_and_player_placement_is_validated(self):
        topology = HistoricalWorldTopology(
            maps={1000: HistoricalMapDefinition(1000, 20, 10)}
        )
        domain = SinglePlayerHistoricalDomain()
        self.assertEqual(
            place_player_on_topology(domain, topology, MapPosition(1000, 19, 9)),
            MapPosition(1000, 19, 9),
        )
        with self.assertRaises(ValueError):
            place_player_on_topology(domain, topology, MapPosition(1000, 20, 9))
        with self.assertRaises(ValueError):
            place_player_on_topology(domain, topology, MapPosition(9999, 1, 1))

    def test_collision_verdict_is_external_and_rejection_does_not_mutate(self):
        topology = HistoricalWorldTopology(
            maps={1000: HistoricalMapDefinition(1000, 20, 20)}
        )
        domain = SinglePlayerHistoricalDomain()
        place_player_on_topology(domain, topology, MapPosition(1000, 4, 5))

        blocked = resolve_player_walk(
            domain,
            topology,
            destination=MapPosition(1000, 5, 5),
            entry_allowed=False,
        )
        self.assertFalse(blocked.moved)
        self.assertEqual(
            blocked.blocked_reason,
            "entry_rejected_by_collision_layer",
        )
        self.assertEqual(domain.world.player_position, MapPosition(1000, 4, 5))

        moved = resolve_player_walk(
            domain,
            topology,
            destination=MapPosition(1000, 5, 5),
            entry_allowed=True,
        )
        self.assertTrue(moved.moved)
        self.assertFalse(moved.warp_triggered)
        self.assertEqual(domain.world.player_position, MapPosition(1000, 5, 5))

    def test_normal_walk_cannot_change_floor_or_leave_recovered_bounds(self):
        topology = topology_with_warp()
        domain = SinglePlayerHistoricalDomain()
        place_player_on_topology(domain, topology, MapPosition(1000, 4, 5))

        cross_floor = resolve_player_walk(
            domain,
            topology,
            destination=MapPosition(2000, 10, 11),
            entry_allowed=True,
        )
        self.assertFalse(cross_floor.moved)
        self.assertEqual(
            cross_floor.blocked_reason,
            "walk_floor_change_requires_warp",
        )

        out_of_bounds = resolve_player_walk(
            domain,
            topology,
            destination=MapPosition(1000, 20, 5),
            entry_allowed=True,
        )
        self.assertFalse(out_of_bounds.moved)
        self.assertEqual(out_of_bounds.blocked_reason, "destination_out_of_bounds")
        self.assertEqual(domain.world.player_position, MapPosition(1000, 4, 5))

    def test_classic_warp_occurs_after_entry_and_suppresses_same_step_encounter(self):
        topology = topology_with_warp()
        domain = SinglePlayerHistoricalDomain(static=encounter_static())
        place_player_on_topology(domain, topology, MapPosition(1000, 4, 5))

        result = resolve_player_walk(
            domain,
            topology,
            destination=MapPosition(1000, 5, 5),
            entry_allowed=True,
        )
        self.assertEqual(result.previous_position, MapPosition(1000, 4, 5))
        self.assertEqual(result.entered_position, MapPosition(1000, 5, 5))
        self.assertEqual(result.final_position, MapPosition(2000, 10, 11))
        self.assertTrue(result.warp_triggered)
        self.assertTrue(result.encounter_suppressed)
        self.assertEqual(domain.world.player_position, MapPosition(2000, 10, 11))

        request = domain.request_encounter(
            group_roll=0,
            enemy_roll=0,
            level_roll=1,
        )
        self.assertIsNotNone(request)
        self.assertEqual(request.position, MapPosition(2000, 10, 11))
        self.assertEqual(request.level, 4)

    def test_map_objmove_failure_preserves_historical_nonrollback_boundary(self):
        topology = topology_with_warp()
        domain = SinglePlayerHistoricalDomain()
        place_player_on_topology(domain, topology, MapPosition(1000, 4, 5))

        result = resolve_player_walk(
            domain,
            topology,
            destination=MapPosition(1000, 5, 5),
            entry_allowed=True,
            map_objmove_ok=False,
        )
        self.assertTrue(result.warp_triggered)
        self.assertFalse(result.map_objmove_ok)
        self.assertEqual(domain.world.player_position, MapPosition(2000, 10, 11))

    def test_time_token_is_retained_but_not_interpreted(self):
        edge = LegacyWarpEdge.from_legacy_arg(
            source=MapPosition(1000, 5, 5),
            arg="2000|10|11|N",
        )
        self.assertEqual(edge.time_token, "N")

    def test_unresolved_conditional_warp_ambiguity_is_not_silently_flattened(self):
        maps = {
            1000: HistoricalMapDefinition(1000, 20, 20),
            2000: HistoricalMapDefinition(2000, 20, 20),
        }
        source = MapPosition(1000, 5, 5)
        with self.assertRaises(ValueError):
            HistoricalWorldTopology(
                maps=maps,
                legacy_warps=(
                    LegacyWarpEdge(source, MapPosition(2000, 1, 1), "D", True),
                    LegacyWarpEdge(source, MapPosition(2000, 2, 2), "N", True),
                ),
            )

    def test_invalid_warp_destination_is_rejected_when_topology_loads(self):
        with self.assertRaises(ValueError):
            HistoricalWorldTopology(
                maps={1000: HistoricalMapDefinition(1000, 20, 20)},
                legacy_warps=(
                    LegacyWarpEdge(
                        MapPosition(1000, 5, 5),
                        MapPosition(2000, 1, 1),
                    ),
                ),
            )


if __name__ == "__main__":
    unittest.main()
