# RULES-01 coordinator-bound shop → ITEM-gate → save/reload R1

Date: 2026-10-16. **Scope: a narrow extra test of the existing shop adapter and coordinator, NOT an alternate shop implementation or a historical quest closure.**

## Why this additional verification is necessary

The newly accepted `tools/stoneage_rules01_shop_gate_reference.py` already demonstrates source-bounded normal shop acquisition, recovered25 held-item FREE eligibility and real filesystem serialization. Do **not** clone or replace it. A separate, concrete caller seam remains: the **authoritative `LocalRuntimeSessionCoordinator`** independently performs interaction discovery, spatial source checks, state-gate rechecks, transition execution, occupancy save-snapshot packaging and reload. Prior bounded RULES-01 fixture exercised the evaluator and local session codec, but not that full coordinator dispatch cycle after purchasing and reloading.

The targeted extra test uses the already accepted adapter without creating a new production shop function. The synthetic stack declares all transitions, but puts only the ordinal-3 ITEM-gated WarpMan in the synthetic player's reach, with two invented 3×3 rooms. The item 99901, gold300, base cost80, buy-rate1.25, LV10, NPC bindings, positions and event predicates are **invented fixture data**. None is represented as observed original source, nor is this the actual historical route execution.

## Actual integration exercised

- A new session cannot discover an eligible ITEM/FREE route until it truly owns the matching item; a forged world flag cannot replace ownership.
- The existing **normal one-unit purchase model** inserts the item and lowers persistent Stone from300 to200, without modifying the input session or granting a quest award.
- `LocalRuntimeSessionCoordinator.save_game` stores the bought state through `LocalFilesystemPersistenceStore`; a **new coordinator and store instance** reads it and re-evaluates the current inventory gate.
- After loaded-state discovery and canonical `dispatch_state_gated_interaction`, the coordinator moves to the synthetic target room, with no inferred item consumption, EXP award or world flags.
- A **second independent save/reload** preserves the destination position, Stone, item ID/view and unchanged EXP. A wrong item stays a wrong item after reload and does not unlock; an invented item-permission world flag likewise does not unlock.

This is a real engine-neutral **local reference lifecycle** under explicit source-version constraints. The prior historical route rules remain `LATER_RECOVERED`; the fixture is `SYNTHETIC`. Original JSS1999/TW1.0 NPC ownership, item identity, shop catalogue, fee/reward state, source-authoritative commercial save acknowledgement, and WarpMan random real-world destination still remain `OPEN`.

The companion suite `tests/test_stoneage_rules01_coordinator_gate_reload.py` deliberately depends on the existing shop model, gate evaluator and coordinator. It must not increase historical coverage claims or lead to reenumerating all maps/NPCs, reopening R79 or selecting a new game engine.

After passing independent CI, qualify this as `REFERENCE_COORDINATOR_REENTRY_VERIFIED_HISTORICAL_REWARD_OPEN`. The finite RULES-01 core-playflow audit can then advance to the nine-family Stage A acceptance/gap inventory rather than expanding a duplicate shop implementation.
