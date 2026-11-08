# QUEST18｜吉鲁火之仪式、不死鸟羽毛与巴那姆水壶：原任务、道具、跨地图候选路径（2026-11-08）

## 1. 远端起点和去重

按 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` 重新读取远端分支、HEAD/tree、最新提交、Actions、续接协议、README、来源决策和 `docs/CURRENT-STATE.md`。起点 `73823957f9a0b3343a029440a5b30282c452c186`、tree `69625b80f4d0f143d33e87699bba4d55d154079f`；原 `CURRENT-STATE.md` blob `c89e0e33537990aa2132b47c40fef49a985a935c`（2,709,173B）完整读取，保持原样不修改。QUEST17 已合并并获后验验收，最高待办是 QUEST18 去重后再处理独立可读的原源族。

选定 `giiru/event/sink/sink.create`。此前 QUEST01 已索引全部 **12 个 CREATE 引用／11 份不同脚本／79 个 TYPE 事件段**，因此本轮不是新增 79 个历史上未知的事件；新成果是重新真实读取原物和两份物品表，结合 691 张 MAP09 来源认证地图，进一步明确任务步骤、物品体积状态、37 条传送命令的全部坐标边界，并为未来单机复原留下可测试的版本限定规格。O74 四个大厅的委托书任务已在旧研究验过，排除其重复整理。

## 2. 实际原字节和边界

完整实读私人 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip` 995,176B，SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`，**2,205 个 ZIP 条目 CRC 全部通过**。当前 `sink.create` **2,501B**、SHA256 `2a2506a766194a7e203b78f8057814e0152ef7be0c9394b546b20240c99c5ab0`；逐源读取 11 份原脚本，原尺寸、SHA256、CRC 与 QUEST01 旧来源索引吻合，**79/79 个 EventNo/TYPE/事件规范段 UTF8 SHA 逐一相同**。源文件 CP950 严格解码—回编码相等。未修改原脚本。

`sink.create` 有 12 条生效文本式 `changeevent` 创建参数、一个不同职能的 `bus` 创建参数、两条源码注释禁用块；相同 `sink06` 被两名“火的使者”NPC 配置引用，所以不能把 12 位 NPC 叫 12 份脚本。当前目录另外有六份无活动 CREATE 引用的 `sink04/04a/04b/04c/05/05a`，本份 QUEST01 全量索引对它们的精确引用为 0。不能据此断言全服从不加载或推其发行年代、先后版本。

另独立全 ZIP/CRC 重读 `StoneAge-ITEM01-private-two-itemsets-832-original-RD-icon-observer.zip` 5,868,386B，SHA256 `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa`；838 ZIP 成员通过。该包来自后期混合 2.5 物品行与**另一个台湾1.0零售载体原 RD 图像**，跨载体对应只算候选，不宣称官方同服或原生 UI 渲染。原版权文本、原图、原 ZIP 均不进入 GitHub。

## 3. 玩家能感知的任务条件关系，静态字面

- `sink07` 原 REQUEST `EventNo:40`，`sink01` 对 `NOWEV=40&ITEM!=2706` 有 `GetItem:2706`（不死鸟羽毛）和四个 `20309` 地图的 `NpcWarp` 数字候选；`sink02` 有 `EventNo:40`、`NOWEV=40&ENDEV=4&ITEM=2706` 对应 `DelItem:2706`、`GetItem:2707`、`EndSetFlg:40`。**只能认定原脚本字面可连接为“申请→取羽毛→交羽毛→标志40”，不能认定运行时一定可达、顺序已执行或奖励已发放。**
- `sink03` 对 `2708` 空壶写出不同 `GetItem` 满水候选以及 `GetStone:1149` 的另一分支；源 `GetStone` 数字是石币，不是物品 ID。不能按常识强加分支优先级、领取前置条件或实际扣款顺序。
- `sink044/044a/044b/044c/055/055a` 存在 **37 条字面 `NpcWarp` 操作**，展开至 220 次三元组候选，去重后 **26 个不同 floor/x/y**，落在八个 MAP09 已有来源资格的地图 floor 中，全部数值在各地图宽高范围内。四类 `sink044*` 每段有8或9个候选，`sink055*` 每段4个候选，且有同一坐标被重复列出的情况。**不能把候选列表当随机均匀分布、路线全部可走、已实际传送或原始地图碰撞/入口已验证。**
- `sink06` 存在 **7 条 `GetRandItem` 指令**，原列表长度依次为3/3/4/4/4/5/6，搭配 `DelItem` 字面。未解原选取概率、原背包状态和可重试性。
- 取自脚本中 `GetItem`、`DelItem`、`GetRandItem` 的 **44 个不同真实道具 ID**（已剔除 `*1` 这种数量字段，以及 `GetStone:1149` 的币额）；在两个原 94 栏物品表的 **44×2 行**中逐 ID 均有记录且原 SHA 成对相同。对应台湾1.0原图索引为43个 RD 已解码跨载体候选；`2614` 仍为未取得对应零售 RD 图，不能猜图或补造。
- `2708–2718` 是巴那姆水壶系列，源文本容量不是简单顺序计数：`2709=7/7`、`2710=4/7`、`2711=3/7`、`2712=6/7`、`2713=5/7`、`2714=4/7`、`2715=3/7`、`2716=2/7`、`2717=1/7`、`2718=空`；`2708` 是未装水壶。两对不同 ID 共享 `4/7` 或 `3/7` 标签，不可按水量去重或建立擅自的数值推进公式。11 个壶道具源图别名均为 `12924`。

## 4. 地图证据与保存分类

先前 MAP09 源资格目录 `research/recovered/STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json` 中，本族 12 条 `changeevent` 创建参数所属 floor 唯有 `300` 没在这**一份691地图目录**里；这不是游戏缺图断言。其余 NPC 所在格均在已验尺寸内。37 条传送操作的 26 个去重终点均有同目录认证宽高并且数值不越界。**这次新读取 DAT 整体/单格 = 0**，只复用之前有 SHA 的派生目录，不声称新执行了真实地图绘制或 NPC 碰撞。

按单机复原资料结构建议保留四个独立索引键：`source_carrier/version_scope`、`npc_create→script/event`、`item_id→original_row_hash/quantity_variant`、`floor_id/x/y→source_qualified_MAP`。世界按地理/区域建立可调整父层，宠物、任务和物品各按所属玩法标签分组，但**当前没有原官方归属的分类保持 UNKNOWN**，不能把“吉鲁”脚本名自动投射到台湾1.0原正式地图。

## 5. 本轮止点及下一优先级

公开研究数据：`research/recovered/STONEAGE-QUEST18-GIIRU-SINK-SOURCE-R1.json`；可在 GitHub 纯公开原索引上运行的回归：`tests/test_stoneage_quest18_giiru_sink_source.py`；专门挂进已有 QUEST05–18 CI，不下载私有商业内容。本地原 ZIP 实际字节测得以上原哈希和新静态交叉关系；公开 CI 仅重新证明派生索引的自洽和负证条件，不替代原私人源完整再读或原版程序运行。

**QUEST18=SOURCE_BOUNDED_STATIC**；未经后验不得称已被主线验收。Stage A **7 PARTIAL +2 OPEN**；Stage B/wiki **GATED**；R79 **PAUSED_NON_BLOCKING**；总体完成百分比不报告。**最高下一项：QUEST19**，先与 QUEST01 和 O 系列已审资料查重，再选一族真正不同且私有原源可逐字节核对的任务；有新同源可执行轨迹才重开 QUEST18 原NPC/传送/随机道具结算，避免循环增加没有新玩家内容的辅助工具。始终服务于离线单机复原，不启动账号、网络商业服务端或新引擎。
