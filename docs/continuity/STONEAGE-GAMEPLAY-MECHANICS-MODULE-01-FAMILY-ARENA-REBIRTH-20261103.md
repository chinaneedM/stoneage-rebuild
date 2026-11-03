# GAMEPLAY01｜原家族对战场、挑战计时字段与宠物转生／骑乘文本（2026-11-03）

**阶段：Stage A 原版历史复原。** 从已验收 QUEST04 主线 `2cf326b70e3f59305cec830f5081fe24fd5257ba` 继续，选择现存保存来源内真正可复读的玩法机制原参数，不做新引擎、战斗平衡、游戏体验优化或原创机制。原历史 `docs/CURRENT-STATE.md` blob `c89e0e33537990aa2132b47c40fef49a985a935c` 保留全部原字节。

## 来源与实际恢复

从已保存的 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip` 真正重读2,205份原NPC文件、1,930,332B；对保存文件逐大小、全SHA256/CRC32复核与已提交的CHAR01来源证据一致。ZIP当前整SHA `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`，属原社区混合2.5保存载体的**私人原字节提取件**；本轮**没有**重新读取父361MB RAR。原源、对白和美术不公开，Git仅永久保存数字/来源资格、相互引用、证据止点。

此次按一组实际玩法相关功能恢复 **37条原创建配置**，其中**33条可逐SHA/CRC定位对应的33份实际原参数，合计14,611B；4条 `riderman` 创建配置没有同NPC树内 `file:` 参数引用**。这4条不等于骑乘规则已恢复，也不代表原版不能骑宠。

- **家族对战入口：** `npcgen_fmwarpman` 9份参数带9个原 `ID` 及2组 `WARP` 数字候选，原ID集合准确为 `{1,2,3,4,11,12,13,14,15}`。
- **场内返回：** `npcgen_fmpkman` 9份参数包含同样9个原ID及各1组 `WARP`；9个入口的两组候选目标第一数值均等于同ID场内创建的 `floorid`，而9个场内返回数值第一项均等于同ID入口创建的 `floorid`。这是**同包原文本静态数值交叉**，并非原游戏玩家已能通过、实际传送或比赛运行。
- **成员召集：** `npcgen_fmpkcallman` 5份原参数各有一组 `WARP`，其目标第一数字与该创建配置 `floorid` 同值；文本可见与家族相关消息字段，但未证召集实际发生。
- **赛程：** 5份 `scheduleman` 参数 `id` 恰为 `{11,12,13,14,15}`；5份共有原字面 `loopinterval=1000`、`challengetimeout=1200`、`settingtimeout=60`、`fightinterval=60`。这些是源**整数**，时钟单位、真实调度与计时规则都未执行验证。
- **庄园：** 4份 `manorsman` 的 `id`/`manorid` 为 `{1,2,3,4}`，原数字 `challengewait=86400`、`peacewait=172800`；没有运行依据就不把这些值换算成精确等待天数，亦不证明2004年某官方版本上线。
- **宠物转生与骑乘：** 1份 `npc_transmigration` 参数 `777/ten.arg` 实际包含4组原地区参数 `Item` / `Pet` / `Present` / `Warp`，1个 `PETTRANS` 字段标头和6个 `TENSEI` 编号段。原繁体对白中**有关于二次转生可能导致不能骑乘的警告**，现只记录「原脚本文字如此描述」，并不把这句话当作已实测生效的服务器判断器。

## 任务停止条件与交接

已取得同源参数均实际解析并通过原字节/数值关联核验；同包缺失的4条 `riderman` 具体服务器运行实现需要新的原代码、行为轨迹或合格同部署主表才能提升。原 NPC 类别并不等于全部版本家族PK场地数量，原读取到的4类机制也不能自动投射为日本JSS1999、台湾1.0或大陆1.82官方原玩法。当前 `GAMEPLAY-MECHANICS` 仍**SOURCE_BOUNDED_PARTIAL**，不是完成全部玩法。

公开派生 [GAMEPLAY01完整来源数值索引](../../research/recovered/STONEAGE-GAMEPLAY01-ORIGINAL-FAMILY-ARENA-PET-REBIRTH-R1.json) 有37份配置来源、33份原文件SHA/CRC与逐字段数字；公开自动测试仅检查已发布的来源衍生关系，不能直接证明CI读取原商业ZIP或实际启动原游戏。

**最高 NEXT：`GAMEPLAY-MECHANICS-MODULE-02`**，继续宠物成长、战斗、技能、骑乘等有已取得原数据／客户端程序证据的规则源，按版本分离，不针对缺失原服材料无止境深挖，也不提前开发新石器。Stage A 7 PARTIAL + 2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING、overall_percent=null保持。
