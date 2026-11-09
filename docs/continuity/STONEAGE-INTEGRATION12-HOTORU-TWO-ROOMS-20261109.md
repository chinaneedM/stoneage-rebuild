# INTEGRATION12｜霍特爾两间有据室内场景与物品表冲突（2026-11-09）

## 续接证据与范围

依连续性协议从最新 GitHub `main` 2ad03fd85b8cd8b78fe26ea25789dfd9b2ac3118 / tree d31528ac826fe13fb0965d22587fdd067b03d132 启动。完整 `docs/CURRENT-STATE.md` 通过 Git blob 读取，原 blob `c89e0e33537990aa2132b47c40fef49a985a935c` **未修改**。承接 INTEGRATION11 的明确 NEXT，仅补地板 1306、1310 两间与 1300 互通的室内原内容；不启动原商业服务器，不设计新游戏。

先前保存在用户私人 Library 的 INTEGRATION12 原件包被视为**待核候选**而非远端既成成果。重新从该保管包读取 20 份原文本/地图成员、两张客户端 DAT 和两张原服务器 LS2MAP；31 ZIP 成员 CRC 全通过，20 原成员各自大小/SHA-256/CRC 全通过。两个 DAT 都逐完整 SHA 同 INTEGRATION11 已收录的两原件。源派生 JSON 自身 SHA 与画面原 PNG/RGBA 的 SHA 均重核；私下独立脚本共 **208 检查 PASS**。原混合 2.5 父 RAR 本轮**未整包再读**，因此只沿已存父 SHA 与本次子成员审计陈述其来源，不能冒充完整新一次 RAR 原件验真。

私有 ZIP：3,811,628 B、SHA256 `92f8f16985cad5b841424593526ad7801b520d7d4abd7fcc7e13db7c3f8d70d4`，31 成员；内含派生 JSON 33,379 B、SHA256 `babf44a883c41b7c3ec1962cd46ecc805217e0aacd455983f85463745d31f29c`。原图、源 DAT、脚本正文、私有 HTML 与 ZIP 均不上传公开 Git。

## 两间具体原游戏内容

**1306「霍特爾的長老家」**：原 LS2MAP 名称尾有 `|0`，保留原字符串与供检索显示名的区别。客户端 DAT 为 40×30，原家族长、家族传言板、普通村民各一原 CREATE，传送相关三原 CREATE，共 6。与 1300 的传送表有 6 条双向记录；其中原 `1306(21,21)` 竟有两条不同目标 `1300(53,26)`、`1300(54,26)`，不能按源门格去重或推断原生实际选择。已有私有原像素候选覆盖 265 绘制引用、58 图号，未覆盖 0。

**1310「營養劑名人的家」**：原 DAT 30×30，原商店 CREATE 真实坐标 `(16,16)`，并非其参数文件名后缀 `18_15`；另两个门格 `(10,15)`、`(10,16)` 与 `1300(68,44)`、`1300(68,45)` 对应。共 3 CREATE、4 条双向传送表记录。原像素候选覆盖 128 绘制引用、66 图号，未覆盖 0。跨两间 10 条源传送记录全与 INTEGRATION11 的原行号、行 SHA、方向、CREATE 块 SHA 精确对上。

地图差异须按源格式解读：服务端 LS2MAP 的 44 字节头后两平面是 **大端 u16**，客户端 DAT 8 字节头后三平面是 **小端 u16**。1306 原平面 0 共 1200 格全同，平面 1 有 71 格 `服务器 2 / DAT 0`；1310 平面 0 共 900 格全同，平面 1 有 4 格 `2/0` 和一格 `16073/0`，位于 `(16,15)`。差值不是碰撞或原生对象显示的自动解释；现代候选渲染亦非原版屏幕输出。

## 1310 商店的原始矛盾必须保留

原商店参数有 `ItemList` 16 个 ID、`LimitItemNo` 21 个 ID 和 `special_item` 5 个 ID，范围分别被私有原文逐项展开校验。21 个 ID 在本保留载体的主 `itemset.txt` **全部无匹配**，在备选 `itemset0710.txt` **全部存在**。 `setup.cf` 中 `itemset3/4/5/6file` 条件项引用 `data/itemset.txt`，但编译宏、实际加载的表、成交路径与价格语义尚未从真实原版运行证明。不得把备选表自动当成当时生效的商店，也不得称主表的数据已被修补。

## 验收边界与 NEXT

本包属于**后期社区保存载体的来源合格静态内容及私人离线观察**，不证明台湾 1.0 / 1999 JSS 同部署、原 NPC 实际出现、原角色移动、碰撞、门口选择、原商业交易或原生美术绘制。公开报告仅保留源 SHA、数值及负证；公开 CI 只能复核派生值与此前 Git 源证的约束，不等于本次私有 208 项和原客户端运行。

**NEXT：INTEGRATION13** 在同一已验 1300↔1301–1305 房间群里批量查明尚无可观察内容的实际原房间名称/门点和已存图块是否足够；只新增有源 NPC/场景关联，其他已闭合窗口直接引用。遇到无新增实物或缺同版材料就标明 SOURCE_BOUNDED_PARTIAL，转物品/装备/任务模块交叉整合，不扩抽象查看器。Stage A 仍 7 PARTIAL + 2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，整体完成百分比仍 UNKNOWN。

[公开派生源记录](../../research/recovered/STONEAGE-INTEGRATION12-HOTORU-TWO-ROOMS-SOURCE-JOINS-R1.json)；专项公开测试 `tests/test_stoneage_integration_module_12.py`。

## 内容主线与 CI 实际终验（2026-11-09）

候选 PR #279 内容 HEAD `f0efe97aabc1535af66aebb94c30251e8427ea99` / tree `486ac0187917033b44eb8fdc4036019b24f88ee4`。**候选 14 项 Actions completed/success**。squash 到 `main` 的提交为 `9943b8cbd70dc0d6639f2ed0130f0243844da17d`，tree 与候选 tree 完全相同；**合并内容主线 11 项 Actions completed/success**，其中专项 [run 42560357573](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42560357573) / job 128975202117 的日志实际运行 **6 项公开元数据测试 OK**。

已从合并树逐核五文件 SHA，且 `docs/CURRENT-STATE.md` 原 2,709,173B Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 原样保留。完整源受限事实/私人 ZIP 摘要和公开 JSON 的 Git blob 见[永久验收收据](../../research/recovered/STONEAGE-INTEGRATION12-PUBLICATION-ACCEPTANCE-R1.json)。原生角色、门格与商店执行依然未证；记录本后验提交自身 Actions 之前**不预认其执行结果**。NEXT 保持 INTEGRATION13 源合格房间群批量核查。
