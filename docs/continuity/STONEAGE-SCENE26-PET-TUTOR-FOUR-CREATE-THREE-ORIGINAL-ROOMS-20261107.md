# SCENE26｜四处源宠物导师创建配置 × 三张原室内DAT × 同一份原消息脚本（2026-11-07）

## 1. 本次真实材料恢复

以远端主线 HEAD `c6a8aa84b3bc459f99f94fe794c17cba2d2a507e`、tree `8b274ae941f821691854c31c669bc5e7d340ba6c` 重新启动；重读原生完整 `CURRENT-STATE.md` blob `c89e0e33537990aa2132b47c40fef49a985a935c`、连续性协议、设计/来源和最新11项主线 Actions。INTEGRATION04/05 已验合并，本次按其“跨域回22域、优先新实际内容”要求**停止纯来源索引扩写，取真实私人已保存的原配置/对白/地图字节开展一处可见NPC内容组装**，不再做旧资料重复关系表。

从个人 Library 真实取回并核完整源ZIP：
- `StoneAge-CHAR01-mixed25-all-npc-original-private.zip`：995176B，SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`，2205成员完整CRC成功。原文件 `npc/sa60/newbie/newbie.create` **1548B / SHA256 `761dc3d1ed885fb76b22af446331e5a0db6cf3e59a27cf2ab136a62a88d81d0b` / CRC `3f411954`**；同包原 `npc/sa60/newbie/petmaster` **1365B / SHA256 `04ba49ba514eb469b4c12085c6733cd73c281c6ca682c813c2e35748ab6ac1db` / CRC `e63fc8d8`**。两源均 CP950 无损解码，原 SHA 与已有 QUEST05 源创建/参数文件哈希**完全一致**，不是根据同名文件夹猜测对应。
- `StoneAge-MAP07-private-28-original-room-scene-candidates.zip`：34044818B，SHA256 `2b356fefa1f5c634a2a64837b20904e124ab9839ad6a4e3b9a642e3c05df29a2`，351成员 CRC 成功。重读 1003 / 2003 / 3003 三份原5,408B DAT，完整SHA逐件吻合 QUEST05 与 MAP07 原报告；读三原格平面 u16 并复核原场景PNG完整 RGBA 对 MAP07 已有真实源报告的SHA；没有重新解码台湾1.0的原RD商业资源。**1003、2003、3003的图形原像素是TW1留存原图候选，DAT/CREATE是后期社区保存mixed25；同源重合不得升级为初代官方部署。**

## 2. 四个原NPC配置和实际观察止点

源 `newbie.create` 的8个创建块中，原块序号4—7均直接引用同一原 `changeevent|file:sa60/newbie/petmaster`。下面地名词仅引用**本后期源CREATE中的繁体注释**，不是初版地理归属鉴定；`borncenter` 是来源静态创建位置，不是原客户端运行坐标验证。

| 原注释短标签 | 楼层原ID | borncenter | 源图形号 | 私人原DAT/画面 |
|---|---:|---|---:|---|
| 薩姆寵物店解說員 | 1003 | (19,15) | 16122 | DAT整SHA核同；原像素候选场景，现代坐标标记 |
| 漁村寵物店解說員 | 2003 | (11,12) | 16127 | DAT整SHA核同；原像素候选场景，现代坐标标记 |
| 加加寵物店解說員 | 3003 | (16,19) | 16122 | DAT整SHA核同；原像素候选场景，现代坐标标记 |
| 加魯卡寵物店解說員 | 4003 | (14,17) | 16122 | **QUEST05已有同号完整DAT SHA且MAP09来源候选就绪，但本次私人MAP07小包未收该文件；未绘图** |

四块配置原 `name=寵物常識解說員`、`dir=4`、`createnum=1`；这是四条源配置，**不是四个新物种、四套人物动画或四个原版场景已运行的证据**。三个实际有DAT原字节位置分别读得三个平面u16 `[5000,0,49152]`、`[5006,0,49152]`、`[5000,0,49152]`，原数字不解释为碰撞、触发或通行格。

离线坐标标记复用已有MAP07现代等距观察公式 `(16+(x+y)*32,712+(y-x)*24)`，三个原 `borncenter` 的**现代投影**分别为(1104,616)、(752,736)、(1136,784)。全画布坐标同既有MAP07原格 `placements` 的原始图层anchor一致。黄色圈是本次新加的**研究标注**，没有补造原NPC 16122/16127 的任何动画像素；原NPC选择图、原客户端遮挡、颜色和实际对话运行仍OPEN。

## 3. 同源真实脚本内容，但不当原版实际规则执行

重读的 CP950 原 `petmaster` 文件包含 `TYPE:MESSAGE`、`EVENT:LV>0`、一段主句和八段有编号的窗口说明。原脚本表述的教学主题包括宠物忠诚度、战斗/逃跑、死亡可能影响忠诚、道具提升忠诚、料理/合成/修复、宠物店技能学习以及抓1级野宠的**NPC建议**。本原文件没有字面 `GetPet:` / `GetItem:` / `DelItem:` / `DelPet:`。这是**原配置与静态对话的实际文本内容**，不证明运行态忠诚度计算公式、NPC开窗成功、商店技能实际提供或历史初始版机制。如果原NPC所言与其他版本的代码/资料有差异，保留两者版本来源。

## 4. 新私人可见交付与公共验收

新的 [SCENE26逐源派生数值回执](../../research/recovered/STONEAGE-SCENE26-ORIGINAL-PET-TUTOR-FOUR-CREATE-THREE-SCENE-SOURCE-R1.json)只存四原创建的SHA、坐标、图号、三DAT原u16数值及原私人图像的 SHA；不发表原 `.create`、完整脚本、DAT格正文或任何原PNG。公共测试 [SCENE26来源契约](../../tests/test_stoneage_scene26_pet_tutor_original_source.py)以固定Git blob验证原QUEST05及MAP07公开报告中的4原创建键与3地图整SHA、映射坐标公式、4003有源但本次**私人MAP07包**没画面的严格区别、未证原运行/地理标签等负例；**公开CI不能重新执行本次私人原资源核验**。

私有一键阅读交付 `StoneAge-SCENE26-pet-tutor-three-rooms-private.zip`：**3275768B，SHA256 `826b81df283f311d00b3a4ab4067782647e23ef99493fe2b5f3d6e450f24dab2`、12个成员CRC全过**，包含三个带真实配置坐标标记的现代候选原图、三原DAT、两原CP950配置/脚本、源保管JSON、可独立打开的完整HTML及对比图；HTML SHA256 `a3178d6992b9a125b2de852001ccd348b5d8218f025cb255e5bdc3efd29ac8a6`，合成预览PNG SHA256 `2cc5633df64d392495db73600d4a5ba197692d22e6b14d2270c5e02432683446`。上传至个人私人Library `/石器时代/StoneAge-SCENE26-pet-tutor-three-rooms-private.zip` **成功**，从Library重新完整下载后核总SHA、长度和12个成员CRC全一致。原商业文件仅在私人档案中保存，没有进入公开Git。

**本轮唯一历史新增证据范围**：两原源文件整SHA实际重验 + 三份真实DAT格位置的原数值 + 具原文本注释的四条NPC出生候选和三张带精确来源坐标的离线可观察地图。实际原服务端进程/客户端运行0次、原NPC精灵图真实恢复0、新地图源0、同版本官方身份0；不能把本可见成果当“世界已可玩”。

Stage A仍 **7 PARTIAL + 2 OPEN**；Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、overall百分比未知；所有旧 `CURRENT-STATE.md` 保留完整历史 blob `c89e0e...` 原样未写。

**下一优先**：先以现有资料核16122/16127是否有具体合格同载体动画/像素与原生选择证据，**只有新实物时**加入NPC可见实体；若无，保留SOURCE_BOUNDED_PARTIAL并回其他有原字节可读内容模块，不继续为本NPC扩阅读器框架。4003原DAT本身在955清单已有SHA，等私人合格DAT包实际可取回时补最后一张观察，不能记录为原游戏“缺地图”。
