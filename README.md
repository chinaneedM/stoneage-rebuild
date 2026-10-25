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
