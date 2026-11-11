# INTEGRATION75｜长毛象神社六枚神签及香油钱的原静态来源（2026-11-11）

从新核实 main `582fe47e28cd3b8fdc09e88c6cc098ee914e04fc` / Git tree `185ac4eca1c9f8858bb823aafd91489c7cc14dae` 续接 INTEGRATION74 验收。完整历史 CURRENT Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`（2,709,173B）继续一字未改。[公开派生证据](../../research/recovered/STONEAGE-INTEGRATION75-MAMMOTH-SHRINE-SIX-FORTUNES-SOURCE-R1.json)只记录源 SHA、数字、原行位置和证据边界；源完整文本、94栏原表、原图仍然私人封存。

## 本次来源限定实物与实际关系

**FACT（后期社区 mixed25，不是TW1同服）**：重新读取 CHAR01 私有 NPC ZIP **995,176B/SHA256 c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f**，完整 ZIP 2205/2205 成员 CRC 成功。其四份原 `npc/extra/event/omikuji`、`omikuji2`、`osaisen`、`osaisen2` 均实读原始字节与整 SHA；两份 omikuji 是不同字节但同TYPE结构，osaisen 双成员681B内容同SHA。原抽签两脚本 `GetRandItem` 各为**15个列表位置、6种ID**，2615/2616/2617/2618/2619/2620 字面出现次数为 1/2/4/5/2/1；抽签携 `EndSetFlg:36`，捐献原脚本携 `CleanFlg:36`、`DelStone:50`。这是原脚本文字及静态配置，不是随机算法、扣钱、每日重置等真实运行结果。

**FACT（ITEM01已经原源验过的私人转录与公开表）**：再次读取 ITEM01 私人资料 ZIP **5,868,386B/SHA256 cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa**，成员838/838 CRC通过。六枚原物品ID在两套原物品主表的已有源认证转录中都有94字段源行，两份表同ID整行SHA相同；其六个源行散列与旧公开 [ITEM01 shard02](../../research/recovered/item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-02-R1.json)一一相同，原中文名均为「神簽」，源图号一律24313。**TW1认证零售资源索引缺这个图号（TW1_INDEX_NOT_FOUND）**；没有新原RD或原PNG，绝不臆补美术。旧完整原 itemset.txt / itemset0710.txt 父RAR成员这次**没有**重新取出，不能把再次核转录包装成新原表源阅读。

**OPEN**：仅检查本 ZIP 中 578 个扩展名为 create/template/arg/conf/gen 的文件，找不到 omikuji 或 osaisen **字面**直接引用；这不等于原服务器未加载。原脚本文字提及一天一次，不说明真实定时重置；重复列表位置不推出原生抽中概率，`DelStone:50` 不证明运行扣款。脚本真实装载、同官方版本/同服务器部署、早期TW1/JSS1999规则与原神签图均未经确认，现阶段只建立有据静态跨文件关联。

此包没有新原素材、没有原游戏执行、没有将版权原图/脚本/商业全文上传Git。公开回归仅核对历史归档的来源 SHA 与资格负例；私人CRC与内容来自本轮真实本地回读，不能当远端CI对私人文件的重放。阶段 A **7 PARTIAL + 2 OPEN**，B/wiki GATED，R79 PAUSED_NON_BLOCKING，overall_percent=null。候选和主线Actions以实际后验为准。NEXT另转真实原件就绪且未重复的二维内容；神社待明确原装载引用、原native随机/旗标行为或经认证图24313才重开。
