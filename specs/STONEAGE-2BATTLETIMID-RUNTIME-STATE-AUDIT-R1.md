# StoneAge 2BattleTimid runtime state audit R1

Date: 2026-10-05
Status: **PREIMPLEMENTATION_STATE_AUDIT_ACCEPTED; ORDERED_RUNTIME_OPEN**.
This supplements `STONEAGE-2BATTLETIMID-REFERENCE-R1.md`; it does not add
an executable skill or change the accepted positive-slot pressure coverage.

## Accepted source lifecycle and build limit

The three previously fixed source pins each pass12 textual lifecycle gates.
PetDefaultExit requires a valid player owner, reads its selected roster slot,
resolves that owned pet and delegates to BATTLE_Exit. The normal pet exit
clears the matching battle-array character identity and escape value, sets
battle mode FINAL and battle index-1. It does not delete the owned pet or
apply an HP mutation through the PetDefaultExit helper. PetIn's NORETURN
guard occurs before default exit and owner DEFAULTPET=-1. The accepted
reference still owns the outer K/KS notifications, even when blocked.

This is a textual source audit, not a native execution of the full server
exit. Wolf/fox, invalid owners, mismatched selected pets, invalid battle
arrays and return/error-path compositions remain outside the domain.

Verified preservation/source Action **37311978479 PASS**, input
`57babd06d8e53faefe59bd47179a8d20d941ee7e`, tree
`2429bf3e5ea09ebf5d904b953a3028757be8c10f`.
Derived report commit `126a1362a9d76ce821a883cf47da3a79c96e9ef0`, tree
`5b4fc5d3830da23a9cd12467bf37730e501c36ac`.
The independent bounded executable assay finds one273-byte ELF candidate,
SHA-256 `22a786475540dd734e0b0dc1b21219e53aba1462de8be623270f71fa90c22365`,
with neither PETSKILL_2BattleTimid nor BATTLE_S_AttackDamage symbol.
That absence is inconclusive about any original game build. It cannot
choose UTF-8 versus Big5 literals. Both explicit profiles remain required.
Two discriminator unit tests PASS; the complete reference/native acceptance
remains the previously green37309960471 gate.

## Modern seams inspected at the accepted reference tree

| Seam | Existing behavior | Required 2Timid change |
| --- | --- | --- |
| `BattleParticipant` / `BattleSession` | Owned roster slot available as source_pet_slot; session can list multiple allies | Validate a unique selected pet and owner-aligned battle slot for this bounded skill |
| `begin_persistent_battle` | Validates side, unique slots and0..19; no owner+5 rule | Explicit binding of player owner, default roster slot and selected defender |
| `PersistentBattleState` | Retains session identities and battle_exited_participant_ids across rounds | Add independently validated default-pet selection and NORETURN state |
| `resolve_ordinary_round` | Has generic exited slots and BattleTimid exit resolution | Add distinct 2Timid post event; blocked recall keeps occupancy; successful recall excludes later same-round actions/targets |
| persistent round settlement | Exit identities retained; only captured/escaped enemies are removed from session | Retain recalled owned pet and HP, add pet-only exit provenance and clear selected default pet |
| player-death penalty | Infers default pet from session.allied_pets | Consult actual selection so a recalled pet is not treated as the owner's active default |
| coordinator | Excludes retained battle-exited IDs; carries persistent combat state in battle context | Forward explicit charset/owner/NORETURN binding and the one post draw |
| world/session save | Serializes world player/session and occupancy; active battle lives in coordinator context | Test selected-default state through battle return and world save; do not claim active-battle disk resume |

The existing party-formation `battle_projection` already pairs each player's
selected default pet at owner slot+5. Reuse that ownership rule; it is not
an arbitrary positional convenience. Multiple allied pets are currently
possible in the single-player battle session, so one cannot silently pick
the first allied pet as historical DEFAULTPET. Invalid selection, missing
source roster slot, owner/target mismatch and ambiguous active pets must
fail before damage/RNG mutation when admitting this bounded skill.

## Implementation contract and acceptance witnesses

The next implementation must preserve owned-roster identity separately from
selected-default identity and active battle occupancy. A withdrawn pet can
remain in the session identity graph with positive HP while being excluded
from the rest of the round and later rounds. Withdrawal is neither death
nor owned-pet deletion, player exit, escape, capture, or party discharge.
NORETURN must be explicit authoritative state, not guessed false because a
caller omitted it. This audit introduces no production default or schema.

Required independent witnesses:

- Both UTF-8 and Big5 literal profiles; exact ID636/template/graphic/slot
  admission and raw OPTION digest; no arbitrary original numeric COM1.
- Successful normal-pet recall: prior K selection, current KS=-1, one BS,
  cleared selection, preserved HP/owned identity, no further same-round pet
  action or targeting and no later-round action/targeting of that entry.
- Blocked recall: K/KS still sent, no BS/default mutation/occupancy removal;
  the pet still acts later in that round and remains active next round.
- Player/nonpet target and damage1 still consume the undemoted positive
  event draw; reaction/zero damage own none. Scheduling ATTACK must not
  grant ordinary counters, combo rewriting or an extra hit.
- A later player death reads the cleared selected-default state rather than
  retained pet membership. Battle return/world save preserves ownership and
  the selection result; no false claim of active-battle disk serialization.

Riding, transformations, lethal recall/death overlap, Guardian/reaction
identity compositions, substituted targets with unbound owners, player-side
skill submissions, invalid owners and general multi-owner parties remain
OPEN until specifically admitted. Runtime must reject excluded compositions
explicitly. After ordered/cross-round/coordinator/regression acceptance,
rerun verified preservation pressure before promoting the two positive uses.

**Highest-priority unfinished work:** implement the explicit owner/default-pet/
NORETURN state seam first, then exact typed enemy-AI admission, ordered
settlement, coordinator and battle-return/world-save witnesses. Coverage
remains **2457/2486=98.83%**. Continue WORK under DD-018 and DD-019.
