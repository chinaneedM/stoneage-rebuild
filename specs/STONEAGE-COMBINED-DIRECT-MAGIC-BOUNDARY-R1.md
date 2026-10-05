# Combined direct-magic boundary R1

**COMBINED_DIRECT_MAGIC_MP_BOUNDARY_R1 = CLOSED_CONDITIONAL_ITEM_STATE.**
**RECOVERED25_COMBINED_ORDERED_RUNTIME = OPEN.**

This is later-descendant executable reference evidence, not a playable battle
implementation or proof of original Taiwan-v1 membership.

## Accepted recovered data

`agent/combined-runtime-r1-20261005` starts at verified main
`6e82eb913ae112e4b45f07aae9c90172d7d21e34`, tree
`cb7392f5923be3215be36720711f7a08a019d484`. Main's Combined reference
Actions 37263100740 and 37263234803 pass.

Selected-magic exact-pin Action **37263769848 PASS** at
`d86d3ff04fa2f9698bbc9adb7468d3f821c241ca`; derived report commit
`796e31d88d6d0256bb70366ac7ee9ef2e42b6abb` closes all 19 selected magic
rows across the seven data-only/positive Combined rows. The full `magic.txt`
hash is `b3a57b595bd60dfab571fe7af4dd6e2d43a5839c934eb644ba462897b1bcb6bb`.

Remote bridge Action **37264191245 PASS** at `9cfcf7b5c6bf8513958a3e24d9b149901dd4b04f` validates the exact-row submission bridge against recovered data. This boundary adds `EnemyAiCombinedSubmission.direct_magic_route`, retaining selection as a preceding operation and keeping actual effect execution open.

Only recovered IDs **627/632/637** remain positive runtime candidates. Their
choices bind to four ordinary wrappers:

| Combined ID | Selected magic | Wrapper |
| --- | --- | --- |
| 627 | 21 | MAGIC_Recovery |
| 627 | 139/159/169/179/189 | MAGIC_StatusChange |
| 632 | 240 | MAGIC_AttReverse |
| 637 | 61 | MAGIC_StatusRecovery |

Zero-reference Combined IDs 629/630/646/648 and their extra magic choices
remain data-only. No runtime pressure classification changes here.

## Item-pool dependency

All three fixed source profiles agree:

1. Combined selects a magic in its callback with one raw `rand()%count` draw
   and clears HIGH(COM3) to zero.
2. The battle dispatcher supplies that high half as DirectUse's `itemnum`.
3. For a non-player actor, DirectUse uses `itemnum` as an existing runtime
   item-pool index, so this path reads index **0**.
4. `ITEM_getInt(0, ITEM_MAGICUSEMP)` returns -1 if that slot is invalid, or
   reads the live instance's MP field if valid. Item validity includes its
   live `use` flag. This is not a lookup of configuration item ID 0.
5. The four ordinary wrappers compare current MP to that value and subtract
   it. The negative value is not clamped in DirectUse. With a witnessed
   invalid slot and ordinary nonnegative current MP, a successful wrapper
   can therefore increase MP by 1.

The AttackMagic non-player MP-dead seam cannot be reused for these wrappers.
Neither static recovered item data nor callback HIGH=0 proves the live item
pool's occupancy or MP field at the execution instant.

`RuntimeItemZeroWitness` deliberately distinguishes **unknown**, **observed
invalid**, and **observed valid with an MP value**. Unknown state rejects the
reference route unless Nocast short-circuits before any item access. A future
ordered runtime must obtain an authoritative witness or clearly identify an
explicit conditional execution profile. It cannot silently assume free magic.

## Ordering and return values

The callback owns selection RNG before DirectUse's positive Nocast gate.
Nocast can suppress the item read and wrapper, but cannot undo a draw already
consumed by an accepted callback. This supersedes any handoff wording implying
selection occurs only when a magic effect executes. Status/confusion handling
must be audited separately at its real setup/action boundary.

Missing function pointers still follow the item read. Invalid caster,
initialization mode and insufficient MP reject before deduction. Recovery's
all-target selector 22 rejects **after** MP deduction. Recovery discards its
battle helper's return and returns TRUE; StatusChange, StatusRecovery and
AttReverse propagate their helper's return. A reported successful Recovery
must not be equated with actual HP mutation.

## Reproducible validation

`tools/stoneage_combined_direct_magic_source_audit.py` verifies clean source
trees at the fixed pins used by the Combined reference audit. It preprocesses
the original DirectUse, ITEM integer accessor and four wrappers under each
profile's feature macros, then compiles them transiently with ASan/UBSan.

**1,600 defined native witnesses per profile, 4,800 total** agree with the
independent Python boundary model. Witnesses cover four wrappers, invalid and
valid item slots, negative/zero/positive costs, MP thresholds, invalid caster,
INIT, Nocast, missing callback, helper success/failure and selector 22.

Declared seams: non-player actor, FMINDEX=0, battling state, supplied item
validity/MP field and supplied battle-helper result. Helpers are stubs; target
selection, status parsing, HP/attribute mutation and persistence are not
validated by this native test. Original source is never committed.

## Remaining runtime work

- Actual-byte StatusChange/StatusRecovery parsers need conditional charset
  and table-bound audits; source-label arrays alone do not prove safe scans.
- Initiative must preserve the explicit gavin/iris scaled versus Bismarck
  fixed-range profiles.
- Exact positive-slot admission, target dispatch, effect RNG, state mutation,
  Nocast/status/confusion ordering and persistent coordinator integration
  remain open.
- Family MP modifiers, field routes, original compiler/libc identity and
  historical command encoding remain outside this boundary.
- Dedicated runtime, coordinator, golden, full-region and verified pressure
  gates are still required before adding these five slots to coverage.
