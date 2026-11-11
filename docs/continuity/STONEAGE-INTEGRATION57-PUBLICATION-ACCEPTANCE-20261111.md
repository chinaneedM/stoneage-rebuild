# INTEGRATION57｜吉鲁两族人物与同源原图：正式合并、私人保管及CI验收（2026-11-11）

## 远端连续性原基线

按仓库`docs/PROJECT-CONTINUITY-PROTOCOL-R1.md`从GitHub远端默认main `e66f847cfcf32865a4b1acb1d5da8039bef09d20`，tree `ba1d840b3e7d878da7c48069bd1b84725ee85879`独立重启，现场重读最新分支、HEAD、tree、提交、Actions及README、连续性协议、历史、设计、来源、路线、模块、最新INTEGRATION56验收，完整读取Git blob原`CURRENT-STATE`（普通文件接口返回空，但原Git blob实际**2,709,173字节**，blob `c89e0e33537990aa2132b47c40fef49a985a935c`）。原CURRENT全部保留，未改写、截断或只拿末尾替换。

## 本轮真正的玩家可见内容增量及版权保管

[限定研究报告](STONEAGE-INTEGRATION57-GIIRU-TRIBES-SAME-CARRIER-PIXELS-20261111.md)及[144原RD/PNG源SHA、动作帧序与原创建地图实证](../../research/recovered/STONEAGE-INTEGRATION57-GIIRU-TWO-TRIBES-31205-ORIGINAL-RD-SOURCE-R1.json)以另一后期mixed25社区保存来源为唯一材料类：该RAR SHA256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`，非认证纯净官方版。

- 从私人`StoneAge-QUEST11-two-tribes-original-private.zip`（**264,869B/SHA256 `99002423db31754c514863da018b112adcb7252eabce17cb112c42b815150a49`**，56/56成员CRC）重新读取原`garunaev1.create`与`garunaev3/6`静态剧情源、`original-DAT/31205.dat`完整原25×25地图DAT3,758B/SHA256 `5fb967a40557cb185ee9402beb35e2b2e51e56a356dec6c6285cc0a101c2ed3d`。原CREATE序号2/5依次引用图号100250/100252，原(12,11)/(12,12)，三个未改的原地图u16字段`4015/0/49152`与`4003/0/49152`。两原脚本先前已记录13/15个TYPE段，不称新发现的原文段。
- 真读同社区混合RAR已保管SCENE13私人源包（**975,186B/SHA256 `21b56fe9a49357f0d7815698bd1db67f72076759a2528348888fe06444868238`**，6/6 CRC）。其中真正原RD子块及原内嵌PNG解码后各图完整SHA与旧先验`research/recovered/STONEAGE-SCENE13-PET-ACTION0-R1.json`匹配。两原图形源SPR组100250/100252共16原方向序列、280**按原序且允许重复的帧位置**、144**不同原RD bitmap**。**144/144原RD字节SHA、PNG文件SHA、RGBA像素SHA和尺寸**逐项一致，本轮新原RD解码=0，不混为144种物种。
- 单独私人来源包`StoneAge-INTEGRATION57-Giiru-two-tribes-same-carrier-motion-private.zip`，**869,340B/SHA256 `f43c0bd3a7ff16a2a580ec9a7d024bceb58ab20e31175618a9f174b727306a99`**，297成员/144原RD+144原PNG、原DAT、原CREATE、两原脚本、现代脱机查阅HTML。**上传个人Library `/石器时代/` 后独立下载并逐全包SHA、全部297 CRC、144 RD/PNG/RGBA SHA核验通过**。Chromium实际切换16/16源动作方向序列并载图，JS错误0/外网请求0；这是现代研究工具而不是商业原游戏运行。
- 公开Git只提交**5个版权安全文件**：派生来源JSON、对照测试、Actions工作流、连续性覆层、README追加。原商业DAT、NPC全文、RD、PNG和私人HTML没有进入GitHub。公开CI只回放被保留的Git源数值及SHA；不会下载用户私有资料。

## 准确的远端Git及Actions验收链（含早期失败）

| 阶段 | 实际经GitHub读取的结果 |
| --- | --- |
| 原起点main | `e66f847cfcf32865a4b1acb1d5da8039bef09d20` |
| 最初候选提交 | `ff71234aea114ed720cc7c3e2641709fe01d9469` |
| 最初候选push | **27项：26 completed/success、1 completed/failure**。失败的[run 42950225053](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42950225053)是新专项测试Git blob零字节常量转义写错；保留失败记录，不混为已成功 |
| 更正提交/候选最终HEAD | `6e5bb296522c3926963856ec8e8089690b2f2dd1`，仅修复专项测试Git blob零字节边界，未改变来源报告/商业原件 |
| 更正后候选tree | `4663be93644af6beee38b111f72f5f0b6c6621d5` |
| 更正后候选HEAD Actions | **20/20 completed/success**：push1，[run 42950273323](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42950273323)；pull_request19，[专项run 42950321140](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42950321140) |
| PR | [#325](https://github.com/chinaneedM/stoneage-rebuild/pull/325)，严格按最终HEAD验收、检查main未变且mergeable clean后正式squash合并 |
| 正式内容main HEAD | **`776fe59df0aaa39eeca7c4be50743c3d94d6ea89`** |
| 正式内容main tree | **`4663be93644af6beee38b111f72f5f0b6c6621d5`**，与最终候选tree完全一致 |
| 正式内容main Actions | **27/27 completed/success**，无失败／排队／进行中；[本专项run 42950455758](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42950455758)成功 |
| 原历史连续性blob | `c89e0e33537990aa2132b47c40fef49a985a935c`／2,709,173B，合并后tree再次核同不变 |
| 原始公开派生报告Git blob | `61fc86b23299c2920f4f4b2cf9f45957d1e21a35`，已经长期保存在正式main |

## 原版状态不可晋升边界

同一混合社区RAR保存NPC创建、DAT和同数字图形/原位图，是有来源的**同载体候选实物关系**，并不等于官方初版历史服务器已同版本部署，亦非NPC原生图形选择、动画真正播放、地图碰撞、对话、战斗、任务旗标或物品奖励已经执行。现代离线像素HTML非原商业原生截图。原台湾1.0、JSS1999及大陆1.82的原身份并未得到这种同载体回放的认证。历史Stage A仍**7 PARTIAL + 2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、总体完成率无法给百分比。

## 继续交接

**最高NEXT：** 结束吉鲁两族`31205`和`100250/100252`原动作图号；不要再扩相同源图帧或旧任务。转另外一组**未完成、具原DAT+具名原NPC/任务+实际原可见图或实用原物品图**的原版游戏内容，有强来源才整合。资料缺失就明确止点和切换到其它源充足模块，不新增体验优化、单机引擎或网服账号。保留宽泛分类视图的灵活性，不把UNKNOWN岛屿/原族系强行绑定。

**本页仅在以上内容main 27/27 Actions正式成功后新增提交。此收据HEAD自身不预先宣称另经27项主线Actions验收。**
