# INTEGRATION37｜原加奥利／乌力书信任务：十名创建配置、六图、动作0、脚本和物品联合目录

本工作从 2026-11-10 GitHub 远端 main `454a02a0d0c986ec480760589cf353b7a7920a4b` 开始；`docs/CURRENT-STATE.md` 历史 **2,709,173 字节**，原 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 未改写。本文件是持续性的加法覆层，仍属于 **Stage A 历史复原**，不进入新单机游戏开发。

## 来源及真正的整合价值

这次**没有重新取得原始文件、重新解码图像或重新执行原游戏**。以先前已经经过私人原源验收的 [QUEST13](../../research/recovered/STONEAGE-QUEST13-GOA-ULI-LETTERS-ORIGINAL-SOURCE-R1.json)（Git blob `660a9fb36e0ee5bb83d57e191c797c689b77314b`）和 [CHAR05](../../research/recovered/STONEAGE-CHARACTER-NPC-MODULE-05-30-ORIGINAL-MOTION-SOURCE-BRIDGE-R1.json)（Git blob `9afacb49d11dd7cc546fabe594170053d49b1f9b`）为固定上游，进行同一保存 RAR / NPC ZIP 来源资格下的精确主键连接，产出每个 NPC 一行可检索的“源 CREATE 位置→原三平面 DAT 值→同保存源 SPR 动作材料→精确任务脚本和段数→原物品”目录。这是**新的跨模块查询视图**，不是新的原源身份、10名历史人物或16个新脚本段的发现。

原 CREATE `jaruga/event/event07n.create` 恰有 **10 个独立配置**：20401 两条、20402 一条、20403 一条、20404 两条、20405 一条、20406 三条；原坐标/文件块SHA在报告中逐行固定。六张原 DAT 的来源 SHA 与 50×50（五张）/50×70（一张）原几何已在 QUEST13 验证，本轮仅将每个源创建点此前记录的实际三平面 u16 值精准接到同一行，不扩张成原生碰撞、入口或完整世界地图。

同保留混合2.5父 RAR 中，10条 CREATE 图号分别只有 **100250（5条）与100252（5条）**。CHAR05 前序真实来源已验这两组完整 SPR 段以及动作码 0 的各八方向原图；本轮根据 CREATE 路径与原块 ordinal 唯一关联，同父来源的原 SPR 图号和段 SHA 逐条精确对应。**并未本轮实际重绘、重播或运行原客户端**；完整 SPR 段/实像素不能替代原运行时选帧、调色板和人物身份。

10条 CREATE 对应10份同 RAR 原脚本，先前 QUEST13 已编目的 **16个 TYPE 段**：保留原 event number、TYPE、块 SHA、命令名和所在脚本，不修正原条件写法、不推断标志结算次序。5个相关原 item ID：1206、2414、2424、2425、2426；两份同保存物品表的各行 SHA 一致，跨载体台湾1.0原图像编号只作为**不同来源候选**。数值关系不证明交易、送达、获取奖励或完整任务曾实际完成。

## 验证与未闭合事项

公开的 [10条来源组合目录](../../research/recovered/STONEAGE-INTEGRATION37-GOA-ULI-LETTERS-MAP-SPR-SCRIPT-SOURCE-R1.json)、专门回归测试与 GitHub Actions 仅覆盖 SHA 固定的衍生源索引，完整原商业脚本、原图、DAT 和私人 ZIP 仍不公开。测试逐条比较 QUEST13 的 CREATE/地图格/脚本/物品以及 CHAR05 的同一原块/SPR段 SHA，固定10/6/10/16/2/5的守恒和单条反例；不声称等同于本轮私人原字节重新取证。

历史起源、官方同部署、原动画选帧、分支运作、原生 NPC 对话与任务奖励都仍 **OPEN**；同源保存档案不等于同次历史上线。**Stage A 仍7 PARTIAL＋2 OPEN；Stage B/wiki GATED；R79 PAUSED_NON_BLOCKING；总体完成率未知。** 本组以现有材料止步，NEXT转有新的原游戏内容可整合的模块；只在出现真正同版原运行、完整原输入或新关联时重开。
