# 2026-10-26 — Win32实际颜色、激活与输入接收门槛 P3D

加法连续性覆层。fresh远端main `a665c26676faf63848bc7b15ced8b9444471fb72`、tree
`7f7eee7afed0a7cf96613347e39c4e3fe9472b56`，最新提交/Actions、596分支及0开放PR
重新读取；同HEAD两收据Actions实际success，无运行中，10-07旧queued37642417333保留。
完整tree5870项未截断、无AGENTS。七启动文件、路线、R102材料portfolio及最新P3C覆层
按真实原生Git逐字节核验；CURRENT2680510B/blob `031c76a5a8e431f646853909bb2f2e11e6328cd2`、
SHA256 `f02f85b837fc09973cb2eca33f7daf4db547a77cb35a81a9576c6308f70142c0`及另外四大
历史文件保留。旧CURRENT/NEXT16不替换较新的观察工作顺序。

## 本包目标与严格止点

P3C原登录画面只有15种RGB、QUIT仅悬停高亮、全屏启动已崩溃。本包先回答**当前环境
能否真的实现8bit颜色并接收鼠标输入**，避免继续盲目重下原盘。交付自编Win32基准、
Wine8/24与当前可用原生Windows的实际比较、来源固定的单配置对照和可重放验收。
**原客户端/商业原资源下载0、执行0**，不模拟原服务器，不将合成色块/点击当原游戏。

`tools/stoneage_p3d_control.c` 是独立自编x86程序，只有已知红绿矩形和256项合成色带。
两条显示路径分别是GDI显式CreatePalette/SelectPalette/RealizePalette及DirectDraw
8bit离屏/调色板/primary Blt。两条输入路线分别是X11派发与Win32 SendInput；只允许
定位本程序专用窗口类，不对原StoneAge类或任意进程操作。

成功判据不是API返回码：GetPixel必须等于预期RGB，独立截图必须各有至少19000个
预期红/绿像素；输入必须在目标程序实际增加WM_LBUTTONDOWN、WM_LBUTTONUP和
GetAsyncKeyState高位按下计数。另记前台/active/focus和清理前真实退出。
DirectDraw调用失败时，即使有残留彩色像素也不接受渲染路径。

API边界依据：Microsoft [RealizePalette](https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-realizepalette)
与[SelectPalette](https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-selectpalette)
描述逻辑/设备palette映射；[SendInput](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendinput)
的返回值只表示注入输入流的数量；[GetAsyncKeyState](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getasynckeystate)
的高位才表示当前按下，桌面/权限状态可能使读取失败。文档提供API语义，不是原TW1源。

## 第一组：三环境六条实际显示路径

HEAD `21f9b608bfb886fe2c3a8ee36c15a0e6ff658ac8`，源40270327324实际success。
原生Windows作业121401553060与Wine作业121401553306均实际编译/执行自编x86程序。
Wine使用Ubuntu24.04的Wine9.0 repack4build3、win32/XP设置、CP950；24bit Xvfb在
程序内报告32bpp。原生环境是Windows Server2022上的32位WOW64程序，**不是32位XP**。

| 实测环境/路径 | 程序色深/ACP | 预期红/绿GetPixel | 独立像素及颜色门槛 | SendInput目标接收 | 原客户端合格环境 |
|---|---|---|---|---|---|
| 原生Windows GDI | 32bpp /1252 | (222,0,0)/(0,200,80) | 各19300像素，通过 | down/up各+1，async+8 | 否，色深/编码未满足 |
| 原生Windows DirectDraw | 32bpp /1252 | 同上 | 各19300像素，通过 | down/up各+1，async+7 | 否 |
| Wine8 GDI | 8bpp /950 | (128,0,0)/(0,128,0) | 未得到预期RGB，不通过 | down/up各+1，async+10 | 否，颜色不通过 |
| Wine8 DirectDraw | 8bpp /950 | (224,32,0)/(0,192,64) | 不通过 | down/up各+1，async+10 | 否 |
| Wine24 GDI | 实际32bpp /950 | 预期红/绿 | 通过 | down/up各+1，async+10 | 否，非8bpp |
| Wine24 DirectDraw | 实际32bpp /950 | 两点均黑 | 不通过，尽管Blt HRESULT0 | down/up各+1，async+9 | 否 |

四个Wine案例的X11派发也都实际收到down/up各+1，async分别13/13/12/13；不是只看
xdotool return0。所有六例前台/active/focus都匹配、程序在清理前正常结束。上述轮询
次数只是本次按住期间采样数，不是原游戏帧率或历史输入时序。

FACT：默认Wine8中，显式GDI及DirectDraw的实际颜色仍量化；故P3C不是“只需换截图工具”
即可关闭色彩问题。FACT：自编接收器可接收两种输入路线；不能把P3C原QUIT失败一律
归因X11没有发出按键。OPEN：原游戏自身激活/输入状态仍未测到，不以合成接收器替代。
末次RealizePalette返回0不代表它从未映射，仍以实际RGB和独立截图为准。

原生Windows正常显示/输入的结论只限定两个自编路径及当前桌面。其ACP1252/32bpp
不足以认证原TW1可用，未向该原生runner放入或执行任何原商业程序。

## 上游Wine9来源与单配置假设

实际读取Wine上游tag wine-9.0并固定到commit
`fd1153552d779e1ac14b0b1c48fbd1cde894eb0a`。按Git树取得两文件blob，与完整源内容
重新计算的Git blob相等：palette.c `43974fe88963ca70901af879a101b1f08f45d707`，
x11drv_main.c `d1f31081b09de9ee2168997398a2979111c33851`。
来源元数据见 `research/recovered/STONEAGE-P3D-WINE9-CONFIG-SOURCE-R1.json`，不向本库
复制上游代码。它是Wine上游9.0来源，不能假称Ubuntu repack没有下游补丁。

[x11drv_main.c](https://github.com/wine-mirror/wine/blob/fd1153552d779e1ac14b0b1c48fbd1cde894eb0a/dlls/winex11.drv/x11drv_main.c)
的默认private_color_map为FALSE，并读取X11 Driver下PrivateColorMap配置；
[palette.c](https://github.com/wine-mirror/wine/blob/fd1153552d779e1ac14b0b1c48fbd1cde894eb0a/dlls/winex11.drv/palette.c)
在PseudoColor分支为该选项创建AllocAll私有色板。HYPOTHESIS：只改变REG_SZ
PrivateColorMap=Y可能改善Wine8实际映射；必须先重启旧图形进程并用相同合成程序验证，
不根据注册表设置成功就声称原色已恢复。

## 首次配置对照在重启守卫停止

HEAD `41b4cab201190e268b1c4093ad2f90c2da5e4697`，源40270852795/job121403129834
实际failure，清理与派生工件上传success。JSON cases为空，probe_error为
`old Wine graphics processes not retired`；尚未执行配置后的两个控制路径。
原样报告和包版本保留为 `STONEAGE-P3D-SYNTHETIC-FAILED-PRIVATE-*`，不当配置无效结论。

首守卫要求wineserver -k/-w都返回0，未保留各返回码或实际存活进程。修订为完整记录
两返回码，并在本隔离PID树内检查活着的wineserver进程，区分僵尸和已退出状态；只有
实际无活服务器才允许新控制器启动。另收紧PrivateColorMap查询为准确REG_SZ/Y匹配。
Wine上游[server/main.c](https://github.com/wine-mirror/wine/blob/fd1153552d779e1ac14b0b1c48fbd1cde894eb0a/server/main.c)
中kill/wait选项也有不同退出语义，不能把退出码替代进程观测。
修订版的实际配置对照结果在下面追加，旧失败报告不改。

## 保管和全局边界

原样JSON、包版本、源HEAD/run/job/ZIP/API摘要及派生Git blob链永久记录于
`research/recovered/STONEAGE-P3D-SYNTHETIC-CUSTODY-R1.json`。不把短期Actions工件过期
当作原样派生证据丢失。合成画面没有原商业资产；工件仍只保留测量元数据和版本。
原Windows runner网络未隔离，报告明确该事实；因为这里只有无网络调用的自编程序，
没有原客户端执行，不把它宣称为已经隔离合格的原游戏执行环境。

R20同版名字—实体ID—SPR新增0；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、
overall percent=null。原登录颜色/点击、真实音频与世界仍须原程序单独验收。

## 修订对照：重启可证，但PrivateColorMap单项未解决颜色

HEAD `d83d792362166c55f8620135719cfb333520d953`，源40271128536/job121403967818
实际success。报告实测kill return1、wait return0，存活wineserver PID为空、server_absence
为true；因此先前将kill1当作仍有活服务器的条件不成立。PrivateColorMap严格回读为Y，
新控制器在旧服务器已退出后启动；配置实际测量与旧失败报告分开保存。

GDI仍为(128,0,0)/(0,128,0)，DirectDraw仍为(224,32,0)/(0,192,64)，两者与基线
相同，独立捕获仍不含预期红/绿足量像素。SendInput接收down/up各+1、async分别10/11；
X11接收down/up各+1、async均13，前台/active/focus均匹配。该单项配置的改善假设在本
合成范围内未成立；不能扩大为Wine所有版本/配置、原客户端所有显示路径都不可能。

三轮源作业产生四个ZIP，均已实下独立校验：

| 工件 | 字节 | ZIP SHA256 |
|---|---:|---|
| 12628725347 原生Windows | 1911 | 843931cc7084e93912487a92b4cca179825ed18792f412ecfb151134ce2c8724 |
| 12628171401 Wine8/24 | 6468 | 4198b6bc8fe30b5a411c4a1d800a70066f1d24786e9ff8a96bf0cb1b8524db08 |
| 12628232004 首重启守卫失败 | 959 | 94dbd96cd205a7b29e3e2964b8913dc38abde634b79d807a177f62943debe39d |
| 12628522174 修订配置对照 | 4227 | 1db9c5328703dfb41dcf8e489c405e56c461e55c8e2fb41819ee905a54e96262 |

8份原样JSON/包版本永久保管，实际八个完整路径测量中3条颜色通过、5条不通过，8条
SendInput接收通过；所有原客户端完整前提都未通过。基准正常结束不是原游戏修复。

本地首个保管链重放将跨平台控制源SHA强行视为一值，拒绝了Windows报告；查实是Git
checkout的CRLF与Linux LF差别。把当前9582B规范源精确转换为CRLF后，SHA恰等于原生
报告的ef4d…，Linux源为809599…；两值各自固定，原报告不改。这是本地保管链条件修正，
不是远端源作业失败、控制算法差异或重新编译后冒称原报告。

## 最高NEXT及避免重复工作的边界

最高NEXT `ORIGINAL-GAME-OBSERVATION-P3E-AVAILABLE-WINDOWS-8BIT-QUALIFICATION`：只做
一个有限的可用Windows显示/编码资格包，先查当前原生runner可枚举的色深/兼容模式和
CP950可用条件，再用同一合成颜色/实际输入门槛验证。当前Windows32bpp/ACP1252只证明
自编显示/输入可用；不把更改console codepage当GetACP已变950、不把兼容复选框当实际
8bpp已生效。还须独立验证Windows原进程无外连的隔离措施，不能照搬Linux namespace
结论；不得向未通过前提的环境重拉/运行原件。

若不能取得同时满足8位显示、正确合成RGB、CP950和输入接收的环境，则将原观察暂列
明确环境阻塞，回全22域的原内容R20材料队列；未来只有新的合格环境/真实源可重开。
不在相同Wine9组合中连扩PrivateColorMap/所有GDI/DirectDraw辅助树，不以通过测试、
累计R号或耗时计算复原百分比。本包止点是**可复核的兼容环境判定**，不是原画/原
点击/原游戏世界验收。

## 实际主线终验

内容main `d7fc426a2dea00ee65f705762bc36231a5ce816f`、tree
`3d2afffb297270a156c06638574bf4c263aff2c2` 已非强制快进发布。候选五项及同HEAD主线
六项Actions均completed/success。专用P3D候选40271727303、主线40271806839实际执行
17项不同测试与8份原样派生/失败边界精确重放；主线另有P1、R16/R17/R18和Stage A
兼容成功。离线CI不再运行源控制器，更没有运行原客户端。

21内容路径与远端逐字节一致，包括原生JSON原样CRLF；完整CURRENT及另外四大历史
文件原样保留。[永久发布收据](../../research/recovered/STONEAGE-P3D-SYNTHETIC-PUBLICATION-R1.json)
保存全部候选/main运行作业、内容SHA/blob、三源/四ZIP链接及未解决状态。源失败与本地
跨平台行尾校验修订均未抹去；收据自身CI须发布后实际查看，不预写成功。最高NEXT仍
P3E有限Windows资格检查，未通过则按上节止点返回R20材料；原游戏边界不变。
