# 2026-10-25：R17原战斗地图SAB跨版无损差异来源补记

此文是 **additive checkpoint**。不可覆盖 `docs/CURRENT-STATE.md` 的2680510B旧历史；每轮按远端最新HEAD/树/全部CURRENT/roadmap重新判优先级。本轮从远端main `7691014ba336445ea5864d9e455e77d6447736c4` / tree `2ee91a75188da1dddf023a2281c9d495aba0684f`（来自真实本轮API调用）启动。最新main R16原数据接受 `40197382213` 完成success；协议blob `a064174339b7a4656efe00b4446a066fd7abf304`、CURRENT blob `031c76a5a8e431f646853909bb2f2e11e6328cd2` /2680510B、路线blob `c11eff237a8aaa1cc34488a6c3c7fcdd596f9ce2`。普通文件接口对CURRENT给空内容，已通过原生Git blob重新取到全文，绝不当成空文件。README、决策、年代、SOURCE-REGISTRY、NPC09与R16后验叠层均重读。没有用旧聊天SHA假设当前状态。

当前最高 `OFFICIAL-NAMED-CONTENT-MATERIAL-ROTATION-17`，先选PC战斗地图物理源关系作为一个**真正包含全部文件SHA的无损差异包**，没有新客户端下载；没有把网络论坛截图当实体身份。由已验台湾1.0零售源blob `564233902b10c60760d4f93b1ea65d4dd1469206` 与后期混合2.5已存档文件元数据blob `47157f638cce7023727035981da11f1faecc9c78` 取得 218 和220项完整战斗SAB；前者0..217、后者0..219。218共享数字文件名的SHA全异。438逻辑出现记录/436不同哈希；两个样本各145与146是本样本内部重复，跨样本没有同一SAB哈希。原件删除0B，所谓1608B仅重复分析/存储参照的理想预算；来源版别不混合。

2015资料站转载称北京华义2001更新时让用户下载 `battlemap218.sab` 和 `battlemap219.sab`，但本样本实际 `battle218.sab`/`battle219.sab`；原始官方HTML、同期原下载程序、SHAs和同构建归属没有获得，关联仅为UNQUALIFIED候选。游戏本体任务/常驻更新/限时运营活动归属严格按DD-028；零新增同版具名NPC/任务/宠物主表。源报告/可验证工具和规格见 `docs/specs/STONEAGE-BATTLE-SAB-CROSSVERSION-R17.md`；后续source/main Actions另据实际记录，旧历史失败不重写。

下一优先 `EARLY-OFFICIAL-SERVER-MASTER-DATA-SOURCE-18_OR_EXACT_DOWNLOAD_PAYLOAD_CARRIER`：只要取得一个确切可访问、发行归属可辨的原版实体主表或2001补丁载体才重开实际名字/任务/遭遇绑定；否则精确缺源转22域。Stage A7 PARTIAL+2 OPEN；B/wiki GATED、R79暂停、总体百分比unknown、禁止重复大型原客户端下载。
