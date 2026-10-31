# O34 — “烏力”同归档来源与原 TW1 动画完整字节匹配（2026-11-01）

**真正新增的是更强的宠物来源身份与实物可视化，不是另造宠物系统。** 从远端 `main` `610662c61e40d5be4d87907d15a05772f856f87e`、tree `68ddb62271be478328f708ca182f8568a3eb38ca` 及其完整 `CURRENT-STATE.md` 历史blob出发，复用已保存的后期混合原包 R40 来源和 O33 私人连续村落观察器。原 O33 中的 SPR100297 ↔ 昆伊，只是跨版**数字同号**；本轮将显示对象**换成 R40 有完整动画组同字节证据的“烏力”候选**，并重从台湾1.0原 `P3H` 提取原像素。原版宠物状态、名字是否属于台湾1.0官方服仍不认证。

## 具体来源链（FACT 与 OPEN）

1. 后期保存版 `mixed25` 原压缩包（361255180B/SHA256 `d71e2e67…`）原服务端 `enemybase.txt` 147750B/SHA `1be7d522…`，物理行1有原名 **烏力**、模板号1、原 `IMGNUMBER` **100250**、列38值1，原整行SHA `5f3b4e82…`。源列身份按已有 `STONEAGE-PRESERVED-PET-SPR-MATERIAL-R40.json` 报告，不是本轮重新下载后期原RAR。
2. **同一后期保存压缩包**原客户端子目录的 `spradrn_5.bin` / `spr_4.bin` 中，R40 已实际校验编号100250位于组索引240、原字节范围 `[1674640,1678352)`。其**完整组段 SHA256 `eb1a87cd4cc8e3b409990783c7bcc3bc463acab4cac7d2d961127d899da047ef`**，已与台湾1.0原 `SPR` 同号组完全相等。该事实从 Git 当前已有的 [R40 公共派生报告](../../research/recovered/STONEAGE-PRESERVED-PET-SPR-MATERIAL-R40.json) 和 [R40 源收据](../../research/recovered/STONEAGE-PRESERVED-PET-SPR-SOURCE-R40.json) 复核，**没有本轮重新提取 mixed25 原 `spr_4.bin`**，不能表述成新的一次全RAR认证。
3. 本轮从私人保存的台湾1.0完整ZIP **372626292B/SHA `3a4854ad…`** 自行再次核验 `SPR` / `SPRADRN` / `ADRN` / `REAL` / `Palet_1.sap` 全文件SHA。独立按原 `SPR` 组240得到动画数56、组长度3712B，算得**完全相同的整组SHA**。第一个原始图号95883的ADRN条目 SHA `c6178671…`，REAL原RD第1类RLE字节 SHA `a344ce31…`，实际解码28×52原像素，候选 PNG SHA `2573ee16…`。调色板顺序、透明和纵行方向仍只作为**现代选色候选**，非原客户端在画面中真实运行选法。R40还已接受100251、100252两条同级来源，但本轮**不扩全三只**。

这证明更具体的 **“后期同一保存包内服务端原宠物名/原图号 + 客户端组号 + 完整组字节跨版相等”**；却**不是**同一官方商业服务端/客户端部署证明，**也不是**早期台湾1.0官方名录或玩家实际拥有/跟随的证据。

## 实际画面与验收

仅替换 O33 私人 HTML 的一张宠物原图和必要来源说明、宠物元数据。以前的地图1000/1001、玛丽娜丝显式资料场景2000、全部257个原RD别名、O31的5条 Warp、O32送花/贝壳原静态任务、商店ID0来源数据，原JSON对象均逐值相同。跟随资格继续使用后代 `ITEM_petFollow` 源模型，玩家上一格的宠物位置仍是**现代观察器布局**，不构建新寻路、物品拥有、捕获、存档或NPC逻辑。真实 Chromium/Playwright `page.set_content` 源图浏览器 **36/36 检查通过**：原 PNG 浏览器自然尺寸28×52、7个后代资格/拒绝样例、高等级拒绝、同级允许、跟随、反向行走、三段送物、明确非原版跨村资料切换、入店后仍显示宠物、停止跟随和复位；0 JavaScript 异常、0 外部HTTP。两张原像素实际浏览器截图私存；不宣称 `file://` 双击或原 `sa.exe`/服务器启动。

私人8成员ZIP `/石器时代/StoneAge-O34-private-source-qualified-wuli-world.zip` **3154788B/SHA `0c9c38817f6b4c7838a7be0ec122f7dbe274b52a0153b6c7a23c27365fd1dbe2`**，成功上传个人Library并完整回取，SHA和全部ZIP CRC一致。**原台湾1.0图像、完整 HTML、原剧本文字、原地图不得上传公开Git**。本轮公共仅发布此边界、[数值派生来源收据](../../research/recovered/STONEAGE-O34-WULI-SAME-ARCHIVE-SPR-EQUALITY-R1.json)和 README 指针。

历史 `CURRENT-STATE.md` 完整 2708031B，Git blob `20050acf279a01555ab06a381dfcdc936bd381a6` 已独立全量核读，不替换或重写。Stage A **7 PARTIAL+2 OPEN**、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING、总百分比 null 保持。

**NEXT O35：** 结束宠物跟随界面扩张，跨领域优先核取**真正同来源的原音效事件→音频文件调用关系**或其他尚未有实物的游戏内容；缺原调用点则明确有界止点，转其他22域，不重做 WAV 播放器或新框架。
