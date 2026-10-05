import json
import hashlib
from dataclasses import replace
import tempfile
import unittest
from unittest.mock import patch
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
    BATTLE_COM_GUARD,
    BATTLE_COM_NONE,
    BATTLE_COM_S_CHARGE,
    BATTLE_COM_S_CHARGE_OK,
    BATTLE_COM_S_EARTHROUND0,
    BATTLE_COM_S_EARTHROUND1,
    BATTLE_COM_S_RENZOKU,
    BATTLE_COM_S_GBREAK,
    BATTLE_COM_S_GUARDIAN_ATTACK,
    BATTLE_COM_S_MIGHTY,
    BATTLE_COM_S_NOGUARD,
    BATTLE_COM_S_POWERBALANCE,
    BATTLE_COM_S_STATUSCHANGE,
    BATTLE_COM_S_ABDUCT,
    BATTLE_COM_S_STEAL,
    BATTLE_COM_S_ATTACK_MAGIC,
    BATTLE_COM_WAIT,
    BattleCombatProfile,
    battle_command3_low,
    BattleCommand,
    ContinuationAttackRolls,
    AttackCrazedRolls,
    WildViolentRolls,
    CounterAttemptRolls,
    OrdinaryAttackRolls,
    OrdinaryCaptureContext,
    OrdinaryCaptureRolls,
    OrdinaryAbductRolls,
    OrdinaryStealRolls,
    OrdinaryEscapeContext,
    OrdinaryEscapeRolls,
)
from tools.stoneage_battle_status_model import (
    BaseStatusCombatProfile,
    STATUS_POISON,
)
from tools.stoneage_attack_magic_action_model import (
    AttackMagicTargetRolls,
    EnemyAttackMagicActionRolls,
)
from tools.stoneage_attack_magic_state_model import (
    AttackMagicResistanceRuntime,
    AttackMagicRoundOverlay,
)
from tools.stoneage_enemy_rehp_model import EnemyReHpRolls
from tools.stoneage_enemy_relife_model import EnemyReLifeRolls
from tools.stoneage_nocast_runtime_state import (
    NocastActionRolls,
    NocastParticipantRuntime,
    NocastRoundOverlay,
)
import tools.stoneage_enemy_ai_combined_bridge as combined_bridge
import tools.stoneage_enemy_ai_vary_bridge as vary_bridge
from tools.stoneage_combined_direct_magic_model import RuntimeItemZeroWitness
from tools.stoneage_combined_initiative_model import PROFILE_GAVIN_IRIS_30PCT
from tools.stoneage_combined_runtime_state import (
    CombinedActionRolls,
    CombinedRuntimeOverlay,
    STATUS_MAGIC_PROFILE_IRIS_CP950,
)
from tools.stoneage_vary_runtime_state import (
    PROFILE_GAVIN_IRIS_ATTACK_QUICK,
)
from tools.stoneage_barrier_runtime_state import BarrierActionRolls
from tools.stoneage_recovered25_attack_magic_runtime import (
    Recovered25AttackMagicEntry,
    Recovered25AttackMagicRuntime,
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
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillEntry,
    Recovered25PetSkillRuntime,
)
from tools.stoneage_enemy_ai_wildviolent_bridge import (
    EnemyAiWildViolentSubmission,
)
from tools.stoneage_wildviolent_model import (
    CALLBACK_NAME as WILDVIOLENT_CALLBACK,
    resolve_wildviolent_setup,
)
from tools.stoneage_local_runtime_session_coordinator import (
    InMemoryLocalPersistenceStore,
    LocalRuntimeSessionCoordinator,
)
from tools.stoneage_singleplayer_battle import BattleOutcome
from tools.stoneage_singleplayer_persistence import decode_persistent_state
from tools.stoneage_pet_growth_model import (
    PetLevelGrowthRolls,
    pack_growth_base,
)
from tools.stoneage_singleplayer_domain import (
    EncounterRolls,
    EnemyVariantId,
    HistoricalStaticData,
    InventoryItem,
    InventorySlot,
    ItemTemplateId,
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
            "TACTICSOPTION": (
                "at:1;1;1|gu:1|es:0|wa:0;0;0;0;0;0;0"
            ),
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
                "RARE": 0,
                "PETSKILL1": 10,
                "PETSKILL2": 20,
                "PETSKILL3": 30,
                "PETSKILL4": 40,
                "PETSKILL5": 50,
                "PETSKILL6": 60,
                "PETSKILL7": 70,
                "EARTHAT": 50,
                "WATERAT": 50,
                "FIREAT": 0,
                "WINDAT": 0,
                "SLOT": 4,
                "SIZE": 0,
            }
        )
        self.enemybase_runtime = SimpleNamespace(templates={88: template})
        self.petskill_runtime = Recovered25PetSkillRuntime(
            skills={
                10: Recovered25PetSkillEntry(
                    skill_id=10,
                    field=1,
                    target=3,
                    cost=2,
                    illegal=0,
                    function_name="PETSKILL_NormalAttack",
                    option_bytes=b"",
                ),
                20: Recovered25PetSkillEntry(
                    skill_id=20,
                    field=1,
                    target=3,
                    cost=2,
                    illegal=0,
                    function_name="PETSKILL_NormalGuard",
                    option_bytes=b"",
                ),
                30: Recovered25PetSkillEntry(
                    skill_id=30,
                    field=1,
                    target=3,
                    cost=2,
                    illegal=0,
                    function_name="PETSKILL_None",
                    option_bytes=b"",
                ),
                40: Recovered25PetSkillEntry(
                    skill_id=40,
                    field=1,
                    target=3,
                    cost=2,
                    illegal=0,
                    function_name="PETSKILL_StatusChange",
                    option_bytes="毒turn4 攻%25".encode("cp950"),
                ),
                50: Recovered25PetSkillEntry(
                    skill_id=50,
                    field=1,
                    target=3,
                    cost=2,
                    illegal=0,
                    function_name="PETSKILL_PowerBalance",
                    option_bytes="攻%25 防%-35".encode("cp950"),
                ),
                60: Recovered25PetSkillEntry(
                    skill_id=60,
                    field=1,
                    target=3,
                    cost=2,
                    illegal=0,
                    function_name="PETSKILL_Mighty",
                    option_bytes="倍2 回避30".encode("cp950"),
                ),
                70: Recovered25PetSkillEntry(
                    skill_id=70,
                    field=1,
                    target=3,
                    cost=2,
                    illegal=0,
                    function_name="PETSKILL_GuardBreak",
                    option_bytes=b"ascii-only-option",
                ),
                80: Recovered25PetSkillEntry(
                    skill_id=80,
                    field=1,
                    target=3,
                    cost=2,
                    illegal=0,
                    function_name="PETSKILL_ChargeAttack",
                    option_bytes="2 攻%150".encode("cp950"),
                ),
                90: Recovered25PetSkillEntry(
                    skill_id=90,
                    field=1,
                    target=3,
                    cost=2,
                    illegal=0,
                    function_name="PETSKILL_NoGuard",
                    option_bytes="避%40 擊%60 心%30".encode("cp950"),
                ),
                100: Recovered25PetSkillEntry(
                    skill_id=100,
                    field=1,
                    target=3,
                    cost=2,
                    illegal=0,
                    function_name="PETSKILL_ContinuationAttack",
                    option_bytes=b"3",
                ),
                110: Recovered25PetSkillEntry(
                    skill_id=110,
                    field=1,
                    target=3,
                    cost=2,
                    illegal=0,
                    function_name="PETSKILL_Abduct",
                    option_bytes=b"80 partner",
                ),
                111: Recovered25PetSkillEntry(
                    skill_id=111,
                    field=1,
                    target=3,
                    cost=2,
                    illegal=0,
                    function_name="PETSKILL_Abduct",
                    option_bytes=b"partner",
                ),
                120: Recovered25PetSkillEntry(
                    skill_id=120,
                    field=1,
                    target=3,
                    cost=2,
                    illegal=0,
                    function_name="PETSKILL_EarthRound",
                    option_bytes="攻%90".encode("cp950"),
                ),
                130: Recovered25PetSkillEntry(
                    skill_id=130,
                    field=1,
                    target=3,
                    cost=2,
                    illegal=0,
                    function_name="PETSKILL_Steal",
                    option_bytes=b"",
                ),
                140: Recovered25PetSkillEntry(
                    skill_id=140,
                    field=1,
                    target=3,
                    cost=2,
                    illegal=0,
                    function_name="PETSKILL_Guardian",
                    option_bytes="攻%-20".encode("cp950"),
                ),
                150: Recovered25PetSkillEntry(
                    skill_id=150,
                    field=2,
                    target=3,
                    cost=2,
                    illegal=1,
                    function_name="PETSKILL_Merge",
                    option_bytes=b"",
                ),
                151: Recovered25PetSkillEntry(
                    skill_id=151,
                    field=2,
                    target=3,
                    cost=2,
                    illegal=1,
                    function_name="PETSKILL_Merge",
                    option_bytes=b"",
                ),
                160: Recovered25PetSkillEntry(
                    skill_id=160,
                    field=1,
                    target=3,
                    cost=2,
                    illegal=0,
                    function_name="PETSKILL_AttackMagic",
                    option_bytes=b"magic=301 item=19647",
                ),
            },
            source_file="petskill.txt",
        )

        center=(
            (0,0,0,0,0),
            (0,0,1,0,0),
            (0,0,0,0,0),
        )
        attack_entries={}
        for offset,magic_id in enumerate(range(301,326)):
            skill_id=(160 if magic_id==301 else 1000+magic_id)
            attack_entries[skill_id]=Recovered25AttackMagicEntry(
                skill_id=skill_id,
                magic_id=magic_id,
                item_config_id=19647+offset,
                item_magicusemp=5,
                magic_idx=2+offset,
                element=0,
                power=(3000 if magic_id==301 else 100),
                magic_level=1,
                attacker_side1_matrix=center,
                attacker_side0_matrix=center,
            )
        self.attack_magic_runtime=Recovered25AttackMagicRuntime(
            entries=attack_entries,
            itemset_file="itemset.txt",
        )

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

        with self.assertRaisesRegex(ValueError, "ATTACK/GUARD/WAIT only"):
            self.coordinator.resolve_persistent_attack_wait_round(
                context,
                commands={
                    "player": BattleCommand(BATTLE_COM_ESCAPE),
                    enemy_id: BattleCommand(BATTLE_COM_WAIT),
                },
                initiative_random_subtracts=initiative,
                profiles=profiles,
                attack_rolls=attack_rolls,
                defense_profile="newpower_70pct",
            )

    def test_recovered_enemy_ai_builds_attack_and_guard_from_spawn_variant(self):
        session = LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1, 0, 0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-command"}),
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

        attack = self.coordinator.build_persistent_enemy_attack_guard_commands(
            context,
            mode_rolls_by_enemy_id={enemy_id: 0},
            target_rolls_by_enemy_id={enemy_id: 0},
        )
        self.assertEqual(set(attack), {enemy_id})
        self.assertEqual(attack[enemy_id].command1, BATTLE_COM_ATTACK)
        self.assertEqual(attack[enemy_id].command2, 0)

        guard = self.coordinator.build_persistent_enemy_attack_guard_commands(
            context,
            mode_rolls_by_enemy_id={enemy_id: 1},
        )
        self.assertEqual(guard[enemy_id].command1, BATTLE_COM_GUARD)
        self.assertEqual(guard[enemy_id].command2, -1)

    def test_recovered_enemy_ai_guard_executes_through_persistent_round(self):
        session = LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1, 0, 0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-guard-round"}),
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
        result_context, round_result = (
            self.coordinator
            .resolve_persistent_attack_guard_wait_round_with_enemy_ai(
                context,
                player_side_commands={
                    "player": BattleCommand(
                        BATTLE_COM_ATTACK,
                        command2=10,
                    )
                },
                enemy_mode_rolls={enemy_id: 1},
                enemy_target_rolls=None,
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
                        guard_roll_1_100=1,
                        minimum_damage_roll_0_1=1,
                    )
                },
                defense_profile="newpower_70pct",
            )
        )
        self.assertEqual(round_result.after.turn, 1)
        self.assertEqual(
            round_result.after.last_commands[enemy_id].command1,
            BATTLE_COM_GUARD,
        )
        self.assertGreater(
            round_result.after.hp_by_participant_id[enemy_id],
            0,
        )
        self.assertLess(
            round_result.after.hp_by_participant_id[enemy_id],
            1000,
        )
        self.assertEqual(
            result_context.persistent_battle_state,
            round_result.after,
        )

    def test_recovered_enemy_ai_fails_closed_on_skill_selection(self):
        session = LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1, 0, 0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-fail-closed"}),
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
        skill_variant = replace(
            context.spawned_enemies[0].variant,
            tactics_option="at:0;1;1|gu:0|es:0|wa:1",
        )
        context = replace(
            context,
            spawned_enemies=(
                replace(
                    context.spawned_enemies[0],
                    variant=skill_variant,
                ),
            ),
        )
        context = self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player": 0, enemy_id: 10},
        )
        with self.assertRaisesRegex(
            ValueError,
            "outside coordinator ATTACK/GUARD subset",
        ):
            self.coordinator.build_persistent_enemy_attack_guard_commands(
                context,
                mode_rolls_by_enemy_id={enemy_id: 0},
                target_rolls_by_enemy_id={enemy_id: 0},
            )

    def test_recovered_enemy_ai_wa_resolves_exact_skill_slots(self):
        session = LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1, 0, 0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-wa"}),
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

        attack_context = replace(
            context,
            spawned_enemies=(
                replace(
                    context.spawned_enemies[0],
                    variant=replace(
                        context.spawned_enemies[0].variant,
                        tactics_option=(
                            "at:0;1;1|gu:0|es:0|"
                            "wa:1;0;0;0;0;0;0"
                        ),
                    ),
                ),
            ),
        )
        attack = self.coordinator.build_persistent_enemy_common_commands(
            attack_context,
            mode_rolls_by_enemy_id={enemy_id: 0},
            target_rolls_by_enemy_id={enemy_id: 0},
            allow_escape=True,
            allow_basic_skill=True,
        )
        self.assertEqual(attack[enemy_id].command1, BATTLE_COM_ATTACK)
        self.assertEqual(attack[enemy_id].command2, 0)

        guard_context = replace(
            context,
            spawned_enemies=(
                replace(
                    context.spawned_enemies[0],
                    variant=replace(
                        context.spawned_enemies[0].variant,
                        tactics_option=(
                            "at:0;1;1|gu:0|es:0|"
                            "wa:0;1;0;0;0;0;0"
                        ),
                    ),
                ),
            ),
        )
        guard = self.coordinator.build_persistent_enemy_common_commands(
            guard_context,
            mode_rolls_by_enemy_id={enemy_id: 0},
            target_rolls_by_enemy_id={enemy_id: 0},
            allow_escape=True,
            allow_basic_skill=True,
        )
        self.assertEqual(guard[enemy_id].command1, BATTLE_COM_GUARD)
        self.assertEqual(guard[enemy_id].command2, 0)

        none_context = replace(
            context,
            spawned_enemies=(
                replace(
                    context.spawned_enemies[0],
                    variant=replace(
                        context.spawned_enemies[0].variant,
                        tactics_option=(
                            "at:0;1;1|gu:0|es:0|"
                            "wa:0;0;1;0;0;0;0"
                        ),
                    ),
                ),
            ),
        )
        none = self.coordinator.build_persistent_enemy_common_commands(
            none_context,
            mode_rolls_by_enemy_id={enemy_id: 0},
            target_rolls_by_enemy_id={enemy_id: 0},
            allow_escape=True,
            allow_basic_skill=True,
        )
        self.assertEqual(none[enemy_id].command1, BATTLE_COM_NONE)
        self.assertEqual(none[enemy_id].command2, 0)

    def test_recovered_enemy_ai_statuschange_executes_through_persistent_round(self):
        session = LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1, 0, 0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-statuschange"}),
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
        context = replace(
            context,
            battle=replace(
                context.battle,
                player=replace(
                    context.battle.player,
                    defense=0,
                    quick=10,
                ),
                enemies=(
                    replace(
                        context.battle.enemies[0],
                        quick=200,
                    ),
                ),
            ),
            spawned_enemies=(
                replace(
                    context.spawned_enemies[0],
                    variant=replace(
                        context.spawned_enemies[0].variant,
                        tactics_option=(
                            "at:0;1;1|gu:0|es:0|"
                            "wa:0;0;0;1;0;0;0"
                        ),
                    ),
                ),
            ),
        )
        context = self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player": 0, enemy_id: 10},
        )

        result_context, round_result = (
            self.coordinator
            .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                context,
                player_side_commands={
                    "player": BattleCommand(BATTLE_COM_WAIT),
                },
                enemy_mode_rolls={enemy_id: 0},
                enemy_target_rolls={enemy_id: 0},
                enemy_escape_rolls={},
                opponent_abio_by_participant_id={},
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
                        fixed_luck=10,
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
                    ),
                },
                base_status_combat_profiles_by_participant_id={
                    "player": BaseStatusCombatProfile(
                        vital=25,
                        strength=25,
                        tough=25,
                        dex=25,
                        resistance_by_status={STATUS_POISON: 0},
                    ),
                },
                status_application_rolls_by_attack_id={
                    enemy_id: 1,
                },
                defense_profile="newpower_70pct",
            )
        )
        enemy_event = next(
            event
            for event in round_result.round.events
            if event.participant_id == enemy_id
        )
        self.assertEqual(enemy_event.command1, BATTLE_COM_S_STATUSCHANGE)
        self.assertGreater(enemy_event.damage, 0)
        self.assertIsNotNone(enemy_event.status_application_resolution)
        self.assertTrue(
            enemy_event.status_application_resolution.check.success
        )
        self.assertEqual(
            enemy_event.status_application_resolution.turn_written,
            5,
        )
        self.assertEqual(
            round_result.after
            .base_status_runtime_by_participant_id["player"]
            .status.poison,
            4,
        )
        self.assertEqual(
            result_context.persistent_battle_state.turn,
            context.persistent_battle_state.turn + 1,
        )
        self.assertEqual(
            context.persistent_battle_state
            .base_status_runtime_by_participant_id["player"]
            .status.poison,
            0,
        )

    def test_recovered_enemy_ai_continuationattack_requires_and_executes_hit_rng(self):
        session = LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1, 0, 0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-continuationattack"}),
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
        enemy_id=context.battle.enemies[0].participant_id
        spawned=context.spawned_enemies[0]
        continuation_template=replace(
            spawned.template,
            skill_ids=(100,20,30,40,50,60,70),
            skill_slot_ids=(100,20,30,40,50,60,70),
        )
        context=replace(
            context,
            battle=replace(
                context.battle,
                player=replace(
                    context.battle.player,
                    defense=0,
                    quick=10,
                ),
                enemies=(
                    replace(
                        context.battle.enemies[0],
                        quick=100,
                    ),
                ),
            ),
            spawned_enemies=(
                replace(
                    spawned,
                    template=continuation_template,
                    variant=replace(
                        spawned.variant,
                        tactics_option=(
                            "at:0;1;1|gu:0|es:0|"
                            "wa:1;0;0;0;0;0;0"
                        ),
                    ),
                ),
            ),
        )
        context=self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player":0,enemy_id:10},
        )
        profiles={
            "player":BattleCombatProfile(
                fixed_dex=10,
                fixed_luck=0,
                earth=0,
                water=0,
                fire=0,
                wind=0,
            ),
            enemy_id:BattleCombatProfile(
                fixed_dex=200,
                fixed_luck=0,
                earth=0,
                water=0,
                fire=0,
                wind=0,
            ),
        }
        base_kwargs=dict(
            player_side_commands={
                "player":BattleCommand(BATTLE_COM_WAIT),
            },
            enemy_mode_rolls={enemy_id:0},
            enemy_target_rolls={enemy_id:0},
            enemy_escape_rolls={},
            opponent_abio_by_participant_id={},
            initiative_random_subtracts={
                "player":0,
                enemy_id:0,
            },
            profiles=profiles,
            attack_rolls={},
            defense_profile="newpower_70pct",
        )

        with self.assertRaisesRegex(
            ValueError,
            "ContinuationAttack RNG mismatch",
        ):
            (
                self.coordinator
                .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                    context,
                    **base_kwargs,
                )
            )

        hit=OrdinaryAttackRolls(
            dodge_roll_1_10000=10000,
            critical_roll_1_10000=10000,
            damage_roll=0,
        )
        before_hp=(
            context.persistent_battle_state
            .hp_by_participant_id["player"]
        )
        result_context,round_result=(
            self.coordinator
            .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                context,
                continuation_rolls_by_attack_id={
                    enemy_id:ContinuationAttackRolls((hit,hit,hit)),
                },
                **base_kwargs,
            )
        )
        enemy_hits=[
            event
            for event in round_result.round.events
            if (
                event.participant_id==enemy_id
                and event.command1==BATTLE_COM_S_RENZOKU
                and not event.is_counter
            )
        ]
        self.assertEqual(len(enemy_hits),3)
        self.assertTrue(all(event.damage>0 for event in enemy_hits))
        self.assertLess(
            result_context.persistent_battle_state
            .hp_by_participant_id["player"],
            before_hp,
        )
        self.assertEqual(
            result_context.persistent_battle_state.turn,
            context.persistent_battle_state.turn+1,
        )

    def test_recovered_enemy_ai_noguard_preserves_same_round_dodge_state(self):
        session = LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1, 0, 0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-noguard"}),
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
        enemy_id=context.battle.enemies[0].participant_id
        spawned=context.spawned_enemies[0]
        noguard_template=replace(
            spawned.template,
            skill_ids=(90,20,30,40,50,60,70),
            skill_slot_ids=(90,20,30,40,50,60,70),
        )
        context=replace(
            context,
            battle=replace(
                context.battle,
                player=replace(context.battle.player,quick=200),
                enemies=(replace(context.battle.enemies[0],quick=20),),
            ),
            spawned_enemies=(
                replace(
                    spawned,
                    template=noguard_template,
                    variant=replace(
                        spawned.variant,
                        tactics_option=(
                            "at:0;1;1|gu:0|es:0|"
                            "wa:1;0;0;0;0;0;0"
                        ),
                    ),
                ),
            ),
        )
        context=self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player":0,enemy_id:10},
        )

        result_context,round_result=(
            self.coordinator
            .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                context,
                player_side_commands={
                    "player":BattleCommand(BATTLE_COM_ATTACK,command2=10),
                },
                enemy_mode_rolls={enemy_id:0},
                enemy_target_rolls={enemy_id:0},
                enemy_escape_rolls={},
                opponent_abio_by_participant_id={},
                initiative_random_subtracts={
                    "player":0,
                    enemy_id:0,
                },
                profiles={
                    "player":BattleCombatProfile(
                        fixed_dex=1000,
                        fixed_luck=0,
                        earth=0,
                        water=0,
                        fire=0,
                        wind=0,
                    ),
                    enemy_id:BattleCombatProfile(
                        fixed_dex=1,
                        fixed_luck=0,
                        earth=0,
                        water=0,
                        fire=0,
                        wind=0,
                    ),
                },
                attack_rolls={
                    "player":OrdinaryAttackRolls(
                        dodge_roll_1_10000=2000,
                        critical_roll_1_10000=10000,
                        damage_roll=0,
                    ),
                },
                counter_rolls_by_attack_id={
                    "player":(
                        CounterAttemptRolls(
                            counter_check_roll_1_10000=10000,
                        ),
                    ),
                },
                defense_profile="newpower_70pct",
            )
        )
        player_attack=next(
            event for event in round_result.round.events
            if event.participant_id=="player" and not event.is_counter
        )
        enemy_own=next(
            event for event in round_result.round.events
            if event.participant_id==enemy_id and not event.is_counter
        )
        self.assertEqual(player_attack.result,"dodge")
        self.assertEqual(enemy_own.command1,BATTLE_COM_S_NOGUARD)
        self.assertEqual(enemy_own.result,"noguard_no_action")
        self.assertEqual(
            result_context.persistent_battle_state.turn,
            context.persistent_battle_state.turn+1,
        )

    def test_recovered_enemy_ai_chargeattack_carries_then_fires_without_reroll(self):
        session = LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1, 0, 0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-chargeattack"}),
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
        spawned = context.spawned_enemies[0]
        charge_template = replace(
            spawned.template,
            skill_ids=(80, 20, 30, 40, 50, 60, 70),
            skill_slot_ids=(80, 20, 30, 40, 50, 60, 70),
        )
        context = replace(
            context,
            battle=replace(
                context.battle,
                player=replace(
                    context.battle.player,
                    defense=0,
                    quick=10,
                ),
                enemies=(
                    replace(
                        context.battle.enemies[0],
                        quick=200,
                    ),
                ),
            ),
            spawned_enemies=(
                replace(
                    spawned,
                    template=charge_template,
                    variant=replace(
                        spawned.variant,
                        tactics_option=(
                            "at:0;1;1|gu:0|es:0|"
                            "wa:1;0;0;0;0;0;0"
                        ),
                    ),
                ),
            ),
        )
        context = self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player": 0, enemy_id: 10},
        )
        profiles = {
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
                fixed_luck=10,
                earth=0,
                water=0,
                fire=0,
                wind=0,
            ),
        }

        first_context, first = (
            self.coordinator
            .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                context,
                player_side_commands={
                    "player": BattleCommand(BATTLE_COM_WAIT),
                },
                enemy_mode_rolls={enemy_id: 0},
                enemy_target_rolls={enemy_id: 0},
                enemy_escape_rolls={},
                opponent_abio_by_participant_id={},
                initiative_random_subtracts={
                    "player": 0,
                    enemy_id: 0,
                },
                profiles=profiles,
                attack_rolls={},
                defense_profile="newpower_70pct",
            )
        )
        first_event = next(
            event for event in first.round.events
            if event.participant_id == enemy_id
        )
        self.assertEqual(first_event.command1, BATTLE_COM_S_CHARGE)
        self.assertEqual(first_event.result, "charge_wait")
        carried = (
            first_context.persistent_battle_state
            .carried_commands_by_participant_id[enemy_id]
        )
        self.assertEqual(carried.command1, BATTLE_COM_S_CHARGE)
        self.assertEqual(battle_command3_low(carried.command3), 1)

        second_context, second = (
            self.coordinator
            .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                first_context,
                player_side_commands={
                    "player": BattleCommand(BATTLE_COM_WAIT),
                },
                enemy_mode_rolls={},
                enemy_target_rolls={},
                enemy_escape_rolls={},
                opponent_abio_by_participant_id={},
                initiative_random_subtracts={
                    "player": 0,
                    enemy_id: 0,
                },
                profiles=profiles,
                attack_rolls={},
                defense_profile="newpower_70pct",
            )
        )
        second_event = next(
            event for event in second.round.events
            if event.participant_id == enemy_id
        )
        self.assertEqual(second_event.result, "charge_wait")
        carried = (
            second_context.persistent_battle_state
            .carried_commands_by_participant_id[enemy_id]
        )
        self.assertEqual(battle_command3_low(carried.command3), 0)

        hp_before = (
            second_context.persistent_battle_state
            .hp_by_participant_id["player"]
        )
        third_context, third = (
            self.coordinator
            .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                second_context,
                player_side_commands={
                    "player": BattleCommand(BATTLE_COM_WAIT),
                },
                enemy_mode_rolls={},
                enemy_target_rolls={},
                enemy_escape_rolls={},
                opponent_abio_by_participant_id={},
                initiative_random_subtracts={
                    "player": 0,
                    enemy_id: 0,
                },
                profiles=profiles,
                attack_rolls={
                    enemy_id: OrdinaryAttackRolls(
                        dodge_roll_1_10000=10000,
                        critical_roll_1_10000=10000,
                        damage_roll=0,
                        minimum_damage_roll_0_1=1,
                    ),
                },
                defense_profile="newpower_70pct",
            )
        )
        third_event = next(
            event for event in third.round.events
            if event.participant_id == enemy_id
        )
        self.assertEqual(third_event.command1, BATTLE_COM_S_CHARGE_OK)
        self.assertGreater(third_event.damage, 0)
        self.assertLess(
            third_context.persistent_battle_state
            .hp_by_participant_id["player"],
            hp_before,
        )
        self.assertEqual(
            dict(
                third_context.persistent_battle_state
                .carried_commands_by_participant_id
            ),
            {},
        )

    def test_recovered_enemy_ai_earthround_carries_then_fires_without_reroll(self):
        session = LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1, 0, 0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-earthround"}),
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
        spawned = context.spawned_enemies[0]
        earth_template = replace(
            spawned.template,
            skill_ids=(10, 20, 30, 40, 50, 60, 120),
            skill_slot_ids=(10, 20, 30, 40, 50, 60, 120),
        )
        context = replace(
            context,
            battle=replace(
                context.battle,
                player=replace(
                    context.battle.player,
                    hp=1000,
                    max_hp=1000,
                    defense=0,
                    quick=10,
                ),
                enemies=(
                    replace(
                        context.battle.enemies[0],
                        quick=200,
                    ),
                ),
            ),
            spawned_enemies=(
                replace(
                    spawned,
                    template=earth_template,
                    variant=replace(
                        spawned.variant,
                        tactics_option=(
                            "at:0;1;1|gu:0|es:0|"
                            "wa:0;0;0;0;0;0;1"
                        ),
                    ),
                ),
            ),
        )
        context = self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player": 0, enemy_id: 10},
        )
        profiles = {
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
                fixed_luck=10,
                earth=0,
                water=0,
                fire=0,
                wind=0,
            ),
        }

        first_context, first = (
            self.coordinator
            .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                context,
                player_side_commands={
                    "player": BattleCommand(BATTLE_COM_WAIT),
                },
                enemy_mode_rolls={enemy_id: 0},
                enemy_target_rolls={enemy_id: 0},
                enemy_escape_rolls={},
                opponent_abio_by_participant_id={},
                initiative_random_subtracts={
                    "player": 0,
                    enemy_id: 0,
                },
                profiles=profiles,
                attack_rolls={},
                defense_profile="newpower_70pct",
            )
        )
        first_event = next(
            event for event in first.round.events
            if event.participant_id == enemy_id
        )
        self.assertEqual(
            first_event.command1,
            BATTLE_COM_S_EARTHROUND1,
        )
        self.assertEqual(first_event.result, "earthround_hide")
        self.assertEqual(
            first_context.persistent_battle_state
            .hp_by_participant_id["player"],
            1000,
        )
        carried = (
            first_context.persistent_battle_state
            .carried_commands_by_participant_id[enemy_id]
        )
        self.assertEqual(carried.command1, BATTLE_COM_S_EARTHROUND0)
        self.assertEqual(carried.command3, 90)

        hp_before = (
            first_context.persistent_battle_state
            .hp_by_participant_id["player"]
        )
        second_context, second = (
            self.coordinator
            .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                first_context,
                player_side_commands={
                    "player": BattleCommand(BATTLE_COM_WAIT),
                },
                # Fixed BATTLE_AllCharaCWaitSet preserves EARTHROUND0,
                # so phase two must not consume a new AI mode/target roll.
                enemy_mode_rolls={},
                enemy_target_rolls={},
                enemy_escape_rolls={},
                opponent_abio_by_participant_id={},
                initiative_random_subtracts={
                    "player": 0,
                    enemy_id: 0,
                },
                profiles=profiles,
                attack_rolls={
                    enemy_id: OrdinaryAttackRolls(
                        dodge_roll_1_10000=10000,
                        critical_roll_1_10000=10000,
                        damage_roll=0,
                        minimum_damage_roll_0_1=1,
                    ),
                },
                defense_profile="newpower_70pct",
            )
        )
        second_event = next(
            event for event in second.round.events
            if event.participant_id == enemy_id
        )
        self.assertEqual(
            second_event.command1,
            BATTLE_COM_S_EARTHROUND0,
        )
        self.assertGreater(second_event.damage, 0)
        self.assertLess(
            second_context.persistent_battle_state
            .hp_by_participant_id["player"],
            hp_before,
        )
        self.assertEqual(
            dict(
                second_context.persistent_battle_state
                .carried_commands_by_participant_id
            ),
            {},
        )

    def test_recovered_enemy_ai_attackmagic_executes_and_carries_overlay(self):
        session=LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1,0,0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-attackmagic"}),
        )
        group=self.stack.request_encounter_group(session,group_roll=0)
        context=self.coordinator.start_group_battle(
            session,
            group,
            entry_count_roll=1,
            selection_rolls=(0,),
            birth_rolls=(
                EnemyBirthRolls(
                    level_roll=1,
                    birth_offsets=(0,0,0,0),
                    spawn_allocation_rolls=(0,1,2,3,0,1,2,3,0,1),
                ),
            ),
        )
        enemy_id=context.battle.enemies[0].participant_id
        spawned=context.spawned_enemies[0]
        context=replace(
            context,
            battle=replace(
                context.battle,
                player=replace(
                    context.battle.player,
                    hp=1000,max_hp=1000,quick=10,
                ),
                enemies=(
                    replace(context.battle.enemies[0],quick=200,level=56),
                ),
            ),
            spawned_enemies=(
                replace(
                    spawned,
                    participant=replace(spawned.participant,quick=200,level=56),
                    template=replace(
                        spawned.template,
                        skill_ids=(160,20,30,40,50,60,70),
                        skill_slot_ids=(160,20,30,40,50,60,70),
                    ),
                    variant=replace(
                        spawned.variant,
                        tactics_option=(
                            "at:0;1;1|gu:0|es:0|"
                            "wa:1;0;0;0;0;0;0"
                        ),
                    ),
                ),
            ),
        )
        magic_overlay=AttackMagicRoundOverlay({
            "player":AttackMagicResistanceRuntime(
                levels=(20,5,0,0),
                exps=(90,1,0,0),
            )
        })
        context=self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player":0,enemy_id:15},
            attack_magic_overlay=magic_overlay,
        )
        profiles={
            "player":BattleCombatProfile(
                fixed_dex=10,fixed_luck=0,
                earth=0,water=100,fire=0,wind=0,
            ),
            enemy_id:BattleCombatProfile(
                fixed_dex=200,fixed_luck=0,
                earth=100,water=0,fire=0,wind=0,
            ),
        }
        next_context,result=(
            self.coordinator
            .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                context,
                player_side_commands={
                    "player":BattleCommand(BATTLE_COM_WAIT),
                },
                enemy_mode_rolls={enemy_id:0},
                enemy_target_rolls={enemy_id:0},
                enemy_escape_rolls={},
                opponent_abio_by_participant_id={},
                initiative_random_subtracts={"player":0,enemy_id:0},
                profiles=profiles,
                attack_rolls={},
                defense_profile="newpower_70pct",
                attack_magic_rolls_by_attack_id={
                    enemy_id:EnemyAttackMagicActionRolls(
                        0,{0:AttackMagicTargetRolls(100,0)}
                    )
                },
            )
        )
        event=next(
            event for event in result.round.events
            if event.participant_id==enemy_id
            and event.command1==BATTLE_COM_S_ATTACK_MAGIC
        )
        self.assertEqual(event.result,"attackmagic_hit")
        self.assertEqual(result.after.result,"defeat")
        self.assertIsNotNone(next_context.attack_magic_overlay)
        trained=next_context.attack_magic_overlay.resistance_by_participant_id[
            "player"
        ]
        self.assertEqual(trained.levels[:2],(21,4))
        self.assertEqual(
            result.attack_magic_overlay_after,
            next_context.attack_magic_overlay,
        )

    def test_recovered_enemy_ai_attackmagic_requires_explicit_overlay(self):
        session=LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1,0,0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-attackmagic-no-overlay"}),
        )
        group=self.stack.request_encounter_group(session,group_roll=0)
        context=self.coordinator.start_group_battle(
            session,group,
            entry_count_roll=1,
            selection_rolls=(0,),
            birth_rolls=(
                EnemyBirthRolls(
                    level_roll=1,
                    birth_offsets=(0,0,0,0),
                    spawn_allocation_rolls=(0,1,2,3,0,1,2,3,0,1),
                ),
            ),
        )
        enemy_id=context.battle.enemies[0].participant_id
        spawned=context.spawned_enemies[0]
        context=replace(
            context,
            spawned_enemies=(
                replace(
                    spawned,
                    template=replace(
                        spawned.template,
                        skill_ids=(160,20,30,40,50,60,70),
                        skill_slot_ids=(160,20,30,40,50,60,70),
                    ),
                    variant=replace(
                        spawned.variant,
                        tactics_option=(
                            "at:0;1;1|gu:0|es:0|"
                            "wa:1;0;0;0;0;0;0"
                        ),
                    ),
                ),
            ),
        )
        context=self.coordinator.begin_persistent_group_battle(
            context,slots={"player":0,enemy_id:15}
        )
        with self.assertRaisesRegex(ValueError,"explicit battle overlay"):
            (
                self.coordinator
                .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                    context,
                    player_side_commands={
                        "player":BattleCommand(BATTLE_COM_WAIT),
                    },
                    enemy_mode_rolls={enemy_id:0},
                    enemy_target_rolls={enemy_id:0},
                    enemy_escape_rolls={},
                    opponent_abio_by_participant_id={},
                    initiative_random_subtracts={"player":0,enemy_id:0},
                    profiles={
                        "player":BattleCombatProfile(
                            fixed_dex=10,fixed_luck=0,
                            earth=0,water=100,fire=0,wind=0,
                        ),
                        enemy_id:BattleCombatProfile(
                            fixed_dex=20,fixed_luck=0,
                            earth=100,water=0,fire=0,wind=0,
                        ),
                    },
                    attack_rolls={},
                    defense_profile="newpower_70pct",
                )
            )

    def test_recovered_enemy_ai_merge_is_fail_closed_before_round_execution(self):
        session=LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1,0,0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-merge-ub"}),
        )
        group=self.stack.request_encounter_group(session,group_roll=0)
        context=self.coordinator.start_group_battle(
            session,
            group,
            entry_count_roll=1,
            selection_rolls=(0,),
            birth_rolls=(
                EnemyBirthRolls(
                    level_roll=1,
                    birth_offsets=(0,0,0,0),
                    spawn_allocation_rolls=(0,1,2,3,0,1,2,3,0,1),
                ),
            ),
        )
        enemy_id=context.battle.enemies[0].participant_id
        spawned=context.spawned_enemies[0]
        context=replace(
            context,
            spawned_enemies=(
                replace(
                    spawned,
                    template=replace(
                        spawned.template,
                        skill_ids=(150,20,30,40,50,60,70),
                        skill_slot_ids=(150,20,30,40,50,60,70),
                    ),
                    variant=replace(
                        spawned.variant,
                        tactics_option=(
                            "at:0;1;1|gu:0|es:0|"
                            "wa:1;0;0;0;0;0;0"
                        ),
                    ),
                ),
            ),
        )
        context=self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player":0,enemy_id:10},
        )
        profiles={
            "player":BattleCombatProfile(
                fixed_dex=10,fixed_luck=0,
                earth=0,water=0,fire=0,wind=0,
            ),
            enemy_id:BattleCombatProfile(
                fixed_dex=20,fixed_luck=0,
                earth=0,water=0,fire=0,wind=0,
            ),
        }
        with self.assertRaisesRegex(
            ValueError,
            "historical undefined-return.*fail-closed",
        ):
            (
                self.coordinator
                .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                    context,
                    player_side_commands={
                        "player":BattleCommand(BATTLE_COM_WAIT),
                    },
                    enemy_mode_rolls={enemy_id:0},
                    enemy_target_rolls={enemy_id:0},
                    enemy_escape_rolls={},
                    opponent_abio_by_participant_id={},
                    initiative_random_subtracts={"player":0,enemy_id:0},
                    profiles=profiles,
                    attack_rolls={},
                    defense_profile="newpower_70pct",
                )
            )

    def test_recovered_enemy_ai_guardian_attack_uses_enemy_battle_slot(self):
        session=LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1,0,0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-guardian"}),
        )
        group=self.stack.request_encounter_group(session,group_roll=0)
        context=self.coordinator.start_group_battle(
            session,
            group,
            entry_count_roll=1,
            selection_rolls=(0,),
            birth_rolls=(
                EnemyBirthRolls(
                    level_roll=1,
                    birth_offsets=(0,0,0,0),
                    spawn_allocation_rolls=(
                        0,1,2,3,0,1,2,3,0,1
                    ),
                ),
            ),
        )
        enemy_id=context.battle.enemies[0].participant_id
        spawned=context.spawned_enemies[0]
        context=replace(
            context,
            battle=replace(
                context.battle,
                player=replace(
                    context.battle.player,
                    hp=1000,
                    max_hp=1000,
                    defense=0,
                    quick=10,
                ),
                enemies=(
                    replace(context.battle.enemies[0],quick=200),
                ),
            ),
            spawned_enemies=(
                replace(
                    spawned,
                    template=replace(
                        spawned.template,
                        skill_ids=(140,20,30,40,50,60,70),
                        skill_slot_ids=(140,20,30,40,50,60,70),
                    ),
                    variant=replace(
                        spawned.variant,
                        tactics_option=(
                            "at:0;1;1|gu:0|es:0|"
                            "wa:1;0;0;0;0;0;0"
                        ),
                    ),
                ),
            ),
        )
        context=self.coordinator.begin_persistent_group_battle(
            context,
            # Slot 15 is essential: the fixed Guardian attack branch derives
            # its protected same-side front-row slot from the actor's battle slot.
            slots={"player":0,enemy_id:15},
        )
        profiles={
            "player":BattleCombatProfile(
                fixed_dex=10,fixed_luck=0,
                earth=0,water=0,fire=0,wind=0,
            ),
            enemy_id:BattleCombatProfile(
                fixed_dex=200,fixed_luck=10,
                earth=0,water=0,fire=0,wind=0,
            ),
        }
        before_hp=context.persistent_battle_state.hp_by_participant_id["player"]
        result_context,result=(
            self.coordinator
            .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                context,
                player_side_commands={
                    "player":BattleCommand(BATTLE_COM_WAIT),
                },
                enemy_mode_rolls={enemy_id:0},
                enemy_target_rolls={enemy_id:0},
                enemy_escape_rolls={},
                opponent_abio_by_participant_id={},
                initiative_random_subtracts={"player":0,enemy_id:0},
                profiles=profiles,
                attack_rolls={
                    enemy_id:OrdinaryAttackRolls(
                        dodge_roll_1_10000=10000,
                        critical_roll_1_10000=10000,
                        damage_roll=0,
                        minimum_damage_roll_0_1=1,
                    ),
                },
                defense_profile="newpower_70pct",
            )
        )
        event=next(
            event for event in result.round.events
            if event.participant_id==enemy_id
        )
        self.assertEqual(
            event.command1,
            BATTLE_COM_S_GUARDIAN_ATTACK,
        )
        self.assertGreater(event.damage,0)
        self.assertLess(
            result_context.persistent_battle_state
            .hp_by_participant_id["player"],
            before_hp,
        )

    def test_recovered_enemy_ai_steal_gold_mutates_only_working_clone(self):
        player_state=_battle_player_state()
        fields=dict(player_state.character.fields)
        fields["gold"]=1000
        player_state.character=PlayerState(MappingProxyType(fields))
        session=LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1,0,0),
            player_state=player_state,
            world_flags=frozenset({"enemy-ai-steal-gold"}),
        )
        group=self.stack.request_encounter_group(session,group_roll=0)
        context=self.coordinator.start_group_battle(
            session,
            group,
            entry_count_roll=1,
            selection_rolls=(0,),
            birth_rolls=(
                EnemyBirthRolls(
                    level_roll=1,
                    birth_offsets=(0,0,0,0),
                    spawn_allocation_rolls=(
                        0,1,2,3,0,1,2,3,0,1
                    ),
                ),
            ),
        )
        enemy_id=context.battle.enemies[0].participant_id
        spawned=context.spawned_enemies[0]
        context=replace(
            context,
            battle=replace(
                context.battle,
                player=replace(context.battle.player,quick=10),
                enemies=(replace(context.battle.enemies[0],quick=200),),
            ),
            spawned_enemies=(
                replace(
                    spawned,
                    template=replace(
                        spawned.template,
                        skill_ids=(130,20,30,40,50,60,70),
                        skill_slot_ids=(130,20,30,40,50,60,70),
                    ),
                    variant=replace(
                        spawned.variant,
                        tactics_option=(
                            "at:0;1;1|gu:0|es:0|"
                            "wa:1;0;0;0;0;0;0"
                        ),
                    ),
                ),
            ),
        )
        context=self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player":0,enemy_id:10},
        )
        profiles={
            "player":BattleCombatProfile(
                fixed_dex=10,fixed_luck=0,
                earth=0,water=0,fire=0,wind=0,
            ),
            enemy_id:BattleCombatProfile(
                fixed_dex=100,fixed_luck=0,
                earth=0,water=0,fire=0,wind=0,
            ),
        }
        result_context,result=(
            self.coordinator
            .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                context,
                player_side_commands={
                    "player":BattleCommand(BATTLE_COM_WAIT),
                },
                enemy_mode_rolls={enemy_id:0},
                enemy_target_rolls={enemy_id:0},
                enemy_escape_rolls={},
                opponent_abio_by_participant_id={},
                initiative_random_subtracts={"player":0,enemy_id:0},
                profiles=profiles,
                attack_rolls={},
                steal_rolls_by_attack_id={
                    enemy_id:OrdinaryStealRolls(
                        success_roll_1_100=1,
                        mode_roll_1_100=1,
                        gold_percent_roll_8_12=10,
                    ),
                },
                defense_profile="newpower_70pct",
            )
        )
        event=next(
            event for event in result.round.events
            if event.participant_id==enemy_id
        )
        self.assertEqual(event.command1,BATTLE_COM_S_STEAL)
        self.assertEqual(event.result,"steal_success_gold")
        self.assertEqual(event.steal_resolution.defender_gold_loss,100)
        self.assertEqual(
            result.after.battle_exited_participant_ids,
            (enemy_id,),
        )
        self.assertEqual(result.after.result,"victory")
        payload=json.loads(result_context.working_persistent_state_payload)
        self.assertEqual(payload["character"]["gold"],900)
        self.assertEqual(session.player_state.character.fields["gold"],1000)

        settled=self.coordinator.settle_persistent_group_battle_without_level_crossing(
            result_context
        )
        self.assertEqual(settled.player_state.character.fields["gold"],900)

    def test_recovered_enemy_ai_steal_item_destroys_carried_slot_only(self):
        player_state=_battle_player_state()
        for slot_value,template_id in ((3,501),(7,502)):
            slot=InventorySlot(slot_value)
            player_state.inventory[slot]=InventoryItem(
                slot=slot,
                template_id=ItemTemplateId(template_id),
                view=MappingProxyType({"name":f"item-{template_id}"}),
            )
        session=LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1,0,0),
            player_state=player_state,
            world_flags=frozenset({"enemy-ai-steal-item"}),
        )
        group=self.stack.request_encounter_group(session,group_roll=0)
        context=self.coordinator.start_group_battle(
            session,
            group,
            entry_count_roll=1,
            selection_rolls=(0,),
            birth_rolls=(
                EnemyBirthRolls(
                    level_roll=1,
                    birth_offsets=(0,0,0,0),
                    spawn_allocation_rolls=(
                        0,1,2,3,0,1,2,3,0,1
                    ),
                ),
            ),
        )
        enemy_id=context.battle.enemies[0].participant_id
        spawned=context.spawned_enemies[0]
        context=replace(
            context,
            battle=replace(
                context.battle,
                player=replace(context.battle.player,quick=10),
                enemies=(replace(context.battle.enemies[0],quick=200),),
            ),
            spawned_enemies=(
                replace(
                    spawned,
                    template=replace(
                        spawned.template,
                        skill_ids=(130,20,30,40,50,60,70),
                        skill_slot_ids=(130,20,30,40,50,60,70),
                    ),
                    variant=replace(
                        spawned.variant,
                        tactics_option=(
                            "at:0;1;1|gu:0|es:0|"
                            "wa:1;0;0;0;0;0;0"
                        ),
                    ),
                ),
            ),
        )
        context=self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player":0,enemy_id:10},
        )
        profiles={
            "player":BattleCombatProfile(
                fixed_dex=10,fixed_luck=0,
                earth=0,water=0,fire=0,wind=0,
            ),
            enemy_id:BattleCombatProfile(
                fixed_dex=100,fixed_luck=0,
                earth=0,water=0,fire=0,wind=0,
            ),
        }
        result_context,result=(
            self.coordinator
            .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                context,
                player_side_commands={
                    "player":BattleCommand(BATTLE_COM_WAIT),
                },
                enemy_mode_rolls={enemy_id:0},
                enemy_target_rolls={enemy_id:0},
                enemy_escape_rolls={},
                opponent_abio_by_participant_id={},
                initiative_random_subtracts={"player":0,enemy_id:0},
                profiles=profiles,
                attack_rolls={},
                steal_rolls_by_attack_id={
                    enemy_id:OrdinaryStealRolls(
                        success_roll_1_100=1,
                        mode_roll_1_100=99,
                        chosen_item_ordinal=1,
                    ),
                },
                defense_profile="newpower_70pct",
            )
        )
        event=next(
            event for event in result.round.events
            if event.participant_id==enemy_id
        )
        self.assertEqual(event.result,"steal_success_item")
        self.assertEqual(event.steal_resolution.destroyed_item_slot,7)
        payload=json.loads(result_context.working_persistent_state_payload)
        self.assertEqual(
            [row["slot"] for row in payload["inventory"]],
            [3],
        )
        self.assertEqual(
            sorted(slot.value for slot in session.player_state.inventory),
            [3,7],
        )

        settled=self.coordinator.settle_persistent_group_battle_without_level_crossing(
            result_context
        )
        self.assertEqual(
            sorted(slot.value for slot in settled.player_state.inventory),
            [3],
        )

    def test_recovered_enemy_ai_guardbreak_executes_against_guard(self):
        session = LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1, 0, 0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-guardbreak"}),
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
        context = replace(
            context,
            battle=replace(
                context.battle,
                player=replace(
                    context.battle.player,
                    defense=0,
                    quick=10,
                ),
                enemies=(
                    replace(
                        context.battle.enemies[0],
                        quick=200,
                    ),
                ),
            ),
            spawned_enemies=(
                replace(
                    context.spawned_enemies[0],
                    variant=replace(
                        context.spawned_enemies[0].variant,
                        tactics_option=(
                            "at:0;1;1|gu:0|es:0|"
                            "wa:0;0;0;0;0;0;1"
                        ),
                    ),
                ),
            ),
        )
        context = self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player": 0, enemy_id: 10},
        )

        result_context, round_result = (
            self.coordinator
            .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                context,
                player_side_commands={
                    "player": BattleCommand(BATTLE_COM_GUARD),
                },
                enemy_mode_rolls={enemy_id: 0},
                enemy_target_rolls={enemy_id: 0},
                enemy_escape_rolls={},
                opponent_abio_by_participant_id={},
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
                        fixed_luck=10,
                        earth=0,
                        water=0,
                        fire=0,
                        wind=0,
                    ),
                },
                attack_rolls={
                    enemy_id: OrdinaryAttackRolls(
                        critical_roll_1_10000=10000,
                        damage_roll=0,
                        minimum_damage_roll_0_1=1,
                    ),
                },
                defense_profile="newpower_70pct",
            )
        )
        enemy_event = next(
            event
            for event in round_result.round.events
            if event.participant_id == enemy_id
        )
        self.assertEqual(enemy_event.command1, BATTLE_COM_S_GBREAK)
        self.assertGreater(enemy_event.damage, 0)
        self.assertLess(
            result_context.persistent_battle_state
            .hp_by_participant_id["player"],
            context.persistent_battle_state.hp_by_participant_id["player"],
        )

    def test_recovered_enemy_ai_mighty_executes_through_persistent_round(self):
        session = LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1, 0, 0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-mighty"}),
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
        context = replace(
            context,
            battle=replace(
                context.battle,
                player=replace(
                    context.battle.player,
                    defense=0,
                    quick=10,
                ),
                enemies=(
                    replace(
                        context.battle.enemies[0],
                        quick=200,
                    ),
                ),
            ),
            spawned_enemies=(
                replace(
                    context.spawned_enemies[0],
                    variant=replace(
                        context.spawned_enemies[0].variant,
                        tactics_option=(
                            "at:0;1;1|gu:0|es:0|"
                            "wa:0;0;0;0;0;1;0"
                        ),
                    ),
                ),
            ),
        )
        context = self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player": 0, enemy_id: 10},
        )

        result_context, round_result = (
            self.coordinator
            .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                context,
                player_side_commands={
                    "player": BattleCommand(BATTLE_COM_WAIT),
                },
                enemy_mode_rolls={enemy_id: 0},
                enemy_target_rolls={enemy_id: 0},
                enemy_escape_rolls={},
                opponent_abio_by_participant_id={},
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
                        fixed_luck=10,
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
                    ),
                },
                defense_profile="newpower_70pct",
            )
        )
        enemy_event = next(
            event
            for event in round_result.round.events
            if event.participant_id == enemy_id
        )
        self.assertEqual(enemy_event.command1, BATTLE_COM_S_MIGHTY)
        self.assertGreater(enemy_event.damage, 0)
        self.assertEqual(
            result_context.persistent_battle_state.turn,
            context.persistent_battle_state.turn + 1,
        )

    def test_recovered_enemy_ai_powerbalance_executes_through_persistent_round(self):
        session = LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1, 0, 0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-powerbalance"}),
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
        context = replace(
            context,
            battle=replace(
                context.battle,
                player=replace(
                    context.battle.player,
                    defense=0,
                    quick=10,
                ),
                enemies=(
                    replace(
                        context.battle.enemies[0],
                        quick=200,
                    ),
                ),
            ),
            spawned_enemies=(
                replace(
                    context.spawned_enemies[0],
                    variant=replace(
                        context.spawned_enemies[0].variant,
                        tactics_option=(
                            "at:0;1;1|gu:0|es:0|"
                            "wa:0;0;0;0;1;0;0"
                        ),
                    ),
                ),
            ),
        )
        context = self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player": 0, enemy_id: 10},
        )

        result_context, round_result = (
            self.coordinator
            .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                context,
                player_side_commands={
                    "player": BattleCommand(BATTLE_COM_WAIT),
                },
                enemy_mode_rolls={enemy_id: 0},
                enemy_target_rolls={enemy_id: 0},
                enemy_escape_rolls={},
                opponent_abio_by_participant_id={},
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
                        fixed_luck=10,
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
                    ),
                },
                defense_profile="newpower_70pct",
            )
        )
        enemy_event = next(
            event
            for event in round_result.round.events
            if event.participant_id == enemy_id
        )
        self.assertEqual(enemy_event.command1, BATTLE_COM_S_POWERBALANCE)
        self.assertGreater(enemy_event.damage, 0)
        self.assertEqual(
            result_context.persistent_battle_state.turn,
            context.persistent_battle_state.turn + 1,
        )

    def test_recovered_enemy_ai_statuschange_requires_explicit_eligible_status_rng(self):
        session = LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1, 0, 0),
            player_state=_battle_player_state(),
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
        context = replace(
            context,
            battle=replace(
                context.battle,
                player=replace(context.battle.player, defense=0, quick=10),
                enemies=(replace(context.battle.enemies[0], quick=200),),
            ),
            spawned_enemies=(
                replace(
                    context.spawned_enemies[0],
                    variant=replace(
                        context.spawned_enemies[0].variant,
                        tactics_option=(
                            "at:0;1;1|gu:0|es:0|"
                            "wa:0;0;0;1;0;0;0"
                        ),
                    ),
                ),
            ),
        )
        context = self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player": 0, enemy_id: 10},
        )
        with self.assertRaisesRegex(
            ValueError,
            r"eligible base status check requires RAND\(1,100\)",
        ):
            self.coordinator.resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                context,
                player_side_commands={"player": BattleCommand(BATTLE_COM_WAIT)},
                enemy_mode_rolls={enemy_id: 0},
                enemy_target_rolls={enemy_id: 0},
                enemy_escape_rolls={},
                opponent_abio_by_participant_id={},
                initiative_random_subtracts={"player": 0, enemy_id: 0},
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
                        fixed_luck=10,
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
                    ),
                },
                base_status_combat_profiles_by_participant_id={
                    "player": BaseStatusCombatProfile(
                        vital=25,
                        strength=25,
                        tough=25,
                        dex=25,
                    ),
                },
                defense_profile="newpower_70pct",
            )

    def test_recovered_enemy_ai_abduct_pet_success_persists_entry_exits(self):
        player_state=_battle_player_state()
        pet=PetActor(
            slot=PetSlot(0),
            variant_id=EnemyVariantId(701),
            template_id=PetTemplateId(89),
            runtime_object_id=None,
            state=MappingProxyType(
                {
                    "name":"abduct-target",
                    "level":5,
                    "hp":100,
                    "max_hp":100,
                    "attack":20,
                    "defense":20,
                    "quick":30,
                    "ai":79,
                    "exp":0,
                    "max_exp":500,
                }
            ),
            skills=(),
            growth=None,
        )
        player_state.pets[PetSlot(0)]=pet
        session=LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1,0,0),
            player_state=player_state,
            world_flags=frozenset({"enemy-ai-abduct"}),
        )
        group=self.stack.request_encounter_group(session,group_roll=0)
        context=self.coordinator.start_group_battle(
            session,
            group,
            entry_count_roll=1,
            selection_rolls=(0,),
            birth_rolls=(
                EnemyBirthRolls(
                    level_roll=1,
                    birth_offsets=(0,0,0,0),
                    spawn_allocation_rolls=(
                        0,1,2,3,0,1,2,3,0,1
                    ),
                ),
            ),
            allied_pet_slots=(0,),
        )
        enemy_id=context.battle.enemies[0].participant_id
        spawned=context.spawned_enemies[0]
        context=replace(
            context,
            battle=replace(
                context.battle,
                player=replace(context.battle.player,quick=10),
                enemies=(
                    replace(context.battle.enemies[0],quick=200),
                ),
            ),
            spawned_enemies=(
                replace(
                    spawned,
                    variant=replace(
                        spawned.variant,
                        tactics_option=(
                            "at:0;1;1|gu:0|es:0|"
                            "wa:0;0;0;0;0;0;1"
                        ),
                    ),
                    template=replace(
                        spawned.template,
                        skill_slot_ids=(10,20,30,40,50,60,110),
                    ),
                ),
            ),
        )
        context=self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player":0,"pet:0":1,enemy_id:10},
        )
        result_context,round_result=(
            self.coordinator
            .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                context,
                player_side_commands={
                    "player":BattleCommand(BATTLE_COM_WAIT),
                    "pet:0":BattleCommand(BATTLE_COM_WAIT),
                },
                enemy_mode_rolls={enemy_id:0},
                enemy_target_rolls={enemy_id:1},
                enemy_escape_rolls={},
                opponent_abio_by_participant_id={},
                initiative_random_subtracts={
                    "player":0,"pet:0":0,enemy_id:0,
                },
                profiles={
                    "player":BattleCombatProfile(
                        fixed_dex=10,fixed_luck=0,
                        earth=0,water=0,fire=0,wind=0,
                    ),
                    "pet:0":BattleCombatProfile(
                        fixed_dex=10,fixed_luck=0,
                        earth=0,water=0,fire=0,wind=0,
                    ),
                    enemy_id:BattleCombatProfile(
                        fixed_dex=200,fixed_luck=0,
                        earth=0,water=0,fire=0,wind=0,
                    ),
                },
                attack_rolls={},
                abduct_rolls_by_attack_id={
                    enemy_id:OrdinaryAbductRolls(
                        abduct_roll_1_100=100,
                    ),
                },
                defense_profile="newpower_70pct",
            )
        )
        event=next(
            event for event in round_result.round.events
            if event.participant_id==enemy_id
        )
        self.assertEqual(event.command1,BATTLE_COM_S_ABDUCT)
        self.assertEqual(event.result,"abduct_success")
        self.assertEqual(event.abduct_resolution.probability,200)
        terminal=round_result.after
        self.assertEqual(terminal.phase,"finished")
        self.assertEqual(terminal.result,"victory")
        self.assertEqual(
            set(terminal.battle_exited_participant_ids),
            {enemy_id,"pet:0"},
        )
        self.assertIn(enemy_id,terminal.hp_by_participant_id)
        self.assertIn("pet:0",terminal.hp_by_participant_id)
        self.assertEqual(
            tuple(x.participant_id for x in terminal.session.enemies),
            (enemy_id,),
        )
        self.assertEqual(
            tuple(x.participant_id for x in terminal.session.allied_pets),
            ("pet:0",),
        )
        self.assertEqual(terminal.pending_exp_by_participant_id["player"],0)
        self.assertEqual(
            result_context.persistent_battle_state,
            terminal,
        )

    def test_recovered_enemy_ai_escape_uses_template_rare_and_explicit_abio_rng(self):
        session = LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1, 0, 0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-escape"}),
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
        escape_variant = replace(
            context.spawned_enemies[0].variant,
            tactics_option=(
                "at:0;1;1|gu:0|es:1|wa:0;0;0;0;0;0;0"
            ),
        )
        context = replace(
            context,
            spawned_enemies=(
                replace(
                    context.spawned_enemies[0],
                    variant=escape_variant,
                ),
            ),
        )
        context = self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player": 0, enemy_id: 10},
        )

        result_context, round_result = (
            self.coordinator
            .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                context,
                player_side_commands={
                    "player": BattleCommand(BATTLE_COM_WAIT),
                },
                enemy_mode_rolls={enemy_id: 0},
                enemy_target_rolls=None,
                enemy_escape_rolls={
                    enemy_id: OrdinaryEscapeRolls(
                        escape_roll_1_100=1,
                    )
                },
                opponent_abio_by_participant_id={"player": False},
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
                        fixed_dex=10,
                        fixed_luck=0,
                        earth=0,
                        water=0,
                        fire=0,
                        wind=0,
                    ),
                },
                attack_rolls={},
                defense_profile="newpower_70pct",
            )
        )
        terminal = round_result.after
        self.assertEqual(terminal.phase, "finished")
        self.assertEqual(terminal.result, "victory")
        self.assertNotIn(enemy_id, terminal.hp_by_participant_id)
        self.assertNotIn(enemy_id, terminal.slots)
        self.assertEqual(
            terminal.pending_exp_by_participant_id["player"],
            0,
        )
        escape_events = tuple(
            event
            for event in round_result.round.events
            if event.participant_id == enemy_id
        )
        self.assertEqual(len(escape_events), 1)
        self.assertEqual(escape_events[0].result, "escape_success")
        self.assertIsNotNone(escape_events[0].escape_resolution)
        self.assertEqual(
            escape_events[0].escape_resolution.effective_luck,
            1,
        )
        self.assertEqual(
            escape_events[0].escape_resolution.stored_escape_count_after,
            1,
        )
        self.assertEqual(
            result_context.persistent_battle_state,
            terminal,
        )
        self.assertEqual(
            session.player_state.character.fields["exp"],
            0,
        )

    def test_recovered_enemy_ai_escape_fails_closed_without_rare_provenance(self):
        session = LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1, 0, 0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-escape-rare"}),
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
        spawned = context.spawned_enemies[0]
        context = replace(
            context,
            spawned_enemies=(
                replace(
                    spawned,
                    variant=replace(
                        spawned.variant,
                        tactics_option=(
                            "at:0;1;1|gu:0|es:1|"
                            "wa:0;0;0;0;0;0;0"
                        ),
                    ),
                    template=replace(
                        spawned.template,
                        rare=None,
                    ),
                ),
            ),
        )
        context = self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player": 0, enemy_id: 10},
        )
        with self.assertRaisesRegex(
            ValueError,
            "enemybase RARE provenance",
        ):
            (
                self.coordinator
                .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                    context,
                    player_side_commands={
                        "player": BattleCommand(BATTLE_COM_WAIT),
                    },
                    enemy_mode_rolls={enemy_id: 0},
                    enemy_target_rolls=None,
                    enemy_escape_rolls={
                        enemy_id: OrdinaryEscapeRolls(
                            escape_roll_1_100=1,
                        )
                    },
                    opponent_abio_by_participant_id={"player": False},
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
                            fixed_dex=10,
                            fixed_luck=0,
                            earth=0,
                            water=0,
                            fire=0,
                            wind=0,
                        ),
                    },
                    attack_rolls={},
                    defense_profile="newpower_70pct",
                )
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



    def test_recovered_enemy_ai_rehp_heals_ally_without_historical_numeric_com1(self):
        session=LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1,0,0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-rehp"}),
        )
        group=self.stack.request_encounter_group(session,group_roll=0)
        context=self.coordinator.start_group_battle(
            session,
            group,
            entry_count_roll=1,
            selection_rolls=(0,),
            birth_rolls=(
                EnemyBirthRolls(
                    level_roll=1,
                    birth_offsets=(0,0,0,0),
                    spawn_allocation_rolls=(0,1,2,3,0,1,2,3,0,1),
                ),
            ),
        )
        original=context.spawned_enemies[0]
        caster_id=str(context.battle.enemies[0].participant_id)
        ally_id="enemy:rehp-ally"
        self.stack.petskill_runtime=Recovered25PetSkillRuntime(
            skills={
                **dict(self.stack.petskill_runtime.skills),
                501:Recovered25PetSkillEntry(
                    skill_id=501,
                    field=1,
                    target=1,
                    cost=2,
                    illegal=0,
                    function_name="ENEMYSKILL_ReHP",
                    option_bytes=b"",
                ),
            },
            source_file=self.stack.petskill_runtime.source_file,
        )
        caster_participant=replace(
            context.battle.enemies[0],
            hp=600,max_hp=600,quick=200,
        )
        ally_participant=replace(
            context.battle.enemies[0],
            participant_id=ally_id,
            hp=100,max_hp=600,quick=20,
        )
        caster_spawn=replace(
            original,
            participant=caster_participant,
            template=replace(
                original.template,
                skill_ids=(501,20,30,40,50,60,70),
                skill_slot_ids=(501,20,30,40,50,60,70),
            ),
            variant=replace(
                original.variant,
                tactics_option="at:0;1;1|gu:0|es:0|wa:1;0;0;0;0;0;0",
            ),
        )
        ally_spawn=replace(
            original,
            participant=ally_participant,
            variant=replace(
                original.variant,
                tactics_option="at:0;1;1|gu:1|es:0|wa:0;0;0;0;0;0;0",
            ),
        )
        context=replace(
            context,
            battle=replace(
                context.battle,
                player=replace(
                    context.battle.player,hp=1000,max_hp=1000,quick=10
                ),
                enemies=(caster_participant,ally_participant),
            ),
            spawned_enemies=(caster_spawn,ally_spawn),
        )
        context=self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player":0,caster_id:10,ally_id:11},
        )
        profiles={
            "player":BattleCombatProfile(
                fixed_dex=10,fixed_luck=0,
                earth=0,water=0,fire=0,wind=0,
            ),
            caster_id:BattleCombatProfile(
                fixed_dex=100,fixed_luck=0,
                earth=0,water=0,fire=0,wind=0,
            ),
            ally_id:BattleCombatProfile(
                fixed_dex=10,fixed_luck=0,
                earth=0,water=0,fire=0,wind=0,
            ),
        }
        next_context,result=(
            self.coordinator
            .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                context,
                player_side_commands={"player":BattleCommand(BATTLE_COM_WAIT)},
                enemy_mode_rolls={caster_id:0,ally_id:0},
                enemy_target_rolls={caster_id:0},
                enemy_escape_rolls={},
                opponent_abio_by_participant_id={},
                initiative_random_subtracts={
                    "player":0,caster_id:0,ally_id:0,
                },
                profiles=profiles,
                attack_rolls={},
                defense_profile="newpower_70pct",
                enemy_rehp_rolls_by_attack_id={
                    caster_id:EnemyReHpRolls(0,100,100),
                },
                enemy_rehp_retarget_rolls_by_attack_id={
                    caster_id:None,
                },
            )
        )
        event=next(
            event for event in result.round.events
            if event.participant_id==caster_id
            and event.result=="enemy_rehp"
        )
        self.assertEqual(event.command1,BATTLE_COM_ATTACK)
        self.assertEqual(event.enemy_rehp_resolution.healed_slot,11)
        self.assertEqual(
            next_context.persistent_battle_state.hp_by_participant_id[ally_id],
            200,
        )
        self.assertEqual(
            next_context.persistent_battle_state.hp_by_participant_id["player"],
            1000,
        )


    def test_recovered_enemy_ai_damage_to_hp_executes_physical_drain(self):
        session=LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1,0,0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-damage-to-hp"}),
        )
        group=self.stack.request_encounter_group(session,group_roll=0)
        context=self.coordinator.start_group_battle(
            session,
            group,
            entry_count_roll=1,
            selection_rolls=(0,),
            birth_rolls=(
                EnemyBirthRolls(
                    level_roll=1,
                    birth_offsets=(0,0,0,0),
                    spawn_allocation_rolls=(0,1,2,3,0,1,2,3,0,1),
                ),
            ),
        )
        enemy_id=str(context.battle.enemies[0].participant_id)
        spawned=context.spawned_enemies[0]
        skills=dict(self.stack.petskill_runtime.skills)
        for skill_id,option in (
            (503,b"30|50"),
            (504,b"20|70"),
            (505,b"10|100"),
        ):
            skills[skill_id]=Recovered25PetSkillEntry(
                skill_id=skill_id,
                field=1,target=6,cost=2,illegal=0,
                function_name="PETSKILL_DamageToHp",
                option_bytes=option,
            )
        self.stack.petskill_runtime=Recovered25PetSkillRuntime(
            skills=skills,
            source_file=self.stack.petskill_runtime.source_file,
        )
        enemy=replace(
            context.battle.enemies[0],
            hp=100,max_hp=600,attack=300,defense=0,quick=200,
        )
        context=replace(
            context,
            battle=replace(
                context.battle,
                player=replace(
                    context.battle.player,
                    hp=1000,max_hp=1000,defense=0,quick=10,
                ),
                enemies=(enemy,),
            ),
            spawned_enemies=(
                replace(
                    spawned,
                    participant=enemy,
                    template=replace(
                        spawned.template,
                        skill_ids=(503,20,30,40,50,60,70),
                        skill_slot_ids=(503,20,30,40,50,60,70),
                    ),
                    variant=replace(
                        spawned.variant,
                        tactics_option=(
                            "at:0;1;1|gu:0|es:0|"
                            "wa:1;0;0;0;0;0;0"
                        ),
                    ),
                ),
            ),
        )
        context=self.coordinator.begin_persistent_group_battle(
            context,slots={"player":0,enemy_id:10}
        )
        next_context,result=(
            self.coordinator
            .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                context,
                player_side_commands={"player":BattleCommand(BATTLE_COM_WAIT)},
                enemy_mode_rolls={enemy_id:0},
                enemy_target_rolls={enemy_id:0},
                enemy_escape_rolls={},
                opponent_abio_by_participant_id={},
                initiative_random_subtracts={"player":0,enemy_id:0},
                profiles={
                    "player":BattleCombatProfile(
                        fixed_dex=10,fixed_luck=0,
                        earth=0,water=0,fire=0,wind=0,
                    ),
                    enemy_id:BattleCombatProfile(
                        fixed_dex=200,fixed_luck=0,
                        earth=0,water=0,fire=0,wind=0,
                    ),
                },
                attack_rolls={
                    enemy_id:OrdinaryAttackRolls(
                        dodge_roll_1_10000=10000,
                        critical_roll_1_10000=10000,
                        damage_roll=0,
                        minimum_damage_roll_0_1=1,
                    ),
                },
                defense_profile="newpower_70pct",
            )
        )
        event=next(
            e for e in result.round.events
            if e.participant_id==enemy_id and e.damage_to_hp_recovery
        )
        self.assertEqual(event.damage_to_hp_recovery.recovery_percent,50)
        self.assertGreater(
            next_context.persistent_battle_state.hp_by_participant_id[enemy_id],
            100,
        )


    def test_recovered_enemy_ai_mp_damage_updates_working_player_mp_only(self):
        session=LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1,0,0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-mp-damage"}),
        )
        group=self.stack.request_encounter_group(session,group_roll=0)
        context=self.coordinator.start_group_battle(
            session,group,
            entry_count_roll=1,
            selection_rolls=(0,),
            birth_rolls=(
                EnemyBirthRolls(
                    level_roll=1,
                    birth_offsets=(0,0,0,0),
                    spawn_allocation_rolls=(0,1,2,3,0,1,2,3,0,1),
                ),
            ),
        )
        enemy_id=str(context.battle.enemies[0].participant_id)
        spawned=context.spawned_enemies[0]
        skills=dict(self.stack.petskill_runtime.skills)
        for skill_id,option in (
            (506,b"50|50"),
            (507,b"50|75"),
            (508,b"50|100"),
        ):
            skills[skill_id]=Recovered25PetSkillEntry(
                skill_id=skill_id,field=1,target=6,cost=2,illegal=0,
                function_name="PETSKILL_MpDamage",option_bytes=option,
            )
        self.stack.petskill_runtime=Recovered25PetSkillRuntime(
            skills=skills,source_file=self.stack.petskill_runtime.source_file
        )
        enemy=replace(
            context.battle.enemies[0],
            hp=500,max_hp=500,attack=300,defense=0,quick=200,
        )
        context=replace(
            context,
            battle=replace(
                context.battle,
                player=replace(
                    context.battle.player,
                    hp=1000,max_hp=1000,defense=0,quick=10,
                ),
                enemies=(enemy,),
            ),
            spawned_enemies=(
                replace(
                    spawned,
                    participant=enemy,
                    template=replace(
                        spawned.template,
                        skill_ids=(506,20,30,40,50,60,70),
                        skill_slot_ids=(506,20,30,40,50,60,70),
                    ),
                    variant=replace(
                        spawned.variant,
                        tactics_option=(
                            "at:0;1;1|gu:0|es:0|"
                            "wa:1;0;0;0;0;0;0"
                        ),
                    ),
                ),
            ),
        )
        context=self.coordinator.begin_persistent_group_battle(
            context,slots={"player":0,enemy_id:10}
        )
        next_context,result=(
            self.coordinator
            .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                context,
                player_side_commands={"player":BattleCommand(BATTLE_COM_WAIT)},
                enemy_mode_rolls={enemy_id:0},
                enemy_target_rolls={enemy_id:0},
                enemy_escape_rolls={},
                opponent_abio_by_participant_id={},
                initiative_random_subtracts={"player":0,enemy_id:0},
                profiles={
                    "player":BattleCombatProfile(
                        fixed_dex=10,fixed_luck=0,
                        earth=0,water=0,fire=0,wind=0,
                    ),
                    enemy_id:BattleCombatProfile(
                        fixed_dex=200,fixed_luck=0,
                        earth=0,water=0,fire=0,wind=0,
                    ),
                },
                attack_rolls={
                    enemy_id:OrdinaryAttackRolls(
                        dodge_roll_1_10000=10000,
                        critical_roll_1_10000=10000,
                        damage_roll=0,
                        minimum_damage_roll_0_1=1,
                    ),
                },
                defense_profile="newpower_70pct",
            )
        )
        effect=next(
            e.mp_damage_resolution for e in result.round.events
            if e.mp_damage_resolution is not None
        )
        self.assertEqual((effect.mp_before,effect.mp_after),(40,20))
        working=decode_persistent_state(
            next_context.working_persistent_state_payload
        )
        self.assertEqual(working.character.fields["mp"],20)
        self.assertEqual(session.player_state.character.fields["mp"],40)


    def test_recovered_enemy_ai_fall_ground_executes_semantic_attack(self):
        session=LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1,0,0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-fall-ground"}),
        )
        group=self.stack.request_encounter_group(session,group_roll=0)
        context=self.coordinator.start_group_battle(
            session,
            group,
            entry_count_roll=1,
            selection_rolls=(0,),
            birth_rolls=(
                EnemyBirthRolls(
                    level_roll=1,
                    birth_offsets=(0,0,0,0),
                    spawn_allocation_rolls=(0,1,2,3,0,1,2,3,0,1),
                ),
            ),
        )
        enemy_id=str(context.battle.enemies[0].participant_id)
        spawned=context.spawned_enemies[0]
        skills=dict(self.stack.petskill_runtime.skills)
        skills[210]=Recovered25PetSkillEntry(
            skill_id=210,
            field=1,target=6,cost=2,illegal=3000,
            function_name="PETSKILL_FallGround",
            option_bytes="攻%-30".encode("cp950"),
        )
        self.stack.petskill_runtime=Recovered25PetSkillRuntime(
            skills=skills,
            source_file=self.stack.petskill_runtime.source_file,
        )
        enemy=replace(
            context.battle.enemies[0],
            attack=200,defense=0,quick=200,
        )
        context=replace(
            context,
            battle=replace(
                context.battle,
                player=replace(
                    context.battle.player,
                    hp=100,max_hp=100,defense=0,quick=10,
                ),
                enemies=(enemy,),
            ),
            spawned_enemies=(
                replace(
                    spawned,
                    participant=enemy,
                    template=replace(
                        spawned.template,
                        skill_ids=(210,20,30,40,50,60,70),
                        skill_slot_ids=(210,20,30,40,50,60,70),
                    ),
                    variant=replace(
                        spawned.variant,
                        tactics_option=(
                            "at:0;1;1|gu:0|es:0|"
                            "wa:1;0;0;0;0;0;0"
                        ),
                    ),
                ),
            ),
        )
        context=self.coordinator.begin_persistent_group_battle(
            context,slots={"player":0,enemy_id:10}
        )
        next_context,result=(
            self.coordinator
            .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                context,
                player_side_commands={"player":BattleCommand(BATTLE_COM_WAIT)},
                enemy_mode_rolls={enemy_id:0},
                enemy_target_rolls={enemy_id:0},
                enemy_escape_rolls={},
                opponent_abio_by_participant_id={},
                initiative_random_subtracts={"player":0,enemy_id:0},
                profiles={
                    "player":BattleCombatProfile(
                        fixed_dex=10,fixed_luck=0,
                        earth=0,water=0,fire=0,wind=0,
                    ),
                    enemy_id:BattleCombatProfile(
                        fixed_dex=200,fixed_luck=0,
                        earth=0,water=0,fire=0,wind=0,
                    ),
                },
                attack_rolls={
                    enemy_id:OrdinaryAttackRolls(
                        dodge_roll_1_10000=10000,
                        critical_roll_1_10000=10000,
                        damage_roll=0,
                        minimum_damage_roll_0_1=1,
                    ),
                },
                fall_ground_rolls_by_attack_id={enemy_id:100},
                fall_ground_equipment_resistance_by_participant_id={
                    "player":0,
                },
                defense_profile="newpower_70pct",
            )
        )
        event=next(
            e for e in result.round.events
            if e.participant_id==enemy_id
            and e.fall_ground_resolution is not None
        )
        self.assertTrue(event.fall_ground_resolution.rng_consumed)
        self.assertFalse(event.fall_ground_resolution.fell)
        self.assertIsNone(next_context.persistent_battle_state.ride_pet_runtime)

    def test_recovered_enemy_ai_battle_tear_executes_semantic_attack(self):
        session=LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1,0,0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-battle-tear"}),
        )
        group=self.stack.request_encounter_group(session,group_roll=0)
        context=self.coordinator.start_group_battle(
            session,group,
            entry_count_roll=1,selection_rolls=(0,),
            birth_rolls=(EnemyBirthRolls(
                level_roll=1,birth_offsets=(0,0,0,0),
                spawn_allocation_rolls=(0,1,2,3,0,1,2,3,0,1),
            ),),
        )
        enemy_id=str(context.battle.enemies[0].participant_id)
        spawned=context.spawned_enemies[0]
        skills=dict(self.stack.petskill_runtime.skills)
        for skill_id,option in ((615,b"20"),(616,b"50")):
            skills[skill_id]=Recovered25PetSkillEntry(
                skill_id=skill_id,field=1,target=1,cost=2,illegal=10000,
                function_name="PETSKILL_BattleTearDamage",
                option_bytes=option,
            )
        self.stack.petskill_runtime=Recovered25PetSkillRuntime(
            skills=skills,source_file=self.stack.petskill_runtime.source_file
        )
        enemy=replace(
            context.battle.enemies[0],attack=200,defense=100,quick=200
        )
        context=replace(
            context,
            battle=replace(
                context.battle,
                player=replace(
                    context.battle.player,
                    hp=50,max_hp=100,defense=0,quick=10,
                ),
                enemies=(enemy,),
            ),
            spawned_enemies=(replace(
                spawned,participant=enemy,
                template=replace(
                    spawned.template,
                    skill_ids=(615,20,30,40,50,60,70),
                    skill_slot_ids=(615,20,30,40,50,60,70),
                ),
                variant=replace(
                    spawned.variant,
                    tactics_option="at:0;1;1|gu:0|es:0|wa:1;0;0;0;0;0;0",
                ),
            ),),
        )
        context=self.coordinator.begin_persistent_group_battle(
            context,slots={"player":0,enemy_id:10}
        )
        next_context,result=(
            self.coordinator
            .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                context,
                player_side_commands={"player":BattleCommand(BATTLE_COM_WAIT)},
                enemy_mode_rolls={enemy_id:0},
                enemy_target_rolls={enemy_id:0},
                enemy_escape_rolls={},
                opponent_abio_by_participant_id={},
                initiative_random_subtracts={"player":0,enemy_id:0},
                profiles={
                    "player":BattleCombatProfile(
                        fixed_dex=10,fixed_luck=0,
                        earth=0,water=0,fire=0,wind=0,
                    ),
                    enemy_id:BattleCombatProfile(
                        fixed_dex=200,fixed_luck=0,
                        earth=0,water=0,fire=0,wind=0,
                    ),
                },
                attack_rolls={enemy_id:OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                    minimum_damage_roll_0_1=1,
                )},
                defense_profile="newpower_70pct",
            )
        )
        event=next(
            e for e in result.round.events
            if e.participant_id==enemy_id
            and e.battle_tear_augmentation is not None
        )
        self.assertEqual(event.battle_tear_augmentation.option_percent,20)
        self.assertEqual(event.battle_tear_augmentation.wound_basis,50)
        self.assertEqual(event.battle_tear_augmentation.wound_damage,10)
        self.assertEqual(
            next_context.persistent_battle_state.hp_by_participant_id["player"],
            result.round.hp_by_participant_id["player"],
        )


    def test_recovered_enemy_ai_nocast_executes_and_ticks_persistently(self):
        session=LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1,0,0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-nocast"}),
        )
        group=self.stack.request_encounter_group(session,group_roll=0)
        context=self.coordinator.start_group_battle(
            session,group,
            entry_count_roll=1,selection_rolls=(0,),
            birth_rolls=(EnemyBirthRolls(
                level_roll=1,birth_offsets=(0,0,0,0),
                spawn_allocation_rolls=(0,1,2,3,0,1,2,3,0,1),
            ),),
        )
        enemy_id=str(context.battle.enemies[0].participant_id)
        spawned=context.spawned_enemies[0]
        skills=dict(self.stack.petskill_runtime.skills)
        skills[580]=Recovered25PetSkillEntry(
            skill_id=580,field=1,target=3,cost=2,illegal=1000,
            function_name="PETSKILL_Nocast",
            option_bytes="turn=3 成=50".encode("cp950"),
        )
        self.stack.petskill_runtime=Recovered25PetSkillRuntime(
            skills=skills,source_file=self.stack.petskill_runtime.source_file
        )
        enemy=replace(context.battle.enemies[0],quick=200)
        player=replace(context.battle.player,quick=10)
        context=replace(
            context,
            battle=replace(context.battle,player=player,enemies=(enemy,)),
            spawned_enemies=(replace(
                spawned,participant=enemy,
                template=replace(
                    spawned.template,
                    skill_ids=(580,20,30,40,50,60,70),
                    skill_slot_ids=(580,20,30,40,50,60,70),
                ),
                variant=replace(
                    spawned.variant,
                    tactics_option="at:0;1;1|gu:0|es:0|wa:1;0;0;0;0;0;0",
                ),
            ),),
        )
        overlay=NocastRoundOverlay({
            "player":NocastParticipantRuntime(25,25,25,25),
            enemy_id:NocastParticipantRuntime(25,25,25,25),
        })
        context=self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player":0,enemy_id:10},
            nocast_overlay=overlay,
        )
        profiles={
            "player":BattleCombatProfile(
                fixed_dex=10,fixed_luck=0,
                earth=0,water=0,fire=0,wind=0,
            ),
            enemy_id:BattleCombatProfile(
                fixed_dex=200,fixed_luck=0,
                earth=0,water=0,fire=0,wind=0,
            ),
        }
        context,result=(
            self.coordinator
            .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                context,
                player_side_commands={"player":BattleCommand(BATTLE_COM_WAIT)},
                enemy_mode_rolls={enemy_id:0},
                enemy_target_rolls={enemy_id:0},
                enemy_escape_rolls={},
                opponent_abio_by_participant_id={},
                initiative_random_subtracts={"player":0,enemy_id:0},
                profiles=profiles,
                attack_rolls={},
                nocast_rolls_by_attack_id={
                    enemy_id:NocastActionRolls(
                        hit_rolls_by_slot={0:1}
                    )
                },
                defense_profile="newpower_70pct",
            )
        )
        applied=next(
            event for event in result.round.events
            if event.participant_id==enemy_id
            and event.nocast_application is not None
        )
        self.assertEqual(applied.result,"nocast_applied")
        self.assertEqual(applied.nocast_application.turn_written,3)
        player_runtime=(
            context.persistent_battle_state.nocast_overlay
            .runtime_by_participant_id["player"]
        )
        # Enemy acts first; the player then visits status slot 10 in the same
        # round, so the stored counter is already 2.
        self.assertEqual((player_runtime.counter,player_runtime.nc_flag),(2,1))
        self.assertTrue(
            self.coordinator.persistent_actor_direct_magic_blocked(
                context,"player"
            )
        )

        for expected_counter,expected_flag,blocked in (
            (1,1,True),
            (0,0,False),
        ):
            context,result=self.coordinator.resolve_persistent_attack_wait_round(
                context,
                commands={
                    "player":BattleCommand(BATTLE_COM_WAIT),
                    enemy_id:BattleCommand(BATTLE_COM_WAIT),
                },
                initiative_random_subtracts={"player":0,enemy_id:0},
                profiles=profiles,
                attack_rolls={},
                defense_profile="newpower_70pct",
            )
            player_runtime=(
                context.persistent_battle_state.nocast_overlay
                .runtime_by_participant_id["player"]
            )
            self.assertEqual(
                (player_runtime.counter,player_runtime.nc_flag),
                (expected_counter,expected_flag),
            )
            self.assertEqual(
                self.coordinator.persistent_actor_direct_magic_blocked(
                    context,"player"
                ),
                blocked,
            )


    def test_recovered_enemy_ai_weaken_executes_and_persists(self):
        from unittest.mock import patch
        from tests.test_stoneage_weaken_runtime import SYNTHETIC_HASH, SYNTHETIC_OPTION
        from tools.stoneage_weaken_runtime_state import WeakenActionRolls
        session=LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1,0,0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-weaken"}),
        )
        group=self.stack.request_encounter_group(session,group_roll=0)
        context=self.coordinator.start_group_battle(
            session,group,
            entry_count_roll=1,selection_rolls=(0,),
            birth_rolls=(EnemyBirthRolls(
                level_roll=1,birth_offsets=(0,0,0,0),
                spawn_allocation_rolls=(0,1,2,3,0,1,2,3,0,1),
            ),),
        )
        enemy_id=str(context.battle.enemies[0].participant_id)
        spawned=context.spawned_enemies[0]
        skills=dict(self.stack.petskill_runtime.skills)
        skills[575]=Recovered25PetSkillEntry(
            skill_id=575,field=1,target=6,cost=2,illegal=3000,
            function_name="PETSKILL_Weaken",
            option_bytes=SYNTHETIC_OPTION,
        )
        skills[576]=Recovered25PetSkillEntry(
            skill_id=576,field=1,target=3,cost=2,illegal=0,
            function_name="PETSKILL_Weaken",
            option_bytes=SYNTHETIC_OPTION,
        )
        self.stack.petskill_runtime=Recovered25PetSkillRuntime(
            skills=skills,
            source_file=self.stack.petskill_runtime.source_file,
        )
        enemy=replace(context.battle.enemies[0],quick=200)
        player=replace(context.battle.player,quick=10)
        context=replace(
            context,
            battle=replace(context.battle,player=player,enemies=(enemy,)),
            spawned_enemies=(replace(
                spawned,
                participant=enemy,
                template=replace(
                    spawned.template,
                    skill_ids=(576,20,30,40,50,60,70),
                    skill_slot_ids=(576,20,30,40,50,60,70),
                ),
                variant=replace(
                    spawned.variant,
                    tactics_option="at:0;1;1|gu:0|es:0|wa:1;0;0;0;0;0;0",
                ),
            ),),
        )
        overlay=NocastRoundOverlay({
            "player":NocastParticipantRuntime(25,25,25,25),
            enemy_id:NocastParticipantRuntime(25,25,25,25),
        })
        context=self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player":0,enemy_id:10},
            nocast_overlay=overlay,
        )
        # Synthetic grammar witness; actual preservation hash is gated in data CI.
        with patch('tools.stoneage_enemy_ai_weaken_bridge.EXPECTED_OPTION_SHA256',SYNTHETIC_HASH):
            context,result=(
                self.coordinator
                .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                    context,
                    player_side_commands={
                        "player":BattleCommand(BATTLE_COM_WAIT)
                    },
                    enemy_mode_rolls={enemy_id:0},
                    enemy_target_rolls={enemy_id:0},
                    enemy_escape_rolls={},
                    opponent_abio_by_participant_id={},
                    initiative_random_subtracts={"player":0,enemy_id:0},
                    profiles={
                        "player":BattleCombatProfile(
                            fixed_dex=10,fixed_luck=0,
                            earth=0,water=0,fire=0,wind=0,
                        ),
                        enemy_id:BattleCombatProfile(
                            fixed_dex=200,fixed_luck=0,
                            earth=0,water=0,fire=0,wind=0,
                        ),
                    },
                    attack_rolls={},
                    weaken_rolls_by_attack_id={
                        enemy_id:WeakenActionRolls(
                            hit_rolls_by_slot={0:1}
                        )
                    },
                    defense_profile="newpower_70pct",
                )
            )
        applied=next(
            event for event in result.round.events
            if event.participant_id==enemy_id
            and event.weaken_application is not None
        )
        self.assertEqual(applied.result,"weaken_applied")
        self.assertEqual(applied.weaken_application.counter_written,4)
        self.assertTrue(any(
            event.participant_id=="player"
            and event.result=="wait"
            for event in result.round.events
        ))
        player_runtime=(
            context.persistent_battle_state.nocast_overlay
            .runtime_by_participant_id["player"]
        )
        self.assertEqual(player_runtime.weaken_counter,3)
        self.assertIsNotNone(player_runtime.prepared_weaken_powers)
        self.assertEqual(player_runtime.prepared_weaken_powers.dexterity,8)
        # Three further coordinator calls consume the persisted clock and work
        # snapshot without reapplying the previous preparation on entry.
        context=replace(context,spawned_enemies=(replace(context.spawned_enemies[0],
            variant=replace(context.spawned_enemies[0].variant,
                tactics_option="at:0;1;1|gu:1|es:0|wa:0;0;0;0;0;0;0")),))
        for expected_counter in (2,1,0):
            previous=context.persistent_battle_state
            context,result=self.coordinator.resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                context,player_side_commands={"player":BattleCommand(BATTLE_COM_WAIT)},
                enemy_mode_rolls={enemy_id:0},enemy_target_rolls={},enemy_escape_rolls={},
                opponent_abio_by_participant_id={},initiative_random_subtracts={"player":0,enemy_id:0},
                profiles={"player":BattleCombatProfile(10,0,0,0,0,0),enemy_id:BattleCombatProfile(200,0,0,0,0,0)},
                attack_rolls={},defense_profile="newpower_70pct")
            self.assertEqual(result.before,previous)
            late=context.persistent_battle_state.nocast_overlay.runtime_by_participant_id["player"]
            self.assertEqual(late.weaken_counter,expected_counter)
            if expected_counter:
                self.assertEqual(late.prepared_weaken_powers.dexterity,8)
            else:
                self.assertIsNone(late.prepared_weaken_powers)
                self.assertEqual(context.persistent_battle_state.base_status_runtime_by_participant_id["player"].work_quick,10)

    def test_recovered_enemy_ai_refresh_clears_silence_and_persists(self):
        from tests.test_stoneage_refresh_runtime import (
            SYNTHETIC_HASHES as REFRESH_HASHES,
            SYNTHETIC_OPTIONS as REFRESH_OPTIONS,
        )
        from tools.stoneage_enemy_ai_refresh_bridge import (
            EXPECTED_OPTION_SHA256_BY_ID,
        )
        from tools.stoneage_refresh_runtime_state import RefreshActionRolls

        session=LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1,0,0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-refresh"}),
        )
        group=self.stack.request_encounter_group(session,group_roll=0)
        context=self.coordinator.start_group_battle(
            session,group,
            entry_count_roll=1,selection_rolls=(0,),
            birth_rolls=(EnemyBirthRolls(
                level_roll=1,birth_offsets=(0,0,0,0),
                spawn_allocation_rolls=(0,1,2,3,0,1,2,3,0,1),
            ),),
        )
        enemy_id=str(context.battle.enemies[0].participant_id)
        spawned=context.spawned_enemies[0]
        skills=dict(self.stack.petskill_runtime.skills)
        metadata={
            583:(1,2,2,2000),
            584:(1,2,2,5000),
            591:(1,1,2,5000),
            592:(1,2,2,8000),
            593:(1,2,2,5000),
        }
        for skill_id,(field,target,cost,illegal) in metadata.items():
            skills[skill_id]=Recovered25PetSkillEntry(
                skill_id=skill_id,
                field=field,
                target=target,
                cost=cost,
                illegal=illegal,
                function_name="PETSKILL_Refresh",
                option_bytes=REFRESH_OPTIONS[skill_id],
            )
        self.stack.petskill_runtime=Recovered25PetSkillRuntime(
            skills=skills,
            source_file=self.stack.petskill_runtime.source_file,
        )
        enemy=replace(context.battle.enemies[0],quick=200)
        player=replace(context.battle.player,quick=10)
        context=replace(
            context,
            battle=replace(context.battle,player=player,enemies=(enemy,)),
            spawned_enemies=(replace(
                spawned,
                participant=enemy,
                template=replace(
                    spawned.template,
                    skill_ids=(583,20,30,40,50,60,70),
                    skill_slot_ids=(583,20,30,40,50,60,70),
                ),
                variant=replace(
                    spawned.variant,
                    tactics_option="at:0;1;1|gu:0|es:0|wa:1;0;0;0;0;0;0",
                ),
            ),),
        )
        overlay=NocastRoundOverlay({
            "player":NocastParticipantRuntime(
                25,25,25,25,counter=3,nc_flag=1
            ),
            enemy_id:NocastParticipantRuntime(25,25,25,25),
        })
        context=self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player":0,enemy_id:10},
            nocast_overlay=overlay,
        )
        self.assertTrue(
            self.coordinator.persistent_actor_direct_magic_blocked(
                context,"player"
            )
        )
        with patch.dict(
            EXPECTED_OPTION_SHA256_BY_ID,
            REFRESH_HASHES,
            clear=True,
        ):
            batch=self.coordinator._build_persistent_enemy_common_batch(
                context,
                mode_rolls_by_enemy_id={enemy_id:0},
                target_rolls_by_enemy_id={enemy_id:0},
                allow_refresh_skill=True,
            )
            self.assertEqual(batch.refresh_submissions[enemy_id].skill_id,583)
            context,result=(
                self.coordinator
                .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                    context,
                    player_side_commands={
                        "player":BattleCommand(BATTLE_COM_WAIT)
                    },
                    enemy_mode_rolls={enemy_id:0},
                    enemy_target_rolls={enemy_id:0},
                    enemy_escape_rolls={},
                    opponent_abio_by_participant_id={},
                    initiative_random_subtracts={"player":0,enemy_id:0},
                    profiles={
                        "player":BattleCombatProfile(
                            fixed_dex=10,fixed_luck=0,
                            earth=0,water=0,fire=0,wind=0,
                        ),
                        enemy_id:BattleCombatProfile(
                            fixed_dex=200,fixed_luck=0,
                            earth=0,water=0,fire=0,wind=0,
                        ),
                    },
                    attack_rolls={},
                    refresh_rolls_by_attack_id={
                        enemy_id:RefreshActionRolls()
                    },
                    defense_profile="newpower_70pct",
                )
            )
        event=next(
            event for event in result.round.events
            if event.refresh_skill_id is not None
        )
        self.assertEqual(
            (event.refresh_skill_id,event.refresh_status_index,
             event.refresh_cleared_status),
            (583,10,10),
        )
        late=(
            context.persistent_battle_state.nocast_overlay
            .runtime_by_participant_id["player"]
        )
        self.assertEqual((late.counter,late.nc_flag),(0,0))
        self.assertFalse(
            self.coordinator.persistent_actor_direct_magic_blocked(
                context,"player"
            )
        )
        self.assertEqual(
            context.persistent_battle_state.hp_by_participant_id["player"],
            result.round.hp_by_participant_id["player"],
        )

    def test_recovered_enemy_ai_setmagicpet_tgh_executes_and_persists(self):
        from tests.test_stoneage_setmagicpet_runtime import (
            SYNTHETIC_HASH_BY_ID as SETMAGICPET_HASHES,
            SYNTHETIC_OPTION_BY_ID as SETMAGICPET_OPTIONS,
        )
        from tools.stoneage_enemy_ai_setmagicpet_bridge import (
            EXPECTED_OPTION_SHA256_BY_ID,
        )
        from tools.stoneage_setmagicpet_runtime_state import (
            SetMagicPetActionRolls,
            SetMagicPetParticipantRuntime,
            SetMagicPetRoundOverlay,
        )

        session=LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1,0,0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-setmagicpet"}),
        )
        group=self.stack.request_encounter_group(session,group_roll=0)
        context=self.coordinator.start_group_battle(
            session,group,
            entry_count_roll=1,selection_rolls=(0,),
            birth_rolls=(EnemyBirthRolls(
                level_roll=1,birth_offsets=(0,0,0,0),
                spawn_allocation_rolls=(0,1,2,3,0,1,2,3,0,1),
            ),),
        )
        enemy_id=str(context.battle.enemies[0].participant_id)
        spawned=context.spawned_enemies[0]
        skills=dict(self.stack.petskill_runtime.skills)
        for skill_id in (601,602,603,604):
            skills[skill_id]=Recovered25PetSkillEntry(
                skill_id=skill_id,
                field=1,
                target=2,
                cost=2,
                illegal=2500,
                function_name="PETSKILL_SetMagicPet",
                option_bytes=SETMAGICPET_OPTIONS[skill_id],
            )
        self.stack.petskill_runtime=Recovered25PetSkillRuntime(
            skills=skills,
            source_file=self.stack.petskill_runtime.source_file,
        )
        enemy=replace(context.battle.enemies[0],quick=200)
        player=replace(context.battle.player,quick=10)
        baseline_defense=int(player.defense)
        context=replace(
            context,
            battle=replace(
                context.battle,player=player,enemies=(enemy,)
            ),
            spawned_enemies=(replace(
                spawned,
                participant=enemy,
                template=replace(
                    spawned.template,
                    skill_ids=(601,20,30,40,50,60,70),
                    skill_slot_ids=(601,20,30,40,50,60,70),
                ),
                variant=replace(
                    spawned.variant,
                    tactics_option=(
                        "at:0;1;1|gu:0|es:0|"
                        "wa:1;0;0;0;0;0;0"
                    ),
                ),
            ),),
        )
        context=self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player":0,enemy_id:10},
            setmagicpet_overlay=SetMagicPetRoundOverlay({
                "player":SetMagicPetParticipantRuntime(),
                enemy_id:SetMagicPetParticipantRuntime(),
            }),
        )
        with patch.dict(
            EXPECTED_OPTION_SHA256_BY_ID,
            SETMAGICPET_HASHES,
            clear=True,
        ):
            batch=self.coordinator._build_persistent_enemy_common_batch(
                context,
                mode_rolls_by_enemy_id={enemy_id:0},
                target_rolls_by_enemy_id={enemy_id:0},
                allow_setmagicpet_skill=True,
            )
            self.assertEqual(
                batch.setmagicpet_submissions[enemy_id].skill_id,
                601,
            )
            context,result=(
                self.coordinator
                .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                    context,
                    player_side_commands={
                        "player":BattleCommand(BATTLE_COM_WAIT)
                    },
                    enemy_mode_rolls={enemy_id:0},
                    enemy_target_rolls={enemy_id:0},
                    enemy_escape_rolls={},
                    opponent_abio_by_participant_id={},
                    initiative_random_subtracts={
                        "player":0,enemy_id:0
                    },
                    profiles={
                        "player":BattleCombatProfile(
                            fixed_dex=10,fixed_luck=0,
                            earth=0,water=0,fire=0,wind=0,
                        ),
                        enemy_id:BattleCombatProfile(
                            fixed_dex=200,fixed_luck=0,
                            earth=0,water=0,fire=0,wind=0,
                        ),
                    },
                    attack_rolls={},
                    setmagicpet_rolls_by_attack_id={
                        enemy_id:SetMagicPetActionRolls()
                    },
                    defense_profile="newpower_70pct",
                )
            )
        event=next(
            event for event in result.round.events
            if event.setmagicpet_skill_id is not None
        )
        self.assertEqual(
            (
                event.setmagicpet_skill_id,
                event.setmagicpet_kind,
                event.setmagicpet_applied,
            ),
            (601,"TGH",True),
        )
        magic=(
            context.persistent_battle_state.setmagicpet_overlay
            .runtime_by_participant_id["player"]
        )
        # Enemy acts first: TGH 3 is immediately visited by player's
        # same-round StatusSeq and therefore persists as 2.
        self.assertEqual(
            (magic.state.tgh_turn,magic.state.tgh_power),
            (2,15),
        )
        self.assertIsNotNone(magic.prepared_powers)
        self.assertEqual(
            magic.prepared_powers.defense,
            baseline_defense+(baseline_defense*15)//100,
        )
        self.assertEqual(
            context.persistent_battle_state.hp_by_participant_id["player"],
            result.round.hp_by_participant_id["player"],
        )

    def test_recovered_enemy_ai_barrier_executes_and_persists(self):
        session=LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1,0,0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-barrier"}),
        )
        group=self.stack.request_encounter_group(session,group_roll=0)
        context=self.coordinator.start_group_battle(
            session,group,
            entry_count_roll=1,selection_rolls=(0,),
            birth_rolls=(EnemyBirthRolls(
                level_roll=1,birth_offsets=(0,0,0,0),
                spawn_allocation_rolls=(0,1,2,3,0,1,2,3,0,1),
            ),),
        )
        enemy_id=str(context.battle.enemies[0].participant_id)
        spawned=context.spawned_enemies[0]
        skills=dict(self.stack.petskill_runtime.skills)
        skills[579]=Recovered25PetSkillEntry(
            skill_id=579,field=1,target=3,cost=2,illegal=0,
            function_name="PETSKILL_Barrier",
            option_bytes="turn=1 成=50".encode("cp950"),
        )
        skills[594]=Recovered25PetSkillEntry(
            skill_id=594,field=1,target=3,cost=2,illegal=0,
            function_name="PETSKILL_Barrier",
            option_bytes="turn=3 成=50".encode("cp950"),
        )
        self.stack.petskill_runtime=Recovered25PetSkillRuntime(
            skills=skills,
            source_file=self.stack.petskill_runtime.source_file,
        )
        enemy=replace(context.battle.enemies[0],quick=200)
        player=replace(context.battle.player,quick=10)
        context=replace(
            context,
            battle=replace(context.battle,player=player,enemies=(enemy,)),
            spawned_enemies=(replace(
                spawned,
                participant=enemy,
                template=replace(
                    spawned.template,
                    skill_ids=(594,20,30,40,50,60,70),
                    skill_slot_ids=(594,20,30,40,50,60,70),
                ),
                variant=replace(
                    spawned.variant,
                    tactics_option="at:0;1;1|gu:0|es:0|wa:1;0;0;0;0;0;0",
                ),
            ),),
        )
        overlay=NocastRoundOverlay({
            "player":NocastParticipantRuntime(25,25,25,25),
            enemy_id:NocastParticipantRuntime(25,25,25,25),
        })
        context=self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player":0,enemy_id:10},
            nocast_overlay=overlay,
        )
        context,result=(
            self.coordinator
            .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                context,
                player_side_commands={
                    "player":BattleCommand(BATTLE_COM_ATTACK,command2=10)
                },
                enemy_mode_rolls={enemy_id:0},
                enemy_target_rolls={enemy_id:0},
                enemy_escape_rolls={},
                opponent_abio_by_participant_id={},
                initiative_random_subtracts={"player":0,enemy_id:0},
                profiles={
                    "player":BattleCombatProfile(
                        fixed_dex=10,fixed_luck=0,
                        earth=0,water=0,fire=0,wind=0,
                    ),
                    enemy_id:BattleCombatProfile(
                        fixed_dex=200,fixed_luck=0,
                        earth=0,water=0,fire=0,wind=0,
                    ),
                },
                attack_rolls={},
                barrier_rolls_by_attack_id={
                    enemy_id:BarrierActionRolls(
                        hit_rolls_by_slot={0:1}
                    )
                },
                defense_profile="newpower_70pct",
            )
        )
        applied=next(
            event for event in result.round.events
            if event.participant_id==enemy_id
            and event.barrier_application is not None
        )
        self.assertEqual(applied.result,"barrier_applied")
        self.assertEqual(applied.barrier_application.counter_written,4)
        self.assertTrue(any(
            event.participant_id=="player"
            and event.result=="status_no_action"
            for event in result.round.events
        ))
        player_runtime=(
            context.persistent_battle_state.nocast_overlay
            .runtime_by_participant_id["player"]
        )
        self.assertEqual(player_runtime.barrier_counter,3)

    def test_recovered_enemy_ai_guard_break2_executes_semantic_attack(self):
        session=LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1,0,0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-guard-break2"}),
        )
        group=self.stack.request_encounter_group(session,group_roll=0)
        context=self.coordinator.start_group_battle(
            session,group,
            entry_count_roll=1,selection_rolls=(0,),
            birth_rolls=(EnemyBirthRolls(
                level_roll=1,birth_offsets=(0,0,0,0),
                spawn_allocation_rolls=(0,1,2,3,0,1,2,3,0,1),
            ),),
        )
        enemy_id=str(context.battle.enemies[0].participant_id)
        spawned=context.spawned_enemies[0]
        skills=dict(self.stack.petskill_runtime.skills)
        skills[543]=Recovered25PetSkillEntry(
            skill_id=543,
            field=1,
            target=6,
            cost=2,
            illegal=1000,
            function_name="PETSKILL_GuardBreak2",
            option_bytes=b"",
        )
        self.stack.petskill_runtime=Recovered25PetSkillRuntime(
            skills=skills,
            source_file=self.stack.petskill_runtime.source_file,
        )
        enemy=replace(
            context.battle.enemies[0],
            attack=300,
            defense=0,
            quick=200,
        )
        player=replace(
            context.battle.player,
            hp=500,
            max_hp=500,
            defense=0,
            quick=10,
        )
        context=replace(
            context,
            battle=replace(
                context.battle,
                player=player,
                enemies=(enemy,),
            ),
            spawned_enemies=(replace(
                spawned,
                participant=enemy,
                template=replace(
                    spawned.template,
                    skill_ids=(543,20,30,40,50,60,70),
                    skill_slot_ids=(543,20,30,40,50,60,70),
                ),
                variant=replace(
                    spawned.variant,
                    tactics_option="at:0;1;1|gu:0|es:0|wa:1;0;0;0;0;0;0",
                ),
            ),),
        )
        context=self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player":0,enemy_id:10},
        )
        context,result=(
            self.coordinator
            .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                context,
                player_side_commands={
                    "player":BattleCommand(BATTLE_COM_GUARD)
                },
                enemy_mode_rolls={enemy_id:0},
                enemy_target_rolls={enemy_id:0},
                enemy_escape_rolls={},
                opponent_abio_by_participant_id={},
                initiative_random_subtracts={
                    "player":0,
                    enemy_id:0,
                },
                profiles={
                    "player":BattleCombatProfile(
                        fixed_dex=10,
                        fixed_luck=0,
                        earth=0,water=0,fire=0,wind=0,
                    ),
                    enemy_id:BattleCombatProfile(
                        fixed_dex=200,
                        fixed_luck=0,
                        earth=0,water=0,fire=0,wind=0,
                    ),
                },
                attack_rolls={
                    enemy_id:OrdinaryAttackRolls(
                        critical_roll_1_10000=10000,
                        damage_roll=0,
                        guard_roll_1_100=100,
                    )
                },
                defense_profile="newpower_70pct",
            )
        )
        event=next(
            event for event in result.round.events
            if event.participant_id==enemy_id
            and event.guard_break2_resolution is not None
        )
        self.assertTrue(
            event.guard_break2_resolution.defender_command_is_guard
        )
        self.assertEqual(
            event.guard_break2_resolution.multiplier,
            1.3,
        )
        self.assertLess(
            context.persistent_battle_state.hp_by_participant_id["player"],
            500,
        )

    def test_recovered_enemy_ai_mdfyattack_executes_and_persists(self):
        session=LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1,0,0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-mdfyattack"}),
        )
        group=self.stack.request_encounter_group(session,group_roll=0)
        context=self.coordinator.start_group_battle(
            session,group,
            entry_count_roll=1,selection_rolls=(0,),
            birth_rolls=(EnemyBirthRolls(
                level_roll=1,birth_offsets=(0,0,0,0),
                spawn_allocation_rolls=(0,1,2,3,0,1,2,3,0,1),
            ),),
        )
        enemy_id=str(context.battle.enemies[0].participant_id)
        spawned=context.spawned_enemies[0]
        skills=dict(self.stack.petskill_runtime.skills)
        for i,code in enumerate((b"EA",b"WA",b"FI",b"WI")):
            skills[548+i]=Recovered25PetSkillEntry(
                skill_id=548+i,field=1,target=6,cost=2,illegal=2000,
                function_name="PETSKILL_Mdfyattack",option_bytes=code+b"|100",
            )
        self.stack.petskill_runtime=Recovered25PetSkillRuntime(
            skills=skills,
            source_file=self.stack.petskill_runtime.source_file,
        )
        enemy=replace(
            context.battle.enemies[0],
            attack=300,
            defense=0,
            quick=200,
        )
        player=replace(
            context.battle.player,
            hp=2000,
            max_hp=2000,
            defense=0,
            quick=10,
        )
        context=replace(
            context,
            battle=replace(
                context.battle,
                player=player,
                enemies=(enemy,),
            ),
            spawned_enemies=(replace(
                spawned,
                participant=enemy,
                template=replace(
                    spawned.template,
                    skill_ids=(548,20,30,40,50,60,70),
                    skill_slot_ids=(548,20,30,40,50,60,70),
                ),
                variant=replace(
                    spawned.variant,
                    tactics_option="at:0;1;1|gu:0|es:0|wa:1;0;0;0;0;0;0",
                ),
            ),),
        )
        context=self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player":0,enemy_id:10},
        )
        previous_hp=2000
        for turn in range(2):
            context,result=(
                self.coordinator
                .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                    context,
                    player_side_commands={
                        "player":BattleCommand(BATTLE_COM_GUARD)
                    },
                    enemy_mode_rolls={enemy_id:0},
                    enemy_target_rolls={enemy_id:0},
                    enemy_escape_rolls={},
                    opponent_abio_by_participant_id={},
                    initiative_random_subtracts={
                        "player":0,
                        enemy_id:0,
                    },
                    profiles={
                        "player":BattleCombatProfile(
                            fixed_dex=10,
                            fixed_luck=0,
                            earth=0,water=0,fire=0,wind=0,
                        ),
                        enemy_id:BattleCombatProfile(
                            fixed_dex=200,
                            fixed_luck=0,
                            earth=0,water=0,fire=0,wind=0,
                        ),
                    },
                    attack_rolls={
                        enemy_id:OrdinaryAttackRolls(
                            critical_roll_1_10000=10000,
                            damage_roll=0,
                            guard_roll_1_100=100,
                        )
                    },
                    defense_profile="newpower_70pct",
                )
            )
            event=next(e for e in result.round.events if e.mdfyattack_skill_id is not None)
            self.assertEqual((event.mdfyattack_skill_id,event.mdfyattack_element),(548,"earth"))
            self.assertEqual(event.mdfyattack_attack_vector,(100,0,0,0,0))
            self.assertTrue(event.mdfyattack_event_marked)
            self.assertEqual(event.target_hp_before,previous_hp)
            current_hp=context.persistent_battle_state.hp_by_participant_id["player"]
            self.assertEqual(current_hp,result.round.hp_by_participant_id["player"])
            self.assertLess(current_hp,previous_hp)
            previous_hp=current_hp

    def test_recovered_enemy_ai_attack_crazed_executes_and_persists(self):
        session=LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1,0,0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-attack-crazed"}),
        )
        group=self.stack.request_encounter_group(session,group_roll=0)
        context=self.coordinator.start_group_battle(
            session,group,
            entry_count_roll=1,selection_rolls=(0,),
            birth_rolls=(EnemyBirthRolls(
                level_roll=1,birth_offsets=(0,0,0,0),
                spawn_allocation_rolls=(0,1,2,3,0,1,2,3,0,1),
            ),),
        )
        enemy_id=str(context.battle.enemies[0].participant_id)
        spawned=context.spawned_enemies[0]
        skills=dict(self.stack.petskill_runtime.skills)
        skills[613]=Recovered25PetSkillEntry(
            skill_id=613,
            field=1,
            target=1,
            cost=2,
            illegal=0,
            function_name="PETSKILL_AttackCrazed",
            option_bytes=b"3",
        )
        self.stack.petskill_runtime=Recovered25PetSkillRuntime(
            skills=skills,
            source_file=self.stack.petskill_runtime.source_file,
        )
        enemy=replace(
            context.battle.enemies[0],
            attack=300,
            defense=0,
            quick=200,
        )
        player=replace(
            context.battle.player,
            hp=2000,
            max_hp=2000,
            defense=0,
            quick=10,
        )
        context=replace(
            context,
            battle=replace(
                context.battle,
                player=player,
                enemies=(enemy,),
            ),
            spawned_enemies=(replace(
                spawned,
                participant=enemy,
                template=replace(
                    spawned.template,
                    skill_ids=(613,20,30,40,50,60,70),
                    skill_slot_ids=(613,20,30,40,50,60,70),
                ),
                variant=replace(
                    spawned.variant,
                    tactics_option="at:0;1;1|gu:0|es:0|wa:1;0;0;0;0;0;0",
                ),
            ),),
        )
        context=self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player":0,enemy_id:10},
        )
        context,result=(
            self.coordinator
            .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                context,
                player_side_commands={
                    "player":BattleCommand(BATTLE_COM_GUARD)
                },
                enemy_mode_rolls={enemy_id:0},
                enemy_target_rolls={enemy_id:0},
                enemy_escape_rolls={},
                opponent_abio_by_participant_id={},
                initiative_random_subtracts={
                    "player":0,
                    enemy_id:0,
                },
                profiles={
                    "player":BattleCombatProfile(
                        fixed_dex=10,
                        fixed_luck=0,
                        earth=0,water=0,fire=0,wind=0,
                    ),
                    enemy_id:BattleCombatProfile(
                        fixed_dex=200,
                        fixed_luck=0,
                        earth=0,water=0,fire=0,wind=0,
                    ),
                },
                attack_rolls={},
                attack_crazed_rolls_by_attack_id={
                    enemy_id:AttackCrazedRolls(
                        selection_indices=(0,0,0),
                        hit_rolls=(OrdinaryAttackRolls(
                            critical_roll_1_10000=10000,
                            damage_roll=0,guard_roll_1_100=100,
                        ),)*3,
                    )
                },
                defense_profile="newpower_70pct",
            )
        )
        events=tuple(e for e in result.round.events if e.attack_crazed_skill_id is not None)
        self.assertEqual(len(events),3)
        self.assertTrue(all(e.participant_id==enemy_id for e in events))
        self.assertEqual([e.attack_crazed_hit_index for e in events],[0,1,2])
        first_hp=context.persistent_battle_state.hp_by_participant_id["player"]
        self.assertEqual(first_hp,result.round.hp_by_participant_id["player"])
        self.assertLess(first_hp,2000)
        context,result=(
            self.coordinator
            .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                context,
                player_side_commands={
                    "player":BattleCommand(BATTLE_COM_GUARD)
                },
                enemy_mode_rolls={enemy_id:0},
                enemy_target_rolls={enemy_id:0},
                enemy_escape_rolls={},
                opponent_abio_by_participant_id={},
                initiative_random_subtracts={
                    "player":0,
                    enemy_id:0,
                },
                profiles={
                    "player":BattleCombatProfile(
                        fixed_dex=10,
                        fixed_luck=0,
                        earth=0,water=0,fire=0,wind=0,
                    ),
                    enemy_id:BattleCombatProfile(
                        fixed_dex=200,
                        fixed_luck=0,
                        earth=0,water=0,fire=0,wind=0,
                    ),
                },
                attack_rolls={},
                attack_crazed_rolls_by_attack_id={
                    enemy_id:AttackCrazedRolls(
                        selection_indices=(0,0,0),
                        hit_rolls=(OrdinaryAttackRolls(
                            critical_roll_1_10000=10000,
                            damage_roll=0,guard_roll_1_100=100,
                        ),)*3,
                    )
                },
                defense_profile="newpower_70pct",
            )
        )
        events=tuple(e for e in result.round.events if e.attack_crazed_skill_id is not None)
        self.assertEqual(len(events),3)
        self.assertEqual(events[0].target_hp_before,first_hp)
        self.assertLess(context.persistent_battle_state.hp_by_participant_id["player"],first_hp)
        self.assertEqual(context.persistent_battle_state.hp_by_participant_id["player"],result.round.hp_by_participant_id["player"])


    def test_recovered_enemy_ai_wildviolent_executes_and_persists(self):
        from tests.test_stoneage_wildviolent_runtime import SYNTHETIC_OPTIONS, SYNTHETIC_HASHES
        session=LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1,0,0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-wildviolent"}),
        )
        group=self.stack.request_encounter_group(session,group_roll=0)
        context=self.coordinator.start_group_battle(
            session,group,
            entry_count_roll=1,selection_rolls=(0,),
            birth_rolls=(EnemyBirthRolls(
                level_roll=1,birth_offsets=(0,0,0,0),
                spawn_allocation_rolls=(0,1,2,3,0,1,2,3,0,1),
            ),),
        )
        enemy_id=str(context.battle.enemies[0].participant_id)
        spawned=context.spawned_enemies[0]
        skills=dict(self.stack.petskill_runtime.skills)
        skills[541]=Recovered25PetSkillEntry(
            skill_id=541,
            field=1,
            target=6,
            cost=2,
            illegal=1000,
            function_name=WILDVIOLENT_CALLBACK,
            option_bytes=SYNTHETIC_OPTIONS[541],
        )
        skills[652]=replace(skills[541], skill_id=652, option_bytes=SYNTHETIC_OPTIONS[652])
        self.stack.petskill_runtime=Recovered25PetSkillRuntime(
            skills=skills,
            source_file=self.stack.petskill_runtime.source_file,
        )
        enemy=replace(
            context.battle.enemies[0],
            attack=300,
            defense=100,
            quick=200,
        )
        player=replace(
            context.battle.player,
            hp=2000,
            max_hp=2000,
            defense=0,
            quick=10,
        )
        context=replace(
            context,
            battle=replace(
                context.battle,
                player=player,
                enemies=(enemy,),
            ),
            spawned_enemies=(replace(
                spawned,
                participant=enemy,
                template=replace(
                    spawned.template,
                    skill_ids=(541,20,30,40,50,60,70),
                    skill_slot_ids=(541,20,30,40,50,60,70),
                ),
                variant=replace(
                    spawned.variant,
                    tactics_option="at:0;1;1|gu:0|es:0|wa:1;0;0;0;0;0;0",
                ),
            ),),
        )
        context=self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player":0,enemy_id:10},
        )
        hit=OrdinaryAttackRolls(
            critical_roll_1_10000=10000,
            damage_roll=0,
            guard_roll_1_100=100,
            dodge_roll_1_10000=None,
        )
        from tools.stoneage_nocast_runtime_state import PreparedWeakenPowers
        state=context.persistent_battle_state
        late={pid:NocastParticipantRuntime(25,25,25,25) for pid in state.hp_by_participant_id}
        late[enemy_id]=replace(late[enemy_id], weaken_counter=1,
                              prepared_weaken_powers=PreparedWeakenPowers(240,80,160))
        context=replace(context, persistent_battle_state=replace(state, nocast_overlay=NocastRoundOverlay(late)))
        previous_hp=2000
        with patch(
            "tools.stoneage_enemy_ai_wildviolent_bridge.EXPECTED_OPTION_SHA256",
            SYNTHETIC_HASHES,
        ):
            for expected_powers in ((468,52),(585,65)):
                batch=self.coordinator._build_persistent_enemy_common_batch(
                    context, mode_rolls_by_enemy_id={enemy_id:0},
                    target_rolls_by_enemy_id={enemy_id:0}, allow_wildviolent_skill=True)
                setup=batch.wildviolent_submissions[enemy_id].setup
                self.assertEqual((setup.attack_power,setup.defense_power), expected_powers)
                context,result=(
                    self.coordinator
                    .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                        context,
                        player_side_commands={
                            "player":BattleCommand(BATTLE_COM_GUARD)
                        },
                        enemy_mode_rolls={enemy_id:0},
                        enemy_target_rolls={enemy_id:0},
                        enemy_escape_rolls={},
                        opponent_abio_by_participant_id={},
                        initiative_random_subtracts={
                            "player":0,
                            enemy_id:0,
                        },
                        profiles={
                            "player":BattleCombatProfile(
                                fixed_dex=10,
                                fixed_luck=0,
                                earth=0,water=0,fire=0,wind=0,
                            ),
                            enemy_id:BattleCombatProfile(
                                fixed_dex=200,
                                fixed_luck=0,
                                earth=0,water=0,fire=0,wind=0,
                            ),
                        },
                        attack_rolls={},
                        wildviolent_rolls_by_attack_id={
                            enemy_id:WildViolentRolls(
                                3,(hit,hit,hit)
                            )
                        },
                        defense_profile="newpower_70pct",
                    )
                )
                events=tuple(
                    event for event in result.round.events
                    if event.wildviolent_skill_id is not None
                )
                self.assertEqual(len(events),3)
                self.assertEqual(
                    [event.wildviolent_hit_index for event in events],
                    [0,1,2],
                )
                self.assertTrue(
                    all(event.wildviolent_skill_id==541 for event in events)
                )
                self.assertTrue(
                    all(event.wildviolent_attack_count==3 for event in events)
                )
                self.assertTrue(
                    all(
                        event.wildviolent_dodge_percent_points==30
                        for event in events
                    )
                )
                self.assertEqual(events[0].target_hp_before,previous_hp)
                current_hp=(
                    context.persistent_battle_state
                    .hp_by_participant_id["player"]
                )
                self.assertEqual(
                    current_hp,
                    result.round.hp_by_participant_id["player"],
                )
                self.assertLess(current_hp,previous_hp)
                restored=context.persistent_battle_state.nocast_overlay.runtime_by_participant_id[enemy_id]
                self.assertEqual(restored.weaken_counter,0)
                self.assertIsNone(restored.prepared_weaken_powers)
                self.assertEqual(context.persistent_battle_state.session.enemies[0].attack,300)
                previous_hp=current_hp


    def test_recovered_enemy_ai_battletimid_executes_and_persists_exit(self):
        session=LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1,0,0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-battletimid"}),
        )
        group=self.stack.request_encounter_group(session,group_roll=0)
        context=self.coordinator.start_group_battle(
            session,group,
            entry_count_roll=1,selection_rolls=(0,),
            birth_rolls=(EnemyBirthRolls(
                level_roll=1,birth_offsets=(0,0,0,0),
                spawn_allocation_rolls=(0,1,2,3,0,1,2,3,0,1),
            ),),
        )
        enemy_id=str(context.battle.enemies[0].participant_id)
        spawned=context.spawned_enemies[0]
        skills=dict(self.stack.petskill_runtime.skills)
        skills[606]=Recovered25PetSkillEntry(
            skill_id=606,
            field=1,
            target=6,
            cost=2,
            illegal=3000,
            function_name="PETSKILL_BattleTimid",
            option_bytes=b"",
        )
        self.stack.petskill_runtime=Recovered25PetSkillRuntime(
            skills=skills,
            source_file=self.stack.petskill_runtime.source_file,
        )
        enemy=replace(
            context.battle.enemies[0],
            attack=300,
            quick=200,
        )
        player=replace(
            context.battle.player,
            hp=2000,
            max_hp=2000,
            quick=10,
        )
        context=replace(
            context,
            battle=replace(
                context.battle,
                player=player,
                enemies=(enemy,),
            ),
            spawned_enemies=(replace(
                spawned,
                participant=enemy,
                template=replace(
                    spawned.template,
                    skill_ids=(606,20,30,40,50,60,70),
                    skill_slot_ids=(606,20,30,40,50,60,70),
                ),
                variant=replace(
                    spawned.variant,
                    tactics_option=(
                        "at:0;1;1|gu:0|es:0|"
                        "wa:1;0;0;0;0;0;0"
                    ),
                ),
            ),),
        )
        context=self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player":0,enemy_id:10},
        )
        batch=self.coordinator._build_persistent_enemy_common_batch(
            context,
            mode_rolls_by_enemy_id={enemy_id:0},
            target_rolls_by_enemy_id={enemy_id:0},
            allow_battletimid_skill=True,
        )
        submission=batch.battletimid_submissions[enemy_id]
        self.assertEqual(
            (
                submission.skill_id,
                submission.source_target_slot,
                submission.setup.attack_power,
                submission.setup.defence_power,
                submission.setup.quick,
            ),
            (
                606,
                0,
                int(enemy.attack*0.7),
                int(enemy.defense*0.4),
                int(enemy.quick*0.8),
            ),
        )
        context,result=(
            self.coordinator
            .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                context,
                player_side_commands={
                    "player":BattleCommand(BATTLE_COM_WAIT)
                },
                enemy_mode_rolls={enemy_id:0},
                enemy_target_rolls={enemy_id:0},
                enemy_escape_rolls={},
                opponent_abio_by_participant_id={},
                initiative_random_subtracts={"player":0,enemy_id:0},
                profiles={
                    "player":BattleCombatProfile(
                        fixed_dex=10,fixed_luck=0,
                        earth=0,water=0,fire=0,wind=0,
                    ),
                    enemy_id:BattleCombatProfile(
                        fixed_dex=200,fixed_luck=0,
                        earth=0,water=0,fire=0,wind=0,
                    ),
                },
                attack_rolls={
                    enemy_id:OrdinaryAttackRolls(
                        dodge_roll_1_10000=10000,
                        critical_roll_1_10000=10000,
                        damage_roll=0,
                        minimum_damage_roll_0_1=1,
                    )
                },
                battletimid_rolls_by_attack_id={enemy_id:14},
                defense_profile="newpower_70pct",
            )
        )
        event=next(
            event for event in result.round.events
            if event.battletimid_skill_id==606
        )
        self.assertTrue(event.battletimid_resolution.forced_exit)
        self.assertTrue(event.battletimid_resolution.player_battle_exit)
        self.assertGreater(result.after.hp_by_participant_id["player"],0)
        self.assertIn(
            "player",result.after.battle_exited_participant_ids
        )
        self.assertEqual(result.after.result,"defeat")
        self.assertEqual(
            context.persistent_battle_state.result,
            "defeat",
        )

    def test_enemy_ai_battletimid_rng_actor_set_is_exact(self):
        session=LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1,0,0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-battletimid-rng"}),
        )
        group=self.stack.request_encounter_group(session,group_roll=0)
        context=self.coordinator.start_group_battle(
            session,group,
            entry_count_roll=1,selection_rolls=(0,),
            birth_rolls=(EnemyBirthRolls(
                level_roll=1,birth_offsets=(0,0,0,0),
                spawn_allocation_rolls=(0,1,2,3,0,1,2,3,0,1),
            ),),
        )
        enemy_id=str(context.battle.enemies[0].participant_id)
        spawned=context.spawned_enemies[0]
        skills=dict(self.stack.petskill_runtime.skills)
        skills[606]=Recovered25PetSkillEntry(
            606,1,6,2,3000,"PETSKILL_BattleTimid",b""
        )
        self.stack.petskill_runtime=Recovered25PetSkillRuntime(
            skills=skills,
            source_file=self.stack.petskill_runtime.source_file,
        )
        enemy=replace(context.battle.enemies[0],quick=200)
        player=replace(context.battle.player,hp=2000,max_hp=2000,quick=10)
        context=replace(
            context,
            battle=replace(context.battle,player=player,enemies=(enemy,)),
            spawned_enemies=(replace(
                spawned,
                participant=enemy,
                template=replace(
                    spawned.template,
                    skill_ids=(606,20,30,40,50,60,70),
                    skill_slot_ids=(606,20,30,40,50,60,70),
                ),
                variant=replace(
                    spawned.variant,
                    tactics_option="at:0;1;1|gu:0|es:0|wa:1;0;0;0;0;0;0",
                ),
            ),),
        )
        context=self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player":0,enemy_id:10},
        )
        common=dict(
            context=context,
            player_side_commands={"player":BattleCommand(BATTLE_COM_WAIT)},
            enemy_mode_rolls={enemy_id:0},
            enemy_target_rolls={enemy_id:0},
            enemy_escape_rolls={},
            opponent_abio_by_participant_id={},
            initiative_random_subtracts={"player":0,enemy_id:0},
            profiles={
                "player":BattleCombatProfile(10,0,0,0,0,0),
                enemy_id:BattleCombatProfile(200,0,0,0,0,0),
            },
            attack_rolls={
                enemy_id:OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                )
            },
            defense_profile="newpower_70pct",
        )
        with self.assertRaisesRegex(ValueError,"BattleTimid RNG actors mismatch"):
            self.coordinator.resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                **common,
                battletimid_rolls_by_attack_id={},
            )
        with self.assertRaisesRegex(ValueError,"BattleTimid RNG actors mismatch"):
            self.coordinator.resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                **common,
                battletimid_rolls_by_attack_id={
                    enemy_id:14,
                    "ghost":14,
                },
            )


    def test_recovered_enemy_ai_combined_attreverse_executes_and_persists(self):
        session=LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1,0,0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-combined"}),
        )
        group=self.stack.request_encounter_group(session,group_roll=0)
        context=self.coordinator.start_group_battle(
            session,group,
            entry_count_roll=1,selection_rolls=(0,),
            birth_rolls=(EnemyBirthRolls(
                level_roll=1,birth_offsets=(0,0,0,0),
                spawn_allocation_rolls=(0,1,2,3,0,1,2,3,0,1),
            ),),
        )
        enemy_id=str(context.battle.enemies[0].participant_id)
        spawned=context.spawned_enemies[0]

        options={
            627:b"marker|6|21|139|159|169|179|189",
            629:b"marker|5|139|159|169|179|189",
            630:b"marker|1|306",
            632:b"marker|1|240",
            637:b"marker|1|61",
            646:b"marker|6|20|21|22|23|24|25",
            648:b"marker|6|71|81|91|101|121|61",
        }
        meta={
            627:(1,3,2,2000),629:(1,3,2,2000),630:(1,3,2,2000),
            632:(1,1,2,5000),637:(1,2,2,20000),
            646:(1,2,2,20000),648:(1,2,2,20000),
        }
        skills={}
        for skill_id,raw in options.items():
            field,target,cost,illegal=meta[skill_id]
            skills[skill_id]=Recovered25PetSkillEntry(
                skill_id,field,target,cost,illegal,
                "PETSKILL_Combined",raw,
            )
        combined_runtime=Recovered25PetSkillRuntime(
            skills=skills,source_file="petskill.txt"
        )
        self.stack.petskill_runtime=combined_runtime

        expected_rows=[]
        for skill_id in sorted(options):
            entry=combined_runtime.skills[skill_id]
            marker,declared,effective,magic_ids,well=(
                combined_bridge._option_structure(entry.option_bytes)
            )
            expected_rows.append((
                skill_id,entry.field,entry.target,entry.cost,entry.illegal,
                0,len(entry.option_bytes),
                hashlib.sha256(entry.option_bytes).hexdigest(),
                False,marker,declared,effective,magic_ids,well,
            ))
        functions={
            20:"MAGIC_Recovery",21:"MAGIC_Recovery",22:"MAGIC_Recovery",
            23:"MAGIC_Recovery",24:"MAGIC_Recovery",25:"MAGIC_Recovery",
            61:"MAGIC_StatusRecovery",71:"MAGIC_StatusRecovery",
            81:"MAGIC_StatusRecovery",91:"MAGIC_StatusRecovery",
            101:"MAGIC_StatusRecovery",121:"MAGIC_StatusRecovery",
            139:"MAGIC_StatusChange",159:"MAGIC_StatusChange",
            169:"MAGIC_StatusChange",179:"MAGIC_StatusChange",
            189:"MAGIC_StatusChange",240:"MAGIC_AttReverse",
            306:"MAGIC_AttMagic",
        }
        magic_rows=tuple(
            (
                magic_id,function,
                hashlib.sha256(function.encode("ascii")).hexdigest(),
                1,8,0,None,0,hashlib.sha256(b"").hexdigest(),False,
            )
            for magic_id,function in sorted(functions.items())
        )

        enemy=replace(context.battle.enemies[0],quick=200)
        player=replace(
            context.battle.player,hp=1000,max_hp=1000,quick=10,
        )
        context=replace(
            context,
            battle=replace(context.battle,player=player,enemies=(enemy,)),
            spawned_enemies=(replace(
                spawned,
                participant=enemy,
                template=replace(
                    spawned.template,
                    skill_ids=(632,0,0,0,0,0,0),
                    skill_slot_ids=(632,0,0,0,0,0,0),
                ),
                variant=replace(
                    spawned.variant,
                    tactics_option=(
                        "at:0;1;1|gu:0|es:0|"
                        "wa:1;0;0;0;0;0;0"
                    ),
                ),
            ),),
        )
        context=self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player":0,enemy_id:10},
            nocast_overlay=NocastRoundOverlay({
                "player":NocastParticipantRuntime(25,25,25,25),
                enemy_id:NocastParticipantRuntime(25,25,25,25),
            }),
            combined_overlay=CombinedRuntimeOverlay(
                PROFILE_GAVIN_IRIS_30PCT,
                STATUS_MAGIC_PROFILE_IRIS_CP950,
                RuntimeItemZeroWitness(True,5),
                {enemy_id:20},
                {"player":False,enemy_id:False},
            ),
        )
        profiles={
            "player":BattleCombatProfile(
                fixed_dex=10,fixed_luck=0,
                earth=10,water=20,fire=30,wind=40,
            ),
            enemy_id:BattleCombatProfile(
                fixed_dex=200,fixed_luck=0,
                earth=0,water=0,fire=0,wind=0,
            ),
        }
        common=dict(
            player_side_commands={"player":BattleCommand(BATTLE_COM_WAIT)},
            enemy_mode_rolls={enemy_id:0},
            enemy_target_rolls={enemy_id:0},
            enemy_escape_rolls={},
            opponent_abio_by_participant_id={},
            initiative_random_subtracts={"player":0,enemy_id:0},
            profiles=profiles,
            attack_rolls={},
            defense_profile="newpower_70pct",
            combined_selection_draws_by_enemy_id={enemy_id:0},
            combined_rolls_by_attack_id={enemy_id:CombinedActionRolls()},
        )
        with (
            patch.object(
                combined_bridge,"EXPECTED_EXACT_ROWS",tuple(expected_rows)
            ),
            patch.object(
                combined_bridge,"EXPECTED_EXACT_MAGIC_ROWS",magic_rows
            ),
        ):
            batch=self.coordinator._build_persistent_enemy_common_batch(
                context,
                mode_rolls_by_enemy_id={enemy_id:0},
                target_rolls_by_enemy_id={enemy_id:0},
                allow_combined_skill=True,
                combined_selection_draws_by_enemy_id={enemy_id:0},
            )
            self.assertEqual(
                batch.combined_submissions[enemy_id].magic.magic_id,240
            )
            context,first=(
                self.coordinator
                .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                    context,**common
                )
            )
            event=next(
                e for e in first.round.events
                if e.combined_magic_id==240
            )
            self.assertEqual(event.result,"combined_att_reverse_toggled")
            self.assertTrue(
                context.persistent_battle_state.combined_overlay
                .att_reverse_by_participant_id["player"]
            )
            self.assertEqual(
                context.persistent_battle_state.combined_overlay
                .mp_by_participant_id[enemy_id],
                15,
            )

            context,second=(
                self.coordinator
                .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                    context,**common
                )
            )
        event=next(
            e for e in second.round.events
            if e.combined_magic_id==240
        )
        effect=event.combined_att_reverse_effect
        self.assertEqual(
            (effect.earth,effect.water,effect.fire,effect.wind),
            (30,40,10,20),
        )
        self.assertFalse(
            context.persistent_battle_state.combined_overlay
            .att_reverse_by_participant_id["player"]
        )
        self.assertEqual(
            context.persistent_battle_state.combined_overlay
            .mp_by_participant_id[enemy_id],
            10,
        )

    def test_recovered_enemy_ai_vary_requires_profile_executes_and_blocks_recast(self):
        session=LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1,0,0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-vary"}),
        )
        group=self.stack.request_encounter_group(session,group_roll=0)
        context=self.coordinator.start_group_battle(
            session,group,
            entry_count_roll=1,selection_rolls=(0,),
            birth_rolls=(EnemyBirthRolls(
                level_roll=1,birth_offsets=(0,0,0,0),
                spawn_allocation_rolls=(0,1,2,3,0,1,2,3,0,1),
            ),),
        )
        enemy_id=str(context.battle.enemies[0].participant_id)
        spawned=context.spawned_enemies[0]

        synthetic_option=b"x"*22
        synthetic_digest=hashlib.sha256(synthetic_option).hexdigest()
        self.stack.petskill_runtime=Recovered25PetSkillRuntime(
            skills={
                600:Recovered25PetSkillEntry(
                    600,1,5,2,1000,"PETSKILL_Vary",synthetic_option
                )
            },
            source_file="petskill.txt",
        )

        enemy=replace(
            context.battle.enemies[0],
            attack=100,defense=80,quick=80,
        )
        player=replace(
            context.battle.player,
            hp=1000,max_hp=1000,quick=100,
        )
        context=replace(
            context,
            battle=replace(context.battle,player=player,enemies=(enemy,)),
            spawned_enemies=(replace(
                spawned,
                participant=enemy,
                template=replace(
                    spawned.template,
                    tempno=981,
                    graphic_id=101427,
                    skill_ids=(0,0,600,0,0,0,0),
                    skill_slot_ids=(0,0,600,0,0,0,0),
                ),
                variant=replace(
                    spawned.variant,
                    tactics_option=(
                        "at:0;1;1|gu:0|es:0|"
                        "wa:0;0;1;0;0;0;0"
                    ),
                ),
            ),),
        )
        context=self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player":0,enemy_id:10},
        )

        with patch.object(
            vary_bridge,"EXPECTED_OPTION_SHA256",synthetic_digest
        ):
            with self.assertRaisesRegex(
                ValueError,"explicit descendant profile"
            ):
                self.coordinator._build_persistent_enemy_common_batch(
                    context,
                    mode_rolls_by_enemy_id={enemy_id:0},
                    target_rolls_by_enemy_id={enemy_id:0},
                    allow_vary_skill=True,
                )

            batch=self.coordinator._build_persistent_enemy_common_batch(
                context,
                mode_rolls_by_enemy_id={enemy_id:0},
                target_rolls_by_enemy_id={enemy_id:0},
                allow_vary_skill=True,
                vary_profiles_by_enemy_id={
                    enemy_id:PROFILE_GAVIN_IRIS_ATTACK_QUICK
                },
            )
            submission=batch.vary_submissions[enemy_id]
            self.assertEqual(submission.skill_id,600)
            self.assertEqual(submission.skill_slot,2)
            self.assertEqual(
                (
                    submission.runtime_after_callback.attack_power,
                    submission.runtime_after_callback.defense_power,
                    submission.runtime_after_callback.quick,
                ),
                (130,80,104),
            )

            context,result=(
                self.coordinator
                .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                    context,
                    player_side_commands={
                        "player":BattleCommand(BATTLE_COM_WAIT)
                    },
                    enemy_mode_rolls={enemy_id:0},
                    enemy_target_rolls={enemy_id:0},
                    enemy_escape_rolls={},
                    opponent_abio_by_participant_id={},
                    initiative_random_subtracts={
                        "player":0,enemy_id:0
                    },
                    profiles={
                        "player":BattleCombatProfile(
                            fixed_dex=100,fixed_luck=0,
                            earth=0,water=0,fire=0,wind=0,
                        ),
                        enemy_id:BattleCombatProfile(
                            fixed_dex=80,fixed_luck=0,
                            earth=0,water=0,fire=0,wind=0,
                        ),
                    },
                    attack_rolls={},
                    vary_profiles_by_enemy_id={
                        enemy_id:PROFILE_GAVIN_IRIS_ATTACK_QUICK
                    },
                    defense_profile="newpower_70pct",
                )
            )

            event=next(
                e for e in result.round.events
                if e.vary_skill_id==600
            )
            self.assertEqual(event.result,"vary_applied")
            self.assertTrue(event.vary_visual_effect_enabled)
            self.assertEqual(result.round.action_order,(enemy_id,"player"))
            self.assertEqual(
                result.round.hp_by_participant_id["player"],1000
            )
            active=(
                context.persistent_battle_state.vary_overlay
                .runtime_by_participant_id[enemy_id]
            )
            self.assertEqual(active.work_turn,1)
            self.assertEqual(
                (active.attack_power,active.defense_power,active.quick),
                (130,80,104),
            )

            with self.assertRaisesRegex(ValueError,"recast"):
                (
                    self.coordinator
                    .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                        context,
                        player_side_commands={
                            "player":BattleCommand(BATTLE_COM_WAIT)
                        },
                        enemy_mode_rolls={enemy_id:0},
                        enemy_target_rolls={enemy_id:0},
                        enemy_escape_rolls={},
                        opponent_abio_by_participant_id={},
                        initiative_random_subtracts={
                            "player":0,enemy_id:0
                        },
                        profiles={
                            "player":BattleCombatProfile(
                                fixed_dex=100,fixed_luck=0,
                                earth=0,water=0,fire=0,wind=0,
                            ),
                            enemy_id:BattleCombatProfile(
                                fixed_dex=80,fixed_luck=0,
                                earth=0,water=0,fire=0,wind=0,
                            ),
                        },
                        attack_rolls={},
                        vary_profiles_by_enemy_id={
                            enemy_id:PROFILE_GAVIN_IRIS_ATTACK_QUICK
                        },
                        defense_profile="newpower_70pct",
                    )
                )


    def test_recovered_enemy_ai_relife_revives_retained_dead_entry(self):
        session=LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1,0,0),
            player_state=_battle_player_state(),
            world_flags=frozenset({"enemy-ai-relife"}),
        )
        group=self.stack.request_encounter_group(session,group_roll=0)
        context=self.coordinator.start_group_battle(
            session,
            group,
            entry_count_roll=1,
            selection_rolls=(0,),
            birth_rolls=(
                EnemyBirthRolls(
                    level_roll=1,
                    birth_offsets=(0,0,0,0),
                    spawn_allocation_rolls=(0,1,2,3,0,1,2,3,0,1),
                ),
            ),
        )
        original=context.spawned_enemies[0]
        caster_id=str(context.battle.enemies[0].participant_id)
        ally_id="enemy:relife-dead"

        self.stack.petskill_runtime=Recovered25PetSkillRuntime(
            skills={
                **dict(self.stack.petskill_runtime.skills),
                500:Recovered25PetSkillEntry(
                    skill_id=500,
                    field=1,
                    target=2,
                    cost=2,
                    illegal=0,
                    function_name="ENEMYSKILL_ReLife",
                    option_bytes=b"",
                ),
            },
            source_file=self.stack.petskill_runtime.source_file,
        )
        caster_participant=replace(
            context.battle.enemies[0],
            hp=600,max_hp=600,quick=200,
        )
        ally_participant=replace(
            context.battle.enemies[0],
            participant_id=ally_id,
            hp=0,max_hp=101,quick=20,
        )
        caster_spawn=replace(
            original,
            participant=caster_participant,
            template=replace(
                original.template,
                tempno=39,
                graphic_id=100370,
                skill_ids=(20,30,40,50,500,60,70),
                skill_slot_ids=(20,30,40,50,500,60,70),
            ),
            variant=replace(
                original.variant,
                tactics_option=(
                    "at:0;1;1|gu:0|es:0|"
                    "wa:0;0;0;0;1;0;0"
                ),
            ),
        )
        ally_spawn=replace(
            original,
            participant=ally_participant,
            variant=replace(
                original.variant,
                tactics_option="at:0;1;1|gu:1|es:0|wa:0;0;0;0;0;0;0",
            ),
        )
        context=replace(
            context,
            battle=replace(
                context.battle,
                player=replace(
                    context.battle.player,
                    hp=1000,max_hp=1000,quick=10,
                ),
                enemies=(caster_participant,ally_participant),
            ),
            spawned_enemies=(caster_spawn,ally_spawn),
        )
        context=self.coordinator.begin_persistent_group_battle(
            context,
            slots={"player":0,caster_id:10,ally_id:11},
        )
        context=replace(
            context,
            persistent_battle_state=replace(
                context.persistent_battle_state,
                revivable_dead_participant_ids=(ally_id,),
            ),
        )
        profiles={
            "player":BattleCombatProfile(
                fixed_dex=10,fixed_luck=0,
                earth=0,water=0,fire=0,wind=0,
            ),
            caster_id:BattleCombatProfile(
                fixed_dex=100,fixed_luck=0,
                earth=0,water=0,fire=0,wind=0,
            ),
            ally_id:BattleCombatProfile(
                fixed_dex=10,fixed_luck=0,
                earth=0,water=0,fire=0,wind=0,
            ),
        }
        next_context,result=(
            self.coordinator
            .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
                context,
                player_side_commands={
                    "player":BattleCommand(BATTLE_COM_WAIT)
                },
                enemy_mode_rolls={caster_id:0},
                enemy_target_rolls={caster_id:0},
                enemy_escape_rolls={},
                opponent_abio_by_participant_id={},
                initiative_random_subtracts={
                    "player":0,caster_id:0,
                },
                profiles=profiles,
                attack_rolls={},
                defense_profile="newpower_70pct",
                enemy_relife_rolls_by_attack_id={
                    caster_id:EnemyReLifeRolls(0,55),
                },
                enemy_relife_retarget_rolls_by_attack_id={
                    caster_id:None,
                },
            )
        )
        event=next(
            event for event in result.round.events
            if event.participant_id==caster_id
            and event.result=="enemy_relife"
        )
        self.assertEqual(event.resolved_target_slot,11)
        self.assertEqual(
            event.enemy_relife_resolution.selected_participant_id,
            ally_id,
        )
        self.assertEqual(
            next_context.persistent_battle_state.hp_by_participant_id[
                ally_id
            ],
            55,
        )
        self.assertEqual(
            next_context.persistent_battle_state
            .revivable_dead_participant_ids,
            (),
        )


if __name__ == "__main__":
    unittest.main()
