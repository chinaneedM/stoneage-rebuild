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


### Current original-artwork room observer — SCENE04 (2026-10-28)

The bounded 5×5 private room viewport for recovered map 1001 has been created,
actually opened and interacted with in headless Chromium, and stored in the
owner's private persistent Library. The source-verified 30 map placements
include 28 supplied real-original image references and two clearly marked
missing bitmap IDs (5009/5015); all eight existing source sprites and the
previous SCENE03 3-layer image pixels were revalidated. Camera pan/zoom and
layer toggles are *modern offline viewer* functions; no playable original world
or original client in-world interaction was observed. The source is a community
preserved mixed-2.5 specimen, **not** an authenticated original Taiwan-v1 build.

See [source-safe dated SCENE04 checkpoint](docs/continuity/STONEAGE-SCENE04-ROOM-VIEWPORT-20261028.md)
and [replay metadata](research/recovered/STONEAGE-SCENE04-ROOM-ACCEPTANCE-R4.json).
Private archive, standalone HTML and real Chromium screenshot are retained
outside the public Git repository, with complete post-upload Library readback
hash verification. NEXT: only two source-backed missing bitmap companions from
the already-preserved carrier, followed by original runtime camera/occlusion
and playable-world entry as independently gated work. Stage A, Stage B and R79
boundaries remain unchanged; overall restoration completion percentage is null.


### Source-bound SCENE04 two missing bitmap ADRN entries — 2026-10-28

Following actual R4 source replay and [PR #16](https://github.com/chinaneedM/stoneage-rebuild/pull/16)
main merge `176ff4d92d1aeca6c940d50c23a5824417016dd5` (10/10 main workflows successful), the two
missing 5×5 image IDs 5009/5015 were each found **once** at the original
preserved same-carrier ADRN record field offset 76. This now pins real bitmap
indexes 1624/1630 and private REAL decompressed file offsets/sizes, but not
decoded RD pixels or a verified original-world screenshot. Exact evidence and
remaining extraction gate are appended to the
[SCENE04 dated checkpoint](docs/continuity/STONEAGE-SCENE04-ROOM-VIEWPORT-20261028.md)
and [source-safe bitmap bound report](research/recovered/STONEAGE-SCENE04-TWO-IMAGE-ADRN-BOUND-R1.json).
The next task stays narrowly limited to these two existing private-source
ranges, not a new whole-client download or arbitrary program reverse engineering.


### 2026-10-28 | SCENE06 native display order, bounded no-actor observation

[原程序有限重放与续接记录](docs/continuity/STONEAGE-SCENE06-NATIVE-ORDER-20261028.md)：同混合保存客户端原扫描、ADRN查询、构件链表、原比较器/CRT排序器及消费请求顺序已在隔离指令解释器中有界重放；25地面+5构件按同层反向编号绘制，候选合成3549像素改变。私人R6页可切新旧顺序并已保存/完整回读。180边界用例和后代源码独立编译同一；41项本地检查及DOM模拟通过。本轮未取得Chromium，不认真实浏览器验收；LoadBmp返回失败桩、原生绘图/人物遮挡/原客户端世界进入仍OPEN。NEXT为有限隔离TW1运行环境/世界入口资格P3G，不扩显示helper。原CURRENT全字节不改，Stage A/B/wiki/R79及未知总体百分比保持。


### 2026-10-28 | P3G Windows2025原件运行前提取得实测候选

[三次源实测与续接](docs/continuity/STONEAGE-WINDOWS-P3G-20261028.md)：Windows2022修正命名空间后UTF-8生效但zh-TW仍ACP1252；Windows2025正确清单下同一自编x86接收器实得ACP950/8bpp、真实红绿像素及鼠标接收。另一一次性来宾实验在约5.28秒全程序出站阻断期间仍通过颜色/输入，两程序路径TCP实得WSAEACCES，清理后恢复；没有冒称已遍测IPv6/UDP/loopback或原进程。三个源JSON及完整ZIP/run/job/Git链永久保管，旧失败与CURRENT全文不改。最高NEXT转原TW1真实Windows登录/QUIT有限观察P3H，先验证未改EXE的外置清单和隔离/保管；原程序本轮下载/执行0，世界仍未进入，Stage A/B/wiki/R79及总体百分比未知保持。


### 2026-10-28 | P3H原TW1实际Windows运行/退出，原画面仍黑

[原件有限观察与完整续接](docs/continuity/STONEAGE-WINDOWS-P3H-20261028.md)：未改EXE的外置清单自编前提通过，认证TW1原375文件逐SHA匹配后在临时出站阻断来宾真实运行，已知退出坐标点击后清理前正常退出0。**独立目视三帧的两种图像仅见黑底/IME/光标，游戏画面、原调色板和繁体UI仍未认证，世界没有进入。** 三次失败和修正均保留，原样报告/完整工件保管链永久记录；375原件与观察包已私人持久保存并完整回读核SHA，公开Git不含原件/图像/私钥。最高NEXT为限定只读原生帧读出P3I，判别实际未出图与屏幕抓取路径缺口；不展开参数树。CURRENT完整历史字节与Stage A/B/wiki/R79/总体未知边界不变。


### 2026-10-28 | P3I 只读原生帧分辨实验（源运行待验）

[P3I 受限 DirectDraw primary 读出方案](docs/continuity/STONEAGE-WINDOWS-P3I-20261028.md)：承接 P3H 原 TW1 黑屏/可退出实证，增加不修改原 EXE、不开原进程内存的原生全局 primary 只读索引观察及独立采样证明。其成功读取不等于读取原程序私有 backbuffer，也不等于恢复原画面/世界。优先验证一轮真正 Windows source Action；无实质差异则按协议13回同源现代场景观察，禁止泛化扩 WinXP/驱动助手。完整 CURRENT 2680510B 原文保持不变；Stage A/B/wiki/R79 与总体进度未知保持。


### 2026-10-28 | P3I 原运行 + 原生主表面已实测，原游戏仍未显示

[P3I 实际运行、已核小工件和原生帧采样受限验收](docs/continuity/STONEAGE-WINDOWS-P3I-20261028.md)：原 TW1 本次进程/退出又获认证；Windows source job `40640162726` completed/success，独立主表面 1024×768/32bpp Lock 与客户区像素摘要实得。**它不是原客户端私有绘图缓冲区，也没有找到可见的原游戏图或世界**。小 source-report artifact 4,412B 已独立下载核SHA，45,308B 原报告完整回读；大密文仅证 GitHub CI 上传，不宣称本轮耐久保管。后验只保留永久派生摘要和准确否证状态。P3I 受限排障止点已到；下一回同源现代离线场景观察器，待真正新证才重开原本体世界入口。CURRENT、DD-028/030、Stage A/B/wiki、R79边界及未知百分比不变。


### 2026-10-28 | P3I独立复测仍未出现原游戏画面

[同一P3I日期记录](docs/continuity/STONEAGE-WINDOWS-P3I-20261028.md)追加第二次实际隔离源Run40640619774成功，另一个来宾全局primary 1024×768/32bpp、窗口区域SHA与首轮**完全相同**，原程序仍可在坐标点击后正常退出，但GDI截图仍只见黑底/输入法。两份短期源小ZIP与原报告均独立哈希；大密文只记录Actions来源。外部探针的32bpp不能回填原进程8bpp调色板。这是有限止点而非原游戏画面或世界验收；下一改回现有真实地图/人物/宠物原素材的现代离线观察，直到新同源原生证据出现。Stage A/B/wiki/R79与总体未知不变。


### 2026-10-28 | SCENE07 同载体地图与两组原动画已实际共同观察

[本轮材料、实际浏览器及连续性记录](docs/continuity/STONEAGE-SCENE07-ACTOR-OBSERVATION-20261028.md)：复用已保管混合2.5原载体，完整SHA验证同子树SPR/SPRADRN/ADRN/REAL/SAP，实取100000与100700两组八方向/动作码2和6，共32原动画、208帧出现、128原图；独立解码/RGBA/PNG全部同一。私有R7页真正Chromium解码138图并完成暂停/单步/切换/人工位移、图层与镜头检查；独立Pillow对浏览器691200像素逐字节一致。页面已私人保存且完整回读同SHA。**两个可见人形的名称、原游戏遮挡/碰撞/节拍仍未认证，未进入原世界。** 下一有限接R39/R40同包模板图形键100250/251/252之一的宠物候选；禁止把同包等号当同服官方身份。CURRENT2680510B历史原文、Stage A/B/wiki/R79及总体未知边界不改。


### 2026-10-28 | SCENE08 三组保存模板宠物原图已实际接入观察

[原材料、名称资格与完整续接](docs/continuity/STONEAGE-SCENE08-PET-OBSERVATION-20261028.md)：同保存源「烏力／烏力烏力／烏力斯坦」的图形键100250/251/252，实际读出八方向动作码2，共24段、256帧位置、160不同原图；第三组每方向20帧的重复引用完整保留。原组无动作码6，不套用人物回退；七模板原行全留（含flag0）。私人R8页218图经真实浏览器逐方向/帧检查，独立208RD、32SPR片段及691200画布像素全同；已保留观察页历史版本并完整回读新版本相同。**同包数值关联不证明原服同部署或官方初代物种身份，仍未进入原世界；位置/遮挡/节拍为人工观察。** 下一有限核同保存原程序演员与构件队列遮挡规则09或具名缺口，不扩驱动/全函数树。完整CURRENT和各原历史、Stage A/B/wiki/R79、总体未知保持。


### 2026-10-28 | SCENE09 原片段有演员插序候选与可见遮挡比较

[原源范围、真实重放和续接](docs/continuity/STONEAGE-SCENE09-ACTOR-PARTS-ORDER-20261028.md)：同保存原EXE的演员入队、构件比较、ADRN属性getter与排序器在解释器中48组真实执行，无函数返回桩；原DAT扫描30条请求、208演员记录完整SHA匹配。受控演员先入队条件下，两个演员与五构件形成候选前后关系，固定首帧25位置中7处可见变化、示例5229像素不同。私人R9页218源图实际浏览器可切换比较，三幅画布各691200像素与独立Pillow全同，页面新版本完整回读一致。**原数组/裁片/别名/演员结构与阶段顺序为实验注入，完整原帧调度/GPU/原世界仍未认证。** 下一只核原程序帧内清链表→演员→地图的先后来源10或精确缺口，不扩驱动或全函数树。全部历史与Stage A/B/wiki/R79及总体未知保持。

### 2026-10-28 | SCENE10 私人候选帧阶段独立预检（不是原EXE认证）

[日期续接与负例门槛](docs/continuity/STONEAGE-SCENE10-PRIVATE-PREFLIGHT-20261028.md)：私人 R10 观察页保管副本经完整 SHA 验证，结构记录四条候选帧路径各五个关键调用，另有23个中间调用与所有完整外层路径均未独立重放；96次用例只属于候选自述。公开预检守卫及10项正反测试在 [PR #25](https://github.com/chinaneedM/stoneage-rebuild/pull/25) 的候选/主线专用 Actions 实际通过。**本轮未取得/独立核验同 SHA 原 EXE 的 callsite 原字节，不能据私人观察页自报推原帧调度成立，更未进入可操作原世界。** NEXT为原件可得时有限复核四条路径/缺失回调，遇无证据止点转其他已有真实材料；原版权内容不入公开Git。CURRENT 全部历史原字节不变，DD-028/030、Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停及总体百分比null保持。

### 2026-10-28 | SCENE10 受限原件取证与现代地图真实像素验收（严守证据边界）

[主线研究与连续性回执](docs/continuity/STONEAGE-SCENE10-SOURCE-AND-PIXEL-ACCEPTANCE-20261028.md)：[PR #26](https://github.com/chinaneedM/stoneage-rebuild/pull/26)独立取到原混合保存第一分卷的16MiB HTTP206片段并校验来源SHA，但因RAR仅前缀，未能提取同SHA原EXE，43原调用点仍未独立认证。首次synthetic测试失败原样保留，修正后源门槛成功但业务状态仍为SOURCE_UNQUALIFIED。现代私人R10观察页218幅实际来源图与25处5×5镜头独立Pillow比较，原素材x+1候选画面25/25改变，真实Chromium144三帧每帧691200 RGBA与独立合成完全相同；并不证实原游戏X偏移/完整帧/世界。源工件ZIP/报告逐SHA及失败/成功CI证据永久归档。停止缺源循环，下一转22域可取实物/场景/宠物/交互材料。原CURRENT 2680510B全文、DD-028/030、Stage A/B/wiki、R79及总体百分比null不变。

### 2026-10-28 | SCENE11 原宠物真实图像轮廓、动作重复与非全局换色负例

[完整SCENE11日期续接](docs/continuity/STONEAGE-SCENE11-PET-VISUAL-20261028.md)与[PR #27](https://github.com/chinaneedM/stoneage-rebuild/pull/27)：私人R10观察页原SHA全检并解码208幅来源PNG（宠物160/人物48），同保存包R40原SPR完整段100250/251/252与早期TW1/CN5三段SHA完全相符。原动作码2的八方向对应画面100250与100251各48出现/48不同图，100252有160帧出现但只64不同图，**96重复帧位不可丢**；每方向相同20位置图号模式保留。48个100250/251对应原像素帧38对alpha轮廓完全相同，剩余十对合计仅12 alpha像素不等，全部48对可见RGBA共43069位置不一致；140种源RGBA中125种映射不唯一，不得假设一个固定换色表可再生所有帧。只提交数值/哈希/程序和负例测试，原PNG与private HTML不公开。候选源安全Action40705927012与主线40706155057均已实际completed/success（15测试）；**专用CI不读取私有原图，不等于原版程序实际运行或官方宠物身份**。下一移交新增有实物的其他动作图/场景交互，若无原像素则有限止点回材料轮换，停止R10原EXE分卷空转；旧CURRENT全文2680510B原blob不改，Stage A7 PARTIAL+2 OPEN，B/wiki GATED，R79暂停，总百分比null。


### 2026-10-28 | SCENE12 私人场景观察器受控来源证据范围修复

[SCENE12 日期记录](docs/continuity/STONEAGE-SCENE12-OBSERVER-WITNESS-SCOPE-20261028.md)及[PR #28](https://github.com/chinaneedM/stoneage-rebuild/pull/28)：重新读取SHA认证的私人R10观察页，发现观察器将 R9 100250/方向0受控排序误用于其他选中宠物、方向和帧。48个原R9受控样例对应6400个现代观察可选状态中**仅56个两图号同时吻合**，6344个必须明确显示为现代回退绘制而非原插序事实；加入SHA限定私有HTML修复工具、源安全数值记录及反例测试。私人修正版浏览器实际解码218张图，错误0、外部请求0，原图/HTML未入Git。候选Actions [40709304608](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40709304608)已实际completed/success，PR #28已合并，主线合并提交 e4603d62986ac7ca35174aedd297b6010be25825。此成功**并非原游戏运行或官方宠物身份恢复**，仍是后代混合来源的受控参考；Stage A 7 PARTIAL + 2 OPEN，Stage B/wiki GATED，R79暂停，总完成率未定义。下一最高：材料优先恢复有实际原图的新动作或有同版输入的NPC/地图交互，缺实物则有界停止，不扩大原EXE分卷与泛用渲染helper。


### 2026-10-29 | SCENE13 三组宠物动作码0真实原图与完整逐帧观察

[SCENE13实物与验收](docs/continuity/STONEAGE-SCENE13-PET-ACTION0-20261029.md)：复用已保存原载体并完整认证五成员，实际新解码208原图、24段动作0、352帧位置，144重复帧位置全部保留；真实Chromium266图，全部352画布与独立Pillow逐像素一致。原素材只私人保存，公开Git仅程序/数值/哈希。动作名、原FPS、原生遮挡与官方物种不晋升，仍未进入原世界；最高下一同源NPC/地图交互14，Stage A/B/wiki/R79与总体未知保持。


### 2026-10-29 | SCENE14 地图1001武器店的原位置、17项库存和候选原图

[原配置与实际观察验收](docs/continuity/STONEAGE-SCENE14-ROOM-SHOP-20261029.md)：同已保存原载体的创建块→商店模板→库存参数→原物品表具名联接，原(17,13)与图形16017候选原像素已接入私人房间，实际点图查看原参数。四种整数倍率画布与独立像素合成全同，2.5倍边缘不等未认证；买卖/碰撞/原世界未运行，官方同部署仍未知。最高下一一条房间出口实物增量15，历史与生产边界保留。


### 2026-10-29 | SCENE15 按原出口输入观察室内与室外原图

[一组成对出口与真实像素验收](docs/continuity/STONEAGE-SCENE15-DOORWAY-20261029.md)：定位原创建块和Warp模板，把已有1001(10,15)↔1000(63,99)接入实际两侧7×7原图观察。51原图/81引用，真实浏览器52图、11整数画布与独立像素合成全同；邻门不误用，显式往返，不冒称原服传送/碰撞或进入原世界。主原DAT全SHA/CRC成立，室外地图第二解包复核失败如实保留。下一一名室外落点附近NPC原输入16，完整历史与生产边界保持。


### 2026-10-29 | SCENE16 室外 NPC 原成员资格门槛（原件正文仍未取得）

承接 [SCENE15 成对原门实际两侧观察](docs/continuity/STONEAGE-SCENE15-DOORWAY-20261029.md)，已在已有完整 R18 原服务器成员清单定位 `npc/genout/1000npc_m.create` 为4,413B/完整SHA绑定，但 Git 仅含文件级清单，不含原 NPC 创建脚本文本；(63,103) 是下一调查坐标，**不是本轮已认证 NPC 出生位置**。增加 [SCENE16 来源资格/停止记录](docs/continuity/STONEAGE-SCENE16-NEARBY-NPC-GATE-20261029.md) 与只读原成员整SHA校验、有限目标筛选和模板精确名联接程序；无私有原文件时明确 `SOURCE_NOT_SUPPLIED`、`matched_count=null`，不能报原 NPC 名字/任务/互动或像素恢复。候选独立 [Actions 40787873232](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40787873232) 实际 completed/success，专用15测试通过；只证明程序与原目录/旧门派生守卫，**不证明原版运行或 63,103 NPC 存在**。保留完整 CURRENT、Stage A/B、R79、总体百分比 null。下一限有同SHA原件时真实联接，否则按22域材料优先轮换。


### 2026-10-29 | SCENE17 真实原件：室外出口邻近 NPC 创建配置

[SCENE17 来源报告及日期续接](docs/continuity/STONEAGE-SCENE17-ORIGINAL-NPC-SOURCE-20261029.md)：从既存混合2.5保管分卷通过184次HTTP206/12,013,836B定点取得并双解包全SHA认证 `npc/genout/1000npc_m.create`(4413B) 与 `npcgen.template`(4950B)，原25/41块中有**恰好一条**地图1000、固定坐标(63,103)、图形16048、创建数量1、方向4的NPC创建块，唯一连接模板`npcgen_man`→`TownPeople`。完整源派生文件、原压缩header/range hashes及15条新增反例永久存于[研究JSON](research/recovered/STONEAGE-SCENE17-ORIGINAL-NPC-SOURCE-R1.json)，源Action [40789416440](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40789416440) completed/success，候选校验[40789787160](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40789787160)实测35项通过。所用是混合社区保管，不认证台湾1.0官方同服；原客户端世界仍未进入，NPC姓名、原对白、真实可交互性及原像素未新认证。NEXT限图形16048同载体原图或具名缺件，随后回22域轮换；Stage A/B/wiki/R79边界及总体百分比null不变。


### 2026-10-29 | SCENE18 室外NPC原图索引与真实源工件耐久验收

[SCENE18来源/验收与下一步](docs/continuity/STONEAGE-SCENE18-GRAPHIC16048-ADRN-20261029.md)：独立下载核验成功源工件并永久归档，原图形16048唯一对应bitmap5894、36×79、REAL偏移25018537/1668B。原ADRN全SHA/CRC由unar通过，libarchive不支持压缩过滤器的失败保留；跨版完整记录同SHA提供取图候选，未读mixed25原像素不能称已见NPC。51本地相关测试通过，远端CI后验另记。最高NEXT先查现有私人原图5894，缺件则回22域，不扩解包/驱动链；原世界仍未进入，生产/总体未知边界保持。


### 2026-10-29 | SCENE18主线全过，SCENE19已从保存TW1原件取得人物候选图

[最终验收与新续接](docs/continuity/STONEAGE-SCENE18-GRAPHIC16048-ADRN-20261029.md)：PR34主线21项Actions与候选21项全部通过，51测试真实日志已核。复用已保存TW1原件实读bitmap5894，双解码器一致取得36×79/2844原索引及私人候选PNG；Palet0颜色仍候选，mixed25对应REAL未读，不能认定同源NPC或原世界运行。原图包已私人保存，公开仅派生JSON。最高下一SCENE20先回22域材料复核与有实物内容轮换，停止原RAR/驱动/同摘要空转。


### 2026-10-29 | SCENE20 原TW1全127散装WAV私人离线试听

[材料轮换/实物/真实验收与续接](docs/continuity/STONEAGE-SCENE20-TW10-AUDIO-20261029.md)：复用已保存原件，把116音效目录和11配乐目录原WAV完整接入检索/手动试听页；全127原文件/33587115声道样本独立FFmpeg一致，重复路径保留。远端浏览器只用127合成音频实测，修正浮点归一化假设后逐整数PCM及界面控制通过；本地原声浏览器/助手听觉/游戏事件仍未认证。私人34MB包已保存，原声音不公开。下一只用已有1000.DAT/51RD核NPC坐标附近原图覆盖21，原世界与生产边界保持。


### 2026-10-29 | SCENE21 补齐19地图原图并实际合成NPC附近场景

[实际像素、整前缀订正与下一步](docs/continuity/STONEAGE-SCENE21-TOWN1000-AND-PREFIX-CORRECTION-20261029.md)：复用旧已验整资源前缀证明及已保存原件，重新核完整mixed ADRN/TW ADRN前缀，补齐19地图原图和NPC16048候选。扩展至77格/85地图图像出现，56RD与8完整画面经独立重算同一并实际目视；原图只私人交付。此前只核同索引遗漏整REAL前缀依据，现日期订正，过去0B mixed REAL执行记录不改。42本地测试，合成浏览器源成功；原生绘制/原世界未认证。下一只核这一NPC的精确原参数/对白输入22，不扩helper。


### 2026-10-29 | SCENE22 一名原NPC的精确对白文件已接入离线查阅

[原输入、有限内容合同与续接](docs/continuity/STONEAGE-SCENE22-NPC-ARGUMENT-20261029.md)：原创建块明确指向143B原对白，三份原文件全SHA匹配旧R18，整保管RAR、独立头CRC/原成员CRC均核。它是村民信息/商店买卖口令的新手提示，一行无ASCII逗号，不能由文案推此NPC多分支或交易运行。私人页保留原文与简体释义，原8场景值不变；53本地相关测试通过，远端验收按实际后验另记。**仍未进入原客户端世界**，同服/原生交互不晋升。完整CURRENT原字节作为追加前缀保留；最高下一SCENE23回22域材料轮换，Stage A/B/wiki/R79与总体未知保持。


### 2026-10-29 | SCENE23 十二身体图形候选已有八方向原首帧

[同版原图、两候选配色和完整续接](docs/continuity/STONEAGE-SCENE23-BODY-VISUALS-20261029.md)：原R16数值与原SPR/ADRN/REAL实取96首帧，双解码/192候选配色及卡片独立全同，私人页可按方向/候选配色比较并查原记录。不是已证十二可选人物或全角色/全动画；只观察源728帧位置中的96首帧。35本地测试通过，远端后验另记。原世界未进入，下一限SCENE14原商店前三物品的图号命名空间/原图输入24。


### 2026-10-29 | SCENE24 三件商品原行→别名候选图及错误命名空间对照

[三原行、完整别名扫描与续接](docs/continuity/STONEAGE-SCENE24-SHOP-ITEM-IMAGES-20261029.md)：原ID0/4/10的imagenumber20033/20032/20013对应唯一+76别名物理6006/6005/5986；同值直接物理号读到另一批原图。六RD/两配色12PNG与24现代卡片独立一致；51本地检查通过，原图和源正文只私人保存。仍是候选数值关联，未认证原selector、官方同服或买卖。下一限原房间/NPC和三商品资料的离线整合25；原世界/Stage A/B/wiki/R79/总体未知边界保持。


### 2026-10-29 | SCENE25 房间、武器店与三件商品资料已有限整合

[来源合同和验收续接](docs/continuity/STONEAGE-SCENE25-ROOM-SHOP-INTEGRATION-20261029.md)：原房间/NPC的11PNG及完整模型不变，接入三件既存商品候选原图；资料显式开关、Esc、复位和ID0选择，未增加买卖/价格/金币库存。14原PNG、3原行与四旧整数画布独立核同，79本地相关测试通过；远端仅合成浏览器，后验另记。仍未进入原世界或认证原UI/同服。下一最高SCENE26回22域材料轮换；Stage A/B/wiki/R79与总体未知保持。


### SCENE26 — original pet action=1 bounded sprite-source rotation (2026-10-29)

[SCENE26 evidence and continuation](docs/continuity/STONEAGE-SCENE26-MATERIAL-ROTATION-20261029.md) and [finite source contract](docs/specs/STONEAGE-SCENE26-PET-ACTION1-R1.md): independently rederive 24 direction-sequences/80 frame positions/48 bitmap numbers from exact pinned R40 reports (zero newly obtained raw original material). Original source pixels/action meaning/identity/runtime/world remain unproven; no copyright assets included. Highest next is original-private-byte-qualified action=1 pixel observation only when pinned source material is actually available, otherwise rotate to a new source-qualified 22-domain game-content package. Stage A/B/wiki/R79/overall boundaries unchanged.


### SCENE27 — two further historical publisher screenshots (2026-10-29)

[SCENE27 continuation](docs/continuity/STONEAGE-SCENE27-GALLERY-SOURCES-20261029.md) and [historical screenshot custody](docs/specs/STONEAGE-SCENE27-JP2003-DEVELOPMENT-VISUAL-PROVENANCE-R1.md): two previously unverified 2003 Japanese development-gallery positions now have exact currently retrievable 640×480 JPEG identity, size, SHA256 and wrapper provenance from real GitHub Actions; no original images in Git. This is real historical screenshot **metadata**, not original client/world execution, certified game build, game-rule identity or visual interpretation. Return to source-qualified original-world material after bounded source observation; Stage A/B/wiki/R79 statuses unchanged.


### SCENE28 — Original TW1 action1 pet pixels actually recovered (2026-10-29)

[SCENE28 original source pixel provenance](docs/specs/STONEAGE-SCENE28-TW10-ORIGINAL-ACTION1-PIXELS-R1.md) and [date-specific continuity](docs/continuity/STONEAGE-SCENE28-ACTUAL-TW10-ACTION1-20261029.md): earlier private original Taiwan1.0 372626292B full client package was actually restored from private Library and rehashed; six original resource files verified; original Taiwan SPR segments for pet candidates 100250/251/252 exactly equal prior R40 spans, 24 action1 directional sequences and 80 ordered occurrences; **48 distinct TW1 original RD/bitmap pixel payloads actually decoded with two independent implementations** and 96 candidate-color private PNGs/one functional browser observer checked. Raw sprites/pixels remain in private Library, not Git. This is a genuine original-source image-recovery increment, NOT original native game runtime, official pet names, native palette, exact timing or server-world entry. NEXT original-source-qualified map + actor private observer only when source; Stage A/B/wiki/R79 and overall percent remain unchanged.


### SCENE29 — Original TW1 battle SAB and pet source pixels combined for private observation (2026-10-29)

[SCENE29 actual original material specification](docs/specs/STONEAGE-SCENE29-TW10-ORIGINAL-BATTLE-PET-OBSERVATION-R1.md) and [additive continuity](docs/continuity/STONEAGE-SCENE29-TW10-BATTLE-PET-20261029.md): from the retained authentic TW1 original-source P3H package, three 804-byte battle SAB files match exact original `battle_1.bin` slices. All 1,200 candidate-grid source references from 3 SABs resolve to 158 distinct actually decoded original ADRN/REAL images, each independently RLE checked (1,009,272 original palette-index pixels in total). A private interactive offline viewer joins these source-qualified battlegrounds and the original SCENE28 pet action=1 sprite frames; real Chromium verified 13 interactions and preserved duplicate original frames, with zero JS/network events. Observer and screenshot are retained privately. Public Git stores *only derived hashes and tile memberships, not the 400-cell map positions or game art*. Native palette, original battle render/selection, pet species, encounter and original executable world entry remain unproven; this is NOT native game execution. NEXT: exact-source-qualified Taiwan1.0 world DAT/map component, if available; otherwise return to the 22-domain material queue. Stage A/B/wiki/R79 and unknown overall percentage unchanged.


### 2026-10-30 — SCENE30：零售安装地图路线的有证据止点

[完整核验与下一包](docs/continuity/STONEAGE-SCENE30-TW10-FIELDMAP-BOUNDARY-20261030.md)：核对旧完整383项零售核心清单、七安装文件身份/13项既有解包结果，并实际逐SHA读取现存P3H的375项原运行文件（独立第二实现全核）；遗漏8项恰为安装支持，没有漏复制核心世界DAT。原EXE六处地图缓存指针与旧M/MC静态报告吻合；不重复下载同一盘、不把SAB当世界图。没有新增地图或原世界运行，公开仅派生与程序，25项本地检查通过；CI按后验记录。原CURRENT/Stage A/B/wiki/R79与总体未知保持。最高下一SCENE31回22域，限一个同源body100000动作2的八方向完整原帧观察，保留重复/未知动作名。


### 2026-10-30 — SCENE31：一组原人物八方向完整连续帧

[原件、实图与下一包](docs/continuity/STONEAGE-SCENE31-ORIGINAL-ACTOR-SEQUENCE-20261030.md)：同一已验TW1原件的body候选100000/动作码2，八方向各6帧、48原RD/125612索引像素，新增观察40个后续位置。两候选配色96PNG与96完整画面独立逐像素核同，已实际目视；私人离线观察包已保存，公开仅程序/数值/摘要。原图页浏览器被本地文件URL策略拒绝，未绕过；公开浏览器仅合成像素，按实际后验记录。38项本地检查通过，原动作名/FPS/身份及原世界未认证。下一SCENE32只取已有P3H三张原运行保留画面，核身份并真正目视其内容，不扩人物全动作/驱动/搜盘。CURRENT及Stage A/B/wiki/R79/总体未知保持。


### 2026-10-30 — SCENE32：纠正已阅原生黑屏被重列为未阅的待办

[旧证据联接、实际校核及进入世界下一步](docs/continuity/STONEAGE-SCENE32-NATIVE-FRAME-CONTINUITY-CORRECTION-20261030.md)：SCENE31把原source的false误作尚未阅图，遗漏2026-10-28独立目视后记。本轮同SHA原包三帧/两不同PNG经标准库PNG与Pillow完整RGB复核，仍为黑底/半形/光标，统计与旧97/104/97非黑像素全同；新增图像/原件执行0。P3I全局primary不认证原私有游戏图，P3C曾见有限登录布局但正确色彩/输入/世界仍未过，旧事实均保留。15项新检查通过，公开仅派生；最高下一SCENE33限定既有客户端—服务端配对资格核查，查现存mixed25顶层启动配置/两服务器程序，严格保留修改版与TW1官方的区别，不自动运行或重开驱动链。CURRENT/Stage A/B/wiki/R79/总体未知保持。


### 2026-10-30 — SCENE33：已有客户端／SAAC／GMSV静态配对资格

[原件、依赖、缺件与下一最小启动试验](docs/continuity/STONEAGE-SCENE33-WORLD-ENTRY-SOURCE-PAIR-20261030.md)：复用已保管mixed25父RAR，八目标原件5240403B逐SHA与旧清单相同；两服务端认证端口9200及认证值相合，五PE的有序DLL导入与独立objdump核同。程序／原配置／认证值未入公开Git，也未执行历史程序。说明2009日期、配置8.0及既有C/MIXED-MODIFIED客户端限定版本；三个空配置值、lockip缺引用、SQL后端和客户端本地路由仍OPEN。25项检查通过；原世界未进入。最高下一SCENE34先证明隔离环境回环／对外阻断，再仅限SAAC→GMSV启动和真实错误观测，不启动固定公网客户端，不扩驱动或补库链。CURRENT/Stage A/B/wiki/R79/总体未知保持，Actions按后验记录。


### 2026-10-30 — SCENE34：自编Windows回环实测通过，原服务端启动仍缺私有输入通道

[真实两次观察、失败保留与下一内容包](docs/continuity/STONEAGE-SCENE34-ISOLATED-BOOT-PREREQUISITES-20261030.md)：一次性Windows2025中，自编32位两进程在入/出站Block规则期间完成8字节回环；两次外部TCP canary为10013，清理后外部与回环恢复。首次10060不合格现场原样保留；修正Winsock异常就绪处理后独立重跑，实测规则中仅1.75秒，不冒称120秒。两原报告及ZIP来源摘要永久入Git。当前无私有原件传入runner的接口，因此SAAC/GMSV/客户端执行0、原握手/世界未建立，原boot仍BLOCKED。29新+25回归检查通过，最终CI按后验。按两包前提研究止点回22域，下一SCENE35先与已审遇敌链和WORLD01路线去重，仅交付有原文增量的一张modified包遇敌内容卡，不再扩隔离/传递/驱动helper。CURRENT/Stage A/B/wiki/R79/总体未知保持。


### 2026-10-30 — SCENE35：遇敌候选止步，轮换交付一条原NPC对白内容卡

[原件、止点与下一材料包](docs/continuity/STONEAGE-SCENE35-CONTENT-ROTATION-20261030.md)：已有遇敌全表链/WORLD01模型不重做；实际四表0注释但缺同二进制字段布局，未建立原服遇敌卡。转同mixed包一条显式NPC创建→唯一TownPeople模板→76B原对白；一个ASCII逗号所分两片段按22/52B保留，不能冒称运行分支或任务。原名/原文与三原文件已做成11122B私人静态卡并保存；公开仅摘要/释义/范围，源字节经CP950/Big5/iconv及RAR CRC核同，无JS/外部资源。28新+29回归通过，原世界未进入。下一SCENE36先对第15域既有骑宠资格/界面资料查重，有版本明确的新原文内容才交付，不扩同村NPC/遇敌/运行helper。CURRENT/Stage A/B/wiki/R79与总体未知保持，Actions按后验记录。


### 2026-10-30 — SCENE36：骑宠资料查重，一处官方页面图像引用实际取得

[原图来源、分时捕获与止点](docs/continuity/STONEAGE-SCENE36-RIDING-IMAGE-DELTA-20261030.md)：五份旧骑宠规则/计划不重算；核同Wayi计划原页19964B，实际取得其一处a/img关系中的两JPEG。页内300×225为2004捕获，目标640×480为2006捕获，不能倒称2003同构建。已实际目视室内NPC对话窗/確定取消，未认证赠虎实施或骑宠资格UI，新增骑乘规则0。两原JPEG和静态查阅页已私人保存，公开仅摘要/范围；原图无重绘，旧未取得标记按当时历史保留。29新+28回归通过；下一SCENE37先核既有成人礼/货运/卡坦任务材料，有原文增量才交付，不继续图像/骑宠helper。原世界未进入，CURRENT/Stage A/B/wiki/R79与总体未知保持，Actions按后验记录。


### 2026-10-30 — SCENE37：新手货运任务的一条玩家文献链

[内容、来源差异与下一包](docs/continuity/STONEAGE-SCENE37-QUEST-MATERIAL-DELTA-20261030.md)：查重成人礼／卡坦／通用货运与官方骑宠计划后，实际取得2004、2006标签两份署名玩家迁移稿98453B。恢复四列表行序，保留缺字标题；后稿内部重复两段、跨稿九步骤同文，不计独立见证。文献串联送红宝石、料理返程、展示1级布依至10／20／31级及成人礼后领虎；资格1级／30级以下、材料数字和限领范围未决，不把目标级当XP。官方计划实装和本体／永久／活动起源仍未证，原世界未进入。28新＋29回归通过，CI与源工件按后验。下一SCENE38查重既有宠物技能／训练条件，只推进新来源的具名内容；CURRENT／Stage A/B/wiki/R79／总体未知不变。


### 2026-10-30 — SCENE38：猛毒攻击的一条2001来源归属

[行来源、价目差异与下一包](docs/continuity/STONEAGE-SCENE38-SKILL-MATERIAL-DELTA-20261030.md)：既存CN2.0官方站托管技能页过去仅结构化加工／料理，本轮核同入口与正文151378B，从20011204捕获补猛毒行50%／5回合／4000的来源合同；新网页／技能名／学习资格均0。与旧未定年S2相同、和2004标签S1的30%／3／4400不同，保留冲突，不推补丁、作者／构建或S2日期。币种、实际扣款、MP、教学地点和毒损公式未证；不把R45字段改作学费。27新＋28回归通过，远端源重放／保管按后验。下一SCENE39查重战斗内容，只推进一条原文增量。CURRENT／Stage A/B/wiki/R79／原世界未进入／总体未知不变。

### 2026-10-30 — SCENE39 战斗来源查重与止点（无新增原战斗规则）

[有界来源对照、战败条件分层与下轮](docs/continuity/STONEAGE-SCENE39-BATTLE-MATERIAL-BOUNDARY-20261030.md)：已核大陆2.0的八指令/气绝和JSS2001战后HP1/条件性SP以及TW1原SAB静态可视资料，全部已由旧合同覆盖；没有新战斗来源/原程序执行。新增可审计的**禁止跨版推结算规则**矩阵；旧文献冲突不抹平，不能将台湾1.0候选战场图冒充真实回合。下一转22域17的`SCENE40-ITEM-ECONOMY-ORIGINAL-MATERIAL-DELTA-REVIEW`。原启动仍缺私有输入，Stage A/B/wiki/R79及总体未知状态不变。

### 2026-10-30 — SCENE40 玩家斧头目录的三原行交叉校核

[一个具名玩家资料源的取证、编码异常和界限](docs/continuity/STONEAGE-SCENE40-SINA-AXE-SOURCE-GATE-20261030.md)：Sina玩家投稿网页当前源36312B/SHA `d1fbdacdb50b9b31c0068e270d7026550ea6764f577cc9df3641d20df3432bfb` 已独立回放，10个异常GB18030原字节完整保留，目标三条无异常。小斧头65／莱伊卡Lv1斧头105／普普通通斧头260与旧mixed2.5保存商店ID0/4/10名称价格相合，玩家稿另列购买地；新增官方物品或同版交易事实0。首次失败和修正后run、ZIP/raw摘要及派生JSON均可追溯，原HTML不在Git。下一SCENE41转声音事件绑定查缺；原世界、Stage A/B/wiki/R79及总体未知保持。

### 2026-10-30 — SCENE41：2001标签玩家稿的11条BGM名字与TW1原音源核同

[SCENE41来源范围、实际音频字节身份与历史差异](docs/continuity/STONEAGE-SCENE41-AUDIO-PLAYER-FAQ-20261030.md)：17173玩家问答当前原UTF-8 HTML **50771B**／SHA `3c9af2d5456e52b184580ffa05b7039b7473bac475b32bace3b17caf810a63de`；页面标2001-06-14但无当年原始网页字节证明。11个`sabgm_*`名称/玩家用途标签准确对应原TW1 11份散装BGM文件名，新增原音源0、同版事件实参/世界执行0。2004玩家资料同名音轨用途有冲突，仅作为下一次原字节取证线索。首次编码/正则失败均保留，正确源CI/可重放派生JSON永久归档，原HTML/声音不公开。下一转第19域具名经典辅助工具版本能力，Stage A/B/wiki/R79/原boot及percent=null不变。

### 2026-10-30 — SCENE42：新浪早期辅助工具四行与八原下载href

[版本来源、原表、真实验收及边界](docs/continuity/STONEAGE-SCENE42-HELPER-LIST-20261030.md)：重读旧已归档的2003署期新浪5.0下载页**新增表级资料**：`SACHXP++5042`/`SACHMX5.00B8`/`SACHMX5.00FREEB1`/小明蓝暴自动猜谜器四行、每行各历史FTP+HTTP两href。原页69464B/SHA`812b32be4c9e9df45b956826c5a2a566d644ee8ef9acff5cfb69ab962a1b6a1d`已从网页原字节独立验证；4月3日署期与正文4月6日场次并列，**不据页签认软件发布日期**，不把新B8和旧R103的六月B9直接连成有证发布链。游戏本体/外挂实际运行0，原程序未下载。下一SCENE43转具名官方宠物图像；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、percent null不变。

### 2026-10-30 — SCENE43：2001华义2.0宠物网页两格的真实图片字节

[来源/限制及后验](docs/continuity/STONEAGE-SCENE43-CN20-PET-PIXEL-SOURCE-20261030.md)：旧已验官方网页第85格“瑞德宝”与第86格“瑞里西尔”分别引用原`84.JPG`、`85.JPG`，两原JPEG历史2001-10-26档案字节已真实取证，3753B/SHA`ba7b663a9445a0e32117eb768db33e991c566ddfac8ad1ae5d93bb7cf6372e31`及4494B/SHA`9951490cc47de15342fd88e671a8e54d1c6c33c7786655af4ffe4b93300f16b2`，RGB83×90单帧全解码，原HTML与JPEG不入公开Git。新独立视觉参考2、原客户端宠物/SPR对应0、真实运行0；首次页面2001-10-23与图像2001-10-26并非同刻。这是网页参考覆盖，下一SCENE44转22域/原世界真实可操作性材料；Stage A/B/wiki/R79、overall=null保持。

### 2026-10-30 — 用户确认单机原客户端素材优先（DD-OFFLINE-20261030）

现阶段**不再将联网、原SAAC/GMSV启动或原服登录当作还原地图/人物/宠物的前提**；改以已认证原客户端文件及现有SPR/ADRN/RD解码器，先形成可看的离线私人原帧、再一张真实拼图地图与人物宠物动作。新增`tools/stoneage_singleplayer_observation_kit.py`和[详细实施次序](docs/continuity/STONEAGE-SINGLEPLAYER-ASSET-FIRST-20261030.md)，不内置商业素材、不需要网络。未来新《石器时代》保持简体、单机、可保留网游式玩法深度，但单机自用不是原商业美术/音乐的版权许可。SCENE44外部截图[PR#58](https://github.com/chinaneedM/stoneage-rebuild/pull/58)已按新方向关闭、留分支作旁证；下一优先`OFFLINE-CLIENT-SAME-SOURCE-MAP-SCENE-O2`。原世界未进入、Stage A7 PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent null保持。


### 2026-10-30 — Offline original-pixel map O2 source gate (private)

[O2 bounded map observation continuity](docs/continuity/STONEAGE-OFFLINE-MAP-O2-20261030.md): an optional privately sourced scene21 map observer is now available alongside the TW1 original-animation offline kit. It verifies a preserved **mixed25** `1000.DAT`, 56 original candidate RD images and eight source-pixel-complete composites before producing a private scene viewer; the verified TW1 graphical byte-prefix relation does **not** certify a Taiwan 1.0 world map or native runtime. No original assets in this public repo. Same-source official TW1 O2 verification, client world execution, historical collisions/NPC interactions and overall percent remain OPEN; all old CURRENT history is retained.


### 2026-10-30 — Actual private O2 original-material replay and TW1 sprite observation

[Source-backed private O2 checkpoint](docs/continuity/STONEAGE-O2-ACTUAL-PRIVATE-SOURCE-20261030.md): the previously saved 2,745,658-byte SCENE21 private package was **actually recovered and fully hashed**; all 56 real RD payloads, 77 source cells, 85 placements, eight complete source-pixel composites and eight Chromium original-PNG states replayed. The independently recovered authenticated TW1 retail client was also rehashed; numeric original SPR group 100000 / direction 0 / action 6 yielded seven frame positions and two distinct bitmap records. A private, offline, explicitly cross-version observer was generated and Chromium-validated (modern movement/zoom/toggle; zero network). The proprietary originals and playable observer remain exclusively in the private Library, not public Git. The mixed25 map is **not** certified as a Taiwan 1.0 official deployed map; historical executable/game world, native collision/actions/NPC/battle remain OPEN. See derived [public acceptance receipt](research/recovered/STONEAGE-O2-ACTUAL-PRIVATE-SOURCE-ACCEPTANCE-R1.json). Stage A/B/wiki/R79 and unknown overall completion remain unchanged.


### 2026-10-30 — O4: privately validated original two-floor 1001 ↔ 1000 doorway and bounded NPC documentary observation

[O4 genuine-source two-scene continuity](docs/continuity/STONEAGE-O4-TWO-SCENE-ORIGINAL-OBSERVATION-20261030.md): four PRIVATE source archives were actually retrieved and fully rehashed. On original mixed25 map1000, R15/R21 overlap **54/54 original (cell,layer,image) placements** and **36/36 identical original PNG SHA identities**. Original preserved create blocks describe 1001(10,15)↔1000(63,99); one qualified 1000(63,103) TownPeople NPC references 143B preserved original CP950 text. A private single-page simplified-Chinese observer connects these two actual original-asset scenes with manual, source-coordinate constrained switching, static source text viewing, optional separately attributed TW1 numeric frames and no network/server; actual Chromium verified 67 original image loads, the two-way route and negatives, with **1,442,557 original map pixels exactly independently reproduced** outside modern overlays. Private observer and licensed-content-unknown original images/text stay in the user's Library. This is **not authenticated TW1 original map, original native movement, shop/dialogue execution or original executable game world**. Public [derived proof](research/recovered/STONEAGE-O4-TWO-SCENE-PRIVATE-ACTUAL-ACCEPTANCE-R1.json) and source-only negative tests remain version-scoped; Stage A/B/wiki/R79/overall unknown status unchanged.


### 2026-10-30 — O5：原室内地图与同保存版宠物数字帧的可操作观察

[O5 真正同源原材与私人浏览器验收](docs/continuity/STONEAGE-O5-ORIGINAL-MAP-PET-SOURCE-JOIN-20261030.md)：独立从私人 Library 重取 O4 双场景与 SCENE13 动作0资料，两原保存版 1001.DAT SHA 一致、七个共同室内原 PNG 逐字节 SHA **7/7 相同**。在原 O4 离线研究页面追加**单独的源宠物数字帧栏**，mixed25 数字组100250/251/252 共24方向动画、352帧位置/208原PNG，Chromium 208实际解码与352逐位置操作成功；O4 双向1001↔1000/NPC原静态文档路线仍可操作，0网络与JS错误。私人研究包已保存至 Library；公开仅[派生验收收据](research/recovered/STONEAGE-O5-SAME-CARRIER-PET-PRIVATE-ACCEPTANCE-R1.json)、源-only验证与CI。**未证**官方物种名/实体绑定、台湾1.0地图同版部署、原游戏帧速/原生碰撞/原服世界；O4之前1,442,557像素独立比对没有冒称本轮重跑。下一有限核同源 entity→graphic/SPR 字节；没有原资料则止点回22域。Stage A7 PARTIAL+2 OPEN/B、wiki GATED/R79暂停/总体percent=null不变。


### 2026-10-30 — O6：已验证原素材的私人引擎无关导出

[O6 原图独立目录与范围](docs/continuity/STONEAGE-O6-PRIVATE-ENGINE-NEUTRAL-RESOURCE-PACK-20261030.md)：O5 已归档的私人原图被本轮真正读回并导为 **275 个 PNG + 4 个版本化 JSON/私人说明**：保存版1001的51原 tile/构件图及27次源位置，保存版1000的8张有界合成候选、mixed25的208宠物原图/24方向动画/352源帧位置、另隔离的TW1参考人物7帧与mixed25参考1图。全部原 PNG 逐完整SHA与Pillow尺寸/解码核验；私人ZIP280成员/2,146,298B保存于用户Library，不进入公开Git。新增[公开哈希/边界收据](research/recovered/STONEAGE-O6-PRIVATE-ASSET-EXPORT-ACCEPTANCE-R1.json)、只读私人SHA绑定导出工具及16项全合成否证测试；不能把保存版地图1000的8张 composite 冒称完整 tile 主表，不能把数字SPR当宠物物种、客户端原世界或官方TW1部署。官方同构建宠物实体master仍缺；暂不扩大同一图形helper，下一转有原始材料的22域重要业务包。Stage A7 PARTIAL+2 OPEN/B、wiki GATED/R79暂停/总体percent=null不变。


### 2026-10-30 — O7：武器店三件原物品的说明属性与原字段互证

[O7 原保存版1001武器店源资料联接](docs/continuity/STONEAGE-O7-SHOP-ATTRIBUTES-AND-SOURCE-BOUNDS-20261030.md)：重读私有O6/SCENE24/25三个全哈希来源，原`itemset.txt`前三商店ID0/4/10与原描述中的攻/防/敏数值分别为`+9/-3/-3`、`+7/-2/-2`、`+14/-5/-5`，且都与原第37—42列各双份值精确一致；原价数值字段65/105/260，非已执行交易价格。三原Palet1候选PNG 3/3逐SHA相同，原 imagenumber 与+76别名物理图号仍**只是静态候选**。关键坐标反例：真实保存版店员1001(17,13)在O6室内取样 x7—13 **以外**，不能冒称已走到店员或执行原商店。私人O7 ZIP287成员（承袭O6原280成员+3PNG+4资料）、278PNG/2179790B已保存并二次回读；Chomium内存同原图测试352源帧/208不同原图和三商品实绘/两出口人工路线成功，管理员拒绝file://导航，未声称原版EXE或用户本机文件直开。公开仅[来源数字收据](research/recovered/STONEAGE-O7-SHOP-ITEM-STATS-AND-SCENE-ACCEPTANCE-R1.json)、审计代码和负例；官方同版地图/原交易/宠物身份仍未证。下一转22域新原实物，勿继续无来源交互helper；Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79暂停、percent=null不变。


### 2026-10-30 — O8：保存版武器店柜台5×5有据原图已补入离线双窗口

[原图范围、五格重叠和私人浏览器验收](docs/continuity/STONEAGE-O8-1001-SHOP-ORIGINAL-CROP-OVERLAP-20261030.md)：从已存私人SCENE14原件重新读原`1001.dat`及R14原图，逐源格核(13…17,13…17) **25地块+5构件=30出现/0缺图**，与O7出口窗口原DAT全SHA同；**7/7同号原PNG完整SHA/字节相等**、x13/y13…17 **5条(cell,layer,map_id)重复**，去重后共52条实际原保存版图块布置。新增只需3幅原构件PNG及1幅原店员5863候选PNG；在原NPC坐标1001(17,13)可实际目视有来源的柜台场景，店员原候选图默认关闭、只手动叠加，不伪称原NPC渲染/买卖/碰撞。O8私人ZIP297成员/282原PNG、原O7 287成员逐字节不变，上传用户Library并二次原样回读；Chromium在内存以同SHA原图测试柜台10图片/店员1/商品3、两窗口源坐标人工跨越、两向原出口手动参数、352宠物源帧/208不同原图，JS错误与外部请求0；一次过大data页面导航ERR_ABORTED已保留、改set_content验收，`file://`用户机直开未证。公开仅[源-only收据](research/recovered/STONEAGE-O8-ORIGINAL-SHOP-CROP-ACCEPTANCE-R1.json)与数字变异测试，原美术不公开。下一回22域找新内容/新原始来源，不扩不必要商店helper。官方台湾1.0地图部署、原版游戏世界/原生碰撞、物种与真实交易仍OPEN；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、percent=null不变。


### 2026-10-30 — O9：从原客户端资源恢复1001室内完整30×30可见场景

[完整原字节与独立像素验收](docs/continuity/STONEAGE-O9-FULL-ROOM-OBSERVATION-20261030.md)：原保存版1001.DAT两来源逐字节相同，初代TW1原ADRN/REAL/SAP重新整SHA鉴定，完整30×30含**107原地块+26原构件=133次源图引用、38幅不同RD**，O8局部30元组完整一致，新增103处原可见放置，38RD全部解码、独立NumPy双层/全景逐像素一致，O8原10PNG字节同；新20 PNG只私人。现代候选全景647×617实际目视，非原游戏画面/原生遮挡。私人O9 ZIP328成员/3969208B，旧O8 297成员未动，Library上传后全包SHA回读一致。Chromium原图内存页面检验定位/缩放与0HTTP，file://被管理员阻止，未声称用户本机直开或进入原客户端地图。公开仅派生原源收据及负例。O9到此止点，下一 **O10回22域查新原地图/宠物/音频/任务内容**；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、percent=null不变。


### 2026-10-31 — O10：原保存版村庄1000扩大到19×25格的真实图块候选全景

[O10新地图原字节恢复与数字证据](docs/continuity/STONEAGE-O10-ORIGINAL-VILLAGE-EXTENDED-20261031.md)：完整已保存原1000.DAT(160×160)源位x55—73/y89—113共475格；实有**492原地面/构件布置、183种原图形RD**，相对旧O4局部窗口新增407次图块布置与128种此前该窗未见图号。183个图号在已认证TW1原ADRN均唯一，183原RD实际字节经双实现索引/图色解码、PNG回读与独立NumPy完整1408×1055三层RG​BA一致；现代等角候选画面已目视，不冒称历史原游戏截图。源NPC点1000(63,103)及出口1000(63,99)与O9的1001室内可静态对照；不能推同版官方部署、碰撞、真实行走/交易。私人O10 ZIP888成员/7764347B，O9原328成员全部字节不变，183RD/原80B记录与原DAT仅私人，整ZIP CRC/全源/图像回读通过。**本轮Library自动上传因container session expired未成功**，只提供当前会话已验附件，不能写为Library已归档。Chromium使用等字节原图内存页面8项实际成功，file://受管理员阻止保留失败。公开只留源哈希、O10反例及专用Actions；O11转实体/动作/音频事件及任务交互，停止无界扩画图。Stage A7 PARTIAL+2 OPEN，B/wiki GATED、R79暂停、percent=null不变。


### 2026-10-31 — O11：台湾1.0原SPR动画字段与两种声音索引候选

[O11原源动画与声音的有限关联](docs/continuity/STONEAGE-O11-NATIVE-PET-FRAME-AUDIO-20261031.md)：从原TW1 SPR完整记录中取证三个数字组的24条动画/352原帧位置；对旧保存版208幅数字图重新用台湾1.0 ADRN/REAL源RD独立解码并逐RGBA同一。原帧末尾16-bit数值73/10000保留，73对应原声音地址表零基/一基两种**尚未确认的候选索引**，不称已经确认的宠物叫声、技能或事件；浏览器只是私人手动逐帧/手动试听，并不是旧客户端执行。208原图和两段原WAV仅私人Library保存，公开仓库只有来源派生数字、SHA、24项反例与Actions。原世界未进入，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、percent=null。下一O12回22域寻找能够证明同版事件触发/实体名称的原始主表或编译调用路径，缺件有界停止。


### 2026-10-31 — O12：同版原客户端编译声音编号与资源表不同

[O12原原件声音编号静态取证](docs/continuity/STONEAGE-O12-NATIVE-SOUND-NAMESPACE-20261031.md)：认证TW1原`sa_3.exe`与`data/soundaddr_1.txt`实物，113个原EXE明文SFX、11 BGM、114地址表，102组编号→路径原机器指令三联+独立objdump同一；另11原文件路径使用其它赋值形式未补号。原编译期编号73→`sae_23.wav`，但声音地址表零基73→`sam_18.wav`／一基73→`sam_17.wav`。三个命名空间不等价，O11宠物帧字段73→真正播放编号/事件**仍未证**；源原件未运行、旧世界未进入，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、总体percent=null。源字节仅私人，公开保留102完整派生地址/路径和22负例。下一O13回实体NPC/任务/技能有据材料，不无限扩静态声卡/音频解析。


### 2026-10-31 — O13：原TW1像素与另版本宠物名称的来源分隔

[O13 有界来源审计](docs/continuity/STONEAGE-O13-SOURCE-SEPARATED-NAMED-SPRITE-20261031.md)：私有初代原盘及O11原像素完整SHA再核，三原数字组100250/251/252的动作0共24序列、352有序帧、208原PNG与后期mixed25保存版七条具名模板分版并列；原名烏力／烏力烏力／烏力斯坦仅属后期社区保存版，不认证官方台湾1.0物种身份。私人简体离线观察HTML真实Chromium逐帧、方向、原模板位置开关通过，浏览器0 JS错误/0外部网络；原HTML及原图不公开。O12帧73与三种声音编号命名空间不擅联。公开仅源派生O13收据和来源隔离验证；原TW1同构建具名宠物主表仍缺，原客户端世界仍未进入。下一回22域寻找真正新增具名原件，Stage A 7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79暂停、overall百分比null不变。


### 2026-10-31 — O14：2003玩家投稿中的SOT C/D双路线及“活动”归类边界

[来源隔离的任务合同](docs/continuity/STONEAGE-O14-SOT-CD-2003-PLAYER-QUEST-20261031.md)：现存新浪2003-05-29两篇玩家投稿分别记载萨伊那斯环岛C/D资格、各12个顺序检查点、答题与检查石、完成位置及候选奖励。内容新增为**玩家攻略层**24项可追溯数据，未证明TW1或原服务器同版运行。原文“环岛活动”同时写可重复解，不能归作已证限时节日活动；原HTML字节/源SHA未知，不伪称已取得。原游戏世界未进入，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent null不变。


### 2026-10-31 — O15：SOT旧玩家稿与2021二次转载的坐标及结束点差异

[两套不可合并的来源证据](docs/continuity/STONEAGE-O15-SOT-REPOST-DIVERGENCE-20261031.md)：对O14已归档的2003新浪两条SOT玩家稿逐24检查点和2021转载对比，观察到20处坐标文本、6处答案文本不同；C领取地“萨姆吉尔／卡鲁它那”不一致、2021“目前并不能解”不能倒写成2003原版运行事实。旧O14原JSON和CURRENT全文保持不变，原本体/同版服务器/限时活动身份仍未证。下一轮停止SOT同源循环，转新增原资料或受控场景。Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent null不变。


### 2026-10-31 — O14–O15 主线验收与来源异文止点

[真实三阶段Actions及下一包](docs/continuity/STONEAGE-O14-O15-POSTMERGE-ACCEPTANCE-20261031.md)：O13/O14/O15各自已观测主线11/11成功；O14、O15各候选13/13通过。O14保存2003网友投稿的SOT C/D 24项路线，O15另存2021转载20处坐标与6处答案文本差异及C领奖村矛盾。不将转载覆盖旧文本，不把“活动”冒称限时，也不推原TW1同服规则。完整CURRENT及所有原证据保留；下一O16转22域增量内容，整体percent null。


### 2026-10-31 — O16：台湾1.0原战斗资源233段混排和2296原图号实物检验

[O16源实物解析与私人可见像素](docs/continuity/STONEAGE-O16-TW10-BATTLE-SAB-PALETTE-INTERLEAVE-20261031.md)：从保留的原台湾1.0 P3H完整原件整SHA复核：battle_1.bin / battletxt_1.txt 的233段中包含218张SAB战斗图及插在200/201之间的15张SAP调色板，错误固定步长会偏移10620B。218×400格共87200引用、2296原bitmapID同版ADRN唯一；2295 RD双算法一致，bitmap6729一个解码边界使battle181像素不完整，严格217张全部源RD可解，未认定原本体世界/实际运行颜色。12场景真实原PNG在私人离线页可切换，原图不公开。O17优先真实原大世界DAT或具名NPC/任务同代文件，不扩无界SAB helper；Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暂停、overall_percent=null。


### 2026-10-31 — O16 独立原件复验与证据守卫修复

[复验和续接记录](docs/continuity/STONEAGE-O16-INDEPENDENT-ACCEPTANCE-20261031.md)：重新读取372626292B既存原包，233/233封装切片与散装原件同一；2295图块两算法像素一致，6729在battle181仍溢出一像素，保留为OPEN。修复原校验放过缺失边界、REAL/ADRN身份、后续调色板SHA及缺预览收据的问题，新增只读全源复验入口。原379成员研究包仅有savedata.dat，不据此推断完整零售载体/服务器不存在地图。CURRENT完整原blob不变，未重跑原图浏览器或原游戏。NEXT O17优先从已认证完整载体/实际地图来源寻找新增早期世界数据，禁止把无地图的研究子包当原发行全包。


### 2026-10-31 — O16主线通过，O17完整载体库存查重

[主线终验及地图取证止点](docs/continuity/STONEAGE-O16-INDEPENDENT-ACCEPTANCE-20261031.md)：PR74候选14/14 Checks、main a5709c76的11/11 Actions实际成功，原CURRENT完整blob不变。本轮把375个保存原成员逐SHA对完整383核心文件库存，8个省略件全是安装支持文件，既存完整光盘库存普通世界地图为0。下一O17查真正新增早期地图/缓存/实体原件，不重复下载同盘、不把savedata当世界图。未进入原世界，Stage A/B/wiki/R79及overall_percent=null不变；收据自身CI另据实际观察。


### O17 已明确下一原素材：1003地图候选

[有界地图载体排序](docs/continuity/STONEAGE-O16-INDEPENDENT-ACCEPTANCE-20261031.md)：四已存样本的原目录并非均无世界DAT；TW1/CN5为0，claimed8.5有45条、mixed25有1011条文件名，其中空/微小文件不能算有效图。最高NEXT具体为已有2003双时点和mixed25整SHA一致的1003.DAT：先取精确原成员、核同源图块覆盖，最多一份30×30现代候选场景。后代宠物店名不晋升初代官方身份；缺源有界停止。该场景尚未新绘，Stage A/B/wiki/R79/percent未知不变。


### 2026-10-31 — O17 actual map1003 file + TW1 original graphics observation

[O17 bounded original-source observation](docs/continuity/STONEAGE-O17-MAP1003-SOURCE-PIXEL-20261031.md): actually re-read the private mixed25 RAR and exact 5408-byte map1003.DAT SHA. Of 900 cells there are 107+27 actual visual placements and 38 distinct numeric aliases; all 38 are unique in the actually rehashed TW1 original ADRN, and 38 real TW1 RD source pixels were independently decoded. A **695×665 modern visual candidate** has independently equal full RGBA. Actual original map bytes and 38 TW1 RD and PNG remain private; source-only derived receipt/tests in Git. **The mixed25 ADRN/REAL companion extraction is blocked** by a RAR filter and was not freshly read, so crossversion pixel identity is not newly independently qualified. Historical original-client world, runtime palette, collision, official map name and same deployed build remain OPEN. Next finite **O18 same-period map1003 named NPC/quest/content source** from 22-domain queue if actual original member exists; otherwise stop and rotate. Stage A/B/wiki/R79 and total percent unknown unchanged.


### 2026-10-31 — O18: same-carrier server map1003 and original pet-shop text

[Actual same-carrier original source join](docs/continuity/STONEAGE-O18-MAP1003-SOURCE-NAMED-CONTENT-20261031.md): private preserved mixed25 RAR directly supplied the **3644B original LS2MAP server floor 1003**, whose **two 900-cell original tile/object planes exactly equal the already recovered client's map1003.DAT planes (1800/1800)** and whose original CP950 label reads “薩姆吉爾的寵物店|0”. Three original NPC filenames refer to map1003 positions with source text for pet information, pet shop services, and pet-skill teaching. Original 7-member private ZIP was SHA/CRC verified; public Git holds only [derived evidence](research/recovered/STONEAGE-O18-MAP1003-SAME-CARRIER-NAMED-CONTENT-R1.json) and source-only CI. **Do not retroactively assign the later source name to 2003 or TW1 official service; no runtime NPC creation pointer, native shop or original world entry verified.** NEXT O19: one source-qualified 1003 NPC creation reference or exact stop. Overall completion remains null; Stage A/B/wiki/R79 unchanged.


### 2026-10-31 — O19 actual original petshop create source accepted; NEXT O20

O17 [PR #75](https://github.com/chinaneedM/stoneage-rebuild/pull/75), O18 [PR #76](https://github.com/chinaneedM/stoneage-rebuild/pull/76), and O19 [PR #77](https://github.com/chinaneedM/stoneage-rebuild/pull/77) have all merged to `main` at `1192fbbc`, `8b4bdf60`, and `5b3d52be` respectively. Original source files and previews stay private, with derived reports and guards in `research/recovered/STONEAGE-O17-*`, `STONEAGE-O18-*`, and `STONEAGE-O19-*`. Source-only branch Checks were **14/14**, **14/14**, and **4/4** successful; corresponding postmerge main checks **11/11**, **11/11**, and **1/1** successful. The full `docs/CURRENT-STATE.md` blob is unchanged at `20050acf279a01555ab06a381dfcdc936bd381a6`. O19 adds one exact original `shop_m.create` floor1003 coordinate (12,13) static reference to original `ps_1003_12_13`; **does not** demonstrate original game NPC execution, shop transactions, 2003/TW1 same deployed release, or source-native graphics/occlusion.

**Highest NEXT: O20 bounded same-room private offline visual / one graphic16038 source-qualified observation** using the already recovered map and creation block, with original-source bytes, modern candidate rendering and unproven original runtime behavior sharply separated. If same-build source/runtime is unavailable, retain exact missing evidence and rotate; do not expand indefinitely into helper scaffolding. Stage A = 7 PARTIAL+2 OPEN; B/wiki GATED; R79 paused; overall_percent=null.


### 2026-10-31 — O20 original NPC 16038 alias and offline pixel observer

[O20 preserved original one-NPC scene qualification](docs/continuity/STONEAGE-O20-MAP1003-ONE-NPC-ORIGINAL-PIXEL-20261031.md): after verifying the O17–O19 full original carrier source SHA, a **single original** `1003(12,13)` petshop `shop_m.create` key `graphicname=16038` uniquely resolves by Taiwan1.0 original ADRN logical alias to **physical bitmap 5884**, 36×86 and 1,885B exact RD. Physical bitmap-number 16038 is a different original record, explicitly preserved as a negative namespace counterexample. The source RD was actually read from authenticated TW1 original REAL and decoded by two independent algorithms. The modern, source-scoped observer adds this one original-pixel candidate to the 695×665 preserved mixed25 map reference, with separate original-byte/provenance and modern-overlay labels. Python pixel overwrite and actual Chromium full Canvas RGBA (real embedded original PNG, not synthetic color blocks) match both before/after one candidate NPC; browser zoom, marker and reset work with zero JS errors/HTTP requests. Browser `file://` navigation is policy-blocked in the present environment, so end-user local open is not falsely certified. Original binaries, image bytes, private HTML and CP950 source dialogue are in a verified private ten-member ZIP, never committed publicly. Public [derived O20 acceptance receipt](research/recovered/STONEAGE-O20-MAP1003-NPC16038-ORIGINAL-PIXEL-OBSERVER-R1.json) and source-only tests/workflow have been merged in [PR #78](https://github.com/chinaneedM/stoneage-rebuild/pull/78) (candidate 4/4 checks successful). The original game, native spawning/animation/color/occlusion, collisions, transactions, and same-deployment identity for TW1/2003/mixed25 all remain unverified.

**Highest NEXT O21 — bounded 22-domain material rotation.** After O17–O20, stop expanding the same 1003 floor/graphic helper and prefer a new independently source-qualified material/behavior in the existing 22-domain portfolio; only reopen this NPC when original same-build selector, event/runtime or original-server material is actually recovered. Stage A 7 PARTIAL+2 OPEN, Stage B/wiki GATED, R79 paused, overall_percent=null. Original full `CURRENT-STATE.md` blob `20050acf279a01555ab06a381dfcdc936bd381a6` unchanged.


### 2026-10-31 — O21 bounded original encounter → two named later-pet templates → 24 original TW1 pixels

[Source-qualified O21 finite world content](docs/continuity/STONEAGE-O21-ENCOUNTER-TWO-NAMED-PET-PIXELS-20261031.md): original preserved mixed25 encounter floor100 first source zone links group88→enemy119→template113, named 昆伊, numeric IMGNUMBER100297, and group91→enemy122→template114, named 凱比特, IMGNUMBER100298. Two matching numbers are independently present in the authenticated **separate Taiwan1.0 original** SPRADRN/SPR, each with 56 animations; **24 selected direction0/action0 original RD frames** (8/16), 24 independently decoded PNG and real Chromium 24/24 full canvas RGBA comparisons passed. This is **not** an original official TW1 species roster, same-deployed-build observation, original FPS, encounter trigger or original client runtime. Private original bytes, art and source viewer stay outside Git; only derived hashes / boundary negative tests are public. Highest NEXT **O22 one bounded pet skill or item content source join** with actual preserved source bytes; if no new concrete game content, rotate 22 domains. Stage A/B/wiki/R79 unchanged, overall percentage null.


### 2026-10-31 — O22 one original later-preserved named pet skill source chain

[O22 exact original source-only content link](docs/continuity/STONEAGE-O22-ONE-PET-SKILL-SOURCE-20261031.md): independently re-read five preserved mixed25 server source files. Encounter floor100/area21→group1230→enemy2250→enemybase template29 (CP950 白唬)→original PETSKILL slot3 numeric 61→original petskill table row61 named 猛毒攻擊, original callback-text PETSKILL_StatusChange. Private original five-row archive full SHA/CRC verified; public Git contains only derived IDs, hashes and negative tests. This **does not** execute original battle, guarantee poison chance/duration, authenticate TW1/JSS1999 same skill, or establish original world entry. Highest NEXT O23 rotate to genuinely new sourced battle/item/scene content; avoid unbounded skill-index work. Stage A/B/wiki/R79 and total percentage remain unchanged.


### 2026-10-31 — O23 original three consumable items and six actual TW1 source graphics

[O23 bounded source item/pixel observation](docs/continuity/STONEAGE-O23-THREE-CONSUMABLE-ORIGINAL-PIXELS-20261031.md): actual original 3392473B preserved mixed25 `itemset.txt` was re-extracted and whole-SHA verified; three original 94-column IDs **1234 小塊肉**, **1247 治療中毒的肉**, **1530 復活藥(100)** each have a distinct original static callback and imagenumber24008/24043/23021. Separately authenticated TW1 original ADRN +76 aliases uniquely map to physical 6926/6961/6557; direct physical 24008/24043/23021 are **different real original RD blocks**. All six actual TW1 original RD pixels decode in two independent algorithms; modern original-PNG Chromium Canvas **6/6 full RGBA** exactly agrees with independent Python; mode/zoom/reset all passed. Private 25-member ZIP SHA/CRC verified; no copyrighted original source bits/PNG/HTML in public Git. **Not** official same-deployment item identities, native image-selection proof, game-use effects, original client/world, or actually paid shop cost. NEXT O24 rotate to one genuinely new battle/map-event source-visible content, otherwise rotate 22 domains; Stage A/B/wiki/R79 unchanged, percent=null.


### 2026-10-31 — O24 source-qualified two-town original NPC item event

[O24 preserved two-town static event source](docs/continuity/STONEAGE-O24-TWO-TOWN-ORIGINAL-EVENT-SOURCE-20261031.md): independently re-read the saved mixed25 original RAR: two NPC create blocks (彌生 floor2000 (55,92), 日美子 floor1000 (57,124)) directly refer to two original event scripts, each with three event branches; original same-carrier itemset identifies item IDs 2414 不可思議的貝殼 and 2415 仙尼亞的花. Original map2000.DAT fully re-extracted; map1000.DAT fresh RAR extraction failed CRC, so original full map bytes were instead independently re-read from earlier CRC-verified SCENE21 private ZIP matching RAR member length and CRC. All full original script/map/item bytes remain private; public [O24 derived witness](research/recovered/STONEAGE-O24-TWO-TOWN-EVENT-SOURCE-R1.json) and tests pin source SHA, branch conditions, map coordinates, and negative evidence boundaries. **Static script references only**: no native event execution, no original world entry, no official TW1/JSS1999 deployment and no proved timed event. Full original CURRENT blob remains preserved. Highest NEXT **O25**: if already authenticated source pixels can be retrieved, bounded two-actor graphic candidate; otherwise rotate 22 material domains. Stage A 7 PARTIAL+2 OPEN, Stage B/wiki GATED, R79 paused, overall_percent=null.


### 2026-10-31 — O25 two original TW1 NPC pixel alias candidates

[O25 source-verified original pixel candidate receipt](docs/continuity/STONEAGE-O25-TWO-NPC-ORIGINAL-PIXELS-20261031.md): actual preserved TW1 P3H whole ZIP, ADRN and REAL SHA/CRC re-read; later mixed25 source NPC `graphicname=16027/16030` each has one source-candidate alias in both exact full TW1 and mixed25 ADRN, resolving to physical TW1 bitmaps `5873/5876`. Four actual TW1 original RD images include two real crossversion avatar candidates and **two distinct, wrong same-number physical controls**; four whole pixel-index outputs from two independent decoders and palette-1 modern candidate PNG roundtrips all match. Original art, full RD/ADRN, PNG and contact sheet stored privately in the reread-verified 15-member Library ZIP; only source-derived hashed metadata, mutation tests and continuity are public. No native selector, original TW1/1999 NPC identity, original game/world execution, runtime palette/scene or quest execution is claimed. Full historical CURRENT source blob remains unmodified; Stage A 7 PARTIAL+2 OPEN, B/wiki GATED, R79 paused, overall_percent=null. Highest NEXT **O26 rotate 22 domains for a new sourced game interaction/content** rather than scaling this NPC bitmap subtask.


### 2026-10-31 — O26 real-source two-town private interactive observer

[O26 private original-pixel two-town interaction](docs/continuity/STONEAGE-O26-TWO-TOWN-OFFLINE-OBSERVER-20261031.md): using existing original sources directly, produced two real-original-resource 13×13 local map candidate images (map1000 176 references/101 aliases, map2000 171/56; 157 unique authenticated TW1 original RD aliases), added the two O25 original NPC candidate PNG, and an actual modern Chromium-tested, self-contained Chinese offline HTML for movement, script-backed dialogue and strictly simulated item exchange (ID2415↔2414). Private 8-member deliverable uploaded to Library and independently re-read SHA/CRC. Public Git holds only [bounded derived evidence](research/recovered/STONEAGE-O26-OFFLINE-TWO-TOWN-MATERIAL-R1.json) and this additive checkpoint; no original graphics/dialogue/maps published. This is **not actual historical client/server world entry, original battle, verified collision/warp, or historical item-transfer execution**. Full CURRENT preserved; Stage A7 PARTIAL+2 OPEN, B/wiki GATED, R79 paused, overall_percent=null. **Next O27**: one different evidence-supported gameplay/content outcome, not repeated bitmap/index scaffolding.


### 2026-10-31 — O27 actual original battle SAB + two TW1 animated pet sprite groups

[O27 private source-backed battle visual observer](docs/continuity/STONEAGE-O27-ORIGINAL-BATTLE-OFFLINE-OBSERVER-20261031.md): from the existing whole-SHA-verified original Taiwan v1.0 P3H client, directly reconstructed source battle SAB0 (20×20 cells, 73 unique original tile RD), source SPR100297/100298 raw direction0 actions0/1/2 (52 ordered original frame positions, 39 distinct actor bitmaps), and a **real-original-image Chromium-tested offline interactive Chinese battle observation HTML**. It provides two animated actors, manual frame stepping, selectable raw actions, loop preview, side-by-side source action display, pause/reset; 0 JS errors and 0 external requests. Original complete background RGBA matches independently archived SCENE29 digest. Later mixed25 named encounter 昆伊/凱比特 is only numeric/crossversion candidate, **not** proof of TW1 native species, actual encounter, damage/combat rules or gameplay execution. 58 private-source members/ZIP SHA checked after Library upload/download; all original source art and full HTML stay private. Public [derived source report](research/recovered/STONEAGE-O27-ORIGINAL-BATTLE-PIXELS-R1.json). Full CURRENT unchanged; A7 PARTIAL+2 OPEN, Stage B/wiki gated, R79 paused, completion percent unknown. **NEXT O28** distinct source-supported user experience only; no repeated battle asset expansion.


### 2026-10-31 — O28 original TW1 pixel + later descendant source capture experiment

[O28 source-qualified private pet capture experiment](docs/continuity/STONEAGE-O28-CAPTURE-SOURCE-INTERACTION-20261031.md): reuses the already verified TW1 original pixel SAB0 and animated SPR100297/100298 from O27, with one **different gameplay experience**: original-three-descendant **capture score, target eligibility, strict RAND(1..100) < WorkGet, sleep/HP effects, version-conditional item input, five carried-pet slots and post-success capacity failure**, all visibly operable in a single private offline Chinese HTML. The **capture mechanics are later-descendant evidence, NOT verified Taiwan1.0/1999 commercial mechanics**; all values and named species joins are explicitly illustrative. Actual Chromium loaded real original images; 125 browser JS/Python arithmetic parity cases, 7 edge cases, 11 real UI interaction checks, zero browser JS/network errors. Five-file original-image ZIP stored privately in Library and re-materialized exact SHA/CRC; public [O28 derived provenance](research/recovered/STONEAGE-O28-PET-CAPTURE-ORIGINAL-PIXELS-R1.json) only. This is **not original game execution, combat damage, original item master, complete pet birth/growth or historical save**. Unmodified complete CURRENT, Stage A 7 PARTIAL+2 OPEN, Stage B/wiki GATED, R79 paused, overall_percent=null. **NEXT O29** direct source-backed navigation/game-world outcome instead of increasing observation scaffolding.


### 2026-10-31 — O29 original DAT continuous world walk and source-backed 1000↔1001 doorway

[O29 source-backed continuously navigable private original-resource route](docs/continuity/STONEAGE-O29-SOURCE-WARP-CONTINUOUS-WALK-20261031.md): directly recombines actual preserved mixed25 complete maps1000/1001 and the SHA-checked original `warp_y.create` two-block source coordinates 1000(63,99)↔1001(10,15), rendered with 257 actual source-authenticated TW1 original RD alias images (1,529 source map cells inspected). Browser-verified single-file Chinese offline experience walks with following camera from source NPC vicinity 1000(57,125) to actual static doorway; only a player at the original source coordinate may manually execute the modern transition, then walk to the source shop NPC at 1001(17,13) and inspect three previously authenticated stock rows. Reverse doorway, keyboard, reset and layer controls verified with actual original pixels and zero JS/network errors; O26 neighborhood image RGBA replay independently matches byte-for-byte. 9-file proprietary original-asset/HTML archive preserved **privately** in Library and SHA/ZIP CRC reread passed. Public only [derived evidence](research/recovered/STONEAGE-O29-SOURCE-WARP-CONTINUOUS-OBSERVER-R1.json); no raw art, scripts or map payloads. **No historical client/server started; pathfinding, original collision/warp event execution and cross-era identity remain unproven.** Full CURRENT unchanged; Stage A7 PARTIAL+2 OPEN; Stage B/wiki gated, R79 paused, overall percentage unknown. **NEXT O30** actual source-supported world collision or one new game interaction; avoid growing camera tooling.


### 2026-10-31 — O30 actual-source paired auto-overlap Warp offline observer

[O30 original-source walk-entry/return witness](docs/continuity/STONEAGE-O30-SOURCE-OVERLAP-WARP-20261031.md): private O29 original DAT/TW1 pixel observer now automatically transitions at independently sourced paired coordinate on **new walk-entry** (1000(63,99) ↔ 1001(10,15)), avoiding instant bounce on arrival; manually W still available as a comparison control. Original later-descendant WarpWatch supports walk-overlap as a source candidate, **not** historical TW1 runtime observation. Original DAT event 49155 is shared by adjacent non-warp cells and **not** a reliable marker or native collision proof. Real Chromium144, real embedded source-art HTML, 18/18 visual/interaction checks passed, no JS errors/external requests. Private 10-file 2,668,881B ZIP SHA256 `84e883cd57f2b77100ad7a82ecbf5957b5199ff10ed6b0dbdf9141be882d09fa` uploaded to personal Library and full SHA roundtrip verified. Public Git only contains [derived numerical receipt](research/recovered/STONEAGE-O30-OVERLAP-WARP-INTERACTION-R1.json), source-boundary tests and continuity notes, not copyrighted image, DAT or HTML bytes. Highest NEXT **O31**: check concrete same-carrier collision payload for this small path only; if missing, bounded stop then rotate to different gameplay material. Still not original EXE/server, native collision, official TW1 deployment or original trading. Stage A7PARTIAL+2OPEN, B/wiki GATED, R79 paused, overall_percent=null. The original 2,708,031B CURRENT blob remains intact.


### 2026-10-31 — O31 original three-entry/two-return source doorway complete

[O31 five actual original-source later-preserved Warp create blocks](docs/continuity/STONEAGE-O31-FIVE-DOORWAY-SOURCE-20261031.md): independently re-read the already private verified source `warp_y.create` and source maps1000/1001. **Three original village door coordinates** 1000(63,98),(63,99),(63,100) lead to (10,15),(10,15),(10,16), and **two shop door coordinates** 1001(10,15),(10,16) return to (63,99),(63,100). Not a bijective door pair. Upgraded the same source-art Chinese offline observer without rewriting engine/map tools; actual Chromium original-pixel 28/28 interactive checks passed, 0 JS/HTTP errors. Direct `file://` opening was **blocked by administrator in this environment**, so is not certified. Private original-source eight-member ZIP 2295731B/SHA256 `f14ee7c362e74bb82fabb867bee08729b41f9744208642fd689bf2730d10548f` uploaded to Library and complete SHA/CRC roundtrip passed. [Public derived receipt](research/recovered/STONEAGE-O31-FIVE-DOORWAY-SOURCE-R1.json) contains only original source numerical/hashed evidence, not proprietary bytes. O31 native-collision check **bounded and stopped**: server aggregate collision coverage does not supply same-carrier floor1000/floor1001 LS2MAP and mapset original bytes for exact route-cell verdicts. No native 1999/TW1 execution, same-deployment proof, source-collision simulation or historical item trade. Full old CURRENT untouched; Stage A7 PARTIAL+2 OPEN, B/wiki gated, R79 paused, overall_percent=null. **NEXT O32** one already-source-backed actual NPC/task content observation on the walkable viewer, no speculative collision-helper expansion.

**O31 additive source correction:** O30's supposed non-Warp neighboring DAT cells were proven to be actual Warp creation cells. On map1000, 30 cells have event value 49155 but 10 are not explained by this one `warp_y.create` file; marker exclusivity remains OPEN, not false. Old O30 receipt preserved and later O31 JSON/doc amended; no native collision proof.


### 2026-10-31 — O32 original-source flower-and-shell quest in continuous world

[O32 original-source static NPC task integrated into existing continuous original-pixel observer](docs/continuity/STONEAGE-O32-CONTINUOUS-FLOWER-QUEST-20261031.md): reused proven O24 NPC event02 scripts/items and O26 source images/dialogues inside existing O31 source-backed world — near 1000(57,124) 日美子, simulated request yields source GetItem2415 花; **explicitly labeled modern archive scene switch** (NOT proven original cross-town travel) shows actual preserved 2000 map and original TW1 candidate NPC art at 2000(55,92) 彌生, simulated ACCEPT 2415→2414 贝壳; return to exact original 1000 world position, source ACCEPT 2414→2415; then stop one demonstration cycle to avoid inventing infinite rewards. Original scripts' SP/LV/NOWEV/ENDEV/ITEM actual gates and native inventory unchanged/unexecuted. All 257 source RD alias images, original O31 5 warp edges, shop rowID0 and original 1000/1001 scene data exactly preserved. Actual Chromium original-pixel page rendering and controls **33/33** successful, zero JS/HTTP errors; file-scheme and original native client/server not executed. Six-member private research ZIP 2919651B/SHA256 `03c7e4f5a091efe3ffe84e77e47b0af1f763223b1fc0562256a3926a587de3ce` in Library and fully roundtrip-verified. No proprietary artwork, raw dialogue, or HTML public. [Public numeric derived receipt](research/recovered/STONEAGE-O32-CONTINUOUS-FLOWER-QUEST-R1.json). Historical CURRENT preserved; 7PARTIAL+2OPEN, B/wiki GATED, R79 paused, overall null. **NEXT O33** rotate one source-qualified new game-content domain, no new quest helper framework.


### 2026-10-31 — O33 original TW1 pet-frame follow in continuous viewer

[O33 source-separated original-pixel pet companion observation](docs/continuity/STONEAGE-O33-PET-FOLLOW-ORIGINAL-PIXEL-20261031.md): adds one verified TW1 original SPR100297 frame 60×42 to the **same** O32 Chinese original-resource map/quest/doorway observer, using existing convergent-descendant `ITEM_petFollow` rule for hypothetical eligibility (six rejection/success gates, no asserted item consumption or original item ID). Pet moves to preceding player grid cell and repositions after source-based village/shop Warp in a **modern observational animation** only; the O21 mixed25 source pet name 昆伊 remains a cross-version number candidate, not a confirmed Taiwanese-v1 species identity. All source 257 graphic aliases, O31 five Warp edges, O32 original quest and shop item0 preserved exactly; 34/34 actual Chromium browser checks, source-image rendering, 0 JS/HTTP errors. Private seven-member ZIP **3089489B** SHA256 `c6454cf90cc3f803e353583b0c557d45e5e988967dfa5cbd5c7c239cc69ad74f` archived to personal Library and exact SHA/ZIP CRC roundtrip passed; public Git only [derived numeric source receipt](research/recovered/STONEAGE-O33-PRIVATE-FOLLOW-OBSERVER-R1.json) and this checkpoint, no copyrighted art/HTML. **No native follow/riding, pet ownership, historical pathfinding or original EXE/server execution.** Historical CURRENT blob preserved; Stage A7PARTIAL+2OPEN, Stage B/wiki GATED, R79 paused, overall_percent=null. **NEXT O34** finite same-version pet material identity/ownership source join or new material domain, not further follower UI scaffolding.


### 2026-11-01 — O34 original Wuli complete-SPR-byte join in continuous observer

[O34 same-carrier original name / bitmap SHA-qualified Wuli observation](docs/continuity/STONEAGE-O34-WULI-ORIGINAL-SPR-SOURCE-20261101.md): reuses original mixed25 server `enemybase` source row1 **烏力** (IMGNUMBER=100250) and **same preserved archive client SPR100250 group240 full byte sequence** already verified by R40 against the original Taiwan 1.0 client. Re-read independently preserved TW1 whole ZIP 372626292B and raw SPR, SPRADRN, ADRN, REAL and Palet SHA; actual original group240 has 56 animations, 3712B, exact common SHA `eb1a87cd…`. Re-extracted actual original first RD bitmap95883 (28×52), integrated its source PNG into **existing** O33 source-art original map/doorway/quest/follower observer without introducing a new engine or helper; old scenes, 257 original aliases, 5 source Warp edges and task unchanged. Real Chromium **36/36** interaction and source PNG visual checks, no JS/HTTP errors. Private 8-member ZIP 3154788B SHA256 `0c9c38817f6b4c7838a7be0ec122f7dbe274b52a0153b6c7a23c27365fd1dbe2` stored in Library and full SHA/CRC download verified. [Public derived numeric receipt](research/recovered/STONEAGE-O34-WULI-SAME-ARCHIVE-SPR-EQUALITY-R1.json). **Original preserved mixed25 group is R40 prior source, not re-extracted this turn; same archive does not authenticate an official live deployment, TW1 species name, original owned pet, native following, actual collisions, game client or original server.** No proprietary images/HTML published. Historical CURRENT unchanged; Stage A 7 PARTIAL+2 OPEN, B/wiki gated, R79 paused, overall percent=null. **NEXT O35** material original sound-event-to-WAV binding or rotate other 22-domain real content; no new pet-follow UI.


### 2026-11-01 — O35 three-way original sound 73 source witness and audition

[O35 original audio 73 namespace ambiguity and private manual audition](docs/continuity/STONEAGE-O35-AUDIO-73-SOURCE-AMBIGUITY-20261101.md). Previously verified O11 SPR100250 action0 frame2 word73 and O12 compiled sound-number73→`sae_23.wav`, vs original `soundaddr_1.txt` ordinal73→`sam_17.wav` (1-based) or `sam_18.wav` (0-based), are **not demonstrably the same runtime namespace**. Re-read all 3 genuine retail Taiwan1.0 WAV bytes independently: `sae_23`14704B SHA`b6af6267…`, `sam_17`15020B SHA`3426f6e7…`, `sam_18`18892B SHA`dc15de08…`; each differs. Inserted only a collapsed, opt-in **three original sound candidate audition** into private O34 existing continuous world, with no automatic pet/event binding or new player framework. Actual Chromium source-audio and control **21/21**, existing walk/quest/pet **16/16**, plus separate ZIP CRC **1/1** all passed, 0JS errors/0HTTP. Local private four-member ZIP2724452B SHA`14fc7e1b344144bb513eb4feb8c95146de275a6188e1409174e190230ffb8cc6` CRC verified; **Library initially failed twice (expired container session), then succeeded via exact exported file snapshot; complete library download SHA256 and all 4 ZIP CRC passed**. Initial failures retained in dated O35 record. [Non-proprietary JSON receipt](research/recovered/STONEAGE-O35-ORIGINAL-SFX-73-AMBIGUITY-R1.json). Original game runtime/event mapping remains OPEN and no source assets are published. Historical CURRENT preserved, Stage A7PARTIAL+2OPEN, B/wiki gated, R79 paused, percent=null. **NEXT O36:** new evidenced original game-world content; reopen audio event only on actual same-source caller chain or native runtime trace, not guessed sound names.


### 2026-11-01 — O36 PET-STATE-01 caller-owned capture persistence gate

[O36 source-aware persistent captured-pet completeness guard](docs/continuity/STONEAGE-O36-PET-STATE-EXPLICIT-CAPTURE-GATE-20261101.md): at the existing `LocalRuntimeSessionCoordinator.resolve_persistent_capture_round` **persistent owner-state interface only**, six unresolved fields (`mp`, `max_mp`, `exp`, `max_exp`, `rename_flag`, `free_name`) must be supplied explicitly by the capture caller and non-None. Missing values reject **before transaction**, never filled by invented original or descendant defaults. Legacy lower-level experimental capture stays compatible. Added each-key negative/atomicity cases, None rejection and successful capture→settle→disk save→reload six-field retention; previously sparse coordinator test fixture explicitly supplies synthetic values. This addresses portfolio PET-STATE-01 current-code consistency, **not** original TW1 native owned-pet/capture/EXP formula execution. [Derived receipt](research/recovered/STONEAGE-O36-PET-STATE-EXPLICIT-CAPTURE-GATE-R1.json). Historical CURRENT unchanged, A7PARTIAL+2OPEN, B/wiki gated, R79 paused; overall percent unknown. NEXT O37 original map1003 pet-shop material availability, no invented world route.


### 2026-11-01 — O37 four original pet-shop doorway source blocks

[O37 original 1000↔1003 door creation source](docs/continuity/STONEAGE-O37-PETSHOP-FOUR-WARP-SOURCE-20261101.md): the preserved O31 original `warp_y.create` contains two outbound (68,72)→1003(15,21), (69,72)→1003(16,21) and two return static source blocks, all 4 whole-block SHA verified. Original 1000.DAT event 49155 matches both village source cells; native traversal, 1003.DAT return-cell original values and official deployment remain OPEN. [Derived receipt](research/recovered/STONEAGE-O37-PETSHOP-FOUR-WARP-SOURCE-R1.json).

### 2026-11-01 — O38 original two entrance tiles and stop rule

[O38 real source-pixel entrance tile witness, not a complete scene](docs/continuity/STONEAGE-O38-PETSHOP-ENTRANCE-ART-ADMISSION-20261101.md): fully SHA-verified existing O31 original map and Warp plus O35 original TW1 source-art reuse show two real 64×47 source candidates for 1000(68,72)/1000(69,72). Actual Chromium loaded both, no JS or HTTP errors; private self-contained 3-member ZIP was archived and full SHA/CRC download-reverified. Existing O35 asset availability is **23/52 references for 7×7** and **90/129 for 11×11** around the entrance; of O17's 38 original map1003 graphics only 31 are present in O35. O17 original DAT package remains known but raw-byte retrieval unavailable this work-unit; no 1003 return-cell verification, complete map rendering, native collision or original gameplay. [Nonproprietary derived acceptance](research/recovered/STONEAGE-O38-PETSHOP-ENTRANCE-ART-ADMISSION-R1.json). Stage A7PARTIAL+2OPEN, B/wiki gated, R79 paused, percent=null. **NEXT O39** rotate other materially sourced gameplay, reopening 1003 only on actual original DAT+missing art bytes.


### 2026-11-01 — O39 original SAB/SPR battle material inside the preserved modern world observer

[O39 private continuous village and genuine source-pixel battle research integration](docs/continuity/STONEAGE-O39-PRIVATE-ORIGINAL-BATTLE-WORLD-INTEGRATION-20261101.md): reuse already SHA/CRC verified independent O35 modern two-town world and O27 Taiwan1.0 SAB0 (20×20) / SPR100297+100298 source-frame **visual observations**, connecting only one opt-in battle-reference control and isolated iframe. Actual Chromium **26/26** image/frame/return-to-unchanged-map/old world state checks, 0JS errors, 0external requests. Private five-member 3221128B ZIP, SHA f21dc1090324…, was stored in user Library and fully SHA/CRC download-reverified. All private original graphics/audio/HTML remain outside Git. No native game client, random encounter, battle round, damage, background-to-location binding, or source TW1/mixed25 common deployment executed or proven. [Derived metadata](research/recovered/STONEAGE-O39-PRIVATE-ORIGINAL-BATTLE-WORLD-INTEGRATION-R1.json). CURRENT unchanged; Stage A7PARTIAL+2OPEN, B/wiki gated, R79 paused, overall percent=null. **NEXT O40** select newly sourced world content or game-rule gap rather than duplicating already bounded visual experiments.


### 2026-11-01 — O40 TW1 native EXE battle-file name provenance (no new scene claim)

[O40 source-executable-to-original-battle-file static reference join](docs/continuity/STONEAGE-O40-TW10-NATIVE-BATTLE-PATH-SOURCE-20261101.md): independently reread the full authentic TW1 P3H retail archive and original `sa_3.exe` / `StoneAge.exe`. The first contains **218 distinct `data\\battleMap\\battleNNN.sab` literal paths**, complete 0..217 and exactly matching already-preserved individual original SAB members; the second contains original `divideBattleFiles` and packed-index filename patterns. Existing O16 had **already established** that the packed `battle_1.bin` 10620B interleave is exactly 15 original 708B `Palet_1..15.sap`, and 233/233 packed slices are source-equal. The initial mistaken new-unknown interpretation was corrected before publication. Only the EXE↔asset **static path** cross-witness is a new qualified link; no new battle maps, native read call trace, background selection, engine, game rules or original executable run. [Derived proof](research/recovered/STONEAGE-O40-TW10-NATIVE-BATTLE-PATH-SOURCE-R1.json). Original assets remain private; CURRENT and Stage A7PARTIAL+2OPEN, B/wiki GATED, R79 paused, overall percent=null unchanged. **NEXT O41** return to genuinely missing same-build world content/entity/rule evidence, do not expand duplicate battle tooling.


### 2026-11-01 — O41 source-qualified two special village warp entrances, destination gated

[O41 exact two non-49155 original source-door cells and four return source configurations](docs/continuity/STONEAGE-O41-TWO-SPECIAL-WARP-SOURCE-20261101.md): O31 had already recorded two atypical original event values; O41 **does not re-claim that discovery**. Re-read verified original later-preserved mixed25 `1000.DAT`/`warp_y.create`: 1000(63,117) has original tile103/parts0/event**49158** and a source creation to **1011(10,15)**; 1000(63,118) has 103/0/**49159** to **1014(10,16)**. The same original create file contains two returns from 1011 and two from 1014; all six blocks have exact byte spans and SHA in [derived receipt](research/recovered/STONEAGE-O41-TWO-SPECIAL-WARP-SOURCE-R1.json). Existing O39 real-source-pixel viewer already has bitmap103 and both cells within its loaded map; only add source-only door markers and an already-present W control's **read-only refusal** to enter missing target floors. Actual Chromium **25/25** walk/source-message/refusal/preserved five-door weapon shop/battle/audio checks success, 0JS/HTTP errors. Private five-member ZIP 3518188B SHA7305a97d... saved to Library and roundtrip SHA/CRC verified. No original 1011/1014 map pixels, native collision, runtime trigger or server deployed proof. Historical CURRENT unchanged, Stage A7PARTIAL+2OPEN, B/wiki gated, R79 paused, percent=null. **NEXT O42** source-proven NPC or gameplay-rule content; reopen destination scene only with original same-carrier map/collision bytes.


### 2026-11-01 — O42 original inline NPC near source-qualified special doors

[O42 one real later-preserved NPC creation, original map cell, template and inline greeting](docs/continuity/STONEAGE-O42-SAME-CARRIER-NPC-INLINE-GREETING-20261101.md): independent full-SHA replay of the existing private O31/SCENE22/O41 packages qualifies source floor1000 (62,115), original map tile/parts/event 117/0/49152, graphic ID16209, `npcgen_man`→`TownPeople` and a 10-character inline greeting. Only a small modern proximity E/readout and source-coordinate marker were added to the private offline observer; actual Chromium `page.set_content` 14/14 passes (file navigation blocked). No original NPC sprite, native NPC execution, official same-build proof or new official source. Private five-member zip SHA b53fc9c7... is in the local handoff; Library upload failed and is not claimed. Public Git retains derived numbers only; CURRENT unchanged, Stage A 7PARTIAL+2OPEN, B/wiki gated, R79 paused, percent=null. **NEXT O43** real same-carrier graphic16209 or full gameplay-rule material only; stop expanding source-only UI without real inputs.


### 2026-11-01 — O43 exact original TW1 NPC graphic alias pixels and false literal-ID control

[O43 primary-source original pixel candidate for O42 NPC16209](docs/continuity/STONEAGE-O43-NPC16209-ORIGINAL-PIXEL-ALIAS-20261101.md): original complete rehashed Taiwan1.0 P3H client ADRN125996 index records show **unique alias-value16209→physical bitmap5929**, genuine source RD **36×84**, independent decoders agree; physical bitmap16209 is **different** 40×88 original art. A small source-pixel addition to the O42 private offline viewer passed **14/14** actual Chromium checks. Public [derived numerical custody](research/recovered/STONEAGE-O43-NPC16209-ORIGINAL-PIXEL-ALIAS-R1.json), no proprietary pixels or original text. Previous fully verified original TW1→specific preserved mixed25 full index/REAL prefix is **historical prior proof**, not freshly re-read mixed parent; no original selector, same-deployed build, actual historical palette, original client/server/world execution. Private eight-member 3452831B ZIP SHA644ed6a0... retained as this-turn local handoff; Library upload unconfirmed. CURRENT preserved, Stage A 7PARTIAL+2OPEN, B/wiki gated, R79 paused, overall percent null. **NEXT O44** material rotation to new actual-source gameplay/world content; do not expand source-only NPC UI.


#### O43 private custody follow-up — verified after candidate draft

The previously unconfirmed O43 private ZIP **was subsequently uploaded** to user Library at `/石器时代/StoneAge-O43-original-NPC16209-actual-art-final.zip`. Exact whole-object download roundtrip independently matches **3,452,831B**, SHA256 `644ed6a0085a7253093624d787476c6b460b47a11b8581f891aaff39031d9d4a`, 8 ZIP members and all CRC. Earlier failed O42 private upload remains a distinct historic failure. This upload does not promote original runtime/source version claims.


### 2026-11-01 — O44 original two village Dengon boards and real-source map windows

[O44 two independent original preserved village bulletin board service creations, actual original pixel candidates, and two minimal 7×7 world windows](docs/continuity/STONEAGE-O44-TWO-VILLAGE-DENGON-SOURCE-20261101.md): from verified preserved same-carrier `1000npc_m.create` / `npcgen.template` / `1000.DAT`, two **1000(94,93)** and **1000(93,66)** original “薩姆吉爾的傳言板” sources bind to template `Dengon`, create `graphicname=10062`. Original TW1 client full ADRN 125996-record scan uniquely joins alias10062→physical4766 (**64×107 actual board pixels**), whereas physical10062 is a **different 68×70 character sprite**. Two 7×7 windows re-render **98 authentic saved map cells** with **111 graphic occurrences / 65 exact TW1 original image aliases**, plus opt-in original bulletin board candidates; actual Chromium **13/13** passed, 0JS/HTTP. This is modern original-pixel observation, **not** original game runtime, native selector, original posts/service rules, original palette or common TW1/mixed25 deployment. [Public derived source and bounded nonclaims](research/recovered/STONEAGE-O44-TWO-VILLAGE-DENGON-SOURCE-R1.json); private source bytes/HTML/PNG/150-member ZIP **1,532,715B SHA0b56e450...** saved to user Library and SHA/CRC roundtrip verified, never put in public Git. CURRENT unchanged, Stage A7PARTIAL+2OPEN, B/wiki gated, R79 paused, overall percent=null. **NEXT O45:** another truly sourced pet, gameplay or world mechanism; no speculative bulletin-board UI.


### 2026-11-01 — O45 original teacher and five children source pixel neighborhood

[O45 original source-qualified teacher and five children in a previously unrendered village cluster](docs/continuity/STONEAGE-O45-SIX-TIMEMAN-TEACHER-CHILDREN-20261101.md): 6 original `npcgen_timeman` creation records in preserved mixed25 floor1000, genuine 192 map cells / 206 image occurrences / 94 distinct original map keys; all 6 real original candidate NPC art aliases from authentic TW1 retail ADRN (100 distinct keys total, whole 125996 records scanned). Source six-person scene, map-only and teacher-only rendered with real original RD pixels, 2 independent RD decoders and full independent Pillow/NumPy composite equality; actual Chromium **23/23** original PNG switch/identity checks, 0 JS or HTTP. **Six external tman_* behavior payloads not in available inputs**; original class schedule, native selector, official same-deployed build and original running game all OPEN. [Bounded derived source SHA and coordinates](research/recovered/STONEAGE-O45-SIX-TIMEMAN-TEACHER-CHILDREN-R1.json); private **2,659,116B/213-member ZIP SHA cd730c69…** saved to Library and roundtrip SHA/CRC verified, original RD/DAT/creation/HTML remain private. CURRENT unchanged; Stage A 7PARTIAL+2OPEN, B/wiki gated, R79 paused, percent null. **NEXT O46** source-complete gameplay material rotation; do not expand this cluster into an invented timetable.


### 2026-11-01 — O46 exact original TimeMan source content recovery

[O46 all six original teacher/child behavior source inputs](docs/continuity/STONEAGE-O46-SIX-TIMEMAN-SOURCE-CONTENT-20261101.md): recovered all six referenced `tman_1000_*` payloads (569 bytes) from the previously preserved **complete mixed25 RAR**, checked whole source RAR SHA256, six historical R18 file SHA256 values, six independent RAR CRC32, exact O45 NPC creation references and CP950/Big5 lossless reading. The teacher has four literal `main_msg` text segments, each of five children one; `time:ALLNOON` is a **literal source value**, not proof of native time scheduling. This precisely corrects O45's selected-subarchive source availability gap, not its execution boundary. [Derived receipt](research/recovered/STONEAGE-O46-SIX-TIMEMAN-SOURCE-CONTENT-R1.json). Original text stays private; CURRENT unchanged, Stage A7PARTIAL+2OPEN, B/wiki gated, R79 paused, percent=null; real original-world execution unproven. **NEXT O47:** original source-complete movement/encounter, pet or quest game rule; no further static TimeMan UI.


### 2026-11-01 — O47 four original village encounter-source rows, no invented encounters

[O47 exact source-row village encounter gap](docs/continuity/STONEAGE-O47-FOUR-VILLAGE-ENCOUNTER-SOURCE-GATE-20261101.md): one genuine preserved mixed25 `encount.txt` row per four starting village floors 1000/2000/3000/4000, from 660 original 33-column rows; all four **group ID columns 10..19 are blank**. Floor4000 retains five weights `50,40,30,20,30` in columns20..24 **without group IDs**; preserve anomaly, never infer missing monsters/valid fallback or original zero encounter probability. Full original source file SHA/CRC and two independent parsers checked, [derived numerical receipt](research/recovered/STONEAGE-O47-FOUR-VILLAGE-ENCOUNTER-SOURCE-GATE-R1.json). Historical TW1/JSS1999 same-deployment and native runtime encounters are unproven. CURRENT unchanged, Stage A7PARTIAL+2OPEN, B/wiki gated, R79 paused, percent=null. **NEXT O48:** rotate to actually sourced positive gameplay/interaction; do not expand empty encounter helpers.


### 2026-11-01 — O48 original two-status quest journal and four storyline objective source rows

[O48 original preserved mission and quest status source audit](docs/continuity/STONEAGE-O48-JOURNAL-MISSION-ORIGINAL-SOURCE-20261101.md): source-complete original mixed25 `jobdaily.txt` **220 four-column rows / 110 two-state entries** plus independent `mission.txt` **4 five-column storyline rows** were selectively read from the already saved whole-SHA-verified RAR and matched original R18 file SHA + RAR CRC headers. Across the 110 journal entries **only 105 distinct event integers** occur: 5 pairs reuse numbers; four mission numeric lists have **11 different numbers**, all present in the journal's event set. These source facts prevent premature ID deduplication or unjustified mapping of mission row IDs to journal entry IDs. A mismatch in trailing final LF is also recorded without claiming native parser failure. [Nonproprietary numeric/hashes JSON](research/recovered/STONEAGE-O48-JOURNAL-MISSION-ORIGINAL-SOURCE-R1.json). Original full text stays private, no source TW1/JSS1999 deployment or runtime claimed. Stage A7PARTIAL+2OPEN, B/wiki gated, R79 paused, overall percent=null. **NEXT O49:** identify actual status writer/reader only if original evidence exists; else rotate, no invented quest engine.

### 2026-11-01 — O49 original adult-ceremony flag linked to two world-entry NPCs

[O49 exact original source join](docs/continuity/STONEAGE-O49-ADULT-CEREMONY-WARPMAN-SOURCE-GATE-20261101.md): matched preserved mixed25 `jobdaily.txt` journal entry 1 `ENDEV=4` to two original `npcgen_warpman` spawn records on floor200 at (358,671) and (359,671), each uniquely referencing an independently named source behavior file. Both byte-identical original inputs contain `FREE:LV>64&ENDEV=4` and `WARP:21001,4,3`; `npcgen.template` supplies `WarpMan`. Five original source files match previous R18 SHA256, RAR member CRC32 and full private archive SHA. [Derived numeric/hash receipt](research/recovered/STONEAGE-O49-ADULT-CEREMONY-WARPMAN-SOURCE-GATE-R1.json). **These are static preserved community-version source relationships only:** completion flag writer, native conditional evaluation, actual travel and initial JSS1999/TW1.0 deployment remain unverified. Prior O49 attempted write was blocked; this is its additive recovery. Original bytes privately retained; full CURRENT unchanged. Stage A7PARTIAL+2OPEN, B/wiki gated, R79 paused, percent=null. **NEXT O50:** different source-backed material gameplay system; do not expand this NPC gate into speculative UI.

### 2026-11-01 — O50 original mixed25 two pet-skill table formats joined by all 56 numeric IDs

[O50 bounded 56-row original skill ID crosswalk](docs/continuity/STONEAGE-O50-PETSKILL-LEGACY-56-ID-CROSSWALK-20261101.md): the preserved and separately SHA/CRC-verified 9-column `petskill1.txt` has **56/56 unique IDs present in 12-column active `petskill.txt` (147 IDs)**, with same relative order, callbacks, options, FIELD and TARGET; it is **not configured as the selected skill file** in old verified `setup.cf`. On ID-matched records, 26 source names differ (25 have prefix `E` only in 12-column; one word-order difference), 6 descriptions differ, and one final numeric slot at ID210 is 0 vs 3000 with two exact source-row hashes. Numeric meaning and native 9-column loader UNKNOWN; do not call it MP, price or official early-era update. Earlier R45 147 records and prior skillcode 146 analysis are not new discoveries. [Derived source and ID receipt](research/recovered/STONEAGE-O50-PETSKILL-LEGACY-56-CROSSWALK-R1.json). Original full texts remain private, CURRENT untouched, Stage A7PARTIAL+2OPEN, B/wiki GATED, R79 paused, percent=null. **NEXT O51:** material different-domain rotation; no further 147-row helper probes.


### 2026-11-01 — O51 original preserved quiz quest links named NPCs, events, item IDs, and reward-source clauses

[O51 actual source-backed quiz three-brothers content join](docs/continuity/STONEAGE-O51-QUIZ-QUEST-NPC-ITEM-EVENT-JOIN-20261101.md): recovered one **specific preserved mixed25 quest input chain** from 10 original source files, reverified whole 361,255,180B source RAR SHA256, each file R18 exact SHA and independently checked RAR CRC. O48 journal quest entries 2/3 are `ENDEV/NOWEV=44/47`; 8 original NPC spawn blocks on floors 800/810/812/850 reference `npcgen_quiz`/four `changeevent` script inputs. Four **real itemset numeric IDs** 2752 (ticket), 2753 (membership), 2754 (exchange voucher), 2759 (mystery box) each join one genuine 13,254-row, 94-column source item table (ID column index16, not source line index). Original scripts expressly contain `GetPet:14`, `GetPet:351`, flag fields 44/47 and three `GetRandItem` branches; all 49 nonempty reward numbers match real original item IDs, **but highest branch has one empty comma token**. Separate 82-row `racequiz.txt` is **not directly path-linked** in these scripts and is not invented as their question bank. [Derived source-only numeric/hashes receipt](research/recovered/STONEAGE-O51-QUIZ-QUEST-NPC-ITEM-EVENT-JOIN-R1.json). Actual game engine, rewards, official earliest version, permanent-vs-activity category and pet identities unproven. No commercial dialogue/raw source in public Git; complete CURRENT unchanged. Stage A7PARTIAL+2OPEN, B/wiki GATED, R79 paused, percent=null. **NEXT O52:** rotate to genuine world / pet-state original material or native execution evidence; avoid speculative quiz engine.


### 2026-11-01 — O52 default battle pet must be an actually owned slot

[O52 local pet-state persistence integrity](docs/continuity/STONEAGE-O52-DEFAULT-PET-OWNER-SLOT-SAVE-GATE-20261101.md): an otherwise in-range `default_pet_slot` pointing to an empty carried-pet slot is rejected at both serialization and deserialization, before invalid selection can reach battle state. No new schema, pet engine, historical original claim or private original assets. Full historical CURRENT unchanged; Stage A 7PARTIAL+2OPEN, B/wiki gated, R79 paused, percent null, original playable world open. **NEXT O53:** source-backed world or pet ownership/storage material.


### 2026-11-01 — O53 actual original pet-shop entrance 11×11 world pixels from retained TW1 client

[O53 original floor1000 entrance-window recovery](docs/continuity/STONEAGE-O53-PETSHOP-ENTRANCE-ORIGINAL-PIXELS-20261101.md): actually reread the previously SHA-qualified **372,626,292B TW1 P3H retail client** and **O31 original preserved mixed25 1000.DAT** (both whole-source SHA matched). After applying the prior **exact REAL/ADRN common-prefix proof**, scanned all TW1 ADRN alias values and decoded **92/92 original RD images**, restoring **129/129 source graphic occurrences** across a real-data 11×11 (121-cell) bounded entrance window. Earlier O38 **32 absent distinct aliases** are now available. O38 two existing entrance PNGs match newly decoded source pixels exactly; O37 four original directional Warp block SHAs match. Four full-color *candidate* composites (7×7/11×11, tile/layer) passed **4/4 actual Chromium image-mode checks**, 0 JS errors and 0 external requests; source colors, draw layer and native Warp remain unverified. [Public SHA/source receipt](research/recovered/STONEAGE-O53-PETSHOP-ENTRANCE-ORIGINAL-SOURCE-R1.json) excludes proprietary original pixels. The **1,981,910B private ZIP** was built and SHA/CRC checked locally, but Library upload failed twice with container-session-expired and is **not** claimed durable in Library. Historic CURRENT retained; Stage A 7 PARTIAL + 2 OPEN, B/wiki gated, R79 paused, percent null, original playable world OPEN. **NEXT O54:** source-verified actual 1003.DAT interior and seven missing interior aliases if obtainable; otherwise rotate to another directly visible source gap, no invented native pet shop.


### 2026-11-01 — O54 original-pixel continuous village NPC to pet-shop entrance source window

[O54 finite original source corridor](docs/continuity/STONEAGE-O54-VILLAGE-TO-PETSHOP-SOURCE-PIXEL-CORRIDOR-20261101.md): reverified retained mixed25 original floor1000.DAT with TW1 full-prefix-qualified original image bytes. **532 real map cells, 549 real graphic references, 194 exact unique original image aliases**, plus one original NPC 16048 source candidate, in the bounded [60,69]—[73,106] window connecting two original pet-shop entrances (68/69,72) to previous village NPC (63,103). **199 original RD pieces** independently double decoded including 4 needed for exact **4/4** O53 PNG regression. Three 1744×1507 original-material modern candidate views passed **3/3 actual Chromium** image/Canvas checks with 3 source-position jump controls, 0 JS errors, 0 external requests. [Public metadata only](research/recovered/STONEAGE-O54-VILLAGE-TO-PETSHOP-SOURCE-CORRIDOR-R1.json); original pixel/data ZIP 5824336B archived **privately in Library** and independently re-downloaded exact SHA/CRC. The previously failed-to-upload O53 ZIP also now verified present in Library on separate re-download. No true native gameplay, collision, warp or official TW1 world deployment certified; original 1003.DAT still unavailable. Complete CURRENT retained; Stage A 7 PARTIAL+2 OPEN, B/wiki GATED, R79 paused, percent=null. **NEXT O55:** obtain source-authenticated original 1003.DAT if possible, else rotate to a new original-world/pet/quest material gap; no invented interior or runtime.


### 2026-11-01 — O55 verified existing PNGs in one offline source-only observer

[O55 finite two-scene research viewer](docs/continuity/STONEAGE-O55-TWO-SOURCE-SCENES-20261101.md) and [source-only HTML](tools/stoneage_o55_two_scene_observer.html): users locally select two already archived private images, O54 `O54-world.png` (1000) and O17 `map1003-combined-palette1-candidate.png` (1003); exact prior original-source candidate PNG SHA-256 and dimensions are required before showing or switching them. No proprietary image is embedded or uploaded. The two-map switch is an explicit **modern observation control only**; it is not the native Warp, original game launch, map1003 return-cell verification, official same-build proof, collision or pet-shop execution. Original O17 ZIP is listed in Library but raw-byte materialization denied in this session, so O55 freshly read **zero** bytes of original `1003.DAT`; its earlier independently SHA-verified recovery remains historically intact. Browser UI used synthetic PNGs and a mocked digest under restricted navigation, not fresh original PNG validation. Original CURRENT blob unchanged; Stage A 7PARTIAL+2OPEN, Stage B/wiki GATED, R79 paused, percent=null. **NEXT O56**: only reopen raw `1003.DAT` after authorized full-hash access; otherwise rotate to new source-backed pet/quest/world content, avoiding further scene simulation.


### 2026-11-01 — O56 preserve exact numeric identity in offline pet/item saves

[O56 bounded single-player persistence correctness](docs/continuity/STONEAGE-O56-PERSISTENT-OWNED-IDENTITY-INTEGER-20261101.md): the existing r1–r4 JSON loader previously used coercive `int(...)` on pet/item slot IDs, pet variants/templates/skills, growth and default pet selection; fractional numbers, booleans and numeric strings could silently alter what a loaded save owns. Use one strict JSON integer gate at the existing read boundary, 42 negative cases and transactional failed-restore coverage. Reuse existing save/logout Actions workflow to run the single-player persistence suite; no new schema or workflow. This is **modern local state correctness**, not a newly recovered original game rule or world asset; CURRENT original complete blob and all Stage A/B/wiki/R79/percent limitations remain unchanged. **NEXT O57**: stop revisiting save coercion; choose actual byte-available original pet/quest/world source material, reopening 1003 only after exact original DAT read.


### 2026-11-01 — O57 bounded source-backed pet-shop behavior comparison

[O57 cross-carrier pet-shop source audit](docs/continuity/STONEAGE-O57-PETSHOP-CODE-CROSS-CARRIER-20261101.md) compares the already hash-verified preserved mixed25 floor1003/(12,13) pet-shop create→397B argument (O18/O19) with **a newly read, immutable public 2026 integrated source snapshot** `BismarckDD/Stoneage@2f736808` / `npc_petshop.c` Git blob `5f18141188fb7a1bd2ce236a4559e54dc1a82294`. That later code contains separate sale and deposit/withdraw branches, riding/default-pet/available-slot guards, `pool_flg` conditional menu and a level-based fee expression; the original mixed25 script also contains `pool_cost` but this comparison source file never parses that quoted field. **Cross-carrier behavior clues, not 1.0/JSS1999 official rule, actual mixed25 execution, or proof the original `pool_cost` was ignored.** The existing O19 workflow downloads the fixed source file only to CI temp and checks the exact Git blob/size, selected code structure and original O18/O19 derived receipts. No raw code, private NPC text, DAT or image enters this public repo; full CURRENT stays untouched, original world OPEN, Stage A/B/wiki/R79/unknown percent unchanged. **NEXT O58:** rotate immediately to new independently sourced pet/quest/world material, not more invented pet-shop UI or pricing; re-open map1003 door cells only after full original DAT byte access.


### 2026-11-01 — O58 original pet-shop return-cell byte evidence admitted

[O58 original floor1003 return cells and four source warps](docs/continuity/STONEAGE-O58-PETSHOP-RETURN-CELLS-20261101.md): freshly whole-SHA verified preserved mixed25 private RAR and actually read original 5408B `1003.DAT`, 3644B same-carrier server map, 24588B original `warp_y.create` (plus opaque 1003.MAP). **Only two** floor1003 third-plane values are 49155, exactly **(15,21):5013/0/49155** and **(16,21):5014/0/49155**, which match both previously O37 source-qualified 1000(68/69,72) entrances and four original two-way create blocks (exact archived SHA verified). Server 1003 two graphics planes match original client DAT **900/900 each**. Previous independently verified full O45 1000.DAT re-read; a separate fresh RAR 1000.DAT extraction failed after 131072/153608B and was rejected, not rebranded as a pass. [Copyright-safe numerical receipt](research/recovered/STONEAGE-O58-PETSHOP-RETURN-CELLS-SOURCE-R1.json). No original Warp/runtime collision or official TW1/JSS1999 same deployment shown, no original-world entry and no private assets published; CURRENT unchanged, Stage A 7PARTIAL+2OPEN, B/wiki GATED, R79 paused, percent=null. **NEXT O59:** rotate to newly sourced pet capture/quest/original execution evidence, not pet-shop UI/price simulation.


### 2026-11-01 — O59 named wild pets capture-source inputs, source label conflict preserved

[O59 two source-qualified wild pet capture inputs](docs/continuity/STONEAGE-O59-NAMED-WILD-CAPTURE-SOURCE-20261101.md): from exact full-SHA and per-file CRC verified retained **mixed25** private RAR, re-read all four original encount/group/enemy/enemybase source tables and connected the already O21-authenticated encounter area floor100, source groups **88/91** → enemy IDs **119/122** → original templates **113/114** to instance **ENEMY_PETFLG=1/1** and template **E_T_GET=11/9**. Under pinned *later* capture-source logic these are eligible target flags and **input modifiers**, not 11%/9% capture probabilities or actual successful catch evidence. The original enemy instance suffix **「昆依」** differs from its own template name **「昆伊」**; neither original string was normalized away. A different *non-member* enemy2250/template29 source contrast has **PETFLG=0**, **GET=-5**, and cannot reach probability scoring under that later source gate. [Exact source, CRC, row hashes and bounded nonclaims](research/recovered/STONEAGE-O59-NAMED-WILD-CAPTURE-SOURCE-R1.json). No original server execution, no original TW1/JSS1999 deployment, no client raw content in public Git. Reuse O21 CI for derived-only anti-promotion and cross-source checks; original CURRENT unchanged, Stage A7PARTIAL+2OPEN, B/wiki gated, R79 paused, percent null. **NEXT O60** rotate to newly verifiable pet ownership, quest or early-village playable content, not another capture simulator.


### 2026-11-01 — O60 four-village original-preserved novice mentor source and two actual floor-cell anchors

[O60 four-village combat and pet teaching source](docs/continuity/STONEAGE-O60-FOUR-VILLAGE-NOVICE-MENTORS-20261101.md): newly extracted and whole SHA + independent RAR CRC verified **three** original files in the **later `sa60/newbie` subtree of the mixed25 private RAR**. Eight exact source `NPCCREATE` blocks in `newbie.create` name four outdoor battle mentors at floors **1000/2000/3000/4000** and four pet-shop educators at **1003/2003/3003/4003**, each group pointing to its own *single* `changeevent` teaching script. Both `fighter` and `petmaster` have precisely nine `NomalWindowMsg[0..8]` message rows, `EventNo:-1`, `TYPE:MESSAGE`, `LV>0`, and no grant/transaction commands. Sourced teaching topics include combat level/first-level capture/elements and pet loyalty/death/recovery/skills, **not executed numerical combat or loyalty rules**. Re-read original DAT same-carrier village floor1000 cell (48,62) **243/0/49152** and pet-shop floor1003 cell (19,15) **5000/0/49152**. [Exact files, 8 block SHA, 18 line hashes, CRC and strict boundaries](research/recovered/STONEAGE-O60-FOUR-VILLAGE-NOVICE-MENTORS-SOURCE-R1.json); no script-load/official TW1 or JSS1999/running client/actual display asserted. Public Git has no proprietary dialogue or DAT; complete CURRENT unchanged, Stage A7PARTIAL+2OPEN, B/wiki gated, R79 paused, percent null. **NEXT O61** rotate to a new material gameplay evidence seam; do not build new tutor UI or loyalty engine from dialogue.


### 2026-11-01 — O61 real four-village tiger-trainer source grants, unresolved reward pet template namespace

[O61 preserved four tiger mentors and explicit 12 pet grants](docs/continuity/STONEAGE-O61-FOUR-TIGER-TRAINERS-20261101.md): source RAR full SHA reread and original file SHA/independent RAR CRC verified for **tiger.create** (4 NPC creator blocks at 1040/2030/3030/4030) and its **m_tiger** companion script (16 TALKEVENT branches). Twelve static grant branches use **AddPet** values red 2483 / green 2481 / gold 2484 / yellow 2482 plus **Event_Now:166** and `LV>29&ENDEV=4&NOWEV!=166&TRANS=0`; raw BBI conditions form four pairwise disjoint 60-value groups covering **100000..100239** exactly. Four other branches contain no AddPet. **Corrected ID namespace:** all four AddPet IDs are absent as direct TEMPNO values, but **uniquely match original preserved `enemy.txt` ENEMY_ID** 2481/2482/2483/2484 → original ENEMY_TEMPNO 161/162/163/164 → saved same-carrier enemybase graphic numbers 100327/100328/100329/100330. Actual CP950 named variants and four original row hashes recorded. Independently read later integrated `NPC_EventAddPet` code, which looks up `ENEMY_ID`, but it is **not** proven to be the mixed25 running binary or the effective NEWWARPMAN path. Thus actual receiving/owning pet, persistence, riding unlock, original service load and JSS1999/TW1 rules still unproven; prior candidate TEMPNO-only negative explicitly corrected. [Exact source hashes, fixed numeric branches and source limits](research/recovered/STONEAGE-O61-FOUR-TIGER-TRAINERS-SOURCE-R1.json). No proprietary source/assets published. Complete historical CURRENT untouched, Stage A7PARTIAL+2OPEN, B/wiki gated, R79 paused, percent=null. **NEXT O62** seek real AddPet ID resolver / pet ownership storage or switch content if missing.


### 2026-11-01 — O62 original tiger trainer AddPet static handler and owner-slot chain

[O62 fixed-source NEWWARPMAN/AddPet-to-owned-pet call chain](docs/continuity/STONEAGE-O62-TIGER-ADDPET-CALLCHAIN-20261101.md): a **separate pinned later Bismarck source tree** has a `_NEW_WARPMAN` conditional path from selected TALKEVENT/YES through `Action_RunDoEventAction` and the *correct* `NPC_ActionAddPet` (not ExChangeMan `GetPet`) to `ENEMY_ID`, pet creation, `CHAR_setCharPet` and owner fields. The same source has non-atomic failure paths: `Event_Now` cannot be treated as evidence that a pet was successfully received. This qualifies a later **source-level conditional chain**, not an executed mixed25 original binary, real owner persistence, riding unlock, original JSS1999/TW1 gameplay, or entry into the original world. Historical CURRENT remains unchanged; Stage A7PARTIAL+2OPEN, B/wiki gated, R79 paused, completion percentage null. **NEXT O63** seek verified original pet graphic bytes 100327–100330 for visible offline comparison, or another exact material player-experience seam; stop if no authenticated bytes rather than expand generic C helpers.

### 2026-11-01 — O63 four named tiger pet source SPR groups and 992 source bitmap references

[O63 complete original TW1 animation metadata reconstruction and bounded same-carrier SPR index](docs/continuity/STONEAGE-O63-FOUR-TIGER-SPR-SOURCE-20261101.md): four saved mixed25 source template sprite numbers **100327–100330** map to original same-carrier SPR index positions **301–304**, with distinct exact segment bounds. TW1.0 accepted archive metadata independently re-encodes four full SHA-matching animation segments: **224 animation sequences / 1,968 frame positions**, and all **992 distinct nonzero bitmap IDs** have original ADRN index records. Four chosen direction0/action0 first frames **113019/113267/113515/113763** have exact REAL source offsets and 48×87 size metadata. **No original RD pixel bytes have been read in this work unit; no images or browser visual output are claimed.** No same-deployed-build, original game entry, pet grant execution or riding is claimed; same-name SPR raw-byte equality between TW1 and mixed25 remains unproven. Full historical CURRENT unchanged; Stage A7PARTIAL+2OPEN, B/wiki gated, R79 paused, overall percent null. **NEXT O64** source-verify and decode exactly four original RD blocks if accessible; else bounded stop and rotate to other material gameplay content.


### 2026-11-01 — O64 real original four pet RD pixels privately observed

[O64 four original real RD blocks and two original SAP palette candidate visual inspection](docs/continuity/STONEAGE-O64-FOUR-TIGER-ORIGINAL-RD-20261101.md): recovered the **actual source P3H TW1 original client** from private Library and verified entire 372,626,292B archive plus original SPR/SPRADRN/ADRN/REAL/SAP files. Exact four authenticated original 48×87 RD blocks for first-frame bitmap IDs **113019, 113267, 113515, 113763** were decoded with source RLE and rendered to **eight private candidate PNGs**. A private 16-entry 99,064B ZIP was uploaded, then recovered with whole-SHA and all CRC equal. **Private pixels were actually viewed; no original game's palette selector, game process, pet grant, pet ride or original-era species identity was authenticated.** Public Git holds only metadata and bounded source documentation, original historical CURRENT stays byte-identical; Stage A7PARTIAL+2OPEN, B/wiki gated, R79 paused, overall percent null. NEXT O65: bounded original motion/frame-sequence viewing only if materially valuable, not another generic parser/helper.


### 2026-11-01 — O65 four actual original tiger-pet action0/direction0 source motion previews

[O65 source motion and private 85-file original-pixel witness](docs/continuity/STONEAGE-O65-FOUR-TIGER-MOTION-20261101.md): recovered TW1 P3H original client SPR/ADRN/REAL with full source SHA, **30 ordered source frame occurrences / 24 actual individually decoded RD images**, separately checked by two RLE implementations. Unlike O64 first frames, selected original motion RD dimensions vary from **48–84 wide, 86–115 high**; source ADRN offsets are retained. Eight private GIFs (both SAP palette candidates) plus an 18-step four-up preview actually produced; modern **160ms/frame** playback is not native source FPS. Private **1,303,823B 85-file ZIP** uploaded to personal Library and re-downloaded with identical SHA/CRC. [O65 public derived report](research/recovered/STONEAGE-O65-FOUR-TIGER-MOTION-SOURCE-R1.json) also explicitly corrects one **60-character O64 publication typo** for bitmap113019 P1 PNG SHA without mutating historical source. All commercial pixels retained privately; no original client execution, deployed server, riding or original-world entry certified. Historical CURRENT unchanged; A7PARTIAL+2OPEN, B/wiki gated, R79 paused, percent null. **NEXT O66:** rotate to material game-world navigation / pet riding / concrete quest state evidence, not expand same 224-animation library.


### 2026-11-01 — O66 authenticated pet-shop original map pixels and route collision, two-warp BFS correction

[O66 original floor1003 static map/collision/warp/teacher source route](docs/continuity/STONEAGE-O66-PETSHOP-COLLISION-ROUTE-20261101.md): re-read complete SHA-qualified retained mixed25 361,255,180B RAR and **six actual 1003 DAT/server mapset/mapset1/warp/mentor creator sources**, source CRC/SHA match prior O58/O60 and collision coverage. Both original 900-item graphical planes equal server map; **all 40 source graphic IDs have matching collision metadata** (two saved mapsets agree), **71 ordinary-static-walkable cells of 900**. Exact stored warp entrances **(15,21)/(16,21)** each have a static path to pet-teacher NPC-adjacent **(19,16)** in **9/8 steps** respectively, **without entering the other warp tile**. Corrects initial false claim that west door required visiting east portal: one ordinary BFS tie route did cross, but an equal 9-step safe alternative was verified. TW1 actual full original REAL/P3H SHA rechecked; **39/39 nonzero map graphic aliases independently decoded to actual original RD pixels**, 2040×1559 source-only modern candidate view, private path overlays; later pet mentor graphic alias **16122 missing from TW1 ADRN**, so no fabricated NPC image. [Copyright-safe source/path SHA receipt](research/recovered/STONEAGE-O66-PETSHOP-ORIGINAL-COLLISION-ROUTE-R1.json). Private 19-member **3,373,088B** research ZIP uploaded to Library then re-downloaded exact SHA/CRC. No original runtime movement/warp, native palette/layout, TW1 same deployment or real playable-world entry proven; full historical CURRENT preserved. Stage A7PARTIAL+2OPEN, B/wiki gated, R79 paused, completion percent null. **NEXT O67** actual warp source trigger/execution qualification or a new source-backed material game-state seam; no general-purpose map tool expansion.


### 2026-11-01 — O67 same-private-carrier independent original mapwarp and npcgen_warp template

[O67 full-source warp table + NPC Warp template crosswalk](docs/continuity/STONEAGE-O67-ORIGINAL-WARP-CONFIG-20261101.md): reauthenticated the private preserved mixed25 original RAR and actually fully extracted new **110,674B `mapwarp.txt`** and **4,950B `npcgen.template`** with exact member SHA/CRC (the latter also matches the old R18 source record). Of **2,981 mapwarp rows**, exactly rows **1392–1395** give the four directed floor1000(68/69,72) ⇄ floor1003(15/16,21) relationships already independently present in O58/O66 `warp_y.create`; the source template explicitly binds `npcgen_warp` to **`functionset=Warp`**, not WarpMan. Bounded attempt to extract original saved `gmsv.exe` **failed CRC after 1,835,008/1,897,867 B** and was rejected, **not called native execution**. [Public metadata-only SHA receipt](research/recovered/STONEAGE-O67-ORIGINAL-WARP-CONFIG-SOURCE-R1.json). All native runtime dispatch, spawn-on-portal behavior, commercial same-deployment and original world entry still OPEN. Historical CURRENT unchanged; Stage A7PARTIAL+2OPEN, B/wiki gated, R79 paused, percent null. **NEXT O68:** only use an independently complete runtime witness for exact Warp trigger, otherwise rotate to a fresh concrete original game-content seam; no speculative original warp engine.


### 2026-11-01 — O68 actual offline movable private original-source petshop room observer

[O68 private offline floor1003 walking observation using 39 authentic TW1 RD graphics](docs/continuity/STONEAGE-O68-PRIVATE-OFFLINE-PETSHOP-WALK-20261101.md): reused the **actually reconstructed 2040×1559 original image block composite** and exact saved later mixed25 30×30 static collision bitmask (**71/900 passable**) without introducing a new engine or server simulator. Built one **self-contained private Chinese HTML**, manual arrow/WASD/on-screen steps, starting at either saved entrance, exact (x,y)/step counter, blocked-cell refusal and independently verified 8/9-step route overlays. Real Chromium full HTML with `set_content` passed both complete keyboard routes and a blocked step, map image size, SVG overlays, 0 JS errors / 0 network calls; direct `file:` URL was **blocked by execution environment admin policy**, not misreported as passed. HTML 713,710B/private-only; private four-member 1,037,642B ZIP uploaded to Library and SHA/CRC independently checked after redownload. [Public derived verification only](research/recovered/STONEAGE-O68-PRIVATE-OFFLINE-PETSHOP-WALK-R1.json); original art HTML/screenshot not published. This is a **modern static original-material research viewer**, **NOT** an executed original StoneAge client, original server, warp/dialogue, or official same-build world. Historic CURRENT unchanged, Stage A7PARTIAL+2OPEN, B/wiki gated, R79 paused, percent null. **NEXT O69** rotate to new source-backed original-world/quest/riding material; do not repeatedly extend this shop viewer.


### 2026-11-01 — O69 骑宠菜单与训练 NPC 原配置双候选来源界线

[O69 从原混合保存包完整核验的八项静态骑宠来源](docs/continuity/STONEAGE-O69-RIDING-STATIC-SOURCE-20261101.md)：用户私人 RAR 再读整文件 SHA（361,255,180B），并实取已被 R18 库存包含的 8 个原配置/共 7,778B，各 CRC/SHA 全等。两份骑师菜单对照为 **4 档（Lv40/80/120/不限；5000/10000/15000/20000）** 与 **1 档特级/20000**；`ride.txt` 13 行六字段，另有 17/9 `NPCPOINT` 分歧、`.bak` 与另一个参数全字节一致。两 `rider.create` 引用 `npcgen_warpman`，不可等同 O67 `npcgen_warp`。课程文案、`takegold`、`AddItem` 都**不能当作已执行扣金、发奖或学骑宠的事实**，也没有确认哪份配置上线。 [公开哈希与字段数字回执](research/recovered/STONEAGE-O69-RIDING-STATIC-SOURCE-R1.json)；原文件未入公开 Git。历史 CURRENT 全文未改，Stage A7PARTIAL+2OPEN，B/wiki gated，R79 paused，percent=null。**NEXT O70**：有同构建运行证据才追骑师链，否则转有实物的任务/捕获场景，不建无证骑宠模拟器。


### 2026-11-01 — O70 四地区原委托、宠物提交与捕捉来源级联接

[O70 任务管理 NPC → 47条未注释宠物/料理委托 → 原奖励配置 → O59两宠捕捉候选](docs/continuity/STONEAGE-O70-FOUR-VILLAGE-COMMISSION-20261101.md)：从同份原 mixed25 RAR 整SHA复核实际7原文件（四脚本、NPC创建、完整itemset与jobdaily），原CRC/SHA均同。四 NPC 静态在 floor1009/2009/3009/4009 的(18,12)，对应 **47条未注释委托=23宠物+24料理**，另有**注释停用块20064**与**条件×1/扣除×2不一致20025**。47委托书/料理材料/13候选随机道具数值ID在完整13254行×94列itemset中唯一；奖赏45条石币、2条随机道具列表。源同保存档 O59 的模板113/114正好匹配委托书20001的2+2只宠物与400石币配置，形成静态捕宠→交付来源链；不代表实战捕捉/交付/奖励成功。原活动/常驻分类、官方初代同服和实际地图路线均 OPEN。完整47条数字与哈希在[O70公共派生回执](research/recovered/STONEAGE-O70-FOUR-VILLAGE-COMMISSION-R1.json)，**原脚本/对白/道具表不入公开Git**。旧CURRENT字节不动，Stage A7PARTIAL+2OPEN、B/wiki gated、R79暂停、percent=null。**NEXT O71**：仅有合格同版地图/NPC素材时重建一条真实素材任务观察，否则转其他有实物游戏内容，不造无证任务模拟器。


### 2026-11-01 — O71 floor1009 原地图/NPC/双入口静态路线与私人离线观察

[O71 原1009.DAT、独立MAP、服务端LS2MAP与两份碰撞源的实物核验](docs/continuity/STONEAGE-O71-FLOOR1009-SOURCE-ROUTE-20261101.md)：同旧保存后代mixed25 RAR重新整SHA并取5源原字节（各CRC/SHA同），确认40×60地图、DAT与server地面图形2400/2400同、**物件层右边界x39有12格不同**，故静态可走DAT候选2141、server候选2153。O70委托NPC位于(18,12)，原warp_y.create证两处1009侧入口(10,25)/(10,26)；避免另一入口的源静态路线到NPC邻格分别20/21步。原完整mixed ADRN中的86张图块别名+NPC16200都在旧已证TW1公共前缀，**但本轮REAL原像素提取失败，不能称1009原画已恢复**。已制作**非原图的现代数据格网**、实际Chromium键盘路线/阻挡/切源验证，0JS/0网络，私人ZIP155868B上传Library并回下载完全同SHA。公开仅[数值与SHA回执](research/recovered/STONEAGE-O71-FLOOR1009-SOURCE-ROUTE-R1.json)，原商业资源未进Git；历史CURRENT原Blob未动，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79 PAUSED、percent=null。**NEXT O72**仅在原图像资源全字节可校时补真实场景，否则轮换新领域，不扩泛用模拟器。


### 2026-11-02 — O72 委托房间1009实际原图像素成功恢复（现代静态观察候选）

[O72 从已存台湾1.0完整REAL重建floor1009原图块](docs/continuity/STONEAGE-O72-FLOOR1009-ORIGINAL-PIXELS-20261102.md)：实取 mixed25 的1009.DAT（40×60）及私人 P3H 台湾1.0的完整ADRN/REAL/Palet_1，全文件SHA分别重新认证；当前再证全部125996条完整ADRN前缀与mixed25原ADRN逐字节相同，完整REAL前缀沿用此前已验来源报告，**未重跑后代763MB REAL比较**。地图85种图形+NPC16200一图，**86/86原RD真实图块**被两套独立解码器逐像素重放一致，总386898B源RD，地图**1034次原图块放置**（861地面+173物件），产生2071×1705的现代候选画面及原NPC邻域画面，已经本地实际目视。私人ZIP **11754955B/SHA256 4bc6c2ae8431d1563f3c4b9ac07e344e1e7d9c7b005e388c832ae07b0ecf4b45**、8成员CRC验证通过；尚未上传个人Library。公开仅[派生数值与哈希](research/recovered/STONEAGE-O72-FLOOR1009-ORIGINAL-PIXELS-R1.json)，原图/HTML/DAT/商业资源不入Git。**现代图像色表、绘制顺序、NPC叠加绝非原版截图/同部署鉴真或原客户端运行。** CURRENT原历史大文件字节不变，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null。**NEXT O73**：限实物原字节和可见内容差异，对其他2009/3009/4009委托房间作一次有界原画比较；若只有重复或缺件则立即转真实玩家交互/任务缺口，不扩泛用模拟工具。


### 2026-11-02 — O73 四地区委托大厅原图块实物差异，51种真正新增原图

[O73 四个保存版委托大厅的原始DAT/ADRN/REAL静态视觉对照](docs/continuity/STONEAGE-O73-FOUR-COMMISSION-HALLS-20261102.md)：实际从完整SHA合格mixed25 RAR取出原1009、2009、3009、4009四张各14408B/40×60原地图（各独立完整SHA/原RAR CRC32验同）；前三层都保留原数值，不把第三层认作互动事件。四图去重得**136种**地图图号，相对O72已有85种净增加**51个**真正新图号。实取已验TW1.0原REAL公共前缀中的136地图+16200NPC共**137/137原始RD**，源共890157B、新51 RD共503259B，全部两套独立RLE实现逐像素一致；O72原1009完整PNG复绘SHA原样一致。四张不同布局现代原像素组合与四房间对照图实际生成/目视；私人包**12217740B、SHA256 491eb39b08088c68d348661911dcad6ea16f7cf9ab62c190a493e511eda1c58c**、8成员CRC验收，尚未上传个人Library。公共仅[数字来源及哈希](research/recovered/STONEAGE-O73-FOUR-COMMISSION-HALLS-PIXEL-COMPARISON-R1.json)，商业原图和DAT不公开。**没运行原客户端，没有认证调色板/绘制顺序/商业部署或任务互动；mixed25完整REAL字节前缀复用历史鉴真而非本轮重比较。**历史CURRENT保持原字节，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、percent=null。**NEXT O74** 回玩家实际交互证据，有确切运行/原代码来源才核一名委托NPC的执行，否则轮换内容域，不反复静态画房间或造模拟任务引擎。


### 2026-11-02 — O74 四处原委托书贩售员与第二 NPC 原图，宠物委托23/23来源闭环

[O74 四委托大厅售书 NPC 的原始配置与NPC像素](docs/continuity/STONEAGE-O74-COMMISSION-TICKET-SELLER-20261102.md)：重新从已存混合后代2.5 RAR 整SHA实核12份相关原小脚本/配置（每份CRC/SHA/CP950往返同一），其中 `npc/genout/mission.create` 创建4位**委託書販售員**，分别在1009/2009/3009/4009的**(20,12)**、图形别名**16201**，与O70四位(18,12)/16200任务管理员不是同一NPC。各 `npcgen_shop` 模板源函数名为 `ItemShop`。四售书列表为6+6+5+6共**23张不同宠物委托书**，与O70有效宠物委托23条ID逐项精确同一；**20064** 同时在 O70 原脚本注释停用及本轮售书列表缺席，但另有原itemset道具行。O59模板113/114→售书ID20001→O70任务要求/奖励字段形成**同档静态资料闭环**，不是购买/捕获/发奖执行。另24张料理委托书未见于这四家售书原列表；限额扫描2,201份原NPC小资料 `ItemList` 也无其直接出售记录，**不能推出全源不存在**；“工作介紹中心”独立ItemList18563–18566不混作料理售书。台湾1.0原 REAL/ADRN 已核图形16201的**32×86真实RD像素**，与16200管理员原图均双解码一致，叠入4幅O73原画大厅构成现代**私人静态候选**。私人6成员ZIP**11,706,985B/SHA256 e19b7b7b19c66e3f75c5cee9d25637ac7c14ddc2cea8e15e9a04855f40073008**完整CRC通过；公开只存[来源/哈希/界限](research/recovered/STONEAGE-O74-COMMISSION-BOOK-SELLER-ORIGINAL-SOURCE-R1.json)，原图/脚本原文/旧EXE不入Git；原客户端/商服仍未执行，同版部署与原生调色板/绘制未证。旧CURRENT原样、Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暂停、总体percent=null。**NEXT O75**停止在委托静态脚本循环，转实源可验的另一个具体玩家操作/玩法；只有同版服务端运行见证才重开购买/领奖执行。


### 2026-11-02 — O75 原NPC料理／加工教学及两地主厨食谱源，原图16053/16066/16209

[O75 原同档厨师教师窗口/原物品交叉核实](docs/continuity/STONEAGE-O75-ORIGINAL-PET-COOK-CRAFT-TEACHERS-20261102.md)：在本轮重新核验远端 `main=04079d8d9f4f7f0a1f676d6b129f53f6f5e32daf` /10项主线CI成功、原CURRENT整Git Blob不变后，完整 SHA 验已存后期混合2.5 RAR并实际CRC/SHA核9份直接材料：6位原NPC创建（地图1009/4009加工教师25,30；2009/3009料理教师13,14；两主厨2009:25,41与3009:25,43）、原 `cook.conf` **10窗口**，`gousei.conf` **8窗口**及两份主厨菜单 **5＋4窗口**，所有原 `gotowin` 在源图中可达。原文本实际说明**宠物而非玩家执行料理／加工**，料理选至少两种素材、右键标记→具技能的宠物→施放料理技能；加工源写素材＋素材／道具＋道具／素材＋道具，匹配品质、宠物适性仅文本定性不补概率。两地主厨6道菜只对**3009的3道**找到同档94列 `itemset.txt` 唯一同名原物品ID **12607、12780、12754**、对应原用法/食材原子8名均查证；2009三道菜单与物品表存在字序/菜名差异，**不擅自统一**；原 `ingvalue` 不等同菜单“1个”或成功率。台湾1.0原 `REAL/ADRN` 的三个真实 RD 图形**16053/16066/16209**全部双RLE解码逐像素一致；私人原说明窗口导航＋三图本地离线观察ZIP **37,761B/SHA256 988b8cbdd10dd26deead694b8a2437c96a03f99cd0740e4cec6edaf4866e3023**，7成员CRC验通过，私有原文/图像不上Git。仅公共[派生SHA、数值合同及反证](research/recovered/STONEAGE-O75-ORIGINAL-COOKING-CRAFTING-NPC-SOURCE-R1.json)。**原游戏、服务器、NPC原生UI点击、宠物真的料理、道具效果及JSS1999/TW1.0同版部署未认证。**CURRENT原样、Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暂停、overall_percent=null。**NEXT O76**：停止继续扩13k料理/加工静态表，转另一有实源证据的玩家输入或原生运行可见内容缺口，不造料理成功率/游戏UI模拟器。


O75 CI史实订正：PR #133 初稿的 Stage A 检查 run 41362507873 因两处派生报告字段键名错误失败；首次修订后的 run 41362584714 因遗漏一处 `R79` 大小写键名仍失败，以上原始失败记录保留在 GitHub Actions。现已按公开报告真实键名修正，后续须以实际重验结果为准，不把旧失败宣称通过。


### 2026-11-02 — O76 原始战斗／宠物新手指引的玩家操作证据

[O76 四村战斗与宠物教学 NPC 原配置](docs/continuity/STONEAGE-O76-ORIGINAL-BEGINNER-BATTLE-PET-SOURCE-20261102.md)：本轮重新实核私人后期混合2.5 RAR **361,255,180B**、来源完整 SHA；实取五份源成员，每份原 RAR CRC / 解出 CRC / 全 SHA / CP950 往返一致。现行 `newbie.create` **8条**：四村战斗指导员各一位（地图1000/2000/3000/4000，图16496），四地宠物知识讲解员各一位（1003/2003/3003/4003，图16122/16127），分别引用 `fighter` 和 `petmaster` 两个原静态事件，各有**9段**说明。战斗文本明确描述鼠标悬停查看敌人等级、一级宠物捕获建议、敏捷／逃跑／合击及属性克制；宠物文本说明忠诚、战斗与技能学习；**只是文字事实，不是已执行原版游戏交互、概率公式或早期官方归属。** 原 `newbie.create.bak` 34块保留现行8块，又有**8018地图备用第五位宠物导师**，不擅自提升为现行已启用NPC；同长 `newbie2.create` 为其他NPC资料，未混同。公开仅 [派生结构与 SHA / CRC 证据](research/recovered/STONEAGE-O76-ORIGINAL-BEGINNER-BATTLE-PET-SOURCE-R1.json)，原脚本/图像留私。**NEXT O77**：同版原客户端鼠标目标信息入口或真正玩家输入见证；没有实源即限定止点轮换，不加模拟器。旧CURRENT字节不变，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、percent=null。

### 2026-11-02 — O77 台湾1.0原客户端Win32鼠标事件与坐标处理实源（非原生战斗执行）

[O77 原 `sa_3.exe` 鼠标原生分派证据](docs/continuity/STONEAGE-O77-TW1-NATIVE-MOUSE-WINDOW-DISPATCH-20261102.md)：重验原P3H私人TW1 372,626,292B ZIP整SHA及379成员全部CRC；源425,984B `sa_3.exe` 的真实Win32 `WndProc` 0x41C970/跳表0x41D40C查得鼠标移动、左右键按下/抬起/双击7条明确消息处理入口；鼠标X/Y由0x42DED0写入原全局状态，0x425290实际读取坐标做矩形界限判断。标准库原字节断言与objdump独立交叉核实；完整[源SHA、消息目标及反证收据](research/recovered/STONEAGE-O77-TW1-NATIVE-MOUSE-INPUT-SOURCE-R1.json)。**这是原版客户端真实存在的输入代码，不是原程序在战斗中展示敌人等级的运行证据，更不是将O76后期2.5教程认证为同版TW1事实。** 不能宣称原世界已进入/战斗目标命中/原生像素已显示；没有开发模拟器、优化玩家体验或公开EXE。连续性协议§16正式固化**复原阶段忠实记录、未来新石器阶段才考虑体验优化**。原CURRENT SHA保持字节不变，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、percent=null。**NEXT O78**：限原TW1战斗目标命中→等级显示确证入口，有新来源才能推进，否则有界止点轮换原版内容域。

### 2026-11-02 — O78 台湾1.0原客户端鼠标对象命中→原等级文案→有条件绘制调用

[O78 原 `sa_3.exe` 同版代码链](docs/continuity/STONEAGE-O78-TW1-HOVER-LEVEL-STATIC-SOURCE-20261102.md)：原P3H台湾1.0私人ZIP **372,626,292B/379成员全CRC**及原425,984B EXE全SHA重新校验；从原帧循环 `0x40D29A` 到 `0x42E320` 的对象鼠标坐标/图形宽高命中处理，确认被选字段、状态9/10等显示条件，以及同一原EXE .data 内 8条CP950原模板（`%s  Lv：%d`、可选第二名称、`耐`与`氣`值），格式化到原缓冲区后 `0x42E82D→0x40DF50→0x40CED0` 发出绘制请求（有标志位条件）。本轮实际从原字节断言14个指令锚、4个相对CALL，`objdump`独立核对，详见[源数值与负面边界](research/recovered/STONEAGE-O78-TW1-HOVER-LEVEL-STATIC-SOURCE-R1.json)。**FACT仅限原客户端静态条件调用：仍未实见原画面/原生鼠标悬停、未确定命中对象一定为战斗敌人，不能把O76后期2.5教学与TW1视为同版部署。** 无EXE/原图入公开Git，无体验优化/新石器开发。完整历史CURRENT Blob不变，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、整体percent=null。**NEXT O79**：停止无界扩张通用反编译，轮换尚未覆盖的原客户端游戏世界、NPC、地图或宠物具实源内容；当有原版战斗运行画面才重开O78实际验收。


### 2026-11-02 — O79 后期保存包七宠物对话配置与原物品主表联接

[O79 原始宠物对话菜单/事件/道具关联](docs/continuity/STONEAGE-O79-ORIGINAL-PET-TALK-SOURCE-20261102.md)：重新从私有 SHA 合格的 mixed25 RAR 实际提取 `pettalk.menu` 与7脚本及 `itemset.txt` 共9个原成员，逐原 RAR CRC、完整 SHA、CP950往返核实。菜单原序7个唯一 `PETTEMPNO` 为718/2/914/913/170/401/1147；7脚本合计 **132个静态 `TalkMsg` 标签**（OTHER7/TALKRUN38/EVENTRUN67/BOTH20）。原道具条件编号2414及 `AddItem` 编号2848、19688各在同档13,254行/94列物品表唯一存在；来源哈希、单行摘要见[公开数值回执](research/recovered/STONEAGE-O79-ORIGINAL-PET-TALK-SOURCE-R1.json)。可核的是**后期混合归档原静态宠物对话内容**，不是原游戏运行的宠物说话、道具发放、同服/TW1/JSS1999归属。未公开源脚本/旧资产，没有体验优化、模拟宠物说话或原客户端世界进入。完整CURRENT不变，Stage A7PARTIAL+2OPEN，B/wiki GATED，R79暂停，整体百分比null。**NEXT O80**：只核有真实来源的宠物对话触发/调用器；缺相同原始证据立即轮换其他未复原内容，不空转扩助手层。


### 2026-11-02 — O80 四村聊天室门票→源 NPC→原进出传送→地图证据

[O80 四村聊天室原始静态内容联接](docs/continuity/STONEAGE-O80-ORIGINAL-CHATROOM-TICKET-GATES-20261102.md)：自已保管 mixed25 RAR 重新验全档 SHA，实取四村 ticket、NPC chatroom.create、generated 原创建、8份四对 wpm、四村完整 DAT/MAP、chatroom.conf及原itemset；各原成员 SHA/CRC 和回执见[O80 原始来源数字证据](research/recovered/STONEAGE-O80-ORIGINAL-CHATROOM-TICKET-GATES-R1.json)。四村1012/2012/3012/4012分别用门票2521/2522/2523/2524，由(18,16)售票NPC和(14,13)引导员指向中央110的(37,21/25/29/33)，再由中央(37,20/24/28/32)返回对应村(13,13)。原四图30×30、票据同档物品表各唯一；1012/4012 MAP 全同但 DAT有5个16位格差。保留ticket130中GetItem2602与EVENT:ITEM2054不一致，未无证纠正。对605份原NPC小文本扫不到独立 pettalk dispatcher，不能证明服务器 native 不存在。**全部为后期私人混合载体静态事实**：未运行原客户端、商业服、原生传送/扣票或图像，不能替代TW1/JSS1999证据；不做未来游戏体验优化。CURRENT原blob不改、Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、整体完成百分比null。**NEXT O81**：在已有真原图条件下择一有界聊天室内景观察/来源联接，否则转其他新实物内容。


### 2026-11-02 — O81 中央聊天室110原地图与24图像索引的真实原始材料联接

[O81 110原图像ID/地图格核验](docs/continuity/STONEAGE-O81-ORIGINAL-CHATROOM110-MAP-ALIAS-20261102.md)：重新取证原 mixed25 保存包的110.DAT（46×45、三个2070格数值层）和两份**逐字节相同**的110.MAP；检验四村进出源参数的八个110地图格，均在范围内且各具原三数值。取一处8×17有限门户区域的**136格**，从两原图像图层得**24种图像别名、138次引用**，使用此前已核完整源SHA的全量18765120B ADRN逐个确认唯一记录与RD范围，均位于既存 TW1 REAL 完整字节前缀有证范围（不是认定地图TW1官方部署）；来源、24条原地址/SHA见[数字回执](research/recovered/STONEAGE-O81-ORIGINAL-CHATROOM110-MAP-ALIAS-R1.json)。本轮实际读RD像素**0B**：当前RAR大图像资源过滤器不支持，旧封存ADRN可实读，**不能假称原内景完成/原客户端运行**。所有商业源图/原文件不公开、CURRENT原blob未变、Stage A 7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、整体百分比未知；不开发新游戏、不优化玩家体验。**NEXT O82**：有独立原RD像素来源才继续110真实画面，否则轮换新实源世界内容。


### 2026-11-02 — O82 风之守护兽原版战斗/NPC/敌人/地图原始配置

[O82 風的守護獸原始NPC→两战斗配置→十一种敌人→三地图证据](docs/continuity/STONEAGE-O82-ORIGINAL-WIND-GUARDIAN-20261102.md)：从整包SHA合格的私人mixed25 RAR实际重读/核验11份原成员，逐原RAR头CRC、字节数、完整SHA独立通过。原NPC坐标11208:(26,40)/(42,38)、11214:(41,36)，`NPCEnemy` 的两模板 `sb_kbu/sb_kgi` 与脚本一致；每脚本10个含重复的enemyno槽位，整包原敌人表2087条有效唯一数字ID中11种真实对应，均有原名/源行SHA。原 `sb_kgi` 写有 `dieact:1` 与传送目标11215:(9,16)，三地图DAT/MAP原字节尺寸与四坐标实格全核，**未执行原生战斗/传送或验证原怪物出现**。先有界试取O81的REAL图像，但压缩库在393216B处报Invalid symbol，未得到有效原RD图像，聊天室原像素仍OPEN。来源是**后期私人混合档**，不强归属TW1/JSS1999；不做现代玩法优化、引擎模拟或发布版权原件。完整历史 CURRENT 不变、Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、percent=null。数字回执见[O82 原文件SHA/CRC及数字联接](research/recovered/STONEAGE-O82-ORIGINAL-WIND-GUARDIAN-R1.json)。**NEXT O83**：再择一源实物内容缺口或原生执行证据，避免继续扩失败解包/通用引擎助手。


### 2026-11-02 — O83 家族银行八原NPC坐标、原银行双账户菜单和八组地图格

[O83 源级家族银行原始静态内容](docs/continuity/STONEAGE-O83-ORIGINAL-FAMILY-BANK-MAP-20261102.md)：重新整包 SHA 校验私人后期混合2.5 RAR，实际解出原 `bankman.create`、`bankman.conf` 及八地图 16 DAT/MAP 共**18份原文件/53139B**，逐源CRC、完整SHA、坐标与地图全格范围核验。配置保留四庄园 floor1041/2031/3031/4031 与四村 floor1006/2006/3006/4006 八处银行管理员，均原名「家族銀行」、原图号16017，八个原坐标及DAT三层/MAP原数值收于[哈希和格子证据回执](research/recovered/STONEAGE-O83-ORIGINAL-FAMILY-BANK-MAP-R1.json)。菜单明确原文「家族個人帳戶」「家族共同帳戶」，但仅定义 winno1，选择流向5/6在该文件没有窗口定义；**不能擅称实际执行存取款或余额**。楼层3031的movecenter两组坐标不等(15,13与17,11)，保留原状。另确认骑宠来源已在O69做过归档，未重复立项。私有原脚本/地图/原图不公开，后期保存包不冒充TW1/JSS1999，原客户端未执行；无体验优化/新游戏开发。历史 CURRENT blob 不变，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、总体百分比未知。**NEXT O84**：轮换别的真实未恢复原版游戏内容或原生执行依据。


### 2026-11-02 — O84 萨姆吉尔两组人物的原叙事来源、五个NPC原地图格

[O84 原剧情人物静态取证](docs/continuity/STONEAGE-O84-SAMUGIRU-STORY-NPCS-20261102.md)：从已保存、实际CRC/SHA核验的 O45 私人原件包读取4413B后期保存版 `1000npc_m.create` 和完整153608B `1000.DAT`。新归档三位相邻`村莊小姑娘` (118,95)/(118,96)/(117,95) 的原配置（图号16032/16033/16038），两行提到卡卓父母担忧和公园旁叹息；另两位分别有原名`願藏的母親` (82,39)/16021、`願藏的父親` (79,37)/16019，并保留三个外部原对白文件的确切指针。**两组不同姓名绝不拼成同一家族/确定任务**。原DAT五格数值、原块SHA、旧O29/O45/O54有限像素子集资格见[数字收据](research/recovered/STONEAGE-O84-SAMUGIRU-STORY-NPC-SOURCE-R1.json)；本轮未解码五角色原RD、未执行NPC对话/原客户端，未新下载原大包。NEXT **O85** 只用可认证的确切外部对白源深化一条，否则轮换原版内容域。CURRENT旧blob不变；Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总体percent=null；不进行新游戏体验优化。


### 2026-11-02 — O85 愿藏三原对白、桥上敌对NPC与两条敌人主表同源核验

[O85 村民叙事→桥上愿藏NPC→源级战斗/敌人主表](docs/continuity/STONEAGE-O85-YUANZANG-DIALOGUE-BATTLE-20261102.md)：独立全SHA复验已保管混合2.5 RAR **361255180B**，15原成员逐原RAR头CRC/字节/全SHA一致；O84缺失的三份原 `msg_1000_118_95`、`msg_1000_82_39`、`msg_1000_79_37` 全部真实读取，证实相邻少女与愿藏父母围绕“通往沙漠的桥”的同名叙事线索。独立实取敌对 NPC `sb_ganzo.create/template/arg`（floor100:472,297、图号100401、NPCEnemy、敌人ID253/254），同源 `enemy.txt` / `enemybase.txt` 唯一ID→模板号500/501链接。**254敌人名「呼拔雄」与模板501原名「呼拔吉」不一致**，原传送参数三行是注释而非已执行Warp。更广的king/event69叙事单独限定未证运行。原100.DAT/MAP提取分别131072/1179648B便失败，未将坏片段升格成地图；无原客户端执行/原生对话或战斗/官方最初版归属。公开仅[数值/哈希](research/recovered/STONEAGE-O85-YUANZANG-DIALOGUE-BATTLE-SOURCE-R1.json)，原资产私有，旧O84及CURRENT不删。**NEXT O86** 轮换独立有真实材料的其它游戏内容。Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79暂停、整体百分比未知；不做新游戏体验优化。


### 2026-11-02 — O86 长毛象交通原路线、站点与原文字证据

[O86 长毛象客运六条源级线路/六站/原站牌](docs/continuity/STONEAGE-O86-MAMMOTH-BUS-ORIGINAL-SOURCE-20261102.md)：新从完整SHA合格的361255180B后期mixed25私人RAR实际提取35个原源成员共14116B，逐CRC/SHA/长度验证；6个Bus创建各唯一指向6份arg（**300坐标点**，原needstone为50/50/25/30/20/40，waittime全部180）。另26个genout静态原NPC/告示与26份对应原文字节确认；两组各三站共六站，六条路线/12张双端费用牌互核，六张使用方法站牌写明同伴按钮上下车、停站3分钟。**bus.arg第二禁带号403与另五条2403不一致；bus2.arg及bus.create编码不完全合法；一处向导地名与邻近站牌矛盾；3000残留两条无匹配Bus车辆，全部原样留疑**。与2001官方手册的两组三站/三分钟仅做跨年代对照，无法认证容量4、原生不遇敌或同部署。完整[派生SHA/CRC/路线数字](research/recovered/STONEAGE-O86-MAMMOTH-BUS-SOURCE-R1.json)，原脚本和图像不公开。CURRENT历史Git blob不变；NEXT O87轮换另一实源材料，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、percent=null；不做新游戏体验优化。


### 2026-11-02 — O87 原家族留言板、家族秘书邀请函与骑宠同意书源

[O87 原源核验与历史边界](docs/continuity/STONEAGE-O87-FAMILY-BOARD-LETTER-20261102.md)：从完整SHA合格的私人后期混合2.5 RAR定向取证22份原成员，原RAR CRC及逐成员SHA校验一致。原 `fmdengon.create` 有**16条**家族留言板创建坐标，原模板`FmDengon`，窗口支持家族成员列表、家族留言、家族之间留言；其中**15条**在同包地图DAT真实坐标格有三数值，floor3006的DAT在此包缺件，不推原游戏无图。四族长屋原 `fmletter` 秘书菜单含**家族邀请函／骑乘学习同意书**两项；原9个邀请函编号均在同档13,254行×94列`itemset.txt`主键列唯一命中、另9个骑乘同意书编号均不在该列。源配置yes指向5/6但本文件只有1/10/20窗口，保留运行handler与外部表未知，不擅自认定BUG或发放成功。仅静态来源事实，**没有执行原客户端或原商业服，没有真实留言/领函/习骑见证，也不认证JSS1999/TW1同部署**。仅公开[派生源SHA/CRC及结构数值](research/recovered/STONEAGE-O87-FAMILY-BOARD-LETTER-SOURCE-R1.json)，商业原字节不入Git。历史CURRENT blob原样、Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暂停、总体百分比未知；**NEXT O88** 回22域另一具实源游戏内容，不扩泛化家族模拟器或现代体验优化。


### 2026-11-02 — O88 后期保存包第二届家族猎宠活动／妮可／截止日期／猎宠证主表缺项

[O88 具日期原事件证据和精确负例](docs/continuity/STONEAGE-O88-FAMILY-PET-HUNT-EVENT-20261102.md)：重新核对原私人mixed2.5 RAR全SHA及7份原成员独立RAR头CRC／解出CRC／完整SHA，原`race2/second.template`确实注记**第二届猎宠大会**，具名NPC妮可`floor3206:(15,19)`的`npc_raceman`原创建指向`race2/second.arg`，源活动说明要求**族长组织族员按猎宠证捕宠并登记**，而`time_msg`原文字写**2004年12月22日截止**。源`CheckItem/GetItem=20760`在同档13,254行×94列`itemset.txt`原物品号列16**0匹配**；一次相似数字子串属于其它列的`320760`，不得当ID存在。`3206.DAT/MAP`均原尺寸30×40，NPC坐标有效格三层(5000,0,49152)、MAP格0；并未证明原游戏碰撞或NPC真实加载。同档82行`racequiz.txt`无直接脚本关联，不并为猎宠题库。此为**有时间点的活动任务源**，不混同常驻本体任务，也未证明2004年实际运营启用/关停、Raceman行为、记录归零、奖品发放、JSS1999或TW1同部署。原商业字节不入Git，仅[派生数值与哈希](research/recovered/STONEAGE-O88-FAMILY-PET-HUNT-DATED-EVENT-R1.json)。完整历史CURRENT未改，Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暂停、percent=null。**NEXT O89**回22域另一未复原有原件的内容，不重复赛事模拟/原猜谜。


### 2026-11-02 — O89 原始150条世界知识问答的游戏内线索（静态资料，非已运行答题）

[O89 原150题逐行证据与限制](docs/continuity/STONEAGE-O89-ORIGINAL-150-QUESTION-SOURCE-20261102.md)：从私人完整SHA核验的后期mixed2.5 RAR**实际抽取**`gmsv/data/question.txt` 10,821B，原RAR成员头CRC／解出CRC及SHA256一致、原CP950全字节往返。真实原150行ID1—150唯一连续，149行9列、ID8仅8列；非空应答格数**43条仅1项、23条2项、84条3项**；不同问句148个（**1=22、10=47**重复）。题目包含四出生村、长毛象公车/大厅、宠物医院、料理、精灵等可供后续交叉考据的原文本线索，但**选项不等于验证的游戏规则/发行日期**，源数字字段的正确项/题型含义及原服务端题目handler、原生UI全未证。此文件**不是**O51所述另一82行`racequiz.txt`，不推两表同任务；常驻/活动归属UNKNOWN。仅[派生结构与SHA记录](research/recovered/STONEAGE-O89-ORIGINAL-150-QUESTION-SOURCE-R1.json)，原版权全文不入公开Git，CURRENT旧Blob不改，Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暂停、overall_percent=null。**NEXT O90**轮换另一有原资料的实际游戏内容，不扩猜题模拟或现代体验优化。


### 2026-11-02 — O90 后期保存包原72职业技能表、同包启动指针与71数值关联

[O90 有据职业技能恢复与版本界限](docs/continuity/STONEAGE-O90-ORIGINAL-PROFESSION-SOURCE-20261102.md)：从私有完整SHA通过的mixed2.5 RAR独立重新实取原`profession.txt` (9703B) 和 `setup.cf` (9715B)，复核同档`itemset.txt` (3392473B)，逐件原RAR头CRC/实取CRC、SHA、CP950往返一致。`setup.cf`第514行真实指向`./data/profession.txt`。原技能表**72条23列、ID1—72连续、60种回调名**；四组原目标数值位置构成**71条、涉及44技能的直接引用**，其中40组伴值70、16组50、6组60、9组0，全部目标ID在本表内，静态图无循环。**ID5附身术四源关联15/16/17/21**、**ID4冰爆术二直接关联14/17并有14→12的间接链**；“加工”与“連環攻擊”、“自給自足”与“激化攻擊”各共用原回调名，保留原样、不擅判BUG。`profession.txt`原零基列10的72数值在同档13,254×94物品主表**键列16零匹配**，不得误称缺技能或编造道具关联。已明确分开先前R59**大陆2003年7.0网页**与本后期静态包的版本来源，没有原生服务器回调、职业就职、学习/施法、UI执行，更非TW1.0/JSS1999已认证原版。[O90派生71关系及来源校验](research/recovered/STONEAGE-O90-ORIGINAL-PROFESSION-SOURCE-GRAPH-R1.json)，原完整商业表/二进制均未公开；历史CURRENT blob不变，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall百分比未知。**NEXT O91**回22域另一有原实物的世界/宠物/生活服务资料，不扩职业模拟器或新石器体验优化。


### 2026-11-02 — O91 早期玩家问答：愿藏守桥、地面拾取与宠物邮件跨来源核验

[O91 原版玩家时代证词及严谨分源](docs/continuity/STONEAGE-O91-EARLY-BRIDGE-PET-MAIL-FAQ-20261102.md)：新增访问并登记17173页标注**2001-06-14**、作者未知的《石器时代之全问答集》，其中玩家述及北岛愿藏守桥、败后短暂不在与跨桥组队、桥附近盗贼；与此前 O85 **后期混合2.5原字节**的具名NPC/桥段对白**仅作跨材料名称与叙事印证**，绝不将页面玩家技巧推为实际执行、将O85的`time:60`推为消失时长或认证同一build。另将早期地面道具右键拾取/丢弃、宠物邮件名片/邮件状态/附带道具与文字输入等用户操作说明存为**玩家主张**；2001页关于超六级拾宠“自抓例外”与旧2003新浪指南“转生例外”并列保留版本/文本差异，未合并成服务端判定。原HTTP字节/SHA、原游戏客户端/服务器执行仍缺；原商业载荷不公开。仅公开[有界衍生8项陈述、来源位置及负证](research/recovered/STONEAGE-O91-EARLY-BRIDGE-PET-MAIL-FAQ-R1.json)，完整历史CURRENT原Git blob不变、Stage A **7 PARTIAL + 2 OPEN**、Stage B/wiki GATED、R79暂停、总体百分比`null`；**NEXT O92**轮换另一有确凿新实物的世界/宠物/生活服务/本体任务源，避免复述资料充工作量或开发新石器优化。


### 2026-11-02 — O92 2001标签的Lv1宠物获取结构核验

[O92有界原版宠物来源与缺口记录](docs/continuity/STONEAGE-O92-EARLY-PET-ACQUISITION-20261102.md)：重新完整审阅**已有R97引用过**的17173署名依波波2001标签网页，结构化**124条目录编号、28个系列、作者自称亲证85项（未证39项）**；分开**4出生赠宠、9条玩家声称JSS赠品（其中2项R97已登记，另7项新增索引）、17暂无资料、4中文版出现待证**。原网页历史HTML/同版服务端宠物master及客户端建角、真实捕捉均未取得；文章序号不是官方宠物ID或原始物种分母，作者星号不是本项目独立认证。另有限登记网易精华区2001-03-28整理人时间的搜索摘要（直接原网页读取失败，未证独立源）及既存17173抓宠经验的未证概率。仅[派生结构索引](research/recovered/STONEAGE-O92-EARLY-PET-ACQUISITION-CENSUS-R1.json)入Git，不复制全篇受版权保护的原网页或资产，旧CURRENT blob不改；Stage A 7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总体完成率未知。**NEXT O93**跳离重复玩家资料，优先真实同版宠物ID→原图/服务器原始资料或其它具原文件的世界内容，当前严格忠实复原、不提前优化体验。


### 2026-11-02 — O93 新取得的固定Git后期服务端宠物原表与静态来源连接

[O93原源限定报告](docs/continuity/STONEAGE-O93-INDEPENDENT-PET-SOURCE-20261102.md)、[数字/负例清单](research/recovered/STONEAGE-O93-INDEPENDENT-PET-SOURCE-JOIN-R1.json)：直接读取首次纳入的独立公开Git仓库`pimpcapital/longzoro-sa` 2016-01-09提交`57b14e2`及同树5份完整原服务端文本/源码的blob。`setup.cf`实际指向`enemy1.txt`/`enemybase1.txt`，原C装载器以实例模板号连接，图形字段取`E_T_IMGNUMBER`。**“初期拥有”四宠各两个实例（8条）→四原模板→图号100251/100296/100292/100266**；非模拟战斗、非台湾1.0同服身份。两源表2958实例/1816模板的原始数字外键扫描：2934唯一、23缺模板、1实例关联到4个同号模板，均不修改原字节。和O92所谓9个JSS奖品文字仅8个名字字面相同，且多个同名模板、1个未匹配；不认证JSS官方发奖或初代宠物清单。原商业图/完整原表不复制公开仓库，`CURRENT-STATE.md`原blob保留。**NEXT O94**优先取得同构建原图/原出生发放行为、或轮换其它原世界材料；Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总体百分比null。


### 2026-11-02 — O94 后代社区原源码的人物创建宠物发放静态链

[O94 七份源文件的出生发宠、配置及同表数值复核](docs/continuity/STONEAGE-O94-NEW-CHARACTER-PET-GRANT-20261102.md)：新增固定源码实据，`CHAR_createNewChar`在宏条件下取出生村→实例ID1–4并调用真实宠物生成/归属/保存；同树配置PET1=2665、PET2=2744，实际分别映射实例青龙(模板凯恩/图101180/Lv1)与葛多雷诺(图101951/Lv150–160)，后者PETLV=1不会降级。另登记槽0全局复用与空槽-1未跳过的**静态条件风险**，不推历史商业服存在BUG或实际赠送。6实例/模板/图号见[派生数值JSON](research/recovered/STONEAGE-O94-NEW-CHARACTER-PET-GRANT-R1.json)，无新同构建原像素、原客户端/服务端运行，也不升级O93的后代为JSS1999/TW1/大陆1.82官方真值。完整历史CURRENT原blob不变，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null。**NEXT O95**先找同构建原图/真实运行资料，证据不足即轮换真实材料。


### 2026-11-02 — O95 后代六宠图号与四份保存客户端原SPR材料逐项对照

[O95原动画跨版实物索引证据](docs/continuity/STONEAGE-O95-SIX-PET-GRAPHIC-CROSSVERSION-20261102.md)及[6条数值/来源报告](research/recovered/STONEAGE-O95-SIX-PET-GRAPHIC-CROSSVERSION-R1.json)：本轮实际解开TW1.0(464组)/大陆5.0候选(1185组)/台湾8.5候选(1739组)既存完整派生gzip元数据，并对后期mixed25已有847行原索引和O94宠物实例号源逐项验证。六图号中，四个`100251/100266/100292/100296`在TW1/CN5/TW85原SPR组的完整段SHA都逐一相同；`101180`仅在所比CN5/TW85各唯一，完整段SHA一致；`101951`仅在此TW85索引号1637有完整段元数据；后期mixed25仅对前四图号有数值索引。未取得2016社区服务端与任何客户端**同一实际部署构建**的证明；原台湾1.0官方具名宠物/领取事件依旧未证，本轮未重读专有原bin/执行客户端/新绘图。原CURRENT历史blob保持不变。**NEXT O96**轮换原世界、NPC或常驻本体任务实物；Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、整体百分比未知。


### 2026-11-02 — 模块优先全量复原执行规则（2026-11-02）

用户提出停止在宠物/NPC/地图/任务间零散跳跃，改为**按内容模块集中处理**：首个主线[PET-MODULE-01 宠物全源归档与可观察恢复](docs/RESTORATION-MODULE-FIRST-20261102.md)，之后按人物/NPC→地图场景→物品→常驻/活动任务→玩法机制→历史整合；具体执行规则写入[连续性协议 §17](docs/PROJECT-CONTINUITY-PROTOCOL-R1.md)。保留此前22域/9系统与O1–O95全部证据，不推翻原台湾1.0、后期候选的版本分工。每只宠物优先对照**实际原图/动作/数值/技能/获取来源**，跨版比较但不凭图号或名字自动认同一物种，不把原SPR组数误认为宠物种数。已取资料做完后允许明确UNKNOWN，后续新源增量扩展；不要求等待未取得的历代所有客户端。**现最高 NEXT：PET-MODULE-01 SOURCE-BATCH-CENSUS**；此前O96跨域轮换被新模块优先规则覆盖。仍属原游戏忠实复原，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停，完成百分比未知。


### 2026-11-02 — PET-MODULE-01 全表宠物模板/实例与四客户端原SPR候选集中归档

[PET-MODULE-01批量恢复报告](docs/continuity/STONEAGE-PET-MODULE-01-SOURCE-BATCH-20261102.md)与[完整派生数值索引](research/recovered/STONEAGE-PET-MODULE-01-BATCH-SOURCE-SPR-INDEX-R1.json)：在新模块优先规则下直接读取2016社区独立源`enemybase1`1816模板行（PETFLG=1共1024行，0共792行、1813个不同模板ID）及`enemy1`2958实例行（2934唯一关联、23缺失、1个歧义4模板），对PETFLG1的598个**不同图号**批量连接TW1/CN5/TW85/mixed25源SPR索引，命中分别130/344/542/260、四者都无56；数值图号不是官方物种种数，尤其不得以晚期后代名义填早期官方物种。同文件号重号完整保留。公开只留1024条结构化源字段、2958条实例链接、598条图号原资源索引和少数例示，不转载商业原图/整表原名，原CURRENT不改。下一优先 **PET-MODULE-02** 比对另一保存MIXED25的988模板，并联接已私存真实宠物画面；保持宠物模块集中推进。Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总体完成率仍未知。


### 2026-11-02 — PET-MODULE-02 同仓库两份原宠物表640/1816行整表比较

[原表差异报告](docs/continuity/STONEAGE-PET-MODULE-02-SERVER-TEMPLATE-DIFF-20261102.md)和[635共有模板ID逐字段差异数据](research/recovered/STONEAGE-PET-MODULE-02-SERVER-TEMPLATE-DIFF-R1.json)：读取同固定2016社区Git树内备选enemybase.txt640行与配置实际引用的enemybase1.txt1816行，完整行核实635共同ID/364原行一致/271差异，其中221仅融合码一列改变，17标志变化、2图形号变化。不是官方版本演变或官方全宠物数量。历史CURRENT原样保留，继续PET-MODULE-03，先解决原保存混合2.5的988行可读性并关联原图与技能，不跨去NPC地图。


### 2026-11-02 — PET-MODULE-03 同源宠物技能批量联接

[PET-MODULE-03报告](docs/continuity/STONEAGE-PET-MODULE-03-SAME-SOURCE-SKILL-JOIN-20261102.md)及[源限定数值索引](research/recovered/STONEAGE-PET-MODULE-03-SAME-SOURCE-SKILL-JOIN-R1.json)：从2016同仓库原技能表`petskill2.txt`核282条定义并接1024条已有PETFLG1模板，实际正数技能槽2886次，其中2784可静态定位、102无定义（30个不同ID）；另20个原负数槽、4262个空槽完整保留。不是官方初版技能或原客户端执行。988条混合2.5原行仍缺、原SPR未于此包重渲染。**NEXT PET-MODULE-04**继续宠物模块，优先同源`skillcode.txt`与实例/模板的整源外键，或复用私人原图观察关联；不跨域散点跳转。


### 2026-11-02 — PET-MODULE-04 pet skillcode static crosswalk

[Report](docs/continuity/STONEAGE-PET-MODULE-04-SKILLCODE-CROSSWALK-20261102.md) and [source-limited 253-row index](research/recovered/STONEAGE-PET-MODULE-04-SKILLCODE-CROSSWALK-R1.json): 160 instance/template matches, 12 original mismatches, 81 absent instances; 79 source two-character code tokens all have a same-tree skill KINDCODE string. Not original official runtime/training or same-deployment evidence. NEXT PET-MODULE-05: link provenance-qualified private SPR frames and action preview to the pet catalogue; do not rotate to NPC/maps.


### 2026-11-02 — PET-MODULE-05 private source pet sprite visual catalog

[Evidence and acceptance boundary](docs/continuity/STONEAGE-PET-MODULE-05-PRIVATE-VISUAL-CATALOG-20261102.md) and [full 598-graphic / 1024-template coverage index](research/recovered/STONEAGE-PET-MODULE-05-CONSOLIDATED-VISUAL-COVERAGE-R1.json): existing private original-resource PNG/sequence materials were rechecked to form one private offline observer for seven SPR keys, 76 source animation/direction sequences, 718 ordered frame occurrences, and 440 actual archived PNGs. Chromium in-memory playback selectors checked; private art/HTML not pushed to public Git. The 7 graphic keys map numerically to 22 rows of the 2016 community PETFLG1 template source, **not** authenticated official TW1 species. NEXT PET-MODULE-06: expand qualified original image batches and consolidate within the pet module.


### 2026-11-02 — PET-MODULE-06 adds two more original private pet sprite groups

[PET06 visual source record](docs/continuity/STONEAGE-PET-MODULE-06-TWO-MORE-SPR-20261102.md) and [latest 598-key/1024-template consolidated registry](research/recovered/STONEAGE-PET-MODULE-06-CONSOLIDATED-VISUAL-COVERAGE-R1.json): rechecked archived TW1 O28 sprite image source: SPR100297/100298 (52 frame occurrences, 39 distinct bitmap PNGs, six action/direction-zero sequences). One private catalog now carries **9 source graphic keys/82 source animation sequences/770 positions/479 original candidate PNG bitmaps**. Still not original official species identity or native gameplay. Continue PET-MODULE-07 source-ready real pet image breadth; no cross-domain rotation yet.


### 2026-11-02 — PET-MODULE-07 台湾1.0完整原客户端批量宠物图形实际像素

[PET07批量实物报告](docs/continuity/STONEAGE-PET-MODULE-07-TW10-130-REAL-PIXEL-BATCH-20261102.md)及[源限定130组/2176块可解码原图证据](research/recovered/STONEAGE-PET-MODULE-07-TW10-BATCH-PUBLIC-R1.json)：重新取用户私人原 P3H 原始包并全SHA固定，对2016后期宠物模板图号与台湾1.0原SPR取130组数值交集，原7568条SPR动作头全组核验，选原动作0/1/2方向0的390源动画/3255帧，原REAL实际重解码2176个RD块，两个真实越界坏源保留负例。私人统一观察器（不公开商业图片）已覆盖130组/451动作方向/3817按原序帧位/2540候选PNG，Chromium144全部451段可切换/下一帧、0JS/0请求。仅跨版数字参考，非TW1官方130种物种。Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、整体完成率未知。**NEXT PET-MODULE-08**：在这一单一宠物目录连接已保管技能数值，但严格分源；余下468个图号继续查已保管不同版本实际像素，不扩无谓查看器。


### 2026-11-02 — PET-MODULE-08 图形/属性/技能严格分源综合目录

[PET08可核的598图号×1024后期模板目录](research/recovered/STONEAGE-PET-MODULE-08-VISUAL-STATS-SKILLS-SOURCE-CATALOG-R1.json)与[PET08实施及证据边界](docs/continuity/STONEAGE-PET-MODULE-08-SOURCE-SEPARATED-CATALOG-20261102.md)：完整联接PET01/03/06/07现有派生证据。130图号存在TW1原图私人可视数据的**跨年代数字候选**，对应201社区模板行；468未进PET07图像批次（412后期有索引/56四载体均无索引）。2,886正数技能槽=2,784后期同源定义+102缺定义；20负值、4,262空槽完整保持。既有私人PET07原图HTML不改、不公开；无新版官方命名或同服运行证明。**NEXT PET-MODULE-09：**有限查已有CN5/TW85私人原像素补齐后期候选，缺原件即记录止点并按模块顺序转人物/NPC。阶段A/B/wiki/R79、总进度未知不变。


### 2026-11-02 — PET-MODULE-09 原SPR跨版验证与八帧TW85既有原像素归位，宠物阶段性有界止点

[PET09完整598图号来源分级](research/recovered/STONEAGE-PET-MODULE-09-CROSSCARRIER-ORIGINAL-MATERIAL-RECEIPTS-R1.json)及[本轮源证/止点](docs/continuity/STONEAGE-PET-MODULE-09-CROSSCARRIER-PIXEL-BOUNDARY-20261102.md)：130图号在PET07先前有TW1原像素；214图号CN5与TW85原SPR整个动画段已证完全一致但不认证RD像素相同；198仅有TW85索引，其中图号101501早在R30已有源验证8帧原RD索引像素/私人PNG收据，本轮与后期社区模板物理行843/1184仅做**跨年代同号链接**，未重新读取私人像素；另外197仍只有索引，56四载体没有图形号索引。累计按图号有131项**先前有真实原像素证据**，并不是131个官方物种。CN5/TW85整批原商业文件本轮不可直接读取，不能把源索引当已解码图；记录材料阻塞后不重复下载大包。**宠物模块现 SOURCE_BOUNDED_PARTIAL**，继续历史复原下一模块 `CHARACTER-NPC-MODULE-01`。原CURRENT不变、Stage A/B/wiki/R79和overall_percent=null不变。


### 2026-11-02 — PET-MODULE-10：混合2.5原始RAR内988行宠物主表/实例/技能完整实物回读

[PET10原8成员完整数值索引与SHA/CRC](research/recovered/STONEAGE-PET-MODULE-10-ORIGINAL-MIXED25-SERVER-TABLES-R1.json)及[实物与来源边界](docs/continuity/STONEAGE-PET-MODULE-10-PRIVATE-SERVER-MATERIAL-20261102.md)：用户Library现存原RAR361255180B全SHA本轮实际重校，libarchive真取8原成员。主表enemybase.txt有效988行/56字段，PETFLG1有495行、424图号；另一份640行/316宠物候选。2087/1494实例分别与对应模板全数ID匹配；主表147原技能定义支持1050正数宠物槽全部定义，备选56技能定义支持661正数槽中的649，12缺。与原RAR同载体847条SPR索引按数值关联，主表495宠物标记行302命中、234不同图号。私人原CP950全字段目录和无网可查HTML已保管，不向公开Git提供原名/原表正文/版权图。原SPR主体本轮受libarchive解压限制未完整取出，不称动画像素新恢复。PET09此前CN5/TW85大包不可读止点照旧；**PET10额外找回同包服务器实物**。宠物模块保持历史部分/来源限定阶段性闭合，**NEXT CHARACTER-NPC-MODULE-01**；无需替用户再要「继续」。Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总体percent=null。


### 2026-11-03 — CHARACTER/NPC-MODULE-01 完整原NPC目录源批量恢复

[CHAR01精确来源与有限结果](docs/continuity/STONEAGE-CHARACTER-NPC-MODULE-01-MIXED25-NPC-BATCH-20261103.md)及[公开源计数/资格收据](research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-MIXED25-SOURCE-RECEIPT-R1.json)：从私人mixed25原RAR本轮真实解出完整NPC目录2205个原文件/1930332B，原RAR目录7952项逐遍历，2205份原大小、SHA、CRC全部通过。189份NPCCREATE含4985静态创建块，46份NPCTEMPLATE含119原块；配置关联4131同目录唯一+853同RAR他目录唯一+1歧义，1803个原file:引用中1788同目录树有源文件、15缺。源可观察私人HTML已本地Chromium实测，原全目录ZIP成功私有Library保存。**这些是配置条目而不是4985个NPC/人物**，无官方版本/原运行晋级；TW1先前12人物SPR与101静态类NPC图元独立保留。大行级公开索引仅当前会话可取，远端只固定其SHA和源统计，禁止冒称已持久Git。**NEXT CHARACTER-NPC-MODULE-02**：TW1人物12组及静态101候选原帧像素批量归档。原CURRENT及Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暂停/总体percent=null不变。


### 2026-11-03 — CHARACTER/NPC-MODULE-02 台湾1.0十二组人物候选原动作2全帧恢复

[CHAR02来源限定真实原像素/动作完整批次](research/recovered/STONEAGE-CHARACTER-NPC-MODULE-02-TW1-12-ACTOR-ACTION2-RECEIPT-R1.json)及[恢复说明](docs/continuity/STONEAGE-CHARACTER-NPC-MODULE-02-TW1-12-ACTOR-PIXELS-20261103.md)：从已认证TW1原零售P3H私人源包逐全原件SHA重核EXE/SPR/ADRN/REAL/双SAP；12图形候选组（100000～100220每20一组）的完整原SPR段SHA与旧SCENE23逐个一致；动作码2的8方向96条原序列共有728源帧位置/576不同原位图，原REAL实际解出576/576块、严格RD失败0，旧SCENE23的96源首帧像素SHA全部一致。私人完整262602B逐帧证据表与6578861B原图HTML只作当前会话可下载，不在Git上传原商美术；Chrome本地实际96段读图/帧和候选配色、0 JS/0网络。原商业游戏未进入、12个候选并非官方认证角色数、动作/真实颜色/FPS未知。**NEXT CHARACTER-NPC-MODULE-03：TW1源静态NPC-like 101图块原像素批量验收**，源R99里101个源bitmap不能当101 NPC。保留原CURRENT和全部历史边界不变。


### 2026-11-03 — CHAR03：台湾1.0 NPC-like 101原静态图实际RD像素批量复原

[原101图原始RD像素收据](research/recovered/STONEAGE-CHARACTER-NPC-MODULE-03-TW1-101-STATIC-RD-RECEIPT-R1.json)及[本轮源边界说明](docs/continuity/STONEAGE-CHARACTER-NPC-MODULE-03-TW1-101-STATIC-RD-20261103.md)：TW1原P3H同源ADRN/REAL及双SAP实际逐完整SHA核实，5846～5946编号101源原RD块逐原像素实际解码101/101成功、0失败，逐源哈希与原R99全部101项吻合。私人原RGB候选原图联系表及浏览器101图（两配色101/101已载入、0JS/0请求）保存为本轮可取文件，原艺术品不公开Git。**101是静态图像数，并非101个官方NPC**：目视混有人形和床铺、钱袋等物件；原`map_number`不是楼层、后期mixed25 NPC姓名不与早期TW1强行绑定。**NEXT CHAR04**审核人物/NPC同源身份绑定，未得同版主表保持UNKNOWN。原CURRENT及Stage A/B/wiki/R79和overall_percent=null不变。


### 2026-11-03 — CHAR04 人物/NPC创建原件→模板功能→同RAR原SPR图号的全量来源关联

[CHAR04真实原件关联及差异审查](docs/continuity/STONEAGE-CHARACTER-NPC-MODULE-04-STATIC-GRAPHIC-FUNCTION-20261103.md)及[CHAR04全量图号×原模板功能×SPR索引](research/recovered/STONEAGE-CHARACTER-NPC-MODULE-04-SAME-CARRIER-GRAPHIC-FUNCTION-JOIN-R1.json)：从用户私人保存的mixed25原NPC目录ZIP全量核2205原文件、4985创建源块、119模板源块SHA全部吻合；把此前只在用户私人资料/会话保存的[CHAR01 4985行无正文源证](research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json)正式永久入Git，字段仅数值/来源位置/散列及文件引用。原功能Warp配置2904（非2904人），模板唯一定位4984/4985。创建原图号有2482条，其中617条/108不同图号命中同原RAR客户端SPR索引；1865条/146不同图号无本索引；35条原模板type与创建graphicname数值不一致，逐条保留；3个既往R40原完整SPR段号100250/251/252可联30条原创建配置。仅同RAR数值关联，**不是**原运行服同部署、同原图可视像素、官方人物或TW1 NPC姓名身份证明。下一优先CHAR05有源批量原SPR/像素及NPC原用途关系，不重复造图及引擎。Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总percent=null；原CURRENT保持原字节。


### 2026-11-03 — CHAR05：30条NPC源配置对应3组已有原动作像素

依据[CHAR05原始素材复用报告](docs/continuity/STONEAGE-CHARACTER-NPC-MODULE-05-SAME-RAR-ORIGINAL-MOTION-20261103.md)，私人CHAR01子树2205源文件及SCENE13的208个旧原RD均本轮逐SHA复核。CHAR04原617条有索引引用涉及108原图号，仅100250/251/252已具原全SPR和R13旧动作0八方向原像素；分别13/3/14条配置、共30条；余105图号/587引用依然INDEX_ONLY，不冒称已实际复原像素。私人HTML在原图基础上增加30条来源搜索，Chromium载入266图、0错误0请求。原版权素材不入公开Git、旧CURRENT全量保留并加法续接。**NEXT CHAR06**：有原SPR/ADRN/REAL才补105图号，否则转NPC功能对白原件；Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null，尚非新石器开发。


### 2026-11-03 — CHAR06：47条同RAR NPC服务源参数，105图号的实际像素仍受限

本轮按[CHAR06完整来源、解包阻塞与领域内容](docs/continuity/STONEAGE-CHARACTER-NPC-MODULE-06-SERVICE-SOURCE-20261103.md)及[CHAR06 47行派生源SHA/数值目录](research/recovered/STONEAGE-CHARACTER-NPC-MODULE-06-SERVICE-SOURCE-RECEIPT-R1.json)续接：原RAR全SHA相符，2205份原NPC文本逐成员大小/CRC/SHA通过，源静态SavePoint21、Bus7、PetShop16、PetSkillShop3实际参数已联接原创建配置、原文件/原文SHA和路径；另有私人原对白可检索资料页。原SPR/REAL解压未能完成资格化，CHAR05的其余105图号/587源配置仍是INDEX_ONLY，不冒作原图或历史运行。新参数据限社区混合2.5保存载体，不回填TW1官方原服。**最高NEXT CHAR07**：继续人物/NPC模块的TownPeople/告示/其他原文本批量内容来源，随后按模块计划转地图；Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暂停、总体percent=null。巨型CURRENT原历史文本仍完整，本文为非替代的加法指针。


### 2026-11-03 — CHAR07：372份村民文本、180份告示原文实物，15处缺件

[CHAR07成批原文来源与限制](docs/continuity/STONEAGE-CHARACTER-NPC-MODULE-07-TOWNPEOPLE-SIGNBOARD-ORIGINAL-TEXT-20261103.md)和[567条源创建→原文本引用/缺件目录](research/recovered/STONEAGE-CHARACTER-NPC-MODULE-07-TOWNPEOPLE-SIGNBOARD-SOURCE-CATALOG-R1.json)已保存原RAR经CRC/SHA核定的TownPeople387引用（372原文可读、15同RAR全7952成员未得）及SignBoard180引用（180均可读）。552份已得原字节CP950可解码，私人原文观察HTML在Chromium144真实筛选552条原文索引及372/180分类筛选验证通过、0JS错误及外部请求；**552为文本源引用数不是NPC数**。公开Git只有源路径/哈希/地图坐标和编码结构数值，不发布完整商用原对白。未进入原商业客户端/原始世界，未将原文回填TW1或推测逗号分支。**下一优先 CHAR08**：同源交换类NPC实际条件/物品参数有据关联，未证的任务起源保持UNKNOWN；Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null。原CURRENT未覆盖。


### 2026-11-03 — CHAR08：315份交换类NPC配置与同包两版物品ID差异

[CHAR08 源限定归档](docs/continuity/STONEAGE-CHARACTER-NPC-MODULE-08-EXCHANGEMAN-ITEM-EVENT-20261103.md)及[公开数字收据](research/recovered/STONEAGE-CHARACTER-NPC-MODULE-08-STATIC-SOURCE-SUMMARY-R1.json)记录本轮重读混合2.5原RAR的295份 ExChangeMan 脚本/315创建引用、两份原itemset 13254/13915物品ID和380不同静态数值引用（373两表有、5仅候选后表、2两表都缺）。12项完整本地索引测试通过；文件中转故障导致338200B逐行索引没有进入Git，仓库诚实保存源SHA与全数值报告，不称可远端全量逐行重放。具体行为、原服来源、任务起源及官方TW1归属均未证。下一CHAR09核 NPCEnemy原始静态数值，再有界结束人物/NPC阶段并继续地图。

### 2026-11-03 — CHAR09：279 份 NPCEnemy 来源配置 → 230 敌人实例 / 214 模板 / 117 SPR 图号

[CHAR09 原文件恢复与来源限制](docs/continuity/STONEAGE-CHARACTER-NPC-MODULE-09-NPCENEMY-SOURCE-20261103.md)及[公开全源派生目录](research/recovered/STONEAGE-CHARACTER-NPC-MODULE-09-ORIGINAL-NPCENEMY-ROSTER-BRIDGE-R1.json)：实际重读已保存社区 mixed25 RAR 的原 `NPCEnemy` 创建/参数文件，以及两套 enemy/基表与原 `spradrn_5.bin`；279 条源配置/260 原参数，跨 230 数字敌人 ID 全部可分别到两套同载体原实例/模板；117 图号均有唯一原 SPR **索引**。但两套实例原字节全部不相同，模板行只有 145/230 对全同；不能认作同一真实运行配置或台湾 1.0 官方身份，原商业战斗与本批原动画/REAL 像素仍未取得。本轮人物/NPC 模块达到 SOURCE_BOUNDED_PARTIAL 阶段性止点，**下一最高 MAP-SCENE-MODULE-01**，回到已经保管的原地图与场景批量来源整合；Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null、原 CURRENT 历史文件不变。

### 2026-11-03 — MAP01：原地图批量源文件 2990 份验SHA，98组同名内容不同

按[MAP01真实原地图来源与界限](docs/continuity/STONEAGE-MAP-SCENE-MODULE-01-ORIGINAL-MAP-SOURCE-20261103.md)及[MAP01完整派生源目录](research/recovered/STONEAGE-MAP-SCENE-MODULE-01-ORIGINAL-SOURCE-MANIFEST-R1.json)，从私人保留混合2.5 RAR 实际解出并校验2990份原地图相关文件原大小/CRC/SHA，另外63份在本地RAR解压器失败（保留错误、不判原包损坏）。可核客户端MAP1019/DAT971、附加工具MAP997及3份服务器mapset/mapwarp：996对相同名字的两处原MAP有898对全字节同、**98对不同**；965对客户端MAP/DAT两者均读得，其中12 DAT是原零字节占位。原服务器mapset两份分别20157/16803数值行、仅ID10230共同记录不同，mapwarp2981源数值传送端点仅证明配置，不证明实际运行。今后按模块只取已真正核过字节的源地图去观察原画面和贴图关系，不据它推初代官方版本或新游戏体验。**当前NEXT MAP-SCENE-MODULE-02**；Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null及完整CURRENT保留。


### 2026-11-03 — MAP02 three verified original DAT floors, full TW1 source RD batch

[MAP02 original three-floor source and pixel limits](docs/continuity/STONEAGE-MAP-SCENE-MODULE-02-THREE-DAT-ORIGINAL-PIXEL-BATCH-20261103.md) and [all 792 source graphic aliases with original SHA / RD cross-carrier metadata](research/recovered/STONEAGE-MAP-SCENE-MODULE-02-THREE-ORIGINAL-DAT-FLOOR-IMAGE-JOIN-R1.json): re-read three private original mixed25 DAT files for floors **1000 (160×160), 1001 and 1003 (30×30 each)**, all whole SHA verified, with **27,400 cells**, three unaltered 16-bit planes each. 1000 has **752 nonzero source image aliases**; **740** uniquely map to genuine TW1 retail original ADRN/REAL RD and were decoded with original source bytes, **12 remain absent from this TW1 original index**. The three-floor union has **792** aliases, **780** genuine original RD decoded, with no RLE failures; private source catalog has 780 images and contact sheet, never published to public Git. Prior O54 **198** source RD/rgba hashes rechecked; **542** additional floor1000 aliases actually decoded compared to O54's previous scope (not historical first discoveries). Floors 1001 and 1003 share dimensions but source planes differ in **8/51/84** grid positions; never collapse same-sized rooms. MAP01's failed extraction of mixed25 1000.DAT remains an explicit failed record: original full bytes were recovered from an independently previously verified O31 private archive, not as a retroactive MAP01 success. Public [six derived evidence and negative-case tests](tests/test_stoneage_map_scene_module_02.py) and Actions workflow verify metadata, **not original commercial byte replay in CI**. Same deployed historical version, native rendering/collision/engine and complete original world remain OPEN. Stage A7PARTIAL+2OPEN, B/wiki GATED, R79 paused, overall_percent=null. **NEXT MAP03:** source-qualified original 12 missing graphic aliases and 98 MAP01 different source-map files only when original source bytes are actually available; do not invent pixels or engine behavior.


### 2026-11-03 — MAP03 actual 98 paired original MAP bytes and twelve late graphic-index bounds

[MAP03 actual original source audit](docs/continuity/STONEAGE-MAP-SCENE-MODULE-03-98-SOURCE-MAPS-AND-12-LATE-INDEX-20261103.md) and [source-bounded derived catalog](research/recovered/STONEAGE-MAP-SCENE-MODULE-03-98-ORIGINAL-MAP-SOURCE-AND-12-INDEX-R1.json): from the independently SHA-verified preserved mixed25 community RAR, actually extracted and whole SHA/CRC replayed **196 original MAP files**, both sides of MAP01's **98 named client/addon mismatches**. **95** have matching width/height and **6,212 differing source numeric cells out of 505,769 comparable cells**; **3** differ in width/height. SHA-pair dedup leaves **94 independent original content contrasts** (98 filenames retained). For floor1000's previous **12 missing TW1 source graphic aliases** at 14 clustered cell occurrences, **11** have actual verified later mixed25 original ADRN index records beyond TW1's initial index/REAL range; alias **22413** lacks a matching record even in the qualified saved later index. These are **not 11 recovered original images**: full later REAL still not decoded, original commercial deployment unknown. Full original MAP byte pairs/verification replay stay privately in Library, never public Git. Public tests check only bounded metadata and negative evidence guards. Prior MAP01 63 failures remain unchanged. Stage A7PARTIAL+2OPEN, Stage B/wiki GATED, R79 paused, completion percentage unknown. **NEXT MAP-SCENE-MODULE-04:** bulk source-qualified original map DAT cells vs actual available graphics, or bounded gap/rotation when real bytes are unavailable; no artificial game-world content.


### 2026-11-03 — MAP04: 955 actual source DAT floors and 4,166 real TW1 RD pixel source blocks

[MAP04 original-byte and pixel-source evidence](docs/continuity/STONEAGE-MAP-SCENE-MODULE-04-955-DAT-REAL-RD-PIXEL-BATCH-20261103.md) and [rights-safe source-derived catalog](research/recovered/STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json): actually re-extracted 971 preserved mixed25 community RAR DAT files with matching MAP01 whole CRC/SHA; 955 have full source 8+6×cell map structure (2,852,551 original cells), 13 zero byte, 3 two-byte BGM nonmap. Across two source graphic-candidate planes, 5,291 distinct nonzero numeric aliases; 4,166 uniquely matched authenticated TW1 retail ADRN and all 4,166 full original REAL RD blocks actually decoded to indexed pixels (4,063 distinct pixel SHA), zero failures. Remaining 1,125 TW1-unmatched numbers: later source ADRN has 85 unique index-only matches, 2 ambiguous and 1,038 still unmapped. All 4,166 real source blocks have privately rendered candidate PNGs with original Palet1, private offline catalog archived and full roundtrip SHA/4,169 ZIP CRC passed. Existing MAP02 source evidence overlap 764 RD/RGBA/PNG SHA all matched. This is source-qualified candidate image material, not same official deployment, native rendering, collision or playable game proof. Original rights-restricted DAT/REAL/RD/PNG remain private. Stage A7PARTIAL+2OPEN, Stage B/wiki GATED, R79 paused, overall completion unknown. NEXT MAP05 source scene observation and bounded handoff to items/equipment, no new engine or gameplay optimization.


### 2026-11-03 — MAP05 五个原格窗口实际原RD候选可观察，转物品装备模块

[MAP05 原来源限定图像观察与证据边界](docs/continuity/STONEAGE-MAP-SCENE-MODULE-05-REAL-PIXEL-SCENE-WINDOWS-20261103.md)、[公开派生来源索引](research/recovered/STONEAGE-MAP-SCENE-MODULE-05-SOURCE-WINDOW-OBSERVATION-R1.json)：从已保存原DAT1000/1001和MAP04实际原RD私人图集，真正重读/核原SHA和ZIP CRC、497已验原PNG SHA/RGBA，构成五个原坐标窗口15张私人现代观察候选，桃红明确标记缺原图，不假装原引擎画面。地图1000原两个图形候选平面26324非零数字引用，结合MAP02/04有26310次原RD来源联接，**14次/12号无真实像素**；地图1001的948次有源RD，但815次低数值不直接当原画面绘制。私人观察包14,774,654B/SHA `a945fdf91d243019caed85d8f1714518e6d81627457adf1539102ed03aaa013e` 本地18项CRC通过，个人Library上传未成功（不称已云端归档），原PNG/原DAT不公开Git。原生画面/同部署/碰撞/游玩仍未验；MAP01既有失败和1125 TW1无索引数字保留。地图模块SOURCE_BOUNDED_PARTIAL，Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暂停、overall_percent=null不变。**当前最高 NEXT `ITEM-EQUIPMENT-SHOP-MODULE-01 SOURCE-BATCH-CENSUS`**，按模块继续原物品装备商店实物批次整理，绝非新石器开发。


### 2026-11-03 — ITEM01 原物品、装备及商店第一轮全量复原，下一批保持物品模块

[ITEM01原始两套物品主表/台湾1.0原图候选/商店来源和缺件报告](docs/continuity/STONEAGE-ITEM-EQUIPMENT-SHOP-MODULE-01-TWO-SOURCE-TABLES-ORIGINAL-832-RD-20261103.md)、[完整来源证据和私人图集凭证](research/recovered/STONEAGE-ITEM-EQUIPMENT-SHOP-MODULE-01-TWO-ORIGINAL-ITEMSETS-AND-TW1-RD-SUMMARY-R1.json)、[逐ID原行SHA数值目录7分片](research/recovered/item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-01-R1.json)：从私人实际原社区混合2.5 RAR 读取两份原物品主表13254/13915唯一ID、94原字段，13254个共同ID中4303行原SHA同/8951行有字段差异，后一表661ID独有；不把0710文件名当官方版本/时间。实际读取台湾1.0零售原ADRN/REAL/PAL，联合1667数字图号中的836具原索引，832真正原RD解码原像素、4解码失败、831无该原索引。私人832候选PNG及13915行全源文本查阅ZIP5868386B/SHA `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa`，已存用户Library、完整原样回读SHA及838项CRC；原商美术和物品原正文不公开。现有商店224份ItemList源参数、191份NPC创建引用可限源静态联接，区间数值解析仅作候选，不是已执行原商店。公开Git仅可发布数字/散列/源分界及测试，Stage A 7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null。物品模块 **SOURCE_BOUNDED_PARTIAL**，**当前最高 NEXT `ITEM-EQUIPMENT-SHOP-MODULE-02`**：继续有真实原件可验证的物品图、装备与商店来源，保持原版游戏复原而不开发新石器。


### 2026-11-03 — ITEM02 原物品32类数值与四条台湾1.0 RD 越界实物复核

[ITEM02具体来源及限制](docs/continuity/STONEAGE-ITEM-EQUIPMENT-SHOP-MODULE-02-NUMERIC-EQUIPMENT-AND-FOUR-RD-20261103.md)和[全32类及四RD SHA目录](research/recovered/STONEAGE-ITEM02-ORIGINAL-NUMERIC-EQUIPMENT-AND-TW1-RD-BOUNDARY-R1.json)：私人原RAR两套13254/13915行物品表完整字节重新取回、全SHA与94列重验，后一表32原type、10036行六攻防敏列非零，共同13254 ID这六数值列不变；TW1原ADRN/REAL全SHA真实重验，四幅旧失败RD原RLE在末尾0xC2刚好越界一个像素，**未晋级为已解码像素或坏原包**。831个TW1无索引图号仍无原图；后期混合RAR ADRN成员提取受libarchive限制，本轮原后期像素0。公开元数据CI验证ITEM01已存13915行/32类及反例；原版权美术不公开；同服/真实玩法未知。**NEXT ITEM-EQUIPMENT-SHOP-MODULE-03**，有源才补图，否则有界转装备附属/商店/任务。旧CURRENT原字节、Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null均保留。


### 2026-11-03 — ITEM03 原材料83字典、物品组成五槽、36兑换源行／24抽奖源行

[ITEM03真实原源与止点](docs/continuity/STONEAGE-ITEM-EQUIPMENT-SHOP-MODULE-03-ORIGINAL-COMPOSITION-SOURCE-20261103.md)及[数字来源全83/36/24目录](research/recovered/STONEAGE-ITEM-MODULE-03-ORIGINAL-COMPOSITION-AND-EXCHANGE-SOURCE-CATALOG-R1.json)：从私人混合2.5原RAR全SHA核实七份原文件及各成员CRC/整SHA，两物品主表原13915行含5条名称`#`前缀，另一表13254行含2条；这些是**物理记录行**，不能当原运行服已启用ID种数。原itematom 83词典数值关联到物品尾10列的五对材料属性，老/后两表分别78/83标签类型、43622/44806具名槽，13254共有ID的10列**全部未变**。bmitem 36条真实原行的G/I数字模式12个位置循环三次，30条有I（45位置/13不同ID），6条仅G；gambleitems 20普通数字配置、3 NEXT、1 END，四标记行的0不可推成实际奖励。公开只留无商业正文/名字/美术的数字及来源SHA和反例；原server未执行、实际合成/兑换/抽奖未证。ITEM01 832已解码TW1图、ITEM02 4 strict RD失败/831缺TW1索引保留源缺口，物品/装备/商店模块阶段性**SOURCE_BOUNDED_PARTIAL**。**最高NEXT QUEST-STORY-MODULE-01**：批量从已得原脚本/对白与地图/NPC/物品关系恢复常驻任务/运营时点活动/来源不明，三区分开；不凭效果字串推任务运行、不开始新游戏开发。旧CURRENT原blob全字节保留、Stage A 7 PARTIAL+2 OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING、overall_percent=null。


### 2026-11-03 — QUEST01 真实原295事件脚本、315创建配置与1349原控制段来源全索引

[QUEST01原RAR实物复读及活动/常驻边界](docs/continuity/STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EVENT-SOURCE-GRAPH-20261103.md)与[全315创建引用×295原脚本×1349原控制段的逐源数字目录](research/recovered/STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json)：重新取得已保存社区混合2.5原RAR，整SHA/2205原NPC文件1930332B的大小/CRC/SHA全部通过。189份原`.create`中的4985条有效enemy创建配置，315条`changeevent`实参引用对应295份不同原脚本/434873B，原`TYPE`控制段1349（MESSAGE769、ACCEPT494、REQUEST81、CLEAN5），原EVENT条件1349，EventNo1348，按完整原Unicode尾空白审查EventEnd1348；较旧CHAR08的1347区别来自实际`EventEnd`后的全角空格，不删除前轮记录。两份异常源脚本缺各1个EventNo/End；静态可识别59不同非负事件号、63数字`EventNo→EndSetFlg`对和694不同物品数字引用（687双表有/5仅候选后表/2两表都缺），**不等于官方任务、游戏运行路线或奖励执行**。315条创建配置的任务起源**全部UNRESOLVED**，目录名event不能单独证明节日活动，更不可将后期混合服关联回TW1/大陆1.82官方。完整源原文只在个人Library私人离线浏览器（295条实际Chromium内存载入/点击/检索，0JS/0网络），Git公开只发布无商业原对白与原图的逐源数字/散列目录和8项派生验证。**最高NEXT QUEST-STORY-MODULE-02**：继续非ExChangeMan已保存原NPC任务控制族的真实条件/地图/物品批量恢复；常驻、时点活动与不明来源严格分开。不转新石器开发。Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null；`CURRENT-STATE.md`原blob保持不变。


### 2026-11-03 — QUEST02 非ExChangeMan原守卫/传送的188份参数与任务状态来源

[QUEST02原原件复原及严格用途界限](docs/continuity/STONEAGE-QUEST-STORY-MODULE-02-ORIGINAL-WARPMAN-SOURCE-20261103.md)、[全202创建引用×188原参数×313源控制段](research/recovered/STONEAGE-QUEST-STORY-MODULE-02-ORIGINAL-WARPMAN-CONDITION-SOURCE-R1.json)：同一私人混合2.5原RAR及2,205 NPC原文件再按全大小/CRC/SHA实核，原`npcgen_warpman`有202条创建引用、全部对应188份真实原参数文件93110B，其中35份原字面有`NEWWARPMAN`首标、153份无。原`FREE`条件313、`TALKEVENT`标记126、`WARP`整数三元组249，其中43组为0,0,0不能冒作已传送目标；`NPCPOINT`三元组26。另从这些原段恢复62不同字面物品数字ID（61在两份原itemset均有，仅20296只在后表）；17不同非负事件状态数值与QUEST01原EventNo/EndSetFlg集合分别有15/16交叉，**这是同社区保存包静态数值碰巧匹配或引用的证据，不是任务链执行/同官方服/地图打通**。原202条创建保留`NOT_PROVEN_QUEST`和`UNRESOLVED`，不可硬塞常驻或活动；公开只有完整数字/源SHA索引，8项正负元数据测试，原全文不上传Git。**最高NEXT QUEST-STORY-MODULE-03**：继续现存`npcgen_quiz`、`npcgen_timeman`等有源任务相关功能，够则阶段性任务模块止点转玩法，缺源也不编造。Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null，原CURRENT文件未重写。


### 2026-11-03 — QUEST03 原22个答题控制与33个时间NPC参数真实来源

[QUEST03来源/缺字段与任务分类止点](docs/continuity/STONEAGE-QUEST-STORY-MODULE-03-QUIZ-TIMEMAN-ORIGINAL-SOURCE-20261103.md)及[完整56创建引用×55原参数SHA/CRC/数字目录](research/recovered/STONEAGE-QUEST-STORY-MODULE-03-QUIZ-TIMEMAN-ORIGINAL-SOURCE-R1.json)：重用并逐全原件CRC/SHA认证私人NPC树2205文件/1930332B，同原社区混合2.5来源，未在本轮重新核父RAR。`npcgen_quiz` 22创建→22原参数/9975B，22个EntryItem、21个Warp、4个GetItem；`quz_812_28_14` 原源没有Warp，不补造。 `npcgen_timeman` 34创建→33参数/3811B，原time为ALLNOON17、ALLNIGHT9、AFTER7，4个change_msg/change_no。源词不是官方任务归属、原服运行时钟或当年奖励认证；56创建`ORIGIN_UNRESOLVED`，不公开原文/商美术。公开8个正负证据契约测试与独立专项Actions需真实后验。Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null、CURRENT原blob不修改。**最高NEXT QUEST-STORY-MODULE-04：**清理有真实原件的剩余任务控制边界，缺源则按模块顺序转玩法。

### 2026-11-03 — QUEST04 原关卡／动作／特殊事件与2004运营活动的有界归档

[QUEST04原实物、同代报道和严格任务来源界限](docs/continuity/STONEAGE-QUEST-STORY-MODULE-04-SOURCE-BOUNDARY-20261103.md)及[25条原创建配置×25份原参数来源散列／数值目录](research/recovered/STONEAGE-QUEST04-SOURCE-BOUNDED-FAMILIES-R1.json)：从已保存的混合2.5社区原NPC私人ZIP真实重复检验2205原文件/1930332B大小、SHA、CRC并逐配置块切片复核，分别恢复9份猜拳条件（原入场物品数字2751、9组WinWarp/LoseWarp；9个失败目标楼层与QUEST03源答题创建数字相交）、8份动作回应字段、7份event69特殊敌人参数（仅event69_13有3个有界NEWEVENT字段）和1份race2/second.arg竞赛参数；总25原文件/9450B，均为静态原来源候选。后者原文字面2004-12-22，物品数字20760仅存在第二份候选itemset。独立找到2004-12-11《遊戲地帶》关于华义2004-12-08至12-22 08:00第二届全民狩猎赛的同期报道，**历史运营活动可独立列活动档，社区保存脚本尚非认证当时官方部署原件**；常驻/活动/不明任务不混合。另4,387条源创建配置不可据此宣布无任务，后续作为世界机制及相关功能材料。QUEST模块在源限制内阶段性`SOURCE_BOUNDED_PARTIAL`，下一个最高NEXT `GAMEPLAY-MECHANICS-MODULE-01`。Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停，overall_percent=null；历史CURRENT原blob不变。

### 2026-11-03 — GAMEPLAY01 原家族对战场／赛程／庄园／宠物转生参数来源

[GAMEPLAY01来源、家族PK双方原数字和骑乘资格缺口](docs/continuity/STONEAGE-GAMEPLAY-MECHANICS-MODULE-01-FAMILY-ARENA-REBIRTH-20261103.md)及[37创建×33实源参数SHA/CRC数字目录](research/recovered/STONEAGE-GAMEPLAY01-ORIGINAL-FAMILY-ARENA-PET-REBIRTH-R1.json)：再次实际核对已私人保存社区mixed25原NPC 2205文件/1930332B的完整SHA/CRC，恢复家族入场9原参数（同ID双目标）、场内返回9、成员召集5、赛程5、庄园4以及人物/宠物转生1；共33实文件/14611B，其中赛程原ID11–15与9竞技场ID的后五项对应，庄园原ID1–4与前四项对应。9场入口原两目标数字均可联同ID内场楼层，返回目标数字回指入口楼层；并非原服已经实现运行。赛程原整数1000/1200/60/60、庄园等待原整数86400/172800的单位/执行未证。转生源有四地区输入数字、六TENSEI节及有关二次转生后可能无法骑乘的源文本警告，未证实际规则；另外4条`riderman`创建记录无同NPC树源file引用，保持INDEX_ONLY，不能猜补。Git不公开原图/原对白，公开9项本地/Actions测试按实际后验。仍Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null；原CURRENT大blob不变。最高NEXT`GAMEPLAY-MECHANICS-MODULE-02`：优先真实来源合格的宠物、战斗及技能机制继续批量考据，不开发新石器。


### 2026-11-03 — GAMEPLAY02 原骑乘配置 `conff:` 链、7份宠物对话及战斗指引原件

[GAMEPLAY02 同包源证与部署边界](docs/continuity/STONEAGE-GAMEPLAY-MECHANICS-MODULE-02-RIDER-PET-TALK-20261103.md)及[20份原文件SHA/CRC与数值关联索引](research/recovered/STONEAGE-GAMEPLAY02-ORIGINAL-RIDER-PET-TALK-SOURCE-R1.json)：重新完整核对私人社区混合2.5 NPC提取ZIP的2205份原文件、1930332原字节，逐文件SHA/CRC与CHAR01相同；父361MB RAR本轮未重读。GAMEPLAY01此前4个骑乘训练师创建块确实没有`file:`，但实际均用`conff:family/riderman.conf`并存在**3237B真实同包原配置**，4课原窗口等级文字40/80/120/全级及`takegold`原整数5000/10000/15000/20000有源。特别训练师在源创建文件仅被注释，`.old`与候选配置不能当上线年代。另实际核三个骑乘物品参数文件的同SHA备份/9与17个NPCPOINT差异、两份9标题宠物战斗指引、7份`PETTEMPNO`宠物对话关联与132个静态段标题。**所有这些都是社区保存版源文件事实，不是原服务器骑乘收费、捕捉、战斗执行、任何初代官方部署或完整原游戏运行。** 原脚本/对白不公开，公开只保存可重放元数据和否定断言测试；GAMEPLAY01历史原回执不覆盖。主线阶段A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null，原CURRENT完整blob `c89e0e33537990aa2132b47c40fef49a985a935c`保留。**最高 NEXT `GAMEPLAY-MECHANICS-MODULE-03`**：批量考据已取得的战斗和技能实际源证；仍只复原原版，不做新石器体验优化。


### 2026-11-03 — GAMEPLAY03 宠物技能商店21份原配置及23个原技能数字交叉

[GAMEPLAY03 原件与不足界限](docs/continuity/STONEAGE-GAMEPLAY-MECHANICS-MODULE-03-PET-SKILL-SHOP-20261103.md)及[21份原`npcgen_petskillshop`参数/双技能表逐源SHA数字目录](research/recovered/STONEAGE-GAMEPLAY03-ORIGINAL-21-PET-SKILL-SHOP-SOURCE-R1.json)：从已经逐SHA/CRC核过的私人mixed25源ZIP真实读取21条原技能商店创建块对应21份同目录参数、合计2117B；原`skill_rate`字符串1.0/1.1/1.2分别有11/3/7份，原`pet_skill`共150个有数字槽、23不同ID，保留1个原末尾空逗号槽不填造。与已验PET10同RAR`petskill.txt`147行及备选`petskill1.txt`56行逐ID匹配，全部23 ID在两张表都有各自原行/散列；**同归档数字交叉不是同服部署、原宠物技能训练执行、价格计算或任何初代官方玩法鉴真**。不上传源文本/商业美术，公开元数据负例测试已接既有GAMEPLAY01/02工作流，旧`CURRENT-STATE.md` blob `c89e0e33537990aa2132b47c40fef49a985a935c`不覆盖。Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null。**最高 NEXT `GAMEPLAY-MECHANICS-MODULE-04`**：回已证战斗技能协议/客户端材料核具体原生调用，证不足则有限止点，不开发新石器。


### 2026-11-04 — GAMEPLAY04 台湾1.0原生战场SAB读取函数及8个静态调用点

[GAMEPLAY04 实际原二进制与源边界](docs/continuity/STONEAGE-GAMEPLAY-MECHANICS-MODULE-04-TW10-NATIVE-SAB-LOADER-20261104.md)及[原函数VA/源码散列、8处调用点、218原SAB逐源回验](research/recovered/STONEAGE-GAMEPLAY04-TW10-NATIVE-SAB-LOADER-SOURCE-R1.json)：本轮重新读取已认证台湾1.0私人P3H原包372626292B，379成员ZIP CRC通过，实际原`sa_3.exe` 425984B/SHA与O40完全一致。旧O40只发现218个原`battleMap`文件名字面量而**未定位原函数**；本轮由原32位PE机器码确定读取函数`VA0x401260`、8处真正相对CALL、218个源路径指针表、`rb`文件打开包装、4B头的`SAB`子串检查、400次小端双字节源格读入、20×20逐格调用及148～150特殊整数分支。218份原SAB全真重新读取，各804B/源头`SAB `、87200源格/2296不同源数字、217不同整文件SHA及145/146同字节**与既有O16旧成果一致，不算本轮新发现**。原exe源码路径`battleMap`与ZIP路径`battlemap`逐字大小写不同，218项仅显式不区分大小写匹配。本轮是 **STATIC_COMPILED_SOURCE**，尚无原生客户端运行IO、战斗遭遇选SAB规则、技能执行或初代官方同服服务端；源EXE/SAB/商业图像不入Git。旧CURRENT完整SHA `c89e0e33537990aa2132b47c40fef49a985a935c`全字节保持，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总体百分比未知。**下一最高GAMEPLAY-MECHANICS-MODULE-05**：同来源实际宠物店寄放、治疗及记录点等玩法功能参数批量恢复，不重编现代交互或改善体验。


### 2026-11-04 — GAMEPLAY05 原宠物店、记录点、治疗NPC的77创建配置与38份实物

[GAMEPLAY05源实物/字段边界与异常说明](docs/continuity/STONEAGE-GAMEPLAY-MECHANICS-MODULE-05-PETSHOP-SAVEPOINT-HEAL-20261104.md)及[完整77原创建记录/38份源文件散列/派生数值索引](research/recovered/STONEAGE-GAMEPLAY05-ORIGINAL-PETSHOP-SAVEPOINT-HEAL-SOURCE-R1.json)：从已存社区混合2.5私人NPC ZIP真正复核相关77原创建块及38份参数/12707B，全源SHA/CRC与CHAR01历史账一致；父RAR本轮未重新读取。原`npcgen_petshop`16创建及16参数、`npcgen_savepoint`22创建及22参数，另`winhealer`27+普通healer4+fmhealer4+charm4条内联创建。宠物店原`nomal_rate`1.0/0.6/0.7分别13/2/1，`pool_cost`200×5、2000×1、10条字段缺失（不能认0），14条特殊倍率1.5原文。记录点22源ID与原Born三元组，21有GetItem/1缺该字段，209个原候选词槽/116不同物品数字；对现存两原itemset，110数字两表有、仅1732–1737六数字只在备选表。原`1991*`不完整数量、`poru`六个不带数量的物品表达保持，不修源。27医疗配置有14种原四值组合。**所有结论只证明社区保存版静态原件与候选数值，不等于原交易、存储/扣物品、重登录、治愈、收费或TW1/JSS初版运行已验证**。不公开商业原对白/图像，继承CURRENT全字节旧blob `c89e0e33537990aa2132b47c40fef49a985a935c`，Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暂停、总体percent=null。**最高NEXT GAMEPLAY-MECHANICS-MODULE-06**：原捕捉及其他玩法/原UI音效剩余有证材料，证不足则作玩法模块有界止点后进入跨模块历史整合。


### 2026-11-04 — GAMEPLAY06 原交通、飞行、传送、物品寄放和窗口/排行 57 创建配置

[GAMEPLAY06 真实源档、受限归属及缺件报告](docs/continuity/STONEAGE-GAMEPLAY-MECHANICS-MODULE-06-TRANSPORT-WINDOW-20261104.md)和[57原创建SHA/29源引用路径/28原参数文件与数值的完整来源目录](research/recovered/STONEAGE-GAMEPLAY06-ORIGINAL-TRANSPORT-WINDOW-AND-ITEMPOOL-SOURCE-R1.json)：再次实际阅读私有混合2.5原NPC 2205成员ZIP中相关57创建块与28份不同原参数文件，全原字节SHA/CRC与CHAR01已出版原件账一致，28实文件27840B；另一原`sainasu/jujutu01.conf`在保存源树中**缺失**，仍有四条`windowman`创建实际引用，不能造源。源族分布`bus`7、`airplane`5、`transman`7、`npcgen_poolitemshop`5、`bankman`8、`windowman`17、`duelranking`8。原巴士7份/311对二维路由数值；飞行5份/61组三值航线点、oneway原1有2份；传送3原实文件引用7组原WARPPOINT/每项源`LV>0`，7创建实际复用；寄放4原参数有`cost:50`，其中2份整SHA同；银行源有1号窗同时指向本文件未定义的5/6；8份实存窗口参数共有61原`winno`；排名8创建无参数原文件。运输`denieditem`原字段**403**出现5原文件、**2403**出现在6份，另1份无该字段，保持异源字面不“修复”。**所有均是后期社区保存版静态配置，并非已执行交通、扣钱、传送、寄存、银行或原窗口点击，更非JSS1999/TW1/CN1.82当年部署**。原商业源文/图不公开；旧CURRENT原blob `c89e0e33537990aa2132b47c40fef49a985a935c`不重写。仍Stage A 7PARTIAL+2OPEN、B/wiki GATED、R79暂停、整体percent=null。**最高NEXT GAMEPLAY-MECHANICS-MODULE-07**：查看已得捕捉/宠物技能原始行为来源并确定玩法模块有证止点，之后进入跨模块整合，当前不做新游戏开发。


### 2026-11-04 — GAMEPLAY07 27份真实GetPet脚本、24条创建关系及230原NPC敌人的双源技能对照

[GAMEPLAY07 全源界限与捕捉/发宠/敌人技能三条机制区别](docs/continuity/STONEAGE-GAMEPLAY-MECHANICS-MODULE-07-GETPET-WILD-SKILL-20261104.md)及[全部27原NPC脚本、29条GetPet指令行SHA/44次数字、230敌人实例和214个原双候选模板的可验证数字目录](research/recovered/STONEAGE-GAMEPLAY07-GETPET-NPCENEMY-ORIGINAL-SKILL-SOURCE-R1.json)：本轮真实重读私人社区混合2.5 NPC ZIP全2205成员/1930332B并全部逐SHA/CRC核验，发现27份原件具有29条严格`GetPet:`脚本指令（44数字引用/36不同ID）；其中2份原`.old/.BAK`是备份。严格同包CHAR01 `changeevent`创建记录可直接引用23份源脚本/24原CREATE块，另外4份无直连创建记录，不能视为已运行或从来没运行。`quiz/equiz_04`与`.BAK`原数字351/352不同，`jaruga/event/oev_edb`原同一指令重复482两次，都原样保留。36个`GetPet`数字仅有26与保存第一套`enemybase`ID数值相同、7与第二套相同，**同整数不是已验证同ID命名空间，非已发宠物数，也不是野外捕获**。

同时将已核原CHAR09 `NPCEnemy` 279 CREATE/230实例→214原模板/117图号与PET10已核两套原宠物模板、两份技能主表真正合并检查：230实例按模板来源标志 `PETFLG` 0/1分别142/88（**不是实例捕捉资格、宠物种数**），214模板在两候选表已发布数值字段213同/仅ID651技能槽原`0`对`50/51/52`不同；230实例重复展开有530/533正技能槽引用，39不同正技能ID均在两份原技能候选主表有定义，其中19个与GAMEPLAY03原技能商店23 ID数字交叉。O59此前两个野外捕捉源候选敌人119/122并不在这230个NPCEnemy实例中，旧O59资格仅作为**独立来源**验证，不重算成新发现。保存的父361MB后期RAR本轮未重读，不认证单一运营服、原师徒发宠、脚本执行、技能生效、捕捉概率或官方TW1/JSS1999等价；原商业脚本与图片不入Git。旧CURRENT大blob `c89e0e33537990aa2132b47c40fef49a985a935c`原样保留。Stage A仍7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总体percent=null。**下一最高`INTEGRATION-MODULE-01`：**依原模块顺序将宠物、NPC、地图、物品、任务和玩法的已证同源关系简洁整合；游戏仍不可称原客户端可玩，不进行新石器设计或体验优化。


### 2026-11-04 — INTEGRATION01 原NPC/宠物/任务/物品/地图的同源证据链组装

[INTEGRATION01 直接证据组合与原地图读错限制](docs/continuity/STONEAGE-INTEGRATION-MODULE-01-ORIGINAL-SOURCE-GRAPH-20261104.md)及[24条GetPet创建→QUEST01脚本→ITEM01原数字→MAP01原楼层/279条NPCEnemy创建→ARG源敌人ID→PET10候选模板/原地图的完整来源索引](research/recovered/STONEAGE-INTEGRATION01-NPC-PET-QUEST-ITEM-MAP-SOURCE-GRAPH-R1.json)：复用原社区混合2.5归档早已按来源SHA验过的CHAR09、GAMEPLAY07、QUEST01、ITEM01、MAP01，不再重复解压361255180B父RAR，也不编一套游戏运行框架。GAMEPLAY07中23份有CREATE直连的原GetPet脚本和QUEST01按原文件路径、文件SHA、创建块ordinal全部严格对应：**24条直接静态边**；这23脚本在QUEST01源索引下共有116原控制段、309次物品候选数字、101不同ID，均在两套已验itemset各有原行，但不能认定实际消费/发放或每一候选整数都是道具。对应24创建楼层，MAP01组0原MAP+DAT两文件实读均有21条、仅MAP1条、两文件均未成功解出2条，后者保留原提取错误而**不是原版无地图**。CHAR09原279条NPCEnemy创建/260原ARG文件，**3930次ENEMYNO、7000次ENEMYPETNO数字**，全部在230原敌人实例→214候选模板/117SPR图号链有静态数字源；279条创建楼层在MAP01组0原地图文件中，MAP+DAT均成功可读168、仅MAP100、仅DAT6、均不可读5；其中111创建楼层有原提取失败，不能以不可读推定源文件缺失。两队列合计涉及60不同源楼层，源原图/场景原生绘制及同部署未被认证。公开只留数字、路径、sha/CRC和来源约束；原台1正式客户端与后期混合资料绝不强行同服。这是**SOURCE_BOUNDED_PARTIAL**来源图的真实组装，不是复刻世界运行或新石器开发。旧CURRENT原blob `c89e0e33537990aa2132b47c40fef49a985a935c`全字节保持，Stage A 7PARTIAL+2OPEN、B/wiki GATED、R79暂停、整体百分比null。**下一最高INTEGRATION-MODULE-02**：优先在已观察真实原像素、原MAP/DAT与其版本来源边界内组装可见原场景，不伪造缺图或官方同服。


### 2026-11-04 — INTEGRATION02 60座原NPC/任务楼层的DAT与台湾1.0真实RD像素来源边界

[INTEGRATION02原版场景静态整合](docs/continuity/STONEAGE-INTEGRATION-MODULE-02-DAT-RD-VISIBLE-SOURCE-20261104.md)与[完整60楼层原DAT—已验RD源链](research/recovered/STONEAGE-INTEGRATION02-ORIGINAL-SCENE-DAT-RD-CROSSMODULE-R1.json)：复用INTEGRATION01原24条GetPet与279条NPCEnemy创建关联、MAP04原955份DAT和4166原TW1 RD真像素源收据、MAP02/05原1000/1001图像候选。不重新取得版权图像：60楼层中55份同归档原DAT完整SHA精确匹配，1000由O31独立原件得到来源资格（旧MAP01解压失败保留），另100/200/3000/3021四层仍无完整DAT，3021涉及100条NPCEnemy创建候选。55楼层前两平面400100次非零候选数值引用中390351次命中TW1已真实解码RD、9749次无该版候选；1000层26324次中26310命中/14未命中12图号。所联MAP05五个先前私人原像素窗口中四个属1000、一个1001并无本轮任务NPC楼层关联；同RAR与台湾1.0跨来源不等于原服同部署，不证明原生渲染/碰撞/NPC实际出现/原游戏已可玩。测试防止重名冒作SHA、失败冒作缺件、原图候选冒作原native行为。CURRENT原blob c89e0e33537990aa2132b47c40fef49a985a935c全字节保留；Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null。**最高NEXT INTEGRATION-MODULE-03**：对已有同载体人物/宠物原图与楼层关系作有证据的最小可见整合；缺精确可视证据则进行Stage A历史缺口验收，不转新游戏开发。


### 2026-11-04 — INTEGRATION03 原NPC动作整SPR字节—地图DAT—敌人像素候选的有界整合

[INTEGRATION03证据及历史边界](docs/continuity/STONEAGE-INTEGRATION-MODULE-03-NPC-SPR-DAT-SOURCE-20261104.md)和[逐源派生图号/原动画SHA/地图证据](research/recovered/STONEAGE-INTEGRATION03-ORIGINAL-NPC-SPR-DAT-VISUAL-SOURCE-R1.json)：重用已验CHAR05的30份原NPC动画 CREATE/三原SPR源段、INTEGRATION02的60个原DAT楼层和PET07真正已解码台湾1.0原RD收据，获4条原CREATE在11006/2000/20401三层同社区归档完整DAT SHA，涉及原SPR 100250/251/252三组，其原完整段SHA与台湾1.0原SPR源字节**逐一完全同**。同数字不作为同图判断，使用真实整SHA；仍非原正式同服或客户端已经显示NPC。另将CHAR09原230实例/117图号对照PET07的130组真实原RD，96图号只有**数字**跨来源候选、21无候选：279 NPCEnemy 创建中269至少有1候选、54全部数字图号有候选；不是同源SPR整SHA、原宠物种数、原生出场或捕捉执行。原版权素材不公开，新增原图0；继续Stage A 7PARTIAL+2OPEN/B与wiki GATED/R79暂停/overall_percent=null，原2.7MB CURRENT blob `c89e0e33537990aa2132b47c40fef49a985a935c`不改。**最高NEXT Stage A来源缺口总审计**：优先记录原JSS1999和大陆1.82初代同部署/真实可运行原世界不可验证点，以及100/200/3000/3021原DAT缺件；新证据触发才开新微支线，不做Stage B优化。


### 2026-11-04 — Stage A四个原DAT缺口与跨模块原CREATE实证审计

[Stage A四层原DAT与实际影响报告](docs/continuity/STONEAGE-STAGE-A-ORIGINAL-DAT-SOURCE-GAP-20261104.md)及[4楼层107原创建引用/精确RAR错误的只读数字审计](research/recovered/STONEAGE-STAGE-A-ORIGINAL-DAT-AND-SAME-BUILD-SOURCE-GAP-R1.json)：沿最新main原MAP01/INTEGRATION01/02/03/九领域旧审阅的实际Git blob复盘，60楼层已有55整DAT SHA和1000独立源认证，余100/200/3000/3021四层DAT完整原件仍未可读，影响2条GetPet/105条NPCEnemy原静态创建。3021含100条NPCEnemy CREATE，来自同一`doujyou/jyajyadou.create`、指向100不同ARG原文件（**不是100种宠物或100次已打仗**）；其MAP在community归档两个目录各有整SHA相同的可读原件117224B，DAT宣称351656B但先前327680B后CRC报错。全部4楼层原MAP/DAT宣称长度符合8+3×(MAP长度−8)，仅证明归档声明尺寸相容，不代表原DAT已取得、原服缺地图或真正运行。保留全部MAP01旧63读取失败、无补造像素、无新原文件，新版Git只发可核数字路径/散列/源条件与负例。Stage A九族仍7PARTIAL+2OPEN，B/wiki GATED、R79暂停、overall_percent=null。CURRENT全字节/原blob c89e0e33537990aa2132b47c40fef49a985a935c保留。**最高NEXT**：有合格新原件再重开同版初代原客户端运行/商服来源及3021.DAT确切全字节恢复；证据不足停止扩写助手/所谓完成率，不转Stage B。


### 2026-11-04 — Stage A私藏原RAR完整重取与4楼层CRC失败实证、2003纪念1.82来源隔离

[原RAR真实再读/CRC失败与止点](docs/continuity/STONEAGE-STAGE-A-ORIGINAL-RAR-BLOCK-REPLAY-20261104.md)、[含8原成员压缩流SHA/CRC、原文件头和负面资格的机器回执](research/recovered/STONEAGE-STAGE-A-ORIGINAL-RAR-BLOCK-REPLAY-CN182-PROVENANCE-R1.json)：从私人Library**真正取回**361255180B原RAR，整SHA`d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`与旧MAP01完全同。再次用libarchive3.7.4低层`archive_read_data_block`实际读原RAR：`3021.DAT`351656/351656B、`3000.dat`135008/135008B但原成员CRC分别预期`c0d8a645`/实际`0eb2e1fd`、预期`8a628975`/实际`4de1a6cb`，**不能升级为已恢复原DAT**；3021候选头0×0亦与合格原3021.MAP 407×144矛盾。100.DAT只输出162560/3840008B、200.dat只2457600/5760008B且各报过滤器/Prefix错误。对照2000.DAT全135008B+CRC+整SHA均与MAP01已认证原件吻合、同包两份3021.MAP也全CRC/SHA相同；另1000.DAT输出全长度仍CRC坏，说明“字节数够”不是验收。非第二解压器独立成功；未判原RAR是真实损坏还是单解码器问题，不公开版权原DAT、仅数字散列。同期华义2003周年活动与服务限制由当时新浪/17173转载实证：2003-03-21纪念1.82服、原地登出/交易暂不开、可用当时5.0“宠物进化史”客户端登入；2003-08月迁服公告另存于历史年表和来源登记，**与2001大陆1.82初代、原正式客户端字节及TW1.0不混淆**。Stage A仍7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null，CURRENT旧2.7MB原blob完整保持。**最高NEXT**：找真正独立解压器或者可合法认证第二份`3021.DAT`后再试CRC/尺寸/原档来源；不能回填未证原像素/碰撞。早期同版服务端真证也优先。一无实物即止，不启动新石器设计。


### 2026-11-04 — Stage A：3021道场100弟子/200静态跳跃配置与3022双层原地图同字节证据

[私人原RAR重新实读与完整来源/止点](docs/continuity/STONEAGE-STAGE-A-3021-3022-ORIGINAL-STATIC-ROUTE-20261104.md) / [可核数字综合目录](research/recovered/STONEAGE-STAGE-A-3021-3022-ORIGINAL-STATIC-ROUTE-CONTENT-R1.json)：原同保存载体`doujyou/jyajyadou.create`整44134B/SHA回读核CHAR09，实际300个CREATE配置=100个编号弟子（10×10中心网格）+200个跳跃配置（静态目标3022/(1,7)）；300中心全部在已验3021.MAP 407×144格内，未证明挑战/跳跃实际执行。目标3022客户端MAP两份、DAT三层与同包服务端LS2MAP两层均已真正解压并通过原RAR头CRC/全SHA；其15×15大小一致、前两层原格225+225在大小端规范化后**逐值完全同一**，客户端独立事件层保留不补零。是来源明确的**静态配置→目标图数据**连接，不等于当年同服运行/正式官方身份。3021.DAT CRC仍未通过，原生游戏与初代/JSS同版缺件OPEN。Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null和旧完整CURRENT原blob保持不变。最高NEXT：只有独立RAR3解压器或可信原件出现才重开3021.DAT，或转向其他源可读的原游戏实际内容模块；不得做无证优化和脚手架。


### 2026-11-04 — Stage A：独立解压补齐 63 个原地图文件，复原 3021 道场和后期地图图块

[来源、对照结果与续接](docs/continuity/STONEAGE-STAGE-A-INDEPENDENT-RAR-MAP-PIXEL-RECOVERY-20261104.md)及[数字证据收据](research/recovered/STONEAGE-STAGE-A-INDEPENDENT-RAR-MAP-PIXEL-RECOVERY-R1.json)。从相同私人混合 2.5 RAR 以 7-Zip 和 UnRAR 分别提取，3,060 项逐字节一致且通过原长度和 CRC。MAP01 原 63 条读取失败全部恢复，其中 100、200、3000、3021 的客户端 DAT 补齐 INTEGRATION02 四个楼层缺口。3021 同包服务端 LS2MAP 也已恢复，和客户端 DAT 前两层各有 14,080、42,921 个格值不同，分别保留。3022 对照前两层完全一致。763,908,374 字节的后期 REAL 完整通过原 CRC，1000 层旧 12 个缺图号有 11 个取得原索引像素，22413 两处仍缺。生成 1000、3021、3022 的私人静态预览，原服运行和初代版本归属仍待证。原 CURRENT blob 全部保留。另逐份验真 100 道场弟子 ARG，99 个原参数指向 3021 内下一处，第 100 个指向 3008/(20,20)，与另 200 个指向 3022/(1,7) 的跳跃配置分开。**最高 NEXT** 查找同源原行为实现或可复验运行环境，核实两条路线的触发与实际落点。Stage A 7 PARTIAL + 2 OPEN，B/Wiki GATED，R79 暂停，overall_percent=null。


### 2026-11-04 — Stage A 同包原 GMSV/SAAC 账号连接配置先决条件

[原配置静态连接证据与严格运行缺口](docs/continuity/STONEAGE-STAGE-A-GMSV-SAAC-CONFIG-PRECONDITIONS-20261104.md) / [原RAR三配置整件SHA/CRC及数字验收](research/recovered/STONEAGE-STAGE-A-GMSV-SAAC-ORIGINAL-CONFIG-PRECONDITIONS-R1.json)：独立重新从私人保存的社区混合2.5原RAR（361255180B，整SHA `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`）实际取出并按原RAR CRC/长度与原件SHA验真 `gmsv/setup.cf`、`gmsv/setup.cf.bak`、`saac/acserv.cf` 三份原配置。GMSV原参数指向本机SAAC 9200端口，游戏监听9065端口，两端账号认证原字段逐字节相同（**不公开认证原文或单独摘要**）；原NPC模板上限256、创建上限8192仅是配置参数。复核此前原服务端90秒监听9200/9065、716地图和119模板已记录，不追认为本轮新运行或双方连接完成。**真正的已建立TCP会话、NPC创建、原客户端登录与道场原生传送仍OPEN**；原客户端/服务端来源为后期社区混合2.5，不能混作JSS1999、TW1或大陆2001版1.82的官方实际运行。Stage A 7PARTIAL+2OPEN、Stage B/wiki GATED、R79暂停、overall_percent=null；原CURRENT blob `c89e0e33537990aa2132b47c40fef49a985a935c` 原样保留。**最高 NEXT：** 使用已认证的原EXE与隔离来宾，验证地图/模板加载后原GMSV→SAAC真实连接与NPC创建阶段；无合格运行条件即保留缺件止点，不造原游戏运行证据。


### 2026-11-04 — Stage A strictly single-player/offline content priority (supersedes MMO handshake NEXT)

User reconfirmed the purpose: **restore original game maps, pets, NPCs, quests, images, items, sound and mechanics**, for an eventual single-player game. Original client AND server files are used as **data sources**, but no account creation/login, server authentication, socket handshake, or online game infrastructure is needed to restore these contents. This changes *work priority* only: old authentic GMSV/SAAC socket/configuration research and unresolved native behaviors remain preserved.

[DD-031](docs/DESIGN-DECISIONS.md), [continuity protocol section 18](docs/PROJECT-CONTINUITY-PROTOCOL-R1.md), and [the offline evidence/next-work note](docs/continuity/STONEAGE-STAGE-A-OFFLINE-GAME-CONTENT-PRIORITY-20261104.md) are authoritative over the previous GMSV-SAAC runtime NEXT. Retrieved the private O68 offline pet-shop observer with unchanged original ZIP and HTML SHA; actual Chromium re-test displayed the 2040-by-1559 source-derived scene, completed east 8-step/west 9-step movements, and had no script errors or external requests. This is an **offline archaeological scene observer**, not an original-game executable or official version proof; commercial imagery remains private. The full historical CURRENT Git blob c89e0e33537990aa2132b47c40fef49a985a935c is unchanged. Stage A 7 PARTIAL + 2 OPEN, Stage B/wiki GATED, R79 paused, overall percent unknown.

**Highest NEXT: STAGE-A-OFFLINE-WORLD-CONTENT-01**. Reuse already authenticated real 1000/3021/3022 MAP/DAT and original graphic blocks with existing offline viewers; deliver another concrete offline visible scene or source-qualified content relationship, not duplicate viewers, network servers or premature new-game development.


### 2026-11-04 — STAGE-A-OFFLINE-WORLD-CONTENT-01 原百人道场整层离线资料观察

[原本源、完整100条弟子/200 Warp数字地图关系、私人浏览器验收与限制](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-01-DOJO-SOURCE-ATLAS-20261104.md)及[100 ARG整SHA/配置目标/源 MAP 格值公开完整索引](research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-01-DOJO-SOURCE-ATLAS-R1.json)：在已认证的社区 mixed25 原RAR与保管的2205原NPC ZIP上**重新实读**3021.MAP、3022.MAP/DAT（全SHA+原RAR CRC），以及原创建文件44134B/300块和100份 ARG。恢复407×144原3021 MAP代码格与100名弟子中心、200独立跳跃点的逐源原始坐标/格值：弟子1–99 ARG 静态目标3021不同点、第100名3008/(20,20)；200 Warp创建的另一条独立配置目标3022/(1,7)，其原3022 MAP+DAT三层格值同时读出。复用此前原 RD 静态拼合局部图，无新创造商业原美术，私人单文件HTML可离线选择任意弟子/查看ARG目标/切换原3022数据层。真正 Chromium 100选项、两图加载、源参数数值与按钮实测通过，0JS异常/0外网请求；私人HTML已保存在个人Library，原商业原MAP、对白、图像不上传Git。**此为静态来源可视，不是游戏客户端或实际触发战斗/跳跃**。旧GMSV/SAAC联网任务继续非阻塞，旧CURRENT整个 `c89e0e33537990aa2132b47c40fef49a985a935c` 原字节保留。Stage A仍7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null。**最高 NEXT STAGE-A-OFFLINE-WORLD-CONTENT-02**：利用已有1000村庄原图与同载体NPC原配置/任务源，恢复一批可直接定位的实际离线原内容关系，避免重复造观察器、运行网络服务或开始新游戏设计。


## 2026-11-04 Offline source record (WORLD03 latest)

WORLD02 [village1000 original NPC/scene source](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-02-VILLAGE1000-NPC-SOURCE-ATLAS-20261104.md) is accepted. WORLD03 [all 32 village1000 original Warp CREATE and DAT source-cell reconciliation](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-03-VILLAGE1000-32-WARP-DAT-20261104.md) also preserves every original source-bound target without claiming historical native gameplay or official TW1 co-deployment. Current **NEXT STAGE-A-OFFLINE-WORLD-CONTENT-04** moves to new source-bearing original content outside repeated village/dojo static atlases. Original giant CURRENT blob unmodified; Stage A7 PARTIAL+2 OPEN, Stage B/wiki GATED, R79 paused, overall percent unknown.


## 2026-11-04 — Stage A WORLD04 three-village original text source (latest)

Source-qualified original NPC and signboard content from preserved later mixed25 data has been grouped for floors 2000, 3000 and 4000: 46 previously CHAR07-indexed external texts plus one newly documented inline CREATE-name arena board (47 source entries). The private offline source text bundle is retained outside Git; public source hashes, source-map DAT identity and strict non-native-execution limits are in [WORLD04 continuity](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-04-THREE-VILLAGE-TEXT-20261104.md). This supersedes WORLD03's NEXT. **Current highest NEXT: STAGE-A-OFFLINE-WORLD-CONTENT-05** (new original pet/quest/item content linkage). Stage A 7 PARTIAL + 2 OPEN; Stage B/wiki GATED; R79 paused; overall percent unknown. Full CURRENT historical Git blob unchanged.


## 2026-11-04 — WORLD05 original GETPET quest → enemy instance → pet template → SPR source join

[WORLD05 original-source-derived relationship and explicit candidate-table conflicts](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-05-GETPET-PET-SOURCE-20261104.md): from already original-byte-verified **later community mixed25** source indexes (no original RAR reread this unit), reconcile 24 CREATE/QUEST references, 41 GETPET numeric occurrences, 36 distinct original enemy instance identifiers across both candidate enemy tables, 36 corresponding referenced pet templates in both candidate base tables, and 36 single-record preserved SPR graphic-index candidates. **26 direct ID collisions must not be joined as template IDs**; 3 template PETFLG differences (IDs 718, 719, 720) remain unresolved. Source metadata, regression tests and source SHA provenance only; original commercial scripts/sprites kept private, no historical client gameplay or actual reward execution proven. Full CURRENT blob `c89e0e33537990aa2132b47c40fef49a985a935c` unchanged, Stage A 7 PARTIAL+2 OPEN, Stage B/wiki GATED, R79 paused, overall percent unknown. **Highest NEXT WORLD06:** only real qualified original sprite/quest imagery or interaction evidence, not repeat generic viewers nor any MMO account/network implementation.


## 2026-11-04 — WORLD06: 36 source-qualified original TW1 pixel candidate images for GETPET cross-module graph

[WORLD06 actual private original-image replay and 36 source-qualified public receipts](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-06-PET-GETPET-TW10-PIXEL-20261104.md): materialized the prior private TW1.0 PET07 real RD pixel report, HTML and 130-image sheet; original full-file SHA checks matched. The WORLD05 36 distinct quest script instance→template→SPR numeric candidates all have existing original TW1 decoded source pixels; **36 actual private PNG bytes independently verified against previously original-RD-decoded PNG hashes**, and a new private 36-card observation was visually reviewed (SHA256 `411665dc6a2a9aa1bf46fc60ff864f3e518b15ab3bb41a7be5a492684b5aa396`, 329045B). 33 groups use validated action0, 3 use action2; preserve 100401 undecodable action0 bitmap82729 and 100329/100330 old preview PNG vs later candidate PNG SHA differences without fabricating frames. **TW1 original image evidence is separate from later mixed25 same-number quest and does not prove original same-build pet grants.** No original commercial images published to Git, new original REAL/RD decoding this turn=0. Stage A7 PARTIAL+2 OPEN; B/wiki GATED, R79 paused, overall percent unknown. **Highest NEXT WORLD07**: rotate to another verified historical gameplay/content gap; no MMO account/server or new game optimization.


## 2026-11-04 — WORLD07: original GETPET argument semantics from pinned later C source (bounded cross-carrier evidence)

[WORLD07 fixed-community-code static handler audit](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-07-GETPET-SOURCE-SEMANTICS-20261104.md): direct-read `pimpcapital/longzoro-sa@57b14e2bb373ba851c14db28a239273e4a8831bb` C originals (exact Git blobs pinned) show that this **later community implementation** handles GetPet values as **ENEMY_ID instance identifiers**, resolves instance→ENEMY_TEMPNO→template before `ENEMY_createPetFromEnemyIndex`, checks carried pet slots, and distinguishes two event modes. This supplies independent static *implementation* support for previously source-bound WORLD05 foreign-key joins, and guards 27 private-origin archived script files/29 GetPet lines/44 number occurrences/36 different IDs, 4 multi-number directives (including repeated 482), 2 backup paths, 26 wrong same-number template collisions and 3 saved template PETFLG conflicts. **Not proven** same build/executable as the preserved mixed25 archive, not original JSS1999/TW1.0/CN1.82 behavior or executed grants; potential comma-list index reuse remains a code-review caution. No commercial client/server assets or complete third-party source published to Git. Stage A 7 PARTIAL+2 OPEN, B/wiki GATED, R79 paused, percent unknown; big historical CURRENT blob unchanged. **Highest NEXT WORLD08:** move to another real-source-bearing behavior/content family instead of more GETPET tables, old MMO services or Stage B redesign.


## 2026-11-04 — WORLD08: NPCEnemy map body and battle enemy are distinct source namespaces

[WORLD08 original-source-qualified NPCEnemy appearance and win-branch audit](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-08-NPCENEMY-APPEARANCE-OUTCOME-20261104.md) replays all 279 preserved community mixed25 NPCEnemy CREATE refs from the original SHA-qualified CHAR09 catalog against a separately pinned later C handler (Git blob `45c95d9df8b1e3e9d41443ca12f6ac8f4c105fc4`). 200 `gym>0` refs (levels 1–100, each twice) are **potentially rendered as a random one of 48 symbolic gym map NPC bodies**, rather than their 117 combat enemy SPR candidates; 79 refs lack gym. `dieact=1/0` splits 250/29; 10 `onebattle=1`, 2 `NEWNPCENEMY` exceptions preserved. These are source-limited rules and original static numerics, not proof of a compiled same-deployment binary, original game runtime, authenticated official TW1/JSS1999/CN1.82, or new original graphics. Exact source and full test/replay receipt: [WORLD08 numeric summary](research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-08-NPCENEMY-APPEARANCE-OUTCOME-R1.json). No copyrighted original code or imagery published; full giant CURRENT Git blob remains unchanged. Stage A 7 PARTIAL + 2 OPEN, B/wiki GATED, R79 paused, overall percent unknown. **Highest NEXT WORLD09:** move to another original-source-bearing item/quest/mechanics family, not GETPET/NPCEnemy recursion or MMO infrastructure.


## 2026-11-04 — WORLD09: original GetRandItem candidate slots and source-limited later C selection

[WORLD09 original script slot source and fixed C handler review](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-09-ORIGINAL-RANDOM-ITEM-20261104.md) crosschecks the previously actual-extracted community mixed25 QUEST01 source catalog: 50 static `GetRandItem` control blocks from 33 distinct script paths, 718 preserved ordered candidate positions, 328 distinct item numeric IDs (all present as numeric entries in both archived candidate itemsets). 46 ACCEPT/4 MESSAGE blocks; all script origins remain UNRESOLVED. Independently fixed later `pimpcapital/longzoro-sa@57b14e2bb373ba851c14db28a239273e4a8831bb` C handler selects a 1-based source slot using `rand()%n` with zero remapped to n, creates a candidate item and attempts inventory insertion; this is **not proof of same original mixed25 deployment, original real-world probabilities or any executed reward**. No copyrighted original scripts/assets published; full CURRENT Git blob unchanged. [Full source-bound candidate slot catalog](research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-09-GETRANDITEM-SOURCE-SLOTS-R1.json); next **WORLD10** rotates to an actually new original content source, without expanding C helper research, MMO infrastructure or new game development.


## 2026-11-05 — WORLD10: original DAT and NPC anchors for three villages

[WORLD10 source observation and continuation](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-10-THREE-VILLAGE-MAPS-20261105.md) re-reads maps 2000, 3000, 4000, the three original image files, and the 47 NPC/signboard source entries from one preserved community mixed25 archive. Three private windows use 17,515 source RD placements, with 13 missing or ambiguous references kept explicit. All 47 source coordinates have raw DAT plane-2 value 49152 (zero-based plane index). The source holds no new claim of original dialogue execution, original draw order, or official historical deployment. The public [numeric and hash receipt](research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-10-THREE-VILLAGE-MAP-OBSERVATION-R1.json) preserves the joins. **Next WORLD11** qualifies original NPC and signboard appearances at these map anchors.


## 2026-11-05 — WORLD11: original static appearances at the three village anchors

[WORLD11](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-11-NPC-STATIC-APPEARANCE-20261105.md) independently decodes 29 preserved mixed25 RD images and joins all 47 NPC/signboard CREATE placements to the original numeric aliases and signed ADRN offsets. The private overlay preserves the WORLD10 map pixels, anchor links and original dialogue. The verified TW1 byte prefix excludes the two placements' shared sign alias 10400. [Public source receipt](research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-11-NPC-STATIC-APPEARANCE-R1.json). **Next WORLD12** compares the original village door and warp records to DAT event cells.


## 2026-11-05 — WORLD12: original three-village door and warp coordinates

[WORLD12](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-12-THREE-VILLAGE-WARPS-20261105.md) matches all 73 original classic Warp CREATE points to the corresponding three villages' DAT event-cell sets. It reads all 35 destination DATs, preserves the six M/A records and distinguishes 49 exact reciprocal placements from 2 different returns and 22 arrivals with no same-cell point CREATE. [Public source receipt](research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-12-THREE-VILLAGE-WARP-SOURCE-R1.json). These are static archived records. **Next WORLD13** rotates to another material-backed item or quest observation.


## 2026-11-05 — WORLD13: same-source two-script item chain, cross-carrier icon candidates

[WORLD13 source-limited quest→item chain](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-13-TWO-SCRIPT-ITEM-CHAIN-20261105.md) derives a nine-branch input exchange (6 distinct item IDs) producing three intermediate IDs, then three condition branches consuming those exact intermediates and listing seven later item IDs. Two source scripts and four original CREATE references point to floor IDs 2000/4000 but lack recoverable numeric center positions. All 16 distinct original item IDs have unchanged rows in both preserved candidate itemsets and 13 qualified TW1 RD image aliases **previously** decoded across carriers, not re-observed this turn. No same-official-build, NPC coordinates, actual inventory execution, event/base type or original game runtime is inferred. [Public source/row hashes and every branch](research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-13-TWO-SCRIPT-ITEM-CHAIN-R1.json); historical CURRENT remains untouched. Stage A 7 PARTIAL + 2 OPEN, Stage B/wiki GATED, R79 paused, overall percent unknown. **Next WORLD14:** another material-backed game content gap, without MMO infrastructure or Stage B redesign.


## 2026-11-05 — WORLD14: original fishing-rod crafting and reward text in private offline observation

[WORLD14 source-qualified original text and 13 candidate icons](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-14-FISHING-QUEST-ORIGINAL-TEXT-ICON-20261105.md): reread SHA/CRC-verified saved QUEST01 original-text and ITEM01 original-item/RD-candidate archives. Nine original daytime rod-making branches produce three rods, then three fisherman ACCEPT branches consume the rods with **literal original GetItem order** and an original **11872*2** quantity that WORLD13's numeric-only ID catalog did not preserve. A separate MESSAGE condition is distinguished. All 16 item names and 13 previous TW1 original RD alias candidate images are actually visible in a private offline HTML; Chromium replay loaded all 16 without network or JS error. [Public branch/quantity/name/SHA derivation](research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-14-ORIGINAL-FISHING-QUEST-SOURCE-REPLAY-R1.json) includes no complete commercial script or image. Original game/runtime, official same-deployment and quest permanent-vs-event remain unproven. Historical CURRENT unchanged; Stage A 7 PARTIAL + 2 OPEN, B/wiki GATED, R79 paused, percent unknown. **Next WORLD15:** rotate to a different actual source-backed game content gap; no MMO infrastructure or new-game engineering.


## 2026-11-05 — WORLD15：三村野外出口与加加伐木原表

[WORLD15](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-15-VILLAGE-EXIT-ENCOUNTERS-20261105.md) 从保存的社区混合 2.5 原档实取七件配置，核对地图 100/200 的 22 个出口落点与 6 个覆盖遇敌区。加加 10 个点均覆盖 87/88 两区。87 引用的组 799 在两份组表均缺失。88 的组 414 串起採伐許可證 2478、敌方变体 563／模板「木」531 及掉落槽「良質的木材」2468。权重、重叠区选择与实际发放仍待原运行验证。[公开源收据](research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-15-VILLAGE-EXIT-ENCOUNTER-SOURCE-R1.json)。**Next WORLD16** 查同一载体是否保存木材回交和许可回收的确切原字段。


## 2026-11-05 — WORLD16：加加赛尚的原伐木回交

[WORLD16](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-16-JAJA-LOGGING-RETURN-20261105.md) 从同包原 CREATE、模板和完整脚本确认赛尚在加加 3000／(114,69)。17 条原记录覆盖推荐书换证、无证提示、有证无木及 14 档木材回交。14 份写 20,000 石币和「杉的手環」，12 份删除字段省去推荐书，原运行与官方版别待证。[逐段派生收据](research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-16-JAJA-LOGGING-RETURN-SOURCE-R1.json)。**Next WORLD17** 轮换到可核实的同源场景音频。


## 2026-11-05 — WORLD17：地图原格与实际选曲路径

[WORLD17](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-17-MAP-BGM-20261105.md) 从混合 2.5 保存版与认证台湾 1.0 的编译客户端实证格值 40–46 对应七首曲目。重读保存版 995 张结构有效 DAT，共 438 个楼层、3,236 个第二层标记。四村均见 `sabgm_t0.wav` 对应标记；野外 100 有 `f0`，200 有 `f1` 及一处 `t0`。台湾 1.0 WAV 逐件核实，保存版独立曲目载荷、台湾 1.0 官方地图归属及原生播放仍待证。[派生证据](research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-17-MAP-BGM-SOURCE-R1.json)。**Next WORLD18** 核对认证早期客户端的战斗配乐分支。


## 2026-11-05 — WORLD18：战斗入口的 b0／b1 原分支

[WORLD18](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-18-BATTLE-ENTRY-BGM-20261105.md) 从认证台湾 1.0 和社区混合保存版的编译客户端核实：已核战斗入口的 EN 结果 1 选 b0、2 选 b1。该保存包服务端还实证对怪与对玩家的成功路径分别发送 1 和 2，DU 与 ITEM_BattlePK 可进后者。台湾 1.0 官方服务端、其他特殊战与实际播放仍待证。[派生收据](research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-18-BATTLE-ENTRY-BGM-SOURCE-R1.json)。**Next WORLD19** 转向有原件的物品使用关系。


### 2026-11-05｜Stage A WORLD19：原物品使用函数表与 WORLD18 跨模块连接（最新连续节点）

从本轮重新核验的 `main` `20f45be175e91209829b5e392c70fb6525b082c9` 起，按 WORLD18 的 NEXT 完成**WORLD19 原物品使用关系**。从私人保存混合 2.5 原 RAR 重读 `itemset.txt` 和 `itemset0710.txt`，逐条与原 ITEM01 归档核实 13,254 / 13,915 条原 94 字段：后表物品使用函数原字段 59 种、1082 条，前表 52 种、958 条；原 `useaction` 数值与处理函数名严格分离。`ITEM_useRecovery`、`ITEM_useWarp`、`ITEM_useCaptureUp`、`ITEM_useLearnRideCode` 已建立有原行 SHA 的来源索引；原物品 ID 20811、20898 静态指向 `ITEM_BattlePK`，可与 WORLD18 保存版 `BATTLE_CreateVsPlayer` → EN 类型 2 → 客户端槽 6 `sabgm_b1.wav` 的已核编译入口形成来源关联。未证实原物品实际使用／原游戏实际战斗运行。

本次原 EXE 用当前解包器在 1,835,008 字节发生 CRC 错误，不能声称重验完整程序；此前 WORLD18 **独立成功**取得完整 exe 的 SHA 保留。本次既无版权原文件上传公开仓库，也未覆写历史巨大 CURRENT blob `c89e0e33537990aa2132b47c40fef49a985a935c`。具体证据、59 种 handler 完整派生计数与反例、限定条件见 [WORLD19 增量记录](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-19-ITEM-USE-HANDLERS-20261105.md) 及 [WORLD19 派生收据](research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-19-ITEM-USE-HANDLERS-R1.json)。公开验收：`tests/test_stoneage_stage_a_world19_item_use.py`。**最高 NEXT WORLD20**：按 Stage A 离线内容复原优先级转移到下一个有原实物证据增量的宠物／任务／地图缺口，不做帐号网游或新游戏体验优化。Stage A 7 PARTIAL + 2 OPEN；Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING；整体百分比未知。


## 2026-11-05｜WORLD20：660个原遇敌区的完整来源链与私人原图候选（最新连续节点）

本轮重新核远端 main `89ba427e6d16273ab970aab0e4577052b2e2328c` / tree `ad72395438eb1ff06c2fd7357989fcf429d864eb` 及 WORLD19 11 项成功 Actions，按高优先 WORLD20 批量复原实际游戏内容。完整重读同一已保管社区混合2.5原 RAR 361255180B/SHA `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5` 及六份原数据全 SHA：`encount` 660行/421楼层/1965组槽 → 719不同组ID（688在当前指定`group1`有记录、31缺号共39次引用）→ 719不同敌人实例 → 208个不同宠物/人物/敌人模板 → 157不同图号；12个倒序原矩形、21个空组非空权重槽不修补。复用已有台湾1.0 PET07 **先前真实解码**的原RD候选，107图号跨样本同数字，其中104缩略图原PNG摘要吻合；不推官方物种/同服/原生遇敌成功或历史概率。

可实际查询的私人离线来源网页已保存个人 Library `/石器时代/StoneAge-WORLD20-private-encounter-habitat-atlas.zip` 并再次取回验证整ZIP SHA/成员CRC/HTML SHA；Chromium实际检验楼层与区域切换、缺组提示、跨版原图候选加载，0 JS 错误/0外网。公开Git仅保留[WORLD20批量完整数值/SHA来源索引](research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-20-ENCOUNTER-HABITAT-SOURCE-R1.json)、[WORLD20工作记录](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-20-ENCOUNTER-HABITAT-20261105.md)、回归测试与CI，不上传原音图/原表全文或原程序。历史巨型 `docs/CURRENT-STATE.md` 原Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 不变。此处 208 不是官方宠物种数；台湾1.0与混合2.5不是同部署已证；无原生服务端执行。

**最高 NEXT WORLD21**：轮换到另外一项有真实原实物增量的任务／宠物获得关系，先查已完成 WORLD05–16 的源覆盖，避免重复，本阶段仍只做历史复原。Stage A 7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING；整体完成百分比仍未知。


## 2026-11-05｜WORLD21：29条原任务领宠分支、36个实例与野外配置交集（最新连续节点）

本轮从实时 `main` `b7fe68faa7175a58f1a1693e3d4c4a0bca4f7282` / tree `e34fe62a0d07da94e52d1538f28f325a14ebcd71` 及 WORLD20 主线 11/11 成功 Actions 启动。重读保存版私人原 NPC ZIP 995176B / SHA `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`，2205 成员/1930332 原字节/全 CRC 复验；27份原脚本有29条 `GetPet`，涉及36不同原实例ID。新恢复29个源事件块的原 `EVENT` 条件、25 `ACCEPT` / 4 `MESSAGE`、22 `DelItem`、7 `GetItem`、4 `GetRandItem`、24 `EndSetFlg`；保留2份命名备份与奖励重复数字。重新验原 `enemy.txt` / `enemybase.txt` 完整SHA，36实例经真实外键均联到模板/图号，不能直把实例号当模板号。与 WORLD20 当前 `encount→group1→enemy` 719个野外引用实例的交集为**0**，仅限本保存包当前静态配置，**不是**历史绝对无法野外抓获的证据。

新跨任务见证：`poru/team03` 原条件 `NOWEV=64&NOWEV=57&PET=33-721&ITEM=2432`、`GetPet=333`、`GetItem=18559`、`DelItem=2432`；其中2432与 WORLD13/14 原钓竿制作产物同一保存包 ID，可做静态来源关联，不能推任务真实执行。私人原繁体脚本文字和离线检索页已在个人 Library `/石器时代/StoneAge-WORLD21-private-getpet-quest-branches.zip` 保存并重新下载核ZIP全SHA/三成员CRC，Chromium实际29张卡片检索与展开，0JS错误/0外网。公开仅保存[WORLD21原源派生索引](research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-21-GETPET-QUEST-BRANCHES-R1.json)、[证据记录](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-21-GETPET-QUEST-BRANCHES-20261105.md)、测试和Actions；原版权文本/图像不进Git，实际原服任务和官方同部署未认证。旧历史 CURRENT Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` **不变**。

**最高NEXT WORLD22**：转向另一个有原实物增量的 NPC／任务／物品内容缺口，不重复为这36个实例扩概率、账号/网服、新引擎或体验优化。Stage A 7 PARTIAL + 2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，整体完成率未知。


## 2026-11-05｜WORLD22：原任务石币奖励、扣费和124个道具来源（最新连续节点）

[WORLD22来源与界限](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-22-QUEST-CURRENCY-20261105.md)完整重验私人CHAR01的2205原文件，提取26份脚本的115条原石币指令：99 GetStone奖励、16 DelStone扣费；108 ACCEPT / 7 REQUEST。99条奖励沿用QUEST01旧发现，本轮补足16条扣费、原条件/金额/道具/源行SHA。8条`LV*3`/`LV*20`/`LV*40`等级表达式不求值；两份osaisen原脚本无确切CREATE引用，不能当实际部署。关联124道具ID均可查ITEM01联合目录，2391只在另一候选表存在；123个原名经本轮完整SHA合格的itemset.txt原行再核。私人原文阅读ZIP已保存，本地静态HTML结构检查通过，浏览器/原游戏未执行。[公开派生索引](research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-22-QUEST-CURRENCY-SOURCE-R1.json)只含来源数值/条件/哈希；26项相关本地测试通过。历史CURRENT blob `c89e0e33537990aa2132b47c40fef49a985a935c`不变。

**最高NEXT WORLD23：** 在任务/物品内容模块寻找确有原实物增量的任务道具取得/消耗或奖励数量，并与WORLD09/13/14/16/21/22查重；本批货币条件不扩执行器或经济模拟。保持Stage A 7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，整体完成率未知。


## 2026-11-05｜WORLD23：原NPC物品字段全批与WORLD09位置订正（最新连续节点）

[WORLD23来源、加法订正与止点](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-23-NPC-ITEM-TRANSFERS-20261105.md)从2205件完整SHA/CRC合格原NPC文件整理410份脚本的1246条物品字段：GetItem532、DelItem659、GetRandItem55。确切模板用途分开保留任务、传送、存点、答题、比赛及无CREATE引用；数量、原序、重复、6个EVDEL、10空组件和1个1991*缺失数量不猜补。879个道具整数与两份候选物品表联接，2744/2745均缺，11个仅B表存在；866个A表原名逐原行核实。私人410份原文阅读包已保存，HTML只作结构检查，原游戏/浏览器未执行。

**明确订正旧WORLD09解释：** 同一50条列表、相同源SHA实际有959个数字位置+1空位置，26条含重复，另26条首次出现次序与旧投影不同。旧“718原始候选位置/组内无重复”来自去重后的ID投影，不能继续当原文位置证据；718个分块去重引用与328个不同ID仍是旧投影事实。原WORLD09/QUEST01 JSON和旧验收保留；[全批派生及逐列表订正](research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-23-NPC-ITEM-TRANSFERS-R1.json)提供真实原行SHA、顺序和重复，不推实际概率。最终本地29/29通过；复用既有WORLD09工作流验收。历史CURRENT原blob `c89e0e33537990aa2132b47c40fef49a985a935c`不改。

**最高NEXT WORLD24：** 有限核实一类非ExChangeMan物品字段的具体用途（优先SavePoint或Quiz），优先既有合格编译原件，后期源码须明确分版；取得一种有据语义或精确缺源即止，不扩通用执行器、网服、新引擎或体验优化。Stage A 7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，整体完成率未知。


## 2026-11-05｜WORLD24：原编译存点物品条件与127字节读取边界（最新连续节点）

[WORLD24原编译证据与界限](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-24-SAVEPOINT-ITEM-ROLE-20261105.md)完整重读同保存包GMSV原EXE并按WORLD18/SCENE33全SHA核同，核明SavePoint的GetItem用于检查及确认后消耗物品，不能当奖励。原对话传检查模式0，确认回复传消费模式1，明确到CHAR_DelItem的静态调用；没有运行原存点或原服务器。同包22份原参数中21份有GetItem，7份超过此编译读取器的127有效ASCII字节限制，完整原文209个逗号位置的复制投影为161个位置并含截断片段；161不是有效条件数。保留原文、缺失字段和1991*，不修补历史配置。

[公开派生数值/代码窗SHA/22来源](research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-24-SAVEPOINT-ITEM-ROLE-R1.json)经独立nm10符号、objdump14调用核同；39/39本地检查通过。私人22份原文/长度对照包已保存，仅HTML结构核验，无浏览器/原游戏运行。全部历史CURRENT blob `c89e0e33537990aa2132b47c40fef49a985a935c`及WORLD23的旧投影订正继续保留。

**最高NEXT WORLD25：** 有限核原Quiz物品字段用途及4条GetItem来源，优先同保存版完整编译程序；不把SavePoint的消耗语义套入Quiz，不扩通用执行器、网服、新引擎或体验优化。Stage A 7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING，整体完成率未知。


## 2026-11-05｜WORLD25：原答题GetItem的门槛、奖励及入场物品（最新连续节点）

[WORLD25原编译证据与用途区别](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-25-QUIZ-ITEM-ROLE-20261105.md)核明同保存版Quiz GetItem按原序读“门槛,奖励载荷”对，载荷内部候选用点号分隔，并存在创建物品/加入背包/失败清理的编译路径。四份原参数中1和100是比较门槛，奖励候选分别为2754（三份）和2759（一份）；入场2752/2753另由EntryItem描述，不能套用SavePoint消耗语义。未运行答题、得分、发奖、扣物或原客户端，未认证初代官方同部署。

[公开逐行用途限定](research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-25-QUIZ-ITEM-ROLE-R1.json)保留四份源SHA、16条原编译调用和10个符号；独立nm/objdump核同，49/49本地测试通过。WORLD23原始数字投影完整保留，其中门槛不能按数字碰撞算物品；旧879不能当已核全游戏物品数，也不无据重算为878。WORLD24重放报告逐字节不变；私人四份原参数/门槛奖励阅读包已保存，仅结构检查，无浏览器运行。原CURRENT blob `c89e0e33537990aa2132b47c40fef49a985a935c`不改。

**最高NEXT WORLD26：** 有限核剩余Raceman来源GetItem用途，优先同编译样本和确切参数；取得一类有据语义或精确缺源后离开物品字段辅助链，回已有模块内容队列。不扩整答题/竞速引擎、网服、新引擎或体验优化。Stage A 7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING，整体完成率未知。


## 2026-11-05｜WORLD26：Raceman编译匹配缺源止点，回任务模块内容（最新连续节点）

[WORLD26猎宠活动参数与编译表边界](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-26-RACEMAN-SOURCE-BOUNDARY-20261105.md)核对同保存版原EXE完整60项功能名称查找域：没有Raceman，另有PetRaceMaster/PetRacePet不能替代。唯一race2/second.arg的GetItem:20760用途保持OPEN；不是实际加载失败/所有版本缺实现。20760在原候选A表缺、B表有，旧O88/QUEST04结论和WORLD23原始目录保留；本轮无新活动发现、无原游戏执行。

[公开来源限定报告](research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-26-RACEMAN-SOURCE-BOUNDARY-R1.json)记录60项标识/哈希、三份原参数创建模板源SHA及名称查找边界；独立节读取器/nm/objdump核同，56/56本地测试通过。全2,205原NPC文件逐SHA/大小/CRC核同；原程序/对白不公开，旧CURRENT blob c89e0e33537990aa2132b47c40fef49a985a935c不改。

**最高NEXT WORLD27：** 回任务模块，批量整理现有17份原脚本中97条DelPet所属完整原条件与奖励分支，先查重已有任务成果，区分常驻/运营活动/起源未明；不将字段数当任务数、不猜物种命名空间或原生删除行为。离开编译物品字段辅助链，不扩竞速引擎/账号网服/新引擎或体验优化。Stage A 7 PARTIAL+2 OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING，整体完成率未知。


## 2026-11-05｜WORLD27：原交宠任务条件与奖励整批内容（最新连续节点）

[WORLD27交宠任务来源与原文交付](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-27-PET-HANDOVER-QUESTS-20261105.md)整理17份原脚本、97条DelPet所属完整原条件/奖励分支、15次确切创建引用；不是97个已认证任务或15个独立NPC。55条旧QUEST01摘要保留，另外42条来自三份没有直接CREATE路径引用的实存原文件，不推可达/不可达。原147词元位置含140选择器字面和7个未展开EVDEL；保留缺显式数量、条件拼接异常及重复奖励，不猜全体物种命名空间或原生事务。

[公开逐源目录](research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-27-PET-HANDOVER-QUEST-BRANCHES-R1.json)联回90项物品行与4个已有WORLD21奖励实例证据；全批起源ORIGIN_UNRESOLVED，严格不混入已认证本体/永久/运营活动档。私人17原文/97分支/90道具名阅读包已保存，独立源范围与HTML原文本核同，无浏览器/原游戏运行。77/77本地测试通过；WORLD22完整源报告重放逐字节不变，CURRENT历史blob保持。

**最高NEXT WORLD28：** 任务模块统一内容入口：复用已有钓竿、领宠、交宠、委托及运营活动资料，按来源/归属四档集中原文与物品/宠物/地图关联、明确缺环。不扩DelPet/EVDEL编译辅助链、通用框架、网服、新引擎或体验优化。Stage A 7 PARTIAL+2 OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING，整体完成率未知。


## 2026-11-05 — WORLD28：原版任务统一私人原文入口

[WORLD28 已保存原脚本的统一入口与证据界限](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-28-UNIFIED-QUEST-HUB-20261105.md) 由已验7份私人任务原文阅读器原字节拼成一份离线可查目录：原脚本、条件传送、钓竿制作交付、领宠、石币、物品转移、交宠；另独立列五项有日期/主题证据的运营活动。12档原资料按本体／永久／运营／起源未明四档明确隔离，社区混合2.5原源仍属起源未明，未证初代官方同部署。复用 WORLD14 的道具2432 与 WORLD21 静态条件/领宠333关联，保留 WORLD27 selector 与 GetPet 实例不同命名空间。原文和原图私人保存，Git只放[数字/SHA来源表](research/recovered/STONEAGE-STAGE-A-WORLD28-UNIFIED-QUEST-HUB-R1.json)、测试和连续性记录；Chromium 用同一HTML字节完成12卡/7原阅读页无外网检查，但没有原生游戏运行，无法测试本环境 file:// 导航。历史CURRENT原blob不变。**下一步：** 从当前已得资料中选择下一项真正可补原游戏行为的机制模块内容，证据不足才按原版别记录缺环；不扩任务执行器、账号服务器、新作或体验优化。Stage A 7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79暂停、整体进度未知。


## 2026-11-05 — WORLD29：原宠物店收费、卖宠与骑乘限制的分版源码恢复

从私人社区mixed25原NPC子树实际重读16个由CREATE直接引用的宠物商店原参数，再以独立的后期社区C源码固定提交审查售价与寄放规则，**不是已证明同部署或台湾1.0／大陆1.82原生运行**。C参考分支读取 `nomal_rate`／`special_rate` 乘1000，缺省1000／1200；`pool_flg==1`门控寄放；源码中`pool_cost`读取已注释，寄放走 `50 + 4×人物等级` 动态字面，而16份原配置却有5项200、一项2000，**矛盾保留，绝不宣称实际交易费率**。原代码还区分卖宠、店内寄放与可选宠物仓库，并拒售正在骑乘的宠物；静态释放后成本再计算的潜在问题列OPEN。完整来源/默认值/负例见 [WORLD29增量记录](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-29-PETSHOP-CROSSSOURCE-20261105.md) 和 [公开原源SHA及程序分支索引](research/recovered/STONEAGE-STAGE-A-WORLD29-PETSHOP-STATIC-CODE-BOUNDARY-R1.json)。不再展开原旧网游基础设施、引擎或体验优化；Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总进度未知。

## 2026-11-06 — WORLD30：同包复原宠物料理的材料匹配和成品候选

保存版混合 2.5 的编译程序、启动配置、宠技表和材料表共同确认，宠物加工 200／料理 201 进入同一回调，普通路径至少接受两件有效材料，首项类型 20 切入料理搜索。三道原主厨菜单已接到 36 条单原子输入候选行，原料值和程序调整后匹配区间分别记录。详见 [WORLD30 连续性记录](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-30-COOKING-SOURCE-20261106.md) 与 [派生收据](research/recovered/STONEAGE-STAGE-A-WORLD30-COOKING-SOURCE-R1.json)。样本为静态证据，尚无实服制作或早期官方版本认证。下一优先 WORLD31 为同包回复道具的实际回调与参数关系。

## 2026-11-06 — WORLD31：场外与战斗回复参数分流

同一混合 2.5 保存包的配置选中表有 644 行指向回复回调。对 583 行覆盖的 116 种普通参数回放原始 x86 回调后，确认场外对玩家可同时处理体力、气力，战斗回调遇两者并存时优先只传体力。物品场景／目标原字段、回调发出的扣物请求及最终战斗结算分别记录。详见 [WORLD31 证据和连续性](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-31-RECOVERY-SOURCE-20261106.md) 与 [派生收据](research/recovered/STONEAGE-STAGE-A-WORLD31-RECOVERY-SOURCE-R1.json)。下一优先 WORLD32 为同包战斗单目标结算。


## 2026-11-06 — WORLD31 另存物品表差异实源核验（WORLD32 仍未完成）

[来源限定记录](docs/continuity/STONEAGE-WORLD31-ITEMSET-VARIANT-20261106.md)、[公开19条原行哈希/数值证据](research/recovered/STONEAGE-STAGE-A-WORLD31-ITEMSET-VARIANT-R1.json)：复用此前已认证的私人 ITEM01 原表派生目录，完整 ZIP／成员 SHA 核同，按各版本每 ID 94 原字段逐列对照。配置选中 `itemset.txt` 的 644 条回复道具回调与 WORLD31 相符，另存 `itemset0710.txt` 为 663 条；共有 644 条逐字段完全相同，另存表独有 19 条，其中严格普通体力 6、气力 2、其它 11。19 条与已有七份 ITEM01 公开分片原行哈希均匹配，不能当成额外 19 件已部署可用恢复道具，也不能推已改平衡。新的私有原件下载 0、原程序执行 0。公开源限制脚本、测试和 CI 仅在具备原私有 ZIP 时才能重算完整派生；公共 CI 不运行原字节。

**最高 NEXT WORLD32 保持不变：** `BATTLE_MultiRecovery` 同包单目标体力／气力结算，需完整、SHA 合格原 `gmsv.exe` 才能继续真实 x86 核查目标过滤、写入及上限。当前环境缺此原件，不能将 WORLD31 首次属性写入预检算结算完成；缺源已精确归档。不扩账号/网服、新引擎或体验优化。Stage A 7 PARTIAL + 2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING、整体完成率未知；历史 CURRENT 原 blob `c89e0e33537990aa2132b47c40fef49a985a935c` 不变。

## 2026-11-06 — WORLD32：战斗单目标回复的目标过滤、写入与上限

重新取回并核同混合 2.5 原保存档及其中完整 `gmsv.exe`，对 WORLD31 的 116 种普通参数恢复完整回调入参，回放其 79 组结算请求的两端随机值。原战斗指令证实有效目标保留、失效目标同侧重选，以及普通体力／气力分别封顶。临近上限时，原战斗缓冲仍保留截断前增量。同侧没有候选时，原函数返回 `-1` 而列表未填充，调用方下游留待证。详见 [WORLD32 连续性记录](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-32-BATTLE-RECOVERY-SOURCE-20261106.md) 和 [派生收据](research/recovered/STONEAGE-STAGE-A-WORLD32-BATTLE-RECOVERY-SOURCE-R1.json)。原档和原程序保持私有。回放范围为混合保存样本的隔离原指令，无实服回合或扣物证据。

**最高 NEXT WORLD33**。核同保存版战斗物品命令对原表场景／目标字段的判定，复用已核回复物品，对照有限的允许／拒绝情形。Stage A 7 PARTIAL + 2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，整体完成率未知。

## 2026-11-06 — WORLD33：回复物品的客户端场景限制与战斗命令登记

同包原客户端分别在战斗物品栏拒绝 `fieldtype=2`、在场外使用拒绝 `fieldtype=1`。原物品 12555 在客户端战斗栏被挡住，同包 GMSV 战斗入口却仍登记直接送入的普通槽位物品命令。受测服务端入口只读取物品目标字段，群体选择另受目标类型和施用者侧别限制。详见 [WORLD33 连续性记录](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-33-BATTLE-ITEM-GATE-SOURCE-20261106.md) 和 [派生收据](research/recovered/STONEAGE-STAGE-A-WORLD33-BATTLE-ITEM-GATE-SOURCE-R1.json)。证据范围为社区混合保存样本的客户端选择和服务端登记，无实战、联机或扣物验证。

**最高 NEXT WORLD34**。核同保存版场外物品命令的场景字段与普通目标路径。Stage A 7 PARTIAL + 2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，整体完成率未知。


## 2026-11-06 — WORLD34-R2 decoded PE code/data section boundary (original static source)

Rechecked the preserved mixed25 RAR and verified the 23 previously pinned original source windows. The current libarchive GMSV decode fails the full EXE CRC in the COFF symbol table, after the end of all four file-backed PE sections; it does **not** certify the full original executable or prove end-to-end field item outcomes. The bounded original item callback/HP write/delete call sites are now recorded in [WORLD34-R2 static source note](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-34-R2-MAPPED-PE-SOURCE-20261106.md) and [derived source receipt](research/recovered/STONEAGE-STAGE-A-WORLD34-R2-MAPPED-PE-SOURCE-R1.json). **Highest NEXT WORLD34-R3**: original-source-qualified field intake through callback return; do not infer item scene bypass or inventory consumption from static call sites. Historical CURRENT blob unchanged.

## 2026-11-06 — WORLD34-R3：场外回复回调完成与背包消耗

用完整 SHA 和 CRC 合格的混合 2.5 原服务端程序，从场外命令回放到回复回调返回。三件代表道具在有效本人、宠物、队伍目标上均完成相应属性写入与夹具背包消耗。场景 1 的 1232 被原客户端场外检查拦下，同包服务端入口直接接收夹具参数时仍写体力并清槽。空宠物、空队伍与越界目标走到未检查的角色索引 `-1` 读取，隔离回放在边界停止。详见 [WORLD34-R3 连续性记录](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-34-R3-FIELD-ITEM-REPLAY-20261106.md) 和 [45 条派生轨迹](research/recovered/STONEAGE-STAGE-A-WORLD34-R3-FIELD-ITEM-REPLAY-R1.json)。最高优先 WORLD35 为捕捉增益道具与原捕捉判定的同包关系。

## 2026-11-06 — WORLD35：捕捉增益道具与捕捉分数

同包两张物品表的 26 条捕捉增益原行逐字节相同。原指令回放确认道具对接收者累加工作键 32，捕捉判定读取捕捉者本人的该键，完成比较后清零。分数封顶 99，受测整数随机值 98 通过、99 拒绝。另按编译加载器订正 WORLD34-R3 的动作物理列和三个原值，重跑 18 组后属性写入与扣物结果一致。详见 [WORLD35 连续性记录](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-35-CAPTURE-ITEM-SOURCE-20261106.md) 和 [派生收据](research/recovered/STONEAGE-STAGE-A-WORLD35-CAPTURE-ITEM-SOURCE-R1.json)。最高优先 WORLD36 为捕捉判定之后的宠物入栏与归属。

## 2026-11-06 — WORLD36：捕捉结果写入宠物携带栏

隔离回放同包混合 2.5 原指令，从捕捉分数比较进入真实角色池分配、属性重算、宠物入栏与主人绑定。第一个空携带栏接收新角色索引，主人索引、账号与角色名写入新宠物。满携带栏与宠物角色池耗尽分别在不同阶段失败，原携带栏均保留。详见 [WORLD36 连续性记录](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-36-CAPTURE-ROSTER-SOURCE-20261106.md) 和 [派生收据](research/recovered/STONEAGE-STAGE-A-WORLD36-CAPTURE-ROSTER-SOURCE-R1.json)。最高优先 WORLD37 为入栏后战斗目标退出、计数及条件道具。


## 2026-11-06 — WORLD37-R1：捕捉成功后的原野怪退出与条件道具版本分歧（后代源码证据）

三条固定后代源码的九份原文件相互核对，补足 `BATTLE_Capture → _BATTLE_Exit → CHAR_endCharOneArray → CHAR_endCharData` 的成功尾段：战斗席位清除、野怪角色记录标为未使用、捕捉者计数增加；条件道具普通成功消费和宏控制的预检查消费必须分开。**本轮不是混合2.5原GMSV尾段原生回放，更不是台湾1.0官方服务器规则认证**。详见 [WORLD37-R1连续性记录](docs/continuity/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-37-CAPTURE-EXIT-DESCENDANT-20261106.md)、[九份后代源码Git blob及版本收据](research/recovered/STONEAGE-STAGE-A-WORLD37-CAPTURE-EXIT-DESCENDANT-SOURCE-R1.json)。最高下一项WORLD37-R2：只有真实取得合格混合2.5原GMSV字节才进行其尾段指令回放；不能取得则转回有可读原件的模块内容。历史CURRENT文件原样保留，Stage A 7 PARTIAL + 2 OPEN不变。


## 2026-11-06 — ITEM04｜原TW1四个尾端透明RLE溢出图块可作私人有界像素观察

在WORLD37-R2缺混合2.5原GMSV可执行文件时，转向已保存的原台湾1.0零售ADRN/REAL。完整复读并核对832个旧严格可解RD、831个原索引缺失及四个末尾恰多一个透明像素的旧失败RD；从四个原流各取严格画布上限内的**真实原索引像素**，独立解码相符，私有生成4灰度/4候选配色PNG和一联系页，私有ZIP已存Library并重读SHA/CRC。**原严格RD编码器未放宽，原客户端处理末端多一个像素仍未证，混合2.5物品表7个同号物品身份亦非TW1官方同服认定。** [详细连续性记录](docs/continuity/STONEAGE-ITEM-EQUIPMENT-SHOP-MODULE-04-FOUR-TERMINAL-RLE-PRIVATE-PIXELS-20261106.md)、[哈希与数据边界](research/recovered/STONEAGE-ITEM04-TW10-FOUR-TERMINAL-RLE-SOURCE-CANVAS-PREFIX-R1.json)。WORLD37-R2继续有条件OPEN；其余真实游戏内容按可读取原件排序。历史 CURRENT 原样不改。


## 2026-11-06 — BATTLE181｜原台湾1.0战场第181图的400格来源候选画面（ITEM04联动）

真正从原台湾1.0零售包重读战斗SAB181的400格及同包原ADRN/REAL：65个不同原位图号中64个严格RLE可解，余一图号6729只在此SAB出现一次，使用ITEM04独立验过的40×30原画布范围内1200索引像素，私人生成整张1350×1220现代候选战场图、源异常点标注、原图块放大图，并将805734B/4成员ZIP送入私人Library后独立回读整SHA/CRC。**O16旧217/218严格全可解统计保持不变；不能称原客户端对6729多一个透明像素的处理已认证，或218张已原生正常渲染。** [实际来源记录](docs/continuity/STONEAGE-STAGE-A-BATTLE181-TW10-ORIGINAL-SAB-CANVAS-20261106.md)、[原SHA/守恒与边界](research/recovered/STONEAGE-STAGE-A-BATTLE181-TW10-SAB6729-SOURCE-CANVAS-R1.json)、[公开回归测试](tests/test_stoneage_stage_a_battle181_canvas_source.py)。源图/400格原排列未入公开Git，原CURRENT完整保留，WORLD37-R2继续有条件OPEN。


## 2026-11-06 — WORLD37-R2A：原混合2.5编译捕捉成功尾段静态证据

重新核实已保存的361255180B混合2.5 RAR整SHA，libarchive完整长度输出仍存在CRC及整SHA错误，未将其冒作合格EXE；但四个PE实际装载段SHA与此前独立UnRAR合格原程序的段摘要全部相同。原机器码静态核准：捕宠成功分支内宠物创建后存在条件道具处理、角色整数键44读取/加一/回写、战斗退出入口；退出路径存在清席位及野怪类型2角色释放调用。**仅证明受源限定的代码可达结构，未执行这些尾段、扣物、计数或角色池释放。** 详见[WORLD37-R2A连续性记录](docs/continuity/STONEAGE-STAGE-A-WORLD37-R2A-ORIGINAL-CAPTURE-TAIL-STATIC-20261106.md)、[派生收据](research/recovered/STONEAGE-STAGE-A-WORLD37-R2A-ORIGINAL-COMPILED-CAPTURE-TAIL-STATIC-R1.json)。最高条件性NEXT WORLD37-R2B：完整合格原GMSV和隔离x86回放环境可得时验证原指令实际写入，否则切换可读取原来源模块；Stage A 7PARTIAL+2OPEN，Stage B/wiki GATED，R79暂停，完成率未知；历史CURRENT完整原样保留。


## 2026-11-06 — WORLD37-R2B：同包原编译捕捉条件表与两张物品主表实际联接

在前轮WORLD37-R2A静态尾段基础上，重新直接核存混合2.5原RAR全SHA及原服务端可用四PE段SHA；从 `.data` 0x58CD60 完整逐记录解出128×64字节编译初始条件表：11条非零、117条零、13道具引用/12不同ID；原原型函数直接读取角色整数键53并存在条件物品检查/删除静态调用。重新从同包解得两份原始94列物品表完整SHA/行SHA，配置选中的 `itemset.txt` 有9个相关ID，另存 `itemset0710.txt` 有全部12个；20247/20253/20259三种魔法鑽戒只在另存表。重复2236两个关系和1105对应三ID全保留。此为**编译数据和物品内容实际来源联接**，不称捕捉成功/物品实际扣除或三钻戒已在选中表部署；当前解压的GMSV整CRC/SHA仍不合格，WORLD37动态尾段仍OPEN。详见[WORLD37-R2B记录](docs/continuity/STONEAGE-STAGE-A-WORLD37-R2B-CAPTURE-REQUIRED-ITEM-CROSSWALK-20261106.md)、[公开逐行派生收据](research/recovered/STONEAGE-STAGE-A-WORLD37-R2B-COMPILED-CAPTURE-REQUIRED-ITEMS-R1.json)。全部历史 CURRENT Git blob原样保留，Stage A 7PARTIAL+2OPEN、B/wiki GATED、R79暂停、percent=null。NEXT WORLD37-R2C 仅有合格完整EXE/模拟环境才做原指令动态实测，缺源转原内容模块。


## 2026-11-06 — WORLD37-R2B3：同包原捕捉键到宠物图号与 SPR 索引的静态桥接

从已保存并重新全 SHA 核对的混合 2.5 原 RAR 实际复取两份 `enemybase` 与 `spradrn_5.bin`，三文件 SHA/CRC 与 PET10 旧源记录一致。WORLD37 编译条件中 11 个 key53 的同包原模板数字候选分别联到第 37 列 11 个原图号，5 个在本包唯一 SPR 索引有位置、6 个仅此索引未命中；第 38 列 PETFLG 为 10 条 1／1 条 0，后者不删。5 个索引虽各带原 56 动画数量字段，本包没有同源实际 `spr_5.bin` 帧载荷，新增可视原帧 0。另存 enemybase2 仅 7 个匹配，原配置选择主表。此为新增 **11 条受限静态数字关系**，非原成功捕获、宠物历史身份或原版运行。详见[来源/未解边界](docs/continuity/STONEAGE-STAGE-A-WORLD37-R2B3-CAPTURE-SPR-SOURCE-20261106.md)和[公开逐键收据](research/recovered/STONEAGE-STAGE-A-WORLD37-R2B3-CAPTURE-ORIGINAL-SPR-BRIDGE-R1.json)。旧 CURRENT blob `c89e0e33537990aa2132b47c40fef49a985a935c` 全文原样保留。

**最高条件性 NEXT WORLD37-R2C**：完整合格 GMSV 与离线 x86 夹具齐备才验实际尾段；本环境缺合格完整 EXE，先转可新增原宠物 SPR 帧/其它内容载体。不得由动画索引宣称已有动画原帧，或重复无新源的静态辅助分析。Stage A 7 PARTIAL+2 OPEN，B/wiki GATED，R79 暂停，整体完成率未知。

## 2026-11-06 — PET11｜捕捉条件同号的台湾1.0两组原SPR动作与496幅原位图实物观察

从重新全SHA/379成员CRC合格的台湾1.0私人零售原包，及同包混合2.5实际原SPR索引，直接核实图号100329/100355在两种载体的12B SPRADRN索引记录逐字节相同，**不证明历史同一部署**。台湾1.0原SPR组各56原方向/动作序列，共112条、1120帧位置、496个不同原RD位图；真实整ADRN/REAL逐块解码495严格成功，位图113576原尾端0xC2零像素多输出一格，保留严格失败，仅将前9200原索引像素用于私人受限画布观察。每个原帧图片只存个人私人Library，已独立取回整ZIP SHA/CRC一致；程序实际打开112首帧联系图，但Chromium原页未运行，色盘/倒行/透色与原生动作秒数仍未认证。

[PET11来源与边界](docs/continuity/STONEAGE-PET-MODULE-11-CAPTURE-LINKED-TW10-ORIGINAL-SPR-496-PIXELS-20261106.md)、[公开496摘要链与2组原SHA](research/recovered/STONEAGE-PET-MODULE-11-TW10-CAPTURE-SPR-ORIGINAL-496-PIXEL-SOURCE-R1.json)、[私人原件重放器](tools/stoneage_pet11_tw10_capture_sprite_source.py)。本批新增实际可见的**来源限定原像素观察**而非496个历史新发现宠物；100329原SPR元数据此前O63已知。旧 docs/CURRENT-STATE.md 原完整blob c89e0e33537990aa2132b47c40fef49a985a935c保持不变。

**下一优先：** WORLD37-R2C真实捕捉成功尾段仍需完整合格GMSV及隔离x86，故有条件OPEN；可先从已保存合法载体里核剩余6个同版缺SPR索引图号是否有真实原像素，或转其它具原件的宠物/内容项，不扩旧网服/新引擎或改玩家体验。Stage A 7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、overall percent未知。

## 2026-11-06 — PET12｜六个原捕捉图号各56条台湾8.5 SPR原动画与1568个同包RD索引

从源R28已认证台湾8.5*声称*社区保存样本的全SPR元数据，逐组重编码原机器字并全段SHA对照；与R29同一MSI保存包原ADRN/REAL已验整SHA及每RD块SHA逐图联接。WORLD37-R2B3所余六候选图号101279/101280/101281/101564/101736/101737在该TW85载体原索引均各唯一，原 **336条方向动作／2048帧位置／1568不同原位图号**，各位图已对应当时从同包真实原RD计算的SHA/尺寸；前三图号又与保存CN5整段原SPR字节相同，后三无CN5索引，不猜身份。新交付是**源限定原动画规格＋位图定位**，本轮没有重新读私人TW85原REAL像素，新增视觉原帧0；原名字仅混合25静态配置候选，不认证官方TW85捕宠或同一部署。

[PET12详细证据和止点](docs/continuity/STONEAGE-PET-MODULE-12-SIX-CAPTURE-CANDIDATE-TW85-SPR-RD-20261106.md)、[六原段SHA／RD首帧来源与证据边界](research/recovered/STONEAGE-PET-MODULE-12-TW85-SIX-CAPTURE-SPR-RD-BRIDGE-R1.json)、[自动重放工具](tools/stoneage_pet12_tw85_capture_spr_rd_bridge.py)。旧CURRENT完整blob c89e0e33537990aa2132b47c40fef49a985a935c不改；WORLD37-R2C动态尾段有条件OPEN。剩余真正原像素须合法重获同包 `real_158.bin` 及相关资源后再进入私有观察，不重复扩纯索引工程；先继续可读取其它宠物原件内容。Stage A 7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING、overall_percent=null。

## 2026-11-06 — PET13｜原编译捕捉键→同包原宠物模板数值及原技能定义

在PET12六原动画组规格闭合后，重读和逐整SHA／CRC验证混合2.5私人原 `enemybase.txt`／新抽原 `petskill.txt`，11条原捕捉条件key53候选逐原行SHA匹配本包被配置选择的宠物模板第7字段；恢复11×原INITNUM、LVUP字面、四基础属性、四元素、技能槽及原需求道具，25个正数技能槽引用全部落在同源5个原技能ID及定义行。保留**PETFLG=10条1＋1条0（key53=8）**、13需求道具引用／12不同ID、技能空槽及后代社区样本来源资格。只有**静态同包候选关系**，不认证原GMSV真正读取key53的模板映射、不证明11条可捕、不把此后期社区服数值归于TW1/TW85/CN5官方或当代新游戏配置。

[PET13原源核验与断言边界](docs/continuity/STONEAGE-PET-MODULE-13-ORIGINAL-CAPTURE-TEMPLATE-ATTRIBUTES-SKILLS-20261106.md)、[11模板／五原技能条目派生摘要](research/recovered/STONEAGE-PET-MODULE-13-ORIGINAL-CAPTURE-TEMPLATE-ATTRIBUTES-SKILLS-R1.json)、[原件／公开双路径校验工具](tools/stoneage_pet13_capture_template_stats_skills.py)。原商业全文/原像素不公开，旧CURRENT完整blob c89e0e33537990aa2132b47c40fef49a985a935c不改，Stage A 7PARTIAL+2OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING、overall_percent=null。WORLD37-R2C仅在真正齐备原EXE完整SHA/CRC和隔离x86时重开，PET内容继续以现存合格源的实际原像素与可实证名称归属为优先。


## 2026-11-06 — PET14｜台湾1.0既有原像素与混合2.5两份原宠物主表分源观察

在完整保存的PET07 130个台湾1.0原SPR像素图号组与PET10私人原社区混合2.5双宠物主表中作**数值关系**，主表命中309原行（PETFLG=1有188、0有121），备用表命中258原行（PETFLG=1有142、0有116），没有把混合2.5繁体姓名/属性/技能误标成台湾1.0官方身份。私人原像素目录新增可切换图号的后代原名/数值分源查阅，生成HTML `15,198,113B` / SHA256 `949e1d28a228ecec6435ebdd463ac01804bb054c2578d1de839476e667e3b30f`，私人新页未成功上传Library，当前会话提供文件；本批**新增原像素解码0，新增原商服运行0**。公开仅130逐图号数字/原SHA、工具、回归测试和[完整受限证据](docs/continuity/STONEAGE-PET-MODULE-14-TW10-MIXED25-SOURCE-BOUNDARY-20261106.md)、[PET14公开数值桥](research/recovered/STONEAGE-PET-MODULE-14-TW10-MIXED25-SOURCE-SEPARATED-NUMERIC-BRIDGE-R1.json)，商业原像素和原表全文不入Git。旧完整CURRENT Git blob c89e0e33537990aa2132b47c40fef49a985a935c保持不变。PET模块本批SOURCE_BOUNDED_PARTIAL；下一原像素仅在TW85原REAL字节可重取后进行，条件R2C仍待合格原EXE/x86，当前按模块队列转已有来源可读内容；Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停，完成率未知。


## 2026-11-07 — PET15｜台湾1.0样本的全部原方向和动作

重放 131 个候选图号的全部 7,672 条源动作与方向序列、73,500 帧位置。32,155 个原位图中 32,150 个严格解码，5 个仅展示原画布范围内的源索引。新增可查的图号 100400 在混合 2.5 备表有两条宠物标记，配置主表相同模板均标为 0，保留两源的分歧。私人图册保存实际原像素，公开 Git 保留[来源和状态](docs/continuity/STONEAGE-PET-MODULE-15-TW10-ALL-SELECTED-MOTION-20261107.md)及[派生收据](research/recovered/STONEAGE-PET-MODULE-15-TW10-ALL-SELECTED-MOTION-SOURCE-R1.json)。台湾 8.5 缺原 REAL 的六组待新来源；下一优先核原商店库存和两套物品主表。完整历史 CURRENT 原样保留。


## 2026-11-07 — ITEM05–06｜原商店库存对表与 415 幅混合 2.5 原 RD 补图

对照 191 条原 ItemShop 创建引用与 224 份原 ItemList。全库存配置 45 个不同编号只在备表，其中 21 个可追到实际源创建引用，5 个直接列号、16 个为范围候选。从已认证混合 2.5 原 ADRN/REAL 严格解码台湾 1.0 索引原缺的 415 个物品图号，剩余 416 个保留缺口。原 GMSV 完整字节现已重新取回并通过 SHA/CRC，下一优先 WORLD37-R2C 隔离回放。详见[原件、状态与私有观察边界](docs/continuity/STONEAGE-ITEM-MODULE-05-06-MIXED25-SHOPS-AND-RD-20261107.md)。旧完整 CURRENT 原样保留。


## 2026-11-07 — WORLD37-R2C｜原捕捉入口及成功尾段的隔离回放

完整混合 2.5 原 GMSV 经整 SHA、CRC 和原 RAR 成员复验后，执行 42 个有界 x86 回放。11 条编译条件全部验证，13 个逐项缺件对照均在评分前失败。成功路径实见条件道具移除、整数键 44 加一、野怪席位清除与角色池释放，新宠物仍在栏内。备表独有三件只验证夹具中的数字匹配。原服务端进程、网络、存档和官方部署仍待对应来源。详见[来源、轨迹和下一优先](docs/continuity/STONEAGE-STAGE-A-WORLD37-R2C-COMPILED-CAPTURE-REPLAY-20261107.md)。旧完整 CURRENT 原样保留。


## 2026-11-07 — ITEM07｜混合2.5物品缺图的2006台湾官方补丁索引交叉证据

接续 WORLD37-R2C 后首先核台湾8.5六组宠物缺少的 `real_158.bin`，当前可访问私人库仍无同源载荷，**PET12六组本轮新增原像素0**，不把1568个旧RD索引当画面。转用已永久归档的 ITEM06 和2006-09-11官方补丁 `PATCH129` 全量别名源目录，真正逐项联接831个物品图别名：混合2.5原缺图416中，408在补丁有单一RD内容、1个（21600）有三物理位置/两RD内容、7个在补丁也无索引；已经恢复的415原RD在补丁逐项压缩内容SHA完全相同。本次新增**409个来源限定后期官方补丁图块关联**，但新读/新解码/新PNG为0，不代表同版官方道具身份或运行时选图。完整[ITEM07连续性记录](docs/continuity/STONEAGE-ITEM07-PATCH129-SOURCE-ALIAS-CROSSWALK-20261107.md)、[831条完整数值和压缩指纹](research/recovered/STONEAGE-ITEM07-PATCH129-ITEM-ALIAS-CROSSVERSION-SOURCE-R1.json)、源固定工具和测试均已归档。最高NEXT **ITEM08**：只在能合法重读完整SHA认证的官方补丁实际图块载荷时补真实像素；若源缺，明确止点再转其它源合格游戏内容。旧 CURRENT、Stage A7PARTIAL+2OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING、overall_percent=null保留。


## 2026-11-07 — ITEM08 / CHAR10｜像素来源澄清与十二组人物全部原动作

[本轮连续记录](docs/continuity/STONEAGE-ITEM08-CHAR10-PIXEL-SOURCES-AND-BODY-MOTION-20261107.md)：官方PATCH129只提供ADRN索引；ITEM07的RD指纹来自另存的社区声称台湾8.5 `real_158.bin`。826条匹配经完整原记录SHA核同，409个缺图别名的411个精确原位置已归档；原载荷仍未找到，新物品像素0，旧报告保留。按缺源轮换规则，真正重取并核同台湾1.0原件，对CHAR02十二个数字人物候选补齐全部1,248条源动作/方向、6,920帧位置、4,152原位图；4,151严格解码，34699仅原画布范围观察。相对旧动作2增加3,576个可查位图，不是新人物数。私人逐帧查阅ZIP已保存，原商业图不入Git；浏览器因缺Chromium未运行，原色/动作命名/时序/原客户端仍未认证。下一优先CHAR11：同人物模块其余已有来源候选的批量原动作与像素，复用原包与工具、不猜身份。CURRENT原blob完整保留，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总进度未知。


## 2026-11-07 — CHAR11｜其余228个人物源数字组的全部动作与原位图

[CHAR11来源、私人原图与下一工作包](docs/continuity/STONEAGE-CHAR11-TW10-REMAINING-BODY-MOTION-20261107.md)：真正复用并核同台湾1.0原件，对其余228个数字候选组完成23,712条原方向/动作、130,592帧位置；69,620不同原位图中69,592严格解码，28仅原画布范围观察。四个0xFFFFFFFF原位置原样保留，不造图或丢帧，三序列因此仍有不可显示位置。相对CHAR10新增位图覆盖69,044，两轮联合240数字组/73,196原位图，不是对应数量的人物身份。196MB私人逐帧ZIP已保存，全PNG指纹与原索引二次复核；公开仅派生收据/工具/测试，原游戏、官方名册、动作名/时序/配色选择均未认证。下一最高MAP06：恢复有真实DAT和原图、尚未交付的完整场景候选。CURRENT全文与Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总体未知保持。


## 2026-11-07 — MAP06｜两份原地图的实际室内场景候选

[MAP06原件、图像与边界](docs/continuity/STONEAGE-MAP06-TWO-ORIGINAL-ROOM-SCENES-20261107.md)：真正取回并核同1005/1006原DAT，以55幅已有台湾1.0原RD候选PNG生成单层/合层共6张场景图，两源仍不认证同一官方部署。464个现代绘图候选位置经独立全画布重算相同，1795个原1–99非零值保留不猜作可见图。两原DAT、55原图、六图和查阅页的私人包已保存；原生层序/配色/碰撞/原客户端运行未知。下一最高MAP07按地图模块继续有合格原件的批量场景，先保管/复用源批，避免逐图重下大包。CURRENT全文、Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停与总体未知保持。

## 2026-11-07 MAP07｜28份原DAT与234组原RD候选像素批量室内场景

已从远端源重新核验并恢复28张互异SHA的混合2.5原DAT（各30×30，共151,424B），与台湾1.0原RD候选234组原图像配对，在私人离线研究器中获得4,408次候选图形位置、84张分层/合层观察图、28张合层独立逐像素核对和84张私人回放RGBA核对。公开元数据/可重验反例测试和两次源Actions全部保留，私人源/图不进入公开Git。**这不是原客户端渲染、同一官方部署或可玩游戏认证**。私人ZIP已在本地生成、ZIP CRC通过，但Library全ZIP持久归档未确认。

- [MAP07源边界、私人验收和下一工作](docs/continuity/STONEAGE-MAP07-28-ORIGINAL-DAT-SOURCE-ROOM-SCENES-20261107.md)
- [MAP07 28源图与234原图派生回执](research/recovered/STONEAGE-MAP07-28-ORIGINAL-DAT-SOURCE-SCENE-RECEIPT-R1.json)
- NEXT **MAP08**：继续地图模块真实原件优先的更大场景/缺图补证，按原源SHA与跨版本边界进行，Stage A 7PARTIAL+2OPEN不变，不进入引擎/网服建设。

**MAP07私人档案保管后验（2026-11-07）：** 先前container_path上传失败已保留；改用精确文件快照成功保存在个人Library `/石器时代/StoneAge-MAP07-private-28-original-room-scene-candidates.zip`，并完整回读验证34,044,818B、SHA256 `2b356fefa1f5c634a2a64837b20904e124ab9839ad6a4e3b9a642e3c05df29a2`、351项CRC均一致。MAP07初次主线合并 `244c8cc5` 的11项Actions均成功。详细见MAP07连续性记录的“追加后验”，NEXT仍MAP08。

## 2026-11-07 MAP08：955原DAT持久私人保管与6张来源场景

[MAP08来源及实际观察续接](docs/continuity/STONEAGE-MAP08-955-DAT-SIX-LARGE-SCENES-20261107.md)：一次真实取回955份已固定摘要的原DAT（不是955张新发现地图），私人完整保存供后续复用；6张原图齐全场景1200/1400/3100/3300/5100/5500已合成18幅候选原素材画面，47874绘图位置、1298组原PNG。独立NumPy与Pillow全18画布RGBA一致，约120MB私人包完整回读SHA/CRC同一。公仓库仅方法/派生元数据，无商业原文件。原客户端/原生碰撞/官方同部署不晋升。最高NEXT **MAP09**：复用955原DAT与已有像素包批量续原场景，缺图明确保留；不重下大载体。旧CURRENT完整保留，Stage A 7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null不变。

## 2026-11-07 MAP09：691份原地图的集中离线观察目录

[MAP09来源与验收续接](docs/continuity/STONEAGE-MAP09-691-SOURCE-READY-MAP-CATALOG-20261107.md)：复用已保存955原DAT及原PNG包，691份来源就绪文件（688不同原SHA）与3496原PNG集中可查，全部2073完整平面/合层RGBA由两算法独立一致。新增按编号筛选/分层的离线观察器，合成浏览器9画布与控件实测通过，不冒充私人原图浏览器或原客户端运行。其余264份细分为60份仅低值资格缺口与204份大于99缺候选图号；历史状态不改。最高NEXT **MAP10**：以真实原RD来源有限补缺，原件不可得则明确止点；不重复下载同源大包。完整CURRENT保留，Stage A 7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null。


## 2026-11-07 — MAP10｜60份低值语义未证原地图候选增量

已真正复用源SHA/CRC认证的955原DAT包、台湾1.0完整ADRN及MAP04原PNG库：MAP09排除的60份低值语义OPEN地图，64526处大于99合格候选引用，补入此前未收进目录的138幅旧原图，并由Pillow/NumPy独立逐完整画布核得180个新RGBA候选状态。原691份/2073状态不改，私人目录合计751份原DAT索引/3634候选图/2253帧；但低值69830处仍未知，不能认为751严格地图或可玩。其余204份仍有1114种/29748处>99来源原图缺件（15999/9440/3150/22413分类不变），应待合格原REAL/RD而不是索引猜图。单机内容优先、Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暂停、overall_percent=null不变；最高NEXT QUEST-MODULE-01按模块批量梳理真实任务脚本与活动来源。完整[来源、断言边界与私人档案说明](docs/continuity/STONEAGE-MAP10-60-LOW-VALUE-751-SOURCE-OBSERVATIONS-20261107.md)、[公开数值原SHA收据](research/recovered/STONEAGE-MAP10-PUBLIC-ORIGINAL-SOURCE-CUSTODY-R1.json)及[负例测试](tests/test_stoneage_map10_public_source_custody.py)。旧CURRENT全文blob `c89e0e33537990aa2132b47c40fef49a985a935c`原样保留。

### QUEST05（2026-11-07）｜598条来源创建点对应原地图与234条条件传送候选

在旧任务QUEST01–04和MAP04/09/10地图实物基础上，新增可检索的**源创建脚本→原floorid→955份DAT原文件/原SHA→源图资格**联接：598条来源CREATE涉及236个不同楼层，352/11/147/88条分别对应MAP09候选源就绪、MAP10新增低值未明、存在DAT但>99原图有缺口、当前955批次无同号DAT。另有234条带脚本SHA、条件关键词和目标楼层/坐标的**静态传送字面候选**，排除94次零目标展开，全部不能冒称原版已运行路线；南北岛/村庄与任务本体身份继续UNKNOWN。原CURRENT全文blob `c89e0e33537990aa2132b47c40fef49a985a935c`不改；阶段不变。详见 [QUEST05来源限定交叉图](docs/continuity/STONEAGE-QUEST05-598-CREATE-FLOOR-DAT-AND-234-WARP-20261107.md)、[公开全部来源记录](research/recovered/STONEAGE-QUEST05-598-ORIGINAL-CREATE-FLOOR-MAP-AND-WARP-CROSSWALK-R1.json)和[源契约回归](tests/test_stoneage_quest05_original_floor_crosswalk.py)。目前NEXT：有新合格任务源则小批QUEST06，否则进入GAMEPLAY-MECHANICS-MODULE-01；不重复搭建已有任务索引。

## 2026-11-07 — INTEGRATION04｜原捕捉条件 × 道具 × 宠物源表 × 原2D图形资格

[INTEGRATION04来源与边界](docs/continuity/STONEAGE-INTEGRATION-MODULE-04-COMPILED-CAPTURE-PET-ITEM-SPR-20261107.md)将既有WORLD37-R2C原x86隔离捕捉回放与PET11/12/13原来源归档**按每条key53严格连接**：11组编译捕捉条件/11份同后期社区归档宠物模板数字候选、13个单独缺件评分前失败、3个只在社区备用物品主表中的编号（20247、20253、20259）；图形资格为TW1真原像素2组、TW85社区原动作/RD索引且PET12未重新读取原REAL 6组、两包不覆盖3组。保留原表PETFLG=0的key53=8在**人工合格战斗初态**仍捕获成功这一反例，不能推天然可捕或不可捕、真实已部署宠物名称、同一台湾1.0服或原游戏可玩。公开只保留[11行来源限定派生数据](research/recovered/STONEAGE-INTEGRATION04-COMPILED-CAPTURE-PET-ITEM-SPR-SOURCE-BRIDGE-R1.json)和验证，不含任何版权原像素或程序。本轮新增真实原二进制执行/像素读取均为0。原多MB CURRENT Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 原样保存；Stage A仍7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总体percent=null。最高NEXT：Stage A跨模块实际材料缺口审计，仅在出现同部署有证主表/原宠物创建与新的原图实物时增量复核，不重复已有GAMEPLAY01–07或INTEGRATION01–03，不启动新引擎或网服。

## 2026-11-07 — INTEGRATION05｜24条原 GetPet 任务创建点的地图原件资格升级

[来源与受限边界](docs/continuity/STONEAGE-INTEGRATION-MODULE-05-GETPET-QUEST-FLOOR-SOURCE-20261107.md)：严格复用INTEGRATION01/02、QUEST05及INTEGRATION04四份已验派生原来源报告，把旧24条`CREATE→GetPet脚本`原SHA链接逐项接入新955份原DAT的MAP09图像就绪分级；16条同SHA地图有>99原RD候选，5条DAT已验但缺部分>99源图，1000号楼层在955件中没同名文件但**独立MAP02原1000.DAT整SHA已认证**（1条），余100/3000两条原MAP01提取失败保持缺源。23份不同原脚本、19个源楼层和36个不同原`GetPet`数字只是静态原件事实；其数字与INTEGRATION04的11个编译野怪捕捉键没有精确同号交集，不能推宠物身份、任务实际发放或绝对无关系；`event`路径不自动标节日，地图南北岛/村庄UNKNOWN。本轮没有新原DAT/RD/原程序运行，公开仅[24条可重验派生关联](research/recovered/STONEAGE-INTEGRATION05-GETPET-QUEST-MAP-ORIGINAL-SOURCE-GRAPH-R1.json)及8项独立负例，原资产和原多MB CURRENT不变。Stage A仍7PARTIAL+2OPEN、Stage B/wiki GATED、R79暂停、总体percent=null。NEXT对100/3000完整原DAT仅在新源到位后重开，其他图像缺件只读真RD/REAL；当前回22域优先新实物内容，不重复关系脚手架。

## 2026-11-07 — SCENE26｜真实原“宠物常识解说员”四处CREATE与三间室内原场景

[SCENE26 原源认证及私人画面观察](docs/continuity/STONEAGE-SCENE26-PET-TUTOR-FOUR-CREATE-THREE-ORIGINAL-ROOMS-20261107.md)：真正从已经保管的CHAR01私人原配置包与MAP07私人原DAT/像素观察包**重新读原文件**：`sa60/newbie/newbie.create` 原1548B/SHA `761dc3d1...`，同源`petmaster` 原1365B/SHA `04ba49ba...`，均与QUEST05原源SHA/私有ZIP CRC吻合。四条同一导师脚本的源CREATE分别在楼层1003/(19,15)/图16122、2003/(11,12)/图16127、3003/(16,19)/图16122、4003/(14,17)/图16122；源注释提到薩姆、漁村、加加、加魯卡，这些只是后期社区保存原CREATE的字面标签，不升级初版地理鉴定。私人前三份DAT原整SHA与MAP07/Q05核同，逐原位置读取三u16平面值，用现代投影黄色圆点标在已存在的台湾1.0 RD候选房间图上，**没有绘制原NPC精灵、认证其实际运行或证实同一官方版。**`petmaster`原`TYPE:MESSAGE`/`LV>0`教导忠诚、战斗、修复、合成与技能学习，本脚本不含GetPet/GetItem/DelItem/DelPet命令，不据此推出原玩法公式实际执行。4003在Q05的955 DAT目录已证原SHA，本轮私人MAP07小包没有其图，绝非历史缺图。完整两原脚本、三DAT、三标记场景及离线阅读页仅保存在私人Library `/石器时代/StoneAge-SCENE26-pet-tutor-three-rooms-private.zip`，**3275768B/SHA `826b81df...`，库回读12成员CRC和整SHA成功**；公开仅[来源限定数值索引](research/recovered/STONEAGE-SCENE26-ORIGINAL-PET-TUTOR-FOUR-CREATE-THREE-SCENE-SOURCE-R1.json)、校验测试和文档，不泄露商业正文/原图。历史CURRENT原blob `c89e0e33537990aa2132b47c40fef49a985a935c`保持不变；Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null。NEXT：只有拿到匹配来源的16122/16127真实NPC动画及选择或私有4003有证DAT才补实物；否则回其他模块寻找新的原字节内容，严格单机资料复原、不新建网服/引擎。

## 2026-11-07 — QUEST06｜四村长毛象快递真实原脚本、物品与层级差异

[QUEST06源实物和私人验收](docs/continuity/STONEAGE-QUEST06-FOUR-VILLAGE-MAMMOTH-COURIER-20261107.md)：在重新读原后期社区保存 mixed25 NPC 子树时确认 O61–O65 的虎训练师已做，**不重复当新成果**；转而真正复读`sa60/newbie/newbie2.create`及四份不同`worksell_*.conf` CP950原文件并逐原SHA/CRC与 QUEST05 对上。源8条CREATE分属四村组1014/1011、2014/2011、3014/3011、4014/4011，每组一个源脚本，8个楼层的原DAT SHA均已验、但没在本轮重绘或执行NPC。每份6条TALKEVENT的段4/5/6给出LV1–9交物品、10–19交物品、20–29检查PET（**无DelPet**）的静态流程，原奖赏Gold/Exps分别为1000/1000、2000/16000、5000/81000；原`LV>30`与`LV<30`在30级没有明确FREE/NOFREE字面，但这不是运行级漏洞定论。8件源物品同时在两版社区原master中，7件关联6幅**此前已解码**TW1原二维图候选，水/风两种不同合成枪共享图20407，顶级红宝石2622号图22322于TW1无索引、后期另有单独索引但未取得真REAL载荷；不造缺图、不误标2006官方patch含原RD。已私人保存五原文件、六原图、离线查阅页：`/石器时代/StoneAge-QUEST06-mammoth-courier-original-private.zip`，**40204B SHA256 cd26689805ad0c40e23ef934aa7c9509fe461630dd0431f7a43740abd7c91254；库回读及13成员CRC全部通过**。公开仅[原始来源限定JSON](research/recovered/STONEAGE-QUEST06-FOUR-VILLAGE-MAMMOTH-COURIER-SOURCE-R1.json)与9个来源断言，不发布商业脚本/原图/程序，旧CURRENT完整blob`c89e0e33537990aa2132b47c40fef49a985a935c`不改。Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null。下一步仅在相应新原件、原服执行或后期真正REAL出现时重开，其他来源合格游戏内容优先。

## 2026-11-07 — QUEST06-R2｜四村原对白的跨村物品提示连接

[来源边界与原文本限定关系](docs/continuity/STONEAGE-QUEST06-R2-ORIGINAL-DELIVERY-HINT-GRAPH-20261107.md)：私人复验四份原CP950 `worksell_*.conf` 的原SHA/CRC，在已验 QUEST06 原件中恢复8条 `TALKEVENT2/3` 的**源村名提示**，按同物品编号对应四份脚本的 `TALKEVENT4/5` 接收条件，形成四组候选有向脚本关联。1014→2014、2014→1014、3014→4014、4014→2014；本四脚本子集没有指向3014的提示，但不能推断全游戏缺任务。此为原静态对白、不是官方地图路线、运行NPC、发物或早期官方地理认证；公开仅[8条派生关系](research/recovered/STONEAGE-QUEST06-R2-ORIGINAL-COURIER-ITEM-HINT-GRAPH-R1.json)和来源回归。旧CURRENT完整blob不变、Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall百分比未知。NEXT跨域转真实源字节/画面，缺新材料不续建路由框架。

## 2026-11-07 — MAP11｜28间原房间三层复用关系与私人对比画面

[MAP11源完整原DAT逐层关系](docs/continuity/STONEAGE-MAP11-28-ORIGINAL-DAT-PLANE-FAMILIES-20261107.md)：实际重读已保管MAP07源ZIP 34,044,818B、351成员CRC和28份真实5408B DAT；完整28原DAT整SHA各异，但单独三张900格u16数值层整SHA分别有18/28/20种，第0层5个相同组覆盖15份楼层。对其中10对逐原数值格和完整1889×1425合成原RD候选画面比较，相同源第0层的完整场景画面均不同；不得当官方村庄、同一地图、碰撞、可通行状态。新15张画面分组对照及28份完整源指纹已私人Library二次SHA回读；公开仅[派生数值/来源负例](research/recovered/STONEAGE-MAP11-28-ORIGINAL-DAT-PLANE-FAMILIES-R1.json)，原DAT/RD/图像不入Git。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、总体百分比未知。下一项切换其他可读原游戏内容，不继续扩写地图分类框架。

## 2026-11-07 — SCENE26-R2｜原宠物常识导师第四间4003房间真实源像素补齐

[SCENE26-R2来源及四间私人画面](docs/continuity/STONEAGE-SCENE26-R2-FOUR-PET-TUTOR-ORIGINAL-ROOMS-20261107.md)：重新从已保存MAP09私人691场景和955件原DAT取得4003整5,408B/SHA `0a9fa2a089b6936e86eea458bca464038b8d5cb7fee057b9d2b393ffc6c6d6d4`，与SCENE26/QUEST05源CREATE和MAP09原收据同号同SHA。原导师点位4003/(14,17)、图号16122，此原格三u16原值 `5002/12802/49152`；用已验45幅候选原RD重放143绘图位置和三张1889×1425画布，两种独立合成像素与MAP09三SHA一致。SCENE26旧1003/2003/3003三间原DAT/已标记画面复核，四间来源限定现代对照图和离线查阅页已私人保管并库回读。公开仅[来源限定数值规格](research/recovered/STONEAGE-SCENE26-R2-FOUR-ORIGINAL-PET-TUTOR-ROOMS-SOURCE-R1.json)及回归，原商业DAT/RD/CP950正文不入Git。未绘出真正16122/16127 NPC，没有原生执行、同版官方归属/碰撞/图层证明；新原DAT下载0、新RD解码0、Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、整体完成率未知。NEXT不重复四房间，转其它真实原游戏内容。

## 2026-11-07 — SCENE26-R3｜16122/16127原NPC图号的跨版本原位图索引实证

[真实原索引和证据范围](docs/continuity/STONEAGE-SCENE26-R3-NPC16122-16127-ORIGINAL-ALIAS-CROSSVERSION-20261107.md)：将四个已验证导师CREATE的图号与仓库已有完整43,632条原资源目录实际匹配。台湾1.0当前逻辑别名两个均未命中；大陆5.0及台湾PATCH129各命中一次，CN50/patch各对应原RD块SHA完全一致：16122→物理232699/32×87/1930B，16127→物理232704/36×96/2089B。同整数物理位图号16122/16127的源查询均未命中，严禁混用命名空间。本轮是原源定位/完整内容散列，不是已取得图片像素、SPR动画、真实导师角色、同版客户端或原始运行。源Actions、[公开数值](research/recovered/STONEAGE-SCENE26-R3-NPC16122-16127-ORIGINAL-ALIAS-CROSSVERSION-R1.json)和负例CI保存，新原商业素材0，完整CURRENT原Git blob不变。下一项必须以真REAL原块的合法保管为前提，不重复地图图示和空白联表。

## 2026-11-07 — QUEST07｜原新手NPC配置备份的26个未启用候选与九个真实地图

[QUEST07完整来源、私人五房间对照及缺失边界](docs/continuity/STONEAGE-QUEST07-INACTIVE-NEWBIE-BACKUP-NINE-DAT-FIVE-SCENES-20261107.md)：已保存后期社区mixed25原RAR整SHA再验，原`sa60/newbie/newbie.create.bak` 6190B/SHA `fa83b8f1...` 有34条原CREATE，当前`newbie.create`1548B的8条原字段均同备份中8条；另26条**仅为备份候选，绝非已证明启用**，涵盖训练/医疗/商店/宠物技能/对战等9个旧楼层。9份原DAT逐原SHA/CRC取出且与另一私人MAP09完整955原DAT包逐文件相同；5房间9候选NPC站位已在真实原RD来源现代缩略图上私人观察，17个候选坐标仍无匹配来源完整视觉。备份24个外部文件引用仅1个当前同目录原文件存在，23个缺源不补造任务/奖励。原备份、九DAT、五场景及对照图私人Library真实回读ZIP18CRC/SHA；公开仅[来源受限数字](research/recovered/STONEAGE-QUEST07-INACTIVE-NEWBIE-BACKUP-26-CREATE-NINE-ORIGINAL-DAT-R1.json)和负例，未执行原NPC、未取新地图/精灵或改变原历史CURRENT。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、整体完成率未知。NEXT仅在缺失原脚本/官方启用证据到位时重开，其他真实游戏内容优先。


## 2026-11-07 — QUEST08｜原采矿鉴定、救援赠矿与三处兑币配置

[QUEST08来源、完整字面差异及私人原文](docs/continuity/STONEAGE-QUEST08-ORIGINAL-MINING-APPRAISAL-LIMITSHOP-20261107.md)：实际重读源SHA/CRC认证的CHAR01完整2,205原文件，在原有索引中新增恢复6份采矿脚本的21段条件/动作和3份LIMITSHOP数字配置，并逐原字节核9条CREATE。三类矿石2469–2471与鉴定书2472–2474关联明确；前两类低档4条裸DelItem数量保持null，第三类原写*8/*5，不修正为统一数量或宣称实际扣除。三处兑币原rate与6行旧物品原索引相连，不推成交公式；任务起源ORIGIN_UNRESOLVED、真实执行未知。本轮原DAT/RD新读0，13份原文件与全文查阅私人包已保存并回读SHA/15项CRC；公开仅[数字/散列](research/recovered/STONEAGE-QUEST08-MINING-APPRAISAL-AND-LIMITSHOP-SOURCE-R1.json)、提取器及6项来源验收。原CURRENT完整blob不改，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、整体百分比未知。NEXT只对真实可得的采矿权利书出售/矿石来源作有限上游补证，缺源则转其他任务族。


**QUEST08同轮上游追加：** 又实际读取5原参数，定位权利书商店2475–2477于源floor100/(412,337)，入口原目标10601/(28,49)。其与NPC“第五层买权利书”说明的冲突原样保留，不改位置、不推收费或实际无限采矿。最终私人包18原文件/20成员已回读SHA/CRC；7项专项回归和28项相关本地检查通过。最终NEXT转其他真实任务族，实际采矿/许可运行待真源才重开，详见同一QUEST08连续性页的追加。


## 2026-11-08 — QUEST09｜梦幻洞窟原脚本、两套迷宫与实际源画面

[QUEST09来源、原字面冲突与私人两场景](docs/continuity/STONEAGE-QUEST09-DREAM-CAVE-ORIGINAL-SCRIPTS-AND-TWO-MAPS-20261108.md)：真正复读CHAR01完整2,205原文件，从15原配置恢复12事件、117条创建及106条字面传送；供物2603、固定奖励2604/2605/2606及20号随机池保留原序，伊甸/地精灵173分支单独标明。老人与2003攻略相差一格、入口多点及42守门仍指向41等冲突均不修正。又实际复用MAP09原DAT和原候选PNG，对41/42两70×70场景的6幅4K完整画布双实现核同原SHA，私人标出8个源位置；不画假NPC、不认证运行或同官方部署。25成员/28MB原文及画面包已保存并回读SHA/CRC。公开仅[控制值与来源](research/recovered/STONEAGE-QUEST09-DREAM-CAVE-ORIGINAL-CONTROLS-R1.json)、[原地图观察收据](research/recovered/STONEAGE-QUEST09-TWO-ORIGINAL-CAVE-MAPS-OBSERVATION-R1.json)、复用工具与8项回归；36项相关本地检查通过。旧CURRENT全文不改，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、整体百分比未知。NEXT转其他尚未具体恢复的真实任务族，本族运行语义待新证再开。


## 2026-11-08 — QUEST10｜去重纠正后恢复吉鲁采石场与精灵原任务族

[QUEST10原源、旧NEXT纠正与私人材料](docs/continuity/STONEAGE-QUEST10-QUARRY-SPIRITS-SOURCE-AND-DEDUP-CORRECTION-20261108.md)：先发现QUEST09的双村送物NEXT早已由O24/O32完成，不重算成果，转向12份采石/精灵原配置。实际恢复44事件/7创建关系，库伊原创建指向king/event69_1，旧event30_5及.old无本CREATE直接引用且条件/设旗不同；保留ENDEV=4ENDEV=29原异常，不修语法。11道具的21原行正文重建后SHA全匹配；2391只在B表且原名三墀蛇牙，与协议书注释冲突不改名，双镜同名同图不合并。9道具具6幅真原RD候选PNG，7原DAT的8源点在已验旧缩图私人标注；未重绘完整场景、未运行任务或补NPC精灵。56成员私人源/图文包已保存并回读SHA/CRC；公开仅[必要数字/散列](research/recovered/STONEAGE-QUEST10-QUARRY-SPIRITS-ORIGINAL-SOURCE-R1.json)、工具和6项回归，42项相关本地检查通过。完整CURRENT及Stage A/B/wiki/R79/总体未知不改；NEXT必须先查重再选另一来源就绪任务族。

## QUEST11 — 两族误会原任务族（2026-11-08）

[最新接力与来源止点](docs/continuity/STONEAGE-QUEST11-TWO-TRIBES-ORIGINAL-SOURCE-20261108.md)：8事件脚本、68原段、8配置点、13道具/25原行及5原图位置；原拼写和数量省略不修补。矿石商人不误称传送入口，未认证原运行或官方版本归属。


## 2026-11-08 — QUEST12｜矿山比赛、采矿权与原许可证入口

[QUEST12 真实来源与有界止点](docs/continuity/STONEAGE-QUEST12-MINING-COMPETITION-ORIGINAL-SOURCE-20261108.md)：重新回读后期社区 mixed25 私人原档 2,205 成员全 SHA/CRC，恢复 2 名原角色的 13 段任务脚本、1 矿工参数、21 个同名外围 CREATE（其中仅 1 个许可证入口），以及 31805/31806 两份原 DAT 的五处源格。8 件有关物品原 15 行来自既存 ITEM01 源表，原图源身份分离。静态数据表明原入口要求 2527 并指向 31806/(34,6)；全 2,205 文件的 GetItem 字面扫描没有 2533/2534 的发放行，不得据此补造取得路径或宣称所有官方版本不存在。人物与地图真正运行、胜负掉物、原版/活动属性均未认证。公开只存[派生数字/原来源 SHA](research/recovered/STONEAGE-QUEST12-MINING-COMPETITION-ORIGINAL-SOURCE-R1.json)与可复核测试，原游戏素材留私人，完整旧 CURRENT 不变；Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暂停、总体百分比未知。NEXT 按 QUEST 模块对未复原的来源就绪任务族查重择一，不重复 QUEST12。

## 2026-11-08 — QUEST13｜哥亚山洞窟乌力送信、花朵与回信

[QUEST13 原配置、道具、六张真实 DAT 与来源界限](docs/continuity/STONEAGE-QUEST13-GOA-ULI-LETTERS-ORIGINAL-SOURCE-20261108.md)：从已验证的后期社区 mixed25 私人 2,205 个 NPC 原文件中读取 11 份本族原创建／参数，10 个 CREATE 点分布于 20401–20406 的六份真实原 DAT；16 个事件段的源 TYPE/条件散列逐项与既有 QUEST01 目录相同，不重复当新发现。原字面连接 2414/2425/2424/2426/1206 五道具（两份原物品表共 10 原行）；2425/2426 同用原图候选别名 24222 但不是同道具，全部五 ID 仅有跨保存来源的 TW1 候选 RD 图，非原版同部署。私人原文／6 场景标记与原图候选 40 成员包 219161B／SHA256 c6f86d050b22ab6fe3f6e56b8062fc21cbb576ace521a1d7752a12d0845773cd 已上传并回读同 SHA/CRC。公开仅[原来源限定 JSON](research/recovered/STONEAGE-QUEST13-GOA-ULI-LETTERS-ORIGINAL-SOURCE-R1.json)、工具及 9 项回归；原脚本、DAT、图像不入 Git。原生任务选择、数量执行、NPC 行为、历史官方身份均未认证；Stage A7PARTIAL+2OPEN、B/wiki GATED、R79 暂停、总体百分比未知。最高 NEXT QUEST14 三龙／龙之巢穴族，先按新远端及来源查重。

## 2026-11-08 — QUEST14｜龙之巢穴三龙奖励与守护者原任务族

[来源、静态分支和私人原件的有界复原](docs/continuity/STONEAGE-QUEST14-DRAGON-NEST-THREE-DRAGONS-ORIGINAL-SOURCE-20261108.md)：按 GitHub main 最新真实后验及已验 QUEST13 NEXT，重新验证后期社区 mixed25 私人 NPC 2,205 成员全部 SHA/CRC，从 event17 原 CREATE/共享模板与四原脚本恢复4原创建、10 EventNo/TYPE块，段 SHA 与旧 QUEST01 目录独立同。来源 floor20801/20807 两份真实 DAT 70×70/50×50 和4源格实际三平面 u16；七道具2457/2458/2459/2505/2460/2461/2462均实取两物品表各一原行、共14行和独立跨源TW1原RD候选7 PNG。原文三龙条件同为 NOWEV17、四道具齐备，分别 GetItem2462/2460/2461 且 EndSetFlg17；全2,205 原NPC文件没有三龙玉的 GetItem 字面发放行，未推出掉落或游戏缺陷。私人34成员81,015B SHA256 5f004435b501c7e2bded801ec8e847482cfca5fffb409ad7c2160e5247074232 已存个人 Library 并独立回读全SHA/CRC；公开仅[数值/哈希和负证](research/recovered/STONEAGE-QUEST14-DRAGON-NEST-ORIGINAL-SOURCE-R1.json)、工具与10项来源测试。旧CURRENT完整保留，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、完成率未知；无原生对话选择、战斗掉落、领奖重复或官方早期同服证明。NEXT QUEST15 先原族查重后选择下一组真实可读原件。

## 2026-11-08 — QUEST15｜吉德、强恩、沙拉山贼事件原脚本与双物品表

[来源独立重读、28事件段和未认证边界](docs/continuity/STONEAGE-QUEST15-BANDIT-EVENT20-ORIGINAL-SOURCE-20261108.md)：对后期社区 mixed25 私人 2,205 NPC 原 ZIP 及原两物品表实物重验，复原 event20 6个原 CREATE、28原 EVENT 段的条件／取物／删物／随机奖励，逐块与旧 QUEST01 目录 SHA 同一而不重复记新源。九件 2486–2494 两表原行共18条，与九幅跨载体台湾1.0真 RD 候选图散列相联；2488信交换2489、2490–2494原文只是一条随机池命令，LV>79/NOWEV161 的 2744→2745 单独保留，2744/2745 在已验13915原物品目录缺位不代表原游戏从无。3406/20607/20608 三张原地图仅联接旧 MAP09 已验 SHA；3400 来源地图/本轮新 DAT 实物尚缺，不假画场景或推运行。私人36成员33,087B原文及图形包在个人 Library 保管，公开只有[受限数字及哈希](research/recovered/STONEAGE-QUEST15-BANDIT-EVENT20-ORIGINAL-SOURCE-R1.json)、提取工具与12项交叉索引回归。旧CURRENT完整历史、Stage A 7PARTIAL+2OPEN、B/wiki GATED、R79暂停及总体未知均不变。NEXT `QUEST16-DEDUP-AND-SOURCE-READY-NEXT-FAMILY`，先重新读取远端后再选尚未恢复的有真原件任务族。

## 2026-11-08 — QUEST16 造斧／取水／伐木与原木材交易来源限定复原

本轮从已验后期社区 mixed25 私人原源实际读回 `jaruga/event/20501ev.create` + 5 原脚本与共享模板，5 CREATE/36 TYPE 与旧 QUEST01 段 SHA 交叉一致；12 个道具的两份原物品表 24 行及 8 幅跨载体 TW1 原 RD 候选图 SHA 复核。木材商人 14 档 `GetStone` 字面不推运行价格；数量 12 的分支 `DelItem` 少 `2467`，保留原差异，不擅自修复。20507/20508/3300 三张地图仅对接旧 MAP09 已验 SHA，3000 当前源就绪目录缺 DAT，不假造源格。私人 40 成员 ZIP／SHA `b71dfd1244871b3d864621db7f7dc7c6822ac8646ceafb71a8670dfd996688e5` 已独立云端 Library 回读 CRC/整 SHA；原商业素材不公开。详见[QUEST16 来源边界](docs/continuity/STONEAGE-QUEST16-AXE-WOOD-SOURCE-20261108.md)、[可回归源数值](research/recovered/STONEAGE-QUEST16-AXE-WOOD-SOURCE-R1.json)与专项测试。旧 CURRENT Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 全历史不变；Stage A 7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79 暂停、整体百分比未知。最高 NEXT QUEST17 原任务族查重/新源就绪任务；不得重新包装已验事件数或改写官方起源。

## 2026-11-08 — QUEST17 卡鲁它那牧场恐龙打工与调查证明书原资料

[来源边界、三种手环与旧脚本分叉](docs/continuity/STONEAGE-QUEST17-DINO-RANCH-ORIGINAL-SOURCE-20261108.md)：私人 mixed25 原 NPC 包实际重读6条 CREATE、61事件段（全与旧 QUEST01 各段 SHA 一致，非新发现61段），来源限定恢复 21 档石币字面、558/559/560 三个 PET 谓词、2594–2596 训练手环与 2589–2592 调查证明书。保存目录还含三份各18段的未获本 2205 NPC CREATE 引用旧脚本，当前实际指向三个各10段 `*2` 版本，不能并成同一运行规则。两原物品表8 ID/16物理行、跨 TW1 仅4幅不同原RD候选PNG；201/20901地图只复用旧 MAP09 SHA，未新测源 DAT 格。私人 32 成员原字节、SHA/CRC 已在个人 Library 保存后二次回读；公开仅[数值散列目录](research/recovered/STONEAGE-QUEST17-DINO-RANCH-SOURCE-R1.json)、工具和15个回归。CP950 多字节出现 `0x7d` 的原配置按解码后识别花括号，避免截断2条 NPC。旧 `docs/CURRENT-STATE.md` 全历史 blob `c89e0e33537990aa2132b47c40fef49a985a935c` 原样保存，Stage A 7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、总体百分比 null。NEXT QUEST18 先对确有原件的新任务族去重，不扩大网服/引擎/新单机设计。

## 2026-11-08 — QUEST18 / QUEST19：来源限定任务、道具和地图关联续接

[QUEST18 吉鲁火之仪式、羽毛、巴那姆水壶](docs/continuity/STONEAGE-QUEST18-GIIRU-FIRE-RITUAL-SOURCE-20261108.md) 已完成源脚本/44原道具ID/37条NpcWarp候选与现存MAP09的受限数字交叉核验，详见[公开派生数据](research/recovered/STONEAGE-QUEST18-GIIRU-SINK-SOURCE-R1.json)。[QUEST19 马祖送信、切绳石与迷宫十宝袋](docs/continuity/STONEAGE-QUEST19-MARJU-POST-TREASUREBAG-SOURCE-20261108.md) 重新验后期mixed25原 NPC 12配置/12脚本/27既有事件、10个NPC重定位脚本及50位置候选、两组重复数字随机奖品表和61物品ID缓存行；全部源 SHA/CRC 与旧QUEST01/ITEM01和MAP09交叉，原商业资料保持私人。QUEST19 PR #259 经首次测试字段误引失败、修复后的候选/主线 Actions 成功验收，**不能抹掉失败历史**。两包均仅 `ACCEPTED_SOURCE_BOUNDED`：不宣称JSS1999/TW1官方同服或原生NPC、奖品、客户端可玩。旧 `docs/CURRENT-STATE.md` 巨型历史原样保存。Stage A仍7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79暂停。下一项 QUEST20 先对整个任务模块去重/复核优先级，再投入真实可恢复玩家内容。

## 2026-11-08 — QUEST20 五兄弟地下城与任务模块审计

[QUEST20 来源限定静态任务和跨模块关系](docs/continuity/STONEAGE-QUEST20-FIVE-BROTHERS-SOURCE-AND-MODULE-REVIEW-20261108.md)已由[PR #260](https://github.com/chinaneedM/stoneage-rebuild/pull/260)合并并主线CI真实成功：QUEST08–19十二专项80脚本中78早已属于QUEST01的295脚本/1349事件目录，2份仅保留版本分叉，不能当“新增80份任务”；本族另30份原脚本85旧事件，复原23个原选择NPC、五组不同任务道具（十ID同一原图别名24222）、6个原DAT几何候选与五个WORLD21已验领宠实例→同源模板图号=NPC源图别名联接。新结果是源关联规格，非新增5条宠物奖、原游戏跑通或初代台湾/大陆官方同版。首候选CI字段名误引失败、修复后候选/主线全部通过，失败历史保留。原游戏/服务端原字节与私人图像没有公开，`docs/CURRENT-STATE.md` 全历史blob c89e0e33537990aa2132b47c40fef49a985a935c 完全保留。Stage A仍7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79暂停。最高 NEXT QUEST21 先审未专项的真实内容，避免无界重复旧索引。


## 2026-11-08 — QUEST21｜琉璃洞窟原脚本、两袋奖励与2003攻略分源对照

[QUEST21来源、差异和接力](docs/continuity/STONEAGE-QUEST21-LIULI-ORIGINAL-SOURCE-COMPARISON-20261108.md)已通过[PR #261](https://github.com/chinaneedM/stoneage-rebuild/pull/261)及主线CI验收：实际重读并核验2,205原NPC文件，6活动引用脚本/22段均属QUEST01既有材料；本轮恢复日记2698/项链2699交付2701、两袋各85原序奖品位置及2700交付字面、伊布9处移动字面含1重复位置，去重8坐标与既有2003攻略相同。63原地图CREATE含57传送字面，保留两组同坐标多目标、反向不同落点及攻略楼层/内部floor差异，不静默选覆盖规则；17份原DAT仅复用旧SHA/几何，200仍缺匹配本955件目录的原DAT。11原文件/12物品行/六跨源TW1候选PNG的31成员私人包已保存并回读SHA/CRC；公开仅[数字和散列](research/recovered/STONEAGE-QUEST21-LIULI-ORIGINAL-SOURCE-COMPARISON-R1.json)、工具、10专项验证和[实际验收收据](research/recovered/STONEAGE-QUEST21-PUBLICATION-ACCEPTANCE-R1.json)。本地257任务相关检查、候选四项及内容主线专项均成功；旧CURRENT全文不改。原生执行/同官方版本/掉落和随机概率仍未证，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、整体百分比未知。最高NEXT QUEST22：先查重，有限复核碧青洞窟七份真实原脚本与39/40/42前置、2766–2770道具关系，不扩四洞窟全集或新引擎。


## 2026-11-08 — QUEST22｜碧青洞窟原任务关系与三张真实DAT场景

[QUEST22来源、三场景和接力](docs/continuity/STONEAGE-QUEST22-HEKISEI-ORIGINAL-SOURCE-AND-THREE-SCENES-20261108.md)已由[PR #262](https://github.com/chinaneedM/stoneage-rebuild/pull/262)合并并内容主线CI通过：七原脚本/23段和两随机表均属旧QUEST01/WORLD23，不重复当新增任务；本轮连通39/40/42三类独立前置、2768→2769→2770原交付及实际大小箱对应，保留制晶原逗号条件与省略数量。实际重读21215/21308/31302三原DAT和156既有候选PNG，双实现九完整画布SHA同旧MAP09，六个源CREATE格已独立核值并私人标记；没有绘制原NPC或运行原游戏，3400仍缺本955件匹配DAT。194成员原文/地图/候选源图/查阅页私人包保存后二次完整SHA/CRC相同，公开仅[来源数值和散列](research/recovered/STONEAGE-QUEST22-HEKISEI-ORIGINAL-SOURCE-AND-THREE-SCENES-R1.json)、工具、九专项检查和[实际验收收据](research/recovered/STONEAGE-QUEST22-PUBLICATION-ACCEPTANCE-R1.json)。本地266项任务相关测试、候选四项及内容主线专项成功；原CURRENT全文及Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、整体百分比未知保持。最高NEXT QUEST23先做模块材料查重复核，再对来源就绪的poru02剧情批次开展有限实物整合，保留borncenter与旧titan结束标记缺失，不继续扩四洞窟或新引擎。


## 2026-11-08 — QUEST23｜波拉岛四圣石剧情与九张borncenter来源场景

[QUEST23原来源、序号差异和接力](docs/continuity/STONEAGE-QUEST23-PORU-FOUR-STONES-SOURCE-AND-NINE-SCENES-20261108.md)已通过[PR #263](https://github.com/chinaneedM/stoneage-rebuild/pull/263)与内容主线CI：20配置/102原TYPE段和五条GetPet都属旧目录，本轮整合四圣石、训练/交宠、送水及证明书交换与17道具34原行/12跨源候选图。九份原DAT与913既有候选PNG实际重读，双实现27完整画布SHA同MAP09，17个borncenter原格独立测值并现代标记，原四整数保留且不冒作真实出生格；500原DAT仍缺，未画原NPC或运行原游戏。注释商人字段与#}、titan粘接EventEnd原样保存，两套目录以路径/SHA及各自序号联接；初次本地序号联接停止已据实记录。1,014成员私人包保存后二次整SHA/CRC一致，公开仅[派生数字/散列](research/recovered/STONEAGE-QUEST23-PORU-FOUR-STONES-SOURCE-AND-NINE-SCENES-R1.json)、工具、10项检查及[验收收据](research/recovered/STONEAGE-QUEST23-PUBLICATION-ACCEPTANCE-R1.json)。本地276项任务相关测试成功，QUEST22默认报告及194私人成员逐字节不变；旧CURRENT及Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总体百分比未知保持。最高NEXT QUEST24：先对poru01族查重，承接ENDEV63原来源poru/boy04段1与已有村落地图，不扩大网服或引擎。

## 2026-11-08 — QUEST24｜波拉岛旗标63前置、原功能模板与四张DAT场景

[QUEST24来源、实际差异和接力](docs/continuity/STONEAGE-QUEST24-PORU-FLAG63-FUNCTIONS-AND-FOUR-SCENES-20261108.md)已由[PR #264](https://github.com/chinaneedM/stoneage-rebuild/pull/264)合并并内容主线CI通过：poru01原32配置与boss第0配置、12事件文件39旧TYPE段完成精确模板/参数联接，找到原boy04设置63→QUEST23的mary请求63的静态前置；GetPet352仍为WORLD21旧实例，不是新增宠物或实际领奖。保留wpm命名实际为ExChangeMan、两实际WarpMan字面、六肉逗号条件及18544/18558原差异。四原DAT与490既有候选PNG实际重读，双实现12画布同MAP09，27个borncenter来源中心独立核值并现代标记；六个floor500配置仍缺匹配DAT，未运行原客户端。578成员私人包保存后二次整SHA/CRC一致，公开仅[派生证据](research/recovered/STONEAGE-QUEST24-PORU-FLAG63-FUNCTIONS-AND-FOUR-SCENES-R1.json)、工具、10专项检查与[验收收据](research/recovered/STONEAGE-QUEST24-PUBLICATION-ACCEPTANCE-R1.json)。全部286项任务相关测试及候选四项/内容主线专项成功；旧CURRENT与Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总体百分比未知保持。最高NEXT QUEST25：两组波拉岛关系达到来源止点，回任务模块与WORLD/角色/地图/宠物覆盖复核，选择另一组材料就绪且增加实际内容关联的批次，不重复旧TYPE计数或扩缺图加载器。

## 2026-11-08 — QUEST25｜两岛四条环岛路线与48检查站原资料

[QUEST25来源、路线分叉和接力](docs/continuity/STONEAGE-QUEST25-FOUR-ISLAND-TOUR-ROUTES-20261108.md)经[PR #265](https://github.com/chinaneedM/stoneage-rebuild/pull/265)与内容主线CI验收：两原CREATE各27配置、54旧脚本/322既有TYPE段组织为A/B/C/D各12站，精确连接原NPC坐标、两组证明石、48关键词、退出/终点奖励、48道具ID/96原行/18跨源候选图与15个WORLD21既有宠物实例。保留B仅首站带ENDEV2、C全站带ENDEV17、D先列另一线路提示、A终点奖励先列及奖品重复位置，不据原排列断定运行选择或随机概率。35地图资格仅复用旧元数据，未新读DAT/运行原游戏，活动起源未决。173成员私人原文资料包保存后二次整SHA/CRC相同，公开仅[来源数字/散列](research/recovered/STONEAGE-QUEST25-FOUR-ISLAND-TOUR-ROUTES-SOURCE-R1.json)、工具、10专项验证和[验收收据](research/recovered/STONEAGE-QUEST25-PUBLICATION-ACCEPTANCE-R1.json)。全部296项任务相关检查通过，私人页110链接/57原文/48换石与关键词独立核同，浏览器未执行。首次新分支误用更新接口的两次422及随后创建分支修正如实保留；候选四项/内容主线专项实际成功。旧CURRENT完整不改；Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总体百分比未知。最高NEXT QUEST26：有限核原event02_1/2的SP条件、CleanFlg2和2414/2415贝壳/花互送，衔接ENDEV2原来源，不扩环岛看板、缺图或分支解释器。

## 2026-11-08 — QUEST26｜贝壳／花互送、原CLEAN与旗标2跨任务衔接

[QUEST26原来源与接力](docs/continuity/STONEAGE-QUEST26-SHELL-FLOWER-FLAG2-20261108.md)经[PR #266](https://github.com/chinaneedM/stoneage-rebuild/pull/266)及内容主线CI验收：两原NPC/六旧段明确保留SP整数分组、原逗号、2414/2415双向交换、CleanFlg2和EndSetFlg2；把两设置来源接上QUEST25中16文件39个精确ENDEV2条件，以及QUEST24两条ITEM2414门槛和另一贝壳取得来源，不称旗标2为环岛通关或唯一贝壳出处。两原道具四行、两跨来源原候选PNG/RGBA再验并实际查看；DAT/原NPC/浏览器/原游戏未运行，SP业务含义和实际清旗标仍未知。12成员私人包保存后二次整SHA/CRC一致，公开仅[数字与散列](research/recovered/STONEAGE-QUEST26-SHELL-FLOWER-FLAG2-SOURCE-R1.json)、工具、10项验证和[验收收据](research/recovered/STONEAGE-QUEST26-PUBLICATION-ACCEPTANCE-R1.json)。全部306任务相关检查、候选四项/内容主线专项通过；巨型CURRENT全历史不改，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总体百分比未知。最高NEXT QUEST27：集中复核event03_1/2同时承载的事件3/5斧头交付与感谢函往返，按原引用关联道具和坐标，不再扩大CLEAN或SP解释器。

## 2026-11-08 — QUEST27｜事件3／5斧头与感谢函完整双端来源

[QUEST27原来源、同图异字段与接力](docs/continuity/STONEAGE-QUEST27-AXE-LETTER-EVENT3-5-20261108.md)经[PR #267](https://github.com/chinaneedM/stoneage-rebuild/pull/267)与内容主线CI验收：两旧脚本/五段连接原斧头2416交付→旗标3→感谢函2423→奖励斧头2448，保留CREATE0指event03_2、CREATE1指event03_1的反序、原物理段序及ENDEV3/5逗号。两原表六行原SHA一致，2416/2448共用候选图但原第79栏1/0不同；字段按既有后代94栏命名，与原对白差异并列，不称原丢弃/消失实验或官方同版。三ID仅两幅原候选PNG/RGBA核同并查看，无新原RD/DAT/NPC/浏览器或原程序执行。14成员私人包保存后二次整SHA/CRC一致，公开仅[源数值和散列](research/recovered/STONEAGE-QUEST27-AXE-LETTER-EVENT3-5-SOURCE-R1.json)、工具、8项验证及[验收收据](research/recovered/STONEAGE-QUEST27-PUBLICATION-ACCEPTANCE-R1.json)。全部314项任务相关检查通过；共用读取函数后QUEST26默认报告及12私人成员字节不变，候选四项与内容主线专项实际成功。旧CURRENT/四历史不改，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总体百分比未知。最高NEXT QUEST28回任务模块查重，集中药草/药剂剩余来源材料，保留后期分叉，不继续扩CLEAN/SP/丢弃helper。

## 2026-11-08 — QUEST28｜药草／药粉、骨头交换与四场景

[QUEST28 原源脚本、道具与四 DAT 场景](docs/continuity/STONEAGE-QUEST28-HERBS-MEDICINE-FOUR-SCENES-20261108.md)完成独立私人包复验：五原脚本15段与旧 QUEST01 完全同源（新增脚本0），8原NPC/配置/模板文件、两原物品表9 ID/18行、4 原DAT场景6个CREATE格及439幅有据候选地图PNG逐散列核验。保留 `ITEM=2446*10` 与裸 `DelItem:2446` 不一致、1982未明确删除、药草旗标1/87逗号三条件、缺 `nevent02_1` 与地图3200的限定缺图，不将后代1984粉剂归于初代。私人原脚本/地图/像素仅留 Library，公开[数字和来源哈希](research/recovered/STONEAGE-QUEST28-HERB-MEDICINE-FOUR-SCENES-SOURCE-R1.json)、测试及验收说明，原客户端未运行。巨型 CURRENT 原样保留、Stage A 7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79暂停、整体完成率未知。**最高NEXT QUEST29**：对任务模块全局查重后选另一实际新增玩家可见资料的批次；不得重复小范围辅助工具。

## 2026-11-08 — QUEST29｜精灵王事件69来源与任务模块去重

[QUEST29 原来源审查](docs/continuity/STONEAGE-QUEST29-SPIRIT-KING-ORIGINAL-SOURCE-20261108.md) 已经 [PR #269](https://github.com/chinaneedM/stoneage-rebuild/pull/269) 合并并经主线专项 CI 实测成功。复用原 QUEST01 的295脚本/1349段/14源目录查重，event69的13脚本/71段全部为旧已归档来源，不称新发现；本轮把25原CREATE、36原文件、48道具ID/96原行、随机重复位置和三条GetPet原操作数355/484/1479联接。仅5个道具具有TW1跨来源原像候选，43个没有合格候选；绝不视作初代没有物品。私人原脚本、物品行、图像留用户Library，最终138成员包91,171B/SHA256 e710f97dfc165e06680f3b016b19313c6a5569558cfc700759da1cc2f0f28407已二次回读整SHA及CRC同。公开仅[派生证据](research/recovered/STONEAGE-QUEST29-SPIRIT-KING-EVENT69-SOURCE-R1.json)、工具、10项回归及[主线验收收据](research/recovered/STONEAGE-QUEST29-PUBLICATION-ACCEPTANCE-R1.json)。候选4项、主线专项1项Actions实际成功。旧CURRENT blob c89e0e33537990aa2132b47c40fef49a985a935c全文不改，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null。最高 NEXT QUEST30：只选未专项整合且有真实来源增量的任务批次；否则有界转跨模块联合复核，不扩网服/引擎/体验优化。


## 2026-11-08 — QUEST30｜恐龙收集任务与道具2607来源冲突

[QUEST30 原来源、旗标35、两轮交宠与跨源矛盾](docs/continuity/STONEAGE-QUEST30-DINOSAUR-COLLECTOR-EVENT35-SOURCE-20261108.md)：严格去重排除已由QUEST16覆盖的20501ev1..5和QUEST09已覆盖的seimu/event/event01_1/2，本轮专项复读seimu/event/event02_1、对应原CREATE及功能模板，共8个QUEST01已有TYPE，0新增原脚本。保留两轮原PET/DelPet/EVDEL语法、GetPet93/341与WORLD21既有模板171/274的来源联接；最重要是同载体脚本将道具2607视为收集证明，但两原94栏itemset的2607均名为“火難的戒指”，未确定具体版本/加载原因，不能擅自统一。floor100四整数为CREATE范围、现955 DAT目录无匹配，未假造地图。私人商业正文和跨源原图仅入个人Library并复取验SHA/CRC；公开仅[数字与散列证据](research/recovered/STONEAGE-QUEST30-DINOSAUR-COLLECTOR-EVENT35-SOURCE-R1.json)、可选原件再读工具及11项派生回归。原客户端/宠物领奖未运行，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null；**最高NEXT QUEST31** 先全任务缺口审查，若缺来源就绪新增批次则转跨模块内容整合，不继续累加任务编号。


## 2026-11-08 — QUEST31｜四地NPC事件9—12与保护石／风琴关系来源

[QUEST31 四地点原NPC与旧脚本交叉整合](docs/continuity/STONEAGE-QUEST31-FOUR-VILLAGE-EVENT09-12-SOURCE-20261108.md)：从本次新核的主线继续，对原QUEST01全295脚本／1349旧段／14目录查重；本批4份脚本、18个TYPE、4 CREATE和6源道具ID／12原物品行与6个TW1跨来源候选PNG核验。事件12保护石2419/2420、事件10/11的独立逗号旗标10,12／11,12、事件9凭10/11/12结束条件奖励1357、事件12的41／42与2736风琴条件保持原字面。三处floor已有MAP09旧DAT证据，floor1300在955就绪目录缺件，不伪造世界地图或原运行次序。原NPC/原行/原图只入私人Library且已独立SHA/CRC回读；公开只有[来源数字与SHA](research/recovered/STONEAGE-QUEST31-FOUR-VILLAGE-EVENT09-12-SOURCE-R1.json)、原件再读工具、13派生回归、专题工作流。没有新增原脚本或原生执行证明。CURRENT历史blob c89e0e33537990aa2132b47c40fef49a985a935c不改；Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、整体百分比未知。最高NEXT QUEST32先检任务模块是否已达来源止点，必要时转跨模块关系整合，不继续为数量增加任务编号。


QUEST31 [正式出版验收](research/recovered/STONEAGE-QUEST31-PUBLICATION-ACCEPTANCE-R1.json)：PR #271 已合并，最终候选14/14与内容主线11/11 Actions成功；复合EndSetFlg12未纳入旧纯整数目录的反例已补13项测试。私人原件不入公开Git，当前主线历史CURRENT完全不改，最高NEXT QUEST32进行任务模块阶段止点及跨模块审查。


## 2026-11-08 — QUEST32 任务源脚本覆盖审计与有界收口

[QUEST32 24份专项源脚本查重与保留缺口](docs/continuity/STONEAGE-QUEST32-MODULE-DEDUPE-AUDIT-20261108.md)使用同一后期社区混合源的QUEST01原295份CREATE引用脚本/1349 TYPE段及QUEST08–31全部24份公开派生报告，逐原脚本路径+完整源SHA核对：236次所选原脚本记录，235不同路径，233份与旧QUEST01目录同路径同SHA；QUEST10有2份未被旧CREATE引用目录收录的原保存变体，QUEST10/29共享king/event69_1同SHA，不能增加新发现计数。原295目录仍有62份未进入这24专项选集（不等于原件缺失或没有任务价值）。公开[重算工具](tools/stoneage_quest32_module_audit.py)、[守恒快照](research/recovered/STONEAGE-QUEST32-MODULE-DEDUPE-AUDIT-R1.json)及专项测试；私人原版权源不上传，原CURRENT巨型历史blob c89e0e33537990aa2132b47c40fef49a985a935c原样。任务模块SOURCE_BOUNDED_PARTIAL，不称早期官方同版或原生可玩，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总体percent=null；最高NEXT INTEGRATION06跨NPC/地图/物品/宠物真实关系复核。CI/合并后验另据GitHub事实补证。


## 2026-11-08 — INTEGRATION06｜地图1300来源读取缺口与六原NPC创建点

[INTEGRATION06原1300.MAP/DAT资格及跨任务关系](docs/continuity/STONEAGE-INTEGRATION06-MAP1300-QUALIFICATION-20261108.md)：新联合复核已公开 MAP01/QUEST05/QUEST19/25/27/31 六份SHA固定派生证据。同一保存RAR中1300.MAP组0/1各20008B、整SHA一致、100×100头信息候选；1300.DAT原RAR目录记60008B，但旧 libarchive 原“File CRC error”、实际读取0B，不能把“本955已验DAT无匹配”认作“原游戏没有地图”，也不能从MAP补造DAT。QUEST05六条创建：QUEST19寄信、QUEST25环岛检查站、QUEST27斧头感谢函、QUEST31事件9–12四条ExChangeMan源关联以及两条QUEST03 Timeman共享参数；六是配置，不是游戏实际NPC人口。公开[来源索引](research/recovered/STONEAGE-INTEGRATION06-MAP1300-MAP-DAT-SIX-CREATE-SOURCE-R1.json)及5项重算测试，不增原像素、原脚本、原程序运行或早期官方身份证。CURRENT历史blob c89e0e33537990aa2132b47c40fef49a985a935c完整不变；Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、完成率未知。**NEXT Stage A跨模块材料缺口审阅**；正式验收以CI后验为准。


## 2026-11-08 — INTEGRATION07｜14份未匹配DAT楼层的真实来源分类与大小写漏项

[INTEGRATION07全部14楼层、88原CREATE源数与MAP/DAT资格](docs/continuity/STONEAGE-INTEGRATION07-14-MISSING-DAT-QUALIFICATION-20261108.md)：复用QUEST05、MAP01、MAP02及INTEGRATION06已发表源SHA目录，实际查得QUEST05对955原DAT缺匹配的14层/88配置可细分为：1000独立已验完整DAT（19创建）、12层有原DAT目录及原解包失败（67创建）、830本选定来源无MAP/DAT成员（2创建）。**200.dat／3000.dat原错误名小写**，遗漏大小写会错判无记录；400.MAP两组完整原字节SHA不同，不可合并同图；13个原DAT错误长度与MAP成员尺寸公式相合不是成功解码。公开[来源守恒索引](research/recovered/STONEAGE-INTEGRATION07-FOURTEEN-UNMATCHED-DAT-QUALIFICATION-R1.json)、10项回归，不新取原DAT或启动原程序，不补造地图。原CURRENT全文保留，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、整体完成率未知。最高NEXT Stage A代表性玩家路径跨模块联合审查；CI合并后验另记。


## 2026-11-08 — INTEGRATION08｜源地图1000和19配置原内容严格联接

[INTEGRATION08 同源160×160原DAT与19个NPC/任务创建块](docs/continuity/STONEAGE-INTEGRATION08-FLOOR1000-NPC-SOURCE-20261108.md)：把MAP02独立已核1000.DAT 153608B/SHA94b19cb…，与QUEST05/CHAR01同混合2.5保存来源的19创建配置逐原路径+序号+适当SHA作用域严谨连接：7条changeevent、2条warp、10条timeman，17个有`borncorner`原四整数（且在尺寸界内）、1条仅`borncenter`、1条无两字段；18个不同图别名不是18个NPC。连通QUEST25三条环岛/检查站配置、QUEST26一条贝壳/花交换及INTEGRATION05原GetPet命令（非已获宠物）；TW1原RD 26310/26324只是跨载体数字候选、14次未命中。本轮没有重新解商业原文件、没有本地原游戏NPC运行、没有官方同服证明。公开[可核19行](research/recovered/STONEAGE-INTEGRATION08-FLOOR1000-19-CREATE-ORIGINAL-SOURCE-R1.json)和9项来源测试；历史CURRENT原blob完整保留，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停，percent未知。最高NEXT Stage A代表性玩家路径可证/缺口联合审查。


## 2026-11-08 — INTEGRATION09｜有据玩家内容链与原生可玩缺口

[INTEGRATION09 1001⇄1000双向传送原块、邻近NPC及任务/宠物关系的来源审查](docs/continuity/STONEAGE-INTEGRATION09-REPRESENTATIVE-PLAYER-CONTENT-CHAIN-20261108.md)：复用同一受限mixed25存档和此前已出版SCENE15/22、INTEGRATION08、QUEST25/26、INTEGRATION06/07派生原证，1001(10,15)↔1000(63,99)源传送关系、1000(63,103)村民原提示输入（仅坐标差0,+4）及1000上C/D环岛/2414-2415交换/原GetPet字面组成**静态原始内容网络**；不能称实际可走、触发、通关或宠物领取。特别核出SCENE22村民不属于INTEGRATION08的19条QUEST05特殊CREATE样本，不以19算总人口。1300有原MAP和6条CREATE但DAT仍为原CRC读错。公开[逐来源SHA索引](research/recovered/STONEAGE-INTEGRATION09-REPRESENTATIVE-PLAYER-CONTENT-CHAIN-R1.json)与8项静态反例测试；其中原C线第2/9站floor1100/1300、D线5站floor100共7个检查站DAT源成员读取失败，不能据此断言原路线可行或文件不存在；CURRENT `c89e0e33537990aa2132b47c40fef49a985a935c` 全历史不动、原资产不入Git。Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null。NEXT选择有**新合格原实物及真实玩家内容增量**的跨域缺口，不延伸虚构步行路线或网服。


## 2026-11-09 — INTEGRATION10｜十二份失读原DAT实际补回与七检查站场景

[INTEGRATION10原件恢复、七窗与接力](docs/continuity/STONEAGE-INTEGRATION10-TWELVE-DAT-SEVEN-SCENES-20261109.md)：实际重验已保存361255180B mixed25原RAR，从12条旧失读成员完整提取16,497,180B、2,749,514原格，逐原头CRC/成员CRC/新SHA通过。1300与1100等地图现在有真DAT；QUEST05既有67条CREATE可联接原图，原830两配置仍缺本选源DAT。保留MAP01旧63次失败，不称全部解决；旧捕获报告已有7层同SHA，不当新发现12地图。实际用279旧原图候选构成C2/C9/D1/D2/D5/D7/D12七处11×11来源场景，819引用无缺图，NumPy独立复算21完整画布全部同。314成员私人源/图包和联系图已保存，原商业素材不入Git。公开仅[来源数值/散列](research/recovered/STONEAGE-INTEGRATION10-TWELVE-RECOVERED-DAT-SEVEN-CHECKPOINT-SCENES-R1.json)、工具与9项专项，75项相关本地测试成功；出版CI须真实后验。CURRENT原blob c89e0e33537990aa2132b47c40fef49a985a935c完整不改，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总体百分比未知。最高NEXT复用新DAT对1300六CREATE及出入口做有据内容联接，先核图像覆盖，不冒充原生可玩路线。

## 2026-11-09 — INTEGRATION11｜霍特爾 1300 原图、创建配置与双侧传送端点

完成 1300 全图候选。补齐 20 个台湾 1.0 原 RD 别名对应的 43 次引用，全图 6,192 次候选绘制有原图。六条原 CREATE 落在五个坐标，两个时钟块同格，另保留寄信与普通对话配置的同格关系。46 条传送表记录与直接 CREATE 一一吻合，双方格值已核八张相连原 DAT。原生触发、碰撞及历史同部署仍待证。下一包优先核 1306、1310 房间来源与门点。见[本轮接续](docs/continuity/STONEAGE-INTEGRATION11-FLOOR1300-SOURCE-SCENE-20261109.md)。

## 2026-11-09 — INTEGRATION12｜霍特爾两间室内有据场景

用已保管的原源资料复核 1306「霍特爾的長老家」与 1310「營養劑名人的家」两间地图、9 条原 CREATE 与 10 条双端传送记录；私人图像候选合计 393 绘制引用无缺源。公开保留原服务器两层与客户端 DAT 差值，以及 1310 商店主物品表缺 21 ID、备用表有 21 ID 的冲突。原生门点行为、商店实际买卖及初版归属仍未证明。见[INTEGRATION12 证据与 NEXT](docs/continuity/STONEAGE-INTEGRATION12-HOTORU-TWO-ROOMS-20261109.md)。

## 2026-11-09 — INTEGRATION13｜霍特爾五間室內原房名、門點與 NPC 配置

[INTEGRATION13 原資料與下一步](docs/continuity/STONEAGE-INTEGRATION13-HOTORU-FIVE-ROOMS-20261109.md)核對 1301–1305 五張原 DAT/LS2MAP、29 條原 CREATE 和 20 條雙端傳送記錄。沿用 MAP07 已驗的五張候選底圖，私人頁加入 28 個配置座標標記。1302 同格的兩份配置分列，1304 保留物件層 60 格差值，1305 醫療參數保留原數字串。原生載入、互動與官方同部署仍待證。下一項查霍特爾商店參數與物品表的實際差異。

## 2026-11-09 — INTEGRATION14｜霍特爾医院与营养剂商人的物品来源

[INTEGRATION14 原配置、备表与图像证据](docs/continuity/STONEAGE-INTEGRATION14-HOTORU-SHOP-ITEM-SOURCE-20261109.md)串起两处原创建块、三种原参数字段和七条备表原行。医院七个编号只出现在其 `LimitItemNo`，其中五个也在营养剂名人家的 `ItemList` 中。图像记录按载体和原压缩块来源分列，原生加载与实际交易仍待证。
## 2026-11-09 — INTEGRATION15-R1｜霍特爾寵物店 1303 原服務資料現場關聯（PARTIAL）

[INTEGRATION15 來源與續接界限](docs/continuity/STONEAGE-INTEGRATION15-HOTORU-PET-SERVICE-BRIDGE-20261109.md)以 INTEGRATION13 原場景座標與 GAMEPLAY03／05 原參數全 SHA 核對 1303 寵物寄放和七項技能候選，明確分開與技能導師同圖號的 TownPeople。新原 RD 解碼和私人現場 HTML 實際修改均為零；下一步只在能取回私人觀察與合格原像素時才做 R2，原生互動與官方同部署維持未證。
## 2026-11-09 — INTEGRATION15-R2｜霍特爾宠物店 1303 原图候选与服务资料合并观察

[INTEGRATION15-R2 私人实物交付与来源边界](docs/continuity/STONEAGE-INTEGRATION15-R2-HOTORU-PET-SOURCE-VISUAL-20261109.md)：实际回读 INTEGRATION13 与 WORLD11 私人 ZIP，按已验 PNG/RGBA/RD 哈希将 16048、16049 两张静态原图候选关联到 1303 的三条独立 CREATE 与原参数，保留五间房原底图、人物共享图号但不同 NPC 的关系。私人离线页新增显式可关叠图、三个可点资料卡及原 CP950 参数；现代叠图不代表原客户端实际呈现。浏览器只能用内存测试副本（文件/localhost 导航被禁），原生交易/技能/人物层序/官方同部署均未证；私人包已存档并回读 SHA 验收。

## 2026-11-09 — INTEGRATION16｜柯奧、柯爾克與瑪麗娜絲三間寵物店

[INTEGRATION16 來源、離線觀察與續接](docs/continuity/STONEAGE-INTEGRATION16-THREE-PET-ROOMS-20261109.md)把 1103／1203／2003 的原房名、六筆寵物店／技能教學配置、五個有原 RD 證據的靜態造型和十二筆傳送原行接到三張已驗底圖。造型 16046 在兩房分屬不同服務，兩筆 CREATE 獨立。下一優先 INTEGRATION17 核 1403／3103／3203 的同類關係，以取得原 DAT、底圖和確切 RD 字節為條件。

## 2026-11-09 — INTEGRATION17｜卡坦、塔姆塔姆與多多三間寵物店

[INTEGRATION17 來源與續接](docs/continuity/STONEAGE-INTEGRATION17-THREE-PET-ROOMS-20261109.md)接上 1403／3103／3203 的六處服務、六個原靜態造型與十一條原傳送方向。塔姆塔姆的額外出店方向由 mapwarp 與原 Warp CREATE 互證。另從原混合 2.5 REAL 實讀、解碼 16122／16127 兩個解說員 RD，四間候選底圖已復驗。下一優先 INTEGRATION18／SCENE26-R4 接入四間解說員房。

## 2026-11-09 — INTEGRATION18 / SCENE26-R4｜四間寵物常識解說員房與原造型來源界限

[INTEGRATION18 四房來源限定續接](docs/continuity/STONEAGE-INTEGRATION18-SCENE26-R4-SOURCE-BOUNDED-20261109.md)重新核四筆原 CREATE、`petmaster` 原 CP950 教學內容、四份 MAP09 原 DAT 與 16122／16127 兩個已驗 RD 像素指紋；私人候選觀察頁實際有四處原圖尺寸的**空心佔位框**和十項原文，**尚未放入這兩張原人物圖**。最新可取私人包沒有其真 PNG/RD 字節；在兩件均經原 SHA/尺寸/像素核驗前不冒稱原人物已顯示。私人有限包在本會話生成（14 件、完整 CRC 與本地重演）、已成功持久上傳個人 Library 並獨立回讀全 ZIP SHA / CRC；Chromium 僅內存載入測試，直接 file URL 被環境攔截。公開原數據接點與反例測試另存 [來源限定收據](research/recovered/STONEAGE-INTEGRATION18-SCENE26-R4-BOUNDED-TUTOR-LAYOUT-R1.json)。歷史 CURRENT 原 blob 保持不變，Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暫停、全體百分比未知。下一輪有來源的 3303／3403／4003 寵物服務可先整合；R4 原像素只在兩份真圖源齊全時重開，不進新引擎或網服。


## 2026-11-09 — INTEGRATION19｜三間寵物店原服務、11 條有向門點與 4003 原圖候選

[INTEGRATION19 來源限定復核、私人實物與 NEXT](docs/continuity/STONEAGE-INTEGRATION19-THREE-PET-SERVICES-20261109.md)：重新取原私人包並驗 SHA/CRC，核 3303／3403／4003 的六條原 CREATE、六份 CP950 參數、十一條原 mapwarp 與獨立 Warp CREATE。3303 (16,20) → 3300 (51,60) 有原單向出店記錄、未列該格反向；4003 原 PetShop 有 `pool_flg=1`／`pool_cost=200`，原運行費率未證。4003 真原 DAT 兩服務格、解說員格及兩門點三平面 u16 重核，1889×1425 來源限定候選圖重新驗 RGBA；原 16033 靜態像素只作 3403 單獨資料卡，不冒充其房內原造型。3303／3403 原 DAT／完整底圖本輪只有先前 MAP09 來源指紋，未取回私人原字節，故不造場景。新 16 成員私人 ZIP 兩次逐字節同、CRC 全通，已存個人 Library 再回讀全 SHA；本環境無可啟動 Chromium，沒有真瀏覽器驗收。公開只存[派生數值與原來源資格](research/recovered/STONEAGE-INTEGRATION19-THREE-PET-SERVICES-SOURCE-R1.json)及回歸測試，所有原商素材留私人。CURRENT 完整 2,709,173 B 原 Git blob 未改；Stage A 7PARTIAL+2OPEN、Stage B/wiki GATED、R79 暫停、overall_percent=null。下一次有來源的 3303／3403 DAT、室外 3400 及其餘人物原圖補件才重開本批；否則轉下一有新實物的原版內容。


## 2026-11-09 — INTEGRATION20｜烏魯力、奇喀喀寵物店真 DAT 與室內候選圖補回

[INTEGRATION20 原件、合成驗收與 3400 有界缺口](docs/continuity/STONEAGE-INTEGRATION20-TWO-PET-ROOMS-20261109.md)：重新從個人 Library 取回 46,844,444B MAP09 原圖與 955 DAT 包及 361,255,180B 原 mixed25 RAR，整源 SHA、4195 ZIP CRC 均核。原 3303／3403 DAT 及 LS2MAP 真字節已取回，兩房 30×30 原兩層的 101／162 次原圖候選位置、各三幅 1889×1425 畫布用 Pillow/NumPy 獨立逐像素完全吻合 MAP09 舊原源 SHA；保留服務端第二層 256／32 格不同，非已證碰撞。**四筆** PetShop／PetSkillShop CREATE 和七條有向 Warp 原行，3303 另有未列反向的出店方向，均按原三平面格值核實。3403 真原靜態圖 16033 在私人候選場景可選叠圖，其他缺圖不造。原 3400.DAT 在 RAR 有條目但未成功可靠解出；獨立成功的單平面 3400.MAP 不冒充三平面 DAT。私人 101 成員 ZIP 2,585,668B 已存個人 Library 並重新回讀 SHA/CRC；Chromium 僅以原 PNG 字節內存開啟驗候選交互，file:// 被環境阻斷。公開只存[來源限定數值/哈希](research/recovered/STONEAGE-INTEGRATION20-TWO-PET-ROOMS-ORIGINAL-SOURCE-R1.json)與反例測試，不發原商業字節；原史 CURRENT blob 完全保留，Stage A 7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79 暫停、overall_percent=null。下一項只在可驗真 3400 完整 DAT 或 NPC 原 RD 時重開本批，否則轉下一有來源材料的 Stage A 內容。

## 2026-11-09 — INTEGRATION21｜十間原寵物店的跨房間服務與方向目錄

[INTEGRATION21 真來源與缺件止點](docs/continuity/STONEAGE-INTEGRATION21-TEN-PET-ROOMS-ATLAS-20261109.md)：重新逐 Git blob 交叉核 INTEGRATION13／15／16／17／19／20 六份已驗證源索引，10 個原 DAT 房間、10 PetShop＋10 PetSkillShop CREATE、38 條有向 mapwarp 原記錄、36 明確雙向記錄與兩條僅單向（3103→3100、3303→3300）進入可查的跨室內 [原 SHA／原 ID 合同目錄](research/recovered/STONEAGE-INTEGRATION21-TEN-PET-ROOMS-SOURCE-ATLAS-R1.json)；16033、16035、16046 同圖號各有不同 CREATE，不合併原 NPC。私人 INTEGRATION20 原 ZIP 整 SHA 核對後實讀獨立 3400.MAP 單平面，`(53,49)`／`(54,49)` 在**明列的行優先小端假設**下 u16 均 0；此並非已驗 3400 三平面 DAT，也不證原碰撞或可進門。公開無商業原像素，CI 僅重播來源數字／SHA／反例。歷史 CURRENT 2,709,173 B 原 blob `c89e0e33537990aa2132b47c40fef49a985a935c` 不改；Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79 暫停、總完成率未知。**最高NEXT：** 按模組來源輪換下一份有新增原材料的 Stage A 可見內容；僅有新合格 3400.DAT、NPC RD 才重開本店，不重畫舊背景或捏造原世界操作。

## 2026-11-09 — INTEGRATION22｜三村六間原商店、十份 CREATE 與 108 明列商品

[INTEGRATION22 六房十店／真原件與缺口](docs/continuity/STONEAGE-INTEGRATION22-THREE-VILLAGE-SHOPS-20261109.md)：從已存 361,255,180 B mixed25 原 RAR 實取十份 CP950 原參數與六份 3644 B LS2MAP，連已驗 MAP09 955 原 DAT、ITEM01 原雙物品表／原圖候選及 INTEGRATION17 真 CREATE/mapwarp；六張 30×30 原三平面 DAT 的 125 個候選原圖塊各自真像素，以 Pillow／NumPy 重建六幅 1889×1425 場景並逐 RGBA 完整 SHA 匹配 MAP09。三村六房十個獨立 ItemShop CREATE，有原 LimitItemType 分 3 OFFENCE／3 DEFENCE／3 ACCESSORY；額外柯奧 1102 (14,14)「素材屋」空類型但兩段 11960-11967,11970-11977 原範圍。九一般商店 **108 個原明列 ItemList 項次**，素材屋兩來源範圍若閉區間展開有 **16 個未驗 native 的候選**；124 個對照項次在兩份原 mixed25 物品表源行 SHA 一致，120 個不同 ID、89 來源限定 TW1.0 原圖候選號，絕不把跨載體圖像冒認原服實際賣貨。原 mapwarp 合共 23 有向記錄、22 條有顯式反向、1101 (16,21) →1100 (52,72) 一條無明列逆向；六房 DAT 格已真核，1200／2000 原室外 DAT 具文件，**1100 外端 DAT 於本次955來源缺件**保留 null。不宣稱原生碰撞、交易、真正原版遊戲操作或早期官方版本同服。私人觀察 ZIP 6,134,890 B／SHA 12239bcab57215586fe4ca755a9503900daaa91be7abdecb6e21621db9d6b92d 共131成員，已存個人 Library 並獨立重讀整 SHA/CRC；公開只有[來源派生索引](research/recovered/STONEAGE-INTEGRATION22-THREE-VILLAGE-TEN-SHOPS-SOURCE-R1.json)、精確反例測試與日期覆層，原圖／原文／DAT不入Git。docs/CURRENT-STATE.md 原 2,709,173 B blob c89e0e33537990aa2132b47c40fef49a985a935c 完全不改，Stage A 7 PARTIAL+2 OPEN、B/wiki GATED、R79暫停、overall_percent=null。**最高NEXT** 依模組順序轉其它未整合且有實物的原版內容；僅取得驗實 1100 三平面 DAT 或解說員真 RD 才回補缺口，不重造新引擎與網服。

## 2026-11-09 — INTEGRATION23｜薩姆吉爾、霍特爾、卡坦三村六間原商店

[INTEGRATION23 三村十一店原來源及下步](docs/continuity/STONEAGE-INTEGRATION23-THREE-VILLAGE-SHOPS-20261109.md)：從最新遠端 main 06351789（tree 3fed55a，原 CURRENT c89e0e3 保持完整 2,709,173 B）啟動，原 mixed25 361,255,180B RAR 真實解回 6 份 3,644B LS2MAP／11 份 CP950 商店參數並核 RAR 原 CRC/SHA，與原 shop_m.create 的 11 CREATE、MAP09 六張 30×30 原 DAT、ITEM01 兩原 itemset 主表和台灣 1.0 原圖候選分來源關聯。薩姆吉爾1001/1002、霍特爾1301/1302、卡坦1401/1402 原**九一般店明列 109 ItemList 位置**，分 3 OFFENCE／3 DEFENCE／3 ACCESSORY；兩個素材屋各含 2 個原字面範圍、按閉區間只是 32 候選，合 141 物品表對照／139 不同 ID、94 不同跨版圖號。霍特爾道具屋原 `LimitItemNo=2421`、六個 ItemList 卻沒有 2421，另有同來源物品原行 SHA；不推定原版限賣或實際購買。六份 DAT 的 104 不同原圖塊候選重新繪出 6 個 1889×1425 畫布，Pillow/NumPy 逐整幅 RGBA 完全同 MAP09 原 SHA；LS2MAP 第二層差格分別 4/30/0/0/34/1，不把原值 2 直接解為碰撞。26 條有向 mapwarp 原行，24 有明列逆向，另兩條 1000→1001/1002 無精確逆向；1000／1300 室外 DAT 在所選 955 原 DAT 中缺件（null），1400 DAT 成功復核，不虛構路線。私有 136 成員 ZIP 5,219,008B／SHA `7cab6cf75184331c4f09a7525c0081956b21c641a1ec487b0ec93b4e4d49c4b0` 已入個人 Library 並重新下載全 SHA/CRC 同；原商業圖／DAT／原文本不入 Git。公開[來源哈希數值索引](research/recovered/STONEAGE-INTEGRATION23-THREE-VILLAGE-ELEVEN-SHOPS-SOURCE-R1.json)＋負例測試／Action 僅派生重播；沒有原生買賣、角色走動／完整原遊戲客戶端或官方跨版同服證明。Stage A 仍 7PARTIAL+2OPEN，B/wiki GATED，R79暫停，總進度未知。最高 NEXT 擇下一份尚未接入的真原材料（如市場食物／藥／素材 NPC、任務），不重畫同六房也不進網服或新遊戲。

## 2026-11-09 — INTEGRATION24｜五村原藥師、十二種明列藥品與原圖來源關聯

[INTEGRATION24 五間原藥劑商店／藥品與地圖有界來源](docs/continuity/STONEAGE-INTEGRATION24-FIVE-MEDICINE-SHOPS-20261109.md)：從主線 `b4bf4337471b37c1d2e500cbb79bf1ff575d8c8d` 與完整原 CURRENT blob `c89e0e33537990aa2132b47c40fef49a985a935c` 續接，實取私人 CHAR01 2205 原 NPC ZIP（995176B/SHA `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`）和 ITEM01 838 原物品／候選原圖 ZIP（5868386B/SHA `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa`），兩份整包SHA及逐成員CRC重新通過。五份 CP950 原藥師參數與 `shop_m.create` CREATE 精確核 SHA，五村 floor1005/1105/1205/1305/1405 共五個 source ItemShop，每個明列12個相同藥品ID，合計**60個明列項次／12不同 ID**；原 `buy_rate` 字串依次1.0/1.1/1.5/1.3/1.4，`sell_rate=0.2`，`LimitItemNo=1500-1550` 為原範圍字串、**不視作另外39種實際上架**。12個物品在同保存載體兩原 itemset 行SHA相同；來自不同版本零售TW1的來源限定原圖候選僅11別名，1530/1531不同物品共用23021。既驗 MAP09 五原 DAT/畫布SHA只作原來源索引連結，本輪不重讀DAT、不重繪像素。公開[帶哈希原配置關聯索引](research/recovered/STONEAGE-INTEGRATION24-FIVE-VILLAGE-MEDICINE-SHOPS-SOURCE-R1.json)、負例測試與專項CI，原商業文本/圖/DAT/RD仍私人；原商店買賣、原計價、物品使用、同版官方部署及原生畫面/碰撞全部未驗。最高NEXT選下一組已有原件且未重複的食物／肉／市場商店或任務NPC，不造新引擎、聯網或虛構原玩法。Stage A 7PARTIAL+2OPEN、B/wiki GATED、R79暫停、overall_percent=null；合併／Actions須由實際後驗另記。

## 2026-11-09 — INTEGRATION25｜原第2009市場七店：肉、魚、蔬菜、水果、米、地方特產

[INTEGRATION25 七市場店原實物關聯、33字面 ID 與37原區間](docs/continuity/STONEAGE-INTEGRATION25-MARKET-SEVEN-SHOPS-20261109.md)：從最新遠端 main `675e70b942df3b8f695e837d6bf5c47b292bdc01`／tree `e055bf1b55eb2a632611df6336810a6cfc34c6c3` 續接；整份 CURRENT Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`、2,709,173B 全保留。本輪真實重讀私人 CHAR01 原 NPC 2205 成員 ZIP 整 SHA/CRC 和 ITEM01 原兩表／候選原圖 838 成員 ZIP 整 SHA/CRC，核真 `shop_m.create` 七獨立 CREATE 與七份 CP950 參數 SHA；排除另外兩個不同 `mission.create` 原商店引用。第2009號地圖已有 MAP09 真原 40×60／14,408B DAT SHA 及完整候選畫布 SHA，本輪僅引用、不虛報重新解碼。七商店有 **33個原文逐字面 ID、37個原區間字串（若含端點展開149個數值候選）**；是182次來源明列／推導出現、**181個不同 ID**，唯一重合12221在一店為區間候選、另一店為原明列單 ID，兩類證據不混同。所有181 ID 在同保存載體兩份原 itemset 全行SHA相同；**169項**具先前真正解碼的台灣1.0零售原RD候選（88別名），另12 ID `12218-12229` 在該零售索引缺位置（3圖號24552/24553/24560），均不代表同官方部署。地方特產NPC原 `buy_rate=4.0` 只是原欄字串，不證原生加價公式；`LimitItemNo` 額外範圍不能充當實售庫存。公開[181物品和七份原來源關聯索引](research/recovered/STONEAGE-INTEGRATION25-ORIGINAL-2009-MARKET-SEVEN-SHOPS-SOURCE-R1.json)及正反測試、專項 CI，原 NPC 原文、原商業圖、RD/DAT原件不入Git。原版買賣、物品效果、真正NPC/地圖呈現及原生運行未驗；Stage A 7PARTIAL＋2OPEN、Stage B/wiki GATED、R79暫停、總體完成比例null。NEXT依來源先選另一組未完整接入的原市場／任務NPC或模組；禁止無證交易引擎、重畫同七房或新聯網。

## 2026-11-09 — INTEGRATION26｜原市場12種台灣1.0索引缺圖回接同源mixed25真RD像素

[INTEGRATION26 十二物品三份真原RD像素來源、使命索引查重止點](docs/continuity/STONEAGE-INTEGRATION26-2009-MARKET-ORIGINAL-MIXED25-PIXEL-BRIDGE-20261109.md)：從遠端主線 `65444b93df5f92ddffb5915883848cc516d25dd7` 起，先查已驗市場 I25 181項與 ITEM06 後期保存混合2.5的415原RD，**本輪並非新解碼415張**；已存私人 ITEM06 HTML 1,242,805B/SHA `ff901220af1484a3367ef52014fe561b25bd6ee9d270b4b6d3fb220ff1f8a700` 真重新全檔 SHA 核驗，實際擷取三份私人嵌入 PNG（尺寸32×33/32×28/36×36、全PNG SHA逐份合已驗 ITEM06）對應原別名 **24552／24553／24560**；精確源同載體關聯 I25 已有12個零售TW1 `INDEX_NOT_FOUND` 的物品 ID12218–12229，保留它們在七原市場配置的13個明列／區間候選出現（12221雙出現不可合併）。因此本來源審核範圍181原物品ID中：169各有**不同載體TW1原圖候選**，餘12有**後期mixed25同保存來源原RD候選**，合181件各有至少一份有源資格的原像素候選；不代表181張不同圖、同版官方部署、原生選圖、真商店庫存或交易。公開[十二件精確來源索引](research/recovered/STONEAGE-INTEGRATION26-MARKET-12-MIXED25-ORIGINAL-PIXEL-BRIDGE-R1.json)及反例/CI，原圖／HTML／RD不入Git；原完整 CURRENT blob `c89e0e33537990aa2132b47c40fef49a985a935c` 未動。**查重更正NEXT：O70早有47原委託、O74早有23售書和 NPC 圖，不能再重做 mission.create 當新成果**；按模組來源審核後轉真正未整合的原遊戲內容。Stage A 7PARTIAL+2OPEN、B/wiki GATED、R79暫停、percent=null；本PR與Action驗收須待遠端後驗確認。

## 2026-11-09 — INTEGRATION27｜四间宠物解说员原图与奇喀喀室外门点

[四房原图及 3400.DAT 来源续接](docs/continuity/STONEAGE-INTEGRATION27-PET-TUTORS-AND-3400-DAT-20261109.md)：同保存混合 2.5 原 RAR 取回 16122／16127 两份原 RD，ADRN、RD、索引、RGBA 与 PNG 全 SHA 对上 INTEGRATION17。四条独立 CREATE 接入 1003／2003／3003／4003 的已验底图，原图候选和十条原文可离线查阅。另成功取得 86,408 B、120×120 的 3400 三平面原 DAT，核对两组门格和四条明列往返配置。公开[来源收据](research/recovered/STONEAGE-INTEGRATION27-PET-TUTORS-AND-3400-DAT-SOURCE-R1.json)保留原件散列与执行边界。历史 CURRENT 原 blob 完整保留。下一步转尚未整合且有原件的 Stage A 内容，原生绘制、教学和传送运行待证。

## 2026-11-09 — INTEGRATION28｜奇喀喀全村与宠物店门内外

[全村来源及门点验收](docs/continuity/STONEAGE-INTEGRATION28-QIKAKA-VILLAGE-SCENES-20261109.md)：3400 的 12×11 门外窗口接 3403 室内，两组原门点可点选对照。全村 120×120 原 DAT 的 6,461 次候选放置所需 329 个图号均有源，321 个复用 TW1 图块逐块与 mixed25 原 RD 同哈希，另 8 个重新从原 RD 双解码。33 条涉及 3400 的有向原配置与 Warp CREATE 完全相合，核齐八个楼层的两端 DAT 三平面值。历史 CURRENT 原 blob 完整保留。下一步接 3406 村长家与 QUEST15 的两条 event20 原 CREATE。

## 2026-11-10 — INTEGRATION29｜奇喀喀村长家、吉德与 event20

[门内外及原脚本来源](docs/continuity/STONEAGE-INTEGRATION29-QIKAKA-CHIEF-HOUSE-EVENT20-20261110.md)：3406 村长家底图和 3400 门外候选接上三条原门点、吉德三处人物位置与三份 event20 脚本的 14 段原文。村外 16030 从同保存载体原 RD 双解码。保留 3406 (10,16) 的额外单向出口及原运行边界。下一项接 20607／20608 的三处地下城配置，已预检原 DAT、脚本和图号命名空间。


## 2026-11-10 — INTEGRATION30｜原 event20 地下城 20607／20608

[有界来源与续接](docs/continuity/STONEAGE-INTEGRATION30-EVENT20-DUNGEON-20261110.md)：两张原三平面 DAT 地下城场景、三处 NPC CREATE、三份 CP950 原脚本共14段、16029／16032 原静态图、100431 原 SPR 明确候选图和 11 条原有向门点已联接；同一原格 20607(75,13) 明列两种不同出口，不能混合。私人原件 ZIP 6,980,092 B／28 CRC／SHA 811139ca9f78ccf20a90d05c5e0535ace34a4be7600f8e0efd9335f3e774441b 已独立读取核验；公共仓库仅[派生数字/来源收据](research/recovered/STONEAGE-INTEGRATION30-EVENT20-DUNGEON-SOURCE-R1.json)与回归，历史 CURRENT 原 blob 完整保留。不宣称原版游戏原生执行、触发和同早期官方部署。Stage A 7PARTIAL+2OPEN、Stage B/wiki GATED、R79暂停、overall_percent=null。下一优先复核 20606 入口源是否尚有真材料增量。


## 2026-11-10 — INTEGRATION31｜20606 条件 NPC 实际配置与 20607 地下城入口

[入口有界来源及纠错](docs/continuity/STONEAGE-INTEGRATION31-DUNGEON-WARPMAN-ENTRY-20261110.md)：私人 CHAR01 同源 `20600npc.create` 第25块 20606 (9,23)「山賊守衛」引用96字节原 `wpm_20606_9_23`，字面 `WARP:20607,7,5`、`FREE:LV>0`；原普通 mapwarp 2307 则独立为20607(7,5)→20606(8,23)，2,981行普通 mapwarp 不存在20606→20607对应方向。两个机制不能混写成双向普通传送。两原 DAT 三平面实读、CHAR01私人ZIP 995,176B／2205 CRC和 SHA均核；原素材原对白不进Git。公共[数值哈希证据](research/recovered/STONEAGE-INTEGRATION31-DUNGEON-WARPMAN-ENTRY-SOURCE-R1.json)及反例测试重用 I30 CI。未执行原游戏，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总进度未知。此局部止点后转下一项新的已获原内容，不为缺失原生触发制造推论。


## 2026-11-10 — INTEGRATION32｜奇喀喀四间原房的服务 NPC 与宠物事件

[四房原资料和有界下项](docs/continuity/STONEAGE-INTEGRATION32-QIKAKA-FOUR-ROOMS-20261110.md)：从新核远端 `47732f7eed74b5581941c8ced712005dbea78248` 出发，私人 I28/CHAR01/ITEM01 三包分别 373/2,205/838 CRC 与整 SHA 重新核实。原楼层3404肉店、3405医院、3409便利商店、3412民家四份 DAT/LS2MAP 复核既有 MAP09 与 I28 原记录，16条普通有向门点来源哈希不变；**新增** 7 原 `shop_m2.create` NPC 服务配置、1民家 `kikukuev.create`／4段走失宠物事件、46个商店明确 ID、16个肉店范围定义候选与6个任务道具ID，合68不同原物品定义，独立TW1零售像素只作跨载体候选。两段相同 `PET>14-524` 的 ACCEPT 不擅合并，原名 `加特力奴/加特利奴` 差别保留；范围不冒充真实库存、原文不公开、原生任务／买卖／治疗执行未证。公共[来源索引](research/recovered/STONEAGE-INTEGRATION32-QIKAKA-FOUR-ROOMS-SOURCE-R1.json)与负例测试共用现成 CI。完整 CURRENT 原 blob 保留，Stage A7PARTIAL＋2OPEN，Stage B/wiki GATED，R79暂停，总体完成率未知。下轮转其他有新来源内容；缺同版宠物主数据或原生运行证据前不扩 PET 任务机制推论。


## 2026-11-10 — INTEGRATION33｜薩伊那斯两组原任务的跨模块来源联接

[老人萨顿三家宝与恐龙博士哈鲁双阶段源证](docs/continuity/STONEAGE-INTEGRATION33-SAINASU-TWO-QUEST-CHAINS-20261110.md)：私人CHAR01、ITEM01、INTEGRATION10三包共3,357个ZIP成员全部CRC与整SHA重新核验，实际重读四份未在QUEST08–31专项覆盖的原script与两份CREATE，共4源NPC／13个TYPE段／3个原DAT地图范围。1100 DAT私有源原样重读并核(86,99)三平面值；1112／11006引用已验MAP09。任务13关联5个有来源道具（家宝／盗贼脚印／秘药）；任务15/16分别保留`PET>14-74`、`PET>29-191`、`GetRandItem`八候选与`GetPet:95`，13个不同物品ID双表SHA精确相同，PET10同载体备选模板95均对应SPR图号100394，但两个原行SHA不同，原生奖励未证。旧INTEGRATION05已知GetPet95，不重复认作新发现。公共[来源哈希/数值索引](research/recovered/STONEAGE-INTEGRATION33-SAINASU-TWO-QUEST-CHAINS-SOURCE-R1.json)与逐字段回归；原商业原文/图/DAT仍只私人，当前Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停，总进度未知。下一项继续未整合源或新原像素，不凭脚本改写初代玩法。


## 2026-11-10 — INTEGRATION34｜GetPet95 的跨版本原像素候选100394

[同号宠物原动画图像重新实物核验及止点](docs/continuity/STONEAGE-INTEGRATION34-GETPET95-CROSSCARRIER-VISUAL-20261110.md)：从已保存的私人 PET07 原像素 HTML 15,123,277B 和原 RD 全收据 JSON 1,617,404B 实际回读两整SHA，限定到 TW1.0原SPR图号100394；三条动作方向0源序列合23个原帧位置／16个不同 bitmap，逐张真正解出16份嵌入PNG共71,187B，16/16 PNG整SHA及Pillow解码原尺寸均与先前真实原RD收据一致。依据本轮I33已连接的晚期同RAR任务脚本 `GetPet:95`→两备选模板ID95/图号100394，和**不同载体**台湾1.0源原图号100394同号，提供来源明确的跨版本视觉候选，而非原任务实际奖励图或官方同版物种。原图/HTML/RD仍私人，公开[派生数值哈希](research/recovered/STONEAGE-INTEGRATION34-GETPET95-CROSSCARRIER-ORIGINAL-PIXEL-R1.json)和新反例测试；不冒充新发现原RD、完整56动画原生绘制或原客户端运行。CURRENT原blob不动、Stage A 7PARTIAL+2OPEN，B/wiki GATED，R79暂停，整体完成率未知。后续移向不同真实来源内容，停止重复该图号。

## 2026-11-10 — INTEGRATION35｜柯尔克矿坑三类矿石鉴定、被困矿工与办事处

[本轮来源限定报告](docs/continuity/STONEAGE-INTEGRATION35-SAINASU-MINERAL-APPRAISAL-20261110.md)：从私人原 CHAR01（995,176 B、2,205成员）与 ITEM01（5,868,386 B、838成员）重新整包 SHA/全部 CRC 复核，精确连原 `nevent03.create` 六份独立NPC配置、原6脚本/21段 TYPE（12 ACCEPT/9 MESSAGE）、MAP09 已验证的10605/10603/1212三原DAT场景、六原矿石与鉴定书ID及同载体双 itemset 全行 SHA；不同载体台湾1.0零售原图仅4份候选（3矿石+3证书共用1图）。原前两等级第3/4段 `DelItem` 为裸ID，最高级为显式 `*8/*5`；重复条件谓词、MESSAGE下的 `GetItem` 和兑换文案不能晋升为原生消耗、奖励或交易执行。QUEST01此前已编目这6原脚本，本轮是跨模块有界聚合，不冒称新增原文件/图像/官方初版完整任务。原版权素材、完整对白和私人观察包不进Git；[派生来源索引](research/recovered/STONEAGE-INTEGRATION35-SAINASU-MINERAL-APPRAISAL-SOURCE-R1.json)及独立反例回归公开。完整 CURRENT 2,709,173B／Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 完全不变；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、总体完成率未知。**NEXT** 转未集成且具有真正原件的新内容，缺原生分支/同版数据不重开此组。

## 2026-11-10 — INTEGRATION36｜猜谜三兄弟原入场券与未引用任务备份

[完整来源关联和原 BAK 差异](docs/continuity/STONEAGE-INTEGRATION36-QUIZ-THREE-BROTHERS-20261110.md)：私人CHAR01、ITEM01两ZIP整SHA与2,205＋838成员CRC实际复核。源 `quiz.create`11独立CREATE位于812/810/850/2020/4020，六原脚本23段在QUEST01已有编目；本轮连接六独立票据/会员证/箱子原物品行、49不同随机道具ID与三份原 `GetRandItem` 候选列表（首份13字段含一个空值），原`GetPet14/351`此前 I05 已证索引，不能虚构原奖品已发。**真正新变体**：同RAR `equiz_04.BAK` 801B不被现有CREATE引用，ASCII控制行`EventNo45/GetPet352/EndSetFlg45`对照引用脚本`47/351/47`；PET10同源两候选图号100040却原行SHA不同，不据此说历史运行/先后。同来源地图812/2020/4020先前MAP09合格；810/850仅未被此目录认证，非旧服无图。独立TW1零售原24222图候选真实PNG 1,438B/28×39全SHA重读；24314、24309缺零售索引。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、总体percent=null；完整原 CURRENT 2,709,173B Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`未动。版权原图/原任务文本/私人ZIP不进Git；[公开派生索引](research/recovered/STONEAGE-INTEGRATION36-QUIZ-THREE-BROTHERS-ORIGINAL-SOURCE-R1.json)和11项精确正反回归。


## 2026-11-10 — INTEGRATION37｜加奥利／乌力书信的原地图、NPC图像、脚本和物品统一来源视图

[有界来源组合与下项](docs/continuity/STONEAGE-INTEGRATION37-GOA-ULI-LETTERS-20261110.md)：复用已验QUEST13与CHAR05确切Git blob，按同保存混合2.5原RAR/NPC ZIP的原CREATE路径和序号唯一联接10条配置、6张已有原DAT/10个真实格三平面值、2个同RAR已验动作0八方向原SPR组、10份原任务脚本/16旧事件段及5个同源物品表记录。该轮新增**可独立核对的跨模块整合视图**，无新原商业脚本／图像下载、原RD解码和原生任务执行；历史任务是否正式/常驻、实际选帧/对话/发奖励及官方同服均待证。公开[数字/哈希原源联接](research/recovered/STONEAGE-INTEGRATION37-GOA-ULI-LETTERS-MAP-SPR-SCRIPT-SOURCE-R1.json)与源固定回归验证；完整旧CURRENT 2,709,173B Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`不改。Stage A 7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79暂停，总进度未知。NEXT转真正未集成且有可靠原材料的玩法内容。


## 2026-11-10 — INTEGRATION38｜SBC／JBA两饲育员协会的原证书及双门点

[完整证据及欠源边界](docs/continuity/STONEAGE-INTEGRATION38-SBC-JBA-CERTIFICATE-20261110.md)：从已保私有CHAR01/ITEM01/MAP09三个原ZIP再次完整核SHA/CRC，真实重读SBC/JBA管理员3创建、2脚本旧4TYPE、2入门配置及原2参数共8份原NPC文件，源字面分别包含2479与2480双证互换的DelItem/GetItem和10913→10920、20704→20712的对应FREE证书门槛。物品双表两证逐原行SHA同，TW1零售跨版原RD两私有PNG实际核SHA/尺寸；原955 DAT真读20712/10913/20704及格值，10920缺当前档案DAT且20712不在MAP09资格像素集，不能凭缺件宣布历史无图。新的是一条可查双组织来源关系，不是新增旧脚本或实际运行互斥/发证/传送。公开仅[派生数字/证据SHA](research/recovered/STONEAGE-INTEGRATION38-SBC-JBA-CERTIFICATE-ACCESS-ORIGINAL-SOURCE-R1.json)、CI反例与这份加法连续性；旧CURRENT原2,709,173B/固定blob不变。Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暂停、整体未知；NEXT转不同有材料内容。


## 2026-11-10 — INTEGRATION39｜成年／转生原目录的五组配置与事件标志来源联接

[有界原来源关系与验收边界](docs/continuity/STONEAGE-INTEGRATION39-ADULT-REBIRTH-SOURCE-20261110.md)：从完整远端原生 Git blob 重放既有 CHAR01 与 QUEST01，确切联接同一保存社区 mixed25 归档的1个`my/chengren`、4个`my/zhuansheng`原 CHANGE EVENT CREATE，地图原编号2000的(54,50)与(47–50,58)五个数值位置、各自的原图形编号与五原脚本六个TYPE；原字面 EndSetFlg 4/39/40/42/46。原`zhuans.create`第4/5块却分别是道场模板与宠物店模板，不得因路径共现并为转生事件。QUEST32标记的此前未专题集成五份脚本，现在建立可回放跨表关系，**不是新获原脚本或原生转生执行证明**；公开[派生索引](research/recovered/STONEAGE-INTEGRATION39-ADULT-REBIRTH-EVENT-CREATE-SOURCE-R1.json)只含旧原源SHA、数字与原事件段哈希。MAP09没有合格2000场景，不等于原DAT/游戏世界不存在。SOURCE_BOUNDED_PARTIAL，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、总完成率未知。NEXT移向其它确有增量的原始内容，不补造成年／转生玩法阈值或状态。


## 2026-11-10 — INTEGRATION40｜原成人与四大洞事件标志，地图2000原数值与局部候选原像素

[实际原字节与边界](docs/continuity/STONEAGE-INTEGRATION40-FOUR-CAVE-SOURCE-AND-FLOOR2000-20261110.md)：重新完整 SHA／CRC 验私人 995,176B/2,205 原NPC源ZIP、46,844,444B/4,195 MAP09 ZIP及内嵌955 DAT、35,673,334B/4,169 台湾1.0原像素候选包；不是仅复用索引。直接 CP950 读成年LV>29/flag4、四个后期社区转生捷径LV>139/flag39、40、42、46；同一NPC来源另四个不同原脚本对同号flag另设任务物品、前置条件及原DelItem/GetItem，绝不能把省四洞的晚期社区提示当作早期官方原始规则或已见证运行。原DAT floor2000真读150×150与六个NPC点位三平面；342格目标小范围353次>99图号都有已验TW1零售原RD候选，另60次低值未认定；整图仍14次/11图号缺源资格。私有48,395B/8成员原图候选与位置联系包已存个人Library、回下载全SHA/CRC一致，无商业原脚本/图/DAT上传Git。公开 [来源数值/哈希对照](research/recovered/STONEAGE-INTEGRATION40-FOUR-CAVE-FLAG-BYPASS-FLOOR2000-SOURCE-R1.json)、专用反例测试；不认证原程序执行、原生转生、官方同服或整世界。旧CURRENT完整原2,709,173B保持；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、总进度未知。NEXT转其它有真正实物的新内容。


## 2026-11-10 — INTEGRATION41｜加鲁卡环岛 B 路线原地图与检查站

[来源与当前续接](docs/continuity/STONEAGE-INTEGRATION41-JARUGA-ROUTE-B-20261110.md)：实际重读八张保存社区混合 2.5 原 DAT、14 个 CREATE 块和对应原脚本，联接报名、12 站与终点。1,712 次大于 99 的局部图号引用中 1,708 次有台湾 1.0 原像素候选，报名点仍缺三个后期图号。另双解码四份人物候选原 RD，独立复核 42 个画布。原生可达性与官方同部署仍待证。最高 NEXT 是核三个报名图号的后期原 REAL，然后按来源资格补图或停止。


## 2026-11-10 — INTEGRATION42｜环岛报名点原图补证及地图 3000 全图

[来源与下一项](docs/continuity/STONEAGE-INTEGRATION42-JARUGA-REGISTRATION-ORIGINAL-TILES-20261110.md)。从完整混合 2.5 原 ADRN/REAL 恢复 24307、24309、24310，补齐报名窗口 4 处原图引用至 126/126。同包图块重放地图 3000 全图，覆盖 10,851/10,853 处高值引用，保留 22413 两处无匹配原格。最高 NEXT 为地图 4000 与环岛 A6、A 终点的同源整合。


## 2026-11-10 — INTEGRATION43｜A6／A终点与地图4000原资料有限整合

[来源限定与下一步](docs/continuity/STONEAGE-INTEGRATION43-JARUGA-A6-FINISH-SOURCE-BOUNDARY-20261110.md)：从本轮真实重新核 SHA/CRC 的 QUEST25、INTEGRATION41、INTEGRATION42 三份私人包与 Q25/I41/I42 Git 派生证据，确定 mixed25 原 CREATE 的 A6 地图4000 (63,66)、终点 (54,47)，分别联接原 oev_6 的2557→2558与 oev_ed1 的2564要求、原奖品数字列表。12 原 TYPE 段可逐 SHA 追溯；不解释重叠条件的分支执行，台湾1.0图仅跨载体候选。地图4000 全图8603高值引用中4缺号、两处窗口131/139引用是旧来源预检；本轮**未取得4000原DAT字节，未重新解码RD或绘制地图像素**，故仅完成两条来源限定跨模块关系，不虚报原版客户端/服务器运行。原商业资料不公开，完整 CURRENT 2,709,173B 原blob c89e0e33537990aa2132b47c40fef49a985a935c 保留；Stage A 7PARTIAL+2OPEN，Stage B/wiki GATED，R79暂停，总进度未知。NEXT需有同 SHA 原4000.dat才重开像素，否则轮换其它有源原内容。


## 2026-11-10 — INTEGRATION44｜环岛A1原地图与原人物图像实际观察

[原源画面与止点](docs/continuity/STONEAGE-INTEGRATION44-JARUGA-A1-ACTUAL-ORIGINAL-SOURCE-PIXELS-20261110.md)：上轮A6/终点的地图4000原DAT仍未取得，按来源止点改用可真实读到的原地图3000。地图A1原(99,64)周边121格、132高值图块引用全部对应73份有资格原图；I41现成52、MAP04现成20、**TW1原REAL新重取图号8335一幅**。又从TW1完整REAL实解人物候选16068。原 DAT、ADRN、REAL、SAP五份私人源包整SHA/CRC和双RD解码/独立三种736×745 RGBA画布完全吻合，场景已目视；A1原配置与`oev_1`的`ITEM=2552→2553`联接，现代额外人物、标记不是原生画面。私人2,035,837B/85成员ZIP SHA`330e3568…114df1`已存个人Library并回读同SHA；原DAT、RD、PNG、原脚本不公开。只发布[派生数字、来源及证据边界](research/recovered/STONEAGE-INTEGRATION44-JARUGA-A1-ORIGINAL-SOURCE-PIXELS-R1.json)及CI。仍未取得4000原 DAT、未证明原版运行/同服/原NPC动作，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、总体百分比未知。NEXT优先有真实原 DAT 的其它 A 路场景，否则按模块轮换，不扩无源地图/新引擎。


## 2026-11-10 — INTEGRATION45｜环岛A3、A7、A11原地图实像与任务来源

[原DAT及独立实像重放](docs/continuity/STONEAGE-INTEGRATION45-JARUGA-A3-A7-A11-ORIGINAL-SOURCE-SCENES-20261110.md)：从已验原 I41 MAP/DAT＋台湾1.0 MAP04 原 RD 图＋QUEST25 原脚本实物恢复 A3地图20105/(25,49)、A7地图20301/(238,118)、A11地图20601/(5,11)，共**363个源格／264次大于99图像引用全部有源／108个跨场景不同原图号**，另215次低值仅保留数字。三处真实原DAT整SHA、原 NPC CREATE/脚本逐成员 SHA核验；重新从纯净TW1原REAL实际双解 `16067` 人物RD，旧16068原RD同源复核。九幅分层RGBA均Pillow/NumPy及另一独立归档重放逐像素相同，现代独立画面不是原生客户端。私有 **5,098,689B／132成员／SHA `a705e963…350d018`** 已存个人Library并整包回读完全相同；原DAT、RD、PNG和商业脚本正文均不入Git。公开[源格与图像哈希／历史界限索引](research/recovered/STONEAGE-INTEGRATION45-JARUGA-A3-A7-A11-ORIGINAL-SOURCE-SCENES-R1.json)只供回归；Stage A 7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79暂停、整体百分比未知。最高 NEXT：已有保留 I10 原`3400.dat`的 A12 检查站画面实源复核、拼合与原任务关系；`4000.dat`仍缺原件，不推断原生运行或官方同服。


## 2026-11-10 — INTEGRATION46｜环岛A12原地图3400实像与静态任务归档

[原始来源与止点](docs/continuity/STONEAGE-INTEGRATION46-JARUGA-A12-ORIGINAL-SOURCE-PIXEL-20261110.md)：从I10原补救包真读混合2.5社区 `3400.dat` 86,408B SHA`a3c6918b…ca263c4`，并重新检验QUEST25原 `oev.create#12`、`oev_12` 六段、坐标(69,61)、道具2563→2564。11×11窗口**121格、135次>99原图引用、69种不同图号全部有台湾1.0原像素资格、21次低值单独保留**。原TW1完整REAL/ADRN/SAP重SHA；旧16067 RD从I45保管包重读、两套解码与原REAL字节再次匹配，不称新图发现。三张736×769候选场景Pillow/NumPy及第三独立ZIP重放逐RGBA完全一致，另原人物/坐标标记仅现代叠加；实际已目视绿地、树木、河岸。私人 **1,314,729B/80成员/SHA `d5885220…6159e`** 已存个人Library并回下载整包SHA、CRC完全一致；原DAT、原RD、原脚本及商业像素均不入Git。公开[派生数字/SHA及不确定性](research/recovered/STONEAGE-INTEGRATION46-JARUGA-A12-ORIGINAL-DAT-AND-PIXEL-SOURCE-R1.json)。先前原RAR 3400.DAT中途CRC读错史保留，本轮从I10保存源确实可读；原客户端/同官方服/原生碰撞与任务执行仍OPEN。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、总体百分比未知。环岛其它 A2/A8/A9/4000等MAP缺原DAT，NEXT按模块计划转其它有实物的新原内容；不补造游戏地图、不启动新单机引擎。


## 2026-11-10 — INTEGRATION47｜波鲁13张已存原地图的关系验真与任务63/64静态接缝

[原始来源和止点](docs/continuity/STONEAGE-INTEGRATION47-PORU-13-SCENE-STATIC-SOURCE-GRAPH-20261110.md)：从原私人QUEST23/24 ZIP全包重新SHA/CRC、59次原NPC成员SHA、13原DAT整SHA及旧现代候选RGBA像素SHA实际回验；两份已存TW1原图候选913/490逻辑号的78个同号PNG实际全字节SHA吻合，合并1325个图号，**不是1325张新发现美术**。原格22564次>99图号、8057次1–99低值保留。真实源参数给出mixed25地图5509(37,35)经WarpMan字面指向5510(16,49)，邻格5510(16,50)原模板是ExChangeMan/MESSAGE且无WARP，不凭文件名编逆向传送。来源任务boy04 GetPet352/flag63与mary01四道具/GetPet310/flag64保留静态联系，samugiru01 MESSAGE所需18544与末段18558不同，不抹平；原floor500 DAT缺源。同官方部署、原运行、任务执行、原版世界图均未证，台湾1.0原图仅跨保存载体候选。没有新增原DAT/原脚本/原RD，原商图/脚本/地图均私人保管；公开仅[数字／哈希来源索引](research/recovered/STONEAGE-INTEGRATION47-PORU-13-SCENE-SOURCE-GRAPH-R1.json)、反例测试和CI。原CURRENT 2709173B/blob c89e0e33537990aa2132b47c40fef49a985a935c 保持全字节不变；Stage A7 PARTIAL＋2 OPEN、Stage B/wiki GATED、R79暂停、overall_percent=null。NEXT依模块队列转另一组有原实物的非波鲁内容，不扩无源floor500、新引擎或登录服务。


## 2026-11-10 — INTEGRATION48｜四村长毛象快递任务原条件提示、验收与来源不完备性

[来源实证与止点](docs/continuity/STONEAGE-INTEGRATION48-FOUR-VILLAGE-COURIER-SOURCE-CONDITION-20261110.md)：从私人 QUEST06 原ZIP **40,204B／13成员**重新全SHA/CRC、4份完整CP950原脚本/24 TALKEVENT/8个NPC创建位，以及6份已存台湾1.0零售原图候选PNG逐字节SHA重验；另将不同原文件的 QUEST31 四村事件ZIP **27,565B／26成员**全SHA/CRC核同，**两套任务不能因“四村”同名并作一个原版剧情**。真实原静态条件连接八个正向ITEM提示候选至四份脚本的唯一接收条件，阶段一提示2622出现2次、**2625缺正向提示**；阶段二提示4224出现2次、**4212缺正向提示**，故不编造完整四村循环或物品取得步骤。每脚本只有1—9、10—19、20—29三个验收等级段，LV30原字面没有明确分支；宠物条件分别原值1-13/1-292，四份都无DelPet，不证明历史宠物被收取。前序 QUEST06 8 NPC地图/任务来源实际已归档，本轮只新建条件的可复核定向关系而无新原DAT/RD、原生NPC或交易运行。源社区mixed25任务与TW1跨版本候选美术严格分离，商业脚本/PNG/源文件只私人保存，公开仅[派生哈希及负证索引](research/recovered/STONEAGE-INTEGRATION48-FOUR-VILLAGE-COURIER-SOURCE-HINT-ACCEPTANCE-R1.json)、反例测试与专项CI。原CURRENT全 2709173B/blob c89e0e33537990aa2132b47c40fef49a985a935c 未改。Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暂停、总体完成率未知；**NEXT** 有新原发件/同源场景才重开此包，否则回另一组有实际DAT/图像/NPC实物的游戏内容，避免循环无证路线或新引擎。


## 2026-11-10 — INTEGRATION49｜28间原DAT房间的NPC功能及传送来源分类

[实际原DAT/创建配置及研究画面复核](docs/continuity/STONEAGE-INTEGRATION49-28-ROOM-NPC-WARP-20261110.md)：在本轮新读的私人MAP07旧28间原DAT/原TW1图候选场景（原保存ZIP 34,044,818B SHA2b356fef…，351成员CRC全过）与CHAR01原2205成员NPC包（995,176B SHAc35ed126…）上，全28原DAT SHA/CRC、139原CREATE配置块SHA/12个涉及原源文件整SHA、234候选原图PNG与28幅现代合层整RGBA独立复核。前28房间属于**已取得的旧原素材**，本轮新增可回归的房间—NPC功能—出口关系，**不是28张新发现DAT或139个新发现NPC**。房间实际按原Warp目标分成六组主图 1000:3、1100:5、1200:5、1300:5、2000:5、3000:5，完全不由地图编号或猜测岛屿划归。源配置功能有56 Warp、32 ItemShop、6 PetShop、6 PetSkillShop、8 TownPeople、5 WindowHealer、3 Windowman、3 ExChangeMan、2 Charm、18原空功能；三ExChangeMan无原CREATE直接坐标而不能补造。56处房间出口原DAT第三平面均实读49155；父图同坐标原配置返程有50条逐格精确、6条回相邻格，**不是56条同格双向**。1100/1300原DAT已在旧INTEGRATION10真正找回，本轮不能追认旧MAP09样本缺DAT为永久不存在。28幅现代坐标标注私人图集16,857,395B SHA76e8f099…已保存个人Library且回取整SHA/29 CRC/28逐图SHA核同；新原RD解码0。跨保存样本TW1候选图与mixed25原地图/NPC严格分离，原商业DAT/脚本/PNG只私人保管；公开仅[数字、哈希与分组](research/recovered/STONEAGE-INTEGRATION49-28-ORIGINAL-ROOM-NPC-WARP-SOURCE-ATLAS-R1.json)和负证CI。原版客户端执行/碰撞/原生NPC/同官方部署未证；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、总体percent=null。历史CURRENT 2,709,173B/blob c89e0e33537990aa2132b47c40fef49a985a935c 保持全字节不变。**NEXT** 转已有原件的其他非本28室场景服务/宠物/物品实际内容，避免重复本批索引、无据编造地理或启动新引擎。


## 2026-11-10 — INTEGRATION50｜28间原房的商店、宠物和技能菜单来源关系

[逐原文件哈希、参数关系及边界](docs/continuity/STONEAGE-INTEGRATION50-28-ROOM-SHOP-PET-MENUS-20261110.md)：从私人CHAR01完整来源ZIP重核2,205成员CRC、44条CREATE对应43份唯一原参数文件整SHA；对INTEGRATION49既有28室建立32条ItemShop（攻击7、防御5、饰品6、原字面空类别8、类别字段缺失6；29条同旧物品索引按路径+SHA精确连，3条缺ItemList）、6条PetShop（1003/2003/3003有原pool两个字面字段）、6条PetSkillShop（六个原技能数字列表50出现位置/15不同ID/共同0、1、2、3）的来源联接。新增的是静态跨表对应，不是原DAT/NPC新增、已执行交易/教学、台湾1.0同服或原版可玩世界；不补造缺失字段。公开[纯派生JSON](research/recovered/STONEAGE-INTEGRATION50-28-ROOM-SHOP-PET-ARGUMENT-BRIDGE-R1.json)及回归，原件和原文私人保管。原CURRENT 2,709,173B/blob `c89e0e33537990aa2132b47c40fef49a985a935c`保留；本轮大文件接口未能回传完整正文，不虚称全文成功读取。Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79暂停、总进度未知。NEXT优先28室外有新原物证的原内容；本批CI和主线验收另据后验记录。


## 2026-11-10 — INTEGRATION51｜两座百人道场的原NPC与地图来源对照

[1021／3021原百人道场的逐关原源关系](docs/continuity/STONEAGE-INTEGRATION51-TWO-DOJOS-ORIGINAL-SOURCE-20261110.md)：从私人社区mixed25原NPC ZIP本轮整SHA及2,205个CRC真实核对，两原CREATE合计600原块；对1021未专题的100个原对战参数、200个独立Warp配置，与旧3021百人图谱100/100逐关验证坐标与目标的对应。两馆同源敌人候选字面564—580，但宠物候选分别655—690与687—720；两馆第100关参数分别转1008(20,20)与3008(20,20)，原100对玩家字面并非已执行100场战斗。1021旧MAP01 DAT(407×144)有源合格记录，但此轮没重读DAT/生成原像素；旧3021.DAT读取失败仍保留负证，1021／3021原MAP SHA不同，不共用原画面。公开[100条源SHA/坐标/门点数值索引](research/recovered/STONEAGE-INTEGRATION51-TWO-ORIGINAL-100-DOJOS-SOURCE-BRIDGE-R1.json)、12项跨旧图谱与MAP01回归；私人原NPC、地图、图像不进Git。完整CURRENT原blob `c89e0e33537990aa2132b47c40fef49a985a935c`不动，本轮Git原blob接口成功返回全文文本。Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暂停，总进度未知。NEXT转不同的真实原内容；CI/正式主线验收另据后验。


## 2026-11-10 — INTEGRATION52｜原1021百人道场DAT格、图像与100 NPC/200 Warp的可核对应

[原图观察／来源详情](docs/continuity/STONEAGE-INTEGRATION52-DOJO-ORIGINAL-DAT-PIXEL-OBSERVATION-20261110.md)及[公开300个原格的来源索引](research/recovered/STONEAGE-INTEGRATION52-1021-DOJO-ORIGINAL-MAP09-300-CELL-PIXEL-SOURCE-R1.json)：复用已保存MAP09私人原件46,844,444B／4,195 ZIP CRC、其内955原DAT CRC，**真正重读**1021.DAT 351,656B、1022.DAT 1,358B及1008.DAT 9,608B逐完整SHA与先前MAP01/MAP09相同；逐一核查前次INTEGRATION51来源的100对战NPC＋200独立Warp共300个不同原地图坐标，全部平面0源字面>99、平面1原字面0，第三平面不作碰撞/事件解释；来源NPC底图号4008/5062/5087分别55/21/24。六个**私有**实际来源图候选局部是1021第1/10/51/100关、1022(1,7)入口、1008(20,20)终点；137个原保存图块源别名逐PNG/RGBA SHA核同，新增原RD解码0，原商业资产没有公开。私人13成员观察包/图已保管于Library并经保存后二次全SHA/CRC核实。原图是mix25后代DAT×TW1原图候选叠加现代十字，非原生渲染、原生NPC/胜利/传送实测。3021.DAT旧读取失败与原完整CURRENT blob `c89e0e33537990aa2132b47c40fef49a985a935c`均保留；Stage A7 PARTIAL+2 OPEN，B/wiki GATED，R79暂停，整体百分比未知。NEXT离开同一百关素材，转另一个实际游戏内容增量。GitHub CI与正式主线验收另依后验。


## 2026-11-10 — INTEGRATION53｜三龙任务原NPC位置与台湾1.0原SPR动画像素证据的跨来源接缝

[有界来源工作报告](docs/continuity/STONEAGE-INTEGRATION53-DRAGON-NEST-TW10-SPR-VISUAL-20261110.md)／[三个原NPC—不同样本原动画与模板证据](research/recovered/STONEAGE-INTEGRATION53-THREE-DRAGONS-QUEST-NPC-TW10-SPR-SOURCE-BRIDGE-R1.json)：从最新main独立重读QUEST14、PET07、PET15、PET10四份**完整公开派生原来源索引的Git blob**，把后期mixed25保存的三龙创建图号100384/385/386、原20807 DAT格(7,8)/(23,6)/(41,14)、三条不同原GetItem(2462/2460/2461)，逐原CREATE/脚本/DAT SHA对到**另一个台湾1.0零售保存样本**原SPR索引350/351/352及PET15早已实绘的各56段、712帧位置/232组内不同bitmap。各图号同时有多种后期服务器宠物模板原行/原SHA，绝不当成已证物种或同服NPC动画。**本包新增原RD解码0、原DAT获取0、原生任务和原NPC渲染0**：只新增此前缺失的原NPC→已验TW1图像候选跨模块证据关系。专用11项静态来源／否证回归必须据真实Actions后验记录，不以私人原资产为公开CI输入。历史CURRENT原2,709,173B Git blob c89e0e33537990aa2132b47c40fef49a985a935c完全不动；Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null。**NEXT** 转非本三龙、非百人道场的确有原字节/可见新内容关联的场景；无更强证据则保留原生身份/行为OPEN，不重跑相同图号或启动新引擎。


## 2026-11-11 — INTEGRATION54｜吉鲁矿山矿工原地图与100401台湾1.0真正原像素观察

[有界报告](docs/continuity/STONEAGE-INTEGRATION54-GIIRU-MINER-ORIGINAL-DAT-TW10-PIXELS-20261111.md)／[原来源数字和SHA](research/recovered/STONEAGE-INTEGRATION54-GIIRU-MINER-DAT-TW10-REAL-PIXELS-R1.json)：私人QUEST12原包113,328字节、32CRC完整重读两张50×50原DAT(31805/31806)及5个目标格；原NPC矿工巴卡斯的社区2.5 `borncenter=26,23,1,1`、图号100401及静态`item=2535`源实物复核。另一台湾1.0零售PET07原HTML15,123,277B中实际取出8幅真实原RD已解码PNG候选(82737—82744)，逐PNG SHA/尺寸与旧源收据一致；现代私人研究拼版已上传Library、独立取回验证593,529字节/10成员/全部CRC。**严格负证：** PET07动画动作0/方向0的原RD bitmap82729严格RLE失败，PET15后来bounded处理不可追认无损恢复；社区两原表同图号模板719主/备PETFLG为1/0，不推唯一宠物或真原服身份。本轮原RD新解码0、原客户端/服运行0、私人图或原DAT公开0。历史CURRENT原blob c89e0e33537990aa2132b47c40fef49a985a935c/2,709,173B保全，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总进度未知。NEXT转其它未专项的真实可见游戏内容，非再次反复矿工同号。


## 2026-11-11 — INTEGRATION55｜恐龙牧场三条真实原宠物条件→台湾1.0 SPR 48幅实物图像

[原始资料重读与三色凭证源限定说明](docs/continuity/STONEAGE-INTEGRATION55-DINO-RANCH-THREE-PET-REAL-PIXELS-20261111.md)／[公开源脚本→宠物表→真原动画48幅SHA及4物品图关联](research/recovered/STONEAGE-INTEGRATION55-DINO-RANCH-THREE-PETS-TW1-48-REAL-PIXELS-R1.json)：从私人Library实际再次取回QUEST17原包29,802B／32ZIP成员CRC和PET07私人原图离线HTML15,123,277B以及原RD逐图来源表1,617,404B；真读原`bait_03a2/b2/c2`脚本，`PET=560/559/558`原`DelPet`四个数量字面各有源SHA，牧场201楼层三NPC坐标(19,13)/(19,14)/(19,15)，凭证原物品ID2594/2595/2596。在两原mixed25宠物模板表找到一致数值图号100271/100335/100368，分别跨版本接独立**台湾1.0**零售原SPR组261/305/334；每组原动作0/2/1已存且本次实读**16张不同原位图PNG**（合计48），逐PNG整SHA、原RD SHA、尺寸/动画来源复核成功。另从QUEST17原ZIP真读并核对4种独立原物品图号22114/22118/22120/24222的4张PNG。现代私人52图集/图像收据ZIP582,786B、54成员**已上传个人Library后独立回取全SHA/CRC/48图SHA合格**，私有原画不入Git。原DAT201/20901本轮实读0，原RD新解码0、原游戏/宠物交换执行0，非同一认证早期原服或已认证宠物物种。旧CURRENT完整2,709,173B/blob c89e0e33537990aa2132b47c40fef49a985a935c不变；Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null。NEXT转不同可取得原景观/人物实物的内容领域，不重复牧场同号。

## 2026-11-11 — INTEGRATION56｜梦幻洞窟双守卫四源点／原41和42层／台湾1.0原像素32张

[源实物与边界](docs/continuity/STONEAGE-INTEGRATION56-DREAM-CAVE-TWO-GUARDS-20261111.md)及[公开可复核原CREATE／原DAT／原SPR／像素来源联接](research/recovered/STONEAGE-INTEGRATION56-DREAM-CAVE-GUARDS-41-42-TW1-32-PIXELS-R1.json)：私人QUEST09原包28,306,717B/25成员完整SHA/CRC重读，原`sb_mugen.create`四个原块及两张70×70原DAT(41/42)实际SHA核同，现场读两层守卫格(34,41)/(33,41)三原uint16层。另一私人台湾1.0零售PET07原图HTML和独立RD收据完整SHA重读，原SPR编号100343/100346各16个不同原位图、33帧位置，共32幅实际已解原PNG/66帧位置逐SHA和尺寸验一致。本轮**新RD解码0**；原地图社区mixed25与早期美术不是已认证同部署或原版NPC行为。私人41成员15,621,429B压缩包SHA `aca681e3eee04a67bab488dcbbab00dda3d479274482c87d37a170478541bcce` 已上传个人Library并独立下载全SHA/CRC核验；原PNG、DAT、NPC全文不公开。历史CURRENT全2,709,173B原blob c89e0e33537990aa2132b47c40fef49a985a935c不改，Stage A7 PARTIAL+2 OPEN/B/wiki GATED/R79暂停/总体未知。**NEXT** 改到其它真正有原地图/原NPC/原像素实物的场景或内容，勿重复本双守卫图号，缺原实物即精确止点；候选与主线CI另据实时状态验收。


## 2026-11-11 — INTEGRATION57｜吉鲁两族任务两原配置与同载体144份原RD/PNG实物

[本轮来源与私人实物审查](docs/continuity/STONEAGE-INTEGRATION57-GIIRU-TRIBES-SAME-CARRIER-PIXELS-20261111.md)及[可远端重放数字/散列/原帧序](research/recovered/STONEAGE-INTEGRATION57-GIIRU-TWO-TRIBES-31205-ORIGINAL-RD-SOURCE-R1.json)：从私人QUEST11实际重读原`garunaev1.create`序号2/5及两脚本`garunaev3/6`，恢复吉鲁`31205`原DAT25×25两格(12,11)/(12,12)的原三u16值，原NPC图号100250/100252。两组图的同混合2.5保存RAR SCENE13原RD子ZIP+原PNG内嵌实物、先前R40/CHAR05源SPR段散列重新核对：**8+8方向序列、72+208原有序帧位置、64+80不同bitmap，每一份144/144 RD/PNG/RGBA原SHA一致**，新原RD解码0、原客户端/服务器运行0。私人869340B／297成员ZIP已存个人Library并独立回取整SHA/CRC/144源像素核验，现代查看器16方向图像读取/0JS错误/0网络。源图、原脚本、DAT仍私人；公开不带版权资产。同保存载体非原官方同部署/原NPC动作证明，不把144图当宠物种数。旧CURRENT2,709,173B原blob c89e0e33537990aa2132b47c40fef49a985a935c完整保留；Stage A 7PARTIAL+2OPEN，Stage B/wiki GATED，R79暂停，overall_percent=null。**NEXT** 更换其它来源充足的原图+地图+NPC/任务关系，不重复双角色动画或引擎/账号开发。候选及正式主线验收另据实际Actions。


## 2026-11-11 — INTEGRATION58｜波鲁龙巢三原DAT／原事件63与台湾1.0两组真原像素

[原源、三地图和私人实物核验](docs/continuity/STONEAGE-INTEGRATION58-PORU-DRAGON-FLAG63-THREE-SCENES-20261111.md)与[公共数值／哈希可复核联接](research/recovered/STONEAGE-INTEGRATION58-PORU-THREE-MAP-DRAGON-FLAG63-TW1-32-PIXELS-R1.json)：私人QUEST24原ZIP23,451,751B/578成员CRC全部实际重读，原5509/5510/5511 DAT各完整SHA核定，NPC #21(5509,(37,35),图100388)、#27(5510,(16,50),图100388)、boss #0(5511,(17,12),龙王图100373)分别查原CREATE及原三u16格。原脚本字面5509条件`WARP=5510,16,49`／`FREE ITEM=2414`和龙王事件63的`GetPet:352`→既有mixed25模板303/同数字图号100373、`EndSetFlg:63`仅为静态证据。独立台湾1.0原PET07源SPR354/339两组动作0/2/1方向0保存**52+27=79源帧位置、18+14=32张不同旧已解原RD候选PNG**，实际读HTML内嵌32真PNG并逐完整SHA/原RD收据和尺寸合格；本轮原RD原字节重读0、新解码0。私人47成员8,265,963B/SHA256`a6262443dabe1181e2ebbbab99fca3e31b98cd316d2d67f17e290a0d2a8892a2`已存Library并独立回取整SHA/CRC和32像素核验，公开原图和商业正文0。同数字跨载体不证明同原官方部署或任务奖励、原客户端/服务端执行。旧CURRENT2,709,173B/blob c89e0e33537990aa2132b47c40fef49a985a935c不变，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、整体完成率未知。**NEXT** 换未专项且有原实物的其它内容，不重复波鲁龙巢相同来源或转新引擎；候选和main CI另按实际后验。



### 2026-11-11 — INTEGRATION59 four-village original shop numeric crosswalk

[INTEGRATION59 source-bounded record](docs/continuity/STONEAGE-INTEGRATION59-FOUR-VILLAGE-SHOP-NUMERIC-PIXEL-20261111.md) connects eight existing mixed25 shop CREATE/ItemList sources across 1001/2001/3001/4001 to 120 item references, 56 distinct original item rows with literal paired numeric fields 37–42, and 45 preserved Taiwan 1.0 original pixel aliases. Private ITEM01 ZIP all 838 members CRC-verified; full historical CURRENT remains untouched. Static cross-carrier candidates only, not original native equipment execution or official same-deployment. Next: source-ready different original item/skill/recipe/quest join, Stage A remains 7 PARTIAL + 2 OPEN.


## 2026-11-11 — INTEGRATION60 five original preserved clinic source joins

[Source-bounded five-clinic medicine study](docs/continuity/STONEAGE-INTEGRATION60-FIVE-CLINICS-MEDICINES-20261111.md) links five previously DAT/CREATE-qualified mixed25 rooms (1105/1205/1305/2005/3005) with ten original nurse/pharmacist configurations, 60 explicit medicine ID occurrences (12 distinct IDs), three original literal item-use callback families, and 11 independently saved TW1 original RD pixel candidates. Full private CHAR01 2205 and ITEM01 838 member CRC reread succeeded; new 28-member/52,450-byte private custody ZIP saved to Library and independently reread by SHA/CRC. Distinct nurse four-argument literals and medicine shop buy-rate literals are preserved without inventing native healing or trade effects. All original copyrighted material remains private; see [derived source crosswalk](research/recovered/STONEAGE-INTEGRATION60-FIVE-ORIGINAL-CLINICS-NURSE-MEDICINE-ITEM-HANDLER-PIXEL-SOURCE-R1.json). Stage A 7 PARTIAL + 2 OPEN, Stage B/wiki gated, historical CURRENT unchanged.


## 2026-11-11 — INTEGRATION61｜两地主厨三道物品与早期真实RD像素

[原始来源、私人实物重读与未知边界](docs/continuity/STONEAGE-INTEGRATION61-CHEF-DISH-PIXEL-SOURCE-20261111.md)及[派生数值/散列索引](research/recovered/STONEAGE-INTEGRATION61-TWO-CHEFS-THREE-DISHES-TW1-PIXEL-SOURCE-R1.json)：从已认证O75原两地主厨菜单中严格保留2009的三条UNKNOWN、3009的三条同名物品ID12607/12780/12754；本轮私人ITEM01原ZIP完整SHA及838/838成员CRC实读通过，三原TW1保存PNG逐SHA/尺寸/RGBA复验成功，完成itemset别名24484/24443/24531→原ADRN物理位图6651/6610/6698的**跨来源候选**联接。不是新增三份原始菜名或新RD解码，也不是实际原生料理或官方同部署认证。历史CURRENT blob c89e0e33537990aa2132b47c40fef49a985a935c原样不动。Stage A7 PARTIAL+2 OPEN/B/wiki GATED/R79暂停、总体完成率null。NEXT不同来源就绪的宠物技能/任务物品/服务实物关系，禁止无证料理模拟与提前Stage B。


## 2026-11-11 — INTEGRATION62｜恐龙收集原GetPet两组宠物29张真实原RD图像来源接合

[来源限定说明与私人原图边界](docs/continuity/STONEAGE-INTEGRATION62-QUEST30-TWO-PET-REWARD-ORIGINAL-PIXELS-20261111.md)及[公开源数值／散列原动作帧序与像素身份](research/recovered/STONEAGE-INTEGRATION62-QUEST30-TWO-GETPET-TW1-29-RD-PIXELS-R1.json)：QUEST30/WORLD21旧已知`GetPet:93/341`和后期社区mixed25 `instance93/341→template171/274→graphic100319/100362`，本轮**实际重新读取并独立验收**已保存的台湾1.0原PET07真实PNG像素：原6段动作（0/2/1、方向0）共21+25源帧位置／13+16不重复原RD位图，29/29图逐文件SHA/尺寸与旧真实RD来源收据同，6源有序位图序列uint32le SHA同；新原RD二进制解码0。271047B/31成员的原图对照小包已私人Library存档并从独立新副本核完整SHA/CRC；原商美术和原脚本正文从未进公开Git。原任务道具2607同源名称矛盾、2.5双表运行选型、跨官方同部署、真实领宠/动画和floor100原DAT仍OPEN。历史CURRENT原Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 原样保留。Stage A 7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING、overall_percent=null。NEXT按材料去重再选**其它**真实任务道具/宠物技能/NPC地图原二维像素关系，避免重复本两图或提前运行网服/建设新引擎。


## 2026-11-11 — INTEGRATION63｜吉鲁巴那姆水壶11原状态与16种有据脚本替换关系

[原件来源边界与11物品/17原脚本复核](docs/continuity/STONEAGE-INTEGRATION63-BANUM-WATER-VESSEL-SOURCE-GRAPH-20261111.md)／[不含版权原文的派生状态/事件边目录](research/recovered/STONEAGE-INTEGRATION63-BANUM-11-VESSEL-STATES-16-SOURCE-EDGES-R1.json)：从旧QUEST18已经归档的吉鲁source sink家族中，本轮真实重读私人原NPC **2205/2205 CRC**、私人itemset **838/838 CRC**，核17份原script完整SHA／11个水壶ID的两份94字段CP950整行SHA，得到**49次源TYPE:ACCEPT单项DelItem/GetItem（16种有向关系，35次在11个已有CREATE引用脚本，14次只在其它保存脚本）**。另有8处批量删除+空壶、7处仅删除与1处外部物品19292关系不可混算。原物品`2710/2714`和`2711/2715`分别同显示4/7、3/7，除ID列外93字段完全同，绝不按相同水量合并源状态。11项共用原图别名12924，已保存真实TW1原RD物理5178、52×68 PNG字节SHA/RGBA核同；这**不是11幅新图，也不是台湾1.0官方同服脚本证明**。私人43成员25951B证据包已存Library并独立全字节/SHA/CRC复核；公开Git无原美术或脚本对话。历史CURRENT原blob `c89e0e33537990aa2132b47c40fef49a985a935c`完整不变，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、总体进度未知。NEXT转其它源就绪的原地图/NPC/道具或宠物可见内容；不凭静态命令模拟原版交易、账号、网络或未来新引擎。


## 2026-11-11 — INTEGRATION64｜四属性宝珠、结晶石到月光手镯的来源限定跨模块联接

[INTEGRATION64 四宝珠与原 NPC 静态来源](docs/continuity/STONEAGE-INTEGRATION64-HOUGYOKU-SOURCE-20261111.md)：从最新 main `9c1208d0ea9deed4a420e1d34ba9817e58b2309d` 及完整旧 CURRENT Git blob 重新核查，排除 O70/O74 委托、INTEGRATION63 水壶等已闭合内容。真正重读私人 CHAR01 2205 原 NPC 文件和 ITEM01 838 成员 ZIP 全 SHA/CRC。原 `extra/event/hougyoku`（1 原 CREATE，6000/(58,44)，图号16047）含 4 TYPE：`ACCEPT` 的 `LV>59` 且物品 2764/2760–2763 与 `DelItem`、`GetItem:2765`、`EndSetFlg:45`，另 `REQUEST` 字面 `GetItem:2764*1`，以及一条四组目的地的 `NpcWarp` 原数字字面；不宣称运行传送/奖品。六原物品 2760–2765 在两套 94 栏原 itemset 逐行 SHA 相同，别名 24059/24055/24061/24057/24198/22082 分别连六幅私人已验台湾1.0原 RD 候选；不同载体**不证明同一官方部署**。公开[派生数值和每段源 SHA](research/recovered/STONEAGE-INTEGRATION64-HOUGYOKU-SIX-ITEMS-ORIGINAL-SOURCE-R1.json)及 8 项反例测试；私人 21 成员 ZIP 15,469B/SHA256 `ef6ed11dc1b25c13e41190d08d3910fc5adbdeb37231d1b5d5c8bfdccd3afa94` 已保存个人 Library 后再取回 SHA/CRC 全验证；原图/原文本未公开。MAP09 691 可见候选有 5105 而未收 6000，不能推原游戏缺地图。Stage A 7 PARTIAL +2 OPEN；Stage B/wiki GATED；R79 PAUSED_NON_BLOCKING；overall_percent=null。NEXT 转其它未做过且实源合格的地图/NPC/宠物/道具，不重复这条事件或造新引擎。此段仅作候选接力记录；主线/CI 只有远端实际验收后另行确认。


### INTEGRATION64 正式验收回执（2026-11-11）

[原宝珠－手镯内容关联的候选及主线后验](docs/continuity/STONEAGE-INTEGRATION64-PUBLICATION-ACCEPTANCE-20261111.md)：[PR #332](https://github.com/chinaneedM/stoneage-rebuild/pull/332) 已合并；候选最终 `3a2314a8b82b47ac82214415daf532d2a9d5308b` 46/46 项 Actions 真正成功（27 push＋19 PR），合并 `main=c149209bebf22e45f99929c01400b742f0748ab8` / tree `1b1ed88e1ecfddfb8d2ee7db6b609a6210ae16ec`，主线 27/27 真正成功，专项 run42984499374 成功。私人 21 成员原源 ZIP 已重新从 Library 回取整 SHA 和 CRC 一致；原 `CURRENT` blob 未变。已归档[全部远端 run 收据](research/recovered/STONEAGE-INTEGRATION64-PUBLICATION-ACCEPTANCE-R1.json)。本回执后续单独 HEAD CI 不预称通过。Stage A 7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，overall_percent=null；NEXT 转不同的未覆盖原内容。


## 2026-11-11 — INTEGRATION65｜玄黄洞窟三原NPC脚本、风的手镯及25件物品／18份真实像素候选

[INTEGRATION65 原来源与有界止点](docs/continuity/STONEAGE-INTEGRATION65-GENOU-BRACELET-PET-ITEM-SOURCE-20261111.md)及[公开数字/完整源SHA/像素身份](research/recovered/STONEAGE-INTEGRATION65-GENOU-THREE-SCRIPTS-25-ITEMS-18-TW1-CANDIDATES-R1.json)：从本轮新核主线 `7983016707d48e13728aed321fb40bd5a74b74b7`／tree `7507b253cad735e975c29370f7bb7e0cd08a6b4f` 启动，实际重新读取私人CHAR01 2205/2205与ITEM01 838/838成员CRC；旧QUEST22 `genou_1`仅作背景，新增对 `genou_2/3/4` 三脚本11段TYPE的专项联接，同一CREATE五NPC配置（11215两名使者/11206看守人/100传话人等），11215/11206旧MAP09实际DAT可见资料存在、100不在该691场景目录。`genou_2`三条宠物＋2758字面交换有8/13/14个有序GetRandItem数字＝35出现/24不同ID，重复数字绝不等于已经证明概率，第一条件中`ITEM=2758LV>0`、PET60/59数值冲突严格原样留证。原注释称「風之豎琴事件」，两套原物品表2758却确实名为「風的手鐲 [風]」；旧2736竖琴不冒充2758。25件物品双表94字段原行SHA核对，全关联18张先前已真正解码TW1零售RD候选PNG并本轮逐SHA/RGBA核实；不是同官方部署或本轮新解码18张。**95,997B／76成员私人源ZIP**已经个人Library持久保存并独立回读全SHA/76CRC，原图、原94字段、原脚本不进入公开Git；源命令静态不等于实际运行。保留原CURRENT Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`，Stage A 7PARTIAL＋2OPEN、Stage B/wiki GATED、R79暂停、整体percent=null。NEXT不同、确有原字节且未做过的游戏内容，不扩框架、网服或现代新引擎。候选和main的Actions另据实测验收。


### INTEGRATION65 真实正式验收回执（2026-11-11）

[原玄黄洞窟风手镯宠物交换来源及远端验收](docs/continuity/STONEAGE-INTEGRATION65-PUBLICATION-ACCEPTANCE-20261111.md)：[PR #333](https://github.com/chinaneedM/stoneage-rebuild/pull/333) 内容候选 `589de0018cde3bcf9d30358b7b44ca0c4256bd08` 的 **46/46 Actions**（27push＋19PR）成功，squash主线 `112cb206ddb890cade92e17ef11c30a2e0cb4440`／tree `dc3af0d7d61a221f81ecacab498323aca3c0afc2` 的 **27/27 Actions** 全部成功，原同树与完整CURRENT旧blob保留。私人76成员ZIP 95997B已独立从Library回读全SHA/CRC；公开源报告 blob `6676bc788f897bfa42f6ad67220e700f4d106db5`。所有真实run IDs存[机器回执](research/recovered/STONEAGE-INTEGRATION65-PUBLICATION-ACCEPTANCE-R1.json)，本验收回执自身新HEAD CI另据实际后验。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、完成率未知；NEXT未重复原游戏实源内容。


## 2026-11-11 — INTEGRATION66｜四岛环岛原19个宠物奖励字面×15组台湾1.0真原SPR候选

[来源边界与私人原像交付](docs/continuity/STONEAGE-INTEGRATION66-FOUR-ISLAND-PET-ORIGINAL-PIXELS-20261111.md)／[公开15组/236图源数值与SHA](research/recovered/STONEAGE-INTEGRATION66-FOUR-ISLAND-TOUR-15-PET-TW1-ORIGINAL-PIXELS-R1.json)：从私人QUEST25原ZIP重读4终点脚本、173/173 CRC和实际GetPet，保留19次数字出现/15不同社区mixed25实例（B路线482重复），经同保存本enemy实例/模板接到不同台湾1.0零售PET07的15个同号原SPR图形候选。PET07私人HTML15,123,277B／原RD来源报告1,617,404B复核45原动作/方向、347帧位、236原PNG；其中230张与PET07首选候选SHA同，另6张（113515—113520）保留旧PET06配色候选SHA并与先前报告吻合，不宣称236张同首选配色。私人242成员／1,182,803B ZIP已个人Library保存及独立回读整SHA/CRC，原像和原脚本不公开；本轮RD新解码0、原生领宠运行0、官方同部署认证0。完整旧CURRENT2,709,173B原blob不动；Stage A7 PARTIAL+2 OPEN/B/wiki GATED/R79暂停/总体完成率null。NEXT不同有真实原件且未专项的游戏内容，而非重复图号或新引擎；candidate/main CI依真实后验。


### INTEGRATION66 已验收发布回执（2026-11-11）

[正式PR、源范围及全CI后验](docs/continuity/STONEAGE-INTEGRATION66-PUBLICATION-ACCEPTANCE-20261111.md)： [PR #334](https://github.com/chinaneedM/stoneage-rebuild/pull/334)合并内容主线 `c4d6bb05569d5beda4ffffe10d4bad78f4f156d8`／tree `ca39fd9ab6da5ac461ffb3368b43adac04075761`；原候选46/46（27push＋19PR）、最终候选19/19PR、合并内容主线27/27push Actions均已真实成功，INTEGRATION66专项实测成功。个人Library原236张候选PNG私有242成员zip重新取回SHA/CRC全吻合；原历史CURRENT blob `c89e0e33537990aa2132b47c40fef49a985a935c`不变。机器回执见[运行清单](research/recovered/STONEAGE-INTEGRATION66-PUBLICATION-ACCEPTANCE-R1.json)。本验收记录自身新HEAD Actions需另查，不预支成功；Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暂停、完成率未知；下一步新内容来源。


## 2026-11-11 — INTEGRATION67｜精灵王事件3份原GetPet×台湾1.0真原宠物像素

[原脚本—宠物—原SPR/RD来源边界](docs/continuity/STONEAGE-INTEGRATION67-SPIRIT-KING-THREE-PET-PIXELS-20261111.md)与[公开数字/散列/动作和原RD资格](research/recovered/STONEAGE-INTEGRATION67-SPIRIT-KING-THREE-GETPET-TW1-ORIGINAL-PIXELS-R1.json)：私人QUEST29原ZIP实读138/138 CRC，原 `king/event69_1`／`event69_24`／`event69_7` 的3条真实GetPet行分别为355/484/1479。对照已验同社区mixed25 enemy1→enemybase1主表的原SHA，模板图号分别100376/100430/100451；进一步用**另一台湾1.0零售** PET07原SPR/RD实物重新核9条动作/方向序列、74个原帧位置及48张已保存原PNG，每图原RD/PNG SHA和尺寸均通过，原帧顺序u32le SHA全同；原RD新解码0。私人56成员437505B ZIP已保存Library并独立回取全SHA/CRC，商业图像/脚本不入Git。该跨载体同图号不等于官方早期同服、物种身份或实际领奖；原CURRENT完整旧blob不改，Stage A7 PARTIAL＋2 OPEN，Stage B/wiki GATED，R79暂停，overall_percent=null。NEXT改查另一个未重复且真正有原实物的地图/NPC/道具/宠物连接，不做网服/引擎；候选与主线Actions另据后验验收。


### INTEGRATION67 实际远端内容验收（2026-11-11）

[正式合并及完整运行回执](docs/continuity/STONEAGE-INTEGRATION67-PUBLICATION-ACCEPTANCE-20261111.md)：[PR #336](https://github.com/chinaneedM/stoneage-rebuild/pull/336)合并源内容 `74c06b7a8360424c4d6344cb3858c8b194afc13d`／tree `411d7c53d6b7d52e77827f76e30cdc904e79f353`，候选46/46（27push＋19PR）与内容合并后main **27/27 Actions** 实际completed/success，专项 run42999969506 success。私人56成员437505B/48原PNG已从Library独立复验SHA/CRC；完整CURRENT旧blob未变。后验收据自身新HEAD的Actions不得预支。Stage A7PARTIAL＋2OPEN、B/wiki GATED、R79暂停、完成率未知；NEXT新的原实物内容。


## 2026-11-11 — INTEGRATION68｜四村保护石任务四NPC原图号与TW1.0原RD像素候选

[来源有界原件、真正独立解码及PRIVATE源像保管](docs/continuity/STONEAGE-INTEGRATION68-FOUR-VILLAGE-QUEST-NPC-PIXELS-20261111.md)／[公开数字/80B源索引/RD像素散列与负证](research/recovered/STONEAGE-INTEGRATION68-FOUR-VILLAGE-QUEST-NPC-FOUR-TW1-ORIGINAL-PIXELS-R1.json)：从 `main=9af43766f...`／tree `3987b6a...`与其26/26成功Actions重新启动，完整读取旧CURRENT Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`（2,709,173B，**未改**），先对旧QUEST31 4个保存版创建记录查重。真正整SHA复验原QUEST31私人包27,565B与TW1 retail P3H私有源包372,626,292B；**新重解码4份原TW1 RD**：原mixed25四创建图号16205/16206/16203/16057分别经原ADRN+76唯一别名精确对应物理5925/5926/5923/5903，实际像素40×93/36×94/32×87/36×66，双解码逐原索引一致，4图已目视；同号物理块是另外图，不能以编号直接互代。私人11成员24,425B ZIP已保存个人Library并独立回取整SHA/CRC，原RD/PNG/CREATE/HTML没有进Git；10项公开源/否证专项本地通过，候选/main CI仅能据实际远端后验。此关联**不是**后期社区mixed25与官方TW1同服、原NPC形象/原任务执行、实际调色板或已完成完整世界；floor1300源DAT缺件仍OPEN。Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暂停、总体完成率null。**NEXT** 继续另一非重复有真正原件可见的地图/宠物/物品/技能关系，不复查本四像素、不开网服/账号或新引擎。


### INTEGRATION68 正式验收回执（2026-11-11）

[真实PR与内容主线/私人保管验收](docs/continuity/STONEAGE-INTEGRATION68-PUBLICATION-ACCEPTANCE-20261111.md)：[PR #338](https://github.com/chinaneedM/stoneage-rebuild/pull/338) 已squash合并，候选 `1183c2699af967ec37471614e0e53dc66bad4fe5` 的 **46/46 Actions**（27push＋19PR）以及正式内容main `9b4ace498f6083e963eb78b9dcb7fecb365b6641`／tree `473b7cbdef41f5a94bfced7380bbb79383a99426` 的 **27/27 Actions**均已实际成功，INTEGRATION68专项候选push、PR和main成功。私人11成员24,425B原像/RD ZIP从Library独立回读整SHA和CRC吻合，原历史CURRENT blob `c89e0e33537990aa2132b47c40fef49a985a935c` 未变。全部73条运行ID和状态归档在[机器验收回执](research/recovered/STONEAGE-INTEGRATION68-PUBLICATION-ACCEPTANCE-R1.json)。这份回执提交自身的Actions以后续实际结果为准；Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79暂停、overall_percent=null。NEXT非重复且具真实来源的其它二维内容。


## 2026-11-11 — INTEGRATION69｜三件被盜家寶：event13兩NPC／五道具／七幅TW1原RD像

[完整源材料、原腳本控制字面和私人原像重讀](docs/continuity/STONEAGE-INTEGRATION69-EVENT13-HEIRLOOM-ORIGINAL-NPC-ITEM-PIXELS-20261111.md)／[公開有限原證JSON](research/recovered/STONEAGE-INTEGRATION69-HEIRLOOM-EVENT13-NPC-ITEM-TW1-PIXEL-SOURCE-R1.json)：重新從 `main=899c69e573e349ed404b8a3d1362c499cfad73f2`／tree `083cf8dc657c8f83bbc360c8890da2132b172436` 的26/26成功Actions與完整原CURRENT Git blob啟動。舊QUEST01已索引兩腳本5段，故本輪新增腳本0；真正新增的是後期mixed25保存的 `event13n.create` 兩條有SHA原NPC與ACT／REQUEST／MESSAGE／CLEAN腳本、五件原物品兩套94欄的關係，並以不同TW1零售原ADRN/REAL真源重新解碼7幅候選(2NPC/5物品)、雙獨立RD解碼完全一致、5舊物品保存PNG逐RGBA一致。兩NPC源地圖1112有舊MAP09 DAT資格、1100在本955批次無匹配；不能稱官方同服、原生NPC／任務執行或失蹤的1100不存在。原 `CLEAN:13` 靜態條件未經實測，不用其發明原旗標/重複觸發語義。私人31成員75,935B原腳本/RD/PNG已存個人Library後完整回取SHA/CRC合格，原商原件不入Git。Stage A7 PARTIAL＋2 OPEN、B/wiki GATED、R79暫停、overall_percent=null。NEXT轉其他具合格原件的遊戲內容，不擴本事件或開發網服/引擎。候選/main Actions須按實際遠端後驗。

### INTEGRATION69 真实正式验收（2026-11-11）

[PR与私人源保管正式验收](docs/continuity/STONEAGE-INTEGRATION69-PUBLICATION-ACCEPTANCE-20261111.md)：[PR #340](https://github.com/chinaneedM/stoneage-rebuild/pull/340)已squash合并，候选 `8c9a7421662b8a573900d78a7116863677b7a75c` **46/46 Actions**（27push＋19PR）和内容主线 `d933def55effcf041ac58b899cde157b9ca35930`／tree `418f8c90167dd2ea9e7145b8452ae0efe25c741f` **27/27 main Actions** 都真实completed/success，包含INTEGRATION69三处专项push/PR/main均通过。私人31成员75,935B原脚本/原TW1 RD/PNG保管ZIP在个人Library独立回读SHA/CRC完全相同；原历史CURRENT blob `c89e0e33537990aa2132b47c40fef49a985a935c`未改。全部73项精确运行身份见[机器验收回执](research/recovered/STONEAGE-INTEGRATION69-PUBLICATION-ACCEPTANCE-R1.json)。本回执自身新HEAD CI不得预支成功。Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79暂停、overall_percent=null；NEXT未重复真实原件内容。


## 2026-11-11 — INTEGRATION70｜恐龙博士哈鲁的两阶段原始资料和八项真正原像候选

[来源和边界](docs/continuity/STONEAGE-INTEGRATION70-HARU-EVENT15-SOURCE-20261111.md)／[数字与SHA证据](research/recovered/STONEAGE-INTEGRATION70-HARU-EVENT15-TWO-STAGE-NPC-EIGHT-ITEM-TW1-PIXEL-SOURCE-R1.json)：已独立读取私人混合后期载体源 event15.create（2原NPC在11006）和2原脚本，恢复事件15/16的DelPet、GetRandItem（8候选物品ID）、GetPet:95静态来源链；与两份已验原itemset及另一台湾1.0零售已解码8幅RD候选图源关联。私人12成员ZIP 15,265B已上传个人Library并独立重取SHA/CRC全同；新原RD二进制解码0、原脚本新发现0、无实际原服执行或官方同服认证。历史 CURRENT 完整旧blob不改，Stage A 7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、总体率null。NEXT转另一不重复且有真实原件的游戏内容；PR/CI结果以后验为准。

### INTEGRATION70 实际GitHub验收（2026-11-11）

[正式验收与私人源证独立回读](docs/continuity/STONEAGE-INTEGRATION70-PUBLICATION-ACCEPTANCE-20261111.md)：[PR #342](https://github.com/chinaneedM/stoneage-rebuild/pull/342) 已合并，候选 `23a0cce9a7092896c8ec492d57e7356338e7962c` **46/46 Actions**（27 push＋19 PR）及内容主线 `1b10144a3a14dbec2753072a8f02e9f260d4afac`／tree `027b897f6b6b1bd268936dc91cb894a507bccc57` **27/27 Actions** 均真实 completed/success（含专项 run43020555960）。私人12成员15,265B原源／旧原图ZIP已自Library独立回读SHA/CRC全相同；公开Git仅源数字/散列，旧完整CURRENT blob `c89e0e33537990aa2132b47c40fef49a985a935c`原样保留。73个实际run身份存[机器回执](research/recovered/STONEAGE-INTEGRATION70-PUBLICATION-ACCEPTANCE-R1.json)，本验收回执自身的后续HEAD CI另按实际后验。Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暂停、完成率未知；NEXT 非重复原二维内容来源。


## 2026-11-11 — INTEGRATION71｜查罕族祭司、五件原物品和「神秘的調和水」五幅原RD候选

[新源限定合成关系](docs/continuity/STONEAGE-INTEGRATION71-CHAHAN-PRIEST-TIGER-WATER-20261111.md)／[公开数值、SHA与反证](research/recovered/STONEAGE-INTEGRATION71-CHAHAN-PRIEST-TIGER-WATER-ORIGINAL-SOURCE-R1.json)：真正核私人 mixed25 NPC2205成员与 ITEM01838成员全部CRC，原查罕族祭司在10007 的1份`tiger_water.arg`含3段原**MESSAGE**，其中一个消息块含5项`DelItem`与`GetItem:19563*1`；原ITEM01六ID的94栏双表源行SHA对应到不同认证TW1零售来源的**五幅此前已解原RD真像**，5/5 PNG和RGBA复验，2400/19563两物品共图23012。原floor10007和10408有MAP09已验DAT但同CREATE其它2位windowman并非同脚本。私人9成员45,710B证据ZIP已存Library且独立回读整SHA和CRC；公开无原图、台词及源原文。无原脚本新发现/新RD二进制解码或原生交易/合成/早期同服证明。历史CURRENT原blob `c89e0e33537990aa2132b47c40fef49a985a935c`保持，Stage A 7PARTIAL/2OPEN、B/wiki GATED、R79暂停、总体完成率null；候选和主线Actions按真正后验另记。

### INTEGRATION71 正式远端内容验收（2026-11-11）

[查罕族祭司真实Actions/私人源证正式回执](docs/continuity/STONEAGE-INTEGRATION71-PUBLICATION-ACCEPTANCE-20261111.md)：[PR #344](https://github.com/chinaneedM/stoneage-rebuild/pull/344)候选 `b5bfe1d9a76e2619c12cbb0e1f5780a508225cfc` **46/46** Actions (27 push＋19 PR)和内容主线 `d10e39f60c492151860523f67515ba88d5749eee`／tree `b3551a1c1402b987f5d28b7a17f17e96b70021cb` **27/27** Actions均已实测成功，包括INTEGRATION71专项。私人9成员45,710B源和既存TW1原像ZIP已自Library独立回读完整SHA/CRC；公开只保留源数值与SHA、未修改历史CURRENT blob `c89e0e33537990aa2132b47c40fef49a985a935c`。完整73条实际run ID见[机器验收](research/recovered/STONEAGE-INTEGRATION71-PUBLICATION-ACCEPTANCE-R1.json)。此验收记录自身新HEAD的Actions另待后验；不把来源条件当旧服实际合成。Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总体进度未知；NEXT 真新原实物内容。


## 2026-11-11 — INTEGRATION72｜梦幻洞窟四物品原图候选来源关联

[有界原NPC/四物品/台湾1.0原RD候选源证](docs/continuity/STONEAGE-INTEGRATION72-DREAM-SAGE-FOUR-ITEM-PIXELS-20261111.md)／[公开SHA数值证据](research/recovered/STONEAGE-INTEGRATION72-DREAM-SAGE-FOUR-ITEM-TW1-ORIGINAL-PIXEL-SOURCE-R1.json)：依据本次fresh main `7dcfdb85526756551d54ae342e40196f6b675dc7`/tree `ec9771cc7acdb55167003bcf7aa422a8a0315c6e` 与26/26成功Actions，真正重读私人社区混合25 NPC ZIP 2205CRC和ITEM01 ZIP 838CRC，老人原REQUEST项2603对应仙人三段DelItem2603→GetItem2604/2605/2606来源静态合同；两份94列原物品表8行原SHA及4个不同TW1零售原RD保存图PNG/RGBA 4/4本轮重核，分别别名14648/21000/21531/24212、物理5600/6301/6396/6979。新原脚本0、新RD从原REAL解码0、原游戏执行0、同官方部署认证0。私人12成员18371B源证ZIP存个人Library并独立回读完整SHA/CRC；原图、台词、完整商品数据不入公开Git。完整旧CURRENT blob `c89e0e33537990aa2132b47c40fef49a985a935c` 未改，Stage A 7PARTIAL＋2OPEN，Stage B/wiki GATED，R79暂停，整体percent=null。NEXT转其它未重复、真实来源就绪的原2D游戏内容；本次正式候选/main CI仅按远端实际完成结果后验。


### INTEGRATION72 正式候选、主线及私人保管验收（2026-11-11）

[梦幻洞窟四物品来源关联的远端验收回执](docs/continuity/STONEAGE-INTEGRATION72-PUBLICATION-ACCEPTANCE-20261111.md)： [PR #346](https://github.com/chinaneedM/stoneage-rebuild/pull/346)已合并，候选 `92f84e5bcf326d58fd885f558abbc9edbdf24f25` **46/46**（27 push＋19PR）与内容主线 `2a1ae4c754a73393a30155961695829b3dc50c9b`／tree `11a2a80d7c14eb908752d7f391d2ca6f48896ed6` **27/27** Actions 均实测 completed/success，含三处 INTEGRATION72 专项。全部73个真实运行ID见[机器回执](research/recovered/STONEAGE-INTEGRATION72-PUBLICATION-ACCEPTANCE-R1.json)。私人原NPC/物品/4幅已解台湾1.0候选PNG组成的12成员18,371B ZIP已经个人Library独立回读整SHA/CRC；原版权资产未公开。原CURRENT `c89e0e33537990aa2132b47c40fef49a985a935c` 未变，Stage A 7PARTIAL＋2OPEN、B/wiki GATED、R79暂停、overall_percent=null。该回执自身新HEAD Actions不预支；NEXT另转未做过、真实材料合格的游戏内容。


## 2026-11-11 — INTEGRATION73｜萨姆吉尔五枚勾玉／英雄祝福原来源关系

[原NPC与12幅早期原像候选的限定接缝](docs/continuity/STONEAGE-INTEGRATION73-SAMUGIRU-FIVE-GEMS-HERO-BLESSING-20261111.md)／[来源数值、逐段SHA与负证](research/recovered/STONEAGE-INTEGRATION73-SAMUGIRU-SOURCE-12-ORIGINAL-ITEM-PIXELS-R1.json)：基于全新main `924e3502`/tree `860a0950` 与26/26实际成功Actions，私人mixed25 NPC 2205/2205 CRC与ITEM01 838/838 CRC实回读；`poru/hero.create` floor5501连接`poru/samugiru`（10原段），`poru/samugiru01.create` floor1013连接`poru/girl`（7原段），5种原交付物→5枚不同勾玉→首饰18537与英雄祝福18543的原字面静态关系。12份原A/B物品行、12个不同TW1零售原RD PNG候选已保存并本轮整SHA/尺寸复核；本轮无新RD解码/原生脚本执行/官方同服认证。尤其首饰与五份祝福的源字面数量、NOWEV/ENDEV63差异及未直接创建引用的samugiru_test对照保留。31成员/58,292B私人原件ZIP已存个人Library并独立回读CRC/SHA，原图/商业台词/原94列不公开。完整CURRENT原blob不变，Stage A7PARTIAL＋2OPEN、Stage B/wiki GATED、R79暂停、整体进度null。下一项轮换不重复的实际原2D游戏内容；专项及主线Actions成功后再做正式验收。


### INTEGRATION73 正式候选、主线与私人原件验收（2026-11-11）

[萨姆吉尔五勾玉／12台湾1.0原像候选正式验收](docs/continuity/STONEAGE-INTEGRATION73-PUBLICATION-ACCEPTANCE-20261111.md)：[PR #348](https://github.com/chinaneedM/stoneage-rebuild/pull/348)已squash合并。候选 `768d2d1b2e8f492165eef14d931faf2ca5a04991`／tree `14c57050a8db35483490637ffae7340c618391ab` **46/46 Actions**（push27/27、PR19/19）与内容主线 `46553a6a8d98b62423cb12f5fce623035897c36b`／同tree **27/27 Actions**真实全部success，专项三个job各实录12项测试OK。全部73个运行ID见[机器回执](research/recovered/STONEAGE-INTEGRATION73-PUBLICATION-ACCEPTANCE-R1.json)。私人58,292B/31成员原NPC/物品94栏/12原RD候选图包已上传个人Library后独立回取全SHA/CRC通过；商业原文字/原图不入Git。原CURRENT `c89e0e33537990aa2132b47c40fef49a985a935c` 未改，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、整体完成率null；正式验收收据本身Actions不预支，NEXT另寻未重复且有实物的历史2D内容。


## 2026-11-11 — INTEGRATION74｜愿藏桥上敌人NPC与两组真实TW1完整SPR动作的来源限定联接

[原始NPC两角色↔完整二维源动作与私人像素观察](docs/continuity/STONEAGE-INTEGRATION74-YUANZANG-TWO-TW1-FULL-MOTION-20261111.md)／[源SHA及160段动作、576原RD物理图证据](research/recovered/STONEAGE-INTEGRATION74-YUANZANG-TWO-TW1-FULL-MOTION-SOURCE-R1.json)：以fresh main `ad2e6efd586231eff46e016b4a99539f1d316b76`/tree `8fc03d5627cfa395b83fe284ce3b5345e194b1fe` 与26/26成功Actions为起点，重取mixed25 NPC 2205CRC和认证TW1 P3H 372626292B/379CRC，逐整SHA核原SPR/ADRN/REAL，源NPC floor100/graphic100401、实例253/254→模板500/501→图号100401/100280的后期社区静态内容与不同来源TW1图号候选相连；完整原组104+56序列/496+288帧位置/344+232不同物理RD实读并私人展示，575 strict、1原RLE有界异常82729。PET15已覆盖全部这些原图：**新历史独特美术0、新物种0**，31个PET07重合源RD/ADRN/索引SHA相等，RGBA预览31/31一致但原PNG字节编码不同。581成员1826064B私人包已存Library并独立回取整SHA/CRC；浏览器内存160选择、0JS/0外部请求，file://和localhost直接导航被宿主安全策略禁止，不虚称成功。原版同服/NPC原生对话战斗/地图100/原调色板仍OPEN，版权原图/原脚本和私有观察页不公开。原CURRENT完整Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`保持原样，Stage A 7PARTIAL＋2OPEN、B/wiki GATED、R79暂停、总体percent=null；待正式候选/main CI后验。NEXT另寻非重复且有真实原件增量的其它内容。


### INTEGRATION74 正式候选、主线与私人源保管验收（2026-11-11）

[原愿藏两名敌人图号来源／160段台湾1.0原动画验收](docs/continuity/STONEAGE-INTEGRATION74-PUBLICATION-ACCEPTANCE-20261111.md)：[PR #349](https://github.com/chinaneedM/stoneage-rebuild/pull/349)已squash合并，候选 `bf2a42ef1b39f1f777b91a719560b7e2dad92fa9`／tree `a5efaf2ecc8bd185802ab7c2ce5e4542a8ab4d31` **46/46 Actions**（push27＋PR19）与内容主线 `cb42b8b076a9639c73a4f2463600e7c7d54e2b3c`／同tree **27/27 Actions**真实completed/success，三次专项实际job各12项测试OK。全73条真实运行收据见[机器回执](research/recovered/STONEAGE-INTEGRATION74-PUBLICATION-ACCEPTANCE-R1.json)。真实重读台湾1.0原SPR/REAL 576不同RD（575 strict、1限定尾零），但PET15已有全部这些原图，此轮新美术0；成果是O85具名后期NPC/敌人两模板→另一载体TW1两组全动作的有据资料接缝。私人1,826,064B/581成员包已Library独立回读SHA/CRC；版权原图/脚本不进Git。原CURRENT `c89e0e33537990aa2132b47c40fef49a985a935c` 保留，Stage A7PARTIAL＋2OPEN、B/wiki GATED、R79暂停、overall=null。正式验收回执自身Actions不预支，NEXT转未重复的真正原始游戏内容。


## 2026-11-11 — INTEGRATION75｜长毛象神社抽签六原物品源关系

[原脚本及六神签来源边界](docs/continuity/STONEAGE-INTEGRATION75-MAMMOTH-SHRINE-SIX-FORTUNES-20261111.md)／[源数字与SHA](research/recovered/STONEAGE-INTEGRATION75-MAMMOTH-SHRINE-SIX-FORTUNES-SOURCE-R1.json)：社区mixed25四原脚本已真实重读、2205 ZIP CRC成功；原抽签15列表位置→6种神签原ID，静态旗标36及捐献50；既存ITEM01两原表六物品整SHA相同、源图号24313在TW1零售原索引缺失，新增原图0、原服实际执行与每日重置/抽中概率未认证。保留原CURRENT完整Git blob和Stage A 7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、总体完成率未知。专项及主线Actions只以后验记录；NEXT其它有真原件、未重复的二维游戏内容。


### INTEGRATION75 实际候选、主线、私人源保管验收（2026-11-11）

[神社六枚神签来源关联正式验收](docs/continuity/STONEAGE-INTEGRATION75-PUBLICATION-ACCEPTANCE-20261111.md)：[PR #350](https://github.com/chinaneedM/stoneage-rebuild/pull/350)已squash merged，候选 `4d89f8a0ffea7f4552e6051c6255050f5875bd6f`／tree `25a75944ff681787b64ac2370152604af5b24278` **46/46** Actions（27 push＋19 PR）与内容主线 `abc895b8bab29f98df7145d1123edc26c684af95`／同tree **27/27** Actions均实际success，3次专项各9项测试OK。全部73个真实run ID存[机器回执](research/recovered/STONEAGE-INTEGRATION75-PUBLICATION-ACCEPTANCE-R1.json)。原NPC/物品源的小型私人整理包8102B／11成员已存个人Library并独立取回逐字节SHA/CRC通过，原脚本与94栏转录未公开。全部抽签原列表只是15处字面，真实概率/每日刷新/原生执行与TW1图号24313均未证；不算新增原RD。旧CURRENT Git blob不变，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总体完成率null；验收收据自身新HEAD Actions另按实际后验。NEXT非重复的真实二维游戏内容。


## 2026-11-11 — INTEGRATION76｜周年生日蛋糕停用NPC配置与原版二维蛋糕图候选

[原脚本、四处注释的CREATE及原图源证](docs/continuity/STONEAGE-INTEGRATION76-ANNIVERSARY-CAKE-ORIGINAL-PIXEL-20261111.md)／[无版权SHA、数值和负证](research/recovered/STONEAGE-INTEGRATION76-ANNIVERSARY-CAKE-ORIGINAL-IMAGE-SOURCE-R1.json)：从fresh main `7356d728f4e3d4ad564c694e89059b9f6a39dab5` / tree `dc408d8740145d5efa7f33f87867ad4bf38a9e01` 与26/26成功Actions启动。真正重读私人mixed25 NPC 2205成员及 ITEM01 保存转录838成员ZIP CRC；原cake脚本两段对应 ITEM13030，四处floor1000/2000/3000/4000生日蛋糕 NPC CREATE **全部源行注释**，不得谎称原服部署。旧两物品表ID13030完整SHA相同，图别名24409在独立台湾1.0零售原REAL已有1,341B/56×36真实RD及旧2,837B候选PNG；本轮PNG/RGBA整SHA重核，新原RD解码0、新美术0。私人7成员7317B原脚本/原行/原图包已存Library并独立回读SHA/CRC；原图、脚本、94栏与观察页未公开。未认证官方周年年份、真实原游戏发放或当时NPC画面。原CURRENT 2709173B全历史blob不变；Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总体percent=null。本轮CI以远端后验记，NEXT转不重复且有真实原件的其它2D游戏内容。


### INTEGRATION76 正式候选/main Actions及私人来源验收（2026-11-11）

[周年生日蛋糕停用原NPC／台湾1.0原候选像素正式回执](docs/continuity/STONEAGE-INTEGRATION76-PUBLICATION-ACCEPTANCE-20261111.md)：[PR #351](https://github.com/chinaneedM/stoneage-rebuild/pull/351)已squash合并，候选 `6888d3e373315ecf518c71936bbbd59f8133bba0`／tree `ec413768b0dc1e61fd04542d57b51a727daa7d1f` **46/46 Actions**（27 push＋19PR），内容主线 `97388fd9c28ed4d77089db94a852f0f8f9c5a1c2`／同tree **27/27 Actions**均真正success，三次专项各9测试通过；全部73真实run ID见[机器收据](research/recovered/STONEAGE-INTEGRATION76-PUBLICATION-ACCEPTANCE-R1.json)。原社区mixed25 576B周年脚本→后期原物品13030，原633B四个floor CREATE整段被注释；台湾1.0老RD位图6576/56×36候选源原PNG重新核SHA，新增原像0、原服实际活动仍OPEN。7成员7317B私人原脚本/物品行/PNG已存个人Library且独立回读SHA与CRC全同。旧CURRENT blob保持，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停，整体percent=null。本正式回执自身CI另按后验；NEXT其它真实原二维内容。


## 2026-11-12 — INTEGRATION77｜长毛象大厅19份原NPC创建与演出证件证据边界

[19处NPC创建、15份同原件参数、四工作人员通行条件及无直接引用的两份演出证据](docs/continuity/STONEAGE-INTEGRATION77-MAMMOTH-HALL-SOURCE-20261112.md)／[公开派生源证](research/recovered/STONEAGE-INTEGRATION77-MAMMOTH-HALL-ORIGINAL-SOURCE-R1.json)：重新私人核对保存的社区mixed25原NPC ZIP 2205/2205 CRC，原 floor116 16个＋floor117 3个配置，15/15 `file:` 指向同ZIP实物。原四人员 `ITEM=2608`／`ITEM!=2609` 仅为静态条件；`syutuen` 的2608发证与`karikari` 的2703发证都未在该ZIP找到直接创建引用，不能认定生效或同物异号；真实游戏触发与同官方版本仍OPEN。本次新原2D像素0、原服务器执行0；私有原NPC不公开，旧CURRENT blob `c89e0e33537990aa2132b47c40fef49a985a935c`未改。Stage A7 PARTIAL＋2 OPEN，B/wiki GATED、R79暂停、总体percent未知。下一优先转另外有原实物的非重复可视内容；正式CI按远端后验另记。


### INTEGRATION77 正式远端验收与来源保管（2026-11-12）

[真实PR/main CI、73条运行和原始文件保管边界](docs/continuity/STONEAGE-INTEGRATION77-PUBLICATION-ACCEPTANCE-20261112.md)：[PR #352](https://github.com/chinaneedM/stoneage-rebuild/pull/352)候选 `3bd58436` 经46/46 Actions（27 push＋19PR），正式内容主线 `413411ad`／tree `d2be756d` 经27/27 Actions，均为实际completed/success。专用push/PR/main三次均实录8项测试OK。完整源ZIP 2205/2205 CRC本轮私有核实，原商业内容不入Git；旧CURRENT完整历史blob原封不动。该验收收据自身CI仍须另行后验。Stage A7 PARTIAL＋2 OPEN、Stage B/wiki GATED、R79暂停、总体完成率未知；NEXT新非重复原二维内容，不重复无直引演出证脚本。


## 2026-11-12 — INTEGRATION78｜骑乘同意书16原物品、四村秘书/训练师与旧TW1真像候选

[来源有界16件文书、九字段制证窗口、四训练师和台湾1.0已存真实原像关系](docs/continuity/STONEAGE-INTEGRATION78-RIDING-CONSENT-ORIGINAL-PIXEL-20261112.md)／[逐ID原行SHA/原CREATE区间与负证](research/recovered/STONEAGE-INTEGRATION78-RIDING-CONSENT-ORIGINAL-ITEM-PIXEL-SOURCE-R1.json)：从远端`main=74aaaccd`/tree`0ba0c825`及26/26成功Actions启动，重新读取完整旧CURRENT Git blob保持不变。真正重读私人社区mixed25原NPC 2205/2205 CRC和先前ITEM01保存目录838/838 CRC；16份骑乘同意书原94字段行分别整SHA验证，**全部仅存itemset0710、原itemset.txt均无**，16件均别名24176。四旧骑师创建/4课程`19005–19008`与四秘书创建/制证窗口9 ID、有源特殊`20296`及另6项仅源行严格分层；旧固定后代源码早已证明骑师letter检查被`#if 0`停用，不复述为新发现或推测初代。台湾1.0零售原RD图号24176→物理6840的旧52×44 PNG实读SHA、尺寸和目视复核，**新原RD解码0、新美术0、原服执行0**。ID20833另为两表共有的兑换券，图号24371在当前TW1索引无匹配，不与24176无证合并。14成员17,977B私人原图/脚本/物品行离线资料包已存个人Library且独立回读整SHA/CRC，原版权没有入公开Git；公开12项来源反例本地通过，远端CI按完成后验。Stage A7 PARTIAL＋2 OPEN、B/wiki GATED、R79暂停、overall_percent=null。NEXT轮换另一非重复真实二维内容，不将文书当成原版必需技能或官方同部署。


### INTEGRATION78 正式GitHub与私人原件验收（2026-11-12）

[真实PR、73项 Actions、源身份和私人Library二次保管回执](docs/continuity/STONEAGE-INTEGRATION78-PUBLICATION-ACCEPTANCE-20261112.md)：[PR #353](https://github.com/chinaneedM/stoneage-rebuild/pull/353)已squash合并，候选 `37c9473002e53ab046aa6d613279b40cdd6b5bb8`／tree `ab85aa434a1a77626dcf0d51b83e51055fb28346` **46/46 Actions**（push27、PR19），内容主线 `8758e0af84eb619d50e5d5c718f0d1e25033e399`／同tree **27/27 Actions**全部实际completed/success，新专项push/PR/main各实录12项测试OK。73条run身份永久存[机器回执](research/recovered/STONEAGE-INTEGRATION78-PUBLICATION-ACCEPTANCE-R1.json)，本验收收据自身新HEAD Actions必须另查。私人17977B/14成员原图/原脚本/骑证完整行资料ZIP已存个人Library并独立重取全SHA/CRC验证；未向公开Git上传原版权资产。历史CURRENT完整原blob `c89e0e33537990aa2132b47c40fef49a985a935c`不变，Stage A7 PARTIAL＋2 OPEN、Stage B/wiki GATED、R79暂停、整体进度未知。NEXT其他真实非重复原二维内容。


## 2026-11-12 — INTEGRATION79｜13家精灵羽毛原商店、27组原传送参数与旧TW1真实原像候选

[13份原NPC与13参数文件、28个原道具ID、56整源行SHA、27组目标坐标及5件洞窟羽毛跨表差异](docs/continuity/STONEAGE-INTEGRATION79-FEATHER-SHOPS-ORIGINAL-2D-SOURCE-20261112.md)／[完整公开来源数值与负证](research/recovered/STONEAGE-INTEGRATION79-FEATHER-SHOP-ORIGINAL-NPC-ITEM-PIXEL-R1.json)：从远端`main=b15bae4c`／tree`a003c48a`与26/26成功Actions启动、完整历史CURRENT原blob不改。原私人mixed25 NPC ZIP 2205/2205 CRC、旧ITEM01保存包838/838 CRC、TW1动作旧包4154/4154 CRC均完整核实。原`shop_nuke1.create`有13创建块直联13原参数；28源道具中27件羽毛均有ITEM_useWarp及4整数目的地，另一件是太阳神首饰非传送。两物品表56/56原94字段行CP950重组SHA完整相符；5个洞窟羽毛**只有图号字段17差异**：旧表全用24076、另一表改24381/24378/24379/24377/24380，后五在已核TW1零售图索引无证。保存TW1羽毛24076、首饰22030、人物16300三旧原像PNG实际读SHA/尺寸/像素；均不是本轮新RD解码，新原美术0，客户端/服务端实际买卖、传送、同部署全OPEN。私人36,546B/76成员原脚本/原行/PNG/纯离线图文包已存用户Library并独立回读整SHA及76/76 CRC；版权内容不入公开Git。本地12项源派生反例测试通过，正式Actions按远端后验。Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暂停、总体percent未知。NEXT轮换未重复真实原二维宠物/武器/地图内容，不扩原服交易/传送引擎。


### INTEGRATION79 正式PR／Actions与私人来源保管验收（2026-11-12）

[13家羽毛商店／28原物品／27目标坐标的来源及73条真实GitHub运行验收](docs/continuity/STONEAGE-INTEGRATION79-PUBLICATION-ACCEPTANCE-20261112.md)：[PR #354](https://github.com/chinaneedM/stoneage-rebuild/pull/354)已squash合并，候选`84ed4bf54ee922f9008ec1e0ef1d84395ceacc44`／tree`ecdb4c982b8812b1bb16d5ff9652766288639ff3`经**46/46 Actions**成功（push27、PR19），正式内容主线`fa9839485eea054c1a12b43f25ca88d279f99eb1`／同tree经**27/27 Actions**成功。专项三轮push/PR/main实录均12测试OK，真实73条run ID/HEAD/时间见[机器验收](research/recovered/STONEAGE-INTEGRATION79-PUBLICATION-ACCEPTANCE-R1.json)。私人原NPC/物品原行/三张旧真实原图的36,546B／76成员ZIP已存个人Library，**独立重取整SHA与76/76 CRC成功**；版权内容未公开。五洞窟羽毛图号跨表仅一列差异、旧原RD解码0、同服原生传送未证。完整CURRENT原Git blob`c89e0e33537990aa2132b47c40fef49a985a935c`保持不变；Stage A7PARTIAL＋2OPEN、Stage B/wiki GATED、R79暂停、总体percent未知。本验收收据自身新HEAD Actions需独立后验。NEXT换真实未重复原二维游戏内容。


## 2026-11-12 — INTEGRATION80｜dungeon03 原13处静态传送创建 × 5份地图原格 × 4张已有原2D场景候选

[真实原RAR、13处原NPC创建、5份原DAT及四原2D场景来源对照](docs/continuity/STONEAGE-INTEGRATION80-DUNGEON03-ORIGINAL-WARP-FIVE-DAT-20261112.md)／[逐块源字节区间、SHA、逐原格三平面及方向反例](research/recovered/STONEAGE-INTEGRATION80-DUNGEON03-NPC-WARP-DAT-SOURCE-R1.json)：从本次远端main `9d058513`／tree `f0935bdd`、本HEAD 26/26成功Actions及完整旧CURRENT Git blob重新启动。个人Library真实取回社区mixed25原RAR 361255180B并核整SHA；直接解原 `dungeon03.create` 1621B及五份原 `40/31301/31302/31401/31501.DAT`，全部与旧MAP09真实DAT档案原字节/全SHA一致。原13个活跃 `npcgen_warp` 创建分布九层、文本上5对互逆；五份本批核过的DAT有9处起始、9处目标原格可读，5条边两端都有原格；精确原值、反向关系和有界缺件逐条保存。旧MAP09有四张TW1零售RD加mixed25 DAT现代原二维候选场景，已私人目视而非原生客户端；floor40只有原DAT无此来源合格旧全图。本批新原RD解码0、新原美术0、原服创建/传送/行走0，旧来源不能偷换为官方同部署。**本轮14项来源及反例专项测试本地通过**；正式PR/main Actions以新运行的实际后验为准。原RAR/DAT/PNG均不公开，历史CURRENT完整blob `c89e0e33`未变。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、overall_percent=null；NEXT选择另一真正不重复原2D游戏内容，有原服实际运行/触发证据才重开这13条传送。


### INTEGRATION80 正式GitHub Actions和私人原件回读取证（2026-11-12）

[13条原创建、五份原DAT与静态传送关系的验收回执](docs/continuity/STONEAGE-INTEGRATION80-PUBLICATION-ACCEPTANCE-20261112.md)：[PR #355](https://github.com/chinaneedM/stoneage-rebuild/pull/355)候选 `853a7279c17cfe50f2355a309417f6e7aa1bd818`／tree `70d850346bc10051dea85119662fdf00cf0b3be2` 经 **45/45 Actions**（push26、PR19）成功，正式内容主线 `7d793560d4a8b112484091d77bb0cffa9a80d210`／同tree经 **27/27 Actions** 成功，专项PR/main两次真实日志均为 **14 tests OK**；72条run记录和来源SHA见[机器验收](research/recovered/STONEAGE-INTEGRATION80-PUBLICATION-ACCEPTANCE-R1.json)。11成员/105583B私人原NPCCREATE、五DAT与四张已存原RD现代合成候选缩略图，已上传个人Library并独立取回SHA及CRC、成员SHA全同，公开Git没有原版权内容；本验收收据自身CI须再单独核验。旧CURRENT完整blob不变，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、总体完成率未知。NEXT其他未重复真实2D内容，不将静态warp确认为原生可通行。


## 2026-11-12 — INTEGRATION81｜九份猜拳NPC原件、九张原DAT和九张可见但缺五图的二维场景

[九原NPC/九原参数/九原DAT × 35张旧已验原RD的来源限定部分实绘](docs/continuity/STONEAGE-INTEGRATION81-JANKEN-NINE-ORIGINAL-PARTIAL-2D-SOURCE-20261112.md)／[逐原CREATE SHA、九参数/九地图、五缺图索引和完整现代画布SHA](research/recovered/STONEAGE-INTEGRATION81-JANKEN-NINE-ORIGINAL-PARTIAL-2D-SOURCE-R1.json)：fresh `main=ca26b05c`/tree `15fa34d0`，当前HEAD 26/26 Actions成功、旧CURRENT Git blob完整重读不改。原私人社区mixed25 RAR全SHA再核，真读`janken.create`的9条活跃NPC创建及9份287B `file:` 原参数，源组拉伊奇/布拉姆/札克羅各3层，9项均`EntryItem:2751*1`，胜负仅原三数字Warp目标；过去Janken模型已知，本轮不重建原服务器规则。MAP09已存原955DAT包里真实读九份不同50×50原DAT/每份3平面，台湾1.0已有原像素候选35图逐原PNG/RGBA SHA核对，九份每张523次>99图引用中518次有源原像素，5次（9420-9423/10940）缺后期原REAL流，九场景合计4662源图块出现、45处留缺。已**实际合成18份带/不带现代标记候选画面**，独立NumPy逐完整RGBA核验9/9同；九原DAT不同但当前有证最终画布只有**3种不同RGBA**。五缺图在原mixed25 ADRN各唯一且均位于TW1认证公共前缀以外；实际后期REAL成员读0字节报`Invalid symbol`，新增原RD0、全新原美术0，不伪造缺件也不宣布原游戏完整地图/原服运行/官方同版。私人16,080,715B/76成员观察包已存个人Library并独立取回全SHA、CRC76/76、内部75项SHA全同，原版权原图/原DAT/原NPC参数不入公开Git。17项本地测试通过，正式PR/main Actions按真实后验。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、overall_percent=null。NEXT后期合格REAL真字节可得再补五图，否则转其他非重复真实二维内容，不扩猜拳规则或新引擎。


### INTEGRATION81 正式GitHub和私人原件验收（2026-11-12）

[猜拳九场景518/523原像素候选、5缺图与真实Actions验收](docs/continuity/STONEAGE-INTEGRATION81-PUBLICATION-ACCEPTANCE-20261112.md)：[PR #356](https://github.com/chinaneedM/stoneage-rebuild/pull/356)候选 `18206b8a2e999cccc5f4e34adcb5256a4442c0cf`／tree `a8cee304c1e7f43b18241d793146f41480932c2b` **46/46 Actions**（push27、PR19）success；正式内容主线 `8381be0c5da7a1bd452f3fbb3cc9d31b13f93e7b`／同tree **27/27 Actions** success，新增专项 push/PR/main 三次真实日志均为 **17 tests OK**，73个run收据见 [机器验收](research/recovered/STONEAGE-INTEGRATION81-PUBLICATION-ACCEPTANCE-R1.json)。私人16,080,715B/76成员九原DAT+NPC参数+35张旧RD候选+18现代二维画面包已存个人Library并独立重取整SHA、76CRC/75成员SHA全同；不上传原商图/脚本。九原DAT各不同但已验证9个现代画布仅3种可见像素；五张后期缺RD仍OPEN、原REAL读0字节报`Invalid symbol`不称原包坏。完整CURRENT blob保持、Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、整体percent=null。本验收回执自身新HEAD Actions另按实际后验；NEXT轮换非重复原2D宠物/物品/任务内容。


## 2026-11-12 — INTEGRATION82｜九张猜拳原DAT三平面差异完整来源保管

[九份原DAT的第一平面13处数值差异](docs/continuity/STONEAGE-INTEGRATION82-JANKEN-DAT-PLANE-DELTAS-20261112.md)／[完整九图三平面SHA公开派生记录](research/recovered/STONEAGE-INTEGRATION82-JANKEN-DAT-PLANE-CUSTODY-R1.json)／[私人原件独立CRC/SHA与GitHub发布后验](docs/continuity/STONEAGE-INTEGRATION82-PUBLICATION-ACCEPTANCE-20261112.md)：个人Library私有源包16,080,715B/76成员已实际复取且全CRC、全SHA相符，九原DAT各15008B，逐原5000B平面复核第一平面2种/其余各9种；802→807有13/2500格精确差异，原静态事实不提升为原生渲染/碰撞/猜拳触发。PR #357经候选2/2真实PR Actions成功并合入main `4fe800a444`/tree `d1a6be09`；该合并HEAD最初无新增Actions，旧SHA成功不能冒称其验收。新原RD解码0，缺后期五图与官方同服均OPEN，原商业资产未上Git。旧CURRENT完整保留、Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总体进度未知；NEXT另一非重复原二维宠物/物品/任务内容。


## 2026-11-12 — INTEGRATION83｜1009／4009兩處素材市場十原商店與45幅既存TW1原RD候選

[十處原CREATE、十份真原參數／123原物品／6個明確缺圖](docs/continuity/STONEAGE-INTEGRATION83-1009-4009-MATERIAL-MARKET-20261112.md)／[逐原CREATE字節區間與完整SHA、商店原ItemList、物品行及45原RD候選圖的公開來源索引](research/recovered/STONEAGE-INTEGRATION83-1009-4009-ORIGINAL-MATERIAL-SHOP-2D-SOURCE-R1.json)：fresh遠端`main=d74f56f4`／tree`6d7642bd`起，舊CURRENT完整原blob`c89e0e33`未改。私人NPC原件ZIP995176B/2205CRC及ITEM01原件ZIP5868386B/838CRC本批實讀，兩原CREATE全SHA與十處原塊字節界限逐源核實；CP950中文字節誤中原位元組`}`的初始8/10分塊法已訂正，最終10/10原商店成立，另外兩寄放店不併入。兩floor各5原店、五組對應ItemList逐字同而完整十參數SHA全異；6明列ID出現＋32段原區間（含端點假設256候選），262候選出現／去重123物品；兩原物品表123×2完整原行各SHA同，117個物品ID連已取得TW1零售45原RD候選PNG實核像素SHA，餘4個ID=2個原RD解碼失敗別名與2個ID=2個TW1索引缺失別名，不能捏造原圖。私人現代原像源觀察ZIP156739B/69CRC/68非清單SHA已Library獨立回讀，同包45舊候選原圖／十原參數／123原行選摘，原版源私有不公開，新原RD解碼0、原商城/官方同部署OPEN。本地13項契約反例測試OK，正式CI後驗分SHA記，不預報成功。Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暫停、總percent未知；NEXT輪換不重複合格原2D寵物／物品／任務資料。


### INTEGRATION83 正式PR／Actions與私人原件保管（2026-11-12）

[兩處原素材市場的73條GitHub真實運行、13項專用測試三輪及私有原檔回讀驗收](docs/continuity/STONEAGE-INTEGRATION83-PUBLICATION-ACCEPTANCE-20261112.md)：[PR #359](https://github.com/chinaneedM/stoneage-rebuild/pull/359) 候選 `1960688af3020cf3bfe8974d93a43b8801bb8c24`／tree `69064a00e97d59027f0bb40edb7aee28a2582ab8` 經**46/46 Actions**（27 push、19 PR）均completed/success；正式內容main `60f8650628ae19d9e5fba97408e11d4579a4d7b9`／同tree經**27/27 Actions**均success，專項三輪實際日誌各**13 tests OK**；73條run與SHA綁定永久見[機器回執](research/recovered/STONEAGE-INTEGRATION83-PUBLICATION-ACTIONS-R1.json)。私人ZIP156739B/69成員在個人Library獨立取回全SHA/CRC/68項內容SHA成功，保留10原CREATE/10參數/123ID兩份原行、45既存TW1真RD候選與6缺圖負證，原商用圖、原創建全文不上公開Git。原 `CURRENT-STATE.md` 2,709,173B Git blob `c89e0e33` 完整不變，Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暫停、總percent未知。此新回執提交自身的CI需另驗；NEXT輪換非重複真實原2D寵物／物品／任務來源。


## 2026-11-12 — INTEGRATION84｜JBA 20712 九原NPC、六參數與54幅既存台灣1.0原二維物品候選

[原來源、完整負證與私人原像素保管](docs/continuity/STONEAGE-INTEGRATION84-JBA-ORIGINAL-SHOP-2D-20261112.md)／[九原CREATE逐字節位置、六原參數SHA、60物品ID與54幅既存原RD候選來源索引](research/recovered/STONEAGE-INTEGRATION84-JBA-ITEM-SOURCE-R1.json)：從全新遠端main `fb5ce1db`／tree `8dbb7568` 起，完整CURRENT歷史Git blob `c89e0e33` 真讀且不修改，最新main自身26／26 Actions全success、無PR。私人NPC 2205／2205及物品838／838原ZIP CRC和完整SHA重核；原`shop_event2.create`的floor20712共9原CREATE連4店舖與2寵技真原參數。三店有獨立 `ItemList:` 行合計44原ID，第四店的另16原物品號僅嵌在 `itemfull_msg` 裡，不能稱為實際售貨欄位。兩寵技原數字12／9，合計21，未證原技能執行。60不同物品ID全連先前已保管TW1零售54幅跨來源原RD PNG候選，逐原像SHA實重核，**新增RD解碼0**；原伺服器／JSS/TW1官方同部署、交易、NPC行為仍OPEN。私人57成員112511B候選原像資料 ZIP SHA `b6ec3b9122cc9d037f68988d0b9e9875745973ad94b3ac76faa20a23349c5f4f` 存個人Library且獨立取回整SHA／CRC全部成功；原圖／原參數全文不入公開Git。15項本地公開元數據來源負例測試通過；PR/main CI須依實際後驗單獨記錄，不能預支。Stage A7 PARTIAL＋2 OPEN、Stage B/wiki GATED、R79暫停、overall_percent=null不變。**NEXT** 已驗 JBA 源鏈有界止點，轉另一不同真正原2D寵物／物品／任務內容，只有原native解析／執行證據才重開16內嵌文本候選，不臆造原服上架。


### INTEGRATION84 正式主線／73條Actions與私人原像保管驗收（2026-11-12）

[九原JBA NPC與二維原候選的完整正式驗收](docs/continuity/STONEAGE-INTEGRATION84-PUBLICATION-ACCEPTANCE-20261112.md)：[PR #360](https://github.com/chinaneedM/stoneage-rebuild/pull/360) 候選`2daed99b`／tree `b93f26fa`經46/46成功（27push＋19PR），正式內容main `201e9a848`／**同tree**經27/27 Actions completed/success。三次專項push/PR/main run `43229416339`/`43229468428`/`43229724656` 均success，73條逐真實SHA/事件/run收據見[機器JSON](research/recovered/STONEAGE-INTEGRATION84-PUBLICATION-ACCEPTANCE-R1.json)。原source ZIP 2205+838 CRC、120份94欄CP950重組SHA及54份TW1真原圖候選已私核；57成員112511B私人包在個人Library獨立重取全SHA／CRC通過，原商業內容未入Git；`itemfull_msg`嵌16 ItemList ID仍非經證實上架。完整CURRENT原Git blob `c89e0e33`保持，Stage A7 PARTIAL＋2 OPEN、B/wiki GATED、R79暫停、overall_percent未知；本收據自身CI須另查，NEXT轉不同不重複真正原二維內容。


## 2026-11-13 — INTEGRATION85｜四方守護者兩類原NPC／四勾玉／兩石像與22幅既存真正原二維候選

[20原 NPC 配置／事件檔 CP950 實物、12個 NPCEnemy與4個 changeevent分層、四勾玉與16個石像來源獎勵、22張原圖資格](docs/continuity/STONEAGE-INTEGRATION85-FOUR-GUARDIAN-SHRINE-2D-20261113.md)／[逐CREATE原位元組區間、12原 battle arg、4原勾玉事件、2石像共用事件、20物品雙表及 TW1 原圖完整SHA](research/recovered/STONEAGE-INTEGRATION85-FOUR-GUARDIAN-SHRINE-ORIGINAL-2D-R1.json)：從遠端main `cb0626c866`／tree `18dab1d064`、同SHA 26/26 Actions成功與0開放PR啟動，歷史CURRENT完整Git blob `c89e0e33` 真讀不改。私人原社群 mixed25 NPC2205/2205 CRC、ITEM01838/838 CRC和 TW1 PET07 15MB 原像資料全SHA重讀；同源 `sb_4sin.create` 3個floor31603/31606/31609各4個NPCEnemy及十二arg、`nev1_1.create` 在31609另有4不同坐標原 changeevent NPC 和31610兩石像，共12+4+2原 CREATE。四 changeevent原GetItem/ITEM條件=2528地／2529水／2530火／2531風；兩石像共用原`nev1_5`，文字有四DelItem及16個GetRandItem候選，不證原native選獎、概率、戰鬥或同部署。四勾玉及16候選獎勵共20 ID ×兩原94欄行=40整SHA確認，其中6 ID原欄30/31異；跨分離來源TW1零售實讀18物品RD原PNG與4原SPR幀PNG共22幅，逐PNG SHA/原RGBA/尺寸核同，**本輪新原RD解碼0**、無新商業美術。私人ZIP137532B／46成員已Library獨立取回整SHA／46CRC/45個成員SHA成功，原商用圖／NPC事件原文不公開；新增21項公開原數值反例測試本地OK，GitHub PR/main Actions依後驗記錄。Stage A7 PARTIAL＋2OPEN、Stage B/wiki GATED、R79暫停、overall_percent=null。**NEXT** 轉另一真正未重複原二維內容家族，只以新增同版本實物或原native運行證據重開此NPC/條件/勾玉觸發語義，不把此現代觀察器叫原遊戲。


### INTEGRATION85 正式主線及73條 Actions／私人來源終驗（2026-11-13）

[四方守護者來源限定、73條真正成功 GitHub Actions 與私人原像保管驗收](docs/continuity/STONEAGE-INTEGRATION85-PUBLICATION-ACCEPTANCE-20261113.md)：[PR #361](https://github.com/chinaneedM/stoneage-rebuild/pull/361) 候選 `f980cc04`／tree `145f498e` 經27/27 push＋19/19 PR全部成功，正式內容 main `ed58e02c`／**同tree**經27/27 push完成success。新增21項公開測試於候選push／PR／主線三次真實log均 `Ran 21 tests / OK`，73條真實 SHA/事件/run ID收據見[機器JSON](research/recovered/STONEAGE-INTEGRATION85-PUBLICATION-ACCEPTANCE-R1.json)。私人源NPC2205CRC／ITEM838CRC／TW1 22原像候選、40份94欄原行 SHA 都合格；私人137532B／46成員原圖包已Library獨立回讀整SHA及46CRC／45成員SHA成功。原商用圖與NPC正文未上Git；新原RD解碼0、原服／世界未執行。歷史CURRENT原2,709,173B Git blob `c89e0e33`不變，Stage A7 PARTIAL＋2 OPEN、B/wiki GATED、R79暫停、整體percent未知。此驗收提交自身新HEAD CI另查；NEXT輪換非重複原2D寵物／物品／任務內容。


## 2026-11-13 — INTEGRATION86｜漆黑洞窟五考古事件、兩守護獸、精靈王與19幅既有真正原二維候選

[來源限定實讀：8洞窟 CREATE＋2獨立 NPCEnemy／5份考古腳本16段／兩份不同轉生參數](docs/continuity/STONEAGE-INTEGRATION86-SIKKOKU-ORIGINAL-QUEST-2D-20261113.md)／[逐原CREATE/事件字節界限及SHA、19原物品35行雙表、16物品原RD與3原SPR、負證完整索引](research/recovered/STONEAGE-INTEGRATION86-SIKKOKU-SOURCE-2D-R1.json)：從遠端 `main=58e182f2`／tree `8709843f`、最新26/26 Actions成功與0 PR啟動、完整歷史CURRENT原Git blob `c89e0e33`實讀且不變。已重驗私人原NPC 2205/2205 CRC、ITEM01 838/838 CRC與 TW1 PET07 全原像HTML SHA；原 community mixed25 洞窟八NPC包括五位各不同樓層考古家、精靈王及兩護士，另兩原守護獸 NPCEnemy 為不同來源CREATE，兩個原參數的靜態目標32011/32021不證原生戰後傳送。五份考古事件16 TYPE段，前四各原文字面GetItem 2771–2774；第五事件53原 `EVENT` 要求2701/2707/2735/2770，**卻原 `DelItem` 為2701/2702/2703/2704**，交集僅1，不能擅修或認定已成功執行。原 `GetItem` 20570–20572在第一主表不存在、第二主表有確切原94欄行；19個原物品ID總35原行SHA實重組，台灣1.0實存16原物品PNG和3個原SPR候選像素各驗真SHA，共19幅既有原圖，另3原alias 20241/24314/24315當前 TW1 索引缺件，**新RD解碼0／新美術0**。五考古檔註釋都稱16樓但原創建樓層32002/6/9/14/16不同；精靈王實指 `777/ten.arg`，非另存 `sikkoku/ten.arg` 且兩檔真SHA不同。前者有寵物二次轉生後不能騎乘的源文本警告，**無原native可操作證據**。私人源文件+原圖/現代離線查閱ZIP 113454B／35成員／SHA `1433a5638f2e7358b39a5d2955cb706a8bd48082467e5d781ba37238f1b43b70` 已存個人Library、實際獨立回讀全SHA／35CRC／34檔SHA同，原商業腳本/圖不公開；新增21正反契約本地PASS，GitHub候選/main另按真後驗。Stage A7 PARTIAL＋2 OPEN、Stage B/wiki GATED、R79暫停、overall_percent=null。**NEXT** 再輪換另一非重複且有真原件的原二維寵物／任務／物品內容，只有原程式實執行證據才重審此EVENT/DelItem、二次轉生騎乘等規則。


### INTEGRATION86 正式Github來源與73條Actions／私人原像保管終驗（2026-11-13）

[漆黑洞窟10原NPC、16來源事件段、原EVENT/DelItem負證、19既存真原二維候選與GitHub正式驗收](docs/continuity/STONEAGE-INTEGRATION86-PUBLICATION-ACCEPTANCE-20261113.md)：[PR #362](https://github.com/chinaneedM/stoneage-rebuild/pull/362) 候選 `16911a67`／tree `f24ceaf2` 真實經27/27 push＋19/19 PR Actions成功，正式內容 main `3fc574ef`／同tree經27/27 Actions成功，合計73條按SHA的確切執行收據見[機器JSON](research/recovered/STONEAGE-INTEGRATION86-PUBLICATION-ACCEPTANCE-R1.json)。專用來源契約21項於候選push/PR/main三次真job log均顯示 `Ran 21 tests / OK`。私人原NPC 2205CRC／ITEM838CRC、35原94欄行 SHA／19張TW1既存真原PNG均重驗，另三TW1別名缺圖。私人113454B/35成員原源離線包已Library獨立取回整ZIP SHA／35CRC／34成員SHA通過，原商業原文／原像未入公開Git；新原RD解碼0、原生世界未進入。CURRENT原2,709,173B blob `c89e0e33`完整不變，Stage A7 PARTIAL＋2OPEN、B/wiki GATED、R79暫停、總percent未知。**本驗收收據提交自身CI另按該HEAD後驗**；NEXT轉另一有真原2D與原配置且非重複的遊戲內容家族。


## 2026-11-13 — INTEGRATION87｜36個GetPet原靜態數值→台灣1.0真正原SPR二維候選完整來源索引

[原來源及負證報告](docs/continuity/STONEAGE-INTEGRATION87-36-GETPET-TW10-2D-CENSUS-20261113.md)／[完整36組逐原行及動畫SHA](research/recovered/STONEAGE-INTEGRATION87-36-GETPET-TW10-SPR-2D-BRIDGE-R1.json)：以遠端main `40e857168`／tree`f47fcb0a`啟動，原CURRENT全2,709,173B／Git blob `c89e0e33`真讀不改。原社群mixed25 WORLD21資料27原腳本、44條GetPet字面、36不同原獎勵實例按其原enemy→enemybase的字段數值連到36不同原圖形號，**另一來源台灣1.0 PET07**的130組原SPR中恰36組同數值、原段SHA/動作0、2、1方向0共108條序列可定位。三份現存私人原資料全SHA重驗，混合2.5原CP950 36/36原欄位數值直接吻合；沒重拉父RAR、新原像素解碼=0、新寵物物種確認=0。`GetPet1481`／graphic100401動作0含原位圖82729嚴格RLE解碼越界，不能冒稱所有原動畫可看。INTEGRATION62／66／67已個別核過20源實例，原數值關係不當官方同服或實際發獎。Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暫停、overall_percent=null不變。**NEXT** 轉另一非重複有真實原件的原二維內容家族，不做引擎／新遊戲或無據物種推測。

### INTEGRATION87 正式主線／修正後Actions與兩條原失敗永久保留（2026-11-13）

[PR #363](https://github.com/chinaneedM/stoneage-rebuild/pull/363) 初候選 `b84ebcae` push+PR **兩次真failure**，原因為一條「不是原生執行」負證測試正反極性錯誤；修正候選 `a5780b7b`後，專項push `43362998905`及PR `43363002385`均6/6測試PASS，兩條共存O11/O12 PR工作流亦success（候選合計4/4），內容正式main `aebb5405fbedff10a5705ff32bf2f658af728f0f`／同tree `c0f5481eab88bb3ae245e3862cbc180cddd10ee1` 的專項 `43363096290`亦6/6 PASS。原失敗不追認，**此驗收接收提交自身CI另據後驗**。全部精確RUN、SHA、4新檔blob、私人實物哈希與OPEN界限見[永久接受收據](research/recovered/STONEAGE-INTEGRATION87-PUBLICATION-ACCEPTANCE-R1.json)和[文字報告](docs/continuity/STONEAGE-INTEGRATION87-PUBLICATION-ACCEPTANCE-20261113.md)。完整原CURRENT不改，商業原源和2D私有像素不公開，最高NEXT保持更換真原2D內容族。


## 2026-11-13 — INTEGRATION88｜三隊營地／原三個門衛通行證／99原CREATE與57真二維原像候選

[INTEGRATION88源實物、私人可見原像及不確定性](docs/continuity/STONEAGE-INTEGRATION88-TEAM-CAMP-ORIGINAL-2D-20261113.md)及[99原位元組span/46來源引文/44直接Warp/三門票雙原物品master/四組SPR原SHA](research/recovered/STONEAGE-INTEGRATION88-TEAM-CAMP-GATE-WARP-ORIGINAL-2D-R1.json)：從fresh main `a1a0ac45`／tree`e9e7ba46`、最新26/26成功Actions與0PR啟動，完整CURRENT原2,709,173B／Git blob `c89e0e33`真讀、保持原樣。保存的後期社群mixed25原NPC 995176B私ZIP 2205/2205 CRC通；原`genout/500npc_m.create`14674B完整SHA及99個逐原byte span SHA對已驗CHAR01一一成立。99 CREATE含**55有圖形NPC配置、44無圖`npcgen_warp`**；46原`file:`目標全部真讀整SHA。三個原守門條件分別`FREE:ITEM=18553/18554/18555`、原`WARP=5532(0,22)/5536(30,13)/5533(30,11)`、`MONEY:-1`，只屬原靜態資料；三件原ID亦與同來源雙94欄原物品主表整行SHA及TW1舊已解圖號24124/24126/24127接通，不認定通行證實際生效／哪份主表在原服跑。29配置數字對應**不同來源TW1**四組100259/100379/100401/100432的已保存真原SPR候選；**57幅**真原PNG每圖SHA/尺寸全部核同，PRIVATE純離線查閱頁可見75源幀位置；原全101幀位置中100401動作0含RD82729嚴格越界，26幀不造圖；另100406有10配置不在PET07取樣、非早期原整體缺圖證據。私人349552B觀察ZIP已個人Library上傳及獨立回取完整SHA/2CRC，Chromium真測0JS/0外部網絡；原商業原圖與原NPC正文0入公有Git。新原RD解碼0、原native世界未進入、同部署未知，Stage A7PARTIAL+2OPEN，Stage B/wiki GATED，R79暫停，overall_percent=null。

### INTEGRATION88 Github正式驗收及私人來源保管收據（2026-11-13）

[PR #364](https://github.com/chinaneedM/stoneage-rebuild/pull/364)已squash merged。源候選 `23157bf1`、item加入`6f37d043`、測試加入`82d36347`各真實push/PR專項成功且旁路O11/O12 PR通過；最後候選`9b2aca10`受路徑觸發的**3/3 PR Actions成功**，專用11項測試全部PASS，正式內容主線`0966aee017e54cbb23ea37a270ff2c7449395ee1`／tree`94e1e942f29130930a6aa258bf3a7142fe3076e2`對應專用push run`43389211693`/job`131764836061`實際completed/success、原日志`Ran 11 tests / OK`。全部15條候選實際成功run與1條主線、blob及私人整SHA見[永久機器收據](research/recovered/STONEAGE-INTEGRATION88-PUBLICATION-ACCEPTANCE-R1.json)及[文字驗收](docs/continuity/STONEAGE-INTEGRATION88-PUBLICATION-ACCEPTANCE-20261113.md)。**本驗收收據提交本身的Actions另行真核，不預支成功**；完整原CURRENT未動，下一個最高NEXT選別的有真實來源之2D內容家族，不重複此99配置或擴新引擎／MMO。


## 2026-11-13 — INTEGRATION89｜恐龍牧場三洞窟原等級/手環門檻、四店參數與真原二維圖像不同調色板反例

[35原CREATE/三守門/四店/兩份舊原物品主表的SHA及跨來源SPR證據](research/recovered/STONEAGE-INTEGRATION89-DINO-CAVE-GATES-SHOPS-ORIGINAL-2D-R1.json)與[來源實物範圍及各類PNG核驗限度](docs/continuity/STONEAGE-INTEGRATION89-DINO-CAVE-ORIGINAL-GATES-SHOPS-2D-20261113.md)：從重新驗過的main `324c303a`／tree `fcbf782a`、當時26/26成功Actions與0 PR啟動，原CURRENT2,709,173B／Git blob `c89e0e33`整原文讀出、不改舊歷史。新題材不是上一批三隊營地或既有牧場領寵三條件，而是**後期社群mixed25原`npc/genout/bait_01.create`5743B**的35逐原byte窗原CREATE：20 `npcgen_man`、7標牌、3守門、3限售商店、1普通商店、1公告。私人NPC原ZIP2205/2205CRC與16來源arg全部逐字節完整SHA真核。原`FREE:LV>4`、`WARP:20901,0,8`；`ITEM=2595`紅手環→floor20902；`ITEM=2596`藍手環→floor20903；同原保存雙94欄主表手環及店鋪`ItemList12856`各源行SHA皆具；三層肉品收購原`sell_rate`字面0.8/0.7/0.6、原`LimitItemNo:1234-1249`保留原值，不推原服扣費/出貨/玩家實際通行。另一不同來源真正TW1零售SPR10原組/18同數字CREATE候選，公開舊PET07動作方向0 **30段/250幀出現/168原bitmap**有SHA定位。本輪私人舊图库**532PNG候選**全部可重讀，與新原RD選中來源逐圖比對：嚴格**116張PNG SHA同一**，三人物組另**52張不同調色板候選PNG SHA不一致**，其餘**364張不在較新的選取來源報告內**；不謊稱532張均本輪原RD解碼驗證，**新原RD解碼0**。私有離線資料包1,482,192B/SHA256 `a43da4967959afbf593bf3e9319421d13b752c1082fd4d103ab94ace8d4e9090` 已存Library並獨立回下載全SHA+2成員CRC成功，內嵌JS `node --check` PASS；本執行環境Chromium嘗試逾時，瀏覽器功能未驗，不能冒稱成功。私人原對話/原PNG/商業源原文皆未入公開Git。Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暫停、overall_percent=null不變。最高NEXT輪換不同的有真原件2D內容族，不重複洞窟三門/三店，也不擴MMO/新引擎。

### INTEGRATION89 主線/來源永久驗收（2026-11-13）

[PR #365](https://github.com/chinaneedM/stoneage-rebuild/pull/365) 已squash merge，內容正式main `9562fa1d017b343204059e23fbfaa0caef50bc89`／tree `16981ddba998ca59954c8ccce8575cbfcea4c747`，候選末HEAD `57094774abc5c658d1ea2a7424a1549c761d6fa7`／同tree；同HEAD專用push`43393655769`／PR`43393709123` + O11`43393709181`、O12`43393709365` 四條Actions均真success，專用兩次實際日誌均 `Ran 11 tests / OK`。主線內容push `43393854866`／job`131779944693` 真completed/success且 `Ran 11 tests / OK`；不可把先前26條全重算在這個內容SHA。完整精確SHA/runID、私人原ZIP及候選PNG負證由[機器驗收收據](research/recovered/STONEAGE-INTEGRATION89-PUBLICATION-ACCEPTANCE-R1.json)與[主線驗收文檔](docs/continuity/STONEAGE-INTEGRATION89-PUBLICATION-ACCEPTANCE-20261113.md)永久保存。**驗收收據提交自身CI須以其HEAD後驗，不預支成功。**原CURRENT完整blob保留。


## 2026-11-13 — INTEGRATION90｜波魯龍王殿 24 原配置、24 原 DAT 格、92 真 TW1 圖像候選

[完整 source-only 24 條原 CREATE/DAT 格、五 ARG 及六組原 SPR／92 PNG SHA 收據](research/recovered/STONEAGE-INTEGRATION90-PORU-DRAGON-HALL-SOURCE-2D-R1.json)與[實物、保管、獨立 Chromium 原圖觀察、原版限制](docs/continuity/STONEAGE-INTEGRATION90-PORU-DRAGON-HALL-SOURCE-2D-20261113.md)：遠端初始 main `19e81df26af2b8dc2883573109d29065e8fc0f42`／tree `29bc247ff4f73523076dec714ed37d7ed5237f1b` 的 26/26 Actions success，0 PR；原 CURRENT Git blob `c89e0e33` 完整 2,709,173B 保留。後期社群 mixed25 原 `poru/boss.create` 3771B SHA 真取 **24/24 靜態建立塊**、5 不同原 ARG SHA、5511 23條／5510 1條；原 DAT 5511 30×30與5510 60×60 實物 SHA 重讀，24個出生坐標真核原三連續u16平面，末欄5511=49152共23條、5510=49154一條，不偷作碰撞語義。5510守衛 boss.arg 原文字面 10 個敵人 ID、目標 `5511,6,24`，不證真正戰鬥/傳送。不同來源TW1零售真SPR數值接6圖形組，**18源動作／187源幀位置／92不同原位圖候選PNG與PET07 RD派生源SHA嚴格92/92相同**，新原RD解碼0，非本原商服同部署。私有3391913B觀察ZIP SHA `a59c516a...` 已 Library 上傳與獨立回取全SHA/10CRC、Chromium實測24條目/72操作/0JS/0網絡，原圖/腳本/DAT不公開。先前 INTEGRATION58 已查龍王索引0／事件63，本輪不算新機制。Stage A 7PARTIAL+2OPEN、B/wiki GATED、R79暫停、percent=null，NEXT 轉別的源真二維內容，不重做本殿或洞窟。**候選 GitHub Actions 與正式 main 後驗須另據真 run 記錄，不在本條預支成功。**


### INTEGRATION90 正式驗收收據（2026-11-13）

[PR #366](https://github.com/chinaneedM/stoneage-rebuild/pull/366) 已合併，內容正式main `31daa8e79962a93ea790862d79c98ffaede607ce`／與候選 `97a4d4724c77996fefbfa1f29f2de0bc4d895e26` 同tree `2173bb71ef16770ccb192635c0c56198b4d4f7b9`。候選 push/PR **46/46** 真實成功 Actions、main 內容SHA **27/27** 真實成功 Actions，專項兩條候選及main一條日誌均真正 `Ran 11 tests / OK`。逐 run ID／事件／精確 SHA 及原來源實物驗收見[永久 JSON](research/recovered/STONEAGE-INTEGRATION90-PUBLICATION-ACCEPTANCE-R1.json)和[驗收報告](docs/continuity/STONEAGE-INTEGRATION90-PUBLICATION-ACCEPTANCE-20261113.md)。私人3391913B ZIP 全SHA/10CRC獨立回驗，原原圖及DAT未公開；完整原 `CURRENT-STATE.md` blob `c89e0e33` 原樣不動。此收據新 HEAD Actions 須另核不可預支，Stage A 7PARTIAL+2OPEN、B/wiki GATED、R79暫停、總percent=null，NEXT 原來源不同二維家族。


## 2026-11-13 — INTEGRATION91｜長毛象客運 6 原車輛及 300 真原路線點 × 台湾1.0 真原 100355 全 56 動畫 248 原圖候選

[來源限定實物跨模組報告](docs/continuity/STONEAGE-INTEGRATION91-MAMMOTH-BUS-2D-20261113.md)及[35源文件／六原 CREATE byte spans／6段路線 SHA／原SPR 248圖 SHA彙總](research/recovered/STONEAGE-INTEGRATION91-MAMMOTH-BUS-ORIGINAL-2D-R1.json)：以遠端主線 `6a6a4ffc196afffd37ee25fa45361d6dc6f86bb1`／tree `ed3cd0869b2da88536fb48972cf85714a0803685`、26/26同SHA Actions成功及0PR、完整原 CURRENT 2,709,173B blob `c89e0e33` 重讀而未改啟動。重新真讀私人後期 mixed25 NPC ZIP全SHA/2205CRC、原35份 O86 公車源 14116B 逐原SHA，六個原 CREATE 全字節窗SHA與 CHAR01 公有記錄嚴格一致，原數字圖號全為 **100355**、floor100/200各3輛；6路源原 300 座標點與費用50/25/30/50/20/40、waittime180、原403 vs 2403/CP950壞字節等負證不改。另一來源經驗 TW1零售 PET11真正原圖號100355完整 SPR 段 7072B SHA合格，**56真源動畫／640源帧位置／248個不同RD圖**，該組之前248 RD已嚴格解碼，本輪只將現存私有彩色/灰度PNG各248張的真正byte SHA重新全核、兩套都248/248吻合；新RD解碼0、同部署/原服行車0證明，與後期PETFLG0和捕捉鍵8僅不同來源同號候選。私有 **2530925B、37成員** ZIP 已上傳 Library／獨立回下載全SHA與37CRC成功；Chromium真測6條原路線／56方向動作×雙像素模式112載入／56下一幀＋1上一幀，0JS/0外網。真原圖、原路線整坐標與原商業文本只留私有，Git只留衍生數字SHA。Stage A7PARTIAL+2OPEN，B/wiki GATED，R79暫停，overall percent=null；**下一最高NEXT**切換不同具真原圖的歷史內容，非再做 Bus 靜態路線、非新引擎/MMO。候選/main GitHub CI 與實際合併依真後驗另記，不預支成功。


### INTEGRATION91 來源正式主線／兩條首試失敗和更正後完全驗收（2026-11-13）

[PR #367](https://github.com/chinaneedM/stoneage-rebuild/pull/367) 已真合併，首次候選 `661e294aaa33a489b9e1a24fe4085f5eac20d65b` 46條 Actions 44成功、**專用push＋PR各1真failure**（僅測試欄名錯誤，原 source未改）；修正末候選 `98568cc33f36d0302217325beb0162be7daa657b`／tree `a4d99484ace607b7e29d1cc3a28d569b61f435c8` **20/20成功**，正式內容 main `0a7b03e4adba4faf6e0a74a5de276c8af770e475`／同tree **27/27成功**。本輪12項原來源合同在候選push／PR／main三份真 job logs 均 `Ran 12 tests / OK`，不可把舊兩失敗追認成功。Bus6車原 byte span／35保管原文本／300原路線點／TW1 100355全56動作640幀位置248舊原RD圖與此次248彩色＋248索引灰度 PNG逐SHA／私人2530925B ZIP Library雙取全SHA/37CRC／實測Chromium6路線112圖顯示0錯誤詳細見[永久機器驗收](research/recovered/STONEAGE-INTEGRATION91-PUBLICATION-ACCEPTANCE-R1.json)及[文字驗收](docs/continuity/STONEAGE-INTEGRATION91-PUBLICATION-ACCEPTANCE-20261113.md)。舊CURRENT原blob `c89e0e33` 2709173B完整保存，Stage A7 PARTIAL＋2OPEN／Stage B/wiki GATED／R79暫停／percent=null。**此次验收回执提交自身CI另以新HEAD核验**。NEXT换其他已获真原2D内容，不假认巴士原运行。


## 2026-11-13 — INTEGRATION92｜五兄弟地下城30原NPC与5个原TW1二维奖励角色候选

[源资格与私人原二维真图实测](docs/continuity/STONEAGE-INTEGRATION92-FIVE-BROTHERS-ORIGINAL-2D-20261113.md)及[30CREATE/30脚本 SHA链、5原SPR完整段、15候选原动画、86原RD/PNG SHA链](research/recovered/STONEAGE-INTEGRATION92-FIVE-BROTHERS-ORIGINAL-2D-R1.json)：从远端 main `072604a3620bb2da2f7666d7895059baa86ed349`／tree`fe8ded71b96bb0386bb78a17350920608195b48e`、26/26 Actions成功、0PR与完整旧CURRENT 2709173B原blob启动。私人后期mixed25原NPC ZIP995176B/2205CRC、`giiru/event/ev28.create`5199B及30份原脚本30333B逐真源SHA再验，六楼30源NPC坐标与旧QUEST20的DAT几何静态一致。第六层5既有 GetPet源关系对应100287/290/288/289/394；独立TW1零售原SPR五组各56动作头只选每组三段方向0，**15源动画／123帧位置／86原RD候选PNG逐真实PNG SHA86/86同于PET07既有来源**；本轮新RD解码0、无原生领奖或同官方部署结论。私人660522B SHA`b734904c...`、36成员原图/原脚本离线包已Library独立上传下载再核36CRC/全SHA、Chromium144六楼图与15原动作0JS/0外网。原商用图/台词不公开。Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、整体百分比未知。NEXT换其他可见真实原2D内容，GitHub Actions候选/main须另真验收。


### INTEGRATION92 五兄弟原2D現實私源／來源驗收正式main（2026-11-13）

[PR #368](https://github.com/chinaneedM/stoneage-rebuild/pull/368) 真合併。候選 `7140a81cb5b8512027dc34ceab0068d348502d28`／tree`038b21aa5732fa01591bb51ffa80d5394847b4b0` **46/46 真Actions成功**，專項push/PR兩次實日誌均12/12 OK；內容主線 `f3f35595367329ce1a22af41b0ac194bac77539f` 同tree **27/27 真成功**，專項push日誌12/12 OK。原混合25私NPC源2205CRC、30逐byte CREATE與30腳本30333B真SHA，另TW1原PET07五組每56原動畫頭只選方向0每組3動作、源15段123原幀位置86不同原RD候選PNG的逐張SHA86/86真正同，新的RD解碼0；私人660522B/36成員ZIP存Library並獨立回讀全SHA和36CRC、Chromium6樓地點/15動作實顯0JS/0網路，原始遊戲/同官方部署仍未證。版權原商圖/台詞不入Git，完整CURRENT原blob c89e0e33原樣保存，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暫停、percent=null。[永久驗收JSON](research/recovered/STONEAGE-INTEGRATION92-PUBLICATION-ACCEPTANCE-R1.json)、[文字驗收](docs/continuity/STONEAGE-INTEGRATION92-PUBLICATION-ACCEPTANCE-20261113.md)。**收據新HEAD自身Actions另核不預支**；下一NEXT換另一真源2D內容。


## 2026-11-13 — INTEGRATION93｜floor1212四原NPC數值×台灣1.0真原2D候選

[來源驗證、實際私人原圖和現代查閱](docs/continuity/STONEAGE-INTEGRATION93-FLOOR1212-FOUR-ORIGINAL-2D-20261113.md)與[純來源SHA／數值可核公開表](research/recovered/STONEAGE-INTEGRATION93-FLOOR1212-ORIGINAL-2D-R1.json)：fresh main `991d2ba643fd5155165f3ebc99ab3cec183b07c9`／tree `b290cc7f6ae2e4d9c7ac2eac0791a0a8ff36b20d`，0開放PR與原2,709,173B CURRENT Git blob `c89e0e33`不動。後期社群mixed25 `genout/nevent_03.create` 四源CREATE位於floor1212 (12,19)/(14,19)/(16,20)/(18,19)，圖號100326/100265/100259/100294；只復核前期CHAR01原byte-span SHA索引，本輪原CREATE原文實讀0。另一來源TW1真原SPR四組56動畫原段，僅12源動作/方向0、96原幀位置、70不同已存真原PNG逐字節SHA/尺寸重驗，新原RD解碼0。私有474,219B／72 CRC包SHA `ffcee80fc069ec364af35422bdb54b1c951091c7129637f373f356e81686ca50`，Chromium實測四卡12操作、0JS/0外網（用page.set_content，file/localHTTP導航被阻擋，不能稱原瀏覽器文件導航成功）。真正原2D/商用腳本不入公開Git，不證跨版本同官方部署／原生NPC／碰撞／原世界。Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暫停、overall_percent=null；**NEXT**換不同有真原2D實質內容，候選/main Actions及合併均真後驗另記。


### INTEGRATION93 真正合併／73條Actions與私人原像獨立保管驗收（2026-11-13）

[正式驗收](docs/continuity/STONEAGE-INTEGRATION93-PUBLICATION-ACCEPTANCE-20261113.md)／[73條逐run真實收據](research/recovered/STONEAGE-INTEGRATION93-PUBLICATION-ACCEPTANCE-R1.json)：[PR #369](https://github.com/chinaneedM/stoneage-rebuild/pull/369)候選`d9989f9df20f`／tree `e8f13440b0fb` 實核46/46 Actions成功（push27+PR19），專項雙log均Ran 7 tests OK；squash後正式main `3694774daec8`／**同tree**另27/27 Actions completed/success，專項主線真log亦7 tests OK。私人474219B／72CRC真原圖包已上傳個人Library `/石器时代/`，並**獨立回讀**原SHA `ffcee80fc069ec364af35422bdb54b1c951091c7129637f373f356e81686ca50`整字節一致；真正70/70 PNG SHA原像、四卡十二次Chromium互動合格。原商業圖／原腳本不進Git，後期社群NPC原始字節本輪未重新讀、原TW1同部署未證。完整原CURRENT blob `c89e0e33`不變。Stage A7 PARTIAL+2OPEN、B/wiki GATED、R79暫停、overall_percent=null；本驗收追加本身CI另按新SHA核，不預支。**NEXT**不同真原2D來源家族。


## 2026-11-13 — INTEGRATION94｜六楼层18原NPC创建配置×15组台湾1.0真原二维候选

[原20,491B CREATE与18配置／六楼层图目／245张原RD候选PNG逐SHA对照及私人真浏览器](docs/continuity/STONEAGE-INTEGRATION94-SIX-FLOOR-ORIGINAL-NPC-TW1-2D-20261113.md)／[公开来源原段和逐RD/PNG SHA](research/recovered/STONEAGE-INTEGRATION94-SIX-FLOOR-18-NPC-TW1-ORIGINAL-2D-R1.json)：fresh main `0def0b661fe5`／tree `06c60d879b5b`、原CURRENT完整2709173B blob `c89e0e33`保留、0 PR/26 Actions成功。私人历史INTEGRATION22/23两个ZIP原`genout/shop_m.create`全20491B同SHA，实际原字节119原CREATE span逐SHA119/119，18条`npcgen_mugon`分在1003/1103/1203/1303/1403/2003六floor 2/2/3/6/2/3；旧MAP04六floor30×30原DAT数值/SHA仅复用、无原DAT新字节重读。不同来源真台湾1.0零售PET07 15 SPR/56动画各源段，选择45段/323原帧位置/245原RD候选PNG实际重读且按SHA、RGBA验收；193幅与旧Palet1候选PNG字节同，**52幅原图库与Palet1 PNG SHA不同**（三组100250/251/252，旧INTEGRATION89已知差异），不静默认成245张相同色盘，**新原RD解码0**。私人1575502B/248成员原图及原CREATE观察ZIP已Library上传并独立全SHA/248CRC回验；真实Chromium18卡×3控件54次、六floor2/2/3/6/2/3、0 JS/0外网，使用page.set_content，非原file://或原native世界。原商用文件与原PNG仅私人保管；原source类型`npcgen_mugon`≠真实原服商店/交易，跨源同图号≠TW1同部署或原版NPC身份。Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79暂停、整体percent未知。**NEXT**另选具真实原版二维源内容且非重复的新家族，不扩MMO或新引擎。候选/主线Actions依真后验另行记录。


### INTEGRATION94 永久主线验收：73条真正成功Actions与私人原源保管（2026-11-13）

[正式验收记录](docs/continuity/STONEAGE-INTEGRATION94-PUBLICATION-ACCEPTANCE-20261113.md)／[46+27逐真实run机器收据](research/recovered/STONEAGE-INTEGRATION94-PUBLICATION-ACCEPTANCE-R1.json)：[PR #371](https://github.com/chinaneedM/stoneage-rebuild/pull/371)候选 `36888674a69d`／tree `0bed1bc820d4` 46/46 Actions成功（27push+19PR），专用两job日志均**Ran 10 tests / OK**；正式内容main `45245681eba6`／**同tree** 27/27 Actions成功且专用job真实10测试OK。后期社群混合25私有原CREATE`genout/shop_m.create` 20491B/119原byte spans全SHA重新实读，两观察ZIP同原文件但非两个版本；18条`npcgen_mugon`/六floor、TW1另来源15原SPR/45源动画/323帧位置/245私有RD派生候选PNG真实重读，**193幅原PNG SHA同旧Palet1、52幅不同**（旧INTEGRATION89负证）。1,575,502B／248CRC源ZIP `1ae2d376a8ca35cad5c19db24bdf71a94d13508dbe3a8894a8d7d62df735989e` 已存个人Library并独立回读整字节/全SHA/248CRC完全合格，Chromium18卡54次控制/0JS/0外网。商用PNG和CREATE不入公有Git；原DAT本轮未重读、原世界与TW1同服未证。原CURRENT完整2,709,173B/blob `c89e0e33`不变，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、整体percent未知；本验收提交自身的Actions另据真实新HEAD核，不预支。**NEXT**其他非重复真原2D家族。


## 2026-11-13 — INTEGRATION95｜原 dungeon00 147源传送配置和64楼层图（真正原字节新领域）

[17,289B原CREATE全源SHA及147原段、117不同方向、53匹配DAT、现代私人离线观察](docs/continuity/STONEAGE-INTEGRATION95-DUNGEON00-SOURCE-WARP-GRAPH-20261113.md)／[147源原创建原位置数值和逐段SHA](research/recovered/STONEAGE-INTEGRATION95-DUNGEON00-147-ORIGINAL-WARP-AND-PRIOR-DAT-R1.json)：fresh main `d22ddcd3bb88`／tree `daace0cccdff`、26/26 exact HEAD Actions成功、0PR；旧CURRENT 2709173字节/blob `c89e0e33`全历史不改。独立取回私有CHAR01 995176B SHA `c35ed126...` 全2205 CRC，从中实读原`npc/genout/dungeon00.create` 17289B/SHA `1b3d189e...`，147个真实原CREATE byte spans逐SHA 147/147，非又重读361MB父RAR（本轮0B）。同原文本字面 140/147具严格反向配置（70对），**7条无严格反向仅源配置止点**，64源floor形成117不同有向关系、5弱/7强静态图分量，非原世界地图或真实可达性。先前同mixed25 955原DAT目录中53/64楼层有SHA/尺寸、11仅本保存源缺DAT；205端点旧DAT尺寸内、**本轮实际新DAT原字节0**，不据此证碰撞或运行。私人10610B/3成员ZIP `0e13f780...` 内真实原CREATE+现代**合成**SVG来源图，已存Library并独立原SHA/3CRC回取；Chromium 5分量/64节点/147配置及搜索点击真实运行，0JS/0外网；非原客户端/原地图图像。Git仅公开数字/来源SHA/9正负回归，不含商用原CREATE原文。Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79暂停、percent未知。**NEXT**新的非重复同载体原任务/地下城资料，初代官方同服/原native传送继续OPEN；候选与主线CI按实际验收不预支。


### INTEGRATION95 正式发布验收（2026-11-13）：46候选＋27内容主线 Actions 真成功

[INTEGRATION95验收报告](docs/continuity/STONEAGE-INTEGRATION95-PUBLICATION-ACCEPTANCE-20261113.md)／[73条精确run ID与私有原件SHA永久收据](research/recovered/STONEAGE-INTEGRATION95-PUBLICATION-ACCEPTANCE-R1.json)：[PR #373](https://github.com/chinaneedM/stoneage-rebuild/pull/373)候选 `8259498ba826`／tree `8cab7a85ba0d` **46/46** completed/success（27push/19PR），专用两jobs均真日志`Ran 9 tests / OK`；内容合并主线 `897bdadfeb17`／同tree另**27/27** completed/success且专用job真`Ran 9 tests / OK`。私有真实原混合25 `dungeon00.create` 17289B、147原byte spans全SHA；64源floor、117静态方向、70严格反向配置对、7缺对应原字面配置；旧955原DAT对应53floor，**原DAT本轮重读0B**。私人10610B/3CRC原CREATE+现代离线关系图观察ZIP `0e13f780dbd4263e74284329072c0bbb5c8f845647da2bf7916962b9de1a07d5` 已Library上传并独立回读整SHA/CRC，原商业源不入Git；Chromium真验证64源点、147源配置与5来源分组，非原地图原服运行。完整原CURRENT blob `c89e0e33`/2709173B不变，Stage A7 PARTIAL+2 OPEN，B/wiki GATED，R79暂停，整体percent未知。此验收收据新提交自身Actions不预支，须按新HEAD后验。**NEXT**另一个真正可取得的原始任务或地下城素材，不重复无源图谱。


## 2026-11-14 — INTEGRATION102｜原迷宮 NPC 配置與跨原 DAT 來源資格

[來源限定 17 條原 CREATE、14 靜態傳送配置、3 原 handler SHA 與四張已驗 DAT 對照](docs/continuity/STONEAGE-INTEGRATION102-MEIRO-ORIGINAL-MAZE-SOURCE-20261114.md)及[17 條逐原窗口的公開機器收據](research/recovered/STONEAGE-INTEGRATION102-MEIRO-17-ORIGINAL-SOURCE-MAP-R1.json)：以主線 `0c9bc5da57edfec64deced0af299bb03cbc11387` 啟動，原 `CURRENT-STATE.md` 2,709,173B/blob `c89e0e33` 完整保留。已私人讀取後期 mixed25 已驗 NPC ZIP 995,176B / 2,205 CRC，原 `npc/genout/meiro.create` 2,246B/全 SHA，17/17 原 CREATE byte spans、3 原 handler 真原文件/CP950 全 SHA；14 `npcgen_warp` 中 12 有嚴格配置反向匹配，2 沒有；一份 `npcgen_warpman` 文本含 `FREE:LV>49` 與 `WARP:122,6,5` 原字面，不證原生關卡觸發或扣款。舊來源 DAT 四樓層 118/120/121/122 的 10 個來源配置坐標均在原尺寸內，floor 100/119 七配置無同源合格 DAT，本輪新 DAT/原 RD 解碼 0。私有原商用 CREATE/handler 文本不進 Git；原服執行、跨版本官方身份、碰撞及可玩世界全未證。6 個正反公開元數據測試本地通過；正式 GitHub Actions/合併及主線後驗依真實結果另記。Stage A 7 PARTIAL + 2 OPEN，Stage B/wiki GATED，R79 暫停，overall_percent=null。**NEXT**選不同具新原字節／2D 實物的非重複內容族，不繼續原迷宮條目重掃。


## 2026-11-14 — INTEGRATION103｜四村長毛象貨運：12原行李ID、雙服務原參數與舊原二维候選

[真原 NPC 26 CREATE/12參數、12貨物 ID 跨兩原 itemset 的整行SHA對照、8原DAT資料資格與完整12有向靜態貨物對應](docs/continuity/STONEAGE-INTEGRATION103-FOUR-VILLAGE-ORIGINAL-EXPRESS-2D-20261114.md)及[逐原字節段、逐原行、來源負證機器收據](research/recovered/STONEAGE-INTEGRATION103-FOUR-VILLAGE-EXPRESS-CARGO-ORIGINAL-2D-R1.json)：從正式main `747396b15f374f0c1fee10301e2cc121359709c3`／tree `92cd773cc83474837926bf046985b21e3f9b9296` 與完整舊CURRENT 2,709,173B/blob `c89e0e33`啟動；復用私人後期community mixed25 NPC ZIP 995,176B/2,205CRC，實讀此前未單獨整理的`npc/genout/unsoya_1.create` 4,397B/26原CREATE逐window SHA以及12原參數逐SHA/CP950；四原`EXPRESSMAN`的ItemList與四原`LIMITSHOP`的LimitItemNo，對應此前已核 ITEM01原物品表**2402–2413共12ID兩表原整行SHA全部一致**、描述始末短地名以及原圖別名16071，嚴格源數字形成四村12對無自環貨物候選，不宣稱原生營運、運費或運輸。8 floor源DAT歷史索引均有SHA/30×30幾何，1011/1014同SHA，**僅7不同DAT字節身份**，本輪新DAT讀取0B；台灣零售另一來源已验真RD候選行李16071與長毛象100355第一幀 PNG 從舊私有包再次真讀SHA但新RD解碼0，不證原同服。私人28,396B/17成員原小腳本+兩真圖候選+單頁只讀HTML已存個人Library並獨立回取全SHA/17CRC成功；公有Git無原商業完整文本／位圖。10項本地正反合同通過，候選/main Actions與正式合併各依真後驗。保留Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暫停、overall_percent=null；**NEXT**切換另一非重複的原原件遊戲內容族，不擴貨運helper/原服MMO/新引擎。


## 2026-11-14 — INTEGRATION104｜31900 原NPC六樓層，16靜態傳送及兩道具條件／DAT界外反例

[31900原NPC/圖像/傳送來源報告](docs/continuity/STONEAGE-INTEGRATION104-31900-ITEM-GATES-DAT-SOURCE-20261114.md)與[47 CREATE逐原byte span SHA、18原handler SHA、16原來源傳送、9歷史原DAT及2548/2549原物品雙表SHA機器收據](research/recovered/STONEAGE-INTEGRATION104-31900-ITEM-GATE-DAT-SOURCE-R1.json)：本輪按遠端正式main `dc98be953b6a6c5ee114bef6e5904c2db5e05d62`／tree `d443a79b2e337911e201bb3b61aee2562203c8f9` 及完整原CURRENT 2,709,173B/blob `c89e0e33` 啟動；原最新收據HEAD Actions **0條真實運行**，不虛稱通過。真正重讀私有community mixed25 NPC ZIP 995,176B／2,205CRC、`npc/genout/31900npc.create` 7,121B及47全byte SHA，以及18份原CP950 handler 4,249B全部與已核 CHAR01 源索引匹配。新具體靜態來源關係：31910原 **13** 個 `FREE:ITEM=2548`＋`DelItem:2548*1` 独立目標，31903原 **1** 個 `FREE:ITEM=2549` **無DelItem**，另2內聯傳送；全16原目標在先前已核9 DAT header內。重大原反例 **31902 CREATE (9,67) 對以前原DAT 15×10越界**，46/47出生點在界内；未改原字或猜補原生行為。另重新核前存原itemset 2548/2549兩表全行SHA一致，候選TW1真RD已存圖24051/24058/24112三張PNG實讀SHA，**新原RD解碼0、新原DAT讀取0**，不將來源交集等同官方同服。含19原小文本＋3候選原圖＋現代只讀31910地圖點選HTML＋SHA manifest 的私人 **18,408B／24 CRC** ZIP 已存個人Library並獨立回取全SHA一致 `92b3721f0882f37d87698de0c729adb7fcf066ed55c1193b3d787352b6e0f626`，原商用字節/圖像不公開。12項本地正反核驗通過，正式 Actions/PR依遠端精確HEAD後驗，Stage A7PARTIAL+2OPEN，B/wiki GATED，R79暫停，overall_percent=null。**NEXT**輪換別的可取得原實物的2D/人物/任務族；31902界外爭議待新的同載體原DAT/原生運行證據，禁靠推想修掉。


## 2026-11-14 — INTEGRATION105｜dungeon02 原151 CREATE、144原傳送與7原NPC提示／地圖資格負證

[實讀後期mixed25私源與有界結果](docs/continuity/STONEAGE-INTEGRATION105-DUNGEON02-ORIGINAL-STATIC-ROUTES-20261114.md)及[公開逐151段原索引 SHA／144傳送數值／7 handler SHA／DAT資格報告](research/recovered/STONEAGE-INTEGRATION105-DUNGEON02-151-ORIGINAL-STATIC-ROUTES-R1.json)：按fresh main `86d83465745283bf42ebc4384a455eb3025ddc1f`／tree `dd6f8a5306489340b75e8f3c23017a10bbf97050`、0開放PR及最新 HEAD 0 個 Actions、完整 CURRENT 原Git blob `c89e0e33`／2,709,173B重新啟動。不重做 INTEGRATION95–104 或已完成的夢幻洞窟。個人Library既存 CHAR01 原NPC ZIP995176B/2205 CRC 真核，`npc/genout/dungeon02.create` 18174B/SHA `bf047be69b5b1d3f6fda836cac4174e69868031b4e3e57f71c2f7da2b02636b6`，151原 CREATE 段及7原文本合共720B逐SHA對上舊CHAR01公有全源索引。144條 `npcgen_warp` 中132條有精確同文件反向、12無；65源floor中64具舊MAP04合格DAT尺寸，floor300缺合格DAT，135/151源點及128/144目的點在舊已驗尺寸內，其餘分別16/16因floor300缺源，**沒有已資格DAT的越界點**。此包新貢獻是原靜態路由/原文本—原DAT的具體可反證整合，非首次找回原CREATΕ，也非原世界運行或原TW1同部署證明；原商業原文/原圖/原DAT均未進公開Git，新RD解碼0、原DAT新讀0。專用9條metadata反證測試只驗公開源SHA/座標/負證，CI須在候選/main真正運行才可報成功。Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暫停、percent=null，舊CURRENT完整保留。**NEXT**只在有新同源 `300.dat` 原字節時重核其尺寸與新2D可見內容，否則輪換另一個非重複有真原件的寵物／NPC／任務內容族。


### INTEGRATION105 正式主線與73次實際Actions驗收（2026-11-14）

[永久驗收](docs/continuity/STONEAGE-INTEGRATION105-PUBLICATION-ACCEPTANCE-20261114.md)及[73條逐run真實收據](research/recovered/STONEAGE-INTEGRATION105-PUBLICATION-ACCEPTANCE-R1.json)：[PR #393](https://github.com/chinaneedM/stoneage-rebuild/pull/393)已真正合併；候選 `dd1ea58a632842dd9b7b8e63a19d3cd6abc0c380`／正式main `6bfb5a13ca8955eb76ad475687317e5275a0722f` 同 tree `4ae60f86c6ed4ed9399cda8d40df8243e2b2f41f`。候選push27＋PR19 **46/46**全成功，正式main另 **27/27** 全成功，三份專用真job logs均 `Ran 9 tests / OK`。原後期社群混合25 NPC私源 ZIP995176B/2205CRC、`dungeon02.create`18174B/151原窗口及7實原文字 SHA 門檻、本次144靜態原傳送的132精確反向、12無、64原DAT合格地圖與floor300缺原DAT的16/16靜態限制已記錄；非原服/TW1官方同部署和玩法執行，源文字未入Git。CURRENT 2,709,173B原blob `c89e0e33`不動、Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暫停、percent=null。**此收據新提交自身Actions須按新HEAD另判，不預支；NEXT**有floor300新原DAT才重開，否則更換非重複原2D／寵物／NPC／任務素材。


## 2026-11-14 — INTEGRATION106｜shop_m3 40原配置×30组真正台湾零售原2D候选与私人观察

[INTEGRATION106完整来源和观察界限](docs/continuity/STONEAGE-INTEGRATION106-SHOP-M3-40-NPC-ORIGINAL-2D-20261114.md)、[公开逐原CREATE窗口/28原handler SHA、30真正原RD/PNG逐SHA和DAT负证](research/recovered/STONEAGE-INTEGRATION106-SHOP-M3-40-SOURCE-TW1-ORIGINAL-2D-R1.json)：fresh main `c27d7ecd45ec3ff3a9bab1afd9ba48dc79f7dc00`／tree `26a97b62cf31965850d6660efb45ad9e8fd7f381`、26/26 Actions真正成功、0PR及完整 CURRENT 2,709,173B原Git blob `c89e0e33` 重核。INTEGRATION105未决floor300的原 `300.DAT` 在旧RAR目录存在却因RAR过滤器不支持未验CRC，仍不可当合格地图；止点后转已有实源的不同NPC族。私人後期 mixed25原NPC ZIP995176B全2205CRC、本轮原 `npc/genout/shop_m3.create`7139B及40原CREATE段、28真原文本逐SHA重新读取；已知ITEM01目录本就含该族13商店，不计新商店。40源配置涉及14floor、8原功能类别；旧MAP04尺寸38/40坐标界内，floor5000及6000两条缺合格DAT，保留原 CREATE(5105,22,8)与handler文件名 `ss_5105_24_10` 数值不一致，不推断自动纠正。另一独立原 TW1.0零售 P3H ZIP372626292B/379CRC，24个静态ADRNRD＋6个唯一SPR动作0方向0首帧，总 **30不同原RD** 真正提取双解码逐原索引相同，候选Palet1 PNG及RGBA回读30通过；旧PET07/CHAR03已有相关原像，本轮新的是40源NPC与真正2D候选的集成观察，而不是30个新原图/原生官方NPC。同私人HTML浏览器成功40图片/30不同图、楼层筛3/商店筛13、0JS及0外网，宿主`file://`被阻止故仅`page.set_content`用同原PNG字节，**不证明真实商业运行或同部署配色**。私人215924B／92成员 ZIP SHA `308e4a6a0cd00af200a7f9208adf9e630413ed5cb53a3cb15e1cf7b10efcb7c8` 已存个人Library并独立下载回读整SHA/CRC同；原CREATE、台词、RD/PNG与私人页面均不入公开Git。Stage A 7PARTIAL＋2OPEN、B/wiki GATED、R79暂停、总体percent=null。内容候选/main CI 与收据后验另核，不能预支。**NEXT**切换非重复具真原件的宠物、任务或场景内容；受限floor300/5000/6000仅有独立CRC合格原DAT才重开。


### INTEGRATION106 原30组真正二维与全部93次历史Actions正式验收（2026-11-14）

[INTEGRATION106正式验收](docs/continuity/STONEAGE-INTEGRATION106-PUBLICATION-ACCEPTANCE-20261114.md)／[93条逐run完整审计收据](research/recovered/STONEAGE-INTEGRATION106-PUBLICATION-ACCEPTANCE-R1.json)：[PR #395](https://github.com/chinaneedM/stoneage-rebuild/pull/395)已合并；首次候选 `decfae00eca9629015eaee953e868bebb9ebbcc6`／46条CI中**44成功、专用push和PR各1真实failure**，原因是公开测试断言错误（源码和像素没变）。更正后候选 `436388d3e01a762066ad3ef1b66c9d7c50a97b3f` **20/20成功**（push1/PR19），正式内容main `05272d2dc6e7be3c290f388ce92102f2ffe07fb0`／同tree `4ce55125b6a5f319f2bcd74b68094637962027ed` **27/27成功**，三真实专项job均10测试成功。私人 mixed25原NPC ZIP2205CRC、40原CREATE/28 handler SHA、原台湾TW1 P3H 379CRC及24原静态RD+6 SPR首帧的30实际原图双解码、Chromium40卡零外网验证均已核；私有215924B/92CRC原图和脚本观察包已Library独立回读整SHA成功，原商业字节不进公开Git。旧ITEM01原13商店不重报新商店；floor5000/6000旧DAT缺来源，ordinal24源坐标与handler名不一致保留，floor300来源档在旧RAR但CRC不合格。CURRENT 2709173B原blob `c89e0e33`不改、Stage A7 PARTIAL+2OPEN、B/wiki GATED、R79暂停、percent=null。**本验收收据提交自身的Actions另以新HEAD实际核验，不预支；NEXT**轮换另一未重复真实可见游戏素材。


## 2026-11-14 — INTEGRATION107｜SOT 环岛 C/D 原27 NPC／27事件脚本与2003攻略坐标异文

[INTEGRATION107真正原材料核验](docs/continuity/STONEAGE-INTEGRATION107-SOT-CD-ORIGINAL-SOURCE-AND-2003-GUIDE-20261114.md)／[逐源byte span、27事件SHA与24站差异](research/recovered/STONEAGE-INTEGRATION107-SOT-CD-27-ORIGINAL-SOURCE-VS-O14-R1.json)：从精确远端main `89635e38a2f901eada662061de8b32879eeed2be`／tree `20671f295a01cbe2a34ae3116a4a2c67d5a1ada7`、26/26成功Actions、0PR及完整旧CURRENT blob `c89e0e33` 启动。私人后期mixed25原NPC 995176B、2205/2205CRC，本轮真正重读 `sainasu/event/oev2.create` 4719B与27份不同原事件脚本逐SHA，包含报名1、C/D各12检查站与两个终点；24原事件脚本各存在前序DelItem和后续GetItem数值token（2575–2587），不是原生行为或随机奖励执行证据。对照已有O14 **2003年玩家投稿**：24站 **19同坐标／5异坐标**（C-3、D-2、D-3、D-4、D-5），C终点还另有1格异文；原后期脚本不提升成同2003官方或TW1版本。只与既有MAP01合格DAT索引对照，27原CREATE **17几何界内／10该目录无DAT资格／0已资格越界**，本轮无新DAT、RD原像或官方世界实走；私有商业原文不入Git。Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall percent=null。公开专项测试/CI仅重放派生数据，需以后验真实Actions为准；**NEXT**换另一个有实源的非重复宠物／任务／可见二维内容。
