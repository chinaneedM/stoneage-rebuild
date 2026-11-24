# PET-HIGH-FIRST-13｜台湾保存 8.5 长动作及特殊 RD

本轮从 main `73ef393d5eb6fabf2e3eb3056cde39c0d83752c6`、tree `5fbd06b7da522ecf14d4c5ffd88e85b4b81471aa` 启动。47/47 Actions success，开放 PR 为零。完整历史 CURRENT blob `c89e0e33537990aa2132b47c40fef49a985a935c`（2,709,173 字节）保持不变。遵循协议 §27，仅经典 PC 宠物，资源高至低、历史早至晚。

## 真实原容器及双解码

[源 Actions 45347088529](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/45347088529) 已 success；六分卷全部校验，静态提取同包四原文件，重验原 SPR 派生表及 RD 散列。来源仍是保存包而非独立认定官发盘。机器凭证由作业写入 commit `b47c2ef56655ece553ec6bd193331ce31b3eaeb7`，Git blob `97fb8ffecda20d139ce0e72b7fb3548ef72d98dc`：[逐组和特殊头凭证](../../research/pets/PET-HIGH-FIRST-13-TW85-LONG-AND-SPECIAL-R1.json.gz)。实际原像素及公开派生回放摘要一致，旧像素回归3项通过。

| 指标 | 结果 |
|---|---:|
| 本轮物理组 |20|
| 原帧位置 |642|
| 帧物理块 |612|
| 12个长序列中完整组 |10|
| 8个既有失败组中找到完整替代样本 |2|
| 累计至少一段完整的具名物理组 |510/518|
| 原头像完整双解码 |207/207|
| 既有特殊RD诊断 |7|

本轮头像及取样共有819个物理块，810双解码，7拒绝，2不支持。原失败不删除；另有两个长序列未完全通过。累计仍有8个未获完整样本的物理组，不等于8只宠物；510/518也不是全帧、全种数或整体项目完成度。没有图像、音效或原商业二进制提交 Git。原始头与失败原因保留，未猜测负高图方向或修剪 RLE。

## 同期发行证据

[华义2005-11-10新闻稿](https://www.wayi.net/service/files/fd350e9ce1c9b635011fcba84d1e198d.pdf)（民国94年10月营运概况）索引全文可读，明确次年狗年兽规划。原PDF直接页面渲染403，未取得可认证字节或截图。可证运营方预告时间，不能证四个名字、逐宠实发或首次上市日。与2005-12-22后期编年记载、2006新年祭原活动独立分层。[机读来源](../../research/pets/PET-HIGH-FIRST-13-WAYI-2005-DOG-ANNOUNCEMENT-R1.json) · [年兽逐宠资料](../pets/TW85-YEAR-BEASTS-2004-2006.md)。

## NEXT PET-HIGH-FIRST-14

有限核验8个未闭合组的原图块解释：优先以同包原静态解码路径或其他原版本同字节图块证据确定特殊编码；无证则记录无法支持，不人为补像素。继续查台湾高版原同部署宠物主档、发行、技能、成长和取得；没有证据的字段不填。PET唯一活动模块；Stage A 7 PARTIAL + 2 OPEN，Stage B/wiki GATED，R79暂停，总体百分比UNKNOWN。
