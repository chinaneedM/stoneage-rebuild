# PET18｜宠物原捕捉条件、道具数字与同源技能定义精确关系（2026-11-15）

**唯一活动内容模块 PET。PET18 是 PET16/PET17 图鉴的一个实际来源关联增量，不转去做全局道具、NPC或任务。**

## 证据和工具

在已有统一查阅工具 `tools/stoneage_pet16_lookup.py` 增加 `--capture-template`，读取并交叉校验两份**已经归档**的公开派生证据，不复制宠物大目录或原服务器商业文字：

1. [PET13 原编译捕捉候选与同 RAR 宠物主档/技能行](../../research/recovered/STONEAGE-PET-MODULE-13-ORIGINAL-CAPTURE-TEMPLATE-ATTRIBUTES-SKILLS-R1.json)，原 Git blob `835251479b2b7f55b3b6681af4d14b91008a305d`；
2. [PET16 统一七来源目录](../../research/recovered/STONEAGE-PET-MODULE-16-SOURCE-SEPARATED-UNIFIED-CATALOG-R1.json)，原 Git blob `fdb7d9aade2df62d1a1e06b2d2f9e383693ed980`。

**四字段同源关联门槛**：原物理行号 + 原模板ID + 原数字图号 + 原56字段标准化 SHA256 必须全部吻合，且保留 `PETFLG=1` 与 `PETFLG=0` 区别。技能名称还必须由同一归档的技能ID **及技能原行完整 SHA** 同时命中才返回，不能只靠同技能ID乱填名称。

本批既有来源提供 **11** 条编译捕捉候选、其中 **10** 条 `PETFLG=1` 可按四字段接入 PET16 主表，**1** 条 `PETFLG=0` 在 PET13 保留但不插入主宠物目录。原脚本候选涉及 **13次物品数字引用／12不同物品ID**，同源可定位 **5不同技能ID：1、2、60、90、110**，均非原客户端实测规则。

## 可观察的原来源样例

| PET13原模板 | 该来源原名 | PETFLG | 候选图号 | 编译捕捉物品数字 | 图鉴同源联接 |
| ---: | --- | ---: | ---: | --- | --- |
| 524 | 卡特利奴 | 1 | 100329 | 2456 | mixed25主表原行346、完整SHA匹配 |
| 961 | 艾蜜 | 1 | 101280 | 20219 | mixed25主表原行759、完整SHA匹配 |
| 1105 | 夏普德 | 1 | 101564 | 1690、1691、1692 | mixed25主表原行896、完整SHA匹配 |
| 8 | 巨大瑪恩摩 | **0** | 100355 | 1810 | **不进入 PETFLG1 主表** |
| 145/146 | 薩德迪比／薩德斯凱 | 1 | 101737/101736 | 各2236 | 各自原行145/146；不能无依据合并 |

样例原名字限于 mixed25 **社区保留的原服务器静态字段**，不升级为台湾1.0官方零售宠物身份。模板524在 PET17 的原SPR图号100329虽然能查到台湾1.0真原2D动作，其名字、数值、捕捉条件仍不自动属于台湾1.0官方同服。

## 统一查询方式

```bash
python tools/stoneage_pet16_lookup.py --capture-template 524
python tools/stoneage_pet16_lookup.py --capture-template 8
python tools/stoneage_pet16_lookup.py --trace-graphic 100329
python tools/stoneage_pet16_lookup.py --dataset mixed25_main --query 卡特利奴 --details
python -m unittest tests.test_stoneage_pet16_unified_catalog tests.test_stoneage_pet17_graphic_traces tests.test_stoneage_pet18_capture_skill_links
```

响应逐项保留 PET13原记录、同一原包资格匹配的PET16主表行、源技能行号及SHA、可证短名、候选物品数字。不存在的模板不伪造；未匹配 `PETFLG=0` 的记录不强行填充。数据可为将来来源合格的攻略条目与单机设计资料做入口，但**不表示道具真实消耗、捕捉概率、模板选择器、技能发动效果、成长公式、宠物出场或原服运行已获证明**。

## 验收与模块状态

专门新增 PET18 负例测试，并与 PET16/PET17 在 GitHub Actions 同一真实候选 HEAD 上核验。失败与更正必须前向保留；未验收前不声称PASS。

- 未引入新原历史物件、未修改来源数值、未发布受保护商业图像/服务器原文字或本地缓存。
- PET16七项原缺口及官方同部署/原生行为/授权缺口全部保留；不可声明SOURCE_BOUNDED_CLOSED，更不能声明历史100%。
- 历史 `docs/CURRENT-STATE.md` blob `c89e0e33537990aa2132b47c40fef49a985a935c` 不变；Stage A 7 PARTIAL + 2 OPEN；Stage B/wiki GATED；R79 PAUSED_NON_BLOCKING；整体完成率 UNKNOWN。
- **后续仍在 PET 模块内**：优先批量追溯2016同源102个未定义的正数技能槽与mixed25备表12个未定义技能槽；没有可用同版技能主档则保留MISSING_SOURCE；另审查原宠物成长列的有据定义与真正原生效果缺口，不按字段名虚构公式。


## 2026-11-15 前向PET19技能缺源复核

[PET19 102+12次缺定义技能原槽/来源审计](STONEAGE-PET-MODULE-19-MISSING-SKILL-SOURCE-GAPS-20261115.md)已接入同一宠物统一查询入口的 `--skill-gaps`，未另造第二份宠物身份主表。2016备用技能文件原SHA与56个不同技能ID已核，不能补30个缺项；mixed25备表5个缺技能ID在主技能表另有同数字记录，但源表配置未知，不能替代原配对。上文初始 `下一步` 现由这份PET19实际审计前向续接为PET20；PET仍唯一活动模块，旧报告不改写。
