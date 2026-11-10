# INTEGRATION51｜1021与3021两份原百人道场来源联接的正式主线验收（2026-11-10）

[原源核查、地图旧负证及止点](STONEAGE-INTEGRATION51-TWO-DOJOS-ORIGINAL-SOURCE-20261110.md)；[公开的100条samdou原文件来源SHA、创建块及数值关系](../../research/recovered/STONEAGE-INTEGRATION51-TWO-ORIGINAL-100-DOJOS-SOURCE-BRIDGE-R1.json)；[PR #319](https://github.com/chinaneedM/stoneage-rebuild/pull/319)。

## 启动远端与原历史保管

本工作单元依据GitHub远端最新 main 起点 `96bcb2166f4594dd0ddc4a678401a3af98e8ca78` / tree `bb214f50e9c9b56a695c88d1cdef1c25b6378ea4`，重新读取分支、提交、Actions、连续性协议、README、设计/历史/来源、roadmap/module-first/offline-priority和INTEGRATION50正式验收。起点零开放PR；上轮内容主线27/27完成成功。

本轮 `docs/CURRENT-STATE.md` GitHub contents接口对大型文件返回空内容，但**原生Git blob接口实际成功读出原全文**：完整原blob `c89e0e33537990aa2132b47c40fef49a985a935c`，Git树记载2,709,173字节。严格不覆盖，不复写、不将空接口结果当空文件；合并后再次核验树中的原blob及字节大小**完全相同**。公开只有小型加法文件、README末尾指针，不改变历史主状态记录。

## 独立原始文件实证与真正增量

私人原 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip` **995,176B** / SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f` 整ZIP重新验证，2,205成员CRC全部通过。

- 原 `doujyou/samdou.create` **43,834B** / SHA256 `74124b6865ed1a03b6842bba1a0be21eab03e921e67b50307257226cf921fac9`，在本轮真正从私人归档取出；100条道场对战者CREATE、200条独立Warp CREATE、100份 `samdou001.arg`—`samdou100.arg`逐完整原文件SHA/CRC和源参数字面核验，总原参数30,872B。这100份不是初次获得新原文件，而是已保存来源中**新的专题逐关交叉核查**。
- 对原 `doujyou/jyajyadou.create` **44,134B** / SHA256 `ac3e46dc64d2e478cba4a115e15c2d32d3193c38e9de85f53ce8b06f3d99d925` 及100份 `jyajyadou`参数重新核对（30,072B）。其3021道场已在旧 `STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-01-DOJO-SOURCE-ATLAS-R1.json` Git blob `2bc01824650696131dcdd8b7e2f3b763d19e400f` 详录；本轮逐关100/100与该来源一致，不冒称再次发现3021。
- 两组原NPC创建各300条：每组100个静态对战者与200个独立Warp。两组NPC/门点的源坐标逐关一致，`gym=1..100`、`enemyno=564..580`的字面列表一致，但`enemypetno`两组分别为655..690与687..720（仅687..690重合）。原参数整SHA100/100不相同。每组1—99的参数目标楼层分别1021、3021，第100组参数目标为**1008(20,20)**、**3008(20,20)**。独立入口Warp均字面指向1022／3022(1,7)。原消息内容以源SHA在私人归档校验，不公开商业文本。
- 旧 `STONEAGE-MAP-SCENE-MODULE-01-ORIGINAL-SOURCE-MANIFEST-R1.json` Git blob `03675ee98d391f9ef0246315b2426f2a8b721fd3` 已验1021 DAT 407×144/351656B 与对应MAP/1022 DAT/1008 DAT来源。3021 MAP和3022 DAT也已有不同SHA的来源；旧3021 DAT **读取错误**原记录保留（预期351656B、实际327680B、CRC failure），不能声称旧失败证明历史游戏缺地图，也不能称本轮已恢复该DAT。**本轮没有重新读取原DAT正文、没有解原RD/绘新图、没有运行原客户端或服务器。**

新增的是从已保存同RAR物证中提取的另一套100关的**版本限定、可逐原文件追索**的NPC/门点/敌人数字来源关系。道场名称、敌人编号、传送参数不能转述为已实见的游戏战斗、宠物身份或真实通关。保存社区mixed25载体不是已证台湾1.0/JSS1999官方同服。

## GitHub发表/验收链真实后验

- 候选分支 `agent/integration51-parallel-original-dojos-20261110`，HEAD `70f60833a5160119f85f87ffd861fd5209be9459`，tree `4e4aecafba0e14aac7e908fd5f4ba609a0a83381`。相对当时main **ahead=5/behind=0**，仅五路径：公开派生JSON、12项来源正反回归、专项Actions、来源说明、README加法指针。新增JSON Git blob `53d25478dd4c2f38accea1ed6ad6603f1cdb845b`；原版权NPC创建文本/脚本/RAR、地图DAT/SPR/RD/PNG不在公共Git。
- 候选push **27/27 completed/success**，本包专项 [run 42842049473](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42842049473) 成功。PR [#319](https://github.com/chinaneedM/stoneage-rebuild/pull/319) **19/19 completed/success**，本包专项 [run 42842781837](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42842781837) 成功。所有PR检查成功后核实mergeable=true/clean、main起点未变、五公开路径无版权原件，才squash合并。
- PR #319合并后main HEAD **`935e8b878e341257bc7cf19389fe0e22509fa0ac`**，tree **`4e4aecafba0e14aac7e908fd5f4ba609a0a83381`**，与候选tree逐对象相同；main push **27/27 completed/success**，本包专项 [run 42843203477](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42843203477) / job **129923615623** 成功，已核实际日志：**Ran 12 tests in 0.006s / OK**，无fail或skip。源CRC/SHA是本轮真实私人原件复核，公开CI则仅重放公开数值/哈希，二者不能互相假冒。
- 本**后验收据**在主线所有27项真正完成后单独加法提交；不将收据提交自身无对应Action的情况冒称通过，最终收据HEAD须另外再核查。

## 模块级止点与下一工作包

1021／3021此批100关的**静态关系 SOURCE_BOUNDED_PARTIAL**已完整保存；本工作单元不再展开相同两馆的NPC、指令模拟、引擎、假玩家移动或通关奖励。下一个优先工作包回到未专题覆盖且可实际拿到新原始DAT／SPR／NPC／任务／物品的**另一类可见游戏内容**；如果只剩同一百关的已知编号和图形同号猜测，不重做。重新开启1021真实画面需完整原DAT与每原像素来源资格；3021旧读取失败需新的可核原字节才关闭。

Stage A仍 **7 PARTIAL + 2 OPEN**，Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，overall_percent=null；未进入未来新单机开发阶段。
