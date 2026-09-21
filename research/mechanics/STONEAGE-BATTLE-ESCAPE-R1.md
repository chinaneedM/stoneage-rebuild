# StoneAge battle escape R1

Status: **strong stable-descendant mechanics reconstruction; exact JSS-1999 provenance remains open**

## Scope

This note reconstructs ordinary battle escape separately from death penalties, post-battle recovery and general battle finish rewards. The implementation preserves the source escape attempt counter and the fact that a successful escape removes the player from the battle before the normal finish-profit scan.

## Evidence anchors

Primary pinned descendant:

- repository: `gavinlinasd/StoneAge`
- commit: `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
- relevant files:
  - `gmsv/src/battle/battle.c`
  - `gmsv/src/battle/battle_event.c`
  - `gmsv/src/battle/battle_command.c`
  - `gmsv/src/include/battle.h`

Independent control descendant:

- repository: `iriselia/StoneAge`
- commit: `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
- relevant file: `Source/gmsv/battle/battle_event.c`

The escape check arithmetic and counter ordering converge across the pinned descendants.

## Command and actor boundary

**FACT (stable descendant):**

- player wire command `E` stores `BATTLE_COM_ESCAPE`;
- ordinary battle dispatch executes escape only when the actor is not `CHAR_TYPEPET`;
- forced escape uses `BATTLE_COM_COMPELESCAPE` and calls the same `BATTLE_Escape()` function with `flag=1`.

The current status-free reconstruction therefore permits the ordinary escape branch for player/enemy actors and treats a pet escape command as ignored at execution.

## Attempt counter ordering

`EntryInit()` initializes every `BATTLE_ENTRY.escape` to 0.

`BATTLE_Escape()` performs:

```text
entry.escape++
BATTLE_EscapeCheck(...)
```

Inside `BATTLE_EscapeCheck()`:

```text
escape_cnt = entry.escape + 1
```

Therefore the first ordinary escape attempt starts from stored 0, is incremented to 1, and is evaluated with effective count **2**. This apparently redundant double step is preserved exactly rather than normalized to an intuitive one-based counter.

A failed attempt retains the incremented stored counter and therefore changes the next attempt.

## Luck and opponent average

For enemy actors, RARE maps to escape luck:

- RARE 0 -> luck 1
- RARE 1 -> luck 3
- otherwise -> luck 5

For non-enemy actors, fixed luck is clamped to 1..5.

The check averages the opposing battle entries that remain present. For an opponent carrying `CHAR_BATTLEFLG_ABIO`, the source subtracts 100 before adding that opponent's level. Integer division uses C truncation toward zero.

If there are no valid opponents, the source starts from `Esc=100`.

## Probability and RNG

With an opponent average present:

- luck >= 5: `Esc = 95 * escape_cnt`
- luck 4: `Esc = 60 * escape_cnt - 2 * (enemy_average - actor_level)`
- luck 3: `Esc = 50 * escape_cnt - 2 * (enemy_average - actor_level)`
- luck 2: `Esc = 40 * escape_cnt - 2 * (enemy_average - actor_level)`
- luck 1: `Esc = 30 * escape_cnt - 2 * (enemy_average - actor_level)`

The lower end is clamped to 1. There is no upper cap.

Ordinary success is strict:

```c
RAND(1,100) < Esc
```

Consequences preserved by regression tests:

- `Esc == 1` cannot succeed with a 1..100 roll;
- `Esc == 100` fails only on roll 100;
- values above 100 make every 1..100 roll succeed.

## PvP and forced escape

`BATTLE_EscapeCheck()` returns success immediately for PvP battle type, before consuming its ordinary escape RNG.

Forced escape does **not** bypass the check call. `BATTLE_Escape()` increments the stored counter and performs the check first; `flag==1` then forces the exit even if that check failed. The deterministic model therefore still requires and records the ordinary RNG for non-PvP forced escape.

## Successful exit and active pet entry

On success, `BATTLE_Escape()` calls `BATTLE_Exit(attackindex,battleindex)`.

The player branch of `BATTLE_Exit()` also clears the active pet battle entry paired with that player entry. The ordinary-round model therefore marks both the player and current allied battle pet as exited from later actions after a successful player escape.

The persistent battle state represents this as terminal result `escape`, not as victory or defeat.

## Escape does not receive normal finish profit

Normal battle completion calls `BATTLE_Finish()`, which scans battle entries and for each still-valid entry executes:

```text
BATTLE_GetProfit(...)
BATTLE_Exit(...)
```

A successful escape already called `BATTLE_Exit()`, which clears that player's battle entry. When the eventual finish scan encounters the cleared slot, it skips it and therefore does not call `BATTLE_GetProfit()` for that escapee.

This is materially different from "earned rewards are always settled at battle end." Pending `WORKGETEXP` and the battle-entry pending item buffer are not promoted through the normal finish-profit path after that player has escaped.

Accordingly, the single-player runtime's ordinary victory/defeat finishers now reject an `escape` terminal rather than accidentally settling pending EXP or item drops.

## Recovery boundary intentionally left separate

`BATTLE_Exit()` also contains status cleanup, battle-mode cleanup, active-pet detachment and HP-floor handling for certain player/pet states. Those effects are broader than escape and overlap the project's death/recovery seam.

R1 therefore does **not** yet expose a dedicated persistent escape-return settlement. The next seam is to reconstruct the exact BATTLE_Exit recovery/status behavior and only then project escape HP/pet state back to persistent single-player state.

## Implemented deterministic seams

- `cfa3f855f09e8147ba241d66428377ce3e1df20e`
  - source counter ordering, luck bands, opponent average, ABIO adjustment;
  - strict RNG boundary;
  - PvP and forced-exit behavior;
  - battle-core Action `35550194003` success;
  - gameplay Action `35550194001` success.

- `454952adfbbef33090719bb2d45162481c188da7`
  - escape executes inside ordinary action order;
  - successful player escape removes the active allied pet from subsequent actions;
  - battle-core Action `35550379184` success;
  - gameplay Action `35550379230` success.

- `a8c228e946c1c810a1cf32c7cbba76aa0611f830`
  - stored escape counters moved into persistent battle-entry state;
  - caller context is validated against stored count;
  - successful player escape becomes a distinct persistent terminal result;
  - battle-core Action `35550479374` success;
  - gameplay Action `35550479386` success.

## Confidence boundary

**CLOSED for the strong stable-descendant mechanics profile:**

- command identity and ordinary non-pet actor gate;
- attempt counter initialization/increment/check ordering;
- enemy RARE and player fixed-luck mapping;
- opponent average and ABIO adjustment;
- probability bands, lower clamp, no upper clamp;
- strict `RAND(1,100) < Esc`;
- PvP early success;
- forced-exit check-before-force behavior;
- BATTLE_Exit-shaped successful action exit;
- active allied-pet removal from later action execution;
- exclusion of escaped players from the normal BATTLE_Finish profit scan.

**OPEN / separate seam:**

- byte-level confirmation that all details are identical to the 1999 JSS server;
- exact early-JSS map/event restrictions around whether escape command submission is permitted;
- complete BATTLE_Exit recovery/status cleanup and its exact early-version profile;
- death penalties and post-defeat recovery;
- any later `_ESCAPE_RESET`, event scoring or private-server anti-abuse behavior.
