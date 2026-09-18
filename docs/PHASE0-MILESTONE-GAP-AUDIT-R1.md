# StoneAge Phase 0 Milestone / Gap Audit R1

Status: **current remote-state audit; no historical-baseline promotion**
Date: 2026-09-18
Authority: `main` remote state at the start of this audit.

## Purpose

This audit separates four things that had begun to mix together in continuity notes:

1. early/core deterministic mechanics already reconstructed;
2. remaining early/core deterministic gaps;
3. later/versioned optional systems that must not be flattened into the baseline;
4. modern-rebuild engineering work that belongs after historical behavior is understood.

The recovered 2.5 bundle remains a mixed preservation specimen. Its useful bytes and descendant source can establish formats, data relationships and implementation behavior, but they do **not** by themselves establish a 1999/JSS baseline.

## A. Early/core deterministic mechanics already reconstructed

The repository already has independently written models/tests or source/data reports for the following loop segments:

- character creation and four-hometown birth linkage;
- player EXP/growth and transmigration/reset semantics;
- enemy-base templates, concrete enemy variants, groups and encounter-area selection;
- battle entry/core/reward behavior at the currently modeled boundary;
- player death and in-place resurrection;
- pet capture and pet growth;
- field party formation and battle projection;
- item use/equipment movement and parameter recomputation;
- healer/recovery service behavior;
- direct player trade;
- ordinary NPC item-shop buy/resale behavior;
- periodic save, save-point save request semantics, logout cleanup and SAAC acknowledgement ordering;
- `appear.txt` login-return / non-resumable-floor behavior in the older fixed descendants;
- recovered gameplay-table inventory and cross-table coherence checks;
- recovered item, skill/magic, pet-skill, EXP, DAT/map and REAL/ADRN/RD/SPR resource-family probes.

These pieces now cover most of the ordinary loop:

```
create
 -> spawn
 -> world movement / encounter
 -> battle
 -> reward / capture / damage / death
 -> party / equipment / healing / trade / shop
 -> persistence / logout
```

The largest remaining gaps are therefore no longer “basic combat exists?” questions. They are the world-state transitions and storage/content joins around that loop.

## B. Remaining early/core gaps

### B1 — Save point / elder / return-point state — highest priority

This is the immediate next seam.

Why it ranks first:

- character birth initializes `LASTTALKELDER` and a save-point bit;
- save-point NPCs mutate the same persistent fields;
- `appear.txt` login handling redirects selected saved floors through `LASTTALKELDER`;
- death/revival work already identified return-to-record-point behavior as an unresolved boundary;
- save/logout work already establishes the persistence transport used by save points.

The fixed descendants show a server-owned elder-coordinate registry plus per-character `LASTTALKELDER` and `SAVEPOINT` state. Reconstructing this closes birth -> savepoint -> login return -> persistence as one deterministic state machine.

### B2 — Persistent item/pet storage and pet-shop transfer

Direct trade and item shops are modeled, but movement between carried state and persistent storage/pool state is not yet closed. This should cover:

- item deposit/withdraw;
- pet deposit/withdraw;
- capacity and ownership checks;
- persistence boundary;
- pet-shop buy/sell or release semantics where they belong to the ordinary early loop.

Later shared-pool extensions must remain versioned.

### B3 — Field warp / portal / map-transition authority

Map formats and login-return policy are known, but ordinary field traversal still needs a source-level model for:

- map exit/warp triggers;
- destination floor/x/y resolution;
- party propagation;
- invalid destination handling;
- logout/login interaction with no-resume or no-exit areas.

This is separate from graphical DAT caching.

### B4 — NPC placement / creation and event-data loading

The recovered server corpus contains a large NPC configuration tree, but it is not yet normalized into an authoritative world-content graph.

Needed:

- creation/template/include relationships;
- NPC type/function dispatch;
- floor/x/y placement;
- argument/config linkage;
- early/core NPC classes versus expansion/event content.

This should be provenance-preserving and aggregate-first; original content payloads should not be committed by default.

### B5 — Item/skill effect callback joins

The repository has item/skill/magic tables and equipment/use mechanics, but a complete table-record -> callback/function -> battle/world effect graph is still incomplete. This is needed before claiming full deterministic reconstruction of consumables, magic and pet skills.

### B6 — Detailed combat sub-mechanics not yet promoted

The battle core is sufficient for the present loop audit, but future deterministic closure still needs source-verified treatment of the remaining action/status/AI formulas where not already modeled. These should be added only when they are early/core-relevant rather than by copying later feature branches wholesale.

## C. Later/versioned optional systems — do not promote into early core by default

Keep these as separate version-diff tracks unless earlier evidence independently requires them:

- professions/job systems and profession skills;
- ordinary-player riding and later mount extensions;
- family/guild systems;
- AutoPK / tournament / arena extensions;
- pet fusion/egg systems;
- six-player party extensions;
- shared pool item/pet systems;
- binding/free-trade restrictions, fame/tax/shop extensions;
- later mission/event packages, hero/angel branches and high-level rebirth additions;
- later graphics/compression/high-color branches.

Presence in a descendant source tree is not evidence of launch-era presence.

## D. Data/content extraction gaps

The recovered gameplay inventory already exists and must remain the index rather than being recreated.

Current high-value extraction gaps are:

- classify the remaining root server tables by authority and runtime loader;
- build an NPC/world-content graph without publishing original text payloads;
- connect item/skill/magic records to executable behavior;
- preserve cross-version mismatch evidence in the mixed 2.5 specimen rather than silently “repairing” it;
- compare the same tables against the first clean 1.74 / 1.74a / JSS bridge artifact when recovered.

The current encounter coherence defects are specimen-integrity evidence, not rules to reproduce.

## E. Modern rebuild engineering — intentionally separate from archaeology

Do not “fix” historical behavior inside the reconstruction model. Record the old behavior first, then design improvements separately.

Likely modern-engineering work includes:

- transactional save/trade/storage operations;
- typed schemas and import pipelines for authoritative game data;
- deterministic simulation/replay tests;
- explicit versioned rule packs instead of compile-time macro sprawl;
- safe ID/range validation;
- modern engine selection, rendering, networking and UI architecture;
- independently recreated/licensed assets.

These are DESIGN decisions, not historical FACTs.

## F. Evidence/provenance blockers

No repository or CI blocker is present.

The principal historical blocker remains the absence of a provenance-preserving clean early client/server artifact. The recovered 2.5 bundle is technically valuable but cross-revision and contaminated; its internal mismatches must remain visible.

## Ordered next work

1. Reconstruct **save point / elder / LASTTALKELDER return-point semantics** across the fixed source descendants.
2. Add deterministic tests for registration, unlock bits, last-elder switching, requirement-gated activation and return lookup.
3. Explicitly record representation/version hazards rather than normalizing them away.
4. Then close **persistent item/pet storage**.
5. Then close **field warp / portal / map-transition authority**.
6. Then build the **NPC/world-content graph** and remaining item/skill effect joins.

This ordering closes the ordinary game-state loop before expanding into optional systems.
