# StoneAge ordinary battle EXP settlement — R1

Date: 2026-09-20

Status: **ordinary single-hit accumulation and explicit player threshold-crossing profiles closed; exact JSS profile/table and pet level-up remain OPEN**

## Purpose

This record separates three concepts that descendant code keeps distinct:

1. enemy reward EXP;
2. battle-local pending EXP (CHAR_WORKGETEXP);
3. persistent character EXP plus level-transition policy.

Keeping those boundaries separate prevents later private-server progression
features from leaking into the early reconstruction.

## 1. Stable source chain

Pinned stable-descendant reference:

- gavinlinasd/StoneAge@1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56
- gmsv/src/battle/battle.c
- gmsv/src/char/char.c
- gmsv/src/char/char_base.c
- gmsv/src/char/char_data.c

The relevant ordering is:

    battle entry
      -> BATTLE_ClearGetExp()
      -> WORKGETEXP = 0 for player and owned pets

    ordinary action resolves
      -> BATTLE_AddProfit()
      -> BATTLE_AddExpItem()
      -> newly dead enemy scanned once
      -> adjusted reward added to acting participant WORKGETEXP

    battle finish
      -> BATTLE_GetProfit()
      -> BATTLE_GetExpGold()
      -> living player BATTLE_GetExp()
      -> living owned pets with WORKGETEXP > 0 BATTLE_GetExp()
      -> level checks

## 2. Ordinary kill attribution

Before an ordinary actor executes, stable BATTLE_AttackSeq initializes the
attack list to that actor alone.

After the attack it calls BATTLE_AddProfit(). BATTLE_AddExpItem() scans enemies
satisfying HP <= 0 and not already marked dead. The reward is therefore
processed on the first qualifying death scan and the enemy is then marked dead.

For the currently reconstructed ordinary single-target ATTACK/GUARD/WAIT seam:

- a player kill awards the player;
- an allied-pet kill awards that allied pet;
- non-killing participants do not automatically share the reward.

Combo/counter/status execution can construct different attack lists and
remains outside this R1 attribution seam.

## 3. Per-enemy award arithmetic

The stable level-gap rule already preserved by battle_exp_from_enemy() is
applied independently for each defeated enemy.

For reward EXP E and receiver-level gap (receiver_level - enemy_level):

- gap <= 5: E;
- gap 6..19: linearly reduced through 14/15 .. 1/15;
- gap >= 20: minimum 1.

No ordinary party-size divisor is present in this loop.

The stable source has a separate ride-pet award of 60% after the level-gap
calculation. That path is not yet represented by the current single-player
battle participant model and remains separate.

## 4. Reconstruction state

Implementation:

- BattleParticipant.reward_exp preserves concrete enemy reward provenance
  from EnemyVariantBridge.exp_override.
- PersistentBattleState.pending_exp_by_participant_id is initialized to zero
  for player-side battle participants.
- ordinary round resolution adds EXP only when one event changes an enemy from
  positive HP to zero.
- the pending accumulator survives across rounds and is not itself persistent
  character EXP.

Commit:

- 81e9572f1ff309982d13c7f1979a51516a5593a8

Validation:

- gameplay-model run 35514277568 — success;
- battle-core run 35514277633 — success.

## 5. Finish-time recipient eligibility

Stable BATTLE_GetExpGold() first rejects a dead player. Its owned-pet EXP loop
is below that early return.

Therefore, for the current one-player PvE reconstruction:

- a dead player receives no pending EXP;
- when the player is dead, owned pets do not receive their pending EXP through
  that result path either;
- when the player is alive, dead pets are skipped;
- living pets with positive pending EXP may proceed to their own EXP/level
  processing.

This is stricter than a generic all-surviving-participants-gain-EXP rule.

## 6. EXP/max-EXP semantics and the level-transition split

Taiwan v1 directly exposes separate numeric EXP and max-EXP positions in the
player and pet status surfaces. The semantic labels are supported by the early
generated protocol lineage.

Stable descendant CHAR_makeStatusString('P') likewise sends:

- CHAR_EXP as EXP;
- CHAR_GetLevelExp(level + 1) as max/next EXP.

However, the descendant code preserves two different progression regimes.

### Legacy compiled cumulative path

Without _NEWOPEN_MAXEXP:

- CHAR_AddMaxExp() adds the award to persistent CHAR_EXP;
- CHAR_LevelUpCheck() compares that cumulative value with
  LevelUpTbl[level + 1];
- level increments do not subtract the crossed threshold.

Therefore EXP and next EXP are in cumulative coordinates.

### Later external per-level path

With _NEWOPEN_MAXEXP / external EXP configuration:

- CHAR_EXP represents progress within the current level;
- CHAR_GetLevelExp() returns the per-level requirement;
- CHAR_HandleExp() subtracts the requirement when a level is gained.

The recovered mixed 2.5 exp.txt belongs to this later/configurable evidence
track. It is not automatically an early JSS threshold table.

## 7. Reconstruction-safe common subset

Before a threshold is reached, both regimes perform the same observable
operation:

    new_exp = current_exp + pending_exp
    level unchanged
    max_exp unchanged

Therefore SinglePlayerHistoricalRuntime.finish_persistent_battle_without_level_crossing()
implements only the common subset and requires:

    current_exp + pending_exp < max_exp

If the award reaches or crosses max EXP, the method fails before applying any
HP/EXP mutation.

Commit:

- b3207d71bc8dafa557e31d3450be2d6efb00bd29

Validation:

- gameplay-model run 35514525635 — success.

## 8. Explicit player threshold-crossing settlement

`tools/stoneage_player_growth_model.py` now represents both recovered
progression regimes explicitly:

- `LEGACY_CUMULATIVE_EXP`: cumulative EXP is retained after each level;
- `PER_LEVEL_EXP`: each crossed current-level requirement is subtracted.

`resolve_player_exp_transition()` requires every post-crossing threshold as an
explicit input. It returns, rather than hides, the stable player side effects:

- `+3` free-stat points per gained level;
- duel points `+= new_level * 10` for each gained level;
- charm `+2` once when one or more levels are gained.

`SinglePlayerHistoricalRuntime.finish_persistent_battle_with_player_progression()`
can now persist a player crossing only when:

- the progression profile is explicitly selected;
- all required future threshold values are supplied;
- the persistent player already contains `free_stat_points`, `charm`, and
  `duel_point_like_state` so no new field is fabricated.

Pet EXP remains prevalidated before any mutation. If a living pet would reach
or cross its own `max_exp`, the entire settlement is rejected atomically until
the randomized pet-growth seam is modeled.

Validation:

- `509ac9fa68e67ce3e962bb700eae7e1817aee578` / run **35514947237** — player EXP profile model;
- `1a48e8f57d3673c3a902351a754b5c6e5d8907f4` / run **35515032705** — runtime player threshold-crossing settlement.

## 9. Explicitly OPEN

Before threshold-crossing persistence can be promoted for the early baseline,
the project still needs an explicit/versioned decision or stronger evidence
for:

- JSS-1999 threshold representation and exact table;
- pet level-up random growth application;
- maximum-level behavior;
- ride-pet EXP;
- combo/counter/status kill attribution.

Those uncertainties must remain visible rather than being hidden behind the
mixed 2.5 server defaults.
