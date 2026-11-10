# INTEGRATION50｜28间原房的道具、宠物和技能商店原配置接缝（2026-11-10）

## 任务目标与可证范围

本工作包接续已验收 INTEGRATION49，不重新绘图或把139条CREATE当新增原NPC。恢复对象是这28张已保存原DAT房间内的**具体服务配置**：哪些原房间配置道具销售、宠物商店和宠物技能商店；它们的原字面物品类别、候选ItemList索引、宠物相关费率与技能数字列表有何差别。此批提供的是**静态来源关联**，不是原生运行证明、可交易世界或正式台湾1.0/JSS1999商店目录。

远端启动依据：主线HEAD `9657ca20cde60445de96f8e56ae7340963cb2414`，tree `dcd185b8ce483fa75757d4209b0d3ee7743ea6aa`；前一收据为 [INTEGRATION49](STONEAGE-INTEGRATION49-PUBLICATION-ACCEPTANCE-20261110.md)。其后专项验收须以本批实际GitHub Actions为准。

## 原载体与独立来源界限

- 个人Library保存的原 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip`，995,176字节；完整 SHA-256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`；实际读取全部2,205 ZIP成员，CRC无错。
- 本轮按INTEGRATION49的每条CREATE来源路径、块序数、原块SHA、坐标和原参数路径，从私人原ZIP实际逐文件取出**44条配置对应的43个不同原参数文件**，逐份完整SHA匹配公开I49；严格CP950读取相应参数字段。44是CREATE记录数，不能说成44个新增NPC、43件原初代文件或44个独立服务商。
- [I49旧公开房间索引](../../research/recovered/STONEAGE-INTEGRATION49-28-ORIGINAL-ROOM-NPC-WARP-SOURCE-ATLAS-R1.json)，Git blob `673fd0ebd71a909a5678d919f706bab7a8e5e7cc`；[ITEM模块先前224份ItemList原参数索引](../../research/recovered/STONEAGE-ITEM-EQUIPMENT-SHOP-MODULE-01-224-SOURCE-ITEMLISTS-191-CREATE-REFERENCES-R1.json)，Git blob `3bde3b7df43725f28cdac355823667a0ba87e9b1`。这两个是**既有来源**，本轮新增的是28室具体CREATE与物品/宠物/技能参数之间的精确关系。
- 历史 `docs/CURRENT-STATE.md` 现远端Git树仍指向原始blob `c89e0e33537990aa2132b47c40fef49a985a935c`，2,709,173字节，**完全不编辑**。本轮文件接口对非空大文档返回空串；按协议§9、§14用树/文件元数据固定历史blob并另写加法续接，**不能宣称本轮已完整下载其正文**。保留全部既有历史，不把读取异常当历史不存在。

## 原字段实际结果

| 原模板服务 | 原CREATE记录 | 新的可核对接缝 |
| --- | ---: | --- |
| `ItemShop` | 32 | 31个不同原参数路径；类别字面`OFFENCE`7、`DEFENCE`5、`ACCESSORY`6、显式空值8、字段不存在6；其中29条原参数与既有ITEM主索引的**路径和整SHA双重一致**，剩余3条`lbis_`参数没有ItemList字段、也未在旧ItemList目录内；不把缺ItemList填成空库存。 |
| `PetShop` | 6 | 原`nomal_rate`（沿用原拼写）五处1.0、一处地图1203为0.7；`special_rate`六处1.5；1003/2003/3003明确同时有`pool_flg=1`和`pool_cost=200`，其它三处**没有这两个原字段**；六条的`special_pet`字面为空。 |
| `PetSkillShop` | 6 | 六份原技能数字菜单合计50个出现位置、15个不同数字；各菜单共有`0,1,2,3`。原`skill_rate`分别1003=1.0、1103=1.0、1203=1.2、1303=1.1、2003=1.0、3003=1.0。不给数字自造技能名称、经验消耗或训练成功规则。 |

原`genout/ss_1302_12_15`在房间1302有两条独立CREATE记录共用原参数；两份CREATE块SHA不同。本轮保留这两条，原NPC数量、显示方式、脚本分支/加载优先级和真实售卖/教学的发生都未得到本轮证实。

更细的逐配置楼层、坐标、CREATE块SHA、参数整SHA、静态费率与先前物品索引交叉证明见[新公开纯派生索引](../../research/recovered/STONEAGE-INTEGRATION50-28-ROOM-SHOP-PET-ARGUMENT-BRIDGE-R1.json)。原文本、原图片、地图DAT、原档案和可能受版权保护的服务字符串均未进入公开Git。

## 验收与后续

专项回归只复核**公开资料间的SHA/数字关系和边界**：44条源CREATE恒等映射、32/6/6角色守恒、29+3道具索引归属、字段空/缺区别、六份技能目录与池费候选、重复CREATE及否证条件。公开Actions不能读取私人ZIP，不能代替本轮独立原件CRC/SHA检查，更不能证明官方原客户端执行。最终CI与PR合并结果以另立验收记录为准。

停点：I49的28间房目前得到对应服务菜单的来源关系；若没有**同版本相应原始执行证据**，不推断实际购买、宠物寄养、技能学会、原始售价、图像显示，也不继续在同28房空转。**NEXT** 回到本项目现有22域和地图/人物/物品来源目录，选这28室**之外**确有新原DAT、NPC或可见像素实物、可产生不同游戏内容关系的房间/场景；无原件即明确止点，绝不进行网络服务器、账号、单机新引擎或体验优化。

Stage A 保持 **7 PARTIAL + 2 OPEN**；Stage B/wiki **GATED**；R79 **PAUSED_NON_BLOCKING**；overall_percent=null。
