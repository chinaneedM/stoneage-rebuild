# INTEGRATION109 — `kingwarp.create` 309 条原静态传送配置与旧 DAT 几何边界

**日期**：2026-11-14。**证据等级**：后期社区保存载体真实原文件（FACT_SOURCE），不是 JSS1999 / 台湾 1.0 同服证明，不是原程序运行。只做 Stage A 历史内容还原，没有新游戏功能。

## 远端续接和独立原字节

从 GitHub `main` 精确 HEAD `fa080c78bbf5823b2239f51a5866fcac288150d7`、tree `3db40611cc73d16254bf650e74893dd50de610dd` 启动；0 开放 PR、此 HEAD 26/26 Actions 完整 `completed/success`。按原协议全文读取 `docs/CURRENT-STATE.md` 的原生 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` / **2,709,173 字节**；此轮不修改它也不以旧聊天作状态源。

个人 Library 已有 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip` 实际提取校验：完整 ZIP **995,176B**，SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`，**2,205/2,205** 成员 CRC 无错。直接读取其中 `npc/genout/kingwarp.create` 原 **36,355B**，完整 SHA256 `33f29f58215d07e139df4cd94b8a9b8bacb87b0acdebba58af704a3174712983`，原 ZIP CRC32 `31c690a2`。没有重取 361MB 原 RAR，也没有把原游戏商业脚本放入公开 Git。旧 `CHAR01` 原 RAR / 原 NPC 的载体属性继续以先前仓库保管账为准。

真正逐原字节提取 **309** 个 `NPCCREATE` 配置块，均为 `npcgen_warp` 的来源参数：逐块固定原 byte `[start,end)`、SHA256、源 `floorid`/出生坐标、原 `enemy` 目标 floor/坐标，完整 309 条机器记录在 [无版权来源衍生索引](../../research/recovered/STONEAGE-INTEGRATION109-KINGWARP-ORIGINAL-STATIC-ROUTES-R1.json)。全部 **309/309** byte span、原块 SHA、起点 floor/坐标、模版 `npcgen_warp` 与已经正式入库的 `STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json` **逐条一致，0 冲突**。这份原文件不是本轮首次被保存：**新的材料成果是将原配置的目标坐标、方向关系与已有来源资格化 DAT 的边界联合核验**，不是报告 309 个新 NPC / 309 张地图。

## 实质静态来源图与拒绝推断

- **309 个原配置出现位置**中有 **261 个不同原配置块 SHA**；重复 48 个出现位置全部保留，不按数量当不同 NPC。
- **35 个不同 floor 数字**（34 个出发 floor），**75 个有向 floor 对**，**261 条不同定点有向数值关系**；以无向连通性查看是 **5 个静态分量**，floor 数分别 **11/9/9/3/3**。这是源配置图，不是原官方世界导航或可达性验证。
- **222/309** 条配置存在来源点、目标点严格交换后的另一条同文件原配置；剩余 **87** 条未找到同文件严格逆向配置。不能把这 87 条认定为运行时单程传送、封锁或设计缺陷。
- 将前述 **35 floor** 与已验的 `STONEAGE-25-STABLE-WORLD-CONTENT-COVERAGE-R1.txt` 原 DAT 保存索引核对，**26 floor** 有既存有效尺寸及原文件 SHA 元数据，**9 floor 缺该索引资格**：`300, 30605, 30607, 30689, 30691, 30692, 30693, 30694, 30695`。缺该索引不等于原世界中不存在地图，不能按缺件反推原运行规则。
- 现有资格 DAT 尺寸内：**出发点 268 / 268，目标点 264 / 264**；因缺上述 DAT 资格而不能验证的是 **出发点 41、目标点 45**；**有资格的越界证据为 0**。仅据以前保存的尺寸元数据对照，本轮 **没有重新读取原 DAT 任一字节**，没有读取三平面格值，不能声称碰撞/通行、原生传送成功或实际画面。

原生游戏、同服务器部署、真实地图指向、条件触发、原 NPC 对话、原二维图像、真正玩家操作均仍 **OPEN/UNPROVEN**。本轮新原 RD/SPR/PNG/可见画面 **0**；不把现代静态索引冒充可玩复原。原用户期望的单机复原仍属未来阶段，当前仅历史来源整理。

## 再现与停止条件

新增有限的 `tests/test_stoneage_integration109_kingwarp.py` 与专项 GitHub workflow，验证 309 原 byte-span/SHA 与旧 CHAR01 全记录精确相交、26 个资格 DAT 的边界、逆向匹配、重复计数，包含 SHA/坐标/越界伪造反例。检查只用已公开的来源衍生数值和 SHA，**CI 不分发商业原字节**。

**本模块止点**：309 条已有实物全部覆盖；剩余 9 floor 缺旧 DAT 资格，除非获得 CRC/SHA 独立合格的同载体原 DAT 或真正原客户端实测，不继续穷举同文件/补图像想象。**NEXT** 切换另一件有新独立原文件或真实二维可见证据的未重复宠物、任务、场景家族，避免连续做无新画面的静态图；不扩 MMO 登录、网络、服务端、引擎。Stage A **7 PARTIAL + 2 OPEN**，Stage B / wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，overall completion percentage **UNKNOWN/null**，全部旧历史及失败记录不改。本包候选和主线的 CI 只在远端真正发生后记录，不在本报告预写成功。
