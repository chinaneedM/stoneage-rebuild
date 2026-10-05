# StoneAge PETSKILL_Combined ordered runtime R1

Status: **PENDING_FULL_REGION_AND_PRESSURE_ACCEPTANCE**  
Date: 2026-10-05  
Scope: recovered25 positive enemy uses of `PETSKILL_Combined` only.

## 1. Evidence boundary

This runtime is downstream of the already accepted bounded Combined reference:

- Full recovered25 callback population: 627 / 629 / 630 / 632 / 637 / 646 / 648.
- Positive enemy references only: **627 / 632 / 637**, five slot uses across five templates.
- Executable selected-magic choices:
  - 627 -> 21 / 139 / 159 / 169 / 179 / 189
  - 632 -> 240
  - 637 -> 61
- The callback consumes one `rand()%effective_count` draw, stores the selected
  magic in LOW(COM3), clears HIGH(COM3) to zero and dispatches
  `MAGIC_DirectUse`.
- HIGH(COM3)==0 is a **live item-pool index 0**, not a static item configuration
  identifier. The runtime therefore requires an explicit `RuntimeItemZeroWitness`.
- Status-magic bytes are admitted only under the explicitly conditional
  `iris_cp950` parser profile. This is not a claim about the recovered original
  executable charset.

No original JSS/Taiwan-v1 introduction date, original binary/compiler identity
or original numeric COM1 identity is inferred by this runtime.

## 2. Runtime admission

Ordered execution admits only IDs **627, 632 and 637**. Zero-reference family
rows 629/630/646/648 remain data-only.

The coordinator uses ordinary ATTACK only as an internal scheduling carrier.
The historical semantic command remains `BATTLE_COM_JYUJYUTU`; the modern
runtime does not assign that descendant numeric command value to the recovered
binary.

A `CombinedRuntimeOverlay` is mandatory when Combined executes. It carries
only explicit conditional/live state:

- descendant initiative profile:
  - `gavin_iris_scaled_30pct`, or
  - `bismarck_fixed_15`;
- status-magic profile: currently only `iris_cp950`;
- live item-pool slot-0 witness;
- explicit current MP for Combined actors;
- persistent semantic AttReverse flag for every battle participant.

The overlay cannot be synthesized from static item rows or guessed compiler
identity.

## 3. RNG ownership and ordering

The runtime keeps the source order explicit.

1. Enemy AI chooses the recovered skill slot.
2. Combined callback consumes exactly one reduced selection draw.
3. Initiative consumes its own explicit reduced draw according to the selected
   descendant profile.
4. `MAGIC_DirectUse` checks Nocast, item0, function/caster/battle state and MP.
5. Only after DirectUse reaches the battle-effect seam may target/effect RNG be
   consumed:
   - dead-single MultiList retarget draws 0..9 as required;
   - Recovery 21 consumes one reduced RAND(90,110);
   - eligible StatusChange consumes one RAND(1,100);
   - StatusRecovery 61 and AttReverse 240 consume no effect RNG.

Nocast, missing/invalid execution state or MP rejection never refunds the
already-consumed callback selection draw, and cannot consume downstream
target/effect RNG.

## 4. Initiative divergence

The fixed descendants disagree inside `BATTLE_DexCalc` for
`BATTLE_COM_JYUJYUTU`.

- gavin/iris: `WORKQUICK + 20 - RAND(0, work*0.3)`
- fixed Bismarck: `WORKQUICK + 20 - RAND(0,15)`

R1 requires the caller to select the profile explicitly. There is no
"original" default. The fixed Bismarck source has the older `dex<=1` clamp
commented out, so the Bismarck profile does not silently inherit the common
older clamp.

Persistent round preparation passes the Combined action value as an explicit
override into the common sorter; equal-value qsort uncertainty remains governed
by the existing explicit tie-break rule.

## 5. Positive effect seams

### Recovery 21

Verified recovered magic data derives `power=100, percent=0`. R1 admits the
non-riding battle path only.

- target resolution uses the ordinary single-target MultiList behavior;
- recovery rate is target-owned;
- RAND witness must be 90..110;
- HP is capped at MAXHP;
- actor MP is persisted in the Combined overlay.

Mounted/riding Recovery remains fail-closed.

### StatusChange 139 / 159 / 169 / 179 / 189

Under the conditional iris CP950 parser profile:

- 139 -> status index 1
- 159 -> status index 4
- 169 -> status index 6
- 179 -> status index 5
- 189 -> status index 3
- turn = 5
- downstream StatusAttackCheck offset = 15

The runtime calls the accepted common `StatusAttackCheck` model with explicit
combat stats/resistance and explicit RNG. Existing modeled late status blocks
the status attempt without consuming StatusAttackCheck RNG. Unmodeled late
status remains fail-closed.

Successful paralysis/sleep/stone command cancellation is applied immediately to
the target's round command. If the target has not yet taken its turn, normal
same-round StatusSeq processing then observes the newly written counter.

### StatusRecovery 61

Under iris CP950, ID 61 resolves to wildcard status 0. R1 reuses the accepted
Refresh status projection/recovery logic:

- select only the highest active modeled status;
- clear at most that one status;
- Nocast clear restores its NC flag/counter;
- unmodeled active status fails closed.

### AttReverse 240

R1 persists a semantic reverse flag and reuses the accepted
`BATTLE_MultiAttReverse -> BATTLE_AttReverse` behavior.

- cast toggles the flag;
- OFF->ON immediately swaps earth<->fire and water<->wind;
- ON->OFF leaves the currently reversed fixed values unchanged for the
  remainder of that round;
- the next persistent PreCommand boundary rebuilds baseline fixed elements and
  reapplies the flag if still ON.

This preserves the source timing rather than normalizing the OFF cast into an
immediate attribute restoration.

## 6. Persistent/coordinator integration

The persistent battle state carries `CombinedRuntimeOverlay` across rounds.
When battle entries are removed, MP/reverse maps are filtered to the remaining
session participants.

The local session coordinator:

- accepts an explicit Combined overlay at persistent-battle creation;
- consumes callback selection RNG during enemy-AI command construction;
- passes only post-selection action RNG into the ordered round;
- persists HP/status/Nocast/MP/AttReverse state through the existing battle
  transaction.

## 7. Explicitly open boundaries

R1 does **not** close:

- original recovered executable charset/compiler identity;
- gavin/iris vs Bismarck original lineage choice;
- exact libc RNG state identity;
- unknown live item-pool slot 0;
- family MP multipliers;
- field/non-battle DirectUse;
- Recovery target selector 22;
- mounted/riding Recovery;
- unmodeled extension statuses;
- malformed Combined OPTION behavior;
- execution of zero-reference IDs 629/630/646/648;
- unreferenced selected magic 306;
- original numeric COM1/array-index identity;
- original JSS/Taiwan-v1 membership or introduction date.

## 8. Acceptance gates

Accepted before final closure:

- Combined direct-wrapper source/data gate: **37265053597 PASS**
- Combined verified-data gate: **37265053470 PASS**
- Status-magic actual-byte gates: **37266411923 / 37266742566 PASS**
- Dedicated Combined ordered runtime: **37272560488 PASS**
- Local runtime coordinator including two-round Combined E2E:
  **37272501370 PASS**
- Runtime golden contract on the production integration:
  **37272234289 PASS**

Still required before pressure reclassification:

1. recovered25 full-region/runtime-stack gate **37272501409** must PASS;
2. only then add exact `PETSKILL_Combined` to the pressure classifier;
3. verified preservation-bundle pressure workflow must PASS and rewrite the
   derived report;
4. accept the mechanically selected next OPEN callback from that report.

Until those gates pass:

**RECOVERED25_COMBINED_ORDERED_RUNTIME_R1 = PENDING_FULL_REGION_AND_PRESSURE.**
