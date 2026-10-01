#!/usr/bin/env python3
"""Engine-neutral local runtime session coordinator.

This application layer sits above a concrete recovered25 local runtime stack.
It owns session lifecycle and command ordering, but deliberately does not own
rendering, input devices, RNG, legacy networking, account services, or an
unproven collision decoder.

Ordinary movement therefore requires an explicit collision verdict from a
validated collision layer. Classic overlap-Warp resolution is delegated to the
already-tested historical world model. Dialogue/state-gated transitions are
spatially checked against their recovered source rectangle before the live gate
evaluator is consulted.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from tools.stoneage_enemy_spawn_model import (
    EnemyBirthRolls,
    SpawnedEnemy,
)
from tools.stoneage_enemy_ai_petskill_bridge import (
    resolve_enemy_ai_supported_petskill_command,
)
from tools.stoneage_enemy_ai_model import (
    ATTACK as ENEMY_AI_ATTACK,
    ESCAPE as ENEMY_AI_ESCAPE,
    GUARD as ENEMY_AI_GUARD,
    SKILL as ENEMY_AI_SKILL,
    EnemyAiTarget,
    resolve_common_normal_enemy_ai,
)
from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_CAPTURE,
    BATTLE_COM_ESCAPE,
    BATTLE_COM_GUARD,
    BATTLE_COM_S_CHARGE,
    BATTLE_COM_S_RENZOKU,
    BATTLE_COM_S_STATUSCHANGE,
    BATTLE_COM_S_ABDUCT,
    BATTLE_COM_WAIT,
    BattleCombatProfile,
    BattleCommand,
    BattleCommandSetupEffects,
    ContinuationAttackRolls,
    CounterAttemptRolls,
    OrdinaryAttackRolls,
    OrdinaryCaptureContext,
    OrdinaryCaptureRolls,
    OrdinaryAbductContext,
    OrdinaryAbductRolls,
    OrdinaryEscapeContext,
    OrdinaryEscapeRolls,
)
from tools.stoneage_battle_status_model import (
    BaseStatusCombatProfile,
    BaseStatusTurnRolls,
)
from tools.stoneage_battle_state_model import (
    PersistentBattleState,
    PersistentRoundResult,
    begin_persistent_battle,
    resolve_persistent_ordinary_round,
)
from tools.stoneage_encounter_frequency_model import (
    EncounterFrequencyDecision,
    EncounterFrequencyState,
    refresh_frequency_bounds,
    resolve_frequency_step,
)
from tools.stoneage_map_collision_model import (
    CollisionDecision,
    DynamicOccupant,
)
from tools.stoneage_player_death_model import (
    death_transition,
    resurrect_transition,
)
from tools.stoneage_runtime_dynamic_occupancy import (
    resolve_runtime_collision_with_occupancy,
)
from tools.stoneage_runtime_occupancy_registry import (
    RuntimeDynamicOccupancyRegistry,
)
from tools.stoneage_local_runtime_core import (
    LOCAL_SESSION_SCHEMA,
    LocalPersistenceStore,
    LocalRuntimeSessionState,
    MaterializedWorldRegion,
    TransitionGateDecision,
    decode_local_runtime_session,
)
from tools.stoneage_local_runtime_save import (
    LOCAL_RUNTIME_SAVE_SCHEMA,
    LocalRuntimeSaveSnapshot,
    build_initial_occupancy_registry,
    build_local_runtime_occupancy_delta,
    decode_local_runtime_save,
    encode_local_runtime_save,
    local_runtime_payload_schema,
    restore_local_runtime_occupancy_registry,
)
from tools.stoneage_singleplayer_battle import (
    BattleOutcome,
    BattleSession,
    apply_battle_outcome,
    begin_group_battle,
)
from tools.stoneage_singleplayer_domain import (
    EncounterRequest,
    EncounterRolls,
    GroupEncounterRequest,
    MapPosition,
    PetActor,
    SinglePlayerHistoricalDomain,
)
from tools.stoneage_singleplayer_runtime import (
    SinglePlayerHistoricalRuntime,
)
from tools.stoneage_singleplayer_persistence import (
    decode_persistent_state,
    encode_persistent_state,
)
from tools.stoneage_singleplayer_world import (
    WalkResolution,
    place_player_on_topology,
    resolve_player_walk,
)
from tools.stoneage_tw10_25_encounter_bridge import (
    active_encounter_area,
)


@dataclass(frozen=True)
class LocalRuntimeWalkResult:
    session: LocalRuntimeSessionState
    resolution: WalkResolution
    collision: CollisionDecision | None = None
    collision_provider_kind: str | None = None
    collision_evidence_class: str | None = None
    collision_semantic_profile: str | None = None
    collision_exact_binary_proof: bool | None = None
    static_collision: CollisionDecision | None = None
    dynamic_collision: CollisionDecision | None = None
    dynamic_occupancy_profile: str | None = None
    dynamic_occupancy_evidence_class: str | None = None
    live_occupancy_registry_profile: str | None = None
    live_occupancy_object_ids: tuple[str, ...] = ()
    live_occupancy_provenance: tuple[str, ...] = ()


@dataclass(frozen=True)
class LocalRuntimeEncounterWalkResult:
    """One ordinary movement result plus descendant CEP/encounter resolution."""

    walk: LocalRuntimeWalkResult
    frequency: EncounterFrequencyDecision | None
    group_encounter: GroupEncounterRequest | None = None
    encounter: EncounterRequest | None = None

    @property
    def session(self) -> LocalRuntimeSessionState:
        return self.walk.session


@dataclass(frozen=True)
class LocalRuntimeBattleContext:
    """Transient local battle shell over a cloned persistent-state snapshot."""

    contract_id: str
    world_profile: str
    hometown_ordinal: int
    origin_position: MapPosition
    world_flags: frozenset[str]
    persistent_state_payload: str
    battle: BattleSession
    spawned_enemies: tuple[SpawnedEnemy, ...]
    persistent_battle_state: PersistentBattleState | None = None
    working_persistent_state_payload: str | None = None

    def __post_init__(self) -> None:
        if not str(self.contract_id).strip():
            raise ValueError("battle context contract_id must be non-empty")
        if not str(self.world_profile).strip():
            raise ValueError("battle context world_profile must be non-empty")
        if int(self.hometown_ordinal) not in {1, 2, 3, 4}:
            raise ValueError("battle context hometown ordinal must be 1..4")
        if self.battle.origin_position != self.origin_position:
            raise ValueError("battle context origin/battle position drift")
        object.__setattr__(
            self,
            "world_flags",
            frozenset(str(x) for x in self.world_flags),
        )
        object.__setattr__(
            self,
            "spawned_enemies",
            tuple(self.spawned_enemies),
        )
        if self.persistent_battle_state is not None:
            if (
                self.persistent_battle_state.session.origin_position
                != self.origin_position
            ):
                raise ValueError("persistent battle origin drift")
            if (
                self.persistent_battle_state.session.player.participant_id
                != self.battle.player.participant_id
            ):
                raise ValueError("persistent battle player identity drift")
        if self.working_persistent_state_payload is not None:
            if not str(self.working_persistent_state_payload).strip():
                raise ValueError("working persistent payload must be non-empty")


@dataclass(frozen=True)
class LocalRuntimePlayerDeathPlan:
    """Explicit core_Dying plan; world drop/party actions remain external."""

    session: LocalRuntimeSessionState
    party_discharged: bool
    item_drop_mode: str
    requested_item_drop_slots: tuple[int, ...]
    random_item_drop_candidates: tuple[int, ...]
    random_item_drop_count: int
    requested_ground_gold: int
    final_carried_gold: int
    dead_count_after: int
    cleared_statuses: tuple[str, ...]
    is_dead: bool
    is_attacked: bool


@dataclass(frozen=True)
class LocalRuntimePlayerResurrectionResult:
    """In-place CHAR_playerresurrect projection without warp or MP refill."""

    session: LocalRuntimeSessionState
    base_image_restored: bool
    is_dead: bool
    is_attacked: bool
    is_overed: bool
    mp_unchanged: bool
    location_unchanged: bool


@dataclass(frozen=True)
class LocalRuntimeTransitionResult:
    session: LocalRuntimeSessionState
    decision: TransitionGateDecision


@dataclass(frozen=True)
class LocalRuntimeInteraction:
    """Presentation-safe view of one spatially available recovered interaction."""

    transition_id: str
    interaction_kind: str
    allowed: bool
    reason: str
    provenance: Mapping[str, Any]
    execution_supported: bool

    def __post_init__(self) -> None:
        transition_id = str(self.transition_id).strip()
        interaction_kind = str(self.interaction_kind).strip()
        reason = str(self.reason).strip()
        if not transition_id:
            raise ValueError("runtime interaction transition_id must be non-empty")
        if not interaction_kind:
            raise ValueError("runtime interaction kind must be non-empty")
        if not reason:
            raise ValueError("runtime interaction reason must be non-empty")
        object.__setattr__(self, "transition_id", transition_id)
        object.__setattr__(self, "interaction_kind", interaction_kind)
        object.__setattr__(self, "allowed", bool(self.allowed))
        object.__setattr__(self, "reason", reason)
        object.__setattr__(
            self,
            "provenance",
            MappingProxyType(dict(self.provenance)),
        )
        object.__setattr__(
            self,
            "execution_supported",
            bool(self.execution_supported),
        )


class InMemoryLocalPersistenceStore:
    """Small deterministic LocalPersistenceStore implementation for composition/tests."""

    def __init__(self) -> None:
        self._rows: dict[str, str] = {}

    def save(self, key: str, payload: str) -> None:
        key = _nonempty_key(key)
        self._rows[key] = str(payload)

    def load(self, key: str) -> str | None:
        key = _nonempty_key(key)
        return self._rows.get(key)

    @property
    def rows(self) -> Mapping[str, str]:
        return MappingProxyType(dict(self._rows))


def _nonempty_key(value: str) -> str:
    key = str(value).strip()
    if not key:
        raise ValueError("local save key must be non-empty")
    return key


@dataclass(frozen=True)
class EnemyAiCommonCommandBatch:
    commands: Mapping[str, BattleCommand]
    setup_effects: Mapping[str, BattleCommandSetupEffects]
    abduct_contexts: Mapping[str, OrdinaryAbductContext] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "commands",
            MappingProxyType({
                str(key): value for key, value in self.commands.items()
            }),
        )
        object.__setattr__(
            self,
            "setup_effects",
            MappingProxyType({
                str(key): value for key, value in self.setup_effects.items()
            }),
        )
        unknown = sorted(set(self.setup_effects) - set(self.commands))
        if unknown:
            raise ValueError(
                "enemy AI setup effects lack matching command actors: "
                + ",".join(unknown)
            )
        contexts={
            str(key):value for key,value in self.abduct_contexts.items()
        }
        object.__setattr__(
            self,
            "abduct_contexts",
            MappingProxyType(contexts),
        )
        abduct_command_ids={
            str(pid) for pid,command in self.commands.items()
            if int(command.command1)==BATTLE_COM_S_ABDUCT
        }
        if set(contexts) != abduct_command_ids:
            raise ValueError(
                "enemy AI Abduct contexts must match exactly S_ABDUCT actors"
            )
        if any(
            not isinstance(value,OrdinaryAbductContext)
            for value in contexts.values()
        ):
            raise TypeError("enemy AI Abduct context has wrong type")


@dataclass
class LocalRuntimeSessionCoordinator:
    """Application-service boundary for one authoritative local play session."""

    stack: object
    persistence: LocalPersistenceStore
    occupancy_registry: RuntimeDynamicOccupancyRegistry = field(
        default_factory=RuntimeDynamicOccupancyRegistry
    )
    encounter_frequency: EncounterFrequencyState = field(
        default_factory=EncounterFrequencyState
    )

    def __post_init__(self) -> None:
        initial_occupancy = self._initial_occupancy()
        if initial_occupancy is not None:
            initial_occupancy.populate_registry(self.occupancy_registry)

    def _initial_occupancy(self):
        return getattr(self.stack, "npc_initial_occupancy", None)

    def _validate_occupancy_registry(
        self,
        registry: RuntimeDynamicOccupancyRegistry,
    ) -> RuntimeDynamicOccupancyRegistry:
        if not isinstance(registry, RuntimeDynamicOccupancyRegistry):
            raise TypeError("session coordinator occupancy registry type mismatch")
        invalid = tuple(
            obj.object_id
            for obj in registry.objects.values()
            if not self.topology.is_valid_position(obj.position)
        )
        if invalid:
            raise ValueError(
                "session coordinator occupancy object outside topology: "
                + ",".join(invalid[:5])
            )
        return registry

    def _reset_occupancy_to_initial(self) -> None:
        self.occupancy_registry = self._validate_occupancy_registry(
            build_initial_occupancy_registry(self._initial_occupancy())
        )

    def _reset_encounter_frequency(self) -> None:
        # CEP is stable-descendant connection/runtime state, not player save data.
        self.encounter_frequency = EncounterFrequencyState()

    @property
    def profile(self):
        return self.stack.profile

    @property
    def topology(self):
        return self.stack.world_adapter.topology

    def _validate_session(
        self,
        session: LocalRuntimeSessionState,
    ) -> LocalRuntimeSessionState:
        if session.contract_id != self.profile.contract_id:
            raise ValueError("session coordinator bootstrap contract mismatch")
        if session.world_profile != self.profile.runtime_world_profile:
            raise ValueError("session coordinator world-profile mismatch")
        if not self.topology.is_valid_position(session.player_position):
            raise ValueError("session coordinator player position is outside topology")
        return session

    def new_game(self, hometown_ordinal: int) -> LocalRuntimeSessionState:
        seed = self.stack.create_fresh_start(int(hometown_ordinal))
        session = LocalRuntimeSessionState(
            contract_id=seed.contract_id,
            world_profile=seed.world_profile,
            hometown_ordinal=seed.hometown_ordinal,
            player_position=seed.position,
            player_state=seed.player_state,
        )
        session = self._validate_session(session)
        self._reset_occupancy_to_initial()
        self._reset_encounter_frequency()
        return session

    def save_game(
        self,
        key: str,
        session: LocalRuntimeSessionState,
    ) -> None:
        session = self._validate_session(session)
        self._validate_occupancy_registry(self.occupancy_registry)
        snapshot = LocalRuntimeSaveSnapshot(
            session=session,
            occupancy=build_local_runtime_occupancy_delta(
                registry=self.occupancy_registry,
                initial_occupancy=self._initial_occupancy(),
            ),
        )
        self.persistence.save(
            _nonempty_key(key),
            encode_local_runtime_save(snapshot),
        )

    def continue_game(self, key: str) -> LocalRuntimeSessionState:
        payload = self.persistence.load(_nonempty_key(key))
        if payload is None:
            raise KeyError(f"local save does not exist: {key}")

        schema = local_runtime_payload_schema(payload)
        if schema == LOCAL_RUNTIME_SAVE_SCHEMA:
            snapshot = decode_local_runtime_save(
                payload,
                expected_contract_id=self.profile.contract_id,
                expected_world_profile=self.profile.runtime_world_profile,
            )
            session = self._validate_session(snapshot.session)
            restored = restore_local_runtime_occupancy_registry(
                delta=snapshot.occupancy,
                initial_occupancy=self._initial_occupancy(),
            )
            self.occupancy_registry = self._validate_occupancy_registry(restored)
            self._reset_encounter_frequency()
            return session

        if schema == LOCAL_SESSION_SCHEMA:
            session = decode_local_runtime_session(
                payload,
                expected_contract_id=self.profile.contract_id,
                expected_world_profile=self.profile.runtime_world_profile,
            )
            session = self._validate_session(session)
            self._reset_occupancy_to_initial()
            self._reset_encounter_frequency()
            return session

        raise ValueError(f"unsupported local persistence schema: {schema}")

    def plan_player_core_dying(
        self,
        session: LocalRuntimeSessionState,
        *,
        attacker_class: str,
        equipped_slots: Sequence[int],
        dead_count_before: int,
    ) -> LocalRuntimePlayerDeathPlan:
        """Apply only representable core_Dying persistence and return world actions.

        The historical callback's party discharge, equipment-drop requests,
        hidden death/status flags and dead-count mutation are returned
        semantically because the current local session has no authoritative
        party/equipment/hidden-player-state container. The v1-direct carried
        gold field is representable and is set to zero on a cloned session.
        """

        session = self._validate_session(session)
        if session.player_state.character is None:
            raise ValueError("player death requires persistent character state")
        fields = dict(session.player_state.character.fields)
        if "gold" not in fields:
            raise ValueError("player death requires v1-direct gold field")

        transition = death_transition(
            int(fields["gold"]),
            tuple(int(x) for x in equipped_slots),
            str(attacker_class),
            dead_count=int(dead_count_before),
        )

        working = decode_persistent_state(
            encode_persistent_state(session.player_state)
        )
        if working.character is None:
            raise ValueError("player death clone lost character state")
        next_fields = dict(working.character.fields)
        next_fields["gold"] = int(transition["final_carried_gold"])
        working.character = replace(
            working.character,
            fields=MappingProxyType(next_fields),
        )
        updated = replace(
            session,
            player_state=working,
        )
        self._validate_session(updated)

        return LocalRuntimePlayerDeathPlan(
            session=updated,
            party_discharged=bool(transition["party_discharged"]),
            item_drop_mode=str(transition["item_drop_mode"]),
            requested_item_drop_slots=tuple(
                int(x) for x in transition["requested_item_drop_slots"]
            ),
            random_item_drop_candidates=tuple(
                int(x) for x in transition["random_item_drop_candidates"]
            ),
            random_item_drop_count=int(
                transition["random_item_drop_count"]
            ),
            requested_ground_gold=int(
                transition["requested_ground_gold"]
            ),
            final_carried_gold=int(transition["final_carried_gold"]),
            dead_count_after=int(transition["dead_count"]),
            cleared_statuses=tuple(
                str(x) for x in transition["cleared_statuses"]
            ),
            is_dead=bool(transition["is_dead"]),
            is_attacked=bool(transition["is_attacked"]),
        )

    def resurrect_player_in_place(
        self,
        session: LocalRuntimeSessionState,
        *,
        requested_hp: int,
    ) -> LocalRuntimePlayerResurrectionResult:
        """Apply explicit in-place CHAR_playerresurrect HP semantics only."""

        session = self._validate_session(session)
        if session.player_state.character is None:
            raise ValueError("player resurrection requires character state")
        fields = dict(session.player_state.character.fields)
        if "max_hp" not in fields or "hp" not in fields:
            raise ValueError("player resurrection requires hp/max_hp fields")

        transition = resurrect_transition(
            int(requested_hp),
            int(fields["max_hp"]),
        )
        working = decode_persistent_state(
            encode_persistent_state(session.player_state)
        )
        if working.character is None:
            raise ValueError("player resurrection clone lost character state")
        next_fields = dict(working.character.fields)
        next_fields["hp"] = int(transition["hp"])
        working.character = replace(
            working.character,
            fields=MappingProxyType(next_fields),
        )
        updated = replace(
            session,
            player_state=working,
        )
        self._validate_session(updated)

        return LocalRuntimePlayerResurrectionResult(
            session=updated,
            base_image_restored=bool(
                transition["base_image_restored"]
            ),
            is_dead=bool(transition["is_dead"]),
            is_attacked=bool(transition["is_attacked"]),
            is_overed=bool(transition["is_overed"]),
            mp_unchanged=bool(transition["mp_unchanged"]),
            location_unchanged=bool(
                transition["location_unchanged"]
            ),
        )

    def materialize_current_region(
        self,
        session: LocalRuntimeSessionState,
    ) -> MaterializedWorldRegion:
        session = self._validate_session(session)
        return self.stack.materialize_player_position(session)

    def walk_one_cell(
        self,
        session: LocalRuntimeSessionState,
        *,
        destination: MapPosition,
        entry_allowed: bool,
        map_objmove_ok: bool = True,
    ) -> LocalRuntimeWalkResult:
        """Execute one ordinary walk attempt from an explicit collision verdict.

        The coordinator refuses to infer collision from raw DAT/LS2MAP ids. The
        caller must supply entry_allowed from the selected validated collision
        adapter. This method enforces the ordinary one-cell command shape and
        delegates classic overlap-Warp behavior to resolve_player_walk().
        """

        session = self._validate_session(session)
        origin = session.player_position
        if int(destination.floor_id) != int(origin.floor_id):
            raise ValueError("ordinary walk command cannot change floor directly")
        dx = int(destination.x) - int(origin.x)
        dy = int(destination.y) - int(origin.y)
        if dx == 0 and dy == 0:
            raise ValueError("ordinary walk command cannot be zero-length")
        if abs(dx) > 1 or abs(dy) > 1:
            raise ValueError("ordinary walk command exceeds one cell")

        domain = SinglePlayerHistoricalDomain(persistent=session.player_state)
        place_player_on_topology(domain, self.topology, origin)
        resolution = resolve_player_walk(
            domain,
            self.topology,
            destination=destination,
            entry_allowed=bool(entry_allowed),
            action_is_walk=True,
            map_objmove_ok=bool(map_objmove_ok),
        )
        updated = replace(session, player_position=resolution.final_position)
        self._validate_session(updated)
        return LocalRuntimeWalkResult(
            session=updated,
            resolution=resolution,
        )

    def walk_one_cell_with_server_collision(
        self,
        session: LocalRuntimeSessionState,
        *,
        destination: MapPosition,
        destination_occupants: Sequence[DynamicOccupant] = (),
        is_flying: bool = False,
        map_objmove_ok: bool = True,
    ) -> LocalRuntimeWalkResult:
        """Resolve one step through the stack's provenance-safe server provider."""
        session = self._validate_session(session)
        provider = getattr(self.stack, "collision_provider", None)
        if provider is None:
            raise ValueError("runtime stack has no server collision provider")
        verdict = provider.ordinary_step_verdict(
            origin=session.player_position,
            destination=destination,
            destination_occupants=tuple(destination_occupants),
            is_flying=bool(is_flying),
        )
        result = self.walk_one_cell(
            session,
            destination=destination,
            entry_allowed=verdict.allowed,
            map_objmove_ok=bool(map_objmove_ok),
        )
        return LocalRuntimeWalkResult(
            session=result.session,
            resolution=result.resolution,
            collision=verdict,
        )

    def walk_one_cell_with_runtime_collision(
        self,
        session: LocalRuntimeSessionState,
        *,
        destination: MapPosition,
        destination_occupants: Sequence[DynamicOccupant] = (),
        map_objmove_ok: bool = True,
    ) -> LocalRuntimeWalkResult:
        """Resolve static routed collision, then independent live occupancy."""
        session = self._validate_session(session)
        router = getattr(self.stack, "collision_router", None)
        if router is None:
            raise ValueError("runtime stack has no unified collision router")
        live_query = self.occupancy_registry.query(destination)
        layered = resolve_runtime_collision_with_occupancy(
            router=router,
            origin=session.player_position,
            destination=destination,
            destination_occupants=(
                live_query.occupants + tuple(destination_occupants)
            ),
        )
        routed = layered.static
        result = self.walk_one_cell(
            session,
            destination=destination,
            entry_allowed=layered.decision.allowed,
            map_objmove_ok=bool(map_objmove_ok),
        )
        return LocalRuntimeWalkResult(
            session=result.session,
            resolution=result.resolution,
            collision=layered.decision,
            collision_provider_kind=routed.route.provider_kind,
            collision_evidence_class=routed.route.evidence_class,
            collision_semantic_profile=routed.route.semantic_profile,
            collision_exact_binary_proof=(
                routed.route.exact_recovered25_binary_proof
            ),
            static_collision=routed.decision,
            dynamic_collision=layered.dynamic,
            dynamic_occupancy_profile=layered.dynamic_profile,
            dynamic_occupancy_evidence_class=layered.dynamic_evidence_class,
            live_occupancy_registry_profile=self.occupancy_registry.profile_id,
            live_occupancy_object_ids=live_query.object_ids,
            live_occupancy_provenance=live_query.provenances,
        )

    def walk_one_cell_with_runtime_collision_and_encounter_frequency(
        self,
        session: LocalRuntimeSessionState,
        *,
        destination: MapPosition,
        frequency_roll: int | None,
        encounter_rolls: EncounterRolls,
        destination_occupants: Sequence[DynamicOccupant] = (),
        map_objmove_ok: bool = True,
        encounter_eligible: bool = True,
    ) -> LocalRuntimeEncounterWalkResult:
        """Compose ordinary movement with the reconstructed descendant CEP loop.

        Random values remain explicit caller inputs. CEP is transient runtime
        state and is not serialized into the local player/session save.
        """

        session = self._validate_session(session)
        encounter_runtime = getattr(self.stack, "encounter_runtime", None)
        if encounter_runtime is None:
            raise ValueError("runtime stack has no encounter runtime")
        if not isinstance(encounter_rolls, EncounterRolls):
            raise TypeError("encounter_rolls must be EncounterRolls")

        origin = session.player_position
        walk = self.walk_one_cell_with_runtime_collision(
            session,
            destination=destination,
            destination_occupants=destination_occupants,
            map_objmove_ok=bool(map_objmove_ok),
        )
        if not walk.resolution.moved:
            return LocalRuntimeEncounterWalkResult(
                walk=walk,
                frequency=None,
            )

        source_area = active_encounter_area(
            encounter_runtime.encounter_areas,
            floor=origin.floor_id,
            x=origin.x,
            y=origin.y,
        )
        refreshed = refresh_frequency_bounds(
            self.encounter_frequency,
            source_area,
        )
        frequency = resolve_frequency_step(
            refreshed,
            roll=frequency_roll,
            encounter_enabled=not walk.resolution.encounter_suppressed,
            eligible=bool(encounter_eligible),
        )
        self.encounter_frequency = frequency.after

        group_encounter = None
        encounter = None
        if frequency.encounter_triggered:
            group_encounter = self.stack.request_encounter_group(
                walk.session,
                group_roll=encounter_rolls.group_roll,
            )
            encounter = self.stack.request_encounter(
                walk.session,
                group_roll=encounter_rolls.group_roll,
                enemy_roll=encounter_rolls.enemy_roll,
                level_roll=encounter_rolls.level_roll,
            )

        return LocalRuntimeEncounterWalkResult(
            walk=walk,
            frequency=frequency,
            group_encounter=group_encounter,
            encounter=encounter,
        )

    @staticmethod
    def _battle_working_persistent_payload(
        context: LocalRuntimeBattleContext,
    ) -> str:
        return (
            context.persistent_state_payload
            if context.working_persistent_state_payload is None
            else context.working_persistent_state_payload
        )

    def start_group_battle(
        self,
        session: LocalRuntimeSessionState,
        encounter: GroupEncounterRequest,
        *,
        entry_count_roll: int,
        selection_rolls: Sequence[int],
        birth_rolls: Sequence[EnemyBirthRolls],
        allied_pet_slots: Sequence[int] = (),
        ride_pet_slot: int | None = None,
    ) -> LocalRuntimeBattleContext:
        """Start a transient group battle from explicit recovered spawn rolls."""

        session = self._validate_session(session)
        if encounter.position != session.player_position:
            raise ValueError(
                "group encounter position does not match authoritative session"
            )
        encounter_runtime = getattr(self.stack, "encounter_runtime", None)
        if encounter_runtime is None:
            raise ValueError("runtime stack has no encounter runtime")

        persistent_payload = encode_persistent_state(session.player_state)
        working_state = decode_persistent_state(persistent_payload)
        domain = SinglePlayerHistoricalDomain(
            static=encounter_runtime.static_data,
            persistent=working_state,
        )
        domain.move_player(
            floor_id=session.player_position.floor_id,
            x=session.player_position.x,
            y=session.player_position.y,
        )

        spawned = tuple(
            self.stack.spawn_group_enemies(
                encounter,
                entry_count_roll=int(entry_count_roll),
                selection_rolls=tuple(int(x) for x in selection_rolls),
                birth_rolls=tuple(birth_rolls),
            )
        )
        battle = begin_group_battle(
            domain,
            encounter,
            enemies=tuple(row.participant for row in spawned),
            allied_pet_slots=tuple(int(x) for x in allied_pet_slots),
            ride_pet_slot=(
                None if ride_pet_slot is None else int(ride_pet_slot)
            ),
        )
        return LocalRuntimeBattleContext(
            contract_id=session.contract_id,
            world_profile=session.world_profile,
            hometown_ordinal=session.hometown_ordinal,
            origin_position=session.player_position,
            world_flags=session.world_flags,
            persistent_state_payload=persistent_payload,
            battle=battle,
            spawned_enemies=spawned,
        )

    def settle_group_battle(
        self,
        context: LocalRuntimeBattleContext,
        outcome: BattleOutcome,
    ) -> LocalRuntimeSessionState:
        """Apply one explicit outcome to the battle snapshot and return a new session."""

        if context.contract_id != self.profile.contract_id:
            raise ValueError("battle context bootstrap contract mismatch")
        if context.world_profile != self.profile.runtime_world_profile:
            raise ValueError("battle context world-profile mismatch")
        if not self.topology.is_valid_position(context.origin_position):
            raise ValueError("battle context origin is outside topology")

        encounter_runtime = getattr(self.stack, "encounter_runtime", None)
        if encounter_runtime is None:
            raise ValueError("runtime stack has no encounter runtime")

        working_state = decode_persistent_state(
            self._battle_working_persistent_payload(context)
        )
        domain = SinglePlayerHistoricalDomain(
            static=encounter_runtime.static_data,
            persistent=working_state,
        )
        domain.move_player(
            floor_id=context.origin_position.floor_id,
            x=context.origin_position.x,
            y=context.origin_position.y,
        )
        apply_battle_outcome(
            domain,
            context.battle,
            outcome,
        )
        updated = LocalRuntimeSessionState(
            contract_id=context.contract_id,
            world_profile=context.world_profile,
            hometown_ordinal=context.hometown_ordinal,
            player_position=context.origin_position,
            player_state=domain.persistent,
            world_flags=context.world_flags,
        )
        return self._validate_session(updated)

    def begin_persistent_group_battle(
        self,
        context: LocalRuntimeBattleContext,
        *,
        slots: Mapping[str, int],
    ) -> LocalRuntimeBattleContext:
        """Promote a transient group battle shell into multi-round state."""

        if context.persistent_battle_state is not None:
            raise ValueError("battle context already has persistent state")
        state = begin_persistent_battle(
            context.battle,
            slots={str(key): int(value) for key, value in slots.items()},
        )
        return replace(
            context,
            persistent_battle_state=state,
        )

    def _build_persistent_enemy_common_batch(
        self,
        context: LocalRuntimeBattleContext,
        *,
        mode_rolls_by_enemy_id: Mapping[str, int],
        target_rolls_by_enemy_id: Mapping[str, int] | None = None,
        allow_escape: bool = False,
        allow_basic_skill: bool = False,
        allow_statuschange_skill: bool = False,
        allow_powerbalance_skill: bool = False,
        allow_mighty_skill: bool = False,
        allow_guardbreak_skill: bool = False,
        allow_continuationattack_skill: bool = False,
        allow_chargeattack_skill: bool = False,
        allow_noguard_skill: bool = False,
        allow_abduct_skill: bool = False,
    ) -> EnemyAiCommonCommandBatch:
        """Derive the evidence-closed common enemy-AI command subset.

        ATTACK/GUARD are always available here. ESCAPE is emitted only when the
        caller explicitly opens that execution seam; its probability context
        and RAND(1,100) input are handled separately by the round coordinator.
        A selected wa slot is admitted only when its explicitly enabled
        pet-skill execution seam is closed. Command-submission setup effects
        remain separate from COM1/COM2/COM3 and are returned in the batch.
        All other skill, magic-failure and extension paths remain fail-closed.
        """

        state = context.persistent_battle_state
        if state is None:
            raise ValueError("battle context has no persistent battle state")
        if state.phase != "active":
            raise ValueError("cannot derive enemy AI after battle termination")

        participants = (
            state.session.player,
            *state.session.allied_pets,
            *state.session.enemies,
        )
        inactive_ids=set(state.ultimate_exited_participant_ids)
        inactive_ids.update(state.battle_exited_participant_ids)
        living = {
            str(participant.participant_id): participant
            for participant in participants
            if (
                str(participant.participant_id) in state.hp_by_participant_id
                and str(participant.participant_id) not in inactive_ids
                and int(
                    state.hp_by_participant_id[
                        str(participant.participant_id)
                    ]
                ) > 0
            )
        }
        living_enemy_ids = tuple(
            str(enemy.participant_id)
            for enemy in state.session.enemies
            if str(enemy.participant_id) in living
        )
        carried_enemy_ids={
            enemy_id
            for enemy_id in living_enemy_ids
            if (
                enemy_id in state.carried_commands_by_participant_id
                and int(
                    state.carried_commands_by_participant_id[
                        enemy_id
                    ].command1
                ) == BATTLE_COM_S_CHARGE
            )
        }
        ai_enemy_ids=tuple(
            enemy_id
            for enemy_id in living_enemy_ids
            if enemy_id not in carried_enemy_ids
        )
        supplied_mode_ids = {str(key) for key in mode_rolls_by_enemy_id}
        if supplied_mode_ids != set(ai_enemy_ids):
            missing = sorted(set(ai_enemy_ids) - supplied_mode_ids)
            extra = sorted(supplied_mode_ids - set(ai_enemy_ids))
            raise ValueError(
                "enemy AI mode rolls must cover exactly non-carried living "
                f"enemies; missing={missing}, extra={extra}"
            )

        target_rolls = {
            str(key): int(value)
            for key, value in (target_rolls_by_enemy_id or {}).items()
        }
        unknown_target_rolls = sorted(
            set(target_rolls) - set(ai_enemy_ids)
        )
        if unknown_target_rolls:
            raise ValueError(
                "enemy AI target rolls reference non-AI enemies: "
                + ",".join(unknown_target_rolls)
            )

        spawn_by_participant_id = {}
        for spawned in context.spawned_enemies:
            participant_id = str(spawned.participant.participant_id)
            if participant_id in spawn_by_participant_id:
                raise ValueError(
                    "duplicate spawned-enemy participant identity: "
                    + participant_id
                )
            spawn_by_participant_id[participant_id] = spawned

        targets = []
        for participant in (
            state.session.player,
            *state.session.allied_pets,
        ):
            participant_id = str(participant.participant_id)
            if participant_id not in living:
                continue
            if participant_id not in state.slots:
                raise ValueError(
                    "living enemy-AI target lacks battle slot: "
                    + participant_id
                )
            slot = int(state.slots[participant_id])
            if not 0 <= slot < 10:
                raise ValueError(
                    "enemy-AI opposing target is outside player-side slots: "
                    + participant_id
                )
            kind = (
                participant.kind
                if participant.kind in {"player", "pet"}
                else "other"
            )
            targets.append(
                EnemyAiTarget(
                    slot=slot,
                    participant_id=participant_id,
                    kind=kind,
                    hp=int(state.hp_by_participant_id[participant_id]),
                    alive=True,
                    rescue_mode=False,
                )
            )

        commands = {
            enemy_id:state.carried_commands_by_participant_id[enemy_id]
            for enemy_id in carried_enemy_ids
        }
        setup_effects = {
            enemy_id:state.carried_setup_effects_by_participant_id[enemy_id]
            for enemy_id in carried_enemy_ids
        }
        abduct_contexts={}
        for enemy_id in ai_enemy_ids:
            if enemy_id not in spawn_by_participant_id:
                raise ValueError(
                    "living enemy lacks recovered spawn provenance: "
                    + enemy_id
                )
            spawned = spawn_by_participant_id[enemy_id]
            variant = spawned.variant
            if int(variant.tactics) != 1:
                raise ValueError(
                    f"enemy {enemy_id} uses unsupported TACTICS mode "
                    f"{variant.tactics}"
                )
            if not str(variant.tactics_option):
                raise ValueError(
                    "enemy lacks TACTICSOPTION provenance: " + enemy_id
                )

            decision = resolve_common_normal_enemy_ai(
                str(variant.tactics_option),
                tuple(targets),
                mode_roll=int(mode_rolls_by_enemy_id[enemy_id]),
                target_roll=target_rolls.get(enemy_id),
            )
            if decision is None:
                raise ValueError(
                    "enemy AI produced no executable common decision: "
                    + enemy_id
                )
            if decision.kind == ENEMY_AI_ATTACK:
                commands[enemy_id] = BattleCommand(
                    BATTLE_COM_ATTACK,
                    command2=int(decision.target_slot),
                )
                continue
            if decision.kind == ENEMY_AI_GUARD:
                commands[enemy_id] = BattleCommand(BATTLE_COM_GUARD)
                continue
            if decision.kind == ENEMY_AI_ESCAPE and bool(allow_escape):
                commands[enemy_id] = BattleCommand(BATTLE_COM_ESCAPE)
                continue
            if decision.kind == ENEMY_AI_SKILL and (
                bool(allow_basic_skill)
                or bool(allow_statuschange_skill)
                or bool(allow_powerbalance_skill)
                or bool(allow_mighty_skill)
                or bool(allow_guardbreak_skill)
                or bool(allow_continuationattack_skill)
                or bool(allow_chargeattack_skill)
                or bool(allow_noguard_skill)
                or bool(allow_abduct_skill)
            ):
                petskill_runtime = getattr(self.stack, "petskill_runtime", None)
                if petskill_runtime is None:
                    raise ValueError(
                        "enemy AI pet-skill selection requires recovered "
                        "pet-skill runtime"
                    )
                bridged = resolve_enemy_ai_supported_petskill_command(
                    spawned,
                    skill_slot=int(decision.skill_slot),
                    target_slot=int(decision.target_slot),
                    petskill_runtime=petskill_runtime,
                    allow_status_change=bool(allow_statuschange_skill),
                    allow_power_balance=bool(allow_powerbalance_skill),
                    allow_mighty=bool(allow_mighty_skill),
                    allow_guard_break=bool(allow_guardbreak_skill),
                    allow_continuation_attack=bool(
                        allow_continuationattack_skill
                    ),
                    allow_charge_attack=bool(allow_chargeattack_skill),
                    allow_no_guard=bool(allow_noguard_skill),
                    allow_abduct=bool(allow_abduct_skill),
                )
                commands[enemy_id] = bridged.command
                if bridged.setup_effects != BattleCommandSetupEffects():
                    setup_effects[enemy_id] = bridged.setup_effects
                if bridged.abduct_ai_threshold is not None:
                    abduct_contexts[enemy_id]=OrdinaryAbductContext(
                        skill_array=int(bridged.skill_id),
                        ai_threshold=int(bridged.abduct_ai_threshold),
                        # Local reconstructed ordinary group battles have no
                        # event WinFunc seam; special WinFunc battles remain
                        # outside this coordinator subset.
                        has_win_func=False,
                    )
                continue
            allowed_parts = ["ATTACK", "GUARD"]
            if bool(allow_escape):
                allowed_parts.append("ESCAPE")
            if bool(allow_basic_skill):
                allowed_parts.append("basic-petskill")
            if bool(allow_statuschange_skill):
                allowed_parts.append("StatusChange")
            if bool(allow_powerbalance_skill):
                allowed_parts.append("PowerBalance")
            if bool(allow_mighty_skill):
                allowed_parts.append("Mighty")
            if bool(allow_guardbreak_skill):
                allowed_parts.append("GuardBreak")
            if bool(allow_continuationattack_skill):
                allowed_parts.append("ContinuationAttack")
            if bool(allow_chargeattack_skill):
                allowed_parts.append("ChargeAttack")
            if bool(allow_noguard_skill):
                allowed_parts.append("NoGuard")
            if bool(allow_abduct_skill):
                allowed_parts.append("Abduct")
            allowed = "/".join(allowed_parts)
            raise ValueError(
                "enemy AI selected command outside coordinator "
                f"{allowed} subset: {enemy_id}:{decision.kind}"
            )

        return EnemyAiCommonCommandBatch(
            commands=commands,
            setup_effects=setup_effects,
            abduct_contexts=abduct_contexts,
        )

    def build_persistent_enemy_common_commands(
        self,
        context: LocalRuntimeBattleContext,
        *,
        mode_rolls_by_enemy_id: Mapping[str, int],
        target_rolls_by_enemy_id: Mapping[str, int] | None = None,
        allow_escape: bool = False,
        allow_basic_skill: bool = False,
    ) -> Mapping[str, BattleCommand]:
        """Backward-compatible commands-only view of the common AI batch."""

        return self._build_persistent_enemy_common_batch(
            context,
            mode_rolls_by_enemy_id=mode_rolls_by_enemy_id,
            target_rolls_by_enemy_id=target_rolls_by_enemy_id,
            allow_escape=allow_escape,
            allow_basic_skill=allow_basic_skill,
            allow_statuschange_skill=False,
            allow_powerbalance_skill=False,
            allow_mighty_skill=False,
            allow_guardbreak_skill=False,
            allow_chargeattack_skill=False,
            allow_noguard_skill=False,
            allow_abduct_skill=False,
        ).commands

    def build_persistent_enemy_attack_guard_commands(
        self,
        context: LocalRuntimeBattleContext,
        *,
        mode_rolls_by_enemy_id: Mapping[str, int],
        target_rolls_by_enemy_id: Mapping[str, int] | None = None,
    ) -> Mapping[str, BattleCommand]:
        """Backward-compatible ATTACK/GUARD-only enemy-AI boundary."""

        return self.build_persistent_enemy_common_commands(
            context,
            mode_rolls_by_enemy_id=mode_rolls_by_enemy_id,
            target_rolls_by_enemy_id=target_rolls_by_enemy_id,
            allow_escape=False,
            allow_basic_skill=False,
        )

    def resolve_persistent_attack_guard_wait_round_with_enemy_ai(
        self,
        context: LocalRuntimeBattleContext,
        *,
        player_side_commands: Mapping[str, BattleCommand],
        enemy_mode_rolls: Mapping[str, int],
        enemy_target_rolls: Mapping[str, int] | None,
        initiative_random_subtracts: Mapping[str, int],
        profiles: Mapping[str, BattleCombatProfile],
        attack_rolls: Mapping[str, OrdinaryAttackRolls],
        defense_profile: str,
        no_risk: bool = False,
        field_attr: str = "none",
        field_power: int = 0,
        tie_break_order: Sequence[str] | None = None,
    ) -> tuple[LocalRuntimeBattleContext, PersistentRoundResult]:
        """Advance one ATTACK/GUARD/WAIT round with recovered enemy AI.

        Player-side commands remain explicit. Enemy commands are derived from
        each spawned variant's recovered TACTICS/TACTICSOPTION with explicit
        caller-provided AI rolls.
        """

        state = context.persistent_battle_state
        if state is None:
            raise ValueError("battle context has no persistent battle state")

        living_player_side_ids = {
            str(participant.participant_id)
            for participant in (
                state.session.player,
                *state.session.allied_pets,
            )
            if (
                str(participant.participant_id)
                in state.hp_by_participant_id
                and str(participant.participant_id)
                not in set(state.ultimate_exited_participant_ids)
                and str(participant.participant_id)
                not in set(state.battle_exited_participant_ids)
                and int(
                    state.hp_by_participant_id[
                        str(participant.participant_id)
                    ]
                ) > 0
            )
        }
        normalized_player_commands = {
            str(key): value
            for key, value in player_side_commands.items()
        }
        if set(normalized_player_commands) != living_player_side_ids:
            missing = sorted(
                living_player_side_ids - set(normalized_player_commands)
            )
            extra = sorted(
                set(normalized_player_commands) - living_player_side_ids
            )
            raise ValueError(
                "player-side commands must cover exactly living player-side "
                f"actors; missing={missing}, extra={extra}"
            )

        enemy_commands = self.build_persistent_enemy_attack_guard_commands(
            context,
            mode_rolls_by_enemy_id=enemy_mode_rolls,
            target_rolls_by_enemy_id=enemy_target_rolls,
        )
        commands = {
            **normalized_player_commands,
            **dict(enemy_commands),
        }
        return self.resolve_persistent_attack_wait_round(
            context,
            commands=commands,
            initiative_random_subtracts=initiative_random_subtracts,
            profiles=profiles,
            attack_rolls=attack_rolls,
            defense_profile=defense_profile,
            no_risk=no_risk,
            field_attr=field_attr,
            field_power=field_power,
            tie_break_order=tie_break_order,
        )

    def resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
        self,
        context: LocalRuntimeBattleContext,
        *,
        player_side_commands: Mapping[str, BattleCommand],
        enemy_mode_rolls: Mapping[str, int],
        enemy_target_rolls: Mapping[str, int] | None,
        enemy_escape_rolls: Mapping[str, OrdinaryEscapeRolls],
        opponent_abio_by_participant_id: Mapping[str, bool],
        initiative_random_subtracts: Mapping[str, int],
        profiles: Mapping[str, BattleCombatProfile],
        attack_rolls: Mapping[str, OrdinaryAttackRolls],
        defense_profile: str,
        counter_rolls_by_attack_id: Mapping[
            str, Sequence[CounterAttemptRolls]
        ] | None = None,
        continuation_rolls_by_attack_id: Mapping[
            str, ContinuationAttackRolls
        ] | None = None,
        abduct_rolls_by_attack_id: Mapping[
            str, OrdinaryAbductRolls
        ] | None = None,
        counter_abio_by_participant_id: Mapping[str, bool] | None = None,
        base_status_rolls_by_participant_id: Mapping[
            str, BaseStatusTurnRolls
        ] | None = None,
        base_status_combat_profiles_by_participant_id: Mapping[
            str, BaseStatusCombatProfile
        ] | None = None,
        status_application_rolls_by_attack_id: Mapping[str, int] | None = None,
        no_risk: bool = False,
        field_attr: str = "none",
        field_power: int = 0,
        tie_break_order: Sequence[str] | None = None,
    ) -> tuple[LocalRuntimeBattleContext, PersistentRoundResult]:
        """Advance the currently executable common enemy-AI round.

        ATTACK/GUARD are direct. ESCAPE uses recovered enemybase RARE plus
        explicit RAND/ABIO inputs. wa slots admit None/NormalAttack/NormalGuard
        plus recovered Abduct, ChargeAttack, ContinuationAttack, GuardBreak,
        Mighty, NoGuard, PowerBalance and StatusChange. Abduct carries the
        recovered OPTION atoi threshold and explicit RAND input. NoGuard keeps S_NOGUARD selected for its
        own NoAction turn so later same-round dodge/counter checks can consume
        COM3; ChargeAttack carries its countdown across rounds. GuardBreak
        preserves its dedicated guard-only hit gate and source-shaped Guardian
        settlement quirk; Mighty preserves packed damage-multiplier / dodge
        modifiers; PowerBalance carries immediate work attack/defense setup
        effects; StatusChange keeps setup effects and all status/application RNG
        explicit. Every other callback remains fail-closed.
        """

        state = context.persistent_battle_state
        if state is None:
            raise ValueError("battle context has no persistent battle state")
        if state.phase != "active":
            raise ValueError("cannot execute another round after battle termination")

        living_player_side_ids = {
            str(participant.participant_id)
            for participant in (
                state.session.player,
                *state.session.allied_pets,
            )
            if (
                str(participant.participant_id)
                in state.hp_by_participant_id
                and str(participant.participant_id)
                not in set(state.ultimate_exited_participant_ids)
                and str(participant.participant_id)
                not in set(state.battle_exited_participant_ids)
                and int(
                    state.hp_by_participant_id[
                        str(participant.participant_id)
                    ]
                ) > 0
            )
        }
        normalized_player_commands = {
            str(key): value
            for key, value in player_side_commands.items()
        }
        if set(normalized_player_commands) != living_player_side_ids:
            missing = sorted(
                living_player_side_ids - set(normalized_player_commands)
            )
            extra = sorted(
                set(normalized_player_commands) - living_player_side_ids
            )
            raise ValueError(
                "player-side commands must cover exactly living player-side "
                f"actors; missing={missing}, extra={extra}"
            )
        invalid_player_commands = tuple(
            sorted(
                participant_id
                for participant_id, command
                in normalized_player_commands.items()
                if not isinstance(command, BattleCommand)
                or int(command.command1)
                not in {BATTLE_COM_ATTACK, BATTLE_COM_GUARD, BATTLE_COM_WAIT}
            )
        )
        if invalid_player_commands:
            raise ValueError(
                "enemy-AI escape round accepts player-side "
                "ATTACK/GUARD/WAIT only: "
                + ",".join(invalid_player_commands)
            )

        enemy_batch = self._build_persistent_enemy_common_batch(
            context,
            mode_rolls_by_enemy_id=enemy_mode_rolls,
            target_rolls_by_enemy_id=enemy_target_rolls,
            allow_escape=True,
            allow_basic_skill=True,
            allow_statuschange_skill=True,
            allow_powerbalance_skill=True,
            allow_mighty_skill=True,
            allow_guardbreak_skill=True,
            allow_continuationattack_skill=True,
            allow_chargeattack_skill=True,
            allow_noguard_skill=True,
            allow_abduct_skill=True,
        )
        enemy_commands = enemy_batch.commands
        escaping_enemy_ids = {
            str(participant_id)
            for participant_id, command in enemy_commands.items()
            if int(command.command1) == BATTLE_COM_ESCAPE
        }
        continuation_enemy_ids = {
            str(participant_id)
            for participant_id, command in enemy_commands.items()
            if int(command.command1) == BATTLE_COM_S_RENZOKU
        }
        abduct_enemy_ids = {
            str(participant_id)
            for participant_id, command in enemy_commands.items()
            if int(command.command1) == BATTLE_COM_S_ABDUCT
        }
        normalized_abduct_rolls={
            str(key):value
            for key,value in (abduct_rolls_by_attack_id or {}).items()
        }
        extra_abduct_rolls=sorted(
            set(normalized_abduct_rolls)-abduct_enemy_ids
        )
        if extra_abduct_rolls:
            raise ValueError(
                "enemy Abduct RNG references non-Abduct actors: "
                + ",".join(extra_abduct_rolls)
            )
        for participant_id,rolls in normalized_abduct_rolls.items():
            if not isinstance(rolls,OrdinaryAbductRolls):
                raise TypeError(
                    f"enemy Abduct RNG has wrong type for {participant_id}"
                )
        if set(enemy_batch.abduct_contexts) != abduct_enemy_ids:
            raise ValueError(
                "enemy Abduct context/command actor mismatch"
            )

        normalized_continuation_rolls = {
            str(key): value
            for key, value in (
                continuation_rolls_by_attack_id or {}
            ).items()
        }
        if set(normalized_continuation_rolls) != continuation_enemy_ids:
            missing=sorted(
                continuation_enemy_ids-set(normalized_continuation_rolls)
            )
            extra=sorted(
                set(normalized_continuation_rolls)-continuation_enemy_ids
            )
            raise ValueError(
                "enemy ContinuationAttack RNG mismatch; "
                f"missing={missing}, extra={extra}"
            )
        for participant_id,rolls in normalized_continuation_rolls.items():
            if not isinstance(rolls,ContinuationAttackRolls):
                raise TypeError(
                    "enemy ContinuationAttack RNG has wrong type for "
                    f"{participant_id}"
                )

        statuschange_enemy_ids = {
            str(participant_id)
            for participant_id, command in enemy_commands.items()
            if int(command.command1) == BATTLE_COM_S_STATUSCHANGE
        }
        normalized_status_application_rolls = {
            str(key): int(value)
            for key, value in (
                status_application_rolls_by_attack_id or {}
            ).items()
        }
        extra_status_rolls = sorted(
            set(normalized_status_application_rolls)
            - statuschange_enemy_ids
        )
        if extra_status_rolls:
            raise ValueError(
                "enemy StatusChange RNG references non-StatusChange actors: "
                + ",".join(extra_status_rolls)
            )

        normalized_escape_rolls = {
            str(key): value
            for key, value in enemy_escape_rolls.items()
        }
        if set(normalized_escape_rolls) != escaping_enemy_ids:
            missing = sorted(
                escaping_enemy_ids - set(normalized_escape_rolls)
            )
            extra = sorted(
                set(normalized_escape_rolls) - escaping_enemy_ids
            )
            raise ValueError(
                "enemy escape rolls must cover exactly AI-selected escaping "
                f"enemies; missing={missing}, extra={extra}"
            )
        for enemy_id, rolls in normalized_escape_rolls.items():
            if not isinstance(rolls, OrdinaryEscapeRolls):
                raise TypeError(
                    f"enemy escape rolls for {enemy_id} must be "
                    "OrdinaryEscapeRolls"
                )

        normalized_abio = {
            str(key): bool(value)
            for key, value in opponent_abio_by_participant_id.items()
        }
        expected_abio_ids = (
            living_player_side_ids if escaping_enemy_ids else set()
        )
        if set(normalized_abio) != expected_abio_ids:
            missing = sorted(expected_abio_ids - set(normalized_abio))
            extra = sorted(set(normalized_abio) - expected_abio_ids)
            raise ValueError(
                "enemy escape ABIO inputs must cover exactly current living "
                f"opponents when ESCAPE is selected; missing={missing}, "
                f"extra={extra}"
            )

        spawn_by_participant_id = {
            str(spawned.participant.participant_id): spawned
            for spawned in context.spawned_enemies
        }
        escape_contexts = {}
        for enemy_id in escaping_enemy_ids:
            if enemy_id not in spawn_by_participant_id:
                raise ValueError(
                    "escaping enemy lacks recovered spawn provenance: "
                    + enemy_id
                )
            spawned = spawn_by_participant_id[enemy_id]
            if spawned.template.rare is None:
                raise ValueError(
                    "escaping enemy lacks enemybase RARE provenance: "
                    + enemy_id
                )
            if enemy_id not in state.escape_count_by_participant_id:
                raise ValueError(
                    "escaping enemy lacks persistent escape counter: "
                    + enemy_id
                )
            escape_contexts[enemy_id] = OrdinaryEscapeContext(
                stored_escape_count_before=int(
                    state.escape_count_by_participant_id[enemy_id]
                ),
                actor_rare=int(spawned.template.rare),
                opponent_abio_by_participant_id=normalized_abio,
                pvp=False,
                forced_exit=False,
            )

        commands = {
            **normalized_player_commands,
            **dict(enemy_commands),
        }
        result = resolve_persistent_ordinary_round(
            state,
            commands=commands,
            initiative_random_subtracts={
                str(key): int(value)
                for key, value in initiative_random_subtracts.items()
            },
            profiles=profiles,
            attack_rolls=attack_rolls,
            counter_rolls_by_attack_id=counter_rolls_by_attack_id,
            continuation_rolls_by_attack_id=normalized_continuation_rolls,
            abduct_contexts=enemy_batch.abduct_contexts,
            abduct_rolls=normalized_abduct_rolls,
            counter_abio_by_participant_id=counter_abio_by_participant_id,
            escape_contexts=escape_contexts,
            escape_rolls=normalized_escape_rolls,
            base_status_rolls_by_participant_id=(
                base_status_rolls_by_participant_id
            ),
            base_status_combat_profiles_by_participant_id=(
                base_status_combat_profiles_by_participant_id
            ),
            status_application_rolls_by_attack_id=(
                normalized_status_application_rolls
            ),
            command_setup_effects_by_participant_id=(
                enemy_batch.setup_effects
            ),
            defense_profile=str(defense_profile),
            no_risk=bool(no_risk),
            field_attr=str(field_attr),
            field_power=int(field_power),
            tie_break_order=(
                None
                if tie_break_order is None
                else tuple(str(x) for x in tie_break_order)
            ),
        )
        return (
            replace(
                context,
                persistent_battle_state=result.after,
            ),
            result,
        )

    def resolve_persistent_attack_wait_round(
        self,
        context: LocalRuntimeBattleContext,
        *,
        commands: Mapping[str, BattleCommand],
        initiative_random_subtracts: Mapping[str, int],
        profiles: Mapping[str, BattleCombatProfile],
        attack_rolls: Mapping[str, OrdinaryAttackRolls],
        defense_profile: str,
        no_risk: bool = False,
        field_attr: str = "none",
        field_power: int = 0,
        tie_break_order: Sequence[str] | None = None,
    ) -> tuple[LocalRuntimeBattleContext, PersistentRoundResult]:
        """Advance one explicit ordinary ATTACK/GUARD/WAIT round.

        Capture, escape, item, skill/combo and automatic enemy-AI selection
        remain outside this low-level coordinator seam. The dedicated AI bridge
        above may generate only ATTACK/GUARD before entering this method.
        """

        state = context.persistent_battle_state
        if state is None:
            raise ValueError("battle context has no persistent battle state")

        normalized_commands = {
            str(key): value
            for key, value in commands.items()
        }
        invalid_commands = tuple(
            sorted(
                participant_id
                for participant_id, command in normalized_commands.items()
                if not isinstance(command, BattleCommand)
                or int(command.command1)
                not in {BATTLE_COM_ATTACK, BATTLE_COM_GUARD, BATTLE_COM_WAIT}
            )
        )
        if invalid_commands:
            raise ValueError(
                "persistent coordinator R1 accepts ATTACK/GUARD/WAIT only: "
                + ",".join(invalid_commands)
            )

        result = resolve_persistent_ordinary_round(
            state,
            commands=normalized_commands,
            initiative_random_subtracts={
                str(key): int(value)
                for key, value in initiative_random_subtracts.items()
            },
            profiles=profiles,
            attack_rolls=attack_rolls,
            defense_profile=str(defense_profile),
            no_risk=bool(no_risk),
            field_attr=str(field_attr),
            field_power=int(field_power),
            tie_break_order=(
                None
                if tie_break_order is None
                else tuple(str(x) for x in tie_break_order)
            ),
        )
        return (
            replace(
                context,
                persistent_battle_state=result.after,
            ),
            result,
        )

    def resolve_persistent_capture_round(
        self,
        context: LocalRuntimeBattleContext,
        *,
        commands: Mapping[str, BattleCommand],
        initiative_random_subtracts: Mapping[str, int],
        profiles: Mapping[str, BattleCombatProfile],
        attack_rolls: Mapping[str, OrdinaryAttackRolls],
        capture_context: OrdinaryCaptureContext,
        capture_rolls: OrdinaryCaptureRolls,
        captured_pets_by_target_id: Mapping[str, PetActor],
        defense_profile: str,
        no_risk: bool = False,
        field_attr: str = "none",
        field_power: int = 0,
        tie_break_order: Sequence[str] | None = None,
    ) -> tuple[LocalRuntimeBattleContext, PersistentRoundResult]:
        """Advance one explicit player-capture round transactionally."""

        state = context.persistent_battle_state
        if state is None:
            raise ValueError("battle context has no persistent battle state")

        player_id = str(state.session.player.participant_id)
        normalized_commands = {
            str(key): value
            for key, value in commands.items()
        }
        if player_id not in normalized_commands:
            raise ValueError("capture round requires an explicit player command")
        if int(normalized_commands[player_id].command1) != BATTLE_COM_CAPTURE:
            raise ValueError("capture round requires player CAPTURE command")

        invalid_commands = tuple(
            sorted(
                participant_id
                for participant_id, command in normalized_commands.items()
                if not isinstance(command, BattleCommand)
                or int(command.command1)
                not in {BATTLE_COM_ATTACK, BATTLE_COM_WAIT, BATTLE_COM_CAPTURE}
                or (
                    int(command.command1) == BATTLE_COM_CAPTURE
                    and participant_id != player_id
                )
            )
        )
        if invalid_commands:
            raise ValueError(
                "capture coordinator accepts player CAPTURE and ATTACK/WAIT only: "
                + ",".join(invalid_commands)
            )
        if not isinstance(capture_context, OrdinaryCaptureContext):
            raise TypeError("capture_context must be OrdinaryCaptureContext")
        if not isinstance(capture_rolls, OrdinaryCaptureRolls):
            raise TypeError("capture_rolls must be OrdinaryCaptureRolls")

        encounter_runtime = getattr(self.stack, "encounter_runtime", None)
        if encounter_runtime is None:
            raise ValueError("runtime stack has no encounter runtime")

        working_state = decode_persistent_state(
            self._battle_working_persistent_payload(context)
        )
        domain = SinglePlayerHistoricalDomain(
            static=encounter_runtime.static_data,
            persistent=working_state,
        )
        domain.move_player(
            floor_id=context.origin_position.floor_id,
            x=context.origin_position.x,
            y=context.origin_position.y,
        )
        runtime = SinglePlayerHistoricalRuntime(
            domain=domain,
            topology=self.topology,
        )
        result = runtime.resolve_persistent_battle_round(
            state,
            commands=normalized_commands,
            initiative_random_subtracts={
                str(key): int(value)
                for key, value in initiative_random_subtracts.items()
            },
            profiles=profiles,
            attack_rolls=attack_rolls,
            capture_contexts={player_id: capture_context},
            capture_rolls={player_id: capture_rolls},
            captured_pets_by_target_id={
                str(key): value
                for key, value in captured_pets_by_target_id.items()
            },
            defense_profile=str(defense_profile),
            no_risk=bool(no_risk),
            field_attr=str(field_attr),
            field_power=int(field_power),
            tie_break_order=(
                None
                if tie_break_order is None
                else tuple(str(x) for x in tie_break_order)
            ),
        )
        return (
            replace(
                context,
                persistent_battle_state=result.after,
                working_persistent_state_payload=encode_persistent_state(
                    domain.persistent
                ),
            ),
            result,
        )

    def resolve_persistent_escape_round(
        self,
        context: LocalRuntimeBattleContext,
        *,
        commands: Mapping[str, BattleCommand],
        initiative_random_subtracts: Mapping[str, int],
        profiles: Mapping[str, BattleCombatProfile],
        attack_rolls: Mapping[str, OrdinaryAttackRolls],
        escape_context: OrdinaryEscapeContext,
        escape_rolls: OrdinaryEscapeRolls,
        defense_profile: str,
        no_risk: bool = False,
        field_attr: str = "none",
        field_power: int = 0,
        tie_break_order: Sequence[str] | None = None,
    ) -> tuple[LocalRuntimeBattleContext, PersistentRoundResult]:
        """Advance one explicit player-escape round without synthesizing AI."""

        state = context.persistent_battle_state
        if state is None:
            raise ValueError("battle context has no persistent battle state")

        player_id = str(state.session.player.participant_id)
        normalized_commands = {
            str(key): value
            for key, value in commands.items()
        }
        if player_id not in normalized_commands:
            raise ValueError("escape round requires an explicit player command")
        if int(normalized_commands[player_id].command1) != BATTLE_COM_ESCAPE:
            raise ValueError("escape round requires player ESCAPE command")

        invalid_commands = tuple(
            sorted(
                participant_id
                for participant_id, command in normalized_commands.items()
                if not isinstance(command, BattleCommand)
                or int(command.command1)
                not in {BATTLE_COM_ATTACK, BATTLE_COM_WAIT, BATTLE_COM_ESCAPE}
                or (
                    int(command.command1) == BATTLE_COM_ESCAPE
                    and participant_id != player_id
                )
            )
        )
        if invalid_commands:
            raise ValueError(
                "escape coordinator accepts player ESCAPE and ATTACK/WAIT only: "
                + ",".join(invalid_commands)
            )
        if not isinstance(escape_context, OrdinaryEscapeContext):
            raise TypeError("escape_context must be OrdinaryEscapeContext")
        if not isinstance(escape_rolls, OrdinaryEscapeRolls):
            raise TypeError("escape_rolls must be OrdinaryEscapeRolls")

        result = resolve_persistent_ordinary_round(
            state,
            commands=normalized_commands,
            initiative_random_subtracts={
                str(key): int(value)
                for key, value in initiative_random_subtracts.items()
            },
            profiles=profiles,
            attack_rolls=attack_rolls,
            escape_contexts={player_id: escape_context},
            escape_rolls={player_id: escape_rolls},
            defense_profile=str(defense_profile),
            no_risk=bool(no_risk),
            field_attr=str(field_attr),
            field_power=int(field_power),
            tie_break_order=(
                None
                if tie_break_order is None
                else tuple(str(x) for x in tie_break_order)
            ),
        )
        return (
            replace(
                context,
                persistent_battle_state=result.after,
            ),
            result,
        )

    def settle_persistent_defeat(
        self,
        context: LocalRuntimeBattleContext,
    ) -> LocalRuntimeSessionState:
        """Settle one terminal defeat through the recovered battle-exit seam."""

        state = context.persistent_battle_state
        if state is None:
            raise ValueError("battle context has no persistent battle state")
        if state.phase != "finished" or state.result != "defeat":
            raise ValueError("defeat settlement requires terminal defeat state")
        return self.settle_persistent_group_battle_without_level_crossing(
            context
        )

    def settle_persistent_escape(
        self,
        context: LocalRuntimeBattleContext,
    ) -> LocalRuntimeSessionState:
        """Settle terminal player escape without normal battle profit."""

        state = context.persistent_battle_state
        if state is None:
            raise ValueError("battle context has no persistent battle state")

        encounter_runtime = getattr(self.stack, "encounter_runtime", None)
        if encounter_runtime is None:
            raise ValueError("runtime stack has no encounter runtime")

        working_state = decode_persistent_state(
            self._battle_working_persistent_payload(context)
        )
        domain = SinglePlayerHistoricalDomain(
            static=encounter_runtime.static_data,
            persistent=working_state,
        )
        domain.move_player(
            floor_id=context.origin_position.floor_id,
            x=context.origin_position.x,
            y=context.origin_position.y,
        )
        runtime = SinglePlayerHistoricalRuntime(
            domain=domain,
            topology=self.topology,
        )
        returned = runtime.finish_persistent_escape(state)
        updated = LocalRuntimeSessionState(
            contract_id=context.contract_id,
            world_profile=context.world_profile,
            hometown_ordinal=context.hometown_ordinal,
            player_position=returned.world_position,
            player_state=domain.persistent,
            world_flags=context.world_flags,
        )
        return self._validate_session(updated)

    def settle_persistent_group_battle_without_level_crossing(
        self,
        context: LocalRuntimeBattleContext,
    ) -> LocalRuntimeSessionState:
        """Settle a terminal persistent battle into a new authoritative session."""

        state = context.persistent_battle_state
        if state is None:
            raise ValueError("battle context has no persistent battle state")

        encounter_runtime = getattr(self.stack, "encounter_runtime", None)
        if encounter_runtime is None:
            raise ValueError("runtime stack has no encounter runtime")

        working_state = decode_persistent_state(
            self._battle_working_persistent_payload(context)
        )
        domain = SinglePlayerHistoricalDomain(
            static=encounter_runtime.static_data,
            persistent=working_state,
        )
        domain.move_player(
            floor_id=context.origin_position.floor_id,
            x=context.origin_position.x,
            y=context.origin_position.y,
        )
        runtime = SinglePlayerHistoricalRuntime(
            domain=domain,
            topology=self.topology,
        )
        returned = runtime.finish_persistent_battle_without_level_crossing(
            state
        )
        updated = LocalRuntimeSessionState(
            contract_id=context.contract_id,
            world_profile=context.world_profile,
            hometown_ordinal=context.hometown_ordinal,
            player_position=returned.world_position,
            player_state=domain.persistent,
            world_flags=context.world_flags,
        )
        return self._validate_session(updated)

    def settle_persistent_group_battle_with_progression(
        self,
        context: LocalRuntimeBattleContext,
        *,
        player_exp_profile: str,
        next_player_max_exp_by_level: Mapping[int, int],
        pet_exp_profile: str | None = None,
        next_pet_max_exp_by_slot: Mapping[int, Mapping[int, int]] | None = None,
        pet_level_growth_rolls_by_slot: Mapping[int, Sequence[Any]] | None = None,
    ) -> LocalRuntimeSessionState:
        """Settle terminal battle EXP through the closed explicit progression seam.

        The coordinator owns no threshold table and generates no pet growth RNG.
        Profiles, future thresholds and every pet level-growth roll remain explicit
        caller inputs so unresolved launch-era progression cannot be invented here.
        """

        state = context.persistent_battle_state
        if state is None:
            raise ValueError("battle context has no persistent battle state")

        encounter_runtime = getattr(self.stack, "encounter_runtime", None)
        if encounter_runtime is None:
            raise ValueError("runtime stack has no encounter runtime")

        working_state = decode_persistent_state(
            self._battle_working_persistent_payload(context)
        )
        domain = SinglePlayerHistoricalDomain(
            static=encounter_runtime.static_data,
            persistent=working_state,
        )
        domain.move_player(
            floor_id=context.origin_position.floor_id,
            x=context.origin_position.x,
            y=context.origin_position.y,
        )
        runtime = SinglePlayerHistoricalRuntime(
            domain=domain,
            topology=self.topology,
        )
        returned = runtime.finish_persistent_battle_with_progression(
            state,
            player_exp_profile=player_exp_profile,
            next_player_max_exp_by_level=next_player_max_exp_by_level,
            pet_exp_profile=pet_exp_profile,
            next_pet_max_exp_by_slot=next_pet_max_exp_by_slot,
            pet_level_growth_rolls_by_slot=pet_level_growth_rolls_by_slot,
        )
        updated = LocalRuntimeSessionState(
            contract_id=context.contract_id,
            world_profile=context.world_profile,
            hometown_ordinal=context.hometown_ordinal,
            player_position=returned.world_position,
            player_state=domain.persistent,
            world_flags=context.world_flags,
        )
        return self._validate_session(updated)

    @staticmethod
    def _binding_source_rect(binding) -> tuple[int, int, int, int]:
        if binding.predicate_payload.get("interaction_kind") != "DIALOGUE_WARPMAN":
            raise ValueError("state-gated coordinator currently requires dialogue WarpMan")
        raw = binding.predicate_payload.get("source_rect")
        if not isinstance(raw, tuple) or len(raw) != 4:
            raise ValueError("state-gated binding lacks recovered source rectangle")
        x1, y1, x2, y2 = (int(v) for v in raw)
        return min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)

    @staticmethod
    def _position_in_binding_source(
        position: MapPosition,
        binding,
    ) -> bool:
        x1, y1, x2, y2 = LocalRuntimeSessionCoordinator._binding_source_rect(
            binding
        )
        return (
            int(position.floor_id) == int(binding.source.floor_id)
            and x1 <= int(position.x) <= x2
            and y1 <= int(position.y) <= y2
        )

    def discover_state_gated_interactions(
        self,
        session: LocalRuntimeSessionState,
    ) -> tuple[LocalRuntimeInteraction, ...]:
        """Return semantic interaction views available at the current coordinate.

        Raw recovered source rectangles and legacy NPC argument strings remain
        inside the binding layer; presentation code receives only stable
        transition identity, live eligibility, and provenance.
        """

        session = self._validate_session(session)
        rows = []
        for transition_id in sorted(self.profile.transitions):
            binding = self.stack.resolve_transition(str(transition_id))
            self._binding_source_rect(binding)
            if not self._position_in_binding_source(
                session.player_position,
                binding,
            ):
                continue
            decision = self.stack.evaluate_transition(
                str(transition_id),
                session,
            )
            rows.append(
                LocalRuntimeInteraction(
                    transition_id=str(transition_id),
                    interaction_kind=str(
                        binding.predicate_payload["interaction_kind"]
                    ),
                    allowed=bool(decision.allowed),
                    reason=decision.reason,
                    provenance=binding.provenance,
                    execution_supported=not bool(decision.consumed_state),
                )
            )
        return tuple(rows)

    def dispatch_state_gated_interaction(
        self,
        session: LocalRuntimeSessionState,
        transition_id: str,
    ) -> LocalRuntimeTransitionResult:
        """Dispatch a semantic interaction id through the canonical executor."""

        return self.execute_state_gated_transition(
            session,
            str(transition_id),
        )

    def execute_state_gated_transition(
        self,
        session: LocalRuntimeSessionState,
        transition_id: str,
    ) -> LocalRuntimeTransitionResult:
        """Evaluate and, if allowed, execute one recovered dialogue transition."""

        session = self._validate_session(session)
        binding = self.stack.resolve_transition(str(transition_id))
        spatially_eligible = self._position_in_binding_source(
            session.player_position,
            binding,
        )
        if not spatially_eligible:
            return LocalRuntimeTransitionResult(
                session=session,
                decision=TransitionGateDecision(
                    allowed=False,
                    reason="player is outside recovered transition source rectangle",
                    consumed_state={},
                ),
            )

        decision = self.stack.evaluate_transition(
            str(transition_id),
            session,
        )
        if not decision.allowed:
            return LocalRuntimeTransitionResult(
                session=session,
                decision=decision,
            )
        if decision.consumed_state:
            raise ValueError(
                "state-gated transition returned unimplemented consumed_state mutation"
            )
        if not self.topology.is_valid_position(binding.destination):
            raise ValueError("state-gated transition destination is outside topology")

        updated = replace(
            session,
            player_position=binding.destination,
        )
        self._validate_session(updated)
        return LocalRuntimeTransitionResult(
            session=updated,
            decision=decision,
        )
