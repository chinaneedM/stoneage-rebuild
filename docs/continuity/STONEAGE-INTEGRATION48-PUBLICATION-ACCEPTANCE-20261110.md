# INTEGRATION48｜四村长毛象快递原条件、两份私人来源与主线 Actions 后验验收（2026-11-10）

[独立原脚本核对和停止条件](STONEAGE-INTEGRATION48-FOUR-VILLAGE-COURIER-SOURCE-CONDITION-20261110.md)；[只含来源数值/哈希的永久派生索引](../../research/recovered/STONEAGE-INTEGRATION48-FOUR-VILLAGE-COURIER-SOURCE-HINT-ACCEPTANCE-R1.json)；[PR #316](https://github.com/chinaneedM/stoneage-rebuild/pull/316)。

## 真正远端起点与安全边界

本轮按协议从 GitHub main HEAD 94849761d3b858b4f76b312a5debe14e037f2b31，tree 794bce40809fc3c6239e9ddf0817ea1121d66928，重新读取协议、README、设计、历史、来源登记、路线、模块队列、最新 INTEGRATION47 收据及原历史 CURRENT-STATE 的**整个原生 Git blob**。CURRENT-STATE 原文件**2,709,173字节**／blob **c89e0e33537990aa2132b47c40fef49a985a935c**完整保留，不执行任何替换。

私人 QUEST06 源ZIP实读40,204B、13成员CRC均通过、SHA256 cd26689805ad0c40e23ef934aa7c9509fe461630dd0431f7a43740abd7c91254；原5个 NPC/任务文件逐完整SHA、CP950重读、8 CREATE、4×6 TALKEVENT、6原候选PNG实读SHA与既有私人收据一致。本轮材料是**社区混合2.5保存来源**，不是认证早期官方部署；候选PNG属于另一保存载体的台湾1.0零售图，不能称两者同官方服务器显示。另私人 QUEST31 原ZIP实读27,565B／26成员CRC通过、SHA256 796682fd3621a2bfecab03e7e199ca16936f95cad75f6a7842e6517f1e04dd42；原CREATE路径/整SHA与QUEST06不同，不能误并为同一“四村”任务。原商用脚本、对白、物品表行和图片只私人保留，没有进入公共Git；本轮没取得新原DAT或新增原RD像素解码。

## 新证据交付的准确范围

四个来源脚本原TALKEVENT2/3正向ITEM提示按原数字匹配TALKEVENT4/5的接收条件，形成**8条有来源的静态匹配边，不是执行过的送货/物品发放路线**。第1阶段四验收物品2622/2623/2624/2625，对应正向提示项2622/2623/2624/2622：2622重复、2625未在本四脚本正向提示出现；第2阶段四验收4212/4224/12874/12879，正向提示4224/12879/12874/4224：4224重复、4212缺提示。不可画成完整四村环路，不证明原物品无获得渠道，只有源限定OPEN。

四脚本NOFREE原值LV>30，其余提示LV<30和1—9/10—19/20—29三段列举，数字LV30没有本批显式条件覆盖；没有测试或证明原服LV30真的不能接任务。四宠物段的两种原字符串PET=1-13、PET=1-292都未见DelPet，不能推历史上消耗宠物。原奖励数字1000/1000、2000/16000、5000/81000只是静态脚本命令，不是游戏执行结算。8物品原行/跨版6原PNG候选仅可追源，4212/4224共享图号20407不等于同一物品。原地图来源资格引用QUEST06旧报告，本轮8个原DAT字节并未重新读取，原地图不冒称已进入或实绘。

## 候选 → PR → 主线实际 CI

- 候选分支 agent/integration48-mammoth-courier-cues-20261110，HEAD **63bcad1fcedaa578870facb6d679c6720a678bc6**，tree **cbfcc53a0bee1aba0ec79ffdf5682ad85755ca84**，相对源起点只修改README并新增4源限定文件：索引 JSON Git blob **3186c78865156648caff78f5892cc40c4968d0b6**，测试 Git blob **9e7079d1e1a29d1c496ccaa3b4818220ac1b4ce5**，连续性文档 **cac1561d5972502666421cff0c01929eb83777bb**，workflow **b6dde36d6449e19772de5012fe00ae773c3fd646**。四Blob与本地git hash-object完全一致，历史CURRENT blob未动。
- 候选 **27/27 push Actions completed/success**，专项 [run 42828207431](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42828207431)／job **129870982366**；PR #316 **19/19 pull_request Actions completed/success**，专项 [run 42828266091](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42828266091)／job **129871184639**。本地14测试13通过/1因没有克隆原Git源码而跳过；GitHub runner实际完整checkout仓库，专项job日志确证**Ran 14 tests**且QUEST06独立历史来源对照测试**ok**，没有远端skip或失败。禁止把本地一条skip写成14/14本地运行。
- 在main仍指向启动HEAD、PR clean/可合并、候选HEAD不变、仅5路径且安全边界成立后，PR #316 squash merged到内容主线 **fc39c225625f90faa69cf1772e708303505202ec**，Git tree **cbfcc53a0bee1aba0ec79ffdf5682ad85755ca84**与候选逐对象同一，唯一父提交为启动HEAD。
- 合并后**内容主线** 27/27 push Actions **completed/success**，新专项 [run 42828785709](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42828785709)／job **129872996502**实际成功执行全部14项源数字、独立旧QUEST06目录及负例测试；Stage A其他审阅也成功。这份追加收据提交若无自身新Actions，不预报其CI成功。
- GitHub Actions只核公开派生数据、旧Git报告与防造假负例，**未运行私人ZIP解包、原商业客户端、地图或任务脚本，也未证明原原生玩法**。私有重SHA/CRC和实际CP950源字节解析是本轮独立于CI完成的工作。

## 止点、下一优先与阶段约束

I48只封存八处NPC创建与四份脚本的8条候选条件关系、LV30字面边界、宠物/物品图像来源资格及四村任务来源不合并。**只有取得本批外2625/4212发物源、真正可读同源DAT、可靠事件优先级/原运行行为才重开这些未知；本单元已到证据止点。** 下一最高优先选择非快递、非波鲁、确有原始DAT/候选图像与NPC配置或物品实际连接的内容模块，按DD-032逐区域补有源分类，拒绝无据补齐四岛循环、重复索引和Stage B新引擎。

Stage A仍**7 PARTIAL + 2 OPEN**；Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，overall_percent=null。完整历史CURRENT-STATE保留。
