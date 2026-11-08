# QUEST12｜矿山比赛／采矿权原任务族：原脚本、道具流向及两张真实地图（2026-11-08）

## 远端启动与范围

本轮从 **GitHub 远端 `main` `bd646318f3fba0453aaf444da0145f41fa185a8e`、tree `e4c1b4a84a356c2049bdc81f093e601a03251e21`** 重新启动，读取远端分支、最新提交、Actions、README、连续性协议、`CURRENT-STATE.md` 的完整原 Git blob 及路线和最新 QUEST11 增量。旧 `CURRENT-STATE.md` 是 2,709,173B、blob `c89e0e33537990aa2132b47c40fef49a985a935c`；未覆盖、截断或用较旧聊天记录替换。最新 [QUEST11 交接](STONEAGE-QUEST11-TWO-TRIBES-ORIGINAL-SOURCE-20261108.md)指定 QUEST12，不重复 O24/O32 已完成的任务族；原来已存在的 `1004→template544/SPR100401` 数值联接仍只算旧 CHAR09 证据。

**本包游戏对象：** 后期保存载体中矿山比赛的两名主线 NPC、矿工与许可证入口；优先恢复脚本条件、物品有向引用和楼层真实位置，而不是编造比赛胜负、掉落或权限行为。**源域：** 后期社区 mixed25 组合保存包，`ORIGIN_UNRESOLVED`；其脚本、其他时期 ITEM01 的真实图像候选和地图来源均保留独立载体身份，不能当台湾 1.0／大陆 1.82／日本 JSS1999 的同部署正式资料。现代离线页是私人原文阅读器，不是原游戏执行。

## 1. 真正回读的原件与保管

- 重新从私人 Library 取得 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip`，**995,176B / SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`**。全 2,205 个原文件的文件集合、字节数、SHA256、CRC32 与已在 Git 存档的 CHAR01 原清单逐项相符，非只核 9 个选中文件；所选 CP950 文字往返原字节。具体 9 源文件的 SHA、行位置与源 CREATE 块身份见[公开派生收据](../../research/recovered/STONEAGE-QUEST12-MINING-COMPETITION-ORIGINAL-SOURCE-R1.json)。两主脚本 SHA256 分别 `e18cbf24d2f067bdcf6d797756e14c4b24d11f19b9698b5fc75e0f9405a86557`、`1e476a4d62e216fd891c527e1564dd70ad4e846f11c54a308f6f04381daf746f`；主 CREATE 593B/SHA256 `c04975eb9d46cb328df5d4bee99a235547fae10010d28de95ae1557b21037ace`。
- 物品复用已认证私人 ITEM01 832 候选原图包，**5,868,386B / SHA256 `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa`**，838 件成员 CRC 正常。仅按原 94 栏恢复涉及的 8 个物品 ID 的 **15 份原行位置**；去重后仅 **8 份不同原行散列**，不可将 15 行说成 15 个物品或 15 种不同属性。图像候选依原 PNG 与 RGBA 的既存双散列重验。两件原物品共享图号不代表同种道具；2391 在此包无有资格原图，不能补造。
- 地图复用已保管 MAP09 私人目录包，**46,844,444B / SHA256 `d84d0800dd600798769dfb7251a1d7816588ac061ccc27812ac64a37922d4a8a`**，4,195 件成员 CRC 正常。从其中真实原 DAT 子 ZIP 重新读取 `31805.dat` 和 `31806.dat`，两份均 **50×50／15,008B**，各自整 SHA 与旧 MAP09 来源收据相符；每个目标位置三份原 u16 数值由实际字节独立定位。原缩图仅用现成已验场景画面加标记，没有新增整个地图绘制、原游戏运行、NPC 像素解码。

## 2. 原创建与地图结构（FACT：仅关于此保存包原文件）

| 原 CREATE | floor/(x,y) | 原文件控制身份 |
|---|---|---|
| `giruev2` 主 NPC 1（帖尼姆） | `31805/(19,21)` | 图号 `16062`，参数 `giruev2_1`，共 7 个原事件段 |
| `giruev2` 主 NPC 2（巴巴洛） | `31805/(33,23)` | 图号 `16017`，参数 `giruev2_2`，共 6 个原事件段 |
| 矿工 `sb_bac` | `31805/(26,23)` | 图号 `100401`；原 `arg` 读到 `entype:2`、`item:2535`、`steal:1`、`enemyno:1004`、`time:300` |
| 许可证入口 | `31805/(22,4)` | `genout/giruev2.create` 序号20与 `wpm_31805_22_4` 精确引用 |
| 目标落点（静态参数） | `31806/(34,6)` | 原 `WARP:31806,34,6`；目标 DAT 确有该坐标 |

同名的 `genout/giruev2.create` **共有 21 条 CREATE**：20 个周围信息点与 1 个许可证入口，不是 21 个主线角色。主线的两条 `giiru/event/giruev2.create`、矿工的 `300/sb_bac.create` 分别计数，来源块 SHA、模板引用与原参数外键逐条可追踪。

上述 5 个位置的原 DAT 三 u16 分别为 `(4200,0,49152)`、`(4301,0,49152)`、`(5068,0,49157)`、`(4302,0,49152)`、`(4305,0,49152)`；**仅是原格值**，未推断碰撞、地形、可达性或实际地图事件。私人观察缩图显示 31805 场景与这些现代圈标，非原游戏现场截图。

## 3. 原条件、道具与许可证：逐字面保留

| 脚本原段 | 原条件与原指令 | 已证层级 |
|---|---|---|
| `giruev2_1 #0` | `ENDEV=27&ITEM!=2391`，裸 `GetItem:2527`，`DelStone:1000` | 源字面；1000 未运行扣费 |
| `giruev2_1 #1` | `ITEM=2533&ENDEV!=27`，裸 `GetItem:2527`、裸 `DelItem:2533`、`EndSetFlg:27` | 源交接与完成旗标命令，原语法/执行未知 |
| `giruev2_1 #3` | `LV>29&ENDEV!=27` | 源等级条件，未证明实际进入任务时机 |
| `giruev2_2 #3` | `NOWEV=27&ITEM=2534`，裸 `GetItem:2535`、`DelItem:2534*1,2536` | 2534 显式 *1、2536 **无原数量**，不代填 |
| `giruev2_2 #5` | `NOWEV=27`、`GetItem:2536*1` | 只证明来源脚本确有此物品指令 |
| `giruev2_1 #5` | `ENDEV=27&ITEM=2391&ITEM=2393&ITEM!=2394`、`GetItem:2394*1`、`DelItem:2391*1` | 此分支跨族引用，2391 原表缺图及旧命名冲突继续未决 |
| `wpm_31805_22_4` | `WARP:31806,34,6`、`FREE:ITEM=2527`、`DelItem:2527*1`、`MONEY:-1` | 只证明静态许可证检查/消耗目标，不证明原客户端实际传送 |
| 矿工 `sb_bac.arg` | `item:2535`、`enemyno:1004`、`steal:1`、`time:300` | 只是敌方/奖励参数，不证明击败、偷取或掉落 |

全源 `2205` 个已认证原 NPC 文件按 `GetItem:` 指令扫描，本载体 **未找到 `2533` 或 `2534` 的 GetItem 来源行**。这不是证明全部游戏版本从未发放；它们可能来自不同来源表、制作、掉落、交易或缺失文件，任何一种均须新原件才可成立。`2535` 的脚本 `GetItem` 与矿工 `item` 是两个不同来源的数字控制，不能以相同 ID 宣称已观察到矿工掉落。原完整条件中的 `&`、`!=`、多操作顺序和裸物品数量不运行求值。

已复核 8 道具：`2391/2393/2394/2527/2533/2534/2535/2536`；7 个有目前 ITEM01 包保存的跨来源台湾 1.0 原 RD 候选像素，其余 2391 无合格原图。`2527/2533/2535/2536` 的图像别名均 `24222`，`2534` 为 `14607`，这不属于同一部署的官方道具身份认证。物品表原名称/94 栏保存在私人包，公开只给数字、原行身份 SHA 与前述适度来源称谓。

## 4. 验收边界、实际交付与下一步

**公开交付**：可再生的 [源读取/证据提取工具](../../tools/stoneage_quest12_mining_competition_source.py)、[全数值/来源与负证 JSON](../../research/recovered/STONEAGE-QUEST12-MINING-COMPETITION-ORIGINAL-SOURCE-R1.json)、[10 项独立来源断言](../../tests/test_stoneage_quest12_mining_competition_source.py)及本续接记录；CI 仅可复核派生文字/数字/哈希，不等于 CI 下载私人商业原件。**私人交付**：9 个原配置、15 个原物品行位置、2 份原 DAT、既已合格的候选图、两幅标记缩图、静态离线全文页和来源收据，不公开原商业内容。重验的实际 SHA／CRC 与私人包回读状态在后验追加记录，不能以预期当作成功。

**有界止点**：矿山比赛静态已取得的原任务族中这两位主角、许可证和矿工材料完成了来源受限复原。没有原实际选支/执行、物品 `2533/2534` 上游、同部署原任务全链、敌人胜利掉物或原版可玩角色证据；这些保持 **OPEN**。Stage A **7 PARTIAL + 2 OPEN**，Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，总体完成率 `null`。原商业文件留私人研究范围，新单机游戏引擎、注册/联网/服务器、新玩法均不在本批。

**下一优先项：QUEST13-DEDUP-AND-SOURCE-READY-NEXT-FAMILY**。按任务模块原则先对本源中未成族的现存原事件脚本作有界索引对照（查旧 QUEST01/04/06–12），选择下一组确有来源、独立叙事或实际玩法增量的任务族；优先能连接既存地图/道具的另一族。不得只重复 `giruev2` 或虚构 `2533` 取得路径；若新的同部署原字节到手，再增量重开对应缺口。此 NEXT 不会凌驾后续更新的组合 portfolio 指令。


## 5. 正式合并、远端 CI 与私人保管的后验（2026-11-08）

[PR #252](https://github.com/chinaneedM/stoneage-rebuild/pull/252) 经候选源提交 `fbe9f1939cf3e50560b07d8faa568b97d7c03aa9`、tree `977a9b224cc74f3ba74e3ae63e1d56565abbcb7e` 发布并正式合并到 `main`：内容合并提交 `f6c3c6293e149bb2d76dbfc6a6baf20ca4fad3be`。本轮 GitHub 远端重取核对 6 个变动路径与候选已验 blob；旧 `docs/CURRENT-STATE.md` 仍是完整未改的 blob `c89e0e33537990aa2132b47c40fef49a985a935c`（2,709,173B）。提交中的工具、10 项新测试、派生 JSON 和本连续性记录均为可分发纯数字/文本，不含原商业 NPC 脚本全文、原 DAT、像素图或私人 HTML。

GitHub 远端 **候选 14/14 项 Actions completed/success**，含专用 [QUEST05/06/08–12 复用校验工作流](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42440850239)：job `128609564147` 中本轮新步骤 **“Validate QUEST12 mining competition original source and negative provenance guards”** 为 success，旧 QUEST05/06/06-R2/08/09/10/11 的七组步骤亦全部 success。合并后 `main` **11/11 项 Actions completed/success**，专项 [`42440927130`](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42440927130) 与原资料来源边界等各项均成功。此处仅是实际结果，不追认后续文档提交自身 CI。

原商业文件已打成私人 `StoneAge-QUEST12-mining-competition-original-private.zip`，**113,328B / SHA256 `d93aea416ea40a336e9c05a7cd851dbfc557916322f00152d91224f717c54cd9` / 32 成员**，成功保存于个人「石器时代」Library。保存后独立重新取回，整包 SHA 和 32 CRC 全同；并对 **9** 原配置整 SHA、**15** 原物品行 SHA、**2** 原 DAT 全 SHA 和 **5** 源点全部三 u16 值逐件重核通过。原来源 2,205 成员及保存源包的 SHA/CRC 则已在本包首次回读阶段全部验证，不把私人保管回读夸大成又一次原 RAR 取回。保留原来的 2533/2534 全族缺口与 2391 跨版冲突。

**本轮验收状态**：QUEST12 此份来源受限任务族静态恢复与私人可读证据 **ACCEPTED_SOURCE_BOUNDED**；官方发行身份、任务运行、掉落、完整可玩性仍 **OPEN**。下一 NEXT 依 §4 的 QUEST13 有界查重/原件准备执行。Stage A/B/wiki/R79/总体百分比均与上述限制不变。
