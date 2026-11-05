# Stage A｜WORLD24 原编译存点GetItem用途与127字节读取边界（2026-11-05）

**工作目标和止点：** 从fresh远端main `c448e6acfaae8364ab6948867256b4869c4a5629` / tree `121b75e0033a183799710e0080cbd66b1d986909`、0开放PR及WORLD23内容主线11项实际成功Actions启动。承接最新WORLD23 NEXT，在同包原编译服务端中核实一类非ExChangeMan物品字段的具体用途。本轮选择SavePoint，取得有界原代码语义、关联全部来源配置即止，不扩通用执行器或网服。原CURRENT完整2,709,173 B / blob `c89e0e33537990aa2132b47c40fef49a985a935c`、旧WORLD09订正及全部历史原样保留。

## 1. 实际读取的源与版本资格

复用早先已独立成功解出的完整 `gmsv.exe`，本轮完整重读 **1,897,867 B / SHA256 `d5b08dbcbf9e8736ba8598e38e5901f123d2bff544a9cae53a9ff88ce1971e00`**，与WORLD18、SCENE33已验同包成员身份一致；本轮没有重新解包父RAR，没有把WORLD19曾发生的EXE解包CRC失败追认为成功。原二进制不上传Git或CI工件，不启动服务器。

私人CHAR01原NPC ZIP完整SHA仍为 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`，本轮2,205成员/1,930,332字节逐大小/SHA/CRC重验。22份SavePoint参数与GAMEPLAY05的确切CREATE、目标文件SHA、ID、Born来源字段逐一联接；21条GetItem原行与WORLD23原序及行SHA逐一相同。

二者均属保存社区混合2.5档案，不认证某次历史官方同部署、TW1/JSS1999/CN1.82初代规则或当年运营行为。保存同包源是静态内容联接的范围，不能代替原生运行。

## 2. 编译程序中GetItem是条件性消耗字段

[公开数字/哈希证据](../../research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-24-SAVEPOINT-ITEM-ROLE-R1.json)记录10个原COFF符号、14条确切相对调用、9个代码窗完整SHA，以及编译常量/标识符地址。独立`nm`与`objdump`分别核10/10符号和14/14调用目标，全部一致；不公开原机器码或反汇编全文。

- 原 `_NPC_SavePointTalked` 的未激活检查在 `0x499862` 调 `_NPC_UsedCheck`，第三参数为0，只作所需物品检查。
- 原 `_NPC_SavePointWindowTalked` 在距离≤2、序列字面230、选择字面4的路径，以第三参数1调用同一函数；成功后尾跳 `_NPC_MessageDisp` 的激活分支。回复常量是此编译样本的事实，不泛化成所有客户端UI。
- `_NPC_UsedCheck`读取`GetItem`，先走 `_NPC_AndReduce` 条件检查，消费路径再走 `_NPC_AndReduceDelete` → `_NPC_SavePointItemDelete` → **`CHAR_DelItem`**。相关库存扫描为原槽5–19。因而该处理器的`GetItem`不能按字面名翻译为给玩家奖励。
- 成功激活分支有原状态字段30和59的写入；本轮只核代码控制关系，没有实际库存、位标记写入、服务器回包或存点启用记录。原位移/ID全部运行效果、异常失败与原生事务完整性不在本包推演。
- 当`GetArgStr`本身失败时，UsedCheck返回0；当它成功而未找到GetItem时，原路径返回1。这是带前提的编译控制流，不能直接称某原NPC在游戏中免费启用。

此结论来自**实际保存的编译程序**，不以另一个后期C版本替代原件。既有独立后期C只在复用的WORLD09回归检查中继续核旧合同，不参与本轮SavePoint语义归属。

## 3. 同一编译读取器的实际长度限制

`_NPC_UsedCheck`给原GetItem字段读取器传容量 **128字节**，字段读取器再调用本程序的 `_strcpysafe`。后者在容量不足时复制至`size-1`并补NUL；本批GetItem原值全部ASCII，因此已核的有效读取上限为 **127原字节**。这是有原字节支持的条件性复制投影，不是Python按字符猜切，也不是实际加载/执行轨迹。

全部22份原SavePoint参数：21份有GetItem、1份没有；没有任何一份原文含`NOITEM`字面。21份共有209个原逗号位置，其中14份长度≤127，7份超过上限：

| 原参数路径 | 原ASCII字节 | 复制后逗号位置 | 被截断的尾片段 |
|---|---:|---:|---|
| genout/sp_100_344_466 | 209 | 7 | 2 |
| genout/sp_1300_29_23 | 223 | 13 | 2 |
| genout/sp_1400_76_104 | 251 | 13 | 1 |
| genout/sp_200_406_371 | 251 | 13 | 1 |
| genout/sp_200_449_982 | 250 | 13 | 19 |
| genout/sp_3300_71_51 | 251 | 13 | 1 |
| genout/sp_3400_65_48 | 237 | 13 | 2 |

全批复制投影有161个逗号位置，含7个截断尾片段；**不是161个已验证有效条件**。209仍是完整原配置的原位置数，没有删除或“修复”原文。原`1991*`残缺数量继续留在原文；不能把截断后看不见的部分说成原档不存在，也不能把尾片段1/2/19当成有意设计的新需求或推实际能用哪些物品开存点。

缺GetItem的原文件是`genout/sp_30691_87_60`。`NOITEM`原代码旁路仍记录为编译事实，但22份来源没有这个字面，不给缺字段文件强加NOITEM标记。原源长短、缺字段、读取上限和未实际运行分别保留。

## 4. 私人资料、测试与止点

私人`StoneAge-WORLD24-private-savepoint-item-role.zip`已保存，13,112 B / SHA256 `2348f1ccede7efc7575d72b029e23823f3ad328f72f360b68de30359a1838312`。HTML 23,144 B / SHA `ef9f49fe427792dd123ee4d83536282d00f5352d85fd20c4cc0e8c5c7a8dd5e8`，22份原参数可展开，完整原字段与条件性127字节投影并排核对；本地3成员CRC、22详情HTML结构检查通过，无脚本/外链/外部资源。没有声称本轮浏览器或原客户端运行，原参数全文只留私人包。

本地**39/39测试通过，无skip**；其中10项新增，覆盖同原EXE身份、22份来源、GetItem非奖励用途、读取器调用链、7份截断原文、14份未截断、缺字段与NOITEM区别、ASCII/容量反例及运行/官方版本否定门槛。复用现有WORLD09→WORLD23验收工作流，加入本包；CI只核公开派生和既定独立后期C，不能代替私人EXE重新读取。候选/主线CI后验另据实际追加。

**最高NEXT WORLD25：** 有限核同一保存版Quiz的物品字段用途及实际原参数，优先现成完整编译程序的命名函数与4条GetItem来源；缺精确控制关系就明确止点，不从SavePoint语义回填Quiz、不扩答题整引擎或账号网服。保持Stage A **7 PARTIAL + 2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、整体百分比未知。当前保存版原存点真实执行、初版官方规则及全游戏可玩性仍未认证。

## 实际远端终验（成功后追加）

候选 `ee87e645328a783bdc5dab767abe593ffbd6b80e` 的13项Actions全部实际success；PR #203合并为内容主线 `4ebb9ccf571b6aad117d9613bf2bf18ffde9b4e4`，主线11项Actions全部实际success。两者完整tree同为 `3149b7ba7a11e885397b9182fac172b43b434dec`，六个上传Git blob逐一与本地一致。候选专用run42027804115/job127246285591和主线专用run42027909055真实日志均确认39项全部通过、无skip；公开CI没有读取原EXE/NPC，也没有运行原存点。原CURRENT与WORLD23 Git blob未改，README全部356339B历史前缀保留。[永久终验收据](../../research/recovered/STONEAGE-STAGE-A-WORLD24-PUBLICATION-R1.json)记录全24个运行ID、两专用job、完整来源/调用独立核验和私人交付SHA。收据自身提交不预支Actions；最高NEXT WORLD25与阶段/运行边界不变。
