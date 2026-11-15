# PET32｜JSS 1999-11-22 / 11-26 战斗邮件与宠物邮件原始语义核读

**2026-11-15，PET-only / 1999 chronology active。** 源于已收存的日本 JSS 第一方 `verup.html`，原网页当年运营商自记日期，实际互联网档案捕获日为 **2001-04-17**。源 URL `https://web.archive.org/web/20010417162544id_/http://www.titan.co.jp/stoneage/verup.html`；原件 **11,239 bytes** / SHA256 `ba71d859f34f31261f4293dc61583c53a8e77133898c4a8148c544a452abc3cb`，严格 Shift-JIS 解码。原全页未入公开 Git。

## 本轮新核实的准确范围

- **1999-11-22 / 原页 source_order=31，分句3**：JSS 当年记录：战斗中允许普通邮件操作，可以从快捷方式或窗口栏打开邮件窗口；**明确排除宠物邮件**。该分句原规范化 90 字、SHA256 `4e1b95514e7a7154bb2d01e4530738b3cbec7fdbaec14b723481a25be7353851`，与 PET31 所存子句指纹精确吻合。
- **1999-11-26 / 原页 source_order=30，分句0**：JSS 记录修复了「战斗中的宠物邮件相关故障」，**没有描述准确故障症状、成功后的功能开关、宠物邮件是否能够在战斗中发送**。规范化 25 字、SHA256 `d4bc63f3f1ba485d41bbac66c1a39ddacbb6ae60e121506d5d4f8fb5219b1c56`；精确比对 PET31 来源登记。

2026-11-15 **探针实际运行**：分支候选 `30cbb82310e38132610599bcf4d853774f99f20a`，GitHub Actions run **43710057574** / job **132799455619** completed/success；原 11,239B / SHA 与 40 个运营商自记日期全页核验通过，两条子句实际原文小范围读取并证实。此探针只用于研究语义，不是最终 PET32 新版本的 Actions 验收；内容发布和后续 CI 仍需精确新 SHA 后验。

**避免 PET31 词面误判：** 11月22日的「ペットメール」命中来自明确的**不能使用**，不能把出现关键词反向解释为新开放宠物邮件。11月26日的「修正」只证明官方报告某问题已修，不能推导当日解锁战斗宠邮、取消11月22日禁令或实际服务端运行结果。单句日期不提供客户端/服务器版本号、技能/宠物主表、宠物名单和可获得方式；两条都不是宠物新增或官方具名物种发行证据。

[机器来源边界](../../research/recovered/STONEAGE-PET32-JSS1999-BATTLE-MAIL-SEMANTIC-R1.json) / [可重放代码](../../tools/stoneage_pet32_jss_mail_semantic.py) / [逐源官方历史先行索引](../../research/recovered/STONEAGE-PET31-JSS1999-ALL-CLAUSE-CENSUS-R1.json)。公开只保留来源位置、原文指纹、明确正反功能范围及缺失项；CI 再从精确原件独立生成衍生 JSON 验收，不发布原始整页。

**年度状态不变：** 日本 JSS 1999 `NOT_YEAR_AUDITED`；1999 与 2000 无资格称源尽或历史完整；本批新增实际官服**具名宠物实装证明0**（不等于当时零宠）。最高后续 PET-only NEXT 是继续找 1999 JSS 同年代官方原包装、手册、可恢复客户端/宠物主表和原任务/奖励正式获得证明，并将任何新增早年记录放回原年份。原 `docs/CURRENT-STATE.md` blob `c89e0e33537990aa2132b47c40fef49a985a935c` 保持不变；Stage A 7 PARTIAL+2 OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING、总体 percent UNKNOWN。
