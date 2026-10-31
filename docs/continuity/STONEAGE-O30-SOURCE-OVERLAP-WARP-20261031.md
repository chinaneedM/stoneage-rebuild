# O30：原 DAT 双向行走的重叠式传送交互（2026-10-31）

> **增量事实与边界：** 此记录在完整 `docs/CURRENT-STATE.md` 及 O29 的基础上追加；不覆盖、不截断旧文件。远端起点 main `8d8629c2c92d14667c8b5b25bdf6fa7361295cec`，tree `4ecfb1efdaa23ea7534ccea1759c7d074c58234c`，旧 CURRENT blob `20050acf279a01555ab06a381dfcdc936bd381a6` 未变。

## 本轮真正新增的体验

O29 私人离线观察器此前可沿原 DAT 网格行走，但到地图1000(63,99)后须手动按 W 才执行源成对 Warp。O30 沿用同一源图和同一两张 DAT，把**新走入传送格**作为自动切换的交互候选；立刻落在另一图门格时**不会自动反弹**，必须真正移开并重新进入该格。W 仍保留为手动比对入口。自动引导、键盘正常行走、进入武器店、查看来源商品前三行（含有效ID 0）、重置均保持可用。没有引入新画面资源、地图扩图或新游戏引擎。

**源分层：** 台湾1.0真实原图来自已验 TW1 原资源，地图1000/1001、成对 Warp 坐标与商店资料来自**不同的后期保存 mixed25 原始文件**。后代源码 `NPC_WarpWatch` 模型约束“玩家实际步行进入同格”触发，而不是按键切换；这是设计有来源的现代离线模拟，**并非台湾1.0原客户端或原服务器执行记录**。原同构建角色/地图/Warp/NPC身份仍未证。

## 独立 DAT 事件值反例

原始地图分别核整件 SHA `94b19cb59d72b7b48da70d2741ba68516caad970297fd48ed11ef720fa3ea97e`（1000，153608B）与 `62dbef1614ede0ba032ca9c69cbfdc3d43938e45baba78701885790937b86b90`（1001，5408B）。1000 的(63,99)、(63,100)原事件值均 **49155**；1001 的(10,15)、(10,16)也均 **49155**，低12位为3。因此 **49155 非 Warp 专属标记，更不能据此推断通行/碰撞**。真正的传送候选依据另一个来源：`warp_y.create` 两原块，SHA `d0b4f955…` 与 `d35da32a…`，精确给出 1000(63,99) ↔ 1001(10,15)。不得把事件值与 Warp 创建块混作同一证据。

## 实物及浏览器验收

O29 原件私人 ZIP 完整 SHA/CRC 核实后复用原图。新简体中文单文件 HTML 内嵌原 TW1 像素。私人 Chromium **144.0.7559.96** 以 Playwright `page.set_content` 真实加载原图并完成 **18/18** 操作检查：入格正向传送、自动引导、纯键盘步行、落点不反弹、退出后重入反向传送、离格手动 W 拒绝、NPC前三商品查阅、重置；0 JS 错误/0 外部请求。两张原像素浏览器截图与原HTML一同私存；没有认证浏览器直接 `file://` 文件打开，没有真实启动原 `sa.exe`，没有执行原商业服务器。现代行走未应用或验证原生碰撞，自动导航只保证在已提供网格坐标上移动，不代表历史可达路线。

私人 **10成员 ZIP**：`/石器时代/StoneAge-O30-private-source-overlap-warp.zip`，2668881B，SHA256 `84e883cd57f2b77100ad7a82ecbf5957b5199ff10ed6b0dbdf9141be882d09fa`；上传个人 Library 后重新取回，整包 SHA 一致。原图、完整 HTML、原 DAT/传送配置、截图与原文字**不公开**。公开只写本摘要、来源数值/哈希、负边界和少量无原件字节的测试。

派生收据：[`research/recovered/STONEAGE-O30-OVERLAP-WARP-INTERACTION-R1.json`](../../research/recovered/STONEAGE-O30-OVERLAP-WARP-INTERACTION-R1.json)。本轮前置 O29 是 [O29记录](STONEAGE-O29-SOURCE-WARP-CONTINUOUS-WALK-20261031.md)；所有更早研究文件保留。

## 后续优先级与止点

**O31：只在能拿到这条路线同来源的碰撞元数据/原服务器 LS2MAP 等具体原件时，判定1000/1001的有限相邻格通行及门前行为；否则明确缺失的文件名与风险，立即轮换到有真实内容增量的其他22域任务。** 已有 `stoneage_map_collision_model.py`、`stoneage_recovered25_server_collision_provider.py`、`stoneage_tw10_hit_map_model.py` 供复用，不要重复造碰撞规则。不得用 49155 猜通行、不为这次 O30 再堆相机/UI、也不自动声称原世界已进入。

Stage A 7 PARTIAL + 2 OPEN；Stage B/wiki GATED；R79 PAUSED_NON_BLOCKING；总完成百分比 null。**历史 CURRENT 全量 blob 原样保留**。
