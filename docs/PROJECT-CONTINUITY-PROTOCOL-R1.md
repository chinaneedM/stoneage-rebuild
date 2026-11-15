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
