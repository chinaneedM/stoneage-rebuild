# PET42｜台湾早期华义宠物馆与同版零售盘：双向差异审计

2026-11-15。自 main `17ea207386378e83714b3cb1503555e95797494a` 的 PET39/PET41 **既有已核来源派生记录**增量对照。PET42 **没有重新获取**台湾商业原盘或网页 HTML 原始字节；只使用已归档的来源指纹及源限数据进行新的一次双向差异分类。保留 CURRENT 原 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`，2000 年审查仍 OPEN。

## 实际得到的未匹配边界

- 华义 2001 年初官方站所托管的玩家投稿宠物馆：**128 个网页编号，106 条与台湾 1.0 零售盘的名称逐字相同，对应 105 个不同客户端图号**；「克克爾」网页 0041 和 0103 复用客户端图号 100292。**不能当成 105 个已证官服实装宠种**。
- 原盘 `sa_3.exe` 宠物相册表：**124 个已命名图号**，其中 **19 个客户端原名没有在 128 条馆藏网页中逐字出现**。另有 **22 条网页名称不能和原盘名称逐字相符**。双方采用不同来源及不同时间的记录；22 与 19 不能直接相加当作新物种。
- 22 条中的相近字形、`(深)`/`(紅)` 后缀和「盜賊」等身份修饰只有**文本候选**。尤其「山賊」「盜賊」「小」等条目不保证是玩家持有的宠种。并非原客户端同构建之图像、服务器主表、出生/奖励/捕捉或原运行证据。
- 现有 PET39 原盘 124 条具名候选，PET41 网页 128 条馆藏都 **没有新增官服逐种实装确认**；2000 年全球种数仍 UNKNOWN。

## 22 条网页非精确名称与候选（仅便于未来按原图/同版记录回查）

此表的候选只按原名文本对照；`SINGLE_CHARACTER_NEAR_NAME` 不是字源或物种等同的鉴定。括号/前缀去除后得到的原盘名称亦非同身份定论。

| 网页编号 | 原网页名称 | 分类 | 原盘近名/去修饰基名（候选） |
| ---: | --- | --- | --- |
| 0009 | 布尹 | AMBIGUOUS_SINGLE_CHARACTER_NEAR_NAMES | 布比 / 100254；布伊 / 100256 |
| 0020 | 貝洛寶克 | AMBIGUOUS_SINGLE_CHARACTER_NEAR_NAMES | 貝洛洛克 / 100268；貝洛寶克爾 / 100269；貝洛寶利 / 100270 |
| 0037 | 楊奇洛斯 | SINGLE_CHARACTER_NEAR_NAME | 揚奇洛斯 / 100288 |
| 0055 | 邦洛洛克斯 | SINGLE_CHARACTER_NEAR_NAME | 巴洛洛克斯 / 100384 |
| 0065 | 布洛多斯(深) | ANNOTATED_BASE_TEXT_CANDIDATE | 布洛多斯 / 100351 |
| 0067 | 布洛多斯(紅) | ANNOTATED_BASE_TEXT_CANDIDATE | 布洛多斯 / 100351 |
| 0088 | 拉可拉斯 | SINGLE_CHARACTER_NEAR_NAME | 拉可洛斯 / 100383 |
| 0093 | 迪克牧 | NO_EXACT_OR_SINGLE_CHARACTER_MATCH | 无 |
| 0099 | 山賊志願的近 | NO_EXACT_OR_SINGLE_CHARACTER_MATCH | 无 |
| 0100 | 小卡 | NO_EXACT_OR_SINGLE_CHARACTER_MATCH | 无 |
| 0105 | 卡拉卡拉 | SINGLE_CHARACTER_NEAR_NAME | 卡拉卡利 / 100326 |
| 0106 | 卡拉寶斯 | SINGLE_CHARACTER_NEAR_NAME | 卡搭寶斯 / 100320 |
| 0111 | 山賊格魯頓 | NO_EXACT_OR_SINGLE_CHARACTER_MATCH | 无 |
| 0113 | 特洛加恩 | NO_EXACT_OR_SINGLE_CHARACTER_MATCH | 无 |
| 0118 | 盜賊魯尼帖斯 | ANNOTATED_BASE_TEXT_CANDIDATE | 魯尼帖斯 / 100282 |
| 0119 | 盜賊拉奇魯哥 | ANNOTATED_BASE_TEXT_CANDIDATE | 拉奇魯哥 / 100279 |
| 0120 | 盜賊魯尼帖斯 | ANNOTATED_BASE_TEXT_CANDIDATE | 魯尼帖斯 / 100282 |
| 0121 | 賊呼拔拔 | ANNOTATED_BASE_TEXT_CANDIDATE | 呼拔拔 / 100280 |
| 0124 | 怪力的小馬 | NO_EXACT_OR_SINGLE_CHARACTER_MATCH | 无 |
| 0125 | 鐵壁的小瑪摩 | NO_EXACT_OR_SINGLE_CHARACTER_MATCH | 无 |
| 0126 | 疾風的小秒 | NO_EXACT_OR_SINGLE_CHARACTER_MATCH | 无 |
| 0127 | 庫 | SINGLE_CHARACTER_NEAR_NAME | 鮑 / 100325 |

## 另外 19 条未被网页逐字覆盖的客户端相册名

- `100256`：布伊
- `100269`：貝洛寶克爾
- `100288`：揚奇洛斯
- `100320`：卡搭寶斯
- `100323`：卡克爾
- `100324`：巴克
- `100326`：卡拉卡利
- `100327`：貝魯卡
- `100328`：貝魯伊卡
- `100329`：格魯西斯
- `100330`：金格薩貝魯
- `100338`：多洛布斯
- `100351`：布洛多斯
- `100353`：布拉奇多斯
- `100361`：加寶格恩
- `100368`：克克洛斯
- `100383`：拉可洛斯
- `100384`：巴洛洛克斯
- `100392`：朵洛將恩（同盘头像 RD 缺项）

网页还有两组重名：`克克爾（0041、0103）；盜賊魯尼帖斯（0118、0120）`。网页编号、所引用 GIF 文件编号、客户端图号与宠物身份均是独立命名空间。

## 原件引用与下一来源门槛

- [PET39 同盘原 EXE→原宠名→原 SPR/头像证据](STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-20261115.md)，来源 Git blob `1aada81d7314769bf683b816cc5a8762c3bd9400`，原 TW1 源 ZIP SHA256 `3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24`。
- [PET41 华义旧站 13 页及入口、网页贡献者来源](STONEAGE-PET41-TW-EARLY-WGS-MUSEUM-20261115.md)，来源 Git blob `a01ca037b40c43ce542c7e2656bbaff3ececfb8f`。网页快照多在 2001 年，不能用 2001 年刊载信息倒推出 2000 年某日实装。
- [PET42 双向缺口机读表](../../research/recovered/STONEAGE-PET42-TW10-OPERATOR-MUSEUM-BIDIRECTIONAL-GAP-R1.json)保留 22 网页来源位置及文本候选、19 原盘记录 SHA 与图号，可供未来确切原图/官服同构建证据再核。原游戏商用字节、图像、服务器表均未提交 Git。

**NEXT PET43：** 继续**客户端优先**查找 2000 年地域分轨的 JSS 日本原客户端、Inium 韩国原客户端、华义台湾/大陆初版及补丁，先核原文件与版本资格；明确缺原件后才定向查华义 2000 年 8 月首套三宠卡实物及馆藏 JOT 奖品的运营方发放记录。不要反复泛查后来收藏文、新闻或用拼写相似自行合并。PET 仍唯一 ACTIVE，Stage A 7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，overall percent UNKNOWN。
