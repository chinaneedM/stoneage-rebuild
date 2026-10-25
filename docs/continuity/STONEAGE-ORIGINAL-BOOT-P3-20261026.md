# 2026-10-26 — 原TW1客户端隔离启动与第一屏取证 P3

本记录是加法连续性覆层。启动重新读取GitHub main
`8e98189f4bf6f0bbc4f55225c8c766b5b27e121b`、tree
`4ac70628eee1f43452c33fb4eb084298973ed0d2`、最新提交及Actions；同HEAD
40242023407实际success，0开放PR，旧10-07 queued37642417333保留。七启动文件、路线、
portfolio及P2B覆层按真实远端读取。完整CURRENT仍2680510B、blob
`031c76a5a8e431f646853909bb2f2e11e6328cd2`、SHA256
`f02f85b837fc09973cb2eca33f7daf4db547a77cb35a81a9576c6308f70142c0`，
不截断或覆盖；旧历史/NEXT由本日期记录有界接续。

## 本包交付、原件和止点

目标是**实际运行同SHA台湾1.0原客户端，并取得可目视的第一屏证据**。P2B只有限执行原
初始化指令，本包已运行完整 `sa_3.exe` 映像。它不自动证明登入原服、世界地图/宠物/NPC
显示或原音频体验。暂不扩mock服务器、登录协议或现代引擎。

FACT：认证原盘中375个非安装器运行文件、372529095B，每文件尺寸/SHA256与既有原清单
blob `564233902b10c60760d4f93b1ea65d4dd1469206` 一致，包含原图、声、动画、战斗资源。
8个installer_support成员不执行。固定源程序 `StoneAge/sa_3.exe`425984B，SHA256
`cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a`。
源基线保留，另复制运行目录；结束再次核全部原输入未变，运行副本既存路径无内容变化。
这不是新增客户端版本，也没有补入后期资源、破解程序、旧驱动或服务器数据。

实际启动参数为：

```text
updated realbin:1 adrnbin:1 sprbin:1 spradrnbin:1 soundbin:1 battlebin:1 windowmode IP:0:127.0.0.1:9
```

`updated`、资源bin开关和windowmode来自既有同版启动器静态证据及原说明，参见
`research/clients/STONEAGE-TW10-SERVER-SELECTION-LINEAGE-R1.md`；原解析器的
`IP:0:host:port`形态另核。**127.0.0.1:9是无人监听的合成实验端点，不是历史地址或
已恢复服务器**。没有点击登录、发送实验握手或输入账号。

## 可复核的实际隔离与显示前置

本地Ubuntu容器缺Wine/Xvfb，实际执行在一次性GitHub Ubuntu24.04 runner。Wine9.0
32位前缀、XP兼容设置、zh_TW.UTF-8/ACP950；Xvfb800×600，具体包版本原样保管。
Wine设置不是在真正Windows XP/原硬件上复现的声明。

下载前先编译并运行独立Win32合成控制，确认32位、窗口、GDI捕获、DirectDrawCreate/
SetCooperativeLevel/8bit offscreen/CreatePalette/SetPalette各HRESULT0。24位Xvfb的原生
GetDisplayMode实际报告32bpp；**离屏8bit面可创建不代表当前显示8bit**。后续独立8位
Xvfb控制GetDisplayMode才报告8bpp；控制图非均匀，但8位控制的GDI颜色不是已验原色。

每个控制/原程序及其子进程均在新 `unshare --net --pid --fork --mount-proc` 树中。
硬门槛核host/child网络namespace不同、仅lo、IPv4无路由、IPv6无默认路由、对文档地址
192.0.2.1:9的连接负控返回ENETUNREACH101，任何门槛不符均停止。未仅靠Wine配置或
将目标写成loopback就声称无外连。网络namespace语义参见
[Linux network_namespaces(7)](https://man7.org/linux/man-pages/man7/network_namespaces.7.html)。
源获取发生在隔离执行前的宿主步骤；不把该下载网络说成原程序外连。

## 首轮不足与三次原程序实跑

| 次序 | 源HEAD、运行/作业 | 实际结果与限制 |
|---|---|---|
| 初环境 | 305504fcb5736b90b0a3212dc4af3b7885200454；40242697734 /121317724459 | 重型Wine32+64安装未完成，后由精确run+HEAD+branch守卫取消。prepare取消，控制/下载/原程序步骤skipped，清理success、无报告导致工件upload failure；整体cancelled，不是原程序失败或成功 |
| CP950及原启动参数 | d4d06d68d4dd00af50deaaaac2c665c849913ab8；40243539952 /121320241275 | 实际success；原main窗口及“請使用２５６色的顯示模示”模态框，未通过显示模式要求 |
| 真8bit显示 | b7b7bc1dcc41283e4b0b5f4c8792b0696264a6f1；40243866398 /121321234490 | 实际success；独立8bpp前置通过，三采样只有原main窗口，256色模态框不再出现 |

初源代码也曾遗漏 `updated` 参数，但因安装未完成而从未运行该裸参数客户端。不能将
纠正前版本写成已执行。后改用仅Wine32的较小环境、明确原启动开关；取消权限只针对
该已核HEAD的旧任务，不处理不相关旧queued任务。失败/取消历史不改写。

Win32检查器通过QueryFullProcessImageNameW核窗口所属实际映像
`Z:\\tmp\\stoneage-p3-original\\run\\sa_3.exe`，原main类/标题均为全角
`ＳｔｏｎｅＡｇｅ`，外框[0,0,646,512]。24bit三采样是2窗×3次=6次窗口出现；
8bit是1窗×3次=3次，均是单次启动，不是多个客户端。采样累计约3/10/20秒。

24bit像素RGB SHA256 `3328b78dae4f33e5e063d219403764bc4a3f845d49378e93a11c27159104740c`；
8bit三次相同RGB SHA256 `80af99c48cb3c7c3010446da6d95f9d14e176a8a7784a79afb1e51dd1eece190`，
PNG SHA256 `8d7a9594292e262615c187d2fd21504b3b0f71a4d02e8c9a31811af53f460cc0`。
非均匀像素和原窗口足以证明执行/捕获，不足以证明游戏场景正确出帧。

原始自动报告中的 `preflight_passed=false` 在原程序独立调用中表示该调用不是合成
控制分支；同一作业的前置控制在另外JSON中实际true。所有原自动报告目视/世界/听音
字段仍false，不能为追认后来人工观察而篡改原JSON。

## 来源保管与独立验收

`research/recovered/STONEAGE-TW10-ORIGINAL-BOOT-P3-CUSTODY-R1.json`固定每个源HEAD、
run/job、工件ID、ZIP摘要、原样报告字节数/SHA256/Git blob；三个实际成功源的报告均
按工件原字节保管。只存派生元数据和环境版本，不放商业原程序、原图、音频或完整包。
工件短期过期后仍可核公开原样派生。完整原盘私人长期保管仍未配置。

`tools/stoneage_p3_boot.py`是源文件资格/隔离执行工具；
`tools/stoneage_p3_control.c`是自编合成控制与只读窗口检查器，不能替代原程序；
`tools/stoneage_p3_private_frame.py`仅把一张原截图以会话公钥封装，私钥在公开仓库外；
公开工件只有X25519/HKDF-SHA256/AES256GCM密文，原PNG在runner结束清理。
接收端验证GCM、原PNG完整SHA及报告帧位置后才能本地解密目视。密文与公钥不作为
复原原资源的分发接口，公钥不含会话私钥。

独立 `python -m tools.stoneage_p3_evidence_guard` 核原报告保管、实际窗口映像归属、
24bit错误/8bit无模态框、原exe/参数/原输入、合成与原程序分界、世界/音频未知；
语义反例直接改报告内容，绕过摘要也拒绝外网接口、外部端点、假窗口归属、32bit显示
伪称8bit或执行证据提升为世界/目视。离线CI不再次下载原件或执行原客户端。

## 未完成范围

原源报告只证明原程序已运行、可见主窗口和显示模式纠正；第一屏内容的人工观察结果在
下面单独追加。按钮/输入、登录请求、音频播放和服务器场景仍未验，不把未出现模态框
等同原登录或游戏世界已恢复。

内容线 `EARLY-OFFICIAL-WORLD-ENTITY-SOURCE-20` 同版名字—实体ID—SPR新增0，仍OPEN。
Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING、overall percent=null；
DD-028本体/永久新增/运营活动/起源待考四档和全部旧证据保持。

## 最终私人画面的实际目视结果

第四个源HEAD `893a96a903169e94d2f882f4af9d58259ae4e1d2`，运行40244430667 /
作业121322896143实际completed/success；重复相同8bit原启动只为取回一张可目视帧，
不算新版本或新世界内容。工件12618127255的ZIP21364B，SHA256
`15e1d0006adf134c3c1274dcfeac35d5a117f8ffc600941a999da598ed15845a`已下载独立校验；
5成员是3报告、包版本、单张帧密文。密文封装SHA256
`d7d323207dd1f66a68122b9c4f03932bd0024e10f21d2aeae10db3684d3eaebb`。
在私人路径认证解密的原PNG15972B，完整SHA与源报告第2采样（从0计为1）一致，
也与前一8bit源的PNG/RGB完全相同。公开Git永久保留11个原样元数据/版本文件，
**不保留密文封装、私钥或原PNG**。该单帧已另作私人保存，完整原盘的持久保管状态不变。

FACT（2026-10-26人工目视）：助手已查看该原程序截图。可见Presented by、
JAPAN SYSTEM SUPPLY、石器時代标题、會員帳號/會員密碼输入区及OK!/QUIT按钮，
背景中有原角色图形。**可以认证原客户端实际显示了可辨认的登录面板**；此前P1/P2
离线解码图没有被拿来充当这张截图。

FACT（画面缺陷）：当前背景/角色主要是黑白和点状纹理，保留少量黄/红色。正确色彩
渲染未通过，不能将“有原登录图”升级为原色画面还原。HYPOTHESIS：可能在当前8bit
显示的palette应用或截图对colormap的读取环节；尚未定位，不能断言是原游戏资源损坏。
三采样相同仅表明此时间窗画面静止，不代表原游戏本来没有动画。

无账号/密码输入、无按钮操作日志、无声音听取/录制，无世界地图/宠物/NPC观察，无
原服握手。人工后验单独写入custody，原自动报告中的目视false保持原字节。

最高观察NEXT：`ORIGINAL-GAME-OBSERVATION-P3C-LOGIN-COLOR-AND-INPUT`。有限目标是
区分原DirectDraw画面与Xvfb捕获的palette/colormap误差，取得颜色合格的同源登录截图，
并在隔离无服务端条件下记录一次无账号按钮或退出输入反应。先利用本包原报告和同源
palette事实提出可证伪方案，只在实际取证需要时重取原件；不连扩全部DirectDraw helper。
若Wine8bit路线无法合格，记录精确停止点后比较可用的32位Windows隔离环境，不能继续
用元数据测试替代可看画面。P4回环协议和原历史实体R20仍是独立未完成门槛。

## 本轮主线实际终验与下一步依据

内容HEAD `d9ca4e65bb82001a6027d2cfe74c1a01b4847967`、tree
`f3a6e3df3a3f0ce24c648fc33e774c56fd9cdfae` 已非强制快进main。最终候选五项与
同HEAD主线六项Actions全部completed/success；P3候选40244819800（离线作业
121324049584），主线40244867372，核15个不同测试及独立原样源保管/语义guard。
主线另通过P1离线兼容、R16/R17/R18、Stage A。没有用主线离线CI冒充重新运行原程序。
25改动路径与远端逐字节一致，五个大历史文件原样保留。

[永久发布收据](../../research/recovered/STONEAGE-TW10-ORIGINAL-BOOT-P3-PUBLICATION-R1.json)
保存全部候选/main运行作业、25内容文件摘要/blob及观察边界；源run/job/工件/ZIP/11个
原样派生指纹由其链接的custody保存。收据自身CI须发布后实际观察，不预写成功。

P3C最先应测试的有限假设已有负控依据：两个8bit合成控制的root截图均报告G/B通道
全0、预期红绿计数都0，尽管Win32绘制/DirectDraw调用成功且24bit控制实际捕获各14400
红/绿像素。因此**现有8bit root捕获本身尚未通过颜色保真验收**。下次先比较对应窗口
colormap的捕获与root取色，区分捕获误读和原显示palette错误；这是调查假设，不是
已定位Wine或原客户端故障。无需先改原素材、重跑P2静态解码或扩展服务器内容。
