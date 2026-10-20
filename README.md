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


### 2026-10-18 — 官方冰世界详情：12个原地图名与六场景

按远端main `12d45f491ece5aa53a66b8ce17a64ddab7978cd6`、tree`1af86bcfd66c850024e7fd8e462ecd26667e2ad5`重新启动，核338分支、0开放PR、同HEAD9项main SUCCESS及连续性/完整CURRENT等七文件。TW-WAYI-OFFICIAL-INTRO-DETAIL-01沿真实第一出链，只取game01_01.asp正文及其六张原场景图；实际主题为瑞爾亞斯（冰世界），不从编号预设宠物/任务。

正文实际快照20050614003328，26346B SHA256`f7e10861dd9f8ee3bef19c46863c7bc818d17635ffecab41b0189c63ff2b234c`。取得官方12个新地图原名、冰雪/作物生长困难/居民叙事和“第十大莊園”序位；未恢复地图ID、路线、坐标、NPC/任务/遇敌表。六原JPEG全部220×163并逐张目视，实际快照2006-01-05，与2005正文分开记录；图注分别指冰顫通道、议会厅、24小时便利店、庄园专卖店、训练所和武器店，不能提升为真实交易/全天服务/已知NPC/原生分辨率。

正文“瑞爾亞斯”与三图注“薩爾亞斯”原样保留为UNRESOLVED_VARIANT_OR_TYPO_OR_DISTINCT_NAME，不静默纠错、确认别名或合并实体；骑乘外观仅HYPOTHESIS，无宠物种类或规则。精确客户端构建/首发日期及冰世界等于整个失落世界仍未证，不回填JSS1999/TW1.0。按现有19集合归档合同新增19个研究条目（地区描述1、原地图名12、场景6），不是19张地图，不新增npcs/pets/quests实体。原HTML/JPEG/程序不入Git。

永久派生与规格：`research/recovered/STONEAGE-WAYI-OFFICIAL-ICE-REGION-R1.json`、`STONEAGE-WAYI-OFFICIAL-ICE-REGION-CONTENT-CATALOG-R1.json`、`STONEAGE-WAYI-OFFICIAL-ICE-REGION-SOURCE-INTAKE-R1.json`及`docs/specs/STONEAGE-WAYI-OFFICIAL-ICE-REGION-R1.md`。本地19项边界测试通过；新增独立一正文/六图、两JSON逐字节重放工作流，远端结果与ZIP/raw/Git blob保管链须随后实际验收，未提前宣称。

**最高NEXT `TW-WAYI-OFFICIAL-INTRO-DETAIL-02`**：沿既验介绍页第二条真实未读game01_02.asp，最多一正文，先核题名/内容，形成一份具名宠物/人物/故事/环境或玩法合同即止；若重复、空或有限取源失败，记录具体结果并回全官方22域队列，不自动递归第三/四页。Stage A仍7 PARTIAL+2 OPEN，Stage B/百科GATED，R79暂停，无整体百分比。


### 2026-10-18 — 8.0 systems cross-version source bridge

The current research package qualified *source-described*, not runtime-verified, links among Taiwan Wayi 2005 systems, a dated 2005-06-08 Bahamut release report (with a 17173 derivative that is **not independent**), and an undated Mainland/Jinshan-labelled 17173 8.0 feature list. Pet gear, mentorship, quest log, and one Mainland portal named quest lead now have separate source/region identities. See [cross-version source contract](docs/specs/STONEAGE-80-SYSTEMS-CROSS-VERSION-EVIDENCE-R1.md). The authoritative next action is the latest CURRENT-STATE entry; original TW1.0 runtime, Stage B and R79 gates remain unchanged.


### 2026-10-18 — CN8 source-linked portrait quest content

One exact 17173 Mainland-labelled 8.0 quest index and named walkthrough have been independently byte-fingerprinted and converted into a bounded quest graph: 14 steps, two named NPC roles, five pet-to-pigment turn-ins and a portrait reward claim. The current page has no verified historical publication date, original-server script or TW1.0 build identity. A 2012 article about 8.5 reports a prerequisite and a different portrait count; both source scopes stay separate. See [CN80 quest specification](docs/specs/STONEAGE-CN80-PORTRAIT-QUEST-R1.md). The latest CURRENT-STATE governs the next finite evidence step.


### Current source archive checkpoint — 2026-10-18

The latest [Japanese operator character source](docs/specs/STONEAGE-JP2003-CHARACTER-VISUAL-SOURCE-R1.md)
records twelve unnamed web positions and their paired image references, with
one inspected illustration from a separate 2006 capture. These are source
positions, not authenticated client character IDs. The adjacent
[Wayi marine/social/crafting source](docs/specs/STONEAGE-WAYI-MARINE-SOCIAL-CRAFTING-R1.md)
adds version-bounded official descriptions. Use the final CURRENT-STATE entry
for the live queue; the dated notes below preserve earlier milestones.


### 2026-10-19 — Island history and a region-qualified hero quest source

The [island and hero guide source](docs/specs/STONEAGE-WAEI-CN20-ISLAND-HERO-CONTENT-R1.md)
adds five island descriptions, relative fictional history, and a three-actor
entry route with a birthplace exception. The Mainland official host explicitly
labels the hero island as open in Taiwan and not yet open in Mainland China;
these are documentary claims, not verified original-server execution. The
[six source relations](docs/specs/STONEAGE-WAEI-HERO-GUIDE-SOURCE-RELATIONS-R1.md)
compare the guide with accepted later flower/shell configuration while keeping
names, locators, item IDs and incomplete conditions separate. Both derived
reports and source/artifact custody receipts are retained in Git. Consult the
last CURRENT-STATE entry for the live queue.


### 2026-10-20 — Early riding and pet crafting source specifications

The [CN2.0 riding source](docs/specs/STONEAGE-CN20-RIDING-TRAINER-COMBAT-SOURCE-R1.md) records trainer flow and documentary combat attribute sources; the [4.0-labelled certificate/manor source](docs/specs/STONEAGE-CN40-RIDING-CERTIFICATE-MANOR-SOURCE-R1.md) keeps later certificate and nine-manor service relationships separate. The [early pet crafting source](docs/specs/STONEAGE-CN20-PET-CRAFTING-SOURCE-R1.md) adds processing operations, two skill-price labels and five ingredient categories, preserving advice, hearsay and missing formulas. Operator hosting does not certify guide authorship; later captured images do not prove same-build execution. Derived source replay and custody are retained in Git; original assets and full HTML are not. The final CURRENT-STATE entry remains the live queue authority.


### 2026-10-20 — CN2.0 creation and level-up documentary source

The [creation and status source](docs/specs/STONEAGE-CN20-CREATION-STATUS-SOURCE-R1.md) adds name/face/allocation/birthplace choices, four primary-to-status label relations, reported marginal changes and a three-point level-up claim. Initial creation pools remain unspecified in this body; Japanese initial points and a separate Mainland build recommendation stay separate. The linked picture is an outdoor scene, not an authenticated creation screen. Derived replay and custody survive in Git; unknown original formulas, IDs, authorship and runtime remain explicit. See the final CURRENT-STATE entry for the live queue.


### 2026-10-20 — Japanese pet evolution trial and qualified failure state

The [2008 evolution source](docs/specs/STONEAGE-JP2008-PET-EVOLUTION-SOURCE-R1.md) adds four eligible pet labels, masked evolved names, a named trial NPC and relative cave location, chance/retry/failure descriptions and separate paid guarantee/reroll items. A real official-page capture is dated2009; current concept images are not original runtime evidence. Unknown requirements, rates, initial numbers and untouched state fields remain explicit. Derived source replay and custody are retained in Git; original HTML/images are not. Consult the final CURRENT-STATE entry for the live queue.


### 2026-10-20 — Japanese cooperative events and conditional public rewards

The [2008 cooperation specification](docs/specs/STONEAGE-JP2008-COOPERATION-SOURCE-R1.md) records two item paths, four named narrative roles and eight contribution thresholds from one release quotation and four inspected reward tables. Collection and later reward dates remain separate; actual unlocks, counter population, exchange ratios and original IDs remain unknown. Five current JPEG references and derived CI custody are verified; historical assets stay outside Git. The final CURRENT-STATE entry governs the next material review.


### 2026-10-20 — Taiwan7.5 spirit summoning preview and original interaction references

The [operator preview specification](docs/specs/STONEAGE-TW75-SPIRIT-SUMMON-PREVIEW-SOURCE-R1.md) records messenger/hero player cooperation, token handoff and rewards described for both roles. Three original linked screen references add a named mission target and one bounded spear panel; remaining-time displays and account balance do not become universal quest limits or reward amounts. The index date, later body capture and earlier image captures remain separate. Derived replay and custody survive in Git; original assets do not. The final CURRENT-STATE entry governs the next material review.


### 2026-10-20 — Early Mainland battle commands and separate defeat descriptions

The [CN2.0 battle guide specification](docs/specs/STONEAGE-CN20-BATTLE-COMMANDS-DEFEAT-SOURCE-R1.md) records eight relative command positions, HELP participation, party consequences after escape and separate solo fainting, team continuation and overkill-return descriptions. The linked original picture is an outdoor riding scene and does not restore a battle menu. Unspecified probabilities, timing, original IDs and server execution remain open. Exact derived replay and custody are retained in Git; original HTML/assets stay outside Git. The final CURRENT-STATE entry governs the next material review.


### 2026-10-20 — Taiwan7.5 manor challenge plan and unresolved eligibility threshold

The [manor plan specification](docs/specs/STONEAGE-TW75-MANOR-CHALLENGE-PLAN-SOURCE-R1.md) records family momentum, challenger replacement, declaration timing and proposed stone distribution. Strict ninety-percent wording conflicts with an equality example; both remain unresolved. One menu image does not certify deployed rankings or transactions, and Mainland4.0 rank limits remain a separate regional source. Exact derived replay and custody survive in Git; original HTML/assets do not. Consult the final CURRENT-STATE entry for the next material review.


- R36 台湾2004法师属性修正计划：[来源规格](docs/specs/STONEAGE-TW2004-MAGE-ATTRIBUTE-PLAN-SOURCE-R1.md)及[永久派生保管](research/recovered/STONEAGE-TW2004-MAGE-ATTRIBUTE-PLAN-CUSTODY-R1.json)。双CI完整原JSON已验收；两火、相反转伤方向、未名新酒及2004大图/2015缩图分开，原服与部署未证。


- R37 日服2008虎追任务：[来源规格](docs/specs/STONEAGE-JP2008-TIGER-QUEST-SOURCE-R1.md)与[永久派生保管](research/recovered/STONEAGE-JP2008-TIGER-QUEST-CUSTODY-R1.json)。取得官方9月专页与六月发布文对照；十条内容记录、四媒体场景及六失图HTML声明分开。七章诗全文、物种主表、奖励与部署未证。


- R39：日本2009年Guild异地交流、ハクエン与白炎兑换、临时地图敌人及经验兑换来源已记录于 docs/specs/STONEAGE-JP2009-GUILD-HAKUEN-SOURCE-R1.md，真实双页面摘要与完整派生保管参见 research/recovered/STONEAGE-JP2009-GUILD-HAKUEN-CUSTODY-R1.json。不得把后期Guild倒填最初台湾/大陆家族；NEXT以CURRENT-STATE末条为准。
