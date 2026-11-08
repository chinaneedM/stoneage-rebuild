# INTEGRATION08｜完整原DAT地图1000的19份原NPC/任务创建配置与来源作用域（2026-11-08）

在源限定 Stage A，承接 INTEGRATION07 的14层/88源CREATE真实资格。基准main `c7a8fd9fc1406b0e4d3cc80ff7b2c485e2d3841f`／tree `c2751a7b55bafd26a5a0efb2373290ca93408cc4`；旧CURRENT `c89e0e33537990aa2132b47c40fef49a985a935c` 全文不改。原材料没有重新解包、原图没有重新绘制、没有原程序世界入口执行。

实际复用同保存档的QUEST05 598 CREATE源索引与CHAR01 4985原CREATE块/源文件SHA，连接此前MAP02独立认证的 **1000.DAT（153608字节，SHA256 94b19cb59d72b7b48da70d2741ba68516caad970297fd48ed11ef720fa3ea97e，160×160/25600格）**。旧MAP01读取1000.DAT错误仍保留，不能抹掉。**19/19条**源 floor1000 创建配置可用 `原CREATE路径+序号` 找到CHAR01的对应块，且按QUEST05的SHA作用域（全文或原块）逐项成功一致。各自源参数路径、原参数整SHA、图别名也逐项对应。来源是后期社区混合2.5保存资料，不认证台湾1.0/JSS1999/大陆1.82官方同服。

### 来源功能/原位置覆盖

- **7条 changeevent/ExChangeMan** 源配置：资料可连到任务与兑换条件，但不是7个实际已生成NPC。
- **2条 npcgen_warp** 静态传送功能配置，原目标文件与参数SHA留存；未执行过原碰撞/传送。
- **10条 npcgen_timeman** 静态控制配置；不能因同类型推成NPC人口或原世界时钟事件。
- **17条**原 `borncorner` 四整数，均为 `x,y,x,y`，其前两整数落在源160×160边界内且17个坐标不重叠；还有 **1条**只有 `borncenter=[72,48,1,1]` 而无 `borncorner`，**1条**两字段均无原值。不能把`borncenter`的后两个1擅写成普通`borncorner`，或猜测无坐标时的原实际生成位置。
- 共 **18个不同原图别名**；不是18个已见的人物或认证可选角色。原 `direction`、`createnum` 和原姓名散列原值也保留，不推真实朝向/动作/可见外观。

### 已有玩家内容来源连接，不宣称可走路线

- QUEST25原两岛四路线的三处创建配置引用该floor1000，且三原块SHA、脚本路径和坐标同原CREATE：`sainasu/event/oev_0cd`、`oev_1c`、`oev_edc`。只可说配置原文及布局存在，不说路线实际通关。
- QUEST26贝壳与花互送的 `sainasu/event/event02_2` 在 **1000(57,124)**有同块SHA关联。原脚本的CLEAN、旗标2含义和交付真实效果继续OPEN。
- INTEGRATION05此前已有 `sainasu/event/oev_edc` 一条同源原 `GetPet` 配置，原字面数字 `48,94,350,482`；本轮只是将它严格定位到原地图1000的源创建，不是奖得四只宠物或原程序领取成功。
- INTEGRATION02先前已核该原DAT第一、二平面**26324次非零图号引用**，其中26310次可按数字对应TW1原RD候选、14次没有合格TW1候选；“跨客户端数字图号候选”不是原服同版纹理身份、官方调色板或完整原生屏幕复原。

公开[19行逐SHA/位置/功能/原参数源目录](../../research/recovered/STONEAGE-INTEGRATION08-FLOOR1000-19-CREATE-ORIGINAL-SOURCE-R1.json)与[9项反向检验](../../tests/test_stoneage_integration_module_08.py)，源字节完整出自已发布的七份固定Git Blob，不发布商业原脚本正文、真实原图或商业程序。没有新原DAT、NPC、掉落等原生发现；新结果是已恢复源地图的**整楼层19配置内容索引**，每个原节点与地图和已审剧情可追踪。

**止点：** 原可操作世界、走路/遮挡、NPC真正选图/对话、领宠交易、原版同服身份均未验证。后续只有取得真实运行交互、合格同构建对应资料才能晋级。Stage A仍7PARTIAL+2OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING，完成率未知。NEXT `STAGE-A-REPRESENTATIVE-PLAYER-PATH-GAP-REVIEW`，谨慎从已核游戏内容节点梳理可证/缺件，不假画可玩路线。

> 合并与Actions后验必须另外取得再写，不预支成功。


## 正式GitHub合并与主线后验

[PR #275](https://github.com/chinaneedM/stoneage-rebuild/pull/275) 已squash合并main `445ca5d6710cc620b04866b2617320eddef5abfd`／tree `b822c5a73ff92b1eaa0ba97a80f8638edfcabdb1`，候选最终提交`2298a60cc93f8e183c2c45bdd77cec49268ee926`；同候选 **14/14** Actions实际completed/success（本包push专项run42494918960，PR专项run42494937138）。内容主线合并后 **11/11** completed/success，含[INTEGRATION08专项run42495166316](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42495166316)/job128775844992，9项派生公开来源测试通过。所有运行ID、源证与5个公开Git blob摘要见[正式验收收据](../../research/recovered/STONEAGE-INTEGRATION08-PUBLICATION-ACCEPTANCE-R1.json)。原巨型 `CURRENT-STATE.md`完整Git blob`c89e0e33537990aa2132b47c40fef49a985a935c`不改，历史测试错误和来源边界未抹；本收据自身提交CI不预支。NEXT Stage A代表性有据玩家路径/缺口审查，不将19份CREATE配置等同原生可用NPC。
