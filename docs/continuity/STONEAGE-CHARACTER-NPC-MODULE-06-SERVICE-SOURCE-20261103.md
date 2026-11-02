# CHAR06｜同载体 NPC 服务配置和原始文本批量恢复（2026-11-03）

**阶段：Stage A 历史复原；非新石器设计。** 本轮从远端 `main` HEAD `46bf7fce4f7510a132cd2e3d2d82a0d2c653e950`、tree `0b4f1b3de6d0b2c9da128a608a94559c3393045c` 和完整 `docs/CURRENT-STATE.md` blob `c89e0e33537990aa2132b47c40fef49a985a935c` 重新启动。按连续性协议 §17 承接 CHAR05，人物/NPC 为当前模块，原历史前缀未改。

## 1. 真实原包和文件保管

复用用户私人 Library 已保存原 RAR `stoneage-preserved-mixed25-original.rar`，361255180 字节、SHA-256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`，实测重新全文件 SHA 相符。RAR 目录共 7952 成员。本轮用 libarchive 实际解出 `gmsv/data/npc/` 下**2205/2205 份原文本（1930332 字节）**，逐文件和压缩包目录原始大小、CRC32 核对全过，错误0；另核每份原始文本 SHA-256。这与 CHAR01 的既有文件范围一致，不算发现 2205 名新 NPC，亦不认证此社区混合包属于官方纯净 2.5 或同一运营部署。

对 CHAR05 余下 105 种仅有索引的图号，本轮尝试从**同一 RAR**取原像素源文件。实际源目录：`spradrn_5.bin` 10164B，可完整解出，SHA-256 `5f13c956cf013e073298ab91667d3aaa17767b26ba94d696514726950ce94de6`，含 847 条物理索引；`spr_4.bin` 声明 5588120B，但 libarchive 在输出 1048576B 后报告 `Prefix found`，所得**未完成前缀不予验证和发布**；`real_15.bin` 声明 763908374B，在0B时报 `Invalid symbol`；`adrn_15.bin` 声明 18765120B，在0B时报 `Parsing filters is unsupported`。因此余下 **105 图号/587创建配置仍为 INDEX_ONLY，新增完整SPR/原RD像素=0**。这是当前解包工具能力边界，**不等于原包损坏、这些图不存在或已经获得原图**。不反复试下载大包或虚构原动作。

## 2. 原NPC服务文本与数值的实际来源联接

不继续扩大旧SPR解码器，直接从上述原文本中将同RAR `NPCCREATE` 中 `enemy=模板名|file:相对路径` 与 `NPCTEMPLATE` 的 `functionset`、具体原参数文件逐原路径联接；本批选四种高度可感知服务。每一条均有源创建相对路径、创建块序号、原创建文件SHA、源模板名、图号/floorid、实际参数原路径及原参数文件完整SHA，原文仅私人保管。

| NPC原模板功能 | 源创建→参数实物联接 | 实际原参数字段（仅静态值） |
| --- | ---: | --- |
| `SavePoint` | 21 | 21 个不同的 `ID` 与 `Born` 元组；11 个文件匹配数值形式 `GetItem` 条件 |
| `Bus` | 7 | 7 组 `RouteTo1` 点列，点数 10、11、15、45、55、66、109；`WaitTime` 六组为180、一组120，`NeedStone` 分别有0、20、25、30、40、50等原字面值 |
| `PetShop` | 16 | `nomal_rate` 13组1.0、2组0.6、1组0.7；14组有 `special_rate:1.5`；6组有 `pool_flg:1` 和 `pool_cost`（5组200、1组2000） |
| `PetSkillShop` | 3 | `skill_rate` 两组1.0、一组1.2；`pet_skill` 原值分别11、31、90 |

以上47条指**原源配置与参数文件的关联次数，不是47个独立NPC，也不是全部功能的覆盖量**：CHAR04统计含无独立 `file:` 参数来源的配置，例如 `PetSkillShop` 共有21份功能配置、此次只有3份独立原参数文件。字段名拼写（包括原 `nomal_rate`）和字面量未擅改。价格、时间单位、服务器执行/同服出现/实际画面均未知；`WaitTime=180` 不直接翻译成实际等待180秒。公车 `RouteTo1` 只从原源记录经纬/二维坐标点列，既未复原运行交通，也不自动认作台湾1.0线路。

示例**原字节来源**：`genout/sp.create#0`→`genout/sp_1000_94_99`（`ID=4`、`Born=1000,92,99`），`chatroom/bus.create#0`→`chatroom/bus.arg`（`RouteTo1` 66个点、`WaitTime=180`、`NeedStone=50`），`genout/shop_m.create#21`→`genout/psks_1008_28_24`（`skill_rate=1.0`、`pet_skill=11`）。均为原**文件定义**，不等于历史客户端调用了这些定义。

## 3. 私人可见资料及公开边界

- 已生成**私人自包含静态观察页** `StoneAge-CHAR06-private-NPC-service-observer.html`，可按四类服务、源创建路径、引用参数路径、序号检索47份真实解包原文。私人 HTML 35363B / SHA-256 `cbc6a61fb871292ef6211d4b34f2e5958415438736586ac95b729d45337cd2f8`。页面选择器是现代研究界面，不代表旧游戏屏幕或已完成浏览器运行验收。
- 衍生全量47行数值证据 JSON `STONEAGE-CHARACTER-NPC-MODULE-06-SERVICE-SOURCE-RECEIPT-R1.json` 本轮私人可取17,084B / SHA-256 `57aff8512213208e76aaffd8a6a4e8b2885a48160db5fc44a4cafbdc66ea3c9c`；原NPC对话正文与版权资产**不入公开Git**。全量 JSON 包含逐行原文件SHA/路径/数值及公车原点列摘要；这份报告至少保存完整源证索引的文件身份，未冒称完整私有材料已永久入Git。
- 本轮对2205原NPC文件再次独立核原RAR目录 CRC32/大小，2205/2205相同；新分析只针对有直接原文本的数值字段，不以图形同号/模板名称/静态 `functionset` 假定服务已经运行。

## 4. 状态与下一步

**CHAR06 结论：** 有真实原NPC配置内容增量：47条来源限定服务参数，已有可读的路径及数值。其余105图号依旧没有完成资格认证的实际 SPR/REAL 像素。不得把现代观察器或纯静态参数解释为已进入商业游戏。

**最高 NEXT：`CHARACTER-NPC-MODULE-07`。** 仍留在人物/NPC模块，直接用已实际取出的2205份原文本扩展 `TownPeople`/告示/商店等原对白或原功能的**成批来源索引**，优先确认已有 `file:` 的实内容和特殊缺失路径；仅发布有版权安全的源摘要、参数/文本类别与业务关系，不公开完整商用原文。到可读材料完成且缺件被精确记录的模块止点后再切入地图场景模块；不得另起通用辅助框架。

保留 `Stage A=7 PARTIAL+2 OPEN`、`Stage B/wiki=GATED`、`R79=PAUSED_NON_BLOCKING`、`overall_percent=null`。此前失败/修复记录与原 CURRENT 前缀全部保留，历史身份仅限此混合保存载体。
