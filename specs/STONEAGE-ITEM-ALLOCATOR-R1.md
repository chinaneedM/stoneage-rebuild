# Original item initializer, static cursor and reuse — R1

Status: REMOTE ACCEPTED bounded. Action38068762702/job114261692113 SUCCESS
at f5bfbebcc26bed4bbdbbde06ed48bb9b41673187,11 steps/57 regressions/32 native
encounters including16 retained ownership encounters.80 successful allocations,
48 invalid-ID and16 full-pool rejections,32 original releases. Both artifact
reports independently downloaded and equal local bytes. Pinned Gavin `1f90cb6`
and Bismarck `999ffdf1` late-source builds only; no JSS1999/Taiwan-v1 promotion.

The wrapper extracts unchanged original `_ITEM_initExistItemsOne`,
`ITEM_CHECKITEMTABLE`, `ITEM_constructFunctable` and, for Bismarck, active
`ITEM_setLUAFunction`. Exact preprocessed body hashes are frozen separately
from the inherited item/header/character/battle witnesses. No original game
source or assets are committed. Empty native names execute the original lookup;
Bismarck executes the original fallback against the complete empty original
Lua sentinel. Nonempty Lua lookup/allocation/execution is outside this gate.

After each independently checked original second Loop reward encounter, a
separate explicit eight-slot pool and ID1 template run these controls:

| Control | Literal expectation |
| --- | --- |
| Table checks and rejected IDs -1,3,2 in length3 table | bounds and inactive IDs reject; pool/template/count/lookup unchanged |
| Only slot2 free, original cursor initially1 | allocate2; entire template copied and function pointers cleared by original construction |
| Release2, then only2 free | release preserves item bytes and decrements count; cursor wraps and reuses2 |
| Slots1–7 all active | returns-1 after original scan; entire pool and live count unchanged |
| Slots4/5 inactive; player1 carries4 but warehouse references5 | original scan protects4 by marking active, then reuses5; carried and warehouse references unchanged |
| Release5 with only warehouse reference | frees5 and decrements count; warehouse reference remains5 |
| Free6, then only1 free | next allocations6 and1; original cursor naturally returns to1 |
| Invalid construction indices and Bismarck Lua function bounds | no lookup or pool mutation |

Every comparison includes all256 original item records, all seven original
Char records, the complete BATTLE record, the full template and profile ID
table, and explicit live-count expectations. Reserved slot0 and records8–255
remain unchanged. Native lookup delta is exactly five times one initializer
lookup plus the original function-slot count. Template function pointers are
synthetic nonnull addresses that are never called; Bismarck template Lua fields
are synthetic nonnull addresses, cleared by the original empty fallback.
Template and table bytes remain immutable. Whole empty Lua sentinel is checked.

The carried stale-slot protection writes `use=1` without increasing the live
counter; the oracle preserves that original mismatch. The warehouse-only
reference can therefore alias a newly initialized item. These are bounded
adversarial source behaviors, not natural reachability or modern ownership
decisions. Existing presentation collectors suppress diagnostics/count strict
reward transport; original gameplay functions retain their bodies.

Fixture domains are restored only after all independent comparisons. The
original function-static cursor is never changed and naturally ends at1, so
the next encounter verifies persistence. O0/O2 nonrecovering UBSan must agree
byte-for-byte. The four inherited reward-item encounters and a separate shared/
duplicate/multiple-item matrix retain prior positive player/pet growth and
automatic arena/enemy release.

NEXT: recover original ITEM_makeItemAndRegist/ITEM_makeItem template construction,
table random fields and consumption, then original battle drop selection and
natural reward allocation with provenance. Initializer nonempty callbacks and
failure returns, unique-code/time generation, positive gold, actual transport,
Lua execution, original server ABI and first-release identity remain OPEN.
Pressure2486=2465 bounded closed+18 OPEN+3 historical UB; zero promotions.
