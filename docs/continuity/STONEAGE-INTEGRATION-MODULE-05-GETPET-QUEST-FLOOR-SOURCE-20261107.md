# INTEGRATION05｜原 GetPet 脚本创建点与已认证地图DAT资格重新接通（2026-11-07）

## 起点、真实复原对象与材料边界

从最新已合并主线 `253da64e4d1e726e89a4389c17dc5a0baf8eabfe`（tree `89c6b3f9a9f8c557870a9c5e79526c92d53738d4`）启动；重读完整 `docs/CURRENT-STATE.md` 原生Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`、连续性协议、模块顺序和Actions。INTEGRATION04的11条捕捉条件、3项候选Actions和合并后主线11项Actions均已核实；它并没有证明NPC脚本的 `GetPet` 参数等同于原编译野怪捕捉键。

**本轮目标不是重提取任务或地图**，而是准确补齐一个旧跨模块可见缺口：INTEGRATION01曾把同一个社区保存混合2.5 RAR中 **24条有源 CREATE 引用的 `GetPet` 脚本**连到当时部分MAP01原地图；其后MAP04/09/10已认证955个保存DAT、691组>99候选地图及其原图覆盖，QUEST05又将598条CREATE创建点连到了955批DAT。若仍仅查询INTEGRATION01，地图的当前可观察资格和旧提取错误容易混淆。INTEGRATION02独立已认证的1000.DAT仍必须保留；不能被QUEST05「当前955列表无同名文件」覆盖。

**来源与本轮操作：** 只读4份原有的来源限定派生Git blob，不新增原版权游戏源字节，不重新运行x86、解码RD、绘制地图或拉取RAR。4个上游是：
- [INTEGRATION01](../../research/recovered/STONEAGE-INTEGRATION01-NPC-PET-QUEST-ITEM-MAP-SOURCE-GRAPH-R1.json)，Git blob `5e526512c0277e19ca41dfcd934c230404d1dfb4`：24 CREATE原块SHA、23脚本整SHA、原 `GetPet` 原行序/数字与同脚本任务物品候选；
- [INTEGRATION02](../../research/recovered/STONEAGE-INTEGRATION02-ORIGINAL-SCENE-DAT-RD-CROSSMODULE-R1.json)，blob `2303f1df3749ca28a4f9539869359666021b8783`：对1000.DAT的独立实物整SHA/160×160及100、3000原MAP01提取失败记录；
- [QUEST05](../../research/recovered/STONEAGE-QUEST05-598-ORIGINAL-CREATE-FLOOR-MAP-AND-WARP-CROSSWALK-R1.json)，blob `b004e488e1d0a93ca7c14eb90abb584b23f341fe`：全部598个创建点、955原DAT资格与MAP09/10图像候选；
- [INTEGRATION04](../../research/recovered/STONEAGE-INTEGRATION04-COMPILED-CAPTURE-PET-ITEM-SPR-SOURCE-BRIDGE-R1.json)，blob `69fbac7fd946f14b6ccad9e5882c79c62f86dbf0`：原编译捕捉key53的11个数值，用作**不同机制不可混ID**的交叉负证。

原社区保存RAR原身份 SHA256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`。同归档不证明某正式运营服务器原样部署，更不证明属于台湾1.0/JSS1999/大陆1.82。

## 24个原创建引用的更新后地图实物资格

| 对象 | 原创建数 | 精确断言 |
|---|---:|---|
| 与MAP09有完整DAT SHA且>99原RD候选图已准备 | **16** | 仅现代原图候选观察资格，非原游戏运行渲染 |
| 原DAT整SHA有证、但>99所需来源RD缺件 | **5** | 有原地图格，不补造画面 |
| QUEST05的955表无文件、但INTEGRATION02已有独立整SHA认证 `1000.DAT` | **1** | `160×160`、153608B、SHA256 `94b19cb59d72b7b48da70d2741ba68516caad970297fd48ed11ef720fa3ea97e`；旧MAP01原提取失败仍保留 |
| 已存来源尚未认证完整原DAT（100、3000） | **2** | 之前原MAP01有读取/CRC错误，**不代表历史缺地图** |
| **合计** | **24** | 23份原脚本、19个不同原楼层 |

24条 `CREATE` 的目录键为 `原CREATE文件路径+块序号`，并逐条核对原脚本路径、**整脚本SHA**、原楼层、同一CREATE的QUEST05**整文件SHA**。历史INTEGRATION01的**源CREATE块SHA**另存，两个不同哈希范围不能互相代替。绝不因路径相似或数字相同跨来源并表。以上是地图资料可查询性的分级提升，不是本轮新增24个NPC、24个任务、16张新地图、16条已运行宠物任务。

## 原脚本命令、任务物品与野怪捕捉应分开

这24份创建关联覆盖23个不同 `GetPet` 来源脚本、36个不同 `GetPet` 参数数字。相关QUEST01控制段先前已有101个不同物品候选数值（包括可能是条件、随机权重等其他字段），本轮只是把原脚本与地图资格连通，没有观察到实际领取宠物、扣除物品、任务保存或一次NPC对话。

这36个 `GetPet` 字面数字与INTEGRATION04的11个**编译野怪捕捉条件key53**当前精确数值交集为**0**。这是两个不同机制目录的负面数字交集，**不证明它们历史上绝对无关联**，更不能把NPC脚本数字认作官方宠物物种数、2016模板ID或台湾1.0宠物图号。原 `event` 文件夹名仍为 `ORIGIN_UNRESOLVED`，不擅称运营节日或常驻任务。所有地图南北岛/村庄层级继续UNKNOWN。

## 交付/独立验收/下一工作

[INTEGRATION05逐24创建点的完整源限定索引](../../research/recovered/STONEAGE-INTEGRATION05-GETPET-QUEST-MAP-ORIGINAL-SOURCE-GRAPH-R1.json)保留两个不同CREATE SHA范围、原脚本SHA/行号、原 `GetPet` 字面数字、同源任务物品候选及每张DAT SHA/字节/来源级别和已有提取错误。独立 [8项测试](../../tests/test_stoneage_integration_module_05.py)从4份原Git blob逐记录反算所有24行并检查重名错接、原1000独立DAT丢失、100/3000幻造地图、抹掉原脚本重复数字、SOURCE_READY误说成原客户端运行、`event`误归活动与 `GetPet`/捕捉键误合并。CI只能验证公开派生文件，不能证明商业原件重新执行。

历史 `CURRENT-STATE.md` 原完整字节不更改，原先MAP01读取失败和INTEGRATION01/02/QUEST05事实均不删改。Stage A **7 PARTIAL + 2 OPEN**，Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，overall_percent=null；任务/玩法的真实原版同部署、奖励发放及状态持久化仍OPEN。

**当前止点与 NEXT：** 对这24条原来源已完成可证的任务→NPC CREATE→地图DAT来源资格交叉核对。对100/3000只在重新获得可信完整DAT原件或明确改善读取错误的独立字节来源后重新打开；对另外5条缺图楼层只在取得原RD/REAL真字节后提升图像资格。下一优先回22域，从已有原件寻找真正新的可观察游戏内容或有源机制行为，不对当前关系重复增报告，也不建新引擎/网服。
