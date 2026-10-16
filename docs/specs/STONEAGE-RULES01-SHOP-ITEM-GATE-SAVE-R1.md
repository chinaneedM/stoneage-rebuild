# RULES-01 bounded shop-to-item-to-WarpMan-to-local-save join

Date 2026-10-16. **MODEL_CHAIN_VERIFIED only when its Actions gate passes.** The source scope is a **later recovered25** map/gate/content witness and convergent **descendant** ordinary shop/save rules; this is not a proof of the TW1.0/JSS1999 original NPC, item, prices, quest award, server schema, or production save.

## Material game behavior and gap

RULES-01 preflight linked the *existence* of shop calculation, a persistent inventory, item-gated WarpMan and local session save, but no bounded executable purchase→item→gate→save/reload join had been exercised. WORLD-01 routes 3 and 4 specifically need a **normal affordable shop purchase** before an ITEM/FREE conditional WarpMan. Thus only this seam warranted additional integration; the other routes, full map census and savedata R79 do not.

## Implemented bounded reference adapter

`tools/stoneage_rules01_shop_item_ownership.py` composes the existing ordinary `simulate_purchase` with `PersistentPlayerState.inventory` and the explicit character `gold` field. It requires every content input (source identifier, item ID, view, base cost, buy rate and inventory capacity) from a source-matched caller. It accepts only `recovered25` / `LATER_RECOVERED` and a **single successful ordinary purchase**. It chooses the first empty slot in the caller-provided capacity and copies character/item/pet/selection state into a new session; no existing session is mutated by the adapter. Failure for insufficient Stone or capacity returns the identical unchanged session.

The adapter deliberately **does not** invent available shop stock from item IDs, execute or reverse engineer an original dialogue/script, emulate original partial allocation failure, or grant quest rewards. Original descendant shop code can insert some items before a later insert fails, without deducting Gold; the existing standalone model retains that negative witness. The new local adapter exposes only the success path. This is a modern reference composition, not a claim of old transaction atomicity or an original client purchase UI.

## Five fixed-fixture checks

`tests/test_stoneage_rules01_shop_item_warp_save.py` uses invented item 99901, Stone 300, price 80 × 1.25 = 100, 15 available inventory slots, and two tiny invented map rooms. **All values are synthetic.** The test composes the **actual** source-derived normal shop calculator, `Recovered25TransitionGateEvaluator`, `LocalRuntimeSessionCoordinator` item gate/discovery/dispatch and `LocalRuntimeSaveSnapshot` roundtrips:

1. Without the key item, gate denies. Normal purchase adds one item, deducts Stone and unlocks the exact matching source-shaped ITEM predicate.
2. Save/reload before gate preserves bought item and Stone; the reloaded conditional gate still passes, dispatch moves once, and a second save/reload preserves movement, item and Stone.
3. Neither purchase nor warp invents any quest award, EXP gain, reward flags, item consumption, or pet mutation.
4. Insufficient Stone, full specified inventory, wrong item and absent/wrong historical source classification do not silently unlock the WarpMan.
5. Separate old-shop allocation failure behavior is checked but explicitly *not* promoted to the successful one-item adapter.

Test acceptance, when green, demonstrates a **modern local-reference state join** with actual integration, not historical commercial-server execution, original v1.0 item membership, event scripting, exact original shop inventory or original award state.

## Remaining named blockers and stop

- Exact **recovered25** item/shop/NPC argument and binding payloads are outside the public repo, available only from a hash-pinned transient source bundle; no raw route coordinates, NPC strings, original items, dialogues or proprietary bytes may be invented or committed.
- Exact **1999 / Taiwan1.0** original shop stock, source conditional-NPC content, quest outcome, item consumption (if any), and serializable reward ownership remain `OPEN`.
- Modern local save is independent of original historical server DATA/WORK and SAAC durability; known old unlock-before-write behavior remains a separate safety risk.
- The conditioned original route still requires additional source-qualified player level/fee, map and random destination inputs; passing the synthetic test does not prove guaranteed progression.
- Do not reopen low-level savedata R79 merely to complete this local chain.

**Work-package stop condition:** after the selected direct integration tests and independent CI pass, qualify the ownership seam as `LOCAL_REFERENCE_CHAIN_VERIFIED_HISTORICAL_CONTENT_OPEN`, preserve remaining historical source gaps, and return to RULES-01 domain prioritization / Stage A portfolio review. Source archives and old historical claims remain unchanged. This is not an overall restoration percentage.
