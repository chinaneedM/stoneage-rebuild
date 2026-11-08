# QUEST21：琉璃洞窟原脚本、地图创建与2003攻略的分源对照

2026-11-08（Asia/Shanghai）。从 fresh GitHub main `cdd36eff03dd1131339f9b85b09222b60fc64fa4` / tree `8bbceff7c0263ca72b38e4a6c772a06b667f3fb0` 启动；该 HEAD 的11项Actions均 completed/success、无开放PR。新原生Git检出与远端HEAD/tree一致，协议、README、完整CURRENT、决策、历史、来源、路线、模块顺序、离线优先及QUEST20接力均已核验。完整 `docs/CURRENT-STATE.md` 2,709,173B / Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 原样保留，本文为加法接力。

## 本轮材料与止点

QUEST20要求避免把旧目录的事件段重算为新任务。本轮选择此前已有2003年攻略、但未专项对照真实原脚本的琉璃洞窟：交付日记/项链、大小袋选择和地图原创建的受限规格。**不是发现6个新任务或22个新事件**；6原脚本/22段早已在QUEST01内。本轮增量是原字节复核、实际来源关联、原序奖池、重复坐标及分版本文献比较。

后期社区 mixed25 私人 NPC ZIP 995,176B / SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f` 真实回读；2,205成员全部CRC及完整文件SHA逐项对 CHAR01 原目录一致。选取11原文件共19,084B：6个活动引用脚本、`ruri03a`变体、事件CREATE/模板、`genout/ruri.create`与条件传送参数。六脚本各段TYPE、条件SHA及完整规范化段SHA与QUEST01一致。

ITEM01私人 ZIP 5,868,386B / SHA256 `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa` 全838成员CRC通过。六个核心ID的两份94栏原行从既存私人目录重建，12行SHA逐一与已验ITEM01行目录相同。父361MB RAR、两份完整物品表和新原DAT/RD本轮未重取；六PNG只是复用另一台湾1.0载体的已验RD候选，不认证同版同服。

## 玩家内容的原数字关系

| 保存本来源 | 原静态关系 | 未证明事项 |
|---|---|---|
| ruri02 | `LV>0&ENDEV=4` 请求段给2699；另有遗失补领段 | 原生选择、成人flag跨版本身份 |
| ruri03 | `NOWEV=39&ITEM!=2698` 段给2698，并列NpcWarp原参数 | 实际移动、均匀概率、任务运行 |
| ruri01 | 条件含2698/2699，原DelItem两值、GetItem2701、Charm1、EndSetFlg39 | 实际扣物/奖励/魅力与存档 |
| ruri05 / ruri06 | 都以2700为条件，GetRandItem各85位置，DelItem2700、裸Break行 | 一次给几个、概率、互斥/重复领取 |
| ruri01另一段 | ENDEV39、ENDEV178、19292与缺3900组合，给3900*1 | 是否早期官方内容、实际执行 |

大袋85位置/67不同ID/18重复位置，小袋85位置/57不同ID/28重复位置，原序和参数SHA全保留。重复数字不删除，也不从出现次数推概率。六核心ID为2698/2699/2700/2701/3900/19292；不能因主线相似就把后期3900分支归为2003原版。

全2,205原NPC文件的 `GetItem` 字面扫描未找到2700的发放命令。这是有界NPC文件负证，**不是战斗掉落表、不是证明羽毛从未存在，也不认证攻略提到的怪物身份/掉落**。`ruri03a`保留四段但本批CREATE/备份没有精确文件引用，没有NpcWarp；不能把它与活动引用`ruri03`合并成同一规则，也不能由保存文件路径认定实际加载。

## 地图创建与同坐标候选

`genout/ruri.create`原7,819B / SHA256 `e213f9ea3a1aee2e251e23b15ac8196e14c17bc73a6c9c77f0b07dc66c7e2268`：63个原CREATE配置，其中57个直接`npcgen_warp`字面记录、1个条件WarpMan、1个告示及4个村民信息配置。它们均已属于CHAR01目录，不能当新增63个原NPC。

- 同一个源位置200/(229,988)出现两次，分别指向3413/(10,15)及/(10,16)。
- 同一个源位置21016/(13,21)出现六次，指向21011的六个不同落点。保留六条，不假定first-wins、last-wins或随机。
- 21003/(34,6)去21004/(28,4)，反向原目标是21003/(34,14)，并不回到同一源格；不修成对称边。
- 21011/(5,32)原字面指向21012/(13,21)，另有回21010及往21016的候选。静态关联不证明可通行、碰撞、出口加载顺序或实际寻路。

18个来源楼层中，3413及21001–21016共17份DAT具有MAP04既存整SHA/宽高；本轮只核旧派生目录，没有新读DAT格或重绘场景。200没有匹配这955件目录的原DAT，相关坐标不能宣称完成地图几何验收。其余有几何的原配置坐标逐一在范围内。

## 与既有2003攻略比较，保持版本分离

复用仓库已验 `STONEAGE-CN2003-LIULI-CAVE-SOURCE-R1.json`，本轮没有重新请求原网页。旧R73的原HTML/历史捕获SHA及全部ID=null字段保持原样；指南的作者、商业build和原服运行资格不提升。

伊布原NpcWarp有9个位置出现，200/(115,1011)重复一次；去重后8个坐标与旧2003攻略的八处坐标集合完全一致。它是**分源坐标吻合**，不能证明两个载体同构建或原NPC随机权重。保存本只有一个对应CREATE配置，不是九个或八个NPC实例。

攻略把(34,10)的审判者写在4楼；原CREATE和条件文件在内部floor21003/(34,10)，原WARP为21003/(34,7)，FREE字面为`LV>0&ITEM=2700,LV>0&NOWEV=39,LV>0&ENDEV=39`，MONEY=-1。不把内部floor编号直接换算为显示层数，保留差异；不把FREE/MONEY解释成已运行准入/收费公式。原脚本给源数字不回填指南未知item/NPC ID。

## 私人交付、验证和下一项

原11文件、12物品行、六跨源候选PNG、派生摘要与说明，共31成员私人包 **33,625B / SHA256 `7e649bb321bb6c1f4f92cb82f5bc3f36de9f8906476574a13472b6bed13d55f7`** 已保存，并从保存结果独立回读，整字节/SHA及31成员CRC全部一致。原商业对白、配置、DAT、图像或程序不入公开Git。

公开交付：来源限定JSON、复用QUEST17 CP950解析器的提取工具、10项专项验证，注册进既有QUEST05 CI；没有新增工作流。专项+QUEST17/19/20+原R73共45项本地检查通过。原字节派生再次生成与JSON一致；远端候选/主线验收按实际后验追加，不预支成功。

止点为本族静态关系与分源攻略对照。原生任务/奖品/迷宫均未运行，原始常驻/活动归属仍UNRESOLVED，Stage A **7 PARTIAL+2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、overall_percent=null不变。

**NEXT：QUEST22_DISTINCT_SOURCE_READY_FAMILY_AFTER_DEDUP_OR_MATERIAL_GAMEPLAY_REVIEW。** 先查旧R73、WORLD及QUEST01–21，优先另一族有原字节且能增加玩家内容关系的任务；若只是重算旧TYPE/奖池计数，则回模块组合检查，选择真实宠物、回合战斗或地图实物缺口。琉璃仅在新同部署原掉落表、原DAT200、运行轨迹或坐标加载证据到位时重开；不扩四洞窟全集、网服/账号或新引擎。


## 实际远端验收与下一接力（2026-11-08）

候选 `346d56aeb11bba3b2b8ace93fe91718341dddaea` / tree `083ad3e66e9e2d58bf218e232284a4be212676ca` 的 push QUEST `42470414995`、PR QUEST `42470429480`、PR O11 `42470429498`、PR O12 `42470429430` 四运行均 completed/success。PR专项 job `128699661496` 实际日志确认新增10项通过。候选五份完整远端文件与本地字节全同，完整tree同一。

[PR #261](https://github.com/chinaneedM/stoneage-rebuild/pull/261)已squash合并为 `8400b9ece904bfba7d4f8b17c423c8c5204452ab`，tree仍为上述已验内容tree。内容主线专用 [run42470721385](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42470721385) / job `128700592141` completed/success，日志同样确认10项新检查；公开CI仅读派生元数据，未重读私人原件。全257任务相关本地测试通过；另独立逐源行复核六脚本数字命令顺序、54个有资格目标坐标均在既存DAT几何内。没有新短期原源工件。正式 **QUEST21=ACCEPTED_SOURCE_BOUNDED**，此前“后验另记”由本段真实验收补足；旧失败历史不删除。

完整原CURRENT blob及原攻略ID未知字段保持不变。实际身份与数值资格见 `research/recovered/STONEAGE-QUEST21-PUBLICATION-ACCEPTANCE-R1.json`。本验收追加提交自身Actions不预支；后续重新启动仍须从新远端HEAD/tree/Actions确认。

下一最高明确为 **QUEST22_HEKISEI_WATER_SPIRIT_SEVEN_SOURCE_SCRIPTS_AFTER_DEDUP**：已在同一私人NPC载体确认 `jaruga/event/hekisei.create` 精确引用 `hekisei` 与 `hekisei01–06` 七脚本。先查旧WORLD/QUEST01–21/R73及相关文献覆盖，再仅核三类39/40/42前置与事件46、2766–2770的原获取/交付关系，有真原字节才关联道具/地图；不能把只含TYPE数重算当新内容。本轮仅做了候选可得性预检，**没有声称QUEST22已完成**。若无实质关联增量则回模块组合材料复核，不扩全部四洞窟、账号网服或引擎。所有Stage与未知边界保持。
