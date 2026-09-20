# StoneAge battle money R1

Status: **strong stable-descendant negative evidence; exact JSS-1999 server behavior remains unproven**

## Scope

This note asks one narrow question: does the reconstructed base battle reward path itself grant character currency?

It deliberately separates ordinary character economy fields such as `CHAR_GOLD` from battle reward semantics. A character having a gold balance does not prove that battles award gold.

## Primary stable descendant

Pinned source:

- repository: `gavinlinasd/StoneAge`
- commit: `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
- relevant files:
  - `gmsv/src/battle/battle.c`
  - `gmsv/src/char/enemy.c`
  - `gmsv/src/include/enemy.h`
  - `gmsv/src/include/char_base.h`
  - `gmsv/src/include/version.h`

### Result

**FACT (stable descendant):** the function is named `BATTLE_GetExpGold()`, but its body performs player EXP settlement, pet EXP settlement, level-up handling, battle-item settlement and the result packet. It contains no `CHAR_GOLD` write, no `CHAR_AddGold`, no `WORKGETGOLD`, and no equivalent battle-currency accumulator.

**FACT (stable descendant):** the enemy schema has `ENEMY_EXP` and `ENEMY_DUELPOINT`, followed by item/drop fields. There is no `ENEMY_GOLD` reward field.

**FACT (stable descendant):** `char_base.h` does contain the normal persistent `CHAR_GOLD` economy field and maximum-gold constants. Therefore the absence above is not explained by the source tree lacking a currency system; it is specific to the battle-reward path.

Repository search at the pinned lineage also finds no `_BATTLE_GOLD` or `getBattleGold` feature.

The safest interpretation is that “Gold” survives in the function name as an old semantic/name residue, while this stable implementation does not award battle currency.

## Independent control descendant

Pinned control:

- repository: `iriselia/StoneAge`
- commit: `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`

The corresponding `battle.c` retains `BATTLE_GetExpGold()` but likewise has no battle `CHAR_GOLD` mutation, `_BATTLE_GOLD`, or `getBattleGold`. Its `enemy.h` also has EXP/duel/item fields without an enemy-gold field.

This is strong cross-descendant negative convergence.

## Later private-server extension

A much later derivative, `BismarckDD/stoneage`, contains an explicitly gated extension:

```c
#ifdef _BATTLE_GOLD
  int gold = CHAR_getInt(char_index, CHAR_GOLD);
  if ((gold + getBattleGold()) > CHAR_getMaxHaveGold(char_index))
    gold = CHAR_getMaxHaveGold(char_index);
  else
    gold += getBattleGold();
  CHAR_setInt(char_index, CHAR_GOLD, gold);
#endif
```

Its configuration layer exposes `BATTLEGOLD`; `getBattleGold()` clamps the configured value to 0..100. The repository's setup configuration describes this as a battle-end money option.

This is not evidence for the early base rule. It is a named compile-time/configuration extension absent from both stable comparison descendants and is therefore excluded from the historical base profile.

## Reconstruction rule

For the current stable-descendant reconstruction profile:

- ordinary battle reward settlement does **not** create or mutate character money;
- persistent `gold` is carried through a battle unchanged;
- no per-enemy gold field, split formula, party-money allocator or random money roll is invented;
- any future optional “battle gold” feature must live in a separately named later/private-server or DESIGN profile, never in the historical base path.

Commit `a5f27d5dd792406e653ded8f4e1dce770851a710` makes this a regression invariant in the single-player runtime tests: a player beginning with `gold=1234` still has `gold=1234` after terminal HP settlement and after the below-threshold EXP settlement path.

Validation:

- Taiwan v1.0 gameplay Action `35518043576`: success.

## Confidence boundary

**CLOSED for the stable-descendant base profile:** do not award battle money.

**OPEN for exact 1999 JSS:** the original JSS server source/binary is still unavailable, so this negative convergence must not be overstated as byte-identical proof of the 1999 server.

This distinction is important: the reconstruction has enough evidence to reject an invented battle-money mechanic now, while still allowing an original artifact to revise the historical conclusion later.
