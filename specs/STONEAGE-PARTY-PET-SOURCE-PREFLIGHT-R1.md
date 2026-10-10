# Party/pet original-source entry preflight R1

Status: **PENDING remote CI**. Source-level gate only, **not** party/pet runtime admission.

## Why this is the next gate

Latest accepted solo CreateVsEnemy exercises a leader with no party members and no
default pet. The original source-level entry path may differ by descendant
profile. This isolated gate verifies the branch structure *before* extending the
native original-body harness to a populated party/pet configuration.

The newly authored preflight reads transient, exactly pinned Gavin and
Bismarck trees, extracts their selected preprocessed original bodies, verifies
branch anchors, and publishes **only SHA-256 function/file fingerprints and
semantic observations**, never the proprietary original functions.

### Testable profile differences

- Gavin iterates party slots using a fixed `CHAR_PARTYMAX` bound and excludes
  nonzero member battle modes in its selected profile.
- Bismarck uses `getPartyNum` and admits members in either NONE or FINAL modes.
- Both use the explicitly selected default pet slot, a character validity,
  death and HP guard, and clear GETEXP on the player and each owned valid pet.
- The selected pet wrapper initializes its return value to zero and does not
  forward the result of `BATTLE_NewEntry` through that return value. Verify
  battle occupancy directly; a zero wrapper return must not be treated as
  evidence that a pet was inserted.

These are **proposed source observations** until the exact remote preflight
passes; even when accepted, they establish no native party/pet path execution.

## After source acceptance

Extend the current successful solo native composition to a controlled second
player and an owned, explicitly selected healthy pet. Verify each entered battle
slot and successful Exit against original functions, including player/pet
ownership, selected/default state, battle occupancy and GETEXP reset. Exercise
invalid/dying/zero-HP default pet and occupied/ineligible party-slot negatives.
Preserve Gavin/Bismarck differences, pinned source/master bytes, exact diff
oracles, abort traps, mutation tests and all predecessor report byte gates.

OPEN: native populated party/pet CreateVsEnemy, actual Exit/profit,
BATTLE_Init/TaskLoop, original reclaimer, original ABI, Iris conversion,
1999-JSS and Taiwan-v1 membership. **No runtime evidence promotion**.
