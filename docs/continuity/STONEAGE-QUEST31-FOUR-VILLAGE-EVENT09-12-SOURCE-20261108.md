# QUEST31｜事件9—12：四处原NPC、保护石交换与41／42附属条件（2026-11-08）

按 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` 从本次**重新核验**的 GitHub `main` `4751ebe021110e96867d8c4d802669791bfd1ba4` / tree `06dcb561a86de9187b106a4528d8256c96f1cc4a` 承接 QUEST30。读取 README／协议／决策／历史／来源库／路线／模块和离线优先级，以及原 `docs/CURRENT-STATE.md` 2,709,173 B、Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 全文。起始主线最高接力是先查剩余任务缺口，若只剩旧来源重复便转跨模块整合。此记录只作**增量**，原巨型 CURRENT 不覆盖。

## 1. 先查重，不以编号凑新内容

原 QUEST01 源限定全索引含 **295 份原脚本、1,349 个 TYPE 段、14 个路径目录**。本次复核最初的 QUEST16 20501ev1..5、QUEST09 的 seimu event01_1/2、QUEST30 的 event02_1、QUEST29 的 king/event69、QUEST22 的 hekisei 等来源；它们已有明确专项，不重新计为新任务。选择 `sainasu/event/event09-12.create` 所指向的 **四份保存原脚本**：`event09`、`event10`、`event11`、`event12`。四脚本 **3/5/5/5 = 18 个旧 TYPE** 全已列入 QUEST01；本轮新增脚本发现 **0**、新增 TYPE 发现 **0**。内容增量是四处 NPC、跨地点物品、事件旗标、原物品源表和地图资格的一条**可查询、来源可追溯关系链**。

本批仍来自后期社区混合2.5保存来源，其原始 `event` 目录命名、地理位置与 NPC 对话**不能证明**是 JSS1999、台湾1.0、大陆1.82的官方同服任务。下面“事件链”只是原脚本静态关联的阅读方式，不是游戏执行顺序。

## 2. 四原 NPC、位置与地图

原 `sainasu/event/event09-12.create` 四个 CREATE 块及 `jaruga/event/event.template` `changeevent`→`ExChangeMan` 由原 SHA 与既有 CHAR01 全清单严格联接。四个原 borncorner **四整数原样留存**；此处只摘坐标前两个数，不宣称原玩家实际见到 NPC。

| CREATE序号 | 原NPC短名 | 原floor／x,y | 原图形别名 | 对应脚本 | 该955 DAT来源资格 |
|---:|---|---|---:|---|---|
| 0 | 村姑 | 1200／97,75 | 16205 | event09 | MAP09原DAT散列候选已存 |
| 1 | 村姑 | 1300／65,65 | 16206 | event10 | **NO_MATCHING_DAT_IN_955** |
| 2 | 卡坦的年輕人 | 1400／71,76 | 16203 | event11 | MAP09原DAT散列候选已存 |
| 3 | 夢德（族長） | 11107／24,6 | 16057 | event12 | MAP09原DAT散列候选已存 |

源地图资格复用旧 QUEST05 对应楼层的原DAT散列与覆盖状态：1200 `41cae3e9…15c5f07`，1400 `a706890e…19af54c73f`，11107 `1adbf434…ed9ef3cc`。本轮**没有重新取这三张 DAT 字节、重新绘制图块或运行原客户端**；1300在本955件就绪目录无匹配，不能据此说原游戏没有1300。虽然脚本原短名涉及村名，不由数字floor推出四座独立村庄、岛屿归属或已闭合世界地图。

## 3. 来源原条件与任务物品关系

| 源脚本／原段 | 原条件字面核心 | 原命令字面 |
|---|---|---|
| event12 #0 | `NOWEV=9&NOWEV=10&NOWEV=11&ITEM!=2419&ITEM!=2420` | `GetItem:2419,2420`（两块保护石） |
| event10 #0 | `ENDEV=11&NOWEV=10&ITEM=2419` | `GetItem:2421`、`DelItem:2419`、`EndSetFlg:10,12` |
| event10 #1 | `ENDEV=12&ITEM=2419` | 同样交石／取2421，但 `EndSetFlg:10` |
| event11 #0 | `ENDEV=10&NOWEV=11&ITEM=2420` | `GetItem:1052`、`DelItem:2420`、`EndSetFlg:11,12`、`Charm:1` |
| event11 #1 | `NOWEV=11&ITEM=2420` | 同样交石／取1052，但 `EndSetFlg:11`、`Charm:1` |
| event09 #0 | `ENDEV=12&ENDEV=10&ENDEV=11` | `GetItem:1357`、`EndSetFlg:9` |
| event12 #2/#3 | 源条件引用事件41、42及物品2736 | `GetItem:2736`；#3另有 `EndSetFlg:41` 和 `Charm:1` |

另有五个 REQUEST、五个 MESSAGE 段均保存准确位置、条件 SHA。event12 #1的源原条件为 `ENDEV=12&ITEM=2736,ENDEV=42&ITEM=2736,ENDEV=41&ITEM=2736`，原逗号不可直接被理解成已验证的“或”求值。event10/11分别存在 `EndSetFlg:10,12`／`EndSetFlg:11,12` 的**一整条逗号字面**以及不含12的替代分支；它们是否会分别设置多个旗标、按何优先级匹配、能否反复获奖均 **OPEN**。**新查到一个旧目录投影缺口：** QUEST01 公开 `end_set_flags` 只收纯整数字面，整个旧索引中旗标12的正规化记录为0，但原脚本实际有上述两条 `10,12`／`11,12`。这个0不是源文件没有12，更不能因而否定该任务联接。本批把两条完整原字面与旧归一化0并列保存，**不**修旧历史、拆成已证明运行的两个旗标事务。event12 对41/42的引用与 QUEST22 先前所载的42门槛可以作为**数字旗标来源交叉线索**，但不是同任务顺序或所有玩家实际可达的证明。`Charm:1` 原字面不能擅自定成实际效果。

## 4. 物品与原图来源分开

6个源道具ID：1052、1357、2419、2420、2421、2736，分别是 **芙雷雅Lv1鎧6、黃色大首飾、霍特爾的保護石、卡坦的保護石、勾玉、風的豎琴 [風]**。私人ITEM01中的两套94栏原物品表共 **12 原行**，每行重新按CP950编码、完整 SHA与旧 ITEM01 七公开分片逐字段证据一致，两表各ID的原行在此六项均完全相同。6个ID恰有6种原 `imagenumber` 别名及6个此前确证的**台湾1.0原RD候选像素**；本轮从私人包重取六 PNG、逐 SHA验证，**不是**证明该后期任务在台湾1.0官方服存在或使用同一物品、美术和道具属性，也没有新增RD解码。

## 5. 原件复验与私人保管

私人 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip` **995,176B／SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`** 及 `StoneAge-ITEM01-private-two-itemsets-832-original-RD-icon-observer.zip` **5,868,386B／SHA256 `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa`** 本轮均全 ZIP SHA 重读，2,205 NPC 文件逐全文大小/SHA/CRC同CHAR01；物品 ZIP 838成员CRC，所选6原脚本/模板完整SHA与原目录、18个事件段规范 SHA 100%一致。未重新读取361MB父RAR，不重述为初版客户端启动。

`StoneAge-QUEST31-four-village-original-private.zip` 已存个人 Library 并二次回读整包：**27,565 B／SHA256 `796682fd3621a2bfecab03e7e199ca16936f95cad75f6a7842e6517f1e04dd42`／26成员／CRC全通过**，包含6份NPC原文件、12份原物品行、6幅跨载体候选PNG、一份报告及一份私有离线原文查阅HTML。公开Git**不存**商业对白、原脚本全文、原物品行、原DAT、原图PNG或HTML。私人HTML浏览器执行／原NPC实际游戏交互均未声称验收。

公开只提交[源数值、SHA与证据边界](../../research/recovered/STONEAGE-QUEST31-FOUR-VILLAGE-EVENT09-12-SOURCE-R1.json)、可选私人再提取工具、13项派生回归、最小专项工作流和连续性指针；该专项CI只能验证旧目录/派生数值，**不能**验证私人原像素／原商业游戏。最初独立脚本启动用直接Python路径遇到`ModuleNotFoundError`，随后改以正确`python -m`运行；源输入未改、13/13单测成功，修正过程如实保留。

## 6. 止点、模块转换和下一优先级

`QUEST31=SOURCE_BOUNDED_STATIC`，四处配置与三地图旧SHA候选只是可检索关联、非已有可玩的四村任务。现有 Stage A仍 **7 PARTIAL + 2 OPEN**，Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**，整体完成率未知。**NEXT QUEST32：** 先复核QUEST任务模块剩余**确有独立材料价值**的缺口；若可得只剩旧索引或无合格同源DAT／对应官方版本文件，明确记录任务模块 `SOURCE_BOUNDED_PARTIAL` 的阶段止点，转为跨地图／NPC／物品／宠物的整体关系和来源缺口复核。不为积累QUEST编号反复做小型原字段辅助工具，更不开发网游基础设施或过早选择新单机引擎。

本段属于大CURRENT未改时的加法接力；候选、PR、Actions、主线合并和最终验收 **须在实际远端完成后再追加**，不可提前宣称完成。


## 7. 远端合并与正式验收回执

[PR #271](https://github.com/chinaneedM/stoneage-rebuild/pull/271) 已经 squash 合并到 main `a4d2855698edb0578a696566569ce317d49084e2`／tree `93472ca96dbce4830d1dfdee28d6f83cad375d3b`。候选最终提交 `e63364c752df83bfaa94c8a2c79cea8ce3b4f526` 的 **14/14** GitHub Actions 已实际 `completed/success`，包含QUEST31 PR专项run42488670285/job128756017935与push专项run42488666891/job128756007836；合并后主线 **11/11** Actions 亦全部 `completed/success`，QUEST31主线run42488758749/job128756290065真实成功。公开源、测试、派生JSON、文档、工作流Git blob已由主线完整树独立核定，主线与最后候选全树相同；旧 `docs/CURRENT-STATE.md` blob c89e0e33537990aa2132b47c40fef49a985a935c 未改。`EndSetFlg`复合12漏收已用新报告/13项回归补证；最初候选与补证候选均有远端历史、没有改写旧来源。私人最终包27,565B／SHA796682fd…已上传Library后完整回取并CRC验26成员；初版/中间本地测试包非最终保管版本，不能误称最终。详细运行ID与出版证据见[验收收据](../../research/recovered/STONEAGE-QUEST31-PUBLICATION-ACCEPTANCE-R1.json)。最高NEXT仍QUEST32审查任务模块止点与跨模块源关系；这份后验提交自身的Actions仍需之后另据真实远端状态判断。
