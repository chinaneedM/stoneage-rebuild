# Stage A｜WORLD22 原任务石币奖励、扣费与道具条件（2026-11-05）

本轮从实时 main `b4354472bf00a795bbe40be4b9e8c7f2963e2927`、tree `260eea3ad40ae4dd6965ae5023e7283e5fde0aaf` 启动。849个远端分支、0开放PR；该主线11项Actions均实际 completed/success。完整检出与准确Git blob核验README、协议、CURRENT、决策、时间线、来源表、路线、模块工作序；按最新WORLD21的NEXT推进WORLD22。历史CURRENT 2,709,173 B / blob `c89e0e33537990aa2132b47c40fef49a985a935c` 保留原字节。

**交付与止点：** 批量复原同一已保存社区混合2.5原NPC脚本中全部 `GetStone` / `DelStone` 的原条件、金额字面量、关联道具、确切源行/哈希与CREATE引用。此为源文件内容研究，不建立条件执行器，不推真实交易、早期官方规则或同服。完成本批来源核验与私人阅读资料即止。

## 实取来源与完整核验

重新取得私人 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip`，995,176 B / SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`。全2,205成员、1,930,332原字节，ZIP CRC与CHAR01原清单的每件大小/完整SHA/CRC均一致，无命名重复或成员缺失。父RAR本轮未再重读；既有完整SHA `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5` 仅沿用保管来源，不称再次解包RAR。

公开[逐源派生索引](../../research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-22-QUEST-CURRENCY-SOURCE-R1.json)保留9个现存输入Git blob（CHAR01、QUEST01及ITEM01七分片），不包含原商业对白或原图。现代提取工具读取原件，公开CI只核派生与合成反例，不冒充重新解包私人原件或执行原游戏。

## 全批结果与新旧覆盖

- 26份原脚本、115条货币指令：**99 GetStone、16 DelStone**；108个ACCEPT、7个REQUEST；107个整数字面量、8个未求值的等级表达式。115条皆有实际EventEnd。每条保留原序、EVENT文本、TYPE、物品增删/数量及标志字段，不将原序当运行顺序证明。
- **99条奖励已在QUEST01数字目录中存在**，本轮逐分支核其金额/条件SHA，并接回原件、完整上下文与物品表；不称99条新发现。旧QUEST01没有登记DelStone操作：其中14条扣费的事件块原已存在，另2条来自原件 `extra/event/osaisen` / `osaisen2`，两文件没有确切CREATE引用，不能称原服启用。
- 五份 `chatroom/ticket*` 原分支为 `EVENT:LV>10`、`DelStone:LV*3`、`GetItem:2597`，低等级分支仍另存原文，不把它们混成同一收费规则。五个源CREATE的floor为1000/110/2000/3000/4000；原borncorner与borncenter四元组原样保存，不将范围起点冒充唯一坐标。
- `quiz/uketuke` 原收费分别为 `LV>49 → LV*40 → 2756` 与 `LV>29 → LV*20 → 2755`；`uketuke2` 为 `LV>69 → LV*40 → 2756`。这些是源字段关系，没有执行等级判定或金额公式；不能据此猜原版本门槛、条件短路或实际扣费。
- 固定DelStone字面量分布：50三条、1200两条、3000两条、1000一条；等级表达式另8条。7个REQUEST不是已运行的奖励分支。原条件的逗号、`&`、比较符保留，不替它们发明统一逻辑。
- 26个确切CREATE引用与CHAR01原路径/目标完整SHA逐一匹配。它们不是26个不同NPC或26个已运营任务；无引用的两份原脚本继续明确无部署证据。
- 显式物品条件与增删字段涉及124个不同ID，全部在ITEM01候选表联合索引存在；**2391仅另一候选表有记录，itemset.txt无记录**。本轮完整重读itemset.txt 3,392,473 B / SHA `a415e78f9aab2e5ea5ca92ecb7430253f7be1ba7c876d6b0bb6d067b1b466688`，其余123个原行SHA与已存索引相同，私人页显示该表原名；2391原名不猜、不将候选表差异抹平。另一候选itemset0710全文本轮未重读，公开索引的原行SHA沿用既有证据。

## 私人阅读资料与验证

已保存 `StoneAge-WORLD22-private-quest-currency.zip`，48,421 B / SHA256 `230245fe15687ee4d618ef6ee840887b87715b0ad52bcef25919e944094e0baf`。三成员本地全CRC通过；HTML 85,819 B / SHA `1b359d4efbd3fb280b8a16d61d965ec165596065f98a64c25ef655a68514e2fe`，含26份可展开原繁体脚本文字、115条来源分支、123个经原行核实道具原名及2391缺表标记，可用浏览器原生查找。静态HTML结构核验26详情/115条目/124道具，无脚本、外部链接或外部资源。**本轮没有运行浏览器或原客户端**；只声称结构检查。原文、私人HTML与原表均不上传公开Git。

本地专项10项及WORLD21/WORLD16相关16项，共**26项通过**。首次交叉测试错误地要求两份未被CREATE引用的osaisen脚本也必须属于旧QUEST01范围；按原清单查明后，改为显式检验两份无引用。私人道具原名首次导出因2391在A表不存在而停止，随后保留缺表标记。没有修改原件或补造缺源。Git原生dry-run因无凭证失败，后续使用已连接仓库接口；不扩大权限。候选/主线Actions待真实运行后记录，不提前写成功。

**最高NEXT WORLD23：** 在原任务/物品内容模块选择下一项确有原实物增量的内容缺口；优先源任务道具的取得/消耗或原奖励数量，与既有WORLD09/13/14/16/21/22查重。当前货币分支达到来源止点，不扩通用公式执行器、模拟经济、账号网服、新引擎或体验优化。Stage A保持 **7 PARTIAL + 2 OPEN**，Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，整体完成百分比未知。
