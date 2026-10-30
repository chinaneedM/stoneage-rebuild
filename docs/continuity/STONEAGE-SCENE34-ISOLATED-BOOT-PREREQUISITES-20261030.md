# 2026-10-30 — SCENE34：Windows回环资格有实测，原服务端启动止于私有输入通道

本轮原目标为SCENE33指定的SAAC→GMSV最小隔离启动。**只完成有限的自编32位程序环境资格；原服务端启动未完成。** 没有在Windows取得原件，没有执行SAAC/GMSV/游戏客户端，没有端口9200/9065绑定、原认证握手、数据库加载或世界进入的新增证据。不得将本轮环境实测称为原程序运行或可玩。

## fresh remote、原件与执行能力

重新读取远端main `d5aeee9399a1398b574f8dacadb0af66c41c64c3` / tree `9667fca0312691f4bcff3056fe258a41ac15fd6c`，完整6562项tree、最新五提交、0开放PR和最新收据run40977201848的completed/success；七启动文件、路线/22域/R102及SCENE33覆层重新核对。原本地worktree仍指向已失去的父目录，另从远端新建正常checkout，不信残留文件。完整CURRENT2708031B / blob `20050acf279a01555ab06a381dfcdc936bd381a6` 与该远端逐字节相同，README旧122382B完整保留为追加前缀。依协议14追加本覆层。

既存私人RAR重新取回并全件验证361255180B / SHA `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`，没有重下载游戏载体或重造原件；本轮未重新解出/运行其中程序。SCENE33八件静态身份和C / MIXED-MODIFIED版本限制原样保持。

| 执行/传递条件 | 当前实际能力 | 本轮处理 |
| --- | --- | --- |
| 本地原件读取 | 已保管RAR可取回且整SHA相同 | 只读认证，不执行原件 |
| 本地Windows/Wine/虚拟机 | Linux x86_64；无wine、wine64、QEMU/VirtualBox、pwsh或Windows编译器 | 不扩安装器/驱动或兼容参数树 |
| 一次性Windows | 已有GitData推送→GitHub托管Windows2025 Actions路径 | 仅运行自编x86网络程序，实测一项缺失前提 |
| 私有原件传入Windows | 当前GitHub接口暴露GitData和工件下载，未暴露私有workflow输入、secret设置、私有文件上传至runner | **OPEN：具体阻塞**。不把原件、配置/认证值或带权限下载链接写到公开Git/日志；不把同一个外部游戏包重新下载到runner来绕过既定保管路线 |

这只描述本轮实际工具能力，不宣称GitHub平台或未来环境永远不能私有传递。没有发生审批拒绝或凭证错误，也没有要求用户交出真实账号。

## 两次真实自编程序观察

一个自编Winsock PE32/i386 console程序提供回环listener、8字节精确echo、外部TCP connect和有界hold。两个回环进程分别挂起创建，加入各自active-process-limit=1的Job后恢复；PID、实际映像和Job flags8200读回。没有任何历史二进制、内存注入、原协议模拟或账号。

| 观察 | HEAD / run / job | 实际结果 |
| --- | --- | --- |
| 首次 | 1e1976a425d3921c1b63cabd19684f1508197f8f / 41002704873 / 123890540715 | 阻断前后回环成功；外部连接在规则中报告10060，因此资格失败并停止，没有在规则中执行回环测量，更没有原件执行 |
| 修正后 | bff50fef46d3effeb57c5626876b30cd8e62dda0 / 41002914495 / 123891199286 | 前/规则中/恢复后三组两进程127.0.0.1:19200的8字节echo全同；规则中前后两次外部canary均10013；有限TCP/IPv4资格通过，原件传递仍阻塞 |

首轮自编非阻塞connect只等writefds，没有读Winsock失败连接的exceptfds；增加异常就绪集并在就绪后读SO_ERROR，**没有把10060放宽为合格拒绝**。两次为不同来宾、DNS解析的IPv4也不同，不能当作同来宾/同目标地址的受控A/B或倒改首轮错误含义。两个workflow均completed/success只证明观察脚本完成；首轮资格明确false，不能藏在绿灯下。

修正后Windows镜像20261021.278.1，两个自编进程实际pointer_bytes=4。三组各自server/client正常退出0，PID归属和映像核同，测试只绑定127.0.0.1:19200，不认证原9200/9065可绑定。三profile启用；SYSTEM独立恢复任务注册；入站/出站两规则为all-program/all-protocol/Any profile Block并读回，回环仍可通信。测量到的规则中区间仅**1.75秒**，不能写成完整120秒隔离；120秒是watchdog计划。结束前先关闭所属Job，再删除本包规则，remaining=0；外部TCP canary及回环恢复后均成功。hold进程清理有观察，但不把强制清理冒称自然退出或单独证明kill-on-close路径。

经验网络范围只含一个外部TCP/IPv4端点及自编回环，未遍测UDP/IPv6、来自外部的入站路径或原程序的所有行为；入站规则配置与外部入站实测保持区别。本结果不叫完整安全沙箱，不迁移为原Cygwin行为、原连接握手或数据库依赖已解决。

## 永久证据与核验

两ZIP各独立下载并核GitHub API整SHA；两个原始JSON按原字节（含原换行）保留，未用修正报告改写首轮：

| 实物 | artifact / ZIP字节 / SHA256 | 原JSON字节 / SHA256 |
| --- | --- | --- |
| 首次观察 | 12954430279 / 1500 / c88074774069feeace33c6d6104cf82d70367a414923f868423c79236ca81c1d | 4549 / f9e12d411d1c6d66c1fd2b5738bb2c1662e778b210c645a2acba825d85224c60 |
| 修正观察 | 12954117931 / 1621 / bab3c695438ab0e555d92336030b8e4a93a8da2290b96c236943fc6942218379 | 6051 / f01c0c1508fc66fe3bc1f3d4f6a441629110cdf0497a8d68df379a1af3801638 |

原报告分别为 `STONEAGE-SCENE34-FIRST-OWN-WINDOWS-ACTUAL-R1.json` 和 `STONEAGE-SCENE34-CORRECTED-OWN-WINDOWS-ACTUAL-R1.json`；`STONEAGE-SCENE34-SOURCE-CUSTODY-R1.json` 固定范围、输入能力、源HEAD/代码SHA、run/job/artifact/ZIP/raw身份与止点。各报告的三个源代码SHA均从对应execution HEAD的Git原字节重核，不凭当前工作文件同名认证。公开只保留自编程序和派生报告，无原游戏载荷。

29项新检查和25项SCENE33回归本地通过；反例包含超时冒领拒绝、只绑定冒领echo、PID错属、丢一Job、原件/世界晋升、删私有输入缺口、把watchdog当采样时长及倒改首轮。公开验收只重放这些已保存报告和合成反例，不重做网络/旧程序运行，最终候选/主线Actions按后验另记。

## 具名停止与回22域后的最高下一

SCENE34最小原服务端boot保持**BLOCKED_PRIVATE_INPUT_CHANNEL**，不能标DONE。重启须出现可认证的新能力：在获准Windows执行环境中私下挂载已保管原件，或能把受保护的输入/传递凭证送到一次性runner且不公开。届时复用同一RAR和SCENE33身份门槛，重新实测当时环境，再仅做SAAC→GMSV启动/首个真实错误；不得自动运行固定公网客户端，不需要真实账号。空配置、lockip必需性和SQL后端仍OPEN。

SCENE33/34已经连续两包解决运行前提而没有新增游戏内容；按协议13停止继续造隔离/传递/驱动helper，回22域。已读R102及22域现存材料，SCENE28–31人物/宠物动作与原声音试听已有；不能把这些重复作为新成果。当前新的可解释内容候选为第14域pet_encounter，既存R18只保存了encount/enemy/group等文件的身份，尚无该包的具体区域遇敌链资料。

**最高下一：SCENE35-ONE-MIXED25-ENCOUNTER-CONTENT-JOIN。** 复用已保管父RAR，限一条有原文件字段说明/语义支撑的 `encount.txt → group1.txt → enemy.txt → enemybase.txt` 遇敌候选链；先查既存记录去重，再读原头注释与实际行。只在同包命名空间内核一个区域/一组敌人，记录物种名、数值及坐标/版本未知边界；原字段不够解释、键不唯一、链不闭合就具名停止，不猜列含义、不批量建全物种表、不制造历史地图分布。保持社区修改版范围，绝不转作TW1官方遭遇表或运行观察。该链是否存在/能否闭合尚未预支。

仍在历史恢复阶段；Stage A 7 PARTIAL + 2 OPEN、Stage B/wiki GATED、R79暂停、overall_percent=null不变，原世界尚未进入。
