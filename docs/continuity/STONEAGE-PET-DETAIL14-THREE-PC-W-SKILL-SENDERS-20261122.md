# PET-DETAIL14｜经典PC三套后期社区服务端W技能发送源码对照台湾1.0接收结构

日期：2026-11-22。仅经典2D PC、活动模块PET。本次审查的是三份固定提交的**服务端源代码**，不是原1999—2002年台湾1.0官服同部署服务端，也没有登录或抓取原服封包。

## 直接审阅的三份固定原C代码与定义头

| 代码存档 | Git提交 | 原C文件Git blob | 常量头Git blob |
|---|---|---|---|
| [2012公开保存：librae8226/gmsv](https://github.com/librae8226/gmsv/tree/49928c291c6789013cba56d7c07d389f87cdfb0c) | `49928c291c67…` | `d1028cf7fe89…` | `1f5a5154b23e…` |
| [2016保存社区2.5：chenmingbiao/stone-age](https://github.com/chenmingbiao/stone-age/tree/0c58fb6683a49a178a8ad845a8c296c2cb83bd81) | `0c58fb6683a4…` | `54defb74e0ec…` | `6989d3984506…` |
| [2016后期PC：pimpcapital/longzoro-sa](https://github.com/pimpcapital/longzoro-sa/tree/57b14e2bb373ba851c14db28a239273e4a8831bb) | `57b14e2bb373…` | `5a044dc68bb7…` | `70e340b39731…` |

均实际检查了 `char.c` 的 `CHAR_makeStatusString` 中正常 `case 'w'` 分支，以及同提交 `char_base.h`。三个头文件均给出 `CHAR_MAXPETHAVE=5` 和 `CHAR_MAXPETSKILLHAVE=7`。三套默认发送过程均写 `W%d|` 前缀，然后按**7条技能×5字段，共35个字段**发送。可核文件路径、完整commit和blob SHA在[机器收据](../../research/pets/PET-DETAIL-EVIDENCE14-THREE-PC-W-SKILL-SENDER-LINEAGES-R1.json)中。

## 新确认的数据生成方式

1. `CHAR_getCharPet(index,num)` 从人物指定携带栏取**宠物实例**，不是直接根据相簿图号决定一套物种固定技能。
2. `CHAR_getPetSkill(pindex,petskillloop)` 依次获取该宠物实例当前技能槽的ID，再用 `PETSKILL_getPetskillArray(skillid)` 查对应技能定义。
3. 有效技能：输出三个数值 `PETSKILL_ID / PETSKILL_FIELD / PETSKILL_TARGET` 和两个经转义的文字 `PETSKILL_NAME / PETSKILL_COMMENT`。
4. 没有有效定义时发送五个空字段 `|||||`，保留后续槽位的位置。发送源中有逻辑分支，但其实际游戏运行未做联机验收。

**关键结论：**这三套后期服务器都从*个体已经存储的技能槽*构造 `W` 报文。**技能定义表有某ID不等于某个物种出生自带该技能**，更不能把社区服务端的技能ID填作台湾1.0官方唯一技能ID。

## 台湾1.0原PC与后期W发送器的边界

PET-DETAIL13已从真实台湾1.0原 `sa_3.exe` 得到 `0x430B4F` 的 `W` 接收处理、7行×106字节技能缓存和 `K` 技能栏容量对资料界面的限制。这次后期三源正常W发送在**五字段顺序和七个槽位数**上与早期独立证据相符，但只证明**静态消息形状同型**。后期三源在有效技能查找/空技能输出的实现不自动归属于原TW1服。

更重要：PET-DETAIL11已证明三份后期PC服务器的 `K` 报文在token20发送 `TRANSMIGRATION` 数值，台湾1.0客户端同期位置期待原宠物姓名。**不能从W形状相似得出整套客户端/服务端可直接连接、官方部署同源或技能/出生数值相同。** 2012公开代码的日期也不能证明该代码来自1999—2002官方服务器。后期可选 `y/o/a` 宏分支没有纳入本次默认W审计。

## 现有早期文字对照，不重复计新史料

[2001年玩家抓宠记录](../pets/CN2001-LV1-20-PLAYER-NUMERIC-RANGES.md)已经收录暴龙一级必杀、布伊加工、石龟石化的玩家说法，存在“有技能”未说明是天生还是学习获得的证据缺口。17173旧[宠物技能指南](https://news.17173.com/z/stoneage/chongwu/pet03.htm)汇集技能名称、费用、训练地点，却无可信逐版本发布时点并混有后期技能；因此不作为初代台湾1.0技能名录。此处不是新的独立宠物出生技能实证。

**PET-DETAIL14结果：**三份源级 `W` 技能发包例程结构同型；新增官方原版技能主表0、出生技能0、原始实测W包0、官方新实发宠物0。台湾1.0原客户端124份候选档案仍PARTIAL、历史验收完整0。保留原 `docs/CURRENT-STATE.md` blob `c89e0e33537990aa2132b47c40fef49a985a935c`；Stage A 7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，总完成率UNKNOWN。

**NEXT PET-DETAIL15：**仍以免费合法、可鉴真原PC早期同服技能/学习/宠物主档为先；确无原件时继续按PET维度查真实历史证据，不填造台湾1.0技能ID、不切换其他模块。
