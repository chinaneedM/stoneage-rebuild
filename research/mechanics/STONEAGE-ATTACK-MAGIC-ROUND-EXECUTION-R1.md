# StoneAge AttackMagic command-2002 round execution R1

Date: 2026-10-01

## Boundary

Command 2002 is admitted only for the already-closed recovered25 **enemy**
AttackMagic submission path. Player/pet/general magic command admission remains
outside this seam.

The existing action-order machinery is reused. AttackMagic therefore receives
the same ordinary QUICK+20 minus 0..30% initiative form used by the fixed
enemy path, and it executes only when its ordered entry is reached after the
existing base-status tick/rewrite.

## Round-time semantics

At the 2002 branch the resolver uses the **current** HP/exited state, not the
round-start snapshot, to rebuild living player-side slots. It then:

- verifies the `BattleCommand` payload exactly matches the closed enemy-AI
  AttackMagic submission;
- validates exact `BATTLE_MultiList` retarget RNG (including rejecting unused
  trailing values);
- resolves the recovered25 footprint with nonportable `SortLoc/qsort` states
  fail-closed;
- projects current HP, sleep, four-element resistance/training and mounted
  ride state into the closed action composer;
- applies HP/sleep/resistance/ride changes immediately before later actors
  execute.

One `OrdinaryRoundEvent` is emitted for each actual magic target. This lets the
existing persistent death/profit layer observe HP transitions without a new
parallel settlement system. A spell with `BATTLE_MultiList == -1` emits a
no-target event and consumes no magic RNG. A valid selector whose footprint is
empty can still consume the cast roll, matching the separate side-wide path.

AttackMagic deliberately bypasses physical Guardian, damage-reaction, counter
and Ultimate logic, matching its dedicated magic battle path.

## Persistent result

`PersistentRoundResult` now carries the AttackMagic overlay before/after while
`PersistentBattleState` continues to own HP, base statuses, ride state, turn,
death penalties and termination. The four magic resistance/EXP counters remain
battle-local overlay state until their player/pet persistence schema is
independently reconstructed.

Validation: dedicated CI **36854873316 = PASS**. Concurrent local-session, Taiwan gameplay, battle-core, pet-skill-core and round-state-adapter regressions also passed on the same HEAD.

Marker: **RECOVERED25_ATTACKMAGIC_COMMAND2002_ROUND_EXECUTION_R1 = CLOSED**
