# INTEGRATION54｜吉鲁矿山比赛矿工的原DAT位置与台湾1.0原二维动画（2026-11-11）

## 启动与本次真正复原的对象

本次按远端主线 `9a14e766380e17703eb4556f7c2e28e4934ae908`、tree `9d30d0727a8bf1bafd292f5d5d27083b4e34dea6` 和连续性协议启动，重新核对分支、Actions、最近正式验收、README、完整 `docs/CURRENT-STATE.md` 原 Git blob、路线、设计、来源和历史。没有开放PR。INTEGRATION53三龙来源桥已验收，因此本批转向另一组可见游戏内容：QUEST12 吉鲁矿山比赛里的矿工巴卡斯及地图31805/31806。**目标是对实际原DAT和图号100401的真实保存原图进行来源核对，不是原版客户端执行或新单机游戏。**

两份已经保管的私人原实物在本轮**确实取回并重新读取**：`StoneAge-QUEST12-mining-competition-original-private.zip` 共113,328字节，SHA256 `d93aea416ea40a336e9c05a7cd851dbfc557916322f00152d91224f717c54cd9`，**32/32成员CRC成功**；`StoneAge-PET07-original-sprite-private-catalog.html` 共15,123,277字节，SHA256 `58e8ee4ff5165ed2f61663d67ae1cd0a8183622fa3375c480232784bfce9dc76`。后一原图研究包的台湾1.0八幅图号100401候选PNG，实从内嵌PNG字节取出并解码，逐张SHA、RGBA尺寸与旧PET07真原RD收据完全相等。**这不是本轮从原商业RD再解码八张新原图**；只是新一次私人原图实字节观察。

## 两张原DAT、NPC和静态参数

真正从QUEST12原包读取`31805.dat`与`31806.dat`：各15,008字节、50×50、原格式8+6×2500；全SHA分别 `1766c7d378fdde4bcc2eb45a827cd33e2b2f967b32eae752cbe76372c49c0261`、`a4c0899bd89f66b3fe918af1702f72fc9c997789706db936811096e74819571c`。逐原字节重算五个位置三平面原值：

| floor / (x,y) | 真原DAT三源平面 |
| --- | --- |
| 31805 / (19,21) | [4200,0,49152] |
| 31805 / (33,23) | [4301,0,49152] |
| **31805 / (26,23)** | **[5068,0,49157]** |
| 31805 / (22,4) | [4302,0,49152] |
| 31806 / (34,6) | [4305,0,49152] |

矿工原CREATE完整SHA `3bd43fdb15482cbde4896ded79c5382b777f8e74fe0c0637b97bfa0034613388`，独立块SHA `a9131ce63efe1ddd3d71010f27588dbba0c471ad3c623aae42d6925706a04fe7`，字段`floorid=31805`、`borncenter=26,23,1,1`、`graphicname=100401`、`dir=6`。`300/sb_bac.arg`全SHA `93b2893ee9cf5b0229072a9283f8fbb703004cbc2ec3829fb35af71ebdf1bc30`，源字面`entype=2`、`item=2535`、`steal=1`、`enemyno=1004`、`time=300`；许可证门参数字面`WARP=31806,34,6`、`FREE=ITEM=2527`、`DelItem=2527*1`、`MONEY=-1`。不能因此断言原NPC实出现准确点、矿工掉落2535、许可证已扣除或原生传送成功；第三平面值不可直接叫碰撞。

## 新的关键可视来源与原图缺口

独立**台湾1.0零售**原SPR组100401的索引为**364**、原完整SPR段SHA `0284af96efdff07da2b5b73ccc3f8a84a2a4158e9c653e3a4f3977293f3ec2a4`。先前PET07记录该组104段来源动画、动作0方向0为26原位置、动作2方向0为6原位置、动作1方向0为2原位置。**本轮私人HTML实际严谨显示8帧：bitmap82737—82742（动作2/方向0）和82743—82744（动作1/方向0）**；均已逐原PNG重新取得、实解和源散列重核。独立原图片是可见候选，不证明晚期社区任务中的矿工在真实游戏里加载了这份台湾1.0图像。

需要明确避免误升级的缺口：PET07原动作0/方向0的**26位置序列**因bitmap**82729**严格RLE解码溢出而拒绝显示，原RD SHA `f8f7e0b754e3b454a31546eb181adc9fcd9cf2f946e6b02af82bcbc7eddf687a`，原错误`STRICT_RD_RLE_DECODE_OVERRUN_NO_PIXEL_FABRICATION`。后来PET15将此位图作为**bounded terminal-zero**处理，因此记录全组104段可观察／496位置／344组内不重复bitmap；但它**不能倒写成此前PET07已严格无损恢复82729原像素**，原始RD语义仍待核验。本次不虚构第九帧，也不认定原生动作播放速度或色板。

另在后期社区的两份`enemybase`原表，图号100401均对应候选模板500、544、713、719，**模板719的PETFLG主表=1、备表=0**，整原行SHA不同。不能把这名矿工按同数字自动识别为单一宠物物种、可捕捉对象或已认证同服角色。

## 私人保管与止点

制作一张来源并列的现代研究图：左边为QUEST12已保存现代候选两景，右边为本轮真正重读的8幅台湾1.0原PNG候选，详细标明**不是原客户端场景截图**。私人`StoneAge-INTEGRATION54-Giiru-miner-map-TW1-sprite-private.zip` **593,529字节、10成员、SHA256 `3d296aea5359ecfa13f1e17857f42923208272374c070bd475c0c1bca07805fe`** 已保管在个人Library，**上传后重新独立读取整包SHA、全部CRC及每张PNG SHA均匹配**。研究图完整SHA `1516e83cda96ca3a3622fad7f96f89b36f17f30a4d3de50325216459c2973a2a`。真实DAT、原商业PNG、NPC原文、私人HTML和ZIP均不提交公共Git。

公开仅提供[来源数值/原SHA及负证索引](../../research/recovered/STONEAGE-INTEGRATION54-GIIRU-MINER-DAT-TW10-REAL-PIXELS-R1.json)、合同测试、此文及小型专项Actions。GitHub公开CI只能核已发表证据之间的关系，不下载私人游戏图或重跑商业程序。

**到此停止本矿工/原图号的重复观测。** 除非获得82729更强直接RD解码证据或同部署原客户端渲染，原生身份与动作仍OPEN。最高NEXT转另一组有真实原图片/地图/NPC材料的游戏内容。Stage A 7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，总体完成率未知。完整历史`docs/CURRENT-STATE.md`原2,709,173字节blob `c89e0e33537990aa2132b47c40fef49a985a935c` 不改。
