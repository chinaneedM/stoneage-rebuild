# INTEGRATION78｜骑乘学习同意书、四村训练师及台湾1.0原图候选（2026-11-12）

## 启动来源和实际新内容

从2026-11-12新读取的`main=74aaaccdb59fc4fce94e6bb8b300821c83b21170`／tree `0ba0c825470170a5204ff39afc8c995e24ebbc22`、该HEAD **26/26 completed/success** Actions起步。重新通过Git blob接口读取完整历史 `docs/CURRENT-STATE.md`，确认 2,709,173B／blob `c89e0e33537990aa2132b47c40fef49a985a935c`，不将空内容文件接口误当历史文件为空、不改写或截断历史。按连续性协议§15–18继续Stage A纯历史内容恢复；本批回到玩家可见的**骑宠学习文书与NPC来源接缝**，不开发现代游戏、不建立网络服务器。

此前[GAMEPLAY02](STONEAGE-GAMEPLAY-MECHANICS-MODULE-02-RIDER-PET-TALK-20261103.md)和[RIDERMAN R1](../../research/mechanics/STONEAGE-RIDERMAN-CORE-R1.md)已分别验证四训练师`conff:`、四档费用和后代固定源码里已停用的骑乘同意书检查。这些旧结论**不是本批的新发现**。本批新的实物级业务整理是：**16条原骑乘同意书物品行 ↔ 四个训练师及四个制证秘书的同源配置 ↔ 一幅另一载体台湾1.0零售实际原RD像素候选**，特别固定两份后期原itemset之间的关键负证（这16 ID仅在`itemset0710.txt`，另一份`itemset.txt`没有）。

## 私人真来源逐字核验

- 现存用户个人Library的社区混合2.5保存NPC提取ZIP `StoneAge-CHAR01-mixed25-all-npc-original-private.zip`，995,176B／SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`，**2,205/2,205** ZIP成员CRC本轮全通过。直接读取九份相关原`npc/`文件、逐实字节SHA/CRC；不是台湾1.0原商业服务器同构建。
- 已保管ITEM01私有整理ZIP `StoneAge-ITEM01-private-two-itemsets-832-original-RD-icon-observer.zip`，5,868,386B／SHA256 `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa`，**838/838** ZIP CRC通过；原私人catalog `private-full-catalog.json` 32,057,594B／SHA256 `0438c4fc9bf945223d46c24e9d374de436f2ac981c23fa282776281c2e772e60`。
- 该catalog原源登记原`gmsv/data/itemset.txt` 3,392,473B／SHA256 `a415e78f9aab2e5ea5ca92ecb7430253f7be1ba7c876d6b0bb6d067b1b466688`、另`gmsv/data/itemset0710.txt` 3,668,487B／SHA256 `6d6d63fda59c6bda2f239fe18c9361b5c9da18c84f678b7cc95bde24544292fb`。**本轮读取的是已保存并有先前原源验收的私人完整94字段转录及原行SHA；本轮没有再读这两份原始RAR成员字节**。全部16条按CP950和原94列重构后逐完整SHA等于原行记录；另独立核20833双表原整行SHA一致。文件名“0710”不认证发布日期、官方版号或实际启用表。

## 本轮来源可证明的关联（FACT，限所列源）

1. **十六张同意书，一幅旧原图候选。** 物品ID依次是`19005–19008`、`20224–20228`、`20296`、`20766–20767`和`20813–20816`。16/16源行仅存在于`itemset0710.txt`，全部别名图号`24176`；在另外一份`itemset.txt`是0/16。不是16种原生骑宠，也不是16幅不同图像。两份物品表都来自后期保存源，不能当台湾1.0当年道具主数据。
2. **四处训练师（原同载体创建）。** `family/riderman.create`里4个原创建块对应`family=1/2/3/4`、floor`1040/2030/3030/4030`、原图号`16017/16002/16002/16002`，都以`conff:family/riderman.conf`指向同一真实源。该配置原窗口`110/120/130/140`列`takegold=5000/10000/15000/20000`，每档保留4个`letter1..4`数字`19005–19008`。源文字等级上限为40/80/120/全级，但此处没有原服务器实测，且此前固定后代源码R1发现`letter`前置检查处于`#if 0`，不得声称四张同意书被运行时要求、消耗或费用实际支付。
3. **四处秘书与九个制证字段。** `family/fmletter.create`有4个同源`conff:family/fmletter.conf`引用：floor`1041/2031/3031/4031`，图号`16065/16065/16027/16030`。原`fmletter.conf`窗口20的`letter1..9`字面对应`19005–19008`和`20224–20228`。九个字段不是已执行制作的九张物品；`20224–20228`没有直接进入上述四档训练师的`letter1..4`，不能补造更多已部署训练点。
4. **特殊骑宠以及未接入其他同意书。** `npc/family/rider.arg`、`npc/sa60/rider.arg`与旧`.bak`都有`TRANS=5/6`、`ITEM=20296`及`AddItem:20296`字面，对应同保存包两条原`floor1040`特殊NPC创建候选。它们是不同原字节变体，不证明实际二者同时载入、发证成功或当时机暴可骑。另6件ID`20766/20767/20813–20816`本批只在物品表找到源行，不强接未获证的NPC。
5. **明显不同的换券不能混同。** ID`20833`“騎證換兌卷”在两份物品表均存在且原整行SHA一致，但原图号是`24371`，在当前认证台湾1.0 ADRN索引中0匹配，**不是**上述图号24176，也不能因为名称近似推成相同道具或同一骑证手续。

## 本轮真正可见的二维来源

另一**认证台湾Waei/JSS1.0零售客户端**原ADRN/REAL/RD保存索引已有单一图别名`24176`→物理RD`6840`、52×44、原RD **1,524B**／SHA256 `cddd1a18dec031cec9d9d128da11f41500d8d101663ab1100eb17f066b9d0146`、原索引像素SHA256 `7ce15d463e70ca1177d37ec5260ae3bbbb5de265b60a04c77bbf027e65727f7d`。本轮直接从既存ITEM01私人包实取已解原PNG **2,786B**／SHA256 `82334c031191fb20b31f6a469a9a9985dac36592ba362defc8ed0b9a15a06572`，以Pillow确认RGBA尺寸52×44并实际目视候选文书样式。**新增独特原RD解码0、新独特原图0**；新增的是源文书身份与原视觉图的关联资格，跨载体同图号不证明原台湾1.0服务器存在这些ID或当年选它显示。

私人本地离线图文资料 `StoneAge-INTEGRATION78-riding-consent-original-source-private.zip`：**17,977B／SHA256 `390b2da733861c00875173eefeab689e0b3e717b2e857e063d6cb99a24e6aef8`，14成员**，包含原PNG、上述原NPC有限文件、选取原94列SHA匹配行及静态自包含HTML。已成功上传用户个人Library `/石器时代/`，又从独立Library返回文件再次完整按字节/ZIP SHA比对、14/14成员CRC通过；内嵌原图PNG和单独源PNG完全相等，HTML无脚本及外部HTTP引用。现代离线HTML并非原生游戏UI；本轮无浏览器运行声明。原版权图片、NPC和原94字段都只在私人包，未进入公开Git。

## 验收与止点

公开[机器来源/编号/逐行SHA/来源负证](../../research/recovered/STONEAGE-INTEGRATION78-RIDING-CONSENT-ORIGINAL-ITEM-PIXEL-SOURCE-R1.json)只包含数值、短名称和SHA；新的12项公开回归断言16项物品表身份、4训练师/4秘书、9字段、16只在B表、特殊20296和20833负例、真实旧原图摘要以及Stage A范围。CI只能证明这些已发布派生数据仍自洽，不能访问私有源或证明原服骑宠实现。新验证必须依真实Actions后验记录，不提前声称成功。

**OPEN：** 文件名0710的发布日期和对应官方构建、真实活动表的加载/跨文件跳转、原商业服同意书检查与消费、客户端实际图号选择、原骑宠资格及宠物形象、原台湾1.0同版同服归属；后代固定源码`#if 0`并不证明所有更早官方服都停用。保持Stage A **7 PARTIAL + 2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、overall_percent=null。**NEXT** 不重复骑宠课程源码；下一批寻找其他未复原的真原图/地图/宠物内容关系。完整旧CURRENT历史Git blob维持不变。
