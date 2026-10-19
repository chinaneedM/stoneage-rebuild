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


## 2026-10-17 — QUEST-ITEM-IDENTITY-04 后代物品候选已有来源身份

同源两表各五行候选、实际setup、raw属性/生命周期与不同许可ID已固定，原始早期ID与任务绑定仍OPEN。规格STONEAGE-QUEST-ITEM-IDENTITY-R1；下一项QUEST-NPC-ITEM-BINDING-05仅追踪这五ID的同源NPC配置发放/收回，非全量NPC或通用helper深挖。无明确语法即止，Stage A未终验，Stage B GATED。

## 2026-10-17 QUEST-NPC-ITEM-BINDING-05 后代任务物品NPC字段角色

从五项已验证recovered25物品候选沿同保存包NPC FunctionSet/二级参数建立有限的字段角色抽取。源Action38996224450/job117289269018通过9项语法/否证检查与两分卷、合包来源hash；先前Action38996169729对ItemShop字段规则误判产生一次失败，已保留历史并收紧角色。4,985条NPC创建引用中，30模板歧义、15参数文件缺失。共49次有语法类型的引用、10类，全部ExChangeMan：2465发1收2条件4；2478发1收16条件20；2481发1；2484发2收1条件1；20197本次零合格命中。同图许可不能合并，字段出现不等于事务执行、关卡可达、原服NPC或TW1.0原始ID。

来源ZIP960字节SHA256 3c4774d955c155af0d426f419ce672dba0d2321caa81a27232d4ab2353225cd2、原JSON4546字节SHA256 901e835c921557da9dae7380b70aac0522fe4ff251c888de4289c91fb0da34f6、永久Git blob 7d771b2aa4f39646879659303f4926045ae730cc，完整链与负例重放见STONEAGE-QUEST-NPC-ITEM-ACCEPTANCE-R1。原始包、NPC原文件和商业服务端未加入Git或执行。

最高下一项QUEST-NPC-FLOW-LINK-06：只针对本轮已命中的后代ExChangeMan EventEnd记录核对同一条事件中的发/收/条件组合，不声称真实流程；无明确共现即UNKNOWN、停止。Stage A 7 PARTIAL+2 OPEN，Stage B GATED、R79暂停；原始早期任务、服务器执行和阶段终验均未恢复。


## 2026-10-17 — QUEST-NPC-FLOW-LINK-06 有限同EventEnd配置关联

原固定保存包上重做独立来源取得，9项测试及源SHA验证在Action38997164871/job117292136171 SUCCESS。后代4,985 NPC引用、30模板歧义、15次缺参；旧49角色完全匹配。分隔到27匿名EventEnd记录，其中3条不同ID共现：2条条件与收回2465/发放2484，一条条件与收回2478/发放2481；其余16同ID多角色、8单角色。不能拼成全部伐木流程，原始台湾1.0商业服ID/交易/存档未证明；旧20197零命中只限定语法与来源。派生报告Git blob b9f04bd7956a25a249e182fad4db2f0459719327，原始源未入库，验收链见STONEAGE-QUEST-NPC-FLOW-ACCEPTANCE-R1。

NEXT STAGE-A-PORTFOLIO-CHECKPOINT-02：停止后代NPC无限加深，重新按九系统真实未恢复游戏内容、初代来源可达性和用户审阅关口排序。若无新官方/定年独立早期资料，不再沿同事件向原服任务事实扩写。Stage A未终验、Stage B GATED、R79暂停。


## 2026-10-17 — STAGE-A-PORTFOLIO-CHECKPOINT-02 重新按游戏行为与早期可信度排序

本次对照当前九族联合审阅、阻塞分级、第一方2001-04-18 JSS手册、TW1.0客户端五类交互记录、后代伐木同EventEnd永久档案。九族依旧7 PARTIAL+2 OPEN，7条体验仍是原版客户端结构/后代或现代条件参考、不是初代商业服完整可玩体验。27条后代ExChangeMan同记录与3条跨物品关联在其来源层级内有效，但不能继续据此铺成原始1.0任务图。

组合检查点 docs/STAGE-A-PORTFOLIO-CHECKPOINT-R2.md、research/recovered/STONEAGE-STAGE-A-PORTFOLIO-CHECKPOINT-R2.json 为五类第一方行为设证据合同和停止条件：记录点首次供品/重登、三村组公车3分钟/最多4人/免遇敌、医疗/付费宠技/收宠、送货/矿石劳动、普通落地物品未知时长消失。TW1.0的S:C位置、WN泛用窗口、人宠/物品状态仅是可观察字段**形状**，目前无同版服务事件的绑定，不能冒充2001手册对应台湾1.0服务器执行；真实ACK、车站地图边/费用、工作道具和奖励均保持OPEN。

重新排序：**Highest NEXT EARLY-VILLAGE-SERVICE-JOURNEY-01**，限既有认证JSS2001手册和TW1.0客户端输入/观测面，以5条玩家行为的前置、反馈、缺失的服务端字段形成可否证的规则合同，收束于5行完成或UNKNOWN；之后若无新证停。TW10-ORIGINAL-VISUAL-CALLSITE-02及ORIGINAL-SERVER-CONTENT-REOPEN均仅在新的原始运行/同年代真实材料出现时重开。连续两包无新的规则事实/版本归属/实质衔接则停止分支重评。旧recovered25 NPC、R79暂停、7+2族门禁与Stage B GATED保留。这个组合检查点本身只是工作排序与已存证据验证，**没有新增初代内容载荷、商业服务端回放或复原百分比**。远端CI及main验收只以实际后续运行结果为准。


## 2026-10-17 — EARLY-VILLAGE-SERVICE-JOURNEY-01 五类村庄生活行为来源分层规格

在2026-10-17最新main 70e700243d4ecf363029601f60de7e01a51d4d49上启动，先读取HEAD/tree、最近提交、Actions、连续性协议与全量CURRENT-STATE，再对照官方2001-04-18 JSS手册及原版台湾1.0客户端UI消息形状。五类行为仅限记录点、长毛象公车、医疗/宠技/收宠、送货/矿石工作、普通落地物品消失；13项早期文字断言与12个原客户端通用观察槽仅作为不同来源的并排契约，不宣称同版NPC/服务器事件绑定、原始写盘ACK或实际操作画面。详见 docs/specs/STONEAGE-EARLY-VILLAGE-SERVICE-JOURNEY-R1.md 与 research/recovered/STONEAGE-EARLY-VILLAGE-SERVICE-JOURNEY-R1.json。实际证据仍未新增原始商业服内容、1999样本或真实游戏回放。

**NEXT STAGE-A-EARLY-SOURCE-GAP-TRIAGE-01**：逐个核对村庄服务关键未知是否有新的、可认证的早期一手资料可补。无新证据即标记UNKNOWN并转九族联合审阅，不靠后代NPC继续扩写、不开R79。Stage A 7 PARTIAL+2 OPEN，Stage B GATED。新来源合同独立CI与主线结果必须实际验证后才能宣称通过。



## 2026-10-17 — 五村服务来源可得性审计后转联合审阅

EARLY-VILLAGE-SERVICE-JOURNEY-01的五类行为来源合同已独立成功后，STAGE-A-EARLY-SOURCE-GAP-TRIAGE-01有界检查供品及ACK、公车收费和真实相邻路线、医疗宠技/回购价目、送货矿石任务奖励及普通落地物到期计时。没有取得可核原版同年代、同业务字段的新增一手记录；网页阅读器错误不代表存档不存在，空检索不是全网不存在。每项明确OPEN_EVIDENCE_LIMITED及重开触发，停止基于后代素材编造初代完整任务。报告 `docs/STAGE-A-EARLY-SOURCE-GAP-TRIAGE-R1.md`、机器清单 `research/recovered/STONEAGE-STAGE-A-EARLY-SOURCE-GAP-TRIAGE-R1.json`，分支源Action39001916143 SUCCESS。

**新的最高NEXT STAGE-A-JOINT-REVIEW-DECISION-01**：向用户提交已完成的九系统联合审阅资料、五类缺源证据、版本标签、可复现但不属于原版商业服的参考流程及不可恢复边界，请用户确认是否按证据受限状态收束Stage A，或继续某项具备新证据的初代内容补证。用户的“继续”仅授权继续Stage A日常研究，不等于默认批准Stage B。正式用户审阅之前保持7 PARTIAL+2 OPEN、Stage B GATED；R79暂停。没有理由重开泛用辅助函数或人工计算百分比。


## 2026-10-17 — STAGE-A-JOINT-REVIEW-DECISION-01 待用户明确审阅

已从实时GitHub main重新核验并形成可否证的九系统+七玩家流程+五阻塞+五村服务审阅交叉表：
`docs/STAGE-A-JOINT-REVIEW-DECISION-R1.md` 与
`research/recovered/STONEAGE-STAGE-A-JOINT-REVIEW-DECISION-R1.json`。
这个交付**不是新历史资料**，初代世界/NPC/任务奖励、同版人物宠物具体输入、原服持久化及真实原版画面仍缺直接执行证据。
首次独立源Action39002948717/job117309506410 SUCCESS（证据和否证门），后续归档与main提交必须再查。

**最高NEXT AWAIT_EXPLICIT_USER_STAGE_A_REVIEW_DECISION**：呈交独立的 A继续具名一手补证、B认可证据受限历史研究检查点、C暂停待源 三种选项；不替用户决定，单纯「继续」保持Stage A。即使用户选B也只是记录Stage A有限审阅结论，Stage B的引擎、内容及生产需要单独讨论/授权。未收到明确决定前九系统7 PARTIAL+2 OPEN、Stage A未用户验收，Stage B GATED，R79暂停；不无限重复低价值审计或猜100%进度。

## 2026-10-17 — STAGE-A-EVIDENCE-LIMITED-REVIEW-ACCEPTANCE-01 授权后的正式路线切换

用户针对前一轮A/B/C决定明确委托助手“按照你认为的最优解选择就行 哪怕后续出现错误需要补充改正我们还可以改 我相信你的选择”。本轮按最新远端 main
`abf584d7858c4089aef0b103c41270665f2c8219`核对完整连续性与最近三项SUCCESS主线CI后，采纳**B：证据受限的Stage A研究检查点接受**。

“研究检查点接受”与“初代原游戏恢复完成”独立：九族原有7 PARTIAL+2 OPEN及七代表体验/五阻塞/五早期服务缺源均保留，未经认证的商业服务端世界、NPC/任务、奖励、保存与画面真实运行不算完成；没有全局复原百分比。源资料若有可归属新证，只针对具体业务/版本重开Stage A，旧谱系与反例不删改，R79仍暂停。

**最新NEXT STAGE-B-JOINT-DESIGN-DIRECTION-01**：讨论现代单机新石器的时代/村落出发、人物与宠物关系、回合制、第一次骑宠情感目标、逐步扩展地图/文明、版本化数据和版权合规独立美术；使用`docs/STAGE-B-COLLABORATIVE-DESIGN-BRIEF-R1.md`为预备议程。该阶段为**讨论预备，不是已完成共同设计**。目前未最终决定引擎、未开启新引擎工程、新剧情/地图制作或商业营运。旧Roadmap内所有早期“Highest NEXT”均为当时历史状态，并被本条取代；对应机器决议见`research/recovered/STONEAGE-STAGE-A-EVIDENCE-LIMITED-ACCEPTANCE-R1.json`。


## 2026-10-17 — 新增外挂历史与宠物/任务完整性双证据清单（DD-025）

在Stage A证据受限审阅已获授权接受之后，用户明确强调外挂对各年代石器体验至关重要、未来值得改为合规单机“内挂”，并追问原版所有任务、全部宠物数据、二维图片、精灵动画、成长等是否真正齐备。经本轮查验结论**并未全部复原**：TW1.0原资源125,996图像号/464动画组不是宠物数量；原版graphic_id至实际SPR/帧/UI/地图绑定未闭合；recovered25 active enemybase988行/备表640行是后代记录不是1999物种全集；初代任务/NPC/事件标记/奖赏与服务器保存依然OPEN。

新增史料谱系初录`docs/STONEAGE-LEGACY-ASSISTANT-TOOLS-CATALOG-R1.md`及宠物覆盖度清单`docs/STONEAGE-PET-QUEST-CONTENT-COVERAGE-RECHECK-R1.md`，由JSON记录14来源/16家族/12项候选原生功能，按2001—2002同期玩家证据与2016+、2020+、2023+晚期软件生态区分。早期资料作为外设功能存在证据，不认证最早发行时间；旧外挂可取便利性，不移植作弊协议、复制/特权漏洞。

**新最优NEXT PET-ASSET-GROWTH-CATALOG-MATRIX-02**：为一组可核验的TW1.0身份与2.5后代宠物模板建立来源/版本/名称/图形号/动画/属性/成长/技能/遇敌位置/任务联动矩阵；真实缺数据即OPEN，不误报已全部复原。**并行后续 LEGACY-ASSISTANT-PROVENANCE-EXPANSION-02**：先找早年开发者发布日志、同代截图及具体函数出现年份，不编造后期产品2001首发史。四季度Stage B共同设计不应在这些资源缺口未识别前锁定宠物全集和高级内挂生产范围；仅可讨论玩法方向与体验价值。Stage A旧技术成果继续有效，R79 PAUSED_NON_BLOCKING。


## 2026-10-17 — PREPRODUCTION-HISTORICAL-CONTENT-AND-WIKI-READINESS-01 全域前期准备交付顺序

用户本次进一步强调：老石器全部可核实宠物、NPC、任务、交互/登录/选角界面、人物二维模型、资料官网与外挂所有已知功能，都应先整理作为新作共同设计的素材；未来玩家可查宠物和任务的网站也要提前考虑通用数据结构。**并不表示现在启动新游戏或网站实现**。本节点把此前宠物和外挂双线扩充成覆盖22领域、7个来源版型、15条真实关系连接的版本化全域清单和19个未来网站查询集合，交付docs/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.md及同名JSON。原数据仍缺初代商服任务/NPC、原版UI渲染实证与所有宠物跨表连接；所有未知保留UNKNOWN。

按“数据完整性和未来可使用价值”排序：
1. **PET-ASSET-GROWTH-CATALOG-MATRIX-02**：有可靠同版身份时先对宠物名、资源graphic_id→SPR动画、基础属性/成长、技能、出没/抓捕地点建立真实矩阵，没证据不插值。
2. **ORIGINAL-UI-LOGIN-AVATAR-REVIEW-01**：复查原始客户端登录、人物创建、人物2D动作、NPC窗口、背包/宠物窗口、战斗展示和音效，从可验证的实际图片或二进制调用轨迹追溯，不抄晚期UI为首发样式。
3. **WORLD-NPC-QUEST-SOURCE-JOIN-01**：按版本核可见地图/NPC/对话/任务/条件/道具/奖励/登出后标记与缺口。
4. **LEGACY-ASSISTANT-FULL-FEATURE-ARCHIVE-01**：有名有版本地研究全部辅助软件功能及变化，不预先删除“未来不要”的功能史；不运行可疑外挂或做越权/复制。
5. **HISTORICAL-SITE-IA-AND-WIKI-EXPORT-CONTRACT-01**：搜集原官网和可靠同期资料站页面结构，设计同版实体查询与版权发布检查规则，不写网站运行服务。

首次源Action39007115468已实际SUCCESS，当前历史长文追加与远端主线验收还须独立完成才可宣称。原Stage A历史有界结论仍有效，现因用户补充材料要求重开有意义领域核对；整体复原百分比不能计算，Stage B只讨论准备，正式生产、网站和高级内挂一律未启动；savedata R79继续暂停。


## 2026-10-17 — PET-ASSET-GROWTH-CATALOG-MATRIX-02 源字节索引关联完成，宠物身份未证

新增直接针对四份TW1.0原资源派生gzip索引的逐条跨表核验，Action39024292573和39024503298真实SUCCESS：125996 ADRN bitmap，464 SPR组，39065段animation，242085 frame；238593非空frame全部有原ADRN bitmap身份，3492帧为0xFFFFFFFF空哨兵，其他无法连接帧为0。九个可复核原SPR组样本、各示例bitmap/direction/anim_no存在`research/recovered/STONEAGE-PET-ASSET-GROWTH-CATALOG-MATRIX-R1.json`。特别`spr_no=100410`有352个纯哨兵帧，不能因为有SPR组就说那是某只宠物的完整立绘。外部后代资料988行敌人表、662名称哈希和实际原宠物图形/增长关系仍不同版本、未验实。

本里程碑仅将**同版原SPR动画帧→原位图数据**关系验收，不把S:K graphic_id身份映射、宠物物种名录、原服HP/成长/技能/原野出没、人物/宠物实际画面补成已完成；无原始图像字节提交及版权移植。真正首版宠物内容后续再根据同版server master/原客户端图形查表或一手截图重开。

**最新NEXT ORIGINAL-UI-LOGIN-AVATAR-REVIEW-01**：查原登录/选角/人物2D图像身份/动画/操作界面及对应原客户端/同期图片资料的真实来源；优先识别已存在证据，无法核验不能编造历史UI。其后按既定22域目录推进WORLD-NPC-QUEST-SOURCE-JOIN-01、LEGACY-ASSISTANT-FULL-FEATURE-ARCHIVE-01与HISTORICAL-SITE-IA-AND-WIKI-EXPORT-CONTRACT-01。Stage A旧证据有界审阅仍有效，Stage B生产、玩家百科建设不启动，R79暂停。


## 2026-10-17 — ORIGINAL-UI-LOGIN-AVATAR-REVIEW-01 2001玩家图片索引和台湾1.0原始资源一致性

2001-06-14 17173玩家曾公开stonepic图号类别（NPC、宠物/人物照片、人物/宠物动作、UI），2026-10-17源实测Action39025092843 SUCCESS：16个原位图范围其数字ID全部存在于台湾1.0原盘，后续6段超出125995的图号全部不存在。首次Action39025014067失败仅为工作流job标识问题，旧记录保留。因来源只是玩家分类，不能据存在性验证官方同版实际图片用途、玩家可选人物数或宠物物种数。作者声称“大陆版登陆画面”图126766不在原台湾1.0；真正原登录/角色创建布局仍未重现。

新highest NEXT WORLD-NPC-QUEST-SOURCE-JOIN-01，优先原版任务、NPC与玩家活动真实资料交叉表；其后外挂全功能与玩家网站史料分层。历史来源缺席不推测初代世界图或奖励；Stage B生产未开始。


## 2026-10-17 — ORIGINAL-UI-LOGIN-AVATAR-REVIEW-01 原版调用与官方建角规则

从实时main a041af528eec13a4e832efca09b6c165a146ff8e/tree43265d6f1c317dfc4c396eba91c7934341ba8b41启动，核对最新分支、四条提交、同HEAD全部已返回主线Actions SUCCESS、无待合并PR；完整CURRENT-STATE 1892518字节与Git源逐字节一致，README/协议/Design/Timeline/Source/Roadmap和22域准备顺序已核。最高NEXT原版登录/选角/人物核查，本轮只推进该具名游戏界面内容。

实际重新取得原TW1.0零售盘，校验保存包MD5/SHA1、523449360字节镜像与sa_3.exe SHA256，五种消息ClientLogin/CharList/CreateNewChar/CharDelete/CharLogin各找到一个静态直接发送调用候选与已固定接收回调。建角14压栈、原序列化器13字段转换及字段来源建立有界关联；EARLY_LINEAGE对应的body/face分别加载RVA0x13f709c、0x13f78ac，运行时实际图号、SPR/bitmap身份、完整人物数及屏幕布局均未证明，不把内存地址当图号。

通过JSS官方manual02真实链接取得manual01，实际快照20010418082314（请求20010418083149发生跳转），10924字节，无Shift-JIS替换。第一方明确姓名8个全角字符、能力20点、属性10点且最多分配两类、方向预览/换色/脸部选件/出生村与删除确认；这仅属JSS2001官方说明，不认证1999或台湾1.0同数值同执行。原网页/图片/旧exe未入Git，派生来源及验收链单独永久归档。两页无img引用不代表原游戏无画面。

规格 docs/specs/STONEAGE-TW10-LOGIN-AVATAR-R1.md；机器目录及来源凭据见STONEAGE-TW10-LOGIN-AVATAR-CATALOG-R1.json和STONEAGE-TW10-LOGIN-AVATAR-ACCEPTANCE-R1.json。初次manual01链接片段处理、数字地址转录修正及一次合成测试失败均保留，不据错误零结果下历史结论；独立源/归档/main CI仅按随后真实结果登记。

**最高NEXT WORLD-NPC-QUEST-SOURCE-JOIN-01**：按版本连接现有地图/NPC/对话/任务/物品/条件/奖励与登出标记，选择具名实质记录；无初代同源证据则UNKNOWN，不展开无界后代脚本链。人物实际图号/完整画面需要原版选择表值/边界、运行轨迹或可认证同期截图再重开。其后继续外挂全功能及历史资料站结构。Stage A既有有界研究验收保持、九族7 PARTIAL+2 OPEN；新作/网站生产与R79不启动，无全游戏百分比。


## 2026-10-17 — WORLD-NPC-QUEST-SOURCE-JOIN-01 弥生/日美子任务静态实体连接

从实时main4dfab89f83c45c310dc54a9e6dfee23dae58df48/tree49d9a430fb859a537c2846e264460c6e8ec07686启动，最新主线Action39026108091实际SUCCESS，完整当前状态1897442字节及README/协议/Design/Timeline/Source/Roadmap与Git远端源一致。最高WORLD-NPC-QUEST，具体范围先取弥生—日美子送贝壳，停止于同保存包实体/事件/物品连接，不扩通用helper。

真实重新取固定recovered25双分卷、合包SHA256，通过Action39026390233/job117378103320：4985创建引用中保留30模板歧义和15缺参，精确Big5创建名称彌生、日美子分别连接地图2000/1000（两地图头存在），borncorner配置退化范围55,92与57,124，各有3条EventEnd道具记录。该后代活动itemset两ID2414、2415与NPC条件/收回/发出字段相连，名称字节SHA256分别精确等于Big5“不可思議的貝殼”“仙尼亞的花”。活动表13252行与未活动0710表13910行分别验证，不以备表替代setup。两物品dropatlogout原值0、vanishatdrop原值1；cost80/40是原字段，不当任务奖励/真实商店价格。彌生同记录收2415发2414、日美子同记录收2414发2415仅为配置候选，不声称条件满足、事务、初始任务态、完整循环或原服保存。

独立网页来源Action39026558177实际SUCCESS：新浪当前早期汇编、17173诗雨2001-12-10发表栏玩家文章、2003-05-29双向友谊指南分别记录。玩家位置参考114,662与637,491不自动对应保存包NPC出生范围，坐标语境未知；送物中间贝壳与交付后的花不合成同一物。一次Wayback Availability在20011231附近对指定新浪URL返回空快照集，只限该查询，不推全网没有历史存档，亦不认证当前文章字节在2001原样存在。

规格 docs/specs/STONEAGE-WORLD-NPC-QUEST-SOURCE-JOIN-R1.md，原来源派生/三网页见证/可查询实体关系/保管链分别为STONEAGE-WORLD-NPC-QUEST-SOURCE-JOIN、WITNESSES、CATALOG、ACCEPTANCE的R1 JSON。只存有限姓名查询、数字/指纹与关系，不存原脚本对白/地图/旧exe，不运行原商业服。完整布尔条件、执行顺序、TW1.0相同NPC/地图/ID与持久态仍UNKNOWN。原TW1.0 WN/M/MC只是通用观察面，不与后代配置冒充同版事件。独立归档及main CI必须随后按实际结果登记。

**最高NEXT LEGACY-ASSISTANT-FULL-FEATURE-ARCHIVE-01**：以既有16家族清单中SADE早期版本序列、SaCh/SACHXP与STA同期有版号原文为第一有限批，逐版本列真实功能、出现证据与缺失；好坏功能先完整归档，不现在选择新作采用/实现。人物资源与原服任务只有新可认证同版源才重开。Stage A旧有界验收保持、九族7 PARTIAL+2 OPEN；新作/资料网站生产与R79暂停，不报全游戏百分比。


### WORLD-NPC-QUEST 真实主线验收及STA2.52首批功能见证

WORLD源分支ec2aa8fac09f13a61c73c9542b2dd9c08c9fc1b9/tree0976772698b7470b721452eb726050988d9c2f55已在新复核main不变、ahead3/behind0、17路径0删除后非强制快进。该HEAD主线12项实际SUCCESS，含任务目录Action39026873280、网页见证39026873383及历史/资源来源门。两名NPC、六记录、两ID是后代配置连接，不是原台湾1.0服端完整任务；源ZIP/raw/blob与所有主线运行写入WORLD-NPC-QUEST-ACCEPTANCE-R1。

同轮顺序推进外挂资料第一条具名版本：STA2.52用户评测源Action39026963821实际SUCCESS，原发表栏2002-03-10、作者☆阿仇☆。9条派生记录分别保留报告可用、请求、菜单行为未验证、比较项、对策和传闻，自动脚本恢复/自动缩屏不能误记为已实现；非开发者完整更新日志，原软件未运行，不决定新作采用。派生JSON与独立ZIP/raw/代码blob保管见STONEAGE-LEGACY-STA252-FEATURES及ACCEPTANCE-R1，只有元数据永久存档；本条后归档/main CI另按真实结果确认。

**下一最高NEXT仍LEGACY-ASSISTANT-FULL-FEATURE-ARCHIVE-01**：继续SADE早期版序列及SaCh/SACHXP—STA有版号对照，按实际发布/评测/作者回忆分层；已完成的STA2.52单篇见证不等于该工具全部功能或全部外挂。之后转历史官网/资料站查询结构；不重开R79或新作/网站生产。


## 2026-10-17 — 早期辅助工具有限版本批与下一资料结构包

SADE8条部分更新回顾+0.2g独立变体、同期比较7观察面、配置7观察面、SaCh1.23名称版号见证已形成有界规格STONEAGE-EARLY-ASSISTANT-VERSION-HISTORY-R1及派生保管链，源Action39033762316实际SUCCESS。不等于所有辅助工具/功能完整，原开发者发布记录、精确发布日期与构建兼容仍缺；已有STA2.52九项档案独立保留。

本有限批停止横向扩张，组合前轮宠物资源、登录/建角和具名NPC任务归属成果，**最高NEXT HISTORICAL-SITE-IA-SOURCE-MAP-01**：从真实早期站点导航和文章分类设计未来百科查询结构草案，链接内容域、来源层、年代/版本与缺失，不做现代想象版史料；交付研究目录与可查询结构，非网站代码/部署。工具全功能缺口有具名开发者发布资料才再开。7 PARTIAL+2 OPEN与Stage A既有有界审阅保持；Stage B新作/网站生产、R79仍不启动。归档及主线验收按后续实际CI登记。


### 主线验收与资料站总工作包的当前边界

早期辅助工具归档77f5ffb主线13项实际SUCCESS，来源及归档门完整运行列表在版本ACCEPTANCE-R1。新增HISTORICAL-SITE-IA-AND-WIKI-EXPORT-CONTRACT-01的逐主张查询草案：四份真实派生blob、六个有界查询例；不是网站实现，也未认证原官网布局。SOURCE-MAP-01是该总包的子阶段简称。

**最高NEXT HISTORICAL-SITE-IA-AND-WIKI-EXPORT-CONTRACT-01**：实取有日期的原运营商栏目树和同期媒体索引，固定链接/快照/来源链后映射既有22资料域与19集合，再评审逐主张版本、未知与权利字段。不把当前迁移站导航当早年原站，也不将原资源直接公开。其余原版任务/宠物/UI与工具穷尽缺口保持，未启动网站或新作生产。


## 2026-10-17 — 历史官网真实链接子包有界收束

JSS原域2001快照实取：手册索引47出链，两首页框架引用menu/top，两手册正文和top.html合成6合格页/85有序链接/67 distinct目标；64片段在已取目标快照存在，但不同快照不证明同刻站点或点击成功。三源Action39035106551、39035257822、39035407893成功，全部ATTEMPT与最终派生/代码/ZIP链保留。menu.html原域响应因正文品牌门不足保持未合格；17173四候选实际2004/2006排除早期图。只认证有限导航与资料域候选路由，不认证完整原站或游戏数据，见STONEAGE-HISTORICAL-SITE-NAVIGATION-R1。

**最高NEXT仍HISTORICAL-SITE-IA-AND-WIKI-EXPORT-CONTRACT-01：同期媒体索引子项**。以具名旧文原URL/主机迁移或精确档案索引查1999—2002媒体栏目，至多一个有限来源包；无新具名源则登记边界后转22域前期准备组合评审，不遍历官网所有出链。已有逐主张查询合同与实际JSS来源连接可供后续共同设计参考；不选网页框架、不生产新作、不重开R79。



## 2026-10-17 — 17173同期媒体有限档案回放后内容域源缺口定序

从原五篇17173迁移文章中的旧经验目录原URL出发，GitHub Actions 39038286655已完整执行三条有限Wayback直接回放；实际只返回2006年两次同一快照及2004年一次宠物目录候选，无1999—2002合格目录节点，不能证明它当年不存在。保留报告SHA/ZIP/原始Git blob与逐URL实际时间；EARLY-MEDIA-ARCHIVE-SNAPSHOT-BOUNDARY-01转OPEN_EVIDENCE_LIMITED，不再追逐猜测索引。

按原22域完成来源连接及UNKNOWN矩阵。**新highest NEXT PET-IDENTITY-SAME-BUILD-SOURCE-TRIAGE-01**：围绕现有20玩家别称、TW10 graphic_id与原SPR资源寻找直接同版物种映射的具名原始资料；无法获得时就停止并转任务/NPC原服源补证。九系统7 PARTIAL+2 OPEN、Stage A有界验收、Stage B GATED、R79暂停均不变；不计算全游戏复原百分比。

 
## 2026-10-18 结果导向复原队列超越此前局部NEXT

依据新的`PREPRODUCTION-22-DOMAIN-SOURCE-READY-PORTFOLIO-REVIEW-02`有界22域机读盘点，宠物/原始任务同版服端原材料缺失不是继续空转helper的理由。TW1.0原始ADRN/SPR索引可真实核查，新的TW10-RESOURCE-CATEGORY-SPR-JOIN-01已得原帧与玩家静态/动作区间的物理交集：人物动作区间137508帧/240SPR组，宠物动作区间70236帧/124SPR组；玩家命名的NPC/宠物头像/人物相片/物品/UI静态段0SPR帧（**不是未使用**，静态渲染路径尚未查）。源Action39076262089成功、ZIP原字节及JSON SHA256独立校验已保存；原版具体宠物/角色名、图像显示及原服任务继续OPEN。

**当前最高NEXT TW10-ITEM-STATIC-BITMAP-SOURCE-SELECTOR-01**：仅研究TW1.0物品静态位图（玩家称5973—7003）与已具原客户端S:I协议字段、静态图选择/渲染调用的真实连接，限定可复核的内容载荷和缺口；不自造原物品名称、商店售价/料理或以0个SPR引用否认客户端静态图存在。之后依来源可执行性表移向地图和音频。22域所有旧历史状态不变，7 PARTIAL+2 OPEN与Stage B GATED、R79暂停。历史研究不是用新增R编号或测试数计算完成百分比。

 
## 2026-10-18 — T02物品静态原盘实证验收候选

此前T01原SPR帧与外部2001图号类别交集有完整数据，当前T02新增同构建S:I/I/C的graphic_id位置与原台湾1.0ADRN物品静态区间的物理元数据：1031个bitmap号、1030份不同RD块SHA256，原图号6042/6077有相同块指纹；宠物相片121号均96×104。所有“物品”、“宠物相片”类别仍为**玩家标签**，字段值→bitmap号选择链、同版server itemset及游戏实际渲染未知。规格和可复算机读源 `docs/STONEAGE-TW10-ITEM-STATIC-BITMAP-SOURCE-R1.md` 与 `STONEAGE-TW10-ITEM-STATIC-BITMAP-SOURCE-R1.json`，并非真正原物品类型表。

**最新NEXT T03 `TW10-MAP-CONTENT-ORIGINAL-RESOURCE-BOUNDARY-01`**：从原零售盘/mapcache直接可认证的地图块来源出发做有界地理结构与原服资料差异，无法取得同版NPC/掉落/遇敌绝不填充。九系统、Stage B与R79全部旧限制保持。

 
### 2026-10-18 — T03原地图资源map_number关联检查

TW1原资源9286条去重map_number→bitmap碰撞属性，按仅供候选的2001玩家地形/大物件/NPC位图分类分为4571/1271/101，其他3343。新的交集由源Action39078746682实际SUCCESS，归档Action39079097177实际SUCCESS，但源属性**不等于野外地图floor id**；零售盘仍无field-map DAT，后代资源兼容仅用作跨版对照。详见`docs/STONEAGE-TW10-MAP-CONTENT-COLLISION-R1.md`与源JSON验收凭据。下一T04 `TW10-AUDIO-EVENT-SOURCE-GATE-01`：原盘声音文件/播放器调用与原世界事件的最小直接源连接；无同版运行选择事实则有限停止。

 
### 2026-10-18 — T04原音频选择边界核对与跨域下一批

真正台湾1.0原盘`sa_3.exe`来源独立Action`39080460322` SUCCESS、声音固定源不变。新识别编译体8处WinMM直接文件调用、1处DSOUND ordinal#1导入跳板及1处直接调用跳板；原`data\\se\\`与`data\\bgm\\`字样有原版字符串见证。原声音档案114内嵌索引、116外置音效及11 BGM**已经存在**，不重复算新发现；原游戏事件到具体音轨、实际播放参数和村庄/宠物语义依旧缺证。源码派生详见`STONEAGE-TW10-AUDIO-EVENT-GATE-R1.md`及原二进制逐字节验收回执。

**NEXT `PREPRODUCTION-CROSS-DOMAIN-MATERIAL-EVIDENCE-REVIEW-03`**：重新用T01～T04已实证资料检查22域实际内容闭环与缺源，优先解决能恢复原生故事、人物、宠物、NPC、真实场景的材料，而非继续无限扩展无同版事件值的底层工具链。7 PARTIAL+2 OPEN，Stage B GATED，R79 PAUSED。


## 2026-10-18 — R3实质材料复审与官方内容转向

T01～T04的图像/物品/地图/音频物理证据不等于具名原游戏内容。R3逐行保留22域旧状态，新增JSS2001官方介绍正文及10张实取原JPEG缩图的出处/日期/尺寸/观察；5个链接仅失败或晚期跳转，不推缺席。正文4月、图像6月不得伪装同刻或TW1.0同版。已有手册再整理12节、11组宠物与战斗/合成说明，不计新网页。完整源和来源层见STONEAGE-CROSS-DOMAIN-MATERIAL-REVIEW-R3以及STONEAGE-JSS2001-PET-INTERACTION-AND-VISUAL-R1。

**当前最高NEXT `JSS2001-OFFICIAL-EVENT-QUEST-CONTENT-01`**：沿已验JSS top.html真实event.html链接，有限查一个可定年的官方活动/任务内容页，尝试取得具名剧情/NPC/道具/参加限制；无合格实质内容便记录界限停止，不递归全站、不再扩无同版事件实参的API树。不把JSS2001默认升级成1999/TW1.0，7 PARTIAL+2 OPEN、Stage B/百科生产GATED、R79暂停。


## 2026-10-18 — 官方社交活动有界收束与四村会场资料

原最高JSS2001-OFFICIAL-EVENT-QUEST-CONTENT-01从真正官方event索引及eventjss正文取得两项社交活动公告，未取得NPC任务脚本，故不扩名不副实的“任务恢复”树。同索引具名eventmaz会场页组成有限相邻材料包：四村聊天室入口方向坐标、售票/引导职能、领票进场流程、北侧右起大厅/婚礼场指引及6张实际编辑标注原JPEG。HTML4月和图片6—7月不同刻；所有同TW1.0、原服地图/NPC实体、领取事务归属继续OPEN。具体来源/矛盾/登记见STONEAGE-JSS-OFFICIAL-EVENT-AND-VENUE-R1。

**最高NEXT `JSS-OFFICIAL-EVENT-RESULTS-PET-ATTRIBUTION-01`**：只读取索引真实eventjsk结果页，有限查已发表活动结果是否给出实际参与/奖励宠名字与身份；未知仍未知，不把“未登场稀有宠”猜成某物种，不递归评论或表单、GM后台。7 PARTIAL+2 OPEN、Stage B及百科生产GATED、R79暂停不变。


## 2026-10-18 — 官方第一回结果归属有界收束，转回宠物规则资料

JSS-OFFICIAL-EVENT-RESULTS-PET-ATTRIBUTION-01取得实际官方结果目录16题目/14详情链接与唯一相关第一回搞笑结果正文。正文主办方称完成并列4奖，临时增设个人奖；稀有宠仍未具名。第一回不能拼到此前第二回预告，年份/日期/服务器缺失不补；模板横幅“ねるとん”与正文不一致、误预取07页后纠正09的真实记录保留。三图404、三Availability429后停止，0图像取得，不编画面。具体来源与反例规格STONEAGE-JSS-EVENT-RESULTS-PET-ATTRIBUTION-R1。

官方操作/图像、会场、结果几包已有实际内容归属成果，但不能再因目录有14出链就继续穷举活动页。**最新最高NEXT `JSS-FIRST-PARTY-PET-FAQ-01`**：从已有已验top真实faqmenu.html链接取一个官方FAQ目录，只追最多一条明确宠物、捕获或成长相关正文。若只是安装/账号问题则有界登记后重排，不猜页面名、物种参数或重开原服master/API树。7 PARTIAL+2 OPEN、Stage B/百科生产GATED、R79暂停均维持。


## 2026-10-18 — 官方FAQ有界收束与具名补丁来源优先级

JSS-FIRST-PARTY-PET-FAQ-01实际取得2页官网FAQ：目录41标题/9已修正标签，正文12问答；真实宠物寄存/技能、名称窗口、具名活动触发/证书故障文献补证，及决斗刷新强者表、窗口256色/时间调色板的早期说明。此处无原始服务器修复代码、成长公式或同版物种ID。ヤン＝ミト任务问题仍在调查，不并入目录修复组。faqquest非凭文件名可认证攻略，未访问其它正文/修复下载。22域既有状态不变，文献层增加仅限规格列明项目；不继续FAQ/活动全站遍历。

**最新最高NEXT `JSS-FIRST-PARTY-PATCH-PET-QUEST-01`**：从已认证top真实verup.html取一个更新记录入口；只在实际条目或出链明确对应宠物寄存、指定宠物条件或捕获证书时，最多再追一份必要记录。交付具名玩法变更/修复的日期及版本归属；仅下载说明或无匹配条目则保留未知停止并回到跨域材料评审。不得猜文件名、下载运行程序、填原服脚本或将2001补丁当TW1.0；7 PARTIAL+2 OPEN、Stage B/百科GATED、R79暂停不变。


## 2026-10-18 — 单页早期宠物更新史结束，回到实质材料全域审查

JSS官方verup保存40条1999—2000自标日期，本轮限定7组寄存开放/技能缺陷族/邮件条件/合成调理增加。2001档案不认证1999现场部署，泛称bug不等于FAQ具体症状，12小时与5分钟条件不扩成通用宠物规则。未得三具名任务的具体补丁或构建号，原服/TW1.0身份仍OPEN。见STONEAGE-JSS-PET-PATCH-HISTORY-R1。

**最新最高NEXT `PREPRODUCTION-CROSS-DOMAIN-MATERIAL-EVIDENCE-REVIEW-04`**：把近几包真实操作/图像、会场、第一回结果、FAQ与七日期合同回连22域，选择一项能增加具名人物/宠物/NPC/任务或实际场景的材料来源。复用旧表，不重复API/资源编号，不因40条而全站遍历；缺同版源就明确限制转另一域。7 PARTIAL+2 OPEN，Stage B/百科GATED，R79暂停。


## 2026-10-18 — 用户扩展官方版本参考范围（DD-027）

全官方版本的宠物、任务、模型/动画、界面、地图及玩法均为可收集的设计参考，即使新作不采用。早期基准复原与全官方参考库并行：保留每版自身来源、地区/构建、事实层级与变化；后期内容不必先成为TW1.0同版事实才有研究价值。既有7profile不是完整官方发行表，官方衍生产品/社区改造各自分层。

最高NEXT仍PREPRODUCTION-CROSS-DOMAIN-MATERIAL-EVIDENCE-REVIEW-04，但本轮用户澄清成为其范围约束：22域同时检查官方版本/地区覆盖及资料可取得性，先复用既有目录，再选一项能新增具名宠物、NPC/任务、人物模型/场景或玩法差异的真实来源。避免只围绕原服未知参数/低层helper停滞；以价值、可得性和缺口安排有限资料包，不盲目下载全补丁。尚未收齐的版本列缺源，不宣称全库完成。采纳取舍留给后续共同设计；7 PARTIAL+2 OPEN、Stage B/百科GATED、R79暂停。


## 2026-10-18 — 用户追加世界历史/叙事连接与主动查缺要求

DD-027增加官方世界历史与故事关系维度：现实版本时间线和虚构世界事件线分开，续接/前传/地区分支/译名/改写矛盾/机制调整/UNKNOWN逐条按源判定。同步关注文明/势力/神话、地理/生态/宠物关系、人物动机/任务后果、世界变化和玩家成长情绪，避免只存数值与资源列表。开发意图需文献，研究推断/未来新设定分别记HYPOTHESIS/DESIGN。

最高NEXT仍PREPRODUCTION-CROSS-DOMAIN-MATERIAL-EVIDENCE-REVIEW-04，须在全官方范围及22域现有材料中主动查上述缺口，选择一项真实具名内容源。此处只扩充资料关系要求，不宣称版本必然同一世界线、不开始新世界观创作、不以更多规划取代取源。Stage B/百科GATED，原7 PARTIAL+2 OPEN及R79暂停保留。


## 2026-10-18 — R4全官方材料复审与实际世界叙事来源

R4逐行保留22域旧状态，复用JSS操作/图像/会场/结果/FAQ/七日期合同，并落实DD-027全官方与故事关系要求：旧华义2005主页真实game01链接的新正文明确尼斯/伊甸/文化/海底/失落世界5组与9版本标签，机械文明/失落世界问题仍OPEN。原顺序5.0/7.0先于6.0不强改成严格时间线；2005回顾不晋升初代同版正史。另取得8张2006原GIF插画切片、1片404缺失，7片首次502与重试成功并存，不补全画面或猜物种。

**最新最高NEXT `TW-WAYI-OFFICIAL-INTRO-DETAIL-01`**：沿正文真实game01_01—04之一，标签未知时按源序，最多一页，先验正文题名内容再归具名人物/宠物/故事/环境或玩法，不能据编号猜题。取得一项实际内容合同即停，失败留界后重排；不继续全站/Flash/表单/程序。全官方覆盖目录尚不完整，7 PARTIAL+2 OPEN、Stage B/百科GATED、R79暂停，均不变。


### 2026-10-18 — 官方冰世界详情：12个原地图名与六场景

按远端main `12d45f491ece5aa53a66b8ce17a64ddab7978cd6`、tree`1af86bcfd66c850024e7fd8e462ecd26667e2ad5`重新启动，核338分支、0开放PR、同HEAD9项main SUCCESS及连续性/完整CURRENT等七文件。TW-WAYI-OFFICIAL-INTRO-DETAIL-01沿真实第一出链，只取game01_01.asp正文及其六张原场景图；实际主题为瑞爾亞斯（冰世界），不从编号预设宠物/任务。

正文实际快照20050614003328，26346B SHA256`f7e10861dd9f8ee3bef19c46863c7bc818d17635ffecab41b0189c63ff2b234c`。取得官方12个新地图原名、冰雪/作物生长困难/居民叙事和“第十大莊園”序位；未恢复地图ID、路线、坐标、NPC/任务/遇敌表。六原JPEG全部220×163并逐张目视，实际快照2006-01-05，与2005正文分开记录；图注分别指冰顫通道、议会厅、24小时便利店、庄园专卖店、训练所和武器店，不能提升为真实交易/全天服务/已知NPC/原生分辨率。

正文“瑞爾亞斯”与三图注“薩爾亞斯”原样保留为UNRESOLVED_VARIANT_OR_TYPO_OR_DISTINCT_NAME，不静默纠错、确认别名或合并实体；骑乘外观仅HYPOTHESIS，无宠物种类或规则。精确客户端构建/首发日期及冰世界等于整个失落世界仍未证，不回填JSS1999/TW1.0。按现有19集合归档合同新增19个研究条目（地区描述1、原地图名12、场景6），不是19张地图，不新增npcs/pets/quests实体。原HTML/JPEG/程序不入Git。

永久派生与规格：`research/recovered/STONEAGE-WAYI-OFFICIAL-ICE-REGION-R1.json`、`STONEAGE-WAYI-OFFICIAL-ICE-REGION-CONTENT-CATALOG-R1.json`、`STONEAGE-WAYI-OFFICIAL-ICE-REGION-SOURCE-INTAKE-R1.json`及`docs/specs/STONEAGE-WAYI-OFFICIAL-ICE-REGION-R1.md`。本地19项边界测试通过；新增独立一正文/六图、两JSON逐字节重放工作流，远端结果与ZIP/raw/Git blob保管链须随后实际验收，未提前宣称。

**最高NEXT `TW-WAYI-OFFICIAL-INTRO-DETAIL-02`**：沿既验介绍页第二条真实未读game01_02.asp，最多一正文，先核题名/内容，形成一份具名宠物/人物/故事/环境或玩法合同即止；若重复、空或有限取源失败，记录具体结果并回全官方22域队列，不自动递归第三/四页。Stage A仍7 PARTIAL+2 OPEN，Stage B/百科GATED，R79暂停，无整体百分比。


## 2026-10-18 — TW-WAYI官方第二详情实质内容取得
实际2005华义官网game01_02.asp获单页新材料：宠物装备七种基本部位/三种足型、宠物体型与元素差异、导师5%声望文案和任务日志完成状态描述。原字节固定并在 Actions 39121796764 独立重放成功，4项负例PASS；原 HTML 不入库，资料作为后期官方系统参考，不反填TW1.0/JSS1999运行规则或宣称上线。最高下一有限批CROSS_VERSION_GEAR_MENTOR_QUEST_SOURCE_GAP_REVIEW-01：选择现有官方来源、具名补丁或手册中最有机会闭合具体装备/导师/任务日志规则的一个内容证据，不重开底层无限展开。仍7 PARTIAL+2 OPEN、Stage B/百科GATED、R79暂停。


## 2026-10-18 — Cross-version gear/mentor/quest source gap review accepted as a bounded content reference

Reused the byte-qualified Taiwan Wayi 2005 game01_02 operator page without claiming its actual server implementation. Connected a 2005-06-08 contemporary Taiwan 8.0 release article to this operator system description; its 2005-06-09 simplified 17173 republication explicitly credits Bahamut and **does not count as independent corroboration**. A separate undated Mainland/Jinshan-labelled 17173 8.0 portal records gear eligibility and synthesis, mentor and quest-log menu entries, and one named new quest (爱作画的少女). These are region-bounded source assertions rather than authenticated build/game state. A regional operator/portal label cannot substitute for actual patch provenance.

New permanent bounded source-bridge JSON, MD specification, five structural regression cases and a real green GitHub Actions check are retained; original source HTML and media are not. Highest NEXT: CN80_NAMED_QUEST_ORIGINAL_SOURCE_TRACE-01, one bounded archived-content inspection along the portal's existing quest link; failure or directory-only results must remain OPEN with a precise source blocker. The lack of original server scripts, pet equipment itemset, mentor prestige transaction and quest state flags still blocks actual gameplay closure. Stage A7 PARTIAL+2 OPEN; Stage B and wiki production GATED; R79 PAUSED.


## 2026-10-18 — CN8 named portrait quest source-graph and 8.5 conflict

The 17173 8.0 quest index's real hyperlink points to a 14-step portrait quest walkthrough. Both current live source URLs have strict UTF-8 source SHA256s and independent GitHub Actions replay, producing one named quest evidence record, two guide-described NPC roles, five level-one pet-to-pigment linkages and a five-portrait reported reward. Current online bytes do not certify the original publication date or original commercial server. A 2012 8.5 promotional article instead describes a prerequisite (无法逃离的审判) and one portrait; the undated 8.0 guide lacks a prerequisite statement. Neither narrative is silently promoted to original gameplay truth. The original and derived full provenance are in STONEAGE-CN80-PORTRAIT-QUEST-R1 with permanent Git report and archive.

NEXT CN80_PORTRAIT_PREREQUISITE_VERSION_BOUNDARY-01 is a tightly bounded upgrade gate: admit only an archived contemporary first-party/patch or version-qualified script to settle prerequisite and reward count, else keep conflict OPEN and rotate back to the 22-domain material queue. All original client/server identifiers, original quests and runtime state remain unproven. Stage A historical families 7 PARTIAL + 2 OPEN; Stage B and wiki production remain GATED; R79 PAUSED.


### 2026-10-18 — Portrait prerequisite conflict limited stop, new 2005 player-source gate

The source-qualified CN80 8.0 walkthrough graph is now on main with all 11 checks passing at the exact integrating HEAD. A 2005-07-19 **edited** Bahamut player guide exists for the separate quest 无法逃离的审判, but its text does not establish that the portrait quest depends on it. The undated 8.0 guide's omitted prerequisites and later 2012 8.5 article's explicit prerequisite/one-portrait prose cannot be flattened into a proven version patch or original-server transaction. This finite inquiry is OPEN_EVIDENCE_LIMITED_NO_FIRST_PARTY_RULE.

Highest next: CN80_JUDGMENT_2005_NAMED_CONTENT-01, one source-bounded early dated guide to recover actual named NPC/item/profession constraints with source attribution—not to assert game-rule equivalence, recurse across all articles, or build new-game logic. After a useful content attribution or an explicit evidence stop, rotate back to the 22-domain portfolio. All Stage A PARTIAL/OPEN, Stage B, R79 and copyright gates persist.


## 2026-10-18 — 2005审判任务具名文献关系审计
从巴哈姆特2005编辑标记的《無法逃離的審判》与17173大陆8.0任务页整理具名三NPC、三职业、两项指南前置、风地水机关、地图与物品的**来源限定文本图谱**。前者写OURSA出处，后者内容重合且增补细节，无法证独立原作者/2005首版与原服务器构建；不把同源玩家转载当两份一方证明。与后期《爱作画的少女》前置冲突仍OPEN，原始服务端状态/物品NPC IDs未证。机器来源`STONEAGE-CN80-JUDGMENT-NAMED-CONTENT-R1.json`，新结构测试/Actions验收必须以运行事实为准。

**最高NEXT `ALL_OFFICIAL_VERSION_NAMED_CONTENT_SOURCE-01`**：停止同文循环，按全官方22域优先下一份具名/带年代、地区的官方宠物、故事、场景、任务实质来源；缺同版规则写UNKNOWN。Stage A7 PARTIAL+2 OPEN，Stage B/百科GATED，R79暂停。


## 2026-10-18 — 台湾8.5同期官方版本材料：具体世界线叙事与具名任务

全官方22域队列的新实物包选2006-06-21台湾8.5同期GNN/GameZone报道（另有2006-06-22明示巴哈姆特来源的17173转载）：新闻明确宣称7.5《精靈的召喚》→8.5《魔域大冒險》剧情延续，雷爾/艾巴登、魔军与伊甸大陆边境的有向叙事关系；GameZone另具名任务「支援前線」。计划升级日期不算已部署；与7.5/8.0同世界绝对无断层尚无证明，原服务端实体、条件、坐标和技能奖励保持UNKNOWN，2006素材不倒填TW1.0。

已形成按来源/版本/年代的机器关系、文献规格和6负例测试，以及独立原新闻字节探测工作流；探测成功与源SHA归档必须以Actions实际结果为准，新闻载体不能冒充华义原官网。文献交付 `STONEAGE-TW85-PERIOD-PRESS-WORLDLINE-R1`。

**最高NEXT `TW85_NAMED_QUEST_FIRSTPARTY_MATERIAL_GATE-01`**：只对真正同年代华义第一方任务公告、旧官网源或官方带版本构建原件尝试一份可定年的具体「支援前線」或雷爾/艾巴登任务来源；若无，登记缺源、转其它具名内容域，不再循环新闻转载与无构建玩家攻略。原九族7 PARTIAL+2 OPEN、Stage B及网站GATED、R79暂停。


## 2026-10-18 — 台湾8.5「支援前線」第一方归属闸门与同期任务见证

2006-06-21同期新闻仅证明华义公开宣传具名「支援前線」；对华义2006官网相应任务/补丁和原服源的本次有界访问未获得合格的独立第一方原件，Wayback访问错误仅说明这次无法读页面，不能作为历史材料不存在的结论。玩家指南巴哈姆特G2 sn=3199显示2006-06-23 **编辑日期**，留下具名伊秋娜、奏敷、布克瑟与双补给→魔界之门/詭異洞窟→前哨营地/前线包裹→焦热之地交付链；所有地图floor、NPC/物品ID、具体触发/奖励仍UNKNOWN。后期Wiki同名攻略三个地点坐标有单格差异、另载前置等级，不强合并为2006真服坐标。

该资料已作为来源限定的文献任务图谱，规格`docs/specs/STONEAGE-TW85-SUPPORT-FRONT-GUIDE-GATE-R1.md`与机器源`research/recovered/STONEAGE-TW85-SUPPORT-FRONT-GUIDE-GATE-R1.json`。无原页独立字节SHA，不得将结构CI写成历史原件已认证。

**新的最高NEXT `ALL_OFFICIAL_VERSIONS_NEW_NAMED_FIRSTPARTY_DOMAIN-01`**：按22资料域和全官方发行范围另取真正一手、具名、有日期的非相同任务材料；不同年代单独归属，缺原脚本就登记边界，不继续转载扫荡或savedata R79。Stage A仍7 PARTIAL+2 OPEN、Stage B/百科GATED、R79暂停。


## 2026-10-18 — 第一方新领域取源收束与版本覆盖复审

新最高ALL_OFFICIAL_VERSIONS_NEW_NAMED_FIRSTPARTY_DOMAIN-01取华义2005真实第三详情的一份正文，增加海底融合、任务角色名片状态、五项精工合成扩展的来源限定规格。5类/20宠只具名4类，未补第五类；名片结束保留和下次覆盖、普通手动交换区分；无配方/概率或原服执行。规格与永久源SHA见STONEAGE-WAYI-MARINE-SOCIAL-CRAFTING-R1。

**NEXT OFFICIAL-VERSION-COVERAGE-MATERIAL-REVIEW-05**：复用22域/官方源目录，检查近期台湾2005–2006材料偏重，选另年代/地区一份能带来具名宠物/人物视觉关系的真实材料；一份来源、一项身份连接或精确缺源结论即止，不默认遍历第四详情，不以新规划或无源helper替代实质材料。九族7 PARTIAL+2 OPEN、Stage B及百科GATED、R79暂停不变。


## 2026-10-18 — R5全域复用与日本2003真实人物入口

海底融合/名片/精工第一方资料已在90c7b7cf主线11门实际通过并归档独立ZIP/raw/Git保管链。相邻R5复用22域旧状态，发现近期台湾2005–2006偏重；实际重新取得20031214055553 Hangame官方安装页，从图片按钮静态onclick属性确认chara.asp真实目标，未执行脚本，未读人物页或获得人物像，不以路径名/安装日期认证1.74a构建。机器复审STONEAGE-OFFICIAL-VERSION-COVERAGE-MATERIAL-REVIEW-R5.json保留出处和未知。

**最新最高NEXT JP2003-OFFICIAL-CHARACTER-VISUAL-SOURCE-01**：沿该一条真实出链取一正文，先核主题与实际时刻，最多一份有明确身份对应的原图；有归属关系或具体缺源即收束，不爬站、运行程序或扩大旧台湾任务循环。Stage A/Stage B/R79边界不变。


## 2026-10-18 — 日本官方人物身份/网页资源对应收束

JP2003-OFFICIAL-CHARACTER-VISUAL-SOURCE-01取得实际2003人物正文，运营商明确无固定人物名字；以12研究页面位置绑定原表格中24个图像引用，非原游戏ID。只取一张头像GIF，实际2006快照与2003正文分开；其余23图与客户端模型/配色/动作未验。规格与派生见STONEAGE-JP2003-CHARACTER-VISUAL-SOURCE-R1，未启动新游戏/网站生产。

**最高NEXT JP2003-OFFICIAL-PET-NAMED-VISUAL-SOURCE-01**：从该页真实宠物标签沿chara2.asp只读一正文并验主题/年代，有具名宠物和明确图像关系时最多核一原图；否则保留精确缺源回22域，不递归第三/四分栏，不执行程序。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79暂停不变。


## 2026-10-19 — 日本官方宠物分页目录有限闭合

初始宠物一页/一图资料包完成资格后，仅选同页两条真实分页链接组成相邻有限闭合包，实得124条网页名称/编号/图像引用（45+45+34）。前两页2003、第三页2004、唯一原图2006分别归属；不认作某日完整原服物种或客户端ID。每条记录独立保留出处、空缺和版权，原件不入Git。规格与派生STONEAGE-JP-OFFICIAL-PET-CATALOG-R1。

**最高NEXT OFFICIAL-PET-VISUAL-COVERAGE-AND-VERSION-REVIEW-01**：复用124条与22域，限定最多12条既验原图引用的一次视觉资料包，覆盖不同分页/表格组，核实际时刻/字节/帧与具体失败；不自动取全部123图，不进入其它栏目/程序，不猜别名/属性。九族7 PARTIAL+2 OPEN、Stage B/百科GATED、R79暂停不变。


## 2026-10-19 — 12张具名宠物图像实物与R6有限覆盖复审

从124条已认证引用取得12张实际网页图像并逐张目视，跨2003/2006/2008/2016快照；加既有1张共13引用实得，111未取。严格分离正文与图像时刻、网页插画与原客户端动画，不提升同版物种/数值/成长/技能结论。原124条目录不改，原件不入Git；新独立12图重取/摘要/完整报告cmp与保管链按真实结果验收。R6复用原22域状态，停止继续批量取宠物图。

**最高NEXT JP-OFFICIAL-TOWN-NAMED-GEOGRAPHY-SOURCE-01**：R5已证的town.asp真实静态出链，仅一正文并核实际主题，最多一明确关联图；交付一份具名地理/聚落/日常生活关系或具体缺源即止。没有正文则不从路径推内容，不递归同站；失败保留且轮换其它有身份来源。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79暂停不变。


## 2026-10-19 — 已验12宠物图后转向四处具名村落

宠物视觉内容6ef559c的10分支/11主线门实际全通过，完整独立ZIP/raw/Git保管链永久保存；R6选择的相邻town.asp一正文实取四村的名字与来源限定地理/环境关系，首图2006灰石建筑与2003正文分开，不猜建筑功能/地图ID/坐标。maps集合四研究记录不是已恢复原地图。新正文/唯一图独立源门与主线结果另验；原件不入Git。

**最高NEXT JP-OFFICIAL-VILLAGE-FACILITIES-SOURCE-01**：只沿本页真实设施标签town2.asp取一正文核主题，最多一明确关联图，整理设施/日常生活交互内容或精确缺源即止。不自动递归、不预设NPC和商店/恢复规则。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79暂停保持。


## 2026-10-19 — 13类村落服务源实物与R7地区轮换

沿真实town2.asp一正文认证13类设施描述，含宠物店不能买宠、家点贡献条件、问答门槛/费用、配送和普通步速无怪付费巴士等具体来源行为；不填原服ID/数值/运行事务。首图两次404，无像素，不升级旧建筑功能，其余12图未试。原件不入Git；独立正文重取/首图缺口/完整cmp及保管链/main结果按实际另验。R7保留22域全部原状态，停止连续扩日本分栏。

**最高NEXT TW-WAYI-OFFICIAL-INTRO-DETAIL-04**：明确重新选择原台湾介绍页已验真实第四详情game01_04.asp，仅一正文先核实际主题，交付具名系统/生活/故事材料或精确缺源/重复结论即止；不是默认追第四页、不按编号/站题猜内容、不取图片/程序、不递归。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79暂停不变。


## 2026-10-19 — 设施一方规则已验收，台湾具名游乐循环新实物

日本13设施内容8cd9dc8b候选10/主线11门实际全绿，独立原正文/首图404/完整报告和ZIP/raw/Git链永久留存。R7选择的华义第四真实详情仅取一正文，获得剧场艺术值、魔法牌挑战积分、宠物转轮买票下注积分三组具名描述；正文8.0和旧站题分开，积分钱包/概率/价表/实体ID和实际运行未证，童话/泛称魔王不回填世界史。新包独立源门及main结果另验，不借前包绿灯，原件不入Git。

**最高NEXT OFFICIAL-VERSION-COVERAGE-MATERIAL-REVIEW-08**：复用22域和已有官方源目录，先核早期关键缺口并选一个有身份的官方实物包；精确早期缺源时可换另一官方地区，给一来源/停止条件并开始取源。不重铺矩阵、不循环旧文/图片或R79。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79暂停保持。


## 2026-10-19 — R8早期材料复用：九节物品/邮件/社交/共用场所语义

复用22域后明确选已验JSS2001 manual02的九个尚未形成行为合同的节，不把旧原件/3个已有通用指纹计作新网页。新增物品操作、普通/宠物邮件及登出后果、名片开关、日期聊天文件、免费聊天室与有特定免票情形斗技场的来源合同；只取一个已知正文，无图片/程序，原服数值/ID/保存事务与同构建仍OPEN。独立一源摘要/完整cmp、ZIP/raw/Git及main须按实际验收。

**最高NEXT EARLY-SOURCE-MAIL-VENUE-CROSS-VERSION-BOUNDARY-01**：零新网络源，复用既有2001普通落地/2003设施/2005场所报告与本合同，有限衔接可参考概念及不能合并的计时/物品/场所/版本。不能用新R编号空规划或重开R79替代内容。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79暂停不变。


## 2026-10-19 — 早期九节已验与八组跨来源非等同关系

JSS九节语义内容d75d2d7a候选11/自身主线12门实全通过，独立已知手册/完整报告与ZIP/raw/Git保管链永久留存。相邻零新原源的五报告衔接产生8个sources比较记录，防止计时/票据/费用/场所/名片状态/积分等不当合并；它不是新增原件或实体，独立离线cmp和自身main另验，不借父HEAD绿。

**最高NEXT JSS2001-PLAYER-STATUS-LEVELUP-AND-KNOCKOUT-01**：同一已验正文仅3040/8020/8060三节，补角色参数/经验归属、升级奖励、气绝后果的早期一方合同；无新出链/图片，不从文字推完整原服EXP公式、数值变化或保存写入。不重开R79。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED保持。


## 2026-10-19 — 早期参数、升级、气绝来源说明

JSS2001-PLAYER-STATUS-LEVELUP-AND-KNOCKOUT-01将已知manual02的3040/8020/8060变成3个来源限定教程记录、19状态标签关系；全部早有通用指纹，不算新原件。四元素仅影响关系不造倍率，EXP prose不作完整原服算法，气绝战后1和可能回SP保留条件/时序，魅力/忠诚与四主参数/派生参数分开，初建点数不填升级未知。

**唯一最高NEXT JSS2001-PLAYER-PET-STATUS-AND-CREATION-BOUNDARY-01**：零新原源的现有报告有限衔接，厘清初建/升级、魅力/忠诚、捕获/经验和DP/排名；同原件不作独立双证，完成即回全官方材料覆盖队列，不循环公式/低层helper/R79。Stage A7 PARTIAL+2 OPEN、Stage B及百科GATED、R79暂停保持。


## 2026-10-19 — 角色规则已验收、七组语义边界后回全域材料

角色参数/升级/气绝三节同HEAD11候选/12主线门实际全部success，原源及ZIP/raw/Git保管链留存。相邻四份已验派生报告形成7组初建/升级、魅力/忠诚、气绝、DP/排名、捕获/经验的有限关系，阻止20/10点、60忠诚与差6条件跨语境搬用；两原正文同一运营商，零新增原件或实体。新包离线独立cmp及自身main另验。

**唯一最高NEXT OFFICIAL-VERSION-COVERAGE-MATERIAL-REVIEW-09**：停止本手册语义循环，复用既有22域/官方发行目录，选同手册之外一个有身份实质材料缺口，交代一来源/交付/停止条件并开始取源，不写空矩阵/低层公式helper/R79。Stage A7 PARTIAL+2 OPEN、Stage B及百科GATED、R79暂停不变。


## 2026-10-19 — R9回材料：日本官方早期世界/生活定位

七组角色/宠物衔接自身11候选/12主线检查全通过，永久ZIP/raw/Git回执留存；R9停止本手册循环，复用22域原状态后选择已认证game.asp一个正文。实取2003世界観分栏：四段5sources文献记录覆盖恐龙生活/图鉴宣传、石币商店与学校、组队表情交流和合作氛围；不是宏大世界史/具名NPC/物种总表。初次网页阅读器不可用保留，直接HTTP及本地独立第二取成功不证同构建原服，100下界不并124目录。原件不入Git，独立门/main须实际另验。

**唯一最高NEXT JP2003-OFFICIAL-GAME-FEATURES-SOURCE-01**：本正文真实ゲームの特徴静态game2.asp目标，只一正文核实际主题、时刻，得到一份实质玩法/内容合同或精确缺源即收束，不自动截图栏/图像/程序/递归。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79暂停不变。


## 2026-10-19 — 日本官方游戏特点实质来源

既验game2.asp真实标签入口只一正文，实际2003-12-14，恢复外观12类各4色不改参数、眼口/名片脸、五玩家组队/队长野外移动、道具合作与遇敌切战斗/图标/求助等五行合同；原图仅五引用声明无像素。12×4非48原角色、离队文案非任意运行事务、未知点数/ID/遇敌公式不填。新独立源cmp/main须实际另验，原件不入Git。

**唯一最高NEXT JP2003-CHARACTER-CREATION-VISUAL-REFERENCE-JOIN-01**：仅已验人物/初建/本报告有限离线衔接，分清网页位置/插画/可定制部件/外观维度/玩家姓名；无新源/资产/48实体扩张，完成回全官方材料队列。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79暂停保持。


## 2026-10-19 — 特点已验收，人物/初建参照有限闭合

特点内容10分支/11自身主线门全success并留源/ZIP/raw/Git回执。相邻三固定报告5比较将12×4外观、12网页位置/24图引用、玩家姓名、眼口名片脸、2006唯一像和2001初建点数分开，索引已有12位置但无新实体/ID/同构建join。零新增原件/图片，离线独立cmp/main须按实际另验。

**唯一最高NEXT OFFICIAL-VERSION-COVERAGE-MATERIAL-REVIEW-10**：复用22域选择有实际入口的实物缺口，给一来源/交付/停止条件并开始取源，不空矩阵或同文身份/公式循环，不默认递归截图/图片，不重开R79。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED保持。


## 2026-10-19 — R10有限UI实物补充，停止同站继续取图

人物/初建参照10候选/11自身main全绿、离线ZIP/raw/Git保管；按22域复审明确选截图像素缺口，新有界game3索引+首图包非自动递归。2003索引8引用，唯一GIF却2008捕获，275×200单帧见野外/人物状态/地图窗，另7图未尝试，非2003同刻原生UI/ID/运行认证。8screens=1图+7引用缺口，原件不入Git；独立重取/元数据/全cmp/main另验。

**唯一最高NEXT OFFICIAL-VERSION-REGIONAL-AND-DOMAIN-ROTATION-11**：停止日本同栏和剩余7图，复用22域/官方源索引，选择另一地区或版本/领域一份有身份实物，实际一来源/有限交付/停止条件并取源；缺则精确登记不空规划/猜链接/低层helper/R79。Stage A7 PARTIAL+2 OPEN、Stage B及百科GATED、R79暂停保持。


## 2026-10-19 — R11转台湾一方骑宠设计说明

停止日本图像后，真实官网取源先保留周年错题更正/无文字规则与具名转蛋公告404，再取制作人索引实际具名骑宠计划。2003-12-10为索引日期、正文2005存档，5条来源限定说明新手骑宠门槛、适配虎/较弱与易忠诚保护任务宠、成人礼后领的计划、快递任务+30等级宣称。不是已部署奖励/原服公式或1999/TW1.0骑乘；图说甲子非60级。新独立源cmp/main须按实际另验，原件不入Git。

**唯一最高NEXT TW-WAYI-NEWBIE-RIDING-SUCCESSOR-GATE-01**：只索引真实idno67《新手騎寵計劃（續）》、2003-12-23一正文，核主题/捕获，有限比较计划调整/实施边界，一材料合同或精确缺源即止，无图像/其它栏目/数值/R79扩张。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79暂停不变。


## 2026-10-19 — 前篇骑宠计划已验，续篇矿石工作一方线索

前篇10分支/11自身main实全success，源/ZIP/raw/Git留存；仅真实续篇idno67标2003-12-23、正文2005捕获，新增成人礼/骑宠叙事、渔村礦石研究者采柯奧山奇怪礦石线索及博物馆作者轶谈语境。未确认赠虎按计划部署，矿石奖励未知不搬快递+30；不合并村名/NPC IDs/普遍PvP权限。同系列非独立运行证人，具体赠虎脚本/原数值保持OPEN。新独立源cmp/main须实际另验，原件不入Git。

**唯一最高NEXT OFFICIAL-VERSION-MATERIAL-COVERAGE-REVIEW-12**：复用22域和官方源，停止同系列实施/矿工奖励推断，选另一内容缺口、一合格原源/停止条件并取源；同版原任务/补丁/服务端原件才重开实施问题。不自动其它栏目/图片/低层公式/R79。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED保持。


## 2026-10-19 — R12职业成长来源计划的新原件

全官方22域复审显式选职业入门/高阶技能来源缺口，仅已验idno64《全民就職計劃》标2003-11-14、正文实2004捕获。五文献记录描述新手参与动机、计划一转成人礼→八十级成人礼且降低就职任务难度、二级技能仍需一转以上及作者语境；入职与技能学习不可合并，不补职业树/技能名/原数值，未认证部署。两图未取，原件不入Git。规格/永久报告STONEAGE-WAYI2003-PROFESSION-ACCESS-PLAN-R1，独立源/ZIP/raw/Git及自身main按实际另验。

**唯一最高NEXT OFFICIAL-VERSION-RELEASE-SOURCE-COVERAGE-REVIEW-13**：停止本制作人职业/骑宠系列，复用22域/官方发行索引，优先另一地区或版本一有身份的实质内容缺口，给一实际来源/内容交付/停止条件并开始取源，有限失败精确保存；不空矩阵/猜源/图片批量/公式helper/R79。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79暂停保持。


## 2026-10-19 — 职业计划已验，R13大陆2.0经验表有实质数字内容

台湾职业计划10候选/11自身main全success并留独立源/ZIP/raw/Git回执。R13复用22域停止制作人系列，选择已知大陆2001官方2.0一正文；新结构化完整可见82等级经验对，原28行三组、两空对和不平滑数字，非新原件/原服务端表。累计/增量、角色/宠物、转生、82上限及跨版等同均未知，原件不入Git；独立门/main按实际另验。

**唯一最高NEXT CN20-OFFICIAL-NAMED-NEWCOMER-CONTENT-SOURCE-01**：仅本页实际「新入石器」入链sw/adventure.asp一正文，核实际主题/时刻，交一份来源限定新手/地理/NPC/任务实物合同或精确缺源即止；目前未读，不预设实体、不自动其它页/图像/程序/公式。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79暂停保持。


## 2026-10-19 — 大陆2.0初宠/村落经济/新手建议一正文

只真实新入石器入口取2001官方站无署名正文，10来源记录含初宠照料、肉/石头、护士/购装备/组队叙事及加点/魅力/忠诚建议；官方托管非运营商原创/独立原服验证，20点/防40/魅-4与-1/$2000到100均保留语境，不推公式/阈值/强制重置。两图只未取引用，原件不入Git；独立取源/全cmp及自身main按实际另验。

**唯一最高NEXT EARLY-OFFICIAL-NEWCOMER-AND-PET-CARE-BOUNDARIES-01**：零新原源，只固定已有手册/初建/宠物报告与本指南有限比较，明建议/原数值边界/同源复述，形成实质关系规格后回全官方材料队列，不补跨版公式/实体/R79。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED保持。


## 2026-10-19 — 初宠指南验收，八组早期资料使用边界

新手一正文10候选/11自身main实全success且保留独立原SHA/ZIP/raw/Git回执。相邻4固定派生/3原正文离线形成8关系，初建/每级点数、主人/宠物升级忠诚、魅力/初捕60、KO/药救、回SP/防40和组队EXP分开，不补同构建公式/原服实现。原件不入Git，独立离线门和自身main实际另验。

**唯一最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-14**：停止新手/手册比较，复用22域/全官方源索引，选一具名宠物/NPC/故事/任务/环境实质缺口，给真实来源/有限交付/停止条件并取源，有限失败精确保留；不空矩阵/同文数值/helper/R79。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED保持。


## 2026-10-19 — R14大陆具名宠物首目录实物

停止新手/手册建议比较，R14复用22域，显式选真实新增宠物一正文实2001捕获：40网页格34名字+6问号占位，同格40未取图引用，非客户端ID/40已恢复物种/104完整名册。原大小写/文件顺序与未知属性保留，原件不入Git；独立源/全cmp/自身main须实际另验。

**唯一最高NEXT CN20-NEW-PET-NAMED-VISUAL-REFERENCE-01**：仅第一具名阿米朵位置7真实7.JPG一图，核实际捕获/摘要/格式/尺寸和目视或具体缺源即止，不扩其它图/分页/程序/别名/属性。旧当时未取报告不改。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79暂停保持。


## 2026-10-19 — 目录34具名已验，阿米朵一图视觉材料

首目录10分支/11自身main实全success并留ZIP/raw/Git保管链；相邻只第一具名阿米朵7.JPG一原图实20011205，83×90单帧JPEG精确目视，正文20011204分开。新增1视觉补充引用旧位置，非新物种/客户端精灵/动画/模型，39其它图未取，原件不入Git；独立唯一图/全cmp/自身main实际另验。

**唯一最高NEXT CN20-NEW-PET-CATALOG-FINITE-PAGINATION-01**：明确只两条已验41-80/81-104分页正文作有限目录闭合，核实际题/捕获/格名图关系与占位，具体缺源保留；不其它图/程序/新出链/猜属性或完整原服物种数，闭合或精确缺页后回全官方材料队列。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79暂停保持。


## 2026-10-19 — CN2.0新增宠物两分页实取，104网页位置有限闭合

本轮按实时远端main abcf7a09661bde146cc91e3e271e31bb79a63c7e / tree28c7676ad8a1cc1b3b845adedc1399c08dfaa324启动，373分支、0开放PR、同HEAD10项main实际success、无in_progress；无关旧queued37642417333保留。七连续性文件完整CURRENT及历史前缀、最新树/提交/Actions、22域portfolio和首目录/视觉/R14报告重新远端读取并与新origin/main逐字节核对，无AGENTS.md；不以旧聊天进度推当前。

按唯一最高CN20-NEW-PET-CATALOG-FINITE-PAGINATION-01只取两已有真实href正文，未取图像/程序/新出链。阅读器初不可用保留，直接HTTP初请求20011204194619后分别实跳new_pet1.asp的20011023173210（66451B SHA256dfc191c476dc5c968e1957e58070297d048475e3f3f8d8d5e897ccae56ea0c65）与new_pet2.asp的20011023181629（64382B SHA2562c7aea8d0319c2070d5c7590a95bfc892c2463deb76c5b95fca8c281549c76f0）。严格GB18030，页题石器时代2.0/文题新 增 宠 物/导航1-40、41-80、81-104。两新页十月、旧首目录十二月，分时来源拼合不作同日/同构建或捕获顺序=补丁顺序。

41-80实际8×5具名40格，从呼鲁鲁到欧林吉鲁；81-104实际5/5/5/5/4格具名24，从佩露夏到朱利洛斯。末行缺</tr>但4个td完整，解析按起始tr保存，不漏杨格斯/耶普鲁/尤里蛙/朱利洛斯，不补第105格。位置84裘里蛙配104.JPG、位置89砂鲨配87.JPG，原图引用/大小写/HTML声明尺寸按格保存，非文件号=网页序号/客户端ID。新grid SHA分别4f194a8b3bec04b36a37f629751841509bfaa26bbfb9fccee1b230941f01d182、a52bc5cf3b5b8660b29bbcfd5162463d69c986e546733026e55bbe8b97e72818。

永久STONEAGE-WAEI-CN20-NEW-PET-FINITE-CATALOG-R1.json/规格合计104网页位置=98具名+6原占位，本轮新增64具名位置；首40条逐对象保持原派生，重复???不合并/造名，旧目录/视觉报告不重写。阿米朵既有位置007一图仅引用固定Git补充，新图请求0、跨报告其余103图未取；这不是104物种/104新加宠物或原服完整名册。游戏ID/属性/成长/技能/捕获/骑乘/跨地区实体等同仍未知。原HTML/图片/程序不入Git、版权未批准新游戏复用。

工具/17反例及结构测试、独立仅两实际十月原页+固定父/视觉Git metadata、全报告cmp、derived-only工作流已加；35相关本地测试通过。第二次精确网络重取和候选/自身main源job、ZIP实下载/raw全字节/Git blob验收分别按实际记录，未发生不提前称绿。全部初始历史前缀/失败/22域原状态保留。

**唯一最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-15**：本有限三页目录CLOSED_QUALIFIED_THREE_PAGE_WEB_CATALOG_NOT_GAME_ROSTER，停止分页/图像扩取，返回全部官方版本/22域材料队列，选择具名NPC/任务/故事/环境实际正文缺口、真实来源和有限取源/停止条件；不空矩阵、数值公式循环/helper/R79。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79 PAUSED_NON_BLOCKING，无整体百分比。


## 2026-10-19 — 宠物三页实际保管验收，R15转公共设施一正文

三页内容e3008b0367da961999ada7634debccf9d4f1a1b4 / tree0a1177683927b12ed23e16adae624571ddda6f7e的10候选、自身11项main实际全部success；run39240145512/job118018715274独立仅两十月原页+固定父/视觉Git metadata，17反例/完整cmp。artifact12180084942实下载ZIP7302B SHA25695d7b27a15151ae22b0922d975ea9572bc510f88cb315d402cd89ca0492d6fbf，唯一derived.json173510B SHA2568bcda48e9e8e298efe446b02f0039146fa4a81e509ca4d08c4989e6448f59fdb等于永久Git blobf950aa33af0b3ec8693b2867758faf006aee546b。STONEAGE-WAEI-CN20-NEW-PET-FINITE-CATALOG-ACCEPTANCE-R1.json永久保留实际源job、ZIP/raw/Git及精确HEAD的10/11检查；此有限目录闭合不作原服物种/同日全名册。

按最高OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-15复用全部官方版本/22域来源队列，停止宠物分页及图像扩取，选择大陆村落环境/通用NPC服务/经济真实正文。已取new_pet1.asp实际侧栏「公共设施」href /ZHUANQU/stoneage2/sw/facility.asp；旧宠物派生未列此出链，不伪称旧JSON指针。阅读器不可用保留，直接HTTP初请20011023173210实跳20011204213609；73356B SHA256e18f0bced4935358e3be28e328d50a49a6dfbb8c26476a98c211892974e7ba16，严格GB18030，题石器时代2.0/文公共设施。入口十月、正文十二月分时来源，不推补丁顺序。

新增14设施类别tutorials研究记录：村长家、医院、武器店和防具店、道具店、宠物店、肉店、便利商店、竞技场、聊天室、道场、纪录点、长毛象快递、长毛象公车、加美航空；逐行标题/图片引用/HTML声明尺寸/服务段SHA及来源限定转述。服务内容含村长家教学与家族管理、医院医师/护士/药剂师/美容师、5宠携带与寄宠教学、萨尔吉姆/卡鲁它那加工材料和玛丽娜丝/加加料理材料、原票返村、礼堂、南北百人道场不同挑战、贡品/在线人数、快递押金和陆海交通。原文表示每村设施不一，不给每村强配全表。

护理/竞技场免费「10级以下」不推含10阈值；医师等泛称不当具名NPC；5宠/100关/100题不补完整master/题库/奖励；加工重复段不当独立证人；纪录点回顾不补版本日期；快递「早上（太阳出来前）」与天黑限制原样限定转述，不修成日出后/游戏时钟；十分之一押金只页面描述不实现公式。14图全未取，HTML声明尺寸非实际图片元数据；原服NPC个体ID/坐标/库存/收费/任务脚本与跨地区等同未知，原HTML/图像/程序不入Git。

交付STONEAGE-WAEI-CN20-PUBLIC-FACILITIES-R1.json/规格、R15实质复审、13反例测试及已知侧栏+唯一新正文/全cmp/derived-only工作流。设施13+分页17相关本地测试通过；精确第二次网络重取/独立源job及自身main/ZIP/raw/Git保管须按实际另验，不借父11绿。22域原状态与完整初始历史前缀保留，七资料profile不是全部发行清单。

**唯一最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-16**：本设施14行正文有限关闭，返回全官方发行/22域材料队列，优先具名NPC/任务/故事真实正文缺口，选一真实资格入口与有限取源/停止条件；不自动扩14图、服务数字比较、宠物页/数值公式/helper/R79。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79 PAUSED_NON_BLOCKING，无整体百分比。
