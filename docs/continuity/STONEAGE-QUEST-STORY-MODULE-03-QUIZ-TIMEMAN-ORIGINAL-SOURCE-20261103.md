# QUEST03｜原答题控制与时间NPC参数：两个来源限定批次（2026-11-03）

**工作范围：** 《石器时代》历史资料恢复，不是新石器任务制作或优化。启动依据 GitHub 远端 `main` `9639e513cc837a2c940819d2c3c65148bdd560a7`，QUEST02 已完成且已合并，原巨大 `docs/CURRENT-STATE.md` blob `c89e0e33537990aa2132b47c40fef49a985a935c` 保持不变。

## 实际原来源

本轮从用户私人 Library 保存的 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip` 独立读取原 NPC 树 **2205 原文件 / 1,930,332 字节**，逐个完整大小、SHA-256、CRC32 与已发布 CHAR01 原始清单再次核对一致。ZIP 本轮完整 SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`；它是先前已校验的社区混合 2.5 RAR 中保存的**私人提取文件**，本轮**没有**重新读取 361 MB 父 RAR，因此不虚称本轮重复核了父 RAR 全 SHA。本轮源索引额外通过 GitHub 原 CHAR01 逐创建配置、路径及原 SHA 验证。

- **`npcgen_quiz`：22 条原创建配置→22 份不同原参数文件（9,975B）**，全部原文件存在、完整源 SHA/CRC 匹配、严格 CP950 可读。原 `Type`、`Answer`、`Level`、`Quiznum`、`Border`、`EntryItem` 均各22行，原 `Warp` 有21行而非22行；原 `GetItem` 只有4行。**`genout/quz_812_28_14` 原实物没有 `Warp` 字段**，不能补造隐藏出口。源 `EntryItem` 字面为21条 `2752*1`、1条 `2753*1`，这不是实际消耗的认证记录；源 `GetItem` 的前一个数字也不能无证当作奖励物品ID。
- **`npcgen_timeman`：34 条原创建配置→33 份不同原参数文件（3,811B）**，有1份源文件被两条创建引用。33份都包含原 `time` 与 `main_msg` 字段；时间字面 `ALLNOON` 17、`ALLNIGHT` 9、`AFTER` 7。仅4份带 `change_msg` / `change_no`。原出现的时间词不证明原服务器时钟阈值，也不能将这些 NPC 直接定为任务NPC。

本轮在公开仓库保存[完整56条创建引用×55份来源文件的路径、CRC/SHA及原数值目录](../../research/recovered/STONEAGE-QUEST-STORY-MODULE-03-QUIZ-TIMEMAN-ORIGINAL-SOURCE-R1.json)，不上传原商业对白、原题目文字或受版权保护的图片。原脚本说明仅供查档；其中 `Warp` 里的原数字是静态**字面数值序列**，尚未认证原原生格式、原地图真正可到达性或任务胜负/过关执行。

所有56条配置来源均 `ORIGIN_UNRESOLVED`；无法凭 `quiz` 目录、源题目、`timeman` 时间词判定官方初版、永久版本任务或节日运营活动。来源不是认证台湾1.0、大陆1.82或日本JSS1999原服资料。原玩具/服务器没有启动。Stage A 7 PARTIAL + 2 OPEN，Stage B/wiki GATED，R79 PAUSED，整体percent=null。

**NEXT `QUEST-STORY-MODULE-04`**：以同批确实保存的原NPC文件为边界，对剩余有任务联系的功能做去重并有界结论；没有可认证新字节时将任务模块保持 SOURCE_BOUNDED_PARTIAL 并按模块顺序转到玩法、音画。不要投入新引擎、游戏优化或假设原任务运行。
