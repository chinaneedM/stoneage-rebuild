# PET126B｜官方经典 PC 宠物发行文献专用查询与历史网页零误合并

日期：2026-11-20。基线主线 HEAD `cfee75061886f195ccda9314aa485c3d7ff047e2`，tree `658614437c87142b5edf683d6e8060ee148666d6`。唯一活动模块 **PET**；年份仍 **2026 `NOT_YEAR_AUDITED`**，本任务**不是 2026 年结，也不是宠物模块终审**。

## 为何不是再建一个宠物目录

已有 [PET16 技术/来源目录](../../research/recovered/STONEAGE-PET-MODULE-16-SOURCE-SEPARATED-UNIFIED-CATALOG-R1.json) 的 2,792 条是 **7 个来源域的行、图形、官网位置候选**；普通查询按来源分开，但未提供专门查找“已有官方旧 PC 实际发行文献事件”的模式。直接显示 2,792 为“官方宠物数量”是错误的。现有 [PET25 官方中国经典 PC 发行收据](../../research/recovered/STONEAGE-PET25-OFFICIAL-RELEASE-ROSTER-R1.json)与[PET26 日本经典 PC 收据](../../research/recovered/STONEAGE-PET26-JP-TW-CLASSIC-OFFICIAL-RELEASE-R1.json)已经独立保存；不重复抓取或转录为新物种。

本次直接复用原 [`stoneage_pet16_lookup.py`](../../tools/stoneage_pet16_lookup.py)，增加独立 `--official-releases` 模式：**只从原 PET25+PET26 JSON 实时组合**，不先加载 2.7MB 社区/图像索引；返回原文命名、来源版本、地区、发行文献记录 ID、来源 URL、来源层级和可证日期的独立字段。不得把文献时间称为全球首次上服时间，也不把官方页面位置或原客户端资源图号当宠物身份证。

## 实际可查询的九项文献事件（不是九只宠物）

| 归属 | 文献 ID | 已记名称/类型 | 可确定范围 |
| --- | --- | --- | --- |
| 中国 2002 | `CN-PC-3-YEAR` | 年兽，家族/卡组级 | 3.0 华义历史发行文献，未细拆四属性 |
| 中国 2002 | `CN-PC-3-GP` | GP宠物，家族/卡组级 | 3.0 来源记载，不是一只独立命名宠物 |
| 中国 2002 | `CN-PC-4-MECHLEOPARD` | 艾迪希洛，具名 | 4.0 时期资料，不证明原客户端图号 |
| 中国 2002 | `CN-PC-4-DRAGONBOAT` | 端午兽，家族/卡组级 | 4.0 文献；不能推导独立颜色物种 |
| 中国 2003 | `CN-PC-MONKEY-2003` | 蒙奇，具名 | 大陆历史活动文献；不跨区合并 |
| 日本 2006 | `JP-2006-TWO-MYSTERY` | 两只未具名宠的一**条**发行事件 | 不能当两条命名物种身份 |
| 日本 2008 | `JP-2008-FUKUURI` | フクゥーリ，具名 | 日本官方来源复制文献 |
| 日本 2009 | `JP-2009-HAKUEN` | ハクエン，具名 | 日本官方来源复制文献 |
| 日本 2009 | `JP-2009-KOKUEN` | コクエン，具名 | 日本官方来源复制文献 |

共有 **9 条文献事件**：**5 条具名**、**3 条家族/卡组级**、**1 条双未具名的单事件**。官方 PC 跨地区唯一宠物物种总数仍 `null`，原服务器 PET ID、成长、技能、Sprite-宠物身份连接均未在本任务获得。

## 严格的“早期官网名字”负向交叉测试

资料源是 [2001 年大陆华义旧官网 104 条位置（98 可读名、6 占位）](../../research/recovered/STONEAGE-WAEI-CN20-NEW-PET-FINITE-CATALOG-R1.json)和[2003–2004 年日本 Hangame 124 条位置](../../research/recovered/STONEAGE-JP-OFFICIAL-PET-CATALOG-R1.json)。此次逐条用同地区**字面全等**比对上述9条发行事件命名，得到：

- 中国 5 条文献事件在早期 104 位置中的**原字完全相同命中 0**；不同年份后发内容不能倒填进2001图鉴。
- 日本 4 条事件在早期124个位置中的**原字完全相同命中 0**；2006、2008、2009发行事件不能用2003页面位置补造身份。
- 0 命中仅说明**这两个既定早期网页样本中没有原字全等**；不是证明该宠物历史上不存在，也不能据此否定日后独立同名、更名或同构建原服真实实装。即使命中也只能是“同名待核”，不是同宠物/同图号的证据。

此结果是从仓库已有四份原始衍生收据完成新的明确对照，未取回或发布任何商业原图。2023、2003 年“菲奇亚/朱雀”和 7.0 当时 `StoneAge7.rar` 原分发路径在 [PET66](STONEAGE-PET66-2003-TW6-CN7-PET-SOURCE-20261116.md)及早前规格已归档，本轮查重后**不重复登记为新发行宠物或新取得客户端**。

## 使用（只需 Python 标准库）

```bash
python tools/stoneage_pet16_lookup.py --official-releases --summary
python tools/stoneage_pet16_lookup.py --official-releases --query 年兽
python tools/stoneage_pet16_lookup.py --official-releases --release-region JP --query ハクエン
python tools/stoneage_pet16_lookup.py --official-releases --release-web-name-check
```

所有原原记录还可以使用旧 `--dataset`、`--trace-graphic`、`--capture-template`、`--skill-gaps`、`--operator-web` 各自的**来源专属**查询功能；`--official-releases` 不与这些模式混用。新回归测试验证原始总数、分类、每条 source URL、年份不作为首次发行、9 条 web 零误合并、CLI 模式排斥、以及历史 `docs/CURRENT-STATE.md` 大 blob 不变。

## 缺口、止点与 NEXT

这一工作**没有新获取**认证原经典 PC 安装包、补丁、PET主档、原SPR动作、原技能运行或原服奖励事件；本轮物种实证增量 **0**，不是“没发现宠就等于历史没有”。2026六区仍处于来源前沿，按 PET126 原六区重开门继续。 

PET126B 的查询功能交付后，PET126C 应优先检验：是否真正有**合法、免费、可取得原字节**的经典 PC 客户端／补丁，若无，则对已在源仓的真实可核官方PC宠物资料推进**同构建名称—图像—实际获得**的证据连接；不再重复列举旧网页/卖盘路径。未达到 PET19–20 七维最终验收、原件处理与用户接受的有界停止前，PET仍 `SOURCE_BOUNDED_PARTIAL`，**不可转NPC、Stage B或攻略网站**。Stage A 7 PARTIAL+2 OPEN，R79暂停，总百分比 UNKNOWN。

历史 `docs/CURRENT-STATE.md` Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`，2,709,173字节，严格保留；版权图片/源程序不得公开。
