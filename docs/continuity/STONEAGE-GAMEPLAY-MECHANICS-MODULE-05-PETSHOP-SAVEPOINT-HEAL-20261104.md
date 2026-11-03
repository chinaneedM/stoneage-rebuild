# GAMEPLAY05｜宠物店寄放、记录点与治疗配置的源文件批量复原（2026-11-04）

**范围：** Stage A原版历史复原。原件属**社区保存混合2.5载体**，不是经认证的日本JSS1999、台湾1.0或大陆1.82同部署原服务端。承接GAMEPLAY04已合并主线 `7d6daedef32155c4bff75b055d8db9afde4d159c`。历史 `docs/CURRENT-STATE.md` 的原Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 不变。

## 实际原件及取证

私人已保存的 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip` 995,176B/SHA-256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f` 中，有2205份原NPC成员/1,930,332B；沿用已在GAMEPLAY02验证的原文件全SHA/CRC源登记。**本轮真正重新读取并校验**本批涉及的原CREATE原字节切片及38份原参数实物，逐个SHA、大小及CRC和CHAR01公开源库存一致；父361MB RAR本轮**未重新取回或解压**。这不把旧全ZIP验收计算成新的原历史发现。

本批从保存原始CREATE中连续审查以下**77个原配置块，而非77个不同NPC或实际运行服务**：

| 源函数 | 原CREATE块 | 可定位外部原参数 |
|---|---:|---:|
| `npcgen_petshop` 宠物店 | 16 | 16份，合计4,655B |
| `npcgen_savepoint` 记录点 | 22 | 22份，合计8,052B |
| `npcgen_winhealer` 医疗配置 | 27 | 无额外file，4字段内联 |
| `npcgen_healer` | 4 | 无额外file，内联 |
| `npcgen_fmhealer` | 4 | 无额外file，内联 |
| `npcgen_charm` | 4 | 无额外file，内联 |

38份源参数合计12,707B。原路径、原创建块SHA及各成员完整SHA/CRC和用于可核的有限数字字段已保存到[GAMEPLAY05公开来源限定目录](../../research/recovered/STONEAGE-GAMEPLAY05-ORIGINAL-PETSHOP-SAVEPOINT-HEAL-SOURCE-R1.json)。**无原脚本对白、美术或原商用程序入Git**。

## 一、16份原宠物店费用/寄放参数

源字段拼写保留原样 `nomal_rate`（不可擅自改成`normal_rate`）：其字面数字 `1.0` 出现13次、`0.6` 2次、`0.7` 1次。`pool_flg`只有6份有字面配置；`pool_cost`这6份分别为原整数200×5、2000×1，另10份**本来没有该字段**，不能当作0；`special_rate=1.5`有14份，其余2份无字段；14份 `special_pet` 存在但原值为空，应保留源空值而不补上物种。所谓费率、寄放等是**源脚本参数事实**，非实际账户石币扣费、宠物存取、特殊宠物验证或原服成交。

## 二、22份原记录点及物品候选

22份记录点原配置各有一条源`ID`和`Born`坐标三元组，**实际22种源ID**；21份存在 `GetItem` 字段，1份没有（并非字段值0）。原输入给出209个物品选择词槽、116个不同的纯数字物品候选ID。精确原源异常两处：`genout/sp_200_449_982` 有一段 `1991*` 数量不完整；`poru/sp_5500_35_19` 使用6个单独物品ID而不是数字×数量表达式，均原样保留，**不进行自动修复或误报实际执行失败**。

使用此前ITEM01已公开**两套原itemset差异索引**逐一复核116个物品数字：110个在两套表各有原行，只有编号1732–1737的6个**仅存在于后一套备用物品主表**，无在两表均缺失的ID。这只是同保存包派生数值对照：**无法由此选定当时真正启用哪一套物品表，不能宣称记录点物品已扣除、出生点生效或重登录位置已被真实游戏验证。** 台湾1.0早期官方记录点与其同服关系保持UNKNOWN。

## 三、医疗NPC的原参数形式

27条`npcgen_winhealer`原CREATE块的4个内联参数存在14种不同字面组合；其余12条`healer/fmhealer/charm`则是单字段或空参数的其他源函数。这里记录的是**真实原配置的参数形状**，不是“14种治愈技能”、血/气/金钱计算规则或已经启动的医疗NPC。缺少原生同版本服务端与实际回包，仍属SOURCE_BOUNDED_PARTIAL。

## 证据级别、验收和交接

公开`tests/test_stoneage_gameplay_mechanics_module_05.py`逐项对照原CHAR01创建块SHA/同原载体文件SHA+CRC、116个物品ID在两源表的精确存在关系与所有未证运行边界；加入既有GAMEPLAY01–04专项工作流，不增加重复工具或新报告体系。**公开CI只有源派生索引验证，不能替代私人原字节重新读盘或原游戏执行**；私人原文件仅在研究环境保管。

**最高NEXT：`GAMEPLAY-MECHANICS-MODULE-06`。** 继续源准备就绪的原捕捉/其他原UI与声效玩法机制，优先以现存源证产生实际机制归属或有界止点；若无可验原运行规则，不扩抽象框架，按模块计划进入历史整合。Stage A仍7 PARTIAL + 2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，总体完成率 `null`，未开始新石器开发。