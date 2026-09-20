# StoneAge ordinary battle EXP settlement — R1

Date: 2026-09-20

Status: **descendant EXP attribution/settlement closed through ride-pet and source-shaped profit scans; exact JSS threshold profile/table remains OPEN**

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

For the reconstructed ordinary single-target ATTACK/GUARD/WAIT seam:

- a player kill awards the player;
- an allied-pet kill awards that allied pet;
- non-killing participants do not automatically share the reward.

The pinned descendant also closes the other **reward-attribution shapes**:

- **counter:** after each `BATTLE_Counter()` call, the loop rewrites
  `aAttackList[0] = attackNoSub` and immediately calls
  `BATTLE_AddProfit()`. The actual counter actor is therefore the single
  recipient for that profit trigger.
- **combo:** the loop builds one `aAttackList` from every combo member still
  valid, alive and able to move, then calls `BATTLE_Combo()`. In the pinned
  build, `_Item_ReLifeAct` is enabled and the complete combo attack list is
  then passed to `BATTLE_AddProfit()`; every listed member receives its own
  independently level-adjusted EXP rather than a split share.
- **deferred status death:** `BATTLE_StatusSeq()` can reduce HP to zero and
  set death state without calling `BATTLE_AddProfit()`. The later
  `BATTLE_AddExpItem()` scan does not retain a status/DoT owner; it scans all
  entries satisfying `HP <= 0 && ISDIE == false` and assigns every such
  reward to the **current** attack list before marking those entries processed.
  Therefore a status death can be collected by the next unrelated profit
  trigger. Reconstructing a modern "DoT owner gets credit" rule here would not
  reproduce this descendant behavior.

Full counter/combo/status **action execution** remains a separate combat-mechanics
surface; their EXP attribution no longer needs to be guessed.

## 3. Per-enemy award arithmetic

The stable level-gap rule already preserved by battle_exp_from_enemy() is
applied independently for each defeated enemy.

For reward EXP E and receiver-level gap (receiver_level - enemy_level):

- gap <= 5: E;
- gap 6..19: linearly reduced through 14/15 .. 1/15;
- gap >= 20: minimum 1.

No ordinary party-size divisor is present in this loop.

The stable source has a separate ride-pet award of 60% after the level-gap
calculation. `BATTLE_getRidePet()` resolves that recipient from the **player
actor's owned-pet slot**, not from the attack list. The ride pet uses its own
level for decay, then the result is multiplied by 0.60 with truncation and no
second minimum clamp.

The single-player battle session now preserves that relationship as an
explicit reward-only ride-pet snapshot. A ride pet can therefore receive
pending EXP even when it is not an independent allied battle actor. Settlement
preserves its persistent HP and sends threshold crossings through the same
explicit pet-growth/RNG seam as any other owned pet.

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

## 9. Explicit pet threshold-crossing settlement

The pet path now composes the selected EXP regime with the stable randomized
growth chain without hiding any RNG.

Persistent pet growth identity carries:

- PETRANK;
- packed individualized ALLOCPOINT;
- current internal VITAL / STR / TOUGH / DEX;
- hidden VARIABLEAI.

For every level gained, the caller must provide one `PetLevelGrowthRolls`
bundle containing all ten four-way allocation draws and the rank-band draw.
`resolve_pet_exp_growth_transition()` rejects missing or surplus bundles.

`SinglePlayerHistoricalRuntime.finish_persistent_battle_with_progression()`
then stages, validates and commits the resulting visible and hidden state
atomically. The visible compliance subset currently closed by evidence is:

- level / EXP / max EXP;
- max HP;
- attack;
- defense;
- quick.

Terminal battle HP is preserved unless it exceeds the recalculated maximum; no
level-up heal is invented. Hidden VARIABLEAI receives the stable +500 per
gained level with the recovered clamp. The derived visible AI/loyalty value is
left unchanged because its complete owner/charm/template compliance projection
is a separate seam.

Persistence r3 records VARIABLEAI; r2 migration supplies its recovered creation
default of zero, while r1 remains unable to invent missing growth identity.

Validation chain:

- `250a328660dcd070b0116880f4212c895818b0e8` / **35515398842** — explicit multi-level pet growth;
- `95f7e1e36f06eb4f9a00f3a35088dba32f56acc8` / **35515685028** — persistent hidden loyalty-growth state and atomic outcome staging;
- `687240810018cf5448daeef2e07d79f0e94dc3d3` / **35515940125**, **35515940131**, **35515940173** — integrated pet threshold crossing and all relevant validations.

## 10. Closed side-path attribution and remaining OPEN items

The descendant EXP attribution layer now has executable coverage for:

- ordinary one-actor kill profit;
- player -> owned ride-pet 60% side awards, including reward-only ride pets;
- counter-shaped one-actor profit lists;
- combo-shaped multi-actor profit lists without EXP splitting;
- the source's deferred dead-entry scan, including status deaths that have no
  retained DoT owner in the profit routine.

Validation:

- `ab9d3d90b87fcb857bc5f6ee24a10f2d816ad793` — ride-pet attribution;
  battle-core **35516458527**, gameplay **35516458580** success.
- `dce9ccc6a25f8135a5bad2145b1505c24b99528a` — reward-only ride-pet
  persistent settlement; gameplay **35516543065** success.
- `56fdb2c17aa96b51252b4ee939b2a99664a09487` — source-shaped profit
  scanning for counter/combo/deferred-status attribution; battle-core
  **35516770864** and gameplay **35516770753** success.

Still OPEN:

- JSS-1999 threshold representation and exact table;
- maximum-level and pet-limit-level behavior;
- complete visible pet AI/loyalty compliance;
- independent early-JSS confirmation of later-gated combo profit behavior,
  especially the `_Item_ReLifeAct` boundary;
- full counter/combo/status action, damage and status execution in the modern
  battle runtime. That execution work must reuse the closed attribution rules
  rather than redefine them.

Those uncertainties must remain visible rather than being hidden behind the
mixed 2.5 server defaults.
