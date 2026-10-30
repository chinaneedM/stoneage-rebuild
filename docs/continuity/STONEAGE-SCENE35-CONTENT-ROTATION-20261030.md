# 2026-10-30 — SCENE35：遇敌内容卡按证据止步，轮换交付一条原NPC对白

启动重新读取远端main `26ce92ab771bf9607aee9e14e00b132e3161bf8c` / tree `c12b66639c49f7d129bcd0d886e13ce47fb15abc`、完整6573项tree、最新五提交、0开放PR、最新收据41004119243实际completed/success，核协议和七启动文件、路线/22域/R102及SCENE34最新覆层。本地正常checkout与fresh HEAD一致；完整CURRENT2708031B / blob `20050acf279a01555ab06a381dfcdc936bd381a6` 逐字节核同，README旧123389B保留为完整追加前缀。依协议14使用本覆层，不改写历史正文或旧止点。

**实际结果：遇敌卡没有建立；转第6/7域，完成一个有明确静态引用的76字节NPC对白内容卡。** 来源为已有社区混合2.5保存包，不是新取得官方发行物，不是原客户端/服务端运行，也没有进入原世界。

## 遇敌候选为什么停止

先重读 `STONEAGE-25-ENCOUNT-CHAIN-R1.txt`、`STONEAGE-25-ENCOUNTER-CHAIN-PROBE-R1.txt`、WORLD01四出生地及旧内容覆盖。660行encount、1257行group的链/残缺引用和四条模型路线早已有限审过；没有重新把它们计为新内容。

复用已保管RAR361255180B / SHA `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`，本轮真正取出四表与setup.cf，逐整SHA与R18/SCENE33相同。四表均0条#注释，第一非空记录字段数分别33/24/34/56；这只是字节形状，不认证列名或原生语义。旧链报告明写字段解释来自后代ENCOUNT/GROUP/enemy代码。本轮没有取得这些列与此原GMSV二进制同构建的字段布局桥，所以不凭列数、同名文件或已有模拟器把它晋升为原服规则。止点为 `NOT_BUILT_SOURCE_FIELD_LAYOUT_UNAUTHENTICATED`，不扩列语义逆向/新遇敌模拟器/四路线helper；不是否定旧后代模型成果。

| 原表 | 字节 | 原完整SHA256 |
| --- | ---: | --- |
| encount.txt | 43420 | 70bbd997d98508a0587df183b5bdd48222ff42db91bf21bea632e0ed6f2fea87 |
| group1.txt | 70176 | 4a02f2a3fa3d2dcf5589d8a2a560313c35d5a0a7e5e0589cc8df5f7df159ea8f |
| enemy.txt | 222463 | cc7418d3b6726f1c458fef9e44a24696d05f076b67c62a56ed2293e26ae63bb6 |
| enemybase.txt | 147750 | 1be7d5226798f7abaabe1f1e74aa1533fcd10e3eaf43f6497d63afa91df3e8b7 |

按上一包允许的“具名停止并轮换领域”，改取同包NPC明文键。这条链不需要猜CSV列：原创建文件本身有floorid、borncorner、enemy、graphicname等显式键；再按原enemy声明取唯一模板/文件，止于可读原文。

## 一条真正可查阅的静态内容

| 原件 | 字节 | SHA256 |
| --- | ---: | --- |
| npc/genout/1000npc_m.create | 4413 | c9b000a836b0aae3d88358097039f1beea020d92ba84f6ccc338bb54bc478240 |
| npc/genout/npcgen.template | 4950 | 0c5a58d5e31cafd3b58ccc1fa88fee7d1f95d12c0b87b04db9f06fea3b2a4df3 |
| npc/genout/msg_1000_128_36 | 76 | 147fd7ad70d8fcc81a1cf3b525a3b5a248f1f1eabdcd54725f361a94ad42e46e |

原创建块0起序号17、字节[3075,3240)，块SHA `87b9666c06fb4660b0634a0c5321f63a9aa0459289ff6ccbfd91578ce1f92aa7`，明确floor1000 / borncorner128,36,128,36，graphicname16009、dir6仅保留原整数，不翻成方位或bitmap。`enemy`精确指向 `npcgen_man|file:genout/msg_1000_128_36`；模板唯一同名并有functionset=TownPeople，模板块SHA `5f24ae6f815471af9439ed4b824ae494006a8ba6fb7e4bac43b44b8ae5a89b29`。这是原文本静态引用链，不是函数已执行或同部署认证。

原姓名只在私人卡显示，公开为10B/hash `e92c8ad7f5e67ed5fb0e299f7f7ad7aae06e98d2157215d6a38bfeb5fe731aa8`。编辑简体释义：**少女提到自己睡着了，并好奇对面隐约可见的岛屿上有什么。** 岛名、路线、可达性和任务条件未得到认证，不能据这句话造一个任务。任务来源仍 `ORIGIN_UNRESOLVED`，新增认证任务/奖励/保存标志为0，不把常驻NPC文件名当本体任务分类证据。

原76B中有一个ASCII逗号、一个末LF、无CR；解码39个codepoint。去掉末LF后两个字面片段依原顺序为22B/52B，各整SHA分别 `c30c3647a06279522b131db21984156d97ffa84ace2471b2d67c04439db5e661`、`4c192d61fbb0e8b0690b0cfc592cfb38a9e86f8325b29d66ce1815a17a9e2162`。这与SCENE22的143B/0逗号另一文件不同，不把同模板算新发现，也不把两个字面片段说成两个已运行分支、按序/随机发言或两个选项。原UI与运行选择仍OPEN。

## 原字节核验与私人交付

本轮八个目标源成员共502963B：四表、setup.cf及三NPC文件。系统libarchive经ctypes实际静态解出，全件SHA对R18或SCENE33；独立标准库RAR4头解析扫描7952项文件头（含目录记录），核头CRC、八目标成员CRC及压缩载荷SHA。头解析不是第二解压器，本轮只声称一套成功解压实现。没有执行历史程序，也没有为摘要重下游戏载体。

选定姓名/对白CP950往返且Big5同解；另一iconv实现对完整76B得到相同UTF8，SHA `704c3086b6ad319b4296de8d776e4d1d4db764ad8a9e2de607af6669cb1d5ed6`。私人HTML的原名/完整原文经HTMLParser与另一路元素提取还原相同文本，保留原末LF、逗号和两个片段位置。静态页无JS、无外部资源，未做浏览器运行认证，不使用原美术或冒充原窗口。原文繁体保留，现代说明/操作使用简体。

私人包 `SCENE35-private-seaside-dialogue-card.zip` **11122B / SHA `22fd53e1eb8343ff265dd95a3b1def5b408c317a17ed75c0106a52308bc16ccf`** 已成功保存，身份元数据已应用；没有保存后二次回读，不虚报耐久副本二次SHA。含reader.html、三个完整原NPC文件（9439B）、私人源说明及派生报告，共六成员；不含setup.cf认证值、其它四原表、原程序或图像。保存前三原件全SHA与全部ZIP CRC已核。用户解开后可直接打开reader.html查阅；这只是现代原文卡。

公开仅 `STONEAGE-SCENE35-CONTENT-ROTATION-R1.json`、`STONEAGE-SCENE35-PRIVATE-CARD-AUDIT-R1.json`、工具/反例及本说明；原文、原姓名、原创建正文与私人HTML/ZIP不入公开Git。来源早已保管，这次增量为一条未展示内容的有限查阅与解释，不是新发行材料或整个村庄NPC恢复。

28项新检查和29项SCENE34回归本地通过。公开CI只核冻结派生报告与合成文本的转义/顺序/空片段/字段/范围反例，不读取原RAR或对白、不运行旧程序，source_action_run_id=null。真实候选与主线Actions按后验另记。

## 下一最高与保留边界

本NPC卡与遇敌候选各自到止点；不扩本村25块全部对白/人物图/场景模拟器。遇敌卡重开需同包二进制字段布局或其他可认证同构建字段说明，不以同列数或已有后代模型为触发。

**最高下一：SCENE36-RIDE-MATERIAL-DELTA-REVIEW。** 回22域第15域，先重读已保存的大陆4.0骑证/庄园、台湾8.0骑宠及其来源目录，查是否还有版本/地区明确、未实际交付的一项骑宠资格或界面内容。只取官方原文/客户端实物有据的一小条内容；已完整交付则具名去重并轮换，不重写旧目录计数、不默认1999/TW1已有骑宠、不把运营活动与常驻资格混为一类。用户“第一次骑上宠物”的体验诉求留待后续设计，不提前生产新游戏。没有新实物/正文就停止这一候选，不扩骑宠helper。

SCENE34原SAAC/GMSV启动仍 `BLOCKED_PRIVATE_INPUT_CHANNEL`，没有新传递能力，不重开隔离链。原世界未进入；Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79暂停、overall_percent=null保持。

## 远端最终验收

PR [50](https://github.com/chinaneedM/stoneage-rebuild/pull/50) 已合并。候选 `5311dadaf50bcc0614f6ec28bb2b7ae5708687c3` 的12项Actions、主线合并 `0c59d65dd2da070c9063c12332865e5edc50f421` 的11项全部实际completed/success；整tree `5e69012f690087b3d672be382c4db880e1f5f752` 与本地已验tree及PR临时merge tree完全相同。专用候选41006411855/job123902207021、主线41006531717/job123902576706原日志各核28测试OK与遇敌未建/世界未进入的冻结范围。七内容文件SHA/Git blob、23项验收、私人卡摘要及保存/未回读边界固定于 `research/recovered/STONEAGE-SCENE35-PUBLICATION-R1.json`。本后验收据自身提交不冒领前述23项成功；没有新原源Actions或私人原文CI执行。

下一SCENE36的现存输入已具名：`STONEAGE-CN20-RIDING-TRAINER-COMBAT-SOURCE-R1.md`、`STONEAGE-CN40-RIDING-CERTIFICATE-MANOR-SOURCE-R1.md`、`STONEAGE-WAYI2003-NEWBIE-RIDING-PLAN-R1.md`、`STONEAGE-WAYI2003-RIDING-SUCCESSOR-ORE-WORK-R1.md`（均在docs/specs），及 `research/recovered/STONEAGE-TW80-MOUNT-CERTIFICATE-EQUIPMENT-SOURCE-R1.json`。先实际读取这些旧正文和来源再判断增量，文件名/版本数不算新材料；不重开本NPC或运行helper。
