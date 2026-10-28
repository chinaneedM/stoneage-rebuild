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
