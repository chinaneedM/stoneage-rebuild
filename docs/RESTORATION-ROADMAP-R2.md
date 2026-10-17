# 《石器时代》整体复原路线 R2

日期：2026-10-16（Asia/Shanghai）。性质：研究工作顺序与验收标准；不是新游戏设计，也不是历史复原完成证书。

用户本轮要求：“对的 因为我对整体复原的构架和设计不懂 都是你来执行的 你要规划好我们到底怎么来复原才更合理”。本路线落实助手负责整体规划、必要性判断和取舍的责任。基于本轮重新读取的远端 main；精确 HEAD、tree、证据文件摘要见 `research/recovered/STONEAGE-RESTORATION-PORTFOLIO-R1.json`。

## 一、目标与完成边界

先把可恢复的早期《石器时代》整理成有来源、可解释、可验证的规则和内容规格，再与用户讨论现代单机新作。台湾 Waei/JSS v1.0 纯净客户端继续作为基础；JSS 1999 原版、原始商业服务器资料缺失，不能用后来版本填充成早期事实。

复原需要回答：游戏有什么内容、规则如何运作、数据从哪里来、系统怎样衔接、还有哪些无法证实。无需为了这一目标完整复制旧客户端、C 运行库、Windows 文件系统或运营服务器。

每个重要结论保留两个独立维度：

- **历史归属**：V1_DIRECT、EARLY_LINEAGE、LATER_RECOVERED 或明确 OPEN。
- **规格可用性**：已有可复核规则、已有带前提模型、待补关键依赖，或证据受限。

模型可以在限定版本内可用，同时保持“是否属于台湾1.0”未证。一个技术辅助函数未完全解释，也不自动阻塞其他系统。无法获得的原始服务器资料应形成有搜索范围、缺失影响和重开条件的记录；这不是恢复出了缺失内容，更不能以补造数值解决。

## 二、本轮复核后的整体地图

此表是组合索引，不能把历史文档中限定范围的 CLOSED 扩大成整个系统完成。各系统族仍维持 PARTIAL/OPEN。

| 系统族 | 可复用成果 | 仍影响复原的缺口 | 后续可验收成果 |
|---|---|---|---|
| 版本与原始资料 | TW1.0基础验收、文件哈希、版本隔离政策 | JSS1999、部分地区桥接与商业服务器资料 | 每项规则/内容能追溯到具体版本；不可恢复部分单列 |
| 世界、地图、移动、遇敌 | 原始M/MC地图机制；后期826层世界、四出生点、地图与遇敌适配 | 后期地图不能直接认作1.0；条件传送、数据缺陷和原始世界归属仍需区分 | 四出生点的关键玩法链证据表，逐段标明可用性/版本/缺口 |
| 人物、宠物、成长、捕获 | 出生/成长/捕获模型与部分原始后代代码验证；V1状态布局 | 初代具体参数未齐；捕获后完整宠物当前状态仍由调用方提供 | 每个持久字段有来源，缺失字段保留显式输入，禁止猜默认值 |
| 战斗、技能、状态、结算 | 普通回合、技能与多种有界原始后代执行验证 | 版本配置、自然可达性、真实运行输入与完整链范围 | 关键玩法场景的有版本规则规格；分清能力与实际可达性 |
| 物品、装备、商店、经济、掉落 | 使用/装备/交易/商店与若干所有权、奖励链模型 | 原始具体物品表、跨系统所有权/存档边界与版本差异 | 获得、使用、转移、消耗到保存的字段与状态链 |
| NPC、任务、推进 | 后代通用加载图、常见NPC语义、条件WarpMan与推进模型 | 初代任务脚本/对白及精确NPC人口不全；已有源/数据不匹配 | 复用现有目录，列出有证据任务链和不可恢复内容，不重做全量NPC枚举 |
| 图像、动画、音频、UI | 原始资源身份/格式/元数据与若干协议UI边界 | 尚未构成完整历史交互/显示语义；生产资产另有版权边界 | 可消费的资源/交互规格和原始数据限制；暂不制作新美术或选新引擎 |
| 运行、状态与持久化 | 客户端状态布局；后代角色保存/退出规则；现代参考模型独立保存 | 原始角色服务器格式不全；客户端本地savedata语义仍不全 | 区分三种保存层，记录哪些状态需要保留及证据范围 |
| 系统衔接与复现 | 本地参考协调器、版本化世界适配、golden与历史CI记录 | 可运行模型不等于全历史场景复原；有些输入依赖人工供应 | 关键玩法链的来源和缺口审计，避免单个测试数量替代整体完成度 |

本轮重新运行49项现有基础语义测试（状态布局、人物/宠物成长、地图投递、版本化遇敌、世界适配与golden），全部通过。它只确认当前选定模型的回归；不是重新执行全部历史来源、原始客户端或826张地图的载荷。

## 三、存档支线的处理决定

必须分开以下三层：

1. **原客户端本地 `data/savedata.dat`**：128字节种子及后来R1–R78静态分析；确切业务含义、字段和实际落盘仍有缺口。
2. **历史服务器角色/宠物/物品保存**：后代序列化、SAAC、退出确认顺序等证据；不等于原客户端本地文件。
3. **现代参考模型的本地保存**：为验证重构状态而编写；不能拿其成功反证历史服务器行为。

基础验收文档已将第1层列为 NON-BLOCKING OPEN DETAIL。R1–R78确实积累了有效静态证据，但辅助函数、寄存器、ABI与错误分支的细分不再自动取得全项目最高优先级。

**决定：原客户端savedata深层辅助函数支线暂缓。旧“最高NEXT R79”由本路线及最新CURRENT-STATE明确取代。** R79预检、所有旧报告、失败修正和OPEN问题全部保留。它们不被撤销、删除或称为已解决。

重开必须满足至少一项：新资料直接带来可恢复的业务字段；现有核心规则因该细节存在可证明冲突；具体跨系统规格无法确定且该辅助函数是最小必要依赖。仅仅“还有一个函数没解码”或“可以再补一轮测试”不足以重开。

## 四、实际工作顺序

### 已完成：PORTFOLIO-01 整体复核与重排

形成此路线、九系统矩阵、摘要固定的证据索引、支线暂缓决定、持续执行规则。没有因此新增历史事实、关闭系统族或启动新作生产。

### 当前最高：PET-STATE-01 捕获到持有宠物的状态来源

**当前代码可见的问题**：`build_reconstructed_pet_state()` 仍要求显式MP、maxMP、EXP、maxEXP、renameFlag、freeName等输入；`resolve_persistent_capture_round()` 仍要求成功目标对应完整的、带来源的PetActor。捕获公式与事务已经存在，完整状态来源仍是可明确定位的业务接缝。

本轮已形成 `research/recovered/STONEAGE-CAPTURE-STATE-PREFLIGHT-R1.json`，固定当前函数签名、21项桥接状态键、19项战斗参与者字段及当前验证边界；下一轮直接做字段来源追踪，不重复该预检。另运行9项现有捕获规则测试，确认当前模型明确“不复制敌人EXP、按等级重算maxEXP、VARIABLEAI归零”的后代证据边界；没有据此推广为台湾1.0服务器事实。

先核对现有捕获、出生、成长、协议和桥接数据，逐字段区分：可复制的野生敌人当前状态、可由已有规则计算的状态、静态模板数据、原始证据不足的输入。优先复用已有源与模型；不能把捕获动作误作重新出生，或从名字猜MP/EXP规则。

交付为字段来源/缺口表和一个最小必要修复或证据受限结论。有正面证据才补接；若缺少匹配的当前运行时状态，就继续要求显式来源输入，说明该限制对捕获/保存/再入战的实际影响，不填假默认值。

验收以来源规定的复制/初始化语义和捕获身份、HP/MP、技能、成长身份及保存边界为准；EXP不能直接沿用野生敌人或击杀奖励值。复用现有捕获与协调器测试，只补真实变更的回归。限定最多两个连续工作单元：若仍未得到可改变规格的证据，形成明确受限记录并切换包，不能转向无限追逐任意函数。

### 随后的有限验收包：WORLD-01 四出生点关键玩法链与版本缺口

已有四出生点合同与826层世界闭合成果，不重新证明同一张图。此包用于阶段总验收时核对来源与外部输入；只有发现具体矛盾或缺失接缝，才转成新的恢复任务。

直接复用现有四出生点合同、世界索引、区域载荷来源、碰撞/传送、遇敌、NPC与协调器。不要重新下载或枚举全部地图/NPC，不要从旧文档的旧NEXT重新启动已闭合任务。

交付为四个出生点各一条已存在合同支持的推进路线，覆盖出生位置、地图载荷、移动/传送条件、遇敌/敌人数据、关键NPC/推进、战斗结算六个检查点，共24个有限检查格。每格记录版本角色、来源、已有模型、必要外部输入、已知缺口与影响。不得虚构路线或将后期合同冒充初代自然流程。

明确哪些格在对应后期/后代版本内可复现、哪些只有机制、哪些初代归属未知。已有验收直接引用，只为真实缺口补检查；不因为要填表而再运行全量原始地图/客户端。

### 然后：RULES-01 核心规则和内容归属汇总

围绕战斗/成长/物品/经济/任务，把现成规格的版本、前提、输入和缺口连起来。优先真正妨碍普通玩法复现的差异；已证版本内可用的部分不重做。各包交付后，按影响重新排序，后续包并非不可更改的流水线。

### 最后：STAGE-A-REVIEW 历史复原联合审阅

交付九系统验收表、可复现的代表性玩法链、版本隔离、原始服务器缺失清单和生产限制。只有共同审阅之后才进入新作引擎、内容取舍、美术、UI和生产架构讨论。原始资料不可恢复不应导致永远无法审阅，也不能被报告成“百分之百复原”。

## 五、持续取舍与汇报规则

- 开始一个任务前写清：恢复什么游戏行为/内容、当前缺口、这轮交付、来源范围、停止条件。
- 只有会影响该交付的底层细节才展开；假定、未知、后期版本可以明确留在边界。
- 连续两个单元没有带来新的业务规格、内容归属或关键系统接缝结论，立即回到整体矩阵重排；不可仅沿着最近一条NEXT继续。
- 不因测试数、R编号、反汇编节点数或耗时增加而提高整体进度；不报无分母百分比。
- 每轮先汇报对整体复原新增了什么、仍缺什么及下一项理由，技术摘要放后。
- 每完成一个工作包复核总队列；发现更有价值缺口可主动调整，并在仓库留下理由。用户无需负责审查每个底层函数的必要性。
- 保持每轮约15分钟以上有效工作量；不靠等待、重复拉取、无关测试或人为拆分凑时长。只运行与改动和结论相关的检查。

## 六、可核查来源

完整来源路径、字节数、SHA256与Git blob见组合索引JSON。优先参见：基础验收、恢复阶段门、WORLD-MAP政策、RUNTIME-BOOTSTRAP合同、REGION-PAYLOAD来源、GAMEPLAY-SCHEMA、PET-CAPTURE/GROWTH、SAVE-LOGOUT与R77/R78边界。它们记录的技术关闭与历史未知均按原范围保留。


## 2026-10-16 后续执行记录：PET-STATE-01已作有界处置

本轮完成捕获字段来源表、两个入口的名称/隐藏忠诚变化值检查，以及完整输入条件下的捕获→入栏→磁盘保存/读回→再入战→受控成长验证。已知状态不应被错误替换；没有正面来源的状态不补默认值。

完整宠物自动构造仍为 `OPEN_EVIDENCE_LIMITED_EXPLICIT_STATE_REQUIRED`。这不是整个宠物系统完成，也不是台湾1.0商业服务重现。现有源码/模型可以解释部分复制规则，但当前MP、初始EXP/阈值配置、完整技能/状态和可见AI还需要明确的匹配运行时输入。出生对象仍保留在战斗上下文，不能把最小战斗对象缺字段说成全部来源缺失。

**当前最高改为WORLD-01有限验收包**：按本路线既定24格复用四出生点已有成果，定位影响核心玩法的具体接缝。不重新下载/枚举全世界，不重做已闭合图，不因某一历史字段OPEN继续无限追逐。R79继续暂停。

详见 `docs/specs/STONEAGE-CAPTURE-STATE-SOURCES-R1.md` 和当前状态最新记录。


## 2026-10-16 WORLD-01 有限验收记录及规则队列切换

24格已完成**证据归属/前提/缺口核对**，不是24格早期游戏复原完成。
四路线仅为 recovered25 后代样本，台湾1.0/JSS1999具体地图、NPC、
野怪和任务归属仍 OPEN。第1、2条经典传送可达；第3、4条经典路径不通，
须普通商店购买物品、满足 WarpMan ITEM/FREE 并取合法条件结果，且两者
COMBAT/SHOP先后顺序不同。所有战斗和随机传送为存在性见证，不保证结果。
地图826层=761 DAT三平面+65 LS2MAP双平面；后者的事件层必须保持独立/缺失。
历史原服最终结算、任务奖励与完整存档未因现代参考模型而关闭。

验收文档 `docs/specs/STONEAGE-WORLD01-FOUR-HOMETOWN-REVIEW-R1.md`；
24格与14份来源的SHA/尺寸见
`research/recovered/STONEAGE-WORLD01-FOUR-HOMETOWN-ACCEPTANCE-R1.json`。
独立CI 38907653875 成功，先前脚本错误失败38907621482保留。
WORLD-01仅关闭有限审查包，世界系统仍 PARTIAL/OPEN。

**当前最高转为 RULES-01。** 对战斗结算/EXP→人物与宠物成长→物品购买/
Stone/任务道具→NPC奖励门槛→保存归属做有限版本化连线检查。先读现存
生效模型和前提；只处理实际影响正常玩法的矛盾或缺接缝。不无限追逐
R编号或泛用CRT函数，不把后代资料冒充最初发行版本。


## 2026-10-16 — RULES-01 跨系统规则接缝预检

完成八条**已有模型与证据的连接前提**审计，不代表八条均已复原。
旧版服务器战斗EXP归属、升级阈值两种互斥语义、宠物当前状态与成长
随机输入、商店Stone/道具购买、NPC道具门槛与服务器角色持久化必须
分别保持版本和状态来源边界。TW1.0可见EXP/maxEXP字段不能证明采用
哪套服务端阈值；后期2.5配置不可直接推作JSS1999。
数据具体缺口优先定位为购买后持有物品→NPC条件传送/奖励→保存归属。
现阶段只核对11份既有文件来源和8条规格接缝；原始任务与奖励仍未证实。
证据记录：`research/recovered/STONEAGE-RULES01-CROSSSYSTEM-PREFLIGHT-R1.json`。
成功验证：GitHub Actions 38908646966。最高下一项仍为 RULES-01
的具体数据与状态连接核查；不恢复R79技术深挖。


## 2026-10-16 RULES-01 后续执行：道具持有→条件门槛→本地保存的参考闭环

新接缝 `tools/stoneage_rules01_shop_gate_reference.py` 只接受明确标注
`recovered25/LATER_RECOVERED` 的商店条目、道具身份、价格/倍率、可用背包
容量、当前Stone和物品视图。模型连接普通购买的完成结果与持有道具，后续复用
真实的已建 `ITEM/FREE` 条件判定及本地文件保存/重新读入。余额不足、
容量不足、版本错误、商店条目不匹配或Stone字段缺失不得修改原状态。
最小参考案例使用**完全虚构的测试ID/数值**，仅证明已有接口可形成可执行
现代模型链；没有执行原始商业服务端或取得初代NPC、任务、收费、奖励记录。
原后代商店异常中途创建失败可部分发物品且不扣Stone，该不可回滚情形
**未**被本接缝错误声明为原服原子交易。

另一项正面来源界限必须保留：`ExChangeMan` 在独立后期资料中有2条
带 `LV`/按等级 `DELSTONE` 的 `GETITEM` 奖励记录，并能接向另一
条条件传送路线；它**不是** WORLD-01第3、4出生点的普通商店购买链。
另有 WarpMan `DelItem` 引用，但单纯引用不等于已证明本轮门槛消耗道具。
非商店掉落/AddItem审计的零命中亦不否定ExChangeMan奖励。
新来源界限表 `research/recovered/STONEAGE-RULES01-KEYITEM-AWARD-BOUNDARY-R1.json`
记录7个现存Git blob/字节来源和必须保留的否证边界。

当下真实缺口：完整早期来源归属、目标道具 `ITEM_DROPATLOGOUT`、
事件字段如何由原始服务器存档、SAAC写入及重新登录结果。现代磁盘保存
不能证明历史原服成功；既有R79存档底层分支继续暂停。
验证门槛：独立CI成功后仅关闭 **RULES-01的一个有界参考连接和后期内容归属检查包**，
全部RULES-01历史资料与Stage A九系统状态保持 `PARTIAL/OPEN`。

后续最高优先级转为 **STAGE-A-REVIEW-PREFLIGHT**：依据九系统已有来源与
实际玩法成果，列出仍无法复原的具体历史字段、脚本和资料、对核心体验的影响、
可查证的数据入口与停止/重开条件，再决定下一个最有价值的实际补全包。
这只是整体复原缺口评审，不等于正式Stage A终验、原版全部恢复，
更不允许提前进入新作引擎/内容共同设计。不得继续任意穷举泛用helper，
也不得依据工作编号、通过测试数或经过时间计算无分母总进度。


## 2026-10-16 — RULES-01 coordinated ITEM-gate/save strengthening, Stage A review is next

Existing later-version shop→owned-item→FREE gate→local disk evidence was already
accepted on main, with distinct later ExChangeMan award provenance. The limited
additional unit does **not** add a duplicate shop subsystem: it drives the
existing model through the actual local coordinator's interaction discovery,
guarded WarpMan dispatch, one post-purchase save/reentry and a second postwarp
save/reentry. Negative wrong-item and forged-world-flag cases remain denied.
All event/item/Stone/NPC values are synthetic test fixtures; no first-generation
item, quest, original server save or reward identity is established. Successful
Action38912629479 is a reference integration check, not an original-source
execution. The historical item-drop-at-logout and SAAC durable-ACK restrictions
stay OPEN. Evidence receipt: research/recovered/STONEAGE-RULES01-COORDINATOR-GATE-RELOAD-ACCEPTANCE-R1.json.

**Next: STAGE-A-REVIEW-PREFLIGHT**, the nine-system-family representative
playflow and material-gap inventory selected by the previous current-state
entry. Finite audit, no arbitrary deepening of savedata R79, no engine/new-game
design before Stage A joint acceptance.


## 2026-10-16 — Stage A 九系统来源预审及下一项

九系统状态逐项重查并与初始 Portfolio R1 一致，全部仍属 PARTIAL/OPEN，
Stage A 未终验，Stage B 未启用。记录来源与可复现限定：
`research/recovered/STONEAGE-STAGE-A-NINE-FAMILY-PREFLIGHT-R1.json`。
独立 Actions38913920159 成功验证九族、13份已有源 Git blob 字节身份，
以及5个下一阶段界面语义证据槽。没有在本轮下载原始游戏资产、运行商业
服务器或补造历史任务脚本，因此不计算无分母的总体进度百分比。

**最高下一项 UI-SEMANTICS-01**：优先复原台湾1.0原始客户端五类界面
与玩法事件的证据对应（地图/位置、角色状态、背包道具、宠物/技能、
战斗与NPC窗口），通过既有 V1 状态消息/资源身份和真实来源限制建立
可审核的语义规格。不能将晚期 Windowman 配置或后世教程界面冒充
最早版本；不能仅凭资源ID存在推导原版显示位置/动画。遇缺失必须标 OPEN。
只做历史语义规格，不选新引擎、不进行新游戏UI制作，不重开R79。


## 2026-10-16 — UI-SEMANTICS-01 original-client five-surface acceptance

Source-crosswalk only, not a screen reconstruction: 16 original-v1 decoded
record families and 14 compiled send/receive message envelopes now have
source-pinned field/interaction contracts and 10 adversarial custody/scope
tests with independent Actions acceptance. The compiled B receive
C/P/A/U/default path and status/command queues are separated from later
server battle simulation. Asset presence (REAL/ADRN, SPR/SPRADRN, indexed
SAB/palettes, sound) does not by itself prove an on-screen selector.
Stage A remains PARTIAL/OPEN. Next **UI-RESOURCE-BIND-01**: bounded
two-family original-v1 pet sprite and battle SAB/palette selection trace,
stopping if required source is absent; R79 paused. See
`docs/specs/STONEAGE-TW10-UI-SEMANTICS-R1.md` and the new
`STONEAGE-TW10-UI-SEMANTICS-ACCEPTANCE-R1.json` receipt.


## 2026-10-16 — UI-RESOURCE-BIND-01 bounded source stop

Accepted v1 disk evidence cleanly indexes 218 SAB battle scene records
(804 bytes each) and 15 indexed SAP palettes, with Palet_0.sap unindexed.
A strict synthetic 20×20 big-endian candidate decoder illustrates the
historical descendant interpretation, but the actual v1 runtime select,
decode/draw call, chosen SAB/background/palette and pet graphic-to-SPR
animation mapping are **OPEN**, pending original callsites/traces.
Original B callback source scope is now enforced by a B-prefix guard.
Source-pinned audit and separate successful Actions suites documented in
`research/recovered/STONEAGE-TW10-UI-RESOURCE-BIND-ACCEPTANCE-R1.json`.
Stage A remains PARTIAL/OPEN and Stage B gated.

**Next STAGE-A-NPC-CONTENT-BOUNDARY-01**: return to the critical
player-visible missing original NPC/quest/dialogue content and version
attribution, rather than indefinite image-ID/GUI internals or R79.


## 2026-10-16 — STAGE-A-NPC-CONTENT-BOUNDARY-01 完成有限证据归属，不宣称初代任务复原

原始 v1 客户端 WN 通信接口与缺失的初代商业服务器任务/对白必须分开。核对后期 recovered25 create 4985条、Windowman17条（4缺配置）、TownPeople445条（15缺参数）、NPCEnemy279条和WarpMan202条（160空间候选）；这些是后期证据库目录，不是台湾1.0原生NPC表。ExChangeMan后期奖励与普通购买/条件WarpMan始终分开，缺早期奖赏存档及事件完成证据。源证据矩阵七项/玩家链六段，13个Git blob来源由独立CI38920853733验证。无原始商业服任务/对白字节恢复。
对应 docs/specs/STONEAGE-STAGE-A-NPC-CONTENT-BOUNDARY-R1.md 和research/recovered/STONEAGE-STAGE-A-NPC-CONTENT-BOUNDARY-ACCEPTANCE-R1.json。
**最高下一项 STAGE-A-REVIEW-BLOCKER-TRIAGE-01**：九族联合代表玩法链和原始内容阻塞分级；Stage A仍未最终验收，Stage B GATED，R79继续暂停；不以R编号/测试数作为进度分母。


## 2026-10-16 — STAGE-A-REVIEW-BLOCKER-TRIAGE-01 九族联合阻塞分级

已完成原始客户端→玩家位置/人物宠物→遭遇战斗→任务NPC/条件商店→物品奖励→退出重登→UI资源等七条有边界的代表体验审查。十份不可变源Git blob/尺寸固定；九系统族仍7 PARTIAL+2 OPEN，Stage A 未最终验收，Stage B GATED。四出生点与24格均只属于 recovered25 历史参考；初代商业服务端内容、EXP/宠物完整初始态、原始NPC/奖励/存档不可通过后期测试填补。
具体表 docs/STAGE-A-REVIEW-BLOCKER-TRIAGE-R1.md 与 research/recovered/STONEAGE-STAGE-A-BLOCKER-TRIAGE-ACCEPTANCE-R1.json，独立CI38922063102 SUCCESS。
**下一项 STAGE-A-CONSOLIDATED-REVIEW-PACKET-01**：组织一份可供用户独立联合审阅的九族规格与无法取得的初代内容清单；未完成正式审阅前不生产新引擎/美术/新剧情。R79仍暂停，禁止无根据百分比。


## 2026-10-16 — STAGE-A-CONSOLIDATED-REVIEW-PACKET-01 正式审阅交付

当前统一入口是 docs/STAGE-A-CONSOLIDATED-REVIEW-R1.md 及同名机器审阅清单。
九系统7 PARTIAL+2 OPEN、七条有界体验、五个阻塞和已有技能/装备/交易/
存放/骑乘规格一起交付；没有增加初代商业服剧情、商品、奖励或存档事实。
54份来源字节/Git blob与8份历史连续性前缀被固定。选择性复跑11组既有
测试314项，加5项审阅清单反例检查通过；不是全部历史代码或商业游戏重跑。
远端CI由随后验收receipt记录；此处不提前声明成功。

**Highest NEXT STAGE-A-JOINT-REVIEW-01**：向用户呈交正式审阅包，确认成果
与未恢复范围，再共同决定历史阶段剩余工作。发布/CI不能代替用户审阅。
用户只说“继续”时仍为Stage A；可选择 EARLY-CONTENT-RECOVERY-01，有限
追踪同代地图缓存、NPC/任务、商品/奖赏数字线索，先读来源账本；没有新
实质线索则停止该搜索，不重新编年、全量枚举或深挖R79。Stage B GATED。


## 2026-10-17 — EARLY-CONTENT-RECOVERY-01 有限原始内容补证

恢复JSS第一方手册四类业务合同及新浪指南四条任务轮廓。实际手册快照
2001-04-18；新浪目录日期2001-01-18不认证当前网页字节同年一致，ZIP
未恢复。所有具体服务器ID/事件/存档与TW1.0/JSS1999精确归属继续OPEN。
见docs/specs/STONEAGE-EARLY-CONTENT-GUIDE-MANUAL-R1.md。下一项
EARLY-QUEST-CONTENT-02选择单条任务寻找独立早期证据；不再只增加
组合审查表，不进入Stage B或恢复R79。


## 2026-10-17 — EARLY-QUEST-CONTENT-02 成人仪式获得实际早期文本定年

新浪任务段由真实2001-11-20快照确认，与当前两站同文；不是1月定年、独立多见证或TW1.0原始脚本。形成来源分层的成人流程与空包领15玉规格，保留头盔敏-2/-3差异及后期物品生命周期/协作边界。原始ID与版本归属OPEN，九族仍7 PARTIAL+2 OPEN。规格STONEAGE-ADULT-CEREMONY-SOURCE-CONTRACT-R1。
下一项EARLY-LOGGING-CONTENT-03：已有伐木指南实际快照与尾刀/许可/收益/手环来源对照；一次有限检索，无证即停。正式联合审阅仍待用户，Stage B GATED，R79暂停。


## 2026-10-17 — EARLY-LOGGING-CONTENT-03 来源分层伐木任务

三个实际2003/2004快照限定文本年代与索引1.82编辑归属。尾刀、许可在回购时收回、近似14木5000、断斧修复/新斧分阶段、后期重复接取和手环魅+5/-5差异已有规格；原始ID、事件和商业服构建不补造。下一项QUEST-ITEM-IDENTITY-04只复用已有recovered25物品表schema/修订/获取流程核对手环、许可、斧头几个候选，形成版本化身份清单，不倒填TW1.0、不重新扫全部任务。正式联合审阅仍待用户，九族7 PARTIAL+2 OPEN、Stage B GATED、R79暂停。
