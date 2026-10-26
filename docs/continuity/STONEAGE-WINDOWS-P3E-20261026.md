# 2026-10-26 — 可用Windows显示/编码资格P3E：有界环境阻塞

连续性协议14加法覆层。启动重新读取GitHub main
`71889eaba2835ee70f7ffeafcdb15151fcb3e6bc` / tree
`a6e72c5497862c4fb2489d39e5418d1058e105b9`、最新提交、597分支完整分页、0开放PR、
5890项未截断tree（无AGENTS）与Actions。最新收据40271940068实际success；无运行中，
10-07无关旧queued37642417333保留。七启动文件完整Git字节与远端tree逐blob核对，
另读路线、R102全域portfolio和最新P3D覆层，不据旧聊天推HEAD。CURRENT2680510B、
blob `031c76a5a8e431f646853909bb2f2e11e6328cd2`、SHA256
`f02f85b837fc09973cb2eca33f7daf4db547a77cb35a81a9576c6308f70142c0`；它及决策/历史/
来源/路线五大历史文件原样保留。完整启动摘要见CUSTODY。另用独立工作树保留原目录
已有的一处不相关未提交修改。

## 目标与严格止点

目标是为后续原TW1登录观察验证颜色/输入/编码前提，只检查当前可用Windows2022
runner。有限交付默认、256COLOR、WINXPSP3+256COLOR三设置各两条自编显示路径，
实测GetDeviceCaps、DirectDraw.GetDisplayMode、GetACP、RGB和收到的输入；另测试
一个自编程序路径的防火墙控制。找不到同时满足全部条件的环境即记录阻塞、返回R20，
不继续扩Wine9/兼容参数/驱动树。本包原商业资源下载0、原程序执行0。

## 真实源与六条显示路径

源HEAD `47269aba3620d85f83d785b39fba74c38c069a9f`、tree
`fa147aabd271e5e572e4efa748ef825bf629bfb1`；源Action
[40274977916](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40274977916)、
job121415693950实际completed/success。日志：Windows Server2022，镜像windows-2022 /
20261022.344.1，MSVC x86。是现代Windows上的WOW64程序，不是XP。

新增独立自编检查器/编排，复用P3D控制器的相同颜色和接收计数门槛，两exe均显式
`/MANIFEST:NO`。每个子进程环境传入兼容设置，不能只凭设置字符串判定生效。
原P3D代码、报告和失败历史不改。

| 设置 | 检查器GDI / DDraw当前bpp | 两显示控制器bpp / GetACP | RGB及外部截图 | 实际接收输入 | 完整前提 |
|---|---|---|---|---|---|
| 默认 | 32 / 32 | 32 / 1252 | 两例通过 | down/up各+1，async各+7 | 否 |
| 256COLOR | 8 / 8 | 8 / 1252 | 两例通过 | down/up各+1，async各+7 | 否，ACP不符 |
| WINXPSP3 256COLOR | 8 / 8 | 8 / 1252 | 两例通过 | down/up各+1，async+7/+8 | 否，ACP不符 |

六例GetPixel均红(222,0,0)/绿(0,200,80)，独立ImageGrab各19300个预期红/绿像素。
必要DDraw HRESULT成功，8bpp两例primary palette attach也成功。六例foreground/
active/focus匹配，实际收到WM_LBUTTONDOWN/UP及GetAsyncKeyState高位，清理前真实
正常退出0。合成8位颜色/输入可用是新实测，不能仍把P3D“原生仅32bpp”当唯一环境
结论；也不能反向宣称原游戏颜色或QUIT已修复。

三个设置的EnumDisplaySettings及DDraw枚举各39项（13分辨率×32/16/8bpp），
640×480×8的CDS_TEST均0；**没有实际切换桌面**。默认程序仍32bpp，枚举/测试成功
不是当前8位证明。兼容设置中两API实测8bpp，只认证应用可见8位兼容/模拟路径，
不证明物理设备原生8位。Microsoft
[EnumDisplaySettings](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumdisplaysettingsa)
说明旧桌面应用低色深可由系统模拟、宿主继续32位；API文档与运行实测分开。

## CP950转换和控制台可用，ACP仍不合格

三设置均IsValidCodePage950为true；自编Unicode样本“石器”转CP950字节正确，无默认
字符替代。SetConsoleCP/SetConsoleOutputCP均成功，回读950/950；GetACP前后均1252，
两显示控制器也1252。系统locale=en-US，注册表ACP=1252。CP950转换器和控制台可用
不等于旧程序CP_ACP950。

依据Microsoft [GetACP](https://learn.microsoft.com/en-us/windows/win32/api/winnls/nf-winnls-getacp)、
[SetConsoleCP](https://learn.microsoft.com/en-us/windows/console/setconsolecp)分别解释系统
ANSI与控制台页；[国际设置](https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/configure-international-settings-in-windows?view=windows-11)
说明多数系统locale变更需重启。本包未更改系统locale、未重启，未完成繁中系统开机
后的ACP验证；不能写成“改系统locale已尝试失败”或“Windows不支持CP950”。
当前runner不是经验证的ACP950开机环境，重开需要实际新环境证据。

## 防火墙canary通过，原进程树仍未资格化

自编检查器仅用Winsock连接固定解析的api.github.com IPv4:443，只建TCP、不发游戏包。
按照Microsoft [New-NetFirewallRule](https://learn.microsoft.com/en-us/powershell/module/netsecurity/new-netfirewallrule?view=windowsserver2025-ps)
建立匹配该自编exe绝对路径的Outbound/Block/Any规则，读回路径与参数，三个profile
Enabled均1。真实四时点：加规则前连接成功/error0；加后同路径失败/WSAEACCES10013；
规则仍在时同字节另一未阻断路径连接成功；删除规则、回读剩余0后原路径又成功。

这排除“目标恰好失联”与仅凭规则创建返回值的假隔离。范围仍仅**该程序路径、一个
TCP/IPv4目标**，不证明原程序、子进程、UDP、IPv6、全部外部目标或回环服务。
没有全局关闭runner网络，也不照搬Linux namespace结论。未来原件运行前须验证真实
原路径及后代完整外连策略；本canary不授予原程序运行资格。

## 永久保管与验收

工件12629299095，ZIP4220B，实际下载SHA256
`de929bd18c8765b31aa549268d884aaa93335ffa7bb0122eb76226ac51d04486`与API一致，恰一成员
p3e-derived.json。原样98928B、SHA256
`5cf118f9520a3c868c3dd48e1341eed327889a6b30f440b735b61512978f0069`、Git blob
`349db3db1159792c9af6a19b5c961bcb3f8d022a`永久入Git，无行尾转换。工件/Git均无
exe/obj/截图/原商业资源。[保管链](../../research/recovered/STONEAGE-P3E-WINDOWS-CUSTODY-R1.json)
保存run/job全部步骤、源/ZIP/报告blob及四源码Windows CRLF摘要，与规范LF精确转换
后一致，不把行尾差异当不同算法。源运行成功不等于环境通过。

独立标准库脚本不调用assessment helper，逐核六例RGB/截图像素/输入计数/退出、39
模式、8/32bpp、console950与ACP1252区别和防火墙四时点，全部一致。新增11项及既有
17项共28本地测试通过：不同进程的能力不得拼接、成功派发不得替代接收、API返回不
替代像素、超时不冒WSAEACCES、控制路径失联不认证隔离。归档重放通过；候选/main
CI须发布后据实际结果另记，不预写成功。

## 结论和最高NEXT

**BLOCKED_AVAILABLE_WINDOWS_ENVIRONMENT**：当前自编8位兼容RGB与实际输入通过，
但ACP1252、原路径/后代完整隔离未验收，没有同时满足全部前提的环境。本有限包止点。
原登录颜色/QUIT、原声、原服登录与世界进入均未修复或验收，不给原客户端写启动合格。

最高NEXT返回 **EARLY-OFFICIAL-WORLD-ENTITY-SOURCE-20**：全22域先排除既有原清单、TW1
文本、社区混合2.5与网页目录覆盖，限一个实际可取且有同版原始载体的官方NPC/宠物/
本体任务名字→实体ID→原图/SPR联接。没有新源就给精确缺件与重开条件，不重复旧大包、
不扩字符串/显示helper。观察仅在新的ACP950开机环境、同程序8位RGB/输入及完整隔离
证据出现时重开，设置计划不等于已实测。

本轮R20新增具名原实体0，Stage A7 PARTIAL+2 OPEN，B/wiki GATED，R79暂停，原大包私人
保管仍受限，overall percent=null；测试数和控制路径数不是复原比例。
