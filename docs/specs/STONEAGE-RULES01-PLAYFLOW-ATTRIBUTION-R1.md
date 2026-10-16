# RULES-01 — source-versioned ordinary-playflow cross-system preflight

Date: 2026-10-16. **PREFLIGHT, not RULES-01 closure**. This is an evidence/priority pass after the 24-cell WORLD-01 review. It does not create a new historical ruleset, fill missing commercial server scripts or authorize Stage B design.

## What does this restore?

The goal is to connect ordinary field encounters, reward attribution, player/pet growth, shop and Stone, item-gated NPC progression and persistent state into one properly versioned chain. The principal gap is the *source of authoritative values and state ownership*, not an absence of one more generalized parser or ABI helper.

## Eight explicit joins

| Seam | Current proven/useful source behavior | Material unresolved source or state |
|---|---|---|
| RULES01-01 `WORLD_POSITION_TO_ENCOUNTER` | Recovered25 selected routes and strict encounter-area/group/enemy model support explicit deterministic encounter rolls. | Original TW1.0/JSS1999 enemy population and rate, failed group IDs outside chosen witnesses; do not repair missing rows. |
| RULES01-02 `DEFEAT_TO_BATTLE_LOCAL_EXP` | Ordinary source profit path attributes defeated enemy reward to eligible attack-list participants through WORKGETEXP before finish; non-killing parties do not receive universal free EXP. | Original launch-era EXP award roster and all later gated profit branches not independently dated. |
| RULES01-03 `PLAYER_EXP_TO_LEVEL` | Legacy cumulative EXP profile and later per-level subtracting profile are explicitly incompatible; below crossing the shared EXP-add subset is reusable. | JSS1999 threshold representation/table, exact TW1.0 operating-server regime, level caps/creation defaults. |
| RULES01-04 `CAPTURE_TO_OWNED_PET` | Capture probability/gates and growth identity transfer are source-shaped; new roster/reentry lifecycle is verified only when full explicit PetActor state exists. | Automatic construction has insufficient source for current MP, initial EXP/thresholds, full skills/status and visible AI; no guessed defaults. |
| RULES01-05 `PET_EXP_TO_GROWTH` | Each level gain requires PETRANK, individualized ALLOCPOINT and ten stat allocations plus rank-band roll; hidden VARIABLEAI changes, visible compliance not inferred. | Early JSS growth coefficients, visible loyalty projection and complete source-aligned captured pet initial state. |
| RULES01-06 `SHOP_STONE_TO_ITEM` | Ordinary shop computes int(base cost*buy rate), clamps to free carried slots, inserts instances first and deducts total Stone only after success; partial failure is not rollback-atomic in old source. | Historic commercial NPC inventories/rates and early chronology; exact shop route currently recovered25 only. |
| RULES01-07 `ITEM_OWNERSHIP_TO_WARPMAN_AND_AWARD` | Hometown routes 3/4 have ordinal-specific COMBAT/SHOP ordering, a real normal item purchase, guarded WarpMan FREE predicate and downstream award-side witness. | Exact early quest award/content membership and original commercial NPC scripts/conditions remain unknown; a route witness is not full original quest completion. |
| RULES01-08 `PERSISTENT_FIELDS_TO_SAVE_AND_LOGIN` | Descendant character serialization covers data fields, carried items/pets and ordinary pool, not arbitrary WORK runtime values; logout-only items are deleted pre-save, SAAC unlock precedes known durable write. | Original first-generation server format and successful write/relogin behavior; original client-local savedata and modern reference save are separate layers. |

## Critical distinctions

**1. Early UI does not determine historical EXP semantics.** Taiwan-v1 visible EXP/maxEXP fields coexist with two incompatible descendant EXP transition regimes: cumulative legacy EXP and later subtracting per-level EXP. The mixed 2.5 external EXP table is not a JSS1999 baseline. Both share only the below-threshold addition when the caller has explicit source-valid values.

**2. A kill, a captured pet and a quest reward are three different outcomes.** The battle-local WORKGETEXP profit chain is not general victory loot. Successful capture does not pay kill EXP; captured pet growth identity may transfer, but current MP, initial EXP/maxEXP, skills/status and visible compliance cannot be invented. Ordinary item-shop purchases are conditional on empty slots, exact configuration and Stone; a normal purchase is required before item-gated WarpMan in WORLD-01's conditional routes. No original story reward or commercial NPC argument can be reverse-inferred from the successful route witness.

**3. Durable state has three owners.** Historic server persistent character fields differ from server WORK/session state; TW1.0 client-local savedata is a separate file; modern test-local persistence is a new reference implementation. The source exhibits logout-item deletion and unlock-before-write ordering. A successful local reload proves neither an original commercial transaction nor a safe original save acknowledgement.

## Current priority and stop condition

Start with the **owned item → guarded WarpMan/NPC award → persisted state** representative chain, using the already accepted WORLD-01 and existing shop/persistence/capture models. Inspect concrete callers and authoritative saved fields only where the source contains the needed data. If a specific item gate, reward or save prerequisite is not part of retained source, record `OPEN_EVIDENCE_LIMITED` and skip speculative enumeration. Player/pet EXP threshold regimes remain source-qualified but must not be consolidated into one invented JSS setting. Do not reopen R79 without a named missing business field.

This preflight identifies *which* 8 domain joins exist and what evidence would be required. It does **not** complete them: Stage A families remain PARTIAL/OPEN and Stage B gated.

## Source provenance

Machine-readable source paths, blob SHA, byte sizes, gap/impact/inputs for all eight seams: `research/recovered/STONEAGE-RULES01-CROSSSYSTEM-PREFLIGHT-R1.json`.
- world: `research/recovered/STONEAGE-WORLD01-FOUR-HOMETOWN-ACCEPTANCE-R1.json` (`5b7abe7e05bd6c9074c556cb4cf105d371bfa26e`, 36216 bytes)
- encounter: `docs/RECOVERED25-ENCOUNTER-RUNTIME-R1.md` (`30a8fcddeddfe72f62fb6efc2628a9c63843fe71`, 3806 bytes)
- exp: `research/mechanics/STONEAGE-BATTLE-EXP-SETTLEMENT-R1.md` (`ca29eec6a72dbb30b5668c216dcacc2684bfddcb`, 11999 bytes)
- player: `research/mechanics/STONEAGE-PLAYER-GROWTH-CORE-R1.md` (`a08a8b29ac8c1f466e70d4b1b9a9e471c855bfa7`, 9206 bytes)
- capture: `research/mechanics/STONEAGE-PET-CAPTURE-CORE-R1.md` (`c44ba2ce47c66f9036f4cbdec9faf20c2bf20e3c`, 11243 bytes)
- capture_source: `docs/specs/STONEAGE-CAPTURE-STATE-SOURCES-R1.md` (`854b863ffe31babc64cb64e72c7eba1a967e2a43`, 5190 bytes)
- pet: `research/mechanics/STONEAGE-PET-GROWTH-CORE-R1.md` (`87cdd063f05f6d6f334007cf3db7a31a8d1654a8`, 8969 bytes)
- shop: `research/mechanics/STONEAGE-ITEM-SHOP-CORE-R1.md` (`e355506d98b401f59e5c008fd375505bfb139163`, 11288 bytes)
- npc: `research/mechanics/STONEAGE-NPC-WORLD-CONTENT-GRAPH-R1.md` (`bb03862dd7dd253effd57c506d0a56b490685974`, 12172 bytes)
- persistence: `research/mechanics/STONEAGE-SAVE-LOGOUT-PERSISTENCE-CORE-R1.md` (`324d951341d7e0ac1b1996659857614a08b72f12`, 13349 bytes)
- coordinator: `docs/LOCAL-RUNTIME-SESSION-COORDINATOR-R1.md` (`6341da10aab2b5062f557c13b45b457ddf69649f`, 20857 bytes)
