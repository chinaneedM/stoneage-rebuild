# BecomeFox independent source preaudit R1

Date: 2026-10-06
Status: **PINNED_SOURCE_PREAUDIT_PASS_DATA_AND_NATIVE_ACCEPTANCE_OPEN**

This independent preparation branch starts at accepted main
`d2b309c750049c1585543b4f76514cf8eca19826`, tree
`ff764e45470698514d728aa401e2ef17aba5c2ff`. It does not depend on or merge
the pending BattleModel reference branch.

Accepted pressure identifies `PETSKILL_BecomeFox` as an OPEN family with
positive ID625, two positive slot uses and two templates. These counts do not
close complete callback population, metadata, OPTION bytes or exact placements.

## Evidence scope

`tools/stoneage_becomefox_preaudit.py` verifies three clean pinned descendants:
gavin `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`, iris
`9e6c8ce2cd8ed532a7157773acd1c61582c178b5`, and Bismarck
`999ffdf1d220ec6666eb65339180689c9caf1876`.

All three pass20 textual structural gates (60 total). The derived report
records exact source hashes. This is source preaudit evidence, not a native
equivalence result or ordered runtime acceptance.

## Callback and post-attack transformation

The callback writes symbolic BECOMEFOX, target COM2, C_OK and LOW(COM3)=skill
array. It reads no OPTION and owns no callback RNG. The command shares the
ordinary attack dispatcher path; complete damage/retarget/Guardian semantics
remain to be audited before implementation.

The separate post-attack transform predicate rejects MISS/DODGE/ALLGUARD and
requires a still-living submitted target. ARRANGE exclusion is present too,
conditionally guarded in Bismarck. It then evaluates one `rand()%100 <31`
comparison **before** checking non-player type, nonzero PETFLG and the optional
attacker BECOMEPIG guard. Thus a surviving player or ineligible pet may still
consume this draw even though it cannot transform. This is reduced-draw
ownership, not a claim about original libc PRNG identity or an exactly unbiased
31-percent distribution.

The type test is `!= PLAYER`, not an explicit `== PET` equality. PETFLG is a
separate eligibility witness. The optional pig guard reads the **attacker**.
Success records the current battle turn in FOXROUND and sets fox image101749.
Its ride-cleanup branch clears mounted state and sets PETFALL if reached; actual
reachability in the admitted non-player domain remains OPEN.

## Powers, duration and skill presentation

Before action dispatch, an active FOXROUND causes attack/defence/quick to be
rewritten to the corresponding fixed power multiplied by0.8. Initiative has a
separate `(current quick +20)*0.8` site. The call-order and arithmetic profile
must be established before treating those as a single generic20-percent debuff.

Round recovery checks **current turn minus recorded turn >2**. It restores the
base image, all three fixed powers and the work-state marker, then notifies the
DEFAULTPET of an owner inferred by battle slot minus5. This is not yet a claim
about which player-visible turn boundary counts as expiration.

The command/menu path sends an altered skill-data view. The corresponding
inspected gavin character status builder filters by localized skill **name**, keeping ordinary
wait/attack/guard choices and changing presentation fields for other skills.
The inspected builder does not delete owned skill records. Complete charset
identity and authoritative server-side submission restrictions remain OPEN.

## Recall and exit divergence

FOXROUND is declared as work state. Normal initialization and round recovery
use work-state accessors. In `BATTLE_PetIn`, however:

| Descendant | FOXROUND getter/setter |
|---|---|
| gavin | ordinary integer accessors |
| iris | ordinary integer accessors |
| Bismarck | work-state accessors |

This difference must not be silently repaired or flattened into one historical
behavior. The actual numeric enum/storage consequences require native evidence.
All profiles place this fox-reset block **before NORETURN**, so a blocked
recall can reach reset operations before returning without withdrawal. The
block restores attack and quick, with no defence-restoration site there.

Battle exit independently restores the fox image/base image and work marker.
This preparation does not accept complete terminal/persistent projection.

## Next work and unchanged acceptance boundary

BattleModel's three existing remote gates remain the primary task. After their
acceptance, its runtime work retains priority. BecomeFox preparation can then
be reused for:

1. hash-verified complete callback/metadata/OPTION/placement discovery;
2. fixed-profile native draw ownership, ordinary hit and transformation audit;
3. cross-round power/expiry and skill-eligibility contracts;
4. versioned PetIn accessor/owner/default-pet/NORETURN audit;
5. battle return/save integration after reference acceptance.

No ID625 runtime admission, executable-slot promotion, original numeric COM1,
JSS/Taiwan-v1 membership, production-engine decision or redesigned content is
accepted by this preaudit.
