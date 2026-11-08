# QUEST27：事件3／5的斧头交付、感谢函往返与原物品消失字段

2026-11-08（Asia/Shanghai）。QUEST26完成后，本轮继续相邻的真实任务内容，不以一个小检查结束。重新核远端main `7af65dbda8bdb6f2d1c2c02098283f187e817adb` / tree `d17d9dcaf27d22f80bcf4b3796a6921b1b11ffd7`，该HEAD的11项Actions全部completed/success；README追加接力和最高NEXT已重读，完整CURRENT2,709,173B/blob `c89e0e33537990aa2132b47c40fef49a985a935c`及四历史原样保留。

## 原文件关联，而非按任务号拆错文件

来源为后期社区mixed25保存本。原 `sainasu/event/event03.create` ordinal0位于floor1400/borncorner69,89,69,89，指向event03_2；ordinal1位于floor1300/borncorner18,42,18,42，指向event03_1，均精确绑定同原event.template的changeevent→ExChangeMan。**CREATE顺序与脚本编号相反**，方向、图别名、原块SHA完整保留，不按文件名推配置位置。

两份脚本同时承载事件3、5，共五TYPE段，均逐完整段/条件SHA同QUEST01。WORLD23已经有其物品传递记录；QUEST16的斧头/木材族没有这两文件，WORLD18是战斗入口/BGM材料，没有event03引用。本轮新增原脚本发现0，增量是双端来源定位、跨事件交付与原物品字段的具体整合。

| 来源关系顺序（非实际运行） | 原出处／ordinal | 原条件 | 原命令 |
|---|---|---|---|
| 领取原斧头 | event03_2／1，CREATE0，floor1400 | `LV>0` | GetItem2416 |
| 交付斧头 | event03_1／0，CREATE1，floor1300 | `NOWEV=3&ITEM=2416` | DelItem2416，EndSetFlg3 |
| 领取感谢函 | event03_1／1，CREATE1，floor1300 | `ENDEV=3` | GetItem2423，EventNo5 |
| 交感谢函取奖励 | event03_2／0，CREATE0，floor1400 | `NOWEV=5&ITEM=2423` | GetItem2448，DelItem2423，EndSetFlg5 |

物理顺序仍是event03_1先ACCEPT3再REQUEST5；event03_2先ACCEPT5再REQUEST3再MESSAGE。末条原 `ENDEV=3,ENDEV=5` 保留逗号，不解释成必须同时完成两旗标。命令省略数量保持省略；表中关系不等于任务运行、地图可达或原NPC操作已复现。完整原NPC姓名、对白和说明仅在私人页。

## 同图的两把斧头，原消失字段不同

原两份94栏物品表中2416、2423、2448三ID逐行完整SHA通过，同ID两表各自字节相同，仍保留六个来源行位置，不删除相同证据。按仓库已有**后代94栏schema**，零基第78栏名dropatlogout，第79栏名vanishatdrop：

| 原物品ID | 两表各自第78栏 | 两表各自第79栏 | 候选原图别名 |
|---:|---:|---:|---:|
| 2416 | 0 | 1 | 20041 |
| 2423 | 0 | 1 | 24222 |
| 2448 | 0 | 0 | 20041 |

原对白对第一把斧头“松手即消失”与奖励斧头“不消失”的描述，与该字段差异并列保留，**不是原丢弃实验、原加载器认证或概率/时间结论**。两把斧头共用同一52×35候选原RD PNG，不合并物品身份；感谢函候选28×39。台湾1.0原图与后期服务器物品表保持跨来源资格，PNG及RGBA逐一同ITEM01收据，助手实际查看两幅原候选图。本轮新RD解码0。

复用旧QUEST05对1300/1400的地图资格，不新取DAT、不画原NPC或自造行走路线；原物理条件和后代字段名不升级为JSS1999、TW1或大陆1.82官方同版运行事实。

## 交付与验证

私人ZIP **15,042B /14成员 / SHA256 `e68f61cdadd1a4df59ca2d92ee833b31e90226dbbc10610a30f30c0ab31c9ed2`**，含四完整原NPC/CREATE/模板、六原物品行、两候选PNG、来源报告和资料页。保存后二次回读整字节/SHA/14成员CRC一致；再次生成全部成员与公开报告逐字节相同。原正文和图像不公开。

独立原EventNo→EventEnd重分段核五完整SHA，直接原行读取再核六个表行字段78/79；四CP950原文全文、五HTML表行/三图片引用（两实际PNG）静态核同。8专项与全部314项任务相关测试本地通过。两批共享同一个原物品读取函数；重构后QUEST26默认报告和全部12私人成员逐字节不变，原发布收据不改。没有私人页浏览器、原程序或原丢弃执行，公开CI只校派生数值，候选/main须据实际结果补验。

**最高NEXT `QUEST28_MODULE_REVIEW_AFTER_TWO_COURIER_FAMILIES_SOURCE_STOP`**：两组村落交付达到来源止点，回任务模块材料复核，优先把剩余可取证的药草/药剂内容合成一批（`jaruga/event/event01_1/2` 与 `sainasu/event/nevent02_2/3/4`），先排除WORLD14、QUEST11与旧道具/任务目录已涵盖部分；保留后期1984药粉等原分叉，不把版本差异补为初代药草事实。有真实材料增量才批量恢复，不继续围绕单一CLEAN、SP、丢弃helper或同图斧头扩展。

Stage A仍 **7 PARTIAL+2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、任务起源 **UNRESOLVED**、总体百分比未知。本篇为CURRENT的追加接力，所有原历史保持。

## 实际远端验收

[PR #267](https://github.com/chinaneedM/stoneage-rebuild/pull/267)已合并。候选 `8abccae1149d57a79cdd8881660b091c7ff638f1` 的四项Actions（42479393593、42479396179、42479396414、42479396549）全部completed/success；内容主线 `8221bfbb411e002f393dacf6a0b01704c101f908` / tree `e246ea1efb3161105b52c43e438f7a00527591a7` 的[run42479454504](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42479454504)、job128727992612实际成功，日志含8项AxeLetterSourceEvidence通过。原生Git对六份完整文件和tree核同；首次核验早于异步fetch完成而查不到本地main对象，等待完成后重验成功，此为本地时序问题，非源文件或远端CI失败，记录保留于[验收收据](../../research/recovered/STONEAGE-QUEST27-PUBLICATION-ACCEPTANCE-R1.json)。收据自身CI发布后另验，不预支成功。最高NEXT仍为上述QUEST28药草/药剂批次材料复核。
