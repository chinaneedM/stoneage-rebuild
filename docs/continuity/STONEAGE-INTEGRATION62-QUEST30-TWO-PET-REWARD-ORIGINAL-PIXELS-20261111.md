# INTEGRATION62｜恐龙收集两条 GetPet 原奖励与29幅台湾1.0原RD像素联系（2026-11-11）

## 开工与唯一游戏内容目标

按项目连续性协议，从重新读取的远端 `main=1e647c8628be5f15a1888fc32b86ff2f4542c986`、tree `85e84361ff68c501ea655f50b52c9e917032c279`、最新提交及 Actions 开工。逐源重新核对 README、协议、完整历史 `docs/CURRENT-STATE.md` Git blob、设计/来源/时间/路线、模块工作单、离线优先级及 INTEGRATION61 最新正式验收。主线前一内容提交的27个 Actions 实际全部success，正式验收收据HEAD自身没有新Actions，不能将前一轮成功迁移过去。

最新NEXT要求选择已保存真实来源、不同于五诊疗室和主厨料理的宠物技能／任务物品／NPC场景材料，并先查重。查到GAMEPLAY03对21份原宠物技能店与23项技能ID已完整双表归并，QUEST31六任务物品原图亦已专项：这两项不重复。选择QUEST30恐龙收集任务已有GetPet:93／341、却尚缺实际早期原动画像素逐项身份证据的两条奖励配置。**之前QUEST30/WORLD21已经发现实例93／341与模板171／274的数字关系**；本轮不算新奖励或新原脚本。新增的是同源双宠物表差异界限，以及两图号到真实台湾1.0早期原SPR/RD保存像素的资格接合。

## 原任务、同档两种宠物表、版本分离

旧QUEST30证据含原创建 `seimu/event/event02_n.create`（floor100、borncorner四整数原范围230/180/525/200，不作唯一出生点）→ `seimu/event/event02_1` 8个旧 TYPE；其中#0 `GetPet:93`、#4 `GetPet:341`。两段原条件有事件35、道具2607与宠物数字，**未验证原条件中的逗号语义、EVDEL、事件先后、真正宠物交换**。源道具2607的NPC对白和同源itemset名称冲突继续留原证、不得靠同编号美术化解。floor100在既有955 DAT库无匹配，不把资料缺件判为原版游戏缺地图。

同一个后期社区mixed25保存RAR来源的原 `enemy.txt`／`enemy2.txt` 两套实例表均有 `instance93→template171`、`instance341→template274`；同保存RAR的 `enemybase.txt`／`enemybase2.txt` 两套模板对应图号都是 `100319` 和 `100362`。两套各行物理来源、整行SHA仍分别保存，**不宣称这两套表在原服务器同时生效**，更不把第一列物理行号误当实例ID。跨台湾1.0零售来源仅连图像的相同数值图号，不证明历史正式服同部署。

## 本轮真正重新读回的29张原图／6段源动作

从私人Library取得先前核过的 `StoneAge-PET07-original-sprite-private-catalog.html` **15,123,277B / SHA256 `58e8ee4ff5165ed2f61663d67ae1cd0a8183622fa3375c480232784bfce9dc76`** 和 `StoneAge-PET07-private-original-RD-verified-source-report.json` **1,617,404B / SHA256 `b5ad2e58930afbe90604a1d72e3c17ab0adea446e7c118be775e3973315e6cb4`**。解析私人观察页的原保存数据，不把现代页面当原游戏运行。与 Git 既有PET07公开初级来源逐原组SHA对应，实际对两组动作0/2/1、方向0共6条源序列，用小端uint32串联原bitmap号的SHA逐条一致。

| 原脚本奖励 | 同RAR源宠物实例／模板 | TW1原图号／原SPR索引 | 原动作0／2／1方向0源帧位置 | 真正不重复原RD图 |
|---|---|---|---|---|
| `GetPet:93` | 93 → 171 | 100319 / 293 | 13＋6＋2＝21 | 13张 |
| `GetPet:341` | 341 → 274 | 100362 / 332 | 17＋6＋2＝25 | 16张 |
| 合计 | 2个脚本引用，不是物种计数 | 2组候选图形 | 46个原帧引用 | **29张** |

从嵌入的真实原RD已解PNG中，本轮逐个**读取29张实际图片字节**，逐SHA256、Pillow原尺寸与原PET07保留收据29/29吻合。两组源SPR段完整SHA、每动作原帧顺序hash、每个bitmap的原RD源SHA/索引像素SHA/PNG源SHA均可在公开[派生目录](../../research/recovered/STONEAGE-INTEGRATION62-QUEST30-TWO-GETPET-TW1-29-RD-PIXELS-R1.json)及其引用的原PET07索引间追溯；两组按首次出现排序的全部29图RD+PNG+尺寸另保留独立聚合SHA。**本轮原RD二进制新解码=0**，不将既存截图冒作原客户端屏幕或本轮重新发现29个新原文件。

另外实际完整回读旧 `StoneAge-QUEST30-dinosaur-collector-event35-private.zip` **10,479B/SHA256 `cb6f27c43559049bd05976293c3fd260c9d0ba87cc50b5a93f7ea884b7f4225a`，8成员CRC全过；旧 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip` **995,176B/SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`、2,205成员CRC全过；未重新开361MB父RAR、原服、原客户端。

## 私人资产的合法保管与技术验收界限

新建来源限定小包 `StoneAge-INTEGRATION62-QUEST30-two-original-pet-reward-pixels-private.zip` **271,047B/SHA256 `e075d132aa5ad0a4da25ecb8aaf325785f676291c588b0702173b7216db61cc1`，含29张旧解真实原PNG、一份来源收据和一页现代离线图片对照，共31成员。已上传私人Library`/石器时代/`，再通过新的Library文件引用下载到另一目录，整ZIP逐字节一致／完整SHA与全部31成员CRC成功。**这些版权原图、原脚本正文和私人HTML一律没有放在公开仓库**。公开只有数值源位置、原文件SHA、动画序列数字与负界限。

公开专项测试仅根据历史已发布的 QUEST30／PET10／PET07 Git 派生证据回放：原GetPet分支、不把物理行序误作实例号、双表原SHA差异、源动作帧序小端hash以及29原RD/PNG聚合hash；它不能从Git CI重新读取用户Library内的原图，也不能证明原生宠物奖励、原画面或宠物品质。

## OPEN、阶段与接力

原版官方台湾1.0/JSS1999/大陆1.82的恐龙收集奖励是否同样为93／341、是否采用该混合社区服务端的模板与身份、宠物动画源动作语义与画面配色／帧率、真实战斗捕捉／给予宠物、图像原服同部署、原人物/地形/任务接触均未证。没有正式原生客户端或原服运行；不做账号/网服/单机新引擎。

`docs/CURRENT-STATE.md` 历史原Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`、2,709,173字节全部保留，按协议§14新增本续接及README指针，不危险替换巨文件。Stage A仍 **7 PARTIAL + 2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**，总进度百分比未知。

**最高NEXT：** 本轮QUEST30两组早期原像素接合闭合，下一项换另一条有真原件、尚未专项联接的任务物品／宠物技能／NPC地图与原二维像素资料；先从22域索引查重，缺合格原字节则保留OPEN止点。不重复本两奖励、原宠技能店已整合表，也不提前进行Stage B。候选/main CI和合并结果以未来实际远端后验写独立验收收据。
