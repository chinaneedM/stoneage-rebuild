# INTEGRATION52｜原1021道场：100 NPC＋200 Warp与实际原DAT格/原图候选的可核接合（2026-11-10）

## 起点、问题、止点

遵循[项目连续性协议](../PROJECT-CONTINUITY-PROTOCOL-R1.md)按远端`main`（当时 HEAD `170ac8e871831d5df038197af64f1101257856ea`，tree `f5175fccc02eee4d69fe12f3ebf2272a8ef5e309`）启动，重新取分支/HEAD/tree/最新commit/Actions/README/协议/设计/时间线/来源/模块路线/离线优先及最新[INTEGRATION51正式验收](STONEAGE-INTEGRATION51-PUBLICATION-ACCEPTANCE-20261110.md)。零开放PR，I51内容主线27/27实际success。GitHub contents接口对大文件`docs/CURRENT-STATE.md`返回空字串，但**本轮Git原blob接口实际完整读回**已有2,709,173B的 `c89e0e33537990aa2132b47c40fef49a985a935c`（返回文本2,317,877字符）并保留未修改；只做小型增量索引和README末尾指针。

在[INTEGRATION51的两百关静态NPC来源](../../research/recovered/STONEAGE-INTEGRATION51-TWO-ORIGINAL-100-DOJOS-SOURCE-BRIDGE-R1.json)中，1021已核实原CREATE共100个对战NPC/200独立Warp，但**未在那一轮重读原DAT和把NPC点位直接落在实际原格/图像上**。此前[MAP09来源资格齐全691幅地图](../../research/recovered/STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json)原本已经含1021、1022和1008的DAT与候选图像；本轮不重复宣称发现/解码它们，而是做之前不存在的**100 NPC／200 Warp位置→原DAT三平面字面值→可观测候选原图**逐点关联，并止于该具体玩法场景。

## 真正重新读取的原字节、原格和图像

- 从用户已保存的私人 `StoneAge-MAP09-691-source-ready-map-catalog-private.zip` 重新读取：**46,844,444B**／SHA256 `d84d0800dd600798769dfb7251a1d7816588ac061ccc27812ac64a37922d4a8a`，整**4,195 ZIP成员CRC**通过；内嵌`source-all-955-original-DAT.zip` **1,988,312B**／SHA256 `c079a1c25bfa11902b69c1f2839058d4fb20f025ef15c93f649f636c7e5f833a`，**955个原DAT CRC**全部通过。
- 原1021.DAT **351,656B／407×144**，原文件SHA256 `92abd0a38c5e876d985c33437a252358d1aaa812ce1da99f18752d0a97c81197`；原1022.DAT **1,358B／15×15**，SHA256 `0dbd23cc0d0e9c24266ca9f717206026305b469588dd2531b293cafad6603757`；原1008.DAT **9,608B／40×40**，SHA256 `59314790cd105a52b5d3cbb8eddc6c3423f2d3ed0c5ba62199cf49709648e49f`。这三个原字节均与MAP09私人dataset的逐原DAT base64**全字节一致**，且与[MAP01公开成员SHA/尺寸目录](../../research/recovered/STONEAGE-MAP-SCENE-MODULE-01-ORIGINAL-SOURCE-MANIFEST-R1.json)一致。**此轮新取得原DAT=0**，是已保存原件的针对性重读。
- 对前次I51 **100份原NPC CREATE坐标和200个Warp CREATE坐标**共300个源配置位置，实际访问1021 DAT里的原始三个`LE_U16`平面值：**300个坐标两两不同、全在407×144范围内、全部平面0值大于99、平面1均为字面0**，第三平面只保存原`u16`字面，**绝不解释成碰撞、触发条件、人物进入或对话机制**。100个NPC点的平面0值分布：`4008:55 / 5062:21 / 5087:24`；100个Warp A点：`4000:23 / 4007:24 / 4008:53`；100个Warp B点：`4003:23 / 4008:77`。这个与确切原地图格值的交叉验证是本轮主要新关系，旧I51没有它。
- 从同一私人原DAT直接读取静态目标`1022(1,7)`格 `[4085,0,49152]`、`1008(20,20)`格 `[5046,0,49152]`；这些仅是配置指向的原格存在证明，**不是原客户端实际从100关胜利转移的实测**。
- 从MAP09内原保存台湾1.0 RD经旧验证得到的PNG图块读出局部候选，逐候选原PNG SHA与RGBA SHA对上同包`private-image-source-records.json`，本轮六个取景局部使用**137个不同原图源别名**：1021原关卡1/10/51/100四处，1022入口一处，1008终点一处。先按MAP09候选`x'=origin_x+(x+y)×32`、`y'=origin_y+(y−x)×24`、先平面0后1且逐对角的源原序重放，生成六幅 **720×520** 私人局部候选；图中红色十字和数字为现代标注。另有1021整幅旧MAP09缩略图叠加100个来源NPC点的现代导航图和六图合成画廊；实际人工检查图样（道场地面、门、入口围栏等）。**并非原客户端截图、原显示顺序/配色定论或NPC贴图。** 原DAT第三平面不在候选图层中。

逐关全部**300个DAT字面格值、100个与I51相同的原arg SHA/坐标引用、三原DAT摘要、六个局部无标记RGBA摘要及私人图/回放收据摘要**见[公开数值与负证源索引](../../research/recovered/STONEAGE-INTEGRATION52-1021-DOJO-ORIGINAL-MAP09-300-CELL-PIXEL-SOURCE-R1.json)。无原字节、原png/jpeg、原NPC对白、私有HTML或合成画面进入Git；公开CI只能验证源摘要/数值的跨旧记录一致性，不能重复读取私人原像素。

## 私人原图保存、复核和严格来源边界

私人包 `StoneAge-INTEGRATION52-1021-dojo-map-NPC-source-private.zip` **3,050,639B**／SHA256 `717a5af82fe66e47d0b929b25546be41f41282889f377beeff3a974703b95563`，13成员CRC成功，保存在用户Library `/石器时代/`；重新从Library实取之后**全包SHA、逐字节一致和CRC实际复验成功**。包内为缩略总图、六局部候选PNG、合图、完整私人回放来源收据、原I51纯派生索引、私人重放脚本/说明；原MAP09独立大包未重复封装。私人画廊亦独立保存在Library，便于无需运行原客户端的人工查看。这个私人研究交付**不是新游戏的原素材分发**，不应放入公开Git。源图像早在MAP09已有：**新增实际原RD解码=0**，**新增“NPC落在原图/原格”的可观测内容关联=300位置/六取景**。

来源身份不可合并：地图DAT和NPC源于后期社区mixed25保存资料，图块源于另一个台湾1.0已保存客户端；原始官方同部署、JSS1999／大陆1.82归属、原碰撞/移速/到达条件、原战斗、胜败、奖品、100 NPC源配置是否被原生加载全为**OPEN/未证**。旧MAP01的3021.DAT读取失败（预期351,656B、实际327,680B，`File CRC error`）仍原样保留，本轮绝未据1021图像捏造3021场景或抹掉该失败。

## 验收、止点和下一项

`tests/test_stoneage_integration_module_52.py` 已在本地实际执行**12/12成功**：对I51 100个原CREATE/源文件SHA、MAP09三DAT全SHA/尺寸、300格分布、1022/1008精确目标、现代投影、六候选局部摘要、3021旧否证和原生/版本界限做来源回归。专项GitHub Actions候选/PR/主线与正式验收需依据实际运行记录再写，不预宣称。

**本包到此止点**：1021原图原DAT、NPC和独立Warp精确位置与前述两端目标都已证据限定联接；不继续针对相同道场凑纯数字清单，不做原游戏碰撞/胜利/剧情的无证实现。下一工作包必须是另一处有真实**新内容关联或新的已保存原字节/像素**的玩家可见场景（优先尚缺原NPC、地图、原物品/宠物图的实际链），无实体则记录缺口并轮换。不得把本包误记为原版百人道场已可游玩。

Stage A **7 PARTIAL + 2 OPEN**；Stage B/wiki **GATED**；R79 **PAUSED_NON_BLOCKING**；overall_percent=null，旧历史状态完全保留。
