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
