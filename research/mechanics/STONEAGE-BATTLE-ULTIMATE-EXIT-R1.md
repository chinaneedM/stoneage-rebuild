# StoneAge Battle Ultimate Exit R1

Status: **reconstructed to the accepted stable-descendant boundary**

Scope: the base `BATTLE_UltimateExtra` / `BATTLE_Exit` behavior that follows
an already-classified ultimate/knock-away death. This document does not promote
later profession, TRAP, ACUPUNCTURE, BATTLE_MODEL or other macro-gated branches
into the base rule.

## Evidence anchors

The behavior below is cross-checked against the pinned descendant lineages:

- `gavinlinasd/StoneAge@1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
  - `gmsv/src/battle/battle.c`
  - `gmsv/src/battle/battle_event.c`
- `iriselia/StoneAge@9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
  - `Source/gmsv/battle/battle.c`
  - `Source/gmsv/battle/battle_event.c`
- `BismarckDD/stoneage@999ffdf1d220ec6666eb65339180689c9caf1876`
  - `server/gmsv/battle/battle.c`
  - `server/gmsv/battle/battle_event.c`

These are descendant witnesses, not proof of exact 1999 JSS behavior. Where the
three lineages expose the same base path, this project treats the result as the
strong stable-descendant reconstruction boundary.

## 1. Ultimate exit is immediate, not round-end cleanup

The stable command loop calls `BATTLE_AddProfit()` immediately after an
ordinary `BATTLE_Attack()`. It also calls `BATTLE_AddProfit()` immediately
after every `BATTLE_Counter()`.

Therefore an ultimate death is processed before later actors in the same
already-sorted command list execute.

The reconstruction consequence is important:

- the victim is removed from the active battle-entry set immediately;
- later targeting cannot select that entry;
- a later scheduled action belonging to an exited entry is skipped;
- when the victim is a player, the paired/default active pet is exited first,
  so that pet cannot execute a slower action later in the same round.

A round-end-only implementation would be observably wrong.

## 2. Profit scan order

The stable death scan performs this order:

1. detect HP <= 0 while `CHAR_ISDIE` is still false;
2. set `CHAR_ISDIE = true`;
3. mark/increment death bookkeeping;
4. if the battle entry has `BENT_FLG_ULTIMATE`:
   - call `BATTLE_GetProfit(battleindex, victim_side, victim_entry)`;
   - then call `BATTLE_UltimateExtra(..., victim)`;
5. otherwise call `BATTLE_NormalDeadExtra(...)`.

This means ultimate death is not equivalent to ordinary death plus a cosmetic
flag.

### 2.1 Why the ultimate victim does not receive pending Finish profit

`BATTLE_GetExpGold()` immediately returns when the target entry has
`CHAR_ISDIE == true`.

Because the death scan sets `ISDIE` before the ultimate-path
`BATTLE_GetProfit()`, that immediate call cannot settle the dead player's
pending battle EXP or item buffer.

`BATTLE_UltimateExtra` then removes the entry through `BATTLE_Exit`.

Later, `BATTLE_Finish()` iterates only entries whose character index is still
valid in the battle array, and for each remaining entry executes:

`BATTLE_GetProfit -> BATTLE_Exit`.

An ultimate-exited player is no longer present in that loop. Consequently the
reconstruction must not reinterpret the player's post-exit HP=1 as “alive and
eligible for final EXP/drop settlement.”

This differs from an ordinary dead player that remains a battle entry until
Finish.

## 3. Victim-type behavior in BATTLE_UltimateExtra

### 3.1 Player victim

The stable path:

1. calls `BATTLE_PetDefaultExit(player, battleindex)`;
2. applies the ultimate-specific player charm penalty in PvE/non-no-risk;
3. applies the ultimate-specific VARIABLEAI penalty to the default pet when
   present;
4. in the ordinary PvE branch, calls
   `CHAR_getElderPosition(CHAR_LASTTALKELDER,...)`;
5. if that lookup succeeds, warps the player to the returned elder position;
6. calls `BATTLE_Exit(player,battleindex)`;
7. discharges the party.

The repository does not fabricate `CHAR_LASTTALKELDER` population or an elder
registry. The single-player runtime therefore requires the elder lookup result
as an explicit input:

- a `MapPosition` means the historical lookup succeeded and that position is
  used as the post-battle world position;
- `None` means the lookup failed and the player remains at the battle-origin
  world position.

### 3.2 Pet victim

The stable path:

- clears the owner's default-pet selection;
- applies the ultimate-specific pet VARIABLEAI penalty in the eligible PvE
  path;
- increments the owner's dead-pet counter in the source branches where that
  counter is maintained;
- calls `BATTLE_Exit(pet,battleindex)`.

The pet does not receive the player-wide `BATTLE_Exit` recovery loop at this
instant. It remains dead until later owner/player exit recovery, where
applicable.

### 3.3 Enemy/other victim

The stable path marks the battle flag and calls `BATTLE_Exit`. Enemy exit
destroys the runtime enemy object in the descendant server implementation.

The reconstruction retains enough victim identity in persistent battle state to
audit already-earned kill profit, while marking the entry as ultimate-exited so
it is no longer active.

## 4. BATTLE_Exit cleanup relevant to the current base scope

For a player exit, the stable path includes:

- battle entry removal;
- entry escape counter reset;
- battle mode/index detachment;
- dead-player recovery to HP=1;
- paired/default pet battle-entry removal;
- `BATTLE_BadStatusAllClr(player)`;
- PETFALL cleanup and ride removal when the fall flag is present;
- iteration over carried non-mail pets:
  - dead or HP<=0 pets are restored to HP=1;
  - their battle mode is cleared;
  - `BATTLE_BadStatusAllClr(pet)` is applied.

Within the current common status scope, `BATTLE_BadStatusAllClr` clears the
base poison/paralysis/sleep/stone/drunk/confusion counters.

It does **not** establish a source basis for clearing DamageReact
VANISH/ABSROB/REFLEC state on exit. Those work fields are explicitly reset by
new battle entry initialization instead. The reconstruction therefore does not
invent an exit-time DamageReact clear.

Likewise, no source-backed `BATTLE_Exit` reset of `CHAR_WORKULTIMATE` was
found; the damage functions own that accumulator/reset behavior.

## 5. Reconstruction representation

The in-process model now carries
`ultimate_exited_participant_ids` separately from HP.

This is necessary because:

- a player can be restored to HP=1 by `BATTLE_Exit` while still no longer
  being a battle entry;
- HP alone can no longer determine whether the actor may execute another action
  or receive final battle profit.

The round resolver applies ultimate exits immediately after the attack/counter
profit-trigger point. The persistent state excludes those IDs from later active
participants and side-liveness checks.

For a player ultimate exit, the runtime provides a dedicated settlement seam:

`finish_persistent_player_ultimate_exit(state, elder_return_position=...)`

That seam:

- commits HP/charm/pet loyalty/dead-pet-count exit effects;
- does not settle pending battle EXP or item drops for the exited player;
- uses an explicit elder-return lookup result rather than inventing a location.

The ordinary victory/defeat progression finishers reject a player-ultimate
terminal so the restored HP=1 cannot accidentally re-enable final profit.

## 6. Deliberate exclusions

Still outside this R1 boundary:

- exact 1999 JSS confirmation;
- population/history of `CHAR_LASTTALKELDER` and the elder registry;
- PvP duel-point variants beyond already isolated stable core evidence;
- DEATH_CONTEND and other later compile-time variants;
- profession/TRAP/ACUPUNCTURE/BATTLE_MODEL extensions;
- Combo + DamageReact ultimate return-value/target-order coupling;
- counter-with-ride behavior.

## Validation

Implementation commits:

- `2419c9c2119899764231ea334985f0cf4cac7041` — immediate AddProfit-shaped
  ultimate entry exit, same-round action suppression and player exit cleanup.
- descendant validation head
  `3d2163d26df3bb7403c3fed992c1fd171aecd9ea`:
  - battle-core **35720347532** — success;
  - gameplay **35720347455** — success.
- `cddb50c8b20bd0400fe8c6d6f72fc9a1e6dfe24a` — dedicated player ultimate
  terminal settlement, explicit elder-return input and no erroneous final
  EXP/drop settlement;
  - gameplay **35720731472** — success.

Regression coverage includes:

- ultimate-killed player immediately exits with the default active pet;
- the slower pet action is skipped in the same round;
- player exit restores HP=1 and clears common base statuses;
- PETFALL does not leak past player exit;
- ultimate-exited pets are absent from later active rounds;
- enemy ultimate exit retains already-earned kill profit;
- player ultimate terminal rejects generic profit-bearing finishers;
- explicit elder-return position is applied;
- explicit failed elder lookup keeps the battle-origin position.
