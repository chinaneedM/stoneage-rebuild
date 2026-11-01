# O62 — 四村虎训练师 AddPet 源码链与拥有状态止点（2026-11-01）

## 任务与证据范围

从实际远端 main `27ddb5f877f039c84edd7a21a5505657b67be016`、tree `b7b6b8b61cb95e095bd4b5c9532df1a5e7478627` 续接 O61，不以旧对话推断。最新 main 已合并 O61；其同一保管载体中的 `tiger.create`、`m_tiger`、`enemy.txt`、`enemybase.txt` 及四个宠物身份连接均保持原来的 SHA/CRC 证据，不复造原文件、不重下载 361MB 原档、不提交专有字节。本轮 **O62** 只核对一个固定版后代源树中真正匹配 `NEWWARPMAN` + `AddPet` 的调用链及宠物拥有字段，而非制作新客户端或训练模拟器。

- **原脚本已有 FACT（仅保存的社区混合2.5/sa60载体）**：四个 `npcgen_warpman|file:sa60/newbie/m_tiger` 创建引用，12条带 `AddPet:2481..2484` 与 `Event_Now:166` 的有条件授宠脚本；四个 ID 由同载体原 `enemy.ENEMY_ID` 唯一连接到原 `ENEMY_TEMPNO=161..164` 和静态图号 100327..100330。完整数值和正反证见 [O61](STONEAGE-O61-FOUR-TIGER-TRAINERS-20261101.md)。
- **独立后代源码**：`BismarckDD/Stoneage` 固定 Git commit `2f736808ff4361f5429ee919b718c88fabb60346`，其自身树 `b36a900861b8f550f1725a5b43732b4705d2fb`。**该 Git 源树不是上述 mixed25 RAR 内运行过的服务器二进制或 JSS1999/TW1.0 商业原服。**

## 同一固定源树内可逐行定位的连接（FACT：后代源代码静态关系）

| 层次 | 真实原代码位置 | 已观察到的静态行为 |
|---|---|---|
| 编译条件 | [`include/version.h#L99`](https://github.com/BismarckDD/Stoneage/blob/2f736808ff4361f5429ee919b718c88fabb60346/server/gmsv/include/version.h#L99) | 源码定义 `_NEW_WARPMAN`；不能推出实际编译出的发行包启用该定义 |
| 函数登记 | [`function.c#L432-L436`](https://github.com/BismarckDD/Stoneage/blob/2f736808ff4361f5429ee919b718c88fabb60346/server/gmsv/function.c#L432-L436) | `WarpManInit/Talked/WindowTalked` 等映射到 `NPC_WarpMan*` 函数；是否与 O61 同载体配置一起加载，未证 |
| NPC 对话选择 | [`npc_warpman.c#L167-L174`](https://github.com/BismarckDD/Stoneage/blob/2f736808ff4361f5429ee919b718c88fabb60346/server/gmsv/npc/npc_warpman.c#L167-L174)、[L769-L805](https://github.com/BismarckDD/Stoneage/blob/2f736808ff4361f5429ee919b718c88fabb60346/server/gmsv/npc/npc_warpman.c#L769-L805) | `NEWWARPMAN` 进入多段 `TALKEVENT` 选择，按 `FREE` 调用 `NPC_ActionPassCheck`，再呈现 YES/NO |
| 确认后执行 | [`npc_warpman.c#L381-L468`](https://github.com/BismarckDD/Stoneage/blob/2f736808ff4361f5429ee919b718c88fabb60346/server/gmsv/npc/npc_warpman.c#L381-L468) | 窗口确认后选定 `TALKEVENT` 段，调用 `Action_RunDoEventAction`；取消/队伍检查可中断 |
| 发宠指令分发 | [`npc_eventaction.c#L459-L480`](https://github.com/BismarckDD/Stoneage/blob/2f736808ff4361f5429ee919b718c88fabb60346/server/gmsv/npc/npc_eventaction.c#L459-L480) | `AddPet` 精确指向 **`NPC_ActionAddPet`**；后面的 `Event_Now` 精确指向 `NPC_ActionSetNow`。不是 `npc_exchangeman.c` 的 `GetPet` 处理分支 |
| ID、空槽及创建 | [`npc_eventaction.c#L2054-L2117`](https://github.com/BismarckDD/Stoneage/blob/2f736808ff4361f5429ee919b718c88fabb60346/server/gmsv/npc/npc_eventaction.c#L2054-L2117) | 先检查宠物栏空槽，再按 `ENEMY_ID` 查敌人实例，成功匹配才调用 `ENEMY_createPetFromEnemyIndex` |
| 宠物拥有状态 | [`char/enemy.c#L1359-L1374`](https://github.com/BismarckDD/Stoneage/blob/2f736808ff4361f5429ee919b718c88fabb60346/server/gmsv/char/enemy.c#L1359-L1374)、[L1447-L1499](https://github.com/BismarckDD/Stoneage/blob/2f736808ff4361f5429ee919b718c88fabb60346/server/gmsv/char/enemy.c#L1447-L1499) | 创建前检查模板、玩家空栏等，建立 `CHAR_PETID` 与 `CHAR_PETENEMYID`，调用 `CHAR_setCharPet`，填写 `CHAR_WORKPLAYERINDEX`、`CHAR_OWNERCDKEY`、`CHAR_OWNERCHARANAME`；这是源代码中内存对象/归属字段的连接，不是数据库存档成功 |

已逐源文件定位并以固定 Git blob 锁定（按上述路径顺序）：`version.h=cd68519a68a90b1123f298e16afa00d5798cd844`；`function.c=3a70d4f59dd2f0ccc42d7e00380129f01d8de04b`；`npc_warpman.c=f0e6d737cbc5ec7039e5ca32dd717159dcb93e28`；`npc_eventaction.c=a89b744394079cc476e7e87f6e353d66208e0150`；`char/enemy.c=0bf37ddbc4b923059c7202ad4327ee81f9fe2def`；另证 `npc_exchangeman.c=019a9578b122773df90442719ece50ad79fbe1b4` 中的 **GetPet** 是另一接口，不能代替这一条 AddPet 链。

## 新识别的非原子事务风险（SOURCE-QUALIFIED，不是现场事故）

`NPC_ActionAddPet` 遇宠物栏满会返回 `FALSE`；遇找不到的 `ENEMY_ID` 走 `continue`，最后仍可返回 `TRUE`；创建函数返回无效结果后的部分路径也走 `continue`，而后续 `Event_Now` 在同一个 `Action_RunDoEventAction` 中位于 `AddPet` 之后。**因此不能假设「事件166已设置」必然等于「宠物已经成功归属」；源码不能保证授宠与事件标记是原子事务。** 此为固定后代源码层的异常路径判断，未运行服务端复现实验；O61 的 2481—2484 在静态表中各有唯一匹配，不属于“查无ID”的普通输入。

## 当前结论及下一止点

- **本轮新增**：将 O61 的 `AddPet` 明确接到适用的 `NEWWARPMAN → Action_RunDoEventAction → NPC_ActionAddPet → ENEMY_createPetFromEnemyIndex → CHAR_setCharPet` **后代源码级条件路径**；明确 `GetPet` 路径并不相同；发现不能从事件号推断成功领宠的负面边界。
- **没有证成**：同载体原服务器可执行身份；具体编译宏及 `npcgen_warpman` 模板部署；真实玩家触发/拥有宠物、原服持久化ACK、下线重登、骑乘解锁；JSS1999/TW1 原版规则、四村真实可玩画面。缺必要同版二进制/日志时，停止深挖，不新增发宠模拟器。
- **最高 NEXT O63（材料优先）**：优先从已保管原始客户端提取 O61 四种宠物图号 100327—100330 的准确 ADRN/REAL 像素候选并作可见图像观察，或选择同版可验证的原宠物入栏/骑乘资料。若无已认证的直接材料，记录缺口并切换实际游戏内容包；**不要继续沿着后代 C 函数追求无穷 helper**。

本条为日期加法补充，保留完整 `docs/CURRENT-STATE.md` 原 blob `20050acf279a01555ab06a381dfcdc936bd381a6`（2,708,031B）不修改，不推翻 O61 的早期误判及后续订正。Stage A=7 PARTIAL+2 OPEN；Stage B/wiki=GATED；R79=PAUSED_NON_BLOCKING；overall_percent=null，尚未进入可操作的原游戏世界。