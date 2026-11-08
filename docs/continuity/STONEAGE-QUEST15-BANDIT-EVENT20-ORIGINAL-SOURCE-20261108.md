# QUEST15｜吉德／强恩／沙拉山贼事件族的原脚本、两物品表与跨源图形资格（2026-11-08）

## 1. 从远端重启、查重与历史版本边界

本工作单元按 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` 从 GitHub 远端 `main` 读取分支、HEAD `012419bf9b6d1c6da48664f46415e0263f411441`、tree `90a257f4229436be6031bcbe63bfb5af53365b62`、最新提交、Actions，以及协议、README、路线、组合模块队列和完整历史 `docs/CURRENT-STATE.md` 的 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`。历史 CURRENT 全 2,709,173B 未覆盖、未截断；其普通 Contents 读取空正文时改用原始 Git blob 读回全历史。最新 QUEST14 的后验明确将 **QUEST15 查重与确有原件的下一任务族**设为最高未完成事项。

查重对象是后期社区混合 2.5 保管源 `jaruga/event/event20.create` 及其六个事件脚本。其 **6 个 CREATE 和 28 个 EventNo/TYPE 原段**早在 QUEST01 全量目录中有索引。本轮没有把这些老计数说成新增历史发现；新增的是从原字节逐项复核的**条件、取物／删物／随机奖励、源位置与两物品表/跨源图像联接**。本保管样本不属于经认证的台湾 1.0、最初大陆 1.82、1999 JSS 原始发行或任何已运行服务器；版本来源 `ORIGIN_UNRESOLVED`。

## 2. 真正重读的原件、静态事件结构

私人 Library 中 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip`：995,176B，SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`，2205 个原 NPC 文件全部 ZIP CRC 有效。`event20.create` 原 1041B/SHA256 `cc907c781896f92e584661623566bdacad8dba8ec4eabd841cbd05b0c72efab9`，配同目录六份脚本和共享 `event.template` 共八份真正原文件，原 SHA/CRC 已逐项固定。28 段原 EVENT 的 EventNo、TYPE、条件 SHA 和源段 UTF-8 正规化 SHA，全部逐段与仓库中独立先前 QUEST01 索引一致；分布为 `ACCEPT=13`、`MESSAGE=13`、`REQUEST=2`。源 CP950 原字节与私人对白未上传 GitHub。

原 CREATE 的精确位置与其 `changeevent|file:` 外键：

| 原源角色检索称谓 | floor/(x,y) | 源图形别名 | 实际指向脚本 |
|---|---|---:|---|
| 吉德的朋友 | 3400/(59,66) | 16030 | `event20_1` |
| 吉德 | 3406/(27,14) | 16017 | `event20_2` |
| 吉德的儿子 | 3406/(28,17) | 16046 | `event20_3` |
| 强恩 | 20607/(68,5) | 100431 | `event20_4` |
| 强恩的妻子 | 20607/(71,7) | 16032 | `event20_5` |
| 沙拉 | 20608/(9,3) | 16029 | `event20_6` |

上述原图号仅是源创建字段，**没有**据其数字恢复这六个人物的原帧或证明原生站位、动作、表情。楼层原文本中的村庄、地下城称谓也不能当成早期官方世界地理鉴定。

## 3. 已恢复的原条件及物品有向关系（仅原脚本字面）

- **红花／发饰的来源条件**：`event20_1` 有 `ITEM!=2486`→`GetItem:2486`、`ITEM=2486`→`DelItem:2486`；`event20_3` 有 `NOWEV=20&ITEM!=2487`→`GetItem:2487`；这些是分别存在的源段，不能由事件号自动拼成可运行时序。
- **沙拉的信／吉德交换**：`event20_6 #0` 为 `NOWEV=21&ENDEV=22&ITEM!=2488`→`GetItem:2488`；`event20_2 #0` 为 `ENDEV=20&NOWEV=21&ITEM=2488`→`DelItem:2488`、`GetItem:2489`、`EndSetFlg:21`。这是严格原字段的跨人物有向候选，不证明实际背包容量、对话条件选择、物品扣除成功或同服执行顺序。
- **强恩奖励分支**：`event20_4 #0` 有 `NOWEV=20&ITEM=2487`→`EndSetFlg:20`；其 `#1` 有 `ENDEV=20&NOWEV=21`→**一条** `GetRandItem:2490,2491,2492,2493,2494` 和 `EndSetFlg:22`。这是五 ID 的原随机池字面，**不是五次 GetItem、五件必发、等概率或运行奖励认证**。在本批 2205 原 NPC 文件中，五 ID 均无 `GetItem:` 字面命中，不能据此排除这条 `GetRandItem` 命令或其它来源。
- **单独高等级条件**：`event20_2 #4` 原条件明确含 `LV>79&ENDEV=20&ENDEV=21&NOWEV=161&ITEM=2744`，动作 `GetItem:2745*1`、裸 `DelItem:2744`；下一段校验 `ITEM=2745`。此分支须**独立于 20/21/22 主任务**保存，不能偷换为所有玩家必经，也不能把裸 `DelItem` 自动改为数量一。当前保留的 ITEM01 两表合并 13,915 ID 目录未包含 `2744/2745`，只记此已验目录的缺位，绝不扩大为所有版本中物品不存在。

## 4. 9件原道具、实际图像与地图资格的精确止点

独立重取私人 `StoneAge-ITEM01-private-two-itemsets-832-original-RD-icon-observer.zip`：5,868,386B，SHA256 `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa`，838 ZIP 成员全部 CRC 有效。由实际 `private-full-catalog.json` 逐 94 原字段 CP950 重组，`2486–2494` 共**九个不同道具、18 份两表物理行**；两来源同 ID 的原行逐完整 SHA 相同且独立与公开 ITEM01-02 索引一致。九个来源图形别名分别为 `24175/21522/24222/24200/22013/22060/20033/20230/20111`，本库九幅台湾 1.0 真实原 RD 已解码 **候选 PNG** 原字节逐图 SHA 再验。图像和 mixed25 脚本**跨载体**，无法据静态 ID 联接声称正式同部署身份或真正原游戏画面。

据既存 MAP09 公开验收索引（**本轮不是重解原 DAT**），四个 CREATE floor 中 `3406`、`20607`、`20608` 三张已有源合格 DAT SHA 与完整候选画布哈希记录：分别 `8e643f9c...`（40×30）、`61030ae7...`（80×60）、`c557d486...`（15×15）。`3400` 在 MAP09 691 资格集合与 MAP10 60 新增集合中均未见，但不代表所有原客户端缺少该地图。本次没有重新获取这四张原 DAT 的完整字节、没有逐目标格独立核三平面、没有新渲染场景／人物原像素；真实源地图／画面验收的本批增量 **0**。应等待已有 MAP09 私人实物或其它精确源 DAT 回读后再提升级别。

## 5. 交付、复核、风险与后续

公开产物为[派生数字与逐源散列 JSON](../../research/recovered/STONEAGE-QUEST15-BANDIT-EVENT20-ORIGINAL-SOURCE-R1.json)、[原源提取器](../../tools/stoneage_quest15_bandit_source.py)、[公开来源／负证回归](../../tests/test_stoneage_quest15_bandit_source.py)和本连续性文档；不含原商业脚本对白全文、原物品原文、原 RD 图或历史 DAT。项目公开 CI 只验证来源派生与跨旧索引一致，**不能冒充 GitHub CI 已读取私人商业源**。

私人证据包 `StoneAge-QUEST15-bandit-event20-original-private.zip` 经本地完整 CRC/SHA 检验：**33,087B、SHA256 `ac9168e1bc6d293c9c41b741ac6ebb5d200da9a6ef862f1a77b31b5483caedcd`、36 成员**（8 原 NPC 文件、18 份原物品表行、9 幅真实原 RD 候选 PNG、1 份纯数值收据）。云端 Library 保存及保存后的独立回读仅以实际操作结果为准，不预先宣称完成。正式 PR 合并和远端 Actions 也仅以真实后验记录为准。

**结论：`QUEST15=ACCEPTED_SOURCE_BOUNDED`（资料静态层）**，不是官方早期版本、原人物动画、原脚本运行、可领取奖励或单机游戏已实现；原战斗／事件触发、道具 `2744/2745` 的同源表／奖励概率、地图 `3400` 真实源画面仍 **OPEN**。Stage A **7 PARTIAL + 2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、总体 `overall_percent=null`。不进入账号／联网、服务器、引擎或体验优化。本任务族有界止点后，下一项 **QUEST16-DEDUP-AND-SOURCE-READY-NEXT-FAMILY**：先重读最新远端及旧 QUEST01/04/05–15，不重复本次 28 原段；择另一组确有源原件且尚未专门复原的任务族，或当同源 `3400` DAT/特殊道具表新字节到位时增量重开该缺口。

## 6. 云端私人保管与合并验收后验（2026-11-08）

- 私人真实原文/原物品行/跨源 PNG **36成员、33,087B、SHA256 `ac9168e1bc6d293c9c41b741ac6ebb5d200da9a6ef862f1a77b31b5483caedcd`** 已实际上传个人 Library 为 `StoneAge-QUEST15-bandit-event20-original-private.zip`；从 Library 的**新后验文件 ID**再独立取回 ZIP，核验每一字节与本地最终档完全相同、全36成员 ZIP CRC 通过、成员尺寸全部一致。这里只是受限私人来源保管验收，不是原游戏运行或同一官方版认证。
- [PR #255](https://github.com/chinaneedM/stoneage-rebuild/pull/255) 已实际合并，候选 SHA `fa96ab9d2f21eb2f7d8a138aaebdd8bb3bd325f1`，候选 tree `716545d1c78556eb827101bd8f05e8e25a068db5`；合并 main SHA `56bfaf41b182359966cbabe0279656bd36021cfb`，合并 tree **完全同候选 tree**，不是待合并状态。
- 候选 SHA 的**14/14 GitHub Actions 全部 completed/success**，含专用 [QUEST05—QUEST15 原来源验证 #42454409474](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42454409474)（job `128650256714`）成功；新增步骤 **“Validate QUEST15 original bandit event20 source and map/item limits”** 成功，既有 QUEST13/14 回归均成功。PR 专用 [#42454424143](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42454424143) 同样 success。**公开 CI 不下载、不读取私人商业 ZIP**，仅交叉核公共索引/散列/有界解释。
- 合并后的主线 HEAD 上 **11/11 Actions 全部 completed/success**（其中 QUEST05—15 验证 [#42454496812](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42454496812)）。远端 PR diff 逐项审查确认为 **6处公开文件变更**：4新文件（工具、测试、JSON、连续性档）加 README 和旧来源 workflow；未加入原脚本文本、原道具描述全文、PNG、DAT 或 ZIP。旧 `docs/CURRENT-STATE.md` blob **`c89e0e33537990aa2132b47c40fef49a985a935c`**，**2,709,173B**，没有重写或缩短。
- QUEST15 的最终验收仍然严格为 **`ACCEPTED_SOURCE_BOUNDED`**；没有把原缺失 DAT `3400`、2744/2745 同源物品表、条件脚本真实执行概率或早期官方出处补成事实。Stage A **7 PARTIAL+2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、总体百分比 `null` 不变。**NEXT `QUEST16-DEDUP-AND-SOURCE-READY-NEXT-FAMILY`**，下次必须先按协议重新读取最新远端 main/Actions/协议/CURRENT，再查重、选择原源真正就绪族；不能据本段旧 SHA 直接假定当前 HEAD。后续本接受注释提交的新 CI 需独立核验，不预先归入上述 11 项。
