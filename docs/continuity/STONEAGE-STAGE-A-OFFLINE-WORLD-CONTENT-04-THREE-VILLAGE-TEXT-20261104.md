# Stage A | WORLD04 原始三村落 NPC、告示文本与独立地图来源（2026-11-04）

本轮从全新远端 `main b60dc7bafabce6c1d47ccdeecab890df6f938274`、Git tree `2b52256d9e032f3e569ea74ca00731cc1475e97d` 开始，重读远端7项基础连续性资料、完整 `docs/CURRENT-STATE.md` Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`（2709173B）及上一WORLD03记录。**本文为新的内容复原止点，原CURRENT历史原字节不动**。遵循原版考据优先，不做账号/网关/真实服务端模拟、新石器开发或体验优化。

## 三村落原保存内容的实际实物核验

本轮真实重新读取私人 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip`，完整995176B/SHA `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`，ZIP全部2205成员CRC通过。按原CREATE大括号实际字节区间、楼层、`enemy` 的精确模板键`npcgen_man`／`npcgen_signboard`以及确实存在的同包 `file:` 原件联接：涉及**11份真实CREATE文件、47条有效CREATE和47个不同ARG原文件**，所有原文本CP950可严格无替换解码再逐字节往返，总外部ARG原字节**5634B**。

- **2000地图（源路径为marinasu／玛丽娜丝）**：10条TownPeople、4条SignBoard，共14；
- **3000地图（源路径jaja／加加）**：13条TownPeople、4条SignBoard，共17；
- **4000地图（源路径karutana／卡鲁它那）**：12条TownPeople、4条SignBoard，共16。

这不等于47个原官方时点已出场的不同人物、47次玩家真实对话或47个独立任务。上版CHAR07已公开索引其中46条的原ARG SHA，本轮按`楼层|CREATE路径|原块序号|ARG路径|ARG-SHA`原顺序完整重比46/46相同，规范ASCII键序列FNV1a32=`a53e22e0`，未重复宣称46条属于首次发现。**一条额外原创建配置**在旧CHAR07这批没有纳入：`genout/shop_m.create`源块第95项、2000(87,78)、图号字段10061，`npcgen_signboard`，对应`genout/signb_2000_87_78`（只有**1B LF**，整SHA `01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b`）。可读公告文字**实际位于原CREATE `name` 字段**，其中有4个字面反斜线n；原CREATE全文件SHA、原块SHA和原NAME摘要可在[本轮公开证据记录](../../research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-04-THREE-VILLAGE-NPC-TEXT-SOURCE-R1.json)核对CHAR01旧源码注册表。本批**仅补一条CHAR07范围遗漏，未修改旧567/552历史统计或静默扩成全版本NPC人口**。

按原文件实际文本，可见航空站、飼育员、海底通路等世界设定相关字面；这些都只是当批保存源中的叙述，**不是已在某正式历史服上线的场景、活动任务或剧情执行证明**。全文和CREATE名字只放私人包；公共Git仅文件SHA、原块来源、坐标、源图号、文本长度与字面符号出现次数。

## 三楼层地图来源资格

这47项的原CREATE中心坐标全部位于150×150范围内，分别用原MAP01登记的`2000.DAT`、`4000.DAT`（早前整CRC/SHA实证）及[独立两解压器已复原的`3000.dat`](STONEAGE-STAGE-A-INDEPENDENT-RAR-MAP-PIXEL-RECOVERY-20261104.md)文件身份证据核对。公开报告分别保存完整DAT SHA/CRC/大小/图幅、内容来源；**本轮没有再次读到这三份原DAT的完整格内容，没有凭坐标生成原图像、原碰撞、事件触发或地图名官方身份**。原文件全部属于后期社区 mixed25 保存载体，绝不转称JSS1999、台湾1.0、大陆1.82同版本同部署。

## 私人实际文字观察成果

已完成一个单HTML本地原始文字资料集，三村落源坐标图谱（**现代标记点不是游戏画面**），原CP950全文与`name`字段逐条查看、地图/村民/告示/任意原字检索，并对缺ARG正文但NAME中内联文字的竞技场告示给出明确提醒。

- 私人包：`StoneAge-World04-three-villages-original-dialogues-private.zip`，**28955B**，SHA256=`ddcc7879a5ea91cc63e5f41b338e5730953a2817608fad93c19d233fc90ca3b2`，含完整原文索引/原HTML/来源及浏览器核验收据；原商业文字不入Git。
- 实际Chromium 144.0.7559.96以`page.set_content`载入同字节HTML，已进行**16项**检索、筛选、文本替换、原例外、地图坐标选择等测试，**16/16通过**、0 JS错误、0外部HTTP请求。它是现代本地资料工具，不是原客户端已在当年运行或进入游戏。
- 公开 [47条来源受限目录](../../research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-04-THREE-VILLAGE-NPC-TEXT-SOURCE-R1.json) + 新CI测试只在 GitHub 上重算过去来源文档、文件摘要、坐标/数量闭合及范围反例；GitHub Actions**不读取**私人原NPC ZIP，也不能代替实际私有原文本核验。

## 后续优先级

**NEXT STAGE-A-OFFLINE-WORLD-CONTENT-05**：本批三村落源文字46旧+1补漏完成，下一项换宠物／任务／物品真实源关系（必须有已取得的实际原件及版本资格），不回到单一村庄窗口、泛用观察器、旧网游账号/联网服务端。保持Stage A **7 PARTIAL + 2 OPEN**，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，overall_percent=null。
