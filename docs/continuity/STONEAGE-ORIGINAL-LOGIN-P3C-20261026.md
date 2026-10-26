# 2026-10-26 — 原TW1登录窗口取色与有限输入 P3C

本记录为加法连续性覆层。fresh GitHub main
`512a7b5399b7236befad9a512f1a56e8ebc5bf04`、tree
`63b79b03ff75b941c81f0e2fde30c6ba0978d90f`，最新提交/分支/Actions重新读取，
同HEAD收据40244965090实际success，0开放PR。完整远端tree5847项未截断、无AGENTS；
七启动文件、路线、R102材料portfolio及P3最新覆层均以原生Git完整字节核对。
CURRENT2680510B/blob `031c76a5a8e431f646853909bb2f2e11e6328cd2`、SHA256
`f02f85b837fc09973cb2eca33f7daf4db547a77cb35a81a9576c6308f70142c0`及另外四大历史
文件保持原样；不从旧聊天或CURRENT较旧NEXT16推断当前任务。

## 交付范围与可证伪问题

接P3实际原客户端登录第一屏，本包只解决两个玩家可观察问题：**颜色为何失真，以及
鼠标输入是否真正被原程序响应**。同版TW1原SHA程序/375运行文件、Wine32/ACP950、
实际8bpp显示、独立网络namespace仅lo/无路由的资格保持。原exe/原资源不改，合成
127.0.0.1:9无人服务端，不输入账号/密码，不模拟登录或原服世界。

旧P3的800×600桌面root截图可辨登录布局，但主要黑白/点纹；8bit GDI红绿控制也未保留
预期颜色。此前只提出palette/colormap假设，未认证原素材损坏或Wine具体故障。
本包用原窗口自身colormap重取640×480客户端像素，并对同一索引另套默认colormap作
负控；不以P2离线原图、重着色后期图或生成图替代真实客户端画面。

## 捕获方法及独立颜色控制

新增 `tools/stoneage_p3c_xcapture.c` 用XGetWindowAttributes取得深度、visual和窗口
关联colormap；XGetImage/XGetPixel读取索引，XQueryColors查询每个实际像素号的RGB。
使用Xlib的像素访问接口，避免自行假设stride/byte order。仅支持本包8bit PseudoColor、
可见窗口、受限尺寸/数量；原PPM/索引/768B palette只存在公开Git外的临时目录。
公开JSON只存尺寸、窗口/colormap ID、指纹和已知合成颜色计数。

API依据是[X.Org Xlib规范](https://xorg.freedesktop.org/archive/X11R7.6/doc/libX11/specs/libX11/libX11.html)
的Window Information、Querying Colormap Cells及XGetImage章节：窗口colormap与默认
colormap不能无条件混用；XGetImage的可见/遮挡限制仍适用。本包无人交互覆盖原窗口，
不将所得软件显示帧称为原Windows硬件色度/所有显示模式的复现。

在取原件前，原生X11私有colormap控制用索引42/99画320×160两半：各25600个已知
RGB(222,0,0)/(0,200,80)。正确窗口colormap能逐项计数，默认colormap解释同一索引
的RGB不同，X错误0。该控制没有游戏代码/图像；它验捕获算法，不是原游戏运行证据。

Wine8bit GDI控制另保存：直接绘制的任意红绿RGB没有通过精确颜色计数，
`wine_known_rgb_preserved=false`原样保留；不能把“控制图非均匀”叫作颜色保真成功。
原生X11已知色控制与Wine/GDI/DirectDraw的调色板管理属于不同门槛。

## 首次真实源：取色更清楚，未退出

HEAD `5f0f44d57b6018fca7730ca6ff43591bd3f12ea8`、tree
`7f5f3154c1f5aea9a3e385dea2235ba19150fd55`，源40246202271/job121328176262
实际success；不是原客户端功能全部通过。工件12618348824、ZIP243444B、SHA256
`58ef498127a4e939fd2c702f48e77a5a3afbaa10176e75002c49525b3e464586`已实际下载独立校验。
7成员是四派生/包版本、旧root帧密文、输入前后两张窗口帧密文。原样四文件永久保存为
`STONEAGE-TW10-ORIGINAL-LOGIN-P3C-INITIAL-*`，不改写为后续成功报告。

FACT：640×480原窗口XID8388609使用colormap10485761，默认32，map_installed=false；
同一索引SHA `7cbcb73d00d99ad61ab87fc1ff176c48f3ae7ab915cd1fad6cf3d8ca82af8921`，
窗口colormap RGB SHA `492bb90698518fa79e8a14677b26ef6717a483f12bdfdbed1914886d1b6a4fc1`，
默认colormap RGB SHA `a73bb766fadf30c8a34fc5035fdb852cb340b42ab71a3496b04c2a5c8e6f8d96`。
这些ID是该次运行的临时值，不当历史资源ID。窗口palette SHA
`c21c2c6723dcf829af3b83725556fd689a1e024d0b116c4089b88f93f47809cb`恰与该轮Wine
GDI窗口palette相同；不能宣称它等于原P2B的Palet_0初始化768B SHA。

FACT（人工目视）：登录背景、角色、JSS/WGS标识比旧root帧清楚，但仍明显浅色/抖点，
正确色彩未通过。两张原帧均认证解密后查看，输入前PNG SHA
`dd69f0a57ea38d102dc1afa4fec78d44371471140f2b7e18a5e16e3bd4d5e23f`/108680B。
移动到先前已认证QUIT位置(350,410)并单次短点击后，QUIT由灰底/灰字变成白底/黑字，
说明**鼠标悬停的可见反应**已发生。短点击命令return0，但原窗口仍在、launcher仍运行，
`exit_observed_before_cleanup=false`。输入派发成功不等于游戏退出。

HYPOTHESIS：无窗口管理器的Xvfb尚未使Wine窗口获得所需激活/调色板状态；短按键也
可能未被旧轮询采到。下一次有限对照仅增加XSetInputFocus和200ms单次按住/释放，
不改原程序/资源、不手工套用原SAP或插桩替换DirectDraw。

## 焦点/按住对照：两个简单假设不足

HEAD `0e5ab68a3bf145d3ccaa862b469d0a8ea8f41f30`，运行40246551708 /
作业121329227817实际success。ZIP工件12618912936、243567B、SHA256
`c191ced0260069dbe5b8a3b152344966fea39f7028d60bce447ed6d26aa2a671`已实下校验。
四原样派生另存 `STONEAGE-TW10-ORIGINAL-LOGIN-P3C-FOCUSED-*`。

XSetInputFocus经xdotool派发return0，原640×480窗口仍map_installed=false，
palette摘要仍c21c…，焦点前后不变。200ms左键按住/释放各return0，原main窗口仍在、
launcher仍运行，清理前退出false；不把finally清理杀掉Wine算成QUIT成功。
该源也再次核375/372529095B、全部原文件SHA一致，原输入未变、既存运行副本无变化。

首次输入前PNG实际只有15种RGB；这是图像像素计数，不等同“原游戏设计只有15色”。
窗口自身colormap读取解决了一层错误解释，但XSetInputFocus与延长按住未使其取得
已证正确的完整原色/退出。此结果否定“只需这两个操作即可解决”的简单解释，不穷尽
原Win32激活、DirectDraw、输入采样或Wine兼容原因。

因此增加一次**原程序默认全屏路径**比较：保留全部已证启动开关，仅去掉原可选
`windowmode`，Xvfb从一开始设640×480×8，不给原exe打补丁。QUIT坐标按已经目视的
640×480客户端帧取(350,380)，不是沿用带窗口偏移的root坐标(350,410)。这次仍只
一次200ms输入、不填账号，不从“命令派发return0”预支程序反应。结果另在下面追加。

## 证据保管与边界

各轮实际源的原样派生及ZIP/报告/Git blob链由
`research/recovered/STONEAGE-TW10-ORIGINAL-LOGIN-P3C-CUSTODY-R1.json`保存。
私人原PNG经X25519/HKDF-SHA256/AES256GCM传回，先核密文/原PNG完整SHA再目视；
公开工件只有密文，公开Git不保留原图/索引/完整palette/私钥。完整原盘私人长期保管
仍未配置，不因保存单帧而声称全部官方客户端已长期存妥。

独立guard核原样保管、已知RGB与错误colormap负控、Wine控制实际结果、原映像/输入
资格、密文—帧位置桥及清理前退出判据。语义反例不靠摘要拒绝：已知绿块丢失、负控
被删、Wine颜色声明反转、帧身份替换、账号输入/外连扩大、派发失败冒作退出均须拒绝。
离线CI不下载原件、不运行完整原程序。

原内容R20同版名字—实体ID—SPR新增0；Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、
R79 PAUSED_NON_BLOCKING、overall percent=null。未登录、未听音、未进入原服世界。

## 默认全屏对照：启动后已崩溃，不能认证QUIT

HEAD `b88318a4724a2898f067b10652d8219df2660dc2`，运行40246852113 /
作业121330123334实际completed/success；这里success只表示取证作业完成。
工件12619049977、ZIP44378B、SHA256
`e011d4ea3c92af6c5b7b9936a92fc55beb8b62165768d045b7054616f3f3a7fd`已独立下载校验。
11成员为四派生/版本、旧root帧密文及输入前后三个X11窗口的密文；不是新增客户端。
四原样派生保存为无INITIAL/FOCUSED中缀的P3C文件，三轮合计12份原样元数据/版本。

FACT：原main类/映像出现、外框[0,0,640,480]，但**第一个3秒采样就已有winedbg错误
对话框及Wine Debugger控制台**，三采样均在；Wine日志原文为
`Unhandled page fault on write access to 02DC0000 at address 7AF3E6D3 (thread 0024)`。
对话框称sa_3.exe遇到严重问题，助手已认证解密并目视该错误框。不能根据该地址擅自
归因原游戏代码缺陷、具体DLL、缺地图或服务器不可达；准确崩溃原因仍OPEN。

旧取证代码仍向(350,380)派发了一次200ms输入，命令return0，launcher未退出、原main
仍在。**预期QUIT坐标所在正常登录场景在本次并未成立**，所以这不是合格的QUIT测试，
也不能说点击导致了崩溃：崩溃证据早于输入。公开原JSON中的operation只是代码意图
标签，保留原字节，由本条/custody明确纠正其验收含义。

全屏捕获中三个X11窗口分别涉及原程序、调试器/控制台，不能按数量叫三台游戏；原
窗口又被错误窗口遮挡，XGetImage对遮挡区域的限制适用，不把该张窗口帧当登录画面。
最终私人可看成果选用**第二轮正常窗口模式**640×480登录图：源40246551708，PNG
108700B/SHA `0aebcba5b0f75102e1c9dcde63bc22526387f5527c35749c3d44aaab97607811`，
RGB SHA `1b30216800d701f61e9a85794ac0cc9819f70841eab90b415ad608364c4c512a`。
它已目视并另作私人保存，仍标注颜色不合格。原图、密文和私人文件标识均不入公开Git。

## 输入守卫修正、止点及最高NEXT

本轮补充 `require_login_input_surface`：登录坐标输入前，要求只存在唯一原映像所属
StoneAge主窗；有调试器、原模态框、伪标题/其他映像或无窗都立即拒绝，并报告
input_skipped。焦点操作后、实际派发前再次核验。它来自本轮真实崩溃现场，而非假设
已经恢复了按键。合成反例及真实12份报告的独立guard通过后再发布；不为重复证明崩溃
或本守卫而再次下载原盘。旧三次原始现场和错误的坐标尝试保持可见。

最高NEXT `ORIGINAL-GAME-OBSERVATION-P3D-WIN32-ACTIVATION-AND-PALETTE-GATE`：先在
**无原件合成Win32程序**中验证前台/激活状态、已实现的8bit palette和鼠标按下/释放
事件（游戏实际接收，不仅外部命令return0），确认至少一个可用兼容环境。再按原启动
分支/有限WndProc和palette调用事实检查原程序，不扩所有DirectDraw helper。Wine9这条
路线若不能通过合成实际颜色/输入门槛，则比较可用的隔离32位Windows环境，精确记录
不可用条件并停止，不继续凭同一失败环境反复重拉原盘。

本包止于**一个已证取色解释差异、原悬停高亮、两种窗口输入负结果及默认全屏崩溃
边界**。P3C色彩/点击仍PARTIAL，P4回环登录、真实声音、世界及R20身份内容独立OPEN。
原客户端完整运行的存在性与可正常玩是不同结论，Stage A等既有边界不变。

发布预检另保留一次纠正：会话暂停后的临时基树缓存缺失，首次构造出的未引用tree只含
26个改动路径；本地完整tree比较不相等，**尚未创建提交或更新分支即被阻断**。随后
重新读取实际远端分支HEAD及完整Git tree后重建，不以缓存SHA或尾段替换完整仓库。
这不是远端Actions失败、历史文件删除或原客户端故障。

## 实际主线终验

内容main `30e5be2b4e30e0229f4bb672ec2b580b0ac6916c`、tree
`0e2e4d20f59dd285a06c948453c258e598996971` 已非强制快进发布。候选六项与同HEAD
主线八项Actions全部completed/success；P3C候选40269459891、主线40269527074验证21项
不同单元及原样12源报告/失败边界guard。旧P3、P1、登录图册、R16/R17/R18和Stage A
兼容均过；本地另含旧源语义guard共26项不同测试。主线没有重下原件或再执行原程序。

26内容路径逐字节等于远端，完整CURRENT/其余四大历史文件保持不变。
[永久发布收据](../../research/recovered/STONEAGE-TW10-ORIGINAL-LOGIN-P3C-PUBLICATION-R1.json)
保留全部候选/main运行、作业、内容文件摘要/blob与本轮未通过状态；三实际源的ZIP及
12个原样文件保管链在custody。新增输入守卫只做合成反例验证，没有假称已在原程序
重新验过。收据自身CI在发布后实际观察，不预写成功。最高NEXT仍P3D合成Win32门槛，
所有颜色/点击/原世界和版本身份边界不变。
