# StoneAge Player Death / Revival Core R1

Status: **strong convergent descendant evidence; client death-to-savepoint choreography remains OPEN**  
Scope: player `core_Dying`, the generic player-resurrection helper, player-load death sanitation, and the separately versioned return-to-record-point protocol.

## Why this seam matters

The battle and progression models previously ended at reward/state updates. A playable loop also needs a deterministic failure state. The preserved descendant source family contains a remarkably stable player death callback, plus a small generic resurrection helper.

The important reconstruction constraint is that these mechanisms must **not** be collapsed into an invented single "die -> warp -> revive" action. The code separates:

1. death penalties and death flags;
2. resurrection of a player in place;
3. a later `CharLogout(flg=1)` return-to-record-point protocol;
4. login-time cleanup of persisted death/HP anomalies.

R1 models the first two directly and records the latter two as adjacent state transitions.

## Evidence set

Fixed revisions:

- **BismarckDD/stoneage** @ `999ffdf1d220ec6666eb65339180689c9caf1876`
  - `server/gmsv/function.c`
  - `server/gmsv/char/char_event.c`
  - `server/gmsv/char/char.c`
  - `server/common/gmsv_server_recv.c`
  - `client/stoneage/system/netproc.cpp`
- **gavinlinasd/StoneAge** @ `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
  - `gmsv/src/function.c`
  - `gmsv/src/char/char_event.c`
  - `gmsv/src/char/char.c`
  - `gmsv/src/callfromcli.c`
- **iriselia/StoneAge** @ `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
  - `Source/gmsv/function.c`
  - `Source/gmsv/char/char_event.c`
  - `Source/gmsv/char/char.c`
  - `Source/gmsv/callfromcli.c`

## Player death callback identity

**FACT — convergent descendant code**

All three function registries bind:

```
"core_Dying" -> CHAR_die
```

The preserved default-player function table also assigns `core_Dying` to `CHAR_DYINGFUNC`.

Therefore `CHAR_die()` is not an arbitrary NPC helper; it is the ordinary player death callback in this source family.

## Stable death transition

All three lineages retain the same `CHAR_die()` body.

### Party state

The first operation is:

```c
CHAR_DischargeParty(charaindex, 0);
```

**FACT:** ordinary death discharges the player from party state before applying the rest of the penalty.

### Attacker classification and equipment-loss mode

The code derives a small `bymonster` class from `CHAR_WORKLASTATTACKCHARAINDEX`:

- sentinel `-2` -> class 0;
- valid attacker of `CHAR_TYPEENEMY` -> class 1;
- any other valid character attacker -> class 2;
- unresolved/invalid non-sentinel attacker leaves the initialized class 0.

The penalty branch is:

- class 0 or 1: call `CHAR_DropItem` for **every equipment slot**;
- class 2: collect occupied equipment slots and select **one uniformly random slot** for `CHAR_DropItem`.

R1 therefore calls these categories **enemy**, **non-enemy**, and **unknown** rather than simplifying class 2 to "PvP". A valid pet/NPC-style non-enemy attacker can also enter the same branch.

The model records requested drop slots/candidates. It does **not** claim that every requested item necessarily becomes a world object: `CHAR_DropItem` can fail because of placement/object constraints.

### Gold penalty

The callback requests:

```c
CHAR_DropMoney(charaindex, CHAR_GOLD / 2);
CHAR_setInt(charaindex, CHAR_GOLD, 0);
```

For non-negative gold, the requested ground amount is integer `gold // 2`.

The second line is unconditional. Thus the stable core behavior is:

- request half the carried gold as a ground drop;
- finish with **zero carried gold**.

If the ground-drop helper fails, the callback still zeroes the player's carried-gold field. R1 therefore separates `requested_ground_gold` from `final_carried_gold`.

### Counters, status cleanup and death flags

The callback then:

- recomputes compliance after equipment-loss requests;
- increments `CHAR_DEADCOUNT` by 1;
- clears:
  - paralysis,
  - sleep,
  - stone,
  - drunk,
  - confusion,
  - poison;
- marks `CHAR_ISDIE = 1`;
- marks `CHAR_ISATTACKED = 0`.

**FACT:** `CHAR_die()` itself contains no elder/savepoint lookup and no warp.

## Generic player resurrection

All three lineages preserve the same `CHAR_playerresurrect(charaindex, hp)` helper.

It:

- restores `CHAR_BASEIMAGENUMBER` from `CHAR_BASEBASEIMAGENUMBER`;
- clears `CHAR_ISDIE`;
- sets `CHAR_ISATTACKED = 1`;
- clears `CHAR_ISOVERED`;
- clamps the supplied HP for a normal positive-MAXHP character:
  - `hp >= MAXHP` -> `MAXHP`;
  - `hp <= 0` -> `1`;
  - otherwise keep supplied HP.

It does **not**:

- refill MP;
- move the player;
- select an elder/savepoint;
- itself clear the death penalties already applied.

The deterministic model therefore treats resurrection as an in-place state operation.

## Login-time death sanitation

The preserved player-load path contains two relevant repairs:

1. if persisted `CHAR_ISDIE` is set, it is cleared;
2. if loaded HP is non-positive, HP is set to `1`.

The code obtains the dying-function pointer in the HP repair block but does not call it in the preserved implementation.

This is modeled as a separate `login_sanitize` operation, not as `CHAR_playerresurrect`.

## Return-to-record-point protocol is separate and versioned

The descendant family also contains a later/new logout protocol where `flg == 1` means **return to record point**.

Bismarck's current `_CHAR_NEWLOGOUT` implementation:

- resolves `CHAR_LASTTALKELDER` through `CHAR_getElderPosition`;
- rejects the request during battle;
- contains later feature-specific restrictions;
- warps to the resolved record point when permitted.

Its current client defines:

```c
void charLogoutStart(void) {
    ...
    lssproto_CharLogout_send(sockfd, 1);
}
```

gavinlinasd / iriselia retain the same server-side `flg == 1` meaning, with branch-specific party/item/map restrictions.

However, repository-wide search of the Bismarck client at the fixed revision finds `charLogoutStart` only at its declaration and definition, not a direct death-screen call site. Therefore R1 does **not** claim:

```
CHAR_die -> automatic CharLogout(1)
```

That choreography remains an OPEN client-flow question.

## Deterministic model

Repository artifacts:

- `tools/stoneage_player_death_model.py`
- `tests/test_stoneage_player_death_model.py`
- `.github/workflows/validate-stoneage-player-death.yml`

The model exposes:

- `death_transition(...)`;
- `resurrect_transition(...)`;
- `login_sanitize(...)`.

Regression coverage checks:

- all-equipment drop requests for enemy/unknown deaths;
- one-random-equipped-item semantics for valid non-enemy attackers;
- half-gold ground request plus zero final carried gold;
- stable status cleanup and death-counter increment;
- resurrection HP clamping without movement/MP refill;
- login-time death/HP sanitation.

## Gameplay-loop consequence

The failure side of the ordinary loop is now explicitly representable:

```
battle damage / defeat
  -> core_Dying
  -> party discharge
  -> equipment/gold penalty requests
  -> status cleanup + death flag
  -> [independent revival mechanism]
      OR
     [versioned return-to-record-point / relog flow]
```

The bracketed transitions are deliberately not merged until a source proves the exact client choreography for the target historical version.

## Evidence status

- **FACT:** `core_Dying` maps to `CHAR_die` for the ordinary player function table.
- **FACT:** three lineages agree on party discharge, equipment-loss branching, half-gold drop request, zero final gold, dead-count increment, six-status cleanup and final death flags.
- **FACT:** `CHAR_playerresurrect` is an in-place HP/flag/image operation and does not move the player or refill MP.
- **FACT:** preserved load code clears persisted death state and repairs non-positive HP to 1.
- **FACT:** later/new logout protocol uses flag 1 for return-to-record-point and resolves `LASTTALKELDER`.
- **OPEN:** exact launch-era death UI and whether/how it invokes return-to-record-point.
- **OPEN:** exact historical transition from field/battle zero HP to the registered `CHAR_DYINGFUNC` in each commercial version.
- **OPEN:** launch-era placement-failure behavior experienced by players when death-drop tiles were obstructed.
- **OPEN:** whether the later `_CHAR_NEWLOGOUT` behavior should be used at all in the target baseline reconstruction.

## Next technical seam

The major player failure state is now modeled. The next high-value unmodeled loop closure is **capture/taming**: recover the target-validity gates, capture probability inputs, pet-slot constraints, success state transfer, and how capture interacts with battle termination/rewards. This should be reconstructed before party/formation because it connects the existing wild-enemy/battle model directly to the pet roster/growth model.
