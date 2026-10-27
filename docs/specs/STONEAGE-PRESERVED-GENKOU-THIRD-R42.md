# R42 原保存洞窟第三守护兽参数与有界差异

日期：2026-10-27。范围：一份社区混合2.5保存包的原文件字节，不是官方 JSS1999／台湾1.0、同服务器 build 或原任务运行认证。本轮直接兑现 R41 的 NEXT，不重新下载整包或推断名为「風的守護獸」的完整任务。

## 原件来源和保管

原件取证 GitHub Actions [40456016963](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40456016963)，job 122029396896，source commit `7ed933d66a2e557683db072c8b1de97bf482f26c` 实际 completed/success；通过原 RAR4 7954 个头、184 次 HTTP206 范围，累计读取 12,013,836 字节，低于 16 MiB 边界，未重下 361 MiB 混合客户端/服务端原包。四成员全长 SHA256、RAR CRC 校验成功，前三文件复核 R41：

| 原文件 | 字节 | 原件 SHA256 |
|---|---:|---|
| `sb_geno.create` | 573 | `5aec44349ae3a6071b0882fd40d693f3bf1e7bdaf9ba489ac3ffbc89e26331f1` |
| `sb_geno.template` | 321 | `76a826f1022276dfa9590e5ad51c6a96e9c88146a2fc39790c2cc60cbed60e2d` |
| `sb_kbu.arg` | 258 | `433d17a58869147f91cacc57487795d7686b53415872f0694aba02dbc869502b` |
| `sb_kgi.arg` | 281 | `61c2aefca26c9d84db061f34c66c74b980006cac915fe732394f753daddbd586` |

实际派生 JSON `research/recovered/STONEAGE-PRESERVED-GENKOU-THIRD-SOURCE-R42.json` 是作业日志逐行恢复的有界元数据；Git blob `8ccd29a7e3cca310ea9e0b30acd0138fcfa30434`。原工件 12712234037、ZIP API 摘要 `sha256:0921ac976ba92189aaccad624f43e05edf176d35fa0dd90de257b0ab6b24373a`；本轮未独立下载该 ZIP，**不声称**ZIP 内容与日志重构 JSON 的逐字节交叉确认。源明文只短期留存，CMS 密文／密钥／原 NPC 对白与实际源脚本不进入公开 Git。

## 具体不同字段

两份原 ARG 都严格按 cp950 解码并逐字段保留数值及文本哈希（无原对白正文）。第三 `sb_kgi.arg` 从258增至281字节；共有3个旧字段内容变化：`askbattlemsg1`（对白哈希变化）、`dieact` 由0至1、`enemyno` 完整10次引用从：

- `sb_kbu`：1272,1277,1277,1280,1280,1278,1273,1273,1275,1275
- `sb_kgi`：1271,1274,1274,1281,1281,1276,1279,1279,1276,1276

`sb_kgi` 新增 `warpfl=11215`、`warpx=9`、`warpy=16` 三个字段；旧 `sb_kbu` 的 `time=180` 在第三文件不存在。保留全部重复编号，不借标签推敌人物种、NPC 本体/活动属性、时间单位或服务器行为。

上述字段接 R41 第三创建块：`floorid=11214`、`borncenter=41,36,1,1`、`graphicname=100343`、`100/sb_kgi.arg`。仅建立**保存包原文件之间的静态引用**；`warpfl` 的字面数值不能替代已观测的真实传送/终结动画或任务奖励。与现代11208 YAML 的两NPC/三 warp 严格分开，不宣称 modern 11214 是否存在或内容删除。

## 终验约束及下一工作

独立离线验收逐字段核查旧 R41 原始指纹、R42 完整成员散列、对比字段/数值、重复编号、新增与消失的字段；反例拒绝伪来源、假建构/任务认证、截断、错误 warp、丢重复、报运行、超界下载。source 运行成功仅证明本次实取和元数据，不等于原游戏登录、原服务端执行或官方版本认证。Stage A 7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79 PAUSED、P3E BLOCKED、私有持久原包保管 PAUSED、总体百分比未知。

**NEXT:** R42 单元实物差异已经到有界止点，按连续性协议13轮转22领域原材料队列，优先早期官方同构建**可具名宠物/NPC/本体任务的真实主表或事件**；如源不可得则记录具体缺口，不继续扩 `sb_kgi` / NPC helper。DD-028 任务本体／永久新增／活动／起源待考四类隔离仍有效。
