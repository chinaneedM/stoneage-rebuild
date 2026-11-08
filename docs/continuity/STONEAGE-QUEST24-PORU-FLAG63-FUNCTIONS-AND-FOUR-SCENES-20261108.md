# QUEST24：波拉岛前段剧情、ENDEV63来源与四张真实DAT候选画面

2026-11-08（Asia/Shanghai）。QUEST23内容已验收，随后从fresh远端main `f26565d75231eb0d90cc7258b2496ec7eb22ea05` / tree `bce8b799ff8f2b3eec208720f0e3d7ad940b2e58`承接其NEXT。该HEAD的11项Actions全部completed/success、0开放PR；原生Git与完整连续性/路线字节核同，最新接力已重读。完整CURRENT 2,709,173B / blob `c89e0e33537990aa2132b47c40fef49a985a935c`保持，不用旧聊天状态替代远端。

## 先找到真正的事件63设置者

原`poru/poru01.create`有32条来源配置，其中11条changeevent引用37个既有TYPE段；ENDEV63的设置者**不在该CREATE内**。旧QUEST01指向另一份`poru/boss.create`第0配置→`poru/boy04`，原floor5511、borncenter17,12,1,1、图别名100373，模板链接到ExChangeMan。选取此一龙王来源配置，不据名称或整个boss文件宣称所有条目是战斗NPC。

boy04第1 ordinal段写`NOWEV=63`、`GetPet:352`、`EndSetFlg:63`；QUEST23的mary请求原写`ENDEV=63`。本轮把这条**静态跨文件前置关系**连接到原配置和地图。GetPet352早已在WORLD21，对应同包模板303/IMG100373，不是模板352、新宠物发现或原生发放成功。源NPC图号与该模板图号同数值也不证明实际显示/领奖。

12份事件脚本共39个TYPE段（37+boy04两段）全部与QUEST01完整段SHA一致，新增原脚本发现0。父RAR和整个服务端主表本轮未重取；原NPC ZIP整SHA与2,205成员SHA/CRC、物品包838成员CRC均真实认证。

## 由原模板判功能，不能按文件名推功能或坐标

| poru01来源配置 | 数量 | 原模板functionset |
|---|---:|---|
| npcgen_man | 15 | TownPeople |
| changeevent | 11 | ExChangeMan |
| npcgen_shop | 3 | ItemShop |
| npcgen_warpman | 2 | WarpMan |
| npcgen_winhealer | 1 | WindowHealer |

另选boss第0条ExChangeMan，合计33个来源配置。上述功能全按同载体原模板精确路径/ordinal/函数名连接，不是实际执行。

`poru/wpm_5510_16_50`虽然叫wpm，原CREATE绑定changeevent→ExChangeMan，实际只有MESSAGE段和ITEM2414条件，**没有WARP字段**。两个真正WarpMan参数则为：

| 参数来源 | WARP原值 | FREE原值 | MONEY原值 |
|---|---|---|---|
| wpm_1000_71_49 | 1000,71,49 | ITEM=2414 | -1 |
| wpm_5509_35_35 | 5510,16,49 | ITEM=2414 | -1 |

第二个文件的源CREATE点实际为5509/(37,35)，不能按文件名改成(35,35)。FREE/MONEY仅为字面参数，不补原收费、队伍限制或准入运行证明。poru01第17/18/21/30/31条同时有borncenter与borncorner，两字段和原方向都保留；本轮仅投影center前两数，不认定二者优先级。

## 六种肉、贝壳与18544/18558差异保留

boy05的原条件是`ITEM=2248,ITEM=2249,ITEM=2250,ITEM=2251,ITEM=2252,ITEM=2253`，GetItem2414，DelItem为六ID逗号表。**不把逗号改成AND，不推六肉全部必须拥有、任选一肉或实际扣除数量**。删除项都没有显式数量，仍保留省略。

源samugiru01有一段消息检查18556/18557/18559/18544；QUEST23的最终交付检查18556/18557/18558/18559及NOWEV64。两条原条件分别保存，不擅自把18544改成18558或把消息段当领奖段。boy04另有`ENDEV=63&ITEM!=18544`消息段的GetItem18544*2，保留原显式数量，不把原发放当本轮已运行。

12个相关道具为2248–2253、2414、18544、18556–18559，两份94栏原表24行SHA逐项与ITEM01一致，连接11个既有台湾1.0原RD候选PNG。后期物品表与TW1候选图来源分开，原名/描述仅在私人资料页完整查看。

## 四张原DAT与27个配置中心

复用已保存MAP09包46,844,444B/SHA256 `d84d0800dd600798769dfb7251a1d7816588ac061ccc27812ac64a37922d4a8a`，4,195成员CRC及内嵌955 DAT包SHA/CRC真实通过。此前NEXT只列5500/5510/5511，本轮原参数又精确指向已有合格5509，故补入第四场景；**不是新发现一张原地图**。

| 原floor | DAT宽高 | 本轮测值中心数 |
|---|---|---:|
| 5500 | 50×30 | 22 |
| 5509 | 50×70 | 1 |
| 5510 | 60×60 | 1 |
| 5511 | 30×30 | 3 |

四DAT整SHA/几何均同MAP09，490不同候选PNG逐PNG/RGBA认证；Pillow与NumPy重放12完整画布，SHA全部同旧MAP09。独立三平面NumPy数组再核27原格，原黄点中心像素亦同；图上编号是本页现代marker ID，通过原CREATE路径和原ordinal回查，不是原NPC ID。原生出生格、center后两整数含义、双坐标字段优先级、原palette/遮挡/碰撞依然未知。

助手实际查看四图2×2联系页，村落室内、山顶洞口/天空及两洞窟候选可见。仅画现代来源标记，没有NPC精灵或原客户端执行。六个500大地图配置仍缺匹配955批次DAT；去1000的参数只是原字面，本轮未重读目标1000原DAT，不把记录点连成可玩路线。

## 私人交付与可复核结果

私人包 **23,451,751B / SHA256 `75aad7150fe4ffd4db0da16bc5de92f8ed3c61073beb2fa709a9ad19c8ba83ac` /578成员**含36份原NPC/模板/参数文件、24原道具行、候选源图、四原DAT及完整/标记场景、原文与道具查阅页。保存后独立回读整字节/SHA/全部成员CRC一致；原商业素材不入Git。

10项专项和全部286任务相关测试本地通过。27原格/黄点、36原文CP950逐字解码及全部本地链接独立验证；再次源生成的公开报告和578私人成员逐字节相同。工具复用QUEST23的原目录边界与MAP09双实现，没有新工作流、原引擎或账号/网服；公开CI只检查派生证据，不替代私人原图重放。候选/main后验据真实结果追加，不预支成功。

**NEXT QUEST25_MODULE_CONTENT_REVIEW_AFTER_PORU_FLAG63_AND64_SOURCE_LINKS**：这两组波拉岛前置/四圣石的来源关系达到有限止点，先回任务模块和现有WORLD/角色/地图/宠物覆盖做材料复核，选另一组能增加实际内容关联的原件；不得只重算旧TYPE/目录、反复重放500缺图或穷举borncenter加载器。原生任务、500 DAT和历史官方归属等待相应新源再开，不进入未来新游戏设计。

Stage A仍 **7 PARTIAL+2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**，本体/常驻/活动起源 **UNRESOLVED**、总体完成率未知。
