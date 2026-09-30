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
from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_ESCAPE,
    BATTLE_COM_WAIT,
    BattleCombatProfile,
    BattleCommand,
    OrdinaryAttackRolls,
    OrdinaryEscapeContext,
    OrdinaryEscapeRolls,
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
            context.persistent_state_payload
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
        """Advance one explicit ordinary ATTACK/WAIT round.

        Capture, escape, item, skill, guard/combo and enemy-AI selection remain
        outside this coordinator seam until their dedicated runtime contracts
        are connected explicitly.
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
                not in {BATTLE_COM_ATTACK, BATTLE_COM_WAIT}
            )
        )
        if invalid_commands:
            raise ValueError(
                "persistent coordinator R1 accepts ATTACK/WAIT only: "
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
            context.persistent_state_payload
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
            context.persistent_state_payload
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
