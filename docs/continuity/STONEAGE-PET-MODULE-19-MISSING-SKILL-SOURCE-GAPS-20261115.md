# PET19｜宠物技能缺源核对：2016配置主表与mixed25备表（2026-11-15）

**唯一活动内容模块仍为 PET。** 本批承接 PET16–18，以既有宠物统一入口完成**全量未定义技能引用的可查询清单**。不建立第二份宠物主表，不启动NPC、地图、装备或未来新游戏。

## 原文件证据与选择边界

- 2016 后期社区 `pimpcapital/longzoro-sa` 固定提交 `57b14e2bb373ba851c14db28a239273e4a8831bb`：此前 [PET03 原技能联接](../../research/recovered/STONEAGE-PET-MODULE-03-SAME-SOURCE-SKILL-JOIN-R1.json) 已证 `gmsv/setup.cf` 中的 `petskillfile2` 指向 `gmsv/data/petskill2.txt`（原 blob `83d2daeb9e57b089a304f127361f88514386b870`）。本批**新重新读取**同提交另一份可选 `gmsv/data/petskill.txt` 原 blob `846d379f0c7977b3e74d5a5a9580a35a85cafc51`，核对 56 行全部为 9 字段，第 5 列得到 56 个不同技能 ID；与所有 30 个缺失的正数 ID 的交集为 **0**。备用表不能当作实际选中表、不能从备用表无证补技。
- mixed25 社区保存 RAR `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`，以前 [PET10 原包源收据](../../research/recovered/STONEAGE-PET-MODULE-10-ORIGINAL-MIXED25-SERVER-TABLES-R1.json) 已分别核验 `enemybase.txt ↔ petskill.txt` 与 `enemybase2.txt ↔ petskill1.txt`。本批按原数字与 SHA 重新校对两对源表。**未证明原服务器当时实际选用哪个组合**。
- 统一图鉴仍为 [PET16 2,792条多来源记录](../../research/recovered/STONEAGE-PET-MODULE-16-SOURCE-SEPARATED-UNIFIED-CATALOG-R1.json)。本批只有派生元数据、技能ID/行号/SHA与源引用，不公开原客户端图片、原服务器整行或私有资源。

## 实际审计结果

| 受限定的原源 | PETFLG1模板行 | 正数技能槽 | 同配对表已定义 | 本表缺定义 | 缺失不同ID |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2016后期社区配置模板 + `petskill2.txt` | 1,024 | 2,886 | 2,784 | **102** | 30 |
| mixed25主表 + `petskill.txt` | 495 | 1,050 | 1,050 | **0** | 0 |
| mixed25备表 + `petskill1.txt` | 316 | 661 | 649 | **12** | 5 |

2016 的 102 次缺源覆盖 **76 个不同原模板行**；另外有 **20 次 -1 原负数哨兵槽**，不可计入正数缺技。30个缺源技能 ID 原集合：`18,21,22,42,111,112,113,114,515,517,518,519,520,561,567,568,645,729,730,731,732,737,738,739,740,741,742,743,744,745`。原配置的活跃技能表和已核固定提交备用表均没有这30个 ID。这是**当前取得的两份表缺定义**，不是历史原游戏绝对没有技能。

mixed25 备表缺源 ID：`503,541,542,580,600`。在同一 RAR 保存的**另一份主技能表**中逐个找到同数字定义（仅跨表候选）：

| 技能ID | 备表缺失引用 | 另一主技能表原行 |
| ---: | ---: | ---: |
| 503 | 4 | 61 |
| 541 | 2 | 68 |
| 542 | 1 | 69 |
| 580 | 1 | 88 |
| 600 | 4 | 98 |

原行 SHA 在机器审计中保存，不能借此把主技能表静默替换为备技能表，更不能无原代码或配置认定技能真实生效。

## 同一个图鉴检索入口

[可独立重播与检索的机器审计](../../research/recovered/STONEAGE-PET-MODULE-19-MISSING-SKILL-SOURCE-GAP-AUDIT-R1.json)归档逐个未定义技能ID、原模板行、槽位、原图数值、来源数据ID、必要的源字段SHA、跨表候选技能原行及SHA与明确负证。

```bash
python tools/stoneage_pet16_lookup.py --skill-gaps
python tools/stoneage_pet16_lookup.py --skill-gaps --skill-id 114 --limit 5
python tools/stoneage_pet16_lookup.py --skill-gaps --skill-id 503
python tools/stoneage_pet16_lookup.py --summary
python -m unittest tests.test_stoneage_pet16_unified_catalog tests.test_stoneage_pet17_graphic_traces tests.test_stoneage_pet18_capture_skill_links tests.test_stoneage_pet19_skill_gap_audit
```

`--limit` 只限制每技能显示的原行，**总引用次数永远保持完整**；`--skill-id` 未命中就分来源返回空，不凭数字碰撞造技能定义。回归从PET03原候选、PET10原行索引、PET16统一目录重新计算114条缺源引用，不依赖仅手写统计。外部已核备用表完整 Git blob 加上56个原ID记录于派生审计，供将来有能力重核原字节时再验证。

## 未完成、重开条件及下一个PET工作包

- 2016源：真正满足同一构建与配置的**新增技能主档、源handler与可核编译运行**才可升级缺定义或原效果。目前后期社区源码不能倒填1999 JSS、台湾1.0或大陆1.82。
- mixed25源：只有可证活动配置与原配套技能表/handler才可将跨表候选升级为同部署技能定义；当前**保留SOURCE_CONFLICT**。无新证据则缺源项持续OPEN。
- 所有已记录技能数值、原技能短名、原成长字段并不等于原生效果、学习等级、施放条件或成长公式已验证；不杜撰效果与原本图鉴分类。
- 原档 `docs/CURRENT-STATE.md` git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 未修改；PET16七原缺口不关闭；Stage A **7 PARTIAL + 2 OPEN**，Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，整体百分比 **UNKNOWN**。
- **下一任务 PET20（继续宠物）**：有限核查现存同源成长/属性列的数值字面与源码定义，再检查原宠物行为如捕捉/赠送/骑乘/进化的来源凭据覆盖；没有真正可核原件则界定来源止点，不扩泛化技能或跨模块临时任务。

GitHub Actions 的初次失败、修正、成功及正式main验收应以**对应精确SHA**实际日志判定，本报告自身不提前宣称已经通过。


## 2026-11-15 前向PET20整模块覆盖与结项锁

[PET20七维真实来源覆盖和明确结项门槛](STONEAGE-PET-MODULE-20-WHOLE-MODULE-ACCEPTANCE-BOUNDARY-20261115.md)是本单一PET模块的统一来源覆盖审阅，机器矩阵逐原Git blob审验，保留PET01–19旧收据及本文件源技能缺口。这里所列早期 `下一任务PET20` 已由实际PET20结果前向接续为 **PET21具名官方网页原图批量来源审查**，未解后期源索引及原版未验证行为继续OPEN。PET仍ACTIVE、SOURCE_BOUNDED_PARTIAL，不能据统计数字宣告完成或切换模块。
