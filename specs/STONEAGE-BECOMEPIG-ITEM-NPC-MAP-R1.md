# BecomePig item / NPC / map timer native composition R1

Date: 2026-10-07 (UTC+8)
Status: **NATIVE_COMPOSITION_GATE_PENDING_REMOTE_ACCEPTANCE_ZERO_RUNTIME_PROMOTIONS**

## Scope

This gate covers the next default-feature interaction layer after accepted
main-hit / Guardian / Counter / retarget ownership. All three exact pinned
descendant profiles enable `_ITEM_METAMO`, `_NPCCHANGE_PLAYERIMG`,
`_MAP_TIME`, `_ITEM_UNBECOMEPIG`, `_FIXBUG_ATTACKBOW` and
`_PETSKILL_BECOMEPIG` in their default headers.

The gate transiently extracts exact original conditionals from:

- `ITEM_metamo`: active BecomePig guard;
- `NPC_ActionChangePlayerBBI`: active BecomePig guard;
- `ITEM_useRecovery_Field`: the unpig recovery branch;
- `CONNECT_SysEvent_Loop`: item metamorph expiry and map timer blocks.

Original source bytes remain transient and are never committed.

## Required source order

Before native execution, each pinned profile must prove:

1. the item metamorph BecomePig guard precedes the later
   `CHAR_WORKITEMMETAMO` write;
2. the NPC image-change BecomePig guard precedes both item-metamorph clearing and
   `CHAR_WORKNPCMETAMO` assignment;
3. unpig recovery writes `CHAR_BECOMEPIG=-1` before compliance and item
   consumption;
4. item metamorph expiry clears item and NPC metamorph state before compliance;
5. the map timer is battle-gated, decrements by 10, and its expiry path owns
   warp-to-30008/39/38, HP=1 and charm -3;
6. item metamorph timeout appears before the map timer block in the default
   system loop.

## Native scenarios

Each profile executes five scenarios at O0 and O2 under AddressSanitizer plus
nonrecovering UBSan:

- active pig blocks both item and NPC metamorph guards before later state writes;
- an unpig recovery clears pig state, invokes compliance, consumes the item, and
  both metamorph guards then fall through;
- expired item metamorph clears item/NPC metamorph state, then the same loop's map
  timer expires and performs warp/HP/charm effects while pig state remains active;
- item metamorph expiry uses strict `deadline < now`, so equality does not clear;
- map timer pauses while battle mode is non-NONE.

These witnesses establish direct ownership/order only. The complete
`CHAR_complianceParameter` body is not duplicated here because its restoration,
bad-status, equipment and ride compositions are independently accepted already.
Packet/presentation hooks, item lookup, and the warp implementation itself are
controlled seams.

## Acceptance boundary

Remote acceptance requires 30 native comparisons
(3 profiles × 5 scenarios × O0/O2), exact default feature identities, matching
block/file hashes, identical O0/O2 semantic rows, no ASan/UBSan diagnostics, and:

`BECOMEPIG_ITEM_NPC_MAP_TIMER_NATIVE_COMPOSITION_PASS_ZERO_RUNTIME_PROMOTIONS`

Passing this gate does not promote typed631/635 or any persistent/coordinator
runtime slot. Remaining priorities are broader stat/property/ownership/death/
follow/PvP/watch/enemy paths and historical executable/build/ABI/PRNG provenance.
