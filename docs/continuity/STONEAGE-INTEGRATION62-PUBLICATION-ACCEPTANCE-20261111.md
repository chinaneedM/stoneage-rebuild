# INTEGRATION62｜恐龙收集双GetPet→两原宠物模板→29张台湾1.0原图：正式出版与来源保管验收（2026-11-11）

## 前置主线与真实游戏内容增量

按远端事实源开工：`main=1e647c8628be5f15a1888fc32b86ff2f4542c986` / tree `85e84361ff68c501ea655f50b52c9e917032c279`，核分支、最近提交、Actions、协议、README、历史`CURRENT-STATE.md`完整Git blob、路线与各个最新模块覆层。承接INTEGRATION61的NEXT；查重已经完整处理的GAMEPLAY03 21宠物技能店目录及QUEST31 6原任务物品图像后，选择QUEST30已有原脚本、但尚缺真实早期二维像素实物连接的两条宠物奖励。

[INTEGRATION62有界来源详情](STONEAGE-INTEGRATION62-QUEST30-TWO-PET-REWARD-ORIGINAL-PIXELS-20261111.md)／[可永久Git重放数字、原SPR段/原RD像素散列、6动画源序列](../../research/recovered/STONEAGE-INTEGRATION62-QUEST30-TWO-GETPET-TW1-29-RD-PIXELS-R1.json)，固定：
- 已有原`GetPet:93/341` 的脚本TYPE段#0/#4，数字来源不是本次新发现或已执行奖励；
- 后期社区mixed25原双`enemy`实例表93/341→两`enemybase`模板171/274→图号100319/100362；两份变体的原整行SHA分别保留，原字段数值一致但运行选择未知；
- 早期台湾1.0零售原SPR图组索引293/332的动作0/2/1方向0，**21+25源帧位置、13+16真正不同的原RD PNG，共29幅**。29张已保存原图PNG逐文件SHA与尺寸真实重读一致；6段原帧位置按小端32位字节编码逐整SHA与旧原SPR记录相同。不同source、不同版本的候选关联不升级为同服历史真相。本轮新原RD二进制解码0，原原生客户端/服务端执行0。

## 私人真实原始字节、保管与严格复读

从用户私人Library取得并核：
- `StoneAge-QUEST30-dinosaur-collector-event35-private.zip` **10,479B / SHA256 `cb6f27c43559049bd05976293c3fd260c9d0ba87cc50b5a93f7ea884b7f4225a` /8成员CRC通过**；前人任务源内容不是本轮发现。
- `StoneAge-CHAR01-mixed25-all-npc-original-private.zip` **995,176B / SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f` /2205成员CRC通过**；属于原后期混合存档保存派生子包。
- 既存台湾1.0 PET07已真实解原图的私人HTML **15,123,277B/SHA256 `58e8ee4ff5165ed2f61663d67ae1cd0a8183622fa3375c480232784bfce9dc76`** 与私人真实原RD收据JSON **1,617,404B/SHA256 `b5ad2e58930afbe90604a1d72e3c17ab0adea446e7c118be775e3973315e6cb4`**；全部文件整SHA实际验证，29/29 PNG文件哈希/尺寸及6原动作序列SHA严格同先前收据与公开原图源索引。
- 私有研究输出`StoneAge-INTEGRATION62-QUEST30-two-original-pet-reward-pixels-private.zip` **271,047B/SHA256 `e075d132aa5ad0a4da25ecb8aaf325785f676291c588b0702173b7216db61cc1`**，包括29幅旧已真实解出的原PNG、来源收据、一份现代离线观察页，共**31成员**。已存私人Library`/石器时代/`，独立用新库文件ID回取不同目录，**整包SHA一致、全部原字节逐字节一致、31成员CRC全部通过**。版权原NPC文本和商业原美术一律未入公开Git，公开只有派生数字/散列索引。
- 新派生报告正式Git blob `1e439f0b01902d8a6b2c8dd2fe851e17de08f321`；旧源QUEST30/PET10/PET07 Git blobs分别为 `22315fb6b4363aaafc98375a4fcda9498b608246` / `25a37aeb134fb180e322e7dc335029b7374452d8` / `0b5f81b41a642025ab53a12884638fdee887470e`，前缀未重写。本轮未重开原361MB社区RAR、新解原REAL RD0、原程序原生操作0。

## 候选PR、回归测试与正式主线Actions

| 来源阶段 | GitHub真实后验结果 |
|---|---|
| 候选分支 | `agent/stoneage-integration62-quest30-pet-reward-20261111` |
| 候选最终HEAD | `4270dcbcad5a2d52adfed024dacb8ad95fa39233`，全树 `a49d3ca0734303858701b61bdaa0e191a0f8834b` |
| 正式PR | [#330](https://github.com/chinaneedM/stoneage-rebuild/pull/330)，固定候选HEAD、无并发main变更、PR mergeable=true、来源范围仅5文件、全部真实Actions成功后squash merge |
| 候选完成运行 | **45/45 completed/success**（最终候选HEAD匹配push26 + pull_request19） |
| 专项候选PR | [run42979519120](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42979519120) / job **130386370286** 实际success，**6项**专项单测通过 |
| 早先候选专项push | [run42979186854](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42979186854) 属早期HEAD `8bd96e490d154072d6d359a15c6ff1c01448e457`，也实际success；**不是**最终候选HEAD的专项push，不混写 |
| 内容main HEAD | **`cfce61f71189897e663547cf3da6fe40a554969b`** |
| 内容main tree | **`a49d3ca0734303858701b61bdaa0e191a0f8834b`**，与候选最终tree一致 |
| 正式主线Actions | **27/27 completed/success**；专项 [run42979673726](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42979673726) / job **130386880861** 真实success，6项检查均通过 |
| 旧历史CURRENT | `docs/CURRENT-STATE.md` Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`，2,709,173B，完整原样保持 |

本回执只在内容main的27项真实验收成功后创建；**收据自身新提交HEAD可能没有触发新Actions，不能提前宣称已重新成功**。公开CI依赖之前既有Git派生数值，不能自行从私人Library重取版权图像；private原图SHA重读与公开派生CI各司其证据边界。

## OPEN与下一个最高优先级

Quest30原2607道具“任务文字／同包原itemset物品名称”冲突仍未消除；floor100旧955原DAT目录无匹配不等于原运营无图。原GetPet真实交付、宠物实例与模板在原执行中是否被选中、两原变体表生效选择、早期官方实际同部署/原物种名、动画帧率和配色、原客户端可操作世界，全都OPEN。Stage A **7 PARTIAL + 2 OPEN**；Stage B/wiki **GATED**；R79 **PAUSED_NON_BLOCKING**；overall_percent=null。版权原文、原美术不发布，不接网络注册/服务器，也不提前进行现代单机游戏制作。

**最高NEXT：** 本次两奖励源像素桥已有限闭合。按22域查重，优先选择**不同的**真实原件与原图、NPC/地图服务、原物品或宠物技能之间尚未专项接合的一条可见关系；只有实际原字节或新的材料内容关系才继续，缺源明确止点并轮换。不重复本次两源SPR，也不模拟原宠物交付/任务系统。
