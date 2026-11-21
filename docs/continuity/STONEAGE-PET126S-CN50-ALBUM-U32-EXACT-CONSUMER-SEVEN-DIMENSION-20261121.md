# PET126S｜原PC大陆5.0相册尾数值：原编译+24 → 本地+36 → 第四调用参数；七维缺口有界复审

**2026-11-21｜PET唯一活动模块｜官方原经典2D PC历史。** 本轮按远端重新读取的 `main=0d7245e8632900a6a0703eb008d0f3a73a70c65e`、tree `575d73db66f0f2e437f020b30c57f3d62cb220b0`、32/32主线Actions、完整2,709,173字节历史CURRENT Git blob起步。遵守连续性协议§26 PC-only。原大陆5.0载体为第三方保存的经典PC安装CAB，**压盘官源未获独立认证**，原软件不运行，不把网页／跨版资源当在服物种。

## 原始客户端与静态数据传递新证

重复SHA锁定原保存`sa_5000.exe`：630,784B，SHA256 `5dbcc3fa276f9f245fb706bce957e9c3300d870df813889502b789b727e49c97`；源码静态反汇编扫描131,461条原编译指令。**真正的原材料重放和合成测试都通过**：[Actions 44884234678](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/44884234678)，[原始结果的永久派生JSON](../../research/recovered/STONEAGE-PET126S-CN50-PC-ORIGINAL-RUNTIME-ALBUM-U32-CONSUMER-R1.json)。

- `0x43476e` 从原相册28B源行 `+24` 读取u32；紧接 `0x434774` 写入本地80B运行时记录 `+36`。PET126R已证，本轮真正重读原EXE并复验；
- 全`.text`按原绝对字段 `0x3300ccc = 0x3300ca8+36` 精确扫描，仅**2条直接同字面引用**：`0x434774`写、`0x439f0e`读并 `push DWORD PTR [eax+0x3300ccc]`。**这不是别名分析完备**，通过其他寄存器／基址的间接消费者不能据此否认；
- `0x439f0a`—`0x439f2b` 五次入栈顺序为 `ebx`、该`+36`内存值、`0x69`、`ecx`、`eax`。两端没有插入调用、额外改栈或分支；`0x439f2b` 调 `0x453b68`，之后 `add esp,0x14`。因此**在这一静态调用点能确证该数值位于五个栈参数中的第4个**；
- 被调函数 `0x453b68` 在原前96条有限静态指令中确实消费 `[ebp+0x14]`：`0x453bf4`装入`eax`，经不改`eax`的 `0x453bf7`，`0x453bfb`将它写入内部结构 `[esi+8]`。存在 `0x453bcf`对第四参数的条件修改，**不可说所有执行路径保持原始数字不变**；未认证该结构就是实际原SPR、ADRN/REAL绘制器或原服务器物种选择器。

结论：**原客户端本地“名称行末尾数值→相册记录→五参函数→内部字段”的有限静态链成立**，属于新原代码调用证据；不等于真实运行、实际显示、完整图像链、官服已发宠物身份／物种表。沿原 `0x453b68` 后续泛化驱动和通用函数无限扩展，仍不符合有界证据规则，除非取得明确同构建图像选择器或PET主档。

## 既有PET126R完整名字/图形资料仍严格按源分层

大陆5.0原编译名362槽、**305具名／57空**；套用台湾1.0图号公式提出的同CAB SPR匹配为190条具名＋30条空位；124条具名候选的源SPR完整段SHA与台湾1.0零售原源段完全相同。**305不是已发物种，190不是原生selector已证物种，124只是跨版本资产同SHA而非同服或身份合并。** 可复用[已归档362槽目录](../../research/recovered/STONEAGE-PET126R-CN50-PC-ORIGINAL-ALBUM-FULL-362-SLOT-SOURCE-CATALOGUE-R1.json)，并由PET16 `cn50_compiled_album`独立检索，`graphic_number`仍故意为空。

## 七个来源维度及2026六地区差额

[本轮七维与六区机读缺口矩阵](../../research/recovered/STONEAGE-PET126S-PET20-PC-SEVEN-DIMENSION-SOURCE-DELTA-R1.json)继承PET126F真实私人原件回读、PET20七维、PET126R新PC名称及本轮原调用链：**七个维度仍都不是CLOSED**，分别为：①原客户端/版别来源，②原宠物身份/名字/图鉴，③原二维/动作/头像，④属性成长，⑤技能，⑥捕捉/任务/骑乘/融合，⑦资料保管/版权。尤其原2000前期JP/KR同服PET主档，CN/TW等多区真正在服ID与技能成长、发奖原证并未从本地相册源出现。2026 CN/TW/HK_MO/KR/JP/OTHER独立游标仍YTD_PARTIAL_OPEN，不能用大陆5.0代码去证明2026年新发宠、以旧年份游戏资源冒充后期版本首发。

[机器验收凭证](../../research/recovered/STONEAGE-PET126S-CN50-PC-NATIVE-PLUS36-ACCEPTANCE-R1.json)独立钉牢源码SHA、两次既往成功源验、最终run/job、源结果Git blob、七维矩阵Git blob、证据结论和否定条件。原商业EXE/CAB/SPR/REAL/图像**没有进入公开Git**；原代码只做少量来源有界反汇编文本和数值派生。

## 下一项与结项规则

**NEXT PET126T：** 以已保存的原源目录和此七维缺口矩阵作全模块最终来源有界审阅与跨版本/地区重开条件统一；优先合法免费可直接读取的同构建官方PET身份/服端主档/真实投放材料，若无新字节不再继续无界挖普通图像/CRT通用函数。阶段PET保持`SOURCE_BOUNDED_PARTIAL`，2026`NOT_YEAR_AUDITED`，Stage A 7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING、总百分比UNKNOWN。**用户未批准换NPC**，不能暗自切模块或开始新游戏设计。历史 `docs/CURRENT-STATE.md` 2,709,173B／Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 原样保留。
