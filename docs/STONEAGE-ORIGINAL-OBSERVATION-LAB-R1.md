# 《石器时代》原版观察实验台｜P0–P4 实施与证据门槛 R1
日期：2026-10-25。**性质：复原用研究工具，不是现代新游戏开发，也不是原版游戏已运行证书。**

## 起点和用户决策
用户批准按最优解把“真正看见、听见、操作原始游戏”列为复原工作的一环。启动 fresh 远端main HEAD `21b14d6b0c50245f1dd607a48113563cef61a243`、tree `5b0e47521d8efd82078922ff5a859a067729d20d`，最近main运行R16/R17/R18/R19/StageA均success。协议 `a064174339b7a4656efe00b4446a066fd7abf304`、整个CURRENT blob `031c76a5a8e431f646853909bb2f2e11e6328cd2`（原Git blob已实际读回，普通文件接口空不是文件空）、路线 `c11eff237a8aaa1cc34488a6c3c7fcdd596f9ce2`、作品集及R19叠层已重读。保留原NEXT `EARLY-OFFICIAL-WORLD-ENTITY-SOURCE-20` 为内容检索主线。用户新的观察优先级让实验台先行，但不是将同版实体主表缺口标为已完成。

## 有用而可证伪的分阶段交付
| 顺位 | 最小实际交付和优先收益 | 通过的硬门槛 | 无源停止条件 |
|---|---|---|---|
| P0 原包和样本资格 | 原已认证TW1.0 Redump 104630；私人离线研究目录/本地程序沙箱；严格地区/时间/build来源记录 | 已知完整文件大小、SHA一致、生成报告固定源位置、原件零写入 | 缺跨会话私人持久存储时，不大包重复下载；本地输入外部另行提供 |
| P1 图像声音直接观察 | 读取原ADRN80B索引、REAL的RD段，输出**私人**灰度索引PNG；读取原WAV验证格式并用离线HTML本地播放 | 同版原文件SHA、原资源记录、原RD块和解码像素SHA、全部偏移界限；画面人工观察有来源ID | 未恢复原调色板只说灰度结构预览；无原件不得假报已看过 |
| P2 动画/调色板 | 从原SPR frame/animation表及已验证原palette字节重建多帧/调色板可视化 | 每帧时序与bitmap键来自同版、调色板格式原程序/原资源证明、输出可复核帧SHA | 缺准确调色板/姿态序列则保留未知，禁止把灰度渲染当原色 |
| P3 原客户真实启动 | 在隔离Windows兼容环境（适用时Wine或32位虚拟机）运行已哈希验证的原程序，录制启动、按钮、登录场景、音频设备行为 | 确认原程序SHA、分辨率窗口、真实帧/声音采样和输入日志；明确已观察/未观察区间 | 失败要区分环境兼容、服务器不可达、缺地图资源，不启用旧驱动/未知内核扩展 |
| P4 最小本地回环场景 | 只在必要字段有原版协议事实时实现非联网的mock握手、地图缓存M/MC、NPC/宠物可观察实例 | 原客户端真实登录路径/行为记录与报文字段、服务端模拟明确标识；同版实体主表证据独立保留 | 无原服主表不得虚构历史NPC、任务/宠物值或声称官方服务器恢复 |

**观察证据等级**：ORIGINAL_BYTES（哈希原件）≠ DECODED_PIXELS（索引值）≠ RENDERED_APPROXIMATION（灰度PNG）≠ AUTHENTIC_GAME_DISPLAY（真实客户端出帧）≠ SERVER_HISTORICAL_GAMEPLAY（已验证原服行为）。不能互相提升。此项目是2D图像/精灵系统，不能因为没有现代3D模型就认定人物/宠物资产缺失。

## 本包落地 P1（不会泄露原版权素材）
- `tools/stoneage_original_observation_lab.py`：只读原ADRN/REAL，原盘文件SHA精确固定；选一个真实图形 record index/bitmapno，核RD头和有界像素后输出**本机公开仓库外**的PNG灰度/JSON证据。内容SHA与源SHA完整记录；原色、真实游戏画面、具名宠物NPC、任务归属全部否定断言。
- `tools/original-observation-viewer.html`：零网络的本地文件选择器，展示PNG或播放用户本机原WAV；不内置商业素材，不能替代真正游戏运行。
- `tests/test_stoneage_original_observation_lab.py` 和独立合成CI：合成RLE、PNG、碰撞编号、强制源SHA和路径、WAV格式、篡改拒绝；CI不下载原包、不保存版权图/声音。
- 原WAV分析只读取已接受`STONEAGE-TW10-CLIENT-INVENTORY-R1.txt`中真实路径/大小/SHA，并使用Python `wave`；无法由此给音效标注游戏事件。
- 如果私人本地已解包资源不存在，此次只能交付**可执行工具且合成测试通过**，不能声称已生成/目视原版素材。

## 私人原件和运行隔离规则
私人原件长期保管仍 `BLOCKED_PRIVATE_STORAGE_NOT_PROVISIONED`；当前GitHub Actions临时runner及本聊天容器不是跨会话原始素材库。不得把原安装包、程序、PNG、WAV、GIF、对话正文自动写入公共仓库；影像只作为研究者本机可观察输出。原客户端禁止直连历史外网地址；必要时隔离网络并只允许可审计127.0.0.1实验服务，不执行来源不明的驱动、PortTalk或者游戏外挂。2001官方已验证资源与2.5社区保存包严格分域。

## 后续排程条件
先让P1原盘真实索引PNG私有目录可看/音频可听；再验证帧动画与真实调色板，再进行隔离原版程序启动。不以“写了查看器”代替已经亲眼看到原画。每个观察样本需要版别、路径、原SHA、bitmap/spr/file-offset、截图/音效观察与人工确认标签；观察主观猜测单列HYPOTHESIS。同步推进 `EARLY-OFFICIAL-WORLD-ENTITY-SOURCE-20` 真正同版名字—实体ID—SPR联接，维持DD-028活动与本体任务四档独立。

状态：P1工具可进入远端自动化验收，**原版程序未运行、原色/原画面未还原、原服世界未进入**。Stage A7 PARTIAL+2 OPEN，B/wiki GATED，R79 PAUSED_NON_BLOCKING，总体完成率null。

## 2026-10-26 P2A：原动画帧序已接到私人播放器

P2拆为P2A帧序/像素与P2B真实调色板。P2A原源Actions40237734461实际成功，四完整原文件SHA、原SPR全组段、原ADRN/RD逐块与旧源表相同；25帧出现位置/16不同位图实际解码并导出三私人HTML。原素材及嵌图HTML只在临时私人目录，工件/公开Git仅保留派生JSON。无原程序运行/原色/历史FPS或助手亲自观看原版体验。见`docs/continuity/STONEAGE-ORIGINAL-ANIMATION-P2A-20261026.md`。

在仓库根目录，提供同一已认证TW1 `data`目录，运行：

```bash
python -m tools.stoneage_original_animation_lab --original-dir /private/TW1/StoneAge/data --spr-no 100000 --direction 0 --action 6 --output /private/observations/tw1-animation.html
```

输出目录须先存在、位于公开仓库外，文件须尚不存在。生成HTML包含本地灰度PNG，无需服务器，支持前后帧、循环、帧位置、可调人为预览节拍和源偏移/声音字段。原SPR倒计时被保留；预览每秒节拍不是已证原游戏帧率。索引0不擅自抠透明、不命名动作/物种。缺任一四原文件或SHA不符则拒绝，不能用现代资源混替。`--check-report`仅重放派生元数据，不要求下载原件，也不声称完成原像素读取。

下一P2B须验证同版SAP实际解释和保留索引颜色，不能仅用后代读取器或16个旧文件名给原图着色。P3真实启动仍独立OPEN。原内容任务R20和Stage A/B边界不变。

## 2026-10-26 P2B：初始化色已通过原指令与真实像素联接

源40241350181实际成功：原TW1初始化代码的限定执行与重建RGB逐字节相等，三原动画已导出Palet_0初始化色的私人HTML。32保留色、224 BGR项、强制黑168号及非零缓存跳过条件均有原源；16位图原解码索引与P2A相同。见`docs/continuity/STONEAGE-ORIGINAL-PALETTE-P2B-20261026.md`及`tools/stoneage_tw10_palette.py`命令。页面显示初始化色来源、场景选色未知；不把它当原客户端截图/完整运行。下一有限包转P3隔离兼容环境和真实第一屏，昼夜/渐变/全场景选色仍独立OPEN，不继续低级渲染helper。独立内容线R20与全部历史/生产边界保持。

## 2026-10-26 P3：原程序实跑、登录面板可见，色彩仍未合格

原SHA `sa_3.exe` 已在仅lo/无路由的新网络namespace、Wine32/ACP950中真实运行，375个
原运行文件逐一鉴真。首次24bit显示出现原256色要求；纠正为GetDisplayMode实际8bpp后，
三采样无该提示框。最终源40244430667实际success，一张原帧经会话公钥密文传回、
本地认证解密并由助手目视：原JSS/石器时代登录面板和账号/密码、OK/QUIT可辨。
画面主要黑白抖点、少量黄红色，**正确颜色未验收**；未输入账号、未听音、未进入世界。
不是现代页面或P2离线预览冒充原游戏。原截图仅私人保存，公开Git保留原样派生证据和
哈希，11文件保管链及旧取消/纠正历史详见
`docs/continuity/STONEAGE-ORIGINAL-BOOT-P3-20261026.md`。

最高观察NEXT P3C：有限定位8bit原显示/截图的palette或colormap差异，取合格原登录颜色
并记录一次隔离输入响应；不以窗口/测试通过宣布整段P3或原世界完成。P4与R20仍独立OPEN。

## 2026-10-26 P3C：窗口取色已区分，颜色及点击仍PARTIAL

原生X11已知红绿块/错误colormap负控通过，原窗口自身colormap取色比root清楚；正常
窗口的原登录图已私人保存，仍只有15种RGB，未验原色。实际QUIT悬停高亮可见，但两轮
窗口模式短按/200ms按住均未退出；原默认全屏在输入前已出现Wine崩溃/调试器，不能把
该次坐标派发称为QUIT响应。三源Actions取证作业success不等于原功能通过。

见 `docs/continuity/STONEAGE-ORIGINAL-LOGIN-P3C-20261026.md` 和12份原样派生保管链。
已补输入前后异常/调试器窗口守卫，原exe/资源未修改。NEXT P3D先让合成Win32实际颜色、
激活和接收输入通过，再决定可用的32位兼容环境；不继续同环境重复原盘下载。原声、
回环服务端和世界仍未观察；R20与Stage A/B/R79边界不变。

## 2026-10-26 P3D：合成环境资格已有实际判定

自编Win32 GDI/DirectDraw在四环境/配置共8路径实际完成颜色、前台/active/focus、消息
及异步按下接收；8例SendInput接收成立，但只有3例颜色通过。原生Windows2022的32位
程序可以正确显示和收输入，却报告32bpp/ACP1252；Wine8报告8bpp/CP950但颜色量化，
基于Wine9上游原始代码的PrivateColorMap单项复测也未改善。重启守卫首败及修订实际
记录均保留，本轮未下载/执行原客户端。

见 `docs/continuity/STONEAGE-SYNTHETIC-WIN32-P3D-20261026.md`。NEXT P3E只查一种可用
Windows8位/编码/网络隔离资格方案并用同一合成门槛验收；不得把console codepage、
兼容选项或成功注入等同实际ACP/色深/接收。未通过就记录环境阻塞、返回22域材料队列，
不连扩Wine9低层helper。原游戏颜色/QUIT、声音、服务器及世界仍独立OPEN。
