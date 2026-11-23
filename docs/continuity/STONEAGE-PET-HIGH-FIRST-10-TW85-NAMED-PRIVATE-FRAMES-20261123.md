# PET-HIGH-FIRST-10｜台湾保存 8.5 原版客户端雷帝斯洛：具名原图与旧私人 8 帧像素对接

日期：2026-11-23。**仅经典2D PC《石器时代》宠物模块。** 本包不重新下载巨型客户端，也不伪称本轮重新解码原像素；重用独立历史R30真实像素验收及PET08/PET09新恢复的原程序本地姓名，让已有原帧第一次具有可复核的原客户端本地姓名关联。

## 四条独立的同源实证链

1. 原始私有像素：历史[台湾8.5 R30原8帧报告](STONEAGE-TW85-ORIGINAL-RD-PRIVATE-R30-20261026.md)与[源run 40329157425](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40329157425)。已按完整原包和原ADRN/REAL SHA逐字节核实、解出真实8个原RD中的原调色板索引图像，私人灰度接触图已目视。那一轮没有本地姓名，原R30报告的“name unverified”历史状态不删不改。
2. 2026-11-23 [PET08原四程序图号到相簿名选择器](STONEAGE-PET-HIGH-FIRST-08-TW85-NATIVE-SPR-NAME-BRIDGE-20261123.md)：台湾保存安装器四套 sa/sb/sc/sd 原程序，对SPR图号101501均走到相簿槽362、第一整数305、原名“雷帝斯洛”、本地头像逻辑别名28429，各轨28字节原名字行SHA完全一致。
3. [PET09逐SPR原帧与头像原RD来源索引](STONEAGE-PET-HIGH-FIRST-09-TW85-VISUAL-ACTION-REFERENCES-20261123.md)：原物理SPR组1185整段SHA与旧R30逐字节相同，原动画索引1恰含8帧。原R30八原物理位图号303039—303046的每一整RD SHA、原ADRN行哈希、原像素索引与灰度PNG哈希均在本轮源限定证据中逐项绑定。
4. 头像单独关联：本地逻辑头像别名28429对应原华义补丁与保存TW85的物理RD位图303372，原尺寸96×104，原RD SHA fa9ddb2acabd1a5bf03be3d6b08ee079ccf36badaaf70558d8d817aafc04523c。它**不是**旧R30实际解码的8张动作图，而且头像在本轮没有新解码。

[PET10机读证据](../../research/pets/PET-HIGH-FIRST-TW85-NAMED-PRIVATE-FRAMES-R1.json)包含四份原Git blob的定量锁定、四轨同名条件、原完整SPR SHA、逐原帧RD/ADRN/私有像素SHA与明确证据边界；[可重复核对脚本](../../tools/stoneage_pet_high_first_tw85_named_private_frame_join.py)与[反向篡改测试](../../tests/test_stoneage_pet_high_first_tw85_named_frame.py)阻断篡改别名、SPR号、RD像素、跨轨不同名。

## 具体完成与未完成

- **新增已证内容：** 1条经典PC高版本来源本地宠物名“雷帝斯洛”→原SPR图组101501→已私人真实观察的8个原RD动作帧的**跨记录源级关联**；原本R30没有这个名字。
- **未新增的旧成果：** 旧R30实际解码/目视8帧；**PET10新增解码0帧**。原图像本轮没有放进公开Git，不以原索引/哈希假装此刻看到了RGB彩色/实际游戏动作。
- **仍未证：** 声称台湾8.5的第三方保存包不等于独立认证运营商原零售光盘；本地编译名称不证明该宠物实际对玩家发行。官服Pet ID、原服PetMaster、初始三围、元素、成长与技能、捕捉/活动/发放日期、原动作数值2的正式语义、方向动画或帧率以及原RGB/透明/官方运行实际演出，全部保持OPEN/null。来源原名仍为繁体“雷帝斯洛”。

[逐宠参考条目](../pets/TW85-SOURCE-G101501.md)面向未来同版本资料补证。PET依旧唯一活动模块；Stage A 7 PARTIAL + 2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，总体完成率UNKNOWN。完整历史 docs/CURRENT-STATE.md blob c89e0e33537990aa2132b47c40fef49a985a935c 完整不覆盖。

**NEXT PET-HIGH-FIRST-11：** 优先复用已合法保存并实际观察过的更多PC高版本私有原画面，与PET09原生姓名表批量关联（有源且可验证才列）；缺此前私有原图时，只在原客户端原字节可合法直接取得的具体源上有限私有解码新头像及原动作，不重复无收益的巨大下载。同步探索原运营同年官方实发及同部署服务器宠物原表；不得以原资源数量冒称正式物种总数。
