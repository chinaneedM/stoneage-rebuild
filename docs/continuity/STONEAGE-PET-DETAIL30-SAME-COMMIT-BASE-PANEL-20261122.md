# PET-DETAIL30｜同提交PC宠物出生→升级→未加成面板可复现（2026-11-22）

## 起点、实证和范围

启动后核验远端主线 HEAD `da4c572dcfbfde7be9f82b78cf4fd7d3b1574248`、完整tree `a44c2af8a0600972b3f12c0c1c0dddef9631cab6`、最近提交/Actions、连续性协议、README和完整原 `docs/CURRENT-STATE.md` Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`（2,709,173字节）。本任务续 PET29 的唯一活动宠物模块，遵守经典2D PC、非手游、无收费卖盘、史实与后期社区源码分层。

本轮逐段复读 `gavinlinasd/StoneAge` 固定提交 `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56` 中的 `gmsv/data/enemybase1.txt`（blob a19a5089…）、`gmsv/src/char/enemy.c`（65e5a2e3…）、`gmsv/src/char/char_data.c`（924238fa…）和 `gmsv/src/char/char.c`（fcc14db9…）。这些是共享后代的社区经典PC源码，非1999、台湾1.0或大陆1.82原官方同部署代码。

## 单例可重演计算：2016后代模板ID1

使用同版 `enemybase1.txt` 首行、图形100250、名称「乌力」的模板参数：四BASE=20/12/15/25、INITNUM=10。**这只证明同源配置的数字，不证明早年TW1乌力的官服参数或游戏实发。** 在Lv1演示中 `(level-1)*LVUPPOINT`恒为零，现有模拟函数入参将该无关项显式置0，**不声称原模板LVUPPOINT数值是0**。

本次不是声称观察原随机数生成器：人为固定四随机偏移(-2,+1,+2,0)，出生十点按0/1/2/3轴分配为(3,2,2,3)，令存储成长BASE=(18,13,17,25)、`CHAR_ALLOCPOINT=0x120d1119`、Rank=5、Lv1内部能力(210,150,190,280)。已查2016同提交的 `CHAR_initcharWorkInt`，仅在**没有装备、状态、其他修正**的第一次基础能力计算下，得基础MAXHP/攻击/防御/敏捷=(14,2,2,2)。

随后独立固定升级新十点同一轴分配和Rank5档内倍率整数550；沿PET29已对C binary32验证的逐项计算，四内部增量为(115,82,104,154)，Lv2内部=(325,232,294,434)，`VARIABLEAI:0→500`，存储的BASE和Rank不被重新投掷。未经加成的Lv2基础MAXHP/攻击/防御/敏捷=(22,3,3,4)。所有数值是可复现的**指定骰值实验个例**，不代表出生概率、平均成长率、随机真实发放或早期1.0任意宠物基础属性。

| 阶段 | 内部V/S/T/D | 仅基础MAXHP/攻/防/敏 | 来源限定 |
|---|---|---|---|
| 后代模拟Lv1出生 | 210 / 150 / 190 / 280 | 14 / 2 / 2 / 2 | 模板+ENEMY创建+基础投影 |
| 后代模拟Lv2升级 | 325 / 232 / 294 / 434 | 22 / 3 / 3 / 4 | 固定十骰+倍率550+基础投影 |

## “基础面板”绝非实际游戏画面

同提交 `_CHAR_complianceParameter` 先 `CHAR_initcharWorkInt`，后 `ITEM_equipEffect`，再刷新WORKATTACKPOWER/DEFENCEPOWER/QUICK并执行 `Other_DefcharWorkInt`，随后还会夹带HP/MP钳制、图形状态等。因此 **MAXHP不是当前HP**；本次四值只定义“未经装备/特殊状态修正的内部基准”，不是实机最终K封包、截图、战斗面板。HP基础投影先计算C式 `(4*V+S+T+D)*0.01` 并落到C `float hp`，才转int；攻击、防御、敏捷按原C double表达式分别转int，避免再将有界理想有理数模型伪称C任意输入bit-exact。真正同平台/编译选项的全链可执行验证仍缺失。

新增 `project_pet_source_base_panel` 和单例/负例单元测试，复用既有 `project_pet_birth`、`advance_pet_growth`，不扩新的后期服务器装备系统。机读来源、明确指定骰值与历史限制见 [PET-DETAIL30机读收据](../../research/pets/PET-DETAIL-EVIDENCE30-SAME-COMMIT-BIRTH-LEVEL-BASE-PANEL-R1.json)。

## 止点与NEXT

新增早期认证同服PC模板0、原客户端实机数值0、早年官方全字段宠物0；原TW1具名候选仍124份PARTIAL、原头像120份，Stage A 7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79暂停、整体完成率仍未知。完整 `CURRENT-STATE.md` blob保留不改、不将后期同图号迁移为初代官方值。

**NEXT PET-DETAIL31**：有合法且确实可读取的早期PC同构建官方Pet主表/等级面板/服务器代码时优先实证；若继续没有原件，停止在后期社区版中无限研究装备/状态支线，回到宠物官方版本来源与缺失字段的批量归档，避免以技术辅助替代宠物模块复原。
