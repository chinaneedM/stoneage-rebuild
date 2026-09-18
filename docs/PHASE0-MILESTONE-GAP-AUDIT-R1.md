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

### B1 — Save point / elder / return-point state — completed in R1

This is the immediate next seam.

Why it ranks first:

- character birth initializes `LASTTALKELDER` and a save-point bit;
- save-point NPCs mutate the same persistent fields;
- `appear.txt` login handling redirects selected saved floors through `LASTTALKELDER`;
- death/revival work already identified return-to-record-point behavior as an unresolved boundary;
- save/logout work already establishes the persistence transport used by save points.

The fixed descendants show a server-owned elder-coordinate registry plus per-character `LASTTALKELDER` and `SAVEPOINT` state. Reconstructing this closes birth -> savepoint -> login return -> persistence as one deterministic state machine.

### B2 — Persistent item/pet storage and pet-shop transfer — completed in R1

Direct trade and item shops are modeled, but movement between carried state and persistent storage/pool state is not yet closed. This should cover:

- item deposit/withdraw;
- pet deposit/withdraw;
- capacity and ownership checks;
- persistence boundary;
- pet-shop buy/sell or release semantics where they belong to the ordinary early loop.

Later account-shared **Depot/warehouse** extensions must remain versioned; ordinary character-embedded pool storage is a separate fixed-descendant persistence surface.

### B3 — Field warp / portal / map-transition authority — completed in R1

Map formats and login-return policy are known, but ordinary field traversal still needs a source-level model for:

- map exit/warp triggers;
- destination floor/x/y resolution;
- party propagation;
- invalid destination handling;
- logout/login interaction with no-resume or no-exit areas.

This is separate from graphical DAT caching.

### B4 — NPC placement / creation and event-data loading — completed in R1

The generic NPC world graph is now reconstructed and real-byte-probed:

- recursive magic-file discovery;
- template -> create reference resolution;
- map-floor validation;
- function-set dispatch and direct-override order;
- runtime generation / INITFUNC specialization;
- create argument linkage;
- generation timing and population gates.

The recovered 2.5 specimen contains 4,985 effective create blocks with complete template/map resolution. It also exposes two provenance hazards that must remain explicit: 30 create blocks reference duplicated template names, and 13 recovered function-set tokens are absent from all three fixed descendant source tables.

Class-specific secondary argument/config semantics remain follow-on content archaeology, not a blocker for the generic graph.

### B5 — Item / magic / pet-skill callback joins — completed in R1

The recovered active callback tokens are now cross-checked against the three fixed descendant dispatch tables without exposing proprietary table strings.

Result:

- magic: 17/17 unique tokens and 181/181 rows resolve in all three;
- item non-use callback slots: all recovered tokens resolve in all three;
- item use: 36 common + 16 branch-specific unique tokens, with zero all-source-missing tokens;
- pet skill: 65 common tokens plus 4 tokens/4 rows absent from all three fixed source tables.

The four pet-skill misses remain provenance/version-skew evidence rather than invented behavior.

### B6 — Ordinary magic effect semantics — completed in R1

The three pinned descendant dispatch tables share exactly nine unguarded magic callbacks, and the active recovered table aligns with that boundary:

- 9 all-three unguarded callback tokens / 130 active rows;
- 8 all-three guarded callback tokens / 51 active rows;
- no mixed-guard, partial-source, or all-source-missing active magic tokens.

R1 reconstructs the nine-function common core across:

- MP gate and mutation ordering;
- field/battle routing;
- living/dead target expansion;
- Recovery target-mode guards;
- VITAL-scaled recovery;
- field attribute changes;
- ordinary status application/recovery;
- magic-defense timers;
- resurrection;
- attribute reverse;
- resurrection + defense.

The model preserves historical quirks such as battle-only casts spending MP before field rejection, nonzero resurrection overwriting its earlier percentage-derived amount, highest-index-only status recovery, and non-immediate attribute restoration when reverse is toggled off.

`tools/stoneage_magic_effect_model.py` is covered by 35 deterministic regression tests. GitHub Actions run `35370420953` completed successfully.

### B7 — Common item effect semantics — highest priority

The enhanced active-item/source guard classification now gives a clean next boundary:

- 17 USE tokens / 818 active row uses are unguarded in all three fixed source lineages;
- 19 USE tokens / 86 rows are guarded in all three;
- 16 USE tokens / 53 rows have partial source-lineage coverage;
- no active USE token is absent from all three.

The next reconstruction should focus on the 17 all-three unguarded USE callbacks and the already-common non-use callback slots.

Initial common semantic families include:

- field/battle HP/MP recovery;
- status change/recovery;
- magic defense;
- parameter change;
- field-attribute change;
- attribute reverse;
- resurrection;
- capture-rate modification;
- warp/travel;
- encounter/no-encounter controls;
- selected persistent/player/pet state mutations.

Guarded and partial-source item callbacks remain explicit version-diff tracks.

### B8 — Common pet-skill effect semantics

After common item effects, reconstruct the 65 pet-skill callback tokens / 143 rows that resolve in all three fixed source tables.

Keep the four active pet-skill tokens / four rows absent from all three fixed source tables quarantined as source/data skew.

### B9 — Detailed combat sub-mechanics not yet promoted

The battle core is sufficient for the present loop audit, but future deterministic closure still needs source-verified treatment of remaining action/status/AI formulas where not already modeled. Add these only when early/core evidence requires them rather than copying later feature branches wholesale.

## C. Later/versioned optional systems — do not promote into early core by default

Keep these as separate version-diff tracks unless earlier evidence independently requires them:

- professions/job systems and profession skills;
- ordinary-player riding and later mount extensions;
- family/guild systems;
- AutoPK / tournament / arena extensions;
- pet fusion/egg systems;
- six-player party extensions;
- account-shared Depot/warehouse item and pet systems;
- binding/free-trade restrictions, fame/tax/shop extensions;
- later mission/event packages, hero/angel branches and high-level rebirth additions;
- later graphics/compression/high-color branches.

Presence in a descendant source tree is not evidence of launch-era presence.

## D. Data/content extraction gaps

The recovered gameplay inventory already exists and must remain the index rather than being recreated.

Current high-value extraction gaps are:

- classify the remaining root server tables by authority and runtime loader;
- resolve early/core NPC class-specific secondary argument/config edges where they materially affect core gameplay;
- complete common item and pet-skill semantic joins after the now-closed magic core;
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

1. ~~Reconstruct save point / elder / LASTTALKELDER return-point semantics.~~ **Completed.**
2. ~~Close persistent item/pet Pool storage while separating later shared Depot storage.~~ **Completed.**
3. ~~Close field warp / portal / map-transition authority while separating later mapwarp/no-exit layers.~~ **Completed.**
4. ~~Build the NPC/world-content graph: magic-file discovery, template/create relationships, dispatch, placement and argument linkage.~~ **Completed.**
5. ~~Close item / magic / pet-skill callback joins and classify fixed-source coverage.~~ **Completed.**
6. ~~Reconstruct the nine all-three unguarded ordinary magic effect callbacks.~~ **Completed.**
7. Reconstruct the **17 all-three unguarded common item USE callbacks** plus common non-use callback semantics.
8. Reconstruct the 65 all-three common pet-skill callback families, keeping four all-source-missing recovered rows quarantined.
9. Resolve only early/core NPC secondary argument/config edges that materially remain.
10. Continue detailed combat sub-mechanics only where evidence shows an early/core gap.

This ordering closes the ordinary game-state loop before expanding into optional systems.
