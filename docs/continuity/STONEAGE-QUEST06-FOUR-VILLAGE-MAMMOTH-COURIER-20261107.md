# QUEST06｜四村长毛象快递委托：原创建配置、三段交付、八件原物品和候选原图（2026-11-07）

## 本轮新增内容及复核界限

在 GitHub 远端 `main=4885fb69ea0a2e374e5fd952d596edad725f3816` / tree `710e39af92745372fca8e32a80fe35ae439ce493`、最新11/11成功 Actions、完整连续性协议与 `CURRENT-STATE.md` 原 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 基础上推进。SCENE26止点为图形 `16122/16127` 暂无同载体合格 SPR 实物；同载体 `npc/sa60/newbie/m_tiger` 虽然被重新读原SHA，复查仓库发现 O61–O65 **早已完成**四村虎训练师16段、240 BBI条件、奖励实例及原二维动画/原RD的来源研究，**不再把它记为新成果**。

本次真正增加的游戏内容规格来自同一来源中**此前尚未规格化的四份长毛象快递委托 `worksell_*.conf`**。在私人原 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip`（995176B、SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`）重新逐文件读原字节，五份原 CP950 文件逐个与既存 QUEST05 源SHA完全相同、CRC一致：`sa60/newbie/newbie2.create` 1548B / SHA `31ef809c62f2cc208d0e5439796ee3a2e5466cda64e7561b7094248bf8a7455f`；`worksell_1014.conf` 1923B / SHA `d5139cb534128f4c4eb5551cd0bd3d4660a09b54a81a48911440b8d68fcea69b`；`worksell_2014.conf` 1885B / SHA `d9ad7e5f15a448238f9d7eec1339adee6cc8fbfb60525ab2f221d10d99d3f522`；`worksell_3014.conf` 1899B / SHA `eda96a3d8ce3d02e6235edf2425746aa8ddec3ce64ac72fde8351abab64410a0`；`worksell_4014.conf` 1937B / SHA `6ac7689410fa7af8ca75a1a25997217214fa32cb3861f00ccb90ec98c3c8298e`。

这是**后期社区保存的混合2.5版本原游戏脚本**，不是已认证JSS1999/TW1.0/大陆1.82正式发行/实际在线启用脚本。原商业文件全文和像素仅私人保管；Git收据仅保存原SHA、数字规则、来源资格和明确否定项。

## 源创建配置、八个楼层和空间资格

原 `sa60/newbie/newbie2.create` 含八段原 CREATE，四村各有两处来源配置；具体来源创建块→参数SHA→原DAT完整SHA由 [QUEST05 原598条CREATE联表](../../research/recovered/STONEAGE-QUEST05-598-ORIGINAL-CREATE-FLOOR-MAP-AND-WARP-CROSSWALK-R1.json)逐个验证。

| 委托脚本 | 源楼层（同一脚本的两处创建） | 原 `graphicname` | 原DAT |
|---|---|---:|---|
| worksell_1014.conf | 1014、1011；原borncenter均(14,20) | 16018 | 2个楼层ID的原DAT SHA相同，**不能当两种不同地图实物** |
| worksell_2014.conf | 2014、2011；原borncenter均(16,16) | 16092 | 2份原DAT SHA |
| worksell_3014.conf | 3014、3011；原borncenter均(16,16) | 16092 | 2份原DAT SHA |
| worksell_4014.conf | 4014、4011；原borncenter均(19,16) | 16018 | 2份原DAT SHA |

八条创建点均对应已验长度5408B的保存版原DAT整SHA，当前MAP09候选图层资料就绪。**本轮没有重新取回、绘制八张地图或者让NPC在客户端中出现。** 同源地图数字不产生官方南岛/北岛和村名分类；同图号不证明同一NPC人物动画。

## 源四个脚本×三段委托，按源字面保存

每一份原脚本有六段 `TALKEVENT`；段4、5、6分别按原 `LV` 字面区间分配任务与奖励。四份原脚本总共24段事件文本，**不是24项已执行任务**。段1—3属于源对话/提示；第3阶段的 `PET` 只作条件，不出现 `DelPet`，所以**绝不能把其写成扣除或上缴宠物已证**。

| 原同组楼层 | LV1–9物品条件及 `DelItem` | LV10–19物品条件及 `DelItem` | LV20–29宠物条件 |
|---|---|---|---|
| 1014 / 1011 | 2623（頂級的貝殼） | 12879（櫻桃醬汁牛排） | `PET=1-13` |
| 2014 / 2011 | 2622（頂級的紅寶石） | 4224（合成槍1［風］） | `PET=1-13` |
| 3014 / 3011 | 2625（特級的釣竿） | 4212（合成槍1［水］） | `PET=1-292` |
| 4014 / 4011 | 2624（特級的紅檜） | 12874（蘋果醬汁牛排） | `PET=1-292` |

三个阶段分别有源字面奖励 `AddGold/AddExps`：**1000/1000、2000/16000、5000/81000**。源脚本另含 `NOFREE:LV>30`、新手头部 `FREE:LV<30`。因此**恰好30级没有现存显式 LV 免费或拒绝分支**；这只能定位静态脚本条件空档，不能证明程序运行时玩家30级必然卡关，也不能自行补源条件。

## 八件源物品及原图的真实资格

八个源物品编号同时存在于保存版两套原物品主表 `itemset.txt` / `itemset0710.txt`（公开 [ITEM01分片02](../../research/recovered/item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-02-R1.json)、[ITEM01分片05](../../research/recovered/item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-05-R1.json)）；两份表各原行SHA有据。六组旧台湾1.0已实际解码二维原像素候选覆盖七个源物品编号：`4212` 与 `4224` 虽是不同物品ID且各自在两份保存物品主表存在原行差异，图号却都为 **20407**，因此复用同一原图不是同一种装备或相同历史数值的证明。

`2622` 对应保存版原图号 **22322**，不在**已保存台湾1.0零售原ADRN**中。本轮查到 [ITEM07后期来源索引](../../research/recovered/STONEAGE-ITEM07-PATCH129-ITEM-ALIAS-CROSSVERSION-SOURCE-R1.json)已有该图号的一条后期物理索引候选（物理位号244029、28×35、RD候选摘要），但依据 [ITEM08来源订正](STONEAGE-ITEM08-CHAR10-PIXEL-SOURCES-AND-BODY-MOTION-20261107.md)，其实际RD指纹来自**后期社区声称台湾8.5的另一来源**，2006官方PATCH129只供ADRN索引，**当前没有可读取的相应REAL载荷**。故不说它历史不存在，也不说已恢复原红宝石像素；本包不合成假图。六组可读原图是**以前已解码、这次私人复用**，本轮新增原RD解码0。

## 交付、验收和真正止点

- [QUEST06源限定JSON](../../research/recovered/STONEAGE-QUEST06-FOUR-VILLAGE-MAMMOTH-COURIER-SOURCE-R1.json)公开8条CREATE、4脚本/12交付段、8件原物品的双主表SHA、图像资格与完整证据边界；无原脚本全文、原商业美术、原程序字节。
- [QUEST06公开9项独立来源回归](../../tests/test_stoneage_quest06_four_courier_source.py)从三份锁定Git原数据逐创建、阶段、物品SHA重算，并拒绝虚构扣宠、同版图、同物品、官方起源、客户端已完成任务等变异。公开CI不充当私人原源的再读取。
- 私人 `StoneAge-QUEST06-mammoth-courier-original-private.zip` **40204B、SHA256 `cd26689805ad0c40e23ef934aa7c9509fe461630dd0431f7a43740abd7c91254`，13成员CRC全部通过**；含五原CP950文件、六原二维图PNG、私人索引/离线查阅页，已保存私人Library `/石器时代/StoneAge-QUEST06-mammoth-courier-original-private.zip` 并从库重新完整取得、整SHA及全成员CRC复验一致。没有把原商业文件投放公开Git。
- 不误记O61—O65的旧虎任务为本次新增成果。历史2.7MB `CURRENT-STATE.md` blob `c89e0e33537990aa2132b47c40fef49a985a935c` 原样保留，Stage A **7 PARTIAL + 2 OPEN**、B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、总体百分比UNKNOWN。

**NEXT：**有合格原商业同部署交付/奖赏调用实际记录时才验证支出、经验、事件状态和宠物处理；若后期22322真实REAL或同版NPC图号16018/16092合格原RD取得则追加对应私人可视内容；否则按22域/模块工作顺序转其他有可读原件的内容，绝不为LV30空档造玩法修正，也不进入引擎/网服重建。

