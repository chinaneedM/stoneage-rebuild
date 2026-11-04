# Stage A｜WORLD09：任务随机物品奖励原候选槽与后期源码解释（2026-11-04）

从新验主线 `66caeb8e6e6e35f74d410cdb24b248af52605bf1` / tree `1bb5a5fea83db740969d627940c5581410d907f6`，按最高 WORLD09 直接回收原任务/物品来源事实。原 `CURRENT-STATE.md` blob `c89e0e33537990aa2132b47c40fef49a985a935c` 2709173B 完整保持。

## 真实原材料与新统计

用之前已实读私人保存的社区混合 2.5 RAR 任务脚本所得、完整公开派生[QUEST01 1349 原 TYPE 控制段目录](../../research/recovered/STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json)，固定 Git blob `52db8b4b6cd43cd2afa4a8d2e8460f214933f5e2`；**本轮没有重新实读私有 RAR**。严格按源 `source_operations.GetRandItem` 筛出50个原控制段、33份不同原脚本（原脚本完整 SHA、控制段 SHA、原行与顺序详见[新逐来源目录](../../research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-09-GETRANDITEM-SOURCE-SLOTS-R1.json)）。46段 `ACCEPT`、4段 `MESSAGE`；这些是静态原脚本控制段，不是50项已运行任务。

原脚本共718个随机物品候选**位置**、328个不同物品数字ID。50组全部有非空数字候选，每组位置内未出现相同数字ID重复；没有任何一组同时包含 `GetItem` 字面。**这并不意味着不同脚本之间的相同物品要去重**：原718个位置完整保持，50组分别候选范围为3–67。328不同ID全部在既有两份原候选 itemset 表中有数字记录，本批所联两候选主表只提供“有此数字行”，不决定原运行选用哪份表或真实奖励。

## 单独固定的另一份后期社区 C 源码

直接读取 [`pimpcapital/longzoro-sa` 固定提交的 `npc_exchangeman.c`](https://github.com/pimpcapital/longzoro-sa/blob/57b14e2bb373ba851c14db28a239273e4a8831bb/gmsv/src/npc/npc_exchangeman.c#L2820-L2874)，Git blob `7a9cc7ea6d76bfdae367c580db4ce6fcb42d7d15`。在此**后期独立源码**里，`NPC_RandItemGet` 对 `rand_j==0` 返回 FALSE，对正数选择 `rand()%rand_j` 并把数字0改作末位置 `rand_j`，再使用**1起始位置**从逗号列表取ID；若新物品创建成功则尝试加入玩家物品栏，失败时销毁刚分配的物品。调用处存在背包空格的静态检查，带 `GetItem` 的另一路输入检查，不能把所有原脚本统一设为同一奖励数。

因此新复原规则应保存**原顺序、完整候选位置和失败路径**，不要把 `GetRandItem` 误作一个固定物品号或删除重复的跨脚本候选。静态源码展示索引映射，不认证当年实测概率（含 `rand()` 的伪随机分布/取模偏差）、已生效编译宏或持久化成功。

## 来源边界与验收

这份 C 源码与原私有混合2.5 RAR **未证同一构建或运行部署**，不能把它提升为1999日本、台湾1.0或2001大陆1.82的官方物品规则。任务起源全部仍 `ORIGIN_UNRESOLVED`，并不以 `event` 路径名视为运营活动，也没有进入原商业游戏执行任务。CI重算原公开派生目录的50段、718位置、328 ID和每段原 SHA，再拉一份 Git SHA 锁定的 C 原件验证静态函数；无商业原文、素材或原执行载荷入公共仓库。

**WORLD09 SOURCE_BOUNDED_PARTIAL。最高下一项 WORLD10**：轮换到真实未闭合的地图/人物/物品等原内容实物，优先能实绘、实读的新内容，避免重复 C 辅助函数研究；不转网游账号/服务器、不做新石器优化。Stage A 7PARTIAL+2OPEN，Stage B/wiki GATED，R79暂停，总体复原百分比未知。
