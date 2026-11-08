# QUEST13｜哥亚山洞窟乌力送信、月光花与回信：有来源的原任务族（2026-11-08）

## 1. 远端起点与止点

从重新核验的远端 `main` **`955a633ea7b036d627ecc8d81b288a9251730deb`**、tree **`167fe6ee4780954b182780ab1d2ce0a1349f6e43`** 启动；最新提交为 QUEST12 的已验收后验。检查 HEAD、最近提交、Actions、无开放 PR、连续性协议、README、完整当前状态原 blob、设计/时间线/来源登记、路线/模块优先级及 QUEST12 最新接力。`docs/CURRENT-STATE.md` 原 blob **`c89e0e33537990aa2132b47c40fef49a985a935c`，2,709,173 字节**，历史前缀全保留；本轮用新的加法记录而不覆写它。

**游戏对象：** 哥亚山洞窟中的乌力斯凯、乌力美、花店以及周围八个原创建 NPC 对应的送信／花朵任务族。**来源：** 已保存的后期社区 mixed25 组合服务器文件，`ORIGIN_UNRESOLVED`；本材料不认证日本 JSS1999、台湾零售 1.0 或大陆简体 1.82 的原版同部署内容，也不证明常驻/活动历史分类。恢复范围为真实原配置、物品有向引用、6 张原 DAT 的 10 处原值和私人原文、图像候选观察，不执行原游戏或实现新的任务系统。

**查重：** 旧 QUEST01 原 1,349 个 TYPE 段的通用索引已收录此族 16 段，本包不是新发现 16 段、也不重算这些通用统计。QUEST04 属另一来源有限任务族；QUEST06–12 的叙事、地图、道具交付均保留，并未发现该 `jaruga/event/event07n.create` 完整故事族已有相同的独立来源—道具—原六图位置交付。先前记录中的其他乌力、送信或花朵，不靠相似中文名合并。

## 2. 真实来源、保管与完整性

- `StoneAge-CHAR01-mixed25-all-npc-original-private.zip`：**995,176 字节／SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`**。全 **2,205** 个原 NPC 成员的路径、长度、整文件 SHA256、CRC32 逐一与既有 CHAR01 Git 数值清单完全一致；非仅验证本族。此族选中 `jaruga/event/event07n.create` 加 `jaruga/event/event07_1`—`_10` **共 11 个原文件**，全部可逆 CP950，原字节、源行号、每段起止偏移和散列另见[公开派生数值证据](../../research/recovered/STONEAGE-QUEST13-GOA-ULI-LETTERS-ORIGINAL-SOURCE-R1.json)。所有 10 条 CREATE 的切片 SHA 与此前原始 CREATE 清单逐项相同，10 个脚本外键均按真实源路径和文件 SHA 对应。
- 已发布旧 QUEST01 TYPE 段目录的 Git blob 为 **`52db8b4b6cd43cd2afa4a8d2e8460f214933f5e2`**。本轮 16 个原段的 ordinal、TYPE、EventNo 和严格 UTF8 条件散列逐段与目录核同；旧目录的 16 段只是**独立交叉审计**，没有冒充 16 段新原件。没有自动改写任何原拼写、原标点、原数量省略或对白。
- `StoneAge-ITEM01-private-two-itemsets-832-original-RD-icon-observer.zip`：**5,868,386 字节／SHA256 `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa`**，原包 **838 成员** ZIP CRC 通过。五 ID 的两份各 94 原字段物品行（共 **10 个物理行**）逐 CP950 字节重建、SHA 与 `item-module-01` Git 原数字索引 **01/02** 双向吻合。复用已验证的台湾 1.0 原 RD 候选 PNG 和 RGBA 双散列，没有本轮新解码原像素。物品表与台湾原美术不是已证明的同部署商用组合。
- `StoneAge-MAP09-691-source-ready-map-catalog-private.zip`：**46,844,444 字节／SHA256 `d84d0800dd600798769dfb7251a1d7816588ac061ccc27812ac64a37922d4a8a`**、**4,195 成员** CRC 通过；内层 955 DAT 原包整 SHA 相符。确实读取 `20401`—`20406` 六份 DAT，来源验证收据 Git blob **`137580e7c25aadf3d679b6ebfb5080b79912cc4f`**；每份整 SHA 和三平面数值位置从真实原字节独立回读核验。现成原图候选缩图只加现代位置圈标；**不是**原生客户端画面/碰撞/任务传送证明。

## 3. NPC、场景与原任务字面（FACT 仅对本保存载体原文件）

| CREATE序号 | 原 floor/(x,y) | 原图形别名 | 原参数 | 来源内角色／功能 |
|---|---|---|---|---|
| 0 | 20401/(14,10) | 100252 | event07_1 | 乌力斯凯：发信／回信与奖励 |
| 1 | 20404/(44,13) | 100252 | event07_3 | 乌力花店：任务花朵 |
| 2 | 20406/(36,34) | 100250 | event07_2 | 乌力美：收信／回信 |
| 3 | 20401/(30,26) | 100250 | event07_4 | 乌力姆：对白 |
| 4 | 20402/(25,18) | 100250 | event07_5 | 乌力库：对白 |
| 5 | 20403/(19,19) | 100252 | event07_6 | 乌力隆：对白 |
| 6 | 20404/(24,36) | 100250 | event07_7 | 乌力卡：对白 |
| 7 | 20405/(40,32) | 100252 | event07_9 | 乌力泰：对白 |
| 8 | 20406/(20,25) | 100252 | event07_8 | 乌力可：对白 |
| 9 | 20406/(17,38) | 100250 | event07_10 | 乌力米：对白 |

10 个原 CREATE 共 **16 段**，按脚本 4/3/2/1/1/1/1/1/1/1；实际 TYPE 为 **3 ACCEPT、2 REQUEST、11 MESSAGE**。本载体源脚本明确出现事件号 **7 和 8**，但不是经运行验证的原故事节点顺序。

| 本源脚本与段序（零基） | 字面原条件 | 字面原数值操作／阅读关联 |
|---|---|---|
| `event07_1 #1` | `LV>0&ITEM=2414` / EventNo7 | `GetItem:2425`，乌力斯凯交付信件来源指令 |
| `event07_3 #0` | `NOWEV=7&ITEM=2414&ITEM=2425&ITEM!=2424` / EventNo7 | `GetItem:2424`，花店交付花朵来源指令 |
| `event07_2 #0` | `NOWEV=7&ITEM=2414&ITEM=2424&ITEM=2425` / EventNo7 | `DelItem:2425,2424`、`EndSetFlg:7`，乌力美接收 |
| `event07_2 #1` | `LV>0&ENDEV=7&ITEM=2414` / EventNo8 | `GetItem:2426`，乌力美回信来源指令 |
| `event07_1 #0` | `NOWEV=8&ITEM=2414&ITEM=2426` / EventNo8 | `GetItem:1206`、`DelItem:2426`、`EndSetFlg:8`，乌力斯凯回信奖励来源指令 |

这些仅是**原文件可追溯的有向物品关系**，箭头不是实测的事件解释器、同回合得失物顺序、完整交互或任务可完成性。`GetItem`／`DelItem` 均为裸 ID，不自动假定数量是 `*1`。`event07_3 #1` 的 `ENDEV=7,ENDEV=8&ITEM=2414` 原逗号与 `&` 混写，原样保留，**不把它自动解释成 OR/AND**。不同段的 `Nomal...` 原拼写及 CP950 繁体未被静默修正。

**道具 ID：** `1206/2414/2424/2425/2426` 五个不同 ID；两源主表各一原行，总 10 行，五者有已保管 TW1 候选 RD 图像。`2425` 和 `2426` 在该跨来源图像索引同用别名 **24222**，并不证明同一种道具、同对象或原渲染在 mixed25 服务器/客户端中出现。`2414` 也在 QUEST11 后期同保存来源的海螺情节出现，仅作**带来源数字交叉引用**，不认定两个事件族同时启用、同一原商业部署、同一事件进度规则。角色 SPR 别名 `100250/100252` 与此前 CHAR05 相关视觉候选可以通过原数值检索，但本轮**没有取到该创建点正在运行的原 NPC 精灵画面**，也未把既有跨载体像素当本地运行。

**地图：** 六份 3×u16 原始源 DAT 都完整、同来源数值表确认；`20401`—`20405` 为 50×50、`20406` 为 50×70，10 个原 CREATE 坐标均位于其实际范围。十处原三值可在派生 JSON 按精确 floor/CREATE 序号直接查出；本轮没有将三张原数据平面冒充已证明的景物绘制顺序、碰撞或道路邻接图。所有标记 JPG 属私人观察，不公开原商业底图。

## 4. 交付、测试与证据上限

本包新增：[复用式原文件提取器](../../tools/stoneage_quest13_goa_uli_letter_source.py)、[公开纯数值来源 JSON](../../research/recovered/STONEAGE-QUEST13-GOA-ULI-LETTERS-ORIGINAL-SOURCE-R1.json)、[9 条来源约束与负证测试](../../tests/test_stoneage_quest13_goa_uli_letter_source.py)。私有观察器含 **11 原配置、10 原物品行、6 原 DAT、6 既有缩图加坐标标记、4 不同既有原 RD 候选 PNG、静态全文 HTML 及源收据**。原游戏商业图、脚本全文、地图格数据和私人 HTML **不进公开 Git**。

**私人保管后验（实际完成）：** `StoneAge-QUEST13-Goa-Uli-letters-original-private.zip`：**219,161 字节，SHA256 `c6f86d050b22ab6fe3f6e56b8062fc21cbb576ace521a1d7752a12d0845773cd`，40 成员**。上传到个人「石器时代」Library 后又独立重新取得完整文件，长度、整 SHA、40 成员 CRC 全部一致。原包阶段与压缩包阶段另分别检查 11 全原配置、10 原物品行、6 DAT、10 原格的每个三 u16 值，全部一致。程序是来源有限的现代 **离线资料查阅器**，不是原版游戏执行、任务可操作世界、原始图层、动画、音效、商店、养成或单机新游戏功能。

本地 `python -m unittest tests.test_stoneage_quest13_goa_uli_letter_source tests.test_stoneage_quest12_mining_competition_source` **19/19 通过**（QUEST13 9，回归 QUEST12 10）。CI 只校验公开派生数据；GitHub 候选和 main Actions **必须按实际后验另记**，不得因为本地通过提前宣称远端成功。以前失败／纠正／不同载体证据均不删除。

**止点：** 本族的来源就绪静态叙事、原创建/道具/六图索引已恢复，原客户端实际人物与地图互动、脚本选择、道具变化、原版身份、活动属性、官方同部署仍 **OPEN**。Stage A **7 PARTIAL + 2 OPEN**，Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，整体复原百分比 **`null`**。不为这份任务补原网游账号、服务器兼容或未来新游戏玩法。

**最高 NEXT：QUEST14-DRAGON-NEST-SOURCE-FAMILY。** 已以真正已保管 CHAR01 ZIP 初步核 `jaruga/event/event17.create` + `event17_1..4` 五原文件、4 条 CREATE、10 个 QUEST01 已有原事件段及 `2457/2458/2459/2460/2461/2462/2505` 七道具源索引；所需 `20801/20807` 两份原 DAT 和已有 MAP09 缩图均存在。下一轮重新从**新远端**核状况与查重，再恢复守护者／三龙奖励的完整原控制、位置与道具，绝不把 3 个可交换奖励推成已经能实战遇龙。若出现新组合 portfolio 更高优先级，以后验为准。


## 5. 正式合并与远端独立验收后验

- 候选内容提交 **`e8e6ad4f5392b88fa52b5322471b184206327536`**、候选 tree **`3d399d315a016c5e181e0066635a5bb15e4b04f5`**，六路径公开变动与本地已验来源 Git blob 完全一致；基线 parent **`955a633ea7b036d627ecc8d81b288a9251730deb`**。原 `CURRENT-STATE.md` 的完整 blob **`c89e0e33537990aa2132b47c40fef49a985a935c`** 保持未变。
- [PR #253](https://github.com/chinaneedM/stoneage-rebuild/pull/253) 已实际合并，主线内容合并 **`619e4a6fd44dbbdb44956d49bc3f322f87187d06`**；其远端 Git tree 与候选**完全相同**，保留旧主线为第一 parent、候选为第二 parent，不改写历史。
- 候选 **14/14 项 Actions completed/success**：专用 [QUEST05—QUEST13 同步来源核验运行 42441996027](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42441996027) / job **128612986005** 的新步骤 **“Validate QUEST13 original Goa mountain Uli letter and flower source guards”** 已实证 success；其旧 QUEST05/06/06-R2/08–12 等复用任务同为 success。其余候选检查也已实证完成并成功，不把本地 19 项测试冒充 GitHub 原文件执行。
- 主线 **11/11 项 Actions completed/success**：`42442054026`、`42442053965`、`42442053963`、`42442053914`、`42442053997`、`42442054006`、`42442054025`、`42442054008`、`42442053915`、`42442053934`、`42442054185`。专项 [42442053934](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42442053934) completed/success。以上均为实际查询的后验；**本验收文字追加提交自身的 Actions 尚未在本段预告成功**。
- 私人存档个人 Library 上传后另独立再次读取同 **219,161B/SHA256 `c6f86d050b22ab6fe3f6e56b8062fc21cbb576ace521a1d7752a12d0845773cd`**，全部 **40** ZIP 成员 CRC 正常。11 原配置、10 原道具物理行、6 DAT 全 SHA 与 10 个三平面原值已另用保存后的数据包独立核同。公开 Git 原商业素材 **0**；所有历史版本与原生运行负证继续保持。
- **QUEST13 静态资料的来源限定验收为 `ACCEPTED_SOURCE_BOUNDED`，不是原版可玩任务或官方初版复原完成**。下一次从 fresh remote 延续 **QUEST14—龙之巢穴三龙奖励原任务族**，先真实查重与源身份核验；Stage A 7 PARTIAL+2 OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING、overall_percent=null 不变。
