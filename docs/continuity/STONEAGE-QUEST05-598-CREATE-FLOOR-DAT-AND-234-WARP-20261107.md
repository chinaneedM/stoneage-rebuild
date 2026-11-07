# QUEST05｜原任务/NPC创建点 → 已保存地图DAT、条件传送来源关系（2026-11-07）

## 启动锚点和工作目标

从GitHub远端main `c4b738f30a0c6d7377093d75cd4c231480ce1818`重新核实 HEAD、tree、最新提交、Actions、无未合PR、连续性协议、全量历史 `docs/CURRENT-STATE.md`（原blob `c89e0e33537990aa2132b47c40fef49a985a935c`、2709173字节）、模块路线和最新MAP10工作止点。本批接其 `QUEST-MODULE-01` 优先事项，但发现QUEST01–04早已存在、不能虚称首次复原任务；遂执行**QUEST05源限定内容整合**：让已有原创建脚本和已恢复的地图实物用可检索的关系真正连接起来，不重复抽取原图，不新开发游戏。

## 实际使用的七份来源限定可复算公开索引

[598条NPC创建、236源楼层、234条条件传送字面候选索引](../../research/recovered/STONEAGE-QUEST05-598-ORIGINAL-CREATE-FLOOR-MAP-AND-WARP-CROSSWALK-R1.json)逐条保留来源Git blob、原CREATE文件/块序、SHA256、参数路径/原字节SHA、实际原 `floorid` 与真实DAT文件SHA。

- QUEST01 315条：`STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json` Git blob `52db8b4b6cd43cd2afa4a8d2e8460f214933f5e2`
- QUEST02 202条：`STONEAGE-QUEST-STORY-MODULE-02-ORIGINAL-WARPMAN-CONDITION-SOURCE-R1.json` blob `006f47a7aed7a565a643d6bf0d1f477a584d63db`
- QUEST03 56条：`STONEAGE-QUEST-STORY-MODULE-03-QUIZ-TIMEMAN-ORIGINAL-SOURCE-R1.json` blob `f5f3581460e642c64a3dc71626cf0cba3d4a768e`
- QUEST04 25条：`STONEAGE-QUEST04-SOURCE-BOUNDED-FAMILIES-R1.json` blob `f2ca24ed0897e8ccba743b7aeba43febe52358ca`
- 955份同社区保存RAR原DAT的物理字节/尺寸/SHA索引：`STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json` blob `1ef8c004179128ea44ffa4fb4259748bc8c83911`
- MAP09 691份>99原图候选就绪DAT：`STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json` blob `137580e7c25aadf3d679b6ebfb5080b79912cc4f`
- MAP10新增60份低值语义未明DAT：`STONEAGE-MAP10-PUBLIC-ORIGINAL-SOURCE-CUSTODY-R1.json` blob `93fc47684d96c96ce2b67ac91838b92b4dabe3a3`

这七份记录保留的混合2.5社区保存RAR来源身份为 `d71e2e6766e8ac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`。数字同名之所以能被联接仅是**同一个可复核的保存载体内容引用**，不证明当年某商业服同时部署、任务实际生成或地图能进入；同一DAT的可见候选位图另外来自**台湾1.0官方零售客户端**，仍不是同源同部署验证。本批新获早期官方原始任务数据 **0**；新跨模块可检索关系来自已保存且已验来源文件，不冒充新历史实体。

## 创建→地图 DAT 核实结果（不是任务数量）

| 同保存源原创建关联等级 | CREATE原创建引用数 | 不同CREATE原楼层数 | 资格 |
|---|---:|---:|---|
| MAP09候选>99真实RD可用 | **352** | **168** | DAT字节有源，跨版位图只作候选；1–99和native排序不定 |
| MAP10后补60份、低值未知 | **11** | **4** | >99图候选可观察，1–99原值不猜含义 |
| 当前DAT存在但>99原RD仍缺 | **147** | **50** | 有原地图结构及SHA，未补造贴图 |
| 当前955件DAT没有同编号文件 | **88** | **14** | 仅当前保存源缺文件，不是历史地图/任务不存在 |
| **合计** | **598** | **236** | 四批来源引用数；不等于236或598个任务 |

14个当前DAT未命中楼层号的字面值：100、119、200、300、400、500、830、1000、1100、1300、3000、3400、6000、10920。全量按楼层索引、CREATE具体原文件和源SHA已收录入机器目录；不能因为`floorid`与DAT文件同数字就进一步断言所属**南岛、北岛、某村庄、原世界线**。

## 静态条件传送关联：234条候选，保留条件及无效哨兵

从QUEST02已保存313段控制源中，先以**参数文件路径+原整SHA**连接到202个真实CREATE，再从已解析的原 `WARP` 三整数提取**209条非零首整数**来源限定候选边；遇 `[0,0,0]` 等首整数为0的字面记录，共**94次CREATE实例展开**，禁止错当地图0可达出口。从QUEST04再联接9个猜拳参数原SHA的赢/输 `WINWARP/LOSEWARP` 共**18条**，及7组 `event69` 原脚本的 `warp_literal` 共**7条**，合计 **234条静态边**。目标DAT分组：137条MAP09、3条MAP10、72条DAT在但缺合格原图、22条当前955缺同号DAT。

关系边保留源脚本和来源片段SHA、具体源CREATE位置、条件关键字计数、目标楼层及坐标。**既不是可运行路线，也不证明传送条件真实满足、地图出入口能通过、同原服运行、原NPC发生交互。** 不能将`event69`文件名直接晋级为真实运营节庆，也不能将相同ID的别版地图拼接成一个已验证世界。

## 与 DD-032 内容分类原则的具体落地、缺口与后续

这次提供了可从**脚本创建点→floorid→原DAT→资格等级→条件WARP目标楼层**查询的实际原内容联接。地图岛屿/村庄字段暂不虚填；`quest_origin_class`一律 `ORIGIN_UNRESOLVED`，先和运营活动历史档案分离。商品/宠物/奖励关系只沿既有有证索引，不在此批冒称任何奖励实际触发。

[独立回归测试](../../tests/test_stoneage_quest05_original_floor_crosswalk.py)从这七份原公开索引重建全部598创建行、逐原SHA和955图源资格比对、精确重建234条静态传送及94次零值排除，另强制检测缺图、不存在DAT、未证地理分类及原生运行负例。[专用CI](../../.github/workflows/verify-stoneage-quest05-source-floor-crosswalk.yml)验收该派生关系数据，不代表CI读取私人商业原图或执行原客户端。

**止点：** QUEST模块仍 `SOURCE_BOUNDED_PARTIAL`；原本体/永久/时限活动身份仍需各地区同版本证据。Stage A **7 PARTIAL + 2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**，总体 `overall_percent=null`。历史CURRENT全blob保留，不能截断重写。

**NEXT：** 若有真正可读且未审过的原任务来源可做`QUEST06`局部批量来源核验；否则按既有QUEST04源限定止点进入 **GAMEPLAY-MECHANICS-MODULE-01**，从真实客户端/服务端规则实物复原捕捉、战斗、骑宠、成长、合成与状态。新分类/关系只随真实原内容新增维护，不再建立另一套空架构。
