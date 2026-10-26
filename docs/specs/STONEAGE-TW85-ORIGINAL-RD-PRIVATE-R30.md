# 保存台版8.5样本 R30：真实 RD 原像素八帧私人观察

日期：2026-10-26。任务 `TW85-FRAME-ORIGINAL-RD-PIXEL-PREVIEW-30`。取证目的是让 R29 原动画→原位图完整数值绑定实际前进一步，得到可以由研究者观看的**同保存包真实位图像素**，不是继续增加元数据 helper 或假设具名物种。

## 本轮远端新会话启动

新远端 `main` HEAD `67818af4d80ea22d9d353b97892e882fb214689c` / tree `11823eb2ec367fb35be1fbd9fa326a69c5397b07`，最新提交为 R29 主线后验收据。依协议顺序重新读取 README、协议、完整原生 `docs/CURRENT-STATE.md` blob `031c76a5a8e431f646853909bb2f2e11e6328cd2`（2,680,510B）、设计/历史/来源/路线及最新 Actions。旧 CURRENT 及四个巨型主簿保持原 blob，不以旧聊替代。0开放 PR；当时 R29 主线 6 项实际 success，原件源工作流在 main 被按设计 skipped。

## 游戏可见实物、选择条件和发生的事实

1. R28 原台版8.5*声称*保存包的 `SPR-GROUP/ANIMATION/FRAME` 所有1,739组、113,737动画、735,666帧先由永久源 SHA 及 R29 全表校验；R06 在相同 **557文件 MSI 保存载体**取得的 `ADRN/REAL` 416,220条实际结构与每个原 RD 块 SHA、R29 全量730,907非哨兵帧唯一对应。不是临时选择别的游戏包凑图。
2. 选择规则（在下载原件**之前**执行且实际通过）：在554个 R28 与固定CN5原SPR段未形成同数值同完整段 SHA 匹配的组中，按原顺序选首个有6–12帧、至少3不同位图、8帧以内且原图≤256×256、原RD原片段≤300,000B、实际原物理位图唯一匹配、flag0/1可解的动画。该条件在保存包派生材料中确定选到原 `group_index=1185`、`spr_no=101501`、`anim_index=1`、方向原数值0、动作原数值2、duration原word1000，**8帧位图号303039–303046**。
3. 这些实际原 RD 帧尺寸分别为100×126、100×125、92×123、88×134、84×123、108×133、112×120、124×121，原RD压缩flag全为1。选前先完整检R28全源/同安装包资格，未因为页面宠物名或游戏人物联想改选。
4. 源实物 Action **40329157425**（preflight job **121593631715**、actual source job **121594000184**）均completed/success。六份已经登记的分卷（前五份各209,715,200B；第六份96,889,184B）实际重新下载，合共**1,145,465,184B**、每份服务尺寸/全SHA完整通过；原 MSI InstallShield **静态拆包，不执行商业程序**。这次下载是实际首次获得这八幅图像源像素，不是为原SHA重复拉包。
5. 真正原件 `adrn_158.bin` 33,297,600B/SHA `16ba4fa3825b2c4b6645bab8b4fe3152a262a4789c8bb89e3043a7d3f0d53681`、`real_158.bin` 1,607,321,502B/SHA `e0f9c0d20fd3d9daae0701d8a872c9842e27d3da1be4d449d558c9c76d1c5f5b` 于 runner 实际验证。每幅原ADRN **80B整记录**SHA 与R06原索引报告逐行一致，真实 REAL 读区间、**完整RD块SHA**与以前source报告逐块一致，然后调用既有只读 `stoneage_rd_codec.decode_rd_block`，得到8幅实际调色板索引像素、原索引像素SHA以及私人灰度PNG SHA。
6. 完整源图/PNG仅保留 runner 临时目录及**会话RSA3072公钥包裹AES256-GCM随机对称密钥**加密后的短期 Actions 工件；私钥只有当轮私人环境拥有，不在GitHub原仓库、不在CI日志。源临时目录经清理。短期artifact ZIP 34,235B/SHA `265dffe92a7ed89370f9d45ecb3f97ab0241652c9168e175e5852c8fd19bb554` / ID **12654905609**；密文30415B/SHA `c689e21a7b1e699951ec6b3014fcb5934670254dcff739a66e0d5bbd652bb02f`。计划artifact ID **12653666487** ZIP SHA `81b2ac85c8069d76a6f2048d7bd4df38e0ffeb7032fbcd4115baa12185f9bfe8`。
7. 会话本地实际再次下载工件ZIP、独立整ZIP重SHA、限制工件只有密文/加密envelope/不含像素的SOURCE JSON三件；用CI未知的研究者本地私钥 RSA-OAEP SHA256 解密随机 AES 密钥，AES-GCM鉴真解出私人30,399B ZIP，含8 PNG及 `PRIVATE-R30.json`；全部8帧私人PNG哈希、尺寸和 RD哈希同源报告一致，用户可私人下载两行×四列灰度接触图及人为节拍GIF。**助手在当轮已目视该私人灰度接触图**：可辨该组连续变化的复杂生物/人物型轮廓，但没有来源证明物种、动作含义或原色。
8. 原像素索引直接映射 0–255 灰度用于研究者观察；没有认证 TW8.5 同版初始化SAP/游戏实际使用调色板、alpha/索引0透明语义、叠图遮挡、方向或真FPS；当轮GIF为研究演示随意定时175ms/帧，不可称游戏播放。原原始PIXEL索引只存在私人PNG/会话临时载体；公开Git没有图像或游戏程序。

## 完整证据与独立接受

永久派生、不含原图，目录 `research/recovered/tw85-rd-private-r30/`：

- `PLAN-R30.json` 5,744B/SHA256 `805e6f1ef0039f48f40c7c6cc46296d1297b8e629617e3ddfdf629e8e1204a09` / Git blob `59bbb09d55c33076e1616499a2710c8de588dcee`，原全表选择规则、8帧每原offset/真实ADRN物理行号、块SHA、压缩flag、尺寸。
- `SOURCE-R30.json` 10,602B/SHA256 `f70b5ce996e2fbf4acb8dfa5103d8729bdbf6d2779df86c2a35bc71768f253e6` / Git blob `9fb54267a59561ce8b1dfaa387b857f17a94a896`，真实源作业的8块原SHA、原像素SHA、私人PNG SHA和八帧来源。
- `R30-PUBLIC-CUSTODY.json` 3,773B / Git blob `58f2c64cb795a7ef7c418f8b7733585bc0217dc0`，源执行run/job、artifact哈希与界限。
- 限定工具 `tools/stoneage_tw85_r30_preview.py`、否证测试 `tests/test_stoneage_tw85_r30_preview.py`、独立归档工具 `tools/stoneage_tw85_r30_archive.py` 与离线验收 `tools/stoneage_tw85_r30_verify.py`。归档run **40330184123**/job **121597232482**实际 completed/success：独立从 R28/R06/R29 全表重新选同组并对齐8原RD SHA及公钥密文指纹，**只提交派生 JSON**到研究分支 commit `1aa739bf7b1edaf80ee90507a88e4569cb133961`。

审计失败：最初 `40329053102`、`40329130269` 因公共RSA公钥 heredoc 未缩进进入无jobs YAML解析失败；随后修正，新真正源run `40329157425` 成功。旧失败不删除不伪称实际取源。用有限一次下载取得私人可观测实物后，该资源族阶段即止，不再无限重复载体、扩调色板/渲染helper。

## 仍为 OPEN 与下一优先次序

“原始图像实际像素被读入和私人可视化”已获本保存包单组选样证明；不等于全 554组都已渲染、不等于所有官方版本下载完、不等于完整私人客户端长存、更不等于**JSS1999/TW1.0官方原物种身份**，旧R20具名名字→实体ID→SPR仍未关闭。照片的灰阶外观不是原色场景，原Wine/Windows P3E缺ACP950隔离环境，原客户端未进入世界，声音未真实听到。R30 stop condition达成后，按协议§13返回实质玩家可见内容：

**NEXT `ORIGINAL_SAME_BUILD_NAMED_WORLD_ENTITY_MASTER_31`**：先按22域索引筛现存**实际官方早期客户端或合法服务器主表**是否有可认证的同构建宠物/NPC/地图/本体任务名字、实体ID与动画SPR/原RD关联；仅限一个具名、可精确证物的目标或写清缺源并转其他内容域。不得猜101501是哪种宠物、不得把活动任务混入原生任务，不继续一味做动画/图像helper，不为了纯metadata重新下1.145GB大包。

Stage A保留7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING、overall_progress_percent=null，原历史CURRENT全文不覆写。
