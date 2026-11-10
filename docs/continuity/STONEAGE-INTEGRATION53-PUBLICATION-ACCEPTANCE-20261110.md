# INTEGRATION53｜三龙原NPC→台湾1.0独立SPR原图来源桥接：正式合并与验收（2026-11-10）

## 远端事实和连续性文件保全

- 本轮按 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` 从真正的 GitHub 远端 `main` `8962808b3a62ab89fa631c051a90db1d212f0ccd`、tree `933387fca611d69df8d63d237bb483838744dcae` 续接；当时最近正式验收为 INTEGRATION52。
- 远端 `docs/CURRENT-STATE.md` 由原Git blob API真实回读全部历史正文，而普通文件接口对这个大文件返回空正文。原历史准确 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`，**2,709,173 原字节**。此包未编辑、缩短、重建或覆盖它；合并候选树再次确认完全同一blob。
- 依照上次最高NEXT，停止重做1021/3021百人道场，转龙之巢穴已存原NPC、原DAT场景和另一来源的真实原SPR二维动画材料。当前交付仅补齐未做过的**任务NPC图号→TW1零售原动画索引**，非新原图发掘。

## 提交、PR 和实际CI验收

| 阶段 | 远端实际结果 |
| --- | --- |
| 分支 | `agent/stoneage-integration53-dragon-tw10-20261110` |
| 候选commit | `d295af9a8767b3945754ada4f4771cbdb9e7425a` |
| 候选tree | `38f4097cfd5ccc2c70d249ff7a59015169b05959` |
| PR | [#321](https://github.com/chinaneedM/stoneage-rebuild/pull/321)，真实合并（squash） |
| 合并后主线HEAD | `5caea5f6c0f67d89961f756f627f4ef50254718c` |
| 合并后主线tree | `38f4097cfd5ccc2c70d249ff7a59015169b05959`，与候选tree相等 |
| 候选push+PR Actions | **46/46 completed/success**，分为push 27和PR 19，零失败 |
| 合并后main Actions | **27/27 completed/success**，零失败 |
| main 专项验收 | [run 42852323796](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42852323796)，job `129956045454`，`python -m unittest discover -s tests -p 'test_stoneage_integration_module_53.py' -v` 步骤 completed/success，11项专项来源断言 |

此前候选push专项 [run 42851846917](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42851846917)／job `129954349466` 及 PR 专项run `42852192549` 也已完成成功；这里只将各自HEAD上的运行当作该HEAD真实验证，不把候选CI代替合并后main结果。

PR真实差异为**五处权利安全公开文件变化**：新增来源JSON、连续性说明、11项测试、专用Actions工作流，并仅向README追加章节。无任何原商业DAT、RD、原动画原像素、私人ZIP/HTML/PNG、完整NPC对白或原物品正文进Git。原历史CURRENT保持不变。

## 此轮可证的内容增量与不能升级的结论

- 原mixed25保存任务 `jaruga/event/event17.create` 三名不同NPC，原楼层20807与位置(7,8)/(23,6)/(41,14)、原图号100384/100385/100386以及脚本原SHA和取物候选ID2462/2460/2461来自此前QUEST14实际原文件的完整派生源收据；没有在本轮再次声明“发现3个新NPC”。
- 独立台湾1.0零售原SPR收据PET07/PET15具有这三图号对应组350/351/352；各组此前实证56个原序列／712个原帧位置／232个不同组内原bitmap。此轮首度将这组已验原二维图像**作为三名晚期资料NPC的跨版可视候选**精确交叉；源SPR块SHA、旧样本动作、原帧位置逐条进入[公开来源表](../../research/recovered/STONEAGE-INTEGRATION53-THREE-DRAGONS-QUEST-NPC-TW10-SPR-SOURCE-BRIDGE-R1.json)并经公开CI和原PET07/PET15不可变Git索引核等。
- PET10原社区同保存档中的`enemybase.txt`和`enemybase2.txt`各存在同图号的多条物理宠物模板行，`PETFLG`有0与1；两表模板331/332/333的SHA不相同。这是有界的数字候选关联，既不能等同原NPC真实宠物物种，也不能断言哪份备选服务器表被实际加载。
- **本轮没有重新打开私人原RD/SPR、原动画PNG、MAP09原DAT、NPC原脚本正文或原服务器运行**；新增的原商业字节、真正独立原图解码、可玩场景、原生战斗、原生奖励结果均为0。公开CI仅可复验先前原件的派生数字/来源哈希关系，不等同原商用二进制本轮私人复测。尚不能证早期JSS1999、TW1或大陆1.82中该后期任务与这三组原图**同一部署、同一种宠物、同一地理、实际NPC显示、碰撞和角色动作**。

## 止点和交接

INTEGRATION53 = **ACCEPTED_SOURCE_BOUNDED_CROSSCARRIER_VISUAL_CANDIDATE**。本组来源级关系已验收，无新同部署原件时不重复画三龙、重录PET07原图号或模拟任务奖励。

最高下一项：选择**本三龙与百人道场之外**，确有新可得原始图像／DAT／NPC或更强独立可见来源的区域，优先形成真实场景→原NPC/宠物/物品的可检验关系；若源件缺失，则如实OPEN并转22域中其它有实物模块。始终Stage A **7 PARTIAL + 2 OPEN**，Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，overall_percent=null。维持离线单机历史内容取证优先，不创建登录服务器、MMO功能或新引擎。

**本后验收据本身是后来新提交，以上27/27只属于合并内容HEAD `5caea5f6`；不得自动宣传这份收据自己的新提交也已跑过27项Actions。**
