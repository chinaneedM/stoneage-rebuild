# BattleModel empty-equipment ItemCrush chronology R1

Date: 2026-10-06 (UTC+8)
Status: **CLOSED_BOUNDED_EMPTY_EQUIPMENT_ITEMCRUSH_FULL_RUNTIME_OPEN**

## Evidence and declared variants

Three clean fixed descendant pins remain gavin1f90cb6c, iris9e6c8ce2 and
bismarck999ffdf1. Their battle.c declares gItemCrushRate=400000. This is a
source default, not an inferred original executable setting. Context requires
an explicit current global rate and raw rand maximum; the audit supplies raw
values and does not reproduce an original libc generator or its state.

The reduced five-slot equipment enum is read transiently from each pin's
char_base.h with extra belt/shield/shoes/glove features excluded. Bismarck's
separate pet equipment enum has seven slots. Context requires every mapped
participant's identity/kind/level and an explicit all-minus-one equipment
tuple; real equipment and wrong tuple lengths fail closed. Actor/defender
levels additionally match the physical profiles when using the real adapter.

| Declared variant | Fixed source evidence | Empty-equipment behavior |
| --- | --- | --- |
| legacy | all three | Player actual defender draws RAND(1,currentRate), strict roll<level; successful check scans five items and returns FALSE at empty j==0, before any second RAND. Nonplayers draw nothing. |
| take_itemdamage | all three | Actual defender draws full raw rand, reduces modulo100 to weighted initial slot, scans five empty slots; then attacker ARM lookup. No further draw or mutation. |
| take_itemdamage_fix | bismarck | Initial slot uses raw rand modulo five instead of weighted modulo100. |
| take_itemdamage_pet | bismarck | Pet scan length is seven, weighted initial slot still modulo100. |
| take_itemdamage_pet_fix | bismarck | Pet initial slot is raw rand modulo seven; player/enemy remains modulo five. |

**FACT (literal source boundary):** all TAKE variants retain `(slot+1)%5`
after a failed lookup, including seven-slot pets. For pet FIX raw6, observed
lookup sequence is6,2,3,4,0,1,2; it is not silently normalized to modulo7.
This is an experimental reconstruction witness, not production equipment logic.
Macro combinations do not establish membership in any original retail build.

## Caller order and RNG ownership

New `ITEMCRUSH_HIT_LOOP_SCOPE_R1` replaces only the previous explicit
no-ItemCrush exclusion with declared empty-equipment ItemCrush. Reduced
SIDE_OFFSET10/no ride/nonthrowing/gDamageDiv0 and the neutral physical scope
remain mandatory. Old no-ItemCrush scope still works and rejects an ItemCrush
context; new scope requires one. Ordinary round/state/coordinator is not enabled.

- Source helper calls ItemCrush whenever the actual defender survives, after
  damage/wakeup and before status. No positive-damage gate is added.
- **DODGE, MISS, ALLGUARD and zero damage still reach ItemCrush** on a surviving
  target. DODGE skips settlement but now retains ItemCrush before marker restore.
  Its safe modern presentation damage0 is not a historical wire-value claim.
- Original target selection/pet pre-hit guard/physical Duck/Guardian order is
  retained. The actual live Guardian determines ItemCrush type and level.
- Dead targets skip ItemCrush. Critical pet death owns its death draw first;
  later sampled dead targets retain selection RNG and skip physical/item work.
- `itemcrush_check` and `itemcrush_raw_rand` are distinct owned tape entries,
  with scheduled ordinal/range validation. AttackSeq cannot consume them.
  Item checks still occur if a preexisting status suppresses later status RNG.
  Missing, unused or misordered draws fail closed; no item mutations are invented.

## Validation and acceptance boundary

170 shared/admission/loop/physical/core/Guardian tests PASS locally, including13
new ItemCrush tests. Real physical witnesses cover guard-clearing followed by
later item checks, real Duck with item RNG, real critical pet death, reflection,
Guardian kind routing, empty scans, strict level threshold, modulo boundaries,
explicit feature/profile/identity/rate and owner failures.

Native audit transiently compiles original Check/Seq/helper and original legacy
ItemCrush empty-scan body. TAKE mutation is a controlled trap proven unreachable
with the original empty check; equipped mutation remains outside this audit.
Physical settlement/status arithmetic and getters are controlled dependencies,
already independently accepted elsewhere; this is not a complete native battle.
Each variant runs60 direct sequence cases plus320 original helper cases. Two
variants each at gavin/iris yield760/profile; five at bismarck yield1900;
**3420 comparisons total** verify checks/raw/death/status ownership, reachability,
lookup recipient/order and item-RNG-before-status phase. Source files/hashes are
emitted; original code is not retained. Existing696 native physical comparisons
remain PASS. Extended settlement CI also reproduces1920 settlement calls,480
marker comparisons and60 pet guards. Exact remote input/run follows publication.

**OPEN:** equipped mutations and recomputed stats/UI/persistence, extra equipment
slot features, original PRNG/build/charset/numeric COM1 membership, prepared
action cancellation, ordinary round/state/coordinator propagation, ultimate exit,
golden/full-region and verified pressure. Empty-equipment ItemCrush agreement
does not close ID638's two positive slots or alter existing coverage.


## Remote bounded acceptance — 2026-10-06

37411512720 SUCCESS, job112100761415, exact input
7c7de32d7284eca3ea4dc66b8534f0c04bc14455,
tree8b81bae80313f02aed8295a21a10917c99de97ed.170 shared tests,3420
ItemCrush comparisons,696 physical comparisons,1920 settlement/480 marker/
60 pet checks reproduce remotely; derived artifact11389775634 uploaded.
Earlier pending records are historical and superseded. Acceptance receipt:
`research/recovered/STONEAGE-BATTLEMODEL-ITEMCRUSH-ACCEPTANCE-R1.json`.
Only explicit empty-equipment chronology is closed; all full-runtime and
equipped/feature/profile boundaries above remain OPEN, zero638 slots promoted.
