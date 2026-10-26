# 2026-10-25：R17原战斗地图SAB跨版无损差异来源补记

此文是 **additive checkpoint**。不可覆盖 `docs/CURRENT-STATE.md` 的2680510B旧历史；每轮按远端最新HEAD/树/全部CURRENT/roadmap重新判优先级。本轮从远端main `7691014ba336445ea5864d9e455e77d6447736c4` / tree `2ee91a75188da1dddf023a2281c9d495aba0684f`（来自真实本轮API调用）启动。最新main R16原数据接受 `40197382213` 完成success；协议blob `a064174339b7a4656efe00b4446a066fd7abf304`、CURRENT blob `031c76a5a8e431f646853909bb2f2e11e6328cd2` /2680510B、路线blob `c11eff237a8aaa1cc34488a6c3c7fcdd596f9ce2`。普通文件接口对CURRENT给空内容，已通过原生Git blob重新取到全文，绝不当成空文件。README、决策、年代、SOURCE-REGISTRY、NPC09与R16后验叠层均重读。没有用旧聊天SHA假设当前状态。

当前最高 `OFFICIAL-NAMED-CONTENT-MATERIAL-ROTATION-17`，先选PC战斗地图物理源关系作为一个**真正包含全部文件SHA的无损差异包**，没有新客户端下载；没有把网络论坛截图当实体身份。由已验台湾1.0零售源blob `564233902b10c60760d4f93b1ea65d4dd1469206` 与后期混合2.5已存档文件元数据blob `47157f638cce7023727035981da11f1faecc9c78` 取得 218 和220项完整战斗SAB；前者0..217、后者0..219。218共享数字文件名的SHA全异。438逻辑出现记录/436不同哈希；两个样本各145与146是本样本内部重复，跨样本没有同一SAB哈希。原件删除0B，所谓1608B仅重复分析/存储参照的理想预算；来源版别不混合。

2015资料站转载称北京华义2001更新时让用户下载 `battlemap218.sab` 和 `battlemap219.sab`，但本样本实际 `battle218.sab`/`battle219.sab`；原始官方HTML、同期原下载程序、SHAs和同构建归属没有获得，关联仅为UNQUALIFIED候选。游戏本体任务/常驻更新/限时运营活动归属严格按DD-028；零新增同版具名NPC/任务/宠物主表。源报告/可验证工具和规格见 `docs/specs/STONEAGE-BATTLE-SAB-CROSSVERSION-R17.md`；后续source/main Actions另据实际记录，旧历史失败不重写。

下一优先 `EARLY-OFFICIAL-SERVER-MASTER-DATA-SOURCE-18_OR_EXACT_DOWNLOAD_PAYLOAD_CARRIER`：只要取得一个确切可访问、发行归属可辨的原版实体主表或2001补丁载体才重开实际名字/任务/遭遇绑定；否则精确缺源转22域。Stage A7 PARTIAL+2 OPEN；B/wiki GATED、R79暂停、总体百分比unknown、禁止重复大型原客户端下载。

## R17 候选验收纠错历史

首次含文档门禁的候选 Actions `40198986497/job121185894377` 为 completed/failure：13个测试仅一项失败，原因是规格没有出现守卫要求的精确字面“同构建”，尽管原文已经说明2.5混合保存包的发行build无法鉴真。修订规格后，候选 Actions `40199112279/job121186270112` 已实际 completed/success；原始两份索引、438条出现、436个哈希、218项差异、2001公告转载证据等级均未改变。首轮失败保留可追溯，不追写成success。此次连续性补记提交本身的Actions需后验核实。

## R17候选／主线实际成功与失败后验（2026-10-25）

已从远端**实际检查**候选源报告、纠错记录及主线Actions，不是预填的成功声明。候选源索引校验 `40198686693` completed/success；首次加入文档门槛的 `40198986497/job121185894377` completed/failure（13项1项因没有字面“同构建”，来源档案无误）；订正后候选 `40199112279/job121186270112` completed/success；最终候选 `40199182374/job121186488104` completed/success，旧失败记录永久保留。

内容通过非强制快进从main `7691014ba336445ea5864d9e455e77d6447736c4` 发布至 `2d9565f96f101de2d3738cc473c2cb12cacaeeca` / tree `e52cc739f5b6aab29ec6428d5546bf8de01a7cd0`，9路径diff，Git原生全树5769条/truncated=false。同HEAD主线 R17 `40199244812/job121186678119`、旧R16 `40199244818/job121186677927`、StageA `40199244821/job121186677939` 三项均 completed/success。派生报告Git blob `215654d2a35bbd6add2a0316075c882fb7d83b69` /93155B，本包不依赖短期ZIP工件，Git直接保管438项已有来源归档的SHA/路径而非版权原载荷。原 `docs/CURRENT-STATE.md` blob仍 `031c76a5a8e431f646853909bb2f2e11e6328cd2` / 2680510B，路线 `c11eff237a8aaa1cc34488a6c3c7fcdd596f9ce2` 完整保存。主来源和所有旧失败原记录未删。

后验收据 `research/recovered/STONEAGE-BATTLE-SAB-R17-PUBLICATION.json` 固定这些**实际已发生**的来源与运行记录；本次后验提交自身Action结果继续以后续真实查询为准。下一项仍是获得确属同一早期地区发行版的正式NPC／宠物／本体任务主表，或认证2001编号218/219补丁原下载字节及文件名同一性；无源不造身份或运行历史。DD-028任务四档、Stage A7PARTIAL/2OPEN、Stage B/wiki GATED、R79暂停、总体百分比null不变。


> **2026-10-26 R24勘误：本节旧R17的218同号不同/436内容结论已撤回。旧工具混用了TW1去4字节头payload哈希与mixed804字节完整文件哈希；同域纠正为218同号全部相同、438引用219内容。原文和旧原报告保留作历史，现行事实见[四样本整合与勘误](../specs/STONEAGE-FOUR-CLIENT-CONTENT-R24.md)及`STONEAGE-BATTLE-SAB-CROSSVERSION-R17-CORRECTED-R24.json`。**
