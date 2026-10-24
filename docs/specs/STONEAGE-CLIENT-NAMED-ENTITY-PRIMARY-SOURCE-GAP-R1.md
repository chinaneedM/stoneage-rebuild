# 《石器时代》同构建具名实体与原图形号：原件优先来源缺口验收 R1

**2026-10-24 | CLIENT-ARTIFACT-NAMED-ENTITY-PROVENANCE-01 | FACT/OPEN，非新游戏 DESIGN。**

本次从刚核的 GitHub main `0e450712b23d61ce54bc9e7fa230bef3df186aa1`、tree `21050bef2ffe4f4b11290822d6bb9066cd999022` 出发，按完整 `CURRENT-STATE.md` 最后NEXT执行。先核近期候选/main源工件、P2B真实全101项表、TW1.0实际写入起源、JSS一手截图/FAQ、2000韩国官方发行线索。目标为至少一个可审查的 **具名角色/宠物/NPC ↔ 同构建原始bitmap/SPR资源号**。**本轮未获取新官方安装包，也未恢复任何一个具名↔ID实证配对**；结果为有精确字段的取源阻塞，必须转入官方原包实字节资格，而非重复扫十个写点。

## 源层对照的实测结论

| 原始或可信一级来源 | 现有**可验**数据 | 尚缺而不可虚构 |
|---|---|---|
| 台湾Waei/JSS 1.0零售客户端与大陆5.0实际资源对照 | P2B直接101/101项原RD块、ADRN属性同ID同字节；每行 `original_npc_name`、`original_npc_id`、`original_pet_species_id` 均为null | 同构建NPC/宠物master、原始实例名、角色图形ID写入真实来源、原服出生NPC/任务脚本 |
| 台湾1.0原 `sa_3.exe`（SHA256 `cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a`） | 10处0x124原指令词法写点：7栈、2内存、1运算；独立主线保管收据 | 写点至同一R101 selector对象的完整控制流/实际原服报文、名称↔图形编号；十处并非十个NPC |
| 2001日本JSS官网介绍与pet FAQ | 2001 JSS官方介绍与10张真实可验原截图、涉及宠物界面；原FAQ有部分专名和BUG条目 | 1999首发/台湾1.0相同构建、图片上具名实体的原资源ID，原商服宠物master；FAQ任务名也不是任务脚本 |
| JSS 2001官网归档 `stoneage.exe` | 2001存档原字节217,088B、SHA256 `6795d9349168f77aa025d7c4ea05d005c5bbfe33dd4b227eb7731802fa7eb82b` 曾实取，只能证明更新器 | 1999游戏安装光盘的本体内容、角色/宠物映射，**不重复算新下载** |
| 韩国Inium/Hananet/CNET早期运营下载目录 | Hananet档号8119正式版`sa.exe`约260M、8120试玩`sa_demo.exe`约240M；CNET `Software_Id=200009263856`→约257MB `/pc/games/online/stoneage.zip` | 这三种原包**实际字节和SHA**、具体build、同版实体名称表及和TW1差异；目录链接不是下载成功 |

本轮交叉解析 Git 仓库中已有的真实原始来源**派生**表，将101项目中所有三种原服身份字段逐个验证为null；证实既有独立原件结果的界限而不是靠文字猜一批宠物。原像素/音频/商业EXE不入Git，不能以图块数量、同号跨版重用、网页名字、外设私服来源宣称“宠物数据还原”。

## 具体实物获取队列与止点

1. **KR 2000–01**：首先在经过鉴别的原Inium/Hananet/CNET存档或原运营安装媒介寻找完整 `sa.exe` / `sa_demo.exe` / `stoneage.zip`。需原URL链、完整包尺寸+SHA256、实际压缩/安装器内部文件级SHA、构建ID、污染检查。以**取得可独立验证新原包**或对确切档案端点形成带状态、日期的失败证据为一个有限单元；不要重复已有16次CNET零命中的Wayback API查询冒充全球丢失。
2. **JP 1999**：只有具实字节且可辨识零售/测试/更新级别的JSS原游戏盘或原发行文件才进入资源对比；2001 `SaUpdate.EXE` 的真实字节已获取，不能当作一套新1999客户端。
3. **TW1同构建身份**：正式官方物种/NPC/人物 `name`、`entity_id`、`bitmap_id|spr_group_id` 的原始表/调用日志，或同构建原程序名字取值及绘图选择完整实例证据；缺任一核心键留OPEN。旧P2B十写点词法分析有界关闭，新的原实物才允许重开。
4. **其它官方版本**：真实原件分别给地区、版本、渠道及文件级去重索引；同图形SHA的可重复使用只证明资源继承，不推人物/任务/宠物数量。活动任务仍须DD-028四档分开。

**当前专业判断**：具名绑定`0`不是游戏里面没有NPC/宠物，而是现有证据达不到“同构建原始身份↔物理资源”的门槛。下一NEXT为 `EARLY-OFFICIAL-CLIENT-ORIGINAL-PAYLOAD-QUALIFICATION-02`；一旦原装字节确证，优先原生master/selector链，不再靠网页玩家标签倒推。若原字节仍不可取得，在有限来源核查后转世界地图/NPC原服务档与其它22域，不生成无限地址扫描。Stage A保持7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79暂停，整局百分比null。

## 永久凭据与保管

机器审计表：`research/recovered/STONEAGE-CLIENT-NAMED-ENTITY-PRIMARY-SOURCE-GAP-R1.json`，列8份原始Git派生来源的blob锁、101行三身份空值审查、日方截图与韩方准确信息的取证边界；校验入口 `python -m tools.stoneage_client_named_entity_primary_source_gate`。未声称本次重取原JSS/KR/TW1字节或CI下载短期工件。历史记录仅通过CURRENT末尾新日期条增补，全部原前缀保留。若需更改早期资料，应新增纠错而非覆盖。
