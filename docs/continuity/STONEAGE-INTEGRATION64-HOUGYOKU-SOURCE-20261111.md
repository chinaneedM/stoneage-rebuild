# INTEGRATION64｜四属性宝珠与月光手镯：原吉鲁以外 NPC 物品操作、四个传送数字及六张原图候选（2026-11-11）

## 重启、查重与边界

按 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` 重新读取 2026-11-11 远端 `main` HEAD `9c1208d0ea9deed4a420e1d34ba9817e58b2309d`／tree `4356fbcb66ecca441e67c6f1152b1fa6920bc131`、最新提交与 Actions、README、协议、设计、版本时间线、来源、路线、模块优先级以及完整历史 `docs/CURRENT-STATE.md` 原生 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`。INTEGRATION63 水壶 11 ID/16 原边已闭合，本轮不重复 O70/O74 的四村 47 委托任务／23 售书、QUEST30 两只恐龙、I61 料理或 I60 诊疗。逐项查 README 中 `extra/event/hougyoku` 及六原 ID 未见此前同样的专项图；既有 QUEST01 只把该脚本编入 295 脚本/1349 TYPE 的**数字目录**，本轮做出真正可查的 NPC 创建、源事件、六件原物品和六个原图候选的可审计跨模块联接。

**注意：** 源是后期社区 mixed25 保存，**不是已认证的初代 JSS、台湾1.0 或大陆1.82 官方服务器部署**；早期台湾 1.0 RD 候选图是**另一载体**，二者关联仅基于原同图号。原条件不代表客户端已触发；原地图未运行；不把来源路径 `extra/event` 判定为官方永久或限时事件。所有原文、PNG、原完整物品行保留在私人 ZIP。

## 真正回读的原始来源

- 原NPC保存 ZIP **995,176B／SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`**，已重新读取所有 **2,205/2,205** 成员，ZIP CRC 无错误。原脚本 `npc/extra/event/hougyoku` **1944B**、SHA256 `fbc23c845a63a4fd126f5f0b8aefd85802210950db5818d2f56ab4588aa22888`，原 `hougyoku.create` **342B**、SHA256 `ed001acc16e29c2efaeb146840a2b563bc0265b64b364bf91ff22900abf5e0d5`。两份完整 CP950 原件逐 SHA、解码重编码往返。原 CREATE 唯一创建块为 `floorid=6000`、`borncorner=58,44,58,44`、图号16047、`enemy=changeevent|file:extra/event/hougyoku`。与 QUEST01 旧原目录中精确路径/原 SHA 的 1 次创建引用一致。
- 原物品私人 ITEM01 ZIP **5,868,386B／SHA256 `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa`**，本轮 **838/838** 成员 CRC 复验。原 ID 2760–2765 在 `itemset.txt` 与 `itemset0710.txt` 各有 6 原行，逐 **94** 原 CP950 栏重编码并比对 12 个整行 SHA，各 ID 的两行完全相同，并与已公开 `item-module-01` shard02 的原行 SHA/原图号吻合。保留原 price/type 数字而**不**推实际商店售价、使用效果。
- 台湾1.0 零售 RD 私人保存的 **6 个原 PNG** 分别从包实际重读全字节 SHA 与尺寸；六张对应不同原 RD 物理编号，数量绝不混为同版任务的已生效美术。物品清单与源 SHA 详见 [派生 JSON](../../research/recovered/STONEAGE-INTEGRATION64-HOUGYOKU-SIX-ITEMS-ORIGINAL-SOURCE-R1.json)。

## 本轮具体恢复的静态游戏内容

源创建位置 `6000/(58,44)` 的一份脚本原共有**四**个严格 TYPE 段，按物理次序为 `ACCEPT`、`REQUEST`、`MESSAGE`、`MESSAGE`。其中两个 `EventNo:45`，另两个 `EventNo:-1`；不是四位 NPC、四次成功操作或四个独立任务。

| 源段 | 条件原数字字面 | 操作字面 | 只允许的解释 |
|---|---|---|---|
| ACCEPT | `LV>59`，要求 `ITEM=2764,2760,2761,2762,2763` | `DelItem:2764,2760,2761,2762,2763`；`GetItem:2765`；`EndSetFlg:45` | 源条件/消耗与奖励**候选**，不是实际收走五件与发放手镯 |
| REQUEST | `LV>59` | `GetItem:2764*1` | 与 ACCEPT 的五件交付**分开**，是结晶石的另一源命令，不是任务执行链已证 |
| MESSAGE | `LV>59&ENDEV=45` | 无物品命令 | 文字分支仅存来源 SHA |
| MESSAGE | `LV>0` | 无物品命令 | 未验证优先级和触发次序 |

ACCEPT 还写有**一条** `NpcWarp:4000.53.101,2000.44.39,5105.14.3,6000.58.44`。源分隔数字四组分别是 `4000/(53,101)`、`2000/(44,39)`、`5105/(14,3)`、`6000/(58,44)`。不能把它读成已发生的“四次连续传送”、按顺序依次发送或四个不同 NPC 的实际地图路径，NPC Warp 参数解释与随机机制均 `OPEN`。现有 MAP09 的 691 张可见画布目录中 `5105` 有原 DAT/图像派生资格，但不包含 `6000` 的可见画布记录；这仅是该**筛选目录**缺记录，绝不是官方原地图没有 6000 的证明。本轮没有直接解码或运行原 DAT。

六原物品与真实图号关系：**2760 地、2761 水、2762 火、2763 风、2764 结晶石、2765 月光的手镯**（名称按源原行的限定标签）；原 alias 依次为 `24059/24055/24061/24057/24198/22082`，六幅原零售 RD 候选均逐 SHA 与原保存包相同。五个条件物品与一个脚本产物的**不同主键**得到核实；不同原字段类型（前五源 type16、手镯源 type8）不能因同一事件就合并成一个“宝珠系列”。既有早期图不能证明后期社区脚本曾采用其图像，也不能证明装备效果真正生效。

## 私人保管、公开验证与继续

私人包 `StoneAge-INTEGRATION64-Hougyoku-original-source-private.zip` **15,469B／SHA256 `ef6ed11dc1b25c13e41190d08d3910fc5adbdeb37231d1b5d5c8bfdccd3afa94`／21 成员**，含 2 原 NPC 文件、两套各 6 原 CP950 物品行、6 台湾1.0 原图 PNG、一份私有派生收据。已从原 ZIP 重新逐字节核对原行/原图SHA、21 个新包成员 CRC，无原物公开至 Git。保存到用户私人 Library `/石器时代/` 后需再次独立重读验证；不能在未二次重读之前宣称“已回取”。

公开仅发布派生 SHA、数字、原条件操作锚点、地图编号候选与 8 组公开专项测试，CI 测试已有 QUEST01 原创建与 TYPE 目录、ITEM01 shard02、MAP09 691 帧候选和本轮原始字节新归档形成的派生关系。**公开 CI 无法重读私人 ZIP**，故其 success 不证明原游戏脚本执行。本轮任何未完成的 PR/Actions/main 验收另据远端实跑填写，不预称成功。

`docs/CURRENT-STATE.md` 原大文件整 blob `c89e0e33537990aa2132b47c40fef49a985a935c` **保持原样**，只用独立日期文件追加接力。Stage A **7 PARTIAL + 2 OPEN**，Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，总体百分比 `null`。

**NEXT：** 这六物件/一NPC四段的静态联接已核。换其他有新真实原字节可回放、玩家可感知、未被 O/QUEST/INTEGRATION 专项覆盖的内容；若想进一步证明这次 6000 原房间/传送路径，须获得**同版本有资格的原地图 DAT + 真实执行见证**，只凭脚本字面不重开、不写模拟任务引擎。
