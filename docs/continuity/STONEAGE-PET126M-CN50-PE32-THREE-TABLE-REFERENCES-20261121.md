# PET126M｜大陆5.0原PC三处编译宠物名称表地址：指令级来源审查

日期：2026-11-21。唯一工作模块PET，范围限定经典原生PC。

**源材料：** 同一个第三方保存大陆5.0 PC原CAB中的 sa_5000.exe (630784B)，完整SHA256 `5dbcc3fa276f9f245fb706bce957e9c3300d870df813889502b789b727e49c97`；编译名称表原362行×28B SHA256 `ba3ad4db233971ee5d9603cdbded6b871f73082445f1ca51d02f0fdf0314d39b`；已验 PET126L 原索引收据。原CAB尚未独立认证为当年官方零售压盘。原程序不执行、不提交公开Git。

**实际重放：** [Actions #44870583521](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/44870583521) 静态GNU binutils Intel格式反汇编、程序整SHA、名称表SHA、三处引用源字节与PE地址映射全部通过；[JSON来源收据](../../research/recovered/STONEAGE-PET126M-CN50-PE32-THREE-NAME-REFERENCE-STATIC-INSTRUCTION-R1.json)。首次测试曾因审计脚本混淆引用发生处VA与名称表目标VA而失败，修复后真实原件重跑及合成测试均success；失败记录保留在Actions。

## 三处真实指令与可验证语义

| 文件偏移 | 原 `.text` 解码指令 | 邻接静态运算 | 可以确认 |
|---|---|---|---|
| `199700` | `lea    esi,[eax+0x482f68]` | `imul eax,eax,0x1c` → `[esi]` 读首整数 → 乘5再乘16 | 28字节名称行，首字段被用作80倍记录索引 |
| `200343` | `mov    esi,DWORD PTR [ecx+0x482f68]` | `imul ecx,ecx,0x1c` → 比较 `esi==-1` → 乘5再左移4位 → `[eax+0x3300cf4]` | 读取名字表首i32，识别空位，以固定80字节步长索引未知内存结构 |
| `214772` | `mov    eax,DWORD PTR [eax+0x482f68]` | `imul eax,eax,0x1c` → 比较 `-1` 空位 | 另一条真实名称首字段读取路径；终端绘图身份未证 |

三处绝对地址在原 `.text` 均被识别为单条线性解码指令。静态线性反汇编不能单独证明指令运行可达，不能把邻接上下文当作完整控制流追踪。

## 边界与下一步

PET126L 已证：原名称表两数字字段都不能直接当成同CAB SPR组号。现在能确证原程序引用了28字节编译名字行的**首整数字段**，其一条路径把该字段乘80用于未知记录的内存寻址；原始 ADRN 磁盘结构也恰好80字节，仅构成候选，**没有验证这个内存表实际就是ADRN、SPR或宠物身份结构**。不把305名字、124台湾相册同槽头像别名、内存记录或静态引用提升为官服实际投放、游戏内技能成长或全球物种种数。

**NEXT PET126N：** 同源界内验证该80字节运行时记录的真实含义，寻求名字表首i32到原SPR/ADRN索引及图形选择的完整可复核链；缺原件时有界止点。继续仅PC宠物模块，不转NPC，不接手游、付费卖盘和私服发宠资料。

本轮新确认官服实发物种0；2026 `NOT_YEAR_AUDITED`，PET `SOURCE_BOUNDED_PARTIAL`且历史整体不完整；Stage A7PARTIAL+2OPEN，Stage B/wiki GATED，R79暂停，总进度百分比UNKNOWN；2709173B原 `docs/CURRENT-STATE.md` blob `c89e0e33537990aa2132b47c40fef49a985a935c` 不修改。
