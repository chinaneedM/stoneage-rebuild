# INTEGRATION56｜梦幻洞窟双守卫原地图与台湾1.0原像素：正式合并、私人保管及Actions验收（2026-11-11）

## 启动基线及源事实

- 本轮按 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` 从 GitHub 最新main `5661035716f3355cfb6b91f24c85a00fb583d663`，Git tree `21beb282867277ca1ef12e579b2a84e22129f515` 重新启动，重读分支、HEAD、tree、提交、Actions、README、协议、CURRENT完整Git blob、设计、历史、来源、路线与最新INTEGRATION55。
- 原 `docs/CURRENT-STATE.md` 本轮源blob `c89e0e33537990aa2132b47c40fef49a985a935c`、**2,709,173字节**，由于普通内容API空响应，已遵照协议以Git blob原生接口成功读取完整文本；候选及正式内容main的完整tree证明**未修改本文件一字节**。
- 最新INTEGRATION55 NEXT要求离开牧场、矿工、三龙及道场，寻找**别处原场景/NPC/真正原图**。本轮选择旧QUEST09未专项视觉桥接的**梦幻洞窟两层两守卫**，不是重新计算既已验地图或宣称原游戏运行。

## 验收链：每个阶段均是实际远端状态

| 项目 | 经本轮核验 |
| --- | --- |
| 功能分支 | `agent/stoneage-integration56-dream-cave-guards-20261111` |
| 候选HEAD | `f4cb1a26035f38768645e96b2a3cacad2b0818cb` |
| 候选tree | `9e8eb50624e5847387e7c5fadb8a140618381f80` |
| PR | [#324](https://github.com/chinaneedM/stoneage-rebuild/pull/324) 已正式squash合并 |
| 候选push+PR Actions | **46/46 completed/success**，push27，pull_request19，无失败 |
| 内容main HEAD | **`bcc9ef4f3da0e92bb69d98373da670b3fb1b198d`** |
| 内容main tree | **`9e8eb50624e5847387e7c5fadb8a140618381f80`**，与候选tree完全一致 |
| 内容main Actions | **27/27 completed/success**，无排队/失败 |
| main专项运行 | [run 42932236293](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42932236293)，job `130233581956`、`python -m unittest discover -s tests -p 'test_stoneage_integration_module_56.py' -v` 完成且success |
| 主线增量文件 | 公开来源限定JSON、11? 不预先宣称专项数量（逐单元测试以脚本为准）、专项测试、工作流、来源覆层、README追加，共**五个**文件 |
| 原 `CURRENT-STATE` | **原完整blob不变**，Stage A 7 PARTIAL+2 OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING、overall_percent=null |

## 原始实物和版权边界

1. 私人 `StoneAge-QUEST09-dream-cave-original-private.zip` 完整**28,306,717B/SHA256 `ae5e626a7c27922c9fa373be1d25ca6561b4f353cd9529cb66d7e49c827df070`**、25成员CRC通过；原`400/sb_mugen.create`793原字节及4段原块SHA分别核验，同原件两个`arg`文件核读。两份原DAT41/42各29,408B和之前存原地图候选来源图再次逐SHA验真，实际按**三个非交错uint16平面**读出两层(34,41)/(33,41)四个原格。
2. 另一独立的**台湾1.0零售**PET07私人原图HTML**15,123,277B/SHA256 `58e8ee4ff5165ed2f61663d67ae1cd0a8183622fa3375c480232784bfce9dc76`**和先前原RD逐块凭据**1,617,404B/SHA256 `b5ad2e58930afbe90604a1d72e3c17ab0adea446e7c118be775e3973315e6cb4`**完整回读。源SPR候选100343/100346各16组真实已解PNG的原SHA及尺寸逐**32/32**对应；两组共66个原帧位置，32个不同bitmap，本轮新原RD解码0。
3. 私人研究归档 `StoneAge-INTEGRATION56-dream-cave-two-guards-TW1-32-pixels-private.zip` **15,621,429B/SHA256 `aca681e3eee04a67bab488dcbbab00dda3d479274482c87d37a170478541bcce`**、41 ZIP成员CRC全过。上传个人Library `/石器时代/` 后**独立重新下载并重新核对整SHA/CRC**；原始DAT、原始NPC文本和32份原商业PNG、现代候选对照图均**不进入公开Git**。现代研究拼板不冒充原生运行截图。
4. 公开 [数值与来源散列](../../research/recovered/STONEAGE-INTEGRATION56-DREAM-CAVE-GUARDS-41-42-TW1-32-PIXELS-R1.json) 仅有引自旧合格原索引的NPC数值、原地图三平面格、图号及16×2的旧原PNG逐SHA和负证合同。Actions**只读公开派生数据**，不下载个人Library的私人版权资产；其成功不能替代真人实际运行原客户端/服务端。

## 必须维持OPEN

- mixed25社区保存NPC与TW1零售SPR同数字号只是**跨载体来源资格候选**，不是官方同版同部署或NPC实际绘制证据；也非初始日本JSS1999或大陆1.82已经证实同图。
- CREATE位置、原DAT真格与`arg`敌人参数只表明原文本/地图定义；不能推出NPC原生出现、交互触发、真实战斗/传送、颜色、帧率、碰撞、原商业客户端操作。
- 旧保留DAT画布只按来源制作了独立观察，非原生游戏画面；本包原游戏客户端运行0、服务器运行0、同服身份0、官方物种身份0、新原RD解码0。不要把32bitmap称为32种宠物或四CREATE称为4个独立原世界角色。
- 仓库源历史保留旧失败尝试与全CURRENT，没有覆盖或纠正掉旧证据。

## 正式交接

**最高NEXT：** 停止继续扩大已完成的梦幻洞窟双守卫、牧场、矿工、三龙和道场图号。优先找一组**其他不同实际来源的原DAT+原NPC创建/原任务+真实原可见图像**的有证据新增世界内容；如原二进制原件不在私人保管范围，记录具体缺口并转来源充足的模块，不发明原像素、不启动账号服、不重做观察器或体验优化。未来单机开发Stage B仍待正式转阶段。

**本页是在上述内容main的全部27项Actions验收后，作为单独新增收据提交。其自身的HEAD没有在此预先宣称通过相同27项Actions。**
