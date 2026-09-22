# StoneAge Combo DamageReact Ultimate Coupling R1

Status: **closed to the accepted stable-descendant base boundary**

Scope: the literal base `BATTLE_Combo` interaction between per-member
DamageReact handling and ultimate/knock-away bookkeeping. Profession/TRAP,
ACUPUNCTURE, BATTLE_MODEL and other macro-gated variants remain excluded.

## Fixed descendant witnesses

The same core ordering is present in the pinned descendant lineages:

- `gavinlinasd/StoneAge@1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
  - `gmsv/src/battle/battle_event.c`
- `iriselia/StoneAge@9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
  - `Source/gmsv/battle/battle_event.c`
- `BismarckDD/stoneage@999ffdf1d220ec6666eb65339180689c9caf1876`
  - `server/gmsv/battle/battle_event.c`

These are descendant witnesses, not direct 1999 JSS proof.

## 1. Per-member reaction path

For each Combo member the source pre-fetches:

`react = BATTLE_GetDamageReact(defindex)`

Base handling is then:

- REFLEC with non-throwing weapon:
  - call `BATTLE_DamageSub(...)` immediately;
- ABSROB or VANISH:
  - call `BATTLE_DamageSub(...)` immediately;
- otherwise:
  - call `BATTLE_DamageSubCale(...)`;
  - add the resulting rider/player and ride-pet portions into
    `AllDamage` / `AllPetDamage`.

The return value of every immediate `BATTLE_DamageSub` call is discarded.

That discarded return is not equivalent to “nothing happened”: the function
has already mutated HP, ride-pet HP/PETFALL, reaction charges and
`CHAR_WORKULTIMATE`.

The reconstruction therefore preserves the internal ultimate accumulator/reset
side effect while deliberately **not** converting the immediate return into
`BENT_FLG_ULTIMATE`.

## 2. Final DamageSub2 assignment

Only after the final Combo member does the source execute:

`ultimate = BATTLE_DamageSub2(last_attackindex, defindex,
                               &AllDamage, &AllPetDamage, refrect=-1)`

Consequences:

- only deferred/non-reacted Combo damage contributes to this assigned
  `ultimate` value;
- immediate REFLEC/ABSROB/VANISH returns do not survive into the local
  `ultimate` variable;
- `DamageSub2` still performs normal `CHAR_WORKULTIMATE` accumulator/reset
  mutation for its target.

## 3. Reflect target-order quirk

After `DamageSub2` has already executed against the original defender, the
source does:

`if (react == BATTLE_MD_REFLEC) defindex = attackindex;`

The subsequent death check, ABIO/enemy-critical override and final
`BENT_FLG_ULTIMATE` write use this rewritten `defindex`.

Therefore the source can:

1. compute an ultimate result from accumulated damage applied to the original
   defender;
2. rewrite `defindex` to the final Combo attacker because stale
   `react == REFLEC`;
3. write `BENT_FLG_ULTIMATE` to the attacker entry instead.

This also applies to the throwing-weapon Reflect bypass because the pre-fetched
`react` remains REFLEC even when reflection itself was blocked.

The project intentionally preserves this ordering rather than normalizing it.

## 4. AddProfit timing and round-local flag lifetime

`BATTLE_Combo` returns before the stable caller performs `BATTLE_AddProfit`.

Accordingly, all `BENT_FLG_ULTIMATE` writes produced inside one Combo call
exist before the subsequent death scan.

The source clears `BENT_FLG_ULTIMATE` at the start of each battle turn:

`entry.flg &= ~BENT_FLG_ULTIMATE`

So this flag is round-local, not persistent across turns.

The model consequently:

- stores explicit round-event flag target/kind metadata;
- first collects all flag writes from a Combo call;
- then scans deaths, matching the post-Combo `BATTLE_AddProfit` order;
- does not persist the raw entry flag into `PersistentBattleState`.

## 5. Proven edge cases now represented

### 5.1 Immediate Reflect ultimate return discarded

If immediate reflected damage itself crosses the ultimate threshold,
`BATTLE_DamageSub` may return kind 1/2 and reset `CHAR_WORKULTIMATE`, but
because `BATTLE_Combo` discards that return, no entry ultimate flag is created
from that return alone.

A reflected attacker can therefore die normally even though the immediate
damage function internally classified the hit as ultimate.

### 5.2 Final Reflect misroutes DamageSub2 ultimate flag

If earlier deferred Combo damage makes final `DamageSub2` return ultimate,
while the final member has stale REFLEC:

- accumulated damage is applied to the original defender;
- the local `ultimate` value comes from that defender transaction;
- death check/flag target is then changed to the final attacker;
- the attacker entry may receive `BENT_FLG_ULTIMATE`;
- the original defender can die without that flag and therefore follow normal
  death handling in the subsequent AddProfit scan.

This is a literal source quirk, not a design choice.

## 6. Reconstruction representation

`OrdinaryRoundEvent` now has explicit round-local fields:

- `ultimate_flag_target_slot`
- `ultimate_flag_kind`

These are distinct from:

- `ultimate_damage_resolution` — what a damage helper internally computed;
- `ultimate_kind` — the source-visible final local ultimate value on the
  relevant execution path;
- `ultimate_exited_participant_ids` — who actually went through
  `BATTLE_UltimateExtra` after the AddProfit death scan.

Persistent death penalties use the actual ultimate-exit set rather than simply
assuming every internal damage classification caused UltimateExtra.

## 7. Deliberate exclusions

Still outside this R1 boundary:

- exact 1999 JSS confirmation;
- profession TRAP;
- ACUPUNCTURE;
- BATTLE_MODEL variants;
- LER immunity variants beyond already isolated core guards;
- counter-with-ride interaction.

## Validation

Implementation:

- `fdc12106fa91a45d8cc08224e3d662b6685abdba` — add round-local
  `BENT_FLG_ULTIMATE` representation and make persistent ultimate penalties
  depend on actual UltimateExtra exit;
  - battle-core **35723010783** success;
  - gameplay **35723010759** success;
  - pet-skill **35723010689** success.
- `17eae020746968f18cc8aa5cdd2839f9b7346fca` — preserve discarded immediate
  `BATTLE_DamageSub` ultimate returns, their accumulator side effects, final
  `DamageSub2` assignment and Reflect target-order misrouting;
  - battle-core **35723491402** success;
  - gameplay **35723491531** success;
  - pet-skill **35723491375** success.

Regression coverage explicitly proves both discarded-immediate-return behavior
and the final Reflect misrouted flag case.
