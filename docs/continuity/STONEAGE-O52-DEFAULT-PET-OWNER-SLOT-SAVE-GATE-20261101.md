# O52 — 默认出战宠物不能指向空栏位（2026-11-01）

## 远端起点与实质缺口

从 GitHub main `9da141db447de3b58eb643eb24aa43b630b12618`、完整 tree `e7c33c8d055fba596155f2bbd8141194cb3432e8`（6838条）、最新提交和成功 Actions 出发，读取连续性协议、完整历史 CURRENT 原 Git blob `20050acf279a01555ab06a381dfcdc936bd381a6`（2,708,031B）、README、设计决策、史表、源登记、路线与 O51。没有依旧聊天推测新状态。O51 来源级问答任务已到止点，本轮不扩 Quiz 引擎、NPC 与奖励模型。

转向**宠物拥有状态**：现有 `tools/stoneage_singleplayer_persistence.py` 允许 `default_pet_slot` 是合法编号却指向并不存在于 `state.pets` 中的宠物。此前只校验编号范围，下一场战斗又将该默认选择传给战斗状态。这是现代本地存档完整性风险，不是原版行为仍缺证而须猜测的规则。

## 最小变更与验收

在原有 `dump_persistent_state` 和 `load_persistent_state` 两处直接检查：**非 null 默认栏位必须指向已有的携带宠物槽**，否则报 `ValueError`。不新建 helper、schema、数据层、服务器或推测默认宠物。历史 r1/r2/r3 存档没有默认槽，`None`、正常已拥有槽2与其他原功能保持原状。

向既有 persistence 单测加一项：仅拥有槽2时，选择合法但空的槽1必须在写入/编码与读取时均拒绝；无宠物时却选槽2也必须拒绝。既有测试继续核验正常槽2、`None`、旧 schema 升迁和重复槽。

这是**现代存档设计与数据完整性（DESIGN）**，而非历史原台湾1.0/JSS1999选择机制；未经原客户端和服务端执行，不宣称已经进入原游戏世界。版权原资源/商业原文/二进制没有读取或提交。CI 成绩以后验实际 Actions 为准。

## 历史边界与后续

完整 CURRENT 大文件不改，使用协议第14节日期加法覆层，原历史条目/来源不覆盖。Stage A **7 PARTIAL + 2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、`overall_percent=null`、原游戏世界仍未进入。

**NEXT O53：**返回同来源可认证的原世界交互或宠物拥有/托管内容；只有能改变可观察游戏内容或来源结论的新材料才推进。不继续泛化默认槽检查，也不重做 O28—O51 原场景或静态内容。
