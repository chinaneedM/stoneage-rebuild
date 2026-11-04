# Stage A | WORLD06：36组任务GETPET数值的台湾1.0真实原像素候选观察（2026-11-04）

## 来源与执行边界

此批从已验 GitHub main `2d7020304e6fb7004c2a4e63c0325b036eae42e8` / tree `55203c28106acbe66b888150560c7da301d1d3c3` 继续，承接[WORLD05原任务→实例→模板→SPR链](STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-05-GETPET-PET-SOURCE-20261104.md)。不改完整历史 `docs/CURRENT-STATE.md` blob `c89e0e33537990aa2132b47c40fef49a985a935c`。

**本轮实际取回私人用户Library已有**台湾1.0 PET07原SPR像素观察材料，并核整文件SHA：
- 原已验私人来源报告 `StoneAge-PET07-private-original-RD-verified-source-report.json`：1,617,404B / SHA256 `b5ad2e58930afbe90604a1d72e3c17ab0adea446e7c118be775e3973315e6cb4`；
- 原私人完整HTML原像素观察器：15,123,277B / SHA256 `58e8ee4ff5165ed2f61663d67ae1cd0a8183622fa3375c480232784bfce9dc76`；
- 原130组联系图：692,966B / SHA256 `69f08d2ca66d6dca8fdc7e7099df5c3c53aefc28c631548c8e27f346541f6ea3`。

由同字节HTML完整解析2,540个嵌入原像素候选PNG及130个分组，沿WORLD05的正确实例外键关联的**36个图号全部命中**；每组真正读取一帧私人PNG字节，并与既往实际从台湾1.0原REAL/RD解码的[PET07 逐图源收据](../../research/recovered/STONEAGE-PET-MODULE-07-TW10-BATCH-PUBLIC-R1.json)里对应的原bitmap、RD_SHA、候选PNG_SHA做精确核对，**36/36摘要一致**。本轮并未重新从原REAL读取、二次解码新的原RD，新增原游戏资产=0；新增的证据是**现存原像素与原任务静态关联候选的有界、独立复核和私人实图比对**。

实际目视新作私人36组静态参考图，共329,045B / SHA256 `411665dc6a2a9aa1bf46fc60ff864f3e518b15ab3bb41a7be5a492684b5aa396`，未上传公开Git。每个卡片明确显示GETPET数值、按原敌人实例真实外键关联的宠物模板ID、台湾1.0真实像素的同数字图号与真正选用的原动作/方向/位图。原版权素材和私人图库仍保持私有；公开仅保留从两端公开源证索引衍生的数字、SHA、原RD尺寸、动作选择与失败边界。本轮私人逐帧核验收据SHA `58a7f5def92ae0ba91f344b1615c9449d89da4fb7d21e445b74ed1a58365efb2`。

## 不能抹平的3个源差异

- **33组**：原动作0/方向0的首帧即可与PET07当前原RD→候选PNG SHA吻合；
- **100329/100330两组**：私人旧图库动作0首帧分别仍是PET06已记录的旧候选PNG摘要，与后续PET07当前候选PNG编码摘要不同；**并非原RD被篡改**。本轮没有把旧图库PNG伪称当前PET07验真帧，而各选择原动作2/方向0的确实保存帧113521、113769，且逐SHA与原RD收据中的PNG一致；
- **100401组**：原动作0/方向0有26原帧位置，但含位图82729，其原RD已由PET07记录严格RLE解码溢出，因此该整动作序列不能显示为完整合格图。本轮只选保管中动作2/方向0原有效bitmap82737。**不填补、不推算缺失帧**。

另沿WORLD05保留模板`718/719/720`的PETFLG两候选表冲突（原GETPET数字1479/1481/1483），不可根据外观判断其历史宠物身份/活动身份。见[本轮36条逐源元数据与特例](../../research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-06-TW10-GETPET-ORIGINAL-PIXEL-BRIDGE-R1.json)。

## 仍然OPEN与下一工作

台湾1.0 SPR、ADRN、REAL的**原像素收据**与后期社区mixed25任务数字均真实存在，但同数字**不等于同原SPR段SHA、同一官方服务器、原任务实际发宠或原客户端真实画面**。两样本的正式历史身份与执行链继续严格分离。私人图为现代资料观察，不是已进入原版游戏或正在开发新石器。公开Actions只重跑派生表间的对应/负例，不能读取私人原图替代本次图像目视。

Stage A保持7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，overall_percent=null，历史CURRENT原字节不变。

**最高 NEXT WORLD07**：36组图像已达材料性止点，按模块轮转到另一批实际可取原件的任务/战斗/机制/声画交互缺口；若没有新原版原件则记录受限止点，不重复修图库或泛用观察器，不做账号/联网服务，也不开始体验优化。
