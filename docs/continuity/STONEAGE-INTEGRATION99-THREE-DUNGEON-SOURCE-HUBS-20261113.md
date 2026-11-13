# INTEGRATION99｜三组原地下城配置的共同楼层编号（2026-11-13）

## 原版内容增量与证据口径

以远端主线 `9d0cb1c468cc939606adaac2790ac87853a00b66` / tree `27154c2f1f71b0bf00b6f5b4e864e25747bb4eee` 及Git原生读取的完整历史 `docs/CURRENT-STATE.md` blob `c89e0e33537990aa2132b47c40fef49a985a935c`（2,709,173字节）作为出发点。已核原连续性协议、路线及 INTEGRATION98 正式接受记录。该大文件不重写。

目标是把此前三个**独立归档的原NPC创建配置来源**——dungeon00（INTEGRATION95）、dungeon01 的7个守门人（INTEGRATION96）、dungeon03（INTEGRATION80）——通过同一保存载体中的**原楼层数字**建立一张有限的跨配置关系表。这是 Stage A 的真实内容来源**整理/关系集成**，不是发现新的原像、原客户端运行或新游戏实现；本次并未重新读取私人原始 CREATE / RAR / DAT 字节。

## 精确输入与新关系

三份旧报告均有各自此前的私有原文件SHA核验及公开只含派生字段的Git文件；本轮按本次HEAD从Git重新读取并锁定原Git blob SHA：

| 原文件组 | 以前证实的源CREATE/handler范围 | 此次输入Git blob |
|---|---:|---|
| [dungeon00 / INTEGRATION95](../../research/recovered/STONEAGE-INTEGRATION95-DUNGEON00-147-ORIGINAL-WARP-AND-PRIOR-DAT-R1.json) | 147条原静态warp创建记录 | `285857ec36ffe7cdadec5f6093a861ed0e5be05a` |
| [dungeon01 / INTEGRATION96](../../research/recovered/STONEAGE-INTEGRATION96-DUNGEON01-SEVEN-WARPMAN-ORIGINAL-SOURCE-R1.json) | 7条原守门人warp目标（原CREATE共有257条，另250条静态warp**不在本索引**） | `f98ebaad7c730df91737f293f109dc4eda7a3bc3` |
| [dungeon03 / INTEGRATION80](../../research/recovered/STONEAGE-INTEGRATION80-DUNGEON03-NPC-WARP-DAT-SOURCE-R1.json) | 13条原静态warp创建记录 | `af8bfb07a1446cde2cdd727a57e032c6b77cc13b` |

三组共有 **167条**已经提取的源记录、**78个**源或目标楼层数字。按同楼层编号做跨文件并集，公共编号仅有：

- **100**：dungeon00 和 dungeon03，参与的已记录源边/目标边19条；
- **200**：dungeon00、dungeon01、dungeon03，参与的已记录源边/目标边7条。

这26条被公共楼层触及的记录，逐条保存原索引行号、源/目标楼层及坐标、旧CREATE块哈希（守门人另保存旧原handler完整SHA）至[机器索引](../../research/recovered/STONEAGE-INTEGRATION99-THREE-DUNGEON-SOURCE-HUBS-R1.json)，不发布商业文本。将全部167条记录不分方向地只按静态原目标成图，得**7个弱连通分量**，规模为 **46、10、9、8、3、1、1个楼层编号**。它是有限配置关系图；将条件守卫目标当普通边只是研究上限，不表示玩家能走这条路。

## 反例与止点

- **楼层100、200的原DAT地图字节未由三份专项索引资格化。** dungeon00旧MAP04的相关端点标记为未取到DAT；dungeon01守卫楼层200亦未取到对应DAT；dungeon03本次引用的5个原DAT也不包括这两个公共编号。因此只有数字交集，**无法证明同一地图实际可见、坐标通行或三文件曾在同服加载**。
- dungeon01本次只有**7个守门人**的handler目标，不把其另250个静态warp CREATE算作已并入本图；必须补齐原配置行才能修订本次覆盖。
- 所谓弱连通**仅**源脚本静态数字图；原 FREE/ITEM/ENDEV 门槛、时间、传送触发、实际人物移动、碰撞和原生客户端画面均未执行、未证明。
- 三份原件源头同后期**社区保存 mixed2.5**父RAR（旧来源SHA `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`），不是已验TW1/JSS1999、初代大陆1.82同构建。不能把跨文件共同数字当历史官方同时上线证据。
- 原商业CREATE、对话、二进制和2D像素均未添加到公有Git；不更新已验旧记录，不冒称本轮重新提取原件。所有结论标为 **SOURCE_DERIVED_PARTIAL**。

## 核验与后续

新 `tests/test_stoneage_integration99_three_dungeon_hubs.py` 会在真实Git checkout中重新读三份旧源派生文件，核对Git blob字节、逐行交集、167/78、7个弱分量/规模、公共楼层26条记录和上述负证。**本报告写作时CI尚未运行，不能先报成功。**

阶段边界仍是 Stage A **7 PARTIAL+2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、总体百分比未知。**NEXT**转另外一个有新增原实物或者真实二维像素增量的宠物/NPC/任务/地图家族；只有拿到对应楼层100/200原DAT及同来源运行证据才重开可达性，不重复扩大这份静态图。
