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


- R40: Japan-2006 volcanic island, conditional volcano dungeon, wind valley and river-source rain forest now have a source-qualified geography crosswalk in docs/specs/STONEAGE-JP2006-WORLD-GEOGRAPHY-SOURCE-R1.md with derived CI custody in research/recovered/STONEAGE-JP2006-WORLD-GEOGRAPHY-CUSTODY-R1.json. This is documentary Japanese-version geography, not recovered Taiwan v1.0 maps or an implemented game. Consult the final CURRENT-STATE entry for NEXT41.


- R41：日本2007新手武器、装备附咒与商城入口的分层来源见 [规格](docs/specs/STONEAGE-JP2007-STARTER-CLUB-SOURCE-R1.md)。运营引文与媒体领取说明分别保留；隐藏属性、码输入UI及实服过程仍未知。NEXT以CURRENT-STATE末条为准。


- R42：日本2005三处特殊地图、未具名亲犬收集任务及2009地名对照见 [规格](docs/specs/STONEAGE-JP2005-SPECIAL-MAPS-SOURCE-R1.md)。古代遗址叙事、媒体入场说明/组队担忧分层，地图同名不推原ID相同；NEXT以CURRENT-STATE末条为准。


- R43：大陆2003“2.0”运营服务器分支的骑宠/交易/家族宣传、组别更名和新组收费范围见 [规格](docs/specs/STONEAGE-CN2003-CLASSIC20-BRANCH-SOURCE-R1.md)。不认证2001客户端构建；四庄园部分名单与既验九行表分源保留。NEXT以CURRENT-STATE末条为准。


- R44：日本2007レン/ワイト恋情与新居建材交换、全队巧克力及人物魅力香水见 [来源规格](docs/specs/STONEAGE-JP2007-REN-HOME-SOURCE-R1.md)。日期/星期矛盾原样保留，故事续接不当结婚已发生；NEXT以CURRENT-STATE末条为准。


- R45：胜思2011/2012摆摊入口、物品/宠物上架、待售标记和四张当前源链接图见 [规格](docs/specs/STONEAGE-CN2011-2012-STALL-SOURCE-R1.md)。宣传不当全地图/零税费规则，样本价与重复场景不认证主表或构建；NEXT以CURRENT-STATE末条为准。


- R46：独立作品SA2宠物AI培养、DEN、交配、寿命/转生/离家与普通E邮件的具名访谈见 [规格](docs/specs/STONEAGE-SA2-PET-CARE-INTERVIEW-SOURCE-R1.md)。2006年2月录制由同期后续报道定位，精确刊日未知；不回填SA初代规则，NEXT以CURRENT-STATE末条为准。


## 2026-10-21 R47 华义2.0(2)开服后四庄园与家族具名报告

新读main ac389193dbd71e5977975840601404e1fc022134 / tree d0a200343d5701c0e44af580096126b0ae32a060、435分支/0开放PR/4934项完整树无AGENTS、自身main9项全SUCCESS；旧queued37642417333保留。九启动全文与路线/22域索引固定，最高NEXT47进入有限的家族/庄园内容归属审查。

新浪2003-11-20 16:43明确转华义消息的后续报道当前33636B/GB18030，核心SHA d16ab4ca25e051f0c88916df49003cfc46d66c819864be53ae4ec2d457ca8aac；按原顺序：萨姆吉尔/圣战部落光/4524，玛丽娜丝/永远友情/2280，加加/龙族/4079，卡鲁它那/友情岁月/2811。报告11月19日“中午”开机，不推精确12:00/时区/构建。平均同时在线2000人以上、24小时内建族超过200均为运营方报告；“四家族人数超过90”范围不明，不拆每家族90。声望不是门槛，家族不是2026当前占领者。专属骑宠地位表述无名单/规则；挑战/PK为未来时；20日早晨繁忙临调恢复是运营方陈述，非独立执行/uptime/补偿见证。

实际正文一图当前19585B/300×225、SHA ad1f011da8a7c83187e856064e376d011b88114ddf1590136722afa9ecd03c40，原http/requested HTTPS分开，完整Pillow解码/目视；不标庄园家族/宠物ID、拍摄日期、原生分辨率或事件证明。正文外编辑相关链接实际指回R43预告，固定旧契约全文字节/原生Git blob；仅新文补玛丽娜丝/卡鲁它那和占领快照，旧文remaining_manor_names=null保持。09:00维护与“中午”事后报告不合成精确开服，WGS执行/九变四补丁/跨版本规则不证明。

8派生记录、中文规格 docs/specs/STONEAGE-CN2003-GROUP2-MANOR-REPORT-SOURCE-R1.md、真实取源工具/18实际源改写绕过digest门拒绝/外层script正例；独立正则HTML实体重建正文与顺序列表一致。初轮10本包/109相关测试零跳过。原HTML/版权JPEG不入Git；候选/main自身Actions和ZIP永久保管另据实追加。有限包止点一页一图一旧契约，不扩庄园/声望helper；重开需具名规则/原ID/实际过程或有日期原档。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-48回全22域另一具名材料，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部历史前缀保留。


## 2026-10-21 R48胜思高厨料理采购、宠物制作、交付与荣誉用途

新读main551e93eef582066eef6ffc8540adb41bd4ba2e09/tree6bbbd62a56ef8578284d35938359cc60c7b9798f、436分支/0开放PR/4927项完整树无AGENTS；R47保管提交自身候选10/main11项Actions全SUCCESS，完成前轮收尾核验。九启动全文/原生Git与22域索引重新固定。当前最高NEXT48，轮换生活技能/任务/经济，不扩庄园helper。

新浪2012-02-10 15:51胜思具名宣传https://games.sina.com.cn/o/n/2012-02-10/1551581681.shtml 当前146067B/GB18030，正文规范SHA f7a15a015e8791ed94221d43203f414b43714edff394fc1448bbeacc31111f11；两实际sa.cins.cn链接/自称胜思，未认证原始运营文件或2012原快照。五条版本化记录及规格docs/specs/STONEAGE-CN2012-COOKING-EVENT-SOURCE-R1.md：周一至日19—21点高厨料理，准备料理宠/村庄宠物店可学，向扑满乌力/黑乌力购买，制作两具名蔬菜色拉，交加加村24店大厨换奖励，荣誉值可换宠物/道具/装备。原文或者不改同时，配方/价格/坐标ID/奖励值/次数/时区/端点/首次上线未知。

宣传并列8.5魔域大冒险与2.5精灵王传说，活动适用组null，不推两组共有、不当2002原2.5或TW1/JSS1999；荣誉值不当石币或现金。两实际图115307/125689B、550×410/550×409完整Pillow解码/目视为人群宠物背景，不证料理或交付；第三壁纸只存链接、未取未验。原HTML/版权图不入Git。19真实正文语义改写绕过摘要门拒绝、外围script正例通过；独立核心/流程另核，候选/main自身取源与永久ZIP保管另据实追加。

止于一活动五记录双背景图；重开需同组具名配方奖励表/坐标ID/时区次数说明或原服过程。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-49回全22域另一材料，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，完整历史前缀保留，无分母不报恢复百分比。


## 2026-10-21 R49大陆6.0登录建角、新手村及透明伴随图边界

新读main51bec22420b3ebdef554a6ebaeee3904350002f9/treeaa3dbc5f746a4141b3187a508b0538db8d8cee5f，437分支/0开放PR/4937项完整树无AGENTS，R48保管提交自身main11项Actions全SUCCESS。九启动全文/原生Git与22域索引重读固定，最高NEXT49轮换登录建角，不扩料理/荣誉助手。

新取得新浪6.0新手流程https://games.sina.com.cn/zhqu/sta/liucheng.shtml 当前64286B/GB18030，显示新浪游戏2003-05-30 14:14、投稿入口及2006-10-09重生成注记。投稿入口不证明网友作者，亦未认证华义原版手册；注记不当原刊或拍摄日。所选进入/建角/新手村与图链接核心SHA7530ed367b3deb63486378be93773078bb4e484e5da84506789c496dd62af92e。另新浪2003-06-09 12:15运营口吻分服升级预告https://games.sina.com.cn/newgames/2003/06/06092201.shtml 当前33218B，去广告核心65c6c350d032f4e6d6be5099db28bfaaef09d4be7fcb781f89ffa7d7831723de；预告6月10日中国网通9先升、其他分期并需更新客户端/有新手村，不当实际执行、不替指南和图认证构建。

七条记录与规格docs/specs/STONEAGE-CN2003-ONBOARDING-SOURCE-R1.md：Deeplay/登录说明、插叙角色页、12人物各4配色、8个字符/面部可设、20点经验值原词、四具名出生宠/未名技能、新手村出至萨姆吉尔后不能再入等均保留来源层。字节/汉字数、独立4×4色、EXP或属性点真实语义、技能ID/首发、地图NPC坐标与执行未知；原文乌力乌力不擅改，速度体力建议不当最优公式。

实际十GIF中032/035/038/041/044为五张当前低分辨率画面；033/036/039/042/045各73B全透明，逐一完整Pillow解码alpha[0,0]，不算另外五张恢复画面。五画面目视，尺寸不当原生分辨率/确切构建；原HTML/版权图不进Git。20真实正文语义改写绕过摘要门拒绝、双外层script与重生成注记正例通过；独立核心/数值/有序图链另核。候选/main独立取源与实际ZIP永久保管另据实追加。

有限止点两源选定内容/十图对象；重开需同构建原手册或运行过程、姓名编码/20点规则/技能ID或传送证据。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-50回全22域另一具名材料，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，所有历史前缀完整，无分母不报整体完成百分比。


## 2026-10-21 R50日服2004聊天过滤、探索信息与NPC配置分期

新读main531f15f7f3831300a288e66b8883adfafbb3c9f0/tree8b749c1c0a13648759d36703700cf55cf9feef38，438分支/0开放PR/4947项完整树无AGENTS；R49保管提交自身main11项Actions全SUCCESS，九启动全文/原生Git与22域索引新读固定。最高NEXT50轮换社交交互，不扩R49建角/新手村助手。

4Gamer2004-07-30 23:12署名Kawamura同期报道https://www.4gamer.net/news/history/2004.07/20040730231235detail.html 当前10860B/CP932，正文核心SHA4ea1de1163cd989576c5fd90714eb43644b6a222416ceedad8fd0aa9ab5af506；不是逐字运营发布文或运行见证。HTML meta作者不当正文署名，五正文槽仅一实文四空模板，不认证2004原字节。六记录/规格docs/specs/STONEAGE-JP2004-CHAT-UPDATE-SOURCE-R1.md新增。

报道登记对象聊天过滤，不补UI/容量/频道/身份键/保存、封号或交易阻断；首次大更新仅指报道所称2004年6月正式服务以后，8月1日15—16时为维护计划。新未名岛、サイナス岛/ジャルガ岛各一未名洞窟、マーナ推测秘密均不补地名ID/入口/剧情Boss；部分NPC迁居带ようだ，非执行认证。8月3/6日任务NPC配置及约30分钟维护，与记者推测新任务届时触发分开；无任务条件/实际开放/精确时刻。新用户十日试用不当所有人永久免费。

实际三图按HTML顺序_0/_2/_1，31490/26016/24235B、200×133/170×141/170×141，完整Pillow解码/目视为地图示意、木桥与洞口场景，均无聊天过滤面板，不认证地图/人物身份或原生分辨率。原HTML/版权JPEG不进Git。20真实正文语义改写绕过摘要门拒绝，外层script与meta作者正例通过；独立核心/日程/推断词/图序另核。候选/main独立取源及实际ZIP永久保管另据实追加。

有限止点一报道六记录三图，不扩聊天实现/未名地图/任务助手；重开需同构建官方UI/手册、实际过滤过程、地图名入口或任务开放日志。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-51回全22域另一具名材料，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，历史前缀完整，不报无分母整体百分比。


## 2026-10-21 R51大陆2.0记录点贡品、原地登出与重入资料

新读main b1b12ebfacdb09580b812dd1fc5a498564145237/tree9f0ac6b72e66c5e8b00eb7cd4f1079c2819805da、439分支/0开放PR/4974项完整树无AGENTS，R50保管提交自身main11项Actions全SUCCESS。九启动全文/原生Git与22域索引重新固定；仅旧run37642417333仍queued，无in_progress，不抹去旧历史。最高NEXT51轮换记录点/位置重入，不扩聊天过滤助手。

从实际华义2.0导航取得基本操作、存储肉位置、公共设施：四精确档案20011204194619/20011204000349/20011204220248/20011204213609，HTML69317/68863/69407/73356B；不是首刊日、具体build或运行证据。运营站承载不认证具名作者/原手册逐字内容；正文“储存”指肉贡品换记录点，不当物品银行。三岛17表行加原地登出/交易YES/纪录点三行为，20记录及规格docs/specs/STONEAGE-CN20-RECORDPOINT-SOURCE-R1.md。

普通注销重入记录点、原地登出回登出地、被打飞回记录点，原地登出/原地注销标签分别保存，不推任何败北/掉线/跨重启；不是本地savedata.dat证明，不重开R79。对纪录点说话取在线人数，统计范围与刷新未知；贡品是否消耗/事务/保存载体未知。基本操作页交易只证接收方YES，不从2010或SA2指南补双OK。

17行北岛7/南岛8/吉鲁岛2，原地名、X/x、多坐标/多肉原样保留。加加/塔姆塔姆重复481，92与426，94、奇喀喀肉不详、191 365/342 466缺逗号均不校正；无地图NPC/物品ID，多坐标意义/多肉AND或OR不补。实际纪录点图片img/image011.jpg按本次正文捕获请求HTTP404，未取得图，不冒称画面恢复或所有档案无图；其余设施/操作图未递归。四HTML/原资产不入Git。

20真实源语义改写移除摘要门仍拒绝、外层script正例通过；独立正则实体表格与重入核心另核，候选/main自身取源与永久派生保管据实另记。有限止点一导航三页选段一失图请求；重开需同构建地图/NPC表、贡品日志/坐标对照或原服重入过程。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-52回全22域，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部历史前缀保留。


## 2026-10-21 R52大陆2.0三宠物网页外观补充与阿米朵旧对照

新读main47b593b715e25ecb55af2e9b080d92b7a247b182/tree16f697a355ccdf82a07dc4ed038e9688aa4b690f、440分支/0开放PR/4984完整树无AGENTS；R51保管提交自身main11项全SUCCESS。九启动全文/原生Git与22域索引重新固定，仅旧37642417333仍queued，无in_progress。最高NEXT52轮换宠物外观，不扩R51记录点/保存。

选材核对发现104格三页目录已验收，故不重做名录。固定首目录、有限目录和阿米朵视觉报告全文，重取既有20011204194619华义2.0正文69317B/SHA561950fd7bba41e7d39f4a781a671e11e175c7fe08dd1b5481fdf1fd23ba351b。本轮新增网页位置001/004/040三图片像素，007阿米朵仅旧对照；规格docs/specs/STONEAGE-CN20-PET-VISUAL-BATCH-SOURCE-R1.md，三研究记录不当原宠物实体。

001字面???→img/newpet/6.JPG，20011205050022/4196B；004字面??2→2.jpg，实际20011023194345/3785B且最终原主机无www；007阿米朵→7.JPG，20011205051046/4831B旧SHA一致；040呼波波→40.JPG，20011023183116/3520B。四JPEG全Pillow解码RGB83×90单文件帧并原像素目视：绿色四足、蓝圆形轮廓内浅色形象、既有黄褐阿米朵、蓝色直立形象。问号两名不补，呼波波来自源单元格；不推物种ID/技能/SPR/模型/动画。初次从正文档案跳各图，CI只精确取最终捕获，不重演初跳；主机差异不当全站等价。001/004有HTML83×90，007/040未声明，不回填。

旧104位置/98具名/6问号历史报告不变；补充后4引用已取、100未取，本轮新增3/旧对照1、新解名0、新原游戏实体0，不当物种总数或百分比。14实际HTML改写排除digest仍拒绝、4图真实字节反例与外围script正例；独立单元格/实体/路径大小写及JPEG SOF尺寸另核，候选/main实际取源和永久保管据实另记。

止于一既有正文/三新图一旧图/三父Git报告，不自动追100图或helper。重开需明确原名、同构建SPR/原动画/数值表。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-53回全22域，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部历史前缀完整；原HTML/JPEG不进Git。


## 2026-10-21 R53大陆2.0回复法术13行、正文目标与数值疑点

新读main7a6042d15f102e18cfb9eec01ef0f6e8e430639a/treeb88673c3d3ea14845fef48a55dda4558090ce344、441分支/0开放PR/4994完整树无AGENTS；R52保管提交自身main11项全SUCCESS。九启动全文/原生Git与22域索引重读，仅旧37642417333仍queued，无in_progress。最高NEXT53轮换战斗回复，不扩R52剩余100图。

既有华义导航真实“回复系”href取得新正文：20011204194619导航69317B，实际回复页20011204210425/67848B/严格GB18030/SHAaa159ec42c9faf663dd726b98d356e4fb56f6903d7a75270fb52c367518e4f80，核心d9e2a259142d981fdc2e4581979ba519b3a0b2f83daa11b8521786efa77c12cf。初请导航时间实际跳正文捕获，CI只取最终精确URL；无署名运营主机指南，不认证作者/首刊/精确build/原服。13等级行+1正文语境均带七字段，规格docs/specs/STONEAGE-CN20-HEALING-SPELLS-SOURCE-R1.md。

原rowspan4/4/3/2为治愈/滋润/恩惠/复活，费用依序5/8/11/14、8/12/16/20、20/30/40、20/35。滋润LV2原+10且耗12，低于LV1+50，疑点保留不补100；表LV不当人物要求/跨版最高等级，耐久力/气力不自动绑定HP/MP原字段。哈鲁仅玩家/表自身、芙蕾雅我方一人或一宠/表单体、提欧全员/表己方全体分层；正文神恩/表恩惠不改名。复活三名希鲁菲尔/雅鲁/哈恩不强配表两等级，也不推顺序升降。主要寄宿衣服铠甲防具不当仅限或全部；宠物昏厥复活建议的少量忠诚下降与经验不当零损/满返公式。

固定旧战斗派生全文/原生Git，CN20-BATTLE-02装备附魔只作定性对照，不重新取旧正文图、不认证同build或执行。18真实源语义改写排除digest仍拒绝/外围script正例；独立13行及疑点/费用/名字另核。内容无图，不抓导航chrome/其它法术页；原HTML/资产不入Git。候选/main自身取源及永久派生保管据实另记。

本地预检曾错误把旧source_reported对象当字符串，首轮10项1项错误/重放拒绝；修正实际meaning读取并建立有效基线。导航反例按真实font嵌套修正，不冒称那轮已通过；非来源变化或远端Actions失败。有限止点一导航一正文一父Git，不实现治疗或扩其它四系；重开需同版配置/ID、原文+10更正或战斗/气力/忠诚经验日志。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-54回全22域，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部历史前缀完整。


## Continuity note — 2026-10-25 NPC-09 evidence delta

The 2.66 MB historical `docs/CURRENT-STATE.md` is still preserved byte-for-byte. The latest post-PET-08 NPC-09 material-result, exact modern source qualification, corrected source-backed NPC-vs-warp counts, CI failure/correction history and bounded NPC-10 next action are documented in `docs/continuity/NPC09-MATERIAL-DELTA-20261025.md`. On every restart read the actual GitHub main HEAD/tree and entire CURRENT first; treat this dated delta as an additive record only, subordinate to any newer authoritative CURRENT/roadmap entry. Do not confuse later community bytes with JSS1999/TW1.0 source or original playable NPC/quest restoration.


## 2026-10-25 NPC-10载体补正

最新连续性见CURRENT/路线末条及[玄黄脚本保存包资格](docs/specs/STONEAGE-NPC-ORIGINAL-SCRIPT-CARRIER-QUALIFICATION-R1.md)：既有混合包确有三成员摘要，现代arg同长异SHA；官方build仍未知。NPC09覆层保留，现由此条接续NEXT：小型官方sa.exe实际登录/UI资源内容审查，禁止重复路径哈希或大包重拉。


- 2026-10-25：[官方小型程序实际资源目录](docs/specs/STONEAGE-WAYI-SAEXE-RESOURCE-CONTENT-R1.md)完成8条压缩/解压载荷资格对照；没有登录画面或标签，CURRENT末条NEXT为同SHA ClientLogin明确场景资源绑定12。NPC10主线12项Actions已实过，旧历史全保留。


- NPC10/UI11后验：[永久收据](research/recovered/STONEAGE-NPC10-UI11-PUBLICATION-R1.json)记录UI11候选11项与主线12项真实成功及源作业；内容主线3f697331。NEXT仍同SHA登录场景实际资源绑定12，未恢复登录画面。


- 2026-10-25：[原登录面板逻辑资源绑定12](docs/specs/STONEAGE-WAYI-LOGIN-SCENE-ALIAS-BINDING-R1.md)已将26301/2/3经真实查表语义联至官方patch物理376059/60/61与既验REAL摘要；640×480底图及双叠层仍为静态跨样本联接，未运行/渲染原画面。NEXT转已有全表的跨版逻辑别名目录13。


- 登录资源绑定12[发布收据](research/recovered/STONEAGE-WAYI-LOGIN-SCENE-ALIAS-BINDING-PUBLICATION-R1.json)：首候选12/补强11/主线13项Actions实过；下一目录包已有TW1/CN5折叠范围和官方patch全部出现计数预检，避免遗漏或将资源号混成实体ID。


- 2026-10-25：[跨版本逻辑别名目录13](docs/specs/STONEAGE-CROSSVERSION-LOGICAL-ALIAS-CATALOG-R1.md)接入43632引用/19236内容块，并以原属性块SHA补回旧快照折叠的588条关联，旧快照不改；可按逻辑号/物理号/内容SHA查询。NEXT转具体差异材料14，不把目录当实体主表或全官方版本完成。


- 别名目录13[实际验收收据](research/recovered/STONEAGE-CROSSVERSION-LOGICAL-ALIAS-CATALOG-PUBLICATION-R1.json)记录候选11/主线12项成功、源重放作业、三份永久数据摘要及588条恢复依据；直接接NEXT14的有限差异查询。


### 2026-10-25 — 五组原资源别名实际差异14

[五组材料报告](docs/specs/STONEAGE-ALIAS-MATERIAL-DIFFERENCES-R1.md)已将17来源位置/9个不同原RD块核到完整物理表：两个CN5-only别名无精确TW1/TW8.5原块对应，相同物理号已指向不同内容；另外三组保留旧块与多候选，未认证原服最终覆盖。没有以缺键推官方删除、以640×480猜登录图或以块SHA异直接证画面异。最高NEXT为有限原音频内容/索引差异15，先排除旧覆盖，不扩别名/WinMM helper；Stage A/生产边界及私人原大包保管暂停不变。最终CURRENT与实际发布收据为准。


五组差异14内容主线58523210已获候选11/main12项实际Actions成功；[不可变发布收据](research/recovered/STONEAGE-ALIAS-MATERIAL-DIFFERENCES-PUBLICATION-R1.json)保留全部运行/作业、来源链和报告blob。NEXT仍有限音频原内容15，不把验证通过当原游戏复原完成。


### 2026-10-25 — 原音频内容15与实际sound3三重重复

[原音频材料报告](docs/specs/STONEAGE-CROSSVERSION-AUDIO-CONTENT-R1.md)将114旧分段接入同字节后期载体，并实际有界读取soundaddr_3/sound_3：27表项、26不同WAV块，2.7MB容器是三份相同898978B段，81物理位置不作81新声音。独立源Action40188767159真实通过，原声音/原表正文不进Git；没有播放事件/物种绑定。NEXT转同版人物创建body基表与SPR实际关联16，停音频helper；完整CURRENT/路线末条与实际发布收据为准。


音频15内容主线30490180已获独立有界源验收、候选11/main12项实际成功；[永久发布收据](research/recovered/STONEAGE-CROSSVERSION-AUDIO-CONTENT-PUBLICATION-R1.json)保留全部源/离线作业及派生blob。下一包人物创建同版body表与SPR材料16；不把音频块数/测试数当整体复原率。


### 2026-10-25 — TW1.0原版人物创建数值材料16

本轮最高 `ORIGINAL-CHARACTER-CREATION-CONTENT-16` 的一项原始数值—同版SPR组号联接已通过来源及独立报告验收：原始程序 `sa_3.exe` 静态indexed body来源连续十二值 `100000..100220`（步长20），均在TW1.0原464组SPR表；紧随其后值198。**只有候选源表相交，没有原生表长/实际选角人数/人物姓名/原画面认证。** 详情见 [R16材质规格](docs/specs/STONEAGE-TW10-CHARACTER-CREATION-BODY-SOURCE-R16.md)、[永久原始派生数值](research/recovered/STONEAGE-TW10-CREATION-BODY-WINDOW-R16.json)、[日期连续性补记](docs/continuity/CHARACTER-CREATION-R16-MATERIAL-20261025.md)。未修改原巨大CURRENT正文，继续依其最新真实状态和路线优先级。下一有限目标返回22域同版官方具名内容原件轮换，Stage A7 PARTIAL+2 OPEN，B/wiki GATED，R79暂停，百分比未知。


### 2026-10-25 — 战斗场景SAB资源跨样本无损索引 R17

已按[原文件清单与完整SHA的交叉规格](docs/specs/STONEAGE-BATTLE-SAB-CROSSVERSION-R17.md)及[438出现位置机器档案](research/recovered/STONEAGE-BATTLE-SAB-CROSSVERSION-R17.json)直接比较早期台湾1.0的218个战斗SAB和混合2.5保存包220个SAB：共享0–217编号的文件内容SHA均不同，后期保存包另有218/219两编号，436不同块/438原参照（重复145/146各一对）不执行原件删除。2015二次转载的2001华义补丁文件名与现存包文件名不全相同，未认证原补丁或原服内容。历史全量CURRENT原样保留，[独立R17连续性记录](docs/continuity/BATTLE-SAB-R17-MATERIAL-20261025.md)说明下一优先源载体；Stage A、B/wiki、R79和总体百分比状态不变。


### 2026-10-25 — R18原文件主表全源守恒

本轮发现2.5混合保存包的旧筛选清单比实际服务器 `gmsv/data` **少选18个真实原文件（731424B）**，包括遇敌组合 `group.txt` / `group1.txt`、骑宠 `ride.txt`。已从旧静态ALL-FILE SHA256原清单补齐全部2245路径，核得10465523B、2121唯一内容SHA、53组/124个重复出现引用且0原件删除。来源只是旧社区混合包，不能证明任何TW1.0原服NPC/任务/宠物；没有重新下载商业载荷。参见[源保管规格](docs/specs/STONEAGE-MIXED25-SERVER-FULL-CONSERVATION-R18.md)、[2245路径原SHA机器档](research/recovered/STONEAGE-MIXED25-SERVER-FULL-SOURCE-R18.json)、[独立日期记录](docs/continuity/MIXED25-SERVER-R18-MATERIAL-20261025.md)。最高NEXT19回早期官方原件具名内容。原2.68MB CURRENT不变，Stage A7 PARTIAL/2 OPEN，B/wiki GATED、R79暂停、总体百分比未知。


### 2026-10-25 — TW1.0原程序短文本实物 R19

已通过真实源Action `40203596474` 对官方台湾1.0原版 `sa_3.exe` / `StoneAge.exe` 的尺寸及SHA逐一鉴真，并在非执行PE数据段检得带原文件偏移和原字节哈希的繁体短文本（例如“戰場地圖錯誤”“沒有參戰的寵物”“下載失敗”）；独立Guard核原清单及源文本的cp950回算。原始文本实例不是宠物/任务实体、不是原版界面实际显示证明。首跑大小上限失败、第二跑机器码乱码、第三跑校正成功均在[完整R19连续性记录](docs/continuity/TW10-ORIGINAL-TEXT-R19-MATERIAL-20261025.md)，[来源限定派生JSON](research/recovered/STONEAGE-TW10-ORIGINAL-EXE-TEXT-CANDIDATES-R19.json)。NEXT `EARLY-OFFICIAL-WORLD-ENTITY-SOURCE-20`：同版原商业NPC/宠物/本体任务名字-实体ID-原图SPR的真实来源联接。全文CURRENT原样保留；Stage A7 PARTIAL+2 OPEN，B/wiki GATED，R79暂停，总体进度比例未知。


### 2026-10-25 — 原版运行与直接观察实验台 P1 开始

用户明确决定将亲自看/听/操作原版游戏纳入复原关键路径，现已建立[原版观察实验台路线及否定证据门槛](docs/STONEAGE-ORIGINAL-OBSERVATION-LAB-R1.md)。初次交付为本机[只读ADRN/REAL原字节灰度PNG/音频源校验工具](tools/stoneage_original_observation_lab.py)＋[本地离线图/声查看页](tools/original-observation-viewer.html)与合成守卫，绝不把色彩索引灰度当原游戏真实颜色、动画/场景/角色身份、亲自运行体验；也不把原版权PNG/WAV发布到公开仓库。官方原版客户端真实启动及本地模拟服务器属于后续独立门槛；原内容NEXT `EARLY-OFFICIAL-WORLD-ENTITY-SOURCE-20` 仍单独推进。私人原件长期存储仍受限，Stage A7 PARTIAL/2 OPEN、B/wiki GATED、R79暂停、overall percent未知均未改变。


- 原版观察台P1[两张原台湾1.0 RD图像真实字节解码+单WAV原版结构](research/recovered/STONEAGE-TW10-ORIGINAL-OBSERVATION-P1-SOURCE-R1.json)已在源Actions `40206034214` verified success（原程序未执行）。bitmap5846/5847各输出只存在Actions暂存的**灰度索引PNG**，原图/声音/商业程序已清理；音频`sas_20.wav`实际原文件验证成功但未播放。来源、原SHA及既存R99逐块交叉验收见[日期连续性](docs/continuity/STONEAGE-ORIGINAL-OBSERVATION-P1-20261025.md)。仍未真实观看原色、登入游戏或复原具名实体，P2先恢复真正颜色和SPR时序，原R20具名内容任务与Stage A等边界不变。


### 2026-10-26 — 原SPR多帧私人观察 P2A

[本轮续接记录](docs/continuity/STONEAGE-ORIGINAL-ANIMATION-P2A-20261026.md)接原TW1 SPR组100000的三序列：25帧位置、16不同位图、原倒计时与偏移。真实原源Action40237734461已通过四原文件鉴真、16原RD解码及三份私人灰度动画导出；[原样永久源收据](research/recovered/STONEAGE-TW10-ANIMATION-OBSERVATION-P2A-ACTUAL-SOURCE-R1.json)只存派生指纹。可逐帧/循环查看的HTML由本地工具生成，原图不进公开Git。仍无原色、原帧率、人物/宠物身份或真实原游戏启动。观察NEXT是有限同版调色板资格P2B；内容R20、Stage A/B、R79等边界保留。CURRENT全文未覆盖。


### 2026-10-26 — 原初始化调色板与彩色动画 P2B

[本轮续接记录](docs/continuity/STONEAGE-ORIGINAL-PALETTE-P2B-20261026.md)通过原TW1路径指针表、原初始化指令限定执行和实际像素导出，恢复Palet_0的BGR读取、32保留色及168号强制黑规则；25帧位置/16位图已导出私人彩色动画。它是同版初始化色预览，尚未证明某地图/时间/战斗的实际选色，也未启动完整客户端。原源40241350181真实success、原样派生保管及独立guard见记录；原图/完整SAP/商业程序不入公开Git。最高观察NEXT转原客户端隔离启动环境与第一屏验证P3；R20内容缺口和Stage A/B/R79边界保持。


### 2026-10-26 — 原客户端真实启动与私人登录画面取证 P3

[本轮续接记录](docs/continuity/STONEAGE-ORIGINAL-BOOT-P3-20261026.md)已通过原TW1程序和375运行文件鉴真，在无外部接口/路由的Wine32环境真实启动。24bit的原256色提示、改为实际8bpp后无该提示及取消的初环境尝试均原样保留。最终源40244430667真实success；助手已目视经加密私人传回的原登录面板（JSS/石器时代、账号/密码、OK/QUIT），**当前色彩明显失真，未登录、未听音、未进入世界**。11个原样派生文件及[来源保管链](research/recovered/STONEAGE-TW10-ORIGINAL-BOOT-P3-CUSTODY-R1.json)永久入Git，原图/原程序/私钥不公开。最高观察NEXT为P3C登录色彩与有限输入验证；R20和Stage A/B/R79等边界不变，完整CURRENT原样保留。


### 2026-10-26 — 原登录窗口取色与输入边界 P3C

[三次真实对照记录](docs/continuity/STONEAGE-ORIGINAL-LOGIN-P3C-20261026.md)已用已知红绿块验证窗口colormap捕获，原登录图比旧桌面截图清楚，并实际观察到QUIT悬停高亮；**窗口模式仍只有15种RGB，短按及200ms按住均未退出，颜色/点击未通过**。原默认全屏路径在输入前即出现Wine错误/调试器，不认证QUIT；已增加异常窗口阻断输入的守卫。12份原样派生及[来源链](research/recovered/STONEAGE-TW10-ORIGINAL-LOGIN-P3C-CUSTODY-R1.json)保管三源run/job/ZIP/blob；原图仍私人保存。NEXT P3D先以合成Win32验证真实激活、palette和接收输入门槛，再决定原环境路线；不继续在同一失败环境盲目重拉原盘。未登录、未听音、未进入世界，完整CURRENT及R20/Stage A等边界保持。


### 2026-10-26 — 兼容环境实际颜色与输入资格 P3D

[本轮环境判定](docs/continuity/STONEAGE-SYNTHETIC-WIN32-P3D-20261026.md)实际比较自编x86程序的GDI/DirectDraw路径：Windows2022、Wine8、Wine24和来源固定的PrivateColorMap单项对照，共8条完整测量。目标程序均收到SendInput按下/释放及轮询状态；3条颜色通过、5条未通过。原生Windows正确显示但仍32bpp/ACP1252；Wine8仍量化，PrivateColorMap单项未改善，**尚无满足原客户端全部前提的环境**。8份原样派生、四ZIP和一次重启守卫失败均在[永久保管链](research/recovered/STONEAGE-P3D-SYNTHETIC-CUSTODY-R1.json)，本轮原件下载/执行均0。NEXT P3E限一次可用Windows8bit/CP950/隔离资格包，失败则明确环境阻塞并回22域R20材料，不继续Wine9参数树。P3C原画/点击、原声与世界仍未验收，历史CURRENT原样保留。


### 2026-10-26 — Windows资格P3E有界止点

[实测续接记录](docs/continuity/STONEAGE-WINDOWS-P3E-20261026.md)确认256COLOR及XP+256COLOR下，自编程序实际报告8bpp、正确RGB并收到输入；三组ACP仍1252，即使console已950。单自编exe路径防火墙四时点对照通过，但原程序/后代完整隔离未资格化。当前环境明确BLOCKED，原件下载/执行0；停止显示参数扩展，最高NEXT回R20同版原具名实体材料队列。原登录颜色/QUIT、原声与世界未验收；完整CURRENT/历史文件原样保留，Stage A/B/R79及百分比未知边界不变。


### 2026-10-26 — R20缺源止点与四图原资源材料R21

[续接记录](docs/continuity/STONEAGE-WORLD-MATERIAL-R20-R21-20261026.md)记录R20本轮没有取得新同版具名实体源；已停止重复字符串/端点扩展，转从2003历史小地图包实际读取四图。新增前两层数值—TW1/CN5/官方补丁原资源候选联接：4000第二层值4的133格在TW1无别名匹配，后期多内容候选不能任选；3000的三组同内容重复则保留来源。完整原样派生以无损XZ永久保管，无原地图网格/像素/程序公开。最高NEXT转单WAV私人真实试听资格22，不把数值匹配当同build渲染或具名NPC；P3E运行阻塞、Stage A/B/wiki/R79和百分比未知边界不变，CURRENT历史全文原样保留。


### 2026-10-26 — 单段原WAV私人可听交付R22

[本轮续接](docs/continuity/STONEAGE-PRIVATE-AUDIO-R22-20261026.md)已从有界CN5保存载体取原`saam_01.wav`（27180B/约1.23秒），加密私人传回、持久保存并独立完整回读相同；全部PCM经两解码器核对一致。当前模型音频输入实际返回不支持，因此助手未声称听到；用户实际播放、原游戏内播放及具体事件身份也未认证。明文音频/私钥不公开，旧报告未改成播放成功。最高NEXT转本阶段原实物与观察结果的22域增量材料复核23，再选实质内容包；P3E、R20及Stage A/B/wiki/R79等边界保持，CURRENT历史全文原样保留。


### 2026-10-26 — 22域材料增量复核R23、四样本整合R24与R17勘误

[最新续接](docs/continuity/STONEAGE-MATERIAL-R23-CLIENT-CONTENT-R24-20261026.md)按新远端全字节重读后复核22域四层证据，直接联接四份已取得样本3655条完整文件引用→2488内容，原路径全留，非全部官方版本认证。整合发现旧R17混用800字节payload和804字节完整哈希，明确撤回218同号均不同/436内容结论；当前工具及新报告纠正为218同号全相同、438引用219内容，旧原报告/历史原样保留。原世界未进入，彩色动画源端生成不等于持久交付、私人WAV不等于助手已听。最高NEXT转日服官方目录前12个尚未取得的具名宠物GIF材料25，不再连续做管理索引；Stage A/B/wiki/R79及身份边界保持。


### 2026-10-26 — 日服具名宠物图片材料R25：10实得、2连接失败

[本轮续接](docs/continuity/STONEAGE-JP-PET-VISUAL-R25-20261026.md)按新远端最高NEXT，从已有124网页位置扣除已取13引用后，单次尝试前12个剩余GIF，实际取得并目视10图，14/15连接拒绝未重试。原页名称、图像捕获年代（2003两图、2006八图）与来源分开；原样源报告和完整ZIP/run/job/Git保管链永久保存，原图/私钥/密文不入Git。现23引用有图、101未取，不是新增物种或原客户端动画身份。本地独立核PNG/RGBA，未收到原GIF，未宣称持久用户图片交付。最高NEXT转直接CN5原派生动画组100700/100701/100702的完整帧内容联接26，停止网页图批次；原世界、R20/P3E、Stage A/B/wiki/R79边界保持。


### 2026-10-26 — CN5三组完整原动画材料R26

[最新续接](docs/continuity/STONEAGE-CN5-ANIMATION-R26-20261026.md)直接联接已取得原CN5动画组100700/100701/100702，共312原动画、1464帧位置、936完整RD内容；三段SPR内存重编码SHA均匹配。三组共享48个位图、144位置均在原动作码12；完整TW1索引没有这936内容的相同size/SHA匹配。9源固定，独立SQLite完整源联接和14项验证保留重复帧、声音word与证据边界，不猜具名角色/动作/音效、不把duration叫FPS或声明原画面执行。原数据/大历史不改，无新大包下载或原二进制公开。最高NEXT按DD-029回已登记韩国NetmarbleStoneAge120的一份公开客户端载体27，来源/版本待资格，不扩动画/helper或网页图批次；Stage A/B/wiki/R79、R20/P3E及百分比未知保持。


### 2026-10-26 — 韩国Netmarble120原源R27：权限阻塞，未取得新客户端

[最新续接](docs/continuity/STONEAGE-KR-NETMARBLE120-R27-20261026.md)对已登记thread2117作一次真实公开读取，原标题可见但页面显示“您無權進行當前操作”，正文/下载链接未取得。原样报告、HTTP指纹、run/job/ZIP/raw/Git链永久保存；新增客户端/包字节/抽取文件均0，检查工作流成功不等于客户端下载成功，不猜韩国1.74或120版本含义，也不证明包不存在。未登录/回复/购买积分，不重复权限探测。最高NEXT回声称台版8.5已固定SPR137两原件的完整动画材料28，复用现有取源路径，不新增空样本、不把保存包认证官方；原世界/身份及Stage A/B/wiki/R79边界保持。


### 2026-10-26 — 台湾8.5保存样本SPR137完整原动画材料 R28

依据本轮重新读取的远端最高NEXT，从六分卷保存载体实际取得原`spradrn_137.bin`和`spr_137.bin`并严格验证原哈希；全量解出**1,739个动画组、113,737动画和735,666帧**，保留4,759 sentinel帧及原重复键。与已固定TW1/CN5完整组段精确比对：464组命中TW1，1,185组命中CN5（TW1命中包含于CN5），另**554个动画组位置**没有与这两份现存表形成同ID同SHA匹配——不等于554个新物种。所有原SPR物理区间经独立逐帧重编码SHA完整覆盖。源Actions40321448446与独立归档40322474289均已实际success；全量压缩**派生元数据与独立来源链**永久保存在`research/recovered/tw85-spr137-r28/`，原安装器/图像/声音/程序均不入Git。详见[完整限定规格](docs/specs/STONEAGE-TW85-SPR137-MATERIAL-R28.md)和[日期连续性](docs/continuity/STONEAGE-TW85-SPR137-R28-20261026.md)。保存包尚非独立认证的官方纯净build，具名人物/宠物/NPC、真实原画面、运行世界仍未认证；最高后续回22域具体同构建可见内容与同源ADRN/REAL关联来源，避免无收益重复下载。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、总体百分比未知及完整CURRENT历史均未改。


### 2026-10-26 — R29同保存包原动画帧→ADRN/REAL图像内容完整数值联接

[本轮完整来源规格](docs/specs/STONEAGE-TW85-FRAME-BITMAP-R29.md)和[日期连续性](docs/continuity/STONEAGE-TW85-FRAME-BITMAP-R29-20261026.md)保留事实边界。R28已实得735666原帧（4759哨兵），本轮不用重下大型原包即全部联接剩余730907帧到**同557文件保存样本**的唯一ADRN/REAL原索引，共397443不同图像编号/392083不同完整RD(size,SHA)内容；无本样本缺索引、同号多候选。原R28新增差异554组的137192非哨兵帧全部有唯一原图内容来源。全量原派生表、独立SQLite和合成守卫永久验收，保留原顺序/重复/所有缺项，不猜新物种。此为原帧到真实资源块的元数据联接，非原彩色画面或具名宠物、原游戏实际运行。R30有限原图私人预览资格或有界缺源止点，拒绝无收益再下1.145GB原客户端；Stage A7 PARTIAL/2 OPEN、B/wiki GATED、R79暂停、总体复原百分比仍未知，旧CURRENT全文未替换。


### 2026-10-26 — R30实取8帧原RD像素、私人灰度动画

按[原实物观察规格](docs/specs/STONEAGE-TW85-ORIGINAL-RD-PRIVATE-R30.md)及[本轮连续性记录](docs/continuity/STONEAGE-TW85-ORIGINAL-RD-PRIVATE-R30-20261026.md)，不再只靠帧号和哈希推断：复用R29同保存包真实绑定，预选原 `spr_no=101501`、group index1185的动作数值2/方向0的八个帧bitmap 303039–303046；已从六分卷原样实际再取**1,145,465,184B**、静态解包并严格逐SHA验证 `adrn_158.bin` + `real_158.bin`，八原ADRN80B行/整RD块SHA一致后，实际解码八幅调色板索引图（flag1），产生私人灰度PNG与人为节拍GIF，并经加密传回/独立解密核8幅原SHA后目视连续轮廓。原商用图/音/程序及私钥不公开，Git只保留 `research/recovered/tw85-rd-private-r30/` 的计划/原块SHA/像素SHA与加密保管链元数据。source Actions 40329157425、归档40330184123真实success，前两次无作业YAML错误原样保留。**灰度不是历史RGB；未命名宠物/人物或动作，无原游戏程序运行，也未认证社区保存包为官方纯净build。** R30有限交付已够，最高NEXT改回同版具名宠物/NPC/本体任务master实物31，不连续扩RD helper；Stage A7 PARTIAL/2 OPEN、B/wiki GATED、R79暂停、整体百分比未知。原2.68MB CURRENT全文与各主簿没有修改。


### 2026-10-26 — R31同构建具名实体主表有限取证：真实八帧仍无可认证物种名

[规格](docs/specs/STONEAGE-ORIGINAL-SAME-BUILD-NAMED-ENTITY-R31.md)和[连续性补记](docs/continuity/STONEAGE-ORIGINAL-NAMED-ENTITY-R31-20261026.md)按新远端R30终态，逐核557条原保存客户端文件路径/原SHA、8帧SPR→ADRN/REAL完整原SHA和TW1.0原索引范围。557唯一文件路径、546不同文件SHA，显式pet/npc/quest/master**文件叶名**0，不等于exe/auto.dat内部不存在数据；8帧与源R30逐SHA一致，但物理号303039–303046不是TW1.0同号，不能猜宠物身份。新增同构建原服具名主表与实体ID→SPR绑定**0**；未知保持OPEN、没有重下载原1.145GB或发原美术。五原Git blob固定、离线严审脚本和否证测试可复核。最高NEXT转 `ORIGINAL_WORLD_MAP_CONTENT_MATERIAL_32` 做有界已得原地图具体内容验证；同构建原NPC/宠物/本体任务主表有真实来源才重开。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、P3E/R79/私人长存边界和未知总百分比不变。


### 2026-10-26 — R32历史原地图110的三处实际字段变化

[逐格规格](docs/specs/STONEAGE-ORIGINAL-MAP110-MATERIAL-R32.md) / [源链覆层](docs/continuity/STONEAGE-ORIGINAL-MAP110-R32-20261026.md)按新远端最高NEXT直接实取两份2003历史map.exe并逐SHA静态取map/110.DAT，46×45三原u16平面6210位置全比对：第一/第二原平面不变，第三平面仅原flat索引1/2/3由16384(0x4000)改49152(0xC000)，rowmajor坐标是候选而非原运行证明。第一次7z失效run仍保留，修正unar后源run40335682973实成功。唯一原派生2,832B经ZIP独立下载、SHA与Git blob永久入库；不存原地图、无原服/官方1.0/事件语义晋升。新任务优先原保存样本R30真实RD索引与同版调色板RGB来源33；Stage A7 PARTIAL/2 OPEN、B/wiki GATED、P3E/R79暂停、总体百分比未知。


### 2026-10-26 — R33 原SPR/RD调色板同载体全16字节匹配

[材料记录](docs/continuity/STONEAGE-PALETTE-SAME-CARRIER-R33-20261026.md)与[实际主线验收记录](docs/continuity/STONEAGE-R33-CI-FINAL-20261026.md)保留TW1.0与台8.5保存样本的16/16原SAP逐路径同SHA、R30八原索引帧同保存载体见证，以及仅TW1原代码验证的Palet_0初始化RGB规则。候选/main原内容Actions均真实SUCCESS。台8.5真实运行选色、纯净官方归属、宠物/NPC身份和原游戏世界仍未认证；下一主动最高为原世界玩家可见内容R34，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、总体百分比未知。


### 2026-10-27 — R34四间村落室内地图的实际数值变化

[原实物规格](docs/specs/STONEAGE-VILLAGE-INTERIORS-MATERIAL-R34.md)和[续接记录](docs/continuity/STONEAGE-VILLAGE-INTERIORS-R34-20261027.md)核两份2003历史小地图包中的1001/1003/1005/1006八个原成员：第一层均不变，1001第二层4格0→2，三张第三层共199格0x4000→0xC000，1003全层相同。本地另取原件/独立解码11700对字段与源Actions40407952047一致；原报告永久保管，原网格/程序未公开。萨姆吉尔武器店/宠物店/医院/村长家只作后期服务器头名称参考，不升级为初代同服场景或任务/碰撞规则。下一优先回DD-029原客户端实物与22域具名原数据队列35，停止扩本地图支线。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、总体百分比未知。


### 2026-10-27 — R35原客户端相册的148条名称字段、76个名称位置候选

[本轮原材料规格](docs/specs/STONEAGE-CLIENT-ALBUM-MATERIAL-R35.md)和[连续性记录](docs/continuity/STONEAGE-CLIENT-ALBUM-R35-20261027.md)按R35先完成有限原客户端回收止点（新增可认证官方客户端0），再仅从既有混合2.5包前16MiB实际取三数据文件并逐完整SHA复核。相册161424B中148条flag1名称字段覆盖76槽/76名，严格GBK及同槽后代文本对照一致；原字段可见乌力、乌力斯坦、黑乌力等，但**不是物种全集/原服master**。已排除随机初始化图号/属性，不解账号键或发表昵称；原载荷私人核验不入Git。下一目标36仅在有实际同源exe字节时补原相册表/原图号，否则有界止点轮转。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、总体百分比未知。


### 2026-10-27 — R36原程序281行相册表与224槽名称/图号

[原材料规格](docs/specs/STONEAGE-NATIVE-ALBUM-MATERIAL-R36.md)及[续接记录](docs/continuity/STONEAGE-NATIVE-ALBUM-R36-20261027.md)：仅稀疏读取既有混合2.5包7995392B，实取两份旧完整SHA匹配的原exe，不运行、不公开原程序。原指令定界281行/28B表，其中224有效槽、57内部空位；R35相册148次名称/76槽全部按槽匹配。乌力→表内28001等关联直接来自原程序，遇见flag1与拍照flag2写图号区别亦有原指令支持；尚未联到物理bitmap/SPR、不认证官方构建或原服物种主表。首次取件失败及7-Zip崩溃均保留，unar成功后逐全SHA/CRC验收。最高NEXT37仅有限核同源逻辑图号→原资源关系，否则轮转22域；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、总体百分比未知。


### 2026-10-27 — R37 原相册表内图号到同保存客户端 ADRN 物理资源的静态关联

[原材料规格](docs/specs/STONEAGE-PRESERVED-ALBUM-ALIAS-R37.md) / [连续性追加记录](docs/continuity/STONEAGE-ALBUM-ADRN-R37-20261027.md) / [实际主线验收收据](research/recovered/STONEAGE-PRESERVED-ALBUM-R37-PUBLICATION.json)：从社区混合2.5保存客户端同子树原 `adrn_15.bin` 完整18,765,120B/234,564条80B记录取得来源校验。R36原程序相册表内乌力face28001→原ADRN物理bitmap7246、乌力乌力28002→7247、乌力斯坦28003→7248；同号物理28001–28003实际是逻辑字段0的另外三条记录，不可混作相册真实绑定。首次源run40419864727虽然作业绿色，实际原件`NOT_ACQUIRED`；修正源run40420077051才有完整SHA/CRC匹配。R37内容候选run40422114956与主线run40422191047实际`completed/success`，按非强制快进合入主线。全部原程序/原REAL/密文私钥不入Git。**未取得**同源原REAL像素验证、运行时绘制、相同部署构建证明或官方早期物种master，认证纯净官方新客户端仍0。下一有界包`PRESERVED_CLIENT_ALBUM_RENDER_REAL_CONFIRMATION_38_OR_FINITE_EVIDENCE_GAP`只可取有界三图实物offset/size/RD，证据缺失则记录后回22域；Stage A 7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、整体完成比例仍未知。


### 2026-10-27 — R38原同包REAL文件头与三图偏移容量验证

[文件头规格](docs/specs/STONEAGE-ALBUM-REAL-HEADER-R38.md)与[连续性补记](docs/continuity/STONEAGE-ALBUM-REAL-R38-20261027.md)：原RAR4目录7954头全走、184个HTTP206范围/12,013,836B无损有限源，确认已有社区混合2.5同目录唯一`real_15.bin`文件头声明763,908,374B解压、338,458,942B压缩、RAR4 method53。R37三图物理7246/7247/7248对应ADRN解压地址26119737起的三个连续有界区间，全部落入该文件头声明大小。**只验证索引容量关系，尚未读取任何该REAL文件内RD头、图像块或像素**，不能将压缩RAR物理Range直接当图像偏移，也不认证官方同部署构建。R38原source Actions40422947999实际成功，原源报告和负面限制永久入库；未额外下载338MB压缩源。止于证据边界后回22域具名实体/NPC/本体任务主源队列，只有可验证有限REAL解压/私人保管条件才重开像素配对。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、官方原客户端新增0，整体完成率仍未知。


### 2026-10-27 — R39 原服务器三种名称的七条模板记录

[原材料规格](docs/specs/STONEAGE-PRESERVED-PET-TEMPLATE-MATERIAL-R39.md) / [续接记录](docs/continuity/STONEAGE-PET-TEMPLATE-R39-20261027.md)：从同社区混合保存包有限实取原配置与宠物模板，完整SHA/CRC吻合；“烏力/烏力烏力/烏力斯坦”对应7条原位置，图形字段分别100250/100251/100252。烏力斯坦4模板中一条标志0、其余1，不能按名称合并或任选标准模板。此为社区原始文件的有限字段事实，不是官方初代物种主表、原服务器运行或客户端同部署认证；相册头像字段与动画图形字段分别保留。source40449204618真实成功，原样派生JSON与独立ZIP来源链永久保存，原整表/商业载荷不公开。NEXT有限同保存包三图形字段→原SPR内容40；取源受限即回22域NPC/本体任务，不扩大REAL下载。Stage A/B/wiki/R79及未知整体百分比保持，完整CURRENT历史不变。


### 2026-10-27 — R40 三个宠物图形字段到原客户端完整动画

[原材料规格](docs/specs/STONEAGE-PRESERVED-PET-SPR-MATERIAL-R40.md) / [续接记录](docs/continuity/STONEAGE-PET-SPR-R40-20261027.md)：实际有界取同保存包原SPR两文件并核全SHA/CRC，R39七服务器模板的三个图形整数100250/100251/100252均唯一命中同包原客户端动画，完整168序列/1144帧；三段与TW1.0/CN5同号完整段SHA全部相同。847索引与三段全帧独立重编码原SHA一致，重复位置、声音word和非零保留字段均保留。只证明来源限定数值/动画内容关系，不认证官方初代名称、同部署、原画面/原声或捕获规则；没有下载大REAL。source40450507347真实成功，原样派生与独立ZIP来源链永久保存。最高NEXT41回原NPC洞窟三小文件的真实字节差异，停止扩宠物资源支线；完整CURRENT与Stage A/B/wiki/R79等边界不变。


### 2026-10-27 — R41 原NPC参数异SHA原因与三条创建配置

[原材料规格](docs/specs/STONEAGE-PRESERVED-NPC-DELTA-MATERIAL-R41.md) / [续接记录](docs/continuity/STONEAGE-NPC-DELTA-R41-20261027.md)：实取旧sb_kbu.arg与两份原创建/模板文件，全SHA/CRC吻合。旧/现代258B参数114字节位置不同，原因是编码转换加三个对白字段14处繁简替换；数字和键相同，不能只叫纯转码或宣称运行逻辑等价。原创建文件实际3条風的守護獸配置：11208两条、11214一条，现代11208单地图仅覆盖前两，3warp另类、不报第三条删除。source40451830173真实成功，原样派生、独立私人原字节比较与ZIP链永久保存，原对白/脚本明文和密钥不公开。NEXT42仅取第三条所引sb_kgi.arg作有界材料比较，随后轮转；官方同build、任务起源/运行仍未认证，完整CURRENT与Stage A/B/wiki/R79边界不变。


### 2026-10-27 — R42 原保存第三守护兽参数实物

[R42 第三 ARG 原件差异规格](docs/specs/STONEAGE-PRESERVED-GENKOU-THIRD-R42.md)及[连续性增量](docs/continuity/STONEAGE-GENKOU-THIRD-R42-20261027.md)记录原 `sb_kgi.arg` 281B 全 SHA/CRC、同 R41 三原件联合取证：第三创建配置所引参数有 `warpfl=11215`、`warpx=9`、`warpy=16`，`dieact=1` 与另一组10次敌号；旧 `sb_kbu.arg` 的 `time=180` 在第三参数不存在。R42 source run40456016963实际 success；原工件不进公开仓。来源只是社区混合包，原服务器触发／任务起源与官方初代同构建未证。最高NEXT按协议13回22域，优先有可追溯来源的早期官方具名宠物/NPC/本体任务实体表及事件，不扩该NPC helper；Stage A/B/wiki/R79、原客户端P3E与整体完成率边界不变。


### 2026-10-27 — R43 相册224具名槽跨样本原资源整合

[材料规格](docs/specs/STONEAGE-ALBUM-CROSSVERSION-MATERIAL-R43.md) / [连续性](docs/continuity/STONEAGE-ALBUM-CROSSVERSION-R43-20261027.md)：有限官方来源核查未取得新同构建主表后，直接联接既有原程序224相册名称槽与三份原资源目录，保留57内部空位。TW1命中120槽、与后两样本相同完整RD内容；CN5及patch各224槽/228引用，4逻辑键各两不同内容完整保留。576引用经独立SQLite全字段联接相同，未把后期名称回填为TW1原版物种认证，没有原像素/大包新下载。NEXT轮转一份有界物品/商店具名原数据44，Stage A/B/wiki/R79与未知整体完成率不变。


### 2026-10-27 — R44 原商店参数的34个ID与6条具名物品模板

[原材料规格](docs/specs/STONEAGE-PRESERVED-ITEM-SHOP-MATERIAL-R44.md) / [连续性](docs/continuity/STONEAGE-ITEM-SHOP-R44-20261027.md)：三件原文件全SHA/CRC吻合，原库存34编号全在同保存样本实际配置物品表；前6条含5个同名“合成兜 10”不同模板和一条“合成鎧 10”，全部原行位置/摘要保留。后代代码33条上限模拟会截断末项20905，但原服务器显示/交易未证。首轮路径断言错误、三件已取却派生未验的绿色run原样保留，修正source40495285257才内容成功；51本地检查及两独立下载ZIP来源链已核。不是官方初代物品/同部署认证，无原master/对白/程序公开。NEXT转宠物技能小原表45，Stage A/B/wiki/R79及整体百分比未知不变。


### 2026-10-27 — R45 六条原技能名称、字段及模型关联

[原材料规格](docs/specs/STONEAGE-PRESERVED-PET-SKILL-MATERIAL-R45.md) / [连续性](docs/continuity/STONEAGE-PET-SKILL-R45-20261027.md)：实际取同保存包原配置和技能表，全SHA/CRC及unar/libarchive双解码字节一致；原名称“待機/攻擊/防禦/破除防禦/連續攻擊/三段攻擊”接ID0/1/2/3/10/11与既有复原模型。两个1字节OPTION的精确数值见证2/3接既有命令桥验证，不把COST2当MP/学费，不把147条混合表当147可学技能；首过窄前缀校验失败原样保留，修正source40499885826才内容成功。48本地检查及双ZIP永久源链已核，无原表/描述/程序公开或原服执行。NEXT转一份有界治疗NPC创建材料46，Stage A/B/wiki/R79和未知总体完成率不变。


### 2026-10-27 — R46 原社区家族护士三条命名NPC原配置

[材料规格](docs/specs/STONEAGE-PRESERVED-HEALING-NPC-MATERIAL-R46.md) / [连续性覆层](docs/continuity/STONEAGE-HEALING-NPC-R46-20261027.md)：按上一轮NEXT实际有限获取源混合保存包`npc/family/fmhealer.create`649B，原完整SHA/CRC与既有清单相同，184个严格HTTP206范围、unar/libarchive独立同字节解码、Big5/CP950严格文本一致；原配置共4块，本轮限前三条均“家族小護士”，floorid1041/2031/3031、不同borncorner、相同图形16023与服务声明`npcgen_fmhealer|1`。第四块仅计总数，无拓展解释。source40502401619真实success，派生原始报告和审计只入安全元数据，不公开原脚本/对话/包。**不认证台湾1.0同构建、实际NPC服务/后代Healer函数绑定或本体任务**；仍`ORIGIN_UNRESOLVED`。NEXT回22域可追溯原具名实体/本体任务材料，不扩治疗helper。Stage A/B/wiki/R79及总体恢复率未知边界不变。


## 2026-10-27｜原始素材现代观察R1验收后的最新优先级（历史前缀保持原样）

历史Stage A独立验收按其原始7369B README前缀永久固定。本节将之前放在文件开头的2026-10-27新决策附录迁移到文末，保留老档完整字节并维持新优先级；不可回写或重写已验历史事实。分支候选与主线验收及失败修正详见 [主线验收回执](docs/continuity/STONEAGE-MODERN-OBSERVATION-R1-MAIN-ACCEPTANCE-20261027.md)。当前主线现代观察专用CI成功，但历史原EXE只见登录画面，世界仍未进入。地形原图的实际私有可视验收、原客户端ACP950/8bpp/可操作环境及同建绘制语义均OPEN。

## Highest active priority — Original-world observation (2026-10-27)

The user explicitly elevated **actually entering and experiencing the original StoneAge game world** above further unconstrained material search. The original authenticated Taiwan-v1 `sa_3.exe` was **already executed**, and the genuine login screen was captured and visually inspected; **the playable world, combat and audio in that client have NOT been observed**. Earlier synthetic 8-bit Windows checks did not jointly satisfy ACP950, direct RGB and input qualification. The P3F synthetic Windows Server 2022 process `zh-TW` manifest probe was executed and **did not qualify** (ACP stayed 1252). The immediate practical route is a modern offline, source-tagged resource observer; qualifying an isolated zh-TW Windows guest remains the separate original-executable verification path, not a prerequisite for viewing authenticated image/animation resources. A successful synthetic job must never be called original gameplay. See [dated priority and acceptance gates](docs/continuity/STONEAGE-ORIGINAL-WORLD-OBSERVATION-PRIORITY-20261027.md) and [P3/P3E historical records](docs/STONEAGE-ORIGINAL-OBSERVATION-LAB-R1.md).

## Accepted new-game language and observation route — 2026-10-27

**Design decision DD-030:** The future new StoneAge game will present its player interface, quests, story and systems in **Simplified Chinese (zh-CN), Unicode/UTF-8 by default**. The user played the Mainland edition; mainland names and visual experience are important design references. Japanese, Korean, Taiwanese and Mainland originals remain version-tagged and their original text is not overwritten by product localization.

A modern offline resource-viewing route now takes priority alongside authentic original-client research. Old 256-color/ANSI Windows compatibility is not a blocker for building the modern observation environment. The **source-qualified Simplified Chinese offline observer R1** was merged to main via [PR #13](https://github.com/chinaneedM/stoneage-rebuild/pull/13) at `573046d14597c6b127b0a529fc66d4e8737169c9`; both its candidate CI (41 Python tests + Node mock browser) and its main-merge dedicated observer job completed successfully. This is a **research tool acceptance only**, not original-world entry or a production game. See [modern observation viewer](tools/modern-observation-viewer.html), [private frame exporter](tools/stoneage_private_sprite_frame_export_r1.py), [research image contact sheet](tools/scene-original-graphic-contact-sheet.html), and [main acceptance receipt](docs/continuity/STONEAGE-MODERN-OBSERVATION-R1-MAIN-ACCEPTANCE-20261027.md). Full decision: [DD-030](docs/DESIGN-DECISIONS.md).

### Source-bound map artwork observer — source-logic accepted, real private artwork still OPEN

The merged observer provides a bounded **private** recovered25 map-ID → ADRN/REAL image-data probe. It only admits the whole-file SHA-qualified preserved recovered25 sources and map plane payloads, retains duplicate-ID ambiguity and exports up to 16 grayscale indexed-image previews **outside Git**. The companion [private source-image contact sheet](tools/scene-original-graphic-contact-sheet.html) checks each PNG SHA and actual browser decode, displaying source map/bitmap numbers instead of fabricating a historical village. The same-build original draw-selection behavior, scene palette, isometric layout and authentic gameplay remain OPEN, and the private 763 MB REAL file was **not** read or visually inspected in this session. See [source join limitations](docs/continuity/STONEAGE-SCENE-RESOURCE-JOIN-R1-20261027.md) and [post-merge acceptance](docs/continuity/STONEAGE-MODERN-OBSERVATION-R1-MAIN-ACCEPTANCE-20261027.md).

### 2026-10-28｜真实地图素材第一次按现代观察路径取出并目视，固定载体已可复用

[SCENE02实际观察与保管回执](docs/continuity/STONEAGE-SCENE02-REAL-OBSERVATION-20261028.md)：固定混合2.5原载体361255180B及同包完整ADRN/763908374B REAL/1001.DAT均逐完整SHA匹配；地图1001中央3×3格实际解出8张灰度索引图，独立RD解码与Pillow PNG字节一致，观察者已真正查看并列图册。首次libarchive过滤器失败40591003447原样保留，unar修正源40591156280实际成功。完整原载体及限定观察包已私人保存并从持久副本完整回读核SHA；公开Git只留工具/测试/派生报告。**尚未拼成原色场景、没有原客户端选角/移动/战斗或世界进入**，也不认证该社区保存包为官方初代。NEXT为复用既有载体的 `SCENE-PALETTE-PROJECTION-03` 小片段候选色板/排列验证，停止无限NPC网页轮转；DD-030简体中文、原历史前缀、Stage A/B/R79与整体百分比未知均保留。

### 2026-10-28｜SCENE03同保存原程序选色与真实彩色地图片段候选

[颜色/排列回执](docs/continuity/STONEAGE-SCENE03-COLOR-LAYOUT-20261028.md)：直接复用已保管原载体，实际取16份SAP及同子树原EXE，发现程序表第0项静态引用指向Palet_1.sap，不能按编号猜Palet_0。原3×3的8张源图按有来源的自下向上行序、32/24锚点、有符号ADRN偏移和key0生成连续地面/三立体构件候选并已目视；独立源码坐标片段编译得到12个引用，独立SAP/RGBA实现重建三层像素完全相同。新增商业原包网络下载0B。**这是同保存源颜色和后代源码排列候选，尚非原版实拍、同建遮挡认证或可操作原世界。** 原SAP/程序/图像不入公开Git；NEXT为同一地图房间视口的实际镜头/图层观察04，Stage A/B/R79与整体百分比未知保持。
