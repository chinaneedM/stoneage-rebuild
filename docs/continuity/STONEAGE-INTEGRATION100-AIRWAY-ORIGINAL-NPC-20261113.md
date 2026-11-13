# INTEGRATION100｜加美航空五原向导、十原看板和六个地图来源关系（2026-11-13）

## 本轮实际从原件恢复了什么

本包承接已完成验收的 INTEGRATION99（原地下城配置数字交集），按最新主线 `68b35428e842048673b894f333d092efef83a7a4` / tree `bd7645ec1acc20d3cbddee1c4c1729987fd90c1a` 重新启动。已读取连续性协议、最新来源优先级及整个原 Git blob 的 `docs/CURRENT-STATE.md`（2,709,173B）；保留其 `c89e0e33537990aa2132b47c40fef49a985a935c` 原样，不重写。

这次选择了既有原始 NPC 资料包内**未见单独整合的另一个内容家族**：`npc/genout/airway.create`，而不是已整理的长毛象客运／家族商店／地下城静态图。实际从私人 Library 取回 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip`，ZIP **995,176B**／SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`，**2,205/2,205 CRC** 成功。实取源 `airway.create` **2,747B**、完整SHA `faaf7850d8cc400764b6f4b700dafced16664a988069e15b3ba18315d52ded9e`，CP950字节往返一致。原15个 CREATE byte spans逐SHA与以前的源索引完全吻合，**15/15实际处理文件**独立完整SHA与CP950往返全同，12个不同原文件正文SHA（其中一类看板文本复用4次）；没有重拉361MB父RAR，也没有原生游戏运行。

### 有界游戏内容关系

| 原资料类别 | 实际原配置数量 | 来源限定结果 |
|---|---:|---|
| `npcgen_man` 航空向导 | **5** | 五份不同原处理文本；仅源文描述航点 |
| `npcgen_signboard` 普通去向牌 | **8** | 四处看板指向奇努伊，奇努伊四牌分别指向四处机场；各牌源原文字面`1000s` |
| `npcgen_signboard` 空投区牌 | **2** | 北吉鲁／西吉鲁空投区域看板；**未见`1000s`原文** |
| 全部 CREATE→handler | **15** | 15个源位置、源图形编号、源类型、原字节窗口SHA与15个原处理文件全SHA均已绑定 |

由后期保存包**原向导文字和原看板**只能确认对「瑪麗娜絲」「卡魯它那」「達那」「米蘭達」「奇努伊」等地点的方向说明，不能把此表当成可起飞的玩家路网、实际飞行脚本、运行扣费或两个运营版本的共同NPC模型。`1000s`是看板中的历史**文本**，不是已认证实际扣款金额。

再对照原[MAP04 955份 DAT 目录](../../research/recovered/STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json)，15条配置只分布于原图号 **2000、4000、5000、5100、5543、6000** 六楼层；其中 **2000、4000、5100、5543** 四楼层已记录原DAT完整SHA与真实头部尺寸，涉及**8处源NPC创建坐标**都在旧DAT头尺寸范围内；目录中**5000、6000缺原DAT资格**，另7处只有源CREATE数字，不可借别的地图证明完整场景、碰撞、可行走或真实机场存在。

## 证据与公开边界

同载体原档属于**后期社区保留 mixed2.5**，未经证实为TW1.0/JSS1999/初代大陆1.82官方同运营部署。新的[机读原子来源索引](../../research/recovered/STONEAGE-INTEGRATION100-AIRWAY-15-ORIGINAL-NPC-SOURCE-R1.json)仅保留15条原创建段位置、原NPC数字/类别、12种处理正文SHA、文字去向的短标签、此前原DAT的来源SHA和证据边界；**原航空人员对白、完整文本、原商业SPR/PNG及原DAT均不上传公有Git**。旧的[CHAR01完整来源索引](../../research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json)与MAP04 Git原blob保持不动。

验证包括真实私人ZIP SHA/CRC、15原CREATE窗口SHA、15原处理字节与CP950，以及新公开metadata在GitHub Actions checkout对两份旧来源索引的完整SHA、逐15创建/handler引用、楼层DAT几何和反例检查；**只有真正 Actions 结果才能作为远端验收**。本轮没有新原像素 RD 解码、没有运行真实飞机NPC/航线、没有到原服务器注册登录，更没有设计现代单机飞机功能。

## 本阶段止点

判定 **SOURCE_BOUNDED_PARTIAL**。缺原程序的实际航空/扣费逻辑与对应版本的可观察运行时，不再无限扩大纯静态出行路网。Stage A **7 PARTIAL + 2 OPEN**，Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，整体百分比未知。NEXT转新的原实物内容家族；若未来获得同源航空 handler/原生航程与原DAT，则增量重开。
