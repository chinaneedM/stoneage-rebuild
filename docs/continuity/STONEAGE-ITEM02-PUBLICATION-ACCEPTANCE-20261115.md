# ITEM02 — 四份有界原RD与93条真实Actions（包含2条初始失败）的永久验收（2026-11-15）

本收据仅归档[内容PR #416](https://github.com/chinaneedM/stoneage-rebuild/pull/416)已经真正发生的候选／内容主线 Actions，**绝不预支本归档PR及其未来主线Actions的成功**。历史 `docs/CURRENT-STATE.md` 2,709,173字节/blob `c89e0e33537990aa2132b47c40fef49a985a935c` 未修改。

[真实原RD与保留的负证](STONEAGE-ITEM02-FOUR-TW10-ORIGINAL-RD-BOUNDED-PREFIX-20261115.md)／[四个原ADRN/RD来源摘要](../../research/recovered/STONEAGE-ITEM02-FOUR-TW10-RD-BOUNDED-PREFIX-R1.json)／[93个真Actions逐ID及精确SHA收据](../../research/recovered/STONEAGE-ITEM02-PUBLICATION-ACCEPTANCE-R1.json)。

- **初始候选** `20505e2c36cb50cdb145daafdcf47b77dc13e9ad`：GitHub真正触发 **46条**（27 push +19 pull_request）；其中**44 success、2 failure**。真实失败 [43678096678](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43678096678) 与 [43678099237](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43678099237) 均在10项测试中9项通过，1项是测试把 `original_RD_SHA256` 错拼成 `original_RD_sha256` 引起 `KeyError`。**不是商业原源字节出错，也不能追认原失败成功**。
- **修正候选** `f42db686057e7cf30e5139c3f7a93f3432ce5148`：仅前向修正测试中一处字段大小写，不修改来源派生、四原RD内容或历史失败。新提交精确HEAD实际 **20/20 completed/success**（1 push + 19 pull_request），专用 GitHub 真日志 `Ran 10 tests / OK`。前后候选由于所改文件不同，工作流触发集合不同；不应虚称本修正HEAD 46条成功。
- **内容正式主线** `6354b4065b2ebc41176c7bd47524bac49366aa2b`：合并后按精确HEAD **27/27 push Actions completed/success**，tree `66cbd27623b89b78577d8cbb0687a52ce8af1d97` 与修正候选完全同一。上述三套互不重复的运行ID **共93条，其中91成功、2失败**，具体workflow、event、HEAD、状态、时间和URL全部写机器收据。93只是运行记录，不是原游戏图、物品、物种或功能的数量。
- 从认证台湾1.0零售P3H原ZIP372,626,292字节/379CRC实读四原ADRN及REAL RD，四者都以尾字节 `C2` 多生成一位透明零；两独立完整RLE实现全索引流逐字节同一，四张画布前缀共3,552索引位置确实有据。**旧ITEM01的832严格成功＋4严格失败＋831缺原索引并未改写**；本研究提供4个 `SOURCE_PREFIX_BOUNDED` 二维观察候选，但不证明原客户端是否接受末尾零、不证明后期mixed25物品主表与TW1.0同服，不更改商业原文件。
- 私人候选联图ZIP **15,424字节/SHA256 `fa4cfcd974b5c5f4e4971f8c87c042abd47191bcbaddc0c775841977a3d6319d`** 已在Library保存并独立再次下载核整SHA、4个ZIP成员CRC；原图片、原RD或原物品完整正文不入公开Git。

Stage A **7 PARTIAL + 2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、`overall_percent=null`。**下一项**：另一份真正未重复的宠物、任务或场景原材料；不扩大任意RD越界截断，不开始新石器玩法优化或原网服复建。