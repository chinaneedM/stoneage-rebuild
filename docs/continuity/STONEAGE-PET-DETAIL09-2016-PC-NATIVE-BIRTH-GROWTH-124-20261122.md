# PET-DETAIL09｜PC宠物原生创建／成长源码与124图号2016同树数值研究（2026-11-22）

## 启动与只读审计

本批重新取得远端GitHub主线 `chinaneedM/stoneage-rebuild` HEAD `c1548e39e05a23145f74703ccbfcb1629d70d988`、默认main、最近提交、历史连续性协议、README、PET模块目录、年度路线、完整原历史 `docs/CURRENT-STATE.md` blob `c89e0e33537990aa2132b47c40fef49a985a935c`（Git 2,709,173B，connector返回全文2,317,877 JS chars）、上一批PET08原文与机读收据；候选PET08原分支21/21 Actions成功且已合并。旧CURRENT巨文件始终保留原SHA，不裁剪。用户此前提出“宠物生成必有初始模板／规则，应该直接从原端找”，因此本次直接审原C源码、同版配置，不再查零散玩家攻略。

## 本轮真正取得的原C源码事实

从已登记为**2016年后期社区PC服务器**而**非官方台湾1.0服务端**的 `pimpcapital/longzoro-sa` 固定提交 `57b14e2bb373ba851c14db28a239273e4a8831bb`，这次确实读取了真实原文件：
- `gmsv/src/char/enemy.c` 原 Git blob `72e43f44a76db4baa23dfcea568f16d54d3bf620`，含 `ENEMY_getRank`、`ENEMY_createEnemy`、`ENEMY_createPetFromEnemyIndex`（第二条是玩家获得新宠物的生成代码路径，不能冒称原早期服捕获成功）。
- `gmsv/src/char/char_data.c` 原 Git blob `f12bee31be5ad9b7bd6754201631b441d1e4107e`，含 `CHAR_PetLevelUp`：直接读`CHAR_ALLOCPOINT`及`CHAR_PETRANK`，十次随机分配、根据六档随机范围450–500至550–600，再按0.01倍率计算四能力增量。
- `gmsv/src/include/util.h` 原 Git blob `a86dd72c1d71cef41ce0f1ad228b7cc1832daa90`确认`RAND(x,y)`**上下界均含**；`gmsv/src/include/enemy.h` blob `f929766fb3b3aa9b15b6d4278109ad9368a7e18e`验证内部字段宏；`gmsv/setup.cf` blob `9d5992bfb1065d6c405ebe4a0677acb7be0de5f9`确认2016本配置选择同提交`data/enemybase1.txt`及`data/enemy1.txt`。

**真实创建公式是同一来源C的FACT，不是跨源码脑补**：随机等级来自敌人实例最小/最大配置；从模板读取`INITNUM`、`LVUPPOINT`、四BASE，给四BASE各随机`RAND(0,4)-2`，打包进`CHAR_ALLOCPOINT`；再把10个0–3随机落点分给四暂存数；`CHAR_VITAL/STR/TOUGH/DEX`按 `((LV-1)*LVUPPOINT + INITNUM) * (BASE + 个人扰动 + 十点分配)` 更新。rank`ENEMY_getRank`用未经个人扰动的四BASE原和分100/95/90/85/80/0六档；代码在生成宠物时向`CharNew.unionTable`复制模板技能槽。原生成后还走`CHAR_complianceParameter`，因此所求**创建中间内部四数值不等于面板HP/攻/防/敏**；没在本会话编译/运行该2016服务端，也不能据此确认实际出生分布或原官服。

## 124份逐宠Lv1中间属性候选与两源差异

从以前已经SHA证明的**同一个2016提交**[PET-MODULE-01 1816行模板+2958行实例](../../research/recovered/STONEAGE-PET-MODULE-01-BATCH-SOURCE-SPR-INDEX-R1.json)，把原台湾1.0具名图形号做数字相等索引：124/124原图形命中2016 `PETFLG1`共195条原模板，195个不同模板ID。2016 `enemy1.txt`内176模板有1级可选的原实例行，共370条原实例；全部124个原TW1来源图号至少可以找到一条**后代2016静态Lv1候选**。它只表明配置可选LV1，不证服端实际刷怪、原TW1起始四围或2016的官服身份。

每个2016模板均按原创建逻辑给出**假设Lv1的单项内部属性可达包络**：`INITNUM*(BASE-2)`至`INITNUM*(BASE+12)`；四属性共享10个随机加点，不可同时取四个最大值。其角色显示值须再审`CHAR_complianceParameter`等实际流程而非仅用十点公式。

针对另一个**非同一原包**的混合2.5社区PC保存[PET08后期服务器源](../pets/TW10-124-MIXED25-SERVER-TEMPLATE-STATS-REFERENCE.md)，只在**同图形整数且全部初始数值/元素/技能槽字段一一相同**时才记录“不同后期存档数字吻合”：2016年195条模板中152条满足，覆盖121个TW1图号，剩余三项图号**无完全相同配置**：`PET-000025`石龜100274、`PET-000096`霍爾克100369、`PET-000097`奇寶100370。前两套社区资料可能有复制/共同祖源，**不能把152条当成两份独立当代官方初值验证**。1999日本JSS、TW2000正式原服或大陆1.82原客户端与此2016规则等同仍无一手证据。

[124份逐只可查生成/成长视图](../pets/TW10-124-2016-PC-SOURCE-PET-BIRTH-GROWTH-REFERENCE.md)、[机器模型195模板/370Lv1实例/152跨社区相同记录](../../research/pets/PET-DETAIL-EVIDENCE09-2016-PC-BIRTH-GROWTH-124-LV1-REFERENCE-R1.json)、新增测试。公开只存数值/原Git哈希/源码入口，不转存第三方完整商业资产或服务器配置文本。真正新增的原官方PC二进制0字节；early官方初值0行，官方实发物种0只；124份TW1来源永久档案仍PARTIAL、全字段0，2026 PC年度仍`NOT_YEAR_AUDITED`，PET唯一活动、StageA7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总百分比UNKNOWN。

**下一 PET-DETAIL10**：优先寻找台湾1.0／大陆1.82等有来源可读的原始同构建PC Pet master 或真实宠物初生与技能运行日志；若不可得，先按已经恢复的TW1原EXE仅在有源偏移窗口核对服务器宠物状态接收，不能由“客户端接收宠物字段”推出“绝对不存在本地生成函数”。没有实际新内容就以来源有界止点记录，不无限增大后期社区GMSV解释，不切NPC、不含手游、私服专属物种或付费介质。
