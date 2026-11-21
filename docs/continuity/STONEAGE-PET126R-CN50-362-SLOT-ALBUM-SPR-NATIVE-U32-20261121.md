# PET126R｜大陆 5.0 原经典 PC 全 362 个相册槽位、图形候选及原 `+24 → +36` 字段传递

**2026-11-21；唯一活动模块 PET，经典原版 2D PC。** 重新验证远端起点 `main=6964235cf22fe6d148eab5564309b24b035f9565`、tree `3effc7e82d6def2d1e5850af33bc5afbbbbd52f6`、完整CURRENT Git blob，并从旧PET126Q止点继续。第三方保存 CN5.0 `Stoneage-5` CAB 非已独立认证的当年官方原压盘，不等于该时代已实际发行的所有宠物。

## 可连续查阅的完整原客户端编译名称目录

原 `sa_5000.exe` 630,784B / SHA256 `5dbcc3fa276f9f245fb706bce957e9c3300d870df813889502b789b727e49c97`，源表362×28B / SHA256 `ba3ad4db233971ee5d9603cdbded6b871f73082445f1ca51d02f0fdf0314d39b`。同CAB `SPR-GROUP-R1.tsv.gz` 已由完整来源 SHA/manifest 固定。本轮原件静态重放 [Actions #44880073848](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/44880073848) 的真实EXE与合成检查 `success`。先前两次合成脚本修正的失败记录均保留。

- [PET126R 362 槽完整派生目录（JSON）](../../research/recovered/STONEAGE-PET126R-CN50-PC-ORIGINAL-ALBUM-FULL-362-SLOT-SOURCE-CATALOGUE-R1.json)：每槽含原编译名称（空位为 `null`）、物理行偏移、原行SHA、`raw_i32` 与 `raw_u32`、由台湾1.0版别提出的假设图号、本CAB是否存在该SPR及原SPR段哈希、与已认证TW1.0源段是否逐字节同SHA、证据否定标志。
- [PET126R 原件与衍生收据](../../research/recovered/STONEAGE-PET126R-CN50-PC-ORIGINAL-ALBUM-SOURCE-ACCEPTANCE-R1.json)：原SHA、真实来源Actions Run/job、保留初次失败、派生JSON Git blob、重开门与全部保守范围。

| 源来源维度 | 精确结果 | 解释限制 |
| --- | ---: | --- |
| 编译源槽位／具名／空位 | **362／305／57** | 源名不等于可获取的官方物种 |
| 具名槽位：以TW1 `100250+ordinal` 为待验图号在CN5.0找到SPR组 | **190** | 算术候选；未证CN5.0运行时选择器 |
| 空位下同图号假设在CN5.0找到SPR组 | **30** | 恰可证明图像存在≠已具名物种 |
| TW1官方零售源具名槽位对应CN5.0同图号且完整SPR段SHA相同 | **124** | 跨版资产继承强证，但并非同服物种和CN5.0本地选择器 |
| 其余未命中该假设的CN5.0具名槽位 | **115** | 不能解释为CN5.0丢失115种；待验公式本身可能不适用 |

**新真实源码证据，不是数值猜测**：该PE的 `.text` 精确含两处 `0x482f80`（相册表 `0x482f68+24`）的直接操作。`0x430bf0` 将其作为来源地址候选；`0x43476e` 实际执行形态为 `mov eax,DWORD PTR [eax+0x482f80]`，紧邻 `0x434774` 为 `mov DWORD PTR [edi+0x3300ccc],eax`，右侧属于原运行时记录基址 `0x3300ca8+36`。因此在**编译指令层面证实原相册末尾u32值直接移入本地运行时记录的 +36 字段**。尚未证明所有调用可达、具体索引的运行时身份、该值由渲染器消费，或它是实际SPR图号。未经独立认证，不把 fseek/fread、ADRN头像别名、相册文件头及真实发宠混为一个事实。

原 `.text` 中常量图号100250出现两次，但目前只是赋常量到对象字段，不可据此宣称本函数渲染本相册中的所有宠物。两个不同构建的相同段SHA是资产同一事实，不自动继承大陆服务器宠物数据、成长/技能、获取、出现日期及别名；原国家/运营/版本分轨保留。

## 工作止点／下一最高优先级

对当前来源足够证明的362条原客户端编译目录已全量存档并保留逐条查询字段，不需要再从网页复制同一批名字。**NEXT PET126S**：针对已证 `raw_u32→运行时+36` 字段，最多做一项明确的原客户端图像消费者同源证据核查；若找不到真正图形函数/原同服主档，明确有界停下转向现有 PET20／PET126F 七维来源有界最终审阅；官方在服实发宠物总数仍未知，不能被305/190/124代替。

原 `docs/CURRENT-STATE.md` **2,709,173B**／blob `c89e0e33537990aa2132b47c40fef49a985a935c` **未写改**；2026年 `NOT_YEAR_AUDITED`；PET `SOURCE_BOUNDED_PARTIAL`，Stage A 7PARTIAL+2OPEN，Stage B/wiki GATED，R79暂停，`overall_percent=null`；不切NPC或开始新游戏，也不公开原商业EXE、CAB、音画原材。
