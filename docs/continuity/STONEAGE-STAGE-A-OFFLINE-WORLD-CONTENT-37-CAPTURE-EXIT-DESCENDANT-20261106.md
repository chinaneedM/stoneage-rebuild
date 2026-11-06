# WORLD37-R1｜捕捉入栏后的战斗退出、捕捉计数与条件道具：三条固定后代源码交叉核对

**版本及停止线：** 2026-11-06，从远端 `main` `5c4cdd0023d88fbe1123645d03ea7f555d70de80`、完整 tree `b96690a43447f53afec1d1a6fc99e8d08ddc2c9c`（7,271项）接续。历史 `docs/CURRENT-STATE.md` Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 完整2,709,173B原样保留。WORLD36已用混合2.5原GMSV指令回放验证入栏，但停点前野怪原记录未变化；**本页是对另一组有来源的后代C源码的新增收尾语义核验，不能叫WORLD37混合2.5原二进制已回放或TW1官方行为已证。**

## 一、本轮确实补足的游戏行为：不是仅有一个函数名

沿三条固定commit，各自实际读取 `battle_event.c` 捕捉调用方 → `battle.c` 的 `_BATTLE_Exit` → `char_base.c` 的 `CHAR_endCharOneArray` / `CHAR_endCharData`。逐个原函数对照而不是依赖外部文字简介：

- **成功且宠物确实分配：** 调用方首先填写宠物取得等级，条件匹配时处理所需道具，**给捕捉者** `CHAR_GETPETCOUNT` 加一，继而调用 `BATTLE_Exit(野怪角色索引, 战斗索引)`，之后进行宠物属性合规、`VARIABLEAI=0` 和结果命令。失败路径不进入计数与目标退出。
- **野怪在战斗里的实际去向：** `_BATTLE_Exit` 逐侧逐席寻找角色索引，找到则将该席的 `charaindex/char_index` 写 `-1`，清该席逃跑标志，将原野怪工作战斗模式写 `FINAL`、战斗索引写 `-1`；当角色类型是 `CHAR_TYPEENEMY` 执行 `CHAR_endCharOneArray`。后者委托 `CHAR_endCharData`，清理挂载的道具和道具池并将原角色记录 `use=FALSE`。所以这不等于“仅视觉消失”或“把原野怪转成新宠物”：**新宠物角色槽是WORLD36另行分配的角色**。
- **条件与失败保护：** 缺所需道具、未过捕捉判定、成功判定后宠物栏/池分配失败，都**不触发成功尾段的GETPETCOUNT增加、BATTLE_Exit**。WORLD36原指令对容量失败仅证实未入栏且野怪原记录不变，当前不据此冒认尾段已原生执行。

## 二、条件道具必须按配置分版，不可只写“成功后扣一件”

固定后代源码 `NeedEnemy` 中存在宠物模板ID与道具ID的条件表，例如 `524→2456`；这只是**后代源码示例**，不是TW1初代官方同服表，也不能证明混合2.5已编译的具体表内容。至少有四种不同语义：

| 原编译条件 | 已读源代码结果 | 不允许推出 |
| --- | --- | --- |
| 没有对应条件表项 | 直接放行条件道具门槛 | 不等于所有野怪免费捕捉 |
| 常规非 `_CAPTURE_FREES` | 成功分配后依所需单一ID扫描背包，删匹配物品 | 不能默认为仅删除一份，循环未在首次匹配后退出 |
| `_CAPTURE_FREES` | 条件可含多个ID；成功尾段遍历需要的ID及背包栏，匹配副本可全部被删 | 不能折成固定一件、一ID或统一历史表 |
| 同时 `_NEED_ITEM_ENEMY` 且 `getDelNeedItem()!=0` | 在前置条件检查时就可能删匹配物品，**即便其后捕捉失败** | 因此“所有分支都仅成功时消费”是错误断言 |

`_DEL_NOT_25_NEED_ITEM`、`_WOLF_TAKE_AXE` 会改变实例条目；部分版本有从 `data/needitemeneny.txt` 读取的入口。不得把固定后代源码编译选项、生效表或玩家历史记忆当成混合2.5 GMSV实际可执行的配置。

## 三、九份源码、三条版本线的实物身份

| 后代来源与固定commit | `battle_event.c` Git blob | `battle.c` Git blob | `char_base.c` Git blob |
| --- | --- | --- | --- |
| [BismarckDD/stoneage](https://github.com/BismarckDD/stoneage/tree/999ffdf1d220ec6666eb65339180689c9caf1876) `999ffdf1d220` | `be9f2d476f80` | `99c3ad4ccfc4` | `5f646eba671b` |
| [gavinlinasd/StoneAge](https://github.com/gavinlinasd/StoneAge/tree/1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56) `1f90cb6cb57c` | `76ecf3ffee05` | `df5a04b94cbd` | `783b8803333b` |
| [iriselia/StoneAge](https://github.com/iriselia/StoneAge/tree/9e6c8ce2cd8ed532a7157773acd1c61582c178b5) `9e6c8ce2cd8e` | `8be4a044690e` | `3bd9f3603db4` | `bc35f7313b6a` |

全40位源码Git blob、路径、函数行段、成功/失败程序步骤与版本配置矩阵，固定在[派生证据收据](../../research/recovered/STONEAGE-STAGE-A-WORLD37-CAPTURE-EXIT-DESCENDANT-SOURCE-R1.json)。回查各固定SHA：
- [BismarckDD/stoneage 捕捉分支](https://github.com/BismarckDD/stoneage/blob/999ffdf1d220ec6666eb65339180689c9caf1876/server/gmsv/battle/battle_event.c#L3941-L4074) · [战斗退出](https://github.com/BismarckDD/stoneage/blob/999ffdf1d220ec6666eb65339180689c9caf1876/server/gmsv/battle/battle.c#L1097-L1189) · [角色释放](https://github.com/BismarckDD/stoneage/blob/999ffdf1d220ec6666eb65339180689c9caf1876/server/gmsv/char/char_base.c#L2353-L2381)
- [gavinlinasd/StoneAge 捕捉分支](https://github.com/gavinlinasd/StoneAge/blob/1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56/gmsv/src/battle/battle_event.c#L4026-L4146) · [战斗退出](https://github.com/gavinlinasd/StoneAge/blob/1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56/gmsv/src/battle/battle.c#L1149-L1206) · [角色释放](https://github.com/gavinlinasd/StoneAge/blob/1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56/gmsv/src/char/char_base.c#L1824-L1853)
- [iriselia/StoneAge 捕捉分支](https://github.com/iriselia/StoneAge/blob/9e6c8ce2cd8ed532a7157773acd1c61582c178b5/Source/gmsv/battle/battle_event.c#L4020-L4141) · [战斗退出](https://github.com/iriselia/StoneAge/blob/9e6c8ce2cd8ed532a7157773acd1c61582c178b5/Source/gmsv/battle/battle.c#L1154-L1212) · [角色释放](https://github.com/iriselia/StoneAge/blob/9e6c8ce2cd8ed532a7157773acd1c61582c178b5/Source/gmsv/char/char_base.c#L1587-L1616)

## 四、验收与真正剩余问题

公开测试只检查来源版本身份、九个完整Git blob pin、跨函数成功/失败规格、混合2.5原生证据边界与WORLD36原收据的容量/目标未变基线；**它没有执行历史二进制、没有自动验证Github上游当前分支的源码、没有模拟真实网络或旧服务端存档。** 不触及原专有资源、私有RAR、原图/对白与登录系统。

**WORLD37-R1 = 后代源码三线交叉确认，混合2.5原GMSV后半段仍OPEN。** 可恢复下一真实内容应从同一混合2.5原GMSV实际字节出发，沿 `0x538443` 后的 `BATTLE_Capture` 原分支追捕捉计数、`_BATTLE_Exit`、消费路径及回合回报；核实原表、容量失败和原野怪角色池释放。在未重新取得该私有合格原件的环境**不得伪造本轮原生回放**；其余来源有了证据可增量打开。维持 Stage A 7 PARTIAL + 2 OPEN、Stage B/wiki GATED、R79 暂停、overall_percent 未知。维持单机内容还原主线，不转建账号/联网服务。

**NEXT：WORLD37-R2 原GMSV收尾有界回放（条件：实际取得已认证私有原字节）；否则按模块集中路线轮换实际可取得的原始世界内容。**
