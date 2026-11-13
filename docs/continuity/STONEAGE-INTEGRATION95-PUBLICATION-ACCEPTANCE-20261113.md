# INTEGRATION95｜原 dungeon00 147条配置和64楼层静态图｜永久主线验收（2026-11-13）

## 真正的候选、合并和主线 CI

本轮新增 **[PR #373](https://github.com/chinaneedM/stoneage-rebuild/pull/373)**。内容候选 `8259498ba826aada5c14474a2ac7294945e4a81d` / tree `8cab7a85ba0de56c37e944ec2950cee89c3e4020` 全部 **46/46 GitHub Actions completed/success**（27 push、19 pull_request）；专用 push run [43433198749](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43433198749) job `131911592231` 和 PR run [43433206510](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43433206510) job `131911618883` 已独立读出**真实日志`Ran 9 tests / OK`**。通过合并前严格HEAD、base、无冲突及全部Actions核验后 squash merge，内容正式 main `897bdadfeb179d6250d22b90aedf3c3e600459e0` / **同tree** `8cab7a85ba0de56c37e944ec2950cee89c3e4020`，然后独立实核该精确内容主线 **27/27 GitHub Actions completed/success**。主线专用 run [43434159465](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43434159465) job `131914882040` 真日志同为 `Ran 9 tests / OK`。

[永久机器验收收据](../../research/recovered/STONEAGE-INTEGRATION95-PUBLICATION-ACCEPTANCE-R1.json)收录候选46与主线27共**73条真实run ID、原head、event、name、status、conclusion**，并固定公开原资料报告 Git blob `285857ec36ffe7cdadec5f6093a861ed0e5be05a` 和专用测试 blob `ab544c5a20cfadb5f8c40685ebd05722b757bb6e`，不是拿PR候选通过冒充主线正式通过。**本验收报告提交自身的CI须按其新SHA后验，不在这条记录预支。**

## 实际私人原件、独立保管与原研究范围

本轮源是先前保存于个人Library的 CHAR01 原私人ZIP **995,176B／SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`，2205成员CRC验证**。真正重新逐原字节读取其中 mixed25 `npc/genout/dungeon00.create` **17,289B／SHA256 `1b3d189ea8ae5e42de4321efce19d3fb9517f0b25b6130ff0cb73761cd62514b`**；147原 NPCCREATE 的具体 byte span SHA 与旧 Git CHAR01 指纹 **147/147相同**。整361MB父RAR并未本轮重新取字节；不会说已重读父RAR。源里注释提到的 `data/npc/sainasu/dungeon/dungeon00.gen` 上游生成输入没有取到。

**纯静态来源图**：147原创建配置，140条文字数据有70对严格反向源配置、7条在此CREATE里无严格反向；64不同源floor，117不同楼层方向，5弱/7强图分量。它不证明70对传送真的双向可通行，更不能将7条推成单向原玩法。旧MAP04同mixed25保存源**955份原DAT索引**仅按旧SHA和地图尺寸复合本批53/64 floor，有11未命中；有原DAT尺寸的205个原端点在范围内，本轮原DAT字节重读 **0**。混合后期社区保存数据不等于原台湾1.0、早期大陆1.82商业服同部署；原native角色实际踩点、地图绘制/碰撞/传送脚本和历史场景OPEN。

私人源图包 `StoneAge-INTEGRATION95-dungeon00-147-original-warp-source-private.zip` **10,610B/SHA256 `0e13f780dbd4263e74284329072c0bbb5c8f845647da2bf7916962b9de1a07d5`，3/3 CRC**，含原CREATE和现代SVG关系观察HTML；已保存个人Library `/石器时代/`，并另一次真实从Library独立回取，两份ZIP全字节与SHA一致、3CRC合格、原CREATE成员又复核全SHA。Chromium使用 `page.set_content` 实测64原floor数字节点、147创建候选、5分组实际筛选、搜索与真实点击/重置，0 JS/console错误和0外网；不是原商业游戏画面或file://导航成功声明。原游戏商业原件不上传公有Git，仅发布 SHA、数字和不确定性。

现主线保留完整原 `docs/CURRENT-STATE.md` blob `c89e0e33537990aa2132b47c40fef49a985a935c`、**2,709,173B**不变；Stage A仍**7 PARTIAL+2 OPEN**，B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，overall_percent=null。

**INTEGRATION95为SOURCE_BOUNDED_ACCEPTED，不是GAMEPLAY_VERIFIED**。NEXT：选另一组可验证真实来源且不重复的地下城、任务或同版本行为证据；不要重复静态数字图、扩无证原生MMO或提前开发新单机引擎。
