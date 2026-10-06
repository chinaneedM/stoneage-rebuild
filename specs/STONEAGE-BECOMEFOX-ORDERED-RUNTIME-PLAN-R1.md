# StoneAge BecomeFox ordered/runtime semantics plan R1

Date: 2026-10-06  
Status: **SOURCE_EXECUTION_ORDER_GATE_IMPLEMENTED / NATIVE_PENDING**

The accepted recovered25 source/data reference closes ID625 and its two exact
placements, but does not yet authorize a pressure promotion. This stage separates
effective execution from misleading comments or dead writes before any persistent
runtime implementation is admitted.

## Corrected execution-order finding

All three pinned descendants write `dex=(QUICK+20)*0.8` before the
`BATTLE_DexCalc` command switch. ATTACK, GUARD and NONE have no dedicated case
there and therefore reach `default`, which recomputes `work` and overwrites
`dex`. Consequently the source comment describing an additional20-percent
initiative penalty is **not** accepted as an effective runtime rule for the
commands a fox is actually allowed to use.

The profile divergence is material: gavin/iris default dex uses a RAND upper
bound of work*0.3, while fixed Bismarck uses work*0.1. That divergence must stay
versioned until executable evidence resolves it.

## Bounded semantic model

The R1 model admits only source facts that survive execution-order review:

- post-hit command/result/alive gates precede the one modulo-100 draw;
- the draw occurs before target type, PETFLG and optional pig eligibility;
-30 succeeds and31 fails the `<31` predicate;
- success sets FOXROUND to the current turn and image101749;
- ride cleanup is success-only;
- active FOXROUND rewrites attack/defense/quick from fixed baselines at action
  time using C-style truncation;
- recovery is strict turn difference >2 and restores image/fixed powers/marker;
- exit restores image/marker only;
- PetIn reset occurs before NORETURN, restores attack+quick but not defense, and
  preserves the ordinary-int (gavin/iris) versus work-int (Bismarck) marker split.

## Next gate

A dedicated transient native harness must execute the exact postattack
BecomeFox block for all three pinned descendants with controlled draw/result/
target inputs and compare every side effect against this bounded model. After
that, whole ordered command integration and persistent recovered25 runtime can
be admitted separately. No pressure change occurs in this source-order commit.
