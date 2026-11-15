# PET16｜统一宠物资料目录、统计与证据缺口（2026-11-15）

**唯一活动模块：宠物（PET）。模块尚未完成，不允许自动转入NPC、地图或装备。**

## 可交付的检索成果

[源限定全量机器索引](../../research/recovered/STONEAGE-PET-MODULE-16-SOURCE-SEPARATED-UNIFIED-CATALOG-R1.json)与[纯标准库查询程序](../../tools/stoneage_pet16_lookup.py)，可以按中文/日文名字、原源行号、模板ID、图形号搜索。目录保留原来源归属、原始字段可证数值、原始行SHA、技能槽、来源索引、原图序列统计、原网页URL/抓取时间及其不确定性；方便今后的游戏参考与攻略网站利用。

| 独立来源命名空间 | 本次进入检索目录的记录 |
|---|---:|
| 2016后期社区服务端宠物模板 | 1024 |
| 2016后期社区宠物候选图号 | 598 |
| mixed25同一个原包主宠物表 PETFLG1 | 495 |
| mixed25同一个原包备选宠物表 PETFLG1 | 316 |
| 台湾1.0已真实读取图像的SPR候选组 | 131 |
| 日本Hangame原官方宠物网页位置 | 124 |
| 中国华义原官方网页位置 | 104 |

**以上共 2792 条来源记录，不代表同样数量的官方宠物**。彼此存在同源重复、候选跨载体同号和网页位置；不允许任意相加/合并为种数。

## 重要源证统计

- 台湾1.0零售 SPR 的131候选组包含 **7672 原动作方向段、73500 原帧引用、32155 独立原RD图像号**；**32150 严格两实现可解码、5 仅原画布范围内可观察**。PET15的原始私人图像档不公开，也没有证实131个官方物种。
- mixed25保留主表和备表各自的版本选择未知，不视为同一时期同时生效。PET13此前实核的11条编译捕捉候选，只有10条为主表PETFLG1，且根据**原物理行、模板ID、图号及56字段SHA同时相同**才在公共目录显示10个原名字；其余源名字仍为null。
- 2016后期社区资料内，2886 个正数技能槽中2784个可在同源码表定位、102个缺源定义；mixed25备表另有12个正数技能槽无同表定义。不声称官方台湾1.0技能效果或原生执行。
- 日本原官方网页124位置为原文具名页录，目前有一张独立原图已取得；中国华义网页104位置中98具名、6个源占位词仍未知，网页影像不能默认为可复用客户端贴图。
- 早先[GETPET 36条实例源关联](../../research/recovered/STONEAGE-INTEGRATION87-36-GETPET-TW10-SPR-2D-BRIDGE-R1.json)已列为宠物模块参考证据；静态可检索不等于原生颁发/捕捉完成。相关原任务、骑宠、进化材料只作依赖入口，不启动另一个模块。

## 可复用查询方式

```bash
python tools/stoneage_pet16_lookup.py --summary
python tools/stoneage_pet16_lookup.py --query 100400 --limit 15
python tools/stoneage_pet16_lookup.py --query 卡特利奴
python tools/stoneage_pet16_lookup.py --dataset jp_official_web --query ウーリ
python tools/stoneage_pet16_lookup.py --dataset cn_official_web --query 朱利洛斯
python -m unittest tests.test_stoneage_pet16_unified_catalog
```

输出按来源区分，而非自动拼出“同一宠物”。未来游戏设计可以由此定位原图私人保管记录及数值来源，未来百科可以由此生成有据命名、分版本内容；**本工作不授予商业美术公开或新游戏直接复用许可**。

## 七项可追踪缺口及恢复前提

- **PET16-01 official_early_pet_species_id**〔MISSING_SOURCE〕：TW10 retail SPR images are authentic but original same-build species-ID naming master absent。重开：Find and qualify same-client-build official server pet master or source in original client establishing name/ID/SPR identity
- **PET16-02 full_historical_species_roster**〔UNKNOWN〕：Official JP124/CN104 website slots are not complete game rosters; 598 graphic numbers, 131 groups and template rows are not species。重开：Obtain exact version/release authoritative full population with documented completeness
- **PET16-03 more_original_pixels_and_palette_timing**〔SOURCE_BOUNDED_PARTIAL〕：TW10 32150 strict, 5 bounded; CN5/TW85 original REAL coverage incomplete; client-native frame rate/color not verified。重开：New original complete source-qualified REAL/SPR/ADRN and verified native selector/replay
- **PET16-04 native_skills_growth_training**〔UNVERIFIED_RUNTIME〕：Static late source skills and 2016 missing 102 positive references plus mixed25 alt 12; no early official same-deployment execution。重开：Matched compiled handler/qualified original native behavior and complete source skill definitions
- **PET16-05 capture_encounters_gifts_evolution_riding**〔STATIC_PARTIAL〕：PET13 11 static capture keys, 36 GetPet instance IDs from integration87, official evolution references not proof of original runtime。重开：Qualified original game build state, handlers or authoritative primary rules for each original version
- **PET16-06 private_media_and_future_rights**〔RIGHTS_UNCLEARED〕：Retained client sprites and original archived page images belong in private custody; no automatic public game/wiki license。重开：Rights clearance or independent permitted artwork prior to any publication
- **PET16-07 original_server_table_active_choice**〔SOURCE_CONFLICT〕：mixed25 original main and alternative petflags conflict, 2016 later templates independent from TW10。重开：Qualify exact active configuration and deployment source for a known historical build

**下一项仅限宠物：PET17**，按目录优先补官方同版本已具名宠物身份关系、已有真实原RD与动画来源归属、技能/成长/捕捉真实相互引用，逐批改写本统一目录，不重复制造第N份无关联的零散报告。缺失同部署证据即保持UNKNOWN。宠物模块仍 ACTIVE / SOURCE_BOUNDED_PARTIAL，Stage A 7 PARTIAL+2 OPEN，Stage B及wiki GATED，R79 PAUSED_NON_BLOCKING，整体完成率UNKNOWN；历史CURRENT 2,709,173字节 blob `c89e0e33537990aa2132b47c40fef49a985a935c`不改。
