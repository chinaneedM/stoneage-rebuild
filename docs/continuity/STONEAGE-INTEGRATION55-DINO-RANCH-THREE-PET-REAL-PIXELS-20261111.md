# INTEGRATION55｜恐龙牧场三色宠物任务：原脚本、两个宠物表与台湾1.0真实动画的实物关联（2026-11-11）

## 目标、重新核验的最新远端状态

从真正 GitHub `main` `ac262f06d8d32ecf75d0bfec773d4f0bc2123f85`／tree `954b0a6b8ae44cad8dd0a51fe294800de1dedfb1` 起步，重读远端分支、HEAD/tree、最新提交和Actions，读取 `README`、原历史 `CURRENT-STATE` 完整原Git blob、全部协议启动文件、模块优先级与最新INTEGRATION54正式验收。无开放PR。继矿山、龙之巢穴和百人道场后，本批推进独立真实内容：**恐龙牧场**`jaruga/event/bait01.create`六名NPC、楼层201/20901、三个候选宠物的凭证脚本，以及独立台湾1.0零售的三组真实宠物动画。重点是原图实际可见与来源边界，不猜造原玩法执行或首发版本。

## 本轮实际取回的两份私人原实物

- 重新下载 `StoneAge-QUEST17-dino-ranch-original-private.zip`，**29,802字节／SHA256 `07fac6014b9eeef0a352d8c7b74f2fb1ac47cd97347ed796d16a0c7a52243081`／32个ZIP成员全部CRC成功**。包内10份原NPC CREATE/脚本、16份原物品两主表候选行、4张原物品RD已解码PNG、完整公开派生索引。实际核该包内公开派生索引的Git blob **`20bae57956e9b3a25df94a71f47fff0641b81b4d`**，与仓库源文件相同；直接从原三个`bait_03*a2`脚本再次按CP950实读出`DelPet:PET>0-560/559/558*4`、`*3`、`*2`、`*1`四种字面参数及`NotDel`、`DelPet:EVDEL`。**这些是原脚本字面，不证明服务端原生完成兑换。**
- 重新下载 `StoneAge-PET07-original-sprite-private-catalog.html`，**15,123,277字节／SHA256 `58e8ee4ff5165ed2f61663d67ae1cd0a8183622fa3375c480232784bfce9dc76`**，以及其私有源RD凭据`StoneAge-PET07-private-original-RD-verified-source-report.json`（1,617,404字节／SHA256 `b5ad2e58930afbe90604a1d72e3c17ab0adea446e7c118be775e3973315e6cb4`）。实际从HTML内嵌原PNG字节取出48张源图：三组各16张，全部以私人源RD凭据`PNG_SHA256`、原宽高及公共PET07源RD_SHA作严格交叉验证。本轮**只是重新打开并验证以前真原RD已解码像素；新增原RD解码为0**。

## 三条有来源的角色、宠物、凭证关联

| 晚期社区原NPC脚本 | NPC原楼层与位置 | 宠物条件原号 | 同保存档两表候选图号 | 台湾1.0原SPR组 | 原脚本凭证ID |
| --- | --- | --- | --- | --- | --- |
| `bait_03a2` | 201 (19,13) | PET 560 | 100271 | 261 | 2594 |
| `bait_03b2` | 201 (19,14) | PET 559 | 100335 | 305 | 2595 |
| `bait_03c2` | 201 (19,15) | PET 558 | 100368 | 334 | 2596 |

- 三个原NPC配置来自 QUEST17 同一社区保存档，原脚本各有独立全文SHA，源CREATE六名的另外三名楼层201／20901也保留在[公开来源索引](../../research/recovered/STONEAGE-INTEGRATION55-DINO-RANCH-THREE-PETS-TW1-48-REAL-PIXELS-R1.json)。原脚本指向的仅为**有来源的数值候选PET模板**；`enemybase.txt`和`enemybase2.txt`三种模板各**一条，原图号和行SHA一致，且PETFLG字面=1**。但各原图号**也被其他模板行重用**，不能把一图号、一模板当唯一实际宠物物种、抓捕规则或官方基线。
- 独立真实台湾1.0零售原SPR原组 **261、305、334**，各原组56源动画序列，PET07选中原动作0/2/1且方向0。源动画帧位置分别 **16、17、54**，其中`100368`同一帧号码多次重复；**原不同bitmap各16张**，每组完整原SPR段SHA/顺序bitmap SHA和逐原PNG的RD来源SHA均可核查，绝不按位置数捏造54张不同动物图片或按三个组推“原服三种正式可抓宠”。
- 四个实物候选物品图号 **22114、22118、22120、24222** 也从此前QUEST17私包内直接逐原PNG散列核对。三个手环物品ID2594/2595/2596分别按社区原`itemset`两表行限定指向图号22120/22114/22118，再独立对照TW1原RD像素；另图号24222同时被多条社区原物品ID引用，**图号不是物品唯一ID**。这些跨版图只具**形象参考资格**，未证同一正式运行部署。

## 私人图集、真正后验保管与源缺口

制作1690×1260的私人研究对照图，展示上述三行原动物动作0/2/1的精选实际像素及四个原物品图标，图像SHA256 `a7c3799d4b883422a26eabe98d01c1f02541ed428451cdc654a784f3faa7cdcf`；并将48宠物原PNG、4物品原PNG、图集及私人逐文件SHA/来源收据共**54个成员**归档至`StoneAge-INTEGRATION55-ranch-three-pet-original-pixels-private.zip`，**582,786字节／SHA256 `970326a4169e5ffb6a9a70b8219162e6d59c319f1f151afb048781ebde9b23e8`**。资料已实际上传**个人Library**，再从Library**独立下载**，完成ZIP整字节比较、54成员CRC和全部48幅宠物原PNG逐SHA一致核验。私人原画、DAT、脚本、ZIP和图册不公开Git；公开只存原号/来源/sha/候选关系与测试。

本轮**没有重新取得并重读**楼层201与20901的原DAT字节；以前的MAP09原DAT SHA、尺寸仅以旧源索引资格引用，因此**这次不报告两张DAT的真实格数值、原地图场景绘制或原NPC实站位**。同样未亲身运行原客户端、原服务端、交换/删除宠物、原色板或原帧率。分支脚本`EVDEL`、条件优先级以及后备的`bait_03a/b/c`是否在任何真实服务器启用均OPEN。历史JSS1999、大陆1.82和台湾1.0的同一部署不认证。

公共交付：[有界数字和源SHA](../../research/recovered/STONEAGE-INTEGRATION55-DINO-RANCH-THREE-PETS-TW1-48-REAL-PIXELS-R1.json)、回归测试、此连续性记录和README追加；专项CI仅核过去已公开源材料的匹配关系，不能用来替代私人字节复读证明。

**完成条件与NEXT：** 牧场三条候选`PET`条件→原表图号→台湾1.0原SPR完整段→真读48PNG→原凭证图号/4PNG的可查接缝已完成，停止无新的源证据反复放大同一牧场/图号。下一批优先真实不同场景/村庄中尚缺原图实观的玩家可见对象；若前期MAP09源实物不可重取，则保持源DAT `NOT_REPLAYED_THIS_WORK`，不造场景。Stage A仍7 PARTIAL + 2 OPEN，Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING、overall_percent=null；历史`docs/CURRENT-STATE.md`完整2,709,173字节、blob`c89e0e33537990aa2132b47c40fef49a985a935c`不改。
