# INTEGRATION108｜原斗技场 34 NPC 配置、四村回路、26 原参数及来源二维候选（2026-11-14）

## 任务与远端起点

严格按 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` 重新读取远端 `main` `ebd200b9ffcceb6f7661ad4f969ed39846655eee`／tree `2c9a462b9f1a3e45ab486351688ec93920e2fc8b`、最新提交、当前精确 HEAD Actions **26/26 completed/success**、开放 PR **0**、完整 README 与协议指定的设计／历史／来源文件、路线和模块顺序。`docs/CURRENT-STATE.md` 普通接口空响应不表示空文件；按远端 Git tree 取得原 Blob `c89e0e33537990aa2132b47c40fef49a985a935c`，**2,709,173 字节**，完全保留，不用旧记录覆盖。此文档是新的加法层。

**目标：** 让尚未独立整合的 `npc/genout/duelroom.create` 成为有据可查的斗技场静态内容单元——原 NPC 创建与坐标、四村到 130 地图的路线参数、商店和寄存、告示原资料、同载体／跨载体原二维候选。交付只限已保管原文件的来源关联与私人离线观察；原生竞技、入场验证、服务价格、商店交易、NPC显示、碰撞以及服务器加载始终**未证明**。这不是新的单机引擎或现代玩法实现。

**避免重报：** ITEM01 已清点大批原商店 ItemList，CHAR01 已清点 2,205 个 NPC 文件，SCENE13 已观察 `100250` 原 SPR，MAP01 已原字节验收大量 DAT。以前这些都是已有源，**本次新增是斗技场 34 原 CREATE／26 原参数／130 楼层场景／门票来源的具体可查整合，不是新发现 34 个历史独立人物或 100 件新道具**。现有 README 未见 `duelroom.create` 独立的完整来源桥，故本包有限处理该实体；旧家族赛事与原官方规则不能凭相似名自动并入。

## 实际原来源完整核验

- 后期社区混合 2.5 原 NPC 私人 ZIP `StoneAge-CHAR01-mixed25-all-npc-original-private.zip` **995,176B**，整 SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`，**2,205/2,205 ZIP CRC** 真检；本轮真正抽出原 `npc/genout/duelroom.create` **5,732B**／SHA256 `4c47e9c320f9d3fe6616e6860d14d2681df1994bb8c4a849e5b6d93a38998a91`、34/34 个原 CREATE byte spans／SHA，以及确实指向的 **26 份不同**原脚本／外参文件完整 SHA 与 CP950 无损往返。无源码／商用对白上传公开 Git。
- 34 条均是不同的**源楼层与坐标点**：29 在 floor130，另有 floor1000、2000、3000、4000、110 各 1。原函数分组为 `npcgen_warpman`9、`npcgen_shop`9、`npcgen_signboard`5、`npcgen_dengon`5、`npcgen_healer`2，以及 `npcgen_man`、`npcgen_petshop`、`npcgen_poolitemshop`、`npcgen_mugon` 各 1。功能标签来自原配置，不能当真实服已经挂载或已执行的证明。
- 对接已独立 SHA／CRC 验过的 MAP01 派生原文件索引（Git blob `03675ee98d391f9ef0246315b2426f2a8b721fd3`）：floor130 的原 DAT **60×60／21,608B**、SHA256 `85d710a270c6b945de21de53c9257ebaf38647cb54e77071db194cf5c5e203f3`。本包对 **29/29** 个斗技场内部点及 floor110／2000／4000 三个入口点核其来源坐标在已验宽高之内，共 **32/34 WITHIN_DAT_DIMENSIONS**；floor1000／3000 的 DAT 在**该 MAP01 清单中提取未合格**，记作 **2/34 NO_QUALIFIED_DAT_IN_MAP01**，不是宣布这些原图不存在，也不是记录越界或证明可通行。本轮重新读取原 DAT 本体 **0B**、新原 MAP/RD **0**；不能说新跑了原客户端。

## 九条具源参数的静态进出关系

原保存的 5 个外部入口分别为 floor1000 `(56,59)`、2000 `(85,79)`、3000 `(93,86)`、4000 `(88,61)`、110 `(38,37)`；其原 `WARP` 参数目标都在 floor130，分别是 `(57,13)`、`(57,22)`、`(57,31)`、`(57,40)`、`(57,49)`。floor130 内部 4 名导游分别位于 `(57,12)`、`(57,21)`、`(57,30)`、`(57,39)`，原参数目标分别指向 floor1000 `(55,59)`、2000 `(84,79)`、3000 `(92,86)`、4000 `(87,61)`。

**字面上的坐标差一格不能被静默修成相同点。** 这 9 条 `npcgen_warpman` 原文件都包含 `WARP`／`FREE`／`MONEY:-1`，四村门票条件对应 **2597／2598／2599／2600**，floor110 的入口 `FREE` 同时出现 2597–2601 五 ID。`DelItem` 数值来源按原顺序留存；任何一条都不是原服务器实时扣物、返还、收费或传送成功证据。源参原金额 `-1` 不解释为收费或免收费。既有原两套物品表对应票号均是静态 ID，并非确认同一官方运行服务器。

## 商店、告示和原二维来源

- 9 个源 `npcgen_shop` 的 `ItemList` 都是真正取自9个原参数文件的显式整数集合：共 **127 个原列举位置／100 不同 ID**；其中两个 `LimitItemNo` 存在范围表达式，原范围未冒充展开的真实售卖库存。连同原 `FREE`／`DelItem` 的 10 个额外 ID，本次对 **110 个不同物品 ID**复用了 ITEM01 已认证两份原物品表逐行 SHA；原清单已有内容不能重复算作新物品发现。特别留存 `(130,1,14)` 原创建引用文件名 `ss_130_3_14`，以及 `(130,4,14)` 引用参数 `pis_1009_14_13`（文件名含 1009），不因文件名擅改原楼层／出生格。
- 5 条 `npcgen_signboard` 实际原文资料是**等级分档、宠物与道具使用限制、判定回合**方面的原告示；确认有等级数字分组、道具数值 3、回合数值 30，但无法证明官方比赛执法或原生等级公式。5 条 `npcgen_dengon` 是无外部文件字节引用的原配置，不能编造历史玩家留言。另两名治疗者是 `npcgen_healer|1`；宠物店、寄存服务及 `cost:50` 都只是原参数字面，实际价格货币、存储、治疗／买卖未实走。
- 复用**同后期 mixed25 载体** SCENE13 已验 `100250` SPR 动作0方向0首帧原图位图 `95883`，PNG SHA256 `32020af425521f05014d68538fa2355ff70d3c52d73761044ed2e6532bec8a43`，实际从已保存原私人 HTML 按同源位图号取回、整 PNG SHA 与旧原 RD 回执一致；floor130 的 `(48,3)` 原 `graphicname=100250` **只可接为一幅来源合格可见候选**，不是原生实际取帧／遮挡／同服身份。
- 另从已认证 ITEM01 原私人 ZIP **5,868,386B／838 CRC** 真正取回台湾1.0零售原候选图号 `24176`／`24177` 两 PNG：SHA256 `82334c031191fb20b31f6a469a9a9985dac36592ba362defc8ed0b9a15a06572`、`a2f420e60ffc78dd2f17bbfcbac183de95cc5d66e8ff99adb6b2b6d8a3c03843`，逐RGBA和尺寸验真。图号与后期 mixed25 票据物品表字段仅构成**跨载体候选**，不可认定历史同部署配色或原版游戏 UI。

已新建私人只读离线资料页、34 源 NPC 配置、26 原参数文本、1 同源真实首帧 PNG、2 跨版本原票图候选和私人 manifest，封存为 `StoneAge-INTEGRATION108-duelroom-34-original-source-candidates-private.zip` **33,428B／32成员／SHA256 `68ac4bf23f4fa442f8c6b3d687760c84bf0c326ea09359523894a651fc64a892`**。已存个人 Library `/石器时代/`，**独立取回全包逐字节相等、32/32 CRC** 再核。私人 HTML 在本地真正 Chromium 进行静态资料页验证：初始34卡、floor130筛至29卡、商店功能筛至9卡、重置34卡，3张实际私人原图候选 naturalWidth/Height 正确加载，JavaScript错误0、外部HTTP请求0。测试通过 `page.set_content`，不宣称真正 file:// 导航成功；不是商业客户端或原生游戏画面。原 CREATE、完整文本／PNG／HTML 未入公开 Git。

公开内容只保留 [原字节范围／SHA、数字关系和负证 JSON](../../research/recovered/STONEAGE-INTEGRATION108-DUELROOM-34-CREATE-26-SOURCE-WARP-ITEM-R1.json)、对应10项来源限界正反测试及专用 CI。公开 Actions 只能核派生数字与已归档的原 SHA，**不会在 GitHub Actions 下载私人原件**。候选与主线必须分别按精确 HEAD 后验，未验不报通过。

**结论：`SOURCE_BOUNDED_PARTIAL`**。Stage A 仍 **7 PARTIAL＋2 OPEN**；Stage B/wiki **GATED**；R79 **PAUSED_NON_BLOCKING**；整体 percent=null。**NEXT**转另一组非重复、真正原字节／可见2D／宠物或任务材料；floor1000／3000 在此 MAP01 目录仅凭有独立合格原 DAT 才能升地图格资格。禁止无源扩建场景、原生斗技场执法/排名和新游戏引擎。
