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


## 2026-10-19 — 公共设施独立验收与本轮收束

公共设施内容82c1aa6d3a378732ba8bcdf38adcd4c5e69bf078 / tree0f30f74df96a74331b39f178827fcdebc5c593a7的10候选、自身11项main实际全success，无该HEAD失败/重跑。源run39240854129/job118021014559精确重读已知十月侧栏+唯一十二月设施正文，13反例/行段SHA/完整cmp通过；不冒称runner重演初次阅读器错误/跳转。artifact12181666070实下载ZIP4941B SHA25679a01ca15102b0aff681cae13261486dc056e12592c3ed8721db22e759d03436，唯一derived.json26065B SHA25649e48c23b2fc97f5ac64b03ce0b4f2848d04fe722005c5392e778941b33e887b等于永久Git blobfd5fc0e792a1d86b5509aaf663d6d68cf2750fcf。STONEAGE-WAEI-CN20-PUBLIC-FACILITIES-ACCEPTANCE-R1.json永久保留源job/ZIP/raw/Git及精确HEAD的10/11实际检查，CI过期不丢来源保管。

本轮实质：两新分页64具名位置使有限三页目录104位置=98具名+6原占位（非104原服物种/新加物种）；再一官方设施正文14类别和服务描述（非14具名NPC实例）。共3新正文、新图0，48相关本地测试通过；两内容HEAD分别自身11项main实全绿。118研究记录均核七必需字段/19集合合同；旧首40记录、22域原状态与完整初始CURRENT/历史/来源/路线前缀保留，无原HTML/像素/程序入Git，无历史删除。十月/十二月捕获、末行缺tr、图片文件号错位、10级以下含义及快递太阳出来前括注保持来源边界，不造跨地区等同/服务器脚本。

**唯一最高NEXT保持OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-16**：停止宠物三页/14设施扩取，复用全官方发行与22域源索引，优先具名NPC/任务/故事真实正文缺口，选一有真实资格的入口、有限取源与停止条件并实取；不空矩阵、同文数字比较/公式/helper/R79。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79 PAUSED_NON_BLOCKING，无整体百分比。此回执新HEAD必须观察自身Actions，不套用父内容11绿。


## 2026-10-19 — R16五岛世界文字及台湾已开/大陆未开的英雄岛具名攻略

按实时远端main f8f12ebc5e6465cde3e3bda1d04cb32693667913 / tree31bd8fd12a5269d24827e05fa7af64d06ac5afeb启动，375分支、0开放PR、同HEAD10项main实全success；无in_progress，旧无关queued37642417333保留。最新HEAD/tree/提交/Actions、七连续性文件完整CURRENT及历史前缀、22域portfolio/R15/设施派生重新远端读取，Git blob与新origin/main逐项相符；树4647项未截断、无AGENTS.md，不据旧聊天进度推当前。

按唯一最高OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-16停止宠物三页/设施扩取，选择具名任务、NPC及世界时间材料。先探测strategy/index.asp根路径不是实际设施侧栏href，此来历明确保存，不假造资格链；已知设施原文实际「英雄岛」直链/zhuanqu/stoneage2/strategy/hero/1.asp重新核实，旧经验页仅曾列链接不作已读正文。阅读器两次不可用不证历史缺源；直接HTTP初请20011204213609后，根页实20011201212305、69680B SHA2566b29b0115bcc37c4afbbe72e9061ea3ddc13d139a63753919e1a2260bd95e63c（ZHUANQU变zhuanqu），攻略实20011201035642、65205B SHA2561f5ce2dd27e58b9ad3f90b847559bfec1a10667c41c38e23b7c5475de89c198a；严格GB18030/题石器时代2.0。入口设施20011204213609/73356B/e18f0bced4935358e3be28e328d50a49a6dfbb8c26476a98c211892974e7ba16为已知源重取，非第三新正文。精确第二网络重取全报告cmp成功，未重演初次跳转/错误。

根页实际为五岛导航静态隐藏面板，不是具名任务目录：吉鲁岛石/山洞危险、波拉岛英雄萨姆吉尔出生地/龙群占领/借村中小黑猪回50年前、沙姆岛三岛中转海底隧道、塞伊那斯岛尼斯东侧/两村/雕像/海产、加鲁卡岛森林/木文明/加加与卡鲁它那多小岛渔村。五段文字DOM id/长度/原段SHA保留，grid37c1efbe215dcd03f3b1902cf49d60647cb771f733b9d9fa1056bac09a4a7186；50是相对世界年差，非2001减50/任务等级。保留萨姆吉尔村村/英雄萨姆吉尔村字面片段，未静默修正文名。Map_V2.gif仅一主图引用/HTML580×468及五HTML热区，像素/格式/真实尺寸全未取；area坐标非游戏坐标，五目标正文未读、未强配面板与南北岛身份，JavaScript未执行。

攻略原题前往英雄岛，明确「英雄岛在台湾已经开放,大陆目前还没有开放！！」；大陆官方站题2.0≠大陆实装、无署名攻略不证运营商原创/同版服务器执行，台湾精确构建和初发表日期未知。LV80以上/成人礼前置只源描述；日美子萨村村口56.124→送花给鱼村弥生55.93→获不可思议的贝→萨村村內70.40黑乌力对话进入「拨拉岛-英雄岛」。鱼村出生可直接找弥生取贝壳，来源分支[2,3]与其他村[1,2,3]分开，未豁免等级/成人礼。第三步未明写交贝/检查/消耗，不补物品事务。点号定位原样保存，不当原服spawn/地图ID；黑乌力不升宠物物种/模型。

波拉岛/拨拉岛、小黑猪/黑乌力、弥生/旧recovered25彌生、无名花/仙尼亞的花、当前不可思议的贝/未读4.asp不可思议的贝壳均不默认证同实体或同构建；「找寻找孙女」原导航错字保留，2/3/4.asp三正文及北岛交叉引用未取，不因红暴之谜导航推当前宠物奖品。交付STONEAGE-WAEI-CN20-ISLAND-HERO-CONTENT-R1.json/规格和R16复审，maps5描述+quests1攻略+npcs3提及共9研究记录，不是9原服实体；20新反例/与设施共33相关本地测试，独立已知设施+两新正文/全cmp/derived-only工作流。原HTML/图像/程序不入Git，22域/历史前缀保留，独立源job/ZIP/raw/Git及自身main需实际另验，不借父绿。

**唯一最高NEXT CN20-HERO-GUIDE-SOURCE-RELATIONS-01**：只本新报告与既验recovered25花贝配置派生作有限来源关系，核准方向、角色/地点和缺失前置/出生条件的界限；零新原件/图像/攻略/程序请求，不把相似人名/花贝结构当同版同任务，一份有实质关系规格后返回全官方版本队列。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79 PAUSED_NON_BLOCKING，无整体百分比。


## 2026-10-19 — 英雄岛与后代花贝配置六组有限来源关系

岛屿/攻略内容96ed8d94574dfcce50a4a339e8b2e89898cb3d27 / tree20942cea1ef1790d82220e44854f692fe9ec6d2b的10候选检查实全success；源run39242359029/job118025969676实际只已知设施+两原正文、20反例/段落pin/完整cmp。artifact12181014645实下载ZIP4656B SHA256b3edeb7c5e17fc503dedd6435c78c220d8bea44e91908bd4245a7c02ac2022a2，唯一derived.json17457B SHA2564fef4edbb48e837fb49cdcab7faf801040b5d2dfcab7c1ec03e4f8bfc786fe77等于永久Git blob8d95a7b2a64f0aea43b0c25beb8472d1fd114d94。该内容自身main需按实际另验，不能仅套候选10绿。

按当前最高CN20-HERO-GUIDE-SOURCE-RELATIONS-01只两固定Git派生：上述岛屿/攻略报告，及既验STONEAGE-WORLD-NPC-QUEST-CATALOG-R1.json（12778B SHA256ac402f48c7045f431d0e68a48c7c3513d283f19704f3cf6bd90c3d3a773e576e / Git blob5aa29da3b4b62b9f2bf8f2d7ed36c750c3bb8b74）。后者远端精确blob重新读取；后代原bundle/脚本未重新下载或执行，不把旧六事件/两item表当新恢复。零新原件/图像/攻略/程序请求。

六sources关系：大陆站台湾已开/大陆未开攻略与RECOVERED25 profile不当同发行/构建；日美子原56.124 vs后代borncorner57/124、弥生55.93 vs彌生55/92只定位字符串/配置不同，后代亦未证实际spawn，不推一格offset/交互半径/同人物；新攻略无名花→弥生→贝与后代彌生give2414/remove2415方向相似，但贝=不可思議的貝殼2414/花=仙尼亞的花2415和原版ID均不证；鱼村出生可直接取贝与后代give2414/item atoms空记录不合成出生谓词或无条件免费，complete condition仍null，等级/成人礼不被免除；黑乌力第三步超出旧两NPC样本不证整个后代bundle无此角色，也未明写贝消耗/检查；新攻略花→贝→入岛是一个用途链，后代/旧汇编另有反向贝→花，不撤销反向或判补丁/矛盾，也不作完整最终奖励表。所有2414/2415、1000/2000只后代侧，未回填网页。

交付STONEAGE-WAEI-HERO-GUIDE-SOURCE-RELATIONS-R1.json/规格，六条来源关系每条两精确派生pin及可实际解析JSON指针，非六新游戏实体；12反例与独立仅两Git/全cmp/derived-only工作流。45相关本地测试通过（原件20、关系12、设施13），九内容记录/六关系均核七必需字段与19集合合同。完整初始CURRENT/历史/来源/路线前缀及22域状态保留；源job/ZIP/raw/Git与自身main仍须按实际验收，不借父或原件绿灯。

**唯一最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-17**：本六关系有限闭合，返回全官方发行/22域真实材料队列，优先具名任务/故事正文缺口，选一可认证入口与有限交付/停止条件并实取；停止花贝身份/坐标/缺失布尔helper扩张，不盲取未读三攻略/Map2五目标。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79 PAUSED_NON_BLOCKING，无整体百分比。


### R16原件自身main实际验收补记

岛屿/攻略96ed8d94574dfcce50a4a339e8b2e89898cb3d27的自身11项main已实际全部success（含本源工作流与R58）；STONEAGE-WAEI-CN20-ISLAND-HERO-CONTENT-ACCEPTANCE-R1.json保留精确10候选/11main run/HEAD、两原源pin和实下载ZIP/raw/Git链。此为上条待验记录的实际后续，不删除历史待验措辞。关系包新HEAD仍须观察自身检查，不能借本原件11绿；唯一最高NEXT仍OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-17。


## 2026-10-19 — 六关系独立保管验收与本轮收束

关系内容343f69c44b44e8cbda058ee47bc74dd0752abaf3 / tree2a3887e08a1ed0823843687ecd2d344d2423a50a的10候选、自身11项main实际全success，无本HEAD失败/重跑。run39242859389/job118027608853实际只两固定Git报告/12测试/JSON指针解析与完整cmp，零新原件请求。artifact12182300803实下载ZIP3076B SHA256efc34e9209fe165a14e729b060192f688286461b25060dc4e60ea09cb19fb471，唯一derived.json13255B SHA2562fcbe614b13597b8fca7010f344f9db3011b84b20c86d67c54cf4e925274cf00等于永久Git blob0d04d0a697689bf0cfbb0f838aa1deb8eeef46f3。STONEAGE-WAEI-HERO-GUIDE-SOURCE-RELATIONS-ACCEPTANCE-R1.json永久保留实际源job/ZIP/raw/Git、两输入pin、精确HEAD的10/11检查；离线重放非再次取得原网页/客户端或原服执行。

本轮实质为五岛世界/地理文字、台湾开放限定的英雄岛三角色路线/鱼村出生分支，以及六组与后代花贝配置的有限来源关系。共两新正文、一个已知设施重取，新图/原程序0；45相关本地测试通过，两个内容HEAD各自11项main实全绿。九来源内容+六sources关系均核七必需字段/19集合；原件摘要、实际ZIP/raw/Git保管两份回执已永久归档。50年不变绝对年份/前置，波拉/拨拉、小黑猪/黑乌力、弥生/彌生、花贝ID和定位偏移不擅自合并；大陆站转载台湾已开说明不改写为大陆已实装。所有22域原状态、初始完整连续性/历史前缀及失败保留，原HTML/图像/程序不入Git。

**唯一最高NEXT保持OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-17**：停止本岛屿/英雄岛原文和花贝关系扩张，回全官方发行/22域源队列，优先具名任务/故事实正文缺口；选一真实资格入口、有限取源/停止条件并实取，不空矩阵、盲取三攻略/五地图目标、数字/坐标/布尔helper循环或R79。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79 PAUSED_NON_BLOCKING，无整体百分比。此回执新HEAD须观察自身Actions，不套用父内容11绿。


## 2026-10-19 — R17水城心之手环：一个玩家攻略的具名故事与任务关系

按main `01f0075e0118c59bd55f62bf41309130303a4d60` / tree `2312b02af20f57e87869eeb64e2ce35d6048cb44`及完整CURRENT远端原始blob复核，R16英雄岛与花贝关系有限闭合后，依最高`OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-17`返回全官方版本/22域资料队列。选择17173任务首页「石器3.0—伊甸新大陆」真实链接「水城爱情故事——心之手环」，实读`https://news.17173.com/z/stoneage/renwu/sa30_08.htm`一篇（页内署名微笑赢家 多多）；索引和正文读取得到的是**门户托管玩家攻略**，不是官方一方原始公告、原服务器脚本或历史原HTML字节验证，原始刊发日未知。

新资料结构化保留：五前置（成人、转生宠任务、100级以上、金飞航空、携不可思议的贝），四类材料等级（麟11/黏土4/线2/花10不是数量），从伊甸园经尼克斯至水城的玩家路线，四具名NPC喀尔斯/莉娜/麦特/卡蜜儿与11个交接步骤，玩家声称心之手环攻-37/防+37/敏+37/魅+8和与力之手环任务二选一。麦特失踪留信不是第五位NPC；100级边界、贝/花/项链实际消耗、真实NPC ID/坐标/脚本/物品ID及服务器互斥均未知，未读另一任务，无TW1.0回填。新原图片/原始客户端/原服运行0；未声称2026页面代表2002历史快照或二次独立来源。

交付`research/recovered/STONEAGE-CN30-WATERCITY-HEART-BRACELET-GUIDE-R1.json`、`docs/specs/STONEAGE-CN30-WATERCITY-HEART-BRACELET-SOURCE-R1.md`、R17材料评审与专门反例测试/Actions。一个索引真实出链+一正文，有限停机。测试/CI是**机读内容与负面边界验证**，不替代原网页原始字节或原游戏服务器。当前分支新CI/自身main应按实际运行再另记，不提前称绿。原CURRENT所有历史前缀与失败不删，22域原状态、Stage A七PARTIAL二OPEN、Stage B/百科 GATED、R79 PAUSED_NON_BLOCKING保持。

**唯一最高NEXT `OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-18`**：返回官方各版本/地区优先一方任务或故事真实原文，选择不同命名内容的一条可认证入口/一实质规格或精确缺源即止；避免在心之手环数值、坐标、疑似同版身份上空转。无总体复原百分比。


### 2026-10-19 — R17有日期校勘补正：2003新浪水城双结局，防混线

前条R17只读17173一篇玩家攻略、明确其时代出处未证。在证据补核中新增一次限定的**2003-06-05 15:23新浪游戏专题《水城的爱情故事》**正文：https://games.sina.com.cn/zhqu/article/2003-06-05/11022.shtml?from=wap，编辑署名新浪游戏，非原服源码/运营方原始脚本。文章实际分A/B：A=喀尔斯挽回卡蜜儿、奖励力之手环；B=喀尔斯与莉娜情感结局、奖励心之手环（两者仅媒体描述，并非一版原服事实）。17173心之手环十一段与新浪B线**近似**，同构建/同任务脚本/来源独立性均未证，不把A/B并成一条线性正史。

八关系分辨：17173由莉娜制花贝项链，新浪A由喀尔斯、B由莉娜（分支而非统一NPC造物功能）；17173喀尔斯55.51/莉娜83.32，新浪54,51/82,33，未证一格偏移规律、真实spawn；17173「100级以上」条件vs新浪「建议115级」不可互换；两处心之手环数值符号类似但新浪属性后带问号，非物品master；新浪称二选一/若不再转生不能重复，原服reset未知。新增相对日期更强的第三方媒体资料，不把媒体转载=运营方直接披露。双方历史原HTML哈希尚无，只有本轮web-rendered段落及URL/行锚。新图/原字节/可执行脚本0。

补充`research/recovered/STONEAGE-CN30-WATERCITY-TWO-SOURCE-STORY-BRANCHES-R1.json`、`docs/specs/STONEAGE-CN30-WATERCITY-TWO-SOURCE-STORY-BRANCHES-R1.md`与八关系反例测试，独立工作流改为同时检查两机读档。历史上一条R17“仅一正文”不删，因为这是**后续有新材料引发的来源补正**；累计两资料正文，1无期17173 + 1明确日期新浪，不给独立执行双证人。验证待自身Actions实际结果，当前未自动宣称主线绿。止点限定两真实正文，不自动扩其它攻略/图片。

**最高NEXT仍`OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-18`**：回全官方版本一方优先的新具名故事、NPC或任务来源。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79 PAUSED_NON_BLOCKING，无百分比。


### 2026-10-19 — R17派生档案精确摘要/原始资料缺失边界收据

本R17研究内容主线`f8eeda0a473bb0c845d22ceb92cd5100e698a0c9`（tree `b2175beaf176a790b2b8a48802fb4aac699b1d2b`）自身11项main SUCCESS、对应候选分支10项SUCCESS；主线源验证run 39254789891/job118067239223离线`Ran 18 tests ... OK`。两永久Git派生JSON分别Git blob`8eddff3a5c493c1c5434417b6d4ef124b22fd2df`（8619 UTF-8字节、SHA256 `becc0ffa445c52183df16e8a5cb1e3ad7432b7b78539915053aabba2759415a6`）和Git blob`2833ca3e9a8c7ad37ac98f22c01c0fd41090e57c`（7205字节、SHA256 `4ef00084fa42e0a968d8ffb7ab9c4c3a8a5b07d5e0ef5d3ff1a646a0364d5cc8`），实际新校验独立cmp/哈希锚点测试；`STONEAGE-CN30-WATERCITY-SOURCE-BOUNDARY-ACCEPTANCE-R1.json`持久留存。**这是源读后的派生字节保管收据，不是历史原网页的取源哈希或原服务器事实验收**。两个外部原网页历史raw SHA、HTTP重放、ZIP/CI源artifact不存在，明确null；该工作流仅本地测试、无ZIP，不能伪造artifact链。后续须取有时代身份的原始网页快照或同构建官方原服证据方可升级原始来源状态。旧记录、过去当时未验注记均保留，由此后续记录补正。此回执新提交自身Actions须重新实际观察，不能借父11绿。最高NEXT仍`OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-18`，Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79暂停，无百分比。


## 2026-10-19 — R18：2003泪之石任务六段故事，后世玄武版本异文分开

本轮从远端main`e648288e0ec8632bfc2564bf03c9f8e3ca03938e`/tree`d4e23d6c2b949fe4f2726cb39b22d0b4c91883c9`重新读完整CURRENT精确blob、README/协议/决策/历史/来源/路线/22域，远端该HEAD 11项main Actions均SUCCESS、无开放PR；最高任务`OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-18`。先查一方华义旧站档案，web.archive当前读取失败；TW8.5雷尔既在repo，不冒充新取；财务PDF不可直接下载，不引推源文。故选可检索全文六步且明确2003-05-21 22:59的新浪游戏《泪之石的任务》`https://games.sina.com.cn/zhqu/sta/sa6/rw/lzs.shtml`为**同期门户托管玩家“网友投稿”**。网页标“华义官方授权新浪石器”仅其专题授权，不升级任务为华义原始官方脚本；原页直开超时、搜索索引六步可见，没有原始HTML/SHA、确证区域/构建或服务器执行，`sta/sa6/rw`只是门户栏目标签。

来源限定新增故事：夕姬请玩家跨海寻找洛林，与杰夫战斗，六段任务含女戒→克林斯首饰→洛林的信→男戒/信→5泪之石，原文报告5颗合计5点基本能力；“鱼鳃草”只旅行提醒不实证强制消耗；夜晚时间不推时钟或具体脚本；16文字路径/5地点候选不认证原地图ID或传送执行；怪鱼“宫本蚊帐”只保留文字，不提升为原宠物ID。后出`https://www.shiqi.club/renwu/page/602.html`现可读、但几乎逐段抄录，不是独立早期实服证人。2025巴哈玩家`夕姬與洛林（玄武任務）`https://forum.gamer.com.tw/C.php?bsn=1571&snA=81769复用了人物/泪之石却增加奇怪瓶子/旧信/生锈钥匙/羽毛、宠物及不同能力生效阶段；仅四组候选异文关系，不从2025回填2003原服，也不强判同任务扩写、改版/支线。新原始程序、图片、原服脚本、证实游戏实体0。

新增`research/recovered/STONEAGE-CN60-TEARSTONE-STORY-SOURCE-R1.json`、`docs/specs/STONEAGE-CN60-TEARSTONE-STORY-SOURCE-R1.md`、R18材料评审、专门负面测试与Actions。一个同期网页索引六步+一非独立重刊+一后世异文索引，明确限度后停，不空转海底坐标helper，不继续R79。测试/CI的离线验证不会证明2003原网页字节或原版游戏执行；自身main/分支门及永久派生保管须后续按实际另记，不借旧绿。保留完整历史前缀、22域原状态、Stage A 7PARTIAL+2OPEN、Stage B/百科GATED，R79暂停，不计算总体百分比。

**唯一最高NEXT `OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-19`**：返全官方版本/22域队列，优先有真实一方原运营商历史任务/故事/具名NPC来源或独立同期证据；一个具名实源与有效边界即止，不把重刊算重复新增。


## 2026-10-19 — R19五周年犬人萊福：同期报道+后期资料关系，不混原服实体

本轮起点为GitHub main `a72034baaa02db88969fc8628a4106c41daf4000` tree `8e51c5559b58c762698238354a22ea5ac9cdf197`、同HEAD主线后续按实际查看，协议/README/完整CURRENT/决策/历史/来源/路线/22域portfolio重读；唯一最高任务`OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-19`。停止R18泪之石故事重复，寻找运营归因具名剧情。选择同期2005-04-20 19:26:02 巴哈GNN记者小贤《石器時代》五周年活动，首次有具名犬人「萊福」、儿童「乎契」及其父亲营救、霍爾特村附近PC盗贼团基地、任务委托书与「相棲共生」宠物护主牺牲描述；同期活动报道仅作为**媒体转述运营商宣传**，并非华义第一方原HTML、原服运行或原客户端。报道中的蟲蟲危機包商品另保留，不并入任务奖励。

同一任务可能延伸至2006编辑的巴哈社区`犬人拿法...任務詳解`；后期指南写乎契、拓那哩、乎卓、多格樂以及塔姆塔姆/PC洞/霍村八步与道具加工，但仅保留作为来源候选。九组关系严禁把「萊福」=「多格樂」、乎契之父=乎卓、2005任務委託書=后来GM委托书，也不把后期坐标/材料/犬人一级或战斗血量、合成配方回填2005原服。新闻/指南两页浏览器实际HTTP403，搜索全文相关段落可见；原HTML SHA/图片/程序均未取，版号和2005日界仅媒体报道、不证真正部署或活动持续至2006。精确开放触发需华义当年活动原网页或同构建任务脚本/执行数据。

新增`STONEAGE-TW2005-LAIFU-EVENT-SOURCE-R1.json`、`docs/specs/STONEAGE-TW2005-LAIFU-EVENT-SOURCE-R1.md`、R19评审、9项独立负面合同测试/工作流。各数据作为SOURCE_REPORTED而非原始运营数值；历史前缀/已发现的不足均不覆盖。该候选提交的分支/main CI均须实际验收，不能借前一次成功。22域原系统家族7PARTIAL/2OPEN，Stage B/百科GATED，R79暂停，无总体百分比。

**唯一最高NEXT `OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-20`**：停止犬人同文重刊，返回全部官方版本源队列，优先有真实原运营商历史内容/当期具名故事正文，一个限定内容资料包或精确缺源后停，不再扩无源NPC身份/公式。


### 2026-10-19 — R19 派生验收补记

R19 内容主线77b8b06a08ee93aea2e14887fc97de453aa6b19d已检验：候选10与主线11 Actions成功，run39261024329/job118088373092有9项测试成功。派生报告Git blob 3706c4a261ff4a62637e72376828167d0feae95d、UTF-8字节10447、SHA256 fb2b8e473049201e7b4a4e2b98266bc080c5e3edc1d778ef58e06a74fbb2a1b9。外部网页403，2005原始HTML与原服脚本未取，CI无原件ZIP。精确派生保管见STONEAGE-TW2005-LAIFU-DERIVED-CUSTODY-R1.json；新收据本身还需独立CI。最高NEXT R20，Stage A7 PARTIAL+2 OPEN，Stage B/百科GATED，R79暂停。


## 2026-10-19 — R20新浪2004六个早期任务梗概与一个详情链接边界

从远端main `93c76b9e0a33aeccb395b83ab027e4d3073e54a6`/tree`520ffa85204757c92b1f928cdd55d8b509b8a017`启动，前次R19犬人内容及收据已保管且自身main 11 Actions成功；本轮最高NEXT R20按全官方版本/22域转向更早的故事/NPC类内容。新实读2004-02-11 14:10新浪游戏《新任务，新挑战》80行页面：https://games.sina.com.cn/z/sta/2004-02-11/104374.shtml ，6个任务简介为三职业公会就职、九胞胎真相、森林熊患、尊尼/迪克友谊、阿喇吉酿酒和契雷多浪漫送礼，4人名/3职业明确来源限定。沿事实出链64只取2004-02-11 14:40《患难见真情》详情rw4.shtml：网页可见图像引用而无可提取逐步正文，图像0张实取、其余五子页未读。不把简介当原服务器NPC/任务ID、奖励或结局，疑似错字保留，新浪作者与华义公司页脚不推第一方原服脚本；旁侧6.0/7.0链接不证同构建。机读报告 `STONEAGE-CN2004-SIX-QUEST-STORY-VIGNETTES-R1.json`、中文规格、R20评审及源负面测试/CI按实际验收，本次源原始HTML字节/ZIP仍未取得，切勿提前说全绿。旧完整历史和22域状态保留。**唯一最高NEXT `OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-21`**，继续不同原版本的有来源任务/世界故事，Stage A7 PARTIAL+2 OPEN，Stage B/百科GATED，R79暂停，无总完成百分比。


### 2026-10-19 — R20新浪2004六任务梗概派生数据永久保管

研究内容main `5ff985459a2022ce1267254d40f1b677324618be` / tree `773af9b10631fd1eaf920fc8adc2599b69542932` 已分别通过候选10项和main自身11项Actions；main专用run39264102119/job118099065594的8项离线测试成功。原派生报告 `STONEAGE-CN2004-SIX-QUEST-STORY-VIGNETTES-R1.json` Git blob `2273b04bc5ee7ea402aeac0169b616ed72ffa4e0`，共6765 UTF-8字节，SHA256 `edf10446a05f8c9d6d4ef597936e1593343486fa5c7ee73bd49bfb0c3f7c4d73`。保管收据 `STONEAGE-CN2004-SIX-QUEST-CUSTODY-R1.json` 将门户源网页与源出链详情原HTML哈希未知、图像0实取、原服务器脚本缺失和无原件ZIP明确保存；此派生报告SHA绝不能替代网页源SHA。新增独立Python哈希和反例3测试，回执新HEAD需再次验证分支/main而非套用父11绿。唯一最高NEXT保持R21，不扩6项未读图文攻略和补造任务奖励。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79暂停、无全局百分比。


## 2026-10-20 — R21 有效内容轮换：日本运营商连续剧情

已取得日服2008「影の支配者」前三章DigiPark发布文（三篇媒体托管运营稿），交付章节资格与来源限定分支/人物关系规格；现行HTTP/核心摘要与历史快照/实服事实分层。见 `docs/STONEAGE-OFFICIAL-VERSION-NAMED-CONTENT-REVIEW-R21.md`。有限止点为三章来源合同；不扩后续章或无源状态位。最高NEXT `OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-22`，回全官方版本/22域选择另一有运营归因具名内容。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79暂停，无总百分比。


## 2026-10-20 — R22具名宠物与世界故事参考

大陆7.0朱雀华义归因稿已形成有限规格：四神兽技能/封印叙事、菲奇亚名称、概念图与单个体状态图，以及与2002年2.5门户故事的有限来源对照。详见R22评审；图像不作生产素材，截图不变成长表，未解世界线不合并。最高NEXT `OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-23`，返全官方/22域，优先另一具名任务/NPC或故事一方来源；停止本包无源helper扩张。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79暂停。


### 2026-10-20 — R23具名圣诞NPC材料结果与全局续接

R23有限取一篇华义归因2003公告、一2004同期HTML、一真实配图；形成6.0/7.0圣诞兑奖员交谈交物/前置/每人物同服组一次的来源规格。未恢复原服脚本、道具/礼包明细、九处地图或等级精确边界；全服降雪不扩大兑换版本。四研究记录及51相关本地测试，独立源CI/派生保管按实际另记。原portfolio22域状态、Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79 PAUSED_NON_BLOCKING保持。

最高NEXT `OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-24`：返回全官方版本/22域挑另一具名任务/NPC/世界故事一方正文；不继续圣诞坐标、礼包猜测和天气helper。此条后续接替旧局部NEXT，不改历史。


### 2026-10-20 — R24五段海贼王任务指南材料与NEXT25

从R23实际自身8候选/9main验收后返回全局，新增一2003完整门户攻略及一同期HTML，形成贝克—杰克森人龙钥匙/老渔民潜水与战斗交接八研究记录。不是原运营作者或原服脚本，sa6不认证精确地区/build，随机收宠筛选及宝箱内容仍未知。62相关本地测试、两HTML离线重放完成，独立Actions及派生保管按实际另记。最高NEXT `OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-25`，回全官方版本/22域优先另一具名一方任务/NPC/故事，停止本图像递归与钥匙helper。Stage A7 PARTIAL+2 OPEN，Stage B/百科GATED，R79暂停；22域原档与全部历史不改。


### 2026-10-20 — R25赤影迷宫世界事件材料

新增日服2007运营归因叙事与真实2008官方专页/2007媒体HTML回放、单张四格视觉参考，形成双魂封印/喷发地震/三岛海底裂缝/调查动机规格。官方异文与媒体核心分存、同运营链不算独立运行证人，魂壶结局/奖励/原服脚本仍缺。49相关本地测试与四实源离线重放完成，独立CI/派生保管按实际另记。最高NEXT `OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-26`回全官方版本/22域优先另一具名一方任务/NPC/故事；停止本壶helper/商业活动。原22域、Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79暂停不变。


### 2026-10-20 — R26亲子/保护/获宠参考

新增日服2008媒体标发布文的一幼犬/亲犬/保护者任务和完成获宠名称关系、单张宠物视觉参考；六研究记录、59相关本地测试及两实输入离线重放。两固定档案查询空返回，原运营HTML/历史图像/原服脚本未取，资格/个体奖励与结局未知。最高NEXT `OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-27`回全官方版本/22域优先另一具名一方任务/NPC/故事，不扩跟随helper/影子身份。原22域、Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79暂停保持。


### 2026-10-20 — R27早期骑师与骑乘规则材料结果

沿真实官方导航取得2001大陆2.0骑乘正文，形成五来源记录，补第一次骑宠服务链与骑乘攻/敏来源、生命力/损血/防御的文献描述；没有精确权重、费用、等级上限或角色表。单图实际2002捕获，非2001同版像素。45相关本地测试与三实源离线重放，独立CI/派生保管按实际另记。最高NEXT `OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-28`回全官方版本/22域，优先另一具名材料，不扩公式helper。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79暂停、22域原档均保持。


## 2026-10-20 R28有限材料完成，NEXT29

R27早期2.0宠物骑师/骑乘战斗来源完成10候选/11main与双ZIP保管；R28转4.0证明书/流浪骑宠师/九庄园，现页及2002固定快照核心一致，13契约+中文规格+9反例+两实源重放。坏字节、空白、种类上限与庄园数区别保留，门户权威/原服不升级。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-29返回全版本22域另一具名材料；停止同页公式/helper扩展。历史前缀全保留，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停。


## 2026-10-20 R29加工/料理有限材料完成，NEXT30

沿官方真实导航取得三2001正文及两2002链接GIF，形成宠物加工服务链、两技能价格、五料理类别及寄放/礼仪/推荐/传闻分层的14来源记录。69相关测试、六实输入与9实际改写反例通过，独立CI/保管按实际后验；不扩全配方/魔法公式/料理helper。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-30回全版本22域另一具名材料，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、原portfolio和历史全文保留。


## 2026-10-20 R30角色创建/升级有限材料完成，NEXT31

大陆官方站2001年12月创建正文与一分时户外图，新增12来源条目：创建选择、全角姓名、四能力映射/局部增量、每级3点、元素方向/选择、出生地到初宠关系及旧日文/新手指南范围对照。56相关测试、三实源与8实际改写反例通过，CI/保管按后续真实验收。不补创建20/10、不补未列0值、不当完整引擎公式或同版创建UI。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-31回全版本22域另一具名材料，停止同页helper。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，原portfolio与全部历史保持。


## 2026-10-20 R31进化试炼材料完成，NEXT32

轮换到日服DigiPark2008进化首批发布文及真实出链2009官方快照，形成四原标签/遮盖结果名、具名NPC洞窟试炼、随机/重复/失败Lv1与初期状态名字、一宠处理、可选成功保障/一次重抽/促销包的15来源记录。63相关测试、五实输入和8实际改写反例/1外层正例通过，独立CI/保管按真实后验；一官方图404范围保留，不补名称/概率/原服或世界线。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-32回全版本22域另一具名材料，不扩本进化helper。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，原22域与历史完整保留。


## 2026-10-20 R32日服协力活动、交纳总量与奖励开放期

本轮新读远端main553a7b6501218bb510ceea0e0f060e6afe3fc3fa/tree d42f2db50d5c10b491aa021472a01185c3b27589，406分支/0PR，自身9main/8候选success；八连续性/路线/22域全文固定字节/SHA/blob，旧queued37642417333保留。最高NEXT32回全官方22域，选择日服2008初夏协力内容。一篇4Gamer2008/06/20 22:28媒体明确引文发布资料的协力段，当前280409B/SHA256 70e63e25844c698ef069a0a10b39462d26992ad054ce46755de7a9bf8dcbd056，核心SHA256 3a3d781a9f3151dea50e4c0690b04fa35be11b35b754ffed818dd2122a1d772f；一次真实官方出链availability返回429，不宣称档案全面缺失。

17研究合同/中文规格补出敌恐龙掉精霊の雫—恵みの精霊交换精霊の恵み—给予神秘の大樹，以及族长/泉水、大工/便利店、転送員/聊天房三地方援助。四具名角色为来源叙事关系，不认证实际交物NPC/坐标/外观；マンモスルーム与マンモスホール两标签不强合。五JPEG含一树场景及四奖励表全取/目视；五树门槛2000/5000/8000/30000/35000与三地方3000/3000/10000分别记交纳物，不当个人费用或求和；跨服/单服计数范围未知。收集6/24 16:00–7/15 13:00与奖励7/22起常设或7/22–8/12分开；存档点/寄存NPC/技能追加销售/经验活动/宠物重抽及圣水/商店/转送奖励均未证实际开放。

12本包及相关63测试、六实输入重放与8实际正文改写拒绝通过；人工表格转录不称机器OCR，放大复核キヌイ和再抽選。当前HTML/JPEG非2008捕获；008树图不证地图/SPR，另三场景未取。原HTML/图不进Git，无原服执行/原ID/交换比例/概率/商店表/奖励效果，三倍大工叙事不补玩家倍率，存档点不重开R79。独立CI/ZIP保管按后续实际验收。

最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-33回全官方版本22域另一具名材料；止点为本活动来源规格，不扩活动结果、虎追七章或全图递归。同版原脚本/运营结果/计数表/具名菜单或运行才重开未知。Stage A7 PARTIAL+2 OPEN，B/wiki GATED，R79 PAUSED_NON_BLOCKING，原22域及全部旧历史前缀保持。


## 2026-10-20 R32实际双CI、脚本字节差异定位与永久保管

内容82551e491625911130289936da5dac966a039738/tree926c929e2fc1c700a5eba9a08a08129bedd6f9f8自身候选10/main11全success；source run39408860268/39408954668，job118581376480/118581687625各12测试与一HTML五JPEG实重放。artifact12257659302/12258114013已实下载，ZIP均2107B，SHA256 04631b56259dc04f09dfb40fceeaaab7ec24edf65682eb595346ae057adb344e/97a6d9997ce3d45ba420040f4aa6ce16fbfa40ab6724f789acae7b1c0e1a4308；唯一replay.json均6524B/SHA256 61c34db5a406c8a66913787d4f0c8b070e4a234d4e7905a507bcfd09eee14187，两CI逐字节一致但不等于首次本地JSON。差别仅M1输入字节元数据：CI280349B/SHA256 cb18dd7867ea296cf5e0c94164d14493455cbc35952261b72e06afb921580461；核心/其余全字段和五图一致。补取实际当前页恰与两CI全SHA相同，对比原HTML47个script元素，仅零基26变，去script后完整HTML逐字节一致，因此本轮可定位全部变化在脚本内，不泛称任何未来改动安全。两CI原始JSON分别永久保留。

永久CI-CANDIDATE/CI-MAIN-REPLAY/CUSTODY固定源报告/8真实改写反例及外层meta正例/派生JSON字节、SHA、Git blob，精确HEAD/run/job/artifact/ZIP/raw链及八启动全文前缀。独立远端干净检出63相关测试、另一HTML解析器、五全JPEG解码和八完整前缀通过；追加保管用例后64相关测试另实验。人工奖励表不称独立OCR，条件承诺不称实际奖励，原HTML/JPEG不进Git。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-33返回全官方22域另一材料，停止本活动helper；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停保持。保管提交自身Actions另按实际验收，不套父绿灯。


## 2026-10-20 R33台湾7.5精灵召唤预告、玩家分工与具名图内物品

本轮新读远端mainaf5d63d70cbf62277546818a244ecdbeefb2f87f/tree54bcf0b4fcc846880edbb3cb06772d26560a1c0c，409分支/0PR，八连续性/路线/22域全文固定字节/SHA/blob，旧queued37642417333保留。该文档HEAD自身未触发Actions，不套父45b5aaf的10候选/11main/13源测试。最高NEXT33回22域；两GNN台湾2004线索各403后，重取已认证华义制作人目录P0实际20050612011406/28883B/SHA19661e2acca046bf8c6dc86dc968107fe9935cd58a8f3cd8ce5e1de5aeba7f8b，沿同一表行日期2004-5-28/标题7.5版報導之一：精靈的召喚的真实web键84出链，正文实际跳20051129125915/20368B/SHAb073ac516fd358805e961efb9b5f2746552f1d1e8f11c4a8ffa43ce3b67381ef。两页严格Big5；web键不是任务ID，开发近尾声预告不认证部署。新浪大陆2004浏览线索未并入本来源合同。

十研究合同/中文规格补出未明条件召唤玩家—使者寻找勇者—交付精靈信物—勇者得知使命—完成后两角色获奖，及新老玩家重建信任/共抗魔族的明示目的。两角色不是具名NPC，未补等级/配点/六转/组队资格、奖励数量或相同奖项；精灵不等于精灵王，魔族不强合别区世界线。三真实原JPG实际捕获20041211081705/20041211082942/20041211084443，48080/58587/89797B，均640×480，全取目视并放大I3。目录标注日、2005文和2004图分开，不认证2004-5-28首日像素或同构建。

I1提供确定/取消召唤通知，未取声效或原协议绑定；I2任务目标古瓜、剩余6小时33分，不认证NPC主表/坐标/初始或统一时限；I3局部剩余0小时59分/完成领奖提示，交出精靈勇者信物并收下柳牙之槍；所选同名面板耐久100%、攻+85敏-18、毒霧的精靈Lv6，余额8198620不当奖励。泛称信物与图内标签未证规范别名，图内武器不当全任务固定奖，Lv6不当任务等级，三图不同外观不当同人连续任务或两时钟相减。原ID/消耗/公式/原服执行均未知。

12本包及51相关测试、五实输入离线重放与8真实正文语义改写拒绝通过；独立远端/CI/双ZIP保管按后续实际验收。原HTML/JPEG/放大图不进Git，人工转录不称独立OCR。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-34回全官方版本22域另一具名材料；本预告止点已达，不自动扩六转/庄园续篇/全任务池或helper。只有同版资格表/脚本/菜单或轨迹才重开未知。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING，原22域及全部历史前缀保持。


## 2026-10-20 R33实际双CI与原图/派生永久保管

内容2cde1987abce8a77dda80bc9e8cc7c3fbecf73f0/treeec9d487b9b690ffd5fbc919b16eb6131ef9a2641自身候选10/main11全success后非强制快进；source run39411352610/39411464180，job118589614407/118589982458各实际12测试+两HTML三JPEG实重放。artifact12259765024/12258609744已实际下载，ZIP均1993B/SHA256 eadf9527613f97ccf23865236da139a1545d1c1439c32da0e85f5bf6cfd27f25/45eb606c582f16fd12cdb6b87b56911c96f6994be44ec497c1e0ef599441d45d；唯一replay.json均4126B/SHA256 846cb6dbd57a0ad175f39188edf59667bb8c4510f8ae2b118c7d2541dd6134e5，两支原始JSON逐字节一致且等于本地五实输入派生。两份CI原JSON和CUSTODY永久固定源报告/八真实语义反例/派生的字节、SHA、Git blob及精确HEAD/run/job/artifact/ZIP/raw链；五实输入全字节固定，原HTML/图不进Git。

独立远端干净检出51相关测试、另一HTMLParser重提四段hash、三JPEG完整解码、八完整历史前缀与本地完整JSON逐字节一致通过；追加保管用例后52相关测试另实测通过。CI路径补入实际传递依赖shadow_release，源语义未变；保管提交自身Actions随后实际验收，不套父绿灯。角色/资格/泛称与图内信物、倒计时/初始时限、局部面板/全奖励表、余额/奖金额、2004图/2005文及预告/部署保持分开，未认证原服或原ID。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-34回全官方22域另一具名材料，停止本页/续文helper。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部旧历史保持。


## 2026-10-20 R34大陆2.0八战斗指令、逃离队伍与三类失败描述

本轮新读远端mainb83ab9c19380b81e97874b437c290b8068ec7c2a/treec1605fcbb0265e716e3c9934dbefc824ccc69f4f，412分支/0PR，自身8main/7候选success；八连续性/路线/22域全文固定字节/SHA/blob，旧queued37642417333保留。最高NEXT34回全版本22域，轮换到早期战斗交互。已验N1导航临时原字节按当前仓库69317B/SHA561950fd7bba41e7d39f4a781a671e11e175c7fe08dd1b5481fdf1fd23ba351b复用，不算新发现；沿真实“战斗系统”href请求20011204194619，正文实际跳20011201043456/65573B/SHA944d26d035afc11a6f1af4fd135491a7ef516c20970085b68c84e1c4f7069d83，核心SHA83663010b556ecc64829637e738648e49f48a37f51383505c7facab5e2539dc9。严格GB18030，正文无具名署名，官方托管不认证作者、精确构建或部署。

14合同/中文规格补出上排攻击/咒术/捕获/请求帮助与下排防御/道具/宠物/脱离的相对位置、输入等待—决定或超时—处理—未完再等待、装备附魔、捕获可能失败/转生前5之后增加未定、HELP和队员实际退出即离队/领袖退出即解散。轮流输入不当敏捷执行顺序，未补秒数/像素框/协议枚举/成功率/额外容量/队长转让。待机宠接受指令与某些高忠诚宠挡致命击保留原措辞及原坏句“宠物义何中技能”，无状态ID/忠诚阈值或概率。

单人HP0气绝判败后回场景HP1；团体中一人气绝可继续的原文“或”不强改“且”或形式化布尔；伤害远超现有HP另述旋转打飞至纪录点，无倍数/地图/事务。没有死亡不等于没有惩罚，所有气绝不一律回纪录点，HP1不当百分比/最大HP，纪录点不证明本地存盘R79。唯一原图img/5.gif实际跳裸域20011023202109/119327B/SHA7caf79fb6e27b6189669da2396129a4cd76b5e967fb7dc91fa842b6e053b165e，640×480/1帧，已目视/全解码，是户外骑乘而非八命令战斗界面；英文标签不证语言/地区/同构建，外观不绑定原人物/宠/SPR。

14本包及49相关测试、两HTML一GIF实输入重放和10真实正文语义改写拒绝通过。预检曾发现HP1子串误接HP100，已发布前纠为完整整数，失败未抹去。原HTML/GIF/放大图不进Git，独立CI/双ZIP保管按实际后验。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-35回全官方版本22域另一具名材料；本页止点已达，不扩全魔法/战斗helper，原脚本/配置/具名菜单/轨迹才重开未知。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING，全部原历史/22域保持。


## 2026-10-20 R34实际双CI、图文差异与永久派生保管

内容26b1ce900a732260884161704d8edd69ea397324/treed765be25545e030988bf8d835a87f9dc3d771f3f自身候选10/main11全success后非强制快进；source run39413081347/39413323716，job118595391639/118596204622各实际14测试+两HTML一GIF重放。artifact12259289716/12259992868已实下载，ZIP均2076B/SHA256 9d79accb29e4796589ea3590c07092337aa00b249ee17b6c3609c5504ac78cbd/32871b0fa14866ac138b00a20c8a2a48de1498507f94d8c3fca896f1839afd68；唯一replay.json均4360B/SHA256 f5eabc53cfc4faf6b6e04d3b5c4fd9c36c0b6f61bc375319bac3d1fa8ffaaa0d，候选/main/本地完整原派生JSON逐字节一致。双CI原JSON及CUSTODY永久固定源报告/十实际语义改写反例/派生字节、SHA、Git blob，精确HEAD/run/job/artifact/ZIP/raw链和八启动全文前缀；原HTML/GIF不进Git。

独立远端干净检出49相关测试、另一HTMLParser重算正文核心、Pillow完整GIF解码/1帧与八完整历史前缀通过；追加保管用例后50相关测试另实测。户外骑乘原图不当八按钮战斗界面，托管不当作者，待机状态/转生主体/团体“或”措辞不补原状态ID或可执行判定；HP1整数不误接HP100，三类失败/返回地点分开，原脚本/概率/公式/惩罚仍未知。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-35回全官方22域另一具名材料，停止本战斗helper。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停保持。保管提交自身Actions后续按实际，不套父绿灯。


## 2026-10-20 R35台湾7.5庄园约战计划、九成资格冲突与分配边界

本轮新读远端main9f97ea8dd6bb7285a18ad13c5497d571f24c36be/tree6f444bf285f20f9f437b62e4fc8c3c674c177f6d，415分支/0PR，自身8main/7候选全SUCCESS；八连续性/路线/22域全文固定字节/SHA/blob，旧queued37642417333保留。最高NEXT35回22域，选择家族庄园竞争/经济/排行UI，不扩上轮战斗helper；重新选定官方实际web键89，不自动追R33续篇。重取P0目录实际20050612011406/28883B/SHA19661e2acca046bf8c6dc86dc968107fe9935cd58a8f3cd8ce5e1de5aeba7f8b，同表行标题7.5版報導之二：莊園約戰新規/2004-6-17；P1请求目录时刻实际跳20041206162649/18288B/SHA8109af26dabefab11b4bda949c6580e68ae9d48db158a354ddf380b31e93de41。严格Big5，官方“酷哥打算”计划不认证实际部署；目录日期/网页键/捕获不当补丁上线日或游戏ID。

13合同/中文规格补出气势由人数经运算加前次庄园战后累计声望、百人各5点例式100*100/10+1+5*100=1501，算术单独核对不推广一般人数/取整或五点每天。原“高于守方九成”却允许900挑战1000，严格措辞与相等例保留为UNRESOLVED，不改>=或901。更高气势可顶替既有流浪挑战者；宣战18–22、成功后24h开战、22点确认建议，时区/端点/替换重计未写。两族累计声望战后0不清人物终生值；守庄气势×10000、在线成员按贡献每点5000、余入家族银行，不补贡献定义/重置前后取值/离线或挑战方奖/银行事务。休4天、第5宣战、第6战斗不是每周或精确96h；无人挑战视同守庄奖，不补其重置。取消合成料理声望及排行不当删除两功能。

唯一实际内嵌sa0616.JPG请求正文时刻跳20041207062827/107675B/SHA17189e9f25e8b8e0a8c324df28a0588d4eb53cb3b8d282f188412a6a815244a1，450×338，目视/放大核十大家族氣勢选择框、合成/料理旧排行与自己家族气势排名入口。入口不是榜单数据/宣战或到账，旧入口与取消计划并存不证明已保留或已取消，非原生分辨率/同构建/原NPC/SPR。有限引用已验大陆4.0门户派生D1，完整SHA/Git blob固定前10扩前20/九庄园，地区/来源/版本分开，不给台湾附加前20资格或统一补丁序。

14本包边界测试、12真实正文语义改写拒绝与两HTML一JPEG及一已验派生输入重放通过；首次相关命令误写旧测试模块名，仅本地导入错误，纠正实际文件名后重新验证，不当远端失败或源失败。原HTML/JPEG/放大图不进Git，独立CI/双ZIP保管按后续实际。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-36回全官方22域另一具名材料，本篇/唯一直图/有限对照止点已达，不扩六转/PvP助手/全庄园。原脚本/官方勘误/规则账本或运行才重开未知，特别九成门槛与分配取值时点。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING，原22域与全历史保持。


## 2026-10-20 R35实际双CI、阈值冲突与永久派生保管

内容f2cc9bf71421f5923f15b5691f2824bd33628f56/tree023719bced74982b6d09773ba39ca3c178868ea5自身候选10/main11全SUCCESS后非强制快进；source run39415559453/39415672602，job118603581099/118603954916各实际14测试+两HTML一JPEG及一已验派生重放。artifact12262045696/12261546475已实下载，ZIP均2746B/SHA256 f431321647f4b8ae713130f5999eeaf2368fd7a00acc9146c64b3163f4768de5/32a963dc57c25dac27e99904e2fa58d091276f095a6e252c11ae0785617c212c；唯一replay.json均6049B/SHA256 f944228117f0b487c68e56ca249ef5cd06ae3d12b44360fddbde617192b0fefd，候选/main/本地完整原JSON逐字节一致。双CI原JSON与CUSTODY永久固定本源/十二实际语义反例/大陆既验输入/双派生共五文件字节、SHA、Git blob，精确HEAD/run/job/artifact/ZIP/raw链及八启动完整前缀。原HTML/JPEG不进Git。

独立远端干净检出45相关测试、另一HTMLParser重提八段hash、Pillow全JPEG解码450×338、原生Git blob核D1、1501算例与900/1000恰九成算术及八完整历史前缀通过；追加保管用例后46相关测试另实测。计划/部署、严格九成/相等例、人数算例/一般公式、累计/终生声望、在线贡献/全员发钱、战后重置/奖励取值及菜单旧入口/排行实际保留分别保持。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-36回全官方22域另一具名材料，停止本庄园篇/助手递归。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部历史保持。保管提交自身Actions随后实际验收，不套父绿灯。


## 2026-10-20 R36台湾2004法师属性修正、相反转伤方向与两瓶新酒计划

本轮新读main66fd324838517fcd496ae5bf3a7aff1f66d5ae4b/treecabf95e4664aad56116c874ce7357f153dd160e6，418分支/0PR/4825项完整tree无AGENTS、自身main8/候选7全SUCCESS；八连续性/路线/22域全文固定SHA/blob，旧queued37642417333保留。最高NEXT36全域重排，选择职业魔法/骑乘伤害/属性调整任务，停止庄园helper。P0同叶行网页键69/解開法師變強之謎？！/2004-4-5；正文请求目录时刻跳20041206160744/18301B/SHA256 6b3b57b574fa1c200c44aa2ea93dfffb9ce229b4e7268679a7ff0319f091300f，严格Big5。正文未编号，不强贴7.5；模板精灵召唤题名不当文章标题，日期不当修正部署。

8派生记录/中文规格：运营方报告法师攻骑乘目标时，人物地水火风与法术火冰雷错配，引发地人较伤/骑金飞较少伤及不定随机现象；不是原代码/概率。拟分物理元素与闇灵能量，两火同字异义；法术相对物理无属性，原则上人宠平分，另以战场属性优势分配。地人骑金飞例施地的精灵把人物伤害移宠，施风的精灵反向；同属性可保持平分，不补无条件半伤/比例/取整/消耗/持续。拟在訐譙龍任务加入两瓶调人物属性点新酒，未名/方向数值/价格步骤/上线均未知；金飞不绑定物种原ID。

缩略图实际跳20150408182032/36917B/SHA74028b94ae5c9ced3cb537f1d44791bfd55d359dcc6dc90d40e6c21c3ade5cdb/300×225；唯一链接大图跳20040408015726/60745B/SHA7afb898b2c5f202b6c810f474c64376f3decbcf3814929f19716647aac1ba463/640×480。目视洞穴蓝水、橘红长颈骑宠/骑手及旁立人物，酷哥聊天标签；不认证同次图/原生分辨率、任务NPC、金飞外观、酒菜单或修正运行。2015缩图非2004字节。两HTML两JPEG实重放、11真实Big5正文改写在绕过全页字节门后语义拒绝；原件不进Git，CI/ZIP保管另按实际。

来源规格止点已达，不扩訐譙龍全任务/全魔法/酒表；原脚本/同版补丁/具名酒表或运行才重开。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-37回全官方版本22域另一具名材料。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING；全历史与22域前缀保持。


## 2026-10-20 R36实际双CI、两火语义与永久派生保管

内容c5bc2aca0eded77a3116d662a057771da1a91469/treeca30661bc367d45c9996bf2d4cc22c0ed6f651c7自身候选10/main11全SUCCESS，source run39417727148/39417830313、job118610729470/118611070986各实际10测试与两HTML两JPEG重放。artifact12262014170/12262345481已实下载，各ZIP2500B/SHA256 dfcff9d55fffe915e4353c6ec4488dfa1b600744228c5ddaf17e9512e09548f4/73be8a972b268f7f39f3b4a9c96c48927d3f18c5f9b0b0e6451aa945b090781d；唯一replay.json5713B/SHA256 1ed24ae3aa2b476f784d8577c1265900dab355ee4b01821de2bfdd19d9712bcf，候选/main/本地完整原始JSON逐字节一致。CI-CANDIDATE/CI-MAIN-REPLAY/CUSTODY永久固定源报告/11真实正文改写/双派生四文件的字节、SHA与原生Git blob及精确HEAD/tree/run/job/artifact/ZIP/raw链，八启动全文前缀固定；原HTML/JPEG不入Git。

独立远端干净检出46相关测试、另一HTMLParser七段正文hash与两实际图片链接、Pillow完整JPEG双解码和八完整原生Git前缀通过。新增保管用例后47相关测试另验。物理火/闇灵火不混同，原则均分不变无条件引擎，地/风相反转伤方向保留；两瓶酒仍计划且未名，图中酷哥聊天不是任务对话，2015缩图不倒填2004。无版本号/部署/原公式/酒表/实服执行，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停。NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-37回全官方22域另一具名材料，停止本魔法/新酒helper。保管提交自身Actions另按实际验收，不套父绿灯。


## 2026-10-20 R37日服2008虎追任务、传承失而复现与官方谜面

新读main eb9287c662656b4dd127d960e3e25b0e934c9a25/tree9d7d6a46a7634f3f7d8d32ae5cea46be8736283f，421分支/0PR/4835项完整tree无AGENTS，自身main8/候选7全SUCCESS，八连续性/路线/22域全文固定SHA/blob，旧queued37642417333保留。最高NEXT37全域重排，选择日服具名任务/地图/故事，不扩台湾魔法helper。重取R32已知媒体URL，只处理新虎追段；新得官方20080929194642捕获5760B/SHAd7f6df9e6370f8e77d09cdd335c23a735448b935588fda66e40a8e4caa65d829，UTF-8 BOM/声明核实，9月非6月上线当日字节。媒体2008/06/20 22:28发布文引文报6/24实施，编辑归运营者DigiPark，不证部署。

10合同/中文规格新增虎追い山/三匹の虎～虎追いの詩～、七章捕虎传承诗与攻略线索；七章是诗结构，不是七任务且全文未取，三匹不当三种/完整宠物主表。诗在ギール岛重唱，不给山定位。ニース异变与生活变化—虎消失—诗被遗忘—某种到来—重唱的文献叙事，不具名来者/异变年代或倒填1999。官方纯水/追虎武具及防具/相逢才知其意仅谜面，非确证物品/奖励/捕获步骤。官方图示可能不同、未来平衡可能变化两限制语保留。核心官方1220B/SHA8787c1edf9cdbdd8d331382e5efe20b5f2d4db006eb10b5879a62f8f7a3238cf，媒体1180B/SHAe55c11ff1dddbbd7674b2f3b8c55f231b9096e5b6a710d7d62b7110fbeee0f01。

官方真实6GIF href按裸域/www原样一次有限请求均404，未盲递归，不泛化档案全面缺失。媒体真实SS/001–004四250×200 JPEG全取/目视红黑条纹虎和队伍/灰岩走廊/另一人影室内/沙地棕榈肋骨，不绑NPC/物种/原图ID、原生分辨率或捕获奖励运行。当前媒体像素不是2008捕获，不替代缺失官方GIF。原HTML/JPEG不入Git。初次编码猜测Shift-JIS严格拒绝后纠正UTF-8；初次反例命中媒体导语而非发布文，审计未生成致本地测试缺文件，限定发布文容器重做13实际改写拒绝与两外层meta正例后50相关测试通过；不是远端失败或源缺失。

独立CI/ZIP保管按后续实际。止点一官方页/一媒体任务段/四图/六精确失败，不扩七章/全地图/捕获攻略。原脚本、官方具名诗章/奖励/任务轨迹或原ID绑定才重开未知。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-38回全官方22域另一具名材料。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING；R32原范围及全部旧历史/22域前缀保持。


## 2026-10-20 R37实际双CI、官方失图声明元数据与永久保管

内容1463429fa2c14eeb0fd6a0d35985b5a280f14128/tree250e2f1dbefb56aa9637e3e0ac6fda822a0ea6dd自身候选10/main11全SUCCESS；source run39421273992/39421452476，job118622527112/118623140519各实际11测试与一现行媒体HTML、一2008官方HTML、四JPEG重放。artifact12264270040/12263706176实下载，各ZIP2047B/SHA256 162c4982fbe40d696e2d12b842e92891a8249cfe2379f23c532ca56a5923b87f/cb1edf00f5c3e34c4522d6e7cc88aeeb06dd3dcca0a6b8405e165944ad902682；唯一replay.json4599B/SHA256 dbfc56df3e1cbdf5d86d2c0c8a7d7d235a155be325b81434eaad43e5871b466c，候选/main/本地完整原JSON逐字节一致。永久CI-CANDIDATE/CI-MAIN-REPLAY/CUSTODY固定源报告/13实际变异及2正例/新声明元数据/双派生共五文件字节、SHA、原生Git blob和精确HEAD/tree/run/job/artifact/ZIP/raw链。

独立干净远端检出50相关测试、另一HTMLParser两个核心、Pillow四全JPEG、13真实改写与两meta正例重做及八完整历史前缀通过。另从同一已验官方HTML补存六失图href/alt/声明尺寸：banner未声明，uta_osa/tora_in声明250×200，tora_map1/2/3声明150×120；非已取像素实测、NPC/地图名或原ID。此补充在内容双CI之后加入，后续源重放逐字段核实六声明，不改变已验派生JSON格式/语义。加声明边界及保管两用例后52相关测试通过，保管提交自身CI另按实际。原HTML/图不入Git，七章全文、三物种、具体奖励、地图坐标和部署均不补。

最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-38回全官方22域另一具名材料，停止本虎追/全图/全诗helper。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING；全历史保持。


## 2026-10-20 R38 全22域轮换：JP2008具名宠物和直接捕获事件资格

新增内容为2008日本运营发布文里可检索的具名宠物“フクゥーリ”、第200种宣传口径、直接捕获与交易取得分界、限GASH账户参与的一次性外部抽奖事件。没有新增初代宠物master、原游戏捕获算法、完整200种名单或部署见证；不借外部GASH点填原Stone经济。实际带来的是宠物名称—取得途径—时期—外部活动关系一条版本化资料接缝，不是初代物种或任何玩法实现关闭。已有R21《影の支配者》前三章验证成果不重复计数；此前R37虎追后已停止扩展。

优先队列下一项 **OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-39**，回全官方版本22域寻找另一独立具名官方内容的实源并按止点停止，允许资料不足时只保留精确OPEN，不无限抽图或追宠物总表。Stage A有界历史评审7 PARTIAL+2 OPEN不变；Stage B/公开wiki GATED，R79暂停。成果、失败记录、原始当前HTML派生保管见R38专项与CURRENT-STATE末尾；候选CI成功不是主线自身CI。


## 2026-10-20 R39 有界来源成果及 NEXT40

按R38主线完结后另选DigiPark日本2009公会、白炎宠物/积分交换及临时XP发布文。新增业务源规格和永久双样本保管，不扩无原服的公会权限、物品概率或原始地图脚本。跨地区家族不同实现、Gstone与外部GASH/Stone不同币种、白炎袋7种宣称/6具名矛盾，以及网页外围hash改变而运营正文hash保持均予以明示。Stage A七PARTIAL二OPEN，B/wiki GATED，R79暂停。下一包R40再挑全22域另一具名官方材料并尊重原初代资料边界。


## 2026-10-20 R40 限定完成日服2006地图/生态节点证据

本轮改选更直接影响世界观与地图设计的三篇同期GaiaX日本2006来源，提取群岛→西北火山岛→中央多路线条件地牢→上层Boss计划及后续高风峡谷岛/另一岛水源雨林，形成6节点、5关系和4分期的来源限定规格。首阶段“当时发行资料称完成”、后续阶段“拟上线”和原服执行严格分离；不得将日本2006地图倒填台湾1.0/1999，具体坐标/路线/Boss保持OPEN。独立CI与永久派生原Git保管可复核，研究不继续缺失的泛用地图脚本。NEXT R41从22域选择另一有源具名内容，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停。


## 2026-10-21 R41 日本2007新手武器与商城领取的来源分层

本轮重新读取远端429分支/0开放PR、main acaec0ae8698aca8906e782182d53ccf396a5c7f/tree19a48fe90000350eb0c23920f1c2e36b8987c61a及4874项不截断树，无AGENTS；最近R40自身来源Actions39433346041/39433176492 SUCCESS。八启动全文固定，CURRENT-STATE2211377B/blob ac86116799e367881a5d50eb450693f83d35e920。最高NEXT41从全22域轮换到第17域装备/商店，不扩R40地理helper。

2007-02-02 17:39同期4Gamer一页当前19773B严格CP932，GaiaX发布文的两blockquote与媒体oNo导语分层。六记录规格补始まりのこん棒武器（攻击9/敏捷1/未名属性1加成）、Lv1猛毒の精霊零气力中毒及反复使用说明、2月2日17时恒久设置声明、マンモストア/Gストーン和Hangame便利商店入口、两随机恐龙袋。免费/商城—码输入—NPC领取顺序在媒体导语，仅记同期媒体报告，不冒充运营引文；码输入位置、隐藏属性名、毒率/伤害/持续、领取次数和原NPC坐标/ID未知。零气力不等于无其他限制、恒久不证明2026供应、此一武器免费不泛推商城、平台货币不自动合并。

交付 docs/specs/STONEAGE-JP2007-STARTER-CLUB-SOURCE-R1.md、六记录机器合同/真实源派生、解析器和13真实改写反例及外围script正例、专属CI；两个来源层规范SHA分别a13bab545ee37aa82e8a0a645955cc0efae7b10c3e0329d3eb1959516e90daa8 / 44bc2cb09a240c0234197f994539e09a287a17de02e339ff559107cd7f1a5cf2。原网页/图片不进Git，不认证历史2007原字节、实际部署或JSS1999/TW1.0/CN1.82归属。候选及主线CI、永久ZIP保管以后续实证为准。

最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-42，回22域另一有源具名内容；停止本武器/商城/概率helper。Stage A7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，全部旧历史前缀保留。


## 2026-10-21 R42日本2005三特殊地图、犬类收集任务与跨年地名边界

新读远端430分支/0开放PR/main e27c345eaba04a54cbdffc0943065bd7c16bda61/tree99db6e7e328cddb1977f58ae4f2fc33132940627、4884项完整树无AGENTS；主线自身9项Actions全SUCCESS，旧queued37642417333原样保留。八启动全文及22域组合索引新读，CURRENT-STATE2215752B/blob a0126e5bd3f4bf69e23568fae702f3016aca70eb。最高NEXT42回全域，不延长R41武器/商城helper。

先查早期组队/交互，实际大陆2.0已知导航两次/JSS2001已知手册一次精确HTTP均503；记录本轮不可取，不宣称源不存在、不撤销旧保管，也未从无正文猜交易/组队规则。改选同期GaiaX2005地图公告引文（4Gamer 2005-11-29 19:36）：巨獣の島初级/渔民近期发现/低敏蜥脚类/相对适合组队狩猎；閉ざされた氷窟中级冰洞/当地亲犬/多只亲犬换幼犬任务；バルツ山の洞窟高级/古代山地遗址与恐龙幸存者/当时最强层级与具名未知Boss/可能稀有掉落。三地图+未名任务+媒体入场说明+媒体意见六记录及中文规格新增，不补亲犬数量/宠物名、BossID/掉率、绝对古史年或地图坐标。

媒体导语报告12月2日起基础游玩免费、商城票准入，评论担忧组队障碍；两者不冒充运营引文或实测影响，不补票价/时长/全队资格。既验R39派生原生Git固定对照：2009再次具名冰窟只记同名，不证同ID/收费沿用；バルツ山不自动等于本篇洞窟。现行网页269601B/SHA256 fa11e2045e8e1e2ad573ab387ac5e19990f1e4ab84cd16d83a9f9d6b912f62d9，规范运营引文SHA256 5ab95832b1b1b563e0a9a36ead6bbc543fa672dfd4893eeea72103d97c93ddb1，不当2005原始HTML认证。

交付 docs/specs/STONEAGE-JP2005-SPECIAL-MAPS-SOURCE-R1.md、六记录机器合同/解析器/专属CI/派生元数据。13真实正文语义改写绕过digest门后拒绝，另外围script正例及独立正则/HTML实体解码摘要通过；初始反例锚命中meta重复而拒绝，发布前限定body重做成功，不当远端CI失败。原HTML/图片不入Git。独立候选/main取源及ZIP永久保管按实际后验。

最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-43回22域另一具名材料，不扩犬类全集/票据/全地图helper。Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING，全部旧历史前缀保留，未有分母不报总体完成百分比。


## 2026-10-21 R43大陆2003“2.0”服务器分支与家族玩法归属

新读远端431分支/0开放PR/main ad9d1fd0b8ce6b7e43772ab064b294992f096b79/tree46155e691b107d4d1fae53631b153d0d52d530dc、4894项完整树无AGENTS，自身主线9项Actions全SUCCESS，旧queued37642417333保留。八启动全文和22域组合索引新读，CURRENT-STATE2219862B/blob f79f0006590b20ba00c836c021b1ff0cd37b3972。最高NEXT43轮换大陆版本/家族/骑宠/交通归属，停止R42地图/亲犬helper。

台湾复刻版候选页一次本地HTTP403，未用搜索摘要认证正文规则；改取新浪2003-11-18 15:33明确华义官方消息 https://games.sina.com.cn/newgames/2003/11/11188486.shtml 。当前35255B/SHA256 97f455897c76d219a71831406d8308303d458c901b14220e8cd90bb128c74e60，严格GB18030；当前页夹后期广告，绝非已认证2003原始HTML。只原内容标记内运营正文，规范SHA256 d42ada75bf6f21554f64c5373d1f423966d33d78820cceb7e6acf0eb4ca2fc9f，独立移除广告+正则/HTML实体重提与HTMLParser一致。

六记录：2003“石器时代2.0”运营分支不是2001客户端二进制；正文回顾9月4日原组开放（原句无年份）；预告11月19日09:00开始维护后增开2.0(2)，旧组改2.0(1)，09:00不当精确开服。新组(2)开放后收费/WGS出链，不推旧组收费/价格或单位，未取收费说明；骑宠、较安全交易、较快速度、加美航空/村庄羽毛及更多宠物道具均运营宣传，不当首发日期、安全/性能实测或完整表。四大庄园只具名萨姆吉尔/加加，另两名未知；家族频道/管理/战争缺权限/ID/公式。

有限对照既验大陆4.0九行庄园派生表，完整SHA和Git blob固定：来源语境不同，不由九/四推出删五处，不移植骑宠证明书或早期训练/战斗公式，也不合并台湾复刻版。新增 docs/specs/STONEAGE-CN2003-CLASSIC20-BRANCH-SOURCE-R1.md、六条机器记录、工具/专属CI/13实际正文语义改写与外围script正例，原网页/图片/程序不入Git。独立候选/main与ZIP永久保管按后续实际验收。

NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-44回22域另一具名材料，本篇/费用/全庄园/安全助手止点已到。Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING，全部旧历史前缀保留，无分母不报整体百分比。


## 2026-10-21 R44日本2007レン/ワイト故事承接、新居交换与人物魅力

新读远端432分支/0开放PR/main bdaa1a2843d9bc494f9903f2b5d2462068c4c657/tree084140c70bf571184c9a2ac13be5df4314d2c1d4、4904项完整树无AGENTS；主线自身9项Actions全SUCCESS，旧queued37642417333保留。启动README/协议/CURRENT-STATE/决策/历史/来源/路线全文及22域组合索引固定，新读最后状态NEXT44，停止R43费用/庄园helper。

本轮轮换人物任务、世界场景变化、物品和宠物关系。实际取得GaiaX2007一月发布文节录/六月明确原样发布文，两4Gamer页面当前CP932 19602/20085B，规范SHA分别f0801a2577962ff34ee495035cda98febd298799655a2072896b697ae9cae6c1 / df5ce9aad50b0cc97cecd4a3941ec06cb5693cc79479ee822138b6ac203f8182，不认证2007原始字节。八记录及中文规格 docs/specs/STONEAGE-JP2007-REN-HOME-SOURCE-R1.md、机器合同/重放/工具/专属CI新增；原HTML/图片不进Git。

一月レン在カルターナ村长宅收指定材料制巧克力，商店购买仅举例，效果约600体力回复我方全队。心仪对象一月未名，不从六月倒填。六月明确回顾情人节/白色情人节互明心意、ワイト/村长孙女レン与其父最后考验；击败特定恐龙取建材交村边ワイト、按建材等级获奖品+点数，指定量推动新居扩大。没有物种/材料/奖表/阈值/计数范围/最终婚礼或房屋永久性；白色情人节原篇未独立取，续接不当玩家结婚系统。6月27日(火)与按刊年2007日历(水)矛盾双存、实际意图null，不改26或星期。

迪诺香水ディノ・シャルマン三种效果强度在マンモストア销售，用于恢复败北等减少的**人物魅力**；魅力高较易使宠物服从，不是宠物忠诚度、不保证服从，不补价格/回复值/上限/公式。17实际正文改写绕过digest门拒绝、两个外层script正例和独立正则/HTML实体核心SHA核对通过，初始9用例零跳过；独立候选/main取源与ZIP保管按后续实证，不提前套绿灯。

最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-45回全官方22域另一具名材料；本恋情/房屋/魅力helper止点已到。重开需官方具名日程更正/白色情人节原文/材料奖励阈值表或原服过程。Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING，全部历史前缀保留，不报无分母整体百分比。


## 2026-10-21 R44独立候选/主线取源与永久派生保管

内容8f4fad08a4b189ebbdddd47bc5e686f0aee0b50c/tree64d8f7513e55a00491573a43c0408fa4aa7516b5自身候选10项、主线11项适用Actions全SUCCESS。来源候选run39516937794/job118951241072，主线run39516996099/job118951437657各实跑9用例零跳过、HTTP20085/19602B双源与17真实正文语义改写拒绝、两外围script正例。另对实际远端内容main干净检出75相关用例全过，独立正则/HTML实体解码两核心摘要、九启动完整前缀和原生Git标识核实通过。

artifact12307574197/12306859797实际下载，各ZIP3068B，SHA256分别6decb924bacdf91e5a3be960381d151910dc738e64d4ea31a3cd89d2b9225be0 / ec68f5ff337173dc3dcb30aa65a1a9a075c85cda8de9650005e2a86c8543b06a；唯一replay.json7433B/SHA256 f1ecb7f73558449ae9c1939678b0d1a46273f94de06acc27b2ee83f2da014b20、原生Git blob204be2cb0de67b1e5d2ce6f27102bfb4cea0c30f，候选/main/本地完整原JSON逐字节一致。双派生副本、八个来源/工具/工作流/规格pins、21实际workflow条目和九启动完整前缀永久置 research/recovered/STONEAGE-JP2007-REN-HOME-CUSTODY-R1.json。原HTML/版权图不入Git。

新增强制收据门后本包10项/76相关用例全执行通过，删除收据会失败；初始9项历史不改写为10项。保管提交自身候选/main Actions继续独立后验，不套内容提交绿灯。日程原星期矛盾、未名一月对象/六月具名关系、计划新居/实际婚礼、人物魅力/宠物忠诚、建材等级/数量保持分开。有限R44止点完成，NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-45回22域另一具名来源；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部旧历史完整。


## 2026-10-21 R45胜思时期摆摊操作、当前界面图与跨年宣传复用

新读main1f5e940731487851380f8c082255d5dcbf010948/tree67f78fa9436f91c04599534d151e88917aa566d4、433分支/0开放PR/4914项完整树无AGENTS，主线自身9项Actions全SUCCESS，旧queued37642417333保留。九启动完整正文与路线/22域组合索引固定，新读最后NEXT45，停止R44恋情/房屋/魅力helper。本轮改选第17域交易与UI交互，非新游戏生产。

实际取得新浪2011-01-12 10:38及2012-12-04 14:30两篇胜思具名摆摊宣传，严格GB18030当前76967/66924B，规范段落SHA分别30be132158ef2872ebe36eb2ee4a95efae49f37d1ace8b6eada59d2a6bf44e40 / 19f64e22d65c43eec090e5fe86a6b64d085742112c17482a23cad8df5df33489。正文点名胜思及sa.cins.cn出链，但未获认证原站原始文件/署名作者/构建，具体数字版本null，不推8.5或最早版。2011预告1月15日不删档石灰封测，不当实际开放/存档生存。

七记录及中文规格 docs/specs/STONEAGE-CN2011-2012-STALL-SOURCE-R1.md 新增：左上摆摊按钮→店铺设置、物品或宠物→定价→广告→确认，待售红SELL、四聊天议价渠道；原句无须缴纳任务费用/随处摆摊仅宣传，任务原词不修写为任何，不推所有税费零或全地图权限。无货币/价格范围/槽位/锁定/离线/买方扣款结算/退款算法，拍卖标题不补拍卖机制。

四实际源链接JPEG当前94135/10369/60645/114772B，分别550×413/330×60/550×413/550×398，均完整Pillow解码/目视。2011工具栏单图标红框裁图不当原屏坐标；上架窗口可见巴朵兰恩样本1000、议价和SELL，不作标准物价、币种或原物种ID。2012场景与2011首图构图相似，但hash/高度不同，可能复用为HYPOTHESIS，未认证精确变换/截图年代/同构建。两文操作段逐字相同、2012多出weibo字样分开，不把复用当新增功能或两版运行等价。

工具实取两页四图，22实际正文改写绕过digest门拒绝、两外围script正例、原URL与HTTPS请求改写分别保存；首轮10用例零跳过。原HTML/版权图不入Git，只派生记录/指纹/观察；候选/main自身Actions与实际ZIP永久保管按后续实证。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-46回全22域，本摆摊/物价helper止点到；重开需具名版本原UI/真实交易/费用权限/买方结算或离线限制来源。Stage A7 PARTIAL+2 OPEN，B/wiki GATED，R79暂停，全部旧历史前缀保留。


## 2026-10-21 R45独立候选/main双取源、四图指纹与永久派生保管

内容7aa0b4272082972407c84e8347d45d48e8eb03e3/treeb883e06e48392b2389e8aaccced5c2d6ca2ae879自身候选10项/main11项适用Actions全SUCCESS；来源候选run39545800262/job119043570189、主线run39545863012/job119043767652各实际10用例零跳过、HTTP76967/66924B双页+四JPEG、22真实正文改写拒绝和双外围正例。独立远端内容main干净检出86相关测试、九完整历史前缀与原生Git标识通过；另一路正则/HTML实体段落核心SHA一致，本地四JPEG完整Pillow解码/目视。CI图检查准确限定为原字节SHA与SOF尺寸，不冒称历史客户端渲染。

artifact12321353430/12321178973实际下载，各ZIP3693B，SHA256分别f3ec917037e8e22c6b59e47046b027d88140b66d00ed2bd15310aa92cf63fbd2 / 882af32e437077cb0dfbc19210703a1a606fee21b3d7b83f1909cea0252eabdf；各唯一replay.json10853B/SHA256 bda7add6deeb611680a6b00af4950dd4ba4321e248f262ec068d79695a618fdb、原生Git blob9eab3e3c11bb86eaa0c4e55d6b1e7d1805cc70ab，候选/main/本地完整JSON逐字节一致。双raw及八来源/工具/工作流/规格pins、21实际workflow、九启动全前缀永久置 research/recovered/STONEAGE-CN2011-2012-STALL-CUSTODY-R1.json。原HTML/版权图仍不入Git。

新增强制保管门后本包11项/87相关用例实跑通过，删除收据应失败，原内容10项不改写成11项。保管提交自身Actions另独立后验，不套父提交成功。宣传费用/所有税费、SELL待售/成交、样本数字/主表物价、重复操作与相似图片/同构建、网页尺寸/客户端原生尺寸继续分开。R45有限包结束，最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-46回全22域另一具名材料，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，历史前缀完整。


## 2026-10-21 R46独立作品SA2宠物养育、生命状态与有源设计意图

新读maina884ad32e4d6bdcc81ab0fc194905e93cf71d030/treed7ec7b90743989db349e6a98f56766fb3019cd03、434分支/0开放PR/4924项完整树无AGENTS，自身main9项Actions全SUCCESS，旧queued37642417333保留。九启动全文、路线及22域组合索引固定，最高NEXT46回宠物养育/成长领域，停止R45交易helper。

取得4Gamer/TeT的GaiaX遊佐孝之、DigiPark長田妙子/石川彰弘访谈，只取首个29轮宠物问答。当前32699B/严格EUC-JP，规范说话者+回答摘要affbb359cca11ab96b7cf520640531a86670f050e21868d031f76f6df08fea38；最初CP932/UTF8未成功，按页面声明纠正EUC-JP，不当源缺失。另取2006-07-10 16:28 TeT同期定位报道19733B/CP932，实际href指回该访谈且说明2006年2月录制，规范SHA798111f1c6291a4745eac7549a168ad1492230e971180f92007c1e1421a3e943。访谈刊发日仍null，2月14日发布会与页脚2006/07/25发行日分别保存，当前字节非认证2006原快照。

八记录/中文规格 docs/specs/STONEAGE-SA2-PET-CARE-INTERVIEW-SOURCE-R1.md：独立新作非SA补丁、培养影响AI性格/隐藏参数、DEN随房间增大增养量、借出/借入两宠相处产卵/幼宠承双亲资质、宠物为技能学习主体、随行5匹/DEN10—15種類/合计约20匹原单位、寿命与转生复活/照顾不佳离家、久未登录普通E邮件及开发者所说维系离线世界联系的目的。公式/阈值/物种全集、精确DEN槽位、寿命时钟/转生保留态、回归/邮件延迟送达等未知。不得转成SA1/TW1.0/大陆2.0规则，前期访谈不当部署见证，开发者对旧作宠物的比喻也不是旧作客观全集。

本包仅归档，未取版权照片、原客户端/原服务器或实现/发送邮件。16访谈+3定位页实际语义改写绕过digest门拒绝，双外围script正例；独立正则/HTML实体重建29轮摘要一致，首轮11用例零跳过。候选/main自身取源和ZIP永久保管按后续实证。止于一问答块+一期定位页+八记录；重开需具名SA2手册/规则表/原ID/实际过程或有日期原档，不扩养育/寿命/通知helper。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-47回22域另一具名材料，Stage A7 PARTIAL+2 OPEN，B/wiki GATED，R79暂停，全部旧历史前缀保留。


R46验收补记：初次本地派生JSON生成把定位页字段附于末尾，重放CLI把字段置于审计前；解析内容相同但原字节不同。独立原字节核对拒绝后统一采用实际CLI输出顺序，源码/业务事实/19反例不变。首发布候选6029d48be7c7be069b69b4074a9b2392d470d9f2未合main，修正用后续候选重新取源，原提交与实际Actions保持，不把本地序列化差异说成历史源变更或远端CI失败。NEXT47及全部阶段边界保持。


## 2026-10-21 R46实际三产物保管、序列化修正历史与独立main验收

初发6029d48be7c7be069b69b4074a9b2392d470d9f2/tree9134d8ab20ebf9f5c1de07f2166f98c0d9cc5344自身候选10项全SUCCESS；实际来源run39547329830/job119048351386/artifact12322385690。其CI输出本来就是规范顺序，早期本地副本字段排序不同；未合main先由本地原字节核对拒绝，纯序列化修正a2eeaa7d74d044a065880413ea80939c588aef90/tree595d8e29491de06a82b1c785cd0edad816952084候选8项/main11项全SUCCESS。修正候选来源run39547436315/job119048687134/artifact12321882311，主线run39547537087/job119049006704/artifact12322720679，均实跑11用例零跳过、重取32699B访谈+19733B定位页、29轮/19实际语义改写及双外层正例。独立远端内容main干净检出98相关检查、九历史全文前缀与两种独立核心提取通过。

三个ZIP真实下载各2968B，SHA256按初发/修正候选/main分别775706430eb86382b34d3ed02b5f486b879412388813b194a2391d84a15da123 / 8b185be9b17294374a78b63f547299d815cd45e5e83c655131306ecebab0fe5b / 2744ca047d3e8344ea1b3b0fc56c38bca47b10f660a36d0c4440e04692c3e73b；各唯一replay.json7320B/SHA256 876b2966758eb54a8926d5e836cec9b47ee21002b15cc099006ad6f0621cfe66、原生Git blob667b5329a58f8be01d201abdf3dea017352eb865逐字节一致并与修正本地匹配。早期本地副本blob33bfdd55892feeff991585060a43d3ffe94078d1/SHA256 99eaaa6364e80ec847689f9269f57defffeba1e683dc929f70531c88eb5b6785实际由Git重读，确认仅字段顺序不同、解析JSON语义相同；不能说源网页发生变更或初发CI失败。

双raw副本/初发同blob定位、八来源工具工作流规格pins、19修正候选/main workflow与10初发workflow、三完整HEAD/tree/run/job/artifact/ZIP/raw链和九启动全前缀永久存 research/recovered/STONEAGE-SA2-PET-CARE-INTERVIEW-CUSTODY-R1.json。原HTML/照片不进Git。新增强制收据门后本包12项/99相关检查通过，首轮11项不改写为12项；保管提交自身候选/main Actions另独立后验。产品/说话者/前期与部署、录制月/刊发日/页脚发行日、種類/匹/约数、普通E邮件/游戏内邮件保持区分，项目未发信。R46结束，最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-47回22域另一材料，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部旧历史保存。


## 2026-10-21 R47 华义2.0(2)开服后四庄园与家族具名报告

新读main ac389193dbd71e5977975840601404e1fc022134 / tree d0a200343d5701c0e44af580096126b0ae32a060、435分支/0开放PR/4934项完整树无AGENTS、自身main9项全SUCCESS；旧queued37642417333保留。九启动全文与路线/22域索引固定，最高NEXT47进入有限的家族/庄园内容归属审查。

新浪2003-11-20 16:43明确转华义消息的后续报道当前33636B/GB18030，核心SHA d16ab4ca25e051f0c88916df49003cfc46d66c819864be53ae4ec2d457ca8aac；按原顺序：萨姆吉尔/圣战部落光/4524，玛丽娜丝/永远友情/2280，加加/龙族/4079，卡鲁它那/友情岁月/2811。报告11月19日“中午”开机，不推精确12:00/时区/构建。平均同时在线2000人以上、24小时内建族超过200均为运营方报告；“四家族人数超过90”范围不明，不拆每家族90。声望不是门槛，家族不是2026当前占领者。专属骑宠地位表述无名单/规则；挑战/PK为未来时；20日早晨繁忙临调恢复是运营方陈述，非独立执行/uptime/补偿见证。

实际正文一图当前19585B/300×225、SHA ad1f011da8a7c83187e856064e376d011b88114ddf1590136722afa9ecd03c40，原http/requested HTTPS分开，完整Pillow解码/目视；不标庄园家族/宠物ID、拍摄日期、原生分辨率或事件证明。正文外编辑相关链接实际指回R43预告，固定旧契约全文字节/原生Git blob；仅新文补玛丽娜丝/卡鲁它那和占领快照，旧文remaining_manor_names=null保持。09:00维护与“中午”事后报告不合成精确开服，WGS执行/九变四补丁/跨版本规则不证明。

8派生记录、中文规格 docs/specs/STONEAGE-CN2003-GROUP2-MANOR-REPORT-SOURCE-R1.md、真实取源工具/18实际源改写绕过digest门拒绝/外层script正例；独立正则HTML实体重建正文与顺序列表一致。初轮10本包/109相关测试零跳过。原HTML/版权JPEG不入Git；候选/main自身Actions和ZIP永久保管另据实追加。有限包止点一页一图一旧契约，不扩庄园/声望helper；重开需具名规则/原ID/实际过程或有日期原档。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-48回全22域另一具名材料，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部历史前缀保留。


## 2026-10-21 R47双取源原字节保管与主线独立验收

内容119ba1d8ae75384f6af2fb7ff0fb5ce21fc00e44/treed67e445ca011be4e221aeea3053caa78565458e9候选10项/main11项自身适用Actions全SUCCESS。候选run39550739816/job119059107914/artifact12323665629，主线run39550814576/job119059348025/artifact12323641358各实跑10本包用例零跳过，重新取得33636B页面/19585B实际JPEG、18真实源变更拒绝/外围正例。远端内容干净检出109相关检查，独立正则/实体正文核心及有序名单/数字一致，当前图完整Pillow解码/目视；CI只验证图原字节与SOF尺寸。

实际下载双ZIP各3169B，SHA256候选3fc0a10eea71efcb053af2ba8bd25abdc410c3168d463dd6da7d1cec19ae0b03 / main559545f9b4e4ccf80e5fcea4e060548514724cb593c0995eca1f330457d30a62；各唯一replay.json7654B/SHA256d7eeebad05aa8281e6b557a43532f3c667c87e061a4ad137dbc0c14b56dfc249、原生Git blobd742b10ac5fcf1e6ab35e862ca9aef17c739efd6，候选/main/本地逐字节一致。双raw、十来源/工具/工作流/规格/旧契约/依赖pins、九完整启动历史前缀与21实际workflow永久存research/recovered/STONEAGE-CN2003-GROUP2-MANOR-REPORT-CUSTODY-R1.json；原HTML/版权图不入Git。新增强制收据门后本包11项/110相关检查通过，首轮10项不改写为11项；本保管提交自身Actions须后验，不套父提交成功。

R47有限报告包结束，原文“中午”/精确时分、四家族人数歧义/逐家族数、声望快照/规则门槛、未来赛事/已执行、运营方报告/独立统计、R43预告/本次后文与版权图/生产资产分开。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-48回全22域另一具名材料；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，历史完整。


## 2026-10-21 R48胜思高厨料理采购、宠物制作、交付与荣誉用途

新读main551e93eef582066eef6ffc8540adb41bd4ba2e09/tree6bbbd62a56ef8578284d35938359cc60c7b9798f、436分支/0开放PR/4927项完整树无AGENTS；R47保管提交自身候选10/main11项Actions全SUCCESS，完成前轮收尾核验。九启动全文/原生Git与22域索引重新固定。当前最高NEXT48，轮换生活技能/任务/经济，不扩庄园helper。

新浪2012-02-10 15:51胜思具名宣传https://games.sina.com.cn/o/n/2012-02-10/1551581681.shtml 当前146067B/GB18030，正文规范SHA f7a15a015e8791ed94221d43203f414b43714edff394fc1448bbeacc31111f11；两实际sa.cins.cn链接/自称胜思，未认证原始运营文件或2012原快照。五条版本化记录及规格docs/specs/STONEAGE-CN2012-COOKING-EVENT-SOURCE-R1.md：周一至日19—21点高厨料理，准备料理宠/村庄宠物店可学，向扑满乌力/黑乌力购买，制作两具名蔬菜色拉，交加加村24店大厨换奖励，荣誉值可换宠物/道具/装备。原文或者不改同时，配方/价格/坐标ID/奖励值/次数/时区/端点/首次上线未知。

宣传并列8.5魔域大冒险与2.5精灵王传说，活动适用组null，不推两组共有、不当2002原2.5或TW1/JSS1999；荣誉值不当石币或现金。两实际图115307/125689B、550×410/550×409完整Pillow解码/目视为人群宠物背景，不证料理或交付；第三壁纸只存链接、未取未验。原HTML/版权图不入Git。19真实正文语义改写绕过摘要门拒绝、外围script正例通过；独立核心/流程另核，候选/main自身取源与永久ZIP保管另据实追加。

止于一活动五记录双背景图；重开需同组具名配方奖励表/坐标ID/时区次数说明或原服过程。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-49回全22域另一材料，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，完整历史前缀保留，无分母不报恢复百分比。


## 2026-10-21 R48独立双取源、背景图边界与永久派生保管

内容1a6b5f2ed5f06cb68678b701442df1ef9a144f5f/tree5f6254cc7f2dddafd77d83da0dab2b046ca8a570自身候选10项/main11项适用Actions全SUCCESS；候选run39552068852/job119063286716/artifact12324405541、主线run39552188075/job119063656876/artifact12323439299各实跑9本包用例零跳过，HTTP146067B正文/115307与125689B双JPEG、19真实正文语义改写拒绝/外围script正例。干净远端内容检出119相关测试通过；独立正则/HTML实体核心与采购制作交付次序通过，本地双图完整Pillow解码/目视；CI只验原字节与SOF尺寸，不冒称运行截图。

实际下载双ZIP各2902B，SHA256候选03c818f803def6829c1b6161c91c7a40d4cbee2496a2b7ca1b59d412dbad2cf5 / main3d28bf90c46413359a5a56e2dc24476c0a9406c22f5732556edb1cf4c9860fcb；各唯一replay.json7744B/SHA2567f41ff51711db4d11f82faa6b5cc9c701b756a70063895b8ac43800aa04d003c、原生Git blob33abebf55968f3d2909e224476912079efd8358e，候选/main/本地逐字节一致。双raw、十来源工具依赖/工作流/规格pins、九完整启动前缀和21实际workflow永久存research/recovered/STONEAGE-CN2012-COOKING-EVENT-CUSTODY-R1.json；原HTML/版权图不入Git。新增强制收据门后本包10项/120相关检查据实验收，原9项历史不改写为10项；保管提交自身Actions另后验，不套内容提交绿灯。

两服务器宣传/活动实际适用组、或者/两种必交、荣誉值/石币现金、时段/时区次数、背景人群图/料理执行继续分开；R48有限包结束。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-49回全22域另一材料，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部历史保存。


## 2026-10-21 R49大陆6.0登录建角、新手村及透明伴随图边界

新读main51bec22420b3ebdef554a6ebaeee3904350002f9/treeaa3dbc5f746a4141b3187a508b0538db8d8cee5f，437分支/0开放PR/4937项完整树无AGENTS，R48保管提交自身main11项Actions全SUCCESS。九启动全文/原生Git与22域索引重读固定，最高NEXT49轮换登录建角，不扩料理/荣誉助手。

新取得新浪6.0新手流程https://games.sina.com.cn/zhqu/sta/liucheng.shtml 当前64286B/GB18030，显示新浪游戏2003-05-30 14:14、投稿入口及2006-10-09重生成注记。投稿入口不证明网友作者，亦未认证华义原版手册；注记不当原刊或拍摄日。所选进入/建角/新手村与图链接核心SHA7530ed367b3deb63486378be93773078bb4e484e5da84506789c496dd62af92e。另新浪2003-06-09 12:15运营口吻分服升级预告https://games.sina.com.cn/newgames/2003/06/06092201.shtml 当前33218B，去广告核心65c6c350d032f4e6d6be5099db28bfaaef09d4be7fcb781f89ffa7d7831723de；预告6月10日中国网通9先升、其他分期并需更新客户端/有新手村，不当实际执行、不替指南和图认证构建。

七条记录与规格docs/specs/STONEAGE-CN2003-ONBOARDING-SOURCE-R1.md：Deeplay/登录说明、插叙角色页、12人物各4配色、8个字符/面部可设、20点经验值原词、四具名出生宠/未名技能、新手村出至萨姆吉尔后不能再入等均保留来源层。字节/汉字数、独立4×4色、EXP或属性点真实语义、技能ID/首发、地图NPC坐标与执行未知；原文乌力乌力不擅改，速度体力建议不当最优公式。

实际十GIF中032/035/038/041/044为五张当前低分辨率画面；033/036/039/042/045各73B全透明，逐一完整Pillow解码alpha[0,0]，不算另外五张恢复画面。五画面目视，尺寸不当原生分辨率/确切构建；原HTML/版权图不进Git。20真实正文语义改写绕过摘要门拒绝、双外层script与重生成注记正例通过；独立核心/数值/有序图链另核。候选/main独立取源与实际ZIP永久保管另据实追加。

有限止点两源选定内容/十图对象；重开需同构建原手册或运行过程、姓名编码/20点规则/技能ID或传送证据。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-50回全22域另一具名材料，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，所有历史前缀完整，无分母不报整体完成百分比。


## 2026-10-21 R49双来源、十GIF角色及永久派生保管

内容2a0826b6cb5a0b34cc9d64140f64fc84863c4277/treeb5cd837d4fe2596711fa8a4dd85caf39e3508c86自身候选10项/main11项适用Actions全SUCCESS。来源候选run39583968290/job119168158494/artifact12337938078，主线run39584279790/job119169193444/artifact12338712148各实跑10本包用例零跳过、重取64286/33218B两正文与十GIF对象，20真实正文语义改写拒绝/双外围script和重生成注记正例通过。远端内容干净检出130相关测试、九完整历史前缀及原生Git核验通过；独立正则/实体双核心与原词数值/有序图链一致，十图完整Pillow解码、五实际画面目视、五占位alpha[0,0]。CI仅比原字节与GIF结构，不冒称原客户端渲染或执行。

双ZIP真实下载，长度候选4442B/main4442B，SHA256分别21b46bd3a31fac7e30c93ca66c84b32375cdf850f7a213c264b595fdb8b793bd / 484ee50524be6c4c67a41e24532e215fa326d4c77289771b43430ce87f7cd735；各唯一replay.json19804B/SHA2568879a3ec6021797d56a9bfd235a2aaa3794f468f72962c9d0497fbcd78b5cff6/原生Git blobde5b40eefcb5fca0775af785914e97e22bb4a455，候选/main/本地逐字节一致。双raw、十来源/工具/依赖/工作流/规格pins、九完整启动前缀和21实际workflow永久置research/recovered/STONEAGE-CN2003-ONBOARDING-CUSTODY-R1.json；原HTML/版权GIF不入Git。

新增强制收据门后本包11项/131相关检查另实验收、删除收据必须失败；首轮10项历史不改写为11项，保管提交自身Actions后验，不套内容绿灯。投稿入口/作者资格、重生成/刊发、八字符/编码、二十点原词/运行时字段、预告/执行、五画面/五透明伴随对象保持分开。R49有限包结束；最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-50回全22域，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部历史保留。


## 2026-10-21 R50日服2004聊天过滤、探索信息与NPC配置分期

新读main531f15f7f3831300a288e66b8883adfafbb3c9f0/tree8b749c1c0a13648759d36703700cf55cf9feef38，438分支/0开放PR/4947项完整树无AGENTS；R49保管提交自身main11项Actions全SUCCESS，九启动全文/原生Git与22域索引新读固定。最高NEXT50轮换社交交互，不扩R49建角/新手村助手。

4Gamer2004-07-30 23:12署名Kawamura同期报道https://www.4gamer.net/news/history/2004.07/20040730231235detail.html 当前10860B/CP932，正文核心SHA4ea1de1163cd989576c5fd90714eb43644b6a222416ceedad8fd0aa9ab5af506；不是逐字运营发布文或运行见证。HTML meta作者不当正文署名，五正文槽仅一实文四空模板，不认证2004原字节。六记录/规格docs/specs/STONEAGE-JP2004-CHAT-UPDATE-SOURCE-R1.md新增。

报道登记对象聊天过滤，不补UI/容量/频道/身份键/保存、封号或交易阻断；首次大更新仅指报道所称2004年6月正式服务以后，8月1日15—16时为维护计划。新未名岛、サイナス岛/ジャルガ岛各一未名洞窟、マーナ推测秘密均不补地名ID/入口/剧情Boss；部分NPC迁居带ようだ，非执行认证。8月3/6日任务NPC配置及约30分钟维护，与记者推测新任务届时触发分开；无任务条件/实际开放/精确时刻。新用户十日试用不当所有人永久免费。

实际三图按HTML顺序_0/_2/_1，31490/26016/24235B、200×133/170×141/170×141，完整Pillow解码/目视为地图示意、木桥与洞口场景，均无聊天过滤面板，不认证地图/人物身份或原生分辨率。原HTML/版权JPEG不进Git。20真实正文语义改写绕过摘要门拒绝，外层script与meta作者正例通过；独立核心/日程/推断词/图序另核。候选/main独立取源及实际ZIP永久保管另据实追加。

有限止点一报道六记录三图，不扩聊天实现/未名地图/任务助手；重开需同构建官方UI/手册、实际过滤过程、地图名入口或任务开放日志。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-51回全22域另一具名材料，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，历史前缀完整，不报无分母整体百分比。


## 2026-10-21 R50同期报道双取源、图像边界与永久派生保管

内容ba4cb029df19e17e600b8190c91e622d831450e5/tree789916334c019e00db4a0d441a2b5abd33153809自身候选10项/main11项适用Actions全SUCCESS。来源候选run39586280930/job119175869090/artifact12339775719，主线run39586486553/job119176551830/artifact12339479771各实跑10本包用例零跳过，重取10860B正文及31490/26016/24235B三JPEG，20真实语义改写拒绝、外层script/meta作者正例通过。远端内容干净检出141相关测试、九完整历史前缀及原生Git标识核验通过；独立正则/实体核心、日程/约数/推断词与图序一致，三图完整Pillow解码/目视。CI只比原字节与SOF尺寸，不冒称聊天UI或客户端运行。

双ZIP真实下载，候选3435B/main3435B，SHA256分别6668720042822b995a8df522de3ea98ccdc80730edcfa72e724759b6b92ca068 / 9fc374ac7e73316eccfa90e05e98db449afd018c0d0739e88b44d5f7b97225a7；各唯一replay.json9108B/SHA256256f4fa8073b97c077c84518e0af2c3f2f78ddd785fe974c6366f1c85a68f637/原生Git blobaba19db65aafee3fb0cdda6080d129b938739de3，候选/main/本地逐字节一致。双raw、十来源/工具/依赖/工作流/规格pins、九完整启动前缀与21实际workflow永久存research/recovered/STONEAGE-JP2004-CHAT-UPDATE-CUSTODY-R1.json；原HTML/版权JPEG不入Git。

新增强制收据门后本包11项/142相关检查另实跑、删除收据必须失败；初轮10项历史不改写为11项，保管提交自身Actions后验，不套内容绿灯。媒体/运营原文、2004服务阶段/原作首发、维护计划/部署、NPC配置/记者任务推断、约30分/精确时长、聊天过滤/封号、配图/过滤UI与未名地图身份均分开。R50有限包结束；最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-51回全22域，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，历史完整。


## 2026-10-21 R51大陆2.0记录点贡品、原地登出与重入资料

新读main b1b12ebfacdb09580b812dd1fc5a498564145237/tree9f0ac6b72e66c5e8b00eb7cd4f1079c2819805da、439分支/0开放PR/4974项完整树无AGENTS，R50保管提交自身main11项Actions全SUCCESS。九启动全文/原生Git与22域索引重新固定；仅旧run37642417333仍queued，无in_progress，不抹去旧历史。最高NEXT51轮换记录点/位置重入，不扩聊天过滤助手。

从实际华义2.0导航取得基本操作、存储肉位置、公共设施：四精确档案20011204194619/20011204000349/20011204220248/20011204213609，HTML69317/68863/69407/73356B；不是首刊日、具体build或运行证据。运营站承载不认证具名作者/原手册逐字内容；正文“储存”指肉贡品换记录点，不当物品银行。三岛17表行加原地登出/交易YES/纪录点三行为，20记录及规格docs/specs/STONEAGE-CN20-RECORDPOINT-SOURCE-R1.md。

普通注销重入记录点、原地登出回登出地、被打飞回记录点，原地登出/原地注销标签分别保存，不推任何败北/掉线/跨重启；不是本地savedata.dat证明，不重开R79。对纪录点说话取在线人数，统计范围与刷新未知；贡品是否消耗/事务/保存载体未知。基本操作页交易只证接收方YES，不从2010或SA2指南补双OK。

17行北岛7/南岛8/吉鲁岛2，原地名、X/x、多坐标/多肉原样保留。加加/塔姆塔姆重复481，92与426，94、奇喀喀肉不详、191 365/342 466缺逗号均不校正；无地图NPC/物品ID，多坐标意义/多肉AND或OR不补。实际纪录点图片img/image011.jpg按本次正文捕获请求HTTP404，未取得图，不冒称画面恢复或所有档案无图；其余设施/操作图未递归。四HTML/原资产不入Git。

20真实源语义改写移除摘要门仍拒绝、外层script正例通过；独立正则实体表格与重入核心另核，候选/main自身取源与永久派生保管据实另记。有限止点一导航三页选段一失图请求；重开需同构建地图/NPC表、贡品日志/坐标对照或原服重入过程。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-52回全22域，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部历史前缀保留。


## 2026-10-21 R51四档案双重放与永久派生保管

内容a76e513abf98ea7ce0afc058f2aea43d97875496/treef64a5276fcd11250530b3cf57ba8f69da98a29a1自身候选10/main11项适用Actions全SUCCESS。来源候选run39588403816/job119182947281/artifact12339573656，主线run39588493806/job119183259840/artifact12339878480各实跑10本包用例零跳过、四精确HTML69317/68863/69407/73356B、17表行、20真实源语义改写拒绝与外围script正例。干净远端内容检出126相关测试、九完整启动历史前缀及原生Git标识通过；独立正则/实体重建17行、重复坐标/缺肉及重入核心一致。记录点图404仅为本地实际请求观察，CI没有重取图或解码图，不冒称画面恢复。

双ZIP实际下载，候选3296B/main3296B，SHA256分别6ecb21d9a9f207c9bf27df95eb00b494b3c526f2d8904af2b693d5ac1f4c9888 / 83e2d71ad61af87d851a6921e995adde1ed3f67b2f630320f506269a91482968；各唯一replay.json13283B/SHA256ee53863ce796cda16294efc8f2b60dcbda8daa4d4e5f2e4d9bc9c78ba50a3789/原生Git blob6f23139cee40299ba11b087104aa36f865f5b311，候选/main/本地逐字节一致。双raw、九来源/工具/依赖/工作流/规格pins、九启动完整前缀与21实际workflow永久存research/recovered/STONEAGE-CN20-RECORDPOINT-CUSTODY-R1.json；原HTML/版权图不进Git。

新增永久收据强制门后本包11/127相关检查另实跑、移除收据必须失败；首轮10项不改写为11项。保管提交自身Actions另后验，不套内容绿灯。采集日/首刊、运营主机/作者、记录贡品/银行、来源坐标/可执行NPC点、未知肉/免费、多肉顿号/AND或OR、注销目的地/保存载体、局部404/全部失图保持分开。R51有限包结束，最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-52回全22域；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部历史完整。


## 2026-10-21 R52大陆2.0三宠物网页外观补充与阿米朵旧对照

新读main47b593b715e25ecb55af2e9b080d92b7a247b182/tree16f697a355ccdf82a07dc4ed038e9688aa4b690f、440分支/0开放PR/4984完整树无AGENTS；R51保管提交自身main11项全SUCCESS。九启动全文/原生Git与22域索引重新固定，仅旧37642417333仍queued，无in_progress。最高NEXT52轮换宠物外观，不扩R51记录点/保存。

选材核对发现104格三页目录已验收，故不重做名录。固定首目录、有限目录和阿米朵视觉报告全文，重取既有20011204194619华义2.0正文69317B/SHA561950fd7bba41e7d39f4a781a671e11e175c7fe08dd1b5481fdf1fd23ba351b。本轮新增网页位置001/004/040三图片像素，007阿米朵仅旧对照；规格docs/specs/STONEAGE-CN20-PET-VISUAL-BATCH-SOURCE-R1.md，三研究记录不当原宠物实体。

001字面???→img/newpet/6.JPG，20011205050022/4196B；004字面??2→2.jpg，实际20011023194345/3785B且最终原主机无www；007阿米朵→7.JPG，20011205051046/4831B旧SHA一致；040呼波波→40.JPG，20011023183116/3520B。四JPEG全Pillow解码RGB83×90单文件帧并原像素目视：绿色四足、蓝圆形轮廓内浅色形象、既有黄褐阿米朵、蓝色直立形象。问号两名不补，呼波波来自源单元格；不推物种ID/技能/SPR/模型/动画。初次从正文档案跳各图，CI只精确取最终捕获，不重演初跳；主机差异不当全站等价。001/004有HTML83×90，007/040未声明，不回填。

旧104位置/98具名/6问号历史报告不变；补充后4引用已取、100未取，本轮新增3/旧对照1、新解名0、新原游戏实体0，不当物种总数或百分比。14实际HTML改写排除digest仍拒绝、4图真实字节反例与外围script正例；独立单元格/实体/路径大小写及JPEG SOF尺寸另核，候选/main实际取源和永久保管据实另记。

止于一既有正文/三新图一旧图/三父Git报告，不自动追100图或helper。重开需明确原名、同构建SPR/原动画/数值表。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-53回全22域，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部历史前缀完整；原HTML/JPEG不进Git。


## 2026-10-21 R52三新图一旧对照双取源与永久派生保管

内容bbe5302f17e182dddb86a598590cbbe8e38775b0/tree16cd0048f6abb44291fb3850a90882418fe64130自身候选10/main11适用Actions全SUCCESS；来源候选run39590372930/job119189528231/artifact12341830649、主线run39590585725/job119190238811/artifact12341196429各实跑10本包用例零跳过，一69317B已知HTML及4196/3785/4831/3520B四JPEG实际重取并完整像素解码，14真实HTML语义反例、4真实图字节反例和外围script正例通过。干净远端内容检出79相关测试及九完整启动历史前缀/原生Git标识通过；独立四叶单元格名称/路径/大小写、JPEG SOF尺寸一致，四图本地原像素目视。CI不复演人的目视或首次档案跳转。

双ZIP实际下载，候选3289B/main3289B，SHA256分别43ee67d23dc76a9c7904e25ccd91199f0a3ef12f66d020908655cfa6319d43ee / ad4ba2cbf4130491da101b75c45b1d1cd8a8f2e392a313a98f3c23d53b8e78fd；各唯一replay.json11704B/SHA256df992d998a148eecd7e2700b4fae6f0536855858520a5d6086a6d3a0d802ef61/原生Git blob517a955fdb8789f193e30b4b9e1ebbb395cd9847，候选/main/本地逐字节一致。双raw、十三来源/工具/依赖/工作流/规格/父报告pins、九启动完整前缀与21实际workflow永久存research/recovered/STONEAGE-CN20-PET-VISUAL-BATCH-CUSTODY-R1.json；原HTML/JPEG不进Git。

新增强制收据门后本包11/80相关检查另实跑，移除收据及等长改写派生raw一个字节必须失败；首轮10项不改写为11项，保管提交自身Actions另后验。新3/旧对照1、六问号仍未知、104引用中已取4/未取100、网页名/原实体、分时图档/同构建、HTML声明/实测、单JPEG帧/原动画、目视/CI解码、原档主机差异/全站等价继续分开。R52有限包结束；最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-53回全22域，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，所有旧记录完整。


## 2026-10-21 R53大陆2.0回复法术13行、正文目标与数值疑点

新读main7a6042d15f102e18cfb9eec01ef0f6e8e430639a/treeb88673c3d3ea14845fef48a55dda4558090ce344、441分支/0开放PR/4994完整树无AGENTS；R52保管提交自身main11项全SUCCESS。九启动全文/原生Git与22域索引重读，仅旧37642417333仍queued，无in_progress。最高NEXT53轮换战斗回复，不扩R52剩余100图。

既有华义导航真实“回复系”href取得新正文：20011204194619导航69317B，实际回复页20011204210425/67848B/严格GB18030/SHAaa159ec42c9faf663dd726b98d356e4fb56f6903d7a75270fb52c367518e4f80，核心d9e2a259142d981fdc2e4581979ba519b3a0b2f83daa11b8521786efa77c12cf。初请导航时间实际跳正文捕获，CI只取最终精确URL；无署名运营主机指南，不认证作者/首刊/精确build/原服。13等级行+1正文语境均带七字段，规格docs/specs/STONEAGE-CN20-HEALING-SPELLS-SOURCE-R1.md。

原rowspan4/4/3/2为治愈/滋润/恩惠/复活，费用依序5/8/11/14、8/12/16/20、20/30/40、20/35。滋润LV2原+10且耗12，低于LV1+50，疑点保留不补100；表LV不当人物要求/跨版最高等级，耐久力/气力不自动绑定HP/MP原字段。哈鲁仅玩家/表自身、芙蕾雅我方一人或一宠/表单体、提欧全员/表己方全体分层；正文神恩/表恩惠不改名。复活三名希鲁菲尔/雅鲁/哈恩不强配表两等级，也不推顺序升降。主要寄宿衣服铠甲防具不当仅限或全部；宠物昏厥复活建议的少量忠诚下降与经验不当零损/满返公式。

固定旧战斗派生全文/原生Git，CN20-BATTLE-02装备附魔只作定性对照，不重新取旧正文图、不认证同build或执行。18真实源语义改写排除digest仍拒绝/外围script正例；独立13行及疑点/费用/名字另核。内容无图，不抓导航chrome/其它法术页；原HTML/资产不入Git。候选/main自身取源及永久派生保管据实另记。

本地预检曾错误把旧source_reported对象当字符串，首轮10项1项错误/重放拒绝；修正实际meaning读取并建立有效基线。导航反例按真实font嵌套修正，不冒称那轮已通过；非来源变化或远端Actions失败。有限止点一导航一正文一父Git，不实现治疗或扩其它四系；重开需同版配置/ID、原文+10更正或战斗/气力/忠诚经验日志。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-54回全22域，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部历史前缀完整。


## 2026-10-21 R53回复表双重放与永久派生保管

内容0278ba470b32816aaa072f5e4596d812bb0a5d14/tree2876b1b69b23ac322537011de0ee88a5a533ef12自身候选10/main11项适用Actions全SUCCESS。来源候选run39592464093/job119196561009/artifact12341224452，主线run39592599479/job119197008183/artifact12341743477各实跑10本包用例零跳过，实际重取69317/67848B两HTML、解析rowspan4/4/3/2共13行、18真实源语义改写拒绝及外围script正例。干净远端内容检出59相关测试/九完整启动前缀与原生Git标识通过；独立正则/实体13行效果/费用/名字/限定语、中文表13行逐格一致。图片请求0，旧战斗原正文/图不重取，原客户端/服务器/后代治疗模型不执行。

双ZIP实际下载，候选2686B/main2686B，SHA256分别b44cb0bc2f39b40c5532b7fada8fdab5ba71fede4e8a66c4e256035eecfff293 / 36f7b9c7224c75a3b2a9b65d1c0be795ba7be04c284632b3fcff334d38596df2；各唯一replay.json13077B/SHA2567a7826645bba41ad773fe085fc2b40898aad7066b03b3a6f0df3c23b6c3135cf/原生Git blob4e7aa4114c20e5acbe93b0cc3ebc8093714ca35e，候选/main/本地逐字节一致。双raw、十一来源/工具/依赖/工作流/规格/父报告pins、九启动完整前缀及21实际workflow永久存research/recovered/STONEAGE-CN20-HEALING-SPELLS-CUSTODY-R1.json；原HTML/资产不进Git。

新增永久收据强制门后本包11/60相关检查另实跑，移除收据及等长改写派生raw一字节必须失败；首轮10项历史不改写为11项，保管提交自身Actions另后验。原+10/猜100、正文神恩/表恩惠、自己/玩家/单体/全体、三复活名/两等级、主要防具/仅限或全装备、复活建议/零忠诚满经验、气力耐久力原词/运行字段、同站概念/同构建继续分开。本地首轮父报告层级错误与反例锚点修正历史保持，非远端失败。R53有限包结束，最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-54回全22域；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部历史完整。

## 2026-10-21 R54大陆2003宠物加工与料理同期玩家指南边界

本轮以新读远端main 05f14965b3c87481f2dec104813f624e553b76e6/tree f3ddbc12795a7216f002175c3f6064ed28baae62 为基线；完整当前状态原Git blob、连续性协议及22域组合索引新核，R53主线最近可见11项Actions全SUCCESS、0开放PR。最高NEXT54轮换物品/合成/料理，未继续扩大R53回复法术、R52图鉴余图与暂停的R79。

2026-10-21实际查看两2003年新浪游戏网页可读正文：2003-04-15 22:14《石器初体验》标“网友投稿”(https://games.sina.com.cn/zhqu/sta/xsxl/sqcty.shtml)，2003-04-02 16:03《合成入门》署新浪游戏(https://games.sina.com.cn/zhqu/sta/wphc/wphc_1.shtml)。两页不是原始华义服务器规则、具体客户端build或台湾1.0；没有读取/锁存原始HTTP HTML字节或独立SHA，未重取原图，更没有原商业客户端执行。因此仅作同期来源受限文字结构化，不能借用R53真实双重放等级。

新增规格docs/specs/STONEAGE-CN2003-CRAFTING-GUIDES-SOURCE-R1.md与衍生research/recovered/STONEAGE-CN2003-CRAFTING-GUIDES-SOURCE-R1.json：S2原表18条装备类别/有序材料/列示百分比区间，原弓“木＋？＋丝”保持问号；S1七道新手料理、凯比特“加工”与乌力“料理”示例。关键源级矛盾：S2枪“石＋木”表列40–60%、投掷斧“木＋石”表列30–60%，S1木1/石1称枪；无序材料多重集重叠但**不能**证明服务器忽略顺序、确定产枪、随机双结果或指南成功率是原配置。加工/合成UI用词也不自动合并。原料后缀1/2/3不静默映射数量或等级，NPC/道具/技能ID未知。

候选分支agent/cn2003-crafting-guides-r54-20261021，新增本地派生元数据结构测试及专用Action；检查对象仅Git派生JSON的18+7项、未知位、重叠但不提升运行事实、来源级别，并不联网重取两原网页；原商业图片/二进制未入Git。候选/main Actions应以后验实际结果为准，严禁把提交前检验预先称通过。有限止点两页25项，不扩配方全站、数值公式及后代执行。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-55回全22域另取材料；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部旧历史前缀必须保留。


## 2026-10-21 R54加工与料理派生源主线验收及永久收据

R54资料提交2dd1c7a28b8993bebaf141b32b4cd1d4e1a7377c/tree b3fb195f0638443abae575dffe61cdae47375f43，以原main 05f14965b3c87481f2dec104813f624e553b76e6为父；候选分支agent/cn2003-crafting-guides-r54-20261021的10项Actions全部completed/success，主线同SHA的11项Actions全部completed/success，主线通过非强制的fast-forward+expected HEAD安全更新。专用候选run39594725260/job119204095403和主线run39595001302/job119205009874实际日志均显示4项派生数据检查通过、零跳过；其余Actions是现存验证矩阵，不冒称新增网页/原游戏实测。历史原CURRENT-STATE/TIMELINE/ROADMAP/SOURCE-REGISTRY旧Git内容均在R54提交中逐字前缀保留。

本轮另外永久保存research/recovered/STONEAGE-CN2003-CRAFTING-GUIDES-ACCEPTANCE-R1.json，将原派生数据Git blob bb33249f20713199afc488dbf1eee2d9b42907e5、候选/主线运行及工作单元ID、执行范围、原网页字节证据欠缺与非原服事实限制相联。专用回归测试新增必须存在的收据与原派生blob SHA1一致性门，原专用workflow增加收据路径触发；收据提交自身Actions需独立后验，不沿用旧4项绿灯。原始HTML SHA256和独立原客户端执行仍无，永不把派生绿灯提升为原服成功率。R54 25项指南材料有限包结束，下一最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-55轮换22域另取源；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，历史记录不覆盖。

## 2026-10-21 R55早期贝壳送物任务、获取路线与波拉岛入口归属

本轮启动时重新读main 8a0cd2d7f3de81737349250bd042692b07bcc866/tree 0f727a4eadc9c3f6cc48f38f48b81787117515f7，R54上一轮状态及主线验收已保存，最新同HEAD 11项可见Actions全部success/0开放PR，原CURRENT-STATE精确Git blob完整读取。按22域轮换至quest/story/worldline，最高NEXT55，不再重复R54宠物加工或扩R53回复法术。

三同期来源的网页可读正文于2026-10-21核对：2001-12-10 17173《归纳拿不可思议的贝壳的5种方法》署名诗雨玩家投稿；2003-05-29 10:15 新浪《弥生与日美子的友谊》标网友投稿；2003-06-04 18:40 新浪《英雄岛前传》署新浪游戏。未取得原HTTP/HTML字节、源SHA、精确客户端build、原华义服务器脚本或实机运行，不能冒称R53级别的来源双重放。旧2001来源第五条坐标和恐龙名显示损坏原文，保持未解析，不校正。

限定规格docs/specs/STONEAGE-CN2001-2003-SHELL-QUEST-SOURCE-R1.md、衍生research/recovered/STONEAGE-CN2001-2003-SHELL-QUEST-SOURCE-R1.json：2003双方出生地双任务路线Q_A萨姆吉尔/卡鲁它那→日美子送花给弥生→贝壳，Q_B玛丽娜丝/加加→弥生送贝壳给日美子→花；日美子两段局部坐标(56,124)/(57,124)不能自动合并，二村世界坐标不可当NPC局部坐标。2001玩家稿五条贝壳途径只是作者枚举，不当全局穷举：北岛送物、哥亚山/卡鲁它村商人、吉鲁岛小猪爱情、美鲁娜洞窟1000Stone购买、英雄岛饥饿村民食材交换。

**关键新增矛盾**：2001报告弥生→日美子送贝壳得到贝壳，2003同一方向却是贝壳换花。两者分源保留，不擅推版本改动或作者错误。2003说明贝壳宠邮受限、丢地消失、花送贝壳重作损魅力一点；只有玩家指南陈述，非原服道具过滤/忠诚或存档逻辑。2003英雄岛前传说背包持贝壳与萨姆吉尔村黑乌力(71,49)对话进“五十年前的波拉岛”；其80级要求/建议120属于英雄岛前传任务，不上升为传送门自身80级门槛；贝壳是否消耗、服务端时间线与首次原版存在均UNKNOWN。来源只作为未来世界观可选参考，不执行新石器设计。

另有专用衍生记录结构测试/CI，守三个源、双路线、两篇冲突、五条2001作者枚举、文本损坏位置和入口等级限制；CI不能证明HTML源字节与游戏运行。有限止点三页及派生记录，不递归英雄岛全部后续怪/奖励；下一NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-56，从22域另选。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79 PAUSED，全部旧历史前缀必须保留。候选/主线验收以真实Actions后验为准，不能在提交前预先称绿。

## 2026-10-21 R55候选/主线CI真实验收及永久派生收据

内容提交6eada4a406b0d1709b29ad9bb1b0e858b9fe87da/tree085b0d587bcd390ee952591cefcc6756fb7d4ac1已从R54 main8a0cd2d7f3de81737349250bd042692b07bcc866非强制fast-forward、带expected HEAD写入主线。9文件差异是5新增、4历史文件仅追加，Git原有行无删除。候选agent/cn2001-2003-shell-quest-r55-20261021同SHA 10项Actions全completed/success；来源候选专用run39599917007/job119221512082，日志4项派生结构测试成功、零跳过。main同SHA 11项Actions全completed/success；主线专用run39600076749/job119222049029，作业亦success。两run均没有生成/上传ZIP artifact，不捏造artifact ID、ZIP哈希或双次源HTML实时重放。

唯一持久衍生报告research/recovered/STONEAGE-CN2001-2003-SHELL-QUEST-SOURCE-R1.json为原生Git blob7157f1aca0e4f806334bb4892d294d93d106690d、UTF8 7762B、SHA256 411cd1fb8bec4c08e5ac78fa8987fb58f0cd7ee55c41397cbfcc9d0163e91d5f；永久验收收据research/recovered/STONEAGE-CN2001-2003-SHELL-QUEST-ACCEPTANCE-R1.json记候选/main run/job、内容SHA、原来源三URL、正反证据边界及缺失HTTP原字节/原游戏实测。新增收据必须存在+源派生SHA256强制测试，原4项升级为5项后的**收据自身候选/main Actions待后验**，不把早前4项成功写成5项。新工件仅为版权所有无争议的衍生元数据；未取得或存储原网页全文/图片/客户端、构建配置、服务器剧情脚本。

2001弥生→日美子给贝壳/2003同方向给花之矛盾仍OPEN，五途径不是完全集合，2003后续任务80级不是已证黑乌力传送门槛。R55历史材料包完成，下一最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-56回22域轮换；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停。所有过去报告内容保留。


## 2026-10-21 R56宠物技能训练收费、地点与不同网页版本口径

启动新核main 3380fddae94ca94967cb174491a38e8d62f9f552/tree df96f101780232c8aeb693798d0b50ba502ad51d，R55贝壳两提交已整合主线并有永久收据；同HEAD最近可见11项Actions全SUCCESS且0开放PR。最高NEXT56依据22域轮换pet skills / trainer economy，不扩R55英雄岛剧情、R54合成或R79本地存档。

查看新浪2004-02-23 15:24《宠物相关》https://games.sina.com.cn/zhqu/sta/xsxl/cwxg.shtml 和新浪未见可靠文章刊日《宠物资料》https://games.sina.com.cn/zhqu/sta/cwzl/chongwu01.shtml，后者©2006页脚不得当文章发表日。两页均属门户网页文字，不能认证同一个客户端build或初代官方配置。无完整HTML原字节/原SHA、图片下载、原服务端配置或商业原客户端执行；只作可读网页的文献限定派生。

新docs/specs/STONEAGE-CN2004-PET-SKILL-TRAINER-SOURCE-R1.md和research/recovered/STONEAGE-CN2004-PET-SKILL-TRAINER-SOURCE-R1.json：S1可见19行宠物技能名／页面效果／学习地点／列示价格（保留地球一周2399、达那防御例外），S2有界挑11条供语义冲突和后代技能补充。特别保留S1猛毒攻击攻-30%／3回合／4400与S2攻-50%／5回合／4000；一击必杀3倍含模糊“容易被击中”与S2 2.5倍／命中-30%；骑宠课程S1四级与S2下中上三级；旅途／旅程伙伴敌人一人／敌宠一只及学技两村／SBC。不能用S2未定刊期猜改版顺序，不能合并成确定性游戏公式、统一NPC或价格表。

S2宠物邮件笼统称某些落地消失特殊物品不可邮，不具名R55贝壳，故不能当贝壳实际禁邮第二条独立证据。S1忠诚约70/20/10的失控描述仍只是指南，非原服务端阈值；S2九大家族与五转机暴不回填TW1.0。专用派生元数据结构测试/CI只验证19+11行、5组矛盾与版本缺证负边界，不是HTML源双重放或技能实测。候选/main的Actions要按实际结果后验，不预报全绿。本包两页30条有限止点，下一NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-57轮换22域另取，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79继续暂停；旧历史完整保留。


## 2026-10-21 R56技能表候选/主线实跑验收与永久派生收据

内容提交83c8c8279cd5913d9c75eec467c64a965c8cfba1/tree674511414043d78f29b53317d093cac3703a121a由R55主线3380fddae94ca94967cb174491a38e8d62f9f552非强制fast-forward、带expected HEAD写入main；Git compare显示9变动：5新增、4历史文件仅追加/旧行删除0。候选agent/cn2004-pet-skill-trainer-r56-20261021共10个Actions均SUCCESS，主线同内容HEAD共11个Actions均SUCCESS。候选专用run39603382601/job119233280942、主线专用run39603519751/job119233745574各真实执行5项衍生字段/来源边界测试成功、零跳过。双方专用run查得artifact数量均0，不虚构ZIP或初代原客户端重放。

衍生研究research/recovered/STONEAGE-CN2004-PET-SKILL-TRAINER-SOURCE-R1.json原生Git blob b6f42811c23cadc8b80fabb0a53b98a6aa9e8b2f，UTF8长度14778B、派生SHA256 90bc79a7c824ffae88f2e974de692252fb37345eacafa9db26f87bb62bbc9a70，19条S1完整可见学技行＋11条S2对照及5组来源矛盾永久存在Git。新增research/recovered/STONEAGE-CN2004-PET-SKILL-TRAINER-ACCEPTANCE-R1.json记录内容提交/双工作流job/两URL/缺失原HTML与实机证据；测试增加必须存在收据及SHA256原字节逐验门，专用workflow添加收据路径触发。收据**自身提交**的5→6测试与候选/main Actions须完成后另后验，不沿用旧5项绿灯。

2004《宠物相关》与S2未定刊期《宠物资料》同名技能冲突仍不认证任何patch顺序；猛毒攻击效果/费用、一击必杀乘数、骑乘课程3/4级、旅程伙伴对象及训练地分开；宠邮泛指特殊物品不认证R55贝壳过滤器。无原网页HTML SHA/精确build/技能或NPC ID/商业原服测试。本包有限闭合，最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-57回22域另取重要材料；Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79暂停，历史全部前缀保留。


### 2026-10-21 R56永久收据首轮测试路径错误与修复（不改写历史）

首次收据候选7f5dbb1291891ffd27d700d849b9e51ce8038850专用Action run39604156414/job119235960504实际**FAILURE**。本轮静态预检发现测试将派生JSON所在的research/recovered目录作为根，再拼一次research/recovered，导致收据查找路径重复；与网页内容、来源真实性、Git SHA256或客户端规则无关。非强制提交b4f823f1c418b0569a7c938a7dfa99af6a212351仅改测试的仓库根路径为P.parents[2]，对应专用run39604294631同HEAD SUCCESS，首轮失败不称SUCCESS也不从记录中删除。此前来源内容提交83c8c8279cd5913d9c75eec467c64a965c8cfba1的main11项Actions独立全SUCCESS。下一次完整候选/主线Actions将按最终HEAD后验；最高NEXT57不变。


## 2026-10-21 R57 2003年操作、组队交易与原地登出的来源限定取证

新读取main 4e11dc8983cfbe0b1b667e5ee45a3b1ee4a4de6d/tree 5d991edadd52c12dd484dd4c689dc1be6e8127c4、连续性九文件与22域索引，R56候选失败修复历史保留。R57有限审查新浪2003-04-15 23:29网友投稿《游戏操作》（正文多次命名《海贼王遗迹》）及2003-11-18 15:33新浪转述华义《增开服务器组》消息（明确2.0怀旧服）。逐条归档S1指南20项游戏操作与S2公告3项。S1含移动/朝向、面向NPC文字对话、告示牌、背包满/拖地、下7窗/上8键、队长带队、面对对象组队YES、双方交易YES/OK、HELP五人描述、决斗、13动作、原地登出、宠物模式与战斗指令等待等；S2提2003-09-04 2.0服务器组开放、2003-11-19新组及“更安全交易”。两网页都未取得原始HTTP/HTML字节哈希或原商业客户端/服务端执行。

**四项负边界：** (1) S1同页Ctrl+I“所持道具”与Ctrl+L“道具视窗关闭”矛盾并存；(2) S1海贼王遗迹与S2 2003年2.0怀旧服不能合并同build，2003-09-04不是2.0最初发行；(3) 两人OK与“更安全交易”没有服务端原子事务映射；(4) 原地登出／记录点仅网页说明，不证明原TW1.0 savedata字段或商业服务器状态。S1这些操作也不回填初代实机、UI像素、NPC/交易/战斗配置。

新增docs/specs/STONEAGE-CN2003-UI-TEAM-TRADE-SOURCE-R1.md、research/recovered/STONEAGE-CN2003-UI-TEAM-TRADE-SOURCE-R1.json、R57审查页、专用6项派生元数据测试及workflow。来源是2003年具名网页阅读，不冒称原始页面双重放或真实版本运行。研究/候选和main Actions未经验收不得宣称通过；永久派生保管收据应在后验另写。止于两页23个记录；最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-58，Stage A7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，历史旧文本逐字保留。


### 2026-10-21 R57内容提交及双端CI后验，永久派生保管

R57研究提交 72d5dceb03900c7f80a143201bddc11caeb1121d/tree 2a04834f9b930d1716a2b9ca7f6769fc1fdf19b4 从原main4e11dc8983cfbe0b1b667e5ee45a3b1ee4a4de6d建立，仅前进提交；GitHub compare实证9文件、5新增、4只追加、旧历史行删除0。候选分支agent/cn2003-ui-team-trade-r57-20261021该HEAD十项Actions均completed/success；专用run39608021253/job119249213662实际运行6个结构化数据与证据边界测试，零跳过。主线同HEAD十一项Actions均completed/success；专用run39608219457/job119249911845亦success。专用两run均查0 artifact，不捏造ZIP或源HTML独立双重放。

research/recovered/STONEAGE-CN2003-UI-TEAM-TRADE-SOURCE-R1.json源派生Git blob1bac3104c1d6b0d96a65a8c32e901de13a5df53d/UTF8 9904B/SHA256 ef9ee96f478aa9232b1cbb9fb71716ed36302f04dfa885c3cd0eaab29d4d82dd。新增research/recovered/STONEAGE-CN2003-UI-TEAM-TRADE-ACCEPTANCE-R1.json永久收据记录内容提交、双Actions、两个同期网页的来源URL、零artifact、未取得原网页原字节与商业服务端实测。专用CI由6升级至7项，新增收据存在、派生原字节长度和SHA256验收门；收据提交自身的候选/main Actions须另行后验，绝不可把旧6项结果称7项运行。无版权原始HTML/资产入Git。保留快捷键内部矛盾、海贼王遗迹vs2003的2.0怀旧组分期、交易OKvs“更安全”机制未证和原地登出不等于TW10 save原数据。最高NEXT58，Stage A7 PARTIAL+2 OPEN，B/wiki GATED，R79暂停，旧历史全文不改删。


### 2026-10-21 R59：2003职业技能依赖，版本化网页资料包

从22域组合轮换到角色成长/职业系统，真实新增2003两网页的3职业、3共通技能、9例文学习门槛与8条负边界；docs/specs/STONEAGE-CN2003-PROFESSION-DEPENDENCIES-SOURCE-R1.md 与 research/recovered/STONEAGE-CN2003-PROFESSION-DEPENDENCIES-SOURCE-R1.json。此包有实质玩法来源，但只到门户文字，绝不归属初代1.0原服，也不把熟练度70、技能点16直接做新游戏参数。范围闭合后轮换另一个域的另一具名版本内容 NEXT R60，防止无止境扩展职业技能树。Stage A与Stage B门槛不变。


## 2026-10-22 R61：家族成立、权限与庄园服务的来源限定关系

启动重新核main `2102aa48ab2a5abe37c27d852976219071f3bff9`/tree `5ff02575e2fa3388b57e8d468a2cc21b9b0137ac`，455分支、0开放PR、0运行中Actions；该HEAD实际main9项、候选7项均completed/success，不能把路径未触发的其它workflow记为运行。完整CURRENT原Git blob d704519240fdd25aeb16accf3c7528b6bdaad30d和九份启动文件原字节/原生Git标识已核，R60真实失败/修正历史完整保留。按最高NEXT61回22域，从交通转入家族社会服务，未重开R79。

重新阅读新浪2003-04-15 23:29标网友投稿的《游戏操作》https://games.sina.com.cn/zhqu/sta/xsxl/yxcz.shtml ，只补R57没有结构化的家族/家族键/庄园功能章节。**同一URL再次取读不是第二个独立来源**。新增 docs/specs/STONEAGE-CN2003-FAMILY-LIFECYCLE-SOURCE-R1.md、research/recovered/STONEAGE-CN2003-FAMILY-LIFECYCLE-SOURCE-R1.json 与R61审查页：四生命周期节点、七服务关系、五权限记录、三组范围疑点。30级/成人礼/10000石币只是申请说明，三日十成员另列为正式成立条件，族长是否计数、计时起点和超时退款仍UNKNOWN。

正文守护兽涉及特殊合成，不证战斗召唤；光明/黑暗精灵仅分别“影响”回复/攻击性魔法，增减方向和倍率不能补造。医生/银行需庄园及未知声望门槛，不能填免费治疗或账户事务。同页四大家族声望、九庄园与前二十名挑战资格保持分段、范围未解，不拼接一套规则；邀请函房间通行和封闭商店鉴权、骑宠学习同意书亦分别存储。既验R28/R43及TW75气势计划仅固定父报告/版本化对照，不当独立新网页或本文同build证明。

未取得原HTTP/HTML字节摘要或历史快照、原服规则/实际运行；原网页全文/图/商业资源不入Git。不增加只镜像资料行数的测试/专项workflow，采用源段逐核、父Git摘要与完整历史前缀检查、现有相关回归和实际候选/main CI；绿灯不提升来源等级。发布与CI结果须后验，未提前称通过。有限包止于一页家族章节，下一最高 `OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-62` 回22域优先具名版本宠物生态/遇敌或音效事件材料；Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING。


### 2026-10-22 R61内容双端验收及永久派生来源记录

内容提交 `8915bfd99d211a146e7c8ac796c98b61abe6b737`/tree `6cee9d32396d1446798e67afdcbf79cccee44046` 候选9项/main10项适用Actions全部completed/success。目录保管门候选run39687845053/job119526333692、主线run39687935975/job119526644445成功；这些是既有回归/边界工作流，不是新增网页原字节重放或原商业游戏运行。本地20项既有相关测试通过，未增加镜像字段行数的专项测试或workflow。GitHub compare七文件=三新增/四只追加，历史行删除0，九份启动完整前缀和四父报告标识逐一保留。

命令行推送访问中断，未确认发布；随后使用GitHub连接逐blob提交，七blob与本地原生Git全部相等，整tree亦相等，再以实时main预期HEAD保护非强制快进。永久来源记录 `research/recovered/STONEAGE-CN2003-FAMILY-LIFECYCLE-ACCEPTANCE-R1.json` 固定内容SHA/tree、19项实际run及两job、源JSON11824B/SHA256 `047497790eee98cd81db6d08f951580f102062e70516dfee0db20016b6aa07e0`/Git blob `0b2222f5ba48442ae1cfb07c923c83780b72ed2c`。无原HTTP哈希、源重放artifact或原服实测，不虚构ZIP保管链。旧queued37642417333仍单列为无关历史队列。

同一新浪URL不重复计独立证据；三日成员统计、精灵影响方向、四/九/二十适用范围继续OPEN。收据提交自身CI另行实查，不能沿用内容提交绿灯。最高NEXT62不变，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停。


## 2026-10-22 R62：渔村捕宠委托与19个名称的出没地关系

启动新核main `ee3130c269d8834746dd0b83ed60a925b3e836d7`/tree `1f8e60e409ff5c516853a0b1da97dd6f8c21cbb4`、456分支、0运行中Actions，历史queued37642417333单列；R61最终记录提交main8项/候选7项实际completed/success。九份启动全文与CURRENT原Git blob93f18d5609e8320fdfaaabe88d86c2013d253943重新核验、完整历史前缀保留，NEXT62选择宠物出没/任务经济关系，不继续家族或R79。

新取新浪《石器时代2之新鲜速递(三)--任务详解》https://games.sina.com.cn/newgames/0110/10236724.shtml 及其真实首分页10236724_c1.shtml，当前HTTP200、33058/33200B、严格GB18030，SHA256为90316967d80cd1b3fe5ad255624f890501776ce05203a7931b7617b3349a156a / 282fc11dded94b6b9440b51ab0e7dd89296a2e7a479a00a59e153a1f4d3012da。正文2.0标签/新浪署名仅文献范围；URL0110与页脚2004不认证首刊/官方作者/商业build。不是另一款2009续作图鉴，不称原历史快照或原服实测。

形成六份渔村宠物委托A–F：19不同名称、21目标—地点关系，连贩售员20,12/管理员18,12。成本50/80/150/320/400/1500S、报酬500/800/1500/3200/4000/?S各按原表；F未知不补15000，保证金返还/失败/净利未证。E目标与地点行顺序不同且凯比/凯比特为前缀名，按名字对应；两外部坐标不当矩形、便利店与NPC坐标不放同层，科奥/柯奥原字和凯比地下二楼范围保留。无等级/几率/昼夜/物种和地图ID，不把19名当19个已认证初代宠物。

新增docs/specs/STONEAGE-CN20-PET-COMMISSION-HABITATS-SOURCE-R1.md、源JSON、R62审查、有限解析工具和8项独立解析测试/专用workflow；本地真实两页另有16语义改写拒绝/外围script正例及独立逐行六组数值检查。最初本地预检误判“回上页”位置与总述标题唯一性，据原HTML修正后才通过；非远端失败。远端候选/main原页重取和派生工件/永久保管须实际后验，不预报全绿。原HTML/图/商业资产不进Git，第三页不取，料理和萨村其他委托不入本包。

有限止点六份渔村宠物委托，最高NEXT `OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-63` 回22域优先音效事件或具名画面/模型材料；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING。

R62同包增加既有19集合合同的可检索导出：6条quests文献关系、21条encounters地点关系，全部原game_ids=null/RESEARCH_METADATA_NOT_RELEASE_APPROVED，不生成物种master或网站。固定旧归档合同原Git与SHA256，目录含源语义摘要及P1/P2 URL，10项解析/目录测试覆盖名称关联、版本/权利缺字段拒绝。原8项解析通过记录不倒改成10项；远端双输出replay.json/catalog.json须后验。


### 2026-10-22 R62双端真实网页重放及永久派生保管

内容提交 `bfa487ae254aa2f6eb24bf8fa03f481b7f889a47`/tree `bac64b3248a3739193708c2cb79365bd2169e6de` 候选10/main11项适用Actions全部completed/success，主线以实时预期HEAD保护非强制快进。GitHub compare11文件=7新增/4仅追加，历史行删除0；11远端blob/整tree和本地一致，九启动完整前缀保留。源候选run39689552403/job119532052387/artifact12387901290，主线run39689613709/job119532259256/artifact12388126682，各真实执行10单元测试、两当前HTTP取源、16真实源语义改写拒绝与外围script正例；没有原商业运行或原图请求。

双ZIP实际下载4635/4635B，SHA256 `4551ae0c6f837a40d10d3aed3877d14fed77a7fd1f85f885d5e1edd0b6cd943a` / `62620ea98f6a1787b7d6bfed5e2561692d7fe18ec1967b13327ded3f73f2463e`，各含replay.json和catalog.json两派生文件。候选/main/local完整replay原字节均19562B/SHA256 `953f789ca0c5ff3809b6b8c7b04cb81894b6f9ac120c5656ed10ba8e10c3a1f1`，两catalog原字节亦等于永久27关系目录；本次两HTTP均实际重得33058/33200B及同初取摘要。不同ZIP摘要是实际容器差异，不伪称同ZIP。

两完整CI派生原JSON及源/目录分别永久入Git；保管链 `research/recovered/STONEAGE-CN20-PET-COMMISSION-HABITATS-CUSTODY-R1.json` 固定四派生文件原生Git/长度/SHA、来源输入、21实际工作流和双job/artifact/ZIP。原HTML/图不入Git。另加必须存在收据与四文件逐字节验收门，真实移除/等长修改证据文件必须失败；本包单元10→11项，**保管提交自身候选/main CI另行后验**，不倒改旧10项运行历史。

同源两分页不是两独立作者来源，当前网页字节不认证首刊或历史build；F奖励仍?、坐标框架/原ID/刷怪权重未知，27文献关系不当27原游戏实体。最高NEXT63回22域优先音效事件/具名画面或模型材料，Stage A7 PARTIAL+2 OPEN，B/wiki GATED，R79暂停。


## 2026-10-22 R63：日本2003标签开发图集的战斗／野外视觉参考

新核远端main `ba2a846b4f189cbe63ce7962cf338b082f1bf8a1`/tree `349ca12168df63783ed64a43bdb62f50aae9a7ba`、457分支/0开放PR/0运行中Actions，R62最终main9/候选8项实际SUCCESS，旧queued37642417333保留。临时工作区已消失，从精确远端commit建立干净新检出；九启动文件完整读取/原生Git摘要和CURRENT原blob8710fb3069b0b74685bd910d00da05fa257b902e已核，不借旧聊天重造。最高NEXT63音效/具名视觉二选一：原TW10音效事件→音轨绑定仍false、无新触发轨迹，故选有限视觉源，不扩旧helper。

4Gamer索引2003/12/12 20:20的真实图集链接→图库第一页→前二独立页面→其明确原JPEG，共四HTML/两JPEG。索引71076B/EUC-JP，图库3410B/CP932，两个独立页1826/1914B，原图242617/222940B、JPEG/RGB/640×480各单帧，完整SHA和HTTP身份见research/recovered/STONEAGE-JP2003-BATTLE-FIELD-VISUAL-SOURCE-R1.json。图库标1/3及12th Dec.2003，并明确画面开发中；近40张的宣传数不作确切总数。本轮15个第一页缩略—独立页引用中取2原图，其余13/图库页2和3/缩略图/导航图未请求。

目视第一张为战斗/目标选择参考：可见五个相似背甲形象、右上PLAYER两行四格菜单、求助文字及目标提示、中央14。只记共存画面，不证HELP效果/耗回合/目标约束、单位/默认秒数、物种ID或队伍上限。第二张为野外两个人形、左上Mail/右上Action和底部文字区；角色是否NPC、地图/人物ID及按钮行为未知。当前2026原字节、2003图集标签、1999版权年、拍摄时间及原生分辨率分开，未证2003同刻像素或已部署build。

新增中文规格、R63审查、15条screens归档（前2哈希绑定目视/后13实际元数据null）、有限解析/完整解码工具与专用CI。10本包测试与8真实源改写/外围script正例本地通过，原HTML/JPEG/程序不进Git。最初本地EUC-JP索引误按CP932严格解码失败，按真实声明修正后才通过；搜索阅读器打不开独立页但原HTTP成功，不记历史不存在。候选/main自身源重放、ZIP实下及永久派生保管另后验，不能预报绿。

止点前两张原图，最高NEXT `OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-64` 回22域另一地区/内容资料，优先早期具名NPC/任务/地图材料。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停；旧历史前缀完整保留。


### 2026-10-22 R63开发版画面双端重放与永久保管

内容提交 `2e7c6fea0984c015a9dfd3c08efbed5cc738e439`/tree `2d0e6ac9214510777b458ceded454b225b5324fe` 候选10/main11项适用Actions全部completed/success，主线实时预期HEAD保护非强制快进。GitHub compare10文件=6新增/4只追加、旧历史行删0；10远端blob和整tree与本地一致，九启动完整前缀保留。源候选run39693866957/job119546402129/artifact12389916564；主线run39694039366/job119546956810/artifact12390465612，各真实执行10单元、四HTML/两JPEG取源/完整解码、8真实输入反例与外围script正例；CI不复演人的目视或商业运行。

两ZIP实际下载3477/3477B，SHA256 `98211042535da278e81e702b72a8eab63ac7b186df8153adca2d7ec0aa188a33` / `fec412ba5f621dcbcf1aa0cc3e69cda4bc982d07c6fb15278d3248629a641ad7`，各唯一replay.json完整23241B/SHA256 `703a81bc572f3f8bb2e47d2762837bf4db32a7577f0b0b38f9f0b083dbd3b92a`，候选/main/local逐字节相等。六HTTP大小和摘要亦同初取。独立正则重建15缩略—独立页配对；JPEG SOF另验两图640×480/8位/3分量，与Pillow一致，不能据此称原生分辨率。

两原CI派生JSON和保管链 `research/recovered/STONEAGE-JP2003-BATTLE-FIELD-VISUAL-CUSTODY-R1.json` 永久入Git，固定源/双raw/旧音效门/旧归档合同原字节、Git身份、21工作流及双job/artifact/ZIP。原HTML/JPEG/音频/商业程序不入Git，旧音效绑定false未变。新增必须存在收据及逐文件原字节校验，真实证据副本等长改动或移除会拒绝；本包测试10→11，保管提交自身候选/main CI须另行后验，不将旧10项称11项运行。

开发警示、当前HTTP与历史字节未认证、两图目视/十三未取、14无单位与HELP行为未知继续保留。最高NEXT64回全22域另一地区/内容，优先早期具名NPC/任务/地图；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部历史完整。


## 2026-10-22 R64：恐龙博士的具名NPC、捕宠培育与分源奖励

新核远端main `099a196d44c5e34b382c31b912962ac94c158ca4`/tree `b352da6dbf506929ccf324484f16d89998cb280c`、458分支、0开放PR、0运行中Actions，同HEAD main9/候选8项实际SUCCESS；旧queued37642417333无关。完整CURRENT 2309305B及九启动原字节/原生Git身份已核，最新NEXT64选早期具名任务域，不继续上一包日本图库或R79。

本包三份当前HTML：既有新浪汇编入口及真实c2#17、2003-05-29 11:37标网友投稿的《恐龙博士》。HTTP200，37893/36563/52445B与SHA256完整记入research/recovered/STONEAGE-EARLY-DINOSAUR-QUEST-SOURCE-R1.json；旧汇编页是已知网页的新选定节结构化，不重复计新独立来源。早期目录2001-01-18、当前页2004-01-06发布注释、S2的2003时间和2026原字节各自保留，无历史同刻/精确build认证。GB18030替换1/2/0，选定业务段全无替换。

新增中文规格docs/specs/STONEAGE-EARLY-DINOSAUR-QUEST-SOURCE-R1.md、R64审查、有限工具与源重放workflow。S1/S2各两段任务＋S2哈鲁/助手吉鲁共六文献归档关系，原ID均null。鲁尼贴斯/鲁尼帖斯、阿西美加/阿西美拉护符1和18档护符说法分源，不能据此称确定改版；S2玩家15/25仅建议，宠物15以上/30另字段，S1布克布克LV1不回填S2。博士与同名治疗精灵哈鲁不合并，入口328,633与研究所11,12不混层。取走多宠/骑乘宠警示不证选槽/实际消费/事件或存档，原始NPC/物种/任务ID仍未知。原HTML/图像/程序不入Git。

本地六测试和12真实输入语义反例＋script正例通过；初检标题误判（前置条件重复名称）及引号跨段误抓已修复并保留过程，未发生对应远端失败。实际候选/main重放、ZIP下载和永久派生保管须另后验，不预报绿。有限止于两任务三HTML，最高NEXT `OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-65` 回22域另一材料域，优先可归属音效事件或官方地图/生态；Stage A7 PARTIAL+2 OPEN，B/wiki GATED，R79 PAUSED_NON_BLOCKING，全部旧历史原字节前缀保留。


### 2026-10-22 R64双端真实网页重放与永久派生保管

内容提交 `79daaaa74ed66cef7368334d91bc99853e1e87f1`/tree `4d710db760922054f1cca62a517fd94feb391a31` 候选10/main11项适用Actions全部completed/success，以实时main预期HEAD保护非强制快进。GitHub compare10文件=6新增/4只追加，历史删行0，远端十blob/整tree与本地一致，九启动全文前缀保留。候选源run39695579401/job119552007672/artifact12391110582，主线源run39695651564/job119552252036/artifact12390501269，分别真实运行六单元、三当前HTML重取、12语义改写拒绝和script正例；非商业游戏运行。

实际下载两ZIP均1373B，SHA256 `d4edb91ca835ada0c1eb582c9e1f3f5f7e4d81bf721fe4d7103406882fb7cc8f` / `4778d399f727dd9cd678c1987f66f93ddd427f7d64a69253ed9f1b7fd7ece921`，各唯一replay.json，完整2932B/SHA256 `8787d2eb0fd28ecb12c39d5108fab7a5e341d24f128b21c6468ef87f1762af57`/原生Git blob `0a5b5108cf76f8a74d51691eed94160d805d91b8`。两CI/local完整raw逐字节相等，三源输入大小及摘要同初取，真实ZIP差异不抹平。独立一次性词法复核先漏HTML实体解码导致断言失败，补实体解码后原姓名/坐标、建议等级、前置/18档/LV1逐项一致，非来源变化。

永久派生两CI原JSON及research/recovered/STONEAGE-EARLY-DINOSAUR-QUEST-CUSTODY-R1.json固定内容Git、双job/artifact/ZIP、21项Actions和六文件原生Git/SHA/长度，原HTML/图/程序不入Git。新强制保管门检查实际文件缺失及等长篡改，单元六→七；**保管提交自身候选/main CI须另行实查**，不将旧六项倒称七项运行。史料日期、两源名差/奖励差、建议等级、同名精灵非同NPC、取宠/存档未知均保留。最高NEXT65回22域优先音效事件或官方地图/生态，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，旧历史全文不改删。


## 2026-10-22 R65：日服封印地域与宠物展示／放生／邮寄的来源分界

启动新读main `3e1f4c7ce75def12a63e0c3b76ac9a68b6ac0c62`/tree `d42c31975755e9020fcd140d8467d1d59e8d5dbc`、459分支/0开放PR/0运行中Actions，该HEAD main9/候选8项实际SUCCESS，历史queued37642417333无关。完整CURRENT 2313363B/blob d71f2cb9da6741273aadd354cf7a0ab5e26eb8ba及九启动全文指纹核验，按最高NEXT65选地图生态；无新TW10事件实参，旧音效API树不重开。

新取4Gamer Asakura署名2004-09-17 19:12《封印の開放》相关同期报道，10300B/SHA256 f544f907badeb6855cc79bd76821d8e0aaf8c5498e095bc1d193cb5c5e47a057，CP932严格解码；7月已归档报道10860B/160d53f4aa399d06ca9406b00baf0bd85e955370571957fd08e45aceb92455ad仅重取上下文，不计新来源。S2报道第三弹、当日新增封印された洞窟／穀嶺の地和展示／放生／一次一只宠邮；媒体当日完成语气仍非本项目原服认证。官方stoneage.to仅原文出链，未访问或冒称直接运营原文，2004同刻原字节及精确build未证。

新增docs/specs/STONEAGE-JP2004-SEALED-REGION-SOURCE-R1.md、R65审查、research/recovered/STONEAGE-JP2004-SEALED-REGION-SOURCE-R1.json与有限解析/CI：七来源目录=版本1、地图2、未名生态提示1、操作文献3，原ID均null；不是七原游戏实体。S2洞窟东侧参照岛与S1未名新岛、2006群岛不自动连接；地底前往不补洞窟直通、物种/坐标/机械文明秘密。自拾取展示与放生放手不混，永久删除/售款/选槽/持久化未知，宠邮只数不等计时或旧上限。五父报告原生Git/SHA固定，既有19集合合同沿用，原HTML/原图/程序不入Git。

本地七项边界/实际父文件缺失与等长篡改检查，17真实源语义反例（去正文摘要比较）与script/meta作者两正例通过。最初EUC-JP误用按源Shift_JIS声明修正CP932，另反例跨SPAN未命中后缩为真实连续文本；本地修正过程保留，非远端失败。候选/main自身Actions、ZIP实下与永久派生保管需后验。止于两HTML/两区域与三宠物操作，最高NEXT `OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-66` 回22域优先具版号经典辅助工具能力新材料，保留非官方来源；缺新源则选具名物品/配方/经济，不扩本包helper。Stage A7 PARTIAL+2 OPEN，B/wiki GATED，R79暂停，历史完整前缀不改删。


### 2026-10-22 R65双端网页重放与永久派生保管

内容提交 `2a0583bc5961e2220cbf2335e66aeb72df8ec078`/tree `9ca97ba64ca171225f35e50bcc59d1f0e223c779` 候选10/main11项实际Actions均completed/success，以实时main预期HEAD保护非强制快进。compare十文件=六新增/四只追加、历史删行0；十远端blob/整tree与本地一致，九启动原文前缀完整。候选源run39724361777/job119644784179/artifact12402935589，主线源run39724455796/job119645076819/artifact12403070177，各真实执行七单元、两HTML重取、17语义反例（比较去正文摘要）及两正例，均不是原商业运行。

两ZIP实际实下均1619B，SHA256 `8dcabcf0dafddaa738ede42e8ae7d3c9b6be333d50b050098e6bffd16fd7a03d` / `cf5c20a63c5d3952285ead4d89619c1083a820dd772cd6aa5e0a1dfed18ee3f7`；各唯一replay.json完整3136B/SHA256 `d7c30e3a817d34420724bf6b3b56dc08befed20df34e8a7b90cde102daa4495a`/Git blob `899800df88f2ddd8573f0d6311b63db1007b2b9c`，候选/main/local完整原字节相等。两源大小/摘要同初取，正文语义亦同；ZIP差异保留。独立正则/实体解码复核图名顺序、穀字、东侧与地底限定、自拾取、一次一只和正文署名一致，没取像素。

两CI原派生JSON及research/recovered/STONEAGE-JP2004-SEALED-REGION-CUSTODY-R1.json永久入Git，固定内容Git、21工作流、双job/artifact/ZIP及八文件原生Git/SHA/长度。新增收据必须存在、真实新派生文件缺失/等长篡改拒绝，单元七→八，保管提交自身候选/main CI必须另实查，不倒改旧七项。另26项旧7月来源/归档/连续性回归通过。原HTML/原图/音频/程序不入Git，史料≠原服、未名岛不乱并、放生/售款/删除/邮寄计时未知等边界未变。最高NEXT66优先具版号经典辅助工具能力新材料，缺新源选物品/配方/经济；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，历史全保留。


### 2026-10-22 R65并发主线续接与R66来源预检（R66未关闭）

本轮以main2a0583b启动；完成R65独立双ZIP/本地raw逐字节核对与独立词法复核后，发布候选 `2efdf25620dcd6109ebc69cc38b079eb97eb84f8`，十项适用Actions全部成功。合入前新读main发现已前进到 `117fc2a4ec749ca6bde8a353a1cfa7a750041775`（tree1c0a33681173c315d74f7948f73c69ab57a234da），其R65永久保管工作与本轮重合；因此没有把旧候选强写主线，保留该候选为已被主线同类工作取代的研究记录。已按最新主线干净worktree续接，保留该提交全部历史及既有verify_custody接口/收据字段。

实际增量仅为收据整组run唯一性、成功与内容HEAD一致、专用artifact到run/分支/HEAD归属，以及CI输入列表到源报告绑定；补一项反例测试，本包八→九，相关18项本地通过。初轮独立候选重复run反例暴露漏检，续接主线时误用了另一候选收据键导致两项KeyError，按最新main jobs_and_artifacts实际结构修正后才全部通过；均为本地过程，不改写为远端失败或原源变动。此增量候选/main CI另后验，不替换原七/八项历史。

R66已取得一篇新具名版号文献，预检见 research/recovered/STONEAGE-STA253-SPEAKER-SOURCE-HANDOFF-R1.json：17173 2002-03-27页面，当前HTTP200/UTF8严格/45844B/SHA256 de559d52986b8403c96b4657d6744af8f3f164b4611fddab661090532297fb4e。外层作者ZHY、附录暗夜之狼及附录内地藏乌拉引文分三发言层；仅一当前页面，不能计三个独立来源。具名Sta2.53的详细信息/可编辑料理脚本/原地遇敌与速度争议值得下一步有限结构化；当前仅保存选材线索与话语冲突，不决断谁正确、不补未知build、不认证原服或内挂采纳。未下载工具、原HTML/资源不入Git。

最高NEXT仍OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-66，预检不当R66验收或全部外挂完成。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停。所有旧历史完整保留。


## 2026-10-22 R66：STA2.53分发言功能档案与具名beta试用

本轮新读main5ec4ef2a75ef24e2655ff387d8da0d73489fdafc/tree7c6a049df39a5ae8224595e1c11073cd0a0d09ae，462分支/0开放PR/0运行中Actions，原HEAD main9/候选8项全SUCCESS，旧queued37642417333单列。九启动文件完整原字节/原生Git校验，CURRENT2321108B完整历史前缀保留，5087项完整树无AGENTS。按最高NEXT66交付docs/specs/STONEAGE-STA253-SPEAKER-SOURCE-R1.md、来源JSON和有限源重放工具；前次预检原样保留。

三当前HTML中S1与S3为新具名材料，S2仅已归档比较文复取；来源身份、字节摘要和S3畸形链接恢复过程均入派生记录。四类能力形成七条分发言主张；四段附录引文与S2对应段去空白后逐字一致，不增加独立支持数。未具版号外层/引文不借用2.53，具名beta标签不当二进制身份；来源冲突、性能评价、未试用料理、未知设置单位和崩溃原因保留，不决定内挂采用。详见分源规格；原HTML/软件/图片不进Git。

七项独立反例测试、14真实源改写去摘要门及三script正例、本包与旧档案16项本地回归通过；一次性正则/实体另核引文一致与beta限定。搜索阅读器S3打不开、畸形外壳404，与实际内层HTTPS200分别记录，不称历史不存在。候选/main当前网页重取、双ZIP下载及永久派生保管须实际后验，不提前报绿。

有限止点三页/四能力域/七主张和beta观察，不扩STA助手或全构建史。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-67回22域，优先具名物品/配方/经济或地图/NPC；Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING，全部旧历史不改删。


### 2026-10-22 R66双端实源重放验收及永久派生保管

内容提交5a9679dc853c122cd47f83d09615351031e3f9f3/treea4b0e0f4efc98d2fde907cca814e5fd57f329553，候选10/main11项适用Actions全部completed/success，实时main预期SHA保护非强制快进。十文件/整tree与本地一致，四历史文件仅追加，无旧行删除。专用候选run39726627024/job119651903336/artifact12403044614，主线run39726677904/job119652064762/artifact12403541734，均实际七单元、三当前HTTP、14去摘要门反例及三外围script正例，不是工具或原游戏执行。

实际双ZIP各1812B，SHA256 77e921ebf5d8da110ce5b47e9a626dcbcfb33430af2981b211fb6c148edd75b3 / 1c570c5b69d6ecee89812c20812453d71b545c01886db3d659adb6e9f7efd289分别匹配API；唯一replay.json完整4226B/SHA256 52c021152e77da75c752c5a3d7be8127cea4a2298aaf57be3fdb0ad5be4676bd，候选/main/local以及加保管门后本地重放逐字节相等，三输入大小/摘要同初取。完整两CI派生原JSON与research/recovered/STONEAGE-STA253-SPEAKER-CUSTODY-R1.json永久入Git，固定内容Git、21项实际run、双job/artifact/ZIP及七个永久文件原生Git身份。

新增强制保管门：收据/原派生实际缺失及等长篡改、重复run、错HEAD/分支拒绝；单元七→八，与旧档案17项本地回归通过。保管提交自身候选/main CI另行实查，不把旧七项称八项。原网页全文/HTML/图/工具不进Git；附录再引不增独立支持，beta表现与全部2.53同构建/稳定性未知等限制原样保留。最高NEXT67轮换22域的具名物品/配方/经济或地图/NPC，不继续扩STA内部helper；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部历史前缀完整。


## 2026-10-22 R67：料理效果、原料字串与平时／战斗场景

新读mainc84d7af570676d510a520f19b8f8ff1be00c014b/treeeae5686b404d704c3f48266386a54ee0d4541c4d，463分支/0开放PR/0运行中Actions，原HEAD main8/候选7项全SUCCESS，旧queued37642417333单列。九启动文件完整UTF8/原生Git核验，CURRENT2325668B历史前缀完整，5097项完整树无AGENTS。按最高NEXT67从预检进入两页四条具名料理文献记录，详docs/specs/STONEAGE-COOKING-EFFECT-SOURCE-R1.md与research/recovered/STONEAGE-COOKING-EFFECT-SOURCE-R1.json。

当前两HTML实际52549/44295B、严格GB18030，SHA完整保管；可见2003-04-02两刊时与2006整页/2003模块/2015导航注记分开。四行是三具名料理加同名对照，不当四个原游戏实体；行内使用备注不能被PK分类标题覆盖，同名效果字面差别不当原服数值矛盾，原料尾数不猜数量或等级。作者、精确build、原ID和配方执行未证；旧2.0宠物加工/回复法术仅版本化父证据，不倒灌字段。原HTML/图片不入Git。

七项反例测试与12真实源语义改写无摘要门、两外围script正例本地通过；一次性独立正则/实体复核四原单元格。本包与旧档案/组合队列17项相关回归先通过，再加强可见标题归属及负边界不得缺失的检查，本包七项重验通过；无相应远端失败。源候选/main网页重取、ZIP实下和永久派生保管须真实后验，不先报绿。

有限止点两页四行，不扫余下食谱或扩料理helper。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-68回22域，优先具名地图/NPC/任务或有同版实参的音效材料；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING，完整历史保留。


### 2026-10-22 R67双端实源重放与永久派生保管

内容提交e4d05c0016961d5471914db58c2b45b71e274d77/tree05e6d78045b20b6a326b4c5297ddfdd5f810b9a3，候选10/main11项适用Actions全部completed/success，实时main预期SHA保护非强制快进。十文件/整tree与本地一致，四历史文件仅追加，旧行删0。专用候选run39729369175/job119660632222/artifact12404124612，主线run39729448409/job119660886022/artifact12404158041，各实际执行八单元、两当前HTML、12语义反例及两外围script正例；非原商业运行。

实下双ZIP各1643B，SHA256 31f254808efb16370c9dad9c96417d23e5090365c8c4a6744a54932b0a666593 / 73782e55e24be87c8a07f2ba6c2da8a0eb22ce10726367faff99807f10c92d77逐一符合API；各唯一replay.json完整9141B/SHA256 e335e8cc3eae2796dc43bc60fff7c62e05021d67ac2bbd6a00bb9547facc40e7。候选/main/local及加保管门后本地重放四份原字节全等，包含四条原文献记录与四条recipes研究目录；两HTTP摘要仍同初取。

两CI派生原JSON与research/recovered/STONEAGE-COOKING-EFFECT-CUSTODY-R1.json永久入Git，固定内容Git、21真实run、双job/artifact/ZIP与七文件原字节/原生Git。保管门强制收据存在，拒绝实际文件缺失/等长篡改、重复run、错HEAD或分支，并绑定输入、语义、目录及原始来源边界；单元八→九，本包与旧档案19项本地回归通过。保管提交自身候选/main CI另须实查，旧八项不倒改。原HTML/图/程序不进Git；精确build/原ID/原料后缀与实际效果均继续未证。有限包止于两页四行，不扩全食谱。最高NEXT68回22域优先地图/NPC/任务或有同版实参的音效；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部历史完整。


## 2026-10-22 R68：梦幻洞窟的昼夜入口、供物与重复奖励

启动新核main22b987d4b25c026d6ffc7f74437c67c2fed76ed3/tree0baa3b8f5da486e795c26e8486eb3d3e204c1d42，464分支、0开放PR、0运行中Actions，原HEAD main9/候选8项SUCCESS；历史queued37642417333单列。九启动全文UTF8/git show一致，CURRENT2329498B完整历史保留，5106项树未截断且无AGENTS。按最高NEXT68从全22域选择一条具名任务，不重复计已归档成人仪式或泪之石。

新取2003-05-30 13:51新浪《任务功略-梦幻洞窟》，当前HTTP200/49845B/SHA256 2044ba7f8346bba7e043a6601fd9e00fe664c527109bb41e0ddea5b8de57fec9，严格GB18030无替换。网友投稿非官方脚本；2006页首再发布与2003可见刊时、2026字节分别记录。搜索阅读器Unicode错误不等于原HTTP失败。详docs/specs/STONEAGE-CN2003-DREAM-CAVE-SOURCE-R1.md及research/recovered/STONEAGE-CN2003-DREAM-CAVE-SOURCE-R1.json。

保留成人完成仅为具名奖励资格，推荐60非准入硬值；三档装备属性/精灵与第4次后随机、非成人随机分支；先见之光丢地/注销消失与可补领，不推断线或无限补领。昼夜入口明确，村名后三坐标未解，两去回路线表未标昼夜，不能依表序猜配；七怪物标签含人类，不称七物种。村民威胁视角和仙人伙伴解释、年度供物及航空传说分层，未证原服或永久世界变化。原ID/build/随机池/计数存档未知，原HTML/图/程序不入Git。

本包有限解析、五单元、16真实源去摘要门改写及script正例；具体远端候选/main重取与ZIP/永久派生保管须后验，不预告成功。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-69回22域其他地区地图生态/人物或有同版实参的音效；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，旧历史不改删。

本地首次相关回归误写模块名导致ImportError，改用真实tests.test_stoneage_preproduction_archive后19项通过；独立词法复核初将非路线图片表计入，按含路径字段筛选后通过。解析器新增路线成对表结构时先误纳外层父表，实源拒绝后修为只取叶表，五单元与16实源反例重验通过。这些为本地修正，未伪记远端失败或来源改动。


### 2026-10-22 R68双端实源重放验收及永久派生保管

内容提交17c9d9a231ce4eef12daed44881cbff4b2c58db0/tree41ccd755ae0c52ea1c8b75ec7669cf205a7cb585，候选10/main11项适用Actions实际completed/success；实时main预期HEAD保护非强制快进。十文件/整tree与本地一致，四历史文档只追加，旧行删除0。专用候选run39761395749/job119766175945/artifact12417249986，主线run39761469475/job119766416879/artifact12417668351，分别真实执行五单元、当前HTML重取及16实源语义改写/script正例，非原游戏运行。

实下双ZIP均2669B，SHA256 81770b559cfaff84507c6f541a52bca0e69d9f2625525177bc1c36269291a772 / fc0ac725d2de76fab1bfd55a8e792476ffceb72305fb3b45cdf0c0ccb44370ae逐一符合API；各唯一replay.json完整11446B/SHA256 1ca6e1dfcc4ac24f1303d90c2a26f6fc32a7efbd2c1a2574290c68c795560222/Git blob180ad0e60bfab78acd33513ff6ad8a09c6048428。两CI/local/新增保管门后local四份逐字节相同，原HTTP摘要同初取。独立正则/实体复核三奖励属性与精灵、两入口及两路线表，确认无昼夜标签。

双原派生JSON与research/recovered/STONEAGE-CN2003-DREAM-CAVE-CUSTODY-R1.json永久入Git，固定内容Git、21实际run、双job/artifact/ZIP和五永久文件原字节/Git身份。强制保管门拒绝文件缺失/等长篡改、错HEAD/分支、重复run/job和历史字节认证晋升；本包五→六单元，与旧档案/组合队列共20项本地通过。保管提交自身候选/main CI仍需真实后验，不把旧五单元倒称六项。原HTML/图/程序不进Git，资格/路线/坐标/原ID/build边界保留。

最高NEXT69回全22域其他地区具名地图生态/人物关系或有同版实参音效；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，旧历史全文保留。


## 2026-10-22 R69：日服寻宝NPC、两阶段收集与可转交活动物

新核mainc8b13ee1980b52d9e8544c3ed529654309d9715f/treec0d7442939ac75650210c21fb8c246bec99710af，465分支、0开放PR、0运行中Actions，原HEAD main9/候选8项SUCCESS；旧queued37642417333为无关历史。九启动文件完整UTF8/git show原字节一致，CURRENT2333600B历史完整；5115项递归树无AGENTS。按NEXT69回日本具名NPC委托，不重复旧地图/章节资料。

新取4Gamer 2005/09/06 17:23《限定アイテムが入手できるイベント》，HTTP200/19613B/SHA256 70ac6ac9dec4895f67a5d6dc2d83be9a65377acd7698338dbf3600d93c29075b，严格CP932。媒体GaiaX归属/TeT导语、可见FONT运营发布文分别提取；星期金/火异文保留，不借页脚免费模式回填2005。实际原出链event_020.html的单次精确档案查询429，原页未得，不称全档案不存在。同文迁移页未算新独立见证。

交付docs/specs/STONEAGE-JP2005-TREASURE-EVENT-SOURCE-R1.md及SOURCE JSON：サムギルの村光の精霊の使徒委托、两维护窗口、3+2共5种、部分区域低概率掉落、第二阶段收齐全种类兑奖、收集物玩家转交/买卖与可重复。五种不当五件、转交不推广奖品、不补先接任务才掉或每日重置；原ID/build/数量/概率/奖池/断线与最终持久化仍未知。旧2008协力父报告仅做分版机制比较：种类数非交付量、阈值非个人费用、不合并精灵物/NPC或编历史演化。

有限解析/七单元、18真实源去摘要门改写与script正例、本包与旧档案21项相关回归；独立词法核两窗口/份额/具名人和交换/转交。原HTML/图/程序不入Git，候选/main实取与ZIP/永久保管必须另实查，不预报绿。止于一新页、两研究目录和一个限定比较；最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-70回22域宠物/技能/骑乘或同版音效事件。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，旧全文不改删。


### R69来源层资格补正（首次候选后、主线整合前）

人工复核发现任务研究目录同时含媒体给出的活动名/运营归属与刊文末段不确定性，故其source_refs必须同时指S1-RELEASE与S1-EDITORIAL，NPC条目仍只指发布文；源层正式声明父页面S1，防止子来源标签悬空。真实结构化语义未改，须对补正后的候选重新验收。规格初版“六条阈值”是文字计数错误：实际父档案与JSON均为八条（大树五、地方三），本补正取代该句，不改既有2008历史或数值。首次候选的检查不能代替补正提交的检查。


### 2026-10-22 R69合格来源层双端重放及永久保管

最终内容提交acf3fda07761778b22519d41f51fe2ee6bf28b09/tree96985348230d2934585fc4dc76195afd3e770b9c，候选8/main11项适用Actions实际completed/success；实时main预期HEAD非强制快进。初次候选a69b2eb72c11e4b34dfb712a49803ca505bc5bbf的10项成功单独保留，不代替来源层补正后的验收。四连续性文档旧行删除0，完整Git tree及blob与本地吻合；新增资格不是游戏规则变化。

专用候选run39763769475/job119774054126/artifact12419063020，主线run39763847201/job119774310379/artifact12418684089，各真实七单元、当前HTML、18去摘要门语义改写/script正例。实下双ZIP3125B，SHA256 9034ddd04a91fad382a519d2e89ef0a9d365ba75a0f071e048dfb6824a89d1aa / 5b6d9b2759e54c46376517c91c136f984447d3270a74002efb2f4e74948f6830逐一匹配API；各唯一replay.json完整12816B/SHA256 c18bcce46dfaf541e80a705053164f891ea07604e83178c623cbce9d84e0be94/Git blob0474f35cb4f35d450456f878fca3a889bcb1dd4a。双CI/local及加保管门后local四份逐字节相同，输入SHA与初取同。

双原派生JSON和research/recovered/STONEAGE-JP2005-TREASURE-EVENT-CUSTODY-R1.json永久入Git，固定合格内容Git、19实际run、初候选10run、双job/artifact/ZIP及五永久文件原字节/Git身份。新保管门必须存在，拒绝实际文件缺失/等长篡改、错HEAD/分支、重复run/job、历史字节认证晋升和派生比较错配；本包七→八单元，相关本地回归22项成功。保管提交自身候选/main CI须另真实后验，旧七单元不倒称八。原HTML/图/程序不入Git，429不反复请求或否定历史。

星期异文、种类/件数、收集物/奖品的流转范围、两个年份活动非继承关系均保留。最高NEXT70回全22域宠物/技能/骑乘或可归属原音效事件；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部历史保留。


## 2026-10-22 R70：特殊宠技资格、捐献状态与回合落马限制

启动新核main67353924c46d2fa1073a009c7f2fe05f8c47907f/treec82fbbed89a459e659552359386ef745f809ebcf，466分支/0开放PR/0运行中Actions，原HEAD main9/候选8项SUCCESS；旧queued37642417333单列。九启动完整UTF8/git show一致，CURRENT2338194B历史全文保留，5124项树未截断且无AGENTS。按NEXT70选择宠物技能/骑乘，旧R56表格不重复计新来源或擦除冲突。

两新当前HTML：3.0新增要素专题S1之#3/#5、2003-05-01 06:52黄建枝征文S2的技能转引段，HTTP200/42680与50384B，SHA完整入research/recovered/STONEAGE-CN30-SPECIAL-PET-SKILLS-SOURCE-R1.json。严格GB18030无替换；S1首刊/作者未知、导航5.0不改正文3.0，S2作者从5.0开始且引未具名杂志，2006再发布/2003刊时/2026字节分开。原杂志/官方原配置未得。S1定年精确档案一次请求结果见dating_attempt，非全局缺档，不由检索点赋刊期。

交付docs/specs/STONEAGE-CN30-SPECIAL-PET-SKILLS-SOURCE-R1.md：两组各七原名、T类别/机暴与非T捐献/扑满乌力资格、S1两层坐标/非族员进入与S2只内层坐标；末项背水原名差和全半角保留。捐献80仅举例，使用后等待→调回战斗→下一回合，队友目标仍听说。GP落马限制原坐骑至回合结束，不扩为永久/全部宠，次数无限不当零成本或必中。机暴驾驭含义、金乌力交易等级方向、费用/原ID/build/公式/状态enum全保留未知。相似文字不增加独立支持，也不确立抄袭谱系。原HTML/图/杂志全文/程序不入Git。

六单元、21实源去摘要门改写与两script正例、本包及旧档案20项相关本地通过；独立词法另核14原标签/末项异文/两层坐标和状态时序。15研究目录=14技能文献+1骑乘文献，不是15恢复实体。候选/main真实网页重取、ZIP实下及永久保管须另后验，不预报绿。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-71回22域另一地图/NPC/生态或同版音效事件；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部旧历史保留。


### R70精确历史捕获补证：2003-03-24（同包出版前）

上文定年查询返回HTTP200及精确可用捕获，并非空集或限流；随后真实取得 https://web.archive.org/web/20030324221124id_/http://games.sina.com.cn:80/zhuanqu/stoneage3/yaosu.shtml ，无跳转、HTTP200、21853B/SHA256 3a270f86e42cc6e7f68a8e2dd0c765097b442b1dd2d9c4eadeec091d3222059e，严格GB18030。此S3为S1的历史参考，不计第三独立规则见证；2003-03-24是捕获时刻，首刊、官方作者、商业build仍未知，当前原HTML字节不等于旧捕获。该补证取代上文“未得历史正文”的阶段性状态。

S1/S3两个所选节的完整可见文本去空白后逐字相等，#3核心UTF8/摘要与#5核心UTF8/摘要固定在historical_comparison；提取的技能/资格/状态/坐标亦全等。重放新增S3实取，输入总计三个HTML；不重查Availability、不递归截图。七单元、23实源改写和三外围script正例，本包与旧档案21本地检查通过；旧六/21改写/两script的早先结果不倒改。15目录不增实体，S1技能/骑乘记录同时指S1/S3，S2仍只指具名玩家转引。原HTML/图/杂志全文不入Git。


### 2026-10-22 R70三输入双端重放验收与永久派生保管

内容提交b97bccff947c571851db1f9997d76831dc02813a/treed4048b9cf5a41423880f5e7cdcf92bb77031737e，候选10/main11项适用Actions实际completed/success；实时main预期SHA非强制快进。十文件/整tree远端与本地原生Git吻合，四连续性文档仅追加；初始两现页阶段及同包历史补证均保留，不把查询点当捕获日期。

专用候选run39766482469/job119783089446/artifact12419564808，主线run39766563402/job119783360423/artifact12419764140，各实际七单元、两当前HTML和精确20030324221124历史HTML、23去摘要门语义改写及三script正例。实下两ZIP各2912B，SHA256 2bf444b9290b0699ce4c7d7261713e3c00a547f0d574e88c2e3cd1df95e455f3 / ec0c1354c2f92f470cbb2cc97c1696c0ecf9d4bec0d60c07159051d0c6c87bbe逐一符合API；唯一replay.json完整23318B/SHA256 637702fd6eed2b37c6cbece438bc537f55369859b9ff46cdfabb8f94afdd83c6/Git blob8a0fc18068196ff20af9022d237d3a8e8100640c。双CI/local及新增保管门后local四份逐字节全等，三输入摘要同初取。

S1/S3所选全文去空白一致，#3核心712UTF8B/SHA256 810507b9e173d90951e20c68fc563adc208017fcdf05d547b5cbdc41bcca6195，#5核心2493UTF8B/SHA256 7798e1c46150e83a180098fe15c61c4c5c46275fb643a6ce6e61f8b444dbf54a；独立词法另验248/839字符和全文相等，S1当前原字节仍不等于S3历史原字节，未认证同客户端build、原作者或首刊。S2未名杂志、5.0起玩及传闻限定未变。

双原CI JSON与research/recovered/STONEAGE-CN30-SPECIAL-PET-SKILLS-CUSTODY-R1.json永久入Git，固定内容Git、21真实run、双job/artifact/ZIP、明确历史参考捕获及六永久文件原字节/Git身份。保管门强制存在，拒绝缺失/等长篡改、重复run/job、错HEAD/分支、当前网页冒充历史字节及重放错配；本包七→八单元，相关本地22项通过。保管提交自身候选/main CI须另实际后验，不倒称旧七项为八。原HTML/图/杂志/程序不入Git。

最高NEXT71回22域另一具名地图/NPC/生态或同版音效事件，不扩本技能helper；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部旧历史保留。


## 2026-10-22 R71：五兄弟答题、条件通行与成对奖励

新核远端默认main44726d49ed577bcb67ccbf8a0dd7ad5a99eb8b49/tree04dcb80460797a1dc5576fde9bb9d36fd159cd78，467分支/0开放PR/0运行中Actions，原HEAD候选8/main9项SUCCESS；旧queued37642417333单列。启动全文UTF8/git show与原生Git一致，CURRENT2343759B历史完整，5133项完整树无AGENTS。最新NEXT71及22域组合队列新读，选world_map/npc_identity/quest_content并补items/pets归属，不继续技能helper。

新取得新浪2003-06-02 14:22《五兄弟之谜》当前57507B/SHA256 698e278925115ce38b98faa61a3d5f3d9d236dd9076980a4d6be5725a34acc35，以及单次Availability实回20031204051508精确历史捕获40631B/SHA256 fa70ad0d654660d0f90d44c59f68c2b6aa3a7353ef980906a4a6075acd72425f。均HTTP200无跳转/GB18030严格；当前td.l15z与历史span.l15z的整篇可见正文去空白相等，2463字符/6833UTF8B/SHA256 5b8733fd860bc4971255dbbed75c4a52a8d221c74efc4d5cba390ae566b6c9b1。捕获不是首刊或商业build，两个包装只计一来源；当前字节不认证成旧字节。作者栏新浪游戏/官方页脚不当官方原稿认证；原HTML/图不入Git。

交付docs/specs/STONEAGE-CN2003-FIVE-BROTHERS-SOURCE-R1.md及SOURCE JSON：五层题板/答案纸与答案键、五正确纸→蓝人龙两次谈话→秘宝检查通行、地下6层返程/挑战/兑奖点；五颜色明确选择的饰品+一级人龙对，不随机、不一次全领。青/蓝及火风/风火不归一，未注精灵等级不补1。五空道具/一空宠栏为建议，转生后可重做不推终生次数/flag复原。浦鲁德/布鲁德/浦洛斯等按原出现位置保留；两地图生态四加四标签不是完整物种或可捕主表，坐标帧/概率/原ID未知。13研究目录=1任务+5饰品+5一级奖励宠物+2生态地图，不当13恢复实体。

固定旧早期指南与19集合合同；旧文组队入场/注销消失记录不删，本页只明确不能预组队战斗但可战斗中HELP，水晶用“离开这个世界”而非直接注销，掉线与具体销毁位未知。不借相似文字认证同构建/独立见证/同ID。五单元、每输入25去摘要门真实源改写及script正例，本包/旧指南/组合合同24项本地回归通过。独立正则/实体另核全篇相等、五答案/五奖励对；其初版错误假定当前span有结束标签、随后泛化剥标签吞掉颜文字的<，改为按center外界与合法字母标签分隔后与HTMLParser全等。一次性插入脚本初误计两个h赋值位置已在写入前中止并限定首处；没有远端失败或来源改动。

候选/main当前及历史实取、ZIP实下与永久派生保管须实际后验，不预报绿。有限止点一文两包装，不扩全转生/人龙helper；最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-72回22域另一地区具名宠物/模型或物品/经济，音效只凭同版实际调用输入。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部历史原样保留。


### 2026-10-22 R71双包装双端实源验收与永久派生保管

内容提交ab7d54b056d68a2b17e6720b9fd030964470454e/tree6ecc091dd461443bec263a7956b321faddb4156d，候选10/main11项适用Actions实际completed/success；实时main预期SHA保护非强制快进。十文件及整tree与本地原生Git吻合，四连续性文档旧行删除0；首次源验收的五单元历史不倒改。专用候选run39768977232/job119791426926/artifact12420074995，主线run39769093934/job119791819856/artifact12421068332，实际五单元、当前/20031204051508历史两HTML、各25去摘要门语义改写/script正例。

实下双ZIP各4108B，SHA256 7e34113ba0f664f3e55924df2d8536a7944fb4c68039c433a6cd3b0afc92f64d / bbc0c6a02e0dc8ac9a47c5b52759f9c89266b3a0836faffe86297c4ae3ec1f36逐一匹配API；各唯一replay.json完整29401B/SHA256 5cbb83cc283c8303683d52642a6807090617912f772d16f49efe0e1abb80e1c8/Git blob5ccdb6e856362ef0641138eb3574ea236d435478。双CI/local/新增保管门后local四份逐字节全等，两个输入大小/SHA仍同初取。

双原派生JSON及research/recovered/STONEAGE-CN2003-FIVE-BROTHERS-CUSTODY-R1.json永久入Git，固定内容Git、21实际run、双job/artifact/ZIP、历史捕获与五永久文件原字节/Git身份。强制保管门拒绝文件缺失/等长篡改、重复run/job、错HEAD/分支、当前字节冒充历史及语义重放错配；本包五→六单元，相关回归25项本地通过。未知项反例先重建目录，确保不能只靠目录与提取不等而误称边界检查生效。保管提交自身候选/main CI另需实查，不借内容提交五单元绿灯称六项。

五题提示原文、原NPC/道具/地图/宠物ID、商业脚本、HELP具体参数和重复/消失实际存档未得。原HTML/图/程序不进Git，历史包装与现代包装不计独立见证，谱系/名字关系不合并。最高NEXT72回22域另一地区具名宠物/模型或物品/经济；音效只凭同版实际调用输入；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，所有旧历史完整。


## 2026-10-22 R72：コクエン状态展示、黑炎袋与分层兑换

启动新读默认main d9919555940882d24182b26d12a2568e085a7e88/treeff05bf10a5135f1682c30c5ebf4f705848e7bb92，468分支、0开放PR/运行中Actions，原HEAD候选8/main9项SUCCESS；旧queued37642417333单列。九启动来源完整UTF8/git show/原生Git核对，CURRENT2348851B历史保留，5142项完整树无AGENTS。按最新NEXT72/22域回日本具名宠物视觉/状态与物品经济、NPC，不扩五兄弟helper。

新增4Gamer2009/06/29 16:55署归DigiPark并标原样刊厂商文的当前HTML277194B/SHA256 cda0c2ce2d4389ed89107feeef40f58a2470341a01fce800f9cf4eafc23f6cf5，HTTP200/UTF8严格。只取コクエン详节，919字符核心SHA256 d6ef38d7c57410b13298d2f29a013a2d6213f3b0e354b0a6a0f946af6655b0d0；目录不是第二来源，相邻改版/博彩/EXP不在本包。销售2009-06-23维护后至07-21维护前、站点改版06-25、文章06-29分别，不认证2009原站字节或实际部署/build。

原onclick全尺寸001.jpg实取68476B/SHA256 2949b7719977756fe0789b25f687122ba1b9c0381979bd8bf95e606f7bca59a0，JPEG/RGB270×363，完整Pillow解码/目视；人工转录コクエンLv1、EXP0/NEXT2、HP72/72、攻18防19敏15忠诚0，明确绑定精确JPEG且非OCR。正文随机警告限制为展示样本，不当物种初值/成长公式；元素色条不猜数值，原模型/SPR/动画/UI交互未恢复。原HTML/JPEG/程序不进Git。

规格docs/specs/STONEAGE-JP2009-KOKUEN-SOURCE-R1.md及SOURCE JSON记录400Gstone直接袋价、随机1道具/6类；三类混合总10→甲票，3/1/6仅例，5甲票→重抽票、5重抽票→宠物票。CP交換所黒炎系交換員具名无坐标/ID；生成的耐久/气力回复物注销/丢弃消失，不扩大外袋/药/票/宠物。变身主体/时长/属性、重抽保留字段/分布、获宠票数/等级与消费实际执行未知，不推保证抽数或期望花费。9目录=1宠物文献+1NPC+7道具，不当9恢复实体。

固定旧白炎父报告与19集合合同；ハクエン与コクエン不合ID/进化谱，旧7类声明对6具名行异文不被黑炎6类补齐。白炎400买票、黑炎400买袋不混。六单元/18真实HTML去摘要门语义改写、外围script与未选活动正例，本包/旧白炎/组合合同28项本地回归通过；独立词法核919核心、三处10合计、两5票边、两生成物消失说明及原图实参。一次合成图末字节篡改使解码先报OSError而非测试预设ValueError，改用可解码的等长尾随TESTA/TESTB后确证摘要门拒绝，旧本地失败不倒记成功，无远端失败。

候选/main实取、ZIP实下与永久派生保管须实际后验，不预报绿。止于一发布详节/一图/六类/三兑换边；最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-73回22域另一地区具名NPC/剧情/交通或人物界面，音效仍需同版实参，不扩商城helper。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部旧历史完整。


### 2026-10-22 R72双端实源验收、不同整页取证与永久派生保管

内容提交6f434cf519b0e76aaa2ede3c2ceb51ea5b3b637f/tree6d0303abe02843d5f135425f250cba4ee4face47，候选10/main11项适用Actions实际completed/success；实时main预期SHA非强制快进。十文件/整tree与本地原生Git吻合，四连续性文档旧行删除0。专用候选run39771318971/job119799288844/artifact12422213142，主线run39771422647/job119799632302/artifact12422427180，实际六单元、HTML+原图实取、18去摘要门语义改写及外围/相邻活动正例，Pillow12.3.0完整解码。

两CI各整页HTML276942B/SHA256 068a3897a620edb0591ca2945f021c8a3de1f2f423fb81b2cb827a4a152258f3，与初取277194B/cda0c2ce2d4389ed89107feeef40f58a2470341a01fce800f9cf4eafc23f6cf5不同；所选919字符核心/抽取字段/精确JPEG/样本转录/目录/反例结果均相同。两CI原JSON逐字节相等，但不能称等于初取local。保留各自原始inputs，不删字段或规范化改写来假造原字节全等；加入保管门后local仍逐字节等于门前初取local。

实下双ZIP各2665B，SHA256 7aa7eba4710c87a9bcbc820acc594d27da8787e0d358b1a1942a399cb7f85a59 / 9fc6a362c218552cf96584950081f09de5a3cf8bd3310d24af9905971fd9b2e4逐一匹配API；唯一replay.json完整12859B/SHA256 cb40620d16d3ac61e87317d9e141ab7aee5c4b400e6c318dc98b55f013d371f4/Git blob1d85db17802d7705b9b508d5d815f7ba3708b200。原图始终68476B/2949b7719977756fe0789b25f687122ba1b9c0381979bd8bf95e606f7bca59a0；没有将HTML波动扩大成图片或所选规则变化。

双CI原JSON与research/recovered/STONEAGE-JP2009-KOKUEN-CUSTODY-R1.json永久入Git，固定内容Git、21实际run、双job/artifact/ZIP、每次原inputs/raw摘要及五永久文件原生Git身份。强制保管门拒绝缺失/等长篡改、错HEAD/分支、重复run/job、图/输入错配、丢失初取历史、把差异写成原字节相等或冒充2009历史字节；六→七单元，相关29项本地通过。保管提交自身候选/main CI需另真实后验，旧六项不倒改。

原ID、精确build/原站快照、固定物种初值、图片模型/动画关联、概率/保留字段/时长/消费/实际保存仍未知；原HTML/JPEG/程序不进Git。止于具名发布详节和一图，不扩商城helper；最高NEXT73回22域另一地区NPC/剧情/交通或人物界面；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部旧历史保留。


## 2026-10-22 R73：琉璃洞窟的父子寻母、女神宿身与主支任务

启动远端默认main7244942f08d3c2a1cc8a0cf7e351bba589629f07/tree3c5a47c1c06c10451ee78424f77186e24b25be0f，469分支/0开放PR/0运行中Actions，原HEAD候选8/main9项SUCCESS；旧queued37642417333单列。九启动来源完整UTF8/git show/原生Git核对，CURRENT2354305B历史保留，5151项树未截断且无AGENTS。新读最高NEXT73及22域索引，回大陆具名NPC/剧情/任务/地图，不扩黑炎商城helper。

新增新浪2003-06-06 14:55《琉璃洞窟》当前55319B/SHA256 e3ec609550d745c6917349d28bf243a91ed979340453c1bf23d009b8640c58ef；单次Availability实际返回并取得20031204051540历史HTML38444B/SHA256 104821fed0069da91a0188eef6f551756c2b14c737df415c42322d469cf08350。两HTTP200无跳转/GB18030严格；整篇可见正文去空白1997字符/5485UTF8B/SHA256 a5ba592e619b77b726bbb89ab0c81531b95c583691866bbaf5ebc7992c067d41完全相等。捕获不当首刊，当前12-25/历史07-02包装注记与06-06刊时分开；作者栏新浪游戏不认证官方原稿/build。两包装只计一来源，原HTML/图/程序不进Git。

交付docs/specs/STONEAGE-CN2003-LIULI-CAVE-SOURCE-R1.md与SOURCE JSON。主线父亲先前说母亲去世、儿子带日记离家、母亲为女神宿身及等待未来探访分层，父子/母子/配偶/宿身/等待五关系入任务研究目录；不报已重聚。14年前为日记时间非儿子年龄，50年为故事宿身周期非现实轮换timer，也不擅改成每母第一胎。主线推荐80未知硬级，第二支要求栏65/建议80，皆列成人条件；主线转生/后洞前提与可选支线无关转生分开，旧梦幻洞窟成人仅具名奖励资格不被覆盖或统一原flag。

五NPC出现、四道具、两支任务和一地图生态合12研究目录，不当12个恢复原实体。伊布8坐标不当8实例，村后双坐标帧未知；守卫9/14层等级以上字面、11→12有限出口不当全几何。项链/日记仅掉地立即消失，不补注销/掉线；项链回避率上升+2不补百分单位，大地的羁绊尾注“制服大地的证据”原字保留不造精灵。第二支50几级目标不猜精确等级，选大袋或小袋/随机，洗涤石图注仅示例，羽毛消费/奖池未知。九怪标签不是完整可捕物种表。

五单元、每输入23实源去摘要门语义改写/script正例；本包/复用正文解析器/旧梦幻/19集合合同29项本地通过。独立正则/实体另核两篇1997核心、双成人要求/建议80、14与50及奖励原字，不能把合成值当历史恢复。解析器只复用既有td/span有界实现并固定原字节/Git身份，不另扩helper。候选/main实取、实际ZIP及永久派生保管须后验，不预报绿。

止于一文两包装/两分支，不扩全四洞窟/转生helper。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-74回全22域另一地区人物/交互界面或交通生活服务，音效仍需同版实参。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部旧历史完整。


### 2026-10-22 R73双端实源重放验收与永久派生保管

内容提交8ff5eddaf5eecb5ab809fe5d8573ac9dc39181e3/tree4c052658257b34fb16972c76a92ca6b739526000，候选10/main11项适用Actions实际completed/success，实时main预期SHA保护非强制快进。初次状态查询时九项queued、一项成功，随后实际完成全部10项才整合，未把排队当成功。十文件/整tree与本地原生Git一致，四连续性文档旧行删除0。专用候选run39775472279/job119813181782/artifact12424417265，主线run39775728979/job119814053556/artifact12424750608，各真实五单元、当前/20031204051540历史两HTML、各23实源去摘要门语义改写及script正例。

实下双ZIP各3604B，SHA256 10cdfeefb06d29a62780182c3c5da1af37347c378c75cf210469788b38891a25 / cd9ccbaa3ba7bd47005a2b60280cd4f079e125dc9dad5b78e046bcf05b1a01a7逐一符合API；各唯一replay.json完整19798B/SHA256 b152d3260f31fc666ce08c301958cf4e8d93e5fba002e8e0f5b76b571addf992/Git blobd9e9768ef78c97890b98b31dd5e366cc3233ab87。双CI/local/加入保管门后local四份逐字节全等，两HTML摘要仍同初取。独立词法全篇1997字符/5485UTF8B再次与历史参考一致，不把捕获当首刊。

双原CI JSON与research/recovered/STONEAGE-CN2003-LIULI-CAVE-CUSTODY-R1.json永久入Git，固定内容Git、21实际run、双job/artifact/ZIP、历史参考与六永久文件原字节/原生Git身份，包含复用解析器。强制保管门拒绝缺失/等长篡改、错HEAD/分支、重复run/job、当代字节冒充历史及语义错配；本包五→六单元，相关30项本地回归通过。保管提交自身候选/main CI须另实查，旧五项不倒称六项。

补核支线目标鲁尼帖斯不在附表九怪标签中，保留各自范围，不擅加第十项、认定同一敌人或称附表完整。母亲宿身关系仍不并原NPC ID，家庭重聚/原服消费/奖池/任务保存未证。原HTML/图/程序不进Git；最高NEXT74回22域另一地区人物/交互界面或交通生活服务，不扩四洞窟helper。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，旧全文保留。


## 2026-10-22 R74：日本市场场地、官方活动与玩家公告申请

启动远端默认maincf43ddb9882102c3c05028833ee48fff5a67a0b9/treefa70becd395e88fc94e8dc1ff889a0777bf007fe；470分支、0开放PR/运行中Actions、原HEAD候选8/main9项成功，旧queued37642417333单列。九启动来源完整原字节/Git核对，CURRENT2359520B历史保留，5160项完整树无AGENTS。新读NEXT74/22域索引，回日本社交场地/生活服务，不扩琉璃洞窟helper。

新增4Gamer2005/06/03 19:15 Seirou文18498B/SHA2564ce485c6f7f64b9c88f3bdac393aa685304de55b6018283d4a7e7d25c00d07da与2005/10/21 15:07 aueki文18275B/8bdb842ff493e7b2a55a8c1679c2105b7c4ef0f6e42ad3fd0478ea34b2c4d78c，均正文点名GaiaX、HTTP200无跳转/严格CP932。属同期媒体报道而非原样官方稿/原页；2026字节不认证2005历史，现代页脚免费字段不回填。正文核心316字符/896UTF8B/6ffcc7a5a93b44fd325dc8d4772620bfdb19b7852ebfa0e3053b7eccb668b54d与485字符/1323UTF8B/afe342fa9db80f015a9b5d71f55c34ecfb7067471e6d5c5f3de15829fd881eaa独立词法复核。

交付docs/specs/STONEAGE-JP2005-FLEA-MARKET-SOURCE-R1.md与SOURCE JSON。水星服务器聊天地图6月14日改装预告、ニースフリーマーケット6月18日18–20时与第2回11月19日18–22时、GM当天巡场聊天合照建议、玩家相互物品/宠物交易分层。S2六月举办且受欢迎仅媒体回述，不冒充原服验收；两活动窗口不是永久场地开放时间。

玩家活动每月两次官网公告服务，本次申请10月20–25日、适用自办活动11月1–15日、计划10月28日刊登分开。付费AND(经营粉丝站OR Blog)只约束公告申请人，不外推市场入场/全玩家办活动权限，也不要求两站同时具备；不补保证录用或每14天固定周期。自由买卖不证免税/离线摆摊/拍卖/自动结算。地图ID/坐标/几何/交易UI/收费/币种/精确build/执行保存未知。

从两文实际a链接取得三big.html再IMG原JPEG，全HTTP200/Pillow完整解码/目视；72711B720×982/26f7e4d4c9e0065e086cd280573179e63e4befd931a6c19891a627ad700151e7、30525B283×567/51ab163d6d190a11e60b2073fe30e80895aaa199c8e5bd450353b28ed6c33a73、128375B648×948/be45d403b623fd69b3810bc646489aaf6e117014c9f8fd83e6a8e851e56c89ce。全为人物插画非地图/交易屏；相似金发构图不当第二场景、具名角色/宠物模型或动画。临时采集ID MAP/VIEW已显式否定为内容分类。原HTML/JPEG不入Git。

固定JSS2001公共聊天房、大陆2011–12摆摊及19集合合同三父报告和共享可见正文解析器；不合地图ID或把晚期摆摊UI回填。3目录=1maps文献场地+2tutorials活动/公告描述，不当恢复实体数。六单元、17实源去摘要门语义改写及每文外围script正例，本包/复用模块14项本地通过。初次泛h5选中菜单、合同测试漏嵌套键的本地错误已修正重跑，不倒记成功；无远端失败。候选/main实际CI及ZIP永久保管须后验。

止于两报道三插画链，不扩全交易系统；重新打开需同版原站规则/投稿页、实际入口地图/交易屏或原ID。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-75回全22域另一地区人物创建/角色外观或交通服务具名材料，音效仅同版实际调用输入。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部旧历史完整。


### 2026-10-22 R74双端实源验收与永久派生保管

内容提交b2371f81689e2a2bba9d56f86a63d0c94c62069f/treebe20947faaf4cd515f078d64d9c4ca163f595898，候选10/main11项适用Actions实际completed/success；最新main预期SHA保护非强制快进。十文件及整tree与本地原生Git一致，四连续性文档旧行删除0。专用候选run39778168917/job119822326970/artifact12425955325，主线run39778315542/job119822823027/artifact12425078703，各真实六单元、两文/三包装/三原JPEG实取、17去摘要门语义改写及每文script正例，Pillow12.3.0完整解码。

实际下载双ZIP各3580B，SHA256 c301dfa0fa74034a98ff1c6cc3f40c4bb7b6c324f146092f5db1c3822c663ef6 / ab6056e8273c99f882c6f63b8e716b3e520fa4883f1b35abeef279d858058c00逐一符合API；唯一replay.json完整12870B/SHA25675c727e6d6ac73ee229487c270adde7d98fe2ef842b462736b1500d36fe72ccd/Git blob64891c06460ff6efc36b6049e228fa9e696f010e。双CI/local/加入保管门后local四份逐字节一致，整页、包装与图片输入仍同初取；不称2005原始字节。

双CI原JSON及research/recovered/STONEAGE-JP2005-FLEA-MARKET-CUSTODY-R1.json永久入Git，固定内容Git、21实际run、双job/artifact/ZIP、每次raw/input摘要和七永久文件原字节/原生Git身份，含三父报告与复用解析器。强制保管门拒绝缺失/等长篡改、错HEAD/分支、重复run/job、遗漏初取历史、虚报原字节相等及历史权威升级；六→七单元，相关38项本地回归通过。保管提交自身候选/main CI须另真实后验，不拿内容六项绿灯称七项。

场地/活动/公告申请分层保持；三插画不是市场地图/UI，付费报名条件不外推入场，自由买卖不证零税费/自动摆摊。原ID/build/投稿表单/交易界面/结算与实际保存仍未知；原HTML/JPEG/程序不进Git。最高NEXT75回22域另一地区人物创建/角色外观或交通服务具名材料；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，旧全文保留。


## 2026-10-22 R75：长毛象公车的上车、聊天发车与退队下车

启动远端main205cfef430798180f981fedee78683f0d139d9cf/tree157aabe0159a2fef1304b007638bba5241115728，472分支/0开放PR/运行中Actions、原HEAD候选8/main9项成功；旧queued37642417333单列。九启动来源完整UTF8/精确git show/原生Git核对，CURRENT2364938B历史完整，5169项未截断树无AGENTS。按最新NEXT75/22域回大陆交通服务，不扩市场helper。

新增新浪2011-12-19 11:08《长毛象公车有木有石器时代长毛象出动》，正文具名广东胜思与出链sa.cins.cn，属运营商具名宣传刊文、非取得原官方页/发行稿。当前HTTP200无跳转70268B/SHA256f0af4be08fe1878032567bca084badd71cb7bd684c2527b596536f012bc0af36，严格GB18030；三交通段389字符/1163UTF8B/831e7c0b1a427aec972f1377c5793305e121e6651248a65f3168f9b8d48f2581独立正则/实体解码复核。页尾同时宣传8.5魔域大冒险/2.5精灵王传说不能绑定具体交通build；1125地图等未选宣传不入本包规则/名录，2026字节不认证2011历史。

交付docs/specs/STONEAGE-CN2011-MAMMOTH-BUS-SOURCE-R1.md与SOURCE JSON：找站选目的地线路、面向长毛象点加入队伍、普通聊天频道小写go提前发车、中途退队下车分层。立即仅宣传时序，不补零延时、GO变体、最少人数/权限、车费、正常等车时长/人数/遇敌或实际ACK/保存。村口描述非完整全村站点表，人口/距离是设点理由非调度公式。

实际两IMG引用仅HTTP升HTTPS后取得，HTTP200，Pillow完整JPEG/RGB解码并目视：I1 74139B550×413/SHA2562b95dc810d305fb58d0cb6132e5d6e0b26f6ac970c1146fa9907e940b698f21b；I2 72157B550×413/3324aaaf92d8b7c39b4d5ea20f8bb60d09d276cc96aaaf5b2554dfece057b239。可见候车石墙/长毛象/人物站牌/顶部工具栏；I2底部可读萨姆吉尔、玛丽那丝两词，分隔符/整行不抄，不当方向边/原NPC-ID/完成乘车或动画序列。图片尺寸非原客户端原生分辨率；第三张壁纸只登记未选，未取像素；原HTML/JPEG不入Git。

固定既有JSS手册服务、CN2003交通玩家稿与19集合合同三父报告，以及两共享解析器原字节/Git身份。JSS2001实际捕获20010418083149中3分钟/4人/不遇敌不补2011未知，2011go不回填2001。CN2003 20–30石币保留其稿范围，go/出发原属加美航空不误配长毛象；旧稿无HTML SHA不被本轮派生pin升级。3目录=1tutorials交通说明+2screens静态场景，不当3恢复实体。

六单元、12实源语义改写在去整页摘要及正文指纹门后均拒绝；外围script/未选地图数量改写正例，相关25项本地回归通过。独立词法复核按钮/频道/go/退队及389核心，候选/main实取、双ZIP及永久派生保管须后验。

止于一文两交通图；重开需同版交通NPC/路线/命令/收费配置、原画面或实际通信/保存。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-76回22域另一地区人物创建/角色外观或具名宠物生态，优先原运营站，音效仍需同版真实输入。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部旧历史保留。


R75验收前措辞收紧：首候选eca552d814b87f42536175d435dfc699077b22a9的“面向”/FACE_MAMMOTH过强；原文仅“在长毛象面前”，现改为STAND_IN_FRONT_OF_MAMMOTH（站在公车面前），不证明人物朝向检查或方向标志。原候选、六单元工件及其Git历史保留，新内容提交需重新实取验收，不能借前稿绿灯。本次不是源正文或图片变化。


### 2026-10-22 R75修正稿双端实源验收与永久派生保管

最终内容提交057eadeb49fa847d4d6092840afd64a79efd3765/tree757c3c3bdeb013646a178b6f3774cc765c55fa81，候选10/main11项实际completed/success，最新main预期SHA保护非强制快进。正文/图片字节不变，步骤已收紧为站在长毛象面前，朝向检查不证。首候选eca552d814b87f42536175d435dfc699077b22a9及其source run39786866710/job119852281383/artifact12429049151、11036B原派生摘要dcdf6c4ada9b6ef6c9a966882d1057ad8015e1d4ca692705d7371f3fd0f3752b仅保留更正历史/元数据，不借其绿灯验收最终语义；原候选源报告Git仍可读，旧临时raw未另永久归档，收据明确区分。

正确稿专用候选run39787629042/job119854849617/artifact12429068184，主线run39787861655/job119855657301/artifact12430325393，实际各六单元、一文两原JPEG实取完整解码、12去整页摘要及正文指纹门语义改写、外围script/未选地图宣传正例。独立另核五个字段确实动态变化，三个隐藏正文条件无法被页尾同文补证。

实际双ZIP各3429B，SHA2561f03d67183cc5057f532796805b3018cab9ffce09540cc3a1017d933b91f7f2c / d25376d500deea65d8e9f6a3b938a53d5a411aba3739a47f6b237f86b28cd2dd逐一比API；唯一replay.json各11062B/SHA256b80fa0a345db306b86bd2e3b3588e1a4bba548dae4707da14e33537f8a701c3c/Git blob22ac399dca4162ff69b0ef3a9d5d8e7938341adb。双CI/修正后local/保管门后local四份逐字节一致，原HTML与两图输入均同初取，不称2011原始字节。

双正确稿原CI JSON与research/recovered/STONEAGE-CN2011-MAMMOTH-BUS-CUSTODY-R1.json永久入Git，固定最终内容Git、21实际run、双job/artifact/ZIP/raw/input、八永久文件原生Git身份，含三父报告/两共享解析器，并保留首稿更正归属。强制保管门拒绝缺失/等长篡改、错HEAD/分支、重复run/job、历史权威升级/虚报字节相等或借首稿作最终验收；六→七单元，相关26项本地通过。保管提交自身候选/main CI须另真实后验，不把首内容六项绿灯写成七项。

两图只作静态交通场景/标签，不证go执行/乘车成功/方向检查/完整拓扑；早期3分钟4人/2003航空go不回填，收费/容量/遇敌/权限/原ID/build/保存仍未知。原HTML/JPEG/程序不入Git；最高NEXT76回另一地区人物创建/外观或具名宠物生态，优先运营站；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部旧历史完整。


## 2026-10-22 R76：Netmarble手游具名人物背景与官方立绘

启动远端main7fad6905615b3b6167820a2aa4d786d6afb4d799/tree0674e93a1194e36d2a9ea36e1b3be34c6b14b033；474分支、0开放PR，原HEAD候选8/main9项成功。首稿eca旧run39786866705仍in_progress、旧queued37642417333单列，不与最终HEAD混淆或取消。九启动来源完整UTF8/精确git show/原生Git核对，CURRENT2371038B历史保留，5178项树未截断无AGENTS；读取最新NEXT76与22域索引，回人物身份/外观，依既有资料库规范将现代手游/同IP续作独立产品归档。

新增第一方https://stoneage.netmarble.com/ja/gameinfo/character ，title/og:title《ストーンエイジ：放置冒険》、ja/canonical同页，页脚Netmarble Corp./N2 Inc.。当前HTTP200无跳转37246B/SHA256bf0c6d8ecd7a59378749b763b46baacaee634a8a5761e7549674d54511e2b87d、严格UTF8。无页面刊时/精确build，2026-10-22仅观察日；CDN20260209/文件名数字/meta年份不当发行日期，不是原PC历史页面或原客户端。

交付docs/specs/STONEAGE-NETMARBLE-JA-WOODY-SOURCE-R1.md及SOURCE JSON，一默认SSR detail具名ウッディ，两个相同em只一角色；背景去空白55字符/165UTF8B/SHA256937adccae4696a3d60ffdfa3d8504a9da299010a42e447b56a8e4d974b152db3独立词法核对。サムギル村为故事居住关系非出生点/地图ID，優柔不断/天然/楽天的保留原词不作数值；冒险后逐渐勇敢/正义感是叙事非等级/任务触发/buff。文本年龄/性别、HP/技能/原ID/模型/精灵与动画均未知。

同detail figure.image-main实际IMG PNG取得HTTP200，133427B/SHA256623e33509df4f46aa7adaf8862d1d9676606579bc3b81fc4b13f66cf6ce5a62a，960×1196、PNG/P单帧、alpha0–255，Pillow完整解码/目视。棕发发束、毛皮装束、赤脚、肩扛大石刃仅图像描述，不命名装备/攻击数值，非游戏精灵/模型/动画/原TW1调色板或客户端分辨率。原HTML/PNG不进Git、生产权利未授；未取缩略图/其他角色/JS/样式/音效，BGM按钮不构成真实调用输入。

固定旧Hangame2003人物SOURCE、19集合合同、允许现代手游但要求产品隔离的资料库规范三父文件与共享可见标记解析器。早期运营商无固定名字/玩家命名、12页面位置不被本手游具名改写；不合2003位置1、2006头像或原body/face/模型ID，不报同一世界线retcon或早期资料被推翻。一个characters研究目录不是一位可玩初代人物恢复，也不称全手游名单。

六单元、12实源语义改写在去整页摘要/背景指纹门后均拒绝；外围script/修改CDN路径仍不认发布日期正例。合成不同村落/性格另证动态提取，目录重建后的权威/未知反例及父报告/解析器缺失/等长篡改拒绝，本包/复用模块14项本地通过。一次探索缺BeautifulSoup后改标准库，未新增依赖；候选/main实源重放/实际ZIP/永久派生保管须后验。

止于官网默认一角色一图，重新打开需另一明确官方人物正文/同产品模型或实际剧情规则，初代身份仍需对应原件。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-77回另一地区PC官方NPC/任务或具名宠物生态，优先运营站/同期一手；不连续扩本手游缩略图/商城，音效需同版真实输入。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部旧历史完整。


### 2026-10-22 R76双端官网实取、整页差异与永久派生保管

内容提交2902639e92e733f15a6169da02dfffa097de0f57/tree87b6aa2894efd9fa37f0369f89106cebd860661d，候选10/main11项实际completed/success，最新main预期SHA非强制快进。十文件/整tree与本地原生Git一致，四连续性旧文前缀完整。专用候选run39790920975/job119866404613/artifact12431123105，主线run39791101746/job119867034158/artifact12431177139，各实际六单元、第一方当前detail+原PNG实取完整解码、12去整页摘要/背景指纹门语义改写及两正例。

两CI整页37247B/SHA2561496a6eea925ab6aa86ae249196d6b3e9700156e718be3ebb3c9a198fb25ab35，与初取local37246B/bf0c6d8ecd7a59378749b763b46baacaee634a8a5761e7549674d54511e2b87d不同；长度多1B不等于证明只改一个字符，未获CI原HTML的差异位置/原因。一次有界local复取仍同初取37246B，原因保留未知。所选55字符背景、名字/产品/字段、精确PNG、目视观察、目录/版本比较和反例结果均一致。保留每次原inputs，不删字段/规范化伪造全字节相等。

实际下载双ZIP各2488B，SHA25682460ffe608da649f22591c4d7e6805b9829d947f828a565b50bbc3f463c6f73 / 8c6b9e24393c9d2b2c249a7e468bff434528abfdfd5f0336fb4d46f44eb61505逐一比API；唯一replay.json各6987B/SHA256fee0f3377b8fe76e258182d2dbbd34432acf2fe9371f78f258dc8947be7f0935/Git bloba154d4fe30c57bca50479a8f28ec1edf82fc5495。双CI原JSON逐字节全等，但与初取local不同；加入保管门后对初取输入的local重放仍与门前local逐字节全等。PNG始终133427B/623e33509df4f46aa7adaf8862d1d9676606579bc3b81fc4b13f66cf6ce5a62a，不把HTML差异扩大成角色或图片变化。

双CI原JSON与research/recovered/STONEAGE-NETMARBLE-JA-WOODY-CUSTODY-R1.json永久入Git，固定内容Git/21真实run/双job-artifact-ZIP、原raw/input及七文件原生Git身份，含三父报告/共享解析器。强制门拒绝缺失/等长篡改、错HEAD/分支、重复run/job、遗漏初取历史、虚报CI等于local、擅定整页变化原因/历史权威升级；六→七单元，相关15项本地通过。保管提交自身候选/main CI须另真实后验，不拿旧六项绿灯冒充七项。

本手游身份/叙事/静态原图不合早期PC角色；未恢复初代人名、原模型/精灵/动画、数值或可玩剧情。原HTML/PNG/程序不入Git，止于默认一角色一图。最高NEXT77回另一地区PC官方NPC/任务或具名宠物生态、优先运营站/同期一手；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部旧历史完整。


## 2026-10-22 R77：小水怪还子、掳兽动机与双路线奖励

启动远端main77da6d7c634c3c8d4729bb350e14910a4dd194ca/tree9520c9c78e1bca922033af18c4a37ed0a8fe628e；476分支、0开放PR/运行中Actions，原HEAD候选8/main9项成功，旧queued37642417333单列。九启动来源完整UTF8/精确git show/原生Git核对，CURRENT2377067B历史保留，5187项完整树无AGENTS；读最新NEXT77及22域索引，回大陆PC时代NPC/任务/生态，不扩现代手游人物helper。

新增新浪《石器时代》任务功略-小水怪事件，标2003-06-03 11:57/作者新浪游戏，当前HTTP200无跳转54531B/SHA256e9308a360a7fa4acf63cfb1965f4c18dc72e504a5b7da1266d88e5f405b580a3。一次Availability请求20031201只返closest20160929133108，实际历史HTML60767B/265aa1cbfbf7f2f413a1d4055953981191850817900d54c800c5d3caafb84d33，GB18030严格/HTTP200，2016捕获不冒充2003原始字节/首刊/build。双包装仅一来源，作者/官方原稿和精确商业版本未认证；伊甸语境不认TW1.0。正文去导航尾2897字符/8409UTF8B/SHA256c4fbb96139601b83f89e4a1be243cc370a12fb8396358d3a1a2a53c7f64657bc相等，独立词法复核。

交付docs/specs/STONEAGE-CN2003-WATER-MONSTER-SOURCE-R1.md与SOURCE JSON。105是建议非已证硬准入；携不可思议贝壳/解金飞是条件栏，贝壳在剧情中仅听懂动物，未证入口钥匙/消耗/装备位。三条取得任务是替代途径，不当三项全前提。传送师栏写尼克斯城不造同名NPC。尼克斯东南受损、亲代水怪因幼兽被网捕而报复、女王/妮芙偏好尽量不武力、还子和解与赠晚餐蛙记来源叙事，不证捕食AI/动态世界保存。

A路线先麦叶传送/战100级水怪再调查巴克，B先动物园/救幼兽再还子，不能把B没叙述水怪战斗扩大成原服绝不会触发。两线巴克100/跟班75，禁组队只该战；HELP/带宠未知，建议先打巴克非强制目标排序。两线奖励尤里蛙；B另双头叉攻+75敏-25滋润Lv5及近卫队象征。“维修过后第一时间”是未量化攻略条件，不补库存1/每日/秒数/必得。幼兽正文莫拉司/图注莫拉斯保留异文、未并原ID，不当奖励宠物或玩家所有。

四互动对象邬莉叶/麦叶/水怪克拉肯/副园长巴克，各自职责/层数/坐标有界；地下水路入口291,34、8层标题、80–100、5怪标签不是全可捕物种/地图几何/原ID，末两图注果字保留。18实际原图引用登记，仅取第4/10条两原JPEG：I1 71197B/11afbc0228cba1784870958ae96472595a3fbe9876fc13580ed8a8c067c73f27；I2 95671B/248f1daeb4d1e9b12c9b523d69971ae604ecabdddcf44500c6d5a06314c1387d，各640×480/RGB、HTTP200完整Pillow解码/目视。目标克拉肯Lv100不混中央25；物品叉+75/-25/Lv5与正文一致，玩家样本Lv87非准入证明；当前JPEG不因2016 HTML引用相同就认证历史原图。16图未取，原HTML/JPEG/程序不进Git。

固定旧琉璃家庭叙事SOURCE、早期友谊送壳服务/指南及19集合三父报告与共享解析器原字节。琉璃未完成重聚不被本攻略还子结局覆盖，亲代/幼兽/各任务不合ID；早期贝壳不补沟通功能或同原物品ID。11目录=1双路线任务+4互动对象+2道具+1奖励宠+1生态地图+2截图，不当11个恢复原实体。

六单元/每包装22去整页摘要与正文指纹门语义改写共44及script正例，相关18项本地通过。独立正则/实体解码核2897核心、四坐标出现次数、双巴克等级、A/B顺序、三贝壳来源及武器数值。初稿把将/把原晚餐措辞统一造成一次本地失败，已按原文修正重跑；无远端失败。实际候选/main实取/ZIP永久保管须后验。

止于一攻略双包装/双路线/两图，不扩全动物园/金飞/地图。重开需同版官方原稿/商业脚本/原ID、维修奖励规则、历史原图或实际通信/保存。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-78回另一地区PC宠物生态/技能或具名NPC，音效仍需同版真实输入。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部旧历史完整。


## R77 实际CI与永久证据保管验收（2026-10-22）

内容提交 `87fd1bcb8b2b3e4d00cc506a9b11c601289d4b6b`，原生Git tree `905773d0fe86a872620fb8c274e198ec30f29db7`：候选10/main11个实际Actions全部completed/success，来源任务两端各6单元及实际双HTML/双JPEG取回、44个去摘要/正文指纹门语义反例成功。逐一下载ZIP、核API大小和SHA256、只含replay.json，再与SOURCE语义/两图/11目录逐字段比较。

- candidate run `39795522113` / job `119881789480` / artifact `12433431840`：ZIP 4852B `sha256:c5d95daf925f8116bdca3e629469dcab9dca0f3c3600d5a3a84cde27ddc867a7`；原始JSON 24288B/SHA256 `50af6fdbbd0b27fbc76d0d6a5421857382f210c1a543d624cbee2c764a3cdf47`/Git blob `c3314e43dd714f723a10e185e13c507448a5ba4c`。
- main run `39797430927` / job `119888249554` / artifact `12434366035`：ZIP 4852B `sha256:fb13ce4af18767aaf65f365cc689c8d4edeccbded6fbbed52a869adcc9486417`；原始JSON 24288B/SHA256 `50af6fdbbd0b27fbc76d0d6a5421857382f210c1a543d624cbee2c764a3cdf47`/Git blob `c3314e43dd714f723a10e185e13c507448a5ba4c`。

两个CI原始报告逐字节相同：True；两端各自等于初始HTTP输入：[True, True]。逐字节相同只是这次实际观察，不把当前HTTP或2016存档包装称为2003原始字节。原始derived JSON两份及CUSTODY收据永久进入Git，七pin固定SOURCE、三亲代报告、共享解析器与两原始报告；30天工件过期不删除这条已核链。原HTML/JPEG及任何专有资产均未归档。

CLI现强制要求收据；缺失、同长篡改、门禁遗漏/重复、错误分支/HEAD/任务/工件、改报输入相等、抬高历史/运行权威均拒绝。加入保管反例后本包7单元，相关合19项本地回归及同输入重放通过，旧6单元CI历史保留；保管提交自身候选/main检查另行后验，不预报结果。

这完成的是有来源的分支任务/NPC/动物沟通/奖励与生态规格；官方作者、商业build、原服ID/flags、硬准入、实际HELP/宠物、维修奖励配额与真实服执行仍OPEN。Stage A仍7 PARTIAL+2 OPEN，B/wiki仍GATED，savedata R79仍PAUSED_NON_BLOCKING。最高NEXT：OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-78，回另一地区PC官方宠物生态/技能或具名NPC材料；不扩本攻略其他16张图，不因相近名字合并早期贝壳ID。


## 2026-10-23 R78：日服具名宠物商城取得与相对概率边界

按远端main dc789d85a4a2f438f049b487a5cd7fecdb66cc79/tree6f856d2344050329e7a0642d85b950f18f321cac重新启动。分页核478分支，最新R77保管候选同HEAD；0开放PR/运行中Actions，旧queued37642417333仍单列。该HEAD候选8/main9项实际completed/success，保管提交的7单元检查亦已真实通过。协议等八启动文件完整UTF8/精确git show/原生Git核对，CURRENT原2383555B、SHA25689eccf51fc62c947d93af53535325855a1e57f91bc94fe90d0e29537b638200d；旧历史前缀完整保留。读取最高NEXT78及22域索引，无AGENTS。

本包恢复的是日本PC2007两种具名宠物的取得途径与版本差异，非商城实现。新增4Gamer2007/07/30 19:47明示UTDエンターテインメント配信元/原文转载的厂商发布文：当前HTTP200无跳转19696B/SHA2560b584c6a5af65b4344f703b20c7676f9accbea9e4c4d5df59e0bf406bebc6e43，严格CP932。引文可见核心675字符/1673UTF8B/b02e9b6773e5c569ce64bc2c28e686bed92cdac38e0f6b1e451464b4aaab763b，独立正则/实体解码复核；当前字节不认证2007原件。

黒檀のくじ称7月27日起售，7月30日18:00至31日13:00ギガドラン/ドルーザス出现率各加倍，余四种略降，终点亦售卖结束。年份按刊年关联、正文窗口不另写年/时区；1000GStone是マンモストア虚拟币价格标签，不补券数/捆绑单位/汇率/保底。未取官网所指18时以后详细概率表，不解出绝对率、四个名字、归一化或野外遭遇/捕获率；与既验2008フクゥーリ直接捕获/GASH活动分开，原ID/build/成长/技能/栖地与执行保存OPEN。

两条实际IMG附图HTTP200完整JPEG/RGB解码并目视：I1 26401B140×240/b511b1091843075a2f8e08915fa2b7fc1fda4fbb83197e89a4d71b56bdd2b516为促销横幅，I2 44950B306×189/194a88bf354674e896bbfb871858d26f15aa3ddc34010665d98dee73c4b62fac为双角兽促销插画；无左右名字，不按正文排序强合物种，不当原SPR/模型/动画或原生分辨率。一次官网首页Availability请求20070730返回20070805235420，捕获未取/不是详细概率页；一次推测7月27日文章URL的网页读取失败，未作来源/继续猜号。

交付docs/specs/STONEAGE-JP2007-EBONY-LOTTERY-SOURCE-R1.md、SOURCE JSON和有界实源重放工具/工作流。4目录=1抽签物品描述+2具名获宠描述+1公告/余项规则，附两图元数据，不当4恢复原实体。两父报告与复用可见标记解析器原生Git身份固定。13去指纹门语义改写、隐藏/移引文外2反例、外围script正例，本包5单元/相关合20项本地通过，精确原输入离线重放通过。候选/main实取、实际ZIP和永久派生保管待后验，不预报通过；原HTML/JPEG/程序不进Git。

止于一发布文两附图。重开需原运营概率表/同版配置、具名原画或实际通信/保存。不递归商城。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-79回22域另一地区的早期人物创建、交互界面或生活服务具名原件（此内容队列编号与暂停的savedata R79无关）。Stage A仍7 PARTIAL+2 OPEN，B/wiki仍GATED，savedata R79仍PAUSED_NON_BLOCKING；无整体完成百分比。


### 2026-10-23 R78双端实源验收与永久派生保管

内容提交7d6cae1fb2353bd163e687da368596c4343939f2/tree44f322bca54ab4c115a49ed9f7a5829888ded917，候选10/main11项实际completed/success；主线新读旧HEAD后以expected_sha保护非强制快进。九文件Git blob与整tree逐一符合本地原生Git，四连续性文档完整前缀保留。专用候选run39866592550/job120130214377/artifact12463688573，主线run39866717616/job120130630206/artifact12464660896，各真实5单元、一发布文两JPEG实取/完整解码、13去正文指纹门语义改写及隐藏/引文外2反例和外围script正例。

两ZIP均2169B，SHA2565d7317aefeaecc9a249bde33b5d2a13915359664179a75959a335a9a2537f675 / e454bb122f25028e842e1da7c30517aa3bcba54615bc469843535f214e51c143逐一符合API；唯一replay.json均6934B/SHA2562d4cc54965cc7d60ec05af66461571c8463b3516a238bf1b7de6d5f05aee72e2。候选/main/local/加入保管门后local四份逐字节相等，三HTTP输入亦同初取；不把2026当前字节称2007原件。

两原CI JSON与research/recovered/STONEAGE-JP2007-EBONY-LOTTERY-CUSTODY-R1.json永久入Git。六pin固定SOURCE、两父报告、共享解析器与两原CI报告原生Git身份；收据含内容Git、21实际run、双job/artifact/ZIP/raw/input及初取历史。CLI强制验收收据，拒绝缺失/同长篡改、错HEAD/tree/分支/任务/工件、遗漏/重复run、失败改成功、复用job/artifact、虚报输入相等或抬高历史/运行权威。本包5→6单元，相关21项本地回归与原输入逐字节重放通过；保管提交自身候选/main检查另实际后验，不倒称内容CI跑过6单元。

相对商城概率、四未名余项、币种和时间边界保持；左右物种配对、绝对率、初代归属、原成长/技能/栖地/ID/build与真实部署保存仍未知。止于一公告两插画，不继续扩商城。最高NEXT79回另一地区的早期人物创建/交互界面/生活服务具名原件，与暂停savedata R79无关；Stage A7 PARTIAL+2 OPEN，B/wiki GATED，旧历史全文保留。

原CI JSON原生Git blob：62047d8f74202da0b929391a24d3995e73e0478e（两端原字节相同）。


### R78目录合同更正与保管提交后验（2026-10-23）

保管提交49c6c8d789121eae12f0cd8cd52a46ba692016ea/tree4e089f0c4b81918756eb4f5b398342243afffe3c的候选10/main11项实际completed/success，专用候选39867056285/job120131759360已真实跑6单元/取源。末次逐字段核19集合record_contract时发现：原SOURCE/CI的四个catalog_records行缺必填entity_type，前述“符合合同”范围过强，现明确这些只是保留的原始派生行，不是完整导出目录。原SOURCE、双CI及六pin收据一字不改，保留可核验历史。

新增独立STONEAGE-JP2007-EBONY-LOTTERY-CATALOG-R1.json，给四行各补文献语义类型，固定原SOURCE字节/Git身份，显式记录旧行缺字段及原报告完整保留。CLI强制核对新导出与原语义并逐条检查既有全部必填字段/集合，不升级成原游戏实体或生产权利。新增缺失任一必填字段、物种master类型、TW10改版和错误来源摘要反例；本包7单元，相关22项本地通过，源重放输出仍与原CI逐字节一致。新导出/检查的候选/main验收须随后实际核对，不借前6单元绿灯。最高NEXT79与阶段门不变；这是一次目录可消费性修正，无新增历史事实。


## 2026-10-23 R79内容：早期名片窗口、宠物状态与家族文书权限

从新读远端main63b50f86101de7c8e29c86322d5b9ccba5cc0cde/tree0383f022fcb1cc417a13d3ab91a977533224bd94启动，481分支/0开放PR与运行中Actions，前轮最终候选8/main9项实际completed/success；旧queued37642417333继续单列。八启动文件完整UTF8/精确git show/原生Git比对，CURRENT2390237B/SHA2568e290c68167544f945b82825a96e271dc390dc1644e4b3f883e0ad6d98870ebf全历史保留，无AGENTS。读最高NEXT79/22域，从日服后期商城转大陆早期操作界面；这是内容队列R79，非暂停的savedata R79。

本包补真实名片界面与2001运营站操作/通讯/文书权限来源。重新取得既验基本操作精确捕获20011204000349、68863B/SHA2569be8b3ea0d48ebc17639e1114cba6606eba1a135a181ed5ad8f192392e554809，GB18030严格/HTTP200无跳转，正文题名基本操作。与记录点包同一页面/同字节，旧包仅选原地登出/交易YES；不称新发现网页或独立证人。现在结构化22完整章节，可见正文1650字符/4786UTF8B/SHA2568bbcbf8e9867f60fc07d3eb5c4c79ce54b94e3cf552705b5f6fa49b1320f4d05，独立正则/实体解码复核。官网托管不认证具名作者，存档/2.0题名不认证首刊/精确build或初代规则。

恢复文献中的底部七窗/左上八键、附近或队伍Enter文字、面对NPC/看板、状态含队友、五宠物模式和三种各限一只、已学骑乘AND选中可骑宠才显示选项。家族分频道/全体频道、族长职能/在线族员广播、招募/成员管理与让位分层；只有四大庄园族长可制邀请函、持函入所属庄园房间、持学习同意书在对应庄园学骑宠，不补庄园名/ID/费用/物种与技能主表。HELP接近/面对/按钮与最多5玩家、决斗YES、13动作保留来源，不当5个含宠物actor或已恢复13动画。状况/状态视窗原标签并存，宠物详情句尾残句不补造。

新取得正文实际img/4.gif原图，初请同正文时刻且www域，实际转20011227175240裸域。HTTP200，155995B/SHA256e91b36552855db65420ca2c0762f7409ef797ce8d88c2d87532c6bac92322a4b，GIF/P640×480单帧完整Pillow解码/目视。真实名片窗可见四条（三有资料/一空）、LV/DP、Online/Offline、Mail/Delete及户外图腾石墙；未抄玩家名、数值、页码。四可视条不是总容量；静态Online不证实服状态，按钮不证投递/删除/保存，Eng不认证地区/语言/build。正文12/4和图12/27分开，不当同版一次运行；缩略图仅声明240×180未取像素，原图尺寸不当原生分辨率。

与既验2003门户攻略分源：本文没叙述双方OK、队长跟随/组队YES、Ctrl+I/CTRL+L，不能反向填入或把缺叙述当原服没有功能；相似用词不认证作者/抄袭/同构建。旧门户报告无HTML字节SHA保持null。JSS2001名片登出开关NO、战斗宠邮限制/失散时限亦不补大陆。宠邮文字不证所有权永久转移，曾拥有可拍照不当自动全历史相簿，音效设置不作音频事件绑定；不重开savedata。

交付docs/specs/STONEAGE-CN20-OPERATION-UI-SOURCE-R1.md、SOURCE JSON及独立实源工作流。8条完整目录=7组教程+1静态屏幕，七必填字段/19集合逐一核验，不当8恢复原实体。四父报告与共享可见解析器原字节/Git固定。23去全部章节/正文指纹门语义改写、隐藏/移正文外同词2反例、外围script正例，本包7单元及相关25项本地/源重放通过。一次合成测试替换了不含空格的题名导致无实际改写并失败，已按原基 本 操 作修正重跑；无远端失败。候选/main实取、实际ZIP/永久报告保管须后验，不提前宣称通过。原HTML/GIF/程序不进Git。

止于一已知正文/一新获实际界面图，不扩全部快捷键、庄园或helper。重开需同build屏幕/操作轨迹、原协议配置、名片或文书持久化原件。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-80回22域另一地区具名任务、宠物生态或世界叙事原件。Stage A7 PARTIAL+2 OPEN，B/wiki GATED，savedata R79 PAUSED_NON_BLOCKING；不报整体百分比。


### R79内容双端实源验收与永久保管（2026-10-23）

内容416cbe29e663b02665f0a24e1fef131ad9069941/tree2a06ae793788cdeb46664b78a39c97fb753fd851的候选10/main11项实际completed/success；主线新读旧HEAD后expected_sha保护非强制快进。九文件与整tree逐一符合本地原生Git，四连续性历史旧前缀完整。专用候选run39868987195/job120138321325/artifact12465576209，主线run39869070986/job120138610152/artifact12465227797，实际各7单元及12/4正文、独立12/27原GIF取源/完整解码，23去全部章节/正文指纹门语义改写和隐藏/移正文外2反例通过。

双ZIP各6344B，SHA25658dbcda024024d3d2edcc6a4ac4ad086344c0f406f7b7b2843784833cdf5d1af / ea9669ae0f7726ea0d74738be583cdb8f43b3e74faabccee33eca6616dcbae4e逐一符合API；唯一replay.json均23470B/SHA2565f4d13881af77a13cab06f6c232cde1dba89fd19b63254fbebca496b6527413e。候选/main/local/加入保管门后local四份逐字节相等，两HTTP输入均同初取；已知正文亦同旧记录点包原件，不新增独立见证或提升为原服执行。

原CI JSON两份及research/recovered/STONEAGE-CN20-OPERATION-UI-CUSTODY-R1.json永久入Git，八pin固定SOURCE、四亲代报告、共享解析器、双原报告的原字节/Git身份；收据含21真实run及双job/artifact/ZIP/raw/input初取历史。CLI强制保管门拒绝缺失/同长篡改、错HEAD/tree/分支/工件、门遗漏/重复、失败改成功、复用job/artifact、虚报输入相等或把正文/图拼成同版/首刊/实服。补强源首刊空值/取源元数据守卫，增加保管反例后本包7→8单元，相关26项本地回归/原输入重放通过；内容CI七单元历史保留，保管提交自身候选/main须另后验，不提前倒称八单元。

真实名片窗口仅证明图像中可见四条，不认证容量/在线或Mail/Delete执行。两存档时间/域名变化与缩略图未取范围完整保留，原HTML/GIF/程序不入Git。骑宠AND条件、邀请函所属庄园/学习文书、HELP玩家数和既验JSS/2003版本边界不变；最高NEXT80回另一地区具名任务/宠物生态/世界叙事，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、savedata R79暂停，旧全文保留。

双CI原JSON原生Git blob：06f3f04280311dbd7b49f4477f76856b7152cc56。


### 2026-10-23 R80日本料理挑战与活动奖励分层

最高NEXT80完成为JP2005-AUTUMN-COOKING来源规格：一同期新闻/一实际料理插画，五活动/11文献行，料理全完成奖、两村食材半价、两服GM课程、官网竞赛ガーヴィ与两类佳作奖、仮称变身活动分别归属。不是原配方/任务实现；身份/ID/成长/公式/部署均OPEN，配图不认具名宠物或NPC。三父报告与解析器固定，27语义/2隐藏正文外反例，7本包/27相关本地单元通过，远端与永久保管后验。不再扩UI/helper/商城。下一最高OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-81回另一地区早期地图/NPC/世界任务或具名宠物生态原件；同版原运营菜谱/配置或执行材料才重开本支。Stage A7 PARTIAL+2 OPEN，B/wiki GATED；savedata R79 PAUSED_NON_BLOCKING。旧历史全文保留。


### R80双端独立取源与永久派生保管（2026-10-23）

内容1661fbf97dc3daee68db7cf888dbd0cd1316971e/tree0a23592f4fe6bf87acf715a81fb505155e7854ca，候选10/main11实际completed/success。九文件原生Git blob/整tree一致，四连续性文档原全文前缀保留；主线新读HEAD后expected_sha非强制快进。专用候选run39872608102/job120150412494/artifact12465759972，主线run39872716074/job120150771890/artifact12465814773，日志实际各7单元、一同期正文一JPEG取源/完整解码、27去全部指纹门改写及隐藏/正文外2反例通过。

两下载ZIP各4152B，SHA25653d34d07464b432f855e4ddc825a60055e605c212bc4e8baba24677a0e593b14 / f05269a5ce19739ec5386bf2eea54f93d19a5dff99f6d96fbed38badcaf50648分别符合API；唯一replay.json两份均17829B/SHA256a892610a1740692743adb95090e007daa9fc376880b5237c8b790e925cd42d82。候选/main/local/保管门后local四份逐字节相等，两HTTP输入摘要也均同初取。双CI原JSON和STONEAGE-JP2005-AUTUMN-COOKING-CUSTODY-R1.json永久入Git，原文/插画仅临时验证不入Git。

七pin固定SOURCE、三父报告、复用解析器和两原CI JSON的原字节/Git身份；收据永久记录21真实run和双job/artifact/ZIP/raw/input初取历史。CLI强制验保管，除缺失/同长篡改、错内容HEAD/tree/分支/原输入相等性和运行权威，还固定整21项实际run清单摘要及准确run/job/artifact ID，拒绝仅用另一成功门替代。本包7→8单元、相关28项本地通过；保管门后输出逐字节不变，七单元内容CI历史不改称八单元。保管提交自身候选/main另实际后验。

本次是同期报道的可审计内容规格，不提升为直取运营公告或已发生发奖。料理挑战/官网竞赛、两村食材范围、指定服课程、配图无身份边界保持；菜谱数量/原ID/数值/实例唯一性/公式/持久化仍OPEN。下一最高NEXT81为另一地区早期地图/NPC/世界任务或具名宠物生态原件；Stage A7 PARTIAL+2 OPEN，B/wiki GATED，savedata R79 PAUSED_NON_BLOCKING，旧历史不删。


### 2026-10-23 R81三村守护石与梦德洞窟

最高NEXT81交付CN2003-MENGDE-CAVE具名内容规格：一标2003/5/29的未具名作者门户攻略、两实际奖品全图，三村叙事/7 NPC出现/井口暗号/两守卫/取石及卡坦→霍特尔→柯尔克奖励次序，17文献行。推荐60/成人前置/反序失黄首饰各按原文归属，不冒原flag或脚本；同称村姑/世界局部坐标/勾玉售价/静态tooltip/早期记录点和吉鲁生态不混。27语义改写/2隐藏正文外反例，本包7单元/相关24本地通过；远端及永久保管待实际。停止一文两图，最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-82转台湾具名宠物模型/技能/生态或官方版本世界线资料。原商业脚本/ID/历史像素/实服行为才重开本支；不再延长盗物helper。Stage A7 PARTIAL+2 OPEN，B/wiki GATED，savedata R79 PAUSED_NON_BLOCKING。


### R81双端取源验收与永久派生保管（2026-10-23）

内容2530499c76c3780e8b7d2e15982563d88f93f0c5/treed112a01ed9f932df14745e94792acf92f412f29c，候选10/main11项实际completed/success，九文件原生Git blob及整tree逐一相符，四连续性旧全文前缀完整；新读main旧HEAD后expected_sha保护非强制快进。专用候选run39874364409/job120156231594/artifact12466888933，主线run39874471682/job120156583328/artifact12467880934，实际各7单元及一正文两完整JPEG实取解码、27去正文指纹门语义改写、隐藏/正文外2反例成功。

两实际ZIP各5170B，SHA25686f190d3e823f3c69ab6bc823a7256b4bace790c8b6061ac981c4eb51f225ef7 / 8922bd5b4b1067e48a207800bab5b30f3fa4c28d58b9bdbed9055d68e85ce93f分别符合API；唯一replay.json各32210B/SHA25643a01c1bcce470814879c163a7b1d135874b5777aa218c2a92063263a64861cb。候选/main/local/保管门后local四份逐字节相同，三HTTP输入均同初取；这不是2003原字节/原像素认证或原服事件运行。

双原CI JSON与STONEAGE-CN2003-MENGDE-CAVE-CUSTODY-R1.json永久入Git；七pin固定SOURCE、三父报告、共享解析器和双原报告原字节/Git身份。收据保存内容HEAD/tree、21实际run、双job/artifact/ZIP/raw/input历史。CLI强制验保管并固定完整21项run摘要及源run/job/artifact准确ID，拒绝缺失/同长篡改、错HEAD/tree/分支/任务、遗漏/重复或成功门替代、复用工件、虚报初取相等或提升官方作者/历史字节/原服权威。新增第8保管单元，相关25项本地回归通过，原输出字节不变；原内容CI七单元历史不改称八单元。保管提交自身候选/main须另实后验。

本包可查的是三村叙事、文献NPC出现/分层坐标、口令、取石和顺序敏感奖励，未取得原任务脚本/flag、模型或盗物算法。领奖次序与原字串、2000S可售非现金、推荐非硬门、画面非实发奖及早期记录点/吉鲁生态边界不变。最高NEXT82转台湾具名宠物模型/技能/生态或官方版本世界线；Stage A7 PARTIAL+2 OPEN，B/wiki GATED，savedata R79 PAUSED_NON_BLOCKING，旧历史全留。


### 2026-10-23 R82狼人战斗形态与取得语境

最高NEXT82交付TW2002-WEREWOLF-FORMS规格：一2002标日/2019捕获GNN新闻、三实际120×120小插图，补狼人平时人形/战斗画面狼形及月夜變身称谓；图不认证两形态或火/地兽身份。当前原正文403，捕获不作同期原字节；台湾市场语境不认证精确服/build。取得限量包、WGS/石币内容、手机条件、卡牌周边/预告两兽和140张/骰子分层，不把月夜推夜间门、NO.1推数值、4.0媒体推首发。10研究目录，23语义/2隐藏正文外反例、本包7/相关23本地通过，远端和永久保管后验。停止一存档三小图，不连扩付费商品。最高NEXT83回早期具名任务/地图生态或同版实参音效；原宠物/技能表、具名原画/选择链、形态/兑换轨迹才重开。Stage A7 PARTIAL+2 OPEN，B/wiki GATED，savedata R79 PAUSED_NON_BLOCKING。


### R82双端实源验收与永久派生保管（2026-10-23）

内容1a851305330508a55cc70e5b8b4e8f15fac585e4/tree9237a486886b45509d89baf12dcff12a97993603，候选10/main11项实际completed/success。九文件原生Git blob及整tree逐一一致，四连续性旧全文前缀完整；新读main旧HEAD后expected_sha非强制快进。专用候选run39901001585/job120242308486/artifact12478711794，主线run39901121177/job120242684110/artifact12478952260，日志实际各7单元、精确2019存档三120小JPEG实取/完整解码、23去全部段落/正文指纹门改写及隐藏/正文外2反例成功。未重新访问403原文或重查Availability。

两实际ZIP各4138B，SHA25610e0dc6f684a1d261e814e0bf531d0e9792ce67bd07b64e6617158288066236c / 41914e47e5c11c690e37f193b31eba4aed2968ee794fc8320301456b02b5b325逐一符合API；唯一replay.json各19228B/SHA2562cac950f34acb4a5f034703bc150e91fab5ca8c74dd054c9311dd8d3cb6c8817。候选/main/local/保管门后local四份逐字节相同，四HTTP输入均同初取。这只比较存档与三当前CDN小图，不称未取得的当前GNN正文也相等，不认证2002原字节/像素。

双原CI JSON与STONEAGE-TW2002-WEREWOLF-FORMS-CUSTODY-R1.json永久入Git。七pin固定SOURCE、三父报告、共享解析器和双原报告的字节/SHA256/原生Git身份；收据记录21实际run、准确双run/job/artifact及ZIP/raw/input初取历史。CLI强制保管门拒绝缺失/同长篡改、错HEAD/tree/分支/任务/ID、门遗漏/重复或成功门替代、工件复用、虚报输入相等或抬高运行/官方作者/历史权威；另显式拒绝捕获=刊时、声称取得当前正文或完整原图。新增第8保管单元，相关24项本地回归与原输入逐字节重放通过；旧内容CI七单元不改称八单元，保管自身候选/main另实际后验。

狼人进入战斗才狼形及月夜原称谓、逆转换未知、促销强度/限量非数字主表、4.0媒体不认证build、手机/实体卡牌不混虚拟兑换、三小图不按颜色/顺序绑定物种的边界全部保留。最高NEXT83回早期具名任务/地图生态或有同版实参音效，不连扩付费商品；Stage A7 PARTIAL+2 OPEN，B/wiki GATED，savedata R79 PAUSED_NON_BLOCKING，历史旧全文不删。


## 2026-10-23 R83：强恩一族家庭选择、三口令与来源分域洞窟生态

按新远端main491d43c2b0aad5f9231da806205576f050a21825/tree66f6e049bc5aea45f07296e637024fcaeb5ffc1c启动，489分支/0开放PR/运行中Actions，旧queued37642417333继续单列不动。前轮最终候选10/main11实际completed/success。八启动文件完整UTF8/精确git show/原生Git一致，CURRENT2415368B/SHA256526c37ea41995311f5f4655e1bcda343a0daa5175a6714acc4ac408fb2362f1a，旧全文前缀保留，无AGENTS。读最高NEXT83/22域后转早期具名世界任务，不重开暂停savedataR79。查成人仪式已有规格保持关闭不重复计新成果；强恩/卡娜木笛未有独立规格，未采用现代私服主表。

交付STONEAGE-CN2003-QIANG-EN-FAMILY-SOURCE-CONTRACT-R1及SOURCE/工具/专用工作流。S1新浪《石器时代》任务功略-强恩一族，标2003-05-30 10:17/新浪游戏/网友投稿，无具名作者；https://games.sina.com.cn/zhqu/sta/article/2003-05-30/9898.shtml 当前200无跳转54963B/33b20cfa59c64834592247eb21aad0a457d5dfa65a0dd532f2a108280c3dc60f。S2南岛座标标2003-04-03 14:19，同门户/投稿，https://games.sina.com.cn/zhqu/sta/sqdt/sqdt_2.shtml 71509B/521512039fd1edefd36581e315a52b566f73b90f5673d0211557df6c80f3f727。严格GB18030零替换；非直取运营作者/认证2003原字节/精确build，两同站页不称独立见证或同版。S1业务2143字符/6135UTF8B/a88a3b5b2f3ef45664dd62b2d4f2c5d5f9b9860ad302bec9cf8d5ef165f6c1ee；S2只洞窟主行258字符/402UTF8B/5bc777ad65d017d71fcd1f0935a5d1c0f4097d6e9f0b4e65a200d35a05ca77e5，均独立去标签/实体归一逐字核对。

恢复凯伊（吉德的朋友58,66）给花→村长家深处吉德→未具名儿子给母亲发饰→沙拉→转告强恩女儿选择→给双亲的信回吉德→卡娜木笛的文献任务流。强恩68,7/妻70,8愿尊重女儿，沙拉选择留下养育家庭，不是强制护送回亲生父亲；母亲已亡/信名给双亲不冲掉叙事。16年前绑架、当时四岁、母亲两年后逝为所述相对时间，不推当下年龄/历法。卡那/卡娜、阿尔鲁山南侧/阿鲁姆山字串分别留，不强别名。村140,1007与124,1048不赋入口出口，50为建议、不补成人仪式或无任何前置；羽毛无只本指南栏。

洞口285,926，三层出口4F11,54红色月亮的光芒/5F51,5蓝色山脉即力量/6F8,23白色之风即速度逐层关联。四层以后随机伯恩/玛琼拉/卡鲁德可能掉盗贼秘密文件，明确直接说口令即可、不必有文件；七层固定三人联合战与随机遭遇分开，不补掉率/原实例ID/消费。强恩随机一道具，羽饰只是一次样例；吉德木笛魅+2毒+5石-5眠+5复活精灵Lv2，缩写不补免疫百分比/伤害/已发生效果。原任务flag/ID/重做重置/物品消费/服务器事件仍OPEN。

S1敌Lv31–48/六标签，S2Lv30–40/山贼、59.齐尔格尔顿、72.格鲁西斯分域存；59/72不当原宠ID，格尔顿不强合齐尔格尔顿。S2地上8楼/13条带方向层间坐标保留，不自动反向；S1只列1–7楼及沙拉房图未说共七楼，不宣称已证冲突或房间为8F。与R81北岛梦德仅正文文本关系，不合原阵营/前置/领奖序；琉璃家庭故事不挪入本篇。

20实际全图/缩略对只取009沙拉和012木笛。I1 87716B/5e57c456dd9b0cf648e91eca585f6958a704ef14643c2b1a08c01fa546f941e7、I2 116396B/68a756ea81d19f4cc63d006c2222defa04a8577832cf5ac05dc12ba2da8550d6，均200无跳转JPEG/RGB640×480单帧完整解码/目视。I1石屋床桌人物/沙拉标签，无选择对话；I2物品说明数值吻合且吉德标签，静态图不证明原NPC ID/发奖/效果/历史原像素，原HTML/JPEG不入Git，其余18图不取。

18完整文献目录（任务1、故事NPC6、口令守卫3、战斗组1、地图1、物品流4、屏幕2）七必填/19集合核验，非18原实体。三父报告/共享解析器原字节固定，34去全部指纹门语义改写、隐藏/正文外2+地图行外1反例、两外围script正例。首次本地修改生成后语义摘要校验报错，独立重算磁盘摘要一致后重新运行七单元/原输入回放通过；不抹除该本地失败，远端验收待后验。停止于两指南两图，重开须同版原脚本/ID/认证像素或实服交互证据。

最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-84转另一地区早期具名宠物/生态，或有同版实参的音效资料，避免连续大陆洞窟/helper扩张。Stage A7 PARTIAL+2 OPEN，B/wiki GATED，savedataR79 PAUSED_NON_BLOCKING，无整体百分比，历史旧全文不删。


### R83双端实源验收与永久派生保管（2026-10-23）

内容64553597373015c99b90c1d2953b31230d3e835b/treec82760bc9c68e592b6099568198bfe9196a69d2d，候选10/main11实际completed/success。九文件原生Git blob及整tree逐一一致，四连续性旧全文前缀完整；新读main旧HEAD后expected_sha非强制快进。专用候选run39902606043/job120247332480/artifact12479626746，主线run39902723105/job120247695519/artifact12479800876，实际日志各七单元、两HTTP正文/两全JPEG实取解码、34去全部指纹门语义改写、隐藏/正文外2+地图行外1反例及两外围script正例通过。

两ZIP各6599B，SHA2563ddcef8c9ca7d5d3b5240a3169f3355e50692af8714c98dc2bc0c5e33561e634 / 1e3812f798ab2f32549a95287ea520b77f56cd935bb48c77b3f9b49d94da51bc分别符合API。唯一replay.json各43717B/SHA25693907315f3d9a34af6899f1a240fc379861486f1c098c09b6fa22d12747a83d8，候选/main/local/保管门后local四份逐字节相等，四实际HTTP输入摘要均同初取；这不认证2003原文/原像素、同build或两独立作者。

双原CI JSON与STONEAGE-CN2003-QIANG-EN-FAMILY-CUSTODY-R1.json永久入Git。七pin固定SOURCE、三父报告、共享解析器和双原报告原字节/SHA256/Git blob。收据保存21真实run、准确双run/job/artifact、ZIP与raw/input初取历史。CLI强制保管，固定完整run清单摘要、实际run/job/artifact和ZIP长度/摘要，拒绝缺失/同长篡改、错HEAD/tree/分支/任务/ID、门遗漏重复或成功门替换、工件复用、虚报输入相等及抬高历史/官方/原服权威。新增第8保管单元，本包8/相关22本地通过，原输出字节不变；内容CI原七单元历史不改称八单元。保管提交自身候选/main另实后验。

本轮交付18条可查询文献记录和家庭选择/口令/可选文件/道具流/分域生态规格；原任务引擎、flag、ID、原模型及实服发奖仍OPEN。保持沙拉自主留下、母亲已亡、羽饰非保证、木笛缩写、两地名/母名异写、三层口令关联、方向坐标与两页敌Lv范围，S1七层截图不当总七楼。下一最高NEXT84转另一地区早期具名宠物/生态或同版实参音效，不连扩本洞窟helper；Stage A7 PARTIAL+2 OPEN，B/wiki GATED，savedataR79 PAUSED_NON_BLOCKING，旧历史全留。


## 2026-10-23 R84：台湾宠物进化史的融合蛋孵化流程与身份未知

按新远端mainaaf30a6f9753936e85f46ac4181fb1c31a9f6df3/treee492fed4b65f156cb2a6f2100cad4d0c7bc6832b启动，491分支、0开放PR/运行中Actions，仅旧queued37642417333单列不动。前轮最终候选10/main11实际completed/success。八启动文件完整UTF8/精确git show/原生Git核对，CURRENT2422321B/SHA2565607c85245270eae9dd9bd011b1bcf8fc4687624d23d3bd4c7288b49d89bdd0e，22域SOURCE-READY-PORTFOLIO-R2全文15948B/7d50de08f7855cf16dbe54b1747e258f1cc1223de88cc217172fd145f3c704ce，历史前缀全留，无AGENTS。按最高NEXT84转另一地区早期宠物材料，不重开R79或连扩强恩洞窟。初日服/台湾宠物检索未得到同版原物种表，转实际可取的2002台湾融合报道；不把发现级现代私服/编年史当原数据。

新增STONEAGE-TW2002-FUSION-HATCHING-SOURCE-CONTRACT-R1、SOURCE/工具/专用工作流。GNN《許慧欣見證「寵物進化史」》标2002-11-14 21:41:11，GNN记者未具名。https://gnn.gamer.com.tw/detail.php?sn=6751 网页读取器403，未取得当前正文、不预称相等。一次Availability以20021201查询，实际返回20190821163207，取https://web.archive.org/web/20190821163207id_/https://gnn.gamer.com.tw/detail.php?sn=6751 ，200无跳转26265B/c9bbe57924b5f3e8fa69ee1494d53934b07d7181926ef9b24166688629add7a9，严格UTF8。2019捕获不是2002原字节/上线日/build，台湾市场归属是语境判断，非直取运营发布稿。正文四段405字符/1211UTF8B/26ef0acd0cba5a0efcb7cd56eea80c78f4bdd9592ad8eb22840a061a59679206，独立去标签/实体归一逐字一致。

恢复文献链：三只不同的宠物＋特殊药材→一枚宠物蛋→特殊饲料孵化→新第三代宠物。不同不擅定为三物种，也不补性别/等级/转生/亲缘条件；药材/饲料只是原文泛称，无原名/ID/数量/配方。不能捕捉或任务取得仅所述将推出第三代，不扩成全宠；第三代不当第三代血缘，前二代不对应1.0/2.0客户端。正文只具名“石器時代-寵物進化史”、未写数字5.0，不倒填后期编年史。引言推出/细段将推出语气分存，不推部署时刻。输入消耗/失败概率/喂食间隔/孵化总时长/离线计时/蛋槽位交易保存/子代物种继承与组合算法全部OPEN。

柴垣秀樹是文中归属的华义聘日本设定画家、第三代造型设计，不认MMO唯一作者或已得原设定稿。许慧欣与《連接》是代言/广告曲语境，非游戏BGM或融合孵化音效；未提取歌词/音频。不以广告曲重开声音底层。与JP2008进化的试炼、四剑齿虎、失败Lv1、付费保障票分开，与TW2002狼人战斗变形/卡牌两兽不合融合输出；共同画家名字不证明同原资产ID。另发现数字之墙2002宠物日志包企业稿，因商品/SBC/刮卡非本流程证据不纳入规则，也不研究实体光盘。

正文实际8条无图注S图库，取第1/8两张当前120×120照片。I1 12389B/bfa82936606a9207af6484866c20325b5893461233792a13ebdfa02ce56d4b1c，舞台多人持萨克斯；I2 12778B/826855871234f9d260ca58511a269d289c36248a6bc1e7433fa87e50ecd5e6f0，一人与两侧扮装人物。均200无跳转JPEG/RGB单帧完整解码/目视，非宠物模型/游戏画面/融合实录，不按扮装/次序认物种或仅像素认证人名，现像素不认证2002原图。另六图未取、不猜B大图；原HTML/JPEG不入Git。

9完整研究目录=版本1/未具名宠类别1/流程1/泛称材料与蛋3/设计广告边界教程1/照片2，具名新物种0，不当9原实体。七必填/19集合核验，三父报告和共享解析器原字节Git固定；19去全部指纹门真实语义改写、隐藏/正文外2反例和外围script正例，本包七单元/原输入回放通过。工作流复用时旧名称/三图文字未替换，在提交前审查修正，未产生错误远端门。候选/main和永久保管待实际后验。

停止于一存档两照片，重开需同地区版本原材料/宠物主表、具名原画绑定、配置或实服流程。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-85回大陆以外具名世界任务/场景NPC、早期宠物生态/资源身份或同版实参音效，优先具体身份，避免连收无名宣传。Stage A7 PARTIAL+2 OPEN，B/wiki GATED，savedataR79 PAUSED_NON_BLOCKING，无整体百分比，旧历史全留。


### R84双端实源验收与永久派生保管（2026-10-23）

内容c1bec4061c26d83835757a650673a5b859881e18/tree6706e55c087a6622b2a1fd81177057fd77a30462，候选10/main11实际completed/success。九文件原生Git blob及整tree逐一一致，四连续性旧全文前缀完整；fresh main expected_sha保护非强制快进。专用候选run39903937009/job120251467895/artifact12479469761，主线run39904047488/job120251808268/artifact12479568177，日志实际各七单元、精确2019存档/两当前小JPEG实取完整解码、19去全部指纹门语义改写/隐藏正文外2反例/外围script正例通过。没有重新查Availability或声称已取当前403原文。

实际两ZIP各3839B，SHA256cf8fa208414c3f505502fc09050faaec289990aed415299f42ae5e7f5af7aa9e / 5674174133cda9231d48d934b7ba71f149bcf22ccd7e552e2c24a669e3e7d0f4分别符合API。唯一replay.json各17341B/SHA256d0c47d27314e14c05fa061df96112250cec0abc0b548e969cb6028235b619baf，候选/main/local/保管门后local四份逐字节相等，三实际HTTP输入摘要同初取；不认证2002原字节/照片像素/精确build/实服融合，也不虚称未取当前GNN正文相等。

双原CI JSON和STONEAGE-TW2002-FUSION-HATCHING-CUSTODY-R1.json永久入Git；七pin固定SOURCE、三父报告、共享解析器、双原报告原字节/SHA256/Git blob。收据保存21实际run、准确双run/job/artifact/ZIP/raw/input初取历史。CLI强制保管且固定整清单摘要/实际ID/ZIP长度摘要，拒绝缺失或同长篡改、错内容HEAD/tree/分支/任务、遗漏重复或成功门替换、复用工件、虚报输入相等/捕获即刊时/全图与当前正文已取得。另明确拒绝抬高官方/原服/历史权威，或将未得物种身份、融合公式、游戏音效绑定改成已证。新增第8保管单元，本包8/相关28本地通过，原输出不变；内容CI七单元历史不改称八单元。保管提交自身候选/main另实后验。

成果是具名版本报道下三宠/药材→一蛋→特殊饲料→第三代的文献流程、9研究目录（新具名物种0），不是原融合引擎/成长或组合公式。三只不同不强解为三物种，第三代不当血缘，未来语气不当开服日，柴垣设计/广告曲/扮装照片不补原宠模型或声音调用；日服2008试炼与台湾狼人/卡牌不混。最高NEXT85优先另一地区具名世界任务/场景NPC、早期生态/资源身份或同版实参音效，避免连续无名宣传扩张。Stage A7 PARTIAL+2 OPEN，B/wiki GATED，savedataR79 PAUSED_NON_BLOCKING，所有旧历史完整保留。


## 2026-10-23 R85：日服GW两层集章任务与具名モモトラ奖励

按新远端main9b59a8cda968bedf699262d0be2c6137e529a60d/tree5073c3c3d1bbfefbcd253dabcd73c9736e9c5131启动，493分支/0开放PR/运行中Actions，仅旧queued37642417333单列不动。前轮最终候选10/main11实际completed/success。八启动文件完整UTF8/精确git show/原生Git核对，CURRENT2429354B/SHA2561ab67e32d86d97e1f909946c06e583ab7fd926df1d18c9582946c3e7cf6547db，22域SOURCE-READY-PORTFOLIO-R2完整重读，原历史前缀全留，无AGENTS。最高NEXT85优先具体身份，选择日服2005集章任务与明确モモトラ奖励；远端规格未有该名/活动，不重复旧成果，不重开R79。

新增STONEAGE-JP2005-GW-STAMP-RALLY-SOURCE-CONTRACT-R1及SOURCE/工具/专用工作流。一篇4Gamer同期报道https://www.4gamer.net/news/history/2005.04/20050415190236detail.html ，可见2005/04/15 19:02/Seirou，点名ガイアックス、移管自ボーステック；非原样运营发布稿、未取原活动详情，当前200无跳转16431B/4e6c10774e52aba19737ca22cd9899c8c066e0fce49022a8a11c645802549f3a，严格Shift_JIS。五模板槽一非空，核心止记者签名389字符/1101UTF8B/b89a6f3a4bfb691928a78855d21b0ae312a195d5408dcdcf3d9f608b9283d470，独立去标签/实体归一逐字一致。当前字节不认证2005原件/精确build/原服执行。

恢复ストーンエイジ・GWスタンプラリー的4/28—5/10计划（2005刊时语境），普通お楽しみ面向所有玩家、访问四未具名村集章，奖励Lv1ペット モモトラ，文本明确粉红虎型/等级1；进阶チャレンジ面向中级以上、游历世界集章，推进须先完成普通任务，奖励未具名GW限定物品。数字等级、四村名/原地图/NPC/坐标/路径、精确印章数或其是否道具、奖励数量/效果/ID/重做重置/消费保存均OPEN。前置不是只访问、仅领奖校验或自动开挑战；所有玩家不补服务免费/无任何原服条件，限定不推过期消失。モモトラ不按中文别名强合初代物种，属性成长技能/元素/原SPR/野生栖息未得。

与JSS2001四村会场对照不因同数字四而搬村名/接待NPC/方向坐标；同年寻宝光精灵/结晶掉落/交易重复规则不挪到集章。现代页尾免费不补2005资格。一实际全/缩略链接只取_0big.jpg，未猜其它序号；I1 200无跳转534047B/455b747ed9f0912672a238101b4e17b5469d40e81cef6ac6cc35e583f544bab6，JPEG/RGB640×480单帧完整解码/目视，是草地石路桥水、多人物/宠物聚会，不是具名モモトラ特写或集章实况。底部七导航标签マップ/ステータス/ペット/アイテム/メール/アルバム/システム仅可见标签，未点开/验证功能；无图注/宠物名/任务字、无发奖证明，不认证原像素/原模型或客户端原生分辨率。原HTML/JPEG不入Git。

6完整研究目录=活动教程1/任务2/具名奖励宠1/未具名物品1/画面1，七必填/19集合核验，不当6原实体。三父报告/解析器原字节Git固定，15去全部指纹门真实HTML语义改写、隐藏正文外2反例/外围script正例，本包七单元/原输入回放通过。初试正文one匹配遇五模板槽失败，改唯一非空；首语义改写用去标签串而原A标签隔开导致失败，改真实HTML锚后通过。两本地失败不抹除、不冒初次已过；尚未产生失败远端Actions，双端取源/保管另后验。

有限止点一文一全图，重开须原活动详情/脚本、四村/NPC、具名宠设定或同版资源/主表/原服轨迹。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-86回早期明确地图/生态或同版实参音效，优先具体身份与世界故事，不连扩节庆/奖励宣传或无名截图。Stage A7 PARTIAL+2 OPEN，B/wiki GATED，savedataR79 PAUSED_NON_BLOCKING，无整体百分比，旧历史全留。


### R85双端实源验收与永久派生保管（2026-10-23）

内容c323190544a2cd55bcabae410e2cb94aedbe2799/tree27955abc4e53869277a925c142807561b7ea9ad7，候选10/main11实际completed/success。九文件原生Git blob及整tree逐一相符，四连续性旧全文前缀保留，新读main后expected_sha非强制快进。专用候选run39906959724/job120261013195/artifact12481033475，主线run39907102925/job120261458913/artifact12480943950，日志实际各七单元、一篇当前旧报道/一实际全JPEG实取解码、15去正文指纹语义改写/隐藏正文外2反例/外围script正例通过。

两实际ZIP各3013B，SHA256caeef6e0fab43f2e6c52d70dafb8547904fabf7784eb60551d723a214d5f1928 / 97940f9df0d272562412d47a975532d8bb7551bd99cda9f2c0fa192637bc595d分别符合API。唯一replay.json各12118B/SHA25673ec96fecc759e454ec739927c9e9ad9609e87d40e63177e1ea095f779059aa1，候选/main/local/保管门后local四份逐字节相等，两HTTP输入摘要均同初取。当前报道与JPEG相等不是2005原字节/原像素/原服发奖或活动已执行。

双原CI JSON与STONEAGE-JP2005-GW-STAMP-RALLY-CUSTODY-R1.json永久入Git；七pin固定SOURCE、三父报告、共享解析器和双原报告原字节/SHA256/Git blob。收据保留21真实run、准确双run/job/artifact/ZIP/raw/input初取历史；CLI强制保管且固定整清单摘要/准确ID/实际ZIP长度摘要，拒绝缺失/同长篡改、错HEAD/tree/分支/任务、遗漏重复或成功门替换、复用工件/虚报输入相等或提升原服/历史/运营详情来源权威。还明确拒绝将截图认作モモトラ、把导航可见当交互已测或把未得宠物原数值/ID改成已证。第8保管单元加入后本包8/相关28本地通过，输出原字节不变；原内容CI七单元不冒称八单元。保管提交自身候选/main另实后验。

补查现有官方124网页宠目录/研究JSON，无既有本活动/モモトラ规格命中；一次精确名称检索仍仅得到同一4Gamer文章及无关结果，不作全网穷尽证明，也不计迁移ddo主机为第二独立来源。没有新增原设定图/绑定，不以颜色指认截图宠物。

本轮交付两具名任务的完成前置、具名粉红虎型Lv1モモトラ奖励、6文献行和七可见导航标签，原宠表/任务脚本与执行仍OPEN。四村不因数字四强合JSS出生村，中级不补数字等级，挑战未知奖励不改作宠物，图片不证明任务/发奖或交互。最高NEXT86回早期明确地图/生态或同版实参音效、优先身份与世界故事，不连扩节庆/奖励宣传。Stage A7 PARTIAL+2 OPEN，B/wiki GATED，savedataR79 PAUSED_NON_BLOCKING，旧历史全文完整。


## R86 — 2026-10-23 CN2003 拉多拉／巴那姆／深红地理生态（内容候选，待双分支验收）

FACT：本轮从新读远端 main `a16fde079936e9fd893f68e8b2941162b7b33030`、tree `85386d8acd448bdc9a8619085022e158019ec285` 启动；495个分支、无开放PR及运行中Actions，旧排队run37642417333未触碰。上一轮候选10／main11检查均成功；八份连续性文件完整读取并与fresh checkout逐字节比对。CURRENT旧前缀2435984 bytes，SHA256 `138babb2a3a29f30bbda5edd9a78e3dcecd3e79ae2e98a2b3f3303cd04de228f`。最高优先项 OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-86。

交付：`research/recovered/STONEAGE-CN2003-LADORA-CRIMSON-SOURCE-R1.json`，SHA256 `98cacbd0c24d93fe1f2c8f1a969a678dfd8ab8c237375c01664e84fb15f1f051`；专用工具／测试／Actions：`stoneage_cn2003_ladora_crimson_source`。版本范围 CN_SINA2003_LADORA_CRIMSON_GEOGRAPHY_EXACT_BUILD_UNKNOWN，仅选取同一2003年门户攻略的地理、生态和世界叙事段落，停止于1页＋1张实际链接示意图，不扩大音效helper。

来源：https://games.sina.com.cn/zhqu/sta/article/2003-06-09/11645.shtml ，标题《石器时代》任务功略-深红洞窟，显示2003-06-09 14:03、作者字段新浪游戏、我要投稿链接，未署名原作者，不认证官方脚本。当前GB18030严格解码59256 bytes／SHA256 `684983365e929e42d7987e86f962ca2d7641e6185c98464cd4788023909fe3ae`，HTTP200无重定向。实际图 `https://image2.sina.com.cn/gm/newgames/0303/images/tuxing0610_03.jpg`，22812 bytes／SHA256 `15f3e751a5828d906815e2b3d514e0d9940e87c52cb2f605789dcd7b2183e9ef`，Pillow完整解码JPEG RGB500×236、单帧，已人工查看。

实质新增：四条登顶路线各3条有向边，7条按正文出现位置分开的地理／生态记录；世界坐标、回廊内坐标、巴那姆地下2楼内坐标分别保存。两个巴那姆入口(295,259)/(388,337)，两个深红入口(45,41)/(26,5)，格鲁西／格鲁西斯原样分存。怪物等级和种类仅为攻略陈述，非可捕宠物主表。吉鲁火山、百余年、伊拉祈祷和不死鸟以奇宝形体现身／被发现后换山顶为世界故事与指南描述，非地质模拟或已观测服务端机制。

图像是路线示意图，非游戏运行截图；8个印刷节点含c120302、c120303、c120306、c120305、c120304、c120308、c120307、c120309及10条箭头单独记录。图共用c120309山顶标签与正文“四座不同山顶”并存，原生地图ID、实例数及几何均OPEN。四洞口与四路线不强行一一映射，推荐80级／成人仪式仅保留关联任务表头语境，不提升为全图准入。

10条目录记录满足7必填字段／19合法集合；game_ids空、仅研究元数据非发行授权。三个父规格和共享解析器钉原始bytes／SHA256／Git blob。41项真实HTML语义改写（排除所有指纹）＋2项隐藏／正文外反例＋外围脚本正例；独立regex/entity生态读取一致。初始本地26项关联测试成功，源回放成功。原始HTML和图像留临时目录，Git仅派生JSON。完整两支任务、送水7/7奖励表、其他配图、本服运行、版本号和原始地图／宠物ID均未恢复。

NEXT：内容候选10项成功后以fresh main expected-SHA非强制快进，再核main11项；永久保存原样CI JSON和完整run/job/artifact/ZIP/raw/blob保管链，加入强制缺失／等长损坏／身份替换拒绝测试，再验收保管链候选与main。阶段A仍7PARTIAL＋2OPEN，阶段B/wiki GATED；savedata R79 PAUSED_NON_BLOCKING。之后 OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-87 优先具名宠物／人物原始内容或具体原始UI交互证据，避免连续扩洞窟路线；若找到同版本实际audio调用实参才重开音效依赖。


### R86 内容双分支实际验收与永久保管链 — 2026-10-23

内容提交 `3c0b80a38ad7cdfc2604496681020b4a7ad126f0`，tree `e4be822c5f6e2e594103d896ca7511deb2b73f72`；候选10／main11共21个实际Actions全部completed/success，专用job初始7tests成功。

candidate: run39934221560／job120349672167／artifact12492434392，ZIP4125 bytes `sha256:369e57a355b72c5795201f05ec71b9b53d3448259546739879e4c041894ea998`；原样JSON28147 bytes SHA256 `4c84646a0e36b39fe938ccf08cb07a036d3296cc658176e3a06b9da6467f2fa9`，Git blob `55cf00fe36db65e10a79079a4c92c59e38340c75`。

main: run39934550590／job120350775724／artifact12492594617，ZIP4125 bytes `sha256:46eea10ea08ed5f94b55df2cb8b2a3b7415ee2a07435863536fede12b767b414`；原样JSON28147 bytes SHA256 `4c84646a0e36b39fe938ccf08cb07a036d3296cc658176e3a06b9da6467f2fa9`，Git blob `55cf00fe36db65e10a79079a4c92c59e38340c75`。

两个ZIP均实际下载核对GitHub digest与长度，成员仅replay.json；CI原样JSON与初始本地回放逐字节相同，输入当前原页／JPEG bytes和SHA256一致。永久保存CI-CANDIDATE、CI-MAIN、CUSTODY三个派生JSON（原始HTML/JPEG不入Git）；收据固定全部21run清单摘要、两个真实run/job/artifact、ZIP长度/digest、raw字节SHA256与Git blob、7份永久证据pin。CLI强制校验；第8项测试拒绝缺失／等长破坏／run和job替换／重复清单／ZIP身份变化／原生ID或运行覆盖抬高。保管链候选及主线仍须按实际Actions再验收。

NEXT最高 OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-87：优先具名宠物／人物内容或原始UI交互证据；版本／本服运行／可捕性仍OPEN，阶段B/wiki GATED，savedata R79保持非阻塞暂停。


## R87 — 2026-10-23 JP2005 宠物图鉴的画面登记与两阶段更新

FACT：按新读远端main `cf52a0a35ea7d4f13e24b1ff17abfefd4ebb16a0`／tree `2dd6065ef8fa7c3d44f6540a385893bd3e84c54c` 启动，497分支、0开放PR／运行中Actions，上一轮最终候选10/main11实际全部成功；旧queued37642417333单列不动。八启动文件严格UTF8完整读取并比对fresh checkout原生Git；CURRENT旧全文2441519 bytes／SHA256 `27cc3dadfee0ef9794f3170f0b8645b4cede828dae8ac00d7472e6530240cc18`，无AGENTS，22域索引全文核读。按最高OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-87转具体图鉴交互文献，查JP2004展示宠物和CN2003操作已有规格，不重复计新结果。

交付 `STONEAGE-JP2005-PET-ENCYCLOPEDIA-SOURCE-CONTRACT-R1`、SOURCE JSON、专用工具／测试／工作流 `stoneage_jp2005_pet_encyclopedia_source`。只选2005日本GaiaX运营时期报道，不认证1999／TW1／CN1.82同build，也不把新作StoneAge2的Pal图鉴规则挪入。没有同版audio实参，不重开音效helper或savedataR79。

来源 https://www.4gamer.net/news/history/2005.07/20050705162235detail.html ，标题ガイアックス，「ストーンエイジ」で新ペット恐竜を実装，显示2005/07/05 16:22，署名TET。当前200无跳转17834 bytes／SHA256 `983b11f84dd9c492c4b868bc96921fecbbb582e87a6243c322c9f8ad684f06b9`，SHIFT_JIS严格解码零替换。为同期记者报道，非原样运营公告；当前字节不认证2005原字节，原更新页／脚本／精确客户端未取得。

实质规格：7月5日定期维护后补新宠及同种野外怪物图形、扩充宠物图鉴；7月12日维护后补此前未出现的Lv.1野外恐龙并改部分配置，明确新恐龙实际登场在第二次补丁后。图形存在不等于已在世界启用，不把“此前未出Lv1”扩大成全游戏首次有Lv1，也不补物种数／具体地点／刷新率。两阶段部署与事件仅为所报／所计划，不是实服执行验证。

图鉴正文明确：新宠显示在画面上→该新宠的名字登记于ペット図鑑。此句不以捕获／拥有为触发，不把名字登记当得到宠物或全属性／技能已登记；其它必要条件、全部旧宠适用、精确按钮与版面、持久化、重复处理与存储仍OPEN。7月12日22时前后GM展示为计划与约时，无精确分秒／时区；寻找GM是指南建议，不当只有GM展示才能登记。与CN2.0“曾拥有宠可拍照”的相簿描述、JP官方网页宠物目录分别存，不互补规则／不当同一UI。

实际配图只有正文链接 `/news/image/2005.07/20050705162235_0.jpg`，3371 bytes／SHA256 `81a547ca33684426e6c9b42fcace9850e543955b379d49487d2da6d276383394`，200无跳转，JPEG RGB96×104单帧完整解码／目视：浅蓝甲壳蟹形小插图、黑底，无物种名／图鉴UI；不猜_big图，不认作原SPR／动画／某具名物种，不因一图宣称只新增一宠，不认证历史像素。原HTML/JPEG仅临时保存，Git为派生研究元数据。

5条目录记录：两阶段教程＋登记规则教程＋计划GM展示教程＋未具名插图，7必填／19合法集合、game_ids空／非发行授权。三父报告及共享解析器固定原bytes／SHA256／Git blob。独立regex/entity正文逐字一致，19项真实HTML语义改写排除全部指纹门、2项隐藏／正文外反例及外围script正例通过；初始本包7tests及关联回归、源回放通过。止点一报道一实际小图，重开需原操作视频／同build脚本或具名图像／数值绑定，不靠更多匿名宣传图扩张。

NEXT：候选10/main11实际成功后永久保存双端原样派生JSON与准确run/job/artifact/ZIP/raw/blob收据，强制保管链校验并再验收。最高后续 OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-88 优先早期具名人物/NPC对话或具名宠物属性的原始证据，不连扩匿名插图或奖励宣传。阶段A仍7PARTIAL＋2OPEN，B/wiki GATED，savedataR79 PAUSED_NON_BLOCKING；无整体完成百分比。


### R87 内容双端实际验收与永久派生保管 — 2026-10-23

内容提交 `7c734e08fc53540045063816409484c8133732df`／tree `8cc44097da5c022ef12e488ec72156411b1b7e7f`，候选10/main11共21个实际Actions全部completed/success，专用日志初始各7tests成功。

candidate: run39935988520／job120355531891／artifact12494111171，ZIP2720 bytes `sha256:0179f8b274a1003612b70f36cab4355ecd3fb257c7d731fcdf8642c8ed8169a4`；原样JSON10170 bytes SHA256 `c1f6ba1456c16a9cd5479deb43456d00e14f03e10c2f352eb13451ea32fdaaa5`，Git blob `b0142336c98750fc831b753179c7a23e5e3d56e1`。

main: run39936177726／job120356148265／artifact12493847454，ZIP2720 bytes `sha256:d65293c7d90e418f886c28c56698424e73bbc5d4d89c3c1fb8ec65f8f5c3815d`；原样JSON10170 bytes SHA256 `c1f6ba1456c16a9cd5479deb43456d00e14f03e10c2f352eb13451ea32fdaaa5`，Git blob `b0142336c98750fc831b753179c7a23e5e3d56e1`。

双ZIP已实际下载核GitHub长度与digest，唯一成员replay.json；候选/main/初始local的原样JSON与两个实际输入bytes/SHA256一致。双原CI派生JSON及CUSTODY永久入Git，原HTML/JPEG不入Git；7份证据pin固定SOURCE、三父、解析器和双原报告bytes/SHA256/Git blob。收据与代码常量锁定完整七pin清单摘要，反例同时改证据与重算receipt pin仍拒绝；收据锁定21真实run清单摘要、准确双run/job/artifact及ZIP摘要；CLI强制保管，拒绝缺失/等长篡改、run/job/artifact替换、遗漏/重复/复用工件、虚报原输入相等及历史/本服权威抬高。第8项专测还拒绝插图指认物种、图鉴实际交互已测、名字登记等于获得宠物。保管候选及main自身仍须实际后验；原内容CI7tests历史不改称8tests。

交付为文献中的画面显示→名字登记与两次更新范围；没有运行原服/完整图鉴数据/宠物原属性或UI画面。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-88优先早期具名人物/NPC对话或具名宠物属性，避免连续匿名插图/奖励宣传。Stage A7PARTIAL+2OPEN，B/wiki GATED，savedataR79 PAUSED_NON_BLOCKING。

R87保管门本包8项／关联24项本地测试成功；CLI原输入回放与初始输出逐字节不变。完整七pin身份摘要另固定在代码常量中，连同篡改证据后重算收据pin的反例一起通过。


## R88 — 2026-10-23 伊甸动物园：具名NPC条件、拉斯基状态样本与交还顺序

FACT：按新远端main `7b358092650612d506b2a29cd5c8be7715186d53`／tree `47327c3c7d841ceb1ff19101f0ee67cd52bbd1c1` 启动。499分支，无开放PR／运行中Actions；上一轮最终候选10/main11全部completed/success，旧queued37642417333未动。八启动文件完整严格UTF8读取并与fresh checkout精确git show一致，CURRENT旧前缀2447908 bytes／SHA256 `afc036e02ff0f1fbd7199331217400d5751e6869cec3ec0af94134062bc101da`；全tree无AGENTS，22域索引全文读取。最高OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-88转具名NPC／宠物属性证据，网页宠物目录已有同名项但没有本任务规格；不以同名强接原生实体。

交付 `STONEAGE-CN2003-ZOO-RESCUE-SOURCE-CONTRACT-R1`、SOURCE JSON（SHA256 `bf37d19e3f88b711483289dd1b17255925d0bfcdbbbe64bea52f13815f7b2ca6`）、专用工具／7单元／Actions `stoneage_cn2003_zoo_rescue_source`。范围一篇同期攻略＋两张实链全图；完整记录本文所述救援流程，不宣称恢复原任务脚本／原服执行或全部版本动物园。

来源 https://games.sina.com.cn/zhqu/sta/article/2003-06-03/10646.shtml ，《石器时代》任务功略-动物园任务，显示2003-06-03 17:58、作者字段新浪游戏／我要投稿链接，无具名原作者。当前HTTP200无跳转72640 bytes／SHA256 `e92f92126182fb0834f7ec329a615cb1b7629e54da1de1943dd016af828ad046`，GB18030严格解码零替换。门户攻略不是经认证运营脚本、2003原字节或确切build；伊甸与尼斯语境分别保留，不反投TW1.0/CN1.82或混入2024手游复演／私服。

具名流程：沙利斯园长委托找雷尔胖／波波顿／拉斯基；布伊太郎饲料与雷尔胖鉴定，蓝色目标75,170不是任一布伊胖；波波顿170,181仅指南所述等级1，经鲛岛太郎鉴定。一次一种正确饲料为攻略建议，混带“很难遇见”不写成零概率；先打一击建议不变捕获公式。推荐90非硬门槛，完成金飞为本文前置，不展开另一任务。雷尔大人是故事中的园主／宠物主人称谓；贝壳及三出处只是正文关联，不补消费或已完整恢复其余两条支线。

里拉拉22处、伯特5处表格逐行解析，里拉拉末6处室内坐标分别保留，不能并进同一世界坐标；里拉拉81,69／伯特171,72的“服务器重开机”注记只是指南声称。伯特按所列顺序走为描述，无周期秒数／已测重启算法。伯特、铲子、啦啦口令与白萝卜／红萝卜3／柯奥红萝卜4交换上等白萝卜相连；不太差／还不差异写不强原物品别名。保留铲子落地消失及可重领、萝卜落地消失、见兔前丢铲子、带铲子或红萝卜时连上等白萝卜被收走的本任务条件，不泛化全局道具规则。

里拉拉前五次及后续叙事分别存，“再找”不捏造第六个服务端flag；啦啦是里拉拉口令，拉拉是它所述拉斯基别名。林务局是误导线索，项圈→再问南边雷尔大雕像→黑色的服→动物园后方藏身处／4楼黑色的旗→5楼席格逐步关联；不给掉率／保证掉落／原消费flag。席格为塔尔塔战士团寻老团长、乔装救动物的角色叙事，“动物园是驯兽中心”为其怀疑，兔子释放计划不是他们的安排。

四组敌人资料按场景存原标签、以上下界和区间、技能文字。林务局与洞窟格尔希洛不能合一套数值；正文称后者较不凶悍，与各自数字分别保存不强协调。席格两项攻击力500／700照录，防御力未知，不擅改700为防御。洞窟总览0,64与一楼入口20,64并列OPEN，四层各入口／出口不强反向或接原地图ID。

领奖关键顺序：先把救出的拉斯基带给里拉拉报平安，再向园长交还三宠得到一只“刚出生”的布伊胖；随后以咬过白萝卜换铠。遗漏前置报平安会失去铠的提示单列；不将布伊胖“刚出生”推成已证数值Lv1。铠原称防+40敏+10、恩惠的精灵Lv4，实际发奖／精灵效果未测。

26实际全图/缩略对中只取08和020，其余24全图不取。I1 `https://image2.sina.com.cn/gm/newgames/0303/images/dongwu0603_08.jpg` 108055 bytes／SHA256 `3cdfea6514804d9ee9d7a0dd6b72c40df4bc2dafbf5c94654a190360dda82301`，物品窗可见可以挖萝卜的铲子／好用的铲子。I2 `https://image2.sina.com.cn/gm/newgames/0303/images/dongwu0603_020.jpg` 88503 bytes／SHA256 `1afc3b40e06f874c4b5b016bc2c852769ded5bcfa6c04a19bccee75d39425b8c`，状态窗显示“动物园养的拉斯基”：等级1、NEXT2、耐久力17/17、攻击力2、防御力3、敏捷力2、忠诚度100；火／风色条可见，不从像素长度推比例。仅这只显示宠物的静态样本，不当整个物种初值、成长、原SPR/ID/实际交付证明；不把旁边无名字人物指认为原生席格。两图均200无跳转JPEG RGB640×480单帧完整解码／人工查看，不认证原像素。原HTML/JPEG不入Git。

16条文献目录＝任务1／具名行动者或会说话物件7／救援目标3／奖励宠1／任务地图1／铠1／画面2；满足7必填与19集合，原game_ids空，非发行授权。三父与解析器原bytes/SHA256/Git blob固定；49项真实HTML去全部指纹语义改写、隐藏/正文外2反例与外围脚本正例通过，独立regex/entity全文相同。初始20项关联测试成功。补充园主／两场景语义后，快速同尺寸写入摘要导致本地Python缓存仍读旧常量，一次validate及两测试失败；核对磁盘摘要与JSON一致、移除本包缓存后 fresh import／20项测试及源回放通过，保留此失败事实。未产生失败远端Actions，远端验收仍待实际后验。

NEXT：先内容候选10/main11实际验收，再永久保留双原派生CI JSON及真实run/job/artifact/ZIP/raw/blob收据，强制保管与反篡改测试后再次验收。最高后续 OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-89 优先另一地区具名宠物技能／成长／骑乘或早期登录人物视觉的原始资料，避免连续扩本篇伊甸线或通用helper；同版实际audio实参才重开音效。Stage A7PARTIAL+2OPEN，B/wiki GATED，savedataR79 PAUSED_NON_BLOCKING；无整体完成百分比，旧历史全部保留。


### R88 内容双端实际验收与永久派生保管 — 2026-10-23

内容提交 `34c59aabfbd96b20c41df22dbbe44e8191ac1010`／tree `4a178c2b41cbccf284f5fc9785c7812991bdfee4`，候选10/main11共21个实际Actions全部completed/success，专用日志初始各7tests成功。

candidate: run39938717033／job120364577573／artifact12493839392，ZIP9699 bytes `sha256:212bfa8808e70bad2e49de3a232d43a8ed494274637dcc12b7d02b1d87c0603c`；原样JSON71990 bytes SHA256 `e4f1c8b8e11497ead6beb3f41a5706d7c79472f608c17be7782611e3cfe55d1e`，Git blob `4d8e620cc87dd073ca3ac2fb3f6fdc322a2a39a9`。

main: run39938920735／job120365251773／artifact12495411010，ZIP9699 bytes `sha256:1cc958f7e0ef623e3e18637084c17716b7b3c93758fa132de2597ef851fea071`；原样JSON71990 bytes SHA256 `e4f1c8b8e11497ead6beb3f41a5706d7c79472f608c17be7782611e3cfe55d1e`，Git blob `4d8e620cc87dd073ca3ac2fb3f6fdc322a2a39a9`。

双ZIP实际下载核对GitHub digest与长度，唯一成员replay.json；双端原样JSON与初始local相等，3个HTTP输入bytes/SHA256同初取。双原CI派生JSON及CUSTODY永久入Git，原HTML/JPEG不入Git。7证据pin固定SOURCE、三父、解析器和双原报告bytes/SHA256/Git blob，代码另锁完整7pin清单摘要；同时篡改证据和重算receipt pin仍拒绝。收据固定21真实run清单摘要、准确双run/job/artifact及ZIP长度/摘要；CLI强制保管，拒绝缺失/等长破坏、错HEAD/tree/分支/任务/ID、重复或遗漏门、工件复用、虚报初取相等及历史/运营/运行权威抬高。第8单元还拒绝单只拉斯基截图升物种主表、静态图升任务执行、席格第二攻击力改防御。原内容CI7tests不改称8tests；保管候选/main自身仍须另实际后验。

最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-89：另一地区具名宠物技能/成长/骑乘或早期登录人物视觉，避免连扩本篇伊甸与无名宣传图。新候选分支将使总分支超过500；下轮分支清单须继续分页到不足100条，不能停在固定第5页。Stage A7PARTIAL+2OPEN，B/wiki GATED，savedataR79 PAUSED_NON_BLOCKING。

R88保管提交前：本包8项／关联21项本地测试成功；原始3输入经强制保管门回放，输出与初始local／双原CI JSON逐字节相同。完整旧历史前缀保持不变。


### R89 报社回刊的2000人物选择记述与早期标题照片 — 2026-10-23

启动以GitHub实际main `5b364c4685e6a1405a9337818cc87ff32715f6f2` / tree `ad8405ea6549de06ed0a0ad67e8cbc0013b54f9e` 为基线；501分支完整读取至第6页，0 open PR、0 in_progress；旧无关queued37642417333不动。HEAD候选10/main11全部completed/success，tree5286条无截断、无AGENTS。八启动文件完整UTF8读取并逐字等于本次Git checkout；CURRENT前缀2456591 bytes/SHA256 `76b9a960f3d168ea0307b4c0ac73d3bd622da47fedf53a8cbd31502da51dadd6`。遵循最高OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-89，补早期人物视觉及人物选择记述，不连扩伊甸。

FACT（限定报社回刊）：报时光／聯合報系2023-04-13 13:22《元祖級Online Game！ 2000年上線的「石器時代」》https://time.udn.com/udntime/story/122835/7095433 明确引用2000-04-11《民生報》37版3C新聞網《網路電玩石器時代上線了》。引文记4種顏色與48種不同造型、自设人物、WGS预付卡扣点对比普通月费，以及面向新人的不喪命／宠物忠诚降低简述。保存原措辞；不乘成192、不分解为12×4、不填原版TW10人物总数/13个创建字段或CN20类型颜色数，不升成完整死亡/复活/扣忠诚公式或收费单位价格。昨日发表来自日本的游戏不是精确服务器开服日。2023外层正文的骑乘及计次非计时不反填至2000引文。

配图图注独立署名2000/02/10 林信昌攝影，写今年3月底將推出（预告而非已执行开服），不混成4月11日或2023发表日期。实际查看可见人在键盘前、CRT上StoneAge字样及中央竖向菜单轮廓，按钮及账号文字不可读；现代報時光水印可见。底层uc.udn直接图URL实取403；页面真实img src的pgw.udn代理实取200无跳转，109235 bytes/SHA256 `7477d5b56427520ede444b5d8f8baa105373a4d004efa2420782ff6e3de11ddc`，JPEG RGB800×450单帧完整解码。照片不是客户端直接截图、原始像素布局、原生800×450分辨率、已操作登录流程、48个可见人物或原图字节鉴真；代理裁切缩放和当前水印不等于2000原件。

初取HTML137674 bytes/SHA256 `44553c4e5c981b8d28534bf250a32f60496d116b84cc42b14071be441682b238`；不是2000原报扫描或原始照片master，也非运营方原脚本。精确build、原报排印与历史像素原件均OPEN。严格固定所选标题/回刊日期/唯一引文/图注/实际图链接；对推荐栏等范围外包装漂移保留各次实际inputs bytes/hash，source_identity如实标明是否等于初取；不以CI哈希覆写初取，不要求不同包装的双原报告字节相等。引文归一化366字符1036 UTF8 bytes SHA256 `7e2ec89c02af77c06da7fee3d8498f816dc9939e065073a879b3053794362a46`；图注109字符305 bytes SHA256 `a669030b71e7b959b9a61d3ac6610e69d0507b510185237a5230c2016a238af6`。

产物：SOURCE、可重放工具、7项单元、专用Actions、内容契约；4条纪录为人物选择数量组/败北简述/支付简述/标题照片，使用19集合及7必需字段，game_ids null，仅研究元数据不获发行授权。三父SOURCE及共享parser bytes/SHA/Git blob固定不改。独立regex/entity归一化与解析器双核对；16语义变异在不依赖全文fingerprint下拒绝、2隐藏/范围外伪修复拒绝、script与外层回顾改写正例保留。测试使用内存合成JPEG，未提交原HTML/JPEG。本地语义键改名后3单元与CLI曾因同秒等长重写残留pyc SHA失配，清除此任务缓存后7项全部通过；失败不抹除，不伪称远端失败或成功。

待双端真实CI与原样派生报告永久保管后验收。下一优先OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-90：另一地区具名宠物技能、成长或骑乘材料，优先具体规则与可辨认宠物，不连续拓展本回刊泛述。Stage A7PARTIAL+2OPEN，B/wiki GATED，savedataR79 PAUSED_NON_BLOCKING；缺同build真实音频参数不扩音频helper。


### R89 内容双端实际验收及原样派生报告永久保管 — 2026-10-23

内容commit `6c753de234e5fe173b1f312839e272101d6dbb88` / tree `8d7cfe602786543d9d534cd41231d7e2f69baafc`。候选10/main11共21个实际Actions全部completed/success，双专用任务日志均7tests与真实网络重放成功。

candidate实际run39940945771 / job120371931887 / artifact12495304253；ZIP3184 bytes `sha256:ee3f97d59bc297b6058a843e68bd55a9448bb85b4af703a9d231c4142363f77d`；原样JSON11015 bytes SHA256 `1dc1787940c20bbd9627ef06e1498561b6fc84b6cd1d5a7f4746f425582b1b89` / Git blob `a2cc7bab38e292a05e17531d8a1be42d08a36658`。实际HTML137528 bytes / `95df497b74e0415641829eb05a2b4d865fa35b456896fd17742fc2f82582006e`，equals_initial_inputs=false。

main实际run39941078117 / job120372368259 / artifact12496250941；ZIP3184 bytes `sha256:a2ba935c6afe0751204efd4bb766ce83eb61060ca3e2226d51bc28ae38aba6db`；原样JSON11015 bytes SHA256 `de842a9ab4fb1fa74b8b4fc0bae9f64f26da1d65e1daca1529f072cb0f3a4dfb` / Git blob `93bc265dd144affe91a480e95b754e97b1c75e88`。实际HTML137670 bytes / `14137dd92f1529dcf8b0e32de0b779e67b767e18c45adf62e396b0017028f9b3`，equals_initial_inputs=false。

双ZIP真实下载核对API摘要与长度，唯一成员replay.json；原样JSON分别永久入Git，candidate_main_raw_bytes_equal=false。两端所选引文/图注fingerprints、4条内容语义、照片bytes/full decode/视觉观察、父比较、16语义变异及2隐藏反例和双范围外正例严格相等；两次HTML整页均不等于初取且互异，source_identity.full_html_equals_initial_intake=false。保留初取137674/hash44553c…不改写，原件鉴真仍false；网页推荐/广告包装变化不影响选定内容，亦不构成原报或历史像素鉴真。没有把两份不同原样JSON重写成同一份。

保管收据固定SOURCE、三父、parser、双原报告共7证据的bytes/SHA256/Git blob，代码另锁完整7pin清单摘要；同时破坏证据并重算receipt pin仍拒绝。固定21真实run清单摘要、精确内容HEAD/tree/候选分支、双run/job/artifact与ZIP摘要/长度；检查每份schema/实际inputs、是否初取的真实布尔值与source_identity、内容语义和边界。CLI强制检查保管；新增第8项反例覆盖缺失、等长破坏、重算pin、虚报相等、任务/分支/HEAD/ID/ZIP错误、复用工件、冒充原报/服务器执行及数量填原版主表/照片升截图/外层骑乘反填。初始远端日志7项不改称8项；本地最终8项及20项相关父域测试共28项通过，原初取输入重放输出与初始local逐字相等，diff check通过。保管提交候选/main自身仍须远端8项和全门后验。

最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-90：另一地区具名宠物技能、成长或骑乘，要求具体来源和宠物，不连扩回刊泛述或匿名宣传；Stage A7PARTIAL+2OPEN、B/wiki GATED、savedataR79 PAUSED_NON_BLOCKING保持。原HTML/JPEG及原报扫描未入Git；4条研究记录不是48个已恢复原版人物。


### R90 台湾8.0具名骑宠资格、类型装备栏与静态面板 — 2026-10-23

FACT：以本轮GitHub新读main `8c60f9139ff149f4e1f846e74a4f575c73321ee7` / tree `344ec5027bfcd2c59e5a9105c40d8c864f235c8d` 启动；503分支分页至第6页3条，0 open PR/in_progress；HEAD候选10/main11共21实际Actions全success，旧queued37642417333不动。tree5294完整无AGENTS。八启动全文严格UTF8与fresh checkout原生Git逐字一致，当前22域索引15948B/hash7d50de…完整核读；CURRENT旧前缀2463657 bytes/SHA256 `b68540c8adf394fa389e88c92e8110879e3034bea5ad927d9c821b17ff9babb2`。最高OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-90补具名宠物骑乘条件，不连扩回刊/匿名图或无关helper。

查重：JP2008进化公告已有规格，不计新；GNN sn20167原页本次HTTP403，未取得，不规避访问限制。改取已知同文的正常公开新浪衍生转载，不能称两份独立一手证据或本轮首次发现8.0宠物装备。旧 `docs/specs/STONEAGE-PET-80-CONTEMPORARY-RELEASE-EVIDENCE-R1.md` 已保存2005发布意义，完整固定不改；本轮新增实际内容语义、具名骑乘条件、真实图像与可执行重放。不是突破旧PET配对build/opcode127缺口。

来源 https://games.sina.com.cn/o/n/2005-06-09/1552109910.shtml ，可见标题《石器时代8.0》开放全新宠物装备(图)，2005-06-09 15:52，来源巴哈姆特、编辑梁凌；明确台湾地区消息。HTML200无跳转48685 bytes/SHA256 `a67c9ee21070d048c7dae901cf8c505b6ced3c888abd1ebcc190f764c1f7f4d8`，GB18030严格解码。Sina URL日期、转载时间与“今日上线”不单独证台湾6月9日开服，不改旧原GNN6月8日报道日期；原运营稿、2005原字节、精确build未取得。

具体骑乘规格：8.0报道新增骑乘对象2只，水魔鬼鱼史卡鲁、恐龙系罗多克雷；新骑宠不等于新物种。仅史卡鲁被说明为新庄园宠、主要出现泪之海；取得难易为定性，而想骑则需新庄园族长发给骑宠证。证书门只绑定该句的史卡鲁，不扩至罗多克雷；证书原ID/族长名字坐标/领取条件/费用/是否消耗/角色对应/等级/忠诚/骑乘属性未知。与CN2.0四庄园骑师、三课程、忠诚100、人物训练及骑战公式分版，不相互补齐。

装备段依宠物类型给予不同装备字段；七大类＝头/牙/爪/胸/背/翅/脚，脚括注两只脚/四只脚/鱼鳍不是三个额外大类，不推出所有宠物都有七栏。可通过合成制作装备，装备自身有属性，按地水火风关系出现能力增减；无具体宠物身体类型对照、装备数值、叠加/取整/相克倍率或全配方表。相邻合成上限由11到15为报道语境，不当人物等级15或全15级配方已恢复。

真实链接链：正文第6个图文链接指向 https://games.sina.com.cn/o/i/2005-06-09/61677.shtml ，图库标题宠物装备套装／2005-06-09 15:52新浪游戏，35353 bytes/SHA256 `41ae049999094a87ef0a6a1789c2ab9ef55d226093267d9a1a191a883c5b11fc`；真实myImage及点击查看原图均指同一非_c全图。仅将页面明示http同主机同路径改https实取，未猜图名或递归其余5图。全图 https://image2.sina.com.cn/gm/o/n/2005-06-09/U508P115T9D109910F376DT20050609155230.jpg ，200无跳转77930 bytes/SHA256 `3126fbb80a7d379530519840e78563dc850707a17e89764f21ad2b82df52aa23`，JPEG RGB640×480单帧完整Pillow解码并实际目视。搜索打开同图曾超时，本机实际请求成功；不混报下载失败或2005原图鉴真。

可见PET STATUS、黄色鸟形宠、人物位于黄色骑乘形象上、右侧7位置装备栏及图标背包、持物光标和绿色格框。未抄不确定宠名/装备名或状态数字，不把此黄色图认作史卡鲁/罗多克雷；像素条非属性百分比、单体状态非物种初值/成长、静态持物光标非成功穿戴/服务器IO/包127/可用PET宏build。640×480当前图幅不是客户端全局原生布局或原SPR动画。原HTML/JPEG不入Git。

交付SOURCE、5条研究目录（具名骑宠2/类型装备教程1/合成上限语境1/面板参考1）、契约、专用工具7单元及Actions。7必填/19合法集合、game_ids null、非发行授权。两HTML各自实际bytes/hash与初取是否相等如实保留，选定三正文段/图库图注与链接严格固定；初取基线不被CI包装变化覆写，JPEG完整固定。三父（旧CN20骑乘、旧PET80发布规格、内容档案）及parser完整固定。独立regex/entity三段与解析一致；20语义变异移除fingerprint仍拒绝、3图库身份反例、2隐藏/正文外伪修复及外围script正例通过。本地生成器首有正则引号语法错误，继有脚括号内顿号误拆；修正结构分组后，真实反例发现“不能透过合成制作”仍命中子串，收紧肯定完整句后20变异/7项通过。保留预检失败，不冒称已远端验收。

止点：一台湾报道衍生转载＋一实际图库＋一全图，完成具名骑证条件与装备类型资料，不实现骑乘/装备或推原服。候选/main真实CI后保存双原派生报告和收据再验收。最高后续OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-91：优先早期具名NPC对话/交互界面或另一地区具名宠物技能数值来源，避免连扩本报道其它娱乐设施/无名图；Stage A7PARTIAL+2OPEN，B/wiki GATED，savedataR79 PAUSED_NON_BLOCKING，无整体百分比。


### R90 内容双端实际验收及永久派生保管 — 2026-10-23

内容commit `f2ce09647efd8cbb67994e7f9718b18d3efc8e15` / tree `c5b2d1c9760ff14917fc2f4cee499d87153caf43`，候选10/main11共21实际Actions全completed/success，双专用日志各7tests与真实两HTML一全图取源成功。

candidate: run39943758433 / job120381250855 / artifact12497147418；ZIP3458 bytes `sha256:fc1551cc8a3a904cf00e8c0d36b61eb787c122ce812c55f12defdd4b8be87046`；原样JSON12168 bytes SHA256 `75bb718becb3e152bbe0057988cb355739810351d23c992304456b3cccec41d9` / Git blob `584983c1b8c7137c72b70d64675a1da0ff722801`；equals_initial_inputs=true。

main: run39943895787 / job120381709724 / artifact12496718117；ZIP3458 bytes `sha256:5b12c0a77e9bb6872e01bbfedeff3fef8481188dc408c40d6c371cd09782a028`；原样JSON12168 bytes SHA256 `75bb718becb3e152bbe0057988cb355739810351d23c992304456b3cccec41d9` / Git blob `584983c1b8c7137c72b70d64675a1da0ff722801`；equals_initial_inputs=true。

双ZIP真实下载核API摘要和长度、唯一成员replay.json。双原样JSON与初始local逐字相等，3个实际输入bytes/SHA256一致，candidate_main_raw_bytes_equal=true；S1/S2初取比较均true，如将来包装变化仍各自诚实记录，不覆盖初取。引文三段、图库图注/链接、5纪录、完整解码照片与视觉边界一致。原HTML/JPEG不入Git，永久保留双派生JSON及CUSTODY。

7证据SOURCE、旧CN20骑乘、旧PET80发布规格、内容档案、parser与双原报告按bytes/SHA256/Git blob固定，完整7pin清单摘要另锁代码；证据被改后连receipt pin一起重算仍拒绝。固定21真实run清单摘要、准确内容HEAD/tree/候选分支、双run/job/artifact/ZIP长度与摘要，不接受缺失、等长破坏、漏门/重复/复用工件、虚报初取或双端相等、错任务/分支/HEAD、2005原字节或服务器运行抬高。逐份核schema、两HTML实际identity及初取布尔、全图固定、语义/audit与原件界限。CLI强制保管，第8单元增加所有保管反例及骑证泛化至两宠/七类别变全宠槽位矩阵/静态持物变成功穿戴的拒绝。本地最终8项及关联16项共24通过，原输入强制保管重放输出与初始local逐字相等；独立发布边界工具通过，旧文完整保留。原内容CI7项不改称8项；保管提交候选/main自身仍待实际8项及全门后验。

交付具体收益是把“持有史卡鲁”和“获族长骑乘证”分开，以及宠物类型→可用装备栏、7大类/脚子类型、属性增减的有限资料。没有宠物物种完整数值、技能/成长率、骑证原ID与实际装备事务。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-91：早期具名NPC对话/交互界面或另一地区具名宠物技能数值来源，避免连扩本报道娱乐设施/匿名图。Stage A7PARTIAL+2OPEN、B/wiki GATED、savedataR79 PAUSED_NON_BLOCKING，整体恢复百分比仍null。


## 2026-10-23 R97 — finite website pig catalog identity/source join

Following R96, the highest source-material gap rotated from player world routes to named pet graphic and catalog identities. Read extant 17173 catalog index plus pig detail rows 001—008, historic player Lv1 list and the already-closed TW1.0 bitmap/SPR numeric intersection. R97 found **material naming and filename ambiguities**: catalog row 007/008 names disagree across index/detail; detailed 004/008 duplicate the same name with different element/HP claims; small GIF filenames in detailed 007/008 are swapped. Eight web records cannot be promoted to eight independently proved historical species. No authenticated same-build PET/ADRN/SPR identity binding; original image bytes not archived. Bounded machine-readable contract, provenance and negatives stored as R97 research report and CLI/CI. Content candidate initial CI failure and corrected success recorded in CURRENT-STATE. Research does not constitute game implementation.

**Next highest** `OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-98`: move to different regional early named NPC/map interaction original illustration or truly same-build original pet-to-sprite selector evidence; do not expand remaining 17173 pig catalog pages without a new bridge. Stage A seven PARTIAL / two OPEN, Stage B/wiki GATED; TW10 savedata R79 remains paused, full-game completion numerator/denominator unavailable.
