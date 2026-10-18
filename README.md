# stoneage-rebuild

A long-term research and development project to reconstruct the origins, evolution, and core experience of **StoneAge / 石器时代**, then rebuild it as a modern single-player 2D turn-based RPG.

## Project intent

This project is **not** a binary patch, private-server repack, or direct copy of an old client. The historical clients, manuals, screenshots, magazines, websites, videos, and later regional versions are treated as research evidence.

The development goal is to:

1. Use the accepted **Taiwan Waei/JSS v1.0 clean retail client** as the historical foundation baseline for reconstruction.
2. Preserve provenance and inventory the baseline at file level, then recover its executable/runtime structure, resource formats and deterministic gameplay state.
3. Reconstruct maps, characters, pets, attributes, skills, items, NPC/world systems, UI, text/data tables and other game rules using version-tagged evidence; original server-only content is reconstructed rather than assumed to be present on the retail disc.
4. Diff earlier/later clean official versions when available to reconstruct evolution across JSS, Taiwan, Korea, Mainland China and later branches; later releases are a design/content library rather than mandatory cumulative upgrades.
5. Reimplement the resulting specifications as a private/local-first single-player game with MMORPG-style depth, modern rendering/input/save architecture, and independently created/recreated production assets.
6. Preserve the emotional milestones and core StoneAge design DNA while deliberately redesigning pacing, systems and content where the modern project requires it.

## Current phase

**Phase 1 — Foundation Baseline Technical Reconstruction & Specification**

The Taiwan Waei/JSS v1.0 retail client is accepted as the R1 historical foundation baseline. Open-ended hunting for an absolute-earliest client is no longer on the critical path.

Primary targets:

- close the remaining v1.0 runtime/gameplay semantics that materially affect reconstruction;
- convert recovered graphics, animation, battle, audio, protocol and state evidence into engine-neutral deterministic specifications;
- reconstruct world/map and server-authoritative content from version-tagged evidence without falsely projecting later data into v1.0;
- use later official versions and recovered server/master data as controlled bridges and a future design/content library;
- keep earlier-client discovery opportunistic and non-blocking;
- prepare the local-first single-player architecture without prematurely building MMO services.

See [`docs/CURRENT-STATE.md`](docs/CURRENT-STATE.md).

## Continuity

Every new ChatGPT conversation must start from the repository rather than chat memory.

Read [`docs/PROJECT-CONTINUITY-PROTOCOL-R1.md`](docs/PROJECT-CONTINUITY-PROTOCOL-R1.md) first.

Recommended restart message:

> 继续《石器时代》项目。按仓库 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` 启动，以 GitHub 远端最新状态为唯一事实源。先读取连续性协议、`docs/CURRENT-STATE.md` 和最新提交，然后从最高优先级未完成事项继续推进。

## Repository layout

- `docs/` — project vision, continuity, historical timeline, decisions, current state.
- `research/origin/` — JSS-era origin research.
- `research/clients/` — client/version archaeology and future diff reports.
- `research/sources/` — source notes and archival metadata.
- `game/` — future modern game implementation.
- `tools/` — archaeology/parsing/diff tooling.
- `tests/` — future deterministic tests.

## Copyright boundary

Do not commit copyrighted original game binaries, ripped art, music, sound effects, manuals, or other proprietary assets unless their legal status and repository policy explicitly allow it. Prefer storing metadata, hashes, filenames, observations, and research notes. The rebuilt game should use independently implemented code and newly created/recreated assets.


## Current restoration roadmap — 2026-10-16

Use [Restoration Roadmap R2](docs/RESTORATION-ROADMAP-R2.md) and the latest
CURRENT-STATE entry for the current work order. Priority is PET-STATE-01: qualify current capture-to-owned-pet state sources
and repair only evidence-supported missing joins. Reuse the closed four
hometown routes for later finite overall acceptance; do not repeat them.
The deep client-local savedata helper branch is paused as non-blocking; its
R1–R78 evidence and R79 preflight remain preserved. Restoration still precedes
joint new-game design.


### Current package update — 2026-10-16

PET-STATE-01 has bounded capture/roster/save/reentry/growth acceptance; full
pet autoconstruction remains evidence-limited and requires explicit state.
Highest next is WORLD-01's finite existing-route provenance/gap review, as
recorded in the latest CURRENT-STATE and Roadmap R2 append. R79 stays paused.


### Current work order override — 2026-10-16 Stage A source review

Earlier dated roadmap notes above remain historical context. The authoritative
current work order is the **latest** entry in `docs/CURRENT-STATE.md`.
After the WORLD-01 and bounded RULES-01 representative integration checks,
`STAGE-A-REVIEW-PREFLIGHT` has audited all nine system families without
claiming Stage A completion. The next finite target is `UI-SEMANTICS-01`:
five original Taiwan-v1 client protocol-to-interaction/resource specifications.
Stage A remains PARTIAL/OPEN, Stage B gated and client-local savedata R79 paused.
No original server-only game content is inferred from modern model tests.


### Latest restoration package — UI-SEMANTICS-01 (2026-10-16)

Accepted on a separate branch and source/CI qualified: five original Taiwan
v1 client protocol/UI **input** crosswalks, 16 decoded-record source contracts
and 14 compiled message envelopes. Visual screen placement, art-selection
runtime and original commercial server content remain unproven. Next finite
priority: **UI-RESOURCE-BIND-01**, only original pet graphic selector and
battle SAB/palette selector evidence, not a new engine or post-1.0 UI.
Authoritative detailed order remains the final entry of CURRENT-STATE.


### Latest restoration scope — UI-RESOURCE-BIND-01 (2026-10-16)

Original v1 battle resource identity, address order and lineage-supported
20×20 SAB interpretation now have bounded reference validation; actual
v1 battle palette/background selection and pet drawing-to-animation
bindings remain OPEN. Next priority:
**STAGE-A-NPC-CONTENT-BOUNDARY-01**, source-qualified NPC/quest/dialogue
coverage and missing original-server content. See CURRENT-STATE.


### Current user-review deliverable — 2026-10-16

The [Stage A consolidated review packet](docs/STAGE-A-CONSOLIDATED-REVIEW-R1.md)
is the current user-facing restoration overview, including nine system families,
seven representative player flows, five bounded blockers and source-qualified
skill/equipment/trade/riding specification entry points. The adjacent JSON
manifest pins sources and selective replay commands. Its publication is not
Stage A acceptance: seven families remain PARTIAL, two OPEN, Stage B GATED.
Highest next: STAGE-A-JOINT-REVIEW-01; an ordinary continuation stays in Stage A
and may pursue EARLY-CONTENT-RECOVERY-01 only as bounded, material source work.
R79 remains paused nonblocking; latest CURRENT-STATE governs.


### Latest Stage A decision and new StoneAge design handoff — 2026-10-17

The project owner delegated the previous A/B/C choice, and the assistant selected **B**:
accept the **evidence-limited Stage A historical research review checkpoint**, with
all seven PARTIAL and two OPEN system-family historical statuses preserved.
This does **not** certify a fully restored original game, early commercial
server world, complete original quest/persistence, or a percentage of
historical completion. A future authenticated new early source can reopen
the specific evidence contract without erasing earlier results.

Current controlling decision: [bounded Stage A acceptance](docs/STAGE-A-EVIDENCE-LIMITED-ACCEPTANCE-R1.md).
Next collaborative input: [Stage B design discussion brief](docs/STAGE-B-COLLABORATIVE-DESIGN-BRIEF-R1.md).
**Design discussion is ready; production, final engine lock-in and new content
implementation have not started.** Latest CURRENT-STATE and independent CI
have authority over older README/NEXT markers.

 
### Current research priority — 2026-10-18 (source-ready 22-domain restoration)

The latest repository [22-domain source-ready review](docs/STONEAGE-22-DOMAIN-SOURCE-READY-REVIEW-R2.md)
preserves all historic PARTIAL/OPEN boundaries. A new *original Taiwan v1.0*
SPR-frame-to-bitmap category intersection report has been independently
executed and archived with source ZIP/JSON checksums:
`research/recovered/STONEAGE-TW10-VISUAL-CATEGORY-SPR-JOIN-R1.json`.
It validates only numeric original resource links, **not actual pet species,
avatar identities, first-generation quests or live drawing**. Previous early
server/pet identity work remains evidence-limited. Next finite source task:
`TW10-ITEM-STATIC-BITMAP-SOURCE-SELECTOR-01`. Stage B production and public
wiki implementation have not begun; R79 is paused and the full history in
CURRENT-STATE remains authoritative.

 
### Source-driven original item static resource checkpoint — 2026-10-18

The original Taiwan v1.0 `S:I` full item, `I` incremental item,
and `C` ground-item messages have pinned `graphic_id` field
positions. The player-labeled item bitmap range 5973–7003 contains
1,031 actual original ADRN records and 1,030 distinct source
block hashes (bitmap IDs 6042/6077 share a block hash). This is **not**
a historically verified original 1,031-item table or proven
`graphic_id -> bitmapno` draw path. Provenance and executable
checks are in
`docs/STONEAGE-TW10-ITEM-STATIC-BITMAP-SOURCE-R1.md`.
Next bounded T03 is `TW10-MAP-CONTENT-ORIGINAL-RESOURCE-BOUNDARY-01`.
Stage B production and wiki remain gated.

 
### Latest original map resource source checkpoint — 2026-10-18

The bounded T03 analysis cross-checks 9,286 original Taiwan-v1
ADRN collision-resource map numbers against unverified 2001 player image
categories: 4,571 small-tile, 1,271 large-object, 101 NPC-image
candidates, 3,343 other entries. **Resource map numbers are not floor
IDs or complete world-map payloads**. Original server-delivered
field-map DAT content, NPC/quest/spawn data remain unavailable.
See `docs/STONEAGE-TW10-MAP-CONTENT-COLLISION-R1.md` and the permanent
derived report. Next bounded source work is
`TW10-AUDIO-EVENT-SOURCE-GATE-01`; Stage B remains gated.

 
### Original TW1 runtime audio API callsite checkpoint — 2026-10-18

A bounded static callsite audit of the authenticated original `sa_3.exe`
adds 8 direct WinMM audio file API calls, a DirectSound import trampoline
and its single direct caller. The historical 114 indexed SFX, 116 loose SFX
and 11 BGM WAV entries were already recovered; this task does **not**
claim any original village BGM, pet/attack sound or actual gameplay trigger.
Original callsite evidence and checksums:
`docs/STONEAGE-TW10-AUDIO-EVENT-GATE-R1.md`.
NEXT: `PREPRODUCTION-CROSS-DOMAIN-MATERIAL-EVIDENCE-REVIEW-03`,
to prioritize meaningful original content restoration over endless API probes.


### Latest first-party gameplay and visual material — 2026-10-18

The [R3 cross-domain material review](docs/STONEAGE-CROSS-DOMAIN-MATERIAL-REVIEW-R3.md)
retains all22 historical domain statuses and shifts from resource-only probes
to actual first-party content. A newly acquired JSS April2001 introduction
states12 character types/48 appearances,5 carried pets and5-player parties.
Ten linked original160×120 JPEG thumbnails (June2001 captures) were individually
inspected; five other references remain unobtained after bounded redirects.
The already known official manual adds12 newly structured pet/battle/crafting
sections, not a newly discovered source. See the [source specification](docs/specs/STONEAGE-JSS2001-PET-INTERACTION-AND-VISUAL-R1.md).
These are JSS2001 descriptions/images, not certified Taiwan1.0 build identity.
NEXT: `JSS2001-OFFICIAL-EVENT-QUEST-CONTENT-01`, one finite original linked
event page for named quest/story content. Stage B and public wiki remain gated.


### Latest official event and venue source content — 2026-10-18

Three authenticated original JSS pages add two **social-event announcements**,
four hometown chatroom entrance coordinate descriptions, ticket/guide roles
and hall/wedding entrance directions. Six publisher-annotated JPEG crops were
retrieved and inspected; April2001 HTML and June/July2001 images remain separate.
See [official event and venue source specification](docs/specs/STONEAGE-JSS-OFFICIAL-EVENT-AND-VENUE-R1.md).
No NPC quest script, event year, actual prize award or Taiwan1.0 same-build map
identity is certified. Conflicting meeting times and commented-out registration
links are preserved. NEXT: `JSS-OFFICIAL-EVENT-RESULTS-PET-ATTRIBUTION-01`, one
linked official results page; Stage B and public wiki production remain gated.


### Latest official first-comedy result attribution — 2026-10-18

The official results index has16 event entries/14 detail links. One followed
first-comedy result reports four prize categories, including an ad-hoc individual
award, while still leaving the rare pet unnamed. This first edition cannot be
used as the second edition's result, even where prize amounts match. A mismatched
template banner, one corrected wrong-page prefetch, three404 image attempts
and three429 availability responses are preserved. No result image was acquired.
See [official result attribution](docs/specs/STONEAGE-JSS-EVENT-RESULTS-PET-ATTRIBUTION-R1.md).
NEXT: `JSS-FIRST-PARTY-PET-FAQ-01`, one authentic FAQ index and at most one
clearly pet-related detail page. Stage B and public wiki production remain gated.


### Official JSS FAQ evidence — 2026-10-18

Two original April2001 FAQ pages add nine operator-labelled fixed issues,
including boarded-pet skill loss and named event failures, plus twelve game
answers. Quest investigation, historical reinstall advice, duel-ranking refresh
and256-color window/palette behavior are kept separate from actual fix execution,
server scripts, species IDs and Taiwan-v1 build identity.
See [FAQ source specification](docs/specs/STONEAGE-JSS-FIRST-PARTY-PET-FAQ-R1.md).
NEXT: `JSS-FIRST-PARTY-PATCH-PET-QUEST-01`, a bounded authentic update-record source.
Stage B and public wiki production remain gated.


### Early JSS pet change history — 2026-10-18

One original operator update page preserves40 dated entries and seven selected
pet contracts: boarding availability/skill defects, separate pet-mail timer
contexts, and synthesis/cooking additions. Generic fixes are not exact FAQ
symptom matches. The2001 capture preserves operator-written1999–2000 history,
not launch/Taiwan-v1 build identity. See [dated pet changes](docs/specs/STONEAGE-JSS-PET-PATCH-HISTORY-R1.md).
NEXT: `PREPRODUCTION-CROSS-DOMAIN-MATERIAL-EVIDENCE-REVIEW-04`, a finite22-domain material review.
Stage B/wiki gated; R79 paused.


### Official-version reference library — user direction, 2026-10-18

Collect recoverable content, visual/model/animation references and gameplay
across all authenticated official versions and regional releases, including
features that the future new game may never adopt. Keep the early restoration
baseline and each later version's own provenance and differences. The existing
seven profile classes are not a complete official-release census.
See DD-027 and the current content-archive/roadmap additions for collection
fields and priorities. Selection for the new game remains a later joint decision.


### Official world/story source — 2026-10-18

A newly acquired Taiwan Wayi2005 introduction explicitly connects Nis, Eden,
undersea exploration and the lost world with nine version labels in five
source-ordered groups. The mechanical-ruins/new-civilization question remains
unanswered; version labels do not authenticate nine client builds. Eight
original illustration slices were recovered and inspected; one remains missing.
See [official world synopsis](docs/specs/STONEAGE-WAYI-OFFICIAL-WORLDLINE-R1.md)
and the22-domain material review R4. NEXT: `TW-WAYI-OFFICIAL-INTRO-DETAIL-01`,
one actual detail link, with its own heading/content verified before attribution.
