# PET-HIGH-FIRST-41｜31原件与三宠任务取得链、57图号候选

启动 main `5158fe021a7f0580ab70ca6c74a416607d5b98b6` / tree `6cd989abe5c779d48d50ac98139483d84f6e2b4d`，精确HEAD 42/42 Actions成功；§28以tree确认历史CURRENT仍2,709,173B / c89e0e33537990aa2132b47c40fef49a985a935c。PR #652源提交 `6d167d2c7ebd940c7d7dfa4235c3441b6b757bec`。

[原件派生数据](../../research/pets/PET-HIGH-FIRST-41-MIXED25-ACQUISITION-R1.json) · [57既有档案交叉索引](../../research/pets/PET-HIGH-FIRST-41-ACQUISITION-CROSSWALK-R1.json) · [源Actions 45416445759](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/45416445759)。

实读混合2.5保存RAR，184段HTTP206共12,013,836B、遍历7954头，31完整原成员逐件解包并与既有SHA-256和RAR CRC吻合：配置、四主表及26份非备份quiz/sink脚本。非整包重取，非官方同部署。ZIP实际下载26912B，SHA256 a47ce2b725df4c98971315862b2c53019a97506c063a2d85c73f0c900f16e9f1 与API记录一致；原JSON 240995B，SHA256 a6bd3200085787eead9240936ca8c571252ed4f7fdf36f518f822163a3fc78a3，独立日志重建Git blob和ZIP原JSON一致 746107dc2265e66629d64419fb039934de9baa11。原版权字节不入Git。

## 三条原保存配置任务奖励

|宠物档案|GetPet实例→模板|配置条件／NPC位置|模板字段（地水火风；BASE；INITNUM；LVUP；技能槽）|
|---|---|---|---|
|PET-000006 金布伊|14→12|NOWEV=44&ITEM=2753，删除2753，结束44；810及850 (28,16)|0/0/30/70；31/20/32/12；25；4.50；1,2,3,40|
|PET-000099 左迪洛斯|351→302|ENDEV=44&NOWEV=47&ITEM=2759，删除2759，结束47；812 (32,24)|0/80/20/0；28/30/22/22；26；4.50；1,2,40|
|PET-000100 巴朵蘭恩|352→303|ENDEV=44&NOWEV=45&ITEM=2759，删除2759，结束45；本批未解析到直接create引用|0/20/80/0；23/37/20/25；27；4.50；1,2|

三条实例均Lv1，实例及模板PETFLG均1。技能槽不是已认证出生技能，BASE不是Lv1面板。2001/2002同期玩家猜谜奖励说法和保存金布伊指令对应；左迪洛斯与巴朵蘭恩旧2001目录未列取得法。后期固定PC比较脚本及实例、模板ID用独立CI重验；实际NPC运行注册、官服发奖、地图头和坐标可达性、概率和原始首发日期未证，巴朵蘭恩不得补写NPC坐标。

## 批量候选

58条旧攻略位置中57图号可作来源限定候选；145保存模板行（86 PETFLG=1，59非宠标记），660正权重链中636同时具双宠标记，33含Lv1；43模板有双标记链、29模板有Lv1双标记链。按攻略明确比较模板ID而非只看同图号，38攻略位置有双标记链、29含Lv1；记录各行图号、模板原名、来源行、权重、楼层、矩形和事件字段。**此为静态遇敌配置候选，不是抓捕实测，不是636只宠物。** 57既有研究档追加来源链接，查询位置不新增、不计新增物种。保留与旧指南的差异；本轮未读取地图原二进制，未验证实际捕捉或领取。

PET唯一、Stage A 7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79暂停、总体UNKNOWN。历史CURRENT不改。

## 对旧证据的实质纠偏（不重写历史）

[INTEGRATION36](../../research/recovered/STONEAGE-INTEGRATION36-QUIZ-THREE-BROTHERS-ORIGINAL-SOURCE-R1.json) 已核过 quiz.create 和六活动脚本。此次是原件再访问、扩至sink并纠正GetPet关联语义，不把早已记录的14、351指令再算为新发现。旧报告 GetPet_past_and_same_carrier 把字面数字14/351/352对照同ID的模板行，分别得到图100257、100040、100040；这三个模板并非奖励指令所选目标。R40的后期解析函数证据与R41实读实例表联合表明，应按 ENEMY_ID→实例的模板ID→模板图号查询，实际得到14→12→100255、351→302→100372、352→303→100373。旧模板行真实存在，不删除，只撤销把它们当奖励目标的解释。INTEGRATION36还区分备份352与活动quiz 14/351；R41的352来自另外的非备份sink/equiz_04，直接CREATE未见，不能当已启用。旧报告812原DAT有派生证据、810/850未有，仍不声称本轮实读地图。

[INTEGRATION05](../../research/recovered/STONEAGE-INTEGRATION05-GETPET-QUEST-MAP-ORIGINAL-SOURCE-GRAPH-R1.json) 已登记24个CREATE引用、23个脚本、36个GetPet字面数字、19个楼层。其原件索引可以直接服务下一轮，避免对全NPC树重扫或重复以模板同ID当奖励。

**NEXT PET-HIGH-FIRST-42：** 先使用INTEGRATION05及既有任务块目录的确切脚本、字面数字与来源指纹，通过配置选择的实例表和模板表重接奖励目标，优先卡坦鱼鸟交换和SOT/JOT相关证据；仅在确实缺字段时回读原件，定位分支及地图。不重复纯名字网页，不跨模块。若已存在未验收PR，先完成其验收。
