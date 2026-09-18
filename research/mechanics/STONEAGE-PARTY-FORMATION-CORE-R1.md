# StoneAge Party / Formation Core R1

Status: **strong convergent descendant evidence; optional six-player extension excluded from the common baseline**  
Scope: ordinary five-player field party state, join/leave/disband behavior, follow-chain movement and projection into the ten-slot player-side battle layout.

## Purpose

The recovered encounter/battle core can already create an individual battle. What remained unclear was how the field-world party becomes a battle side.

The source family does not implement a separate arbitrary "formation editor" for the ordinary core. Instead, three linked structures define the formation:

1. a leader-owned five-slot field party roster;
2. slot-ordered follow-the-leader movement;
3. battle projection where live players compact into battle positions 0..4 and each selected default pet is paired at that player's battle position + 5.

This note reconstructs those state transitions and keeps later transport, pet-follow, family-war and six-player extensions separate.

## Evidence set

Fixed source revisions:

- **BismarckDD/stoneage** @ `999ffdf1d220ec6666eb65339180689c9caf1876`
  - `server/gmsv/include/char_base.h`
  - `server/gmsv/include/battle.h`
  - `server/gmsv/char/char_party.c`
  - `server/gmsv/char/char_walk.c`
  - `server/gmsv/battle/battle.c`
- **gavinlinasd/StoneAge** @ `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
  - corresponding `gmsv/src` files
- **iriselia/StoneAge** @ `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
  - corresponding `Source/gmsv` files

## Party modes

All three lineages preserve the same enumeration order:

```
CHAR_PARTY_NONE
CHAR_PARTY_LEADER
CHAR_PARTY_CLIENT
```

Therefore the common numeric values are 0, 1 and 2.

A client member stores its leader in `CHAR_WORKPARTYINDEX1`. The authoritative roster itself is held on the leader across `CHAR_WORKPARTYINDEX1 + slot`.

## Five-member common baseline

gavinlinasd and iriselia directly define:

```
CHAR_PARTYMAX = 5
```

Bismarck preserves the same value in the ordinary branch, while adding an optional:

```c
#ifdef _MULTIPLAYER_
#define CHAR_PARTYMAX 6
#else
#define CHAR_PARTYMAX 5
#endif
```

Its battle header similarly switches player/battle capacities under that macro.

The fixed Bismarck `version.h` does not define `_MULTIPLAYER_`, but compiler/build defines could still activate it externally. More importantly, the shared pet-placement code still uses the historical hard-coded pairing offset `+5`.

R1 therefore models the three-lineage **five-player common core** and treats six-player support as a later/optional extension requiring a separate consistency audit.

## Joining a party

### Search and normalization

**FACT — convergent descendant code**

A player asking to join must currently be `CHAR_PARTY_NONE`.

The ordinary search examines the tile one step in front of the player.

For a player candidate:

- if the candidate is already `CHAR_PARTY_CLIENT`, the code resolves that candidate's leader through `CHAR_WORKPARTYINDEX1`;
- otherwise the candidate itself is the target leader;
- the resolved leader must be within distance 1;
- the resolved leader must not be in battle;
- the resolved leader must have the `CHAR_ISPARTY` join-permission flag enabled;
- the party must have a free member slot.

Family-war floor checks, angel/escape restrictions, player-NPC support and bus/airplane behavior are later/context-specific extensions and are outside this common model.

### Slot 0 is leader-only

`CHAR_getEmptyPartyArray` normalizes to the leader and scans:

```
slot 1 .. slot 4
```

for the first `-1`.

It never allocates slot 0 to an ordinary client.

### First join creates the party

When the target is currently `CHAR_PARTY_NONE`, `CHAR_JoinParty_Main`:

- marks the target as leader;
- writes the leader's own index into slot 0;
- places the joining player in the first empty member slot;
- marks the joining player `CHAR_PARTY_CLIENT`;
- stores the leader index in the joining player's `CHAR_WORKPARTYINDEX1`.

Subsequent joins fill the first free slot 1..4.

This gives a leader-owned roster such as:

```
[leader, memberA, -1, memberC, -1]
```

## Leaving and disbanding

### Leader discharge

If the caller is the leader, the common discharge routine iterates the party roster and returns all valid ordinary party participants to `CHAR_PARTY_NONE`, clears their leader pointers and clears the leader's roster slots.

**FACT:** leader discharge dissolves the whole ordinary party.

### Client leave

If a client leaves:

1. the client's mode becomes NONE;
2. the client's leader pointer is cleared;
3. the matching slot in the leader roster is set to `-1`;
4. higher slots are **not compacted**.

Example:

```
[leader, A, B, C, -1]
B leaves
[leader, A, -1, C, -1]
```

A later join therefore fills slot 2 before slot 4.

If no valid clients remain in slots 1..4, the leader is changed back to `CHAR_PARTY_NONE` and its leader visual is removed.

A subtle raw-state detail is preserved: this "last client leaves" path does not necessarily clear the leader's raw slot-0 self value at the same moment. The logical party is gone because the mode is NONE. R1 therefore does not require raw slot 0 to become empty on the last client leave.

Later item-delete-on-quit and transport-image restoration branches are outside the core.

## Field-world formation

The ordinary formation is a **slot-ordered follow chain**.

When the leader successfully walks:

1. the code remembers the leader's pre-move coordinate;
2. scans party slots 1..4 in order;
3. each valid client moves one step toward the previous chain position;
4. that client's old position becomes the target for the next valid client.

If a party roster has a hole:

```
[leader, -1, B, C, -1]
```

the effective movement chain is:

```
leader -> B -> C
```

The hole is skipped rather than treated as an empty physical formation position.

### Client movement input

The ordinary direct walk handler suppresses positional walking for `CHAR_PARTY_CLIENT`.

A client may still submit turn-only input, but its field position normally follows the leader's movement propagation.

Thus the leader is the movement authority for the ordinary field party.

## Battle projection

### Player positions

`BATTLE_PartyNewEntry` first enters the initiating party player, then iterates leader roster slots 1..4 in order.

For each eligible member, `BATTLE_NewEntry` places a player into the first empty player-side battle slot.

In the five-player baseline:

```
player battle slots = 0..4
```

Because the battle insertion is "first empty", field-party holes are compacted during battle projection.

Example:

```
field slots:
[leader, -1, B, C, -1]

battle player slots:
0 = leader
1 = B
2 = C
```

### Default pet pairing

For a `CHAR_TYPEPET`, `BATTLE_NewEntry`:

1. resolves the owning player's battle number;
2. converts it to the local side player slot;
3. adds the literal offset `5`;
4. allows that pet into exactly that one battle entry.

Therefore the common ten-entry player side is structurally paired:

```
0 player0     5 default-pet-of-player0
1 player1     6 default-pet-of-player1
2 player2     7 default-pet-of-player2
3 player3     8 default-pet-of-player3
4 player4     9 default-pet-of-player4
```

This is the ordinary formation relationship; pet positions are not independently chosen.

### Only the selected default pet enters automatically

`BATTLE_PetDefaultEntry` reads `CHAR_DEFAULTPET`.

If it is `-1`, no pet enters.

If the selected pet exists, is not dead and has HP > 0, that pet is entered at the paired +5 slot.

If it is invalid/dead/non-positive-HP, the player's default-pet field is reset to `-1`.

The active `#if 1` path does **not** automatically search the player's other pets for a replacement. A fallback-search implementation exists only in inactive `#else` code.

### Member battle-state filtering

The ordinary old-core party-entry loop skips client members already in a non-NONE battle mode. Bismarck later accepts a FINAL state in addition to NONE before re-entry; R1 models the simpler common ordinary gate and records this as a descendant difference.

## PvP same-party identity

Before ordinary party-aware PvP creation, each challenged character is normalized to a parent identity:

- leader -> self;
- client -> leader pointer;
- standalone -> `-1`.

If both sides resolve to the same non-negative parent, battle creation rejects them as the same party.

This is further evidence that the leader pointer/slot-0 identity is the canonical party identity.

## Optional six-player extension warning

Bismarck contains an optional `_MULTIPLAYER_` switch that changes:

- `CHAR_PARTYMAX` 5 -> 6;
- `BATTLE_PLAYER_MAX` 5 -> 6;
- `BATTLE_ENTRY_MAX` 10 -> 12;
- `SIDE_OFFSET` 10 -> 12.

At the same fixed revision, the generic pet placement formula still uses:

```
owner-local-player-slot + 5
```

This does not transparently generalize to six player slots.

R1 therefore makes **no claim** that the optional six-player macro is internally complete or historically appropriate. It must be audited independently before any future reconstruction enables it.

## Deterministic model

Repository artifacts:

- `tools/stoneage_party_formation_model.py`
- `tests/test_stoneage_party_formation_model.py`
- `.github/workflows/validate-stoneage-party-formation.yml`

The model covers:

- the five-slot leader-owned roster;
- first-free member-slot allocation;
- first join / leader promotion;
- non-compacting client leave;
- leader disband;
- leader resolution and same-party identity;
- slot-ordered follow chain;
- direct client-walk suppression;
- field-roster -> compact battle-player projection;
- default-pet validity and fixed +5 pairing.

## Evidence status

- **FACT:** three lineages agree on NONE/LEADER/CLIENT modes and the leader-owned roster design.
- **FACT:** the old common party limit is five and slot 0 is reserved for the leader.
- **FACT:** joins fill the first free member slot; leaves create holes rather than compacting the roster.
- **FACT:** the leader walking drives a slot-ordered field follow chain and ordinary clients cannot independently submit positional walking.
- **FACT:** battle projection preserves valid party-member order while compacting out field-roster holes.
- **FACT:** the common battle player-side layout pairs each player's selected default pet at player local slot + 5.
- **FACT:** invalid/dead default pets are cleared rather than automatically replaced by another carried pet in the active path.
- **FACT:** Bismarck carries a later optional six-player macro not shared as the old baseline.
- **OPEN:** exact commercial-version chronology of six-player support and whether all hard-coded +5 assumptions were updated in the corresponding production branch.
- **OPEN:** direct JSS/1999 proof of the five-slot roster and battle pairing constants.
- **OPEN:** exact visual client formation presentation versus the server's authoritative slot/follow chain.

## Next technical seam

The primary field-to-battle multiplayer projection is now reconstructable. The next priority should be chosen by re-auditing the remaining deterministic loop gaps rather than expanding lists blindly. High-value candidates include **trading/economy transfer semantics**, **healing/status recovery service semantics**, and **item equip/use state transitions**, with preference for whichever closes the largest remaining end-to-end gameplay loop in the recovered source family.
