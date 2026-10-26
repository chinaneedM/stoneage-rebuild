# R32｜2003历史两版地图110实际三格差异来源资格

- 本轮起点由远端新读：main `05eb85bb59b2abcaba13b9614dedb37a27f3ca16` / tree `227a49182878cffac54f1120f11be6dceaf2aed0`；CURRENT全量Git blob `031c76a5a8e431f646853909bb2f2e11e6328cd2`，旧主簿均保留。
- **游戏可见对象**：地图内容随版本改变的一个具体区域。**缺口**：旧三状态全图索引已知110.DAT第三平面差3格，但未保存真实原值、新值及原数组索引。
- **原始范围**：2003-06-23 / 2003-12-10两份Wayback历史下载镜像的 `map/110.DAT`，不是TW1.0官方商业原服务器地图，也非单线版本升级证书。旧三态证据保留2003-06=保存混合2.5 whole-file hash的结论，仅是既有保存样本比较。
- **实源门槛**：仅一次实取两份小型历史map.exe，分别全SHA核，静态提取110.DAT后以旧 `STONEAGE-2003-MAP-TIMELINE-R1.txt` 全文件SHA对齐，46×45×3×u16严格全长解析。保留全部三个变化的索引、行优先假设xy与旧/新整数；两个未变平面分别全SHA固定。
- **停止条件**：仅三格原变化并通过独立校验、永久只存衍生少量数值/哈希；若原件服务拒绝或SHA错误，写精确失败而不伪造格值。大盘、游戏原运行、任务/NPC/材质所属语义、原地图名称及第三平面游戏内意义均不得无源推测。
- 旧地图R21四地图1000/2000/3000/4000已验，因此专选未覆盖的110；本轮不重新发明资源别名扫描、TW85全42文件或引擎帮助器。

本源工作流可通过专用分支 push 运行；成功后才固化源作业ID、三个实际格值、raw衍生JSON校验及独立离线拒绝语义反例，再合入main。所有旧CURRENT、设计、来源/历史研究文件不截断覆盖。Stage A 7PARTIAL+2OPEN、B/wiki GATED、R79与P3E暂停、百分比未知。

## 源实物三格材料与性质（2026-10-26）

源工作流第一次 `40335438563` / job `121615630195` 失败：6月map.exe完整SHA通过，12月map.exe完整SHA通过，但12月SFX的`7z`路径提取失败。错误保留，不当“数据文件损坏”。沿旧timeline工作流采用`unar`备用静态解压，修正后的source HEAD `b6eb278ac15833fa346ba1907edb145b1154a3e1`、run `40335682973` / job `121616477087` 实际completed/success。

源完全重取并核原包 SHA，6月 `372426e46765a1cf479041bdafc1d3e58fb019117d00d0b43d6a5f796620776e`、12月 `5f7f58e0d26d596e926a7d551d7c24e8a9a27824d5bdc53be3955b19b0e13abc`。静态提取`map/110.DAT`后各原文件 SHA `7d3e4e1dd8582268e14b3d21d0b0594c166f28062b05c8af260a6b214c41930d`（6月）与 `c2890121aa58447941b45c3e5041b444f22648bcef4403cb9ab18f6adbf41b7a`（12月）逐包符合既有三态材料。该页只保留有界派生，不保留原安装器与地图格网。

结果：46×45=2070格/平面，三个ordinal LE u16 平面均逐字节检查。第一平面两来源同SHA `17345f1fb0847c6ed849777f0a31cd9835c67529b0e15cfd8c61ba99ae5fc082`，非零格1416；第二平面同SHA `eeeba192bccfd84c8ce93e7a45fb91d6a7fdc7d52d1f9b880913d0438b346b01`，非零格934。第三平面旧SHA `a678eb37a26d028b05a507e8ab88c0247d0a495328ddeaecbeb81f49e0d08e88` 与新SHA `3aea662f23ccd0ba298743e9e67eba481909ae1ed7ed7a02b9610553fe4cecfa`，非零格各2070，仅三个原数组位置更改：

| 原数组flat index | 候选row-major (x,y) | 6月原u16 | 12月原u16 | 十六进制 |
|---:|:---|---:|---:|:---|
| 1 | (1,0) | 16384 | 49152 | 0x4000→0xC000 |
| 2 | (2,0) | 16384 | 49152 | 0x4000→0xC000 |
| 3 | (3,0) | 16384 | 49152 | 0x4000→0xC000 |

三个数值是原逐字节读取事实，不代表这就是“事件触发”“地形阻断”“新任务”“传送点”或游戏真实屏幕坐标。**HYPOTHESIS**：两整数存在同值附加位，但原实际读者与语义还未鉴定，不能由编码外形推行为。旧三态June=保存混合2.5的whole-file SHA是旧证据，12月差异不建立线性官方补丁先后关系。

独立下载源工件`12656672965`：ZIP 1209字节/SHA256 `580bef79d991ebf35fb826d3718d87a5864ccab1b1119fdf2a6b5005857bb92f`（与API相同）；唯一元数据成员原样2832字节/SHA256 `b7fcd1f5d134ddcdbe11303e95c8fda78d3d431a14b3018dda19adb2f7ea40f0` / Git blob `a3fac4f5c08d1b0660f302f95901a7d7fb2bee18`。永久派生报告路径 `research/recovered/STONEAGE-ORIGINAL-MAP110-CELL-DELTA-R32.json`，完整取证摘要 `research/recovered/STONEAGE-ORIGINAL-MAP110-SOURCE-CUSTODY-R32.json`。合成源解析8项测试通过；后续离线独立guard固定原三态文本blob、包/文件SHA与三格、坐标边界与nonzero守恒，拒绝跨源冒认。没有原DAT或SFX入公开Git。

本R32是实际源数据的新逐格内容结果，非对旧整图差3的抄录。本包停止地图叠层/helper扩大，**最高NEXT `ORIGINAL_SPR_RD_PALETTE_SAME_CARRIER_33`**：回原图像可视域，有限核对R30当前灰度八帧与保存样本同源的原调色板索引/RGB实际选择关系；无同构建证据就明确保留灰度和重新轮换，避免反复下载1.145GB或渲染猜色。用户指定任务本体/永久版本新增/运营活动/起源待考四档继续分离。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、P3E BLOCKED、R79暂停、percent=null；候选/main CI不得预先写SUCCESS。
