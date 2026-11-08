# QUEST16｜哈恩造斧、科巴尔特取水、巴尔伐木与赛尚木材交易原脚本（2026-11-08）

## 1. 从 GitHub 最新状态续接与旧成果查重

本轮按 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` 从远端 `chinaneedM/stoneage-rebuild` 的 `main` **`a20f84b7e64c11467839e3b33871e70400261e9c` / tree `c5c7b12745d41fe27a54cc299ddac287a51f4b9d`** 启动：实读远端分支/提交/Actions/README/协议/决策/历史/来源库/路线、最新 QUEST15 接续及 `docs/CURRENT-STATE.md` 原 Git blob **`c89e0e33537990aa2132b47c40fef49a985a935c`，2,709,173B**。普通 GitHub Contents 的 CURRENT 空正文不是空文件，原 blob 成功读回；不截断、不覆盖。

**本轮具体游戏对象**：后期社区混合 2.5 保存包中，`jaruga/event/20501ev.create` 指向的五份 `20501ev1..5`，分别涉及斧职人、取水、伐木、介绍与木材交易。事件 **18/19** 原指令、壶→斧→木材/介绍、断键修复与断斧改造、14 档石币字面构成新专项来源资格。不把 `event` 目录等同节日，不把后期脚本宣称 JSS1999、台湾 1.0 或大陆 1.82 官方服务器。本族与此前 QUEST08（矿石鉴定）、QUEST10（采石/精灵）、QUEST12（矿山比赛）、QUEST14（三龙）、QUEST15（山贼 event20）**原文件路径/脚本块并不相同**；但本批 5 条 CREATE、36 原 TYPE 段早已在 QUEST01 全量索引内，仍是**既有原件的实际再读与新专项交叉关联**，不是发现了36个历史上未知的事件。

止点：取得准确源脚本字面、道具双表物理行及跨载体原 RD 候选图、现有地图来源资格和已知负证；未真正运行原 NPC/奖励分支、原地图移动或原商业服务器，不推数学收益公式或修正原脚本。

## 2. 实际原字节及可核身份

- 私人现存 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip` **995,176B / SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`**；本轮实读 2,205 个归档条目的 ZIP CRC 全部正常，真读 1 CREATE + 5 源脚本 + 1 同目录模板的 **7** 件完整原字节。5 脚本原 SHA/CRC、36 段 `EventNo/TYPE/EVENT/section` 哈希与先前 QUEST01 **Git blob `52db8b4b6cd43cd2afa4a8d2e8460f214933f5e2`** 逐段吻合。源脚本末尾存在两种不同换行：`20501ev1` 结束于裸 `EventEnd`，其余仍有尾换行；独立算法最初对这点不符而**拒绝输出**，随后按旧索引真实正规化规则修正，36/36 独立相等，原始脚本不改。
- 物品从已保存私人 `StoneAge-ITEM01-private-two-itemsets-832-original-RD-icon-observer.zip` **5,868,386B / SHA256 `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa`** 真实重新读取。**12 不同物品 ID、24 个原 94 栏物理行**（`itemset.txt` 与 `itemset0710.txt` 各一），逐行 CP950 字节重组 SHA 及公开 ITEM01 原 shard01/02 相符；两份表里同 ID 原行在本批各对相同，不能把24原行叫24种道具。见[无版权正文派生报告](../../research/recovered/STONEAGE-QUEST16-AXE-WOOD-SOURCE-R1.json)。
- 这些 12 ID 的源图别名只对应 **8 幅不同图**。从用户原 ITEM01 私人包实际回读 8 PNG，逐完整 SHA 归档；其原 RD 来源系另一个**台湾 1.0**载体，精确 `alias → RD → PNG` 仅作为跨保存来源**视觉候选**，不能认证当前混合社区服务器与早期同服、道具原 UI 或实际装备外观。

## 3. 五名原 CREATE 与已验证地图来源界限

| 仅本保存源中原名 | 位置 floor/(x,y) | 原图形别名 | 指向原脚本 | 地图证据级别 |
|---|---|---:|---|---|
| 造斧專家哈恩 | `20508/(12,11)` | 16024 | `20501ev1` | MAP09 先前原 DAT SHA 已验，25×25 |
| 看守用水的科巴爾特 | `20507/(32,29)` | 16207 | `20501ev2` | MAP09 先前原 DAT SHA 已验，60×60 |
| 樵夫巴爾 | `3300/(60,75)` | 16018 | `20501ev3` | MAP09 先前原 DAT SHA 已验，120×120 |
| 喜歡八卦的年輕人 | `3300/(46,55)` | 16047 | `20501ev4` | 同上，一份地图不是第二份地图 |
| 木材商人賽尚 | `3000/(114,69)` | 16000 | `20501ev5` | **没有在当前 MAP09 691 份或 MAP10 60 份来源就绪目录取得可复验的本楼层 DAT** |

三份符合来源资格的 DAT 原 SHA 分别为 `20508=8f31c2a1…56a2e`、`20507=6a505b45…c85ec`、`3300=7f47b7ff…381e8`。此处是**独立重读公开既有 MAP09 目录和原 SHA**，本轮新取得原 DAT 字节 **0**，新逐地图三平面格值读取 **0**。不从“某楼层不在当前观察目录”升级为“原游戏没有该地图”。虽有旧现代画面三状态 SHA，本轮不把它们冒充刚启动原客户端；源图层语义与原世界可达仍未知。`3000` 精确缺件保持待源。

## 4. 原控制关键事实（静态字面；非执行）

- `20501ev2 #1`：`ITEM=2463` 的请求交换，字面 `GetItem:2464*1`、`DelItem:2463*1`；原物品名对应哈恩的空壶／满水壶。`20501ev1 #1` 的制作条件 `NOWEV=19&ITEM=2464&ITEM=2466`，字面 `GetItem:2465*1`、裸 `DelItem:2464,2466,2463`、`EndSetFlg:19`。还有 `GetItem:2463` 的再取壶分支；裸参数是否一次消耗、分支顺序和容错没有原生运行证据。
- `20501ev3 #2/#3` 两条接受事件共享 `GetItem:2467,2484`、`DelItem:2465*1`、`EndSetFlg:18`，但**事件号不同**；`#4/#5` 又按 `NOWEV=18` 与 `LV>14` 申请 2466，不根据任务直觉自动合并。`20501ev4` 只有一条与 `ENDEV=18` 关联的 CLEAN 原段。
- 与造斧相关的两个独立原交换：`2484→2485` 是断斧改造；`1837→1838` 是断键修复。二者是在同一脚本中发现的**额外原材料交接分支**，不能宣布所有玩家通关必须经历。
- 商人 `20501ev5` 有 14 条 `ITEM=2478&ITEM=2468*N` 的接受分支，原 `GetStone` 明文各为 **400、1600、2400、3200、4000、4800、5600、6400、7200、8000、10000、12000、16000、20000**，对应 `N=1…14`。这些不是运行实收的石币，也没有证据支持统一线性公式、分支优先序、交易重复性、物品包裹容量或实际商品限额。尤其 **`N=12`** 的 `DelItem` 原字面只列 `2468,2478`，多数其它档是 `2468,2478,2467`；本轮保留这个**来源内部差异**，不私自补 `2467`。并且这些 `DelItem` 都没有显式 `*N`，不得因判定式中的 `*N` 就自动断言会扣 N 件木材。
- 商人还有当持许可证但无木材时 `DelItem:2478` 的分支，及用 `2467` 换取 `2478*1` 的 REQUEST。部分原文条件与其它分支可能重叠，**没有真实事件分支选择机制的回放**，不可推演发生顺序。物品 2463/2464 共用候选图 23010、2465/2485 共用 20020、2466/2467/2478 共用 24222，**同图号不是同物品**。

## 5. 来源分类、局限、保管与下一任务

本轮借现有 DD-032 分类在不复制主数据的前提下建立一族静态关系：`mixed25原配置 → floor/坐标 → 原 changeevent 脚本 → 源条件/物品转移/原旗标 → 独立原物品行 → 跨来源 RD 候选`。地图“村庄/南北岛”归属、原始官方季节/版本、NPC真实表现和受条件影响的流通经济均 **UNKNOWN**。来源属于社区混合保管档，版权原正文只在私人 Library，不在公开 Git、CI、PR。

**私人包独立验收**：`StoneAge-QUEST16-axe-wood-original-private.zip` **32,862B / SHA256 `b71dfd1244871b3d864621db7f7dc7c6822ac8646ceafb71a8670dfd996688e5` / 40 件成员**，由 7 原 NPC 文件、24 条原物品正文行、8 PNG 和 1 份仅数值/摘要报告构成。已实际保存 `/石器时代/` 个人 Library，随后从**新文件 ID**重新取回并逐完整 ZIP SHA、CRC 与成员总数验证通过。这是私人研究资料保管，不等于对原商业服务器运行的验收。

**公开交付**：派生源报告、可选私人源再读提取器、12 项公共回归、本记录与最小必要连续性指针。CI 不下载私人原资产，只验证旧 QUEST01/ITEM01/MAP09 数值 SHA 和推导一致；远端 Actions 成功与否应另以后验确认，不预支状态。原 CURRENT 全 2,709,173B 历史不改写。

**结论与止点**：`QUEST16=SOURCE_BOUNDED_STATIC`；未证实原脚本原生交易/掉落、14 档实际支付、同年代官方任务，地图 `3000` 源 DAT 和三张已验地图对应原格还未由本轮新读。Stage A **7 PARTIAL + 2 OPEN**，Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，`overall_percent=null`。本族已经达到来源就绪专项研究止点，下一最高 **`QUEST17-DEDUP-AND-NEXT-ORIGINAL-SOURCE_FAMILY`**：优先从旧 QUEST01 及已保管原文件中查重后挑另一组确有独立原条件/道具/地图证据的任务族；`3000` 的真正 DAT 或原生执行若有同源输入再单独增量重开，不扩空转工具，也不做单机新作引擎/联网服务器。

## 6. 正式发布、私人保管与 CI 独立后验（2026-11-08）

- 候选 `agent/quest16-axe-wood-source-20261108` 提交 **`9fa2a6b48f6464ee33f03510c4723162f9b93ddd`**，整 tree **`11e4fb95a71eecc6cdbdf444b3a9be63fc124157`**。远端先复核差异恰 **6 路径**：4 新文件（工具、12 专项公共回归、派生 JSON、本文）+ README 指针 + 原 QUEST05—16 工作流追加，无版权原脚本正文、DAT、RD/PNG 或私人 ZIP 入 Git；旧大 CURRENT blob `c89e0e33537990aa2132b47c40fef49a985a935c`/2,709,173B 原样保存。
- **[PR #256](https://github.com/chinaneedM/stoneage-rebuild/pull/256)** 已 `merged=true`，合并主线提交 **`7020875eba396f5744c05bbb732afcfaf9c9d919`**；独立再读主线 Git tree，恰与已验候选 tree **`11e4fb95a71eecc6cdbdf444b3a9be63fc124157`** 相同。
- 候选 push+PR **14/14 Actions completed/success**；专项原来源 [push run 42460199322](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42460199322) job `128667648268` 和 [PR run 42460244206](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42460244206) job `128667784595` 的新增步骤 `Validate QUEST16 original axe, water and wood trade source limits` 实际均为 completed/success；QUEST14/15 回归同通过。合并主线 **11/11 Actions completed/success**，含专项 [main run 42460303877](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42460303877)。这证明公开纯数值/旧来源索引验证成功，**不等于 CI 运行商业原客户端/私人资产**。
- 私人 `StoneAge-QUEST16-axe-wood-original-private.zip` 已写个人 Library，并从新云端文件 ID 独立重新下载，真实全 **32,862B / SHA256 `b71dfd1244871b3d864621db7f7dc7c6822ac8646ceafb71a8670dfd996688e5` / 40成员 / CRC全部通过**；该包实际含 7 原 NPC 字节文件、24 原 itemset 物理行、8 跨来源候选 PNG、1 派生摘要，未进入 Git。保留旧原包全 SHA 与来源限定，不借此宣称早期官方同服。
- **正式止点 `QUEST16=ACCEPTED_SOURCE_BOUNDED`（历史静态内容层）**。`3000` 原 DAT 同源实物仍待取、原商业 NPC 选支及 14 档实际 GetStone/DelItem 执行仍 OPEN；Stage A 7 PARTIAL+2 OPEN、B/wiki GATED、R79 暂停、总体百分比 null。下一最高 `QUEST17-DEDUP-AND-NEXT-ORIGINAL-SOURCE_FAMILY`，必须先 fresh remote 重查，不从这次提交 SHA 假定未来仓库状态；本验收补记提交自己的 Actions 也需事后查看，不能提前算成通过。
