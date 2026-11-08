# QUEST14｜龙之巢穴与三龙奖励：原脚本、双地图、七道具的来源限定复原（2026-11-08）

## 1. 远端启动、对象与旧成果查重

按 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` 重启，重取远端 `main` HEAD **`6c6a193fd937133f94a7901f78744ac53984bf55`**、tree **`4eaea54fcda3fe136f0b18a5c7c9da78e9de784d`**、最新提交及 Actions、完整旧 `docs/CURRENT-STATE.md` Git blob **`c89e0e33537990aa2132b47c40fef49a985a935c`**（2,709,173 B），以及协议、路线、模块队列、历史来源、DD032 和已验 QUEST13 交接。未覆盖旧 CURRENT；无待合并的远端 PR。原 QUEST13 记录最高 NEXT 指向 QUEST14；此源在早期 QUEST01 的全量索引中已有 **4 条 CREATE 引用／10 条 TYPE 事件段**，本次是*真实原文、物品、地图实物与族系联系的专项复原*，不把旧索引计数重算为新增历史文件或新发现物种。

研究对象限定为后期社区 mixed25 组合保存包中的 `jaruga/event/event17.create`，其直接指向 `event17_1`、`event17_2`、`event17_3`、`event17_4`，另实际回读 CREATE 引用的共同 `event.template`。5 个主任务文件 + 1 个共享模板；其历史官方发行版本、部署时期与真实运行均 **ORIGIN_UNRESOLVED/OPEN**，不可推广为台湾 1.0、2001 大陆初代 1.82 或 JSS1999 正式内容。

**目标和止点**：从这些实际原件完整恢复三龙／守护者的源位置、原事件分支和七件道具的有向关系，和两份实有原地图 DAT 的格值交叉核对；在无真原生执行和龙玉产出来源的情况下止于 `ACCEPTED_SOURCE_BOUNDED`。不推演实际对话选择、可重复领奖、遇敌掉落、三个奖励同时取得或已能玩。

## 2. 原文件实读与验证层级

- 从私人 Library 已保留 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip` 原来源包回读，**995,176 B／SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`**；本轮逐项复验**全部 2,205 文件/1,930,332 B** 与既有 `STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json` 的长度、SHA256、CRC32 一致。原文以 CP950 严格解码；6 个直接文件的原字节／散列见[公开数字收据](../../research/recovered/STONEAGE-QUEST14-DRAGON-NEST-ORIGINAL-SOURCE-R1.json)，原文只入私人包。
- 原 `event17.create` 中恰有 **4 个原创建块**，物理偏移与逐块 SHA 均和既有 CHAR01 目录逐一吻合；4 个脚本的 **10 个 EventNo/TYPE/EVENT/EventEnd** 段、条件 SHA 和原段落 SHA 均与**独立旧 QUEST01** 索引相同，无私自改写脚本。5 原主文件实际字节及共享模板一并私人保管。
- 私人原 ITEM01 包 **5,868,386 B／SHA256 `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa`**：七个 ID 在 `itemset.txt` 和 `itemset0710.txt` **各一条 94 栏原记录，合计14条物理行**；全部按原 CP950 逗号重建 SHA 匹配，且七组两源原行相同。与既有公开 ITEM01-02 行哈希、图别名再核对。七件道具分别保有真实从台湾1.0原 RD 解码的**7 幅候选 PNG**，在私人包中逐图 SHA 相同；**像素来源与后期任务脚本不是已认证同部署**。
- 私人 MAP09 包 **46,844,444 B／SHA256 `d84d0800dd600798769dfb7251a1d7816588ac061ccc27812ac64a37922d4a8a`** 内的原 955 DAT ZIP 再核；真正回读 **`20801.dat`（70×70；29,408 B）**、**`20807.dat`（50×50；15,008 B）**，两份 SHA 与旧 MAP09 来源收据一致。地图为原三 u16 **依平面连续存储**，不是将三个数按格交错读取；四个 CREATE 坐标均在原源数据范围内。两张旧私人画面缩图供现代观察，未生成假 NPC 或原生行走画面。

## 3. NPC、两张原图和原三平面格（仅 source FACT）

| 原原型角色／CREATE序号 | 原 floor、坐标 | 角色图像别名（非已验证像素身份） | 对应脚本 | 真原 DAT 三平面 u16 |
|---|---|---:|---|---|
| 疾速龙 #0 | `20807/(7,8)` | `100384` | `event17_1`（2段） | `(4004,0,49152)` |
| 刚气龙 #1 | `20807/(23,6)` | `100385` | `event17_2`（2段） | `(4001,0,49152)` |
| 钢格龙 #2 | `20807/(41,14)` | `100386` | `event17_3`（2段） | `(4008,0,49152)` |
| 守护者 #3 | `20801/(13,63)` | `16208` | `event17_4`（4段） | `(4001,0,49152)` |

表内繁体姓名为本次原 CREATE 中的名称经必要转写的检索称谓，原字节姓名仍留私人，**非官方早期人物认定**。这四个图像别名仅来自原创建配置，不把其数值当成宠物、SPR组数或实际场景像素出现的证明。两张原 DAT 有原格值，也不证明楼层间已找到入口、可达路径、角色实际站位或碰撞属性。

## 4. 原任务条件与奖励／消耗图（字面，不运行）

守护者脚本 `event17_4` 有四段：

- `#0`：`EventNo:17`／`TYPE:ACCEPT`／`NOWEV=17&ITEM!=2505`，裸 `GetItem:2505`；
- `#1`：`EventNo:17`／`TYPE:REQUEST`／`LV>0&ITEM!=2505`，裸 `GetItem:2505`；
- `#2`：`EventNo:17`／`TYPE:MESSAGE`／`NOWEV=17&ITEM=2505`；
- `#3`：`EventNo:-1`／`TYPE:MESSAGE`／`ENDEV=17`。

三条龙各自的首段**完全同一来源条件** `NOWEV=17&ITEM=2457&ITEM=2458&ITEM=2459&ITEM=2505`，也均包含**裸** `DelItem:2457,2458,2459,2505` 和 `EndSetFlg:17`，但 `GetItem` 不同：疾速龙 `2462`（龙之衣），刚气龙 `2460`（龙之枪），钢格龙 `2461`（龙之铠）。各自第二段均为 `EventNo:-1/TYPE:MESSAGE/ENDEV=17`。所有 `GetItem`、`DelItem` 在这批段落中**未显式给出 `*N` 数量**，不能静默补“每件1个”作为原文；原指令执行顺序、标志位变化后的可选分支、物品容量/领奖失败、掉落方式一律未证。七件道具原身份为 `2457/2458/2459` 三龙玉、`2505` 龙笛、`2460/2461/2462` 三项装备，图像别名归属彼此独立且跨源不合并。

**有界负证：** 对全 2,205 个已认证原 NPC 文件，仅按 `GetItem:` 的原字面扫描，`2457/2458/2459` 三个龙玉没有一次取物发放行；`2505` 在守护者文件有两处，`2460/2461/2462` 各在相应三龙文件有一处。这不等于在原游戏中龙玉不能掉落，敌人战斗、合成、商店或缺失同部署表均未由此扫描穷尽。道具原描述提示持有关系，但不能从原名字或简介推成原生战斗必然产出。

## 5. 交付、测试与下一步

**公开**：仅本说明、可独立重放的[来源数字/负证收据](../../research/recovered/STONEAGE-QUEST14-DRAGON-NEST-ORIGINAL-SOURCE-R1.json)、[来源提取工具](../../tools/stoneage_quest14_dragon_nest_source.py)和 [10项可在 GitHub 运行的原来源合同测试](../../tests/test_stoneage_quest14_dragon_nest_source.py)。测试只交叉核已经公开的原物理行 SHA、旧 QUEST01 段 SHA、CHAR01 创建块、映射坐标及负证计数；不能当成重新下载原商业文件的 CI。

**私人**：原 6 NPC 文件、14 条原物品行、2 原 DAT、7 幅 TW1 真源 RD 候选 PNG、2 张既有场景缩图、离线原文阅读器、收据。私人 ZIP **81,015B/SHA256 `5f004435b501c7e2bded801ec8e847482cfca5fffb409ad7c2160e5247074232`／34 个成员**已在本机独立逐件 SHA/CRC 核对。**个人 Library 上传和回读状态须由实际后验记录，不能将当前本地验证说成已云端验收。** 原商业文字／地图／图像不公开 GitHub。

资料说明里记录的尚未认证版本与运行均不补造。Stage A **7 PARTIAL+2 OPEN**，Stage B 和 wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，整体完成率 `null`；依照用户指令始终单机离线内容优先，未来新游戏、引擎和体验修改仍延期。

**最高 NEXT `QUEST15-DEDUP-AND-SOURCE-READY-UNRESTORED-ORIGINAL-FAMILY`**：先重取新远端，再查重 QUEST01/04/05–14 已复原族，择一真有原脚本、物品及场景可证的下一任务；三龙本族原战斗/龙玉来源需新同部署原材料才增量重开。其他组合 portfolio 若后来更新则以后验更高优先级为准。

 
## 6. 私人存档、正式合并与 GitHub Actions 后验（2026-11-08）

- 私人原件已保存个人 Library 的 `StoneAge-QUEST14-dragon-nest-three-dragons-original-private.zip`，**81,015 B／SHA256 `5f004435b501c7e2bded801ec8e847482cfca5fffb409ad7c2160e5247074232`／34 成员**。上传后确实以新文件 ID 重新独立取回，完整 ZIP 的 SHA256 与本地打包相同、`testzip()` 全部 CRC 正常；其中 33 个收据内成员各自原始内容 SHA256/字节数也全部逐项重新核对。这是私有原文/原 DAT/跨载体候选图的保管验收，非公众 Git 仓库内容。
- 候选源提交 **`272c0d65a987d1e493c579ba5797b76425b9eddb`**、tree **`b43cad35b44ed1f801ffbef9eee926df1320e5c7`**，来自 fresh main `6c6a193fd937133f94a7901f78744ac53984bf55`。远端逐文件核验六处公开变动：4 新增公开派生材料 + README 索引 + 旧来源工作流步骤；无原商业 NPC 对白、原 DAT、原 PNG、私人 HTML。完整旧 `CURRENT-STATE.md` 仍为 **blob `c89e0e33537990aa2132b47c40fef49a985a935c`（2,709,173 B）**，未覆盖、修短或改写。
- [PR #254](https://github.com/chinaneedM/stoneage-rebuild/pull/254) **已实际合并**，合并主线提交 **`f45ea47302c746b9464a44a3f71854c288f109bd`**，远端 main tree 与候选 tree **完全一致**；原 main 与候选保留为两个父提交。
- 候选 **14/14 GitHub Actions completed/success**。专用 [QUEST05—QUEST14 来源验证运行 #42452743681](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42452743681)／job **`128645244868`** 真实完成，新增步骤 **“Validate QUEST14 dragon nest literal original source and unknown-runtime guards”** 为 success，既有 QUEST12/QUEST13 回归步骤也 success。测试只在公开派生证据和公开旧目录上重放，并未在 GitHub 读取原商业 ZIP。
- 合并后的 `main` **11/11 GitHub Actions completed/success**，含专用运行 [#42452799851](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42452799851)，其余十项 `42452799852`、`42452799855`、`42452799817`、`42452799857`、`42452799889`、`42452799853`、`42452799839`、`42452799863`、`42452799789`、`42452799864` 全部实证成功。**本段文档后续追加提交自己的 Action 运行必须另验，不能提前归入这 11 次结果。**
- 本次任务族状态 **`ACCEPTED_SOURCE_BOUNDED`**；仅源字面规则、实际原物品行、地图格值、旧 QUEST01 索引对照与有界空白已验，不断言官方早期部署、龙玉实际掉落、遇敌战斗、三奖励真实选择／重复性、原版客户端可玩。Stage A 7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING、整体百分比 null，均不因 10 项测试通过而改变。下一最高 NEXT 是 **`QUEST15-DEDUP-AND-SOURCE-READY-UNRESTORED-ORIGINAL-FAMILY`**，从全新远端与源文件先查重、再选真实可得的独立任务族，不重复 event17。
