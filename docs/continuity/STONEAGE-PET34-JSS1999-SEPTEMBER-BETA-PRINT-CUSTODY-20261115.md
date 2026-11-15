# PET34｜1999年9月 JSS 初代测试期《Play Online》纸本扫描件：原文件保管与不能核读的边界

**2026-11-15；PET-only；当前年份仍为1999。**

## 本轮源层新增（不重复记入现有测试日期成果）

这份1999年9月《Play Online》**No.015**原期扫描件，已在既有 [JSS1999起源考据](../../research/origin/JSS-1999-ORIGIN-EVIDENCE-R1.md)引用，那里已有「1999-09-01—09-30」测试期及分给杂志读者200个候选账户的同期杂志报道。**本轮没有再把这两个数字冒充新发现**。新增的是对当下可访问原扫描PDF进行独立、精确的**文件身份复核**：

- 独立保存站原址：https://www.kingpin.info/download/kingpin/media/magazine/Play_Online_Issue_015_%28Japanese%29_1999-09.pdf
- 正确复取的PDF：**31,915,180 bytes；167页**；完整SHA256 `fd6cb9e4a3f7023115ebff91042d7c9b4a8c956b822c5ffd6379230ec5ee328c`。
- GitHub Actions run `43712624585`（job `132807293725`）从真实URL下载、解析本机PDF页数与原始哈希全通过；run `43713031321` 复取同件、同页数、同SHA成功。中间 run `43712764344` 的缩略图代码因环境缺少Pillow失败，不提供新内容资格；原扫描**并未**写入Git或CI artifact。
- 原扫描含可抽取但**严重乱码的日本语文本层**：针对全167页扫描文本按精确 `STONEAGE/ストーンエイジ/ゲーマーズドリーム` 等词匹配，得**0个可靠匹配页**；部分页的字母组合明显变形，不能把匹配0误读成「印刷文不存在」。
- 外部全文索引声称测试参加者有「特典アイテム」等字句，但当前**未完成原页可读图像与纸本的独立校勘**。该句只留`CANDIDATE_ONLY`；即便存在，其本义亦为「某种特典道具」，**无法把“特典道具”升级成赠送宠物、宠物名或实际入账**。

## PET与版别证据止点

这个扫描文件是**第三方保存的同期杂志**，不是1999日本JSS官方宠物主表、原版测试CD、初回版光盘、当年服务端发放记录或客户端同构建采集截图。来源日期为杂志刊期，非宠物首次开放日期；相较2001 JSS手册和2003日服重开资料仍严格按不同年代处理。

当轮可确定的**新具名官服上线宠物 = 0条新证据**，不代表历史上1999年没有宠物，也不代表扫描册的图片无宠物。宠物总数 `null/UNKNOWN`；1999年 `NOT_YEAR_AUDITED`，CN/TW/JP/KR/OTHER各自审查门槛不变。不得跨到NPC/MAP、Stage B或新单机代码。

[来源校验脚本](../../tools/stoneage_pet34_jss1999_beta_print_custody.py)、[派生机器收据](../../research/recovered/STONEAGE-PET34-JSS1999-SEPTEMBER-BETA-PRINT-SOURCE-R1.json)、[受限反例测试](../../tests/test_stoneage_pet34_jss1999_beta_print_custody.py)。

**NEXT：** 同一1999 JSS阶段换走尚未核验的**原测试／零售光盘、1999版手册、原始版本宠物主表、当年官方具名捕获或发放记录**。对该杂志只有取得可核对的高可读原页/纸本才继续提取内容，避免重复下载31.9MB却把乱码当成果。继承原 `docs/CURRENT-STATE.md` blob `c89e0e33537990aa2132b47c40fef49a985a935c` / 2,709,173B，不改写。Stage A 7 PARTIAL+2 OPEN；Stage B/wiki GATED；R79 PAUSED_NON_BLOCKING；overall percent UNKNOWN。
