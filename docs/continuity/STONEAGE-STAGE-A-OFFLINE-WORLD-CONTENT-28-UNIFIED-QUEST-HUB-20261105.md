# WORLD28｜原任务模块：统一私人原文入口及来源限定索引（2026-11-05）

## 本轮真实交付

在全新核验的远端 `main` `1292a92e09fc46162f31603969b3609f8514aa33` / tree `05a35e2bdbe33d52f9c60888a3b46c1a21c639d6` 上接 WORLD27 的最高任务。已从用户此前保存的私人 Library 取回 7 份原源内容阅读包并逐件校验整 ZIP SHA256、所有成员 CRC 与原 HTML SHA；它们之前各自的原文、图像和完整来源字节均**未被改写**。将原阅读器原样纳入单一私有自包含离线 ZIP，新增一张索引主页用于四档起源筛选、关键词查找、直接进入七个原文阅读器、独立查看已有运营活动史料。**不是新任务执行器，也不发明源外任务顺序。**

**私人交付** `StoneAge-WORLD28-private-unified-original-quest-library.zip`：323,915字节，SHA256 `7072e9180e46ab56af0f21733d0ae17ab0ca7f899bae1d66f660527c1cacde10`；其中新 `index.html` SHA256 `ffc673ef97bf7afbfb1814c6c0172402661c03b0268e4e1a0ed00d6d82d73887`。完整源脚本、版权图及私人 HTML **仅在交付包，不入公开 Git**。私人 Library 新包上传未得到可验证成功回执；本轮可通过本次会话下载归档，不虚称已入永久 Library。

| 可直接查阅的私人原文阅读器 | 保存源量及界限 |
|---|---|
| QUEST01 | 295份原事件脚本／315次创建引用／1,349控制段；不是315任务 |
| QUEST02 | 188份WarpMan原参数输入；不是原版实际传送 |
| WORLD14 | 9个制竿、3个交竿和1个MESSAGE；原奖励 `11872*2` 明确保留 |
| WORLD21 | 29个GetPet任务源分支、36个不同原敌人实例；不是物种数 |
| WORLD22 | 99条GetStone、16条DelStone；金额表达式不擅自求值 |
| WORLD23 | 410份原脚本共1,246个物品控制字段；不等于1,246个任务 |
| WORLD27 | 17份原脚本、97个DelPet字段、7个不展开的EVDEL、15次CREATE引用 |

任务来源按照 `docs/QUEST-ORIGIN-TAXONOMY-R1.md` 的 **BASE_GAME_QUEST／PERMANENT_VERSION_QUEST／OPERATOR_EVENT_QUEST／ORIGIN_UNRESOLVED** 四档分离。全部7组社区mixed25存档源仍为 **ORIGIN_UNRESOLVED**，不能因为文件路径含 `event` 或已有原文字就当官方初版或节日任务。现有可资格判定的运营档另列 R110、R111、R112、R115 和2004华义第二届全民狩猎大赛；其中R112是人工领奖**活动声称**而非原生可执行NPC脚本，2004 `race2/second.arg` 的同时期相似性仍不证明同部署。当前覆层中没有新增已认证本体或永久版本任务，并非证明历史世界不存在它们。

## 真实跨模块关系与否证

- WORLD14 的钓竿制作产物 **2432** 和 WORLD21 `poru/team03` 条件中的 `ITEM=2432` 是保存版相同数字的静态来源联接；其奖励 `GetPet=333` 为另一独立实例ID，不能推钓鱼任务实际前置或连续可跑。
- WORLD27 的 `PET=33-721*1` 是原交宠条件选择器字面，不得因数字相似即等同 `GetPet=333`、敌人模板或物种。
- WORLD14 两原脚本创建记录出现地图编号2000/4000，缺可证明的原出生中心坐标；不得认定原NPC确切位置、原世界可达性或TW1官方任务存在。
- 交宠97条含42条当前无直接创建路径的分支；不据此判为“官方未部署/可执行失败”。EVDEL与异常拼接原句均保留原样。全部原服发奖、扣物、历史保存ACK与原客户端操作仍 **OPEN**。

## 验收与下一项

私人ZIP整包 SHA、10成员CRC与七个原HTML成员SHA全部核对，独立 Chromium/Playwright 将同一HTML字节以 `page.set_content` 实际渲染：主页12条档案（7原文源+5独立活动档）、四档筛选、关键词搜索、7份原HTML分别载入，**0页面JS错误／0外部请求**。本环境 `file://` 和本地HTTP被管理策略阻断，因此不声称浏览器直接文件跳转通过，也没有启动原客户端/服务器。GitHub CI只验公开SHA与数字来源契约，**不能**自动读取私人原文或复制本机浏览器结果。

[公开机器来源／隔离收据](../../research/recovered/STONEAGE-STAGE-A-WORLD28-UNIFIED-QUEST-HUB-R1.json)固定原既有Git blob、私人原文包SHA、四档、五条运营活动、三条跨模块数字指向和必要负证。以前WORLD13/14字面顺序修正、WORLD09/23重复项订正、WORLD27无引用片段及所有旧失败记录全部保留，`docs/CURRENT-STATE.md` 完整 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 不改。

**下一最高：按内容模块轮换到另一个已有真实源、可恢复具体游戏行为的缺口。** 任务原源目录本轮达到当前已得资料的集中查阅止点；如取得同部署官方任务主档、原服行为或新的正版客户端，才增量重开对应任务。当前仍纯 Stage A 历史复原，7 PARTIAL + 2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING，整体百分比未知。禁止为这套静态资料再做通用DelPet/EVDEL编译器、原账号网关、新引擎或体验调整。
