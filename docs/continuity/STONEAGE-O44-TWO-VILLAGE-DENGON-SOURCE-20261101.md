# O44 — 萨姆吉尔两处原始「传言板」NPC配置、真实像素与两个局部世界（2026-11-01）

## 目标、去重与来源边界

承接已完成的 O43，按 fresh remote main `b52c45fe531d8ce9ce42eddeddcebfda549cba8a`、tree `0fb30cc8416bd4750119ece3f5115b48563ffd24` 启动，10/10 同 HEAD 主线 Actions 成功。整份 `docs/CURRENT-STATE.md` Git blob `20050acf279a01555ab06a381dfcdc936bd381a6` 为 **2,708,031B**，由原 blob 接口重新读取（普通 file 接口空字符串但不是空文件），本包**完全不修改**旧 CURRENT 或古早审阅记录。连续性协议的「简单工作不复杂化」优先：O43 NPC16209 的原图研究已止点，本轮不再扩普通 NPC 图像按钮，也不尝试重启旧商业服务器。

选择新的**村庄服务/世界内容**：一处真实来源的 `Dengon` 传言板功能模板与两处村内创建实例。来源不是网页猜图，实际完整 SHA 重读已有私人保存包：

- 既存 SCENE22 私人源包 1,321,290B，SHA256 `7c6d717de639937f3fc0482907cf501afe52ed600f70683b43a70920178110df`；其中原 `1000npc_m.create` 4,413B SHA `c9b000a836b0aae3d88358097039f1beea020d92ba84f6ccc338bb54bc478240` 与 `npcgen.template` 4,950B SHA `0c5a58d5e31cafd3b58ccc1fa88fee7d1f95d12c0b87b04db9f06fea3b2a4df3`；
- 既存 O31 包 2,295,731B SHA `f14ee7c362e74bb82fabb867bee08729b41f9744208642fd689bf2730d10548f`；原 `1000.DAT` 153,608B SHA `94b19cb59d72b7b48da70d2741ba68516caad970297fd48ed11ef720fa3ea97e`；
- 台湾 Waei/JSS 1.0 已验原 P3H 零售 ZIP 372,626,292B SHA `3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24`，本轮完整重 SHA；原 125,996 条 `adrn_1.bin` 10,079,680B SHA `47254c0ff904d363fb5c3c5297edf553c8eaf24cd933f346d8ce7aabed4155c8`，`real_1.bin` 315,842,228B SHA `408e6ee05c83354349691937da2ad8f7488ac10f65f07e6681b7d92cb1c9ed13`，`Palet_0/1.sap` 分别 SHA `89709d906bbd9cd9f5c2b8e0bd993e2897a1c9136ada2e211109983bb3b06cbf` / `32870080c47537a59beaf770b6df7bd79820fd52a23825058460900494f0b4b0`。

上述原服务端配置/地图来自**后期 preserved mixed25**，原图来自**台湾 1.0 官方客户端**。本轮没有重新下载、整包 SHA 重验旧 mixed25 361MB 父 RAR，继承前轮独立保存的子成员/保管证据。先前 TW1 对指定 mixed25 的资源前缀逐字节相同有旧已认证报告，本轮没有重读整 mixed25 REAL/ADRN。**原服务器与零售客户端从未认证同一部署构建**，不可把后期“传言板”推出为 JSS1999/TW1 初始服务。

## 真实源内容：两处不同的村庄留言板

完整解析该 `1000npc_m.create` 的 25 条创建块，其中有 **恰好 2 条** `enemy=npcgen_dengon`、都称「薩姆吉爾的傳言板」，创建 `graphicname=10062`、`floorid=1000`、`dir=6`：

| 创建格 | 原源块半开范围 | 原块 SHA256 | 原地图三 plane (tile / parts / event) |
|---|---|---|---|
| **(94,93)** | [4116,4259) | `96d47e70709db8dd29f397b9cdf40f884c052c5803c3e867b356e430d76d75a0` | **158 / 0 / 49152** |
| **(93,66)** | [4269,4412) | `b5686b1b8860d984bea2db50f40603c3a4c0f7effa56d3362aa87b7a2cc3981e` | **189 / 12928 / 49152** |

不是一条复制记录的重复计数，而是两个有不同坐标、不同块 SHA 的创建实例。对原160×160、三平面16bit `1000.DAT` 精确读取每格。功能来源是原 `npcgen.template` 唯一 `templatename=npcgen_dengon` 块 [641,759)，SHA `13a061836e331d8614aee783bd865f97566b89a8a909360daa99166c5d0a42df`，其中 `functionset=Dengon`、模板默认 `graphicname=2204`，而创建实例各有显式 `graphicname=10062`。**没有原生执行**来认定默认/显式绘图的优先次序。49152 不推断为碰撞/任务/交互标记；同一坐标的服务可用性、公告具体内容、发帖/阅读/服务器数据仍 OPEN。

## 原始真实图像与两个7×7微型原世界

完整扫描 TW1 原 125,996 个80B ADRN：`graphicname=10062` 与原 ADRN 尾 +76 数值同值的候选只有一条，物理 `bitmapno=4766`，记录 SHA `1687829432f16c0d719c7f4dc84a261ab4ca84dc34b6508cfe6b12beaefaeb9a`，REAL 源偏移 **13,813,099**、RD **4,808B** SHA `86cf8cce0e6fe22950c3d6acee9ba5cea977be90fce59011d400594d684af596`、实际索引像素 **64×107** SHA `4082d8337f81b4301f34f3a86ce9a1567a2353e0aa64906ca72fac87132412a7`，在私人候选色图里可见木制告示牌。

错误反例：按同整数直接读取物理 `bitmapno=10062` 也有原图，但是 **68×70 的人物像素**，尾 +76 别名0；RD **1,820B** SHA `fc8e32d2deeb2a05de4068a28bf81fdd73dbcdfb1a970b25128d5e0a42acaa0f`。两条都从原 REAL 实际取字节，用两套独立 RLE 算法逐索引一致；Palet0/1 初始色均为**离线候选**。不能因为“看起来像公告”就当原生 selector 的执行证据。

为了不再拼空白工具，直接取上述两个真实村格各自周围的 **7×7** 原保存版 DAT 窗口，98 格、tile/parts 总 **111 次需要绘制的资源引用**、合计 **65 个不同图号**。这些图号在**本轮完整实际扫描的 TW1 ADRN** 均有唯一别名记录；每条来源记录/RD/实际像素索引完整哈希及 private source bytes 已封存。原64×107告示牌候选分别与两个窗口做**现代独立叠加**，输出两个 map-only 与两个 board-overlay 的现代RGBA/PNG。两种 RD 解码核同，两个独立完整画面叠加反例同；这不是原版地图引擎、原生绘制顺序/遮挡/配色/缩放/触发的证明。现代合成的两个原图窗口已由实际 Chromium 解码，**13/13** 显示开关、图像还原、无 JS 错误、无外部 HTTP 校验通过；没有运行原客户端，`file://` 直接导航没有被认证。

<details><summary>局部 PNG SHA256（私人原图不进入 Git）</summary>

| 画面 | SHA256 |
|---|---|
| (93,66) 原图局部地图 | `0b4ab75dd0564e830a746ba8a30fca56cf1b5c34bc76497d59a1f88103b2a1a9` |
| (93,66) 附原告示牌候选 | `d18bdb859b3176eba16fc32fa47c0de7b957636b0811651d2510e67eb535ed06` |
| (94,93) 原图局部地图 | `3624e11aac9c2839aa0b333d8e915d1bc7344a516f3afa1b4cb02fb017f156ab` |
| (94,93) 附原告示牌候选 | `0906caab542fe6c89b131ca2c85f7b77617cbef7f738249d64dca73302e31177` |

</details>

## 实物私人保管、止点

完整私人 ZIP `StoneAge-O44-private-original-two-village-bulletinboards.zip` **1,532,715B / SHA256 `0b56e45087a820c0bfcf9546017c7c6dc2433e0e5d29ba036b1b06fbe65c1e9f`**，150成员，包括 65 组原地图 RD/80B ADRN 子记录、两幅告示牌候选RD、原 map/NPC/template/palette 源字节、局部PNG、两个真实图像窗口和单文件离线浏览器、原 Chromium 截图与含全部65图号完整来源记录的私有报告。已保存个人 Library `/石器时代/StoneAge-O44-private-original-two-village-bulletinboards.zip`，又从 Library 实际下载，同尺寸/整SHA/150成员 CRC 全相等。**原图/原地图/原脚本/私人HTML/截图不进入公开Git**。本包公开仅本加法记录、[有限来源和数值派生证据](../../research/recovered/STONEAGE-O44-TWO-VILLAGE-DENGON-SOURCE-R1.json)及README指针。ZIP **内部**全量65图来源报告 **49,519B / SHA256 `49e229f4f24bb772d73421df4ab0caf4f6fe758488a5f81722afbfa5bdf57cc8`**，独立保管后本地报告额外加入上传/回读身份字段成为 **50,238B / SHA256 `3c37071714f5d55a6165065cbf124961ad86f8f662e287290af42efc5fef963c`**（不是ZIP内部同一个成员），两者全部65条原图来源对象完全一致。其中65源记录规范化JSON SHA `cc9233bbf73f5618d28a1fd8f481aced670b1856569d1ed2a1bee6f69fd631f4`。

**状态不变：**Stage A **7 PARTIAL + 2 OPEN**、Stage B / wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、overall percent **null**。原游戏可操作世界与原业务留言内容未进入或恢复。**NEXT O45：**轮换到与当前已保存原件直接有关的一个宠物、移动/遇敌或实际任务规则缺口；无新的完整原源合同就按缺件停止。禁止继续在两个板上追加空白交互、公告文本、社交服务器或新游戏产品界面。
