# QUEST19｜马祖送信、切绳石与十处宝袋：静态原任务、奖励、NPC重定位来源

日期：2026-11-08。任务：QUEST19-DEDUP-AND-NEXT_DISTINCT_ORIGINAL_FAMILY。

## 远端续接和证据身份

本轮从 GitHub 远端 `main` `8d53deb9aa5b6fd0580ac89426cfee6ae7b8ea6a`、tree `5a3e57cea67efa5dada1a8c9b0d2f28ef0197068` 读取最新 Actions、协议、README、决策、路线和 QUEST18 后验；`docs/CURRENT-STATE.md` 原 blob `c89e0e33537990aa2132b47c40fef49a985a935c` (2,709,173B) 完整重新读取，不截断、不覆盖。QUEST18 已合并，下一项是 QUEST19。选定不同的 `extra/event/marju.create` 源族；QUEST01 已有其 12 CREATE / 12 脚本 / 27 事件旧全量索引，因此**不是发现了27个历史未知事件**。O74 的四大厅委托书和 QUEST08–18 当前专项不与本源文件重复。

两份已有私人原件本轮实际校验：
- CHAR01 NPC ZIP 995,176B，SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`，2,205成员全 CRC 正常。读取 `marju.create` 原始1,896B和12份不同脚本，CP950 无损还原、全原 SHA/CRC 与 QUEST01 原索引对齐，27个 TYPE 段全有既存规范化段 SHA。
- ITEM01 保存的双物品表94栏逐行源缓存与 TW1 零售原 RD 候选 ZIP 5,868,386B，SHA256 `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa`，838成员 CRC 正常。61个涉及的物品在缓存两表均存在且成对原行 SHA 相同；本轮**没有重新取出最初361MB RAR中的两份完整 itemset.txt 原文件**，不能把缓存复核写成原文本重新提取。

这些是后期社区保存 mixed25 源，`ORIGIN_UNRESOLVED`；**不是**已认证JSS1999、台湾1.0、初期大陆1.82原商业部署。TW1的像素原件是另一载体，只能形成跨载体候选，不得推官方同服、真正客户端 UI、原 NPC 动画或存档效果。受版权保护的原脚本/原图/源 ZIP 均没有加入 GitHub。

## 新联接：送信、工具与宝袋

静态脚本的玩家内容链如下：`marju` 的 `EventNo:37`、`LV>49&ENDEV!=38` 条件下有 `GetItem:2687`（邮寄物）；`marju01` 的 `EventNo:38`、`NOWEV=37&LV>49&ITEM=2687&ITEM!=2697` 下字面有 `DelItem:2687`、`GetItem:2697`（切绳石）、`EndSetFlg:37`；返回 `marju` 的 `EventNo:38`、`ENDEV=37&LV>49` 则有 `GetRandItem:2688,2689,2690` 与 `EndSetFlg:38`。接收人同源还有另外的取石分支，不得武断认为切绳石只能通过送信取得。所有条件均为**静态字面**，原运行时事件优先级、真领取/真发放/状态保存及可重复性尚未验证。

10个“宝袋”NPC，分布在原数值 floor **122六个**、floor **118四个**。它们的 `ACCEPT` 分支共同出现 `LV>0&ITEM=2697`，`GetRandItem`、`DelItem:2697` 和 `NpcWarp`，无石头时为不同 `MESSAGE` 分支。**NpcWarp 是 NPC 重定位命令字面，不能宣传为玩家能传送的路线。** 10条 NpcWarp 总共50个三元坐标，全部不同、均在已认证 MAP09 两层地图的源宽高内；每条有5个候选，其中1个与自己原创建格相同。全部选点概率、移动/消失、碰撞、是否原服可达仍 OPEN。另两位人物创建 floor 119 / 1300 不在当前 MAP09 691目录及 MAP04的955结构源列表，并不等于原游戏不存在这些楼层。此次没有读取新的 DAT 原格或进入原游戏。

**随机物品不是已知掉率。** 11条 `GetRandItem`（马祖1条、宝袋10条）有415次原字面候选引用；马祖奖品列3个；宝袋6份36位列表（其中27不同ID），另4份49位列表（29不同ID），保留相同ID的重复出现。联合是59个不同候选ID；不能假定“重复两次=双倍概率”，更不能把候选数量当真正获奖次数。

关联 `GetItem/DelItem/GetRandItem` 共61个不同物品ID，私有双表源行哈希61/61成对相等。60个ID所对应的原图候选在TW1零售载体可观察，**邮寄物2687的源图别名24314未见于此零售图索引**。61个ID仅有58个不同别名；其中57个是带零售原RD候选的别名，不能按物品ID数量计算不同图/装备种类。

## 成果和停止条件

版本分离索引由`NPC创建位置→脚本/事件条件→原道具ID与行SHA→NPC重定位目标floor/x/y与MAP09宽高`组成；原像素/文字仅留私人档。公开派生JSON `research/recovered/STONEAGE-QUEST19-MARJU-POST-TREASUREBAG-SOURCE-R1.json`，公开回归 `tests/test_stoneage_quest19_marju_source.py`，复用现有 QUEST05 统一工作流。所有“旧索引已覆盖”继续保留，不能把新增验收数量算作 Stage A 完成度。

**QUEST19当前为 SOURCE_BOUNDED_CANDIDATE；只有GitHub候选和主线验收真实成功才转为 ACCEPTED_SOURCE_BOUNDED。** 当前 Stage A 7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，overall百分比 null。下一最高 `QUEST20_DISTINCT_SOURCE_FAMILY_AND_WHOLE_MODULE_PRIORITY_REVIEW`：继续任务族前先查重，并评估是否应转向能够增加真实宠物/战斗/地图可见内容的原件；没有实际新历史业务内容就停止扩张，继续纯离线单机复原，不启动网络帐号、原服或新引擎。

## 后验验收、第一轮失败和续接优先级（2026-11-08）

- 起始候选 `d3b745a93dc11476882b9f7fad2621e3fcb575bd` / tree `c044ebccb903a42c851b3b59bd143a8febd5be38` 只改动 **4 个公开路径**（来源限定数值与SHA JSON、回归测试、连续性研究、既有专项 workflow）；没有受版权保护原NPC/94栏正文、PNG、原ZIP或客户端二进制。候选原脚本/道具ZIP保留在个人 Library 的已保存父来源中，本轮没有制造新的私人子ZIP或声称重新获取官方原服务器。
- 首次 push [#42467038541](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42467038541) 及 PR [#42467058737](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42467058737) **completed/failure**：5个 QUEST19 正面检查成功，1个 negative boundary 测试误引不存在的 JSON 键 `treasurebag_npc_relocation.actual_NpcWarp_selection_UNPROVEN`，是测试代码笔误，**不是源哈希或历史数据矛盾**。首次PR另两条工作流 [#42467058734](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42467058734) 和 [#42467058816](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42467058816) success。失败记录永久保留。
- 修复 commit `affa0279d1da487f8d20d9fc988c88c2bc0c1f7a` **仅更正两个断言**：对原有 `bounds.native_NpcWarp_execution=false` 和 `random_candidates.actual_reward_UNPROVEN=true` 做正确读取。修正后候选 push [#42467182699](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42467182699) success，PR 三组 [#42467186011](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42467186011)、[#42467186059](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42467186059)、[#42467186093](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42467186093) 全部 success。
- [PR #259](https://github.com/chinaneedM/stoneage-rebuild/pull/259) 已确认 merged=true；主线 squash commit `9aa41ceeeb207e774f8bfc88225683c2c4cda0fb`，tree `1881487d1089b93a66b5563d4c79e3c40f4c8bd6`。合并后主线专项 [#42467228444](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42467228444) 实际 **completed/success**，验收只覆盖公开静态证据/负证而非原商业运行、官方部署或真实奖品掉落。
- 正式 **`QUEST19=ACCEPTED_SOURCE_BOUNDED`**。源只确证12 原NPC配置、12不同原脚本、27既存事件、送信/切绳石数值流程、10 宝袋 NPC 重定位与两组随机候选原数字、61 ID 双表保存行SHA及已知跨载体图资格。台湾1.0同部署、原生事件分支、真NPC移动、真实随机概率、原119/1300楼层载荷仍 OPEN。全部 `docs/CURRENT-STATE.md` 旧 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 2,709,173 B **未修改**。
- **下一最高：`QUEST20_DISTINCT_SOURCE_FAMILY_AND_WHOLE_MODULE_PRIORITY_REVIEW`**：重新读主线后先审全任务模块已登记材料，再挑另一组实证原游戏内容；如连续只重复QUEST01旧索引且无法新增真实规则/视觉/跨模块关系，应主动转回宠物/战斗/地图可见内容。不要无界扩任务脚本、账号、联网服务或新引擎。Stage A 7 PARTIAL+2 OPEN；Stage B/wiki GATED；R79 PAUSED_NON_BLOCKING；整体百分比未知。
