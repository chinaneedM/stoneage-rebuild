# StoneAge Engine-Neutral Battle Event / State Contract — R1

Date: 2026-09-28

Status: **DESIGN / implementation contract grounded in closed Taiwan-v1 receive-state evidence**

## Purpose

Taiwan/Waei v1.0 directly proves that battle handling was split between:

1. player-submitted battle intent;
2. authoritative battle-state/status delivery;
3. ordinary execution/animation command delivery;
4. small turn/control synchronization messages;
5. escape/termination state.

The historical client implemented that split through the string-serialized `B`
receive protocol and two fixed four-slot command rings. The modern private
single-player runtime must preserve the *semantic separation* without retaining
the old network/string protocol as an internal dependency.

R1 therefore defines the following engine-neutral transition:

```text
BattleIntent[]
  -> deterministic resolver
  -> BattleStateSnapshot(before)
  -> BattleExecutionEvent[]
  -> BattleTurnSync
  -> BattleStateSnapshot(after)
  -> optional BattleTermination
```

Implementation:

- `tools/stoneage_battle_event_contract.py`
- `tests/test_stoneage_battle_event_contract.py`

## Evidence boundary

Historical evidence authority remains:

- `research/clients/STONEAGE-TW10-BATTLE-RECEIVE-STATE-R1.md`
- `research/recovered/STONEAGE-TW10-GAMEPLAY-CALLBACKS-R1.txt`
- `research/clients/STONEAGE-TW10-GAMEPLAY-SCHEMA-R1.json`

Direct v1 facts include:

- `B(string)` dispatch to RVA `0x32c70`;
- second-byte `C / P / A / U / default` discrimination;
- separate 4 × 4096-byte status and ordinary-command rings;
- BP `%X|%X|%X` parsing;
- BA `%X|%X` parsing plus one-shot turn synchronization;
- BU flag write.

The Python types below are **DESIGN**, not historical packet layouts and not a
claim about the original server's implementation language or in-memory types.

## 1. Submitted intent

`BattleIntent` binds:

- participant identity;
- stable battle slot;
- the existing typed `BattleCommand`.

It deliberately does not contain `H|...`, `B...`, or any other historical wire
string. The deterministic battle resolver remains the only owner of combat
rules.

Intents are exported in stable battle-slot order so mapping insertion order
cannot become a hidden gameplay/presentation dependency.

## 2. Authoritative state snapshot

`BattleStateSnapshot` wraps the existing immutable `PersistentBattleState`
instead of copying selected fields into a second partial state model.

This is intentional:

- `PersistentBattleState` already owns HP, slots, turn, terminal result,
  status/reaction state, ride state, pending reward state, escape state and
  other recovered battle-local authority;
- duplicating only a subset would create two competing definitions of
  authoritative battle state;
- the wrapper creates a clear engine-facing boundary without flattening or
  serializing the state.

Historical BC/status-ring semantics therefore map conceptually to a typed
authoritative snapshot, not to a recreated string queue.

## 3. Execution / presentation event stream

`BattleExecutionEvent` gives each existing typed `OrdinaryRoundEvent` an
explicit deterministic sequence number.

The wrapped event already carries the recovered execution details needed by
presentation systems, including target resolution, damage/HP changes,
critical/guard/counter/combo/status/reaction/ride/ultimate/capture/escape
results where those seams are implemented.

R1 does not invent a new animation opcode table. Presentation code may later
map typed events to animation/audio/UI behavior independently of combat rules.

Historical default battle-command-ring semantics therefore map to an ordered
typed event stream.

## 4. Turn synchronization

`BattleTurnSync` binds:

- previous authoritative turn;
- completed authoritative turn;
- resolver action order.

A normal round must advance exactly one turn. The contract rejects turn drift.

This replaces the historical BA client/server synchronization mechanism with a
local deterministic invariant. It preserves the synchronization *boundary*
without pretending that a local game still has independent server/client turn
counters.

## 5. Termination

`BattleTermination` is emitted only when the resulting authoritative
`PersistentBattleState` is finished.

It carries:

- terminal turn;
- terminal result;
- winning side when the underlying result has one.

The contract checks that the termination record matches the authoritative
after-state exactly. Active rounds cannot emit a terminal event, and finished
rounds cannot omit one.

The historical BU escape flag is therefore not copied as a network-era global.
Escape already becomes the existing typed persistent battle result and is
exposed through the same terminal contract.

## 6. Adapter from the reconstructed battle core

`build_battle_round_transition(PersistentRoundResult)` is the only R1 adapter.

It consumes the existing resolver output and produces the engine-facing
transition without recalculating any battle mechanics.

Invariant:

```text
combat rule authority remains in battle_*_model.py
event contract only organizes already-resolved typed state/events
```

The adapter:

- reads submitted commands from `after.last_commands`;
- joins them to the before-state battle slots;
- rejects command identities absent from the before-state slot map;
- preserves resolver event order;
- requires exactly one turn of progress;
- emits terminal state only when the authoritative after-state is finished.

## 7. Regression boundary

`tests/test_stoneage_battle_event_contract.py` covers:

- active-round intent/state/event/sync layering;
- terminal event emission;
- intent ordering by battle slot rather than mapping order;
- rejection of turn drift;
- rejection of submitted-command identities with no before-state slot.

The contract test is intentionally independent of historical wire strings.

## Consequence

The reconstruction now has a concrete boundary between deterministic battle
rules and future engine presentation/transport code.

A renderer, UI, replay recorder, save/replay system, or a future authorized
transport layer can consume the same typed transition without changing combat
rules or reviving the original `B` protocol internally.

**BATTLE_TYPED_EVENT_STATE_CONTRACT_R1 = IMPLEMENTED**

Next implementation seam: connect this transition contract to the
single-player runtime-facing battle loop/presentation handoff, then define the
first deterministic presentation/replay consumer without coupling it back to
historical network serialization.
