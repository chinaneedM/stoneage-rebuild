# INTEGRATION111｜两族矿山任务：24原NPC配置 × 22张真正台湾1.0原RD像素候选（2026-11-14）

## 远端基线及来源资格

按 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` 新验 GitHub `main=a64e9f5c4079fe891b34e4c79c43d7b44a081d43`、tree `412781cab452df38539176c45059369211bd0b4c`、26/26 本HEAD Actions 成功、0开放PR，已读取原生 `docs/CURRENT-STATE.md` **2,709,173字节／Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`**及启动协议等。此历史原文件完整保留，不用截断写入替代。

**源A：后期社区保存 mixed25 NPC**。重新从个人 Library 取回 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip`（995,176B／SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`），2205/2205 ZIP CRC 通过。实读 `genout/giruev2.create` 3,800B 的21个 CREATE、`giiru/event/giruev2.create` 593B 的2个 CREATE，以及 `300/sb_bac.create` 190B 的矿工 CREATE：共24源原块。**原文件先前已由QUEST12编目，本轮不把它们当新发现。** 又真实读取24份不同被引用的原参数/对白文件，各CP950往返，合共27原文件的全SHA/尺寸/CRC，以及24原块的原窗口 SHA 与先前 `CHAR01` 全源公开索引逐条核同。

**源B：真实台湾 Waei/JSS 1.0 零售 P3H**。私人原客户端包372,626,292B／整SHA `3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24` 和379/379 ZIP CRC 重新实际验真。原 `adrn_1.bin` 10,079,680B、`real_1.bin` 315,842,228B、`spr_1.bin`／`spradrn_1.bin`、原候选 `Palet_1.sap` 全源 SHA 都与旧公开源登记一致。提取完整 REAL 后实读 **22个不同 RD 原块，合计39,941B**，22个各自独一无歧义的 ADRN 原记录；22个原索引图均由两套独立解码实现核对到逐像素相同，源画布有真图，按候选调色和倒行解释生成22张私人PNG并目视接触表。

## 实际新增可见内容（来源限定）

- `31805` 地图保存的两族竞争配置：**帖尼姆團**10位、**巴巴洛組**10位、1位入场管理人；已有 QUEST12 的**两位主要负责人**与**矿工**分别为2、1个原 CREATE，合计 **24个原创建配置**。同图号 `16202` 在两条 NPC 创建记录中出现，因此这23个人物／入口配置只涉及**22个不同静态RD数值**；第24个矿工图号 `100401` 是原 **SPR动画**，已有 `PET15` 真原像素先例，**本轮不重复解码为新图**。也**不能说22张RD就是22种不同人物/造型**，其中存在同一人物的不同方向或姿态。
- 22原RD数值：`13052`、`16016`、`16017`、`16018`、`16019`、`16039`、`16041`、`16042`、`16043`、`16044`、`16045`、`16046`、`16047`、`16048`、`16049`、`16055`、`16056`、`16062`、`16202`、`16203`、`16207`、`16208`。每个记录独立保存原ADRN索引、完整RD块 SHA、索引像素SHA、尺寸、位移及私人候选PNG SHA；公开无商业图像。
- 24个源点均为 floor `31805`，`x/y`位于已有 QUEST12 验证的 **50×50** 原 DAT 范围内。此次重用旧地图整SHA和三平面结论，**没有重新读取原DAT**、没有重新生成地图画面，不把数字位置解释为实际 NPC 上线位置或通行规则。
- 私人只读HTML含23组源数字关联的真实TW1 PNG预览及矿工 `100401` 的既有PET15引用说明。现代 `Palet_1` 初始化色、纵向翻转与原像素索引0透明均为**预览选择**，并非原商业客户端实际配色的认证。私人拼图/HTML虽经本地PNG逐图重放与目视，但没有原游戏客户端、商业服务器、原任务/入场条件的实际执行，也不等于实际历史同服画面。

私人交付 `StoneAge-INTEGRATION111-mining-two-teams-original-2D-private.zip` **212,169B／25成员／SHA256 `efda438c7a57c83bbcc800d0ea0b1ca145d64ea6e7c87d5e0f697aebc330804a`** 已存个人 Library，并**另行下载完整包回读SHA与25/25CRC，均与本地同一**；含22商业PNG、只读HTML、现代私有拼图与来源收据。原NPC参数、原RD、PNG和HTML不放公开Git；保留 [来源衍生JSON](../../research/recovered/STONEAGE-INTEGRATION111-MINING-TWO-TEAMS-TW10-22-ORIGINAL-BITMAP-CANDIDATES-R1.json)与 [8项公开跨源/负例测试](../../tests/test_stoneage_integration111_mining_tw10_2d.py)。CI仅检验公开数值/哈希与原先可复核索引，**不能声称CI重新下载原像素**。

## 已知边界与后续

这是**不同历史载体的数值索引对照**：后期社区NPC源 `graphicname` 与台湾1.0原ADRN里相同整数，只给出一种真实二维**候选**，不证明这批后期资料在早期台湾服上线，不把同号当同一角色、同一皮肤或同一物种。QUEST12 早期静态任务研究已独立完成，此轮没有新增任务分支、许可证执行或矿工胜利掉落；也没有独立历史新美术设计。

Stage A 保持 **7 PARTIAL + 2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、overall_percent=null，原可操作世界未进入。候选/PR/主线Actions和合并必须按精确HEAD真实核验，不预支。**NEXT** 选择另一组尚缺真实可见二维或独立原件的宠物／场景／任务族，持续用同源素材/同部署资格区分事实和候选；不要为了数量重复已经完整观察的PET15或扩无关helper。
