# INTEGRATION105｜dungeon02 原151配置、144静态传送、7 NPC文本源与64张 DAT 地图资格（2026-11-14）

## 启动、材料查重与来源

本轮依仓库 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` 重读远端 `main` HEAD `86d83465745283bf42ebc4384a455eb3025ddc1f` / tree `dd6f8a5306489340b75e8f3c23017a10bbf97050`、最新提交、Actions（此收据 HEAD 无匹配运行）、开放 PR（0）、README、协议、原生 Git blob `docs/CURRENT-STATE.md` 全部 2,709,173 字节与历史边界/路线。旧历史保持完整。本包不重复 INTEGRATION95 `dungeon00.create`、INTEGRATION96 `dungeon01.create`、INTEGRATION102 `meiro.create`、INTEGRATION103 货运、INTEGRATION104 `31900npc.create`；也不重新做 QUEST09/INTEGRATION56 梦幻洞窟。

发现已有 CHAR01 原 2,205 文件总索引记录 `genout/dungeon02.create` 全151原字节段，却尚未见该文件独立的原传送目标、源地图资格和7原 NPC 文本的限定整合。故此包属于**已有原件新关系核验**，不是首次发现一个官方版本、151个新NPC或151幅新原图。

## 实际原件校验

- 私人后期 mixed25 社区保存 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip`：995,176 字节，SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`，**2,205/2,205** ZIP 成员完整 CRC 成功。
- `npc/genout/dungeon02.create`：**18,174 字节**，SHA256 `bf047be69b5b1d3f6fda836cac4174e69868031b4e3e57f71c2f7da2b02636b6`；151 个实际原 `NPCCREATE` 块，与旧 CHAR01 公有源索引 `a088b61a3212f7049e7793f587123ffb29bebad7` 的逐块范围、SHA、原楼层/出生格绑定；独立逐原字节核首、尾及全文件 SHA。
- 7 条 `npcgen_man` 各自精确指向 7 份真实 `genout/msg_*` 原文件，**720 字节**，逐 SHA 与旧 2,205 源文件索引相符。已实际按 CP950 阅读；内容是有关湖、洞窟提示和其他村民话语的**静态来源**，不能认定为 7 个真正运行中有特定对话选项的官方 NPC。原文字节不进 Git。
- 余下 **144** 条原 `npcgen_warp` 含明确三元组目的地。逐坐标核出 **132 条具有同一 CREATE 文件中精确反向**，**12 条找不到精确反向**，原序号 `0,1,34,35,36,37,38,39,40,136,149,150`；不能将“无反向”说成原服单向设计或者未加载对象。
- 144 条原配置互不相同；源出现65个楼层编号、目标59个，合并仍是65；这些楼层编号不是65张已经复原的原始地图画面。

## 既存地图资格与重要缺件

对照先前实际验真的后期社区 DAT 目录（MAP04 955 文件资格索引 Git blob `1ef8c004179128ea44ffa4fb4259748bc8c83911`）：65个源楼层中64有本目录合格 DAT 的 SHA、宽高；**floor 300 在这955范围中缺同等资格的 DAT**。151个源坐标中**135个**在旧 DAT 宽高界内，另**16个**属于 floor300 的 `NO_QUALIFIED_DAT`；144个目的坐标**128个**在界内，另**16个**指向 floor300；既有资格的坐标**没有越界**。这里的“界内”只证宽高算术，不证碰撞、可通行、触发或与源 NPC 同一实际运行版本。

早先 INTEGRATION104 的 `31902 (9,67)` 与旧15×10 DAT 反例仍原样保留。本轮独立 `dungeon02` 在 `31902` 的原坐标没有新的尺寸矛盾，**不能据此修复 INTEGRATION104 的另一原 CREATE 文件**。

重要关系：旧 INTEGRATION63 的巴那姆壶状态和 QUEST18 火之仪式来源与这7份 NPC 文本所涉的地点/词语可能有内容背景重叠，但**没有同版实走、精确任务 flag 或服务端装载顺序**，不得从文案自动并接为一条已验证任务链。

## 派生交付、隐私及止点

[逐来源段、逐条静态方向与DAT负证](../../research/recovered/STONEAGE-INTEGRATION105-DUNGEON02-151-ORIGINAL-STATIC-ROUTES-R1.json)只含数字、文件路径、原字节区间、SHA和来源资格；不用原 CP950 全文、原商业图像、DAT、NPC 脚本及原客户端。独立公开单测逐行核旧 CHAR01/MAP04 现有公有索引，双向关系、边界、负例、报告统计及源保管指纹；CI 仅公开元数据重放，不代表重新从私人 ZIP 在 Actions 解压。

本包已取得原始脚本内容的实质新整合，**SOURCE_BOUNDED_PARTIAL，不是 GAMEPLAY_VERIFIED**。未得新的 DAT 原字节，未解码新的 RD，未运行游戏、碰撞、传送和 NPC 对话。私有来源已有 Library 保管，本轮不另复制或公开原商业材料。原 `CURRENT-STATE.md` 2,709,173 字节/blob `c89e0e33537990aa2132b47c40fef49a985a935c` 不改；Stage A 7 PARTIAL+2 OPEN，Stage B/wiki GATED，savedata R79 PAUSED_NON_BLOCKING，整体 percent=null。

**NEXT**：若能取得同载体 `300.dat` 的完整原始 DAT 和 SHA，有限重开 floor300 坐标资格与相邻可见2D内容；否则轮换另一个未覆盖且具真原字节/2D候选的宠物、任务或地图家族，不重复展开 `dungeon02` 传送 helper、不凭静态内容声称世界可玩。候选/main GitHub CI、PR和发布须以后续真实 Actions 结果记录，不预支通过。
