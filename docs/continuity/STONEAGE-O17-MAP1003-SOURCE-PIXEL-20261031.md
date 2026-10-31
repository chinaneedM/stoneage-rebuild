# O17 原始地图 1003：实际文件与 38 幅原图候选（2026-10-31）

## 启动与证据分层
本轮重新读取远端 `main` HEAD `a6b632bcad474a114ac425391164ece77a8ea69f`、tree `500af3655ef44a031bf5b4b5f542a52dc2bcf676`（6737 项），Actions、协议、README、设计/历史/来源文件、Roadmap 和原 CURRENT blob `20050acf279a01555ab06a381dfcdc936bd381a6`。CURRENT 2,708,031 字节原文完整读取，**没有修改或截断**。当前最高 NEXT 来自较新 README/O17 载体覆层，不回退旧 CURRENT 尾部的 SCENE26。

**FACT／原材料**：私人保存版 mixed25 RAR 361255180B/SHA256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`，本轮全文件重新哈希。实际从成员 1685 提取 `map/1003.DAT` 5408B/SHA256 `fc3037a1850c8baf06ad5874a4cb49ca5e13e9315c020f64c019417c33b694e6`。与既有 2003-06/12 和 mixed25 目录记录同 SHA；没有宣称本轮重取那两个 2003 父包或认定官方原服。

**FACT／地图布局**：30×30、三组各 900 个 u16。第一图层 107 次有效图形引用（793 个零），第二图层 27 次有效图形引用（804 个值 2、69 个零）；134 个图形布置、38 个不同图号。第三图层 898 个 49152、2 个 49155，具体含义未证，不当作已完成的碰撞、可走性或脚本。

**FACT／实际原 RD**：私人 Taiwan 1.0 既存零售研究包 372626292B/SHA256 `3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24` 本轮重新全包哈希。原 ADRN 10079680B、REAL 315842228B、Palet_1.sap 708B 再全件验证；上述 38 个源图号在 TW1 ADRN 的 +76 别名字段分别**唯一**，全图 RD 实际读取 38 段，均为 RLE flag1，两套独立解码实现逐索引同一；无非零保留颜色索引。解码的是原 TW1 像素，不能因 map 值匹配便宣称 mixed25 同部署身份。

**明确缺件／未完成的同源联接**：本轮尝试从同一 mixed25 RAR 实读配套 `adrn_15.bin`，libarchive 在成员 1407 返回 `Parsing filters is unsupported`；未读出 mixed25 原 ADRN 或 REAL。仓库以往完整资源前缀报告仍可作历史桥梁，但本轮没有独立重复 763MB mixed25 REAL 内容的逐字节比较；不能把上述 TW1 原 RD 称为本轮直接取得的 mixed25 同包原像素。限定阻塞，不继续扩通用 RAR 辅助链。

## 一张候选画面与私人包
**DESIGN／现代观察，不是原版运行**：使用 TW1 原 Palet_1 候选 RGB、假设原行倒序和索引 0 透明、地面后构件以及现代等角 (32,24) 绘制序；得到 695×665 候选 PNG，RGBA SHA256 `f0745bba51f8c71a4e059fc7ce2501733048a56ec18f8efba9df4ff7589740ce`、PNG SHA256 `ae1511c3d68cd9335a66d9c91392bde767cd4629ff605c60f557b7f3d5bcc487`。另一像素覆盖实现全 695×665 RGBA 等同，候选图片实际目视。色彩最终值、透明/遮挡/地形脚本、官方地图名和原游戏画面均未认证。

私人 ZIP 1176526B/SHA256 `6bc9d015f4bcfde7a62957ce59d7e2b9bc662df9d67ce765868d0a13ec4b1452`，原 DAT、Palet1、38 TW1 RD、候选 PNG 仅存私人工作区；本轮将 ZIP 全成员 CRC、原 DAT、38 段 RD SHA 和候选 PNG 全部回读验过。原专有资源**不进入公开 Git**。公开仅 `research/recovered/STONEAGE-O17-MAP1003-ACTUAL-PIXEL-CANDIDATE-R1.json` 派生摘要、source-only tests/workflow 和本覆层；在 CI 中不会重跑私人源像素。

## 止点与后继
本包完成 O17 的有界 1003 原地图文件实读、38 幅 TW1 原 RD 和一幅现代候选观察；**未进入原客户端游戏世界**、未证台湾1.0/2003/mixed25 三源同服地形，未实际执行原版 NPC、碰撞、物品交易或音频事件。最高 NEXT 为 **O18-WORLD-MAP1003-NAMED-CONTENT-SOURCE-QUALIFICATION**：回 22 域，优先同一 2003 载体中具有原字节和版本的 `1003` 原创建/NPC 名称/任务或可查格位，给一个具名或行为材料增量；若仅后期宠物店字符串或配套 REAL 无法取出，登记精确缺件并轮换，不无界画所有地图、不装作 TW1 同版。同样保留 Stage A 7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79 暂停、overall_percent=null。
