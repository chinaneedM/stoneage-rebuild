# QUEST30｜卡坦恐龙收集任务、旗标35与道具2607的来源冲突

日期：2026-11-08。严格按 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` 从重新读取的远端 `main` **`95fc5875143c7635ee1773f4e2204c3116d2675f`**／tree **`8d4dfc86d6bd7f3b920a344073e0905b5de60068`** 承接。该 HEAD 的十项主线 Actions 当时全部 `completed/success`，0 开放 PR；`README` 最末 QUEST29 给出的最高 NEXT 为 **QUEST30 未专项材料／有界模块复核**。本次重读远端 README、协议、设计决策、时间表、来源登记、模块路线、离线优先级，并依原树指针将 `docs/CURRENT-STATE.md` 的 **2,709,173 B／Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`** 全文读回，原 blob 不改。旧 CURRENT 不是空文件；本篇为新日期连续性覆层。

## 1. 查重、工作对象与来源界线

复核原 QUEST01 **295 脚本、1,349 段 TYPE**、QUEST09 梦幻洞窟及 WORLD21 领宠原指令、QUEST17 牧场、QUEST29 精灵王事件69。初选 `jaruga/event/20501ev1..5` 实际早由 **QUEST16** 逐原件和 36 段完整专项处理，故直接排除，**没有再算新发现**。另一候选 `seimu/event/event01_1/2` 已属 QUEST09 的梦幻洞窟专项。选取仍未专项独立整合的 `seimu/event/event02_n.create` → `seimu/event/event02_1`，恢复卡坦恐龙收集委托的**具体原创建、两轮宠物交付条件、道具、两个 WORLD21 既有宠物实例**。这条脚本的 8 个 TYPE 段本来就已存在 QUEST01；新原脚本 0、新原 TYPE 0。

原始材料是保管的后期**社区混合 2.5** 样本，不认证 JSS1999／台湾1.0／大陆最早1.82之正式运营同部署；文件名和原 NPC 自述不能单独证明历史投放版别。资料目标是供未来离线单机重建使用的有出处历史档案，非原生行为复刻、新引擎、玩家体验优化或网服。

## 2. 原始字节、配置与实物资格

重新读取私人 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip` **995,176B／SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`**：2,205 原成员逐个实际 bytes／SHA256／CRC 与 CHAR01 公共源目录核同，ZIP CRC 全通过。从中读出以下三个完整原件：

| 来源文件 | 原字节 | SHA256 开头 | 作用 |
|---|---:|---|---|
| `seimu/event/event02_n.create` | 348 | `b19afb9d62d` | 原创建块及位置范围 |
| `seimu/event/event02_1` | 3,451 | `63712fde0c36` | 8 个原 TYPE 事件 |
| `jaruga/event/event.template` | 122 | `9c11ac0cbbd` | 现存 `changeevent` → `ExChangeMan` 模板联接 |

源 CREATE 唯一活动配置在 **floor100**，原 `borncorner=230,180,525,200`、图别名16033、方向4。四整数是**范围**，不是单一确定 NPC 坐标；本次不按地形推断某个固定点。原 `seimu/event/event02_1` 8 段 TYPE/完整段 SHA、条件 SHA、物理 TYPE 行和 EventNo 序列 `35,-1,-1,35,-1,-1,-1,-1` 全部与 QUEST01 旧目录核同。总类型 `ACCEPT 5、MESSAGE 2、REQUEST 1`；末段无所列 GetPet／DelPet，不能把任务对白自动转成领取命令。

## 3. 两轮收集的源字面关系，不是已运行任务

| 原段 | 来源条件摘要 | 物理操作字面 |
|---:|---|---|
| #3 | `ENDEV!=35` | 事件35的 REQUEST 文本；没有 GetPet 指令 |
| #2 | `PET=25-223*1` 与 `PET=25-224*1`、`ITEM!=2607`、`NOWEV=35` | `DelPet` 两来源 token；`GetItem:2607` |
| #0 | `PET=25-221*1` 与 `PET=25-222*1`、`ITEM=2607`、`NOWEV=35` | `DelPet` 两 token、`DelItem:2607`、`GetPet:93`、`EndSetFlg:35` |
| #6 | `PET=25-291*1` 与 `PET=25-294*1`、`ITEM!=2607`、`ENDEV=35` | 两 token、`GetItem:2607` |
| #4 | 两组带逗号的 `PET=25-558/293` 或 `PET=25-292/293`、`ITEM=2607`、`ENDEV=35` | `DelPet:EVDEL`、`DelItem:2607`、`GetPet:341`；**本段无 EndSetFlg** |

上述顺序仅为**资料阅读关系**。原物理脚本顺序仍为 `#0..#7`，未推断优先执行、活动重置、第二轮实际开放、宠物真实掉落/交付、原 `EVDEL` 语义、`PET=25-N` 字符串解析或事件谓词中逗号的求值规则。后期同源文本中两轮描述并存，**并不等于初版游戏有两轮此任务**。

WORLD21 旧证据精确将 `GetPet 93` 接到保存档中 **enemy instance93 → template171 → 图别名100319**；`GetPet 341` 接到 **instance341 → template274 → 图别名100362**。本轮**无新增领宠实例、模板或运行交付**；图号同类关系不证明已验原画面。保留 WORLD21 原证据 Git blob `f8614b9e90e548efb6d61e269d725d17ea173a74`。

## 4. 本轮最重要的原内部差异：2607的用途不能按编号直接合并

从私人 ITEM01 ZIP **5,868,386B／SHA256 `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa`** 实际重读物品 `2607` 的两套 94 栏源表（原行位置2190／2585），各行 CP950 完整 SHA 均为 `cf6d2f1dd560c1fa2d0dad360bf0bfef7b4eb582d65d52074d15fd9ea25f52bd`，与旧 ITEM01 分片一致。**脚本对白将2607指作收集恐龙的凭证，但两份同载体保管的物品表都命名为“火難的戒指”。** 原 `imagenumber` 同为22102，台湾1.0原 RD 候选 PNG 有已验像素（本次再读 PNG 与旧 SHA 相同），但这是**跨载体图片候选**，不能用来消除该角色/道具矛盾。原始两行正文和完整对白只在私人包。

可能的版本混合、配置残留、重复 ID 或原运行选择表在此均为 **OPEN**，不可将任何一条候选说成实测原因。不能直接把2607定名“宠物证明”或在未来游戏主表覆盖“火難的戒指”；需要有实际同部署的原生 itemset/脚本、客户端相应显示/行为或可靠原版取证后另建来源层结论。

QUEST05 旧地图覆盖证明：floor100 在当时 955 DAT 条件下为 `NO_MATCHING_DAT_IN_955`。这只是当前目录**没有匹配原 DAT**；并未恢复这一原地图、显示 NPC 或测试原可达路径。没有原生客户端、旧服务器、战斗/捕捉/物品使用运行。

## 5. 私人保管、公开派生与接力

已保存用户 Library 私人 `StoneAge-QUEST30-dinosaur-collector-event35-private.zip`：**10,479B／8成员／SHA256 `cb6f27c43559049bd05976293c3fd260c9d0ba87cc50b5a93f7ea884b7f4225a`**。内含3份完整原 NPC/模板、2份物品行、1幅跨来源候选原图、一份派生报告及自包含本地查阅页。上传后**以新的 Library 文件 ID 再次完整取回**，整 ZIP 字节／SHA 完全一致、8成员 CRC 全通过。只在私人 Library 存档，未把原脚本正文、原物品行、图像、网页上传公开 Git。

公开 `research/recovered/STONEAGE-QUEST30-DINOSAUR-COLLECTOR-EVENT35-SOURCE-R1.json` 仅保留可核数字、有限源路径、来源 SHA/CRC 和否定边界。`tools/stoneage_quest30_dino_collector_source.py` 独立读指定私人存档再生成派生摘要与私人包，复用旧 QUEST29 解析器，不复制另一套项目基础设施。`tests/test_stoneage_quest30_dino_collector_source.py` 逐段对旧 QUEST01/CHAR01/ITEM01 验证 11 项原证据／反例并在仓库 CI 可检查 WORLD21、QUEST09、QUEST05 原派生证据。本地 11/11 PASS；远端 Actions 需真实验收后才可称通过。

**止点和最高 NEXT：`QUEST31_MODULE_GAP_REVIEW_THEN_CROSS_MODULE_INTEGRATION_IF_NO_DISTINCT_SOURCE_READY_TASK`**。剩余任务来源先全面查重并按游戏可见内容价值决定是否继续；若没有来源完整且产生实质新关联的任务族，则将 QUEST 模块标记 `SOURCE_BOUNDED_PARTIAL`、转已有地图/宠物/物品/NPC/任务的有据跨模块整合，不靠重复任务编号凑进度。现有 Stage A **7 PARTIAL + 2 OPEN**，Stage B／wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，总体完成率仍 `null`，原游戏可玩性 OPEN。