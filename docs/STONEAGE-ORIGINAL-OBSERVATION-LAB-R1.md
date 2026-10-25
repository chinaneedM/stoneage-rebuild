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
