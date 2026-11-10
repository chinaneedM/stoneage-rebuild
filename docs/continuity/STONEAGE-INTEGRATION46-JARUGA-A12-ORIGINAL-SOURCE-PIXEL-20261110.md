# INTEGRATION46｜加鲁卡环岛 A12 地图3400原格、原图像与静态任务真实复核（2026-11-10）

## 正确的远端起点和交付范围

本轮按 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` 重新读取真正远端 main `ba0b473adf3b0b782c70a29f180bd115bab0e05d`、tree `82d49bbff4bb553f56e026747b8748c5d9171996`、最新提交／Actions，以及 README、完整 `docs/CURRENT-STATE.md` 原Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`（2,709,173字节）、史料／来源登记／设计原则和模块优先级。旧CURRENT全文未更改；近两次 I44、I45 的内容提交27/27次主线Actions成功，追加验收收据自身未虚报匹配CI。

承接 I45 精确证据止点，本包只复原**原社区mixed25保存资料的加鲁卡A路线第12站**：实际原 `3400.dat` + 原 CREATE/oev_12 + 台湾1.0零售图像候选，独立完成一次11×11可见候选场景。原地图4000及A2/A8/A9另无已取得DAT，不编造。

## 实际原文件保管链与之前失败的保存

本轮私人重新取回并整文件重算SHA256、遍历ZIP全部CRC的5个父包：

| 私人原件/来源包 | 字节 | ZIP成员 | 身份 |
| --- | ---: | ---: | --- |
| INTEGRATION10 原地图补救包 | 5,759,006 | 314 | `7a4b74af4ca4b0cca3108dcdec55bb9f1892a2edf17b73d400aab4c041fa6b96` |
| MAP04 台湾1.0真实RD像素候选 | 35,673,334 | 4,169 | `e9c43222797c7ebcddfcb1ccab6dbeba205b972bbbff4e1f29c14b3ece320d37` |
| QUEST25 混合2.5社区原NPC/脚本 | 172,328 | 173 | `543cf62ec2b1f5a36a929c7714e86510f1382430039ebf6e7a487d165acffbb2` |
| P3H 台湾1.0原零售客户资源 | 372,626,292 | 379 | `3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24` |
| INTEGRATION45原16067人物RD保管包 | 5,098,689 | 132 | `a705e963612ce24177940feebe9f7d4225a4bbc83af2197624af31bb5350d018` |

额外实际逐整文件SHA重算P3H原 `adrn_1.bin` 10,079,680B、`real_1.bin` **315,842,228B**、`Palet_1.sap` 708B，分别与原旧源sha `47254c0ff904d363fb5c3c5297edf553c8eaf24cd933f346d8ce7aabed4155c8`、`408e6ee05c83354349691937da2ad8f7488ac10f65f07e6681b7d92cb1c9ed13`、`32870080c47537a59beaf770b6df7bd79820fd52a23825058460900494f0b4b0`吻合。

**特别保留来源失败史：** 原RAR/原压缩成员过去曾在3400.DAT读取到65,536B后报`File CRC error`。旧I10经过有界补救取得并永久SHA登记完整3400.dat，并没有因此断言原客户端实际成功读地图。本轮从I10私人ZIP实际取回原 `source/3400.dat`，86,408B、120×120三平面、SHA256 `a3c6918ba21c909e6312329c936615aa6b6d8800d7967ed85a2146d55ca263c4`，与旧I10所得原字节身份严格相同。旧失败未抹去，新一轮读取确实成功，不混淆。

## A12 原地图场景与静态任务的精确交点

原CREATE为 `jaruga/event/oev.create` 第12块，SHA256 `b8951bcc963371d53c4c6f626c4a74eebf82e7f8ca77ebdab5d9854704c9104b`，地图3400坐标`(69,61)`，方向原数值6，图号16067，模板ExChangeMan，确切指向 `jaruga/event/oev_12`。原脚本1,874B SHA256 `f47ab5245c56771a92b53b942fb7305857e33cc2b8bda7d1db017000d1d9b70d`，六段原TYPE。第一段静态条件`LV>0&ITEM=2563`，含`DelItem:2563`与`GetItem:2564`；第三、四、五段存在旧编号/ENDEV2与重复ITEM条件，不证明原服执行优先级、任何实际奖励或可达性。3份原CREATE／模板／脚本成员重新从QUEST25私人源包读出、整成员SHA与旧源清单吻合，未声称新发现脚本。

A12周围原DAT严格窗口`x=64..74, y=56..66`：**121格**，中心原三u16 `[260,0,49152]`；前两平面**135次>99原图编号引用**、**69不同逻辑图号**，全部在已核TW1 MAP04原像素记录有资格。低值1–99原出现**21次**（数字2出现14次，27出现7次），只保留原数字，不当完整地图绘制或碰撞值。69个候选像素全部由此前MAP04实取原图+原ADRN逐唯一命名空间比对、RD SHA/PNG SHA/RGBA SHA和宽高核实，不把物理位图序号误作逻辑图号，也不称69张新绘制的原创美术。

从I45私人保管库实际重读 `16067.rd`（1,694B；SHA256 `8dc805589a31d6627aae8df214f587ae08dd9b6d277bfb0d494e7d44292cddd0`），两个独立RD解码一致；同时本轮重新访问原P3H完整REAL内实际偏移25,054,495处，逐字节与保留RD相同，候选32×78 RGBA SHA与旧I45一致。**旧人形像素重新验真，不计一张新发现的人物图或原NPC必然画法。**

### 实际原像素离线拼合

根据原格投影、ADRN原图位置偏移与原候选像素，真实生成736×769像素的`plane0`、`plane1`、`combined`三张完整现代场景。第一实现为Pillow的原PNG透明拼合，第二为NumPy数组逐像素二值Alpha覆盖，三画面完整RGBA哈希逐一相同；第三个**独立程序**从最终私人交付ZIP重新读原3400.dat、69图PNG、采用另一种对角线遍历，三幅RGBA和交付PNG也完全吻合。第一层SHA256 `4ffd02f563950def8a3d9dd105db2c03b7706fd3b0a427d4fb5d9086f7ea60b9`；第二层 `d58097ff14ef09f8c5d2565f516ccebb71c8809f1aaf90d13c90927370f9ed8d`；合层 `1b8a642dc82a4c4e35d6c0bd0f52c764fba565a1f314ba80e154ff3fc459fe14`。已实际目视绿地、树木、栅栏、岸边岩块和河水等候选原构件。另两张黄色坐标标注与站立人物像素叠加**只是现代观察辅助**；原版客户端原生画面、透明顺序、时间调色板、碰撞及人物方向均未证明。

## 私人归档、公开发布范围、下一工作优先级

完整私人交付 `StoneAge-INTEGRATION46-Jaruga-A12-source-scene-private.zip`，**1,314,729字节、80 ZIP成员、SHA256 `d58852205cf9fae9117d7f0dd0f721818aca5c64b8cc833f2fe4034a48a6159e`**，含原3400.dat、原oev_12、69张原图候选、原16067RD、5现代场景PNG、来源原格/图号/原SHA与离线观察HTML。私有source-derived JSON全SHA `39def1596a27830fd3a8a67c80d1c7f1b52e7fc797497f6b18ebc4620a3f15d6`。实际已上传个人Library `/石器时代/`，再次回下载**全包逐字节相等且80成员CRC通过**。商业原DAT、RD、NPC脚本/原图/HTML均不入GitHub公开仓库。公开[派生数值和SHA索引](../../research/recovered/STONEAGE-INTEGRATION46-JARUGA-A12-ORIGINAL-DAT-AND-PIXEL-SOURCE-R1.json)与专项测试/CI不含原商业字节，不能把公开 Actions 通过解释为CI重新解压了私人原件。

已在本地所有可访问的私人ZIP名称索引上查找原 `3100/3200/3300/20406/20507/20702/4000.dat`，本轮**0个合格候选**；这只是可读归档清单的局部负证，不是证明历史上从不存在。环岛A路线已有来源可见观察在A1、A3、A7、A11、A12节点有独立画面，不重复复制为“完整环岛”。**最高NEXT：暂停扩无源环岛 DAT，按模块优先级转向其他有实际原文件且尚未整合的游戏内容**；只有确切同身份原DAT重新取得才重开A2/A8/A9/4000等缺失场景。

全程 Stage A **7 PARTIAL+2 OPEN**，Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，overall_percent=null。研究阶段尚不选单机引擎，不做美术替换、体验优化或玩法创造。
