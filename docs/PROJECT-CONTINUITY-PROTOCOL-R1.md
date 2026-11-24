# Project Continuity Protocol R1

## 1. Purpose

This protocol exists so the StoneAge project can continue across new conversations without relying on transient chat context.

The **GitHub remote repository state is the single source of truth** for project progress, research status, design decisions, and next actions.

Chat memory may help orientation, but it must never override the repository.

## 2. Startup procedure for every new conversation

When the user sends the restart message, the assistant must:

1. Identify the `stoneage-rebuild` repository owned by the user.
2. Read the latest remote default branch state.
3. Read, in this order:
   - `README.md`
   - `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md`
   - `docs/CURRENT-STATE.md`
   - `docs/DESIGN-DECISIONS.md`
   - `docs/HISTORICAL-TIMELINE.md`
   - `docs/SOURCE-REGISTRY.md`
4. Inspect recent commits to determine what changed most recently.
5. Resume from the highest-priority unfinished item in `docs/CURRENT-STATE.md` unless the user gives a new priority.
6. Do not ask the user to restate already-recorded project history.

## 3. Canonical restart message

> 继续《石器时代》项目。按仓库 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` 启动，以 GitHub 远端最新状态为唯一事实源。先读取连续性协议、`docs/CURRENT-STATE.md` 和最新提交，然后从最高优先级未完成事项继续推进。

A shorter equivalent is acceptable if it explicitly names the protocol and says the latest GitHub remote state is authoritative.

## 4. Evidence taxonomy

Every important claim must be tagged conceptually as one of:

- **FACT** — supported by evidence currently considered reliable enough to state as fact.
- **HYPOTHESIS** — plausible interpretation or inference that still requires confirmation.
- **DESIGN** — a decision for our rebuilt game; not a historical claim.
- **OPEN** — unresolved research question.

Do not silently promote HYPOTHESIS to FACT.

## 5. Source hierarchy

Prefer evidence in this order:

1. Contemporaneous official material: original client, manual, official site, patch notes, packaging.
2. Contemporaneous press and magazines.
3. Preserved binaries, source trees, data files, videos, screenshots with provenance.
4. First-party developer/staff recollections.
5. Later official retrospectives.
6. Contemporary player guides and archives.
7. Later player recollections / community reposts.

Conflicts must be recorded rather than flattened.

## 6. Documentation discipline

At meaningful milestones:

- Update `docs/CURRENT-STATE.md`.
- Add new historical claims and uncertainty to `docs/HISTORICAL-TIMELINE.md`.
- Add sources to `docs/SOURCE-REGISTRY.md`.
- Record irreversible/high-impact design choices in `docs/DESIGN-DECISIONS.md`.
- Commit with a message describing the milestone.

Before ending a long work session or when context limits are approaching, update `docs/CURRENT-STATE.md` so the next conversation can resume without reconstruction.

## 7. Development discipline

Historical reconstruction and modern game implementation are separate layers.

- Research material informs specifications.
- Specifications inform the modern implementation.
- Original technical debt is not inherited merely for historical fidelity.
- Historical assets are not automatically production assets.
- Later-version content may be adopted only through explicit design decisions and coherent world integration.

## 8. Repository safety

Do not place copyrighted proprietary binaries/assets into the repository by default. Store hashes, metadata, filenames, screenshots only where legally appropriate, and research notes instead.

Do not rewrite or delete historical evidence records to make a later theory look cleaner; supersede them with dated corrections.

## 9. Large continuity-file retrieval

An empty file-interface response does not establish that a repository file is
empty. Resolve the fresh remote HEAD, tree and path metadata before interpreting
an empty response. If metadata reports a nonzero size, retrieve the exact Git
blob SHA from that tree with the Git blob interface. A clean checkout fetched
from the same exact remote commit and `git show <commit>:<path>` is also a valid
fallback. Do not fall back to an earlier chat's file content or progress.

Before appending or publishing, validate that the retrieved text preserves the
existing file; compare the resulting remote tree with the locally verified tree.
Never publish a suffix-only replacement after an empty interface response.

Observed on 2026-10-07 at main0fa1e733dfd021a45de63150249c14af9e6fc436:
`docs/CURRENT-STATE.md` has1050607 bytes, blob
`a9377a2e1b2c080167fc1ab7af088cc497fbcf33`. The file-read interface returned
empty content for this nonempty file; the exact Git blob interface returns the
complete current-state text. All earlier continuity records remain preserved.


## 10. Ongoing project publication authorization — 2026-10-09 (Asia/Shanghai)

The user explicitly authorized publishing this turn's commits to
`chinaneedM/stoneage-rebuild`, running Actions, and writing back to main after
acceptance, then granted ongoing authorization for all similar work:

> 我授权将本轮提交推送到 chinaneedM/stoneage-rebuild，执行 Actions，验收通过后写回主线。 今后所有类似内容 全部授权给你

Within this project's established scope, research/development changes, tests,
workflows, derived evidence and continuity records may therefore be submitted
for remote validation and integrated after the relevant gates pass without
asking the user to repeat this authorization. Preserve bounded evidence status
and all unresolved historical/runtime distinctions. Use non-destructive ref
updates; inspect a freshly changed main before integration. This records the
user's project-specific instruction and does not grant authority over unrelated
repositories or unrelated external publication.


## 11. Autonomous work-unit duration — 2026-10-15

The user reaffirmed: “我们还是按照当初定好的 单次任务量最少15分钟为节点 你自己规划 要不然效率太慢”. Each continuation should therefore comprise at least15 minutes of effective sustained project work, planned autonomously. A small passing check is not a stopping point: combine adjacent authorized research, implementation, adversarial verification, independent acceptance and continuity/publication work into a useful unit. Brief progress updates do not end that unit. Do not inflate elapsed time through artificial waiting or unrelated work. Record the completed outcome and remaining highest-priority task; do not require repeated “继续” for each small subtask. Existing publication authorization and evidence boundaries remain in force.


## 12. Durable provenance before short-lived CI artifact expiry — 2026-10-15

For each material source-derived historical milestone, inspect whether the verified artifact is only retained temporarily by GitHub Actions. Where lawful and copyright-safe, permanently commit the **derived metadata/report only** after independent source SHA, artifact ZIP digest, raw JSON hash, negative evidence-boundary guards, and exact semantic replay. Keep original proprietary client binaries, save payloads, music, sprites and other assets out of Git by default. Preserve the original run ID, HEAD, job, artifact ID, ZIP digest, raw-content digest and derived Git blob SHA in a versioned acceptance receipt. If a derived report cannot legally be retained, record its provenance, unavailable status and precise missing evidence; never silently claim full coverage.

Treat the archived derived report and source-custody receipt as complementary. An expired CI artifact cannot automatically invalidate previously verified research when a matching immutable derived Git blob and full chain of custody survive, but source runtime execution, actual IO success or original server-only values remain unproven until separately demonstrated. Every continuation must verify the current remote HEAD/tree, any incomplete branches/Actions, and the full current-state historical prefix before resuming. Prior failed Actions and corrections remain historically visible and must never be rewritten as successful attempts.


## 13. Outcome-driven restoration planning — 2026-10-16

The user reaffirmed that the assistant owns overall restoration planning and
necessary-work judgments. After CURRENT-STATE, read
`docs/RESTORATION-ROADMAP-R2.md` and its current portfolio index. A previous
local NEXT does not outrank a newer portfolio-level supersession.

Before starting a work package, name the game behavior/content being restored,
its material evidence gap, expected deliverable, version/source scope and stop
condition. Expand a low-level dependency only when it changes that deliverable.
After at most two consecutive work units without a new domain specification,
content attribution or material integration result, stop expanding the branch
and reassess the whole-system queue. A family remaining OPEN is not a mandate
to exhaust every helper before another family can advance.

Preserve bounded unknowns and define precise reopening triggers. Never replace
missing original server content with invented facts. Tests, R numbers, decoded
nodes and elapsed time are verification/work measures, not overall restoration
completion. Existing15-minute effective-work and publication rules continue;
do not use repetition, irrelevant checks or artificial waiting to fill time.

Current supersession: PET-STATE-01 is highest. TW1.0 client-local savedata R79 is
PAUSED_NON_BLOCKING pending a named material game-rule/state dependency.
Historical R1–R78 and R79 preflight are retained, not revoked or called complete.


## 14. Dated additive work overlays when large CURRENT cannot be safely written — 2026-10-25

The complete CURRENT remains authoritative historical evidence. If the native-Git full blob (currently >2MB) can be verified but a GitHub file-write request fails due to transport or size, NEVER truncate, reconstruct from an old chat, or replace it with only a tail. Instead create an explicit versioned addendum under `docs/continuity/`, update README with a pointer, and include the exact source HEAD/tree, preserved prior CURRENT blob, work outcome, raw-source evidence limits, CI observations, and next package. Treat it as an **additive checkpoint**, never a substitute for retrieving CURRENT or for a newer portfolio-level supersession. Preserve failed and corrected CI history. At this writing, after reading CURRENT and the roadmap, also inspect `docs/continuity/NPC09-MATERIAL-DELTA-20261025.md` unless a newer remote record already supersedes its NEXT. A future full-CURRENT append may transcribe this checkpoint only after exact historical-prefix verification; retain the original overlay and failure record.

## 15. Simplicity-first execution rule — 2026-10-31

The user explicitly requires avoiding needless complexity across all project work. **Choose the simplest correct, maintainable path that produces the required real outcome.** Before adding a step, ask whether omitting it would materially harm correctness, provenance, acceptance, or delivery; if not, omit it. Reuse already verified sources, tools and implementations before creating new abstractions, helpers, reports, checks or workflows. Do not expand a bounded task after its acceptance criteria are met merely because more detail can be explored; move to the next material priority. Treat unnecessary duplication, speculative engineering and process-for-process's-sake as execution defects to correct, not as progress.

This rule does **not** weaken historical-source fidelity, deterministic correctness, copyright/security boundaries, mandatory verification or remote-publication safety. The minimum effective work-unit duration, where applicable, means progressing to adjacent valuable work, never padding a task with irrelevant work.

## 16. Historical restoration versus future new-game design — 2026-11-02

The user explicitly clarified the boundary: **current work is solely faithful restoration, historical attribution and observation of original StoneAge**. Do not optimize player experience, rebalance, streamline quests or progression, change difficulty, rewrite interaction rules, replace inefficient original mechanics, or treat proposed modernization as an original-game fact. Original flaws and inconvenient behavior are themselves historical subjects to preserve where evidenced. An unknown mechanism must remain OPEN, not filled with a convenient modern alternative.

Modern extraction utilities, offline resource observers and compatibility probes are **research instruments**, not gameplay improvements or proof that the original client was operated. Attribute every observed result to exact source version and evidence type; never substitute modern viewer interactions for the native game's actual behavior. Preserve user-facing original language and version divergence in research, without forcing Simplified Chinese onto historical source strings.

Modern experience optimization, new content, new engine and the default Simplified Chinese localization belong to a **separate future New StoneAge design/development phase**, requiring explicit transition after adequate restoration review. Research may record potential design questions only when clearly labeled DESIGN_FUTURE and not performed as current restoration work. Where older records ambiguously say "optimize experience" as a current-stage goal, this rule supersedes that interpretation. Keep the simplicity-first §15 rule: do not add needless mechanisms or paperwork.


## 17. Module-first, cross-version original-content restoration — 2026-11-02

The user proposed—and the project adopts—**finish the strongest evidence-supported breadth of one whole content module before rotating to another**, rather than interleave many isolated pet/map/NPC/quest microtasks across work units. This rule supersedes older queue instructions that rotate domains after every small bounded observation, but does not erase the 22-domain inventory, nine historical Stage A status families, individual evidence boundaries or earlier NEXT history. The current task priority becomes **PET-MODULE-01**; the earlier O96 generic world/NPC/quest rotation is deferred as a historical next candidate, not undertaken in parallel.

Read [the compact module work order](RESTORATION-MODULE-FIRST-20261102.md) at startup after the existing continuity sources. Restore by **category of game content**, not by a single arbitrary SPR number, one website or just one chronological release. Begin with pets across all provenance-qualified **already acquired and further legitimately recoverable** regional/version carriers, then player characters/NPCs, maps/scenes, items/equipment, permanent/event quests, gameplay mechanisms and final historical integration. Original resources are 2D bitmap/SPR animations where appropriate; do not invent a 3D model. Later-version material may appear in its own version-separated records but cannot be promoted to Taiwan 1.0/JSS1999 original facts.

Within the active module, favor **batch source-file extraction and catalog consolidation**: version-specific original source provenance -> deduplicated image/frame/action candidates -> actual private visual observation -> source-bound attributes/skills and functions -> cross-reference to other modules. Do not use group, bitmap, frame or numeric-ID counts as the number of pets; do not merge identities by coincident numbers or names. Shared capabilities (extractors, viewer, identity/dedup index) are reused across modules, not reimplemented per pet.

**A module may be source-bounded without falsely being historically complete.** A pet with only sprite or only server data is PARTIAL/UNKNOWN on missing fields; avoid endless waits for non-acquired official builds, missing same-deployment server masters or full historical population data. After exhausting the source-ready batch and recording a concrete remaining gap, move to the next module; reopen affected entries incrementally upon genuinely new evidence. Maintain original proprietary assets privately, publish only rights-safe derived indices and evidence. Per-module integration checks can be done when they reveal real original-game relations; final cross-module integration is still required and is not automatically a playable original game.

This is strictly **Stage A historical restoration**. No present redesign, rebalance, fictional content, enhanced original gameplay or premature Stage B. Follow §15 simplicity-first: this policy creates a work order, not a new reporting bureaucracy or extra mandatory tools.


## 18. Offline game-content priority over original MMO infrastructure — 2026-11-04

The user re-confirmed the restoration and eventual new game are **single-player/offline**. Historical account registration/login, GMSV-SAAC handshake, online gateway and multiplayer infrastructure are **not Stage A prerequisites**. This supersedes the immediately preceding network-first NEXT, but does not discard the earlier native runtime evidence or mislabel unresolved historical behavior as verified.

Use original client and server **files** for source-first restoration of pets, characters/NPCs, maps, quests, items and mechanics. Prefer existing offline private observers; add implementation only when it recovers material content. Native program experiments are allowed only where uniquely needed to close a specific historical gameplay-content gap, with a bounded stop condition. Never conflate modern offline synthetic movement/graphics with native game execution or assert a later community archive was an early official deployment. Proprietary original assets stay private.

This is Stage A research; future offline-game engineering, engine choice, local saves and experience optimization remain deferred. Preserve Stage A 7 PARTIAL + 2 OPEN, Stage B/wiki GATED, R79 PAUSED_NON_BLOCKING and unknown overall percent. At every restart, read [the newest work priority and source-bound offline replay](continuity/STONEAGE-STAGE-A-OFFLINE-GAME-CONTENT-PRIORITY-20261104.md) after the module-first order. Its NEXT overrides the old original GMSV-SAAC handshake priority. Do not truncate or replace the multi-megabyte CURRENT history.

## 19. Locked module execution and actual completion gate — 2026-11-15

**User correction superseding subsequent rotating NEXTs:** The user again explicitly requires a whole-module restoration plan, beginning with **pets**, instead of repeatedly switching among isolated pet, NPC, item, map, quest, and sprite work units. Previous work after the 2026-11-02 module-first decision did not consistently follow that instruction. From now on, **PET is the single active content module**. Existing work in other modules is preserved as evidence, not interpreted as permission to resume domain rotation. Later integration summaries and local `NEXT` notes do not unlock another module. In case of conflicting NEXT priorities, this section and the top ACTIVE MODULE LOCK in `docs/RESTORATION-MODULE-FIRST-20261102.md` take precedence until a dated explicit unlock/supersession is accepted.

**No reset of authentic work:** Reuse and audit PET-MODULE-01–15 and relevant later source-qualified pet artifacts, without counting existing source discoveries as new. A pet source record must separate version/carrier and distinguish species or identity claims from bitmap/SPR/animation groups, template rows, instance rows, abilities, skill effects, capture and native gameplay. Reconstruct original 2D pixels and actions where available, not fictitious 3D meshes. Private original commercial art/data remain outside public Git.

**PET closure checklist:**
1. Source provenance inventory for all currently available authenticated and candidate pet-bearing carriers, with file-level SHA/CRC and readable/unreadable bounds.
2. Single searchable source-separated pet catalogue, preserving unique source identifiers, names/aliases, candidate species and version conflicts (unknown identities stay UNKNOWN), original stats/growth data and all missing fields.
3. Actual pixel and SPR animation/frame/direction catalogue, with replayable private visual observations; strictly distinguish physical source coverage, partial RLE exceptions and verified original in-game appearance.
4. Skill IDs/text/source definitions and native effects/learning rules where legitimately proved, otherwise OPEN; trace capture/encounter, gifts, breeding/evolution, growth, riding and other pet behaviors to exact source evidence where it exists.
5. A pet-only acceptance matrix per evidence dimension (`VERIFIED_SOURCE`, `CROSS_CARRIER_CANDIDATE`, `MISSING_SOURCE`, `UNVERIFIED_RUNTIME`), concrete residuals, exact reopening triggers, stable private source references and rights-safe public receipts.
6. Meaningful final pet-module review confirming that every **presently obtainable, provenance-qualified source batch** was either processed or explicitly marked inaccessible with a demonstrated blocker. This is `SOURCE_BOUNDED_CLOSED` only for the declared materials, **not `HISTORICALLY_COMPLETE` or `NATIVE_RUNTIME_VERIFIED`**.

**Change-of-module gate:** Do not switch merely because a smaller pet task is finished, an interesting NPC/quest/map is found, or a source is temporarily missing. Access other modules only as narrow pet dependencies, reporting their evidence under the pet workstream. Before moving to Character/NPC, issue the completed pet catalogue, an explicit field-by-field coverage and unresolved-source matrix, a final evidence-qualified review and clear remaining blockers; otherwise PET remains ACTIVE. If unrecoverable original official sources prevent absolute historical completion, state the limit and seek a deliberate user decision on accepting a **source-bounded stop** before the next module; do not silently declare success or switch.

**After all content modules:** Perform cross-module source-qualified relation checks, then separately assess a new offline playable implementation (renderer/asset license strategy, state systems, combat, input, save/load, UI/audio, full playthrough integration). Complete original-content catalogues do not by themselves execute an original client or constitute a rebuilt playable game. Preserve Stage A 7 PARTIAL + 2 OPEN, Stage B/wiki GATED, R79 PAUSED_NON_BLOCKING, overall percent UNKNOWN, and the historical CURRENT Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` without rewriting it.

**Immediate NEXT: PET-MODULE-16 CONSOLIDATED CATALOGUE GAP AUDIT**, then continue batches within pets until the gate above is met. No unrelated INTEGRATION-style one-off content jobs.


## 20. Official-only global pet roster scope — 2026-11-15 (user supersession)

The user clarified that the **historical pet restoration target is every pet actually released in officially operated StoneAge versions across all regions and later versions**, not only the 1999/JSS or Taiwan 1.0 client, and not private-server-exclusive pets. Mainland China, Taiwan, Japan, Korea and other documented official operator/region releases are all in scope. Zodiac/year-event pets, commercial/limited pets, later fusion/evolution pets and other official additions are first-class priorities. If officially licensed later StoneAge franchise titles are researched, maintain a separate **product-line namespace** rather than claiming they belong to the original PC version or shared historical server.

**This section supersedes prior PET prioritization and roster inclusion interpretations** in §§17–19 and the roadmap, while preserving §19's **PET single active module lock and completion gate**. Taiwan 1.0 is a valuable authentic graphical/technical baseline, not the population boundary or the default identity/naming authority for later regions. The historical scope is not capped at 1.0, and a private server's additions must never be counted as officially released pets.

**Official-release gate:** An original operator page listing, artwork, a press preview, a client resource or an unofficial fan guide is not by itself proof that a pet was actually obtainable/used in an official live version. Separate `OFFICIAL_IN_GAME_RELEASE_CONFIRMED`, `OFFICIAL_ANNOUNCED_OR_WEB_LISTED_RELEASE_UNVERIFIED`, `UNOFFICIAL_RESEARCH_LEAD_ONLY`, `PRIVATE_SERVER_ONLY_EXCLUDED` and `DESIGN_FUTURE`. Require a qualified source-specific official live release/update/event/reward record or authentic same-version gameplay/identity evidence before counting a released pet. Unknown names, dates, exact versions and release mechanism remain UNKNOWN. Keep species, variant, palette/skin, evolution/fusion output, item/egg, source graphic IDs and source web positions separate; do not sum numeric sprite groups or cross-region records into species totals.

**Historical evidence preservation:** Prior community-preserved server material, mixed25 tables and old pet SPR investigations remain preserved as archival technical evidence. They may lead to an independent official source but do not enter the new official release roster by assertion, shared name or matching ID. Use the source-qualified `docs/STONEAGE-PET-OFFICIAL-GLOBAL-INCLUSION-R1.md` and `research/recovered/STONEAGE-PET-OFFICIAL-GLOBAL-RELEASE-EVIDENCE-R1.json` as the official-only working entrypoints; PET16 stays a **legacy technical/source index**, not the pet population. The previously confirmed operator website 124 JP +104 CN positions are source **candidates**, not proof of 228 released species. Future user-designed original pets belong in a separate later new-game design namespace and do not alter the historical catalogue.

**Priority override:** `PET-OFFICIAL-01 GLOBAL OFFICIAL RELEASE ROSTER / VERSION CENSUS` now outranks additional TW1 anonymous SPR-only expansion, repeated archive image network retries and PET23's earlier local next. Begin by locating actually released official pets and their version, operator, regional names, official art, acquisition, stats, animation, skills and original gameplay evidence, with year/zodiac, commercial and fusion branches explicitly in scope. Maintain PET-only module focus, preserve `docs/CURRENT-STATE.md` original Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`, Stage A 7 PARTIAL+2 OPEN, Stage B/wiki GATED, R79 PAUSED_NON_BLOCKING and unknown overall completion percent.


## 21. Year-and-version-first global official pet restoration order — 2026-11-15 (newest user instruction)

**Latest user priority supersession:** Instead of pursuing interesting official pets in opportunistic order, restore the PET module **strictly from the earliest historical operating years forward to the latest**, by year and release/version, maintaining **separate parallel official region/operator/product-line timelines** (Taiwan, mainland China, Japan, Korea and any qualified others). The user should not be asked to remember all official pets, and PET26's immediate JP-2008/2009 roster NEXT is now subordinate to the earlier-year review frontier. Existing researched later records are not deleted: place them into their historical year slots, then return to the **earliest unreviewed year/version**. Newly recovered early items are appended forward-only to their correct historic date; never rewrite old historical ledgers or confuse *date of discovery* with *original release year*.

The initial research window starts **provisionally in 1999**, not as a verified claim about the very first worldwide StoneAge launch; check primary historical operator evidence and extend earlier if necessary. For every year, enumerate independently the officially operated game releases/patches per country (original PC and later licensed product lines independently), official live pet roster, ordinary/commercial/event/zodiac/fusion/evolution pets, aliases and species-versus-forms, authentic art/SPR/animation, stats/skills, obtaining conditions and gaps. Do not jump to a newer year merely because its source is easier or its pet is popular. Finish a **source-bounded audit** of a year/region, listing unresolved and inaccessible sources, before advancing the frontier; this does not require proving false full historical completeness, and every earlier year remains reopenable when genuinely new source evidence arrives.

The working human-readable order is `docs/STONEAGE-PET-CHRONOLOGICAL-RESTORATION-ORDER-R1.md`; the immutable-date and yearly coverage cursor is `research/recovered/STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json`. Existing PET25/PET26 release events with an uncertain actual first appearance are placed by **earliest qualified source attestation year**, and are visibly marked as *attestation chronology*, not the first release. A year with no currently documented release record must be **NOT_YEAR_AUDITED**, never interpreted as zero pets or a closed roster. Historical version chronology from later retrospectives is a candidate, not original operator patch-level proof; conflicting release dates and independently operated regional versions must stay split. All previous official-only (§20), PET-only (§19), private art, future original design and unchanged full `docs/CURRENT-STATE.md` blob rules continue to apply. Stage A 7 PARTIAL + 2 OPEN; B/wiki GATED; R79 paused; completion percent UNKNOWN.

**Highest immediate NEXT:** `PET-OFFICIAL-CHRONOLOGY-01: PRE-2000/2000 ROOT OFFICIAL PC YEAR-VERSION AND PET SOURCE AUDIT`, followed by 2001, 2002 and the succeeding years in order, documenting precise evidence and deferring unproven release claims.

## 22. Project-wide two-axis historical content restoration constitution — 2026-11-15

**Latest user-approved underlying reconstruction logic, binding across ALL future conversations and content modules:** Combine **one locked active content module at a time** with **one global oldest-to-newest official release timeline** separated into independently attested territory/operator/product/version lanes. PET remains ACTIVE until its §19 terminal source-bounded review and explicit user approval of switching modules. Once a new module is intentionally unlocked, **restart the new module at the earliest relevant official year/version**, referencing (not duplicating or inventing) the previously established shared chronological/version/source index; the calendar frontier of PET does not become the starting year of NPC or MAP. This is a long-term implementation invariant for NPC/characters, world/maps, items, quests/story, mechanics, final cross-module integration, future archival guides and later separate offline game design. It supersedes old intermittent rotation instructions or NEXT lines that ask to jump to whatever unrelated content is easiest. Never reinterpret an early-stage cataloguing checkpoint as user permission to change the active module.

**Two histories, not one invented storyline:** Preserve separate **real-world product/operator release history** (patches, official live pet/content, limited merchandise, region availability and dates) and **source-backed in-game lore/world chronology** (NPCs, cultures, villages, maps, task dialogue, mythology). Also keep development/marketing *design intent* and future original new-game *DESIGN_FUTURE* separate. Chronological coincidence between a real-world patch and a fictional legend is not evidence of a causal link; use version-qualified original texts/mechanics and explicit cross-module relation evidence, or leave UNKNOWN. The history of the game world may be reconstructed incrementally, never filled with invented canon to make a pleasing continuous narrative.

**Common join key / data discipline:** Identify the official `product_line_id`, region, operator, server/service period, exact version/build when known, effective date or interval (with distinct planned/published/actual/live/in-world date types), module, original source object key, stable evidence source locator/SHA and status. Source-bound species/skin/SPR/ID, NPC, map, object, quest and mechanic identities remain independent until proved to be the same in a compatible version. Unconfirmed release, private-server-only content, source gaps and runtime gaps are not historical facts; no blanket later-client promotion to 1999/TW1.0. A year with no documented records remains `NOT_YEAR_AUDITED` rather than 0 pets or "complete". When new old-year evidence arrives, forward-append that finding to its true or bounded attestation year, without rewriting earlier work.

**Mandatory startup order and conflict resolution:** On every continuation, verify fresh remote main/ref/HEAD/tree/commit/open PR/exact Actions; read this protocol, the shared [two-axis constitution](STONEAGE-GLOBAL-TWO-AXIS-RESTORATION-CONSTITUTION-R1.md), the [machine-checkable governance](../research/recovered/STONEAGE-RESTORATION-TWO-AXIS-GOVERNANCE-R1.json), the [module-first order](RESTORATION-MODULE-FIRST-20261102.md), the active [pet historical year order](STONEAGE-PET-CHRONOLOGICAL-RESTORATION-ORDER-R1.md) and its PET27 cursor, plus the complete original current-state blob. The precedence is **latest explicit user instruction → this protocol §§19–22 + current module lock and chronological cursor → latest source-qualified active-module plan → old milestone reports/README/CURRENT historical NEXT → chat memory**. If a later user explicitly changes the policy, append a dated supersession to this protocol; do not silently replace the old instructions. New conversations must not require the user to remember the pet roster or repeat settled methodology.

**Current NEXT remains unchanged:** `PET-OFFICIAL-CHRONOLOGY-01`, cautiously investigating actual earliest classic operator/pet evidence around 1999–2000. This policy update itself does not close any year, prove any pet, advance the frontier, restart a different content module, open Stage B or validate original native runtime. Preserve full `docs/CURRENT-STATE.md` Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`, Stage A 7 PARTIAL + 2 OPEN, Stage B/wiki GATED, R79 PAUSED_NON_BLOCKING, unknown overall percent, and private commercial resources.


**Explicit stable startup path manifest (§22; forward-additive, immutable-prefix-compatible):** On new conversations, after fresh main verification and the old §2 sequence, additionally read  `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md`, `docs/STONEAGE-GLOBAL-TWO-AXIS-RESTORATION-CONSTITUTION-R1.md`, `docs/DESIGN-DECISIONS.md`, `docs/RESTORATION-MODULE-FIRST-20261102.md`, `docs/STONEAGE-PET-CHRONOLOGICAL-RESTORATION-ORDER-R1.md`, `research/recovered/STONEAGE-RESTORATION-TWO-AXIS-GOVERNANCE-R1.json`, `docs/CURRENT-STATE.md`; fetch `docs/CURRENT-STATE.md` by the exact Git blob SHA if standard file read is blank. Latest user policy and active PET year frontier override outdated historical NEXT entries. This appended manifest has the same force as §22 and changes no earlier protocol prefix.


## 23. Client-first official pet extraction; historical documents as targeted supplements — 2026-11-15

**User policy supersession:** The user explicitly identified that authentic clients for each official version provide a direct, more systematic starting point for restoring pet content than repeated broad media/news searches. **From this date PET source acquisition and analysis are CLIENT-FIRST** within the existing oldest-to-newest official year/region/version framework (§§19–22). This changes the *evidence acquisition priority*, **not** the official-release inclusion standard, active module or chronological frontier: PET remains the only ACTIVE module; year 1999 has SOURCE_BOUNDED_REVIEWED status only for its declared corpus and remains reopenable; current earliest unreviewed year is 2000. Do not jump directly to late client versions merely because they are on hand. Later and uncertain client resources may be indexed as future-year or unqualified leads, never relabeled as year-2000 official releases.

**Mandatory work sequence whenever a source-qualified client is available:** (1) inventory all already-held original clients and patches in original year/region/operator/version lanes; authenticate archive bytes, ZIP CRC, source/build metadata and file tree; (2) statically inspect client-local data, text/name tables, pet identity fields, sprite and bitmap IDs, animation sequences, skill/resource definitions actually present; (3) link name/ID/graphic/action on the SAME proven client build, record original locations/byte digests and null for absent fields; (4) diff independently authenticated builds and patches, with graphics presence not first live release date; (5) use period first-party news, manuals, official pet lists and historical press **only** to supply missing client/server-side/actual issuance facts, date and version conflicts, or to locate original clients that are genuinely missing. Stop repetitive broad searches of the same news/citation pages once source gaps are explicitly bounded; create a concrete missing-original trigger instead.

**Three evidence gates:** `CLIENT_ASSET_PRESENT` means original resource exists in a verified client; even an indexed SPR group is not necessarily a pet. `CLIENT_PET_IDENTITY_CANDIDATE` requires a source-qualified local or same-build identity/name↔graphic association but still does not prove live issuance. `OFFICIAL_IN_GAME_RELEASE_CONFIRMED` follows §19/PET official inclusion: original operator confirmed released/obtainable, or authenticated same-version native gameplay and availability evidence. Client may contain hidden/unused/future/foreign shared assets; server controlled capture tables, encounter rates, events, rewards, level growth, skills and actual service dates may remain unknown even with all client files. Keep `CLIENT_ASSET_PRESENT` and `OFFICIAL_IN_GAME_RELEASE_CONFIRMED` separately queryable; never convert sprite/graphic or PETFLG counts into world species totals. Community/private-server databases can help decode file formats but **cannot** be backdated or used as official pet lists.

**Already-held origin evidence:** TW Waei/JSS 1.0 retail original private archive had 372,626,292 B, SHA256 `3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24` and 379/379 verified member CRC in earlier accepted work; original PET/SPR/ADRN/REAL source-derived indexes are in repository. This is the **first client-first reinspection target** for the 2000 frontier. Previously certified bytes do not imply they are actually readable in the current conversation—verify custody/access before claiming a new extraction. CN5, TW8.5 and MIXED2.5 are different uncertain/community source grades; JSS1999 original client and KR2000 original client remain missing. See [PET38 audited source inventory](../research/recovered/STONEAGE-PET38-CLIENT-FIRST-AVAILABLE-SOURCE-INVENTORY-R1.json) and [execution addendum](continuity/STONEAGE-PET38-CLIENT-FIRST-RESTORATION-PRIORITY-20261115.md).

**Forward-only effect:** This §23 overrides any older NEXT that prioritizes repeated newspaper, forum, catalog or retrospective research over an accessible authentic client. It does not retract earlier PET28–37 source evidence; these are still valid for the original claims they support. No original proprietary CD, EXE, SPR/REAL or full commercial source data are committed publicly. The historical `docs/CURRENT-STATE.md` Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` (2,709,173 bytes) remains byte-identical; Stage A 7 PARTIAL + 2 OPEN, Stage B/wiki GATED, R79 PAUSED_NON_BLOCKING, overall completion UNKNOWN. At every new session verify HEAD/tree/Actions and native full blob before proceeding with this source-first queue.

## 24. Source-bounded later-client reverse backfill when early clients are missing — 2026-11-15

The user clarified that many old StoneAge client versions may be impossible to recover. Do not block substantive pet restoration indefinitely trying to locate every historical installer. Later source-qualified clients often preserve earlier graphics and can be exploited as reverse-backfill research carriers. This is a working acquisition heuristic, NOT a universal fact that newer clients include every older official pet.

Within the locked PET module and oldest-to-newest official year/version analysis:
1. Reuse already verified old original sources first. If a historic build remains unavailable after a source-bounded search, record the exact missing version, carrier, blocker and reopening trigger, then continue from already held later originals or provenance-labelled preserved candidates.
2. In each later carrier's own region/operator/version namespace, batch-index its local pet names or IDs, raw graphic references, SPR groups, bitmap/frame/action data and skills. Distinguish an authenticated official build from uncertain preserved copies and modern community builds.
3. Link a later-carrier entry to an older record through explicitly graded evidence: same numeric graphic, same name in actual original client tables, exact complete SPR-segment hash, and independently proven same-build pet identity. Exact matching art supports asset inheritance within the compared specimens, not same official server, original stat/growth/skills or historical first availability.
4. Use later assets to help restore missing early visual or animation candidates, but NEVER silently assign later names, species, server-controlled stats, release dates, gifts or capture behavior to an earlier official version. Real versions may delete, rename, modify, reserve or add pets; region/product lines may diverge. Community/private server records are format hints, not historical official-roster proof.
5. Keep CLIENT_RESOURCE_CANDIDATE, CROSS_VERSION_EXACT_SPR_MATCH, SAME_BUILD_NAMED_PET_CANDIDATE and OFFICIAL_IN_GAME_RELEASE_CONFIRMED as distinct searchable evidence grades. Only qualifying operator issuance or original same-deployment gameplay can establish official live release.
6. This source fallback does not skip chronology. The 2000 official year frontier remains OPEN; source-ready later client content may be catalogued with its own version/date key in parallel, awaiting old-year reconciliation. PET cannot switch to NPC until the existing PET completion gate and explicit user acceptance.

PET43 measured an exact bounded example: 124/124 authenticated TW1 local named graphic groups have corresponding numeric SPR groups in preserved CN5, TW85 and mixed25 indices. Full SPR segments are proven byte-identical for TW1-to-TW85 and CN50-to-TW85 for this 124-group cohort by earlier R28, whereas mixed25 is only a numeric group correspondence here. The latter preserved source carriers are NOT authenticated as pure official live builds, and no new old-era official pet issuance follows. See docs/continuity/STONEAGE-PET43-LATER-CLIENT-REVERSE-BACKFILL-20261115.md. This supersedes source-search repetition, not official-only, ownership, chronology or rights restrictions.


## 25. No paid marketplace client-carrier investigations; accessible source bytes first — 2026-11-16

**New explicit user instruction, higher priority than all previous NEXTs and source-acquisition suggestions:** The user has concluded that looking up collector/player-sold StoneAge optical discs, second-hand marketplace listings, pay-to-obtain client media, seller photos, physical disc prices, sale IDs and other material that cannot provide the concrete original client files is not useful for the restoration mission. **Stop searching, studying, comparing or reporting these paid/seller-only carrier leads as standalone work, and do not propose purchases, seller contact, marketplace monitoring, library supplement procurement or other payment-gated recovery.** This also supersedes the pending unmerged PET59 marketplace PR #470, deliberately closed without merging. Earlier historical reports PET58 and prior incidental shopping-market leads remain preserved as past evidence, not an instruction or priority to continue that direction.

**Acceptable PET acquisition path from this date:** (1) reuse and deepen already actually authenticated, legitimately held original client/patch content and its publicly saved derived name/graphic/action/hash indexes, subject to byte custody; (2) search only for **lawfully obtainable, directly accessible, non-paywalled and publicly readable original installer, patch, disc image or original resource bytes**, verify original distribution/version/CRC/SHA and provenance, and extract original pet files when available; (3) when an early original is unavailable, use already preserved later client sources as strictly graded graphical/name backfill under §24 and the existing version gates; (4) for remaining missing live issuance/date/server-side facts, use *free to access*, citable first-party historical product announcements, verified contemporary reports or authenticated gameplay sources, without mistaking them for an exact installer or actual live release. Period official press may remain a historical source even if the underlying physical client cannot be obtained, but do not search sale listings to create work units or a sense of acquisition progress.

**Stop rule:** If no publicly accessible client bytes are available after a bounded search, record exact version/region missing, public accessible source tested and blocking condition once, then continue 2001 chronological **official pet** source review or reusable existing-client actual extraction. Do not cycle through dead URLs or switch to pay-to-obtain collectors. A marketplace listing, printed ©2001 disc label or a seller's “tested” claim can never count as a new client, added official pet, independent original media build, original graphics or a PET milestone. User-supplied original bytes in the future may be analyzed after lawful custody/source verification; this is not a request for the user to purchase anything.

**Immediate current-state effect:** Main retains PET58 as latest merged source report; marketplace-focused PR #470 remains closed/unmerged. The active chronological frontier remains PET year **2001 / NOT_YEAR_AUDITED** with the next item **PET59 reset to FREE_ACCESS_OR_EXISTING_VERIFIED_CLIENT_BYTES_OR_OFFICIAL_LIVE_PET_SOURCE**. No new original client bytes or live pet proofs arise from this method correction. PET remains the only active module; no authority to switch modules, Stage A unchanged **7 PARTIAL + 2 OPEN**, Stage B/wiki GATED, R79 PAUSED_NON_BLOCKING, overall percent unknown. Do not rewrite or replace original `docs/CURRENT-STATE.md` blob `c89e0e33537990aa2132b47c40fef49a985a935c` (2,709,173 bytes). This section supersedes §§23–24 only as to **where to invest acquisition/search effort**, without changing source quality, official-only or chronology rules.

## 26. PC-only StoneAge historical restoration — 2026-11-19 (latest explicit user supersession)

**The user explicitly changed the research scope: "我们不用管手游相关的 这些内容全部删除掉 只关注PC端的". This supersedes §§19–25 and all earlier PET records solely regarding any inclusion or continued research of mobile games or mobile pet releases.** The sole research and reconstruction target is **official historical PC StoneAge**, prioritized for the original classic 2D PC client/operator/version lineage, across China/Taiwan/Japan/Korea and other source-qualified original PC regions. PET remains the only active content module; other modules still locked. Do not proactively research, collect, count, display, recommend, preserve as active catalogue, or use *any* mobile-only pet, mobile marketing, mobile characters, or mobile-game release data. User-facing summary and PC pet statistics must not include mobile product lines.

**PC is about the actual game build and release lineage, not merely the hardware capable of opening a login interface.** A mobile-first title with an emulator, browser portal or PC/mobile shared-account client (including later independent dual-end remakes) is *not* a classic StoneAge PC build. Do not promote mobile/dual-end content to the PC roster on the ground it can run on Windows. A separate officially distributed PC-native game is not implicitly part of the original classic 2D PC historical line; establish primary PC software/operator/build provenance and a deliberate scope qualification before inclusion. If uncertain, classify OUT_OF_SCOPE_PENDING_PC_LINEAGE rather than claiming original PC facts.

**Cleanup and continuity:** Remove out-of-scope mobile records from the *current working PC catalogue, PET25/PET27 active event lists, PC-year evidence reports, search/summary output, and future task queue*. Remove standalone mobile-only deliverables only when their dependency and legal/custody boundaries are understood; adjust tests to assert PC-only source eligibility. Historical commits and previously written milestone claims are not evidence that mobile remains within scope: prior records may stay reachable in Git commit history, but must not drive future work or visible PC totals. Do not history-rewrite old Git commits, mass-delete genuine original PC evidence in mixed reports, remove unrelated content, or overwrite the preserved complete `docs/CURRENT-STATE.md` Git blob. The latest protocol §26 and a PC-only machine-readable filter supersede old mobile-era milestone directions.

Continue oldest-to-newest year/region/version, source-first, no paid marketplace searches, no private-server-only pets, explicit source grades, and no invented completion percentage. All PET closure, Stage A 7 PARTIAL+2 OPEN, Stage B/wiki GATED and R79 paused gates continue unchanged. The active year frontier remains the latest *verified* PET queue cursor, not historical protocol text.

## 27. High-version-first PC resource extraction; backward comparison; oldest-to-newest history — 2026-11-23

**Latest explicit user correction, superseding the source-extraction order inferred from §§21 and 23:** Building a complete original PC content inventory from Taiwan 1.0 upward wrongly treats the earliest build as the identity gate for content introduced in later releases. **Source extraction and backwards compatibility comparison must instead start from the richest/later accessible PC build within each evidenced regional/operator lineage and work backward.** The independent, oldest-to-newest **historical release chronology** continues for date/edition reporting. Do not conflate these two orders.

1. **High → low source work:** From the latest/richest already accessible original or provenance-labelled preserved PC builds, batch-inventory each carrier's own native names, source IDs, graphics, SPR, action frames, and any same-build client/server stats, skills and acquisition data. Treat later-source candidates as independent entries; **no TW1 identity or portrait match is required for entry**. Reuse earlier authenticated source material for backward reconciliation, not as an admission test. Avoid costly inaccessible-client hunts when existing higher carrier bytes/derived source records can be used.
2. **Backward inheritance/variation, not a universal superset:** Within a documented original PC product/region/operator lineage, identify proven inherited images, additions, replacements, deletions, unused preloads, aliases and variants; preserve uncertain relations. Higher builds commonly accumulate content but need not contain all early assets, and a Taiwan 8.5 carrier cannot be assumed to contain every mainland 5.0 item just from its version number. Later images can fill *visual candidates* for old missing originals with explicit source attribution; never backdate them into the early client or claim same official server.
3. **No early match is not a failure:** Label a high-build entry without qualified earlier identity **NOT_LINKED_TO_EARLY_SOURCE**; do not call it an early-version missing pet, an officially released new species, or a proven first appearance. Client asset / native pet candidate / official live release / actual acquisition and attributes remain separate proof gates. Establish true first official date only through version-specific source or operator evidence.
4. **Historical timeline remains early → late:** After recording source-specific records, attribute only proven additions/changes to the independently attested official regional year/version ledger. Historical document review may proceed chronologically, but missing earlier original clients cannot prevent cataloguing already accessible later client contents. Preserve unknown debut and regional differences.
5. **Scope unchanged:** Original classic PC only; PET remains sole active module. No mobile-only content, private-server-only official claims, paid/seller-only media, copyrighted source binaries in public Git, or invented stats/skills/first release.

**PET-DETAIL37 source correction:** Preserved CN5 5.0 (not independently certified as an original operator pressing) has **305 local named album graphic candidates**: 120 with exact TW1 original portrait match, four with an early named identity but missing TW1 portrait and two later art candidates each, and **181 without qualified TW1 identity bridge**. Those 181 are **not a Taiwan 1.0 restoration deficit**. Start from their own later-build source records; independently seek same-build original pet identities, version changes and official live release. The complete CN5 ADRN collision rescan is only a conditional subtask when its original bytes are actually readable, never a gate blocking the broader later-version source inventory. 305 is not an official pet count.

This section explicitly supersedes older lower-to-higher *extraction* NEXTs, not previous evidence, the early-to-late historical presentation, or §§19–26 official-only/PC-only/closure rules. Existing original complete docs/CURRENT-STATE.md Git blob c89e0e33537990aa2132b47c40fef49a985a935c remains untouched. Stage A 7 PARTIAL + 2 OPEN; Stage B/wiki GATED; R79 PAUSED_NON_BLOCKING; overall completion UNKNOWN.

## 28. Compact restart and layered recovery — 2026-11-24 (user-authorized)

The repository remains the sole authoritative project state; a new chat, model upgrade or context cutoff does not alter it. The canonical short restart below is sufficient. This section supersedes earlier startup wording **only for loading/presentation of context and redundant retrieval**, not project goals, evidence standards, verification gates, source access/copyright rules, scope, approval requirements or publication safety.

1. Resolve the named repository and its configured work branch from fresh remote metadata; pin reads to newly discovered HEAD/tree. Inspect recent commits, relevant open PRs (base/head/unresolved state), and exact-HEAD Actions with pagination when needed. Distinguish queued/failed checks, unrelated workflow runs and accepted work; recover an incomplete publication before proceeding where material. Do not guess state from old chat.
2. Read this protocol, authoritative current-state sources and governing policies. Recover objective, invariants, active work, next deliverable, blockers and required gates. Large documents may be parsed/searched/verified in the tool layer, returning only material fields and sections. A truncated, empty or unavailable file read never proves empty content or successful full reading. Retrieve exact Git blobs or an exact-HEAD checkout if needed.
3. Resolve required paths against the live tree; read the latest substantive handoff and current evidence, tests and dependencies. Historical archives remain fully retained and searchable, but do not repeatedly inject all past reports into model context. Expand scope when contradictions, changes, omission risks, unknown dependencies or user requests warrant it. Required acceptance, source and risk checks remain mandatory.
4. Execute the highest material unfinished task directly; use compact status output. No repeated generic history summaries, extra parallel state databases, needless tooling or artificial task padding.
5. At each meaningful work-unit boundary, commit actual results, evidence references, corrections, remaining gaps and concrete NEXT using existing canonical files/continuation notes. Use an early durable checkpoint when useful; mark unfinished work honestly. Follow candidate validation and main-integration acceptance discipline. Don't depend on a final chat summary near context cutoff. Recheck remote branch before publishing, avoid destructive ref updates, verify remote result/CI. Do not imply uncommitted reasoning can be recovered from Git.

### StoneAge adaptation (precedence for archive retrieval and current NEXT only)

- Verify the preserved full historical `docs/CURRENT-STATE.md` by fresh tree metadata: the already accepted 2,709,173-byte immutable archival blob is `c89e0e33537990aa2132b47c40fef49a985a935c`. If the current blob and size match this accepted archive, its unchanged identity is enough for repeated restart integrity checking; do not transfer or render its entire contents again merely for orientation. This supersedes the full-text reread wording in §§2,12,14,22–25 and the restoration constitution solely for this unchanged archive. It does NOT permit overwriting, truncating or discarding any historical prefix. If the blob or size differs, retrieve exact native content, verify historical-prefix preservation and reconcile new history before relying on it. When specific historical evidence is needed, open the relevant exact archive sections. Do not call identity verification a fresh textual reread.
- Read the active governing policy in this protocol (especially §§26–27: classic PC only; high-version-first source extraction with independent oldest-to-newest historical reporting), the global two-axis constitution, machine governance, module order, current version/source queue, and the material design/source/history entries. Verify their live paths, use tool-side selective reads for large registries, expand when evidence completeness demands it. Keep prior priorities as historical records.
- The archived CURRENT tail is not the active cursor. Use the latest substantive continuation document in `docs/continuity/` tied to the newest accepted material work unit, together with its NEXT, recent commit changes, README continuation links and active PET queue/index; check for later superseding records. For a protocol-only commit, follow backward to the latest substantive work; never use README's last heading blindly if a later committed continuation exists. Read the exact latest material report and dependencies. If no unambiguous latest NEXT can be recovered, reconcile the competing evidence rather than guess or begin an unrelated module. Subsequent substantive commits must retain a clear NEXT and identify their continuation path in existing README/commit/continuation records. No new competing state file is required.
- Keep PET as sole active module until its established closure/approval gate; retain historical-only Stage A, Stage B/wiki GATED, R79 paused, and overall completion unknown unless legitimately superseded. No mobile, private-server-only official claims, paid/seller-only acquisition, proprietary asset publication or fabricated fields. High-to-low resource extraction is not a shortcut for chronology or official release proof.
- No game content, research outcome, test, progress percentage or active module is changed by this protocol-only update.

Canonical restart:

```text
继续《石器时代》项目：chinaneedM/stoneage-rebuild，main。按 docs/PROJECT-CONTINUITY-PROTOCOL-R1.md 的远端最新规范恢复并继续推进。
```
