# O19：同保存版1003(12,13)宠物店创建块到原参数文件的一条静态原件链接

## 新读取原字节与精确限定
承接 O17 已合并内容和同轮 O18 正在候选CI的1003服务端命名/三份NPC原文。由已整SHA验证的 mixed25 私人 RAR 本轮**实际读取**原 `gmsv/data/npc/genout/shop_m.create` 20491B，SHA256 `d540e9a1354a0f82839cd30ab315a6dee4a3b0299744a0f63ae5ee461c5b587b`。只选 **恰好一条** `enemy=npcgen_petshop|file:genout/ps_1003_12_13`；它在文件中仅出现一次。创建块原字节 [642,802) 的 SHA256 `669e06a65e61f2346bf424a35e1a4af03f4e1c5f4089e89295115906271b2fe9`，CP950 同字节往返。

原静态字段：`floorid=1003`、`borncorner=12,13,12,13`、`createnum=1`、`dir=4`、`graphicname=16038`、`name=寵物店`、`enemy=npcgen_petshop|file:genout/ps_1003_12_13`。引用的原 `gmsv/data/npc/genout/ps_1003_12_13` 397B/SHA256 `f4759c08d7391033b8fcee4d2580832c77e8210d637009b608be460b51285cbe` 已本轮实际取得与复核。因此，从 **原创建配置 → 原参数文件** 的同保存版静态文件链明确成立，不再只是文件名猜测。

真正原客户端 1003.DAT 在相同数字格 (12,13) 的三平面是 **5001/0/49152**。这不是 `graphicname=16038` 原视觉绘制/碰撞已证：图形别名与地图像素作用不同，49152语义未知。源静态 `createnum=1` 亦不证明真实游戏时已生成一NPC，参数文字不证明真正商店买卖/寄放事件。该混合版不是已认证的2003或TW1官方部署；禁止跨年代晋升。

私人原文件 ZIP `StoneAge-O19-private-original-shop-create-argument-source.zip`，5665B/SHA256 `d7db30ac0a292c37f323e800e26e9bad61f80922d21a5a71c1e7ac3838b7c818`，原创建、原参数、原DAT、服务端地图及元数据五项；CRC、原创建/参数回读通过。原脚本及文本不进入 Git。公开仅 [派生摘要](../../research/recovered/STONEAGE-O19-ONE-PETSHOP-CREATE-ARGUMENT-LINK-R1.json)、守卫/反例/CI、本纪录；不依赖原客户端网络或执行。

**O19止点**：仅证明1003宠物店一条有源指针，不扩全部店、全部NPC、声音/helper。后继 O20 如需推进应优先用现有一条原链接尝试**明确区分原静态数据/现代互动观察**的单点离线展示；若仍无原事件源，记录缺件轮换22域。原游戏世界、原生交易、原官方同版部署未证。保留 Stage A 7 PARTIAL+2 OPEN，B/wiki GATED，R79暂停，总体完成百分比null。
