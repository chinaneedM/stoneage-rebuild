# Stage A | WORLD05：GETPET任务数值→敌人实例→宠物模板→原SPR图号（2026-11-04）

本记录从 fresh GitHub main `3bd64c89b47647cad95c1d4c0547f67c6316b846` / tree `99f68012f11175e57b26656ed038cf24e78b1172` 出发。保留 `docs/CURRENT-STATE.md` 的完整历史 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`，不覆盖、不截断。按协议第15–18节，仅做单机目标的原版资料复原，不做网游注册/网关、现代新石器玩法或体验优化。

## 实际新增的可复验跨模块关系

复用已在先前私有原混合2.5 RAR 中读出并做原SHA/CRC资格的两份公开派生索引，而非再次假装本轮已读取原RAR或实际运行游戏：

- `research/recovered/STONEAGE-INTEGRATION01-NPC-PET-QUEST-ITEM-MAP-SOURCE-GRAPH-R1.json`（Git blob `5e526512c0277e19ca41dfcd934c230404d1dfb4`），原QUEST脚本来源、CREATE原块SHA、脚本SHA、`GETPET`字面数字及源行。
- `research/recovered/STONEAGE-PET-MODULE-10-ORIGINAL-MIXED25-SERVER-TABLES-R1.json`（Git blob `25a37aeb134fb180e322e7dc335029b7374452d8`），同归档 `enemy.txt`、`enemy2.txt`、`enemybase.txt`、`enemybase2.txt` 原行字段摘要、模板PETFLG和同载体 `spradrn_5.bin` 原索引。
- 来源父归档SHA256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`；归档系后期**社区混合2.5保存件**，不是已认证JSS1999、台湾1.0、大陆1.82商业同服原件。

结果：**24个原CREATE→QUEST引用，23个不同脚本路径，41次GETPET字面数值，36个不同数值**。36个数值全部存在于原 `enemy.txt` / `enemy2.txt` 两候选实例表；这两表对这36项都引用**相同模板ID**；沿各自实例→模板外键，36/36在 `enemybase.txt` / `enemybase2.txt` 都有原行，两表各自给出的图号也36/36相同，并且每个图号在已登记的同归档SPR索引中只有一条源记录。

**重要防误配：GETPET字面值不是可以直接当成`enemybase`模板ID的连接键。** 36数值中26个数字也恰巧在第一候选模板表里有同号原行，然而它们对应的**实例表外键指向另一个模板ID**；例如原脚本GETPET数字`54`在`enemy.txt`里指向模板`91`，图号`100287`，不能直接接模板`54`及其不同图号。此前各数值只是无语义提升的脚本字面候选，本轮通过明确外键恢复了一个可检验的**静态候选**源链；最终命令语义和实际发宠需原生执行另证。

**两套候选模板存在3项PETFLG原值冲突**，原GETPET数字 `1479`→模板`718`、`1481`→模板`719`、`1483`→模板`720`，对应 `enemybase.txt`为`1`而`enemybase2.txt`为`0`，图号分别为`100451`、`100401`、`100432`。不得擅选“正确宠物状态”、宣称某个版本后来移除宠物、或以单表掩盖不同候选。

## 已验证与仍然未知

新 [36项逐源数值/原行SHA与24条CREATE关系清单](../../research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-05-GETPET-INSTANCE-TEMPLATE-SPR-R1.json) 仅包含公开许可的散列、数字、源路径和来源资格；没有商业原文、原SPR、图像、运行密钥。新增回归测试对原有两个公开来源文件重新计算外键、全部计数、原同号误配、三项候选矛盾与禁止历史越界。**本轮没有重新读取私有原二进制，也没有新的原像素/画面、GETPET运行、实际任务完成或玩家获得宠物的证据。** 源SPR索引有记录≠已读取原RD动作像素、更不等于原客户端显示和官方同服。

保持 Stage A 7 PARTIAL + 2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，overall_percent=null。此前WORLD04的历史记录完整保留。

**NEXT：STAGE-A-OFFLINE-WORLD-CONTENT-06。** 只在现有私有已认证原SPR/REAL像素与这些脚本关系可精确桥接时做一项具体原内容可见性核验；缺精确原件则保留图像/运行差距并转下一有实物模块，不建新浏览器框架、网游服务器或新游戏玩法。
