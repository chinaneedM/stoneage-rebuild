# StoneAge AttackMagic round-time state adapter R1

Date: 2026-10-01

## Purpose

The ordinary physical battle state already owns authoritative HP, base-status
runtime and ride-pet runtime. It does not yet own the four magic-resistance
levels/experience counters or magic-equipment modifiers required by the fixed
`_FIX_MAGICDAMAGE` path.

This adapter therefore keeps those missing values in a typed battle-local
overlay instead of overloading `BattleCombatProfile` or silently inventing
persistent player-save fields.

## State ownership

Existing `PersistentBattleState` remains authoritative for:

- participant HP;
- common base statuses, including sleep;
- ride-pet HP/mounted/PETFALL state;
- battle slot identity and active/exited membership.

`AttackMagicRoundOverlay` owns only:

- four resistance levels;
- four resistance experience counters;
- four equipment resistance additions;
- magic-dodge equipment value;
- active magic-defense percentage modifier.

The adapter projects the selected element into `MagicExpState`, including the
source-opposed `(element + 1) % 4` resistance pair, then writes both counters
back atomically after defense training.

## Exact execution boundary

`resolve_persistent_enemy_attack_magic_state(...)` accepts the closed enemy-AI
submission rather than a fabricated `BattleCommand(2002)`. At execution time
it:

1. validates a living enemy caster in slots 10..19;
2. derives the currently living player-side slots from `PersistentBattleState`;
3. resolves the recovered25 footprint with exact historical ordering required;
4. builds caster/defender magic state from combat profiles + overlay + base
   status + ride runtime;
5. requires RNG slots to equal the exact target set, preventing unused random
   values from being silently accepted;
6. executes the closed action composer;
7. writes HP, sleep, four-element resistance/training and ride state back.

The function deliberately leaves `turn`, phase/result, ordinary commands,
profit, death flags and kill settlement untouched. Those are the next
command/round adapter layer.

## Riding detail

A ride pet must have an explicit elemental `BattleCombatProfile` when mounted.
This is required even at zero HP if the historical mounted state remains set:
`BATTLE_GetAttr` can still average its elements, while the later HP-sharing
branch independently tests pet HP > 0.

Validation: dedicated CI **36853623595 = PASS**. The adapter remains green after the no-target RNG correction validated by action-composer CI **36854070168 = PASS**.

Marker: **RECOVERED25_ATTACKMAGIC_ROUND_STATE_ADAPTER_R1 = CLOSED**
