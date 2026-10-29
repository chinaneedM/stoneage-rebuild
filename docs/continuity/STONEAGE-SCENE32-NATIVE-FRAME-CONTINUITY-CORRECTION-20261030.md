# SCENE32：原生画面旧证据复核与重复待办纠正

2026-10-30（Asia/Shanghai）。加法覆层；原CURRENT、SCENE31原记及P3H/P3I所有原始报告不改。本包结果是**纠正重复待办、保留准确运行边界并重排进入世界的工作路径**，新增历史图像/原件执行/世界内容均为0。

## fresh remote 与本轮范围

启动重新读取 main `57523f59070898905fb552ceec17979032fa8dfe` / tree `0883e7e92aca15757d46c7be7a0ab1958eaa8aa5`、679远端分支、最新提交和Actions、0开放PR，七启动文件/R2/22域/R102及最新SCENE31覆层；上轮收据40969843329实际completed/success。原本地worktree的父Git目录已丢失，未据残留文件推断状态，另从远端main建立新干净checkout并逐文件与Git核同。CURRENT2708031B / blob `20050acf279a01555ab06a381dfcdc936bd381a6` 全文保留；README旧120552B全文作为追加前缀。

SCENE31最高NEXT要求认证并查看P3H三张保留图，理由是原source report的 `assistant_viewed_original=false`。本轮重新读完整P3H连续性后记、独立VISUAL-REVIEW及P3I后验时，发现这个理由遗漏了**后来的独立目视记录**。

## 明确纠正 SCENE31 的待办判断

**SCENE31将“原报告的当时未阅图标记”理解为“这些图至今未阅图”，是不完整的续接判断。** 原P3H报告保持false是保存现场历史，不应回写原报告；2026-10-28独立后记已实际看过0、1两张图，帧2与帧0字节完全相同。该任务已经有限完成，不能再把阅同一三帧报成新恢复成果。

原review：`research/recovered/STONEAGE-P3H-VISUAL-REVIEW-R1.json`，2806B / SHA256 `5f279c2d4b931e2caa02beab87c31fa85bdb420e3554e89876895ecf9bcea050` / blob `a10d57310f489d511cf467f719ccc267f47a7a8f`。它明确绑定原source report SHA256 `d4417e3b4f415ff18fc816bcd556311da4ca44885e62ab03746c027c6c5615ea`，不是无来源聊天评论。P3H连续性文档的“黑屏原图的独立核对”早已记录97/104/97个非黑像素及止点。

新窄范围否证程序把原source、后续review、P3I按整SHA联接；拒绝删除后记、回写旧false、换同名帧、丢重复位置、以nonuniform或global primary Lock成功冒领游戏画面/原私有缓冲/世界。独立PNG读出只为此次来源交叉核对，不扩展成通用图像或渲染框架。

## 本轮实际原字节核验

既存P3H包从私人保管回读，372626292B / SHA256 `3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24` 全件认证。没有重新下载零售盘、重新运行原EXE、登录或联系历史服务器。包内private-source-report.json41836B / SHA `d5b2ddbc82512f72531f46a6277cb8f1d064533055002779bcd0a0f1b4a453df` 认证；它的全部共有字段与公开P3H report逐语义相同，公开报告仅另有三个保管元数据字段。

三PNG逐整SHA/CRC核对；标准库实现独立检查PNG chunk CRC、RGB8/非交错、受限解压与五种行filter，与Pillow全部RGB逐字节相同，重新计算的像素统计与2026-10-28 review完全相同：

| 位置 | 原PNG字节 | 黑像素 / 307200 | 非黑像素 | 不同RGB数 | 原PNG摘要前缀 |
| --- | ---: | ---: | ---: | ---: | --- |
| 0 | 1122 | 307103 | 97 | 2 | 8d96c6a83c52 |
| 1 | 1135 | 307096 | 104 | 2 | e2b64be9da9a |
| 2 | 1122 | 307103 | 97 | 2 | 与0全字节相同 |

本轮再次实际打开0、1图：黑底、右下“半形”和一处光标，没有可辨游戏背景、角色或菜单。仅为重复原证据的校核；不称三幅新游戏截图。原ANSI GDI文字、正确色板及私有backbuffer原因仍未知。原PNG已经保存在原P3H私人包，不另造一份新的截图交付，也不将原图入公开Git。

## 整体运行证据必须分开

| 既有环境/记录 | 已实际建立 | 未建立 |
| --- | --- | --- |
| P3C Wine窗口模式 | 原客户端曾显示可辨登录布局、角色/标识；出现过悬停反馈 | 原正确色彩、点击后正常退出、登录和世界；不能说从未见过任何原界面 |
| P3C Wine默认全屏 | 原窗口与调试器/崩溃现场 | 本场景的合格QUIT测试；不得把后续点击说成崩溃原因 |
| P3H 隔离Windows | 未改原EXE启动、所属640×480窗口、已知坐标点击后自然退出 | 本次抓图中的游戏美术、菜单和原世界 |
| P3I 两次只读探测 | 全局primary Lock成功、32bpp区域摘要 | 原客户端私有backbuffer、原8bpp色板、原游戏画面归属 |
| SCENE离线观察器 | 有来源的原图/地图候选、现代控件 | 原客户端实际执行、官方同服和原世界进入 |

P3C的取色/输入/崩溃限制来自 `docs/continuity/STONEAGE-ORIGINAL-LOGIN-P3C-20261026.md` 全文；本轮没有重新读取其私人图片、没有新P3C目视或运行。P3I实际永久报告 `STONEAGE-P3I-PRIMARY-ACTUAL-R1.json` SHA `1272e5639907ab5687475ed8a57082737d1aa2d2f5fac459b0f93e9a01fe7bd8`，明确止于 `PRIMARY_SURFACE_BYTES_READ_GAME_CONTENT_UNATTRIBUTED`；旧两次源执行与重复下载记录都保留。本轮同三帧不是重开驱动/WinXP/Wine参数/原生surface支线的新实物触发条件。

## 下一最高：SCENE33-WORLD-ENTRY-SOURCE-PAIR-FEASIBILITY

回22域，将“实际进入并观察游戏”作为优先目标；停止继续扩此人物动画或重复黑屏。下一限定一次**已有客户端—服务端实物的配对资格核查**，不先建另一个观察器，也不预报可以进入：

1. TW1官方历史基准与缺失同版服务器保持一条路线；已有M/MC机制和后代数据不能补造官方世界。
2. 另一条仅作为后代/社区可玩参考候选：既存mixed25父RAR361255180B / SHA `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`。从其现存保管实物有限取**服务端readme、gmsv/setup.cf、saac/acserv.cf及两可执行文件的静态身份/依赖/启动入口**，给出是否存在可在隔离本地运行的成对材料及最小缺件。
3. 原档案清单blob `78e8260e89928df76513799511d45c14a9e24dfc` 已记录 gmsv.exe SHA `d5b08dbcbf9e8736ba8598e38e5901f123d2bff544a9cae53a9ff88ce1971e00`、saac.exe SHA `299910efe3d04ccf83a224a6f670c9fabe379440df36d6e0bf6514d76c834615`；这是文件级线索，尚未证明启动/配对。R18的“完整server source”实际保全的是2245个gmsv/data文件，不含这里的顶层可执行/启动配置，不能拿R18标题假称完整可运行服务端已经验过。
4. 客户端sa_2903.exe SHA `ec678517f76564ebc9ab00cf3f66853ed9975ef6290eb48168b78909a68a5d16` 在既有Assessment已列为 **C / MIXED-MODIFIED**、带固定外部端点和社区改动标记，只能作为有版本限制的参考候选，绝不晋升TW1官方或干净客户端。不得仅因同一RAR就认证同一部署或自动运行。

交付是一张候选配对/可用依赖/缺件/版本归属/下一最小实验表。有真实材料和明确隔离方案才考虑后续受限运行；原配置不能当可信执行指令，不使用真实账号、不接旧公网端点、不把模拟协议或后代世界称为早期官方世界。缺件则具名停止，本包只占一轮，不转无限安装器/驱动/参数辅助链。

## 验证与保管边界

15项新原报告/后记/P3I联接和合成PNG反例本地通过；公开CI不读原私人图、不重跑原EXE。本地源核对收据永久记录为 `STONEAGE-SCENE32-ACTUAL-PRIVATE-FRAME-AUDIT-R1.json`，联接与纠错为 `STONEAGE-SCENE32-RETAINED-NATIVE-FRAMES-R1.json`，均仅派生数值/哈希。真实候选/主线Actions另据后验记录，不能把旧success算作新执行。

原版世界仍未进入；Stage A 7 PARTIAL + 2 OPEN、Stage B/wiki GATED、R79暂停、overall_percent=null保持。本轮无新增历史内容；实质结果是排除重复工作及防止错误的画面/运行晋升。
