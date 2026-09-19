# StoneAge Residual Ordinary NPC Sweep Closure R1

Status: **ordinary non-family NPC core sweep closed for the current recovered 2.5 / fixed-descendant evidence set**

## Scope

This closure records the final residual review after Quiz, Dengon/Duelranking and personal-bank work. It specifically resolves whether LuckyMan or Door justify opening another core subsystem.

Evidence controls:

- recovered bundle SHA-256 d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5
- recovered LuckyMan/Door probe workflow 35420226969: success
- fixed descendant revisions:
  - gavinlinasd/StoneAge @ 1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56
  - iriselia/StoneAge @ 9e6c8ce2cd8ed532a7157773acd1c61582c178b5
  - BismarckDD/stoneage @ 999ffdf1d220ec6666eb65339180689c9caf1876

## Recovered activity: template definitions exist, world instances do not

The recovered 2.5 template corpus contains:

- LuckyMan: 1 template block / 1 stable template-name value
- Door: 3 template blocks / 3 stable template-name values

No mixed-template-name ambiguity exists for either class.

However, after applying the server's case-insensitive create -> template name join, the recovered create corpus contains:

- LuckyMan create refs: **0**
- Door create refs: **0**

The aggregate argument hash is therefore the SHA-256 empty-stream value. This is not a probe failure: template census is nonzero, target names are stable, tests pass, and the measured create-reference population is zero.

Therefore both classes are **defined but not instantiated** in this recovered world snapshot.

## LuckyMan fixed-source semantics

All three pinned fixed descendants preserve the same small service core.

The NPC reads a Stone cost from `Stone`. Cost can be:

- a constant integer; or
- `LV*multiplier`, producing player level x multiplier.

On Yes:

1. verify carried Gold is at least the calculated cost;
2. if insufficient, display NoMoney and stop;
3. deduct the cost from carried Gold;
4. refresh Gold display;
5. select a fortune-message list keyed by the player's exact `CHAR_LUCK` value;
6. choose one comma-separated message variant at random and display it.

The common path does **not**:

- grant an item;
- grant EXP;
- change luck/charm;
- move or warp the player;
- start battle;
- modify pets;
- synchronously save the character.

Thus LuckyMan is a narrow economy sink plus randomized presentation, not a progression mechanic.

Source-only hazards remain documented but are inactive in the recovered snapshot:

- negative configured cost would pass the ordinary cost check and can invert Gold subtraction semantics;
- a missing/empty `luckN` message list can drive the random-selection code into an invalid zero-variant state because the key-read return value is ignored.

These are fixed-source quirks, not recovered active behavior.

## Door fixed-source semantics

All three pinned descendants share the same positional Door argument core.

The first seven argument positions encode:

1. open graphic
2. closed graphic
3. door identity/name
4. required switch count
5. close-duration seconds
6. close-soon flag
7. pass mode

Optional later positions support title-gated doors and room-administration metadata/password coupling.

The ordinary Door core mutates **NPC/world runtime state**:

- open/closed graphic;
- overable/non-overable flag;
- switch counter;
- close deadline;
- transient door password/title/room metadata.

Opening makes the door overable; closing makes it non-overable. Timed doors can close after their configured interval, while close-soon doors close around pass/off events.

Some open-graphic ranges imply a required key-item ID. The check uses possession only; the Door core does not consume the key.

Title-gated and password/room branches likewise check conditions and flip the door but do not directly mutate ordinary player progression.

Room auction/bank-like fields stored on Door are consumed by `RoomAdmin` code, not by the ordinary Door callback. That later package is not promoted into the core merely because the Door struct carries its metadata.

## Persistence boundary

Neither LuckyMan nor ordinary Door introduces a new persistence domain:

- LuckyMan's only ordinary player mutation is carried Gold, which follows the already reconstructed character-save lifecycle;
- Door state is NPC/world runtime state in the inspected common path and is not a new ordinary player save field;
- room-administration persistence remains a separate later package.

## Why the ordinary NPC sweep stops here

The current sweep has already closed the ordinary high-value classes that expose deterministic core state transitions: transport, warp, shops, healing, exchange, battle entry, Janken, Charm, riding, time/presentation routers, bulletin-board persistence, duel-ranking reads, personal bank and Quiz.

The residual common-source classes either:

- reduce to presentation/read-only work state;
- wrap already reconstructed warp/event primitives;
- are not instantiated in the recovered 2.5 world;
- or belong to deferred family/race/VIP/event packages.

Thirteen recovered function-set tokens still do not join to any of the three pinned fixed source tables. Those remain explicit source/data lineage gaps; inventing implementations from similarly named unused/later files would reduce provenance quality.

## Evidence status

- **FACT:** recovered 2.5 contains one LuckyMan template block and three Door template blocks.
- **FACT:** recovered 2.5 contains zero create refs to those LuckyMan/Door template names after case-insensitive template matching.
- **FACT:** LuckyMan's common accepted path deducts Gold and displays a random luck-keyed message only.
- **FACT:** ordinary Door changes door NPC/world runtime state and checks key/title/password conditions without consuming player items or Gold.
- **FACT:** Door room-auction metadata is coupled to separate RoomAdmin code.
- **SOURCE QUIRK, INACTIVE HERE:** LuckyMan negative-cost and missing-luck-list hazards.
- **LATER/DEFERRED:** RoomAdmin, family administration, Raceman, Scheduleman, ManorSman, FMPK/FMWarp and VIP packages.
- **OPEN SOURCE/DATA SKEW:** thirteen recovered function-set tokens lack a join to every pinned fixed source table.
- **OPEN HISTORY:** exact JSS-era presence/behavior of LuckyMan, Door and the unmatched function-set classes until earlier clean source/client evidence is recovered.

## Priority consequence

The ordinary NPC mechanics sweep is closed. Primary priority returns to **earliest clean-client recovery and provenance-preserving client data reconstruction**. Do not reopen the NPC queue unless a cleaner/earlier client or matching source lineage exposes a concrete contradiction or previously missing core dependency.