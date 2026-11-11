# INTEGRATION65｜玄黄洞窟原「风的手镯」NPC／宠物交换／物品图像来源（2026-11-11）

## 从最新远端启动及来源边界

本轮重新读取远端 `main=7983016707d48e13728aed321fb40bd5a74b74b7`／tree `7507b253cad735e975c29370f7bb7e0cd08a6b4f`、Actions（26/26 completed/success）、README、协议、完整 `docs/CURRENT-STATE.md` 原生 blob、设计/历史/来源/路线/模块顺序和INTEGRATION64回执。历史 CURRENT 为 **2,709,173B**／Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`，本轮不改。原材料仅是后期**社区混合2.5保存的原NPC和物品数据**及**台湾1.0零售原RD跨载体图像候选**，不是经鉴定同一早期官方部署，更不是原游戏运行。

先按 QUEST01 295脚本目录、QUEST08–32、WORLD13/14和 INTEGRATION33/38/39/63/64、O70/O74 去重：`sainasu/event/genou_1` 已见于旧QUEST22，不能报为新发现；本轮针对同一 `genou.create` 下仍缺专项的 **`genou_2`、`genou_3`、`genou_4` 三原脚本**，接成实源地图NPC／道具／宠物交换候选关系。之前筛到的 `M_1000` 等四村委托实际早已由O70/O74研究，本轮没有重做。

## 原件完整性、实际NPC配置及地图现状

完整重读私人CHAR01 ZIP **995,176B**／SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`：**2,205/2,205**原成员CRC合格。四份原CP950脚本与 QUEST01 物理文件SHA、CRC一致；同原 CREATE 为 `sainasu/event/genou/genou.create` **989B**／SHA256 `d94613df0dc41560459cd99f1cb052d006c7310448c62285949768849cd6f874`，实际有五份独立配置：

| 创建序号 | 原楼层与出生坐标 | 原 NPC／graphicname | 源脚本 |
|---|---|---|---|
| 0 | 11215 (10,10) | 威爾／100461 | genou_1（旧QUEST22） |
| 1 | 11215 (13,11) | 風的使者／100446 | genou_2 |
| 2 | 11215 (7,11) | 風的使者／100446 | genou_2（第二处原CREATE） |
| 3 | 100 (346,356) | 姆哈薩／100110 | genou_3 |
| 4 | 11206 (5,36) | 看守人／16306 | genou_4 |

MAP09旧已独立原DAT/原图源资格中的楼层11215（20×20）和11206（60×60）确实存在，NPC原坐标也在源几何内；**本轮不重新绘制、不宣称实际原NPC已显示**。楼层100不在MAP09这691张已实绘目录，不能因此说原游戏缺该地图。

## 新补三脚本11 TYPE，保留异常而非补造规则

`genou_2` 原2005B/SHA256 `60258bc49615b9e0de4f1f4cf4f2627419cd5f868d9fbe69f5733d7cf4963de6`：三段 ACCEPT、三段 MESSAGE。三条 ACCEPT 都字面写 `DelItem:2758`、不同的 `DelPet:PET>...95*1` 和 `GetRandItem`。**第一条条件**里同时有 `PET>60-95` 与 `PET>59-95`、串接的 `ITEM=2758LV>0`，但本段 DelPet 明确为 `PET>59-95*1`。保留这个原文本缺陷和源逗号，不擅改为有效的AND/OR、确定概率或历史真实执行。其余两条 PET 数字42-95、0-95不自动归成同物种。

三条 `GetRandItem` 源**有序**数字分别8／13／14个，**35次出现／24不同物品ID**；第二条5种ID各重复2次，第三条6种ID各重复2次。重复是源事实，是否构成权重完全 OPEN；不排序、不去重原序列、更不算掉落概率。

`genou_3` 原849B/SHA256 `e9691b148781d9b2c9cf9d630f6f2a283f601283bea379ace21ff8f013e6e1f9`：2 MESSAGE＋1 REQUEST，字面参照NOWEV42、NOWEV41/ENDEV4；这些数字不证明NPC当年触发或玩家已经完成任务。`genou_4` 原658B/SHA256 `267629a672bfafa3ba3bd6c879afbd5317d65c53410d2ab5620eca12602945b6`：1 ACCEPT＋1 MESSAGE，`ITEM!=2758`条件下有 `GetItem:2758*1`字面，不证明实际领取/刷取。旧 `genou_1` 5段TYPE在新目录中只作旧QUEST22背景；三份新主题脚本合计**11段**，全家族16段，并未发现4份全新脚本。

## 关键冲突及真实原像素

私人ITEM01 ZIP **5,868,386B**／SHA256 `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa` 实际重读，**838/838 CRC**、所选25 ID在两套原94列物品行SHA逐ID相同。物品 **2758** 的两套原名均为**「風的手鐲 [風]」**、图号22119、type8、level65、价数字500；但是 `genou_4` 的原注释写「風之豎琴事件」，另旧 `genou_1` 提及的2736原名才是「風的豎琴 [風]」。两种名称不能替换、两个物品号不能合并。

35次奖励数字指向24不同原物品行；加上2758共**25件物品**、但只有**18个不同图号**。实际从旧已验台湾1.0私人原RD候选包读取18张保存PNG，逐文件SHA、原尺寸及RGBA SHA与原RD收据全部吻合，私人只读页按原序呈现（包括奖励项重复）。**本轮新增原RD解码0张**；跨载体图片不证明原任务在台湾1.0部署。

## 私人保管、公开验收、下一项

私人 `StoneAge-INTEGRATION65-GENOU-ORIGINAL-PRIVATE.zip` 为 **95,997B**／SHA256 `b8e1cebac804e2f538bb3220145ff1253ed4480ba1b6ea1c3c4eda331e8be783`／76成员（4原脚本、原CREATE、两套25项原物品行、18原PNG、离线资料观察页与来源收据）。已存个人Library `/石器时代/`，并独立重新下载到第二路径：整文件完全相等、**76/76 ZIP CRC通过**；原商业全文、真图和原物品行未进入公开Git。

公开只存 [来源SHA/原CREATE/TYPE/25项数值及18原像素身份](../../research/recovered/STONEAGE-INTEGRATION65-GENOU-THREE-SCRIPTS-25-ITEMS-18-TW1-CANDIDATES-R1.json) 和专用公开数据回归，不含原始图片/原商业脚本正文。公开CI只能重放数字和来源边界，不能代替私人源实读或原生执行。候选及主线CI必须**实际完成后**另行验收，不预写成功。

**最高NEXT：** 本genou四源关系到此有限闭合；转未专项的其它有资格原地图／NPC／宠物／物品来源，不扩原命令模拟器、旧网服/账号或新单机引擎。Stage A **7 PARTIAL+2 OPEN**；Stage B/wiki **GATED**；R79 **PAUSED_NON_BLOCKING**；overall_percent=null。
