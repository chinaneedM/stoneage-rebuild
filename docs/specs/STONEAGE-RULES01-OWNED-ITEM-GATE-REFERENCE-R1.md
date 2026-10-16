# RULES-01 — Owned item → conditional WarpMan gate → local save reference R1

Date: 2026-10-16. **Status: reference integration under source-conditional acceptance; not original historical server or quest completion.**

## Gameplay result and source scope

The previous RULES-01 preflight found an actual interaction gap between (a) the convergent descendant ordinary shop buy rule, (b) player-owned inventory items, (c) recovered25 WarpMan `ITEM`/`FREE` predicates and (d) persistent/local-state boundaries. This small adapter makes that join executable without inventing a retail Taiwan 1.0 shop, NPC script or server record.

Inputs are **explicitly supplied**: item offered by the selected shop, selected item identity, unit base/override cost, buy rate, item-view fields, current authoritative Stone/gold, usable capacity, evidence role/version, and a source/fixture receipt. A mismatched offer, unqualified profile, absent gold field or invalid configuration **fails closed**. This module currently accepts only `recovered25` / `LATER_RECOVERED`; it does not infer a launch-era rule.

- Code: `tools/stoneage_rules01_shop_gate_reference.py`.
- Existing priced normal-buy rule: `tools/stoneage_item_shop_model.py` and `research/mechanics/STONEAGE-ITEM-SHOP-CORE-R1.md`.
- Existing held-item predicate: `tools/stoneage_recovered25_world_profile_adapter.py` (`Recovered25TransitionGateEvaluator`).
- Existing local save schema: `tools/stoneage_local_runtime_core.py`, `tools/stoneage_singleplayer_persistence.py`, and `tools/stoneage_local_filesystem_persistence.py`.
- Tests: `tests/test_stoneage_rules01_shop_gate_save_reference.py`. Fixture actor/item IDs, item prices and NPC target are **invented test inputs**.

## End-to-end narrow replay

The regression exercises:

1. No owned key item → recovered25 item-gated predicate rejects; a world flag pretending to grant the item also fails.
2. One explicitly source/fixture-qualified normal purchase → one actual `InventoryItem` in the first available declared-capacity slot; integer-truncated `base_cost * buy_rate` deducted from persistent Stone only when insertion succeeds.
3. Re-evaluating the **current owned inventory** → item-gated recovered25 predicate accepts; `consumed_state` is empty, with no inferred award, fee or quest side-effect.
4. Save the resulting session to a **real temporary local filesystem directory**, reopen it through a new store instance, decode the versioned local session, and re-evaluate the live predicate. Item identity, its supplied view and Stone survive; removing that item revokes the gate. This is a test of *modern reference persistence only*.
5. Insufficient Stone, no available declared-capacity slot, mismatched offered item, missing gold, invalid version/role or malformed inputs fail without modifying the original state.

**No historical content is recovered by the invented fixture.** It proves that the previously separate reusable model boundaries can compose without silently turning a flag into owned inventory or confusing a local disk record with original SAAC server persistence.

## Explicit negative boundaries

- The adapter handles one fully successful normal-unit purchase and ordinary pre-mutation declines only. The descendant source has **no rollback** for abnormal mid-creation/mid-insertion failures; this test neither emulates nor declares such a failure atomic.
- No original item ID, NPC stock list, exact original Gold/Stone amount, game price, item source script, dialogue, reward, original task, first-generation level requirement or shop chronology is asserted.
- WarpMan `FREE` here is a non-consuming predicate. Other gates may require mutations; the coordinator already fails on an unimplemented `consumed_state`, and this adapter has no authority to execute such a route.
- The chosen destination and available transition depend on a source-matched binding and separate legal outcome; the regression does not prove the complete recovered25 live route or any original-server interaction.
- Local save/reentry is explicitly a new engine-neutral DESIGN layer. Original server character serialization includes DATA/items but not generic WORK state; the original asynchronous unlock-before-durable-save problem remains OPEN. TW1.0 client-local savedata R79 stays PAUSED_NON_BLOCKING.
- Player/pet EXP thresholds, capture/skill identity and original award payouts are outside this join and remain independently evidence-limited.

## Closure criterion and next action

This subpackage is useful only if its independent CI succeeds. On acceptance it closes a **bounded reference integration seam**, not the complete RULES-01, quest content, world family or Stage A. Record exact CI run and SHA in the current state; do not claim the source-level original commercial server executed.

Then perform one finite RULES-01 review: determine whether a *real source-qualified NPC award/write input* exists that can extend this narrow item gate into actual historical quest/reward state. If absent, record `OPEN_EVIDENCE_LIMITED` and move to the highest-impact unreviewed Stage A family instead of making up scripts, repeatedly cloning the same bridge test or reopening arbitrary savedata helpers.

## Separate later source: exchange award is not the same shop gate

A bounded source-derived comparison additionally found **two recovered25
ExChangeMan ACCEPT/EventEnd award records** with level threshold and
level-scaled DELSTONE, followed by GETITEM for the withheld key item. The
target is not the event's ITEM prerequisite and is not removed by those
records. The separate later shadowed-branch progression witness traces
award → classic Warp → guarded WarpMan ingress. It is **not** the WORLD-01
hometown-3/4 shop-purchase path and must never be merged into one invented
launch-era quest.

An NPC reference census also finds one WarpMan DelItem reference alongside a
WarpMan FREE reference. Reference presence alone does **not** prove the same
selected instance/branch consumed the gate item. Conversely, the limited
non-shop drop/AddItem probe's zero matches do **not** disprove the separate
ExChangeMan GetItem awards.

Persistence remains the concrete unresolved source seam: whether the exact
awarded/purchased target has ITEM_DROPATLOGOUT, which EventNo/quest state is
serializable, and whether the historical server's asynchronous write
actually survives reconnect cannot be answered by the retained source reports
or by our modern local disk test. No universal historical reward/ownership
durability is promoted.

Source-pinned boundary matrix:
`research/recovered/STONEAGE-RULES01-KEYITEM-AWARD-BOUNDARY-R1.json`;
independent custody and negative-evidence guard:
`tests/test_stoneage_rules01_keyitem_award_boundary.py`.
