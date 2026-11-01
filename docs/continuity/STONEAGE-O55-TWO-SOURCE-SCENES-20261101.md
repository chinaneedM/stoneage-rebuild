# O55 — 已验原素材的两地图离线观察切换（2026-11-01）

## 最新远端与有界目标

从 fresh `main` HEAD `752ff438bf7098f1f55005e8fc136220b78955b9`、tree `e1e8a063a99cf44d9c2603f52b3ec7f0ca3b33c9` 接续；最新 O54 合并已通过对应 10 项主线 Actions，开放 PR 0。完整 CURRENT 原 Git blob `20050acf279a01555ab06a381dfcdc936bd381a6` 与协议、路线、O17/O20/O37/O38/O53/O54记录已读。承接 O54 的 `1003.DAT` 原始二次实读缺口，不重复 O17 的既有原图/数据恢复。

用户私人 Library 中确实可列出 `StoneAge-O17-private-map1003-original-source-candidate.zip` 1,176,526B 以及图像 `O54-world.png` 1,029,228B、`map1003-combined-palette1-candidate.png` 373,876B，后两幅能以 Library 图像接口直接显示。尝试将 O17 ZIP 原字节复制到运行容器，两种已授权的文件引用形式都返回 `This Project file does not have an authorized raw-byte materialization path.`；亦用文件阅读接口读该 ZIP，结果为 `No readable content was found`。这不是文件不存在，也不是重新认证了原 DAT SHA。**本轮实际读取 `1003.DAT` 原始字节 0B，地图(15,21)/(16,21)三平面仍未做本轮原字节验收。** O17 既有原来源 `map/1003.DAT` 5408B / SHA256 `fc3037a1850c8baf06ad5874a4cb49ca5e13e9315c020f64c019417c33b694e6` 保持历史报告事实，而非 O55 新实读。

## 本轮实际可用的观察增量

新增一个不带商业图片的**极简来源校验双场景观察页** `tools/stoneage_o55_two_scene_observer.html`：选择两张已有、用户自己持有的 PNG，浏览器 WebCrypto 验全部原字节 SHA-256、PNG 头及原尺寸才允许显示。O54 外部走廊采用现有 `research/recovered/STONEAGE-O54-VILLAGE-TO-PETSHOP-SOURCE-CORRIDOR-R1.json` 的 **1744×1507** `world.png_sha256=01fa9248...`；O17 已保存室内原图候选采用 `STONEAGE-O17-MAP1003-ACTUAL-PIXEL-CANDIDATE-R1.json` 的 **695×665** `combined_PNG_sha256=ae1511c3...`。不因文件名匹配就接纳错误图片。两入口/反向来源配置引用旧 O37，按钮只做显式资料切换与缩放，不模拟行走、原生 Warp、NPC、商店交易或生成地图数据。原 PNG 从未写入此 HTML 或公开 Git。

这与已有通用 `modern-observation-viewer.html` 的合成研究标记不同：本页**不画人工移动/角色、不将两版本混合装作原服**，只用此前已认证且保存在个人 Library 的两幅原来源画面提供静态连续资料入口。用户可从私人 Library 下载 O54-world.png 和 map1003-combined-palette1-candidate.png，再打开此 HTML、选择两文件。文件不离开用户本机。

## 本轮独立测试与边界

- 本地 Node `--check` 对内联 JavaScript 语法通过；HTMLParser 完整解析成功；新增源凭证吻合、版权空载荷/CSP及异步过期校验三项 Python unittest。
- 本地 Chromium 在受限执行容器禁止 `file://`/自定义 HTTPS 导航，因此使用 `page.set_content` 加**合成红/蓝 PNG、明确模拟 WebCrypto digest**测 UI 路径：错误来源拒绝、正向接纳、切图、缩放、零外部请求/零 JS 错误通过。**这不是原 PNG 的实际浏览器重新验证，也不是原生 WebCrypto 在 `file://` 下的验收**；客户端原 DAT/双原图没有在本轮经浏览器再次实测。
- 源 O17 的候选配色和对角绘制不是原运行画面；O54 的原图像素源桥也不认证同一后期运营 build。原地图进出坐标仅源脚本静态引用，1003 回门格字节、原生碰撞、传送触发、宠物托管与原游戏世界进入仍 **OPEN**。
- 不新增历史数值发现或原地图/物种恢复计数。私有商业 PNG、DAT、RD、RAR 没有进公共仓库。

当前 `CURRENT-STATE.md` 全历史2,708,031B blob 原样保存；Stage A **7 PARTIAL + 2 OPEN**，Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，`overall_percent=null`。历史失败不回写为成功。

**NEXT O56**：O55 已闭合的是现存两张来源 PNG 的*人工观察切换入口*。原 1003 DAT 只有在能授权取回并完整 SHA 验证原字节时才有限复查两出口格；否则立即轮换到别的有具体原件可读、能新增真正宠物/任务/世界体验内容的材料，不能继续为这一项制造模拟地图/传送引擎或重复元数据报告。候选/主线 Actions 验收据实际结果追加，不提前宣称。