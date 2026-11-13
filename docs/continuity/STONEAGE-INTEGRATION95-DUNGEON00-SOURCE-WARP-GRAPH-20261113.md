# INTEGRATION95｜原 `dungeon00.create` 147条静态传送源关系与原DAT资格（2026-11-13）

## 任务定位、历史边界和重启核验

本批从**实际原始保存文件**确认另一组未被INTEGRATION80 `dungeon03.create`、QUEST05条件传送目录取代的历史关卡材料：`genout/dungeon00.create` 的原始传送创建关系。目标是复原**这个确切保存载体内部有哪些楼层引用、起终点和精确反向配置**，不编造游戏实际可进入路线，不重建MMO、不开发新引擎。若出现实际来源缺失则记录止点，不做不相关扫描。

重启以当时fresh GitHub `main=d22ddcd3bb8890e3607c5c00d0c6c580d9e75d0b`、tree `daace0cccdff27292c100ad44f57ddb64c7699f7`、**26/26 exact HEAD Actions completed/success、0开放PR**为准，已读取协议及启动文件。大状态 `docs/CURRENT-STATE.md` **2,709,173字节** Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 完整、原样保留，接口的空文本不等于空文件。已查同一仓库历史INTEGRATION80/QUEST05及此前跨版图像工作，选此不同、尚未独立按原字节建整图的单来源档案，不计旧源为新历史版本。

## 本轮真正取回的原件：147/147源字节验证

从私人Library重新取回现存 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip`，**995,176B／完整SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`**，其全部 **2,205/2,205 ZIP成员CRC**通过。内含真正原始 `npc/genout/dungeon00.create`，**17,289B／SHA256 `1b3d189ea8ae5e42de4321efce19d3fb9517f0b25b6130ff0cb73761cd62514b`／CRC32 `c36d56ad`**。本文件前导注释自述由 `npcgen.perl` 处理 `data/npc/sainasu/dungeon/dungeon00.gen` 而来，**只是原文本中的上游路径线索，未取得和核验该 `.gen` 原件**。后期社区混合2.5父RAR已存原SHA `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`，本轮**未重新读取361MB原RAR**，不能把后代档案说成初代官方源。

用原全文件逐段重解析NPCCREATE和 `npcgen_warp|目标floor|x|y` 原整数，`floorid`、源 `borncorner` 原坐标、目标floor/坐标、原 `time=0` 和 `createnum=1`。每条的真实byte半开窗口与 SHA-256 **147/147** 匹配先前[CHAR01源段索引](../../research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json)。公开[INTEGRATION95机器来源记录](../../research/recovered/STONEAGE-INTEGRATION95-DUNGEON00-147-ORIGINAL-WARP-AND-PRIOR-DAT-R1.json)只保存这147条的数值、原段SHA、来源资格及图关系；**完整原商业CREATE正文仅在私人资料包**。

## 原文数字关系：严格反向与有向图不能偷换成玩法

- **147原创建配置／64个不同floor数字／117种不同的“源floor→目标floor”方向对**。其中 **30条**是在同方向楼层关系上有不同原创建点的重复floor方向映射，不是30个重复原文本或新地图。
- 按**起点floor+起点x/y与目标floor+目标x/y全部严格交换**寻找反向，**140条原配置具精确配对＝70对**，**7条缺严格反向配置**。不配对的真实原创建序号为 **14、29、30、67、68、69、70**：分别是10007→100一条、10204→10202两条不同源格，以及10601→100四条相邻源格。绝不由此判断原服只能单向传送或实际运行返回不存在。
- 以楼层数字形成**5个弱连通分量**（31、10、9、8、6个floor）；进一步形成**7个强连通分量**（26、10、9、8、5、5、1个floor）。这仅是**这一单一CREATE的静态配置图拓扑**，不是五个实际岛屿、七座地下城或全部商业原版世界结构。

## 同保存源DAT目录的可核查资格

与此前真实读取955份同社区mixed25原DAT所得的[MAP04源目录](../../research/recovered/STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json)按**同编号+原保存载体限定**连接。64个不同floor中，**53个有现存DAT完整SHA/文件字节数/头部尺寸记录**，**11个没有此保存目录的DAT**：100、200、1100及10301–10308。该缺失是本轮档案范围的**OPEN**，不证明游戏本身缺图或不可到达。

147条配置中，有**105个源端坐标**可依据旧原DAT头尺寸核界、**100个目标端坐标**可核界，全部**205/205为尺寸内**；**92条配置的双端都有旧已验DAT身份**，另外89个端点没有相应DAT头可核。既存MAP04还保存部分地图非零图元与TW1另来源像素的原候选索引；本轮**未新读取原DAT字节、没有新解码地图图像、没有逐原格核碰撞/原画面**。旧DAT源身份与后期社区CREATE同一个保存载体，并不独立认证当年商业原服部署；台湾1.0的原图更是另一个版本，不可自动并作同部署。

## 实际私人交付与浏览器观测

私人 `StoneAge-INTEGRATION95-dungeon00-147-original-warp-source-private.zip`：**10,610B／完整SHA256 `0e13f780dbd4263e74284329072c0bbb5c8f845647da2bf7916962b9de1a07d5`**，内含17,289B原CREATE、一个由147数值关系生成的**现代二维SVG有向图离线HTML**和来源声明，共 **3/3 ZIP CRC通过**。已上传个人Library `/石器时代/`，并**独立取回**，整ZIP实际字节/整SHA、3CRC、原CREATE SHA完全一致。没有向公开Git上传原商业文件。

真正Chromium `page.set_content` 启动同一HTML字节，实核64个图节点／147条源配置、5次分量过滤所得楼层数31/10/9/8/6，分别显示67/20/16/34/10条源记录、输入楼层定位、节点点击、恢复、跨分量定位和不存在楼层负例，**0 JS错误、0浏览器console错误、0外部HTTP请求**。因环境禁止直接`file://`启动，本轮**不声称成功文件URL导航**。这种SVG布局是现代证据查看器，**绝非原版地下城画面、实际客户端运行/碰撞/传送成功、新游戏内容或引擎**。

## 验收、源限定止点与下一步

新增公开回归9项覆盖旧CHAR01 147原段SHA、7缺严格反向、5弱分量、7强分量、53/11旧DAT资格、205原坐标界、独立私人原件保管及无运行误称。**CI只重算公开派生数值关系，不能自动重取私有原CREATE/DAT；原私源逐SHA审查在本地完成**。候选和合并后真实GitHub Actions均需要按精确SHA验收，不预支成功。

本模块**SOURCE_BOUNDED_PARTIAL**：原文件147条的数字来源链闭合，但历史游戏实际传送、激活、地理身份、原DAT缺件及初代版本资格未闭合。Stage A仍**7 PARTIAL＋2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、overall_percent=null。**NEXT**另选同一保存档案中有真实原字节增量的不同地下城或任务内容；如果需要确认本图传送实际运行，必须获得明确同部署原生客户端/服务端运行轨迹，否则保持OPEN。避免机械重复画同一个来源数字图。
