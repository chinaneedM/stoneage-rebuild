# R18｜既存2.5混合保存包原服务端文件全保管：补回18份候选清单未入选内容

**日期：**2026-10-25。当前任务 `EARLY-OFFICIAL-SERVER-MASTER-DATA-SOURCE-18_OR_EXACT_DOWNLOAD_PAYLOAD_CARRIER`。目标玩法：**原始敌人/宠物主模板、NPC/本体任务、遇敌组合、骑宠及奖励系统的服务端实物证据链**。真实限制：截至本轮，未获取 JSS1999/TW1.0/大陆1.82 **官方同构建原服务器主表**，也无2001华义battlemap218/219官方原始补丁字节。将已保存但来源受限的2.5社区混合包当**独立后代桥接样本**，不提升为早期官方事实。

## 本轮材料、新发现与实际来源

- `research/recovered/STONEAGE-25-PRESERVED-BUNDLE-STATIC-INVENTORY-R1.txt` Git blob `78e8260e89928df76513799511d45c14a9e24dfc`，3,283,845原Git字节，原存档来源 `https://www.lab.welovesa.com/viewthread.php?extra=&page=1&tid=219`；两个RAR保存分卷的2012年日期只认证保存时间。拼接母包既验361,255,180B/SHA256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`。其中 `ALL-FILE SHA256` 原始只读取证段已经记录全部实际解包文件SHA。此次**重新读取的是Git永久报告，不是重新下载361MB商业载荷，也不是重新哈希原服务器正文**。
- `research/recovered/STONEAGE-25-GAMEPLAY-DATA-INVENTORY-R1.txt` Git blob `47157f638cce7023727035981da11f1faecc9c78`，453,664B：`SERVER_FILE`完整占2245行，游戏性优先`CANDIDATE|server`仅2227行。这两个清单出自**同一次混合包原始取源链**，不是两次互不相关原始下载。
- 将 `SERVER_FILE` 的 **2245个原路径+尺寸**全部通过原母包的 `ALL-FILE SHA256` 逐项挂入档案，再对2227个已选候选核实尺寸及SHA，**2245/2245原哈希存在、2227/2227候选与原SHA吻合，0源哈希冲突**。以前没进入候选筛选的18项仍是原包真实文件，此次全部补齐。此前报告保持原封，不追溯改写筛选日志。

## 守恒结果

| 指标 | 原始保存包真实原位置 |
|---|---:|
| `gmsv/data/`完整服务端文件出现位置 | **2245** |
| 完整记录所代表原文件字节数 | **10465523B** |
| 旧CANDIDATE候选子集 | 2227 / 9734099B |
| 原来没纳入CANDIDATE的实存文件 | **18 / 731424B** |
| 内容SHA256不同块 | **2121** |
| 相同SHA重复组 | **53** |
| 多次出现相同内容的超额位置 | **124** |
| 文件路径属`npc/`的出现位置 | **2205** |
| 本轮实际删除原文件 | **0B** |

这份 **2245原位置→SHA索引** 存于 `research/recovered/STONEAGE-MIXED25-SERVER-FULL-SOURCE-R18.json`（仅档案路径/大小/完整SHA/旧候选标签，零版权原代码或NPC对白）。重复位置全部原样保留，不因内容相同删除引用或把一份脚本等同另一NPC实体。**53组与124超额引用不代表有53或124个原生NPC、任务或宠物**。做去重必须同时保留样本父来源、路径、原顺序、文件摘要以及后续跨版本关系。

未曾入选的18项具体为：`appear.txt`、`autopk/autopkaward.txt`、`autopk/autopkhistory.txt`、`clean`、`contract.txt`、`DEADJOE`、`effect.txt`、`gmset.txt`、`group.txt`、`group1.txt`、`history.txt`、`inv.txt`、`malayfia.txt`、`raceman.txt`、`racequiz.txt`、`ride.txt`、`titleconfig.txt`、`titlename.txt`。本轮只证明它们的**存在、长度、原SHA与筛选遗漏**，没有读取或推定正文逻辑、宠物成长数值、真实战斗触发或官方上线状态。

尤其 `group.txt` 68201B / SHA256 `58f722822f5bd95070297092d106622f236f54a1cb1ee5865c91d90210295eac`、`group1.txt` 70176B / SHA256 `4a02f2a3fa3d2dcf5589d8a2a560313c35d5a0a7e5e0589cc8df5f7df159ea8f`、`ride.txt` 287B / SHA256 `e737f79d22b040b64ef344df451126782d03c1206cc091d22e712a141695a808` 均有真实文件摘要；不应仅因旧`CANDIDATE`没有它们就当不存在，也不能以文件名证明原服组队/骑乘机制的具体运行规则。

## 宠物、任务主表命名空间与官方身份明确隔离

该保存包 `gmsv/data` **确实包含** `enemy.txt` (222463B)、`enemy2.txt` (153425B)、`enemybase.txt` (147750B)、`enemybase2.txt` (94248B)，但完整2245条未列 `enemy1.txt` / `enemybase1.txt`。后者见于2012社区GMSV代码及较晚的教程，**不能把不同后代分支的 `enemy1` 模型代码、物种ID或IMGNUMBER字段无源嫁接到这份数据**。已存 `petskill.txt`、`petskill1.txt`、`encount.txt`与 `npc/100/sb_kbu.arg` 亦只是这个混合保存包自己的文件事实；源文件名称不认证其为任一历史官方上线版本。

`npc/` 2205项按原路径保留，包括带 `event` 字面的目录和带 `arg`、`create`、`template` 的实际文件。但**目录包含event字样不等于运营限时活动**，文件存在亦不说明正式发行本体任务/奖励。四档 `BASE_GAME_QUEST` / `PERMANENT_VERSION_QUEST` / `OPERATOR_EVENT_QUEST` / `ORIGIN_UNRESOLVED` 必须要求分别有第一手版别/运营发布时间/上线/原脚本与同构建ID，不能自动给任何这些路径判档。

R17的2001华义 `battlemap218.sab`、`battlemap219.sab` 现仍仅被后期转载提及，其原始官方补丁与同文件校验值未取得。同期正式版大陆服务端也未实取。**本轮新早期官方宠物、NPC、核心任务恢复结果均为0**；Source A保持7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，overall percent=null。整包与原资源仍未建立私人持久保存位置，本轮没有下载或删除任何原包。

## 可重放门禁与下一优先

```bash
python -m unittest tests.test_stoneage_mixed25_server_full_source_r18 -v
python -m tools.stoneage_mixed25_server_full_source_r18
```

工具在离线仓库工作树内重新验证两个**原生Git blob**、母包链、所有2245路径/大小/原SHA、2227旧选集、18之前漏选项、53重复内容组与124额外引用，拒绝后代数据/官方归属偷换。数据源数值联接已形成材料成果，到此止点；**禁止进一步枚举社区服务器helper冒充早期复原**。

**NEXT `EARLY-OFFICIAL-NAMED-CONTENT-SOURCE-19`**：回22域中优先**已认证台湾1.0原客户端的原名字/脚本/外观/界面可读实物**，或找到可直接取回带官方发行谱系的早期服务端主表/正式补丁原件。必须一个具体新原件（SHA/版本/路径）与一个具名内容或直接精确的载体缺口才晋级；不重复旧4个韩国失效endpoint，不从后期教程给1.0反推实体。先按已有完整归档排重，再选原件实读。历史R18文档不是新版游戏实现任务。
