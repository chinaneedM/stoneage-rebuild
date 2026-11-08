# QUEST29｜精灵王事件69原脚本、NPC配置与全任务目录查重（2026-11-08）

## 范围与新鲜远端基线

按仓库 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md`，本单元从新核远端 `main` HEAD `1d92ff6a2b183020e4582c6206ab74b137188be7`、tree `2ea181f8efcd5f8150d6fb421e3d09936fa65da3` 启动。已重新读取 `README.md`、连续性协议、完整 `docs/CURRENT-STATE.md`（旧 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`、2,317,877 字符）、四历史启动文档、路线、模块顺序、QUEST28 交接。该基线最新提交仅为 QUEST28 后验文档，`main` 原 QUEST28 代码提交 `f15f31e` 的 11 项 CI 已实测成功；本轮最初查询的后验文档 HEAD 没有对应新工作流运行，不混称为 11 项通过。0 开放 PR。

**业务目标**：先清点原任务模块中最旧完整目录的重复脚本，再选出一个对玩家实际可见的完整内容族，不随意延长已收敛的药草/投递辅助函数。选择 `king/event69_*` 精灵王长剧情，因为它同时包含道具交接、带条件的对白/选择、NPC 配置地点、随机候选及宠物奖字面；材料已在先前保管的 2205 原 NPC 文件、838 项源包和 QUEST01/ITEM01 索引中，而非凭媒体故事想象任务运行。

## 全模块索引审计与精灵王新增的是什么

- 既有 QUEST01 后期 mixed25 社区保存本索引为 **295 份不同的 TYPE 原脚本／1349 个原 TYPE 段**，源路径目录共 14 组。14 是原目录命名空间数，**不是 14 项独立任务、不是全球任务总数**；同一脚本可由多个 NPC 创建引用。只做已保存载体的账目边界，不把旧脚本数作新的复原百分比。
- `king/event69_*` 的 **13 份原 TYPE 脚本／71 原 TYPE 段**全部在旧 QUEST01 原索引中。**新原始脚本发现 0，新增原 TYPE 段 0**；本轮实质成果是将它们与 **25 条原创建配置、36 个实际原文件、48 个源物品 ID、96 行物品表**和历史版本文本分别联接，同时保留原异常与出处。
- 此前 `docs/specs/STONEAGE-CN25-SPIRIT-KING-STORY-R113.md` 是 2002 玩家文章、2004 网站文稿的**有来源限定的后期叙事**，非此 2205 文件的原脚本实验。两层可以互相提供核查线索，不能以剧情角色同名证明同一运营服、初代发行版或原客户端运行。

## 实物验证与内容关系

本轮实际读取用户 Library 已存的 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip`（995,176 B，SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`）和 `StoneAge-ITEM01-private-two-itemsets-832-original-RD-icon-observer.zip`（5,868,386 B，SHA256 `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa`）。2205 原 NPC 成员逐完整长度、SHA256、ZIP CRC 与已归档 CHAR01 完整清单核对；ITEM 全 838 CRC 通过。旧 QUEST01 精确 Git blob `52db8b4b6cd43cd2afa4a8d2e8460f214933f5e2` 和 CHAR01 `a088b61a3212f7049e7793f587123ffb29bebad7` 独立对比。用户 Library 中的旧 QUEST01 导出版多一个终止 LF，先以 Git 已存 SHA 对该尾 LF 作字节级验证再复原精确原 Git blob，**不是**把不同内容当同一文件。父 361MB RAR 本轮未重新读取，不虚称已二次重验父压缩包。

精确 CREATE：`king/event69_alpha.create` **24 条**，另有 `giiru/event/event30.create` 原序号 4 指向 `king/event69_1`，合计 **25 条**。其中 13 条是 `ExChangeMan` 脚本（原 `changeevent` 模板），其他原来源含 `npcgen_warpman` 与独立 `event69_5/13/15/17/19/21/23` 参数模板，保留原函数类别，不全扁平为同一种对话 NPC。原 CREATE 覆盖 20 个不同原 floor ID；原 `borncorner`、方向、图别名、源字节范围 SHA 与原序号保存，**不是已进入的 20 张原地图**，没有新 DAT、原生碰撞或传送验证。

13 份脚本的 71 个完整 `TYPE` 段、`EVENT` 条件 SHA、物理 TYPE 行号逐项与老目录匹配；类型为 **24 ACCEPT、44 MESSAGE、3 REQUEST**。历史人物叙述涉及新藏、玛蕾菲雅和精灵王关系，仅为该后期社区保存包对白内容，仍需同版本官方来源与原游戏实际执行核实。

原脚本三处不应被“修好”的证据：

1. `king/event69_11` 的原 `DelItem:19633,19634,19635,19636,19637,19638,19639,19640,19645,` **末尾确实有逗号**；原 `EndSetFlg:122,123` 是一条带逗号值的源行，不自动拆成经认证可执行的两个旗标事务。
2. `king/event69_7` 有四条九位 `GetRandItem` 字面序列，且每条存在原重复位置；`king/event69_14` 另有四 ID 的随机候选序列。五条完整顺序和重复已保留，不把出现次数解释为原服概率表。
3. 原 `GetPet` 字面分别出现 **355、484、1479**（对应 `king/event69_1`、`king/event69_24`、`king/event69_7` 的各一段）。它们是原命令的**数值操作数**，不等于三只已在本轮领到的宠物，更不等于三个宠物模板 ID、同版奖品或初代可用内容。

两原 94 栏 itemset 对精灵王族引用的 **48 个不同 ID／96 行**完整行字节、哈希与旧 ITEM01 七个公开索引分片匹配；48 ID 中仅 **5 个**有已认证台湾1.0原 RD 的跨来源候选 PNG，**43 个缺该候选，不代表它们从游戏中不存在**。48 个ID共享 31 个原物品图号别名；同图不合并 ID。实际没有为缺失43图创建新图或从后期脚本推断台湾1.0商品配置。

## 私人观察、公开交付与继续条件

私人包 `StoneAge-QUEST29-spirit-king-event69-private.zip` 已写入用户个人 Library，含 138 成员、原 CP950 文件和道具行、少量有证候选图、自包含现代原文查阅 HTML，**90,890 B / SHA256 `e710f97dfc165e06680f3b016b19313c6a5569558cfc700759da1cc2f0f28407`**。全包 CRC 与公开派生 JSON 哈希核对，不能视作原客户端运行或私人 HTML 浏览器已测试。原商业对白/脚本/物品行/图像均不进入公开 Git。

公开 `research/recovered/STONEAGE-QUEST29-SPIRIT-KING-EVENT69-SOURCE-R1.json` 是可复核的来源数值、完整 SHA 与异常字面；独立回放工具只读取显式私人输入生成报告和私人包。回归测试以仓库旧 QUEST01、CHAR01、ITEM01 数值及完整 SHA 为准；CI 不接触原商业字节。原任务可玩、奖励领用、真实随机概率、原生模板处理、同部署正统身份和早期版本归属仍 OPEN。

**最高 NEXT `QUEST30_NEXT_SOURCE_READY_UNSPECIALIZED_QUEST_FAMILY_OR_BOUNDED_MODULE_STOP_AFTER_KING_EVENT69`**：回旧 295 脚本/22域已验来源继续模块去重。优先另一组实物齐备而此前未专项整合的可见原任务族；若剩余只重复旧脚本或者依赖不可取原件，应明确来源止点转跨模块整合审查，而不是无限写 QUEST 编号。禁止先行新作引擎、在线账户/服务、玩家体验优化。Stage A **7 PARTIAL+2 OPEN**，Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、总体百分比未知。

本篇作为大型 CURRENT 历史未改时的加法续接，最终 PR、Actions 与主线 HEAD 应在验收后补后验，不预支 CI 成功。
