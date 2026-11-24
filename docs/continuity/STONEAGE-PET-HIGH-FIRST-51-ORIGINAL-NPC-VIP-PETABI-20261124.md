# PET-HIGH-FIRST-51｜原 NPC 入口复核与 VIP 固定属性配置

从远端 `main 3a1ec8e7c02318591707cf44e4cbb50885186985`、tree `2c6e06e918211d4accc0518db97306783bce37b1` 接续 PET50。主线 37 项 Actions 已通过，历史 CURRENT 为 2,709,173 字节、blob `c89e0e33537990aa2132b47c40fef49a985a935c`。本轮只审保存经典 PC 宠物来源，以及与这些宠物相关的 NPC 参数。

## 五组无野外入口的模板

获取 [远端原件普查](../../research/pets/PET-HIGH-FIRST-51-ORIGINAL-NPC-CENSUS-R1.json)全部 2,205 个 NPC 文件和两张选中表。逐件核对 R18、CHAR01、PET10 中记录的长度、SHA-256 和 RAR CRC32。早先 CHAR09 的 260 个参数文件在八个群组成员实例号上没有命中。全树另补查两只同名 Lv1 实例 2415、2416，覆盖 10 个实例号和 11 个群组号。

| 已知实例范围 | 选中表配置 | 可证到的来源边界 |
|---|---|---|
| 奇肯沃 2415、2429、2431，奇肯克奈 2416、2430、2432 | 2415／2416 为 Lv1 且宠标记 1，未连已查群组。2431／2432 为 Lv131–140，2429／2430 为 Lv150–200，四个高等级实例的宠标记均 0 | [7.0 专区目录](https://news.17173.com/z/stoneage/banben/sa70_11.htm)两名均写泪之海和 Lv1，没有具体坐标或元素，已记于 PET49。[2007-04-04 玩家珊瑚攻略](https://news.17173.com/z/stoneage/content/2007-04-04/1175676383.shtml)第 70–71 行另报打 Lv130–140 同名对象掉素材，与保存档 131–140 有重叠。文献未给实例号或部署桥 |
| 薩德迪比 2455、薩德斯凱 2456 | 两者均为 Lv1，宠标记 1，有群组成员、无地区正权重入口 | [2011 玩家指南](https://games.sina.com.cn/o/n/2011-12-08/1604559245.shtml)的梦幻洞窟日夜取得说法已记 PET49，缺同部署脚本桥 |
| 瑞里西爾 1642、2187 | 等级 1、101–110，均宠标记 0。保存模板和标称 7.5 同号异指纹 | 保留 PET48 的社区历史说法等级，玩家取得方式未证 |

逐行核对的 39 条数字碰撞出现在 `EVENT`、`GetItem`、`DelItem`、`LimitItemNo`、`item`、`ItemList` 或 `GetRandItem`。没有查到这些编号出现在本次识别的实体引用字段中。该阴性只覆盖原保存档的静态 NPC 目录和所列字段，外部资料与其他部署仍可复查。后期 PC 对照的 [npc_npcenemy.c](https://github.com/pimpcapital/longzoro-sa/blob/57b14e2bb373ba851c14db28a239273e4a8831bb/gmsv/src/npc/npc_npcenemy.c#L83-L104)（blob `45c95d9df8b1e3e9d41443ca12f6ac8f4c105fc4`）显示 `enemyno` 经过 `ENEMY_getEnemyArrayFromId`，不能把事件号或道具号拿来补齐。

## 28 条 VIP 首字段已解析

原文件 `vippetshop1.arg` 19 条、`vippetshop2.arg` 9 条均为 `PETABI` 加七个数字和独立的逗号点数，所有原行及字段散列与 PET50 一致。列义见后期 PC 参考 [npc_eventaction.c 2518–2654 行](https://github.com/BismarckDD/Stoneage/blob/2f736808ff4361f5429ee919b718c88fabb60346/server/gmsv/npc/npc_eventaction.c#L2518-L2654)（blob `a89b744394079cc476e7e87f6e353d66208e0150`）和 [util_string.c](https://github.com/BismarckDD/Stoneage/blob/2f736808ff4361f5429ee919b718c88fabb60346/server/common/utils/util_string.c#L38)（blob `8065a372bfa0c1d4e74d39fd73b405c7b6a7b569`）。条件宏 `_NPC_GET_PETABI` 指示该语法按空格取实例号、等级、转数、血、攻、防、敏，按逗号另取点数。参考代码以 20、80、80、100 四个倍率写内部属性字段。实际原始行 28 条均 Lv1、零转，点数 50–150。保存原始配置数字，实际面板、成长和部署语义均待独立证实。

- 28 个不同原实例号为 2578–2606 中除 2596 外的全体，逐条连到同包原实例、主档、数值字段和 SPR 索引候选。27 条双宠标记，莫拉司 2603→1237 的实例标记为 0、模板标记为 1，独立保留冲突。
- 28 个源模板号均未出现在标称 7.5 的 467 条档案中。27 条以同名同图号给出 33 条查询链接，包含待查位置 144 奇卡洛斯和 208 巴朵蘭恩。链接资格仅限名称和图号。另有 1 条剋剋洛斯未得该类桥，保留原档位置及同包 SPR 索引候选。
- 同包 `vipshop.template` 写 `functionset=VipShop`。独立解出的 `gmsv.exe`（1,897,867 字节、CRC32 `6e31b63a`、SHA-256 `d5b08dbcbf9e8736ba8598e38e5901f123d2bff544a9cae53a9ff88ce1971e00`）未定位 VipShop、VipPet 或 PETABI 的 ASCII、UTF-16LE 标记及 VipShop／VipPet 函数符号。普通 PetShop、AddPet、CheckMenuFree、RunDoEventAction 均可定位。原配置与后期代码能解释字段，同包可执行程序的加载证据尚缺，实际兑换和官服发放均未证。

## 来源保全

- [原件工作流](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/45463436539)，提交 `1abd769dff965a1994db07bc409ad5abf1c5cfe7`，job 138691905651，artifact 14954756093。184 个 HTTP 206 区间读取 12,013,836 字节、遍历 7,954 个 RAR 头。libarchive 完整解出 2,207 件，成员清单聚合 SHA-256 `a4e15cb3c9267fa6457767346232e7406e539c435ed9ec16a78b87e3cd804241`。
- 下载原 ZIP 14,325 字节，SHA-256 `d7bf5efdbab82be28b329914056fb633860bb9c883c64bda7e8799f85e16d40b`。原 JSON 67,660 字节、SHA-256 `7a654c7c9118d0c577f3a2fe9dc8188c3b10e1945bf5e7eed651e32fddd9191f`、Git blob `14103aa39eba7e98c53e050394c0dff02cd0c7e2`，与工作流日志一致。
- 本地重取并独立核对完整原 RAR 361,255,180 字节，SHA-256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`。用 [UnRAR 固定源码](https://github.com/pmachapman/unrar/tree/cacdcb8cbe1813b6151e3f92f2ccec7afe4d6a41)解出同批 2,207 件以及 gmsv，逐件校验完整 SHA/CRC。本地 NPC 和 VIP 第一版投影与原工作流报告完全相同。新增的 [PETABI 逐项收据](../../research/pets/PET-HIGH-FIRST-51-PETABI-SOURCE-LINKS-R1.json) 46,311 字节，SHA-256 `9e98d7c300ce0f99d76c4cd2b775441dc1444ff61b9c98401b6abaf151d6fb0f`、Git blob `ab826bd89e5d1f39f8f219b5a2803efba02248b9`。原版权程序、脚本文本及影像资源不发布。

本次增加 28 条可查询的保存档配置位置，官服实际发放新增 0 项，原生客户端／服务端未执行。PET 仍为唯一活动模块，Stage A 7 PARTIAL + 2 OPEN、Stage B/wiki GATED、R79 暂停，总体 UNKNOWN。

**NEXT PET-HIGH-FIRST-52**。用已获高版本原客户端来源优先核对位置 144、208 的具名图鉴及真实获取证据，明确区分原任务奖励、固定属性 VIP 变体和同名字形。PET51 的 28 条配置只在发现含对应 VIP 处理入口的保存构建、可直接获取的同部署数据或具名官方取得记录时重开。本轮无入口的五组，等待能够直接指向实例／群组的其他来源。
