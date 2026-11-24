# 台湾7.5声称原服主档：来源限定宠物字段目录

## 来源及分级

2012-02-06编辑的玩家ludaxx研究文章（[原帖](https://forum.gamer.com.tw/C.php?bsn=1571&snA=65960)）明确提供自称华义7.5版 enemybase1.txt 的公开下载链接。2026-11-24源作业实际两次获取同一完整143465字节CP950文本，SHA256 1b2e9fb0f8889dc857e80b8b8e7bdb5e2372e52b0789df336b601609e29af832，Git blob 4e4da03e5d40368e9631eefb8b98ed489e789cb1。原始文件在作业临时目录读取，未将原文件上传公开仓库；没有证据证明官服部署、未经改动或首发时间。此为声称原版的公开保存样本，不是确证官方主档。

- [首次实读来源回执](../../research/pets/PET-HIGH-FIRST-15-CLAIMED-TW75-MASTER-PROBE-R1.json) · [源作业](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/45371792664)
- [全字段投影](../../research/pets/PET-HIGH-FIRST-15-TW75-MASTER-FIELD-CATALOG-R1.json) · [源作业](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/45372040686)

## 统计

| 范围 | 数量 |
|---|---:|
| 56列模板记录（唯一原ID） | 960 |
| PETFLG=1字段投影 | 467 |
| PETFLG=0（不列入宠物候选） | 493 |
| PETFLG=1不同原名 | 438 |
| 与后期保存Gavin数据同ID且非名称/素材50列完全一致（全表） | 917 |
| 同ID但50列不同（全表） | 28 |
| 对照表无同ID（全表） | 15 |
| 宠物模板中50列完全一致 | 429 |

Gavin对照为1816条GB18030后期社区保存记录，固定提交1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56，原SHA 7ffb17b161c9d66fcbbaa4e8bcf48d1a9a56223b35770074ae9c3401d270f5d7。强关联说明数据传承或共同祖源的可能性，不是独立官服背书；同名异模板分别保留。

| PETFLG=1客户端名称/图号关系 | 数量 |
|---|---:|
| 台湾1.0同名同图号 | 139 |
| 台湾8.5额外图号的原程序同名路由 | 104 |
| 台湾8.5只证同名相簿 | 179 |
| 台湾1.0图号为其他名 | 16 |
| 台湾8.5图号为其他名 | 14 |
| 尚无合格关联 | 15 |

同名同图号不是同服身份、实发或成长公式的证明。旧台湾1.0档案及高版独立来源原样保存。原始四维成长档顺序体力/腕力/耐力/速度，元素顺序地/水/火/风（原始单位），数值是配置字段，不是一级面板和实测成长率。

## 查询

公开JSON逐行保留原名、原ID、行号、行SHA、初始系数、成长档、野生系数原字符串、元素、技能槽及图号、同源对照状态及不同客户端原名。可用 Python 按原繁体姓名查询，例如：

```python
import json
from pathlib import Path
p = Path("research/pets/PET-HIGH-FIRST-15-TW75-MASTER-FIELD-CATALOG-R1.json")
data = json.loads(p.read_text(encoding="utf-8"))
for row in data["pet_flag_1_field_projections"]:
    if "烏力" in row["name"]:
        print(row["template_id"], row["name"], row["initnum"], row["base"], row["elements"])
```

后续先审原表字段意义、来源谱系、同名异档及冲突，再用已有后期源码模型计算明确标记为候选的一级属性和成长区间，独立寻同期官服投放及技能表。不得把438个名字、467条模板或243条客户端同名同图号关系宣告为官方实发数。PET唯一，完全验收数仍0。
