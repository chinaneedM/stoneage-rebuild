# INTEGRATION72｜梦幻洞窟供物与三件来源奖励的四幅台湾1.0原像候选（2026-11-11）

## 从真实主线启动；增量与去重
已重新核远端 `main=7dcfdb85526756551d54ae342e40196f6b675dc7`／tree `ec9771cc7acdb55167003bcf7aa422a8a0315c6e`、同HEAD **26/26 真正成功 Actions**、连续性协议/完整 2,709,173B 历史 CURRENT blob `c89e0e33537990aa2132b47c40fef49a985a935c`、最新 INTEGRATION71 正式验收及 QUEST09/ITEM01 旧收据。旧 CURRENT 完全未改。QUEST09 原已恢复静态梦幻洞窟两脚本、两原DAT、入口；INTEGRATION56 已覆盖守卫动作像。本包不复做脚本提取/守卫：仅把未专项组合的**供物→三种源奖励→四个实际台湾1.0零售 RD 像素候选**做有界来源联接。

## 原NPC与任务命令的保守合同
真正重读社区后期 mixed25 私人 NPC ZIP：**995,176B／2,205/2,205 CRC**，`seimu/event/event01.create` 677B/SHA `df0d8f32422cc149ed1574a8b6f43a896aa690260c3d7cfd4aa83705efb980b2`，两原脚本 `event01_1`、`event01_2` 完整 SHA 分别 `ac2c035d074904a575448ee424e1c5d0ff9939de60a73f149ddb47799ed9189d`、`38479dec3f115343debb9d1ad74ee6383bf9847595fa514f0a720f7b77587d0b`，均与旧 QUEST09 索引吻合。CREATE 中41、42层为图16024、坐标(34,25)的仙人，6000层为图16001、坐标(73,54)的老人。三 CREATE 都是既知原记录，新原脚本数=0。

| 原事件编号 | 老人原REQUEST | 仙人原ACCEPT |
|---|---|---|
| 34 | GetItem 2603 | DelItem 2603；GetItem 2604 |
| 33 | GetItem 2603 | DelItem 2603；GetItem 2605 |
| 32 | GetItem 2603 | DelItem 2603；GetItem 2606 |

以上是原段的静态来源命令，原条件、各段SHA及源码物理顺序保存在公开 JSON；没有原游戏交易、发奖、分支优先级或等级门槛的执行证明。`event01_2` 另有编号173/物品19550的后期叙事分支，**不可混入**本四物品关系。命令未写数量则不补 `*1`。原地图41/42已由QUEST09另核DAT；6000只是现有955份来源批次缺同名DAT，不能当作游戏中地图不存在。

## 真原位图与来源身份
从私人 ITEM01 5,868,386B／838成员源档重新逐条核对ID2603–2606的**两份原94列整行SHA（8行）**；四ID的原别名依次14648、21000、21531、24212，对应不同真实 TW1 零售原ADRN物理bitmap 5600、6301、6396、6979，尺寸44×55、32×46、44×43、48×42。四幅先前已真实解码的原RD候选PNG在本轮逐文件SHA与解码后RGBA SHA **4/4吻合**；助手目视了四幅原候选图，晶体、衣服、帽子、竖琴形态各不相同。本轮未从原零售REAL重新解码任何新RD：**new_RD=0**。新材料是跨NPC源控制、原物品行和原位图的四种内容关系，并非新获得四种原图片。

台湾1.0真实客户端与后期社区源物品／NPC为**不同载体**。别名、RD、原像成功关联不证明同一官方运行部署、物品效果、原版装备绘制器、原图当时调色板/透明度、仙人16024的原本NPC显示或原任务执行；不得把后期源脚本倒灌为JSS1999、台湾1.0或大陆1.82同服事实。

## 私有原件保管、验收和接力
私人12成员证据ZIP包含3完整NPC源文件、4项双表原94列来源行、4幅真原零售PNG与一份明细清单；**18,371B／SHA256 `1fc467e7068ef12e6de068aa710b785dcd47d297facaef5f60c72f8f7cab5dae`**。已存个人 Library `/石器时代/StoneAge-INTEGRATION72-dream-sage-four-original-item-pixels-private.zip` 并从独立目录重新回读完整ZIP逐字节、SHA及12/12 CRC吻合。版权原始脚本、物品原文、RD/PNG与私人合成图**均未进入公共Git**。

公开报告为 [INTEGRATION72 来源与散列证据](../../research/recovered/STONEAGE-INTEGRATION72-DREAM-SAGE-FOUR-ITEM-TW1-ORIGINAL-PIXEL-SOURCE-R1.json)，仅有数值、短名称、片段SHA及负证；公开测试交叉验证QUEST09/ITEM01已存索引，不能称公开CI重新读取私有原像。Stage A **7 PARTIAL＋2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、完成率 `null`。**NEXT：** 另选不重复且有真实原件的地图/NPC/宠物/道具关系；本四件已止点，不扩脚本解释器、网络帐号、原服务器或现代新引擎。正式候选与主线 Actions 只据新HEAD实际结果后验。
