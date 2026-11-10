# INTEGRATION39｜成年／转生命名目录的原 NPC—事件标志静态联接

来源：重新从 fresh main `d527443507ab66234199e5ab70584af11bafdba9` / tree `0c71823ae26be018fb46e51b3db2f0511d3f5acd` 读取既有 QUEST01、CHAR01、QUEST32 和 MAP09 的 Git 原生 blob。历史 `docs/CURRENT-STATE.md` 为 2,709,173B／`c89e0e33537990aa2132b47c40fef49a985a935c`，仅作完整前缀核验、不改写。

## 具体新增关系

QUEST32 已审计指出 QUEST08–31 的选定脚本中，`my/chengren` 有 1、`my/zhuansheng` 有 4 条尚未构成专项来源关系。本次不重复计作新发现原脚本：以 QUEST01 的原 CREATE 引用 + 原脚本 SHA／TYPE 段，与 CHAR01 原 CREATE 配置块 SHA／楼层／原坐标／图形／模板精确联接。五条来源引用均来自**保存的后期社区混合2.5同一归档**，不是已认证的早期官方服务器部署。

- `my/chengren/chengren.create` 第0块：floor 2000、(54,50)、图形数值16001；确切 `chengren.arg` 原大小429B，2个原 TYPE（ACCEPT／MESSAGE）；前者含一项LV谓词记号及字面 `EndSetFlg:4`，后者有ENDEV记号。仅记录源语法，不认定成人仪式原生触发或完成。
- `my/zhuansheng/zhuans.create` 第0–3块：同 floor 2000 的(47,58)/(48,58)/(49,58)/(50,58)，图形数值100287/100288/100290/100394。各自精确指向 `zhuans1.arg`—`zhuans4.arg`，每份为1个原ACCEPT，条件索引均见LV记号，`EndSetFlg` 分别为39/40/42/46；**并无经证实的等级阈值、重生执行、宠物改变或身份映射**。
- 同一个 `zhuans.create` 还有第4块 `sb_dou`、第5块 `npcgen_petshop`，分别引用`zhuans5.arg`与`jifang.arg`；它们不是上面四份changeevent脚本，不能仅因同创建文件就归为转生事件。第5块 floor32021 亦不可并入2000的五个点。

公开 JSON 保留5个原 CREATE 块SHA、5原脚本SHA/大小/CRC、6个旧TYPE段SHA/条件SHA、逐位置数字、确切函数模板路径及两条负例邻接；这些是**对已验派生原始目录的新增跨表关系**，本轮没有重新取私人原 RAR、解码新增像素、执行旧游戏或取得新的原脚本。MAP09既有691个合格场景中本目标floor2000未取得合格像素入口，不等于相应DAT在私人档案或历史游戏不存在。

## 证据等级与下一项

FACT（对保存的 mixed25 静态原件目录及已验派生索引）：上述5 CREATE→5脚本、6 TYPE、字面标志、图形号、坐标；同目录两条异功能配置必须分开。

OPEN：源文本中LV完整数值门槛、原生事件标志语义、成年/转生操作、玩家／宠物状态效果、原商业运行服务端、早期官方版本归属、2000楼层原图像与执行路径。目录名`chengren/zhuansheng`只是源路径，不等于已证明的玩法机制。无原版权正文、原BIN、图像、商业对白进入公开Git。

交付止点：已有5个可重放精确关系，不继续猜测缺失行为；下一组转其它尚未物化的实际原内容。Stage A 7 PARTIAL＋2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，总完成率未知。
