# StoneAge ExChangeMan Mutation / Accept Core R1

Status: deterministic fixed-descendant reconstruction of the common mutation ordering and secondary-argument side effects.

This R1 continues directly from `STONEAGE-EXCHANGEMAN-CONDITION-CORE-R1.md`. It does not reopen the generic NPC inventory. It models what happens after a one-based EVENT branch has already been selected.

## Fixed source set

The control flow was checked against the same three pinned descendants:

- `gavinlinasd/StoneAge@1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
- `iriselia/StoneAge@9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
- `BismarckDD/stoneage@999ffdf1d220ec6666eb65339180689c9caf1876`

The main order converges across `NPC_EventAdd`, `NPC_AcceptDel`, `NPC_ItemFullCheck`, `NPC_EventDelItem`, `NPC_EventAddItem`, `NPC_EventAddPet`, and `NPC_EventAddEgg`. Bismarck primarily refactors formatting and buffer-size plumbing.

The gavin fixed build has both `_ITEM_PILENUMS` and `_EXCHANGEMAN_REQUEST_DELPET` enabled in `version.h`, so the active branches are recorded rather than treated as hypothetical extensions.

## NPC_ItemFullCheck

The preflight is not a transaction simulator. It computes a slot projection using the carried-inventory domain and several shortcuts.

For ordinary `DelItem`, a starred token subtracts its requested count from projected required slots without verifying inventory or actual stack-slot release.

For a non-star ordinary `DelItem`, the source reuses `i` as both CSV token index and inventory loop index. After the first non-star deletion token scans inventory, `i` exits at `CHAR_MAXITEMHAVE`; the outer CSV loop therefore normally stops and later `DelItem` tokens are not included in capacity projection.

For `DelItem:EVDEL`, the selected EVENT branch is the one-based branch number returned by `NPC_ExChangeManEventCheck`. Starred ITEM terms subtract the requested count. Non-star ITEM terms subtract the number of matching carried slots. `NotDel` excludes matching IDs from this forecast.

`GetRandItem` adds one projected slot only when mode is zero. `GetItem` similarly contributes its item/count total only in mode zero.

## Item deletion domain mismatches

Actual deletion does not use one uniform slot domain.

- Starred ordinary `DelItem` with active pile support and no `Break` calls `NPC_ActionDoPileDelItem`, which scans carried slots.
- Starred ordinary `DelItem` with `Break` scans all item slots.
- Non-star ordinary `DelItem` scans all item slots, including equipment.
- Under active `_ITEM_PILENUMS`, non-star `EVDEL` assigns `itemno=-1` and calls `NPC_ActionDoPileDelItem(talker,-1,-1)`. Real positive item IDs therefore are not deleted by that branch even though capacity preflight may have predicted their removal.

These mismatches are archaeology facts, not recommendations for a future redesign.

## NPC_EventAdd order

The stable path is:

1. select event block / one-based EVENT branch;
2. item-capacity preflight;
3. `DelStone` affordability precheck;
4. mode-zero pet-skill UI early return, if configured;
5. rewrite mode 2 to mode 0 **after** preflight;
6. grant `GetPet` / `GetEgg` for effective mode zero;
7. execute `DelItem`;
8. deduct `DelStone`;
9. prepare `GetRandItem`;
10. for `GetItem` mode zero, run a second post-deletion free-slot check, optionally grant the random item, then call `NPC_EventAddItem`;
11. for mode one, `GetItem` is instead passed to the delete routine;
12. standalone random-item grant if not already attempted;
13. enabled request-side `DelPet`;
14. return.

The path is non-transactional. A pet/egg may already have been granted, items may already have been deleted, and stone may already have been deducted before a later capacity or deletion failure returns false.

`NPC_EventAddItem` failure is propagated in the combined `GetItem` path. `NPC_RandItemGet` return values are ignored.

## NPC_AcceptDel order

The stable accept path is:

1. item-capacity preflight;
2. `DelStone` affordability precheck;
3. `GetStone` cap precheck;
4. mode-zero pet-skill UI early return;
5. `DelPet`;
6. add `GetStone`;
7. grant `GetPet`;
8. grant `GetEgg`;
9. execute `DelItem`;
10. deduct `DelStone`;
11. grant `GetRandItem`;
12. grant `GetItem`;
13. recompute player parameters.

`DelStone` and `GetStone` are prechecked independently against the starting gold. They are not netted. A transaction can therefore be rejected even if the later net result would be affordable or under the cap.

The `GetStone` cap test rejects `current + reward >= max`, so exactly reaching the cap is rejected.

The path has no rollback. If `GetStone` is applied and a later pet grant fails, the added stone remains. Random-item and normal item grant return values are ignored by `NPC_AcceptDel`, so the function can still return success after a failed item reward.

## Pet / egg candidate-list quirk

`NPC_EventAddPet` and `NPC_EventAddEgg` first scan for the first empty pet slot and then reuse that slot index as the starting token index when counting a comma-separated random candidate list.

This creates source-visible edge behavior:

- the legacy delimiter helper treats index 0 as a successful empty result, so first-empty slot 0 still advances through and counts the complete candidate list;
- first-empty indices inside the candidate range also converge on the configured candidate count;
- first-empty index exactly one past the candidate count still decrements back to the true count;
- starting further beyond the candidate list can leave a modulus wider than the configured candidate count, so selection may point beyond configured candidates.

The reconstruction exposes this quirk instead of replacing it with a clean uniform random choice.

## Event-flag mutation semantics

`NPC_EventSetFlg` sets an ENDEVENT bit.

`NPC_NowEventSetFlg` sets a NOWEVENT bit.

`NPC_NowEventSetFlgCls` is not a safe clear: it blindly XOR-toggles the NOWEVENT bit.

`NPC_NowEndEventSetFlgCls` conditionally clears the bit from both NOWEVENT and ENDEVENT if present.

This matters for `EndSetFlg`. Flows that first set the current event and then invoke the toggle clear it as expected; flows that reach `EndSetFlg` without a preexisting current-event bit can toggle that bit on instead.

## Deterministic artifacts

- `tools/stoneage_exchangeman_mutation_model.py`
- `tests/test_stoneage_exchangeman_mutation_model.py`
- `.github/workflows/validate-stoneage-exchangeman-mutation.yml`

Local validation: **25 deterministic tests passed**.

## Evidence status

FACT: the mutation order above converges across the three pinned descendant lineages.

FACT: the fixed gavin build enables both pile-item handling and request-side ExChangeMan pet deletion.

SOURCE QUIRK: ordinary non-star `DelItem` can terminate the capacity-forecast CSV loop early because one index variable is reused.

SOURCE QUIRK: capacity forecast can count starred deletion units as freed slots without verifying actual slot release.

SOURCE QUIRK: active pile-mode non-star `EVDEL` targets item ID `-1`.

SOURCE QUIRK: mode 2 is converted to mode 0 only after capacity preflight.

SOURCE QUIRK: `NPC_AcceptDel` ignores random and normal item-grant return values.

SOURCE QUIRK: `NPC_NowEventSetFlgCls` toggles instead of conditionally clearing.

OPEN: which of these keys and edge forms are actually used by the hash-pinned recovered 2.5 specimen. The next step is an aggregate, payload-free recovered-data probe.

## Next seam

Do not widen to another NPC class yet. Measure recovered ExChangeMan secondary-argument usage from the verified 2.5 preservation bundle, reporting only aggregate key/condition-family counts and source/data mismatches. Then use those results to decide whether another early/core NPC argument edge remains materially unresolved.
