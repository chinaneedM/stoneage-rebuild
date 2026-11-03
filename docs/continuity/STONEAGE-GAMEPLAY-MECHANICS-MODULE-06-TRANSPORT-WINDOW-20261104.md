# GAMEPLAY06｜地面交通、飞行、传送、物品寄放与原窗口配置批量恢复（2026-11-04）

**Stage A 复原，非新石器设计。** 起点远端 `main` `98e6b0734a85567066da3377eee1a45a0cde68b7`；原 `docs/CURRENT-STATE.md` Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 保持全字节不变。**材料来源**：私人已保存 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip` 995176B/SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`，共2205个社区混合2.5原NPC源文件/1930332B。该后期社区材料**非已认证官方JSS1999、台湾1.0、大陆1.82服务端原部署**。

本批实际重读57份创建块，按CHAR01已登记的原始字节偏移取得每块并重算完整SHA；逐条核对来源文件中的`enemy`函数及`file:`/`conff:`原引用。重读28份实存原参数内容，按各自的大小、整SHA、CRC与公开的原2205文件账本核实；另**一条源引用的文件不存在**。这是真正的原文件证据核验，父361MB混合RAR本轮未重读；原脚本/商业图像及完整对白不上传公开仓库。

## 一次处理7个原函数族

| 原保存版函数 | 创建配置块数 | 原文件与事实 |
|---|---:|---|
| `bus` | 7 | 7份实文件，共311组二维`routeto`坐标 |
| `airplane` | 5 | 5份实文件，共61组三整数`routeto` |
| `transman` | 7 | 3份实文件、7组不同源`WARPPOINT`，第一份被5条配置重用 |
| `npcgen_poolitemshop` | 5 | 4份实文件（其中2份原字节SHA相同），4份源均有`cost:50` |
| `bankman` | 8 | 共同引用1份真实`family/bankman.conf`，仅有1个声明的`winno=1` |
| `windowman` | 17 | 源引用9个路径；8份真实存在，合计61个原`winno`数字，另1份缺失 |
| `duelranking` | 8 | 创建参数无文件引用，只有该源函数名本身 |

合计 **57条原CREATE块、29个不同源参数路径（28实存、1缺失），28份实源27840B**。文件引用类型：`file:`24创建、`conff:`25创建、完全无文件参数8创建。所有创建块的原路径、原ordinal、原block SHA、楼层和图号等数字均在[GAMEPLAY06原数值与散列来源目录](../../research/recovered/STONEAGE-GAMEPLAY06-ORIGINAL-TRANSPORT-WINDOW-AND-ITEMPOOL-SOURCE-R1.json)；它们不等于有57个不同真实运行NPC，不能把同名参数重用当作新增设施。

### 地面交通与飞行

七份`bus`均只有原`routenum=1`；六份`waittime:180`，`giiru/banam.arg`源为`waittime:120`。地面交通的`needstone`数字分布为0、20、25、30、40、50、50。五份飞机参数均有`waittime:180`；源`needstone`为1000×3及3000×2，`oneway:0`有3份、`oneway:1`有2份（后二者还有源`pickupitem:0`字面）。**这些只是文本文件中的参数数值，不能断定`waittime`在运行中的秒数、能否扣费、是否完成原生移动/空投，也没有由路径推导原客户端可视轨迹。**

一处重要原始差异：`denieditem`源文件里，有5份包含ID **403**，6份包含ID **2403**，另一份根本没有`denieditem`字段。即使相邻列表其他项很相近，也不得未经同服运行证据把403自动“修正”为2403。

### 原传送与寄放数字

七条`transman`创建只引用三份参数（包括`my/tiancai/transfer.arg`的五次复用），三源合计7个不同`WARPPOINT`原三元组；每组相应`FREE:LV>0`文字存在。传送是否真的允许、是否存在其他条件、记录点状态是否变化，都未运行验证；尤其名含`vipshop`的路径不能倒灌到官方早期版本。

五条`npcgen_poolitemshop`引用四个不同路径的原文件，四文件源`cost:50`；原`genout/pis_3009_18_40`与`genout/pis_4009_15_13`整文件SHA相同。不能将这些50当作已观察到的存入费用、实际扣除或物品服务执行，也不能把配置文本的对话描述当作完整物品银行业务逻辑。

### 银行、信息窗口与排行榜

八条`bankman`共用`family/bankman.conf`；文件定义`winno=1`，同时有指向`gotowin=5/6`的原配置，但**该份文件内没有声明这两个`winno`**。要判定是否跨文件调用或根本缺件需更多源码，不能擅自生成第5/6号窗口。

17条`windowman`中4条来自`sainasu/jujutu.create`，均指向`sainasu/jujutu01.conf`，但在已取得的2205份原NPC源文件清单和ZIP实物中找不到对应文件；缺件保持 **MISSING_IN_CURRENT_ORIGINAL_NPC_ARCHIVE**，既不忽略四条创建，也不编一个临时`.conf`。其余8个`.conf`原窗口文件实际有61条`winno`数字定义，含聊天引导、制作/料理说明、剧情说明等来源文本，但**文件路径中`event`不构成历史运营活动任务的证据**，不将它们误纳入节日活动目录。8条`duelranking`源创建没有附加参数文件，不能凭函数名称确认原排行显示或结算。

## 验收和下一步

验证只使用 **CHAR01原创建块SHA和已公开同包每文件SHA/CRC**，把本轮源数值索引与真源账本双向核对，并加入异常路径、403/2403不混合、缺窗口、不假定原native执行等负例。源码和原档只留私人环境，GitHub CI测试公开派生数据而不能替代真实原客户端或服务器运行。

该批`GAMEPLAY-MECHANICS-MODULE-06`为**SOURCE_BOUNDED_PARTIAL**。仍是Stage A 7 PARTIAL + 2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING，整体百分比未知。**下一最高：GAMEPLAY-MECHANICS-MODULE-07**——直接复查已存捕捉/宠物技能原函数源规则及其它已具资格材料；如果根本没有可验原执行行为，给玩法模块有界止点，转入各模块的跨系统历史整合，不持续堆积无源推测、新引擎或玩家体验优化。
