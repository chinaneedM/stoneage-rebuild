# QUEST01｜原创建配置→事件控制块→任务物品的真实来源索引（2026-11-03）

**阶段：Stage A 原版《石器时代》历史复原，不是新石器任务设计。** 从 fresh GitHub `main` HEAD `42f35e5bfbc06af7481eefa28a228c5abb936c68` / tree `12f07e704620927b819c867c5b82d28ce207b1aa` 启动，11 项 Actions 成功，0 开放 PR。连续性协议、README、历史 `CURRENT-STATE` 原 blob、设计、历史、来源及模块执行文件均重新核实。巨大 `docs/CURRENT-STATE.md` blob `c89e0e33537990aa2132b47c40fef49a985a935c` 原样保留，不从空正文 GitHub 接口重写。

## 1. 真正重新取得原字节，而非网页猜测

从已保存在用户私人资料库的社区混合 2.5 RAR（361255180B / SHA256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`）重新取源。完整父 RAR 现算 SHA 通过；其下 `gmsv/data/npc/` **2,205** 份文件 / **1,930,332B**，逐份重新核原大小、完整 SHA256 与 RAR CRC，0 缺件/CRC 失败。189 份 `.create` 原文件使用原始控制字段审查，原带 `enemy=` 创建块 **4,985**（此外20个大括号块没有此字段），其中 `enemy=changeevent|file:` **315 条**，指向 **295 个不同原脚本文件**、合计 **434,873B**，这些引用目标均在同载体实际存在。295 原脚本全部严格 CP950 可解码。另有5份其他 `.create` 文件本体包含 CP950 不合法字节，创建结构只用容错方式解析**原 ASCII 控制字段**，保留每个原文件 SHA，绝不把异常文字解码冒称内容确认。

**315条是创建配置引用，不是315个任务；295份是源脚本文件，不是295个任务。** `changeevent` 在同 RAR 原 `jaruga/event/event.template` 内与 `functionset=ExChangeMan` 相联；这不证明当年同服运行，也不证明文件目录名 `event` 就是节日/时点活动。

## 2. 1,349 个原 `TYPE` 事件段：全部逐来源重建

以真实原 `TYPE:` 行做 1,349 个控制块锚点，逐个记原文件相对路径、源 SHA、原行序/起止资格、`EventNo` 数字、`EVENT` 条件词类别/摘要、`EndSetFlg` 原数字、字面物品输入/输出的数字 ID、来源文件完整 SHA；**不公开原剧情对白、原商业脚本正文或原美术**。

| 原脚本字面 `TYPE` | 原段数 |
| --- | ---: |
| `MESSAGE` | 769 |
| `ACCEPT` | 494 |
| `REQUEST` | 81 |
| `CLEAN` | 5 |
| **总计** | **1,349** |

严格按 CP950 Unicode 空白消除读原 `EventNo:` **1,348行**、`TYPE:` / `EVENT:` 各 **1,349行**、`EventEnd` **1,348行**。旧 CHAR08 统计 `EventEnd` 1,347，是只覆盖普通原字面结束符的范围；本轮完整检查额外发现1条源 `EventEnd` 后有**全角空格**，1条仅有ASCII尾空格，另有1,346条精确原 ASCII `EventEnd`。保留前轮报告作为旧方法历史，不覆写或误报两份历史不同的源文件。

两个非完整控制实例明确保留：`giiru/event/garunaev6` 有15 `TYPE`、15 `EVENT` 和15 `EventEnd`，但只有14 `EventNo`；`poru/titan` 有8 `EventNo` / `TYPE` / `EVENT` 却只有7个源结束行。解析器只做静态档案，不为缺字段自动补齐，也不宣布原运行引擎会失败。

## 3. 有源的状态编号与原物品关联（非执行版任务链）

原 `EventNo` 有 **59 个不同非负数值**；本轮只对同原静态段 `EventNo→EndSetFlg` 生成 **63 个不同的源数字对**，不冒充真实执行路线、任务完成条件、任务类型。原 `EVENT` 条件中明确出现 `ITEM` 2,733 次、`ENDEV` 1,469 次、`NOWEV` 437 次、`LV` 1,852 次、`PET` 158 次；**计数是原字面关键词出现次数**，不是游戏状态变化次数。阶段字段和物品运算字面均保持条件摘要 SHA，以免丢失无法直接解析的语义。

此次在 CHAR08 的 `ITEM` / `GetItem` / `DelItem` 基础上将 `GetRandItem` 的数字奖品候选**作为独立原字段类型**纳入有界抽取，得到 **694个不同的数字物品 ID**：687 在两份原 itemset 中均有对应行、5 只在后一表有（2054 / 2391 / 20570 / 20571 / 20572），2 在这两表都没有（2744 / 2745）。这不表示 694 个任务、694 个实际奖励，亦不能因缺两原表就判定历史物品不存在。与前轮 CHAR08 的380种不同数目**提取字段范围不同**，并非过去源文件变更。

315个创建引用跨**150个不同 `floorid` 数值**，这是原源字段的地图编号而非150张已可运行的官方地图、当前世界打通或150条任务。源 `borncenter` 在多数创建块并无原字面，缺字段不从文件名猜坐标；已有实际整数则保留。全部创建引用的源起源分类：`UNRESOLVED` **315**；可认证初代/其他官方**常驻**任务0，可认证有日期时点的运营活动0，**不是**“原游戏没有常驻任务或活动”的事实。

## 4. 交付与下一步

- [公开全量来源与任务控制索引](../../research/recovered/STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json)：**315** 原创建来源引用、**295** 原脚本文件来源 SHA/CRC/体量、**1,349** 个控制段的源行/字面状态/条件摘要、独立数值关系和负例边界。GitHub 提交为无原剧情正文的可分源派生 JSON，不把文本版权资产或原 RAR 放入公开仓库。
- 私人 `StoneAge-QUEST01-private-original-source-observer.zip` 含完整295原脚本文本的离线观察 HTML，已保存用户 Library `/石器时代/`；私人ZIP当前源SHA及CRC另核。Chromium 在内存载入 HTML 并实际验证295/295个检索入口、点击真实原文展示、不存在词筛选0结果、0 JavaScript错误/0网络请求；本执行环境直接 `file://` 被管理策略阻断，**不称本机 file:// 运行成功**。这是资料观察，不是进入原游戏。
- GitHub CI专项公开派生源8项正/负契约，逐脚本和逐段守恒并从ITEM01七份13915行数字目录重放694个原物品 ID。CI不读取私有 RAR，不证明服务器脚本生效或官方年代归属。

**QUEST模块仍SOURCE_BOUNDED_PARTIAL，当前最高 NEXT `QUEST-STORY-MODULE-02`**：继续在相同保存的2205份原NPC文件中整理**非ExChangeMan**的任务控制族（如 `NEWWARPMAN` 的原 `TALKEVENT` / `FREE` 及其真实物品与地图参数）和有效原图/对白关系，常驻、时点活动、起源无法判定三类严分，缺源即记止点。绝不由日期词或路径名单独判官方活动，也不开始新石器设计/体验优化。Stage A 7PARTIAL+2OPEN、Stage B/wiki GATED、R79暂停、overall_percent=null，原 `CURRENT-STATE.md` 完整SHA不变。