# 《石器时代》O6：原素材研究结果的引擎无关私人导出（2026-10-30）

## 本轮基点与选择

按协议复读 GitHub `main` HEAD `db615f4d88c4c6eac24809e2056549255b5f1a94` / tree `6bdc327b7e7fb1cb1905fc92ad39318bed50a690`、最新 O5 收据/README/路线/九系统索引；完整 `docs/CURRENT-STATE.md` Git blob `20050acf279a01555ab06a381dfcdc936bd381a6`（2,708,031 字节）经原 Git blob 接口取回，不截断、不重写。O5 相关主线 11 项 Actions 历史真实 success，未出现新的同构建宠物原始身份表。

先明确材料缺口：既有 `PET-IDENTITY-SAME-BUILD-SOURCE-TRIAGE-01` 与 `PET-SPECIES-SAME-BUILD-PRIMARY-MASTER-08` 已审原 TW1 原位图范围与后代 GMSV 源码/示例，但仍**没有**原发行同构建 `name → enemy/template → graphic selection → client SPR/image` 实物链。本轮没有以外观、编号或后代社区示范擅填名称；不重复无目标的 server/helper 逆向。转为可消费游戏资源研究交付，将已验 O5 原素材从私人浏览器单页导成**带明确来源、仍然私人使用、未来引擎可消费**的目录与 JSON/PNG 清单；这是研究资料布局，不是新引擎选型/新作美术/历史游戏运行。

## 实际执行的原件与结果

在本轮实际读取并 SHA256 验证私人 Library 已存 O5 ZIP：2,905,474B / `e2f6beb8789f1d755fe44bf6d3ba70f7bf6baf7cd713eb34cf47d18062aa5bc6`；其中原 O5 页面 2,897,821B / `2637ac0594ab3922b32fe3b6dd8819a173344933981feb7f5ffa6dc0d6816be7`。解析两个已内嵌的静态 JSON 载体 `source` / `o5-data`，校验保存版 DAT、两正反向原出口坐标、NPC 文档指纹、24 原动画/352原帧出现/208位图去重及零同版身份声明。无需启动旧 EXE、服务器、任何网络接口或扩原客户端。

`tools/stoneage_o6_private_export.py` **只允许**上述完整SHA相符的私人 O5 包、事先存在且为空的私人输出目录；若目的地位于公开仓库则拒绝，所有将写的 PNG 先解码、验证尺寸/来源SHA；不会覆盖用户已有数据。导出：
- `images/room1001/`：51 张不同的原保存版候选 tile/构件 PNG；`scene-1001.json` 保留27次原图布置、7×7取样界限、原 map DAT 与双向原 warp/create 元组。这是原 source 布置对应的**现代观察候选**，非原客户端原生绘图顺序。
- `images/town1000/`：8张实际原图片合成的候选画面（旧/扩窗、构件和NPC开关）；`scene-1000.json` 保留 7×11 有源观察界、原图合成原点和源地图 SHA/NPC(63,103)的静态文档摘要。**特别声明**：该私人 O5 页面只内嵌8张 composite 而非 1000 地图完整 tile 图层，故不得将此导出误报为整幅原地图或 tile-level 原渲染器。
- `images/pet_figure/`：208原 PNG；`pet-numeric-timeline.json` 保留原三数字组 100250/251/252 各8方向原码0、352次原帧及重复、不解释的 duration_word。宠物与地图未做实体/刷出联接。
- `images/tw1_separate_actor/` 7张台湾1.0原人物数值帧位置及 `images/saved_mixed25_actor_reference.png` 1张单独候选；前者显式保留跨版本隔离，后者也非已认证的原运行角色身份。
- `manifest.json`：上述275幅 PNG 的逐文件 SHA256、原像素尺寸、版本角色、未证门槛及相对目录路径。全部 **275/275** PNG 用 Pillow 第二条路径重新解码、尺寸/完整SHA复算同源文件。JSON 四文件、PNG及说明一共 **280** 个私人包成员。

产物完整 ZIP：`/石器时代/StoneAge-O6-private-engine-neutral-assets-20261030.zip`，2,146,298B / SHA256 `c64376b4a018cc444f2e2d51b871db75ca7e25106777b2a4475ebf2bfffd0bd5`，ZIP CRC无故障且280成员解回字节同工作目录。四JSON SHA分别写在公开 `research/recovered/STONEAGE-O6-PRIVATE-ASSET-EXPORT-ACCEPTANCE-R1.json`，私人原画和玩家脚本没有入 Git。

## 合成测试与公开验证界限

使用完全**合成的**1×1 PNG/虚构 208个数字位图、两张地图与元组，测试完整生成275图及16条安全/否证路径（PNG哈希错误、损坏PNG、错误DAT、错误warp、冒认证官方地图、改动作码、少帧、残缺资源、重复JSON脚本、目标路径位于公共仓库/已含他人资料等）。本地全部16项通过；合成ZIP取代完整真实原件只在测试函数作用域临时改常量，不会改变正式命令对 O5 SHA 的严格约束。GitHub Actions 只能重跑这16项合成用例，**不能获得私人 O5 的真 PNG，也不能验证真实原版游戏世界执行**。候选及主线 CI 的后验结果单独归档，不在本文预称成功。

可复用命令（示例路径须替换为私人本机位置，输出目录须已建且为空）：

```bash
python3 -m tools.stoneage_o6_private_export \
  --private-o5-zip /private/StoneAge-O5-original-two-scene-and-pet-private-20261030.zip \
  --output-dir /private/stoneage-o6-export
```

## 停止点与下一优先级

**新历史物种身份事实 0；新增真实可消费研究资产布局 1。** 不支持初代 TW1/1999 的特定 1000/1001 地图部署、原版宠物名、旧服产生野怪/捕获/骑宠、原生碰撞/原场景遮挡/自动warp/NPC事件、最终调色/动作时速或原图重分发许可。以这些私人 PNG 做完整单机体验仍需要逐项定义 **DESIGN** 行为、来源版本边界及版权资产替代，不以 O6 假称开始新作生产。

下一阶段优先两者择其一且不得互相伪证：
1. 若真有同构建 original `pet master / enemy template → graphic / SPR` 主表字节及可认证客户端资源，才开启一次有限身份联接；
2. 否则 O6 作为已验证私人研究输入，按项目 22 域组合队列选择一个能带来新游戏内容/规则事实的下一包，**不再扩独立宠物图像 helper，也不把系统研究替换成无证仿真**。

保持 Stage A **7 PARTIAL + 2 OPEN**；Stage B/wiki **GATED**；R79 **PAUSED_NON_BLOCKING**；总体百分比 **null**；原版真正世界仍未进入。保留全部过去失败和旧 CURRENT 前缀。
