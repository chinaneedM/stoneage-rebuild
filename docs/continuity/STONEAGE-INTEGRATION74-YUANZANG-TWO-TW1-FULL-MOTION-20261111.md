# INTEGRATION74｜願藏桥上对手与两组台湾1.0原二维完整动作的来源限定对照（2026-11-11）

## 启动核验及真正增量

按 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` 从真实远端 `main=ad2e6efd586231eff46e016b4a99539f1d316b76`／tree `8fc03d5627cfa395b83fe284ce3b5345e194b1fe` 启动；26/26 当时该HEAD Actions 已实测 `completed/success`，开放 PR 0。重新读 README、协议、原生完整 `CURRENT-STATE` Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`（**2,709,173B**，普通正文接口空值不能解释为文件为空）、设计/历史/来源、路线、模块与最新 INTEGRATION73 回执。完整历史 CURRENT **不修改、不截断**。

本包针对 [O85 已证原人物与敌人主表关系](../../research/recovered/STONEAGE-O85-YUANZANG-DIALOGUE-BATTLE-SOURCE-R1.json)缺少的独立**完整原二维动作可观察链接**。重复检查 [PET07](../../research/recovered/STONEAGE-PET-MODULE-07-TW10-BATCH-PUBLIC-R1.json)和 [PET15](../../research/recovered/STONEAGE-PET-MODULE-15-TW10-ALL-SELECTED-MOTION-SOURCE-R1.json)后确认：100280、100401 原台湾1.0 SPR 段的**整个动作已被 PET15 覆盖**。因此本轮**新原图发现0、全新未整理动作0**；实质成果是把这两组已可真实回放的**104+56个源动作/方向和原位图**，与 O85 同社区保存载体的两条具名敌人模板和原 NPC CREATE/战斗配置逐条带出处连接，并做一份新的可查私人联合原图观察。不能重复记为新宠物或新史料。

**材料版本严格分离：** `100/sb_ganzo.*`、enemy/ enemybase 是后期社区保存 mixed25；独立 P3H 原SPR/ADRN/REAL 是经既有来源认证的台湾 Waei/JSS 1.0 零售客户端。**同图号仅构成跨载体数值/画面候选，不认证JSS1999、台湾1.0或大陆1.82的同部署 NPC 身份、战斗行为或实际宠物身份。**

## mixed25 原 NPC、实例与模板（新实读三个原小文件）

从个人 Library 重取 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip` **995,176B**／SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`；全部 **2,205/2,205** 原成员CRC通过。真正读取 `npc/100/sb_ganzo.create`、`.template`、`.arg` 原字节，三者完整SHA分别 `db26d1b901588f8f1db8d4241ca5d01162bbfb5d4b8dde392b6e08526eb34746`、`96294485dfe3f793d2ff8592d446d53e1a8e0a4824a8aede41bf18e6fa3569d7`、`2044b2167ce4826ab949d88effcf4294004da866950c4f81d97241da03779426`，与 O85 旧精确原件记录一致。原 `CREATE` 为 floor **100** / `borncenter=472,297,1,1` / `graphicname=100401`，模板 `functionset=NPCEnemy`、`type=100401`，ARG 原顺序敌人实例 **253、254**。不从注释行导出真实战胜传送，不把 `time=60` 解释为已证秒数。

既有 O85 原 enemy / enemybase 原实体及原逐行 SHA 各自保留，含**不能擅改的同源名字差异**：

| 社区原实例 | 实例名字 | 关联原模板 | 模板名字 | 模板原 `graphic` |
| --- | --- | --- | --- | ---: |
| 253 | 壞心眼的願藏 | 500 | 壞心眼的願藏 | `100401` |
| 254 | 呼拔雄 | 501 | 呼拔吉 | `100280` |

本轮未重新拿到 O85 所用的完整 `enemy.txt`/`enemybase.txt` 父 RAR 成员，**两条主表原行只以已发布 O85 实物来源SHA及其记录为证**；不谎称新重读那两主表。村落三份愿藏对白前轮也已经源证合格，本轮不是新获得剧情。前轮 floor100 DAT 完整源仍因保存包CRC/过滤器问题而 OPEN，不凭 NPC 坐标声称画出了实际桥、地图、NPC战斗现场。

## 台湾1.0原始SPR动画与真实RD原像：今次独立整批核对

重新取完整私人 `StoneAge-TW1-original-runtime-and-native-observation-P3H.zip`，**372,626,292B**／SHA256 `3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24`；**379/379 ZIP成员 CRC** 成功。原 `spradrn_1.bin`、`spr_1.bin`、`adrn_1.bin`、`real_1.bin`、`Palet_1.sap` 均整字节/整SHA与旧认证吻合。按12B原SPRADRN、原SPR动画头12B+逐帧10B、原ADRN80B和真实REAL偏移/长度逐项重放，整段SHA与 PET15 旧报告和 PET07 组号源证吻合：

| TW1 数值图号 | SPRADRN序号 | 整SPR源动画 | 原帧位置 | 不同原bitmap | 原方向/动作 |
| ---: | ---: | ---: | ---: | ---: | --- |
| 100280 | 270 | **56** | **288** | **232** | 8方向 × 7源动作（0–4、9、10） |
| 100401 | 364 | **104** | **496** | **344** | 8方向 × 13源动作（0–12） |
| **合计** |  | **160** | **784** | **576** | 不能当160个角色/576个新宠物 |

原REAL重新精确读取这 **576 个不同RD块**：575 strict RD成功，另 `bitmap 82729` 源RLE收尾多一个零而真正图幅 `width*height` 范围完整，独立限定为 **`bounded_terminal_zero_outside_canvas`** 并保留原异常；不把它列为strict或修改原字节。576幅 Palet1 **现代候选** PNG重生并在私人ZIP内留来源SHA、画布像素SHA和尺寸。早先PET07有**31个RD/ADRN/像素源重叠**，本轮31/31原RD SHA、ADRN SHA与原像素索引 SHA 都等于旧私人报告，解码后 RGBA **31/31全同**；原PNG文件字节 **0/31相同**，是本轮调色板索引 PNG 与旧 RGBA PNG 文件编码不同，不能把这种字节差异误报为新的游戏美术或色彩变更。

源既有PET15含**这全部160条及576 bitmap**；本轮新创建576幅现代候选图不是史料增量。两个图号在混合25 `enemybase` 里还被其他 PETFLG=1 和PETFLG=0的模板复用：同图号不专属于上述NPC，也不证明宠物物种、玩家可获得的宠物或真实战斗调用图。原二维骨架/原每帧数字可查，原客户端如何选择、精确FPS、透明度、场景配色、历史角色身份均 OPEN。

## 私人源保管与公开回归

私人 `StoneAge-INTEGRATION74-Yuanzang-two-TW1-SPR-original-private.zip`：**1,826,064B / SHA256 `6ffb64f62b74674d0e5c099149001c739137cb1bf2bcdc25ce86ad725c8b2563` / 581成员**，包括三份原NPC小文件、576张台湾1.0原图候选PNG、全部动作/原RD来源清单以及简体中文离线观察页。已存个人Library `/石器时代/`，随后从独立物理路径回取，整字节/整SHA相等，**581/581 CRC成功**。版权图片、原完整脚本、REAL/SPR原二进制和私人HTML都**不在公开Git**。

本轮将**同一HTML JavaScript**改用内存PNG data URL（仅用于测试，原私有ZIP的 `images/*` 链接原样保留），在Chromium里真实走通 **160/160** 个动作/方向选择、576张图片来源无坏项，0 JS错误、0外部网络请求。本环境 `http://127.0.0.1` 和 `file://` 导航受浏览器安全策略阻断，所以**没有声称打开私有ZIP内真实file://页面成功**；浏览器测试的是等价内存加载，不是旧商用客户端运行。

公开Git仅写[完整派生动画/逐物理位图证据与跨载体负证](../../research/recovered/STONEAGE-INTEGRATION74-YUANZANG-TWO-TW1-FULL-MOTION-SOURCE-R1.json)、专项正/负测试、工作流和日期加法记录。CI复算已发表 O85、PET07/PET15 的真实数值、全部160动画/序号/帧SHA与31组旧RD，**CI不能访问本次私人REAL或图片**。候选与主线 Actions 必须真实验收成功才可写结果；此前旧CI失败史保持完整。

**止点／NEXT：** 本愿藏具名敌人↔源SPR关系已达到来源限定止点，仍是历史Stage A **7 PARTIAL+2 OPEN**、B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**，总体完成率 `null`。从未执行原客户端、原战斗或原服务器。下一包轮换一组**不重复且有真正原始地图、NPC、宠物或道具的实际新增关系**；不扩纯辅助解析器/网络账号/新单机引擎。只有获得 floor100 原DAT完整资格、原客户端实测或新同版官方主表时，才重开受影响的原生身份和路线问题。
