# SCENE26 | R40 原宠物组 action=1 逐方向帧序列（有限材料合同）

**来源和定位**：这是对已保管的 R40 同一混合 2.5 客户端/服务端材料的 **新增结构化视图**，不是新客户端下载、原像素重放或进入原游戏。冻结基线 main `fd16de29f24934629559ba8c404e05c180d36259` / tree `1280a6585ec3f391a2e4366845427601670f1cbc`。原数据来源 `research/recovered/STONEAGE-PRESERVED-PET-SPR-SOURCE-R40.json`（Git blob `5b49d54d7cff2d79d3610db7ca4a37108f1f9e03`），跨版同段证据 `research/recovered/STONEAGE-PRESERVED-PET-SPR-MATERIAL-R40.json`（Git blob `cdcfc9fb9a07c60a3320528fdddcdfecdeb6b14d`）。22 域/R102、SCENE11/13/20–25 去重之后，单独补充此前未发布的 action=1 逐帧材料。现有 SCENE13 为 action=0，SCENE11 为 action=2，不能借用其可视化来称 action=1 已运行。

## 有界结果

| 原组号 | R40 索引 | 方向 | 原帧位置 | 唯一位图号 | 每方向的位图位置模式 |
|---|---:|---:|---:|---:|---|
| 100250 | 240 | 8 | 32 | 16 | A,A,A,B |
| 100251 | 241 | 8 | 32 | 16 | A,A,A,B |
| 100252 | 242 | 8 | 16 | 16 | A,B |

总计 24 条方向序列 / 80 个有序帧位置 / 48 个不重复位图号；**80 条原声字段值均为 0**。帧重复位置原样保留，不合并成抽象二帧。这三个组 R40 已记录与原台湾 1.0 / CN5.0 的相同组号 *完整 SPR 段字节同一*；只认证被比较的片段，不认证物种、原服务器部署、音频事件、角色归属、绘制完整性。

每条机器记录保留 group/index、原始 animation index、direction、duration word、header/end offset、全部 [bitmapno, x, y, sound]。原 duration word=100 **不等于 100ms / 100FPS**，action code=1 **不是已经证实的站立/行走/攻击等名称**。同一原位图号不构成宠物种族命名或复原完成度。

## 可复算与止点

`python3 tools/stoneage_scene26_pet_action1.py --check` 首先计算两个原研究文件的完整 Git blob SHA，然后逐条交叉匹配原报告和各区域完整段校验，验证8方向顺序、模式、计数和字段边界；拒绝缺方向、伪跨版相同、变帧和新增声字段。专用 CI 只读公开数字元数据，不接触原 WAV/PNG/REAL/SPR 字节。公开 JSON 未储存版权图像。

**结果级别**：FACT(原 R40 数值、交叉片段同一)，OPEN(原绘制像素、每帧动态外观、准确动作语义、帧时间、原实际音效、具体宠物/同服、原世界执行)。**新历史来源=0**；新交付是可抽取、可验证的原帧顺序合同。

**后续允许继续的明确触发**：私人原版材料可合法复用且经全文件 SHA 重新读取（`spr_4.bin` SHA256 `865b58860c7fe025850bf942f6ce6a5deb4464993ceeecbc20a034c99e159749`，`spradrn_5.bin` SHA256 `5f13c956cf013e073298ab91667d3aaa17767b26ba94d696514726950ce94de6`，相关 ADRN/REAL/Palet 实字节与先前收据核同），才能制作此 action=1 的 **原像素** 8方向时间线并与独立解码器对照。原件不可用时不连续扩展 helper，下一轮轮换到有精确原实物的战斗/人物/地图交互；禁止用合成图替代原图证据。Stage A 保持 7 PARTIAL+2 OPEN，Stage B/百科 GATED，R79 PAUSED，overall_percent=null。
