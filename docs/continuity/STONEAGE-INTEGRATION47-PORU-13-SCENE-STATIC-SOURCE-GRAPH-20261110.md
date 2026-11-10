# INTEGRATION47｜波鲁地区13张原DAT场景与任务63／64的来源限定关系（2026-11-10）

## 起点与交付目标

按[连续性协议](../PROJECT-CONTINUITY-PROTOCOL-R1.md)从真正远端 `main` HEAD `fb02be2d380ff6d09e66a02d03b432e8b324e73c`、tree `105732ddbd6702651688285f92753f1148a338cb` 启动，重新检查提交、Actions、README、协议、历史 CURRENT、设计、史料、来源登记、模块优先级及最新 INTEGRATION46 的止点。历史 `docs/CURRENT-STATE.md` 原2,709,173字节／Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` **全篇通过Git原Blob读取，原字节不变**。I46的环岛A线无更多合格原DAT，按最新最高NEXT返回**有实物的非加鲁卡模块**。

本包只将此前[QUEST23](../../research/recovered/STONEAGE-QUEST23-PORU-FOUR-STONES-SOURCE-AND-NINE-SCENES-R1.json)与[QUEST24](../../research/recovered/STONEAGE-QUEST24-PORU-FLAG63-FUNCTIONS-AND-FOUR-SCENES-R1.json)的私人已验**波鲁地区原地图格、原图像候选、NPC配置、静态任务条件**做一条可独立验算的区域关系；不重新包装两份既有复原成果为新发现。成果为[公开来源数字、哈希和边界](../../research/recovered/STONEAGE-INTEGRATION47-PORU-13-SCENE-SOURCE-GRAPH-R1.json)及12项正反例回归。

## 本轮实际重新读取的私人原始数据

| 私人已保存载体 | 本轮完整ZIP SHA256 | 字节／成员／CRC | 原NPC成员逐SHA |
| --- | --- | --- | ---: |
| `StoneAge-QUEST23-poru-nine-scenes-private.zip` | `fe6eba160e9df38a4182018fb2c581d2f9cdee1f39fe5cdab3f2a8904580cf6a` | 58,171,450B／1,014／全通过 | 23 |
| `StoneAge-QUEST24-poru-flag63-four-scenes-private.zip` | `75aad7150fe4ffd4db0da16bc5de92f8ed3c61073beb2fa709a9ad19c8ba83ac` | 23,451,751B／578／全通过 | 36 |

两份 `source-summary-derived.json` 原字节 Git SHA-1 Blob 分别完全等于仓库QUEST23 `303bafb317e5d5911c4a9bc23ac4ab90066b9b80` 与QUEST24 `c7150d08cace8da3d6b5411036818e1baacb46dc`。本轮逐一实际提取并校验两归档的**13张原DAT**：9张（5530/5532/5533/5535/5537/5538/5541/5542/5543）和4张（5500/5509/5510/5511），每张原宽高、8+6WH字节结构、DAT全SHA均与旧原源报告精确一致；每张旧现代候选合层PNG重新读取为RGBA，全图像素SHA与旧报告一致。合计22,564次>99原图引用、8,057次1–99低值仍保持不解释，未拿低值当碰撞。这里的整像素复验限于**前轮保存的现代候选PNG**与此前原源关系；没有重新从原REAL逐图解码、重新构建13张画面或证明原客户端原生显示。

两包分别包含913和490份基于台湾1.0原图的候选图号：实际按逻辑别名读出每张PNG做SHA256，**78个相同编号逐图PNG SHA全部吻合，零冲突；并集1,325个别名**。这证明**两份已保存图像子集**的78处字节一致，不等于发现1,325张新图片、1,325只宠物、原版同服使用或完整波鲁世界。原源NPC名录为59次成员出现、58个不同路径；两包同路径项SHA一致，59次实际原成员逐SHA/尺寸重验。未取得任何新的原DAT、原NPC脚本、原RD解码，所以新实质结果是**已获证据之间可以追溯的地图／NPC／任务静态关系**。

## 具体关联：有来源的传送方向与相邻非传送NPC

在mixed25同保存社区载体中，`poru/poru01.create`第21个来源块指定地图5509的(37,35)，原格三个u16为`[407,0,49152]`；其模板解析为**WarpMan**。原参数文件`poru/wpm_5509_35_35` SHA256 `51d73ce6e287eac1f0c879ec65707fae7ef918f8927c76eacc899e75368ddc53`确含`WARP=5510,16,49`、`FREE=ITEM=2414`和`MONEY=-1`。目标地图5510原DAT已取得，(16,49)三u16为`[4204,44,49152]`。据此成立一条**同保存载体的静态源参数有向边**：`5509(37,35) → 5510(16,49)`；不能据此断言原客户端执行了传送、收费或条件可达性。

目标的相邻点5510(16,50)有另一个确实存在的CREATE，原格`[4206,0,49152]`，参数指向`poru/wpm_5510_16_50`，但**源模板是ExChangeMan，内容TYPE是MESSAGE且无WARP字段**。不能因文件以`wpm_`命名、距离一步或旁边存在传送点，编造返回5509的逆向WarpMan。仅一条经过参数及两端原DAT联接的边，不可声明波鲁地图联通闭合，更不可升级成初代官方世界地图。

## 具体关联：静态任务标志，不推定任务实际顺序

QUEST24 原`poru/boy04`第1事件字面`NOWEV=63`及`GetPet:352`／`EndSetFlg:63`，QUEST23有明确`ENDEV=63`请求条件。另QUEST23 `poru/mary01`第0段为`NOWEV=64&ITEM=18556&ITEM=18557&ITEM=18558&ITEM=18559`、原`DelItem`字面`18556,18557,18558*1,18559`、`GetPet:310`／`EndSetFlg:64`。是**原脚本字面依赖/奖励指令图**，不是实际运行顺序、交出/取得宠物、存档成功或自然可达的证明；宠物图号候选仍有单独版本来源。

尤其QUEST24 `poru/samugiru01`的MESSAGE条件为`ITEM=18556&ITEM=18557&ITEM=18559&ITEM=18544`，与上述QUEST23四物品条件中的18558**并不一致**，不能把18544改成18558求“任务连贯”。两包均有floor500 CREATE引用（3和6），但已有955 DAT资格目录**未取得500原DAT**，不能以此画出此区原地图或认为历史上不存在地图。

## 来源、验收及后续止点

- 以上原NPC配置和原DAT来自有保管记录的**后期mixed25社区保存资料**，台湾1.0是**不同载体的认证零售图像**，同号跨版不构成原官方同部署。原始文件、完整对话、DAT、RD、PNG/HTML没有上传公开仓库；只发布来源标识、数值、SHA和否定条件。
- 本地逐私人ZIP全CRC、59个原成员全SHA、13 DAT/现代候选RGBA与78同号PNG实字节校验成功。GitHub公开CI只能复算已发布数字、Git Blob和来源限定反例，**不能重跑被私藏的原商业实物**；以候选/PR/主线Actions真实结果作为附加验收，不预写成功。
- 不改`docs/CURRENT-STATE.md`的历史前缀，不改写QUEST23/24结论，不自动把原画/原任务纳入新游戏。Stage A仍 **7 PARTIAL＋2 OPEN**，Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，overall_percent=null。
- **NEXT**：本区域13景、静态边和标志差异到此止点。按模块优先挑选另一组**已实际保存原DAT+原图候选+可解释的NPC/物品关系**；只有取得原floor500 DAT、原生任务执行或有身份的新载体才重开波鲁任务支线。不把“13张候选画面”扩称整个世界已可游玩，也不投入旧网服/新引擎。
