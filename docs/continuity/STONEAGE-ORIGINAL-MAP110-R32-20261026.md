# 2026-10-26｜R32两份2003原始地图110三格材料与真实来源

此为协议§14加法覆层。fresh main `05eb85bb59b2abcaba13b9614dedb37a27f3ca16` / tree `227a49182878cffac54f1120f11be6dceaf2aed0`，远端完整CURRENT blob `031c76a5a8e431f646853909bb2f2e11e6328cd2` / 2,680,510字节；协议、README、设计、历史、来源、路线以及R31最新验收/22域重新读。R31自身run40334294230实际成功，0开放PR、没有该HEAD的未决工作流。本轮未覆写旧CURRENT/任一巨型主簿。

**最高目标R32**：恢复地图110从2003-06到2003-12的三处实际内容原数值，而非再次报道旧timeline的3格计数。2003-06与2003-12两份原始map.exe经SHA重新获得，静态提取DAT并原SHA对齐。第一次source run40335438563/job121615630195 因December 7z exact path失败而失败；修正静态unar兜底后的run40335682973/job121616477087完成success。旧失败保留不可重写。两个原包来源有时间存档链，但不是台湾1.0官方地图，不执行安装器/游戏程序。

46×45地图三个LE uint16顺序层完整6210单元比较。第1层0变化，第2层0变化，第3层flat index1/2/3旧16384→新49152，都是顶行row-major候选x=1/2/3,y=0；第三平面非零总数2070保持，旧文件与已保存混合2.5全SHA匹配仅原有谱系证据。三个格值真实新增而非猜测，但尚未鉴定事件、任务NPC、坐标变换与原色画面。正式地图/实体身份和StageA判断完全不变。

源工件12656672965 ZIP1209B/SHA256 580bef79d991ebf35fb826d3718d87a5864ccab1b1119fdf2a6b5005857bb92f，**实际独立下载**与API一致；只有衍生JSON2832B/SHA b7fcd1f5d134ddcdbe11303e95c8fda78d3d431a14b3018dda19adb2f7ea40f0/Git blob `a3fac4f5c08d1b0660f302f95901a7d7fb2bee18`，原件不入Git。完整来源/负例见[实际规格](../specs/STONEAGE-ORIGINAL-MAP110-MATERIAL-R32.md)、[派生JSON](../../research/recovered/STONEAGE-ORIGINAL-MAP110-CELL-DELTA-R32.json)与[原件保管链](../../research/recovered/STONEAGE-ORIGINAL-MAP110-SOURCE-CUSTODY-R32.json)。候选与main验收须据实际完成后另记，不伪造绿灯。

**NEXT `ORIGINAL_SPR_RD_PALETTE_SAME_CARRIER_33`**，按协议§13回到玩家可感知的画面内容：先明确已有R30真RD索引图是否能由同保存构建的调色板资料恢复史实RGB，不能就止点，不能只是反复做声卡/显卡helper或猜物种。任务四档、Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79/P3E、私人载体长存不足、整体percent=null不变。


## R32实际候选/主线双重验收与位级限定（2026-10-26）

已用未变main HEAD租约非强制快进合入内容 `cffeea30c25f6b33d3c465fe7ce457edf8437a76` / tree `5c7472c159f15e3100d39bb4df84cb363c681a79`。候选和内容主线各七项Actions经实际查询均completed/success，其中主线专用R32 run `40337093816` / job `121621478096` 完成19项源解析与离线负面合同测试及原历史文本pin核验；候选对应run `40336922384` / job `121620870049` 亦success。R31、Stage A、R16、R17、R18、R28等兼容检查分别成功，具体十四项运行编号和状态记录在[本轮实际验收凭证](../../research/recovered/STONEAGE-ORIGINAL-MAP110-PUBLICATION-R32.json)。

源第一次`40335438563`因12月7z失败、修正版`40335682973`成功；中间`40336190397`把报告入库前就启动离线验收，因缺派生报告失败，全部原样记载。旧成功/失败不是同一HEAD，不能混作一次通行。原工件实际单独下载ZIP1209B，摘要与Actions API精确一致，只有合法的派生JSON2832B/Git blob `a3fac4f5c08d1b0660f302f95901a7d7fb2bee18`，报告内容与source stdout JSON相同且独立逐摘要核。主线从旧tree到内容tree恰11文件路径新/改，无旧文件删除；旧CURRENT和其它历史主簿Git blob未改。

数值上三个`0x4000→0xC000` 的XOR都恰为`0x8000`，这是位级**算术FACT**，但此位是否表示事件/通行/遮挡/动态状态完全OPEN，不能命名格子任务。地图来源为2003两批归档的第三方镜像，非TW1.0、非原服坐标；原地图原格网不存公开Git。下一优先原图片调色板同源实物包33；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、P3E/R79和私人原件持久保存边界仍在，总百分比null。后验收据自身提交的Actions须另依事实检查。


## 发布收据自身CI中一个保管防线误报的保留记录

后验收据commit `bdb95b2c322964a63d4054362d6779ea28f535b5` 触发R32 main run `40337484100` / job `121622844296`，前两步真实源码单元及独立派生重放均通过，但最后仅以`*MAP110*`文件数量`<=2`计数，因新增第三份**合法派生**发布收据而失败。这是原守卫过紧，不是源地图、DAT、SHA或格值错误。此次失败原样保留。修正为明确允许`CELL-DELTA`、`SOURCE-CUSTODY`、`PUBLICATION`三份JSON文件名的严格白名单，其他任意`MAP110`文件均拒绝，保持原商用载体不入Git的禁止边界；改动后的Actions须实际查验后再称通过。
