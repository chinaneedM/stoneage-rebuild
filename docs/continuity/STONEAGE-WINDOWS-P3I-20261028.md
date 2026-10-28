# 2026-10-28 — P3I 原 TW1 独立 DirectDraw 主表面只读探测

## 远端起点与证据边界

本包起点为 main HEAD 7ff9179f5a8eb489e09966117345e007abcd18a4 / tree 58aea40ad72b7c7ab52f92e5c9ec6da5f9530a21；完整 CURRENT Git blob 031c76a5a8e431f646853909bb2f2e11e6328cd2 (2,680,510 B) 不改、不截断。P3H 已直接运行原台湾1.0的未改 EXE，并在已知退出位置点选后原进程正常退出，但两个不同 GDI/Pillow 帧目视只有黑底、IME“半形”和光标，不能认为已见到游戏画面。

**本轮唯一材料问题**：另一条原生显示读出路径是否提供区别于 Pillow/GDI 截图的内容，而不是再讨论客户端文件个数或重复研究论坛。

## 实施与安全范围

自写 x86 只读探测器与原件进程分离；仅当 P3H 原窗口 PID、类名、原 EXE 路径及 640×480 客户区全部资格化后调用。探测器再次校验 PID/类名/客户区，以 DirectDrawCreate → DDSCL_NORMAL → 全局 primary surface → DDLOCK_READONLY|DDLOCK_DONOTWAIT 尝试读出当前客户区对应的 primary 像素及可取得的设备调色板。只记录 HRESULT、几何、区域像素 SHA256、8bpp 索引计数与调色板 SHA；不保存其它桌面图像、原始色板条目或商用图像。不写 primary、不改变显示模式、不注入、不读原进程内存、不运行历史服务端。读出最长 8 秒。

运行环境沿用 P3H 的原375文件 SHA/未改 EXE、外置清单前提、一次性 Windows2025 来宾、全出站临时阻断/恢复任务、原进程一任务一进程 Job、断网前后实际 TCP 拒绝见证及最后清理。原文件/画面与原件观察包仅密封为私人受限工件，公开 Git 不提供原像素、程序或私钥。独立原 source report 和密文工件分开上传以便先验证小报告，避免再依赖早期即将过期的单一大包工件。

**证据限制**：即便独立 global primary Lock 成功并有非零像素，也只是观察到当前设备的 primary 值，可能包含桌面合成器/输入法，不是原客户端独占 backbuffer 的直接读出。还需私下对照实际画面、同源原图和原游戏绘制链才能称游戏有画。Lock 失败说明这一路读出不可用，不能反推出原 DirectDraw 从未渲染。合成红绿/ACP950资格仍非原 GetACP 或原色板证据。

## 验收与停止条件

新增 Python 离线否证门：没有原进程、原窗口身份、配对截图、真实 HRESULT 与完整样本哈希则拒绝；即便可读出，也只返回 PRIMARY_SURFACE_BYTES_READ_GAME_CONTENT_UNATTRIBUTED，绝不宣布已恢复菜单/世界。增加 Windows C 编译门和一次源 Windows 实验。需查验实际 workflow 结果，不能预支绿色。

优先执行一次有界 P3I Windows 实测及独立证据检验。若无法得到有意义的独立原生读出，登记具体失败后停止扩大 WinXP/Wine/驱动/参数树，返回已有同源地图/角色/宠物的现代离线观察者，保留原运行画面与世界入口 OPEN。原 Stage A 九域 7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING，整体完成比例未知。

初始状态：P3I_IMPLEMENTED_SOURCE_ACTION_PENDING；没有声称本包曾实际运行原程序。

## 真实源执行及后验验收（2026-10-28）

原 P3I 专项 Windows source run `40640162726` / job `122656198136` 已实际 completed/success。P3H 的未改原 TW1 程序、三个本次 640×480 GDI 截图、已知退出坐标输入后自然退出 0 以及原件期间出站 TCP WSAEACCES 10013 均有源报告，**不含帐号/密码，未进入世界**。同时独立 Windows C 编译和 Ubuntu 否证 job `40640162911` 均 completed/success。这里“原件执行成功”和“原游戏画面成功显示”严格分开。

实测同一原窗口（PID/类名/640×480 双重校验）第一次采样后的独立只读 DirectDraw 主表面探测返回：DirectDrawCreate、DDSCL_NORMAL、CreateSurface(PRIMARY)、Lock(READONLY) 的 HRESULT 均 `0x00000000`；全局显示表面 **1024×768 / 32bpp / stride 4096**，窗口屏幕起点 (3,26)，限定 640×480 的原生像素摘要 `e76e2132c541303e27bf4653104b7eedf60c393524e6847ed9bcd257c61ce98b`。GetPalette 返回 `0x8876023c`，未获取调色板；32bpp 试验不含不同 RGB 总数或颜色空间分类，不能猜 primary 是彩色游戏图还是黑底/输入法/合成器。三个相邻 GDI 帧的 RGB 摘要依次为 `fce460...a114f0a`、相同、`a469dd...9067d`，均未建立原美术画面。本只读实验**没有读取原客户端私有 DirectDraw backbuffer**。

独立从 GitHub Actions 下载原短期ZIP artifact `12795396156` (4412B)、本地完整SHA256 `d523e095168538938a6229cb81fc954e21a1034e325a07e8d6612f750f3344b8` 与 API digest 相符；解开其唯一 source-report.json 45308B，独立哈希 `be1cc255e05059518d90807f308ee4641700b176545a86ea262406e97ecdf534`，核对上述全部数值与安全状态。另一密封私人包 artifact `12795341341` / 上传工件ZIP digest `ff9c4b71d3fe5c23f923f3c4aa1de689f04270281b497a762ca4d70f84b6de2c` 只记录 CI 上传，**未在本轮声称独立下载大密文或持久私人Library回读**；该CI artifact 7天有效，不应把它当永久原件保管。此前 P3H 原375文件保管记录另独立存在。

上述实测摘要、源/工件哈希、全部证据限制已永久记录为 `research/recovered/STONEAGE-P3I-PRIMARY-ACTUAL-R1.json`；其专用否证检查拒绝假造世界进入、原调色板、原画面或原私有缓冲区资格。Source 通过不是“进入原版世界”。

**P3I 本轮结论**：原程序在原生 Windows 正常创建窗口/退出；另一个只读 DirectDraw 路径可以读到**全局主表面**，但因为没有原游戏私有 backbuffer 读取/身份、没有对应像素的独立视觉鉴真、原版 GDI 图片仍为黑底，本研究无法判定原游戏是否实际绘制，也不能恢复登录菜单/世界。达成有限探测止点，不继续无界扩 WinXP/模拟器/显示驱动。

**下一有效工作**：优先返回已取得并可解释同载体地图真实像素的现代离线场景观察器，补源色板、原SPR/人物及可交互的具名源锚；仅在有新的原生取帧或服务端同源见证时重新打开原游戏真实进入门。保持 Stage A 7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79暂停、overall percent=null。此记录为 CURRENT 的日期覆层；其 2680510B 字节整部旧史原样保留。


### 第二次源动作的实际复测（无画面晋升）

候选归档时 source workflow 的 paths 过滤含新修改的证据 guard，额外触发 Windows run `40640619774` / job `122657646996`，已实际 success；这是一次**重复下载/隔离执行，不能冒充必要新增原件**。它在两个独立一次性 Windows 来宾中的结果一致：真实原EXE主窗口/已知坐标退出均实际成功；只读 primary 同为1024×768/32bpp/stride4096，Lock=0；640×480区域 SHA 再次精确为 `e76e2132c541303e27bf4653104b7eedf60c393524e6847ed9bcd257c61ce98b`。三张 GDI 图片只是前一轮相同两个黑底/IME RGB SHA 的排列变化，没有新可辨认原游戏画面。

这次独立下载第二小ZIP artifact `12794718955`，完整 SHA256 `13c38daa6f36e4cb30c2c2943ea5c87f3747c69eeb8f5c84700b656ca8ffb836`；解开原报告45306B/SHA256 `62b8fa915cb2920460b14439ec8c24290923ff43eaaa6ec82d8bdcf347adb58b`。加密大工件 `12795476155` 只从API得到摘要，未独立下载/持久回读。全部复测源号与两个报告SHA追加至永久机读回执。

**归因警戒**：原P3H旧EXE通过专设`__COMPAT_LAYER=256COLOR`运行，但P3I外部只读探针没有继承这一专设环境；其32bpp是**独立全局桌面主表面**观察，不能当作原进程8bpp设备色板/私人缓冲。即便两次主表面SHA完全稳定也不能证明游戏已经实际绘出美术。至此停止本分支重复原包下载及驱动探测，返回已有同保存源现代离线可视观察与人物/宠物真实图像关联。原版可操作登录、地图/战斗仍需新的独立证据。
