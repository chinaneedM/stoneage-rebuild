# INTEGRATION14｜霍特爾两家商店与七条备表物品原行

从 GitHub main `701a86a21793f3dc963f1bf0cb72486906903ea8` / tree `c68ad8b7d14ed1195dcce003783d7d785c92631c` 续接。起点 933 个远端分支、7,554 个文件、零开放 PR，同 HEAD [专项 Actions](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42562428582) 成功。完整 CURRENT 历史 2,709,173 B，Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`，按既有日期续接方式保留。上一轮仅做过范围、编号和台湾后期压缩块索引的预查。本轮复核物理行、原字段关系、原参数引用和替代图像载体。

## 两处商人的字段和位置

再次核验 361,255,180 B 的社区混合 2.5 原 RAR 整体 SHA、7,952 个原文件标头 CRC，实际提取九个目标成员并核大小/CRC。两份完整物品表、两份 CREATE、共享模板、两份参数与 setup 的原 SHA 均对既存记录。附带读取的 708 B `Palet_1.sap` 另与大陆 5.0 MSI 原路径目录核同。

| 原 CREATE 地图和坐标 | 原字段 | 展开编号数 | 主表有行 | 备表有行 | 两表原行完全同字节 |
|---|---|---:|---:|---:|---:|
| 1305 医院商人 (17,18) | ItemList | 12 | 12 | 12 | 12 |
| 1305 医院商人 (17,18) | LimitItemNo | 51 | 44 | 51 | 44 |
| 1305 医院商人 (17,18) | special_item | 0 | 0 | 0 | 0 |
| 1310 营养剂名人家商人 (16,16) | ItemList | 16 | 0 | 16 | 0 |
| 1310 营养剂名人家商人 (16,16) | LimitItemNo | 21 | 0 | 21 | 0 |
| 1310 营养剂名人家商人 (16,16) | special_item | 5 | 0 | 5 | 0 |

医院这条 ItemShop 独立于同房 WindowHealer。1310 原参数文件名后缀为 `18_15`，原出生格以 CREATE 的 `(16,16)` 为准。七个目标号都只在医院的 `LimitItemNo` 出现。1508、1509 在 1310 三个字段均无引用，1546–1550 同时见于 1310 的 `ItemList` 和 `LimitItemNo`，均不在其 `special_item`。两家原倍率字符串另存，未按倍率计算成交价。setup 四个 `itemset3file` 至 `itemset6file` 字面都指向 `data/itemset.txt`；实际运行选择、物品取得和买卖待证。

## 七个模板与六个图号

完整备表行的原行号、字节偏移、行 SHA、原图字段和数值字段均进入[公开派生记录](../../research/recovered/STONEAGE-INTEGRATION14-HOTORU-SHOP-ITEM-SOURCE-R1.json)。1508/1509 是两条不同原行，共用图号 24095，`cost` 字面分别为 12000 和 13000，参数文字也不同。后五条图号各异，`cost` 字面均为 10。七条的 `magicid` 原栏为空，派生用 null 保留。原名、原效果描述和原参数留在私人观察包。

图号 24095 复用已经核验的 ITEM01 台湾 1.0 原候选 PNG。对另五个图号，按压缩 RD 块 SHA 扫描完整大陆 5.0 目录，每个在该目录唯一命中，分别位于 300861、300866、300881、300901、300903。各块与 ITEM07/08 所引用的声称台湾 8.5 后期载体 RD 指纹逐一相同。2006-09-11 官方补丁提供对应 ADRN 索引，RD 像素来源与其分列。

独立来源尝试 [42563744027](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42563744027) 已取得原 CAB 全 SHA 和两份资源整 SHA，随后因误把目录属性摘要当成整条 ADRN 记录摘要而停止。根据原目录生成代码校正属性跨度为 `[28:80]`，完整 80 B 摘要另列。修正后 [42564298848](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42564298848) 遇档案站 500，再次对失败区间加入有限重试。当前静态候选派生保留五个目录命中，像素读取和验收结果待来源重试及本地核对。

## 下一项

**NEXT INTEGRATION15** 优先复用 1303 宠物店已验地图和两处服务配置。先排除 GAMEPLAY03/05 已有的参数重复研究，再把宠物技能导师和收宠服务接到室内观察。WORLD11 有 16048、16049 的已验台湾 1.0 静态图候选；16049 也被同室 TownPeople 引用，按原块与坐标分别保留。只在取得原图或能增加可查现场关系时交付。Stage A 为 7 PARTIAL + 2 OPEN，Stage B/wiki GATED，R79 暂停，整体完成百分比未知。
