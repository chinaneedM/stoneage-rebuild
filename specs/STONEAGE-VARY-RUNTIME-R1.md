# StoneAge PETSKILL_Vary ordered runtime R1

Status: **PENDING_FULL_REGION_AND_PRESSURE_ACCEPTANCE**  
Date: 2026-10-05  
Scope: recovered25 positive enemy uses of `PETSKILL_Vary` / ID 600 only.

## 1. Evidence boundary

This runtime is downstream of the accepted bounded Vary reference:

- exact recovered25 callback population: ID **600** only;
- FIELD **1**, TARGET **5**, COST **2**, ILLEGAL **1000**;
- TARGET 5 is `PETSKILL_TARGET_NONE`;
- exact positive enemy references: **4 slot uses / 4 templates**;
- all positive references are enemybase **PETSKILL3**:
  TEMPNO 981/982/983/984;
- recovered OPTION length **22**, SHA-256
  `17e7ff6e7530a5fc2a0964432699f6c82a3dcc79374a2bad6fc547bbdc5e6f99`;
- transformed wolf image **101428**;
- the callback resets `WORKTURN` to zero and blocks recast while image
  101428 is active.

The verified preservation-bundle executable discriminator was attempted before
runtime profile selection. It found one 273-byte ELF candidate in the bounded
server tree and no `PETSKILL_Vary` symbol carrier. The result is explicitly
`inconclusive_symbol_unavailable`; it does not select a descendant profile.

## 2. Explicit descendant profiles

No "original" profile exists in R1. The caller must choose one of two
gameplay-significant descendant profiles explicitly.

### gavin / iris

- ATTACKPOWER = FIXSTR + trunc(FIXSTR * 0.30)
- QUICK = FIXDEX + trunc(FIXDEX * 0.30)
- DEFENCEPOWER is not modified by Vary;
- the Vary action owns the visual-effect path.

### fixed Bismarck

- ATTACKPOWER = FIXSTR + trunc(FIXSTR * 0.30)
- DEFENCEPOWER = FIXTOUGH + trunc(FIXTOUGH * -0.50)
- QUICK = FIXDEX + trunc(FIXDEX * 0.30)
- the fixed pin does not compile the expansion visual-effect body.

The coordinator therefore requires an explicit profile for each selected
Vary actor. Missing, unknown or surplus profile witnesses fail closed.

## 3. Ordered execution

The recovered numeric COM1 value is not proven. R1 uses ordinary ATTACK only
as an internal scheduling carrier, then intercepts the semantic Vary action
before physical attack settlement.

The callback changes QUICK before `BATTLE_DexCalc`. Therefore the common
round sorter receives the callback-updated QUICK on the initial Vary action.
There is no Vary-special initiative formula: the ordinary action-value path is
used with the transformed QUICK.

The semantic Vary action:

- occupies its normal ordered action position;
- does not deal physical damage;
- is marked with skill ID 600;
- exposes only the profile-owned visual-effect boolean;
- is excluded from ordinary counter and combo-attack eligibility.

Confusion/status command rewrite can suppress the semantic action through the
existing common command lifecycle.

## 4. Persistent transformation lifetime

`VaryRuntimeOverlay` carries only active transformed work state. Immutable
battle/session baseline values are not overwritten.

After successful Vary execution:

1. callback state begins at WORKTURN 0;
2. the initial Vary action advances it to 1;
3. each later completed action by that actor advances it once;
4. when 5 advances past the source threshold, the sixth actor action expires
   the transformation;
5. the overlay then removes the actor and subsequent snapshots use baseline
   battle/session powers again.

Expiry restoration is profile-specific:

- gavin/iris restores base image, attack and quick;
- Bismarck restores base image, attack, defense and quick.

Battle termination/escape drops the Vary overlay. Entry removal filters that
actor from the overlay. Recast while active fails closed.

## 5. Recovered enemy-AI admission

`resolve_enemy_ai_vary_submission` requires all of the following:

- exact callback population ID 600;
- exact recovered row metadata;
- exact OPTION byte length/hash;
- selected slot = PETSKILL3;
- actor TEMPNO in 981/982/983/984;
- exact recovered template graphic identity;
- enemy actor provenance;
- explicit descendant profile.

The local runtime coordinator admits Vary only when the recovered enemy AI
selects the matching `wa` slot. The AI target is preserved solely as the
callback COM2/visual target carrier; it is not reinterpreted as player target
selection for TARGET_NONE.

## 6. Fail-closed interaction boundary

R1 deliberately rejects unsupported work-power composition rather than
inventing an ordering rule. In particular, active Vary is not composed with:

- mounted ride work state;
- drunk work-power modification;
- prepared Weaken powers;
- prepared SetMagicPet powers;
- another semantic callback that owns the same action;
- conflicting callback setup attack/defense writes.

These are bounded R1 exclusions, not claims that historical servers could
never combine the systems.

## 7. Explicitly open boundaries

R1 does **not** establish:

- which descendant profile matches the recovered original executable;
- recovered original executable/compiler/charset identity;
- original numeric `BATTLE_COM_S_VARY` value;
- original JSS/Taiwan-v1 membership or introduction date;
- expansion-image behavior outside the fixed source pins;
- client display/name text;
- unmodeled overlap ordering with the fail-closed work-power systems above.

## 8. Acceptance gates

Accepted before final closure:

- bounded recovered executable-profile discriminator:
  **37282101502 PASS**; result inconclusive by symbol evidence;
- recovered Vary state/admission gate:
  **37282884905 PASS**;
- persistent six-action lifetime gate:
  **37285199740 PASS**;
- latest dedicated Vary runtime including enemy-AI coordinator E2E:
  **37286463853 PASS**;
- latest full local runtime coordinator on the Vary E2E commit:
  **37286420982 PASS**;
- runtime golden contract on the production coordinator integration:
  **37286013147 PASS**.

Pending final closure:

- recovered25 full-region/runtime-stack gate: **37286420991 RUNNING**;
- verified preservation-bundle pressure reclassification:
  **37286756850 RUNNING**.

Until both final gates pass, Vary remains pending pressure closure and the
accepted positive-slot coverage remains **2444/2486 = 98.31%**.

**RECOVERED25_VARY_ORDERED_RUNTIME_R1 = PENDING_FINAL_ACCEPTANCE.**
