# Restoration-first stage gate R1

Status: **ADOPTED WORK ORDER; NOT A COMPLETION CERTIFICATE** (2026-10-12).

## Goal and sequence

First reconstruct and verify as much historically grounded StoneAge material
as can reasonably be recovered. **Only after an auditable historical recovery
review** shall the user and assistant decide how to design and produce their
new modern single-player StoneAge. Do not accelerate to engine/asset/gameplay
production simply because a technical milestone or a reported percentage rises.

## Baselines and historical boundaries

- **FOUNDATION:** accepted clean Taiwan Waei/JSS v1.0 disc and pinned
  evidence-derived metadata. It is not asserted byte-identical to JSS 1999.
- **ORIGIN:** JSS 1999 archaeology and original-design intent, including
  explicit differentiation between published concepts and shipping mechanics.
- **BRIDGES:** Mainland 1.82 and other independently proven early versions.
  Labels without verified client bytes are candidates, not accepted builds.
- **LATER COMPARISONS:** 2.5, 8.0/8.5 and other versioned materials are useful
  controls and a future content reference library, not automatic 1.0 facts.
- **SERVER LIMIT:** retail-client absence does not prove the absence of a
  server-authoritative mechanic; missing original server datasets remain OPEN.

## Completion register (evidence-based, no decorative aggregate percentage)

| Recovery family | Evidence required before closing the family | Current gate |
| --- | --- | --- |
| Original provenance and version lineage | Hash-pinned specimens, independent original identity, cross-version diffs | PARTIAL: TW1.0 foundation accepted; 1999 original and specific regional bridges have gaps |
| Executable/runtime and persistence | Static+dynamic attribution where possible, stack/object ownership, file IO, native save framing/checksum | OPEN: TW1.0 R14 exact register input and caller/global effects |
| World, maps, movement and encounters | Version-scoped maps, transitions, event triggers, geography, spawn and encounter data | PARTIAL: complete original world/server layer not accepted |
| Characters, pets, growth and capture | Deterministic formulas, authority/profile distinctions, client/server evidence | PARTIAL: substantial version-tagged recovery; unresolved authority/gaps |
| Battle, turns, skills and status | End-to-end reproducible scenarios with provenance and negative controls | PARTIAL: extensive battle evidence; outstanding profile/entry/reachability limits |
| Inventory, equipment, economy and drops | Identity, ownership, transaction/transfer, rewards, integrity and persistence | PARTIAL: extensive recovered and tested mechanics; full cross-system closure OPEN |
| Quests, NPC dialogue and progression | Versioned original scripts and server-dependent transitions or explicit gaps | OPEN: do not reconstruct missing original scripts as facts |
| Graphics, animation, sound and UI | Asset/format metadata, display and interaction rules, provenance, licensing boundaries | PARTIAL: engineering/source extraction exists; complete original coverage not accepted |
| Integration and reproducibility | Cross-system deterministic test matrices, version isolation, independent CI/artifact custody | PARTIAL: subsystem evidence exists; full historical acceptance pending |

PARTIAL means work exists, **not** that the listed family is nearly complete.
OPEN means evidentiary closure has not been demonstrated. Both categories
require concrete, version-scoped evidence before advancement.

## Acceptance requirements

1. Inventory every recoverable subsystem and evidence source, with baseline,
   file/build identity, source confidence, date, and what it does **not** prove.
2. Deliver reproducible extraction reports/specifications and bounded tests.
   No original proprietary binaries or assets enter the public repository.
3. Cross-check shared gameplay state and end-to-end dependencies (world ↔
   encounter ↔ combat ↔ reward ↔ roster/inventory ↔ save).
4. Distinguish FACT, HYPOTHESIS, DESIGN and OPEN. Permit explicit **evidence
   unavailable / original server authority unrecovered** closures, without
   misrepresenting them as fully restored facts.
5. Publish an evidence-backed acceptance matrix for all families, including
   unresolved limitations, regressions, historical-version scope, and the
   exact remaining production risks.
6. Obtain a separate joint user review of the restoration results **before**
   choosing a new engine, committing to new lore/era integrations or starting
   the full modern game build.

## Immediate work queue

- TW1.0 R14: determine conservative reaching definitions for EBX at 0x49dec,
  EAX/ESI at 0x4943c/0x4944a/0x49457/0x49463, graph bounds, CALL barriers,
  possible frame prologues and branch joins.
- Next: independently qualify original native persistence / handle / buffer
  semantics if the evidence permits; never silently collapse uncertainty.
- Continue the version-tagged inventory and original world/server gap closure
  without promoting later rules to the earlier baseline.
- Non-core 8.0 provenance tests must not be invoked solely by general
  TW1.0 `CURRENT-STATE.md` continuity updates.

See `docs/CURRENT-STATE.md` and `DD-021` for authoritative next tasks.

## 2026-10-12 queue supersession (R21 accepted)

The original immediate-work bullet retained above describes the historic
R14 entry point; the current authoritative latest CURRENT-STATE entry
supersedes it. R14–R21 bounded static evidence and independent custody
receipts are available; **R21 is conditional static acceptance only**.
Current highest NEXT is **TW1.0 R22**: CALL 0x499d4 effects/input
barriers, HeapReAlloc 0x4a0c4 pre-CALL source feasibility and
post-CALL opaque return, and cycle-aware EAX alias at 0x4a17d.
The original native-save persistence gate and all other system-family
PARTIAL/OPEN states remain unchanged. Engine/content production is
still deferred until joint review of Stage A.
