# O43 — NPC 16209 原始索引别名与实际源像素（2026-11-01）

## 本轮真实原材料

按 fresh main `a66a9bcaf6b2e7bc9f09f4a6d097cf6a6ddee641`、tree `6bbe43ff08b28dba9a6ace84e998a2f0a656be3c`，原始 `docs/CURRENT-STATE.md` 2,708,031B / Git blob `20050acf279a01555ab06a381dfcdc936bd381a6` 全量读取；原历史不覆盖。最新主线十项 Actions 均 completed/success。O42 已有保存版 mixed25 萨姆吉尔 floor1000 (62,115) 的真实 `1000npc_m.create` 块，`graphicname=16209`、一条行内问候及原 DAT 格，仍不证明商业服执行；O43 只解 O42 的**真实图像缺口**，不新做脚本系统或假 NPC。

从私人 Library 重新取回既存台湾 Waei/JSS 1.0 P3H 实物 ZIP **372,626,292B / SHA256 `3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24`**，实际完整 SHA 复验；原 `adrn_1.bin` **10,079,680B** / SHA `47254c0ff904d363fb5c3c5297edf553c8eaf24cd933f346d8ce7aabed4155c8`，原 `real_1.bin` **315,842,228B** / SHA `408e6ee05c83354349691937da2ad8f7488ac10f65f07e6681b7d92cb1c9ed13`，`Palet_0.sap` / `Palet_1.sap` 各 708B 整 SHA 均与旧记录相等。保留的 R1 完整比较已认证 TW1 的 **125,996 条 ADRN 与前 315,842,228B REAL** 是**指定 preserved mixed25 资源的逐字节前缀**；本轮**未再取回/重核完整 mixed25 ADRN/REAL 或 361MB 父 RAR**，不能把旧比较当作本轮实时双父来源重验，也不能证明两端是同一实际部署 build。

## 新的实质像素关联与误读反例

扫描原 TW1 **全部 125,996 条** 80B ADRN：记录最后 +76 的原始数值 `16209` **只出现一处**，物理 `bitmapno=5929`，原 80B 记录 SHA `72c6b9bb151e01034ee53d4ee1662b1582dbf5260b3850791b9c6782ffd65f24`。其真实原 RD 在 REAL 字节偏移 **25,099,083**，长度 **1,937B**，SHA `48f1f20adc4a55fd17c4c1a6038567cbab8d5df8583dab33cd54bd8e5ce2dc23`，解码尺寸 **36×84**，源偏移 **(-17,-74)**，索引像素 SHA `b5f31818d3a04f34767db376ec0460569fb134ffff2862b7a8bfc08283773058`。

严禁误把 `graphicname=16209` 当物理第16209块：**物理 `bitmapno=16209` 也实际存在**，但它的原记录末尾别名值为0；其 RD 在 REAL 偏移 **48,404,388**，大小 **1,848B**，SHA `ac7348aa10552354c8afe99fc0bcf11756d0b156085306dc839e79e69e7d8093`，像素 **40×88**，索引 SHA `488c767c7e2a2e76141718f0c46f3306102c2f56deb6a7e24ef157e3c93fd214`。两块不仅编号不同，像素也确实不同。独立两个 RD RLE 解码实现对两块全部索引像素、尺寸均一致；对 TW1 原 Palet0/1 初始配色候选分别离线导出 RGBA/PNG 并哈希保管，不把候选色认作原游戏场景实际调色板。

## 最少集成、验收与保管

直接修改旧 O42 **私人**原图世界观察页中 (62,115) 的“无证肖像”标识：现在可见**原始 TW1 图块5929 的 Palet1 候选像素**，明确标注「16209→5929 原图别名候选 / 未证原生选图」，保留 O42 同载体 NPC 问候、旧任务/交易资料、O41 缺原目的地拒绝传送以及音频/战斗资料。无新引擎、无 NPC 行为猜测、无官方身份绑定，也无图像公开入 Git。真实本地 Chromium/Playwright `page.set_content` **14/14** 检查通过，包括候选PNG被浏览器解码、来源坐标与问候、任务/背包不变、距离拒绝、缺图传送阻断、0 JS 错误、0 外部 HTTP；`file://` 双击未成功认证。

私人 **8 成员** ZIP `StoneAge-O43-original-NPC16209-actual-art-final.zip` **3,452,831B / SHA256 `644ed6a0085a7253093624d787476c6b460b47a11b8581f891aaff39031d9d4a`**，含原 RD/索引图片和候选画面对照、自包含离线观察页、真实 Chromium 截图及本地验收；ZIP CRC 全过。当前只作为本轮私有文件交付，**个人 Library 上传未确认成功**，不冒称已永久上传。原商业原始图像、原文、EXE、RD、PNG、HTML 都不进入公开仓库。仅 [非专有派生摘要](../../research/recovered/STONEAGE-O43-NPC16209-ORIGINAL-PIXEL-ALIAS-R1.json)及本说明公开。

## 历史边界、止点及 NEXT

上述是 O42 保存版 NPC 数值与 TW1 原资源完整比对链下**可信的原始图像候选**，不是原编译程序的 `graphicname` 查找调用实际执行证明；同一已部署服务器/客户端、NPC 外观真选择、实际位置/遮挡、原生交谈、碰撞/触发、原场景配色均 **OPEN**。过去的完整前缀关系不认证所有后代版本，也不认证最初 JSS1999 商业 NPC。

Stage A **7 PARTIAL + 2 OPEN**，Stage B / wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，整体百分比 **null**。本图像候选已达到当前原字节可证止点；**NEXT O44** 回22域轮换到有实际完整原始载荷的 NPC/宠物/地图或游戏规则，而不是再为同一静态 NPC 增添按钮/假动作。仅得到可溯源同版本原生选图调用轨迹时重开该 selector；1011/1014 室内仍等同载体原 DAT/碰撞字节。


## O43 私人保管后验（正式回读验收，加法补记）

在上述本地ZIP完成后，本轮通过可写个人 Library 工具**实际上传成功**：`/石器时代/StoneAge-O43-original-NPC16209-actual-art-final.zip`。再以该持久化文件 ID 直接回下载 ZIP，**全体 3,452,831 字节 SHA256 `644ed6a0085a7253093624d787476c6b460b47a11b8581f891aaff39031d9d4a` 完全相同**，8个成员 ZIP CRC 全部通过。前文“未确认已上传”描述的是本地封包时的阶段，不是最终保管状态；O42 先前的 Library 上传失败仍然是独立历史事实，不追认 O42 那次成功。该后验只提升O43私人资料保管确定性，不提升历史原版/同服或真实运行结论。
