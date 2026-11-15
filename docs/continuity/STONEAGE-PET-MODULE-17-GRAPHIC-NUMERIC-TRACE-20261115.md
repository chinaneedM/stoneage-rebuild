# PET17｜宠物图鉴多来源图号精确追溯（2026-11-15）

**活动内容模块仅 PET；本批不是结项，不开启 NPC/MAP/ITEM 轮换。**

## 交付与意义

沿用 PET16 唯一数据入口 `research/recovered/STONEAGE-PET-MODULE-16-SOURCE-SEPARATED-UNIFIED-CATALOG-R1.json`（原 Git blob `fdb7d9aade2df62d1a1e06b2d2f9e383693ed980`），不复制第二份大表。原 `tools/stoneage_pet16_lookup.py` 增加：

- `--details`：返回某一原源记录完整的原字段、原行 SHA、技能槽、2D SPR 帧/动作统计、来源与 UNKNOWN，而不仅是简表；
- `--trace-graphic 原图号`：同一数字在 **2016 后期社区模板、2016 候选图号、mixed25 原主表、mixed25 备表、台湾1.0原零售 SPR** 五个命名空间分别列出；提供每一来源的真实命中数、受限输出、是否截断以及原记录；
- 日方 Hangame / 华义官方网站的网页顺序号、原图片 URL **不得充作客户端原图号或宠物 ID**。官方网页具名资料仍可经 `--dataset` 单独搜索。

检索同号关系等级是 `LITERAL_GRAPHIC_NUMBER_COINCIDENCE_ONLY`。不标记跨源同种、同服、TW1 官方宠物姓名、实际捕捉/技能执行。没有读出新的原始商业像素、没有运行原生客户端，也没有取得新增官方源。

## PET16 实际全数据交叉统计

以下是直接对已经归档的 2,792 条来源记录作精确数字查询，不是宠物种数：

| 数据来源 | 与131个台湾1.0已有SPR组同图号的原记录数 | 命中的不同图号数 |
| --- | ---: | ---: |
| 后期2016宠物模板 | 201 | 130 |
| 后期2016候选图号列表 | 130 | 130 |
| mixed25 主表 PETFLG1 | 188 | 130 |
| mixed25 备表 PETFLG1 | 144 | 125 |

- 台湾1.0的 **131个原SPR候选组**中有 **1组 `100400`** 在2016模板与 mixed25 主表找不到同数字，但备表有2条。不能补出主表记录，也不能宣称这组无宠物。
- **44个**台湾1.0 SPR 图号在2016模板中命中多于一条记录；mixed25主表为**41个**，备表为**16个**。图号与“宠物实体／名字”明显不是可靠的一对一键。
- 旧 PET13 的 **10条** mixed25 主表名字经过原行、模板ID、图号和字段 SHA 的同源验证。其中仅**1条**（`卡特利奴`，模板524，图号100329）与当前131个台湾1.0 SPR 组发生**数字重合**；这既不能确定 TW1 的该宠物姓名，也不能说明2001/1999官方服同部署。其余9条的具名事实仍只属于其原社区载体及 PET13 来源范围。
- 具体反例 **100329**：2016模板4条（163、193、524、20002），mixed25主表4条（163、193、524、1214），备表2条（193、524），TW1原SPR组1条。若只凭图号，把这一幅画与所有数值、名字绑定成一个官方宠物，将错误合并多条不同模板；`卡特利奴`仅属于 mixed25 主表原模板524的已校验名字。
- 另一反例 **101737**：mixed25主表具名 `薩德迪比`，但没有131组内的 TW1 已验证动作组；不能以网页名或另版图号伪补原像。

## 可复用命令

```bash
python tools/stoneage_pet16_lookup.py --summary
python tools/stoneage_pet16_lookup.py --trace-graphic 100329 --limit 20
python tools/stoneage_pet16_lookup.py --trace-graphic 100400
python tools/stoneage_pet16_lookup.py --dataset mixed25_main --query 卡特利奴 --details
python tools/stoneage_pet16_lookup.py --dataset jp_official_web --query ウーリ --details
python -m unittest tests.test_stoneage_pet16_unified_catalog tests.test_stoneage_pet17_graphic_traces
```

受限 `--limit` 只限制每来源显示的原行数，原命中总数照常披露。测试覆盖多记录碰撞、主备表互斥、真实台湾1.0动作段哈希与104动作方向段、零命中、不合法图号、官网名称不得自动反向赋ID。

## 验收边界与后续

- 原PET16七个覆盖缺口 `PET16-01..07` 全部保留 OPEN／PARTIAL／UNKNOWN；本批新增的是**有界、可复用的检索与反例验证**，不是发现了历史同种映射。
- 来源资格：PET16数据 `fdb7d9aa...`、原PET15 `e1cac698...`、PET13 `83525147...`；旧 GETPET 36实例 `4c834aa7...` 仅作为宠物获取线索，不并作模板ID或已知捕捉事实。
- 原商业美术、官方网页图片及私人重放包均不入公开Git；不推导原配色、帧时序、原游戏运行或可商用许可。
- 本轮应由精确候选HEAD/正式main Actions **实际完成成功后**才记录通过；不能把提交或工作流定义视为CI成功。
- 未改历史 `docs/CURRENT-STATE.md`，保留原 blob `c89e0e33537990aa2132b47c40fef49a985a935c`。Stage A **7 PARTIAL + 2 OPEN**，Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，总体完成率 **UNKNOWN**。

**下一项仍只能 PET18**：从已保存宠物技能、成长/级别、原捕捉和 GETPET 资料逐个来源建立可查询的技能—模板—实例及获取路径字段关系；同源可证边才接、缺早期官方主档则标 MISSING_SOURCE，绝不因为资料暂缺就退出宠物模块。
