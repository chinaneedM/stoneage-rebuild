# R45 六条原技能名称、数值与既有复原模型的关联

2026-10-27（Asia/Shanghai）。本包限定恢复一张已知保存技能表的前6条显示名称/声明字段，连接到已有复原模型，停止于6条，不穷举所有技能helper。旧研究早已保存147行/69回调、六字符串前缀/五整数及后代运行模型；这些旧数量不是本轮首次发现。新增内容是原名称→原ID/回调/字段→既有模型的可查来源链。

## 两件真实原文件与两种解码器

来源仍是社区混合2.5保存包，未认证为官方初代、纯净发行或同部署客户端/服务器。只取原`gmsv/setup.cf`9715B/SHA `b4936c103efb7b3cad359e5c85c7965187306883a68c0be712ece6c374e3b12d` 和`gmsv/data/petskill.txt`15112B/SHA `f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4`，完整SHA/CRC与旧索引吻合。配置`petskillfile1`和`petskillfile2`均原写`./data/petskill.txt`，不凭编译宏任选不同表。

每次184个严格HTTP206范围，共12013836B，未重下361MB整包，也没重算全包/分卷SHA。两个原成员各由unar和libarchive3.7.2静态解码，完整原字节逐份相等；这是**同批HTTP字节的两解码器验证**，不是两个独立官方来源。

首source40499420515/job122173053693虽作业绿色，双解码/两原件已过，但新整理器错误地限制全部函数名须`PETSKILL_`前缀，遗漏旧压力报告早已记载的`ENEMYSKILL_ReHP/ReLife`。首原报告status=`ORIGINAL_MEMBERS_ACQUIRED_DERIVATION_PENDING`和错误完整保留，不能报内容成功。订正仅接受合法ASCII函数声明标识符，不执行回调。修正source40499885826/job122174615200 / HEAD `1a210bd7dc3c8da674c6e70fae349ba843d47cbc` 才实际派生成功。两次184范围的身份/SHA及两原成员/CRC/压缩块和双解码元数据全相同，总范围字节24027672B；未改原数据。

## 六条原名称与整数列

完整表147个不同ID、146个不同原名称字节串、69个函数token；表混有敌人技能回调，不能叫147个可学习宠物技能。每行均12列：前6字符串、ID/FIELD/TARGET/COST/ILLEGAL五整数及第12列保留文本。第12列仅4行与第三列回调相同，不能整体当另一回调列或擅自加入USETYPE。名称仅在CP950/Big5严格解码相同后保存，不自动简繁转换；描述、OPTION、FREE/KINDCODE及尾列只留长度/SHA。

| 原物理行 | 原ID | 原名称 | 原声明回调 | FIELD | TARGET | COST | ILLEGAL |
|---:|---:|---|---|---:|---:|---:|---:|
| 1 | 0 | 待機 | PETSKILL_None | 1 | 5 | 2 | 500 |
| 2 | 1 | 攻擊 | PETSKILL_NormalAttack | 1 | 6 | 2 | 1000 |
| 3 | 2 | 防禦 | PETSKILL_NormalGuard | 1 | 5 | 2 | 1000 |
| 4 | 3 | 破除防禦 | PETSKILL_GuardBreak | 1 | 6 | 2 | 1500 |
| 5 | 10 | 連續攻擊 | PETSKILL_ContinuationAttack | 1 | 6 | 2 | 2000 |
| 6 | 11 | 三段攻擊 | PETSKILL_ContinuationAttack | 1 | 6 | 2 | 5000 |

前6条按原表顺序、在解码名字之前固定，ID0不是空值或应删除项。列名来自既有后代CFREE6布局，不证明本保存服务端二进制的原生loader。COST全为2不能直接称每次耗2MP或学费；ILLEGAL列保留500/1000等整数，不强压成布尔值。学习NPC、物种可学条件、费用扣除、技能成功回合与真实原服执行仍未证。

## 名称接到已有模型，而非新增原服运行

`STONEAGE-PET-SKILL-NAME-MODEL-CROSSWALK-R45.json`固定6条原行SHA、名称/ID/回调，连接已保存的正数敌人技能压力报告及稳定公共回调模型。6条声明均在既有稳定模型集合；其中5条ID在旧正数敌人报告出现，ID0因旧报告只统计正数而没有该引用，不能因此删掉“待機”。原名称/ID/回调与旧报告所存关系相符。

旧ContinuationAttack的139次正数敌人技能槽使用，是ID10/11/12/13的**整族合计**，不能在“連續攻擊”“三段攻擊”两行各当139次独立新使用，更不能把敌人引用当宠物学习资格。旧模型的closed_runtime标签是原有复原状态，不是本轮原商业服务端执行。

两连攻条目的原OPTION均为1字节；对ASCII0—9作有限重编码，长度和完整SHA分别唯一匹配整数2和3，作为精确数值见证保存，其他OPTION不猜解。使用这两个数值连到**已有Python复原命令/回合桥**，两条分别写入S_RENZOKU的COM3低位2/3；没有执行原回调或声明原画面发生两/三次完整伤害。原有逐击/伤害分摊模型及其证据边界保持，未修改战斗实现。

## 永久保管与验证

两原工件均独立完整下载，ZIP全SHA、恰一份JSON、原JSON全文摘要核对；成功源JSON49019B/SHA `8cb12a7f5dd4ec0ffd39a9112446f82b1583f8cbeb8ced75b8c87c9d7421e914`、Git blob `dd3baaf7e8edda43ef2e136d35f09d1da6717571` 与源日志去时间戳逐字节同一。首失败原JSON/ZIP/run/job/HEAD与双解码及本包184范围收据均永久保留在R45 CUSTODY；原表/描述/OPTION全文、程序及私钥不进Git，不声称原件私人长存。

11项源解析/147行合成回归，16项真实来源/名称映射/跨层命令反例，连同已有loader、schema及回合桥共48项通过。检查包括敌人函数声明、ID0、12列尾字段、同配置不同编译路径拒绝、名称指纹、双解码、来源晋级、ILLEGAL非布尔、COST非MP、正数统计边界和OPTION数值与COST区分。候选/main门槛须实际后验另记；离线重放不再次下载原件。

本包停止扩技能helper。最高NEXT `PRESERVED_HEALING_NPC_NAMED_MATERIAL_46` 轮转NPC服务：先排除旧Healer机制及四出生村路线覆盖；仅核已索引`npc/family/fmhealer.create`649B/SHA `1d7d71960958cc60c5e6ba686fede736b5d66ec15f5d58300041a8a2de893847`，有界验证至多3条原名称/位置/模板服务引用；未取正文前不认定其实际服务、时期或初代出生村归属。缺源/缺函数绑定即有限止点回22域，不回扩洞窟NPC支线或无收益helper。DD-028四档、Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、P3E阻塞、整体百分比未知保持。
