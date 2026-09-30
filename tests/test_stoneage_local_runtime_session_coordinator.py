import json
from dataclasses import replace
import tempfile
import unittest
from pathlib import Path
from types import MappingProxyType, SimpleNamespace

from tools.stoneage_enemy_spawn_model import (
    EnemyBirthRolls,
    materialize_spawn_plan,
    plan_enemy_spawns,
)
from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_CAPTURE,
    BATTLE_COM_ESCAPE,
    BATTLE_COM_WAIT,
    BattleCombatProfile,
    BattleCommand,
    OrdinaryAttackRolls,
    OrdinaryCaptureContext,
    OrdinaryCaptureRolls,
    OrdinaryEscapeContext,
    OrdinaryEscapeRolls,
)
from tools.stoneage_encounter_frequency_model import (
    EncounterFrequencyState,
)
from tools.stoneage_map_collision_model import (
    CHARACTER,
    GOLD,
    CollisionDecision,
    DynamicOccupant,
)
from tools.stoneage_local_filesystem_persistence import (
    LocalFilesystemPersistenceStore,
)
from tools.stoneage_local_runtime_core import (
    FreshStartSeed,
    LocalRuntimeSessionState,
    MaterializedWorldRegion,
    ResolvedTransitionBinding,
    TransitionGateDecision,
    WorldRegionRequest,
    encode_local_runtime_session,
    load_runtime_bootstrap_file,
)
from tools.stoneage_local_runtime_session_coordinator import (
    InMemoryLocalPersistenceStore,
    LocalRuntimeSessionCoordinator,
)
from tools.stoneage_singleplayer_battle import BattleOutcome
from tools.stoneage_pet_growth_model import (
    PetLevelGrowthRolls,
    pack_growth_base,
)
from tools.stoneage_singleplayer_domain import (
    EncounterRolls,
    EnemyVariantId,
    HistoricalStaticData,
    MapPosition,
    PetActor,
    PetGrowthState,
    PetSlot,
    PetTemplateId,
    PersistentPlayerState,
    PlayerState,
    SinglePlayerHistoricalDomain,
)
from tools.stoneage_singleplayer_world import (
    HistoricalMapDefinition,
    HistoricalWorldTopology,
    LegacyWarpEdge,
)
from tools.stoneage_tw10_25_bridge_model import PetTemplateBridge
from tools.stoneage_tw10_25_encounter_bridge import (
    EncounterAreaBridge,
    EnemyVariantBridge,
    GroupBridge,
)


ROOT = Path(__file__).resolve().parents[1]


def _player_state() -> PersistentPlayerState:
    return PersistentPlayerState(
        character=PlayerState(
            MappingProxyType({"name": "coordinator-test", "level": 1})
        )
    )


def _battle_player_state() -> PersistentPlayerState:
    return PersistentPlayerState(
        character=PlayerState(
            MappingProxyType(
                {
                    "name": "battle-player",
                    "level": 5,
                    "hp": 100,
                    "max_hp": 100,
                    "attack": 80,
                    "defense": 60,
                    "quick": 50,
                    "exp": 0,
                    "max_exp": 1000,
                    "charm": 5,
                    "gold": 101,
                    "mp": 40,
                    "max_mp": 50,
                }
            )
        )
    )


class _FakeStack:
    def __init__(self, profile):
        self.profile = profile
        self.allow = True
        self.evaluation_calls = 0
        topology = HistoricalWorldTopology(
            maps={
                1: HistoricalMapDefinition(1, 3, 3),
                2: HistoricalMapDefinition(2, 3, 3),
            },
            legacy_warps=(
                LegacyWarpEdge(
                    source=MapPosition(1, 1, 0),
                    destination=MapPosition(2, 2, 2),
                ),
            ),
        )
        self.world_adapter = SimpleNamespace(topology=topology)
        self.bindings = {
            transition_id: ResolvedTransitionBinding(
                transition_id=transition_id,
                source=MapPosition(2, 1, 1),
                destination=MapPosition(1, 2, 2),
                predicate_payload={
                    "interaction_kind": "DIALOGUE_WARPMAN",
                    "source_rect": (1, 1, 2, 2),
                    "gate_kind": "TEST",
                },
                provenance={"source_profile": "recovered25"},
            )
            for transition_id in profile.transitions
        }
        area = EncounterAreaBridge.from_encount({
            "INDEX": 21,
            "FLOOR": 1,
            "X1": 0,
            "Y1": 0,
            "X2": 2,
            "Y2": 2,
            "PROB_MIN": 10,
            "PROB_MAX": 20,
            "ENEMY_MAX": 2,
            "ZORDER": 1,
            "GROUP_ID1": 7,
            "GROUP_PROB1": 100,
        })
        group = GroupBridge.from_group({
            "GROUP_ID": 7,
            "ENEMY_ID1": 700,
            "CREATE_PROB1": 100,
        })
        enemy = EnemyVariantBridge.from_enemy({
            "ID": 700,
            "TEMPNO": 88,
            "LV_MIN": 3,
            "LV_MAX": 5,
            "CREATEMAXNUM": 2,
            "CREATEMINNUM": 1,
            "TACTICS": 1,
            "EXP": 100,
            "DUELPOINT": 0,
            "STYLE": 0,
            "PETFLG": 1,
        })
        self.encounter_runtime = SimpleNamespace(
            encounter_areas=(area,),
            groups={7: group},
            enemies={700: enemy},
            static_data=HistoricalStaticData(
                encounter_areas=(area,),
                encounter_groups={7: group},
                enemy_variants={700: enemy},
            ),
        )
        template = PetTemplateBridge.from_enemybase(
            {
                "NAME": None,
                "TEMPNO": 88,
                "INITNUM": 10,
                "LVUPPOINT": 5,
                "BASEVITAL": 20,
                "BASESTR": 20,
                "BASETGH": 20,
                "BASEDEX": 20,
                "IMGNUMBER": 10123,
                "MODAI": 4,
                "GET": 0,
                "EARTHAT": 50,
                "WATERAT": 50,
                "FIREAT": 0,
                "WINDAT": 0,
                "SLOT": 4,
                "SIZE": 0,
            }
        )
        self.enemybase_runtime = SimpleNamespace(templates={88: template})

    def create_fresh_start(self, ordinal):
        return FreshStartSeed(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=int(ordinal),
            position=MapPosition(1, 0, 0),
            player_state=_player_state(),
        )

    def materialize_player_position(self, session):
        p = session.player_position
        request = WorldRegionRequest(
            floor_id=p.floor_id,
            x1=p.x,
            y1=p.y,
            x2=p.x,
            y2=p.y,
            world_profile=session.world_profile,
        )
        return MaterializedWorldRegion(
            request=request,
            payload={"cell": (p.floor_id, p.x, p.y)},
            provenance={"world_profile": session.world_profile},
        )

    def resolve_transition(self, transition_id):
        return self.bindings[str(transition_id)]

    def evaluate_transition(self, transition_id, session):
        self.evaluation_calls += 1
        return TransitionGateDecision(
            allowed=self.allow,
            reason=("test gate allowed" if self.allow else "test gate denied"),
            consumed_state={},
        )

    def _encounter_domain(self, session):
        domain = SinglePlayerHistoricalDomain(
            static=self.encounter_runtime.static_data,
            persistent=session.player_state,
        )
        domain.move_player(
            floor_id=session.player_position.floor_id,
            x=session.player_position.x,
            y=session.player_position.y,
        )
        return domain

    def request_encounter_group(self, session, *, group_roll):
        return self._encounter_domain(session).request_encounter_group(
            group_roll=group_roll,
        )

    def request_encounter(
        self,
        session,
        *,
        group_roll,
        enemy_roll,
        level_roll,
    ):
        return self._encounter_domain(session).request_encounter(
            group_roll=group_roll,
            enemy_roll=enemy_roll,
            level_roll=level_roll,
        )


    def spawn_group_enemies(
        self,
        encounter,
        *,
        entry_count_roll,
        selection_rolls,
        birth_rolls,
    ):
        area = next(
            row
            for row in self.encounter_runtime.encounter_areas
            if row.index == encounter.area_index
        )
        group = self.encounter_runtime.groups[encounter.group_id]
        plan = plan_enemy_spawns(
            area,
            group,
            self.encounter_runtime.enemies,
            self.enemybase_runtime.templates,
            entry_count_roll=entry_count_roll,
            selection_rolls=selection_rolls,
        )
        return materialize_spawn_plan(
            plan,
            self.enemybase_runtime.templates,
            birth_rolls=birth_rolls,
        )


class LocalRuntimeSessionCoordinatorTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.profile = load_runtime_bootstrap_file(
            ROOT / "game" / "RUNTIME-BOOTSTRAP-RECOVERED25-R1.json"
        )

    def setUp(self):
        self.stack = _FakeStack(self.profile)
        self.store = InMemoryLocalPersistenceStore()
        self.coordinator = LocalRuntimeSessionCoordinator(
            stack=self.stack,
            persistence=self.store,
        )

    def test_new_game_and_current_region_share_one_authoritative_session(self):
        session = self.coordinator.new_game(1)
        self.assertEqual(session.player_position, MapPosition(1, 0, 0))
        region = self.coordinator.materialize_current_region(session)
        self.assertEqual(region.payload["cell"], (1, 0, 0))

    def test_save_and_continue_round_trip_through_store_port(self):
        session = self.coordinator.new_game(2)
        session = LocalRuntimeSessionState(
            contract_id=session.contract_id,
            world_profile=session.world_profile,
            hometown_ordinal=session.hometown_ordinal,
            player_position=session.player_position,
            player_state=session.player_state,
            world_flags=frozenset({"opened-test-route"}),
        )
        self.coordinator.save_game("slot-1", session)
        restored = self.coordinator.continue_game("slot-1")
        self.assertEqual(restored.player_position, session.player_position)
        self.assertEqual(restored.world_flags, session.world_flags)
        self.assertIn("slot-1", self.store.rows)
        with self.assertRaises(KeyError):
            self.coordinator.continue_game("missing")

    def test_save_continue_persists_live_occupancy_delta_and_new_game_resets(self):
        initial = SimpleNamespace(
            profile_id="TEST_INITIAL_OCCUPANCY_R1",
            populate_registry=lambda registry: registry.register_character(
                object_id="npc-placement:42",
                position=MapPosition(1, 0, 1),
                overable=True,
                provenance="test:initial-npc",
            ),
        )
        self.stack.npc_initial_occupancy = initial
        coordinator = LocalRuntimeSessionCoordinator(
            stack=self.stack,
            persistence=self.store,
        )
        session = coordinator.new_game(1)
        coordinator.occupancy_registry.move(
            "npc-placement:42",
            MapPosition(1, 1, 1),
        )
        coordinator.occupancy_registry.set_overable(
            "npc-placement:42",
            False,
        )
        coordinator.occupancy_registry.register_item(
            object_id="item:drop:9",
            position=MapPosition(1, 2, 1),
            overable=False,
            provenance="test:dropped-item",
        )

        coordinator.save_game("slot-occupancy", session)
        payload = json.loads(self.store.rows["slot-occupancy"])
        self.assertEqual(payload["schema"], "stoneage.local-runtime-save.r1")
        self.assertEqual(
            payload["occupancy"]["base_profile_id"],
            "TEST_INITIAL_OCCUPANCY_R1",
        )
        self.assertEqual(len(payload["occupancy"]["upserts"]), 2)

        coordinator.new_game(1)
        self.assertEqual(
            set(coordinator.occupancy_registry.objects),
            {"npc-placement:42"},
        )
        self.assertEqual(
            coordinator.occupancy_registry.objects["npc-placement:42"].position,
            MapPosition(1, 0, 1),
        )
        self.assertTrue(
            coordinator.occupancy_registry.objects["npc-placement:42"].overable
        )

        restored = coordinator.continue_game("slot-occupancy")
        self.assertEqual(restored.player_position, session.player_position)
        self.assertEqual(
            coordinator.occupancy_registry.objects["npc-placement:42"].position,
            MapPosition(1, 1, 1),
        )
        self.assertFalse(
            coordinator.occupancy_registry.objects["npc-placement:42"].overable
        )
        self.assertIn("item:drop:9", coordinator.occupancy_registry.objects)
        self.assertFalse(
            coordinator.occupancy_registry.objects["item:drop:9"].overable
        )

    def test_filesystem_store_survives_coordinator_reconstruction(self):
        initial = SimpleNamespace(
            profile_id="TEST_INITIAL_OCCUPANCY_R1",
            populate_registry=lambda registry: registry.register_character(
                object_id="npc-placement:42",
                position=MapPosition(1, 0, 1),
                overable=True,
                provenance="test:initial-npc",
            ),
        )
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "saves"
            stack_a = _FakeStack(self.profile)
            stack_a.npc_initial_occupancy = initial
            first = LocalRuntimeSessionCoordinator(
                stack=stack_a,
                persistence=LocalFilesystemPersistenceStore(root),
            )
            session = first.new_game(1)
            session = LocalRuntimeSessionState(
                contract_id=session.contract_id,
                world_profile=session.world_profile,
                hometown_ordinal=session.hometown_ordinal,
                player_position=session.player_position,
                player_state=session.player_state,
                world_flags=frozenset({"restart-proof"}),
            )
            first.occupancy_registry.move(
                "npc-placement:42",
                MapPosition(1, 1, 1),
            )
            first.occupancy_registry.register_item(
                object_id="item:drop:restart",
                position=MapPosition(1, 2, 1),
                overable=False,
                provenance="test:restart-drop",
            )
            first.save_game("restart-slot", session)

            stack_b = _FakeStack(self.profile)
            stack_b.npc_initial_occupancy = initial
            second = LocalRuntimeSessionCoordinator(
                stack=stack_b,
                persistence=LocalFilesystemPersistenceStore(root),
            )
            restored = second.continue_game("restart-slot")

            self.assertEqual(restored.world_flags, frozenset({"restart-proof"}))
            self.assertEqual(
                second.occupancy_registry.objects["npc-placement:42"].position,
                MapPosition(1, 1, 1),
            )
            self.assertIn(
                "item:drop:restart",
                second.occupancy_registry.objects,
            )
            self.assertFalse(
                second.occupancy_registry.objects[
                    "item:drop:restart"
                ].overable
            )

    def test_legacy_session_save_rehydrates_initial_occupancy_without_delta(self):
        initial = SimpleNamespace(
            profile_id="TEST_INITIAL_OCCUPANCY_R1",
            populate_registry=lambda registry: registry.register_character(
                object_id="npc-placement:42",
                position=MapPosition(1, 0, 1),
                overable=True,
                provenance="test:initial-npc",
            ),
        )
        self.stack.npc_initial_occupancy = initial
        coordinator = LocalRuntimeSessionCoordinator(
            stack=self.stack,
            persistence=self.store,
        )
        session = coordinator.new_game(1)
        coordinator.occupancy_registry.move(
            "npc-placement:42",
            MapPosition(1, 1, 1),
        )
        coordinator.occupancy_registry.register_item(
            object_id="item:transient",
            position=MapPosition(1, 2, 1),
            overable=False,
            provenance="test:transient",
        )
        self.store.save("legacy", encode_local_runtime_session(session))

        restored = coordinator.continue_game("legacy")
        self.assertEqual(restored.player_position, session.player_position)
        self.assertEqual(
            set(coordinator.occupancy_registry.objects),
            {"npc-placement:42"},
        )
        self.assertEqual(
            coordinator.occupancy_registry.objects["npc-placement:42"].position,
            MapPosition(1, 0, 1),
        )
        self.assertTrue(
            coordinator.occupancy_registry.objects["npc-placement:42"].overable
        )

    def test_explicit_collision_verdict_controls_one_cell_walk(self):
        session = self.coordinator.new_game(1)
        blocked = self.coordinator.walk_one_cell(
            session,
            destination=MapPosition(1, 0, 1),
            entry_allowed=False,
        )
        self.assertFalse(blocked.resolution.moved)
        self.assertEqual(blocked.session.player_position, MapPosition(1, 0, 0))

        moved = self.coordinator.walk_one_cell(
            session,
            destination=MapPosition(1, 0, 1),
            entry_allowed=True,
        )
        self.assertTrue(moved.resolution.moved)
        self.assertEqual(moved.session.player_position, MapPosition(1, 0, 1))

        with self.assertRaises(ValueError):
            self.coordinator.walk_one_cell(
                session,
                destination=MapPosition(1, 2, 2),
                entry_allowed=True,
            )
        with self.assertRaises(ValueError):
            self.coordinator.walk_one_cell(
                session,
                destination=MapPosition(2, 0, 0),
                entry_allowed=True,
            )

    def test_server_collision_provider_can_drive_one_cell_walk(self):
        session = self.coordinator.new_game(1)
        self.stack.collision_provider = SimpleNamespace(
            ordinary_step_verdict=lambda **_kwargs: CollisionDecision(
                True,
                "server_static_allowed",
            )
        )
        result = self.coordinator.walk_one_cell_with_server_collision(
            session,
            destination=MapPosition(1, 0, 1),
        )
        self.assertTrue(result.resolution.moved)
        self.assertIsNotNone(result.collision)
        self.assertTrue(result.collision.allowed)
        self.assertEqual(result.session.player_position, MapPosition(1, 0, 1))

        self.stack.collision_provider = None
        with self.assertRaisesRegex(ValueError, "no server collision provider"):
            self.coordinator.walk_one_cell_with_server_collision(
                session,
                destination=MapPosition(1, 0, 1),
            )

    def test_unified_collision_router_preserves_evidence_on_walk_result(self):
        session = self.coordinator.new_game(1)
        self.stack.collision_router = SimpleNamespace(
            routed_step_verdict=lambda **_kwargs: SimpleNamespace(
                decision=CollisionDecision(True, "client_hitmap_allowed"),
                route=SimpleNamespace(
                    provider_kind="RECOVERED25_CLIENT_HITMAP_RECONSTRUCTION",
                    evidence_class=(
                        "LATER_RECOVERED_PLUS_PINNED_DESCENDANT_STABLE_ALGORITHM"
                    ),
                    semantic_profile=(
                        "RECOVERED25_DESCENDANT_STABLE_CLIENT_HITMAP_R1"
                    ),
                    exact_recovered25_binary_proof=False,
                ),
            )
        )
        result = self.coordinator.walk_one_cell_with_runtime_collision(
            session,
            destination=MapPosition(1, 0, 1),
        )
        self.assertTrue(result.resolution.moved)
        self.assertEqual(
            result.collision_provider_kind,
            "RECOVERED25_CLIENT_HITMAP_RECONSTRUCTION",
        )
        self.assertEqual(
            result.collision_semantic_profile,
            "RECOVERED25_DESCENDANT_STABLE_CLIENT_HITMAP_R1",
        )
        self.assertFalse(result.collision_exact_binary_proof)

        self.stack.collision_router = None
        with self.assertRaisesRegex(ValueError, "no unified collision router"):
            self.coordinator.walk_one_cell_with_runtime_collision(
                session,
                destination=MapPosition(1, 0, 1),
            )

    def test_unified_runtime_collision_layers_dynamic_occupancy_after_static(self):
        session = self.coordinator.new_game(1)
        self.stack.collision_router = SimpleNamespace(
            routed_step_verdict=lambda **_kwargs: SimpleNamespace(
                decision=CollisionDecision(True, "static_allowed"),
                route=SimpleNamespace(
                    provider_kind="RECOVERED25_SERVER_COLLISION",
                    evidence_class="LATER_RECOVERED_SERVER_PAYLOAD_AND_MAPSET",
                    semantic_profile="RECOVERED25_SERVER_LS2MAP_MAPSET_R1",
                    exact_recovered25_binary_proof=None,
                ),
            )
        )

        blocked = self.coordinator.walk_one_cell_with_runtime_collision(
            session,
            destination=MapPosition(1, 0, 1),
            destination_occupants=(
                DynamicOccupant(kind=CHARACTER, overable=False),
            ),
        )
        self.assertFalse(blocked.resolution.moved)
        self.assertFalse(blocked.collision.allowed)
        self.assertEqual(blocked.collision.reason, "non_overable_character")
        self.assertTrue(blocked.static_collision.allowed)
        self.assertFalse(blocked.dynamic_collision.allowed)
        self.assertEqual(
            blocked.collision_provider_kind,
            "RECOVERED25_SERVER_COLLISION",
        )
        self.assertEqual(
            blocked.dynamic_occupancy_profile,
            "STONEAGE_DESCENDANT_LIVE_OBJECT_OVERABILITY_R1",
        )

        allowed = self.coordinator.walk_one_cell_with_runtime_collision(
            session,
            destination=MapPosition(1, 0, 1),
            destination_occupants=(
                DynamicOccupant(kind=GOLD, overable=False),
            ),
        )
        self.assertTrue(allowed.resolution.moved)
        self.assertTrue(allowed.collision.allowed)
        self.assertTrue(allowed.static_collision.allowed)
        self.assertTrue(allowed.dynamic_collision.allowed)

    def test_runtime_collision_queries_live_occupancy_registry(self):
        session = self.coordinator.new_game(1)
        self.stack.collision_router = SimpleNamespace(
            routed_step_verdict=lambda **_kwargs: SimpleNamespace(
                decision=CollisionDecision(True, "static_allowed"),
                route=SimpleNamespace(
                    provider_kind="RECOVERED25_SERVER_COLLISION",
                    evidence_class="LATER_RECOVERED_SERVER_PAYLOAD_AND_MAPSET",
                    semantic_profile="RECOVERED25_SERVER_LS2MAP_MAPSET_R1",
                    exact_recovered25_binary_proof=None,
                ),
            )
        )
        self.coordinator.occupancy_registry.register_character(
            object_id="char:77",
            position=MapPosition(1, 0, 1),
            overable=False,
            provenance="test:live-character",
        )
        blocked = self.coordinator.walk_one_cell_with_runtime_collision(
            session,
            destination=MapPosition(1, 0, 1),
        )
        self.assertFalse(blocked.resolution.moved)
        self.assertEqual(blocked.collision.reason, "non_overable_character")
        self.assertEqual(blocked.live_occupancy_object_ids, ("char:77",))
        self.assertEqual(
            blocked.live_occupancy_provenance,
            ("test:live-character",),
        )
        self.assertEqual(
            blocked.live_occupancy_registry_profile,
            "STONEAGE_LOCAL_LIVE_OCCUPANCY_STATE_R1",
        )

        self.coordinator.occupancy_registry.set_overable("char:77", True)
        allowed = self.coordinator.walk_one_cell_with_runtime_collision(
            session,
            destination=MapPosition(1, 0, 1),
        )
        self.assertTrue(allowed.resolution.moved)
        self.assertTrue(allowed.dynamic_collision.allowed)

    def test_coordinator_seeds_stack_initial_npc_occupancy(self):
        self.stack.npc_initial_occupancy = SimpleNamespace(
            populate_registry=lambda registry: registry.register_character(
                object_id="npc-placement:42",
                position=MapPosition(1, 0, 1),
                overable=True,
                provenance=(
                    "recovered25:npc-placement:42:"
                    "overability:INHERITED_DEFAULT_OVERABLE"
                ),
            )
        )
        coordinator = LocalRuntimeSessionCoordinator(
            stack=self.stack,
            persistence=InMemoryLocalPersistenceStore(),
        )
        self.stack.collision_router = SimpleNamespace(
            routed_step_verdict=lambda **_kwargs: SimpleNamespace(
                decision=CollisionDecision(True, "static_allowed"),
                route=SimpleNamespace(
                    provider_kind="RECOVERED25_SERVER_COLLISION",
                    evidence_class="LATER_RECOVERED_SERVER_PAYLOAD_AND_MAPSET",
                    semantic_profile="RECOVERED25_SERVER_LS2MAP_MAPSET_R1",
                    exact_recovered25_binary_proof=None,
                ),
            )
        )
        session = coordinator.new_game(1)
        result = coordinator.walk_one_cell_with_runtime_collision(
            session,
            destination=MapPosition(1, 0, 1),
        )
        self.assertTrue(result.resolution.moved)
        self.assertEqual(
            result.live_occupancy_object_ids,
            ("npc-placement:42",),
        )
        self.assertTrue(result.dynamic_collision.allowed)
        self.assertEqual(
            result.live_occupancy_provenance,
            (
                "recovered25:npc-placement:42:"
                "overability:INHERITED_DEFAULT_OVERABLE",
            ),
        )

    def test_dynamic_occupancy_cannot_override_static_denial(self):
        session = self.coordinator.new_game(1)
        self.stack.collision_router = SimpleNamespace(
            routed_step_verdict=lambda **_kwargs: SimpleNamespace(
                decision=CollisionDecision(False, "client_hitmap_blocked"),
                route=SimpleNamespace(
                    provider_kind="RECOVERED25_CLIENT_HITMAP_RECONSTRUCTION",
                    evidence_class=(
                        "LATER_RECOVERED_PLUS_PINNED_DESCENDANT_STABLE_ALGORITHM"
                    ),
                    semantic_profile=(
                        "RECOVERED25_DESCENDANT_STABLE_CLIENT_HITMAP_R1"
                    ),
                    exact_recovered25_binary_proof=False,
                ),
            )
        )
        result = self.coordinator.walk_one_cell_with_runtime_collision(
            session,
            destination=MapPosition(1, 0, 1),
            destination_occupants=(
                DynamicOccupant(kind=GOLD, overable=True),
            ),
        )
        self.assertFalse(result.resolution.moved)
        self.assertEqual(result.collision.reason, "client_hitmap_blocked")
        self.assertEqual(
            result.dynamic_collision.reason,
            "dynamic_occupancy_not_evaluated_static_denied",
        )
        self.assertEqual(
            result.collision_semantic_profile,
            "RECOVERED25_DESCENDANT_STABLE_CLIENT_HITMAP_R1",
        )

    def test_runtime_collision_frequency_miss_then_hit_requests_encounter(self):
        session = self.coordinator.new_game(1)
        self.stack.collision_router = SimpleNamespace(
            routed_step_verdict=lambda **_kwargs: SimpleNamespace(
                decision=CollisionDecision(True, "static_allowed"),
                route=SimpleNamespace(
                    provider_kind="TEST_STATIC",
                    evidence_class="TEST",
                    semantic_profile="TEST_STATIC_R1",
                    exact_recovered25_binary_proof=False,
                ),
            )
        )

        miss = (
            self.coordinator
            .walk_one_cell_with_runtime_collision_and_encounter_frequency(
                session,
                destination=MapPosition(1, 0, 1),
                frequency_roll=119,
                encounter_rolls=EncounterRolls(0, 0, 0),
            )
        )
        self.assertTrue(miss.walk.resolution.moved)
        self.assertIsNotNone(miss.frequency)
        self.assertEqual(miss.frequency.clamped_current, 10)
        self.assertFalse(miss.frequency.roll_hit)
        self.assertEqual(self.coordinator.encounter_frequency.current, 11)
        self.assertIsNone(miss.group_encounter)
        self.assertIsNone(miss.encounter)

        hit = (
            self.coordinator
            .walk_one_cell_with_runtime_collision_and_encounter_frequency(
                miss.session,
                destination=MapPosition(1, 0, 2),
                frequency_roll=10,
                encounter_rolls=EncounterRolls(0, 0, 1),
            )
        )
        self.assertTrue(hit.frequency.roll_hit)
        self.assertTrue(hit.frequency.encounter_triggered)
        self.assertEqual(self.coordinator.encounter_frequency.current, 10)
        self.assertIsNotNone(hit.group_encounter)
        self.assertEqual(hit.group_encounter.group_id, 7)
        self.assertIsNotNone(hit.encounter)
        self.assertEqual(hit.encounter.enemy_variant_id.value, 700)
        self.assertEqual(hit.encounter.pet_template_id.value, 88)
        self.assertEqual(hit.encounter.level, 4)

    def test_classic_warp_suppresses_hit_but_preserves_cep_clamp(self):
        session = self.coordinator.new_game(1)
        self.stack.collision_router = SimpleNamespace(
            routed_step_verdict=lambda **_kwargs: SimpleNamespace(
                decision=CollisionDecision(True, "static_allowed"),
                route=SimpleNamespace(
                    provider_kind="TEST_STATIC",
                    evidence_class="TEST",
                    semantic_profile="TEST_STATIC_R1",
                    exact_recovered25_binary_proof=False,
                ),
            )
        )
        result = (
            self.coordinator
            .walk_one_cell_with_runtime_collision_and_encounter_frequency(
                session,
                destination=MapPosition(1, 1, 0),
                frequency_roll=0,
                encounter_rolls=EncounterRolls(0, 0, 0),
            )
        )
        self.assertTrue(result.walk.resolution.warp_triggered)
        self.assertTrue(result.walk.resolution.encounter_suppressed)
        self.assertTrue(result.frequency.roll_hit)
        self.assertTrue(result.frequency.encounter_suppressed)
        self.assertFalse(result.frequency.encounter_triggered)
        self.assertEqual(self.coordinator.encounter_frequency.current, 10)
        self.assertIsNone(result.group_encounter)
        self.assertIsNone(result.encounter)
        self.assertEqual(result.session.player_position, MapPosition(2, 2, 2))

    def test_blocked_walk_does_not_advance_cep(self):
        session = self.coordinator.new_game(1)
        self.stack.collision_router = SimpleNamespace(
            routed_step_verdict=lambda **_kwargs: SimpleNamespace(
                decision=CollisionDecision(False, "static_blocked"),
                route=SimpleNamespace(
                    provider_kind="TEST_STATIC",
                    evidence_class="TEST",
                    semantic_profile="TEST_STATIC_R1",
                    exact_recovered25_binary_proof=False,
                ),
            )
        )
        result = (
            self.coordinator
            .walk_one_cell_with_runtime_collision_and_encounter_frequency(
                session,
                destination=MapPosition(1, 0, 1),
                frequency_roll=0,
                encounter_rolls=EncounterRolls(0, 0, 0),
            )
        )
        self.assertFalse(result.walk.resolution.moved)
        self.assertIsNone(result.frequency)
        self.assertEqual(
            self.coordinator.encounter_frequency,
            EncounterFrequencyState(),
        )

    def test_cep_is_transient_runtime_state_not_save_payload(self):
        session = self.coordinator.new_game(1)
        self.coordinator.encounter_frequency = EncounterFrequencyState(
            current=17,
            minimum=10,
            maximum=20,
        )
        self.coordinator.save_game("cep-slot", session)
        self.assertNotIn("encounter_frequency", self.store.rows["cep-slot"])

        restored = self.coordinator.continue_game("cep-slot")
        self.assertEqual(restored.player_position, session.player_position)
        self.assertEqual(
            self.coordinator.encounter_frequency,
            EncounterFrequencyState(),
        )

        self.coordinator.encounter_frequency = EncounterFrequencyState(
            current=15,
            minimum=10,
            maximum=20,
        )
        self.coordinator.new_game(1)
        self.assertEqual(
            self.coordinator.encounter_frequency,
            EncounterFrequencyState(),
        )

    def test_group_battle_context_clones_state_and_settlement_returns_new_session(self):
        session = LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1, 0, 0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"battle-route"}),
        )
        group = self.stack.request_encounter_group(
            session,
            group_roll=0,
        )
        self.assertIsNotNone(group)

        context = self.coordinator.start_group_battle(
            session,
            group,
            entry_count_roll=1,
            selection_rolls=(0,),
            birth_rolls=(
                EnemyBirthRolls(
                    level_roll=1,
                    birth_offsets=(0, 0, 0, 0),
                    spawn_allocation_rolls=(0, 1, 2, 3, 0, 1, 2, 3, 0, 1),
                ),
            ),
        )
        self.assertEqual(len(context.spawned_enemies), 1)
        self.assertIsNone(context.battle.enemies[0].name)
        self.assertEqual(context.origin_position, session.player_position)

        settled = self.coordinator.settle_group_battle(
            context,
            BattleOutcome(
                result="victory",
                player_updates={"hp": 70, "exp": 100},
                pet_updates={},
            ),
        )
        self.assertEqual(
            session.player_state.character.fields["hp"],
            100,
        )
        self.assertEqual(
            session.player_state.character.fields["exp"],
            0,
        )
        self.assertEqual(
            settled.player_state.character.fields["hp"],
            70,
        )
        self.assertEqual(
            settled.player_state.character.fields["exp"],
            100,
        )
        self.assertIsNot(
            settled.player_state,
            session.player_state,
        )
        self.assertEqual(settled.player_position, session.player_position)
        self.assertEqual(settled.world_flags, session.world_flags)

    def test_core_dying_plan_zeroes_gold_but_keeps_world_actions_explicit(self):
        session = LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1, 0, 0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"death-plan"}),
        )
        plan = self.coordinator.plan_player_core_dying(
            session,
            attacker_class="enemy",
            equipped_slots=(0, 2, 4),
            dead_count_before=7,
        )
        self.assertTrue(plan.party_discharged)
        self.assertEqual(plan.item_drop_mode, "all_equipped")
        self.assertEqual(plan.requested_item_drop_slots, (0, 2, 4))
        self.assertEqual(plan.random_item_drop_candidates, ())
        self.assertEqual(plan.random_item_drop_count, 0)
        self.assertEqual(plan.requested_ground_gold, 50)
        self.assertEqual(plan.final_carried_gold, 0)
        self.assertEqual(plan.dead_count_after, 8)
        self.assertEqual(
            plan.cleared_statuses,
            (
                "paralysis",
                "sleep",
                "stone",
                "drunk",
                "confusion",
                "poison",
            ),
        )
        self.assertTrue(plan.is_dead)
        self.assertFalse(plan.is_attacked)
        self.assertEqual(
            plan.session.player_state.character.fields["gold"],
            0,
        )
        self.assertEqual(
            session.player_state.character.fields["gold"],
            101,
        )
        self.assertEqual(plan.session.player_position, session.player_position)

    def test_resurrection_is_in_place_hp_only_and_does_not_refill_mp(self):
        session = LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1, 2, 1),
            player_state=_battle_player_state(),
            world_flags=frozenset({"resurrection"}),
        )
        result = self.coordinator.resurrect_player_in_place(
            session,
            requested_hp=0,
        )
        fields = result.session.player_state.character.fields
        self.assertEqual(fields["hp"], 1)
        self.assertEqual(fields["mp"], 40)
        self.assertEqual(result.session.player_position, MapPosition(1, 2, 1))
        self.assertTrue(result.base_image_restored)
        self.assertFalse(result.is_dead)
        self.assertTrue(result.is_attacked)
        self.assertFalse(result.is_overed)
        self.assertTrue(result.mp_unchanged)
        self.assertTrue(result.location_unchanged)
        self.assertEqual(
            session.player_state.character.fields["hp"],
            100,
        )
        self.assertEqual(
            session.player_state.character.fields["mp"],
            40,
        )

    def test_enemy_attack_can_reach_defeat_and_settle_death_hp_charm_without_exp(self):
        session = LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1, 0, 0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"defeat-route"}),
        )
        group = self.stack.request_encounter_group(session, group_roll=0)
        context = self.coordinator.start_group_battle(
            session,
            group,
            entry_count_roll=1,
            selection_rolls=(0,),
            birth_rolls=(
                EnemyBirthRolls(
                    level_roll=1,
                    birth_offsets=(0, 0, 0, 0),
                    spawn_allocation_rolls=(
                        0, 1, 2, 3, 0, 1, 2, 3, 0, 1
                    ),
                ),
            ),
        )
        player = replace(
            context.battle.player,
            hp=100,
            max_hp=100,
            defense=0,
            quick=10,
        )
        enemy = replace(
            context.battle.enemies[0],
            attack=60,
            quick=200,
        )
        context = replace(
            context,
            battle=replace(
                context.battle,
                player=player,
                enemies=(enemy,),
            ),
        )
        enemy_id = enemy.participant_id
        context = self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player": 0, enemy_id: 10},
        )
        result_context, round_result = (
            self.coordinator.resolve_persistent_attack_wait_round(
                context,
                commands={
                    "player": BattleCommand(BATTLE_COM_WAIT),
                    enemy_id: BattleCommand(
                        BATTLE_COM_ATTACK,
                        command2=0,
                    ),
                },
                initiative_random_subtracts={
                    "player": 0,
                    enemy_id: 0,
                },
                profiles={
                    "player": BattleCombatProfile(
                        fixed_dex=10,
                        fixed_luck=0,
                        earth=0,
                        water=0,
                        fire=0,
                        wind=0,
                    ),
                    enemy_id: BattleCombatProfile(
                        fixed_dex=200,
                        fixed_luck=0,
                        earth=0,
                        water=0,
                        fire=0,
                        wind=0,
                    ),
                },
                attack_rolls={
                    enemy_id: OrdinaryAttackRolls(
                        dodge_roll_1_10000=10000,
                        critical_roll_1_10000=10000,
                        damage_roll=0,
                        minimum_damage_roll_0_1=1,
                    )
                },
                defense_profile="newpower_70pct",
            )
        )
        terminal = round_result.after
        self.assertEqual(terminal.phase, "finished")
        self.assertEqual(terminal.result, "defeat")
        self.assertEqual(terminal.winning_side, 1)
        self.assertEqual(terminal.hp_by_participant_id["player"], 0)
        self.assertEqual(terminal.pending_player_charm_delta, -1)
        self.assertEqual(
            terminal.pending_exp_by_participant_id["player"],
            0,
        )

        settled = self.coordinator.settle_persistent_defeat(
            result_context
        )
        fields = settled.player_state.character.fields
        self.assertEqual(fields["hp"], 1)
        self.assertEqual(fields["exp"], 0)
        self.assertEqual(fields["charm"], 4)
        self.assertEqual(settled.player_position, session.player_position)
        self.assertEqual(settled.world_flags, session.world_flags)

        original = session.player_state.character.fields
        self.assertEqual(original["hp"], 100)
        self.assertEqual(original["exp"], 0)
        self.assertEqual(original["charm"], 5)

        with self.assertRaisesRegex(
            ValueError,
            "terminal defeat state",
        ):
            self.coordinator.settle_persistent_defeat(context)

    def test_capture_round_persists_complete_pet_in_working_snapshot_and_settlement(self):
        session = LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1, 0, 0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"capture-route"}),
        )
        group = self.stack.request_encounter_group(session, group_roll=0)
        context = self.coordinator.start_group_battle(
            session,
            group,
            entry_count_roll=1,
            selection_rolls=(0,),
            birth_rolls=(
                EnemyBirthRolls(
                    level_roll=1,
                    birth_offsets=(0, 0, 0, 0),
                    spawn_allocation_rolls=(
                        0, 1, 2, 3, 0, 1, 2, 3, 0, 1
                    ),
                ),
            ),
        )
        enemy = replace(
            context.battle.enemies[0],
            hp=10,
            max_hp=100,
            quick=20,
            capturable=True,
            capture_default=99,
        )
        context = replace(
            context,
            battle=replace(context.battle, enemies=(enemy,)),
        )
        enemy_id = enemy.participant_id
        context = self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player": 0, enemy_id: 10},
        )
        captured = PetActor(
            slot=PetSlot(0),
            variant_id=EnemyVariantId(enemy.source_variant_id),
            template_id=PetTemplateId(enemy.source_template_id),
            runtime_object_id=None,
            state=MappingProxyType(
                {
                    "level": enemy.level,
                    "hp": 10,
                    "max_hp": 100,
                    "exp": 0,
                    "max_exp": 500,
                    "attack": enemy.attack,
                    "defense": enemy.defense,
                    "quick": enemy.quick,
                    "name": "captured-test",
                }
            ),
            skills=(),
            growth=None,
        )
        profiles = {
            "player": BattleCombatProfile(
                fixed_dex=100,
                fixed_luck=7,
                earth=0,
                water=0,
                fire=0,
                wind=0,
            ),
            enemy_id: BattleCombatProfile(
                fixed_dex=20,
                fixed_luck=0,
                earth=0,
                water=0,
                fire=0,
                wind=0,
            ),
        }

        captured_context, result = (
            self.coordinator.resolve_persistent_capture_round(
                context,
                commands={
                    "player": BattleCommand(
                        BATTLE_COM_CAPTURE,
                        command2=10,
                    ),
                    enemy_id: BattleCommand(BATTLE_COM_WAIT),
                },
                initiative_random_subtracts={
                    "player": 0,
                    enemy_id: 0,
                },
                profiles=profiles,
                attack_rolls={},
                capture_context=OrdinaryCaptureContext(
                    attacker_charm=100,
                    occupied_pet_slots=(),
                ),
                capture_rolls=OrdinaryCaptureRolls(
                    capture_roll_1_100=1,
                ),
                captured_pets_by_target_id={
                    enemy_id: captured,
                },
                defense_profile="newpower_70pct",
            )
        )
        self.assertEqual(result.after.phase, "finished")
        self.assertEqual(result.after.result, "victory")
        self.assertEqual(result.round.exited_participant_ids, (enemy_id,))
        self.assertEqual(
            result.after.pending_exp_by_participant_id["player"],
            0,
        )
        self.assertIsNotNone(
            captured_context.working_persistent_state_payload
        )

        settled = (
            self.coordinator
            .settle_persistent_group_battle_without_level_crossing(
                captured_context
            )
        )
        self.assertEqual(session.player_state.pets, {})
        self.assertIn(PetSlot(0), settled.player_state.pets)
        pet = settled.player_state.pets[PetSlot(0)]
        self.assertEqual(pet.variant_id.value, enemy.source_variant_id)
        self.assertEqual(pet.template_id.value, enemy.source_template_id)
        self.assertEqual(pet.state["hp"], 10)
        self.assertEqual(settled.player_state.character.fields["exp"], 0)

        with self.assertRaisesRegex(
            ValueError,
            "captured pet mapping mismatch",
        ):
            self.coordinator.resolve_persistent_capture_round(
                context,
                commands={
                    "player": BattleCommand(
                        BATTLE_COM_CAPTURE,
                        command2=10,
                    ),
                    enemy_id: BattleCommand(BATTLE_COM_WAIT),
                },
                initiative_random_subtracts={
                    "player": 0,
                    enemy_id: 0,
                },
                profiles=profiles,
                attack_rolls={},
                capture_context=OrdinaryCaptureContext(
                    attacker_charm=100,
                    occupied_pet_slots=(),
                ),
                capture_rolls=OrdinaryCaptureRolls(
                    capture_roll_1_100=1,
                ),
                captured_pets_by_target_id={},
                defense_profile="newpower_70pct",
            )
        self.assertIsNone(context.working_persistent_state_payload)
        self.assertEqual(session.player_state.pets, {})

    def test_player_escape_round_is_explicit_terminal_and_discards_profit(self):
        session = LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1, 0, 0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"escape-route"}),
        )
        group = self.stack.request_encounter_group(session, group_roll=0)
        context = self.coordinator.start_group_battle(
            session,
            group,
            entry_count_roll=1,
            selection_rolls=(0,),
            birth_rolls=(
                EnemyBirthRolls(
                    level_roll=1,
                    birth_offsets=(0, 0, 0, 0),
                    spawn_allocation_rolls=(
                        0, 1, 2, 3, 0, 1, 2, 3, 0, 1
                    ),
                ),
            ),
        )
        enemy_id = context.battle.enemies[0].participant_id
        context = self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player": 0, enemy_id: 10},
        )

        profiles = {
            "player": BattleCombatProfile(
                fixed_dex=100,
                fixed_luck=5,
                earth=0,
                water=0,
                fire=0,
                wind=0,
            ),
            enemy_id: BattleCombatProfile(
                fixed_dex=10,
                fixed_luck=0,
                earth=0,
                water=0,
                fire=0,
                wind=0,
            ),
        }
        escaped_context, round_result = (
            self.coordinator.resolve_persistent_escape_round(
                context,
                commands={
                    "player": BattleCommand(BATTLE_COM_ESCAPE),
                    enemy_id: BattleCommand(BATTLE_COM_WAIT),
                },
                initiative_random_subtracts={
                    "player": 0,
                    enemy_id: 0,
                },
                profiles=profiles,
                attack_rolls={},
                escape_context=OrdinaryEscapeContext(
                    stored_escape_count_before=0,
                ),
                escape_rolls=OrdinaryEscapeRolls(
                    escape_roll_1_100=1,
                ),
                defense_profile="newpower_70pct",
            )
        )
        self.assertEqual(round_result.after.phase, "finished")
        self.assertEqual(round_result.after.result, "escape")
        self.assertEqual(
            round_result.after.escape_count_by_participant_id["player"],
            1,
        )
        self.assertEqual(
            round_result.after.pending_exp_by_participant_id["player"],
            0,
        )

        settled = self.coordinator.settle_persistent_escape(
            escaped_context
        )
        self.assertEqual(
            settled.player_state.character.fields["hp"],
            100,
        )
        self.assertEqual(
            settled.player_state.character.fields["exp"],
            0,
        )
        self.assertEqual(settled.player_position, session.player_position)
        self.assertEqual(settled.world_flags, session.world_flags)
        self.assertEqual(
            session.player_state.character.fields["exp"],
            0,
        )

        with self.assertRaisesRegex(ValueError, "requires player ESCAPE"):
            self.coordinator.resolve_persistent_escape_round(
                context,
                commands={
                    "player": BattleCommand(BATTLE_COM_WAIT),
                    enemy_id: BattleCommand(BATTLE_COM_WAIT),
                },
                initiative_random_subtracts={
                    "player": 0,
                    enemy_id: 0,
                },
                profiles=profiles,
                attack_rolls={},
                escape_context=OrdinaryEscapeContext(
                    stored_escape_count_before=0,
                ),
                escape_rolls=OrdinaryEscapeRolls(
                    escape_roll_1_100=1,
                ),
                defense_profile="newpower_70pct",
            )

    def test_persistent_attack_wait_rounds_carry_hp_to_terminal_and_settle_clone(self):
        session = LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1, 0, 0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"persistent-battle"}),
        )
        group = self.stack.request_encounter_group(
            session,
            group_roll=0,
        )
        context = self.coordinator.start_group_battle(
            session,
            group,
            entry_count_roll=1,
            selection_rolls=(0,),
            birth_rolls=(
                EnemyBirthRolls(
                    level_roll=1,
                    birth_offsets=(0, 0, 0, 0),
                    spawn_allocation_rolls=(
                        0, 1, 2, 3, 0, 1, 2, 3, 0, 1
                    ),
                ),
            ),
        )
        enemy = replace(
            context.battle.enemies[0],
            hp=1000,
            max_hp=1000,
            defense=0,
            quick=10,
        )
        context = replace(
            context,
            battle=replace(context.battle, enemies=(enemy,)),
        )
        enemy_id = enemy.participant_id
        context = self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player": 0, enemy_id: 10},
        )

        profiles = {
            "player": BattleCombatProfile(
                fixed_dex=100,
                fixed_luck=0,
                earth=0,
                water=0,
                fire=0,
                wind=0,
            ),
            enemy_id: BattleCombatProfile(
                fixed_dex=10,
                fixed_luck=0,
                earth=0,
                water=0,
                fire=0,
                wind=0,
            ),
        }
        commands = {
            "player": BattleCommand(BATTLE_COM_ATTACK, command2=10),
            enemy_id: BattleCommand(BATTLE_COM_WAIT),
        }
        initiative = {"player": 0, enemy_id: 0}
        attack_rolls = {
            "player": OrdinaryAttackRolls(
                dodge_roll_1_10000=10000,
                critical_roll_1_10000=10000,
                damage_roll=0,
                minimum_damage_roll_0_1=1,
            )
        }

        first_context, first = (
            self.coordinator.resolve_persistent_attack_wait_round(
                context,
                commands=commands,
                initiative_random_subtracts=initiative,
                profiles=profiles,
                attack_rolls=attack_rolls,
                defense_profile="newpower_70pct",
            )
        )
        self.assertEqual(first.after.turn, 1)
        self.assertGreater(first.after.hp_by_participant_id[enemy_id], 0)
        self.assertLess(first.after.hp_by_participant_id[enemy_id], 1000)

        current = first_context
        for _ in range(40):
            if current.persistent_battle_state.phase == "finished":
                break
            current, _round = (
                self.coordinator.resolve_persistent_attack_wait_round(
                    current,
                    commands={
                        participant_id: command
                        for participant_id, command in commands.items()
                        if participant_id
                        in current.persistent_battle_state.hp_by_participant_id
                    },
                    initiative_random_subtracts={
                        participant_id: value
                        for participant_id, value in initiative.items()
                        if participant_id
                        in current.persistent_battle_state.hp_by_participant_id
                    },
                    profiles=profiles,
                    attack_rolls=attack_rolls,
                    defense_profile="newpower_70pct",
                )
            )

        terminal = current.persistent_battle_state
        self.assertEqual(terminal.phase, "finished")
        self.assertEqual(terminal.result, "victory")
        self.assertGreater(terminal.turn, 1)
        self.assertEqual(terminal.hp_by_participant_id[enemy_id], 0)
        self.assertEqual(
            terminal.pending_exp_by_participant_id["player"],
            100,
        )

        settled = (
            self.coordinator
            .settle_persistent_group_battle_without_level_crossing(
                current
            )
        )
        self.assertEqual(
            session.player_state.character.fields["hp"],
            100,
        )
        self.assertEqual(
            session.player_state.character.fields["exp"],
            0,
        )
        self.assertEqual(
            settled.player_state.character.fields["exp"],
            100,
        )
        self.assertEqual(settled.player_position, session.player_position)
        self.assertEqual(settled.world_flags, session.world_flags)

        with self.assertRaisesRegex(ValueError, "ATTACK/WAIT only"):
            self.coordinator.resolve_persistent_attack_wait_round(
                context,
                commands={
                    "player": BattleCommand(2),
                    enemy_id: BattleCommand(BATTLE_COM_WAIT),
                },
                initiative_random_subtracts=initiative,
                profiles=profiles,
                attack_rolls=attack_rolls,
                defense_profile="newpower_70pct",
            )

    def test_terminal_victory_crosses_player_exp_threshold_atomically(self):
        player_state = _battle_player_state()
        player_state.character = PlayerState(
            MappingProxyType(
                {
                    **dict(player_state.character.fields),
                    "exp": 950,
                    "max_exp": 1000,
                    "free_stat_points": 4,
                    "duel_point_like_state": 12,
                }
            )
        )
        session = LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1, 0, 0),
            player_state=player_state,
            world_flags=frozenset({"progression-battle"}),
        )
        group = self.stack.request_encounter_group(session, group_roll=0)
        context = self.coordinator.start_group_battle(
            session,
            group,
            entry_count_roll=1,
            selection_rolls=(0,),
            birth_rolls=(
                EnemyBirthRolls(
                    level_roll=1,
                    birth_offsets=(0, 0, 0, 0),
                    spawn_allocation_rolls=(
                        0, 1, 2, 3, 0, 1, 2, 3, 0, 1
                    ),
                ),
            ),
        )
        enemy = replace(
            context.battle.enemies[0],
            hp=1,
            max_hp=1,
            defense=0,
            quick=10,
        )
        context = replace(
            context,
            battle=replace(context.battle, enemies=(enemy,)),
        )
        enemy_id = enemy.participant_id
        context = self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player": 0, enemy_id: 10},
        )
        context, round_result = (
            self.coordinator.resolve_persistent_attack_wait_round(
                context,
                commands={
                    "player": BattleCommand(BATTLE_COM_ATTACK, command2=10),
                    enemy_id: BattleCommand(BATTLE_COM_WAIT),
                },
                initiative_random_subtracts={
                    "player": 0,
                    enemy_id: 0,
                },
                profiles={
                    "player": BattleCombatProfile(
                        fixed_dex=100,
                        fixed_luck=0,
                        earth=0,
                        water=0,
                        fire=0,
                        wind=0,
                    ),
                    enemy_id: BattleCombatProfile(
                        fixed_dex=10,
                        fixed_luck=0,
                        earth=0,
                        water=0,
                        fire=0,
                        wind=0,
                    ),
                },
                attack_rolls={
                    "player": OrdinaryAttackRolls(
                        dodge_roll_1_10000=10000,
                        critical_roll_1_10000=10000,
                        damage_roll=0,
                        minimum_damage_roll_0_1=1,
                    )
                },
                defense_profile="newpower_70pct",
            )
        )
        terminal = round_result.after
        self.assertEqual(terminal.phase, "finished")
        self.assertEqual(terminal.result, "victory")
        self.assertEqual(
            terminal.pending_exp_by_participant_id["player"],
            100,
        )

        settled = self.coordinator.settle_persistent_group_battle_with_progression(
            context,
            player_exp_profile="legacy_cumulative",
            next_player_max_exp_by_level={6: 1500},
        )
        original = session.player_state.character.fields
        updated = settled.player_state.character.fields
        self.assertEqual(original["level"], 5)
        self.assertEqual(original["exp"], 950)
        self.assertEqual(original["max_exp"], 1000)
        self.assertEqual(original["free_stat_points"], 4)
        self.assertEqual(original["charm"], 5)
        self.assertEqual(original["duel_point_like_state"], 12)
        self.assertEqual(updated["level"], 6)
        self.assertEqual(updated["exp"], 1050)
        self.assertEqual(updated["max_exp"], 1500)
        self.assertEqual(updated["free_stat_points"], 7)
        self.assertEqual(updated["charm"], 7)
        self.assertEqual(updated["duel_point_like_state"], 72)
        self.assertEqual(settled.player_position, session.player_position)
        self.assertEqual(settled.world_flags, session.world_flags)

    def test_reward_only_ride_pet_crosses_exp_threshold_with_explicit_growth(self):
        player_state = _battle_player_state()
        pet = PetActor(
            slot=PetSlot(0),
            variant_id=EnemyVariantId(700),
            template_id=PetTemplateId(88),
            runtime_object_id=None,
            state=MappingProxyType(
                {
                    "name": "ride-progression-test",
                    "level": 5,
                    "hp": 100,
                    "max_hp": 100,
                    "attack": 20,
                    "defense": 20,
                    "quick": 20,
                    "exp": 950,
                    "max_exp": 1000,
                }
            ),
            skills=(),
            growth=PetGrowthState(
                pet_rank=0,
                alloc_point=pack_growth_base(20, 20, 20, 20),
                internal_vital=2000,
                internal_strength=2000,
                internal_toughness=2000,
                internal_dexterity=2000,
                variable_ai=0,
            ),
        )
        player_state.pets[PetSlot(0)] = pet
        session = LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1, 0, 0),
            player_state=player_state,
            world_flags=frozenset({"ride-pet-progression"}),
        )
        group = self.stack.request_encounter_group(session, group_roll=0)
        context = self.coordinator.start_group_battle(
            session,
            group,
            entry_count_roll=1,
            selection_rolls=(0,),
            birth_rolls=(
                EnemyBirthRolls(
                    level_roll=1,
                    birth_offsets=(0, 0, 0, 0),
                    spawn_allocation_rolls=(
                        0, 1, 2, 3, 0, 1, 2, 3, 0, 1
                    ),
                ),
            ),
            ride_pet_slot=0,
        )
        enemy = replace(
            context.battle.enemies[0],
            hp=1,
            max_hp=1,
            defense=0,
            quick=10,
        )
        context = replace(
            context,
            battle=replace(context.battle, enemies=(enemy,)),
        )
        enemy_id = enemy.participant_id
        context = self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player": 0, enemy_id: 10},
        )
        context, round_result = (
            self.coordinator.resolve_persistent_attack_wait_round(
                context,
                commands={
                    "player": BattleCommand(BATTLE_COM_ATTACK, command2=10),
                    enemy_id: BattleCommand(BATTLE_COM_WAIT),
                },
                initiative_random_subtracts={
                    "player": 0,
                    enemy_id: 0,
                },
                profiles={
                    "player": BattleCombatProfile(
                        fixed_dex=100,
                        fixed_luck=0,
                        earth=0,
                        water=0,
                        fire=0,
                        wind=0,
                    ),
                    enemy_id: BattleCombatProfile(
                        fixed_dex=10,
                        fixed_luck=0,
                        earth=0,
                        water=0,
                        fire=0,
                        wind=0,
                    ),
                },
                attack_rolls={
                    "player": OrdinaryAttackRolls(
                        dodge_roll_1_10000=10000,
                        critical_roll_1_10000=10000,
                        damage_roll=0,
                        minimum_damage_roll_0_1=1,
                    )
                },
                defense_profile="newpower_70pct",
            )
        )
        terminal = round_result.after
        self.assertEqual(terminal.phase, "finished")
        self.assertEqual(terminal.result, "victory")
        self.assertEqual(
            terminal.pending_exp_by_participant_id["player"],
            100,
        )
        self.assertEqual(
            terminal.pending_exp_by_participant_id["pet:0"],
            60,
        )

        settled = self.coordinator.settle_persistent_group_battle_with_progression(
            context,
            player_exp_profile="legacy_cumulative",
            next_player_max_exp_by_level={},
            pet_exp_profile="legacy_cumulative",
            next_pet_max_exp_by_slot={0: {6: 1500}},
            pet_level_growth_rolls_by_slot={
                0: (
                    PetLevelGrowthRolls(
                        (0, 0, 0, 1, 1, 2, 2, 2, 3, 3),
                        500,
                    ),
                )
            },
        )
        original_pet = session.player_state.pets[PetSlot(0)]
        updated_pet = settled.player_state.pets[PetSlot(0)]
        self.assertEqual(original_pet.state["level"], 5)
        self.assertEqual(original_pet.state["exp"], 950)
        self.assertEqual(original_pet.state["max_exp"], 1000)
        self.assertEqual(original_pet.growth.internal_vital, 2000)
        self.assertEqual(original_pet.growth.variable_ai, 0)

        self.assertEqual(
            settled.player_state.character.fields["exp"],
            100,
        )
        self.assertEqual(updated_pet.state["level"], 6)
        self.assertEqual(updated_pet.state["exp"], 1010)
        self.assertEqual(updated_pet.state["max_exp"], 1500)
        self.assertEqual(updated_pet.state["hp"], 100)
        self.assertEqual(updated_pet.state["max_hp"], 147)
        self.assertEqual(updated_pet.state["attack"], 26)
        self.assertEqual(updated_pet.state["defense"], 26)
        self.assertEqual(updated_pet.state["quick"], 21)
        self.assertEqual(updated_pet.growth.pet_rank, 0)
        self.assertEqual(
            updated_pet.growth.alloc_point,
            original_pet.growth.alloc_point,
        )
        self.assertEqual(updated_pet.growth.internal_vital, 2115)
        self.assertEqual(updated_pet.growth.internal_strength, 2110)
        self.assertEqual(updated_pet.growth.internal_toughness, 2115)
        self.assertEqual(updated_pet.growth.internal_dexterity, 2110)
        self.assertEqual(updated_pet.growth.variable_ai, 500)
        self.assertEqual(settled.player_position, session.player_position)
        self.assertEqual(settled.world_flags, session.world_flags)

    def test_classic_overlap_warp_is_reused_not_reimplemented(self):
        session = self.coordinator.new_game(1)
        result = self.coordinator.walk_one_cell(
            session,
            destination=MapPosition(1, 1, 0),
            entry_allowed=True,
        )
        self.assertTrue(result.resolution.warp_triggered)
        self.assertTrue(result.resolution.encounter_suppressed)
        self.assertEqual(result.session.player_position, MapPosition(2, 2, 2))

    def test_interaction_discovery_is_spatial_semantic_and_non_mutating(self):
        session = self.coordinator.new_game(1)
        self.assertEqual(
            self.coordinator.discover_state_gated_interactions(session),
            (),
        )
        self.assertEqual(self.stack.evaluation_calls, 0)

        at_gate = LocalRuntimeSessionState(
            contract_id=session.contract_id,
            world_profile=session.world_profile,
            hometown_ordinal=session.hometown_ordinal,
            player_position=MapPosition(2, 2, 2),
            player_state=session.player_state,
        )
        self.stack.allow = False
        denied = self.coordinator.discover_state_gated_interactions(at_gate)
        self.assertEqual(
            tuple(row.transition_id for row in denied),
            tuple(sorted(self.profile.transitions)),
        )
        self.assertTrue(all(row.interaction_kind == "DIALOGUE_WARPMAN" for row in denied))
        self.assertTrue(all(not row.allowed for row in denied))
        self.assertTrue(all(row.execution_supported for row in denied))
        self.assertTrue(
            all(row.provenance["source_profile"] == "recovered25" for row in denied)
        )
        self.assertEqual(
            self.stack.evaluation_calls,
            len(self.profile.transitions),
        )
        self.assertEqual(at_gate.player_position, MapPosition(2, 2, 2))
        self.assertFalse(
            any(
                hasattr(row, attr)
                for row in denied
                for attr in ("source_rect", "destination", "argument_data")
            )
        )

        self.stack.allow = True
        allowed = self.coordinator.discover_state_gated_interactions(at_gate)
        self.assertTrue(all(row.allowed for row in allowed))
        first = allowed[0]
        dispatched = self.coordinator.dispatch_state_gated_interaction(
            at_gate,
            first.transition_id,
        )
        self.assertTrue(dispatched.decision.allowed)
        self.assertEqual(
            dispatched.session.player_position,
            MapPosition(1, 2, 2),
        )

    def test_interaction_discovery_surfaces_future_mutation_as_unsupported(self):
        session = self.coordinator.new_game(1)
        at_gate = LocalRuntimeSessionState(
            contract_id=session.contract_id,
            world_profile=session.world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(2, 2, 2),
            player_state=session.player_state,
        )

        def evaluate_with_consumption(_transition_id, _session):
            return TransitionGateDecision(
                allowed=True,
                reason="future mutation",
                consumed_state={"item": 1},
            )

        self.stack.evaluate_transition = evaluate_with_consumption
        rows = self.coordinator.discover_state_gated_interactions(at_gate)
        self.assertTrue(rows)
        self.assertTrue(all(row.allowed for row in rows))
        self.assertTrue(all(not row.execution_supported for row in rows))

    def test_state_gated_transition_requires_spatial_and_live_gate_checks(self):
        transition_id = next(iter(self.profile.transitions))
        session = self.coordinator.new_game(1)

        outside = self.coordinator.execute_state_gated_transition(
            session,
            transition_id,
        )
        self.assertFalse(outside.decision.allowed)
        self.assertEqual(outside.session, session)
        self.assertEqual(self.stack.evaluation_calls, 0)

        at_gate = LocalRuntimeSessionState(
            contract_id=session.contract_id,
            world_profile=session.world_profile,
            hometown_ordinal=session.hometown_ordinal,
            player_position=MapPosition(2, 2, 2),
            player_state=session.player_state,
        )
        self.stack.allow = False
        denied = self.coordinator.execute_state_gated_transition(
            at_gate,
            transition_id,
        )
        self.assertFalse(denied.decision.allowed)
        self.assertEqual(denied.session.player_position, MapPosition(2, 2, 2))

        self.stack.allow = True
        allowed = self.coordinator.execute_state_gated_transition(
            at_gate,
            transition_id,
        )
        self.assertTrue(allowed.decision.allowed)
        self.assertEqual(allowed.session.player_position, MapPosition(1, 2, 2))

    def test_future_consumed_state_cannot_be_silently_ignored(self):
        transition_id = next(iter(self.profile.transitions))
        session = self.coordinator.new_game(1)
        at_gate = LocalRuntimeSessionState(
            contract_id=session.contract_id,
            world_profile=session.world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(2, 2, 2),
            player_state=session.player_state,
        )

        def evaluate_with_consumption(_transition_id, _session):
            return TransitionGateDecision(
                allowed=True,
                reason="future mutation",
                consumed_state={"item": 1},
            )

        self.stack.evaluate_transition = evaluate_with_consumption
        with self.assertRaises(ValueError):
            self.coordinator.execute_state_gated_transition(
                at_gate,
                transition_id,
            )


if __name__ == "__main__":
    unittest.main()
