# PET-MODULE-10｜从保留的混合2.5完整原RAR重新实际读取宠物主表、技能与实例（2026-11-02）

## 真实原件，不以旧二次摘要替代

PET09结束时认为CN5/TW85大包不能重新读取；在进一步查私人Library时，发现一份**另一性质的已保存原件**——`stoneage-preserved-mixed25-original.rar`，361255180B/SHA256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`。本轮实际材质化原RAR、完整SHA校验、使用Python rarfile遍历7952原目录记录、以本地libarchive真实解压8个必要源成员并逐源完整SHA/归档CRC吻合。所有原文本均CP950完整无损解码，源CSV各行/每字段数验证。

### 直接恢复的实际原游戏服务端内容（但未认证为官方商业同服）

| 真实原成员 | 有效行/索引 | 本轮实读结果 |
| --- | ---: | --- |
| `enemybase.txt` | 988 | **56原字段/行**、995物理行包含7空行；495行原PETFLG=1、493行0；495行含424不同图形数值 |
| `enemybase2.txt` | 640 | 另一56列备选表，316行PETFLG=1（291图号），324行0 |
| `enemy.txt` | 2087 | 原实例ID与主表引用按实字段全数匹配（2087/2087） |
| `enemy2.txt` | 1494 | 原实例ID与备选表引用全数匹配（1494/1494） |
| `petskill.txt` | 147 | 主表本保存包技能定义，495宠物模板正数技能槽1050项均在此表有定义 |
| `petskill1.txt` | 56 | 备选表独立技能定义，316宠物模板661正数技能引用中649有定义、12未找到（5种不同ID） |
| `skillcode.txt` | 146 | 原完整源已校验保管；本包没有额外推断实时技能训练或强行关联 |
| `spradrn_5.bin` | 847个索引 | 841不同图号；主表495宠物标记行有302行同图号能在本包索引命中，涉及234不同图号 |

两份原模板表有640个共享模板ID，**365条56列全值相同，275条至少一列不同**；另一份比主表少348个ID。只代表同一RAR中保存的两套静态表，**不证明服务器加载了两份、官方版本差异或两次发布先后**。主表同源147技能定义可以按数字ID关联；引擎端回调执行、原服配置选择、原版物种完整数及出处仍未验证。

本轮曾尝试继续用本地libarchive从RAR抽 `data/adrn_15.bin` 和 `data/spr_4.bin`，返回 `Parsing filters is unsupported` / `Prefix found` 而未完整解出。原索引 `spradrn_5.bin` 10164B已完整读取/源SHA `5f13c956cf013e073298ab91667d3aaa17767b26ba94d696514726950ce94de6` 与R40既往来源一致；没有将失败的SPR主体或真实RD像素宣称已成功本轮取得。保留此前R40少量实际SPR材料证明，不回写旧失败。

## 可查阅原内容、派生索引和安全边界

- **私人原貌目录** `StoneAge-PET10-private-original-server-pet-catalog.json`，4.10MB，包含每条原CP950文字、字段、原物理行/原源行身份、同保存包SPR索引；仅用户Library，不提交商业原表。
- **私人可检索网页** `StoneAge-PET10-private-mixed25-pet-catalog.html`，263KB，实际支持原名/模板ID/图号检索、两原主表选择、宠物标记筛选、原数值/同源技能/实例引用观察。Chromium `set_content` 实际验证主表495/988及备选316/640筛选、查询、0 JS错误、0外部网络；本环境file://策略拒绝，本地文件URL打开不冒称已验。
- **公开无原文的实质派生资料** [STONEAGE-PET-MODULE-10-ORIGINAL-MIXED25-SERVER-TABLES-R1.json](../../research/recovered/STONEAGE-PET-MODULE-10-ORIGINAL-MIXED25-SERVER-TABLES-R1.json)：8个原成员来源尺寸/SHA/CRC、988+640完整56字段的**必要数值索引+行校验摘要**、2087+1494实例源外键、147+56技能ID、847 SPR索引；无原字段名称批量复刻/原客户端像素/专有二进制。
- 本地原RAR完整SHA/8源成员CRC实物验收；公开CI仅重新检查已发布派生数据的字段守恒、映射与危险升格负例，不伪称CI拥有原RAR或再次执行游戏。

先前PET01的2016后期社区服务端是**另一源**，PET10混合2.5保存包并不是其原版官服替身；即使二者同ID同名也不能默认为已证同部署。原项目CURRENT blob `20050acf279a01555ab06a381dfcdc936bd381a6` 完整保留原样。

### 下一步

这批源就绪的原宠物主表已完整恢复并提供私人可观察视图。**宠物模块为 SOURCE_BOUNDED_PARTIAL，不是全官方历史版本100%完成。** CN5/TW85实际原RD大包、早期同构建官方主表仍缺；按既定模块优先规则，下一模块切人物/NPC，未来有新合格原宠物素材再增量重开。Stage A 7 PARTIAL + 2 OPEN，B/wiki GATED，R79 PAUSED_NON_BLOCKING，总体完成率UNKNOWN，不进入Stage B。
