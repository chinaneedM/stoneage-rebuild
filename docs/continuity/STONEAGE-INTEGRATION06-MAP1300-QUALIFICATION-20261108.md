# INTEGRATION06｜原1300.MAP实物、DAT读取失败与六个任务/NPC创建点的来源关联（2026-11-08）

## 启动与目标

最新远端 main `fbb4b2e4a1a50769ee6020c757d43c59e798076c`／tree `3673a41780a2809f4efa1d5f1cf3018552ddf82f`，原多兆字节 `CURRENT-STATE.md` 保持 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`。遵循 Stage A 的同源先行、跨版本隔离、保留负证与单机离线研究边界。QUEST32 完成24份专项任务源去重并 SOURCE_BOUNDED_PARTIAL 收口之后，不继续产出重复任务编号。

本包选玩家内容影响明确的一处缺口：源静态地板编号 **1300** 同时出现于QUEST19寄信、QUEST25四路线、QUEST27斧头/感谢函、QUEST31四配置人物以及QUEST03已有特殊服务创建目录。旧 QUEST05 的955已验DAT集中给出 `NO_MATCHING_DAT_IN_955`，不能将“没有此批已认证DAT”写成“原游戏没有该地图”。

## 原来源实物与明确未验

从已发表于 Git 的 **MAP01 真实原字节目录**重新核算：原社区保存 mixed25 RAR SHA256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`，**两份 `1300.MAP`** 分属 group 0/1、各**20,008B**、整文件SHA256同为 `a3b25cf753056886f7cd0b8293bade2db0ab917ac4474df9278333e11a882235`、源CRC `fc9288d2`、头信息候选 **100×100**。它是已验两个同字节MAP源成员位置，不是两张不同游戏地图。

同 MAP01 的原始错误清单确有 `group=0, 1300.DAT, expected=60008B, emitted=0B, error="File CRC error"`。这证明此RAR的该路径及预期成员尺寸**在保存索引中存在**，但历史解包器没有取得可信完整DAT字节；**未证明原RAR本身损坏、DAT内容是什么，也未证明另一发行版有相同DAT**。不能拿 MAP 的2字节格大小或候选100×100直接补出 DAT 的6字节格三平面，不能绘制或断言人物路径/碰撞。

## 跨模块六个创建引用

QUEST05来源限定原598 CREATE 索引在floor1300有**6条**：QUEST01源 `npcgen_changeevent` 四条，QUEST03源 `npcgen_timeman` 两条。逐条原CREATE路径+block ordinal+SHA作用域与原参数路径+整SHA全部固化到[派生JSON](../../research/recovered/STONEAGE-INTEGRATION06-MAP1300-MAP-DAT-SIX-CREATE-SOURCE-R1.json)，保持 WHOLE_CREATE_FILE 与 ORIGINAL_CREATE_BLOCK 不同哈希作用域。

四条ExChangeMan有对应既有来源专项：QUEST19 `extra/event/marju` 位于1300(70,51)、图别名16046；QUEST27 `sainasu/event/event03_1` 1300(18,42)、16048；QUEST31 `sainasu/event/event10` 1300(65,65)、16206；QUEST25 `sainasu/event/oev_9c` 1300(65,26)、16068。两个 Timeman CREATE位于 `genout/1300npc_m.create` 不同块，共同引用 `genout/tman_1300_37_26` 同SHA，原图号16033。本轮没从QUEST03的原字节核空间坐标，故不虚构两条时钟NPC的实际位置。**6是创建配置行，不是历史原地图人口或可用任务数**。

## 可重复验收与阶段性止点

将原6份已发表 Git Blob SHA、两份MAP整SHA、原DAT错误、六CREATE引用、四专项中有据的坐标/图别名合并为一个少量[公开数值索引](../../research/recovered/STONEAGE-INTEGRATION06-MAP1300-MAP-DAT-SIX-CREATE-SOURCE-R1.json)。[五项专项测试](../../tests/test_stoneage_integration_module_06.py)从已发表的六份原派生JSON逐个独立反推，验证原地图身份、错误保留、跨文件JOIN、四任务关系与负证，未读取或发布商业图像、脚本正文、DAT二进制。

**交付：** 把“地图1300在已存RAR内存在原MAP，DAT成员读失败，因此六个原创建引用当前无法得到可信DAT场景”的知识变成跨模块可回溯结论。地图不是已加载的原商业世界；六NPC未在原程序运行，不能认定早期JSS1999、台湾1.0或大陆1.82官方同部署，也不能用社区版本地板编号强制分成村庄/岛屿类别。

只在重新取得该源版本或明确来源合格的完整 `1300.DAT`，并实际逐完整CRC/SHA核验后再打开场景/原图链接；不为此重新开发RAR驱动或用纯MAP猜DAT。保持 Stage A 7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，整体percent=null。**NEXT：** 综合审查其他有明确玩家内容影响且真实原件就绪的跨模块缺口；无新材料时转 Stage A 联合审阅，不继续任务编号或低层helper。

> PR、Actions、合并和正式接收只有 GitHub 确认后才能补录，不能预写成功。


## 合并后验与正式出版回执（实际GitHub状态）

[PR #273](https://github.com/chinaneedM/stoneage-rebuild/pull/273) 已以 squash 合并到 main `24dfa1d0aa5af2ad1c36c0c25f385609a1435e04`／tree `2a1b5638e84da82d1126f9314aafa2485f6c67f8`；候选提交 `5158a48891a50efc6e09f7ca7eb9ca9279957a24` 的 **14/14** Actions 均实际 `completed/success`，包括专项 push run 42492009653 与 PR run 42492031783，另两个 O11/O12 PR 检查也成功。合并后 main **11/11** 运行实际 `completed/success`，INTEGRATION06专项 run [42492077895](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42492077895)、job 128766424996 的五项公开派生 unittest 已成功。完整运行ID、五公开文件Git SHA与来源限制见[正式验收收据](../../research/recovered/STONEAGE-INTEGRATION06-PUBLICATION-ACCEPTANCE-R1.json)。

跨模块报告未读取私有 `1300.DAT` 原内容；原失败仍是失败，没有据历史错误记录反推损坏本身或世界内容。原 `CURRENT-STATE.md` Git Blob仍为 `c89e0e33537990aa2132b47c40fef49a985a935c`；全历史完全保留。本收据提交自身的Actions尚无运行结果，不能冒用前一次主线11/11成功。最高NEXT仍为综合Stage A有据材料缺口审查。
