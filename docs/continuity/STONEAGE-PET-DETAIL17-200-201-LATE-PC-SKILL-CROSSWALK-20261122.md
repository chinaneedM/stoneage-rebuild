# PET-DETAIL17｜原台湾1.0客户端技能数字200／201与后期PC社区技能表的候选对应

2026-11-22 · 唯一内容模块：PET · 仅经典2D PC《石器时代》。本批**没有恢复原台湾1.0服务器的技能主档／出生配招**；这是三个后期社区PC原文本表与PET-DETAIL16原客户端数字引用的**分轨比较**。

## 直接读到的新证据（固定提交、文件、原行）

| 来源 | Git提交 | 原文件Blob | 技能200 | 技能201 | 数字列 |
| --- | --- | --- | --- | --- | --- |
| [社区PC库A / `petskill.txt`](https://github.com/chenmingbiao/stone-age/blob/0c58fb6683a49a178a8ad845a8c296c2cb83bd81/gmsv/data/petskill.txt#L29-L30) | `0c58fb6` | `4c0dff7b40dc60077db61bf61faf408079ec25d0` | 第29行：加工 | 第30行：料理 | 第7列（0起算6） |
| [社区PC库B / `petskill.txt`](https://github.com/pimpcapital/longzoro-sa/blob/57b14e2bb373ba851c14db28a239273e4a8831bb/gmsv/data/petskill.txt#L29-L30) | `57b14e2` | `846d379f0c7977b3e74d5a5a9580a35a85cafc51` | 第29行：加工 | 第30行：料理 | 第5列（0起算4） |
| [同社区PC库B / `petskill2.txt`](https://github.com/pimpcapital/longzoro-sa/blob/57b14e2bb373ba851c14db28a239273e4a8831bb/gmsv/data/petskill2.txt#L36-L37) | `57b14e2` | `83d2daeb9e57b089a304f127361f88514386b870` | 第36行：加工 | 第37行：料理 | 第7列（0起算6） |

以上三文件**本轮重新读取真实Git内容**，逐个校验完整Blob SHA及精确行号、CSV字段位置。两份12列、一份9列：按错误的固定列号解析会读成其他数字或空字段。三文件中的两个ID均引用 `PETSKILL_Merge` 处理符号，200是 `PETSKILL_MERGE`，201是 `PETSKILL_MERGE2`；保存的`field/context`数字为2、`target`数字为0。这仅是后期数据在其自身代码体系下的字段内容，不能把后期数字2直接解释为台湾1.0原服特殊技能机制。

**去重提醒：**三份表只有两个Git仓库，且文字、ID与符号高度一致，`petskill.txt`及`petskill2.txt`也出自同一提交。这些可能有共同的旧源或复制链，**不能按“三个独立证人”计数**；两个仓库的Git提交时间也不等于1999–2001官方原始发行时间。

## 与真正早期原PC可执行文件对接的界限

[PET-DETAIL16原始TW1客户端反汇编收据](../../research/pets/PET-DETAIL-EVIDENCE16-TW10-NATIVE-BATTLE-SKILL-ID-AND-TARGET-R1.json)经原件校验，原始`sa_3.exe`在`0x42A85F`查询数字**201**，在`0x42A888`查询数字**200**；该函数查找**已接收的宠物个体技能ID**。这与后期社区表的两个数值构成**有价值的候选数值对应**，也不能排除后期社区沿用了更早的编号惯例。

但仍缺一条关键的**同代、同服、同构建、可验证的技能ID→原名称**连接：原EXE局部硬编码数字并不包含对这两个ID的完整官方命名/技能说明，本轮也没有实际读取私人原EXE、取得当年的官方服务端PetSkill主表、原生`W`发包或真实出生截图。故原台湾1.0的 `200`、`201` **名称/效果维持`null`**，不可改写成“已证明台湾1.0的200=加工、201=料理”；不要通过名字把布伊、石龟或所有124条原相簿候选自动赋予技能。

此前[PET-DETAIL15早期玩家资料](STONEAGE-PET-DETAIL15-SIX-EARLY-PC-SKILL-CLAIM-CROSSWALK-20261122.md)可证“加工”作为文字技能说法出现在迁移版2001玩家页面、2004技能学习指南，但两者没有原版官方技能数值ID、同部署出生实例；玩家“有加工”不等于“出生有加工”。该文字只能给后期名称作为时代背景，不能填补数字跨版同一性的原证缺口。

## 验收/断言及下一步

新机器收据：[PET-DETAIL17三表×两行限定的逐来源字段及认证边界](../../research/pets/PET-DETAIL-EVIDENCE17-200-201-LATE-PC-SKILL-CANDIDATE-BOUNDARY-R1.json)。已存的PET-DETAIL16原原件收据与PET-DETAIL15玩家技能文献的Git Blob作为固定输入；新增的为**后期社区数据候选**，不是早期官网新史料。原历史`docs/CURRENT-STATE.md` Blob `c89e0e33537990aa2132b47c40fef49a985a935c`必须保留。台湾1.0原客户端具名候选124条、逐项部分档案124、全字段史证完成0；本批新增原官服技能主档0、同年代技能名字匹配0、实发物种0，Stage A 7PARTIAL＋2OPEN，Stage B／攻略网站GATED，R79暂停，总体完成率UNKNOWN。

**NEXT PET-DETAIL18：**优先追查早期日本JSS、台湾1.0或大陆1.82正式PC**同构建**PetSkill定义、`W`原生封包、官方技能ID/原名对照或原版实装截图；若免费可合法取得的材料不存在，记录具体缺口后转为复用已验证原客户端的有限实际发现，不反复抓取同一后期社区表，也不切换NPC/装备/地图或启动新游戏开发。
