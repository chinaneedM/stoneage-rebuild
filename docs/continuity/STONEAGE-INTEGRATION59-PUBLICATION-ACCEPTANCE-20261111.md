# INTEGRATION59｜四村八装备店原数值与台湾1.0原图候选：正式出版/Actions验收（2026-11-11）

## 远端连续性基准与选择

本单元按GitHub远端权威状态重新读取 `main` `bf3c1ab27cfa71abb4a9ea32687aa9a178caf0e7` / tree `5df26356495a52894350084d2104d16b782fc800`，复核完整树、最近提交、Actions、`docs/PROJECT-CONTINUITY-PROTOCOL-R1.md`、完整 `docs/CURRENT-STATE.md` Git blob、README、设计/历史/来源/路线、按模块优先级以及INTEGRATION58正式验收。最高NEXT转向尚未完整联系的**原物品/装备/技能/配方与场景/任务的玩家可见材料**；避开重复波鲁龙巢及已编目的商店清单。

新增联接在 [INTEGRATION59日期说明](STONEAGE-INTEGRATION59-FOUR-VILLAGE-SHOP-NUMERIC-PIXEL-20261111.md) 与 [来源限定派生JSON](../../research/recovered/STONEAGE-INTEGRATION59-FOUR-VILLAGE-SHOP-120-ORIGINAL-NUMERIC-TW1-PIXEL-CROSSWALK-R1.json)。原 mixed25 NPC创建和商店参数8个源配置，保存版地图1001/2001/3001/4001各两店：**67攻向数值组+53防向数值组=120原ItemList直接数字引用**；合计56不同源物品ID，45个TW1原RD图号候选。原94列表第37—42零基字段共56组六数值逐行回读、均成三对同值，源A/B同ID整行SHA和这六值一致；原CREATE、ItemList、原物品行和早期图像是来源分层候选，不是相同官方部署或真实装备/商店效果的实测。

## 私人原件实际资格（与公开CI严格分离）

本轮重新从个人Library获得已经依据后期原RAR+原TW1零售像素建档的ITEM01私人源资料包：
`StoneAge-ITEM01-private-two-itemsets-832-original-RD-icon-observer.zip` **5,868,386B/SHA256 `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa`**，整ZIP SHA及**838/838 ZIP成员CRC检查通过**。56条保存的原94列双表记录真正逐内容核对，45张不同保存的真实TW1原PNG也逐SHA与既有原RD保存收据比对（45/45）；非新原图解码。没有在本轮重新打开原始361MB mixed25 RAR、抽取原itemset文件或重新读取原TW1 RD二进制，也没有运行原商业客户端/服务端。此证明是**先前经原件解读的私人研究保留副本重放**，不能提高到原始程序运行证明。

公开Git只有源数值、原成员及原行SHA、已有索引身份交叉、原候选资格、测试/Workflow/说明；没有商业原字节、原物品/脚本正文/完整私人图像或观察HTML。公众 CI 依靠7份Git上旧物品shard和224店/191创建公共目录，不声称在CI里得到私人原像素。

## GitHub候选、合并与实测Actions验收

| 证据阶段 | 已经实际发生的结果 |
|---|---|
| 候选分支 | `agent/stoneage-integration59-four-village-raw-stats-20261111` |
| 候选 HEAD | `5292032ef6762dbf35698505c1004725c53006fa` |
| 候选 tree | `50668ec38926cf6e99316ae50a646c835591a317` |
| Pull Request | [#327](https://github.com/chinaneedM/stoneage-rebuild/pull/327)，源head与base核对后mergeable=true、以候选SHA固定并正式squash合并 |
| 候选 Actions | **46/46 completed/success**（push27/PR19）；专项 [push run42957908688](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42957908688) job130317290941 与 [PR run42958035351](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42958035351) job130317701272 均成功 |
| 内容main HEAD | **`1338e74802d401eef01a1aaa8a935b032e5024fb`** |
| 内容main tree | **`50668ec38926cf6e99316ae50a646c835591a317`**，与候选tree相同 |
| 内容main Actions | **27/27 completed/success**；专项 [run42958263682](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42958263682) job130318437591真实成功 |
| 专项校验 | `python -m unittest discover -s tests -p 'test_stoneage_integration_module_59.py' -v`，7项测试实际在候选push/PR及main运行成功 |
| 历史CURRENT保全 | `docs/CURRENT-STATE.md` blob **`c89e0e33537990aa2132b47c40fef49a985a935c`**；2,709,173B，原样保留、无修改 |

以上 Actions 为实际完成后从GitHub读取，不预先预计成功。**当前此验收收据提交自身HEAD没有在本篇额外宣称运行新的Actions**。

## FACT / OPEN / 新优先级

FACT：在私人保留的原来源派生目录中，四地图8店原CREATE和原物品数字清单均可按原路径/源SHA查到；56独立物品的原值数列具完整源行SHA，120次清单关联对应45个此前已认证原图解码候选。此为一个可复现的静态研究联合层。

OPEN：上述mixed25社区保存的NPC/商店/物品是否曾与TW1零售原图同一官方服实装、是否等价于JSS1999/大陆1.82内容、原装备真生效公式/商店购买交易/原UI原色选择、碰撞NPC交互与玩家原生实际体验。120不是120个物种或120个不同装备；45张图不等于45个新发掘资源。

阶段门槛不变：**Stage A 7 PARTIAL+2 OPEN；Stage B/wiki GATED；R79 PAUSED_NON_BLOCKING；overall_percent=null。** 不启用多人/网络/账号/服务端运营，也不擅自进入新作引擎生产。

**最高NEXT：** 已完成这8间四村装备店的数值—原图源联接，下一轮轮换另一组真实且尚未有据联接的物品功能/技能/配方与地图NPC任务材料；仍必须基于精确实际原件、去重现有目录，无新可验证输入则记止点，绝不继续泛化查看器、舞台进度百分比或虚称原版可玩。
